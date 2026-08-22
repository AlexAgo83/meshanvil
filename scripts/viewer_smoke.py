#!/usr/bin/env python3
"""Exercise the generated viewer in Chrome without adding a browser framework."""
from __future__ import annotations

import argparse, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SMOKE = r"""
<script>
(() => {
  const fail = (message) => {
    document.body.dataset.smoke = "fail";
    document.body.appendChild(Object.assign(document.createElement("pre"), { id: "smoke-result", textContent: message }));
  };
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
  try {
    document.querySelector('[data-workspace="compare"]').click();
    assert(document.querySelector(".app").dataset.workspace === "compare", "compare workspace did not activate");

    const filter = document.querySelector("#outliner-filter");
    filter.value = "voxel";
    filter.dispatchEvent(new Event("input", { bubbles: true }));
    const rows = [...document.querySelectorAll("#outliner .row")];
    assert(rows.length === 1 && rows[0].textContent.toLowerCase().includes("voxel"), "filter did not isolate voxel row");

    rows[0].click();
    const wipe = document.querySelector("[data-wipe]");
    assert(wipe, "comparison wipe input missing");
    wipe.value = "72";
    wipe.dispatchEvent(new Event("input", { bubbles: true }));
    assert(document.querySelector(".compare").style.getPropertyValue("--wipe") === "72%", "wipe value did not update");

    document.querySelector('[data-section-goto="measurements"]').click();
    assert(document.querySelector('[data-section-goto="measurements"]').getAttribute("aria-selected") === "true", "report rail did not select measurements");
    document.body.dataset.smoke = "ok";
    document.body.appendChild(Object.assign(document.createElement("pre"), { id: "smoke-result", textContent: "ok" }));
  } catch (error) {
    fail(error && error.message ? error.message : String(error));
  }
})();
</script>
"""


def chrome_path() -> str | None:
    for candidate in (
        "google-chrome",
        "chromium",
        "chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ):
        found = shutil.which(candidate) if "/" not in candidate else candidate
        if found and Path(found).exists():
            return found
    return None


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshot", type=Path, default=Path(tempfile.gettempdir()) / "meshanvil-viewer-smoke.png")
    args = parser.parse_args()

    chrome = chrome_path()
    if not chrome:
      raise SystemExit("Chrome/Chromium not found; set PATH or install Google Chrome.")

    run([sys.executable, str(ROOT / "scripts" / "fixture_check.py")])
    run([sys.executable, str(ROOT / "bin" / "meshanvil"), "view", "--no-open"])

    with tempfile.TemporaryDirectory(prefix="meshanvil-viewer-smoke-") as tmp:
        tmp_root = Path(tmp)
        shutil.copytree(ROOT / "work" / "viewer", tmp_root / "viewer")
        renders = ROOT / "work" / "renders"
        if renders.exists():
            shutil.copytree(renders, tmp_root / "renders")
        page = tmp_root / "viewer" / "smoke.html"
        page.write_text((tmp_root / "viewer" / "index.html").read_text(encoding="utf-8").replace("</body>", SMOKE + "\n</body>"), encoding="utf-8")
        url = page.resolve().as_uri()
        base = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=2048,1200", "--virtual-time-budget=1500"]
        dom = subprocess.run([*base, "--dump-dom", url], text=True, capture_output=True)
        if dom.returncode:
            raise SystemExit((dom.stderr or dom.stdout or "Chrome did not load the smoke page").strip())
        if 'data-smoke="ok"' not in dom.stdout:
            raise SystemExit((dom.stdout or "Chrome loaded the smoke page without a passing marker").strip())
        shot = subprocess.run([*base, f"--screenshot={args.screenshot}", url], text=True, capture_output=True)
        if shot.returncode:
            raise SystemExit((shot.stderr or shot.stdout).strip())
    if not args.screenshot.exists() or args.screenshot.stat().st_size == 0:
        raise SystemExit("Chrome did not write a screenshot.")
    print(f"viewer-smoke: ok ({args.screenshot})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
