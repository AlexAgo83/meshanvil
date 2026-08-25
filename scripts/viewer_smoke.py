#!/usr/bin/env python3
"""Exercise the generated viewer in Chrome without adding a browser framework."""
from __future__ import annotations

import argparse, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# adr_007: the served page can run a real command and show its real output. `list` needs
# neither Blender nor a Blender-backed project, so it runs for real here -- no mock, no stub.
SERVED_SMOKE = r"""
<script>
(() => {
  const fail = (message) => {
    document.body.dataset.smoke = "fail";
    document.body.appendChild(Object.assign(document.createElement("pre"), { id: "smoke-result", textContent: message }));
  };
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
    const run = async () => {
    const originalCount = DATA.reports.length;
    // The regression this guards: http.server never serves above the directory it is given,
    // so serving only work/viewer/ left every render under work/renders/ 404ing on a served
    // page while the identical file:// page (no server, no root to escape) loaded them fine.
    select(DATA.reports[0].id);   // the first report of a demo chain always carries a render
    await new Promise((done) => setTimeout(done, 100));
    const shown = document.querySelector("#pvstage img");
    assert(shown, "no render is shown on the served page");
    await new Promise((done) => {
      if (shown.complete) return done();
      shown.addEventListener("load", done, { once: true });
      shown.addEventListener("error", done, { once: true });
    });
    assert(shown.naturalWidth > 0, `a render 404'd on the served page: ${shown.src}`);

    // A refresh must not overrule the operator. Assigning the response wholesale put the
    // server's own active project back over a deliberate switch, which read as the page being
    // slow and was the page undoing a choice. Only a served page can prove it: on file:// the
    // fetch returns immediately and the assertion would pass having tested nothing.
    const others = (DATA.projects || []).filter((p) => p.name !== DATA.active);
    if (others.length) {
      const chosen = others[0].name;
      selectProject(chosen);
      const heads = () => [...document.querySelectorAll("#outliner .outgroup[aria-expanded]")]
        .map((h) => h.getAttribute("aria-expanded")).join(",");
      const foldBefore = heads();
      await refreshLive();
      assert(DATA.active === chosen,
        `a refresh replaced the selected project with ${DATA.active}`);
      assert(heads() === foldBefore, "a refresh changed the fold state");
      selectProject(others.length ? DATA.projects[0].name : DATA.active);
    }

    // The round trip only a served page can make: type a note, let it save, and find it in
    // the payload the next refresh brings back.
    const field = document.querySelector("[data-note-kind]");
    assert(field, "no note field on a served report");
    assert(field.dataset.noteKind === "reports", "the note field is not bound to a report");
    field.value = "written by the smoke";
    field.dispatchEvent(new Event("change", { bubbles: true }));
    for (let i = 0; i < 40 && !(DATA.notes && DATA.notes.reports[field.dataset.noteKey]); i++) {
      await new Promise((done) => setTimeout(done, 50));
    }
    assert(DATA.notes.reports[field.dataset.noteKey] === "written by the smoke",
      "a note was typed and never came back from the server");
    const noteKey = field.dataset.noteKey;
    await refreshLive();
    assert(DATA.notes.reports[noteKey] === "written by the smoke",
      "a note did not survive a refresh");
    // The refresh repainted the panel, so the field above is detached and its events no longer
    // reach the document. Ask for the current one.
    const again = document.querySelector("[data-note-kind]");
    assert(again && again !== field, "the refresh did not repaint the note field");
    assert(again.value === "written by the smoke", "the repainted field lost the note");
    again.value = "";
    again.dispatchEvent(new Event("change", { bubbles: true }));
    for (let i = 0; i < 40 && DATA.notes.reports[noteKey]; i++) {
      await new Promise((done) => setTimeout(done, 50));
    }
    assert(!DATA.notes.reports[noteKey], "clearing a note left it behind");

    // A chain can be named, and the name shows where the chain is named -- with the file it
    // starts from still visible beside it, because a name annotates an identity rather than
    // replacing it.
    const chainField = document.querySelector('[data-note-kind="chains"]');
    assert(chainField, "no chain-name field on a served report");
    const fileBefore = document.querySelector("#outliner .outgroup").textContent;
    chainField.value = "Named by the smoke";
    chainField.dispatchEvent(new Event("change", { bubbles: true }));
    for (let i = 0; i < 40 && !(DATA.notes.chains[chainField.dataset.noteKey]); i++) {
      await new Promise((done) => setTimeout(done, 50));
    }
    assert(DATA.notes.chains[chainField.dataset.noteKey] === "Named by the smoke",
      "a chain name was typed and never came back");
    outliner(); nodes();
    const headText = document.querySelector("#outliner .outgroup").textContent;
    assert(headText.includes("Named by the smoke"), `the chain header ignores its name: ${headText}`);
    const file = fileBefore.replace(/^\s*Chain\s+[-\u2014]\s*/, "").trim();
    assert(file && headText.includes(file),
      `naming a chain hid the file it starts from: ${headText}`);
    document.querySelector('[data-note-kind="chains"]').value = "";
    document.querySelector('[data-note-kind="chains"]').dispatchEvent(new Event("change", { bubbles: true }));
    for (let i = 0; i < 40 && DATA.notes.chains[chainField.dataset.noteKey]; i++) {
      await new Promise((done) => setTimeout(done, 50));
    }

    // What the first paint left out arrives when it is asked for. On the served page the
    // payload is thin by design, so selecting another project has to fetch its reports.
    assert(DATA.lazy === true, "the served payload is not the thin one");
    const servedProject = DATA.active;
    const other = (DATA.projects || []).find((p) => p.name !== DATA.active);
    if (other) {
      assert(other.reports.length === 0, "a project nobody selected still ships its reports");
      await selectProject(other.name);
      assert(DATA.reports.length > 0,
        `selecting ${other.name} fetched no reports`);
      assert(document.querySelectorAll("#outliner .row").length > 0,
        "the outliner stayed empty after the reports arrived");
      // Back to the served project: a refresh keeps whatever is selected now, so the live
      // assertions further down would otherwise watch the wrong one.
      await selectProject(servedProject);
      assert(DATA.active === servedProject, "could not return to the served project");
    }

    const controls = document.querySelector(".filectrls");
    assert(controls, "file controls missing on served page");
    assert(!controls.querySelector(".filelabel").textContent.includes("/"), "served file label shows a full path");
    assert(controls.querySelector('[data-file-open][aria-label="Open file"]:not(:disabled)'), "served Open file control missing or disabled");
    assert(controls.querySelector('[data-copy][aria-label="Copy this path"]'), "Copy path control missing accessible name");
    assert(controls.querySelector('[data-file-reveal][aria-label="Reveal file"]:not(:disabled)'), "served Reveal file control missing or disabled");

    document.querySelector('[data-run="list"]').closest("details").open = true;
    const button = document.querySelector('[data-run="list"]');
    assert(button, "the List operations row carries no data-run");
    button.click();
    const modal = document.querySelector("#result-modal");
    for (let waited = 0; waited < 5000 && modal.classList.contains("hidden"); waited += 100) {
      await new Promise((done) => setTimeout(done, 100));
    }
    assert(!modal.classList.contains("hidden"), "the operations modal never appeared");
    assert(!document.querySelector("details.menu[open]"), "a menu stayed open behind the operations modal");
    assert(modal.textContent.includes("scan_defects") && modal.textContent.includes("Bake every modifier"),
      "operations modal did not render translated structured content");
    assert(!modal.textContent.includes("{"), "operations modal shows raw output");
    document.querySelector("[data-result-close]").click();

    document.querySelector('[data-run="doctor"]').closest("details").open = true;
    document.querySelector('[data-run="doctor"]').click();
    for (let waited = 0; waited < 5000 && modal.classList.contains("hidden"); waited += 100) {
      await new Promise((done) => setTimeout(done, 100));
    }
    assert(modal.textContent.includes("Blender") || modal.textContent.includes("blender"), "setup modal missing structured requirements");
    assert(!modal.textContent.includes('"requirements"'), "setup modal shows JSON");
    document.querySelector("[data-result-close]").click();
    for (let waited = 0; waited < 6000 && DATA.reports.length === originalCount; waited += 100) {
      await new Promise((done) => setTimeout(done, 100));
    }
    assert(DATA.reports.length === originalCount + 1, "live refresh did not add the new report");
    if (window.__meshanvilStopLive) window.__meshanvilStopLive();
    document.body.dataset.smoke = "ok";
    document.body.appendChild(Object.assign(document.createElement("pre"), { id: "smoke-result", textContent: "ok" }));
  };
  run().catch((error) => fail(error && error.message ? error.message : String(error)));
})();
</script>
"""

