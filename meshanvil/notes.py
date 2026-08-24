"""Annotations: what a person knows about a report that its numbers do not say.

Kept strictly apart from the reports. A report is the record of what an engine did, and the
project's premise is that every number in it came out of that engine; prose written by a
person cannot go in there without diluting exactly what makes it evidence. So annotations live
in one flat file beside them, readable with `cat` -- an agent returning to a chain is a
first-class reader of it, not only the page. Voir adr_009.
"""
from __future__ import annotations

import json, os, tempfile
from pathlib import Path

FILENAME = "notes.json"
EMPTY: dict = {"reports": {}, "chains": {}}


def path(root: Path) -> Path:
    return root / "work" / FILENAME


def read(root: Path) -> dict:
    """Never raises: a viewer that cannot read an annotation still has to show the reports."""
    try:
        loaded = json.loads(path(root).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(EMPTY)
    return {"reports": dict(loaded.get("reports") or {}),
            "chains": dict(loaded.get("chains") or {})}


def write(root: Path, data: dict) -> None:
    """Whole file, atomically: a temporary file beside it, then a rename.

    A crash or a second writer can leave a stale file; neither can leave a truncated one, and a
    truncated annotation file would take every note with it."""
    target = path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=str(target.parent), prefix=".notes-", suffix=".json")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=1, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def put(root: Path, kind: str, key: str, text: str) -> dict:
    """Set or clear one annotation. An empty text removes the entry rather than storing "".

    `kind` is `reports` or `chains` and nothing else: the request never names a path, and the
    file it lands in is derived from the root the server was launched with."""
    if kind not in ("reports", "chains"):
        raise KeyError(kind)
    if not key:
        raise KeyError("empty key")
    data = read(root)
    if text.strip():
        data[kind][key] = text
    else:
        data[kind].pop(key, None)
    write(root, data)
    return data


def forget_missing_reports(root: Path, kept: set[str]) -> list[str]:
    """Drop notes whose report no longer exists, and say which.

    `prune` deletes reports and knows nothing about annotations, so without this a note outlives
    the thing it describes and rots there. Chain names are not touched: they key on the sha256
    of a source file, which outlives any particular run over it."""
    data = read(root)
    orphans = sorted(key for key in data["reports"] if key not in kept)
    if orphans:
        for key in orphans:
            data["reports"].pop(key, None)
        write(root, data)
    return orphans
