#!/usr/bin/env python3
"""The smallest thing that fails if the host logic breaks. No Blender, no framework.

Covers what is easy to get quietly wrong: identity allocation under collision, parameter
resolution, the bounding-box delta, and the refusals that must leave work/ops untouched.
"""
import contextlib, http.client, io, json, os, shutil, sys, tempfile, threading, time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from meshanvil import demo, doctor, engines, i18n, logics_bridge, manifests, prune, reports, runner, schemas, status, viewer, viewer_server  # noqa: E402
from meshanvil.viewer_routes import events as viewer_events  # noqa: E402
from meshanvil.viewer_routes import run as viewer_run  # noqa: E402
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
    # Nothing above it is a project, so the named directory itself is the fallback project.
    assert paths.resolve(tmp) == (tmp.resolve(), paths.BY_CWD), paths.resolve(tmp)

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

    assets = paths.asset_root(".")
    assert assets != alpha.resolve() and (assets / "meshanvil" / "paths.py").is_file(), assets

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


def check_captured_output_is_utf8():
    """Captured output is UTF-8, and a mark outside the host codepage does not kill the command.

    Windows encodes a pipe with the ANSI codepage: an accent arrives as mojibake and a glyph
    like the viewer's check mark raises UnicodeEncodeError. The catalogues are shared between
    the page and the terminal, so nothing but this stops one reaching a printed string.
    """
    from meshanvil import cli

    class Pipe(io.TextIOWrapper):
        pass

    buffer = io.BytesIO()
    stream = Pipe(buffer, encoding="cp1252", errors="strict", newline="")
    original = sys.stdout
    try:
        sys.stdout = stream
        cli.speak_utf8()
        assert stream.encoding.lower().replace("-", "") == "utf8", stream.encoding
        print("accent \u00e9 and mark \u2713")
        stream.flush()
    finally:
        sys.stdout = original
    assert "\u2713" in buffer.getvalue().decode("utf-8"), buffer.getvalue()


def check_cli_welcome():
    from meshanvil import cli
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        assert cli.main([]) == runner.EXIT_OK
    text = stream.getvalue()
    assert "meshanvil" in text and "meshanvil view" in text and "--help" in text, text
    assert "error:" not in text.lower(), text


def check_cli_json(tmp: Path):
    from meshanvil import cli, paths
    original = (cli.manifests.discover, cli.paths.resolve, cli.paths.work_root,
                cli.doctor.check, cli.prune.run, cli.runner.run)
    project = tmp / "cli-json"; project.mkdir()
    try:
        cli.manifests.discover = lambda: {"op": {"operation": "op", "engine": "blender", "kind": "mesh"}}
        cli.paths.resolve = lambda: (project, paths.BY_CWD)
        cli.paths.work_root = lambda: project
        cli.doctor.check = lambda root: {"ok": True, "requirements": []}
        cli.prune.run = lambda root, keep, dry_run: ([(root / "work" / "out.blend", 12)], 12)
        def run_ok(*args, **kwargs):
            report = project / "work" / "ops" / "001_op.json"
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps({"id": "001", "operation": "op", "status": "ok"}),
                              encoding="utf-8")
            print("work/ops/001_op.json")
            return runner.EXIT_OK

        cli.runner.run = run_ok

        for arguments, key in ((["list", "--json"], "operations"),
                               (["doctor", "--json"], "doctor"),
                               (["prune", "--dry-run", "--json"], "artefacts"),
                               (["run", "op", "source.blend", "--json"], "report_path")):
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                assert cli.main(arguments) == runner.EXIT_OK, arguments
            data = json.loads(stream.getvalue())
            assert data["ok"] is True and key in data, data
        cli.runner.run = lambda *args, **kwargs: (_ for _ in ()).throw(runner.Refused("nope", "unknown_operation"))
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["run", "op", "source.blend", "--json"]) == runner.EXIT_REFUSED
        data = json.loads(stream.getvalue())
        assert data["error"] == {"code": "unknown_operation", "message": "nope"}, data
        for arguments, code, fake in (
            (["run", "op", "source.blend", "--set", "bad", "--json"], "malformed_set", None),
            (["run", "op", "source.blend", "--json"], "engine_missing", engines.EngineMissing("missing")),
            (["run", "op", "source.blend", "--json"], "invalid_parameter", KeyError("bad parameter")),
        ):
            if fake is not None:
                cli.runner.run = lambda *args, error=fake, **kwargs: (_ for _ in ()).throw(error)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                assert cli.main(arguments) == runner.EXIT_REFUSED
            assert json.loads(stream.getvalue())["error"]["code"] == code
    finally:
        (cli.manifests.discover, cli.paths.resolve, cli.paths.work_root,
         cli.doctor.check, cli.prune.run, cli.runner.run) = original