SMOKE = r"""
<script>
(() => {
  const fail = (message) => {
    document.body.dataset.smoke = "fail";
    document.body.appendChild(Object.assign(document.createElement("pre"), { id: "smoke-result", textContent: message }));
  };
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
  const settled = () => Promise.all([...document.images].map((img) =>
    img.complete ? Promise.resolve() : new Promise((done) => {
      img.addEventListener("load", done, { once: true });
      img.addEventListener("error", done, { once: true });
    })));
  const run = async () => {
    const fileMenu = document.querySelector(".menu");
    fileMenu.open = true;
    assert(document.querySelector(".dropdown .grp") && document.querySelector(".cmdrow code"), "command menu surface missing");
    // The clipboard itself needs a focused, permissioned window that headless Chrome never
    // has -- both navigator.clipboard and execCommand("copy") reject here on principle, not
    // on a bug. What the smoke can prove is that clicking the row is safe either way.
    const listRow = document.querySelector('[data-copy="meshanvil list"]');
    assert(listRow && listRow.tagName === "BUTTON", "a menu command is not a clickable button");
    listRow.click();
    fileMenu.open = false;

    document.querySelector("#start-screen").click();
    assert(!document.querySelector("#splash").classList.contains("hidden"), "splash did not open");
    assert(document.querySelectorAll(".splashcols .scol").length === 3, "splash columns missing");
    assert(document.querySelector(".tpl code") && document.querySelector(".chk"), "splash command/check content missing");
    assert(document.querySelector("#splash").textContent.includes("tools/build_demo_chain.sh") && document.querySelector("#splash").textContent.includes("tools/build_figurine_chain.sh"), "demonstration build commands missing");
    assert(document.querySelector(".tpl").tagName === "BUTTON", "a splash template is not a clickable button");
    document.querySelector('[data-splash="close"]').click();
    assert(document.querySelector("#splash").classList.contains("hidden"), "splash did not close");

    // The regression this guards: the canvas draws one chain, the one the selection belongs
    // to, and the layout that positions it runs inside the draw. Placing once at load left
    // every other chain at left:undefined -- nine nodes stacked in the corner, one visible.
    // Two starts are needed to see it at all, which is why the smoke fixture carries a second.
    // Every chain shows where it starts. Without this the canvas drew a chain of inspections
    // as disconnected tiles: they share a source no operation produced, so none of them has a
    // parent and there was nothing to draw a link from.
    const cards = [...document.querySelectorAll("#nodes .node.source")];
    assert(cards.length >= 1, "no source card on a canvas that has a chain");
    const roots = DATA.reports.filter((r) => !(r.links && r.links.parent));
    const drawn = [...document.querySelectorAll("#nodes .node")].filter((n) => n.dataset.id);
    const drawnRoots = drawn.filter((n) => {
      const r = DATA.reports.find((x) => x.id === n.dataset.id);
      return r && !(r.links && r.links.parent);
    });
    assert(drawnRoots.length >= 1, "no root drawn to hang from a source card");
    assert(document.querySelectorAll("#noodles path").length >= drawnRoots.length,
      "fewer links than roots: a root is drawn with no source to come from");
    assert(!cards.some((c) => c.dataset.id),
      "a source card carries a report id: it is a file, not an operation");
    assert(!cards.some((c) => c.tagName === "BUTTON"),
      "a source card is clickable: nothing about it can be selected");

    // Folding belongs to the chain: it takes the chain's branches with it, headers included,
    // and only a chain header offers the control. Keyed by group first, which left a folded
    // chain's branches on screen with nothing above them.
    const heads = () => [...document.querySelectorAll("#outliner .outgroup")];
    const rowCount = () => document.querySelectorAll("#outliner .row").length;
    assert(heads().every((h) => h.tagName === "BUTTON" || !h.querySelector(".ogtri")),
      "a header that is not a button still shows a fold control");
    assert(heads().some((h) => h.tagName !== "BUTTON"),
      "the fixture has no branch header, so this cannot prove branches lost their control");
    for (const head of heads()) {
      if (head.tagName !== "BUTTON") continue;
      assert(!/^Branch/.test(head.textContent.trim()), "a branch header is a fold button");
    }

    const chainHead = heads().find((h) => h.tagName === "BUTTON");
    const rowsBefore = rowCount();
    const headsBefore = heads().length;
    chainHead.click();
    const afterFold = heads();
    assert(afterFold[0].getAttribute("aria-expanded") === "false", "a folded chain reads as expanded");
    assert(afterFold.length < headsBefore,
      "folding a chain kept every header: its branch headers stayed behind");
    assert(rowCount() < rowsBefore, "folding a chain hid none of its rows");
    afterFold[0].click();
    assert(rowCount() === rowsBefore, "unfolding did not bring the rows back");
    assert(heads().length === headsBefore, "unfolding did not bring the branch headers back");
    assert(heads()[0].getAttribute("aria-expanded") === "true", "an unfolded chain reads as collapsed");

    // A chain header is the one that folds; matching on the word "Chain" tied this to a
    // label, and it broke the day the label stopped repeating the word in front of a name.
    const startRows = [...document.querySelectorAll("#outliner .outgroup.fold")];
    assert(startRows.length >= 2, "the smoke fixture must carry two starts to exercise the canvas");
    for (const id of ["001", "900"]) {
      const row = [...document.querySelectorAll("#outliner .row")].find((r) => r.dataset.id === id);
      assert(row, `no outliner row for ${id}`);
      row.click();
      const drawn = [...document.querySelectorAll("#nodes .node")];
      assert(drawn.length, `selecting ${id} drew no node`);
      assert(drawn.some((node) => node.dataset.id === id), `selecting ${id} did not draw ${id}`);
      const spots = new Set(drawn.map((node) => `${node.style.left},${node.style.top}`));
      assert(spots.size === drawn.length,
        `selecting ${id} stacked ${drawn.length} nodes on ${spots.size} positions`);
      assert(![...spots].some((spot) => spot.includes("undefined")),
        `selecting ${id} left a node unplaced`);
    }

    // The regression this guards: opening the splash from the File menu's own "Start screen"
    // row is a click *inside* that open <details>, so the generic "click outside a menu closes
    // it" check never ran for it -- the dropdown used to stay open, visible on top of the modal.
    fileMenu.open = true;
    document.querySelector('[data-splash="open"]').click();
    assert(!document.querySelector("#splash").classList.contains("hidden"), "splash did not open from the File menu");
    assert(!fileMenu.open, "the File menu stayed open behind the splash it just opened");
    document.querySelector('[data-splash="close"]').click();

    document.querySelector('[data-workspace="runbooks"]').click();
    assert(document.querySelector(".app").dataset.workspace === "runbooks", "runbooks workspace did not activate");
    assert(document.querySelector(".rbbody .rbrow"), "runbooks primary rows missing");
    assert(document.querySelector(".rbpurpose") && document.querySelector(".rbapplied"), "runbook row details missing");
    assert(document.querySelector(".rbcols"), "runbooks column header missing");
    assert(document.querySelector("#graph-name").textContent.toLowerCase().includes("runbook"),
      "runbooks table is still filed under the node editor header");
    document.querySelector(".rbbody .rbrow").click();
    const doccontent = document.querySelector("#props .doccontent");
    assert(doccontent, "runbook row did not open its content");
    // A runbook renders as formatted HTML, not raw Markdown source: real heading/list
    // elements, and no literal '##'/'- '/backtick syntax left over in the visible text.
    assert(doccontent.querySelector("h2, h3, h4"), "runbook content has no rendered heading");
    assert(doccontent.querySelector("li"), "runbook content has no rendered list item");
    assert(!/^#{1,6}\s|^[-*]\s|`[^`]+`/m.test(doccontent.textContent),
      "runbook content still shows literal Markdown syntax");

    assert(/^v\d+\.\d+\.\d+$/.test(document.querySelector("#app-version").textContent), "app version missing from Help");
    const reportMenu = document.querySelectorAll(".menubar summary")[2];
    const beforeText = reportMenu.textContent;
    document.querySelector('[data-lang="fr"]').click();
    assert(reportMenu.textContent !== beforeText, "language switch did not repaint the menu bar");
    assert(document.querySelector('[data-lang="fr"]').getAttribute("aria-selected") === "true",
      "the chosen language does not stay marked selected");
    document.querySelector('[data-lang="en"]').click();
    assert(reportMenu.textContent === beforeText, "switching back to English did not restore the menu bar");

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
    const cband = document.querySelector("#pvmeta");
    assert(cband.scrollWidth <= cband.clientWidth + 1,
      `compare band overflows: content ${cband.scrollWidth} in ${cband.clientWidth}`);
    const wrap = document.querySelector("#pvmeta .tablewrap");
    assert(wrap && wrap.scrollWidth <= wrap.clientWidth + 1,
      "compare table does not fit its band and would hide the delta column");
    // The handle offset and the clip-path percentage must resolve against the same box, or
    // they drift apart everywhere except the exact middle.
    await settled();
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
    // The render must fit the panel, not be cropped by it, and the band beside it must hold
    // its own content: an auto-sized grid track took its height from the image, so the
    // image's max-height had nothing definite to resolve against and the bottom was cut.
    await settled();
    const fileControls = document.querySelector(".filectrls");
    assert(fileControls, "file controls missing from file page");
    assert(!fileControls.querySelector(".filelabel").textContent.includes("/"), "file page label shows a full path");
    assert(fileControls.querySelector('[data-copy][aria-label="Copy this path"]'), "file page lost copy path");
    assert(fileControls.querySelector('[data-file-open]:disabled') && fileControls.querySelector('[data-file-reveal]:disabled'),
      "file page presents Open or Reveal as working controls");
    const stage = document.querySelector("#pvstage"), band = document.querySelector("#pvmeta");
    assert(document.querySelector("#pvstage img").naturalWidth > 0, "the render did not load");
    assert(stage.scrollHeight <= stage.clientHeight + 1,
      `render is cropped: stage content ${stage.scrollHeight} in ${stage.clientHeight}`);
    assert(band.scrollWidth <= band.clientWidth + 1,
      `provenance band overflows: content ${band.scrollWidth} in ${band.clientWidth}`);
    const shown = document.querySelector("#pvstage img");
    assert(Math.abs(shown.width / shown.height - shown.naturalWidth / shown.naturalHeight) < 0.02,
      "render is not displayed at its own aspect ratio");
    assert(document.querySelector('[data-section="renders"] .renders img'), "renders block missing");
    assert(document.querySelector('[data-section="artefact"] .state'), "artefact block missing");
    assert(document.querySelector(".title-row .note"), "operation summary missing");
    assert(document.querySelector("#status-branches").textContent.trim()
        && document.querySelector("#status-vertices").textContent.trim()
        && document.querySelector("#status-schema").textContent.trim(), "status bar totals missing");
    assert(document.querySelector(".status #start-screen"), "the start button is not in the status bar");
    // The outliner groups on forks, and the status bar counts them. One number, two readers.
    // Every start opens a group of its own too, so those are discounted rather than assumed
    // to be exactly one: the count broke the day a second chain appeared in the same project.
    const allGroups = [...document.querySelectorAll("#outliner .outgroup")];
    const starts = allGroups.filter((group) => group.classList.contains("fold"));
    const branchGroups = allGroups.length - starts.length;
    const branchCount = Number((document.querySelector("#status-branches").textContent.match(/\d+/) || [0])[0]);
    assert(branchGroups === branchCount,
      `outliner shows ${branchGroups} branch groups, the status bar counts ${branchCount}`);
    assert(document.querySelector("#outliner .row.child"), "branch rows are not indented");

    // Every report through every panel: a path or a wide number in one report is enough to
    // push a panel wider than itself, and only that report shows it.
    const panels = [".propscroll", "#pvmeta", "#outliner", "#nodes"];
    const spilled = [];
    for (const workspace of ["chain", "compare", "runbooks"]) {
      document.querySelector(`[data-workspace="${workspace}"]`).click();
      for (const item of DATA.reports) {
        select(item.id);
        await settled();
        for (const sel of panels) {
          const box = document.querySelector(sel);
          if (box && box.clientWidth && box.scrollWidth > box.clientWidth + 1) {
            spilled.push(`${workspace}/${item.id} ${sel} ${box.clientWidth}<${box.scrollWidth}`);
          }
        }
      }
    }
    assert(!spilled.length, `panels scroll sideways: ${spilled.slice(0, 4).join("; ")}`);
    document.querySelector('[data-workspace="chain"]').click();
    select(DATA.reports[DATA.reports.length - 1].id);
    await settled();

    // The switcher, on a page built with one project. The furniture must not show, and the
    // machinery must still work -- a second project is fabricated here rather than required
    // on disk, because what is under test is the page, not the operator's directories.
    // The filter set earlier is still on; it would hide the rows this block counts.
    const box = document.querySelector("#outliner-filter");
    box.value = "";
    box.dispatchEvent(new Event("input", { bubbles: true }));

    const pick = document.getElementById("project-pick");
    const chooser = document.getElementById("project-select");
    assert(pick && chooser, "project switcher missing from the page");
    assert(DATA.projects && DATA.projects.length >= 1, "no project in the viewer data");
    assert(document.getElementById("project-name").textContent.trim() === DATA.active,
      "the top bar does not name the active project");
    if (DATA.projects.length === 1) {
      assert(pick.classList.contains("hidden"),
        "a single project should not show an empty chooser");
    }

    const only = DATA.projects[0];
    const counted = document.querySelector("#status-counts").textContent;
    DATA.projects.push({ name: "__smoke__", path: "/tmp/__smoke__", ops_exists: true,
                         reports: [only.reports[0]] });
    paintProjects();
    assert(!pick.classList.contains("hidden"), "two projects did not reveal the chooser");
    assert(chooser.options.length === DATA.projects.length, "the chooser lists the wrong count");

    selectProject("__smoke__");
    assert(DATA.active === "__smoke__", "selecting a project did not activate it");
    assert(document.querySelectorAll("#outliner .row").length === 1,
      "the outliner still shows the other project's chain");
    assert(document.querySelector("#status-counts").textContent !== counted,
      "the totals still describe the project that is not shown");

    selectProject(only.name);
    DATA.projects.pop();
    paintProjects();
    assert(DATA.active === only.name && document.querySelector("#status-counts").textContent === counted,
      "switching back did not restore the page");
    await settled();

    // A page with no server shows what is there and offers nothing to type into.
    assert(DATA.lazy !== true, "the filesystem snapshot is the thin payload and has nothing to fetch");
    assert(!document.querySelector("[data-note-kind]"),
      "a page opened from the filesystem offers a note field it cannot save");
    assert(document.querySelector(".noteblock"), "the note block is missing entirely");

    document.querySelector('[data-section-goto="measurements"]').click();
    assert(document.querySelector('[data-section-goto="measurements"]').getAttribute("aria-selected") === "true", "report rail did not select measurements");
    document.body.dataset.smoke = "ok";
    document.body.appendChild(Object.assign(document.createElement("pre"), { id: "smoke-result", textContent: "ok" }));
  };
  run().catch((error) => fail(error && error.message ? error.message : String(error)));
})();
</script>
"""


