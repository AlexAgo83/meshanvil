#!/usr/bin/env python3
"""The smallest thing that fails if the host logic breaks. No Blender, no framework.

Covers what is easy to get quietly wrong: identity allocation under collision, parameter
resolution, the bounding-box delta, and the refusals that must leave work/ops untouched.
"""
import http.client, json, os, shutil, sys, tempfile, threading, time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from meshanvil import doctor, engines, i18n, logics_bridge, manifests, prune, runner, viewer  # noqa: E402
from meshanvil_engine.report import bbox_delta     # noqa: E402


def check_parameters():
    manifest = {"operation": "x", "params": [
        {"name": "ratio", "type": "float", "default": 2.5},
        {"name": "fix", "type": "bool", "default": False}]}
    assert manifests.resolve(manifest, {}) == {"ratio": 2.5, "fix": False}
    assert manifests.resolve(manifest, {"ratio": "3"}) == {"ratio": 3.0, "fix": False}
    assert manifests.resolve(manifest, {"fix": "true"})["fix"] is True
    try:
        manifests.resolve(manifest, {"voxel": "3"})
        raise AssertionError("an unknown parameter must be refused")
    except KeyError:
        pass
    try:
        manifests.resolve(manifest, {"ratio": "nope"})
        raise AssertionError("an invalid parameter must be refused")
    except KeyError:
        pass


def check_identity(tmp: Path):
    (tmp / "work" / "ops").mkdir(parents=True)
    first, path_a = runner.allocate(tmp, "op", None)
    assert first == "001", first
    second, _ = runner.allocate(tmp, "op", None)
    assert second == "002", second          # a claimed identity is never handed out twice
    path_a.write_text(json.dumps({"id": "001", "links": {"parent": None}}), encoding="utf-8")
    child, path_c = runner.allocate(tmp, "op", "001")
    assert child == "003", child            # first child keeps a bare ordinal
    path_c.write_text(json.dumps({"id": child, "links": {"parent": "001"}}), encoding="utf-8")
    sibling, path_s = runner.allocate(tmp, "op", "001")
    assert sibling == "003a", sibling       # a second child of the same parent takes a letter
    path_s.write_text(json.dumps({"id": sibling, "links": {"parent": "001"}}), encoding="utf-8")
    other, _ = runner.allocate(tmp, "other", "001")
    assert other == "003b", other           # an identity is taken whatever operation wrote it


def check_parent(tmp: Path):
    report = tmp / "work" / "ops" / "010_op.json"
    report.write_text(json.dumps({"id": "010", "output": {"sha256": "abc"}}), encoding="utf-8")
    assert runner.resolve_parent(tmp, "abc") == "010"
    assert runner.resolve_parent(tmp, "nope") is None


