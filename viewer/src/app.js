/* The viewer reads. It starts no process and writes nothing -- adr_003. adr_007 carves out
   one exception: a page opened via --serve may POST to that same server's /run endpoint to
   execute a closed set of commands (RUNNABLE in meshanvil/viewer.py), never a string this
   page invents. A file:// page has no server to reach and keeps copying, as before.
   Everything it renders comes from a report, and a report is data written by CAD files,
   so every value is escaped before it reaches the page. */
// @ts-check
"use strict";

import { startLiveRefresh } from "./live.js";
import { esc, mdToHtml } from "./markdown.js";
import { rootOf, isOrphan, groupKey } from "./chains.js";

/** The report contract, as adr_001 defines it. Named OperationReport rather than Report:
 * the DOM already has a Report interface, and the collision silently made every property
 * resolve against it.
 * @typedef {{id:string, chain:string, kind:string, status:string, operation:string,
 *   schema_version:number, error?:string,
 *   params:Object, tool:Object, input:Object, output?:Object, before?:Object, after?:Object,
 *   measured?:Object, bbox_delta_mm?:Object, warnings:string[], findings?:Object[],
 *   renders?:Object[], comparisons?:{view:string,before_url:string,after_url:string,camera:string}[], links:{parent:string|null, parent_source:string|null, docs:string[]},
 *   duration_s:number, created_at:string,
 *   _x?:number, _y?:number}} OperationReport */

let DATA = /** @type {{reports: OperationReport[], generated_at: string, root: string,
 *   lang: string, strings: Object<string,string>, catalogs?: Object<string,Object<string,string>>,
 *   version?: string, run_token?: string|null, docs?: Object<string,Object>, runbooks?: Object[], doctor?: Object, ops_exists?: boolean, files?: {id:string,path:string}[]}} */ (
  /** @type {any} */ (window).MESHANVIL
  || { reports: [], generated_at: "", root: "", lang: "en", strings: {} });
/** @type {any} */ (window).DATA = DATA;

/** adr_007: a served page has a token and a real origin to POST to; a file:// page has
    neither, and location.protocol says so directly rather than by probing a capability. */
let SERVED = location.protocol !== "file:";

/** Same catalogues as the command line, all of them shipped in data.js so Help can switch
    language without a rebuild -- the page reads, adr_003, it does not ask the engine again. */
let lang = DATA.lang || "en";
let strings = mergedCatalog(lang);
function mergedCatalog(code) {
  const books = DATA.catalogs;
  return books ? { ...(books.en || {}), ...(books[code] || {}) } : (DATA.strings || {});
}
function t(key, values) {
  let text = strings[key] || key;
  for (const [name, value] of Object.entries(values || {})) {
    text = text.split(`{${name}}`).join(String(value));
  }
  return text;
}

/** @type {Map<string, OperationReport>} */
let BY_ID = new Map(DATA.reports.map((r) => [r.id, r]));
let current = DATA.reports.length ? DATA.reports[DATA.reports.length - 1].id : null;
let currentDoc = null;
let view = 0;
let wipe = 50;
let start = !DATA.reports.length;
let workspace = "chain";
let filterText = "";

const num = (v) => (v === null || v === undefined ? "—" : Number(v).toLocaleString("en-US"));

/** What the operation is for, from the manifest catalogue. Absent is normal, not an error. */
function summaryOf(operation) {
  const key = `operation.${operation}.summary`;
  const text = t(key);
  return text === key ? "" : text;
}

/** present, pruned or pinned -- the artefact state drives the node dot and the outliner dot. */
function artefactState(report) {
  const output = report.output || null;
  if (!output) return report.status;
  if (output.pinned) return "pinned";
  return output.state === "pruned" ? "pruned" : report.status;
}

/* ---------- projects ----------
   The page holds them all and shows one. Drawing two unrelated chains in one graph would
   merge their outliner groups and sum totals across subjects that share nothing, so the
   switcher selects rather than combines. */
function projectEntries() {
  return /** @type {any[]} */ (/** @type {any} */ (DATA).projects || []);
}

function selectProject(name) {
  const entry = projectEntries().find((p) => p.name === name);
  if (!entry) return;
  /** @type {any} */ (DATA).active = entry.name;
  DATA.reports = entry.reports;
  DATA.ops_exists = entry.ops_exists;
  BY_ID = new Map(DATA.reports.map((r) => [r.id, r]));
  current = DATA.reports.length ? DATA.reports[DATA.reports.length - 1].id : null;
  currentDoc = null;
  view = 0;
  start = !DATA.reports.length;
  paintProjects();
  paintTotals();
  outliner(); nodes(); props(); preview();
}

async function fetchData() {
  if (!SERVED) return false;
  const response = await fetch(`${location.origin}/api/data`, { cache: "no-store" });
  if (!response.ok) return false;
  DATA = await response.json();
  /** @type {any} */ (window).DATA = DATA;
  SERVED = location.protocol !== "file:" && !!DATA.run_token;
  lang = DATA.lang || lang || "en";
  strings = mergedCatalog(lang);
  BY_ID = new Map(DATA.reports.map((r) => [r.id, r]));
  if (!current || !BY_ID.has(current)) current = DATA.reports.length ? DATA.reports[DATA.reports.length - 1].id : null;
  start = !DATA.reports.length;
  paintTotals();
  applyStaticStrings();
  paintProjects();
  outliner(); nodes(); props(); preview();
  return true;
}

async function refreshLive() {
  const started = performance.now();
  try { await fetchData(); }
  catch { /* the next event or timer gets another chance */ }
  return performance.now() - started;
}

function paintProjects() {
  const entries = projectEntries();
  const pick = document.getElementById("project-pick");
  const select = /** @type {HTMLSelectElement} */ (document.getElementById("project-select"));
  const active = /** @type {any} */ (DATA).active;
  document.getElementById("project-name").textContent = active || "—";
  // One project needs no chooser, and an empty one would only be furniture.
  pick.classList.toggle("hidden", entries.length < 2);
  if (entries.length < 2) return;
  select.innerHTML = entries.map((entry) =>
    `<option value="${esc(entry.name)}"${entry.name === active ? " selected" : ""}>${esc(entry.name)} · ${
      esc(t("ui.project_reports", { count: entry.reports.length }))}</option>`).join("");
}

/* ---------- roots: a report with no parent starts its own chain ---------- */
/** The reports drawn on the canvas: the chain the selection belongs to, and only that one. */
function onCanvas() {
  const root = current ? rootOf(BY_ID, current) : null;
  if (!root) return DATA.reports;
  return DATA.reports.filter((report) => rootOf(BY_ID, report.id) === root);
}

/* ---------- layout: depth from the parent chain, siblings stacked ----------
   Called by the draw, not once at load: which reports are on the canvas follows the
   selection now, and a chain that was never placed draws every node at left:undefined. */
