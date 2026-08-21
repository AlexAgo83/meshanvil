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