def check_cli_reports(tmp: Path):
    from meshanvil import cli
    root = tmp / "reports-cli"; ops = root / "work" / "ops"; ops.mkdir(parents=True)
    (ops / "001_scan.json").write_text(json.dumps({
        "id": "001", "operation": "scan", "status": "ok",
        "input": {"path": "work/out/source.blend"},
        "output": {"path": "work/out/result.blend", "state": "present"},
        "created_at": "2026-08-23T00:00:00Z",
    }), encoding="utf-8")
    (ops / "002_bad.json").write_text("{", encoding="utf-8")
    (ops / "003a_scan.json").write_text(json.dumps({"id": "003a", "operation": "scan", "status": "failed"}),
                                        encoding="utf-8")
    original = cli.paths.work_root
    try:
        cli.paths.work_root = lambda: root
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["reports", "--json"]) == runner.EXIT_OK
        listed = json.loads(stream.getvalue())
        assert listed["ok"] is True and len(listed["reports"]) == 3
        assert listed["reports"][1]["warning"]["code"] == "malformed_report"

        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["reports", "--latest", "--json"]) == runner.EXIT_OK
        assert json.loads(stream.getvalue())["report"]["id"] == "003a"

        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["reports", "001", "--json"]) == runner.EXIT_OK
        assert json.loads(stream.getvalue())["report_path"] == "work/ops/001_scan.json"

        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["reports", "00", "--json"]) == runner.EXIT_REFUSED
        assert json.loads(stream.getvalue())["error"]["code"] == "ambiguous_report_id"
    finally:
        cli.paths.work_root = original


def check_cli_status(tmp: Path):
    from meshanvil import cli, paths
    root = tmp / "status-cli"; (root / paths.MARKER).mkdir(parents=True); (root / "work").mkdir()
    binary = tmp / "blender"; binary.write_text("", encoding="utf-8")
    original = (status.paths.resolve, status.doctor.engines.find, status.doctor.engines.version)
    try:
        status.paths.resolve = lambda: (root, paths.BY_MARKER)
        # status reads the setup through doctor.inspect now, so the stub belongs at that seam.
        status.doctor.engines.find = lambda name: binary if name == "blender" else (_ for _ in ()).throw(engines.EngineMissing("missing"))
        status.doctor.engines.version = lambda path: ("5.2.0", "")
        before = sorted(path.relative_to(root) for path in root.rglob("*"))
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["status", "--json"]) == runner.EXIT_OK
        data = json.loads(stream.getvalue())
        after = sorted(path.relative_to(root) for path in root.rglob("*"))
        assert before == after, "status wrote under work"
        assert data["ok"] is True and data["reports"]["count"] == 0
        assert data["next"][-1]["reason"] == "no_reports_yet"

        (root / "work").rmdir()
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert cli.main(["status", "--json"]) == runner.EXIT_REFUSED
        refused = json.loads(stream.getvalue())
        assert refused["ok"] is False and refused["error"]["code"] == "work_unavailable"
        # A found engine must carry the version it was measured at: a requirement that names a
        # floor and no actual version cannot be checked against it.
        found = next(item for item in refused["doctor"]["requirements"] if item["name"] == "blender")
        assert found["state"] == "found" and found["version"] == "5.2.0", found
    finally:
        (status.paths.resolve, status.doctor.engines.find, status.doctor.engines.version) = original


def check_cli_schema():
    from meshanvil import cli
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        assert cli.main(["schema", "--json"]) == runner.EXIT_OK
    data = json.loads(stream.getvalue())
    assert {"report", "operation", "cli"} <= data.keys(), data
    assert set(schemas.ERROR_CODES) == set(data["cli"]["error_codes"])


