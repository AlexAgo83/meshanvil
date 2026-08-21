/* The viewer reads. It starts no process and writes nothing -- adr_003.
   Everything it renders comes from a report, and a report is data written by CAD files,
   so every value is escaped before it reaches the page. */
// @ts-check
"use strict";

/** The report contract, as adr_001 defines it. Named OperationReport rather than Report:
 * the DOM already has a Report interface, and the collision silently made every property
 * resolve against it.
 * @typedef {{id:string, chain:string, kind:string, status:string, operation:string,
 *   schema_version:number, error?:string,
 *   params:Object, tool:Object, input:Object, output?:Object, before?:Object, after?:Object,
 *   measured?:Object, bbox_delta_mm?:Object, warnings:string[], findings?:Object[],
 *   renders?:Object[], links:{parent:string|null, parent_source:string|null, docs:string[]},
 *   duration_s:number, created_at:string,
 *   _x?:number, _y?:number}} OperationReport */

const DATA = /** @type {{reports: OperationReport[], generated_at: string, root: string}} */ (
  /** @type {any} */ (window).MESHANVIL || { reports: [], generated_at: "", root: "" });

/** @type {Map<string, OperationReport>} */
const BY_ID = new Map(DATA.reports.map((r) => [r.id, r]));
let current = DATA.reports.length ? DATA.reports[DATA.reports.length - 1].id : null;
let view = 0;

