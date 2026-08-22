"""Every operator-facing string comes from a catalogue. English is the source and the fallback.

Warning codes, report field names and operation names are identifiers, not text: an agent
parses them, so they are never translated. See item_010.
"""
from __future__ import annotations
import json, locale, os
from functools import lru_cache
from pathlib import Path

SOURCE = "en"


def root() -> Path:
    """Locales ship with the tool, never with a project."""
    from .paths import asset_root
    return asset_root("locales")


def language() -> str:
    """MESHANVIL_LANG, then the system locale, then English."""
    chosen = os.environ.get("MESHANVIL_LANG")
    if not chosen:
        try:
            chosen = (locale.getlocale()[0] or "")[:2]
        except (ValueError, TypeError):
            chosen = ""
    chosen = (chosen or SOURCE).split("_")[0].lower()
    return chosen if (root() / f"{chosen}.json").exists() else SOURCE


@lru_cache(maxsize=None)
def catalogue(lang: str) -> dict:
    path = root() / f"{lang}.json"
    try:
        def flatten(values: dict, prefix: str = "") -> dict:
            result = {}
            for key, value in values.items():
                name = f"{prefix}.{key}" if prefix else key
                result.update(flatten(value, name) if isinstance(value, dict) else {name: value})
            return result
        return flatten(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError):
        return {}


def t(key: str, **values) -> str:
    """A key missing from the chosen language falls back to English, never to the key itself."""
    text = catalogue(language()).get(key) or catalogue(SOURCE).get(key) or key
    try:
        return text.format(**values)
    except (KeyError, IndexError):
        return text
