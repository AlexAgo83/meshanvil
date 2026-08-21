"""Optional JSON boundary to Logics; meshanvil never imports its Python package."""
from __future__ import annotations
import json, shutil, subprocess
from pathlib import Path


def call(*args: str) -> tuple[dict | None, str | None]:
    command = shutil.which("logics-manager")
    if not command:
        return None, "unavailable"
    try:
        done = subprocess.run([command, *args, "--format", "json"], text=True,
                              capture_output=True, check=False, timeout=15)
        if done.returncode:
            return None, done.stderr.strip() or done.stdout.strip() or "failed"
        return json.loads(done.stdout), None
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        return None, str(error)


def evidence(ref: str, report_path: Path, report: dict, command: str) -> str | None:
    task, separator, ac = ref.partition(":")
    if not separator or not task or not ac:
        return "invalid"
    measured = report.get("measured") or report.get("after") or {}
    facts = ", ".join(f"{key}={value}" for key, value in measured.items()
                      if key in {"objects", "vertices", "faces", "shells", "volume_cm3"}
                      and value is not None)
    summary = f"{report.get('operation')} succeeded" + (f" ({facts})" if facts else "")
    _, error = call("flow", "evidence", "add", task, "--ac", ac, "--summary", summary,
                    "--command", command, "--result", str(report_path))
    return error


def documents(refs: set[str]) -> dict[str, dict]:
    result = {}
    for ref in refs:
        value, error = call("sync", "read-doc", ref)
        result[ref] = value if value else {"ref": ref, "missing": True, "error": error}
    return result


def runbook(root: Path, chain: str) -> tuple[str | None, str | None]:
    reports = []
    for path in sorted((root / "work" / "ops").glob("*.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if report.get("chain") == chain:
            reports.append(report)
    if not reports:
        return None, "chain_missing"
    result, error = call("flow", "companion", "runbook", "--title", f"Chain {chain}")
    if error:
        return None, error
    path = root / result["path"]
    facts = "\n".join(f"- `{report['id']}` `{report['operation']}` ({report['status']}): "
                      f"params `{json.dumps(report.get('params', {}), sort_keys=True)}`; "
                      f"measurements `{json.dumps(report.get('measured') or report.get('after') or {}, sort_keys=True)}`"
                      for report in reports)
    text = path.read_text(encoding="utf-8")
    replacements = {
        "(not yet verified)": "Report facts captured; human procedure not yet verified",
        "(describe when this runbook applies)": f"Use this draft to turn chain `{chain}` into a reviewed operating procedure.",
        "(list what must be true or available before running this)": "The source, Blender and the report chain must be available locally.",
        "(list the steps to follow)": "Complete the human procedure from the captured report facts below; this scaffold does not claim one is verified.",
        "(describe how to confirm the procedure worked)": "Compare the next run against the measurements and failure recorded below.",
        "(optional: describe how to undo this procedure)": "Keep the source unchanged and discard only generated work outputs when the procedure is revised.",
        "(none yet)": "Not linked by this report chain.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text + "\n## Report facts\n" + facts + "\n", encoding="utf-8")
    return str(path.relative_to(root)), None