def check_projects(tmp: Path):
    """Two projects, and nothing crosses between them.

    Every namespace here reads whatever directory it is handed, so isolation is a property of
    which root each call receives. That is exactly what regresses the first time a path
    constant is reached for directly, and it is invisible until a second project exists.
    """
    from meshanvil import paths

    alpha, beta = tmp / "alpha", tmp / "beta"
    for project in (alpha, beta):
        root, fresh = paths.initialise(project)
        assert fresh and (root / paths.MARKER).is_dir(), root

    assert paths.resolve(alpha)[0] == alpha.resolve(), paths.resolve(alpha)
    assert paths.resolve(alpha)[1] == paths.BY_MARKER
    # A directory under a project belongs to it; the walk-up is what makes that true.
    inner = alpha / "work" / "out"
    assert paths.resolve(inner)[0] == alpha.resolve(), paths.resolve(inner)
    # Nothing above either of them is a project, so an unmarked directory is the installation.
    assert paths.resolve(tmp)[1] == paths.BY_INSTALLATION, paths.resolve(tmp)

    # Identity restarts per project rather than continuing another one's numbering.
    first_a, path_a = runner.allocate(alpha, "op", None)
    assert first_a == "001", first_a
    path_a.write_text(json.dumps({"id": "001", "links": {"parent": None},
                                  "output": {"sha256": "shared"}}), encoding="utf-8")
    first_b, path_b = runner.allocate(beta, "op", None)
    assert first_b == "001", f"beta continued alpha's numbering: {first_b}"
    path_b.write_text(json.dumps({"id": "001", "links": {"parent": None}}), encoding="utf-8")

    # Two projects opened from the same source share a fingerprint and must still not be
    # linked: parentage is resolved inside a project, never across the disk.
    assert runner.resolve_parent(alpha, "shared") == "001"
    assert runner.resolve_parent(beta, "shared") is None, "a parent was resolved across projects"

    # Retention counts one project's reports, not another's activity.
    dropped, _ = prune.run(beta, 0, dry_run=True)
    assert all(alpha not in path.parents for path, _ in dropped), dropped

    code = paths.code_root()
    assert code != alpha.resolve() and (code / "meshanvil" / "paths.py").is_file(), code

    # The neighbourhood a page may offer. The active root is always in it, reports or not,
    # because that is where a run would land. An unmarked directory sitting next to projects
    # offers none of them: it would show reports nobody is about to write to.
    assert paths.projects(alpha)[0] == alpha.resolve(), paths.projects(alpha)
    assert beta.resolve() in paths.projects(alpha), paths.projects(alpha)
    stranger = tmp / "stranger"
    stranger.mkdir()
    assert paths.projects(stranger) == [stranger.resolve()], paths.projects(stranger)


def check_bbox_delta():
    before = {"bbox_mm": {"min": [-268.0, -247.2, 52.5], "max": [4.4, 127.5, 194.8]}}
    after = {"bbox_mm": {"min": [-268.0, 22.5, 52.5], "max": [-205.1, 127.5, 157.5]}}
    delta = bbox_delta(before, after)
    assert delta["axes_moved"] == ["X", "Y", "Z"], delta
    same = bbox_delta(before, before)
    assert same["axes_moved"] == [], same   # an unchanged box must report no movement
    assert bbox_delta({}, after) is None


def check_refusals():
    for arguments in (["run", "nope", "README.md"],
                      ["run", "scan_defects", "does-not-exist.blend"]):
        from meshanvil import cli
        assert cli.main(arguments) == runner.EXIT_REFUSED, arguments


def check_i18n():
    previous = os.environ.get("MESHANVIL_LANG")
    original_locale, original_catalogue = i18n.locale.getlocale, i18n.catalogue
    try:
        os.environ["MESHANVIL_LANG"] = "fr_FR"
        assert i18n.language() == "fr"
        os.environ.pop("MESHANVIL_LANG")
        i18n.locale.getlocale = lambda: ("fr_FR", "UTF-8")
        assert i18n.language() == "fr"
        os.environ["MESHANVIL_LANG"] = "fr"
        i18n.catalogue = lambda lang: {"fallback": "English"} if lang == "en" else {}
        key = "fallback"
        assert i18n.t(key) == "English"
    finally:
        i18n.locale.getlocale, i18n.catalogue = original_locale, original_catalogue
        if previous is None:
            os.environ.pop("MESHANVIL_LANG", None)
        else:
            os.environ["MESHANVIL_LANG"] = previous


def check_doctor(tmp: Path):
    binary = tmp / "blender"
    binary.write_text("", encoding="utf-8")
    original_find, original_version = engines.find, engines.version
    calls = []
    try:
        engines.find = lambda name: binary if name == "blender" else (_ for _ in ()).throw(engines.EngineMissing())
        engines.version = lambda path: (calls.append(path) or ("5.2.0", ""))
        result = doctor.check(tmp)
        assert result["ok"] is True
        assert [item["state"] for item in result["requirements"]] == ["found", "missing", "found"]
        assert [item["class"] for item in result["requirements"]] == ["required", "optional", "required"]
        assert (tmp / "work" / "doctor.json").is_file()
        assert doctor.check(tmp)["next"] is None and len(calls) == 1
    finally:
        engines.find, engines.version = original_find, original_version