def check_error_codes(tmp: Path):
    """Drive the refusals and hold every code they emit against the declared list.

    Comparing the module constant to itself after a round trip through `schema --json` proves
    only that the command prints it. What an agent needs is the other direction: a code that
    reaches `error.code` from outside the list is a contract the tool published and broke.
    """
    from meshanvil import cli, paths

    declared = set(schemas.ERROR_CODES)
    project = tmp / "codes"
    (project / "work").mkdir(parents=True)
    source = project / "subject.blend"
    source.write_bytes(b"not really a blend")
    original = (cli.paths.resolve, cli.paths.work_root, cli.runner.paths.work_root,
                cli.engines.find, cli.doctor.inspect)
    seen = {}
    try:
        cli.paths.resolve = lambda *args: (project, paths.BY_CWD)
        cli.paths.work_root = lambda: project
        cli.runner.paths.work_root = lambda: project
        cases = {
            "unknown_operation": ["run", "no_such_operation", str(source), "--json"],
            "missing_source_file": ["run", "scan_defects", str(project / "gone.blend"), "--json"],
            "malformed_set": ["run", "scan_defects", str(source), "--set", "bare", "--json"],
            "report_not_found": ["reports", "--latest", "--json"],
        }
        for expected, argv in cases.items():
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                cli.main(argv)
            payload = json.loads(stream.getvalue())
            assert payload["ok"] is False, (expected, payload)
            seen[expected] = payload["error"]["code"]

        # The one an agent is most likely to branch on: the same missing engine, asked two ways.
        cli.engines.find = lambda name: (_ for _ in ()).throw(engines.EngineMissing("gone"))
        cli.doctor.inspect = lambda root, write=True: {
            "ok": False, "next": "blender", "requirements": [
                {"name": "blender", "required": True, "state": "missing",
                 "reason": "needed", "fix": "export MESHANVIL_BLENDER=..."}],
            "project": {"name": "codes", "path": str(project), "resolved_by": paths.BY_CWD}}
        for argv in (["status", "--json"], ["doctor", "--json"]):
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                cli.main(argv)
            seen[argv[0]] = json.loads(stream.getvalue())["error"]["code"]
        assert seen["status"] == seen["doctor"] == "engine_missing", seen
    finally:
        (cli.paths.resolve, cli.paths.work_root, cli.runner.paths.work_root,
         cli.engines.find, cli.doctor.inspect) = original

    undeclared = {name: code for name, code in seen.items() if code not in declared}
    assert not undeclared, f"emitted but not in schemas.ERROR_CODES: {undeclared}"
    for expected, code in seen.items():
        if expected in declared:
            assert code == expected, f"{expected} refusal reported {code}"


def check_demo_command(tmp: Path):
    root = tmp / "demo-project"; root.mkdir()
    original = (demo.paths.work_root, demo.paths.asset_root, demo.engines.find, demo.engines.version,
                demo.engines.check_floor, demo.subprocess.run, demo.runner.run)
    calls = []

    def generate(command, **kwargs):
        destination = Path(command[-1])
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(b"blend")
        calls.append(("generate", destination))
        return SimpleNamespace(returncode=0, stdout="generated", stderr="")

    def run_operation(operation, source, params):
        calls.append(("run", operation, Path(source)))
        print("work/ops/001_scan_defects.json")
        return runner.EXIT_OK

    try:
        demo.paths.work_root = lambda: root
        demo.paths.asset_root = lambda *parts: ROOT.joinpath(*parts)
        demo.engines.find = lambda name: Path("/bin/echo")
        demo.engines.version = lambda binary: ("5.2.0", "")
        demo.engines.check_floor = lambda name, number: None
        demo.subprocess.run = generate
        demo.runner.run = run_operation
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert demo.run("figure") == runner.EXIT_OK
        expected = root / "work" / "out" / "demo_figure.blend"
        assert calls == [("generate", expected), ("run", "scan_defects", expected)], calls
        assert "work/ops/001_scan_defects.json" in stream.getvalue()

        shutil.rmtree(root / "work")
        calls.clear()
        demo.engines.find = lambda name: (_ for _ in ()).throw(engines.EngineMissing("missing"))
        try:
            demo.run("figure")
            raise AssertionError("missing Blender should refuse")
        except engines.EngineMissing:
            pass
        assert calls == [] and not (root / "work").exists()
    finally:
        (demo.paths.work_root, demo.paths.asset_root, demo.engines.find, demo.engines.version,
         demo.engines.check_floor, demo.subprocess.run, demo.runner.run) = original


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
    empty = tmp / "doctor-empty"
    empty.mkdir()
    binary = tmp / "blender"
    binary.write_text("", encoding="utf-8")
    original_find, original_version = engines.find, engines.version
    calls = []
    try:
        engines.find = lambda name: binary if name == "blender" else (_ for _ in ()).throw(engines.EngineMissing())
        engines.version = lambda path: (calls.append(path) or ("5.2.0", ""))
        missing = doctor.check(empty)
        work_item = next(item for item in missing["requirements"] if item["name"] == "work")
        assert missing["ok"] is False and work_item["state"] == "missing", missing
        assert not (empty / "work").exists(), "doctor created work while checking"

        (tmp / "work").mkdir(exist_ok=True)
        calls.clear()
        result = doctor.check(tmp)
        assert result["ok"] is True
        assert [item["state"] for item in result["requirements"]] == ["found", "missing", "found"]
        assert [item["class"] for item in result["requirements"]] == ["required", "optional", "required"]
        assert (tmp / "work" / "doctor.json").is_file()
        assert doctor.check(tmp)["next"] is None and len(calls) == 1
    finally:
        engines.find, engines.version = original_find, original_version