function place() {
  const shown = onCanvas();
  const depth = new Map(), row = new Map();
  for (const report of shown) {
    const parent = report.links && report.links.parent;
    const level = parent && depth.has(parent) ? depth.get(parent) + 1 : 0;
    depth.set(report.id, level);
    const used = row.get(level) || 0;
    row.set(level, used + 1);
    report._x = 20 + level * 232;
    report._y = 20 + used * 196;
  }
  return shown;
}

/* ---------- outliner ---------- */
function outliner() {
  if (start) {
    document.getElementById("outliner").innerHTML = `<div class="blank"><span class="big">${esc(t("ui.start_title"))}</span>
      <span>${esc(t("ui.start_outliner"))}</span></div>`;
    return;
  }
  if (workspace === "runbooks") {
    const runbooks = (DATA.runbooks || []).filter((doc) => `${doc.ref} ${doc.title}`.toLowerCase().includes(filterText));
    document.getElementById("outliner").innerHTML = `<div class="outgroup">${esc(t("ui.runbooks"))}</div>`
      + (runbooks.map((doc) => `<button type="button" class="row" data-doc="${esc(doc.ref)}"
        aria-current="${doc.ref === currentDoc}"><span class="tri">▾</span><span class="kindicon inspection">N</span>
        <span class="label">${esc(doc.title)}</span><span class="dot ${doc.status === "Done" ? "ok" : "pruned"}"></span></button>`).join("")
      || `<div class="blank"><span>${esc(t("ui.not_applied"))}</span></div>`);
    return;
  }
  const chains = groups();
  let html = "";
  let first = true;
  for (const [fork, reports] of chains) {
    const parent = BY_ID.get(fork);
    const root = reports[0] && !reports[0].links.parent ? reports[0] : null;
    // Written out rather than folding the key into one t(): the i18n check reads literals.
    let label = t("ui.branch_named", { name: parent ? `${parent.id} ${parent.operation}` : fork });
    if (root && isOrphan(root)) label = t("ui.orphan_named", { name: chainName(reports) });
    else if (root) label = t("ui.chain_named", { name: chainName(reports) });
    const indent = root ? "" : " child";
    first = false;
    html += `<div class="outgroup">${esc(label)}</div>`;
    for (const report of reports) {
      if (!`${report.id} ${report.operation}`.toLowerCase().includes(filterText)) continue;
      const kind = report.status === "failed" ? "failed" : report.kind;
      const state = artefactState(report);
      const glyph = report.kind === "inspection" ? "i" : "T";
      html += `<button type="button" class="row${indent}" data-id="${esc(report.id)}"
        aria-current="${report.id === current}">
        <span class="tri">▾</span>
        <span class="kindicon ${esc(kind)}">${report.status === "failed" ? "×" : glyph}</span>
        <span class="label"><span class="idx">${esc(report.id)}</span> ${esc(report.operation)}</span>
        <span class="dot ${esc(state)}"></span></button>`;
    }
  }
  document.getElementById("outliner").innerHTML =
    html || `<div class="blank"><span class="big">${esc(t("ui.no_operation_yet"))}</span>
      <span>${esc(t("ui.reports_appear"))}</span></div>`;
}

/** Reports grouped by the fork they descend from, in identity order. */
function groups() {
  const children = new Map();
  for (const report of DATA.reports) {
    const parent = report.links && report.links.parent;
    if (parent) children.set(parent, (children.get(parent) || 0) + 1);
  }
  const groupOf = new Map(), result = new Map();
  for (const report of DATA.reports) {
    // A fork opens a group, a root opens its own; anything else continues its parent's.
    const key = groupKey(report, children, groupOf);
    groupOf.set(report.id, key);
    if (!result.has(key)) result.set(key, []);
    result.get(key).push(report);
  }
  return result;
}

/** A chain is named after the file it started from; the identity is already in the row. */
function chainName(reports) {
  const root = reports.find((r) => !(r.links && r.links.parent)) || reports[0];
  const path = String((root.input || {}).path || "");
  return path.split("/").pop().replace(/\.blend$/, "") || root.chain || root.id;
}

function docFromRef(ref) {
  // list-docs (DATA.runbooks) gives title/status/kind for every runbook, applied or not.
  // read-doc (DATA.docs) gives the full content, but only for refs a report or a runbook
  // actually names. A runbook read from the list needs both merged, content on top.
  const meta = (DATA.runbooks || []).find((item) => item.ref === ref);
  const full = (DATA.docs || {})[ref];
  return { ref, ...meta, ...full };
}

function docPurpose(doc) {
  const sections = doc.sections || {};
  const first = doc.purpose || (sections.Trigger || sections.Overview || sections.Procedure || [])[0];
  return String(first || doc.content || t("ui.runbook_no_summary")).replace(/^[-\d. ]+/, "").slice(0, 180);
}

function fileId(path) {
  const hit = (DATA.files || []).find((item) => item.path === path);
  return hit ? hit.id : "";
}

function fileControls(path, label) {
  const id = fileId(path);
  const served = SERVED && id;
  const disabled = served ? "" : " disabled";
  return `<span class="filectrls"><span class="filelabel">${label}</span>
    <button type="button" class="iconbtn" data-file-open="${esc(id)}"${disabled} aria-label="${esc(t("ui.open_file"))}" title="${esc(t("ui.open_file"))}">↗</button>
    <button type="button" class="iconbtn" data-copy="${esc(path)}" aria-label="${esc(t("ui.copy_path"))}" title="${esc(t("ui.copy_path"))}">⧉</button>
    <button type="button" class="iconbtn" data-file-reveal="${esc(id)}"${disabled} aria-label="${esc(t("ui.reveal_file"))}" title="${esc(t("ui.reveal_file"))}">⌖</button>
  </span>`;
}

/** A runbook applied by a dozen operations turned one table row into a column of pills and
    pushed the rest of the table off screen. Two name the runbook's use; the count carries
    the rest, and the row itself opens the full list. */
const APPLIED_SHOWN = 2;
const shown = (applied) => applied.slice(0, APPLIED_SHOWN);

function runbookRows() {
  const docs = (DATA.runbooks || []).filter((doc) => `${doc.ref} ${doc.title}`.toLowerCase().includes(filterText));
  const head = `<div class="rbcols"><span>${esc(t("ui.rb_col_doc"))}</span>
    <span>${esc(t("ui.rb_col_settles"))}</span><span>${esc(t("ui.rb_col_applied"))}</span></div>`;
  return (docs.length ? head : "") + (docs.map((doc) => {
    const full = docFromRef(doc.ref);
    const applied = DATA.reports.filter((report) => (report.links.docs || []).includes(doc.ref));
    return `<button type="button" class="rbrow" data-doc="${esc(doc.ref)}" aria-current="${doc.ref === currentDoc}">
      <span class="rbhead"><span class="kindicon inspection">N</span><span>${esc(shortRef(doc.ref))}</span><b>${esc(doc.title || doc.ref)}</b></span>
      <span class="rbpurpose">${esc(docPurpose(full))}</span>
      <span class="rbapplied">${applied.length ? shown(applied).map((report) =>
        `<span class="docref docref--op"><code>${esc(report.id)}</code><span class="rtitle">${esc(report.operation)}</span></span>`).join("")
        + (applied.length > APPLIED_SHOWN
          ? `<span class="docref docref--more">${esc(t("ui.applied_more", { count: applied.length - APPLIED_SHOWN }))}</span>`
          : "")
        : `<span class="unapplied">${esc(t("ui.not_applied"))}</span>`}</span>
    </button>`;
  }).join("") || `<div class="blank"><span class="big">${esc(t("ui.runbooks"))}</span><span>${esc(t("ui.runbook_empty"))}</span></div>`);
}

