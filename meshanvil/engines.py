"""Find an engine, and translate paths when the host and the engine disagree on what a path is."""
from __future__ import annotations
import os, platform, plistlib, re, shutil, subprocess
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
        "/mnt/c/Program Files/FreeCAD 1.0/bin/FreeCAD.exe",
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
    """Return (version, build hash) for Blender or FreeCAD."""
    info = binary.parents[1] / "Info.plist"
    if binary.name == "FreeCAD" and info.is_file():
        try:
            bundle = plistlib.load(info.open("rb"))
            return (bundle.get("CFBundleShortVersionString") or bundle.get("CFBundleVersion", "")).split("-")[0], ""
        except (OSError, plistlib.InvalidFileException):
            pass
    try:
        out = subprocess.run([str(binary), "--version"], capture_output=True, text=True,
                             check=False, timeout=5).stdout
    except subprocess.TimeoutExpired:
        return "", ""
    number, build = "", ""
    for line in out.splitlines():
        match = re.search(r"(?:Blender|FreeCAD)\s+(\d+(?:\.\d+)+)", line)
        if match and not number:
            number = match.group(1)
            if "hash" in line:
                build = line.split("hash")[1].strip(" )").split()[0]
        if line.strip().startswith("build hash:") and not build:
            build = line.split(":", 1)[1].strip()
    return number, build


def meets_floor(engine: str, number: str) -> bool:
    try:
        return tuple(int(part) for part in number.split(".")[:2]) >= MIN_VERSION[engine]
    except ValueError:
        return True


def fix_command(engine: str) -> str:
    variable = OVERRIDE[engine]
    if platform.system() == "Windows":
        return f"set {variable}={CANDIDATES[engine][-1]}"
    candidate = next((path for path in CANDIDATES[engine] if path.startswith("/mnt/c/")), CANDIDATES[engine][0])
    return f'export {variable}="{candidate}"'


def check_floor(engine: str, number: str) -> None:
    if not meets_floor(engine, number):
        need = ".".join(str(part) for part in MIN_VERSION[engine])
        reason = "bpy.ops.wm.stl_export" if engine == "blender" else engine
        raise EngineMissing(t("engine.too_old", engine=engine, found=number, needed=need,
                              reason=reason, variable=OVERRIDE[engine]))