def check_run_creates_work(tmp: Path):
    root = tmp / "run-creates-work"; source = root / "source.blend"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"blend")
    original = (runner.paths.work_root, runner.manifests.discover, runner.doctor.work,
                runner.manifests.resolve, runner.engines.find, runner.engines.version,
                runner.engines.check_floor, runner.subprocess.Popen, runner.watch)

    class Done:
        def poll(self): return 0

    try:
        runner.paths.work_root = lambda: root
        runner.manifests.discover = lambda: {"op": {"operation": "op", "kind": "inspection",
                                                    "engine": "blender", "script": "tools/op.py"}}
        runner.doctor.work = doctor.work
        runner.manifests.resolve = lambda manifest, params: {}
        runner.engines.find = lambda name: Path("/bin/echo")
        runner.engines.version = lambda binary: ("5.2.0", "")
        runner.engines.check_floor = lambda name, number: None
        runner.subprocess.Popen = lambda *args, **kwargs: Done()
        def write_report(process, progress, *_):
            report = progress.parents[1] / "001_op.json"
            report.write_text(json.dumps({"id": "001", "status": "ok", "output": {}}, indent=1),
                              encoding="utf-8")
        runner.watch = write_report
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            assert runner.run("op", str(source), {}) == runner.EXIT_OK
        assert (root / "work").is_dir() and "work/ops/001_op.json" in stream.getvalue()
    finally:
        (runner.paths.work_root, runner.manifests.discover, runner.doctor.work,
         runner.manifests.resolve, runner.engines.find, runner.engines.version,
         runner.engines.check_floor, runner.subprocess.Popen, runner.watch) = original


def check_engine_floor():
    try:
        engines.check_floor("blender", "4.1.0")
        raise AssertionError("an old Blender must be refused")
    except engines.EngineMissing as error:
        assert "bpy.ops.wm.stl_export" in str(error) and "MESHANVIL_BLENDER" in str(error)
    assert "MESHANVIL_BLENDER" in engines.fix_command("blender")


def check_fix_command_fits_the_host():
    """The override hint is the one screen a user with no engine is sent to. A /mnt/c path
    offered on macOS is a dead end, so the hint follows the host and not the candidate order."""
    original_wsl, original_system = engines.in_wsl, engines.platform.system
    try:
        engines.in_wsl = lambda: True
        engines.platform.system = lambda: "Linux"
        assert "/mnt/c/" in engines.fix_command("blender")
        engines.in_wsl = lambda: False
        engines.platform.system = lambda: "Darwin"
        assert engines.fix_command("blender").count("/Applications/Blender.app") == 1
        assert "/mnt/c/" not in engines.fix_command("freecad")
        engines.platform.system = lambda: "Windows"
        assert engines.fix_command("blender").startswith("set MESHANVIL_BLENDER=")
    finally:
        engines.in_wsl, engines.platform.system = original_wsl, original_system


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


