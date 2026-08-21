"""Find an engine, and translate paths when the host and the engine disagree on what a path is."""
from __future__ import annotations
import os, platform, shutil, subprocess
from pathlib import Path

from .i18n import t

CANDIDATES = {
    "blender": [
        "/Applications/Blender.app/Contents/MacOS/Blender",
        "/mnt/c/Program Files/Blender Foundation/Blender 5.2/blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
    ],
    "freecad": [
        "/Applications/FreeCAD.app/Contents/MacOS/FreeCAD",
        r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe",
    ],
}
OVERRIDE = {"blender": "MESHANVIL_BLENDER", "freecad": "MESHANVIL_FREECAD"}
MIN_VERSION = {"blender": (4, 2), "freecad": (1, 0)}


class EngineMissing(Exception):
    """Raised when an engine cannot be found or is too old. The runner turns this into exit 2."""


def in_wsl() -> bool:
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


def find(engine: str) -> Path:
    """The override wins, then PATH, then the documented locations."""
    override = os.environ.get(OVERRIDE[engine])
    if override:
        if not Path(override).exists():
            raise EngineMissing(t("engine.override_missing", variable=OVERRIDE[engine],
                                  path=override))
        return Path(override)
    on_path = shutil.which(engine) or shutil.which(engine + ".exe")
    if on_path:
        return Path(on_path)
    for candidate in CANDIDATES[engine]:
        if Path(candidate).exists():
            return Path(candidate)
    raise EngineMissing(t("engine.not_found", engine=engine, variable=OVERRIDE[engine]))


def is_windows_binary(binary: Path) -> bool:
    return binary.suffix.lower() == ".exe"


def for_engine(path: os.PathLike | str, binary: Path) -> str:
    """A Windows engine driven from WSL cannot read a Linux path. Translate at the boundary."""
    text = str(Path(path).resolve())
    if in_wsl() and is_windows_binary(binary):
        return subprocess.run(["wslpath", "-w", text], capture_output=True, text=True,
                              check=True).stdout.strip()
    return text


def version(binary: Path) -> tuple[str, str]:
    """Return (version, build hash). Blender prints both on its first two lines."""
    out = subprocess.run([str(binary), "--version"], capture_output=True, text=True,
                         check=False).stdout
    number, build = "", ""
    for line in out.splitlines():
        if line.startswith("Blender ") and not number:
            number = line.split()[1]
            if "hash" in line:
                build = line.split("hash")[1].strip(" )").split()[0]
        if line.strip().startswith("build hash:") and not build:
            build = line.split(":", 1)[1].strip()
    return number, build


def check_floor(engine: str, number: str) -> None:
    try:
        found = tuple(int(part) for part in number.split(".")[:2])
    except ValueError:
        return  # an unreadable version is not a reason to refuse; the operation will say more
    if found < MIN_VERSION[engine]:
        need = ".".join(str(part) for part in MIN_VERSION[engine])
        raise EngineMissing(t("engine.too_old", engine=engine, found=number, needed=need))