/** Report text is data from CAD files, never markup. */
function esc(value) {
  return String(value === null || value === undefined ? "" : value)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
const num = (v) => (v === null || v === undefined ? "—" : Number(v).toLocaleString("en-US"));

/* ---------- layout: depth from the parent chain, siblings stacked ---------- */
function place() {
  const depth = new Map(), row = new Map();
  for (const report of DATA.reports) {
    const parent = report.links && report.links.parent;
    const level = parent && depth.has(parent) ? depth.get(parent) + 1 : 0;
    depth.set(report.id, level);
    const used = row.get(level) || 0;
    row.set(level, used + 1);
    report._x = 20 + level * 232;
    report._y = 20 + used * 128;
  }
}

/* ---------- outliner ---------- */
function outliner() {
  const chains = new Map();
  for (const report of DATA.reports) {
    const key = report.chain || report.id;
    if (!chains.has(key)) chains.set(key, []);
    chains.get(key).push(report);
  }
  let html = "";
  for (const [chain, reports] of chains) {
    html += `<div class="outgroup">Chain ${esc(chain)}</div>`;
    for (const report of reports) {
      const kind = report.status === "failed" ? "failed" : report.kind;
      const glyph = report.kind === "inspection" ? "i" : "T";
      html += `<button type="button" class="row" data-id="${esc(report.id)}"
        aria-current="${report.id === current}">
        <span class="tri">▾</span>
        <span class="kindicon ${esc(kind)}">${report.status === "failed" ? "×" : glyph}</span>
        <span class="label"><span class="idx">${esc(report.id)}</span> ${esc(report.operation)}</span>
        <span class="dot ${esc(report.status)}"></span></button>`;
    }
  }
  document.getElementById("outliner").innerHTML =
    html || `<div class="blank"><span class="big">No operation yet</span>
      <span>Reports appear here once one has been written under work/ops/.</span></div>`;
}

/* ---------- node editor ---------- */
function nodes() {
  let html = "";
  for (const report of DATA.reports) {
    const kind = report.status === "failed" ? "failed" : report.kind;
    const lines = headline(report).map(([key, value]) =>
      `<div class="nline"><span>${esc(key)}</span><b>${esc(value)}</b></div>`).join("");
    html += `<button type="button" class="node ${esc(kind)}" data-id="${esc(report.id)}"
        aria-current="${report.id === current}" style="left:${report._x}px;top:${report._y}px">
      <div class="nhead"><span class="nidx">${esc(report.id)}</span>${esc(report.operation)}</div>
      <div class="nbody">${lines}</div>
      <div class="nfoot"><span class="dot ${esc(report.status)}"></span>
        ${report.status === "failed" ? "failed · kept" : esc(report.kind)}</div>
    </button>`;
  }
  document.getElementById("nodes").innerHTML = html;
  const canvas = document.getElementById("canvas");
  canvas.style.width = Math.max(860, ...DATA.reports.map((r) => r._x + 240)) + "px";
  canvas.style.height = Math.max(420, ...DATA.reports.map((r) => r._y + 180)) + "px";
  noodles();
}

function headline(report) {
  if (report.kind === "transform" && report.after) {
    return [["vertices", `${num(report.before.vertices)} → ${num(report.after.vertices)}`],
            ["shells", `${num(report.before.shells)} → ${num(report.after.shells)}`]];
  }
  const measured = report.measured || {};
  return [["objects", num(measured.objects)], ["vertices", num(measured.vertices)]];
}

function noodles() {
  let path = "";
  for (const report of DATA.reports) {
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
    <div class="note">This report was produced by engine ${esc(mine)}; others in this chain used
    ${esc(others.join(", "))}. Numbers from different engine versions are not comparable.</div>
  </div></div>`;
}

/* ---------- properties ---------- */
const block = (title, inner) => `<div class="pblock">
  <button type="button" class="phead"><span class="tri">▾</span>${esc(title)}</button>
  <div class="pbody">${inner}</div></div>`;

function measurements(report) {
  const rows = [["objects", "objects"], ["vertices", "vertices"], ["faces", "faces"],
                ["shells", "shells"], ["non-manifold", "non_manifold_edges"],
                ["volume cm³", "volume_cm3"]];
  if (report.kind === "transform" && report.before && report.after) {
    return block("Measurements", `<table><thead><tr><th>&nbsp;</th><th>before</th><th>after</th>
      <th>delta</th></tr></thead><tbody>${rows.map(([label, key]) => {
        const before = report.before[key], after = report.after[key];
        const delta = (before === null || after === null) ? "—" : num(after - before);
        return `<tr><td>${esc(label)}</td><td>${num(before)}</td><td>${num(after)}</td>
          <td class="delta${delta !== "0" && delta !== "—" ? " moved" : ""}">${esc(delta)}</td></tr>`;
      }).join("")}</tbody></table>`);
  }
  const measured = report.measured || {};
  return block("Measurements", `<dl class="kv">${rows.map(([label, key]) =>
    `<dt>${esc(label)}</dt><dd>${num(measured[key])}</dd>`).join("")}</dl>`);
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
  const heads = after ? "<th>before</th><th>after</th>" : "<th>measured</th>";
  const note = delta
    ? `<div class="note">Axes moved: <span class="axis-moved">${esc(moved.join(", ") || "none")}</span>.
       Computed by the report writer, not by the operation.</div>`
    : "";
  return block("Bounding box, mm",
    `<table><thead><tr><th>axis</th>${heads}</tr></thead><tbody>${rows}</tbody></table>${note}`);
}

function props() {
  const target = document.getElementById("props");
  if (!current) {
    target.innerHTML = `<div class="blank"><span class="big">Nothing selected</span>
      <span>A report shows its input, what changed, what was not checked, and its renders.</span></div>`;
    return;
  }
  const report = BY_ID.get(current);
  let html = `<div class="title-row">
      <h2>${esc(report.id)} · ${esc(report.operation)}</h2>
      <div class="badges">
        <span class="badge ${esc(report.kind)}">${esc(report.kind)}</span>
        <span class="badge ${esc(report.status)}">status ${esc(report.status)}</span>
        ${report.output ? `<span class="badge">artefact ${esc(report.output.state)}</span>`
                        : `<span class="badge">no output</span>`}
        <span class="badge">${esc(report.duration_s)} s</span>
      </div>
      ${report.error ? `<p class="note">${esc(report.error)}</p>` : ""}
    </div>`;

  html += driftNotice(report);
  html += block("Input", `<dl class="kv">
      <dt>path</dt><dd>${esc(short(report.input.path))}</dd>
      <dt>sha-256</dt><dd>${esc((report.input.sha256 || "").slice(0, 16))}…</dd>
      <dt>mode</dt><dd>${esc(report.input.mode)}</dd></dl>`);
  if (report.output) {
    html += block("Output", `<dl class="kv">
      <dt>path</dt><dd>${esc(short(report.output.path))}</dd>
      <dt>sha-256</dt><dd>${esc((report.output.sha256 || "").slice(0, 16))}…</dd>
      <dt>state</dt><dd>${esc(report.output.state)}</dd></dl>`);
  }
  html += block("Parameters", `<dl class="kv">${Object.entries(report.params || {}).map(
    ([key, value]) => `<dt>${esc(key)}</dt><dd>${esc(value)}</dd>`).join("")}</dl>`);
  html += measurements(report);
  html += boundingBox(report);
  if (report.findings && report.findings.length) {
    html += block("Findings", `<ul style="margin:0;padding-left:16px;color:var(--dim);
      font-size:11.5px;display:flex;flex-direction:column;gap:4px">${report.findings.map((f) =>
      `<li><b style="color:var(--txt);font-weight:500">${esc(f.code)}</b> — ${
        esc(Object.entries(f).filter(([k]) => k !== "code")
          .map(([k, v]) => `${k}: ${v}`).join(", "))}</li>`).join("")}</ul>`);
  }
  html += block("Not checked", `<div class="codes">${(report.warnings || []).map((w) =>
      `<span class="code">${esc(w)}</span>`).join("") || '<span class="note">nothing declared</span>'}</div>
    <div class="note">Warning codes, not sentences: an agent can act on a code.</div>`);
  html += block("Tool", `<dl class="kv">${Object.entries(report.tool || {}).map(([key, value]) =>
      `<dt>${esc(key)}</dt><dd>${esc(value)}</dd>`).join("")}</dl>`);
  html += block("Links", `<div class="wikilinks">
      ${report.links.parent
        ? `<a class="docref docref--op" href="#" data-goto="${esc(report.links.parent)}">
             <code>${esc(report.links.parent)}</code>
             <span class="rtitle">${esc(BY_ID.get(report.links.parent)
               ? BY_ID.get(report.links.parent).operation : "missing")}</span></a>
           <span class="note">parent resolved by ${esc(report.links.parent_source)}</span>`
        : `<span class="note">No parent — start of the chain.</span>`}
      ${(report.links.docs || []).map((doc) =>
        `<span class="docref docref--runbook"><code>${esc(shortRef(doc))}</code>
           <span class="rtitle">${esc(doc)}</span></span>`).join("")}
    </div>`);
  target.innerHTML = html;
}

const short = (path) => String(path || "").replace(DATA.root + "/", "");
function shortRef(slug) {
  const prefix = { run: "N", req: "R", item: "I", task: "T", prod: "P", adr: "A" };
  const match = /^([a-z]+)_(\d+)/.exec(slug || "");
  return match ? (prefix[match[1]] || match[1][0].toUpperCase()) + match[2] : "?";
}

/* ---------- image editor ---------- */
function preview() {
  const stage = document.getElementById("pvstage"), meta = document.getElementById("pvmeta");
  const views = document.getElementById("pvviews"), title = document.getElementById("pvtitle");
  const report = current ? BY_ID.get(current) : null;
  const renders = (report && report.renders) || [];
  title.textContent = report ? `${report.id}_${report.operation}` : "";
  if (!renders.length) {
    views.innerHTML = "";
    meta.innerHTML = "";
    stage.innerHTML = `<p class="pvempty">This operation left no render.<br>
      Run it with rendering enabled, or open the file in Blender to look at the geometry.</p>`;
    return;
  }
  if (view >= renders.length) view = 0;
  const render = renders[view];
  views.innerHTML = renders.map((r, i) =>
    `<button type="button" role="tab" data-view="${i}" aria-selected="${i === view}">
       ${esc(r.view)}</button>`).join("");
  stage.innerHTML = `<img src="${esc(render.url)}" alt="${esc(render.view)} view of ${
    esc(report.operation)}">`;
  meta.innerHTML = `<div><div class="provenance">${esc(short(render.path))}</div>
      <div class="provenance" style="color:var(--dim);padding-top:3px">${esc(render.camera)}</div></div>
    ${render.tile ? '<div class="tilehint">▲ this one is the node tile</div>' : ""}
    <p class="provenance">Written by the operation and listed in renders[]. The viewer renders
    nothing: it shows what the engine already produced.</p>`;
}