def check_render_urls_are_urls():
    """A render reference is a URL, not a host path.

    On Windows `os.path.relpath` answers with backslashes, and the payload put them straight
    into an `img src`. Chromium folds them back for file:, so it loaded and nothing said
    otherwise -- the kind of defect that only shows up on the platform nobody develops on.
    """
    from meshanvil import viewer_payload

    page = Path("/project/work/viewer")
    report = {"renders": [{"path": "/project/work/renders/001_3q.png"}],
              "comparisons": [{"before": "/project/work/renders/001_before.png",
                               "after": "/project/work/renders/001_after.png"}]}
    built = viewer_payload.with_render_urls(page, report)
    urls = [built["renders"][0]["url"],
            built["comparisons"][0]["before_url"], built["comparisons"][0]["after_url"]]
    for url in urls:
        assert "\\" not in url, f"a backslash reached a render URL: {url!r}"
    assert urls[0] == "../renders/001_3q.png", urls

    # The Windows shape, asserted without a Windows host: ntpath is what runs there.
    import ntpath
    original = viewer_payload.os.path.relpath
    try:
        viewer_payload.os.path.relpath = ntpath.relpath
        windows = viewer_payload.with_render_urls(
            Path(r"C:/project/work/viewer"), {"renders": [{"path": r"C:/project/work/renders/x.png"}]})
        assert windows["renders"][0]["url"] == "../renders/x.png", windows
    finally:
        viewer_payload.os.path.relpath = original


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

    original_run = viewer_run.subprocess.run
    try:
        assert post({"X-Meshanvil-Token": "wrong"}, {"command": "list"}) == 401, "a bad token was accepted"
        assert post({}, {"command": "list"}) == 401, "a missing token was accepted"
        assert post({"X-Meshanvil-Token": token}, {"command": "rm -rf /"}) == 400, "a command outside the closed set was accepted"

        assert post({"X-Meshanvil-Token": token}, {"command": "list"}) == 200, "a valid request was refused"

        released = threading.Event()

        def slow_run(command, *a, **k):
            assert "bin/meshanvil" not in " ".join(map(str, command)), command
            released.wait(timeout=2)
            return SimpleNamespace(stdout="ok", stderr="", returncode=0)

        statuses = []

        def call():
            statuses.append(post({"X-Meshanvil-Token": token}, {"command": "prune"}))
        viewer_run.subprocess.run = slow_run
        first = threading.Thread(target=call)
        first.start()
        time.sleep(0.2)   # let the first request take the lock before the second arrives
        second_status = post({"X-Meshanvil-Token": token}, {"command": "prune"})
        released.set()
        first.join(timeout=2)
        assert second_status == 409, "a concurrent request was queued instead of refused"
        assert statuses == [200], "the in-flight request did not complete normally"
    finally:
        viewer_run.subprocess.run = original_run
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def check_viewer_origin_and_listing(tmp: Path):
    root = tmp / "served-boundary"
    served = root / "work"
    (served / "viewer").mkdir(parents=True)
    (served / "in").mkdir()
    # A minimal page rather than a bare word: the root route injects a <base> into its head,
    # and a fixture with no head would pass by having nothing to find.
    (served / "viewer" / "index.html").write_text(
        "<html><head></head><body>ok</body></html>", encoding="utf-8")
    (served / "viewer" / "data.js").write_text("token", encoding="utf-8")
    server = viewer_server.make_server(served, root, "token")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]

    def request(method, path, headers=None, body=None, skip_host=False):
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        if skip_host:
            conn.putrequest(method, path, skip_host=True)
            for key, value in (headers or {}).items():
                conn.putheader(key, value)
            conn.endheaders()
            if body is not None:
                conn.send(json.dumps(body).encode("utf-8"))
        else:
            conn.request(method, path, body=json.dumps(body) if body is not None else None,
                         headers=headers or {})
        response = conn.getresponse()
        status = response.status
        response.read()
        conn.close()
        return status

    good = {"Host": f"127.0.0.1:{port}"}
    bad_host = {"Host": "evil.example"}
    bad_origin = {"Host": f"127.0.0.1:{port}", "Origin": "http://evil.example"}
    good_origin = {"Host": f"127.0.0.1:{port}", "Origin": f"http://127.0.0.1:{port}"}
    try:
        assert request("GET", "/api/ping", good) == 200
        assert request("GET", "/api/ping", good_origin) == 200
        assert request("GET", "/api/ping", skip_host=True) == 403
        for path in ("/api/ping", "/api/data", "/api/events", "/viewer/data.js"):
            assert request("GET", path, bad_host) == 403, path
        # HEAD is inherited, reaches the static tree by itself, and answered size and existence
        # for every file under work/ until it was guarded too.
        for path in ("/viewer/data.js", "/in/"):
            assert request("HEAD", path, bad_host) == 403, path
        assert request("HEAD", "/viewer/index.html", good) == 200
        for path, body in (("/run", {"command": "list"}), ("/file", {"id": "x", "action": "open"})):
            assert request("POST", path, {**bad_host, "X-Meshanvil-Token": "token"}, body) == 403, path
        assert request("GET", "/api/data", bad_origin) == 403
        # "/" is the address anyone types, and it points at a directory this server refuses to
        # list. It serves the page instead -- with a <base>, since the page's assets are
        # relative to /viewer/ and would otherwise be looked for at the root.
        assert request("GET", "/", good) == 200
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/", headers=good)
        response = conn.getresponse()
        page = response.read().decode("utf-8")
        conn.close()
        assert '<base href="/viewer/">' in page, page[:200]
        # Every other directory still refuses: the redirect is a convenience on one path, not
        # a hole in the listing boundary.
        assert request("GET", "/in/", good) == 404
        assert request("GET", "/viewer/index.html", good) == 200
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def check_first_paint_carries_what_it_draws(tmp: Path):
    """The served first paint leaves out what nothing has asked for yet; the snapshot does not.

    623 KB before a click, of which the reports of projects nobody had selected and the bodies
    of runbooks nobody had opened. Both are fetchable afterwards, which a page opened from the
    filesystem cannot do -- so its snapshot stays whole.
    """
    from meshanvil import viewer_payload

    root = tmp / "first-paint"
    (root / "work" / "ops").mkdir(parents=True)
    (root / "work" / "viewer").mkdir(parents=True)
    (root / "work" / "ops" / "001_op.json").write_text(json.dumps(
        {"id": "001", "operation": "op", "kind": "inspection", "status": "ok",
         "created_at": "2026-01-01T00:00:00Z", "schema_version": 1,
         "input": {"path": str(root / "work" / "out" / "a.blend"), "sha256": "a" * 64},
         "links": {"parent": None, "parent_source": None, "docs": []}}), encoding="utf-8")

    full = viewer_payload.payload(root, root / "work" / "viewer")
    lite = viewer_payload.payload(root, root / "work" / "viewer", full=False)

    assert full["lazy"] is False and lite["lazy"] is True, (full["lazy"], lite["lazy"])
    assert lite["docs"] == {}, "the first paint still ships document bodies"
    assert full["reports"] == lite["reports"], "the active project lost its reports"
    # Both shapes come from one builder, so a field cannot appear in one and be forgotten in
    # the other. Only the two that are deliberately thinner may differ.
    assert set(full) == set(lite), set(full) ^ set(lite)
    differing = {key for key in full if json.dumps(full[key], sort_keys=True)
                 != json.dumps(lite[key], sort_keys=True)}
    assert differing <= {"docs", "projects", "lazy", "generated_at"}, differing
    # files is the map the file controls resolve an id through: a project's reports can arrive
    # later, its files cannot.
    assert full["files"] == lite["files"], "the first paint dropped file references"
    for entry in lite["projects"]:
        if entry["name"] != lite["active"]:
            assert entry["reports"] == [], f"{entry['name']} still ships its reports"