/* ---------- node editor ---------- */
/** One panel, two workspaces: the header says which, so the runbooks table is not
    filed under "Node Editor" the way it was. */
function graphHead(icon, name, scope) {
  document.getElementById("graph-icon").textContent = icon;
  document.getElementById("graph-name").textContent = name;
  document.getElementById("graph-scope").textContent = scope;
}

function nodes() {
  if (start) {
    document.getElementById("nodes").innerHTML = `<div class="start-card"><h2>${esc(t("ui.start_title"))}</h2>
      <p>${esc(t("ui.start_intro"))}</p><ol class="start-steps">
      <li>${esc(t("ui.start_demo"))} <code>tools/build_demo_chain.sh</code></li>
      <li>${esc(t("ui.start_inspect"))} <code>meshanvil init &lt;directory&gt;</code></li>
      <li>${esc(t("ui.start_prepare"))} <code>meshanvil run scan_defects &lt;file&gt;.blend</code></li></ol></div>`;
    const canvas = document.getElementById("canvas"); canvas.style.width = "860px"; canvas.style.height = "420px";
    document.getElementById("noodles").innerHTML = "";
    return;
  }
  if (workspace === "runbooks") {
    graphHead("▤", t("ui.runbooks"), "logics/runbook");
    document.getElementById("nodes").innerHTML = `<div class="rbbody">${runbookRows()}</div>`;
    const canvas = document.getElementById("canvas"); canvas.style.width = "100%"; canvas.style.height = "100%";
    document.getElementById("noodles").innerHTML = "";
    return;
  }
  const shown = place();
  graphHead("⬡", t("ui.node_editor"),
    shown.length ? `chain / ${chainName(shown)}` : "links.parent");
  let html = "";
  for (const report of shown) {
    const kind = report.status === "failed" ? "failed" : report.kind;
    const state = artefactState(report);
    const lines = headline(report).map(([key, value]) =>
      `<div class="nline"><span>${esc(key)}</span><b>${esc(value)}</b></div>`).join("");
    // The tile is the operation's own verification render -- renders[0], or the one it flagged.
    const tile = (report.renders || []).find((r) => r.tile) || (report.renders || [])[0];
    const thumb = tile ? `<img class="thumb" src="${esc(tile.url)}" alt="${esc(t("ui.render_alt", {
      view: tile.view, operation: report.operation }))}" loading="lazy">` : "";
    const foot = [report.status === "failed" ? t("ui.failed_kept_node") : report.kind,
                  report.output ? report.output.state : null].filter(Boolean).join(" · ");
    html += `<button type="button" class="node ${esc(kind)}" data-id="${esc(report.id)}"
        aria-current="${report.id === current}" style="left:${report._x}px;top:${report._y}px">
      <div class="nhead"><span class="nidx">${esc(report.id)}</span>${esc(report.operation)}</div>
      <div class="nbody">${lines}</div>
      ${thumb}
      <div class="nfoot"><span class="dot ${esc(state)}"></span>${esc(foot)}</div>
    </button>`;
  }
  document.getElementById("nodes").innerHTML = html;
  const canvas = document.getElementById("canvas");
  canvas.style.width = Math.max(860, ...shown.map((r) => r._x + 240)) + "px";
  canvas.style.height = Math.max(420, ...shown.map((r) => r._y + 200)) + "px";
  noodles(shown);
}

function headline(report) {
  if (report.kind === "transform" && report.after) {
    return [["vertices", `${num(report.before.vertices)} → ${num(report.after.vertices)}`],
            ["shells", `${num(report.before.shells)} → ${num(report.after.shells)}`]];
  }
  const measured = report.measured || {};
  return [["objects", num(measured.objects)], ["vertices", num(measured.vertices)]];
}

function noodles(shown) {
  let path = "";
  for (const report of shown) {
    const parent = report.links && report.links.parent && BY_ID.get(report.links.parent);
    if (!parent) continue;
    const x1 = parent._x + 186, y1 = parent._y + 56, x2 = report._x, y2 = report._y + 34;
    const bend = Math.max(40, (x2 - x1) / 2);
    const failed = report.status === "failed";
    path += `<path d="M${x1} ${y1} C${x1 + bend} ${y1}, ${x2 - bend} ${y2}, ${x2} ${y2}"
        fill="none" stroke="${failed ? "#6b4040" : "#5c5c5c"}" stroke-width="2"
        ${failed ? 'stroke-dasharray="5 4"' : ""}/>
      <circle cx="${x1}" cy="${y1}" r="3.5" fill="#8a8a8a"/>
      <circle cx="${x2}" cy="${y2}" r="3.5" fill="${failed ? "#a35a5a" : "#8a8a8a"}"/>`;
  }
  document.getElementById("noodles").innerHTML = path;
}

/* ---------- version drift ----------
   A remesh does not produce the same mesh across two Blender versions. Two reports made by
   different engines are not comparable, and saying nothing would let them be compared. */
function engineVersions() {
  const seen = new Map();
  for (const report of DATA.reports) {
    const key = `${(report.tool || {}).engine_version || "?"}`;
    if (!seen.has(key)) seen.set(key, []);
    seen.get(key).push(report.id);
  }
  return seen;
}

function driftNotice(report) {
  const versions = engineVersions();
  if (versions.size < 2) return "";
  const mine = `${(report.tool || {}).engine_version || "?"}`;
  const others = [...versions.keys()].filter((v) => v !== mine);
  return `<div class="pblock"><div class="pbody">
    <div class="codes"><span class="code">engine_version_differs_in_chain</span></div>
    <div class="note">${esc(t("ui.version_drift", { mine: mine, others: others.join(", ") }))}</div>
  </div></div>`;
}

/* ---------- properties ---------- */
const block = (title, inner, section = "") => `<div class="pblock"${section ? ` data-section="${esc(section)}"` : ""}>
  <button type="button" class="phead"><span class="tri">▾</span>${esc(title)}</button>
  <div class="pbody">${inner}</div></div>`;

