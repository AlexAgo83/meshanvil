"""First-run demonstration: generate a source, then run existing operations on it."""
from __future__ import annotations
import contextlib, io, subprocess

from . import engines, paths, runner
from .i18n import t

SUBJECTS = {
    "figure": ("make_demo_figure.py", "demo_figure.blend"),
    "vehicle": ("make_demo_vehicle.py", "demo_vehicle.blend"),
}


def run(subject: str = "figure") -> int:
    script, filename = SUBJECTS[subject]
    binary = engines.find("blender")
    number, _build = engines.version(binary)
    engines.check_floor("blender", number)
    root = paths.work_root()
    out = root / "work" / "out"
    out.mkdir(parents=True, exist_ok=True)
    source = out / filename
    built = subprocess.run([str(binary), "-b", "-P", str(paths.asset_root("tools") / script),
                            "--", str(source)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if built.returncode:
        raise runner.Refused(built.stderr.strip() or built.stdout.strip() or t("cli.demo.failed"))
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        code = runner.run("scan_defects", str(source), {})
    if code != runner.EXIT_OK:
        return code
    print(t("cli.demo.ready", source=source.relative_to(root)))
    for report in stream.getvalue().splitlines():
        if report:
            print(t("cli.demo.report", report=report))
    print(t("cli.demo.next"))
    return runner.EXIT_OK