def check_engine_floor():
    try:
        engines.check_floor("blender", "4.1.0")
        raise AssertionError("an old Blender must be refused")
    except engines.EngineMissing as error:
        assert "bpy.ops.wm.stl_export" in str(error) and "MESHANVIL_BLENDER" in str(error)
    assert "MESHANVIL_BLENDER" in engines.fix_command("blender")


def check_wsl_boundary(tmp: Path):
    original_wsl, original_run = engines.in_wsl, engines.subprocess.run
    try:
        engines.in_wsl = lambda: True
        engines.subprocess.run = lambda *args, **kwargs: SimpleNamespace(stdout="C:\\wsl.localhost\\Ubuntu\\tmp\\job.json\n")
        assert engines.for_engine(tmp / "job.json", Path("Blender.exe")).startswith("C:\\wsl.localhost")
    finally:
        engines.in_wsl, engines.subprocess.run = original_wsl, original_run


def check_doctor_exit_code():
    from meshanvil import cli
    original = doctor.check
    try:
        doctor.check = lambda root: {"ok": False, "requirements": []}
        assert cli.main(["doctor"]) == runner.EXIT_REFUSED
    finally:
        doctor.check = original


def check_viewer_start(tmp: Path):
    root = tmp / "viewer-start"
    root.mkdir()
    (root / "viewer").symlink_to(ROOT / "viewer", target_is_directory=True)
    (root / "work").mkdir()
    (root / "work" / "doctor.json").write_text(
        json.dumps({"ok": False, "requirements": [{"name": "blender", "state": "missing"}]}),
        encoding="utf-8")
    page = viewer.build(root)
    payload = json.loads((page.parent / "data.js").read_text(encoding="utf-8").split("= ", 1)[1].rstrip(";\n"))
    assert payload["reports"] == [] and payload["doctor"]["ok"] is False and not payload["ops_exists"]


def check_run_endpoint(tmp: Path):
    """adr_007: token, closed command set, single-flight -- exercised over a real socket
    against the real handler, with subprocess.run patched so no Blender and no bin/meshanvil
    process is needed."""
    root = tmp / "run-endpoint"
    (root / "work" / "ops").mkdir(parents=True)
    token = "selfcheck-token"
    server = viewer.make_server(root, root, token)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def post(headers, body):
        conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        conn.request("POST", "/run", body=json.dumps(body), headers=headers)
        response = conn.getresponse()
        status = response.status
        response.read()
        conn.close()
        return status

    original_run = viewer.subprocess.run
    try:
        assert post({"X-Meshanvil-Token": "wrong"}, {"command": "list"}) == 401, "a bad token was accepted"
        assert post({}, {"command": "list"}) == 401, "a missing token was accepted"
        assert post({"X-Meshanvil-Token": token}, {"command": "rm -rf /"}) == 400, "a command outside the closed set was accepted"

        viewer.subprocess.run = lambda *a, **k: SimpleNamespace(stdout="ok", stderr="", returncode=0)
        assert post({"X-Meshanvil-Token": token}, {"command": "list"}) == 200, "a valid request was refused"

        released = threading.Event()

        def slow_run(*a, **k):
            released.wait(timeout=2)
            return SimpleNamespace(stdout="ok", stderr="", returncode=0)
        viewer.subprocess.run = slow_run

        statuses = []

        def call():
            statuses.append(post({"X-Meshanvil-Token": token}, {"command": "doctor"}))
        first = threading.Thread(target=call)
        first.start()
        time.sleep(0.2)   # let the first request take the lock before the second arrives
        second_status = post({"X-Meshanvil-Token": token}, {"command": "doctor"})
        released.set()
        first.join(timeout=2)
        assert second_status == 409, "a concurrent request was queued instead of refused"
        assert statuses == [200], "the in-flight request did not complete normally"
    finally:
        viewer.subprocess.run = original_run
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def check_viewer_comparison_layout():
    css = (ROOT / "viewer" / "viewer.css").read_text(encoding="utf-8")
    script = (ROOT / "viewer" / "viewer.js").read_text(encoding="utf-8")
    page = (ROOT / "viewer" / "index.html").read_text(encoding="utf-8")
    assert ".colstack > .editor:first-child{flex:1}" in css
    assert ".compare-after{clip-path:" in css
    assert 'compare.style.setProperty("--wipe", `${wipe}%`)' in script
    assert 'data-workspace="compare"' in page and "function selectWorkspace" in script
    assert 'button[data-workspace]' in script
    assert 'workspace === "runbooks"' in script
    assert 'data-section-goto="input"' in page and 'function jumpReportSection' in script
    assert 'DATA.runbooks || []).filter' in script
    assert 'class="splashcols"' in page and "function renderSplash" in script
    assert ".rbbody" in css and ".wipelabel" in css
    # adr_007's one exception: fetch exists only for the run endpoint, gated by SERVED, and
    # SERVED itself is false whenever the page has no server to reach.
    assert 'fetch(`${location.origin}/run`' in script, "the run endpoint call is missing"
    assert "const SERVED = location.protocol" in script and "if (run && SERVED)" in script