function measurements(report) {
  const rows = [["objects", "objects"], ["vertices", "vertices"], ["faces", "faces"],
                ["shells", "shells"], ["non-manifold", "non_manifold_edges"],
                ["volume cm³", "volume_cm3"]];
  if (report.kind === "transform" && report.before && report.after) {
    return block(t("ui.measurements"), `<div class="tablewrap"><table><thead><tr><th>&nbsp;</th><th>${esc(t("ui.before"))}</th><th>${esc(t("ui.after"))}</th>
      <th>${esc(t("ui.delta"))}</th></tr></thead><tbody>${rows.map(([label, key]) => {
        const before = report.before[key], after = report.after[key];
        const delta = (before === null || after === null) ? "—" : num(after - before);
        return `<tr><td>${esc(label)}</td><td>${num(before)}</td><td>${num(after)}</td>
          <td class="delta${delta !== "0" && delta !== "—" ? " moved" : ""}">${esc(delta)}</td></tr>`;
      }).join("")}</tbody></table></div>`, "measurements");
  }
  const measured = report.measured || {};
  return block(t("ui.measurements"), `<dl class="kv">${rows.map(([label, key]) =>
    `<dt>${esc(label)}</dt><dd>${num(measured[key])}</dd>`).join("")}</dl>`, "measurements");
}

function boundingBox(report) {
  const before = report.before || report.measured, after = report.after;
  if (!before || !before.bbox_mm) return "";
  const delta = report.bbox_delta_mm;
  const moved = delta ? delta.axes_moved : [];
  const rows = ["X", "Y", "Z"].map((axis, i) => {
    const b = `${before.bbox_mm.min[i]} … ${before.bbox_mm.max[i]}`;
    const a = after && after.bbox_mm ? `${after.bbox_mm.min[i]} … ${after.bbox_mm.max[i]}` : "";
    const flag = moved.includes(axis) ? " class=\"axis-moved\"" : "";
    return `<tr><td${flag}>${axis}</td><td>${esc(b)}</td>${a ? `<td${flag}>${esc(a)}</td>` : ""}</tr>`;
  }).join("");
  const heads = after ? `<th>${esc(t("ui.before"))}</th><th>${esc(t("ui.after"))}</th>`
                      : `<th>${esc(t("ui.measured"))}</th>`;
  const note = delta
    ? `<div class="note">${esc(t("ui.axes_moved", { axes: moved.join(", ") || "none" }))}</div>`
    : "";
  return block(t("ui.bounding_box"),
    `<div class="tablewrap"><table><thead><tr><th>${esc(t("ui.axis"))}</th>${heads}</tr></thead>
     <tbody>${rows}</tbody></table></div>${note}`, "bbox");
}

function rendersBlock(report) {
  const renders = report.renders || [];
  if (!renders.length) {
    return block(t("ui.renders"), `<div class="note">${esc(t("ui.no_renders"))}</div>`, "renders");
  }
  return block(t("ui.renders"), `<div class="renders">${renders.map((render, index) =>
    `<figure><img src="${esc(render.url)}" alt="${esc(t("ui.render_alt", {
       view: render.view, operation: report.operation }))}" loading="lazy">
     <figcaption>${esc(render.view)}${render.tile ? ` · ${esc(t("ui.node_tile"))}` : ""}</figcaption></figure>`
    ).join("")}</div>
    <div class="note">${esc(t("ui.render_provenance"))}</div>`, "renders");
}

function props() {
  const target = document.getElementById("props");
  if (currentDoc) {
    const doc = docFromRef(currentDoc);
    const applied = DATA.reports.filter((report) => (report.links.docs || []).includes(currentDoc));
    target.innerHTML = `<div class="title-row"><h2>${esc(doc.title || currentDoc)}</h2><div class="badges"><span class="badge">${esc(doc.kind)}</span><span class="badge">${esc(doc.status)}</span></div></div>
      ${doc.content ? block(t("ui.runbook_content"), `<div class="doccontent">${mdToHtml(doc.content)}</div>`, "input") : ""}
      ${block(t("ui.applied_by"), applied.length ? applied.map((report) => `<button type="button" class="docref docref--op" data-id="${esc(report.id)}"><code>${esc(report.id)}</code><span class="rtitle">${esc(report.operation)}</span></button>`).join("") : `<div class="note">${esc(t("ui.not_applied"))}</div>`, "links")}`;
    return;
  }
  if (start) {
    const doctor = /** @type {any} */ (DATA.doctor);
    const blender = doctor && (doctor.requirements || []).find((item) => item.name === "blender");
    const setup = blender
      ? `<dl class="kv"><dt>${esc(t("ui.start_blender"))}</dt><dd>${esc(blender.path || t("ui.start_missing"))}</dd>
           <dt>${esc(t("ui.start_version"))}</dt><dd>${esc(blender.version || "—")}</dd></dl>
         <div class="note">${esc(blender.reason || "")}</div>${blender.fix ? cmdButton(esc(blender.fix)) : ""}`
      : `<div class="note">${esc(t("ui.start_doctor_missing"))}</div>${cmdButton("meshanvil doctor")}`;
    target.innerHTML = `<div class="title-row"><h2>${esc(t("ui.start_environment"))}</h2>
      <p class="note">${esc(t("ui.start_environment_note"))}</p></div>${block(t("ui.start_doctor"), setup, "input")}
      ${block(t("ui.start_reports"), `<div class="note">${esc(DATA.ops_exists ? t("ui.start_ops_ready") : t("ui.start_ops_missing"))}</div>`, "measurements")}
      ${block(t("ui.start_contributors"), `<div class="note">${esc(t("ui.start_contributors_note"))}</div>`, "links")}`;
    return;
  }
  if (!current) {
    target.innerHTML = `<div class="blank"><span class="big">${esc(t("ui.nothing_selected"))}</span>
      <span>${esc(t("ui.report_shows"))}</span></div>`;
    return;
  }
  const report = BY_ID.get(current);
  let html = `<div class="title-row">
      <h2>${esc(report.id)} · ${esc(report.operation)}</h2>
      <div class="badges">
        <span class="badge ${esc(report.kind)}">${esc(report.kind)}</span>
        <span class="badge ${esc(report.status)}">${esc(t("ui.status", { status: report.status }))}</span>
        ${report.output ? `<span class="badge">${esc(t("ui.artefact_badge", { state: report.output.state }))}</span>`
                        : `<span class="badge">${esc(t("ui.no_output"))}</span>`}
        <span class="badge">${esc(report.duration_s)} s</span>
      </div>
      ${report.error ? `<p class="note">${esc(report.error)}</p>` : ""}
      ${summaryOf(report.operation) ? `<p class="note">${esc(summaryOf(report.operation))}</p>` : ""}
    </div>`;

  html += driftNotice(report);
  html += block(t("ui.input"), `<dl class="kv">
      <dt>${esc(t("ui.file"))}</dt><dd>${fileControls(report.input.path, esc(short(report.input.path)))}</dd>
      <dt>sha-256</dt><dd>${esc((report.input.sha256 || "").slice(0, 16))}…</dd>
      <dt>mode</dt><dd>${esc(report.input.mode)}</dd></dl>`, "input");
  if (report.output) {
    html += block(t("ui.output"), `<dl class="kv">
      <dt>${esc(t("ui.file"))}</dt><dd>${fileControls(report.output.path, esc(short(report.output.path)))}</dd>
      <dt>sha-256</dt><dd>${esc((report.output.sha256 || "").slice(0, 16))}…</dd>
      <dt>state</dt><dd>${esc(report.output.state)}</dd></dl>`, "output");
  }
  html += block(t("ui.parameters"), `<dl class="kv">${Object.entries(report.params || {}).map(
    ([key, value]) => `<dt>${esc(key)}</dt><dd>${esc(value)}</dd>`).join("")}</dl>`, "parameters");
  html += measurements(report);
  html += boundingBox(report);
  if (report.findings && report.findings.length) {
    html += block(t("ui.findings"), `<ul class="findings">${report.findings.map((f) =>
      `<li><b>${esc(f.code)}</b> — ${
        esc(Object.entries(f).filter(([k]) => k !== "code")
          .map(([k, v]) => `${k}: ${v}`).join(", "))}</li>`).join("")}</ul>`, "findings");
  }
  html += block(t("ui.not_checked"), `<div class="codes">${(report.warnings || []).map((w) =>
      `<span class="code">${esc(w)}</span>`).join("") || `<span class="note">${esc(t("ui.nothing_declared"))}</span>`}</div>
    <div class="note">${esc(t("ui.warning_codes_note"))}</div>`, "warnings");
  html += rendersBlock(report);
  if (report.output) {
    html += block(t("ui.artefact"), `<div class="artefact">
        <span class="state ${esc(report.output.state)}">${esc(report.output.state)}</span>
        ${fileControls(report.output.path, `<code class="provenance">${esc(short(report.output.path))}</code>`)}</div>
      <div class="note">${esc(t("ui.artefact_note"))}</div>`, "artefact");
  }
  html += block(t("ui.tool"), `<dl class="kv">${Object.entries(report.tool || {}).map(([key, value]) =>
      `<dt>${esc(key)}</dt><dd>${esc(value)}</dd>`).join("")}</dl>`, "tool");
  html += block(t("ui.links"), `<div class="wikilinks">
      ${report.links.parent
        ? `<a class="docref docref--op" href="#" data-goto="${esc(report.links.parent)}">
             <code>${esc(report.links.parent)}</code>
             <span class="rtitle">${esc(BY_ID.get(report.links.parent)
               ? BY_ID.get(report.links.parent).operation : "missing")}</span></a>
           <span class="note">${esc(t("ui.parent_resolved", { source: report.links.parent_source }))}</span>`
        : `<span class="note">${esc(t("ui.no_parent"))}</span>`}
      ${(report.links.docs || []).map(docChip).join("")}
    </div>`, "links");
  target.innerHTML = html;
}

