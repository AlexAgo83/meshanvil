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
    const fileMenu = document.querySelector(".menu");
    fileMenu.open = true;
    assert(document.querySelector(".dropdown .grp") && document.querySelector(".cmdrow code"), "command menu surface missing");
    fileMenu.open = false;

    document.querySelector("#start-screen").click();
    assert(!document.querySelector("#splash").classList.contains("hidden"), "splash did not open");
    assert(document.querySelectorAll(".splashcols .scol").length === 3, "splash columns missing");
    assert(document.querySelector(".tpl code") && document.querySelector(".chk"), "splash command/check content missing");
    assert(document.querySelector("#splash").textContent.includes("demo_source.blend") && document.querySelector("#splash").textContent.includes("tools/make_demo_scene.py"), "demo dataset option missing");
    document.querySelector('[data-splash="close"]').click();
    assert(document.querySelector("#splash").classList.contains("hidden"), "splash did not close");

    document.querySelector('[data-workspace="runbooks"]').click();
    assert(document.querySelector(".app").dataset.workspace === "runbooks", "runbooks workspace did not activate");
    assert(document.querySelector(".rbbody .rbrow"), "runbooks primary rows missing");
    assert(document.querySelector(".rbpurpose") && document.querySelector(".rbapplied"), "runbook row details missing");
    assert(document.querySelector(".rbcols"), "runbooks column header missing");
    assert(document.querySelector("#graph-name").textContent.toLowerCase().includes("runbook"),
      "runbooks table is still filed under the node editor header");

    document.querySelector('[data-workspace="compare"]').click();
    assert(document.querySelector(".app").dataset.workspace === "compare", "compare workspace did not activate");

    const filter = document.querySelector("#outliner-filter");
    filter.value = "voxel";
    filter.dispatchEvent(new Event("input", { bubbles: true }));
    const rows = [...document.querySelectorAll("#outliner .row")];
    assert(rows.length && rows.every((row) => row.textContent.toLowerCase().includes("voxel")),
      "filter did not isolate the voxel rows");

    rows[0].click();
    const wipe = document.querySelector("[data-wipe]");
    assert(wipe, "comparison wipe input missing");
    assert(document.querySelector(".wipe .handle") && document.querySelector(".wipelabel"), "mockup compare split chrome missing");
    wipe.value = "72";
    wipe.dispatchEvent(new Event("input", { bubbles: true }));
    assert(document.querySelector(".compare").style.getPropertyValue("--wipe") === "72%", "wipe value did not update");

    assert(document.querySelector(".pvmeta table"), "compare before/after table missing");
    // The handle offset and the clip-path percentage must resolve against the same box, or
    // they drift apart everywhere except the exact middle.
    const frame = document.querySelector(".compare");
    const shot = document.querySelector(".compare-before");
    const after = document.querySelector(".compare-after");
    const near = (a, b) => Math.abs(a - b) <= 1;
    assert(near(frame.getBoundingClientRect().width, shot.getBoundingClientRect().width)
        && near(frame.getBoundingClientRect().width, after.getBoundingClientRect().width),
      `wipe frame ${frame.getBoundingClientRect().width} does not hug the render `
      + `${shot.getBoundingClientRect().width}/${after.getBoundingClientRect().width}`);

    document.querySelector('[data-workspace="chain"]').click();
    assert(document.querySelector(".node .thumb"), "node tiles carry no render thumbnail");
    assert(document.querySelector(".pvstage img") && !document.querySelector(".pvstage .compare"),
      "the chain workspace shows the comparison instead of the render");
    assert(document.querySelector(".tilehint") && !document.querySelector(".tilehint").textContent.includes("${"),
      "tile hint is missing or unrendered");
    assert(document.querySelector('[data-section="renders"] .renders img'), "renders block missing");
    assert(document.querySelector('[data-section="artefact"] .state'), "artefact block missing");
    assert(document.querySelector(".title-row .note"), "operation summary missing");
    assert(document.querySelector("#status-branches").textContent.trim()
        && document.querySelector("#status-vertices").textContent.trim()
        && document.querySelector("#status-schema").textContent.trim(), "status bar totals missing");
    assert(!document.querySelector(".tabs #start-screen") && document.querySelector(".status #start-screen"),
      "the start button is not in the status bar");
    // The outliner groups on forks, and the status bar counts them. One number, two readers.
    const branchGroups = [...document.querySelectorAll("#outliner .outgroup")].length - 1;
    const branchCount = Number((document.querySelector("#status-branches").textContent.match(/\d+/) || [0])[0]);
    assert(branchGroups === branchCount,
      `outliner shows ${branchGroups} branch groups, the status bar counts ${branchCount}`);
    assert(document.querySelector("#outliner .row.child"), "branch rows are not indented");

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
        # --use-mock-keychain: a headless Chrome otherwise asks macOS for the login keychain
        # on every launch, which turns a smoke run into a stream of password prompts.
        base = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--use-mock-keychain", "--password-store=basic", "--no-first-run",
                "--window-size=2048,1200", "--virtual-time-budget=1500"]
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
