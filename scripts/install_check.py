#!/usr/bin/env python3
"""Install a built wheel into a clean venv and run the shipped console script."""
from __future__ import annotations
import json, subprocess, sys, tempfile, venv
from pathlib import Path


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)


def main(argv: list[str]) -> int:
    wheels = [Path(arg) for arg in argv]
    if len(wheels) != 1 or not wheels[0].is_file():
        print("usage: install_check.py dist/meshanvil-*.whl", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="meshanvil-install-check-") as tmp:
        env = Path(tmp) / "venv"
        venv.EnvBuilder(with_pip=True).create(env)
        python = env / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        meshanvil = env / ("Scripts/meshanvil.exe" if sys.platform == "win32" else "bin/meshanvil")
        install = run([str(python), "-m", "pip", "install", "--no-deps", str(wheels[0])])
        if install.returncode:
            print(install.stderr or install.stdout, file=sys.stderr)
            return install.returncode
        # From the temporary directory, not the checkout: an installed command has to resolve
        # its project from wherever it was run, and running it here would let it find ours.
        version = run([str(meshanvil), "--version"], cwd=tmp)
        if version.returncode or not version.stdout.startswith("meshanvil "):
            print(version.stderr or version.stdout, file=sys.stderr)
            return 1
        welcome = run([str(meshanvil)], cwd=tmp)
        if welcome.returncode or "meshanvil view" not in welcome.stdout:
            print(welcome.stderr or welcome.stdout, file=sys.stderr)
            return 1
        doctor = run([str(meshanvil), "doctor", "--json"], cwd=tmp)
        try:
            json.loads(doctor.stdout)
        except json.JSONDecodeError:
            print(doctor.stderr or doctor.stdout, file=sys.stderr)
            return 1
        if doctor.returncode not in (0, 2):
            print(doctor.stderr or doctor.stdout, file=sys.stderr)
            return doctor.returncode
        if (Path(tmp) / "work").exists():
            print("doctor created work/ where it was only asked to look", file=sys.stderr)
            return 1
    print("install-check: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
