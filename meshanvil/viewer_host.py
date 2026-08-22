"""Host actions for the local viewer."""
from __future__ import annotations

import subprocess, webbrowser
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
