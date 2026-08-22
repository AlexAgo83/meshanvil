"""Host actions for the local viewer."""
from __future__ import annotations

import os, subprocess, sys, webbrowser
from pathlib import Path

from .engines import in_wsl


def open_in_browser(target: Path | str) -> None:
    if isinstance(target, str):
        webbrowser.open(target)
        return
    if in_wsl():
        windows = subprocess.run(["wslpath", "-w", str(target)], capture_output=True,
                                 text=True, check=False).stdout.strip()
        subprocess.run(["explorer.exe", windows], check=False)
        return
    webbrowser.open(target.as_uri())


def open_file(path: Path) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    elif os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def reveal_file(path: Path) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", "-R", str(path)], check=False)
    elif os.name == "nt":
        subprocess.run(["explorer", f"/select,{path}"], check=False)
    else:
        subprocess.run(["xdg-open", str(path.parent)], check=False)