def check_annotations_stay_out_of_the_reports(tmp: Path):
    """The one route that writes, and the boundary it must not cross. Voir adr_009.

    An annotation is the first content a person authors inside the page. It lands beside the
    reports and never in them, the route is guarded like the two that already write nothing,
    and an interrupted write leaves the previous file rather than a truncated one -- a
    truncated annotation file would take every note with it.
    """
    from meshanvil import notes
    from meshanvil.viewer_routes import note as note_route

    root = tmp / "annotated"
    ops = root / "work" / "ops"
    ops.mkdir(parents=True)
    report = ops / "001_scan_defects.json"
    report.write_text(json.dumps({"id": "001", "links": {"parent": None}}), encoding="utf-8")
    fingerprint = report.read_bytes()

    assert notes.read(root) == {"reports": {}, "chains": {}}, notes.read(root)
    notes.put(root, "reports", "001", "the arch was picked by eye and it showed")
    notes.put(root, "chains", "a" * 64, "Support moteur, second attempt")
    stored = notes.read(root)
    assert stored["reports"]["001"].startswith("the arch"), stored
    assert stored["chains"]["a" * 64].startswith("Support"), stored
    # The report is untouched: that is the whole point of storing this elsewhere.
    assert report.read_bytes() == fingerprint, "writing an annotation modified a report"
    assert notes.path(root).parent == root / "work", notes.path(root)

    # An empty note removes the entry rather than storing an empty string.
    notes.put(root, "reports", "001", "   ")
    assert "001" not in notes.read(root)["reports"], notes.read(root)

    # Only two kinds are writable, and a key is required: the request never names a path.
    for kind, key in (("outputs", "001"), ("reports", "")):
        try:
            notes.put(root, kind, key, "x")
            raise AssertionError(f"an annotation was accepted for {kind!r}/{key!r}")
        except KeyError:
            pass

    # A write that fails partway leaves the previous file intact, never a truncated one.
    notes.put(root, "chains", "b" * 64, "kept")
    before = notes.path(root).read_bytes()
    original_replace = notes.os.replace
    try:
        notes.os.replace = lambda *args: (_ for _ in ()).throw(OSError("disk full"))
        try:
            notes.put(root, "chains", "c" * 64, "lost")
        except OSError:
            pass
    finally:
        notes.os.replace = original_replace
    assert notes.path(root).read_bytes() == before, "an interrupted write damaged the file"
    leftovers = list((root / "work").glob(".notes-*"))
    assert not leftovers, f"a temporary file was left behind: {leftovers}"

    # The route: guarded like the two that already exist, and refusing anything else.
    class Reply:
        def __init__(self):
            self.status, self.error, self.body = None, None, b""
        def write(self, data):
            self.body += data
        def flush(self):
            pass

    class Handler:
        meshanvil_root = root
        meshanvil_token = "token"
        def __init__(self, headers, payload):
            self.headers = headers
            self.rfile = io.BytesIO(json.dumps(payload).encode("utf-8"))
            self.headers.setdefault("Content-Length", str(len(self.rfile.getvalue())))
            self.wfile = Reply()
            self.status = None
            self.error = None
        def send_error(self, code, message=None):
            self.error = code
        def send_response(self, code):
            self.status = code
        def send_header(self, key, value):
            pass
        def end_headers(self):
            pass

    good = {"X-Meshanvil-Token": "token"}
    handler = Handler(dict(good), {"kind": "reports", "key": "001", "text": "through the route"})
    assert note_route.handle_post(handler, "/note", None) is True
    assert handler.status == 200 and handler.error is None, (handler.status, handler.error)
    assert notes.read(root)["reports"]["001"] == "through the route", notes.read(root)
    assert report.read_bytes() == fingerprint, "the route modified a report"

    for headers, payload, why in (
            ({}, {"kind": "reports", "key": "001", "text": "x"}, "no token"),
            ({"X-Meshanvil-Token": "wrong"}, {"kind": "reports", "key": "001", "text": "x"}, "wrong token"),
            (dict(good), {"kind": "outputs", "key": "001", "text": "x"}, "unknown kind"),
            (dict(good), {"kind": "reports", "key": "", "text": "x"}, "empty key"),
            (dict(good), {"kind": "reports", "key": "001"}, "no text"),
            (dict(good), {"kind": "reports", "key": "001", "text": 3}, "text is not a string")):
        rejected = Handler(headers, payload)
        assert note_route.handle_post(rejected, "/note", None) is True, why
        assert rejected.error in (400, 401), (why, rejected.error, rejected.status)
    assert note_route.handle_post(Handler(dict(good), {}), "/other", None) is False

    # Retention tidies an annotation whose report was removed by hand, and keeps chain names,
    # which key on a source file rather than on any particular run over it.
    notes.put(root, "reports", "404", "a report that is not there")
    report.unlink()
    other = ops / "002_list_shells.json"
    other.write_text(json.dumps({"id": "002", "links": {"parent": None}}), encoding="utf-8")
    dropped = notes.forget_missing_reports(root, {"002"})
    assert dropped == ["001", "404"], dropped
    assert notes.read(root)["chains"]["b" * 64] == "kept", notes.read(root)


