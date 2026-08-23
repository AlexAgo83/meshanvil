"""Where the tool is installed, and where the operator's work is kept.

One value used to answer both questions, and every model an operator opened shared one report
directory: a second subject took the first one's identity numbering, merged into its outliner
group, and had its retention decided by the first one's activity.

The installation holds what ships with the tool -- operation manifests, locales and the
viewer's own files. A project holds what the operator makes: reports, sources, renders, the
built page, the setup report and any Logics corpus it wants the viewer to read.

A project is found by walking up from the working directory for a marker, the way a version
control tool finds its own. That keeps the choice visible: the working directory is on screen,
an environment variable is not, and this decides where a destructive run lands. The variable
exists for a non-interactive caller that has no working directory to speak of.

With no marker anywhere above, the current directory is the project. That is what an installed
command needs when it is run outside a checkout.
"""
from __future__ import annotations

from importlib import resources
import os
from pathlib import Path

MARKER = ".meshanvil"
OVERRIDE = "MESHANVIL_PROJECT"

BY_OVERRIDE = "override"
BY_MARKER = "marker"
BY_CWD = "current_directory"


def code_root() -> Path:
    """The installation: host package, runtime assets and contributor corpus."""
    return Path(__file__).resolve().parent.parent


def asset_root(name: str) -> Path:
    """Runtime assets come from the checkout when present, otherwise from the installed wheel."""
    found = code_root() / name
    if found.exists():
        return found
    return Path(resources.files(name))


def resolve(start: Path | None = None) -> tuple[Path, str]:
    """The active project and the rule that chose it, so a caller can say which applied."""
    override = os.environ.get(OVERRIDE)
    if override:
        return Path(override).expanduser().resolve(), BY_OVERRIDE
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / MARKER).is_dir():
            return candidate, BY_MARKER
    return here, BY_CWD


def work_root(start: Path | None = None) -> Path:
    return resolve(start)[0]


def name(root: Path) -> str:
    """What to call a project on screen."""
    return Path(root).resolve().name or "project"


def projects(root: Path | None = None) -> list[Path]:
    """Every project that holds at least one report, the active one first.

    Siblings of the active project are offered because that is how an operator keeps them:
    one directory of subjects. Nothing is discovered outside it, and nothing is remembered
    between runs -- there is no registry to go stale.
    """
    active = Path(root).resolve() if root else work_root()
    # The active root is always first, reports or not: it is where a run would land, and a
    # page that omitted it would name a project the operator is not in.
    found = [active]
    # Siblings are only a neighbourhood when the active root is itself a project. Offering
    # them from an unmarked directory would show someone else's reports as if they were the
    # ones about to be written to.
    parent = active.parent
    if (active / MARKER).is_dir() and parent != active and parent.is_dir():
        for candidate in sorted(parent.iterdir()):
            if candidate == active or not candidate.is_dir():
                continue
            if (candidate / MARKER).is_dir() and (candidate / "work" / "ops").is_dir():
                found.append(candidate.resolve())
    # And whatever the active root contains. A checkout that holds its demonstrations
    # under work/demo is not a sibling of them, so without this the page opened at the place
    # everyone knows lists nothing while the reports sit two directories down.
    for depth in ("*", "*/*", "*/*/*"):     # work/demo/<name> is three down
        for candidate in sorted(active.glob(depth)):
            if not candidate.is_dir() or candidate.resolve() in found:
                continue
            if (candidate / MARKER).is_dir() and (candidate / "work" / "ops").is_dir():
                found.append(candidate.resolve())
    return found


def initialise(root: Path) -> tuple[Path, bool]:
    """Make a directory a project. Idempotent: running it twice is not an error.

    Only the marker and the work directories. There is nothing to configure, because a
    project is a place, not a set of settings.
    """
    root = Path(root).expanduser().resolve()
    marker = root / MARKER
    fresh = not marker.is_dir()
    marker.mkdir(parents=True, exist_ok=True)
    for directory in ("in", "out", "ops", "renders"):
        (root / "work" / directory).mkdir(parents=True, exist_ok=True)
    return root, fresh
