#!/usr/bin/env python3
"""Keep the catalogues honest: same keys, same placeholders, nothing unread.

A key present in one language and not the other, a placeholder that changed on one side, or a
key nothing reads -- all three rot silently, and all three are cheap to catch.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "en"
READERS = ["meshanvil", "viewer", "scripts", "bin"]
PLACEHOLDER = re.compile(r"\{([a-z_]+)\}")


def flatten(values: dict, prefix: str = "") -> dict:
    result = {}
    for key, value in values.items():
        name = f"{prefix}.{key}" if prefix else key
        result.update(flatten(value, name) if isinstance(value, dict) else {name: value})
    return result


def catalogues() -> dict[str, dict]:
    return {path.stem: flatten(json.loads(path.read_text(encoding="utf-8")))
            for path in sorted((ROOT / "locales").glob("*.json"))}


def used_keys() -> set[str]:
    """Keys requested by code or static viewer markup."""
    found = set()
    for directory in READERS:
        for path in (ROOT / directory).rglob("*"):
            if path.suffix not in (".py", ".js", ".html") or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            found |= set(re.findall(r"""\bt\(\s*["']([a-z0-9_.]+)["']""", text))
            found |= set(re.findall(r"""\bdata-i18n(?:-aria-label)?=["']([a-z0-9_.]+)["']""", text))
    for path in (ROOT / "tools").glob("*.op.json"):
        # local_* is an operation that lives in one checkout and ships nothing, catalogues
        # included. Scanned, it reports every local operation as a missing string.
        if path.name.startswith("local_"):
            continue
        found.add(json.loads(path.read_text(encoding="utf-8"))["summary_key"])
    return found


def main() -> int:
    books = catalogues()
    source = books[SOURCE]
    problems = []

    for lang, book in books.items():
        if lang == SOURCE:
            continue
        for key in sorted(set(source) - set(book)):
            problems.append(f"{lang}: missing key {key}")
        for key in sorted(set(book) - set(source)):
            problems.append(f"{lang}: key {key} exists in {lang} but not in {SOURCE}")
        for key in sorted(set(source) & set(book)):
            here, there = set(PLACEHOLDER.findall(source[key])), set(PLACEHOLDER.findall(book[key]))
            if here != there:
                problems.append(f"{lang}: placeholders differ on {key}: "
                                f"{sorted(here)} vs {sorted(there)}")

    asked = used_keys()
    for key in sorted(set(source) - asked):
        problems.append(f"{SOURCE}: key {key} is read by nothing")
    for key in sorted(asked - set(source)):
        problems.append(f"{SOURCE}: key {key} is read but not defined")

    if problems:
        for problem in problems:
            print(problem)
        return 1
    print(f"i18n: ok ({len(source)} keys, {len(books)} languages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