def check_events_cadence_is_declared(tmp: Path):
    """The period between two looks is a declared number, not a multiple of the scan's cost.

    Sleeping for twenty times the scan made the viewer's liveness a function of how much there
    was to watch: with eight sibling projects the scan is dear and the page answered slowest
    exactly when it had most to say. A scan made ten times dearer here must not change the
    period, only eat into it.
    """
    original_signatures, original_sleep, original_counter = (
        viewer_events.signatures, viewer_events.time.sleep, viewer_events.time.perf_counter)
    slept, clock = [], [0.0]

    class Gone:
        def write(self, data):
            if len(slept) > 2:
                raise BrokenPipeError()
        def flush(self):
            pass

    class Handler:
        meshanvil_root = tmp
        wfile = Gone()
        def send_response(self, code): pass
        def send_header(self, key, value): pass
        def end_headers(self): pass

    def run(scan_cost: float) -> list:
        slept.clear()
        clock[0] = 0.0

        def counter():
            clock[0] += scan_cost
            return clock[0]

        viewer_events.time.perf_counter = counter
        viewer_events.signatures = lambda root: {"reports": ()}
        viewer_events.time.sleep = lambda seconds: slept.append(seconds)
        viewer_events.handle_get(Handler(), "/api/events", None)
        return list(slept)

    try:
        cheap = run(0.001)
        dear = run(0.010)
        assert cheap and dear, (cheap, dear)
        for naps, cost in ((cheap, 0.001), (dear, 0.010)):
            for nap in naps:
                assert abs(nap - (viewer_events.INTERVAL - cost)) < 1e-6, (nap, cost)
        # A scan dearer than the period does not push the period out; it runs back to back.
        assert all(nap == 0.0 for nap in run(viewer_events.INTERVAL * 2)), run(viewer_events.INTERVAL * 2)
    finally:
        viewer_events.signatures = original_signatures
        viewer_events.time.sleep = original_sleep
        viewer_events.time.perf_counter = original_counter


def check_events_releases_gone_peer(tmp: Path):
    original_signatures, original_sleep = viewer_events.signatures, viewer_events.time.sleep
    writes = []

    class Gone:
        def write(self, data):
            writes.append(data)
            if len(writes) > 1:
                raise BrokenPipeError()
        def flush(self):
            pass

    class Handler:
        meshanvil_root = tmp
        wfile = Gone()
        def send_response(self, code): pass
        def send_header(self, key, value): pass
        def end_headers(self): pass

    try:
        viewer_events.signatures = lambda root: {"reports": (), "doctor": (), "runbooks": ()}
        viewer_events.time.sleep = lambda seconds: None
        assert viewer_events.handle_get(Handler(), "/api/events", None) is True
        assert writes == [b": connected\n\n", b": poll\n\n"], writes
    finally:
        viewer_events.signatures, viewer_events.time.sleep = original_signatures, original_sleep