/* ---------- shell ---------- */
function select(id) {
  if (id !== current) view = 0;
  current = id;
  outliner(); nodes(); props(); preview();
}

document.addEventListener("click", (event) => {
  const target = /** @type {Element} */ (event.target);
  const goto = target.closest("[data-goto]");
  if (goto) { event.preventDefault(); select(/** @type {HTMLElement} */ (goto).dataset.goto); return; }
  const viewTab = target.closest("[data-view]");
  if (viewTab) { view = Number(/** @type {HTMLElement} */ (viewTab).dataset.view); preview(); return; }
  const node = target.closest("[data-id]");
  if (node) select(/** @type {HTMLElement} */ (node).dataset.id);
});

place();
document.getElementById("chain-name").textContent =
  DATA.reports.length ? (DATA.reports[0].chain || "—") : "—";
document.getElementById("op-count").textContent = `${DATA.reports.length} operations`;
document.getElementById("schema").textContent =
  DATA.reports.length ? `schema ${DATA.reports[0].schema_version}` : "";
document.getElementById("status-counts").textContent =
  `${DATA.reports.length} operations · ${DATA.reports.filter((r) => r.status === "failed").length} failed, kept`;
document.getElementById("generated").textContent = DATA.generated_at
  ? `read ${DATA.generated_at}` : "no report";
select(current);