def second_start(data_js: Path) -> None:
    """Give the fixture a second chain start, which the demo chain does not have.

    The outliner groups by start and the canvas draws one start at a time; with a single
    root every such rule is trivially satisfied, and the layout bug that stacked a whole
    chain in the corner was invisible until a second start existed to switch to.
    """
    text = data_js.read_text(encoding="utf-8")
    prefix, _, body = text.partition("=")
    payload = json.loads(body.strip().rstrip(";"))
    first = payload["reports"][0]
    clone = json.loads(json.dumps(first))
    clone["id"] = "900"
    clone["input"] = {**clone.get("input", {}), "path": "/smoke/second-source.obj"}
    clone["links"] = {**clone.get("links", {}), "parent": None, "parent_source": None}
    payload["reports"].append(clone)
    # projects[] carries its own copy of the same list, and switching projects reads that one:
    # injecting into only one of the two makes the operation count change under a round trip.
    for project in payload.get("projects", []):
        if project.get("name") == payload.get("active"):
            project["reports"].append(clone)
    data_js.write_text(f"{prefix}= {json.dumps(payload, indent=1)};\n", encoding="utf-8")


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


def check_served(chrome: str, project: Path) -> None:
    """adr_007 over a real socket: a real `--serve` subprocess, a real HTTP request from a
    real headless Chrome, a real `bin/meshanvil list` run. `--virtual-time-budget` still
    applies here -- Chrome keeps servicing real sockets while it advances virtual time, it
    just needs enough budget for a real subprocess round trip, not the 1.5s the offline pass
    uses."""
    environment = {**os.environ, "MESHANVIL_PROJECT": str(project), "PYTHONUNBUFFERED": "1"}
    injected = project / "work" / "ops" / "999_smoke_live.json"
    injected.unlink(missing_ok=True)
    server = subprocess.Popen(
        [sys.executable, str(ROOT / "bin" / "meshanvil"), "view", "--serve", "--no-open"],
        cwd=ROOT, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        port, deadline = None, time.time() + 15
        while time.time() < deadline:
            line = server.stdout.readline() if server.stdout else ""
            if not line:
                if server.poll() is not None:
                    break
                continue
            match = re.search(r":(\d+)/", line)
            if match:
                port = int(match.group(1))
                break
        if port is None:
            raise SystemExit("served viewer did not report a port in time")
        served_dir = project / "work" / "viewer"
        smoke_page = served_dir / "served_smoke.html"
        smoke_html = (served_dir / "index.html").read_text(encoding="utf-8")
        smoke_html = re.sub(r'(<script src="viewer\.js[^"]*"></script>)',
                            '<script>window.EventSource = undefined;</script>\n\\1', smoke_html)
        smoke_page.write_text(smoke_html.replace("</body>", SERVED_SMOKE + "\n</body>"), encoding="utf-8")
        try:
            url = f"http://127.0.0.1:{port}/viewer/served_smoke.html"
            live = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--use-mock-keychain", "--password-store=basic", "--no-first-run",
                    "--window-size=1200,900", "--virtual-time-budget=12000"]
            dom = subprocess.Popen([*live, "--dump-dom", url], text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            smoke_report = next((project / "work" / "ops").glob("*.json"))
            time.sleep(1)
            data = json.loads(smoke_report.read_text(encoding="utf-8"))
            data["id"] = "999"
            data["operation"] = "smoke_live"
            injected.write_text(json.dumps(data), encoding="utf-8")
            try:
                stdout, stderr = dom.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                dom.kill()
                stdout, stderr = dom.communicate()
                raise
            finally:
                injected.unlink(missing_ok=True)
            if dom.returncode:
                raise SystemExit((stderr or stdout or "Chrome did not load the served smoke page").strip())
            if 'data-smoke="ok"' not in stdout:
                raise SystemExit((stdout or "the served page did not confirm real execution").strip())
        finally:
            smoke_page.unlink(missing_ok=True)
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshot", type=Path, default=Path(tempfile.gettempdir()) / "meshanvil-viewer-smoke.png")
    args = parser.parse_args()

    chrome = chrome_path()
    if not chrome:
      raise SystemExit("Chrome/Chromium not found; set PATH or install Google Chrome.")

    run([sys.executable, str(ROOT / "scripts" / "fixture_check.py")])

    # The demonstrations are projects now, so the page under test is one of theirs. Building
    # it here would put a Blender chain inside a browser check; requiring it keeps the two
    # apart and names the command when it is missing.
    project = ROOT / "work" / "demo" / "vehicle"
    if not sorted((project / "work" / "ops").glob("*.json")):
        raise SystemExit(f"no demonstration to smoke: run tools/build_demo_chain.sh "
                         f"(expected reports under {project}/work/ops)")
    environment = {**os.environ, "MESHANVIL_PROJECT": str(project)}
    subprocess.run([sys.executable, str(ROOT / "bin" / "meshanvil"), "view", "--file", "--no-open"],
                   cwd=ROOT, env=environment, text=True, capture_output=True, check=True)

    with tempfile.TemporaryDirectory(prefix="meshanvil-viewer-smoke-") as tmp:
        tmp_root = Path(tmp)
        shutil.copytree(project / "work" / "viewer", tmp_root / "viewer")
        second_start(tmp_root / "viewer" / "data.js")
        renders = project / "work" / "renders"
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

    check_served(chrome, project)

    print(f"viewer-smoke: ok ({args.screenshot})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