def check_viewer_comparison_layout():
    css = (ROOT / "viewer" / "viewer.css").read_text(encoding="utf-8")
    script = (ROOT / "viewer" / "src" / "app.js").read_text(encoding="utf-8")
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
    assert "let SERVED = location.protocol" in script and "if (run && SERVED)" in script


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
    root = tmp / "outside-prune"; (root / "work" / "ops").mkdir(parents=True)
    outside = tmp / "outside.blend"; outside.write_bytes(b"outside")
    report = {"id": "009", "chain": "009", "output": {"path": str(outside), "state": "present"}, "links": {"docs": []}}
    (root / "work" / "ops" / "009_op.json").write_text(json.dumps(report), encoding="utf-8")
    assert all(path != outside for _, _, path in prune.candidates(root, 0))
    assert prune.run(root, 0, True)[0] == [] and outside.is_file()
    assert prune.run(root, 0, False)[0] == [] and outside.is_file()


def check_runner_interrupt_stops_engine(tmp: Path):
    root = tmp / "interrupt"; source = root / "source.blend"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"blend")
    original = (runner.paths.work_root, runner.manifests.discover, runner.doctor.work,
                runner.manifests.resolve, runner.engines.find, runner.engines.version,
                runner.engines.check_floor, runner.subprocess.Popen, runner.watch)
    stopped = []

    class FakeProcess:
        def __init__(self):
            self.dead = False
        def poll(self):
            return 0 if self.dead else None
        def terminate(self):
            stopped.append("terminate")
            self.dead = True
        def wait(self, timeout=None):
            return 0
        def kill(self):
            stopped.append("kill")
            self.dead = True

    try:
        runner.paths.work_root = lambda: root
        runner.manifests.discover = lambda: {"op": {"operation": "op", "kind": "inspection",
                                                    "engine": "blender", "script": "tools/op.py"}}
        runner.doctor.work = lambda project: {"state": "found"}
        runner.manifests.resolve = lambda manifest, params: {}
        runner.engines.find = lambda name: Path("/bin/echo")
        runner.engines.version = lambda binary: ("5.2.0", "")
        runner.engines.check_floor = lambda name, number: None
        runner.subprocess.Popen = lambda *args, **kwargs: FakeProcess()
        runner.watch = lambda process, progress, *_: (_ for _ in ()).throw(KeyboardInterrupt())
        try:
            runner.run("op", str(source), {})
            raise AssertionError("interrupt was swallowed")
        except KeyboardInterrupt:
            pass
        assert stopped == ["terminate"], stopped
        assert not list((root / runner.OPS).glob("*.json"))

        # A termination that will not complete must not take the place of the interrupt, or the
        # claimed report survives with nothing in it.
        class Stuck(FakeProcess):
            def wait(self, timeout=None):
                raise runner.subprocess.TimeoutExpired("engine", timeout)

        stopped.clear()
        runner.subprocess.Popen = lambda *args, **kwargs: Stuck()
        try:
            runner.run("op", str(source), {})
            raise AssertionError("interrupt was swallowed")
        except KeyboardInterrupt:
            pass
        assert stopped == ["terminate", "kill"], stopped
        assert not list((root / runner.OPS).glob("*.json"))
    finally:
        (runner.paths.work_root, runner.manifests.discover, runner.doctor.work,
         runner.manifests.resolve, runner.engines.find, runner.engines.version,
         runner.engines.check_floor, runner.subprocess.Popen, runner.watch) = original


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
        check_captured_output_is_utf8()
        check_cli_welcome()
        check_cli_json(tmp)
        check_cli_reports(tmp)
        check_cli_status(tmp)
        check_cli_schema()
        check_error_codes(tmp)
        check_demo_command(tmp)
        check_i18n()
        check_doctor(tmp)
        check_run_creates_work(tmp)
        check_engine_floor()
        check_fix_command_fits_the_host()
        check_wsl_boundary(tmp)
        check_doctor_exit_code()
        check_render_urls_are_urls()
        check_viewer_start(tmp)
        check_run_endpoint(tmp)
        check_viewer_origin_and_listing(tmp)
        check_events_releases_gone_peer(tmp)
        check_viewer_comparison_layout()
        check_logics_bridge()
        check_prune(tmp)
        check_runner_interrupt_stops_engine(tmp)
        check_target_lock(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selfcheck: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
