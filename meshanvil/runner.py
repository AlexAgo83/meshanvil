"""Run one operation: allocate an identity, write a job, launch the engine, read the report back.

Nothing is parsed out of the engine's stdout. The report is a file, which is what makes the
boundary survive a crash, a Windows binary called from WSL, and two interpreters that share
no import. See adr_004 and adr_005.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

from . import SCHEMA_VERSION, VERSION, doctor, engines, logics_bridge, manifests
from .i18n import t

OPS = "work/ops"
RUNS = "work/ops/.run"
JOBS = "work/ops/.job"

EXIT_OK, EXIT_FAILED, EXIT_REFUSED, EXIT_NO_REPORT = 0, 1, 2, 3


class Refused(Exception):
    """The command will not run. Exit code 2, nothing written, nothing touched."""


def fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def allocate(root: Path, name: str, parent: str | None) -> tuple[str, Path]:
    """Identity by exclusive creation: the filesystem arbitrates, so two runners cannot collide.

    A parent that already has a child makes this a sibling, which takes a letter on the same
    ordinal rather than a new one.
    """
    ops = root / OPS
    ops.mkdir(parents=True, exist_ok=True)
    existing = sorted(ops.glob("*.json"))
    siblings = [p for p in existing if parent and _parent_of(p) == parent]
    if siblings:
        ordinal = siblings[0].name.split("_")[0].rstrip("abcdefghijklmnopqrstuvwxyz")
        for letter in "abcdefghijklmnopqrstuvwxyz":
            identity = f"{ordinal}{letter}"
            path = ops / f"{identity}_{name}.json"
            if _claim(path):
                return identity, path
    number = 1 + max((int(p.name.split("_")[0].rstrip("abcdefghijklmnopqrstuvwxyz"))
                      for p in existing), default=0)
    while True:
        identity = f"{number:03d}"
        path = ops / f"{identity}_{name}.json"
        if _claim(path):
            return identity, path
        number += 1


def _claim(path: Path) -> bool:
    """An identity is taken as soon as any report carries it, whatever operation wrote it.

    O_EXCL alone only makes the filename unique, and two operations with different names would
    both have claimed 003a.
    """
    identity = path.name.split("_", 1)[0]
    if any(path.parent.glob(f"{identity}_*.json")):
        return False
    try:
        os.close(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except FileExistsError:
        return False


def _parent_of(report: Path) -> str | None:
    try:
        return json.loads(report.read_text(encoding="utf-8")).get("links", {}).get("parent")
    except (json.JSONDecodeError, OSError):
        return None


def resolve_parent(root: Path, digest: str) -> str | None:
    """The parent is the report whose output has the fingerprint of this operation's input."""
    latest = None
    for path in sorted((root / OPS).glob("*.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if (report.get("output") or {}).get("sha256") == digest:
            latest = report.get("id")
    return latest


STALE_AFTER = 60.0


def watch(process: subprocess.Popen, progress: Path, poll: float = 5.0) -> None:
    """A long operation proves it is alive by touching its progress file.

    There is no default timeout -- a legitimate pass can take an hour -- but a heartbeat that
    stops moving is worth saying out loud, because silence is what makes a caller kill a run
    that was still working. See adr_005.
    """
    said = False
    while process.poll() is None:
        time.sleep(poll)
        beat = progress.stat().st_mtime if progress.exists() else None
        quiet = time.time() - (beat or 0)
        if beat and quiet > STALE_AFTER and not said:
            print(t("run.no_heartbeat", seconds=f"{quiet:.0f}"), file=sys.stderr)
            said = True
        elif beat and quiet <= STALE_AFTER:
            said = False


def run(operation: str, target: str, params: dict[str, str], parent: str | None = None,
        evidence: str | None = None) -> int:
    declared_parent = parent
    root = manifests.root()
    known = manifests.discover()
    if operation not in known:
        raise Refused(t("run.unknown_operation", name=operation))
    manifest = known[operation]
    source = Path(target).resolve()
    if not source.is_file():
        raise Refused(t("run.no_such_file", path=target))
    if (root / "work" / "in") in source.parents and manifest["engine"] != "freecad":
        raise Refused(t("run.source_is_read_only", path=target))
    if doctor.work(root)["state"] != "found":
        raise Refused(t("run.work_unavailable", path=root / "work"))
    values = manifests.resolve(manifest, params)   # validated before an identity is claimed:
    binary = engines.find(manifest["engine"])       # a refusal must leave work/ops untouched
    number, build = engines.version(binary)
    engines.check_floor(manifest["engine"], number)

    digest = fingerprint(source)
    parent = parent or resolve_parent(root, digest)
    identity, report_path = allocate(root, operation, parent)
    (root / RUNS).mkdir(parents=True, exist_ok=True)
    (root / JOBS).mkdir(parents=True, exist_ok=True)

    job = {
        "schema_version": SCHEMA_VERSION,
        "id": identity,
        "root": str(root),
        "operation": operation,
        "kind": manifest["kind"],
        "engine": manifest["engine"],
        "script": manifest["script"],
        "target": str(source),
        "params": values,
        "input_sha256": digest,
        "parent": parent,
        "parent_source": declared_parent and "declared" or (parent and "fingerprint" or None),
        "report": str(report_path),
        "progress": str(root / RUNS / f"{identity}.progress"),
        "tool": {"meshanvil": VERSION, "engine_version": number, "engine_build": build,
                 "platform": f"{sys.platform}", "host_python": sys.version.split()[0]},
    }
    job_path = root / JOBS / f"{identity}.json"
    job_path.write_text(json.dumps(job, indent=1) + "\n", encoding="utf-8")

    if manifest["engine"] == "freecad":
        command = [str(binary), "-c", engines.for_engine(root / manifest["script"], binary),
                   "--", "--job", engines.for_engine(job_path, binary)]
    else:
        command = [str(binary), "-b", engines.for_engine(source, binary),
                   "-P", engines.for_engine(root / manifest["script"], binary),
                   "--", "--job", engines.for_engine(job_path, binary)]
    started = time.time()
    try:
        watch(subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
              root / RUNS / f"{identity}.progress")
    except BaseException:
        report_path.unlink(missing_ok=True)   # a claimed identity with no run is not a report
        raise

    if report_path.stat().st_size == 0:
        print(t("run.no_report", seconds=f"{time.time() - started:.0f}",
                job=job_path.relative_to(root)), file=sys.stderr)
        return EXIT_NO_REPORT
    report = json.loads(report_path.read_text(encoding="utf-8"))
    output = report.get("output") or {}
    if output.get("path") and not output.get("sha256"):
        # The host completes the record before the report is final: it already hashes, and the
        # engine has no reason to re-read a file it just wrote. Nothing else is ever edited.
        output["sha256"] = fingerprint(Path(output["path"]))
        report_path.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    job_path.unlink(missing_ok=True)
    (root / RUNS / f"{identity}.progress").unlink(missing_ok=True)
    print(report_path.relative_to(root))
    if report.get("status") != "ok":
        if evidence:
            print(t("bridge.evidence_failed"), file=sys.stderr)
        return EXIT_FAILED
    if evidence:
        command = "meshanvil run " + operation + " " + target + " ".join(
            f" --set {key}={value}" for key, value in params.items())
        error = logics_bridge.evidence(evidence, report_path, report, command)
        if error:
            message = (t("bridge.evidence_unavailable") if error == "unavailable"
                       else t("bridge.evidence_error", reason=error))
            print(message, file=sys.stderr)
    return EXIT_OK