const short = (path) => String(path || "").split(/[\\/]/).filter(Boolean).pop() || String(path || "");
function shortRef(slug) {
  const prefix = { run: "N", req: "R", item: "I", task: "T", prod: "P", adr: "A" };
  const match = /^([a-z]+)_(\d+)/.exec(slug || "");
  return match ? (prefix[match[1]] || match[1][0].toUpperCase()) + match[2] : "?";
}

function docChip(ref) {
  const doc = (DATA.docs || {})[ref];
  if (!doc || doc.missing) return `<span class="docref docref--missing"><code>${esc(shortRef(ref))}</code>
    <span class="rtitle">${esc(t("ui.document_missing"))}</span></span>`;
  return `<button type="button" class="docref docref--${esc(doc.kind || "runbook")}" data-doc="${esc(ref)}"><code>${esc(shortRef(ref))}</code>
    <span class="rtitle">${esc(doc.title || ref)}</span><small>${esc(doc.kind || "?")} · ${esc(doc.status || "?")}</small></button>`;
}

/* ---------- image editor ---------- */
/** Give the wipe frame the render's own proportions, so the handle sweeps the picture and
    not the empty band beside it. Both images and the handle then share one reference box. */
function fitCompare(stage) {
  const frame = stage.querySelector(".compare");
  const first = frame && frame.querySelector(".compare-before");
  if (!first) return;
  const fit = () => {
    if (first.naturalWidth) frame.style.aspectRatio = `${first.naturalWidth} / ${first.naturalHeight}`;
  };
  if (first.complete) fit();
  else first.addEventListener("load", fit, { once: true });
}

/** Compare says in numbers what the wipe says in pixels; neither is enough alone. */
function compareTable(report) {
  if (!report.before || !report.after) return "";
  const rows = [["vertices", "vertices"], ["faces", "faces"], ["shells", "shells"],
                ["volume cm³", "volume_cm3"]];
  const body = rows.map(([label, key]) => {
    let before = report.before[key], after = report.after[key];
    if (before === null || before === undefined || after === null || after === undefined) return "";
    if (key === "volume_cm3") { before = Math.round(before); after = Math.round(after); }
    const delta = after - before;
    return `<tr><td>${esc(label)}</td><td>${num(before)}</td><td>${num(after)}</td>
      <td class="delta${delta ? " moved" : ""}">${esc(num(delta))}</td></tr>`;
  }).join("");
  if (!body) return "";
  // Its own scroller: clipped inside the band, the delta column simply vanished.
  return `<div class="tablewrap"><table><thead><tr><th>&nbsp;</th><th>${esc(t("ui.before"))}</th>
    <th>${esc(t("ui.after"))}</th><th>${esc(t("ui.delta"))}</th></tr></thead><tbody>${body}</tbody></table></div>`;
}