def check_logics_bridge():
    original_which, original_run = logics_bridge.shutil.which, logics_bridge.subprocess.run
    try:
        logics_bridge.shutil.which = lambda name: None
        assert logics_bridge.call("sync", "read-doc", "missing") == (None, "unavailable")
        logics_bridge.shutil.which = lambda name: "/usr/bin/logics-manager"
        logics_bridge.subprocess.run = lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout='{"ref":"task_1"}')
        assert logics_bridge.call("sync", "read-doc", "task_1")[0]["ref"] == "task_1"
    finally:
        logics_bridge.shutil.which, logics_bridge.subprocess.run = original_which, original_run


def check_prune(tmp: Path):
    root = tmp / "prune"; (root / "work" / "ops").mkdir(parents=True)
    outputs = root / "work" / "out"; outputs.mkdir()
    for index in range(2):
        artefact = outputs / f"{index}.blend"; artefact.write_bytes(b"x" * (index + 1))
        report = {"id": f"00{index}", "chain": "001", "output": {"path": str(artefact), "state": "present"}, "links": {"docs": []}}
        (root / "work" / "ops" / f"00{index}_op.json").write_text(json.dumps(report), encoding="utf-8")
    planned, freed = prune.run(root, 1, True)
    assert len(planned) == 1 and freed == 1 and (outputs / "0.blend").is_file()
    prune.run(root, 1, False)
    changed = json.loads((root / "work" / "ops" / "000_op.json").read_text(encoding="utf-8"))
    assert not (outputs / "0.blend").exists() and changed["output"]["state"] == "pruned"


def check_target_lock(tmp: Path):
    root = tmp / "lock"
    lock = runner.claim_target(root, "same-source")
    try:
        try:
            runner.claim_target(root, "same-source")
            raise AssertionError("a second writer must be refused")
        except runner.Refused:
            pass
    finally:
        lock.unlink()
    assert runner.claim_target(root, "same-source").is_file()


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="meshanvil-selfcheck-"))
    try:
        check_parameters()
        check_identity(tmp)
        check_parent(tmp)
        check_projects(tmp)
        check_bbox_delta()
        check_refusals()
        check_i18n()
        check_doctor(tmp)
        check_engine_floor()
        check_wsl_boundary(tmp)
        check_doctor_exit_code()
        check_viewer_start(tmp)
        check_run_endpoint(tmp)
        check_viewer_comparison_layout()
        check_logics_bridge()
        check_prune(tmp)
        check_target_lock(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selfcheck: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