function preview() {
  const stage = document.getElementById("pvstage"), meta = document.getElementById("pvmeta");
  const views = document.getElementById("pvviews"), title = document.getElementById("pvtitle");
  const report = current ? BY_ID.get(current) : null;
  const renders = (report && report.renders) || [];
  const pairs = (report && report.comparisons) || [];
  if (start) {
    title.textContent = t("ui.start_title"); views.innerHTML = ""; meta.innerHTML = "";
    stage.innerHTML = `<p class="pvempty">${esc(t("ui.start_preview"))}<br><code>tools/build_demo_chain.sh</code></p>`;
    return;
  }
  title.textContent = report ? `${report.id}_${report.operation}` : "";
  if (workspace === "compare" && pairs.length) {
    if (view >= pairs.length) view = 0;
    const pair = pairs[view], delta = report.bbox_delta_mm || {};
    views.innerHTML = pairs.map((item, i) => `<button type="button" role="tab" data-view="${i}" aria-selected="${i === view}">${esc(item.view)}</button>`).join("");
    stage.innerHTML = `<div class="compare wipe" style="--wipe:${wipe}%"><img class="compare-before before" src="${esc(pair.before_url)}" alt="${esc(t("ui.compare_before"))}"><img class="compare-after after" src="${esc(pair.after_url)}" alt="${esc(t("ui.compare_after"))}"><span class="wipelabel l">${esc(t("ui.compare_before"))}</span><span class="wipelabel r">${esc(t("ui.compare_after"))}</span><span class="handle"></span><input data-wipe type="range" min="0" max="100" value="${wipe}" aria-label="${esc(t("ui.compare_wipe"))}" aria-valuetext="${wipe}%"></div>`;
    fitCompare(stage);
    meta.innerHTML = `<div class="filter">${esc(t("ui.workspace_compare"))}</div>
      <div class="provenance">${esc(pair.camera)}</div>
      ${compareTable(report)}
      <div class="note">${esc(t("ui.axes_moved", { axes: (delta.axes_moved || []).join(", ") || "none" }))}</div>
      <div class="note">${esc(t("ui.compare_note"))}</div>`;
    return;
  }
  if (workspace === "compare" && !pairs.length) {
    views.innerHTML = ""; meta.innerHTML = "";
    stage.innerHTML = `<p class="pvempty">${esc(t("ui.no_comparison"))}</p>`;
    return;
  }
  if (!renders.length) {
    views.innerHTML = "";
    meta.innerHTML = "";
    stage.innerHTML = `<p class="pvempty">${esc(t("ui.no_render"))}<br>${esc(t("ui.no_render_hint"))}</p>`;
    return;
  }
  if (view >= renders.length) view = 0;
  const render = renders[view];
  views.innerHTML = renders.map((r, i) =>
    `<button type="button" role="tab" data-view="${i}" aria-selected="${i === view}">
       ${esc(r.view)}</button>`).join("");
  stage.innerHTML = `<img src="${esc(render.url)}" alt="${esc(t("ui.render_alt", {
    view: render.view, operation: report.operation }))}">`;
  meta.innerHTML = `<div>${fileControls(render.path, `<code class="provenance">${esc(short(render.path))}</code>`)}
      <div class="provenance" style="color:var(--dim);padding-top:3px">${esc(render.camera)}</div></div>
    ${render.tile ? `<div class="tilehint">▲ ${esc(t("ui.tile_hint"))}</div>` : ""}
    <p class="provenance">${esc(t("ui.render_provenance"))}</p>`;
}

/* ---------- shell ---------- */
function select(id) {
  start = false;
  currentDoc = null;
  if (id !== current) view = 0;
  current = id;
  updateRunbookCommand();
  outliner(); nodes(); props(); preview();
}

function selectWorkspace(next) {
  start = false;
  if (next !== workspace) view = 0;   // view indexes renders in Chain and pairs in Compare
  workspace = next;
  /** @type {HTMLElement} */ (document.querySelector(".app")).dataset.workspace = next;
  for (const tab of document.querySelectorAll('[role="tab"][data-workspace]')) {
    tab.setAttribute("aria-selected", String(/** @type {HTMLElement} */ (tab).dataset.workspace === next));
  }
  outliner(); nodes(); props(); preview();
}

/** Every static label the markup carries via data-i18n*, plus the generated-at line: the parts
    t() renders once at load and language switching has to redo the same way. */
function applyStaticStrings() {
  document.documentElement.lang = lang;
  document.getElementById("generated").textContent = DATA.generated_at
    ? t("ui.read_at", { at: DATA.generated_at }) : t("ui.no_report");
  for (const node of document.querySelectorAll("[data-i18n]")) {
    node.textContent = t(/** @type {HTMLElement} */ (node).dataset.i18n);
  }
  for (const node of document.querySelectorAll("[data-i18n-aria-label]")) {
    node.setAttribute("aria-label", t(/** @type {HTMLElement} */ (node).dataset.i18nAriaLabel));
  }
  for (const node of document.querySelectorAll("[data-i18n-placeholder]")) {
    node.setAttribute("placeholder", t(/** @type {HTMLElement} */ (node).dataset.i18nPlaceholder));
  }
  for (const node of document.querySelectorAll("[data-i18n-title]")) {
    node.setAttribute("title", t(/** @type {HTMLElement} */ (node).dataset.i18nTitle));
  }
}

function setLanguage(code) {
  if (code === lang || !(DATA.catalogs && DATA.catalogs[code])) return;
  lang = code;
  strings = mergedCatalog(lang);
  for (const button of document.querySelectorAll("[data-lang]")) {
    button.setAttribute("aria-selected", String(/** @type {HTMLElement} */ (button).dataset.lang === lang));
  }
  applyStaticStrings();
  paintTotals(); paintProjects();
  outliner(); nodes(); props(); preview();
  renderSplash();
}

/** A command or file path shown as a real, clickable copy-to-clipboard control, everywhere
    the viewer used to print one as plain `<code>` text with nothing wired to it. `label`
    (already escaped HTML, e.g. a shortened path) is what shows; `full` (raw text) is what
    gets copied, only different from `label` when the display was shortened for space. */
function cmdButton(label, full) {
  return `<button type="button" class="copycmd" data-copy="${esc(full === undefined ? label : full)}">
    <code class="command">${label}</code><span>${esc(t("ui.copy"))}</span></button>`;
}

/** The viewer reads and starts no process -- adr_003. A menu command cannot run itself, but
    it can put its exact text where a terminal is one paste away. */
function copyCommand(button) {
  const code = button.querySelector("code");
  const target = code || button;   // a bare-text path button (no nested <code>) still flashes
  const text = button.dataset.copy || target.textContent;
  const original = target.textContent;
  const flash = () => {
    target.textContent = t("ui.copied");
    setTimeout(() => { target.textContent = original; }, 900);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(flash, () => legacyCopy(text, flash));
  } else {
    legacyCopy(text, flash);
  }
}

/** navigator.clipboard needs a secure context, and a page opened from file:// is not always
    granted one. A hidden, selected textarea plus execCommand works everywhere it does not. */
function legacyCopy(text, done) {
  const area = document.createElement("textarea");
  area.value = text;
  area.style.position = "fixed";
  area.style.opacity = "0";
  document.body.appendChild(area);
  area.select();
  try { document.execCommand("copy"); done(); }
  catch { /* clipboard unavailable here; the command stays visible to copy by hand */ }
  area.remove();
}

/** adr_007: only reachable when SERVED is true, on one of the three rows the server itself
    also allow-lists (RUNNABLE in meshanvil/viewer.py). The name travels, nothing else does. */
async function runCommand(button) {
  const name = button.dataset.run;
  const code = button.querySelector("code");
  const out = document.querySelector(`[data-cmdout="${CSS.escape(name)}"]`);
  const original = code ? code.textContent : "";
  if (code) code.textContent = t("ui.running");
  if (out) { out.classList.remove("hidden"); out.textContent = ""; }
  try {
    const response = await fetch(`${location.origin}/run`, {
      method: "POST",
      headers: { "X-Meshanvil-Token": /** @type {string} */ (DATA.run_token), "Content-Type": "application/json" },
      body: JSON.stringify({ command: name }),
    });
    if (response.status === 409) { if (out) out.textContent = t("ui.run_busy"); return; }
    if (!response.ok) { if (out) out.textContent = t("ui.run_refused", { status: response.status }); return; }
    if (name === "list" || name === "doctor") { showResult(name, await response.json()); return; }
    if (!out) return;
    const result = await response.json();
    out.textContent = t("ui.run_result", { code: result.exit_code })
      + (result.stdout ? "\n" + result.stdout : "")
      + (result.stderr ? "\n" + result.stderr : "");
  } catch {
    if (out) out.textContent = t("ui.run_failed");
  } finally {
    if (code) code.textContent = original;
  }
}

async function runFileAction(id, action) {
  if (!SERVED || !id) return;
  await fetch(`${location.origin}/file`, {
    method: "POST",
    headers: { "X-Meshanvil-Token": /** @type {string} */ (DATA.run_token), "Content-Type": "application/json" },
    body: JSON.stringify({ id, action }),
  });
}

function closeMenus() {
  for (const menu of document.querySelectorAll("details.menu[open]"))
    /** @type {HTMLDetailsElement} */ (menu).open = false;
}

function showResult(name, result) {
  closeMenus();
  document.getElementById("result-title").textContent = t(name === "list" ? "ui.command_list" : "ui.command_doctor");
  document.getElementById("result-subtitle").textContent = t("ui.run_result", { code: result.exit_code });
  document.getElementById("result-body").innerHTML = name === "list"
    ? renderOperationList(result.data && result.data.operations)
    : renderDoctorResult(result.data);
  document.getElementById("result-modal").classList.remove("hidden");
}

function renderOperationList(operations) {
  const rows = Object.entries(/** @type {Object<string, any>} */ (operations || {})).sort().map(([name, op]) => `<tr><td><code>${esc(name)}</code></td>
    <td>${esc(op.engine)}</td><td>${esc(op.kind)}</td><td>${esc(t(op.summary_key))}</td></tr>`).join("");
  return `<div class="tablewrap"><table><thead><tr><th>${esc(t("ui.operation"))}</th><th>${esc(t("ui.engine"))}</th><th>${esc(t("ui.kind"))}</th><th>${esc(t("ui.summary"))}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function renderDoctorResult(doctor) {
  const project = doctor && doctor.project ? {
    name: doctor.project.name,
    path: doctor.project.path,
    rule: doctor.project.resolved_by,
  } : null;
  const rows = (doctor && doctor.requirements || []).map((item) => `<tr><td>${esc(item.name)}</td>
    <td>${esc(setupState(item.state))}</td><td>${esc(item.path || item.fix || "")}</td></tr>`).join("");
  return `<p class="note">${esc(project ? t("ui.splash_project_note", project) : "")}</p>
    <div class="tablewrap"><table><thead><tr><th>${esc(t("ui.requirement"))}</th><th>${esc(t("ui.status_label"))}</th><th>${esc(t("ui.detail"))}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function setupState(state) {
  return state === "found" ? t("ui.setup_found") : t("ui.setup_missing");
}

function updateRunbookCommand() {
  const button = /** @type {HTMLElement|null} */ (document.getElementById("runbook-command"));
  if (!button) return;
  const code = button.querySelector("code");
  const report = current ? BY_ID.get(current) : null;
  const command = report ? `meshanvil runbook ${report.chain || report.id}` : "meshanvil runbook";
  button.dataset.copy = command;
  if (code) code.textContent = report ? command : t("ui.runbook_select_report");
}

function renderSplash() {
  const doctor = /** @type {any} */ (DATA.doctor);
  // Where a run will land. The working directory chose it and the operator cannot see that
  // from the page, so the page says it.
  const where = doctor && doctor.project;
  const project = where
    ? `<span class="chk ok"><span><b>${esc(t("ui.splash_project"))}</b><br>${esc(t("ui.splash_project_note", {
        name: where.name, path: where.path, rule: where.resolved_by }))}</span></span>`
    : "";
  const blender = doctor && (doctor.requirements || []).find((item) => item.name === "blender");
  const check = blender
    ? `<span class="chk ${blender.path ? "ok" : "warn"}"><span><b>${esc(t("ui.start_doctor"))}</b><br>${esc(blender.path || t("ui.start_missing"))}${blender.fix ? `<br>${cmdButton(esc(blender.fix))}` : ""}</span></span>`
    : `<span class="chk warn"><span><b>${esc(t("ui.start_doctor"))}</b><br>${esc(t("ui.start_doctor_missing"))}<br>${cmdButton("meshanvil doctor")}</span></span>`;
  // Each template is a real button, using the same copy-to-clipboard mechanism as the File
  // menu's command rows (copyCommand, wired below through the shared [data-copy] handler).
  // These three scripts are destructive by their own design (they rebuild a whole sibling
  // project from scratch) and stay outside adr_007's closed, served-runnable command set on
  // purpose -- copy-and-paste-in-a-terminal is the deliberate ceiling here, not an oversight.
  document.getElementById("splash-body").innerHTML = `<section class="scol"><h2>${esc(t("ui.splash_templates"))}</h2>
      <button type="button" class="tpl" data-copy="tools/build_demo_chain.sh"><b>${esc(t("ui.splash_tpl_demo"))}</b><code>tools/build_demo_chain.sh</code></button>
      <button type="button" class="tpl" data-copy="tools/build_figurine_chain.sh"><b>${esc(t("ui.splash_tpl_inspect"))}</b><code>tools/build_figurine_chain.sh</code></button>
      <button type="button" class="tpl" data-copy="meshanvil init <directory>"><b>${esc(t("ui.splash_tpl_repair"))}</b><code>meshanvil init &lt;directory&gt;</code></button>
    </section><section class="scol"><h2>${esc(t("ui.splash_recent"))}</h2>
      <p>${esc(DATA.reports.length ? t("ui.splash_recent_found", { count: DATA.reports.length }) : t("ui.splash_recent_empty"))}</p>
      <p>${esc(t("ui.splash_demo_note"))}</p>
      ${cmdButton("work/ops")}
    </section><section class="scol"><h2>${esc(t("ui.start_environment"))}</h2>
      ${project}
      ${check}<span class="chk ${DATA.ops_exists ? "ok" : "warn"}"><span><b>${esc(t("ui.start_reports"))}</b><br>${esc(DATA.ops_exists ? t("ui.start_ops_ready") : t("ui.start_ops_missing"))}</span></span>
      <span class="chk ok"><span><b>${esc(t("ui.start_contributors"))}</b><br>${esc(t("ui.start_contributors_note"))}</span></span>
    </section>`;
}

function showSplash(show) {
  renderSplash();
  // Closing the splash on an empty project used to reveal an empty page, after a button that
  // said "Continue with demo data". It says what it can actually do.
  const go = /** @type {HTMLButtonElement} */ (document.getElementById("splash-continue"));
  const empty = !DATA.reports.length;
  go.textContent = empty ? t("ui.splash_nothing") : t("ui.splash_continue");
  go.disabled = empty;
  document.getElementById("splash").classList.toggle("hidden", !show);
  // Opening the splash is reached from a File-menu row, whose own click handler returns
  // early (the row is inside the open <details>, so the generic "click outside a menu
  // closes it" check at the bottom of the click listener never runs) -- left the dropdown
  // sitting open on top of the modal it just opened.
  if (show) closeMenus();
}

function jumpReportSection(section) {
  const block = document.querySelector(`#props [data-section="${CSS.escape(section)}"]`);
  if (block) block.scrollIntoView({ block: "start" });
  for (const button of document.querySelectorAll("[data-section-goto]")) {
    button.setAttribute("aria-selected", String(/** @type {HTMLElement} */ (button).dataset.sectionGoto === section));
  }
}

document.addEventListener("click", (event) => {
  const target = /** @type {Element} */ (event.target);
  const splash = target.closest("[data-splash]");
  if (splash) {
    showSplash(/** @type {HTMLElement} */ (splash).dataset.splash !== "close");
    if (!/** @type {HTMLElement} */ (splash).dataset.workspace) return;
  }
  const section = target.closest("[data-section-goto]");
  if (section) { jumpReportSection(/** @type {HTMLElement} */ (section).dataset.sectionGoto || "input"); return; }
  const workspaceTab = target.closest('button[data-workspace], [role="tab"][data-workspace]');
  if (workspaceTab) { selectWorkspace(/** @type {HTMLElement} */ (workspaceTab).dataset.workspace || "chain"); return; }
  const langTab = target.closest("[data-lang]");
  if (langTab) { setLanguage(/** @type {HTMLElement} */ (langTab).dataset.lang || "en"); return; }
  const run = target.closest("[data-run]");
  if (run && SERVED) { runCommand(/** @type {HTMLElement} */ (run)); return; }
  const openFile = target.closest("[data-file-open]");
  if (openFile) { runFileAction(/** @type {HTMLElement} */ (openFile).dataset.fileOpen, "open"); return; }
  const revealFile = target.closest("[data-file-reveal]");
  if (revealFile) { runFileAction(/** @type {HTMLElement} */ (revealFile).dataset.fileReveal, "reveal"); return; }
  if (target.closest("[data-result-close]")) { document.getElementById("result-modal").classList.add("hidden"); return; }
  const copy = target.closest("[data-copy]");
  if (copy) { copyCommand(/** @type {HTMLElement} */ (copy)); return; }
  const goto = target.closest("[data-goto]");
  if (goto) { event.preventDefault(); select(/** @type {HTMLElement} */ (goto).dataset.goto); return; }
  const viewTab = target.closest("[data-view]");
  if (viewTab) { view = Number(/** @type {HTMLElement} */ (viewTab).dataset.view); preview(); return; }
  const node = target.closest("[data-id]");
  if (node) { select(/** @type {HTMLElement} */ (node).dataset.id); return; }
  const doc = target.closest("[data-doc]");
  if (doc) { start = false; currentDoc = /** @type {HTMLElement} */ (doc).dataset.doc; current = null; updateRunbookCommand(); outliner(); nodes(); props(); preview(); }
  for (const menu of document.querySelectorAll("details.menu[open]")) {
    if (!menu.contains(target)) /** @type {HTMLDetailsElement} */ (menu).open = false;
  }
});
document.addEventListener("input", (event) => {
  const input = /** @type {HTMLInputElement} */ (event.target);
  if (input.matches("#outliner-filter")) { filterText = input.value.toLowerCase(); outliner(); return; }
  if (!input.matches("[data-wipe]")) return;
  wipe = Number(input.value);
  const compare = /** @type {HTMLElement|null} */ (document.querySelector(".compare"));
  if (compare) compare.style.setProperty("--wipe", `${wipe}%`);
  input.setAttribute("aria-valuetext", `${wipe}%`);
});

document.getElementById("start-screen").addEventListener("click", () => {
  showSplash(true);
});

/** Everything that counts the chain. Re-run on a project switch: totals summed across two
    unrelated subjects describe neither of them. */
function paintTotals() {
  document.getElementById("chain-name").textContent =
    DATA.reports.length ? chainName(DATA.reports) : "—";
  document.getElementById("op-count").textContent = t("ui.operations", { count: DATA.reports.length });
  document.getElementById("schema").textContent =
    DATA.reports.length ? `schema ${DATA.reports[0].schema_version}` : "";
  document.getElementById("status-counts").textContent =
    t("ui.operations", { count: DATA.reports.length }) + " · "
    + t("ui.failed_kept", { count: DATA.reports.filter((r) => r.status === "failed").length });
  // A branch is a report with more than one child: that is where a chain forked and where a
  // reviewer has to choose. Counting parents would count the trunk as a branch too.
  const children = new Map();
  for (const report of DATA.reports) {
    const parent = report.links && report.links.parent;
    if (parent) children.set(parent, (children.get(parent) || 0) + 1);
  }
  document.getElementById("status-branches").textContent =
    t("ui.branches", { count: [...children.values()].filter((n) => n > 1).length });
  const leaf = [...DATA.reports].reverse().find((r) =>
    (r.after && r.after.vertices !== null && r.after.vertices !== undefined)
    || (r.measured && r.measured.vertices !== null && r.measured.vertices !== undefined));
  document.getElementById("status-vertices").textContent = leaf
    ? t("ui.vertices_total", { count: num((leaf.after || leaf.measured).vertices) }) : "";
  document.getElementById("status-schema").textContent = DATA.reports.length
    ? t("ui.schema_ops", { version: DATA.reports[0].schema_version,
                           project: /** @type {any} */ (DATA).active || "" }) : "";
}

async function init() {
  await fetchData();
  paintTotals();
  applyStaticStrings();
  document.getElementById("app-version").textContent = DATA.version ? `v${DATA.version}` : "";
  for (const button of document.querySelectorAll("[data-lang]")) {
    button.setAttribute("aria-selected", String(/** @type {HTMLElement} */ (button).dataset.lang === lang));
  }
  renderSplash();
  paintProjects();
  updateRunbookCommand();
  document.getElementById("project-select").addEventListener("change", (event) => {
    selectProject(/** @type {HTMLSelectElement} */ (event.target).value);
  });
  if (current) select(current);
  else { outliner(); nodes(); props(); preview(); showSplash(true); }
  startLiveRefresh(SERVED, refreshLive);
}

Object.assign(/** @type {any} */ (window), { select, selectProject, paintProjects });
init();
