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
 *   renders?:Object[], comparisons?:{view:string,before_url:string,after_url:string,camera:string}[], links:{parent:string|null, parent_source:string|null, docs:string[]},
 *   duration_s:number, created_at:string,
 *   _x?:number, _y?:number}} OperationReport */

const DATA = /** @type {{reports: OperationReport[], generated_at: string, root: string,
 *   lang: string, strings: Object<string,string>, docs?: Object<string,Object>, runbooks?: Object[], doctor?: Object, ops_exists?: boolean}} */ (
  /** @type {any} */ (window).MESHANVIL
  || { reports: [], generated_at: "", root: "", lang: "en", strings: {} });

/** Same catalogue as the command line, shipped in data.js. English is the fallback. */
function t(key, values) {
  let text = (DATA.strings || {})[key] || key;
  for (const [name, value] of Object.entries(values || {})) {
    text = text.split(`{${name}}`).join(String(value));
  }
  return text;
}

/** @type {Map<string, OperationReport>} */
const BY_ID = new Map(DATA.reports.map((r) => [r.id, r]));
let current = DATA.reports.length ? DATA.reports[DATA.reports.length - 1].id : null;
let currentDoc = null;
let view = 0;
let wipe = 50;
let start = !DATA.reports.length;
let workspace = "chain";
let filterText = "";

/** Report text is data from CAD files, never markup. */
function esc(value) {
  return String(value === null || value === undefined ? "" : value)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
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
    report._y = 20 + used * 196;
  }
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
  const chains = new Map();
  for (const report of DATA.reports) {
    const key = report.chain || report.id;
    if (!chains.has(key)) chains.set(key, []);
    chains.get(key).push(report);
  }
  let html = "";
  let first = true;
  for (const [chain, reports] of chains) {
    const parent = BY_ID.get(chain);
    const label = first ? t("ui.chain_named", { name: chainName(reports) })
                        : t("ui.branch_named", { name: parent ? `${parent.id} ${parent.operation}` : chain });
    first = false;
    html += `<div class="outgroup">${esc(label)}</div>`;
    for (const report of reports) {
      if (!`${report.id} ${report.operation}`.toLowerCase().includes(filterText)) continue;
      const kind = report.status === "failed" ? "failed" : report.kind;
      const state = artefactState(report);
      const glyph = report.kind === "inspection" ? "i" : "T";
      html += `<button type="button" class="row" data-id="${esc(report.id)}"
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

/** A chain is named after the file it started from; the identity is already in the row. */
function chainName(reports) {
  const root = reports[0];
  const path = String((root.input || {}).path || "");
  return path.split("/").pop().replace(/\.blend$/, "") || root.chain || root.id;
}

function docFromRef(ref) {
  return (DATA.runbooks || []).find((item) => item.ref === ref) || (DATA.docs || {})[ref] || { ref };
}

function docPurpose(doc) {
  const sections = doc.sections || {};
  const first = doc.purpose || (sections.Trigger || sections.Overview || sections.Procedure || [])[0];
  return String(first || doc.content || t("ui.runbook_no_summary")).replace(/^[-\d. ]+/, "").slice(0, 180);
}

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
      <span class="rbapplied">${applied.length ? applied.map((report) =>
        `<span class="docref docref--op"><code>${esc(report.id)}</code><span class="rtitle">${esc(report.operation)}</span></span>`).join("")
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
      <li>${esc(t("ui.start_demo"))} <code>blender -b -P tools/make_demo_scene.py</code></li>
      <li>${esc(t("ui.start_inspect"))} <code>meshanvil run scan_defects work/out/demo_source.blend</code></li>
      <li>${esc(t("ui.start_prepare"))} <code>meshanvil run voxel_remesh work/out/demo_source.blend --set voxel_mm=6</code></li></ol></div>`;
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
  graphHead("⬡", t("ui.node_editor"),
    DATA.reports.length ? `chain / ${chainName(DATA.reports)}` : "links.parent");
  let html = "";
  for (const report of DATA.reports) {
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
  canvas.style.width = Math.max(860, ...DATA.reports.map((r) => r._x + 240)) + "px";
  canvas.style.height = Math.max(420, ...DATA.reports.map((r) => r._y + 200)) + "px";
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
    return block(t("ui.measurements"), `<table><thead><tr><th>&nbsp;</th><th>${esc(t("ui.before"))}</th><th>${esc(t("ui.after"))}</th>
      <th>${esc(t("ui.delta"))}</th></tr></thead><tbody>${rows.map(([label, key]) => {
        const before = report.before[key], after = report.after[key];
        const delta = (before === null || after === null) ? "—" : num(after - before);
        return `<tr><td>${esc(label)}</td><td>${num(before)}</td><td>${num(after)}</td>
          <td class="delta${delta !== "0" && delta !== "—" ? " moved" : ""}">${esc(delta)}</td></tr>`;
      }).join("")}</tbody></table>`, "measurements");
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
    `<table><thead><tr><th>${esc(t("ui.axis"))}</th>${heads}</tr></thead><tbody>${rows}</tbody></table>${note}`, "bbox");
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
      ${block(t("ui.applied_by"), applied.length ? applied.map((report) => `<button type="button" class="docref docref--op" data-id="${esc(report.id)}"><code>${esc(report.id)}</code><span class="rtitle">${esc(report.operation)}</span></button>`).join("") : `<div class="note">${esc(t("ui.not_applied"))}</div>`, "links")}`;
    return;
  }
  if (start) {
    const doctor = /** @type {any} */ (DATA.doctor);
    const blender = doctor && (doctor.requirements || []).find((item) => item.name === "blender");
    const setup = blender
      ? `<dl class="kv"><dt>${esc(t("ui.start_blender"))}</dt><dd>${esc(blender.path || t("ui.start_missing"))}</dd>
           <dt>${esc(t("ui.start_version"))}</dt><dd>${esc(blender.version || "—")}</dd></dl>
         <div class="note">${esc(blender.reason || "")}</div>${blender.fix ? `<code class="command">${esc(blender.fix)}</code>` : ""}`
      : `<div class="note">${esc(t("ui.start_doctor_missing"))}</div><code class="command">meshanvil doctor</code>`;
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
      <dt>path</dt><dd>${esc(short(report.input.path))}</dd>
      <dt>sha-256</dt><dd>${esc((report.input.sha256 || "").slice(0, 16))}…</dd>
      <dt>mode</dt><dd>${esc(report.input.mode)}</dd></dl>`, "input");
  if (report.output) {
    html += block(t("ui.output"), `<dl class="kv">
      <dt>path</dt><dd>${esc(short(report.output.path))}</dd>
      <dt>sha-256</dt><dd>${esc((report.output.sha256 || "").slice(0, 16))}…</dd>
      <dt>state</dt><dd>${esc(report.output.state)}</dd></dl>`, "output");
  }
  html += block(t("ui.parameters"), `<dl class="kv">${Object.entries(report.params || {}).map(
    ([key, value]) => `<dt>${esc(key)}</dt><dd>${esc(value)}</dd>`).join("")}</dl>`, "parameters");
  html += measurements(report);
  html += boundingBox(report);
  if (report.findings && report.findings.length) {
    html += block(t("ui.findings"), `<ul style="margin:0;padding-left:16px;color:var(--dim);
      font-size:11.5px;display:flex;flex-direction:column;gap:4px">${report.findings.map((f) =>
      `<li><b style="color:var(--txt);font-weight:500">${esc(f.code)}</b> — ${
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
        <span>${esc(short(report.output.path))}</span></div>
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

const short = (path) => String(path || "").replace(DATA.root + "/", "");
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
/** Compare says in numbers what the wipe says in pixels; neither is enough alone. */
function compareTable(report) {
  if (!report.before || !report.after) return "";
  const rows = [["vertices", "vertices"], ["faces", "faces"], ["shells", "shells"],
                ["volume cm³", "volume_cm3"]];
  const body = rows.map(([label, key]) => {
    const before = report.before[key], after = report.after[key];
    if (before === null || before === undefined || after === null || after === undefined) return "";
    const delta = after - before;
    return `<tr><td>${esc(label)}</td><td>${num(before)}</td><td>${num(after)}</td>
      <td class="delta${delta ? " moved" : ""}">${esc(num(delta))}</td></tr>`;
  }).join("");
  if (!body) return "";
  return `<table><thead><tr><th>&nbsp;</th><th>${esc(t("ui.before"))}</th>
    <th>${esc(t("ui.after"))}</th><th>${esc(t("ui.delta"))}</th></tr></thead><tbody>${body}</tbody></table>`;
}

function preview() {
  const stage = document.getElementById("pvstage"), meta = document.getElementById("pvmeta");
  const views = document.getElementById("pvviews"), title = document.getElementById("pvtitle");
  const report = current ? BY_ID.get(current) : null;
  const renders = (report && report.renders) || [];
  const pairs = (report && report.comparisons) || [];
  if (start) {
    title.textContent = t("ui.start_title"); views.innerHTML = ""; meta.innerHTML = "";
    stage.innerHTML = `<p class="pvempty">${esc(t("ui.start_preview"))}<br><code>tools/make_demo_scene.py</code></p>`;
    return;
  }
  title.textContent = report ? `${report.id}_${report.operation}` : "";
  if (workspace === "compare" && pairs.length) {
    if (view >= pairs.length) view = 0;
    const pair = pairs[view], delta = report.bbox_delta_mm || {};
    views.innerHTML = pairs.map((item, i) => `<button type="button" role="tab" data-view="${i}" aria-selected="${i === view}">${esc(item.view)}</button>`).join("");
    stage.innerHTML = `<div class="compare wipe" style="--wipe:${wipe}%"><img class="compare-before before" src="${esc(pair.before_url)}" alt="${esc(t("ui.compare_before"))}"><img class="compare-after after" src="${esc(pair.after_url)}" alt="${esc(t("ui.compare_after"))}"><span class="wipelabel l">${esc(t("ui.compare_before"))}</span><span class="wipelabel r">${esc(t("ui.compare_after"))}</span><span class="handle"></span><input data-wipe type="range" min="0" max="100" value="${wipe}" aria-label="${esc(t("ui.compare_wipe"))}" aria-valuetext="${wipe}%"></div>`;
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
  meta.innerHTML = `<div><div class="provenance">${esc(short(render.path))}</div>
      <div class="provenance" style="color:var(--dim);padding-top:3px">${esc(render.camera)}</div></div>
    ${render.tile ? `<div class="tilehint">▲ ${esc(t("ui.tile_hint"))}</div>` : ""}
    ${report.output ? `<div class="act">
      <span class="hint">${esc(t("ui.open_in_blender"))}</span>
      <code class="command">blender ${esc(short(report.output.path))}</code>
    </div>` : ""}
    <p class="provenance">${esc(t("ui.render_provenance"))}</p>`;
}

/* ---------- shell ---------- */
function select(id) {
  start = false;
  currentDoc = null;
  if (id !== current) view = 0;
  current = id;
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

function renderSplash() {
  const doctor = /** @type {any} */ (DATA.doctor);
  const blender = doctor && (doctor.requirements || []).find((item) => item.name === "blender");
  const check = blender
    ? `<span class="chk ${blender.path ? "ok" : "warn"}"><span><b>${esc(t("ui.start_doctor"))}</b><br>${esc(blender.path || t("ui.start_missing"))}${blender.fix ? `<br><code>${esc(blender.fix)}</code>` : ""}</span></span>`
    : `<span class="chk warn"><span><b>${esc(t("ui.start_doctor"))}</b><br>${esc(t("ui.start_doctor_missing"))}<br><code>meshanvil doctor</code></span></span>`;
  document.getElementById("splash-body").innerHTML = `<section class="scol"><h2>${esc(t("ui.splash_templates"))}</h2>
      <button type="button" class="tpl" data-splash="close"><b>${esc(t("ui.splash_tpl_demo"))}</b><code>blender -b -P tools/make_demo_scene.py</code></button>
      <button type="button" class="tpl" data-splash="close"><b>${esc(t("ui.splash_tpl_inspect"))}</b><code>meshanvil run scan_defects work/out/demo_source.blend</code></button>
      <button type="button" class="tpl" data-splash="close"><b>${esc(t("ui.splash_tpl_repair"))}</b><code>meshanvil run voxel_remesh work/out/demo_source.blend --set voxel_mm=6</code></button>
    </section><section class="scol"><h2>${esc(t("ui.splash_recent"))}</h2>
      <p>${esc(DATA.reports.length ? t("ui.splash_recent_found", { count: DATA.reports.length }) : t("ui.splash_recent_empty"))}</p>
      <p>${esc(t("ui.splash_demo_note"))}</p>
      <code class="command">work/ops</code>
    </section><section class="scol"><h2>${esc(t("ui.start_environment"))}</h2>
      ${check}<span class="chk ${DATA.ops_exists ? "ok" : "warn"}"><span><b>${esc(t("ui.start_reports"))}</b><br>${esc(DATA.ops_exists ? t("ui.start_ops_ready") : t("ui.start_ops_missing"))}</span></span>
      <span class="chk ok"><span><b>${esc(t("ui.start_contributors"))}</b><br>${esc(t("ui.start_contributors_note"))}</span></span>
    </section>`;
}

function showSplash(show) {
  renderSplash();
  document.getElementById("splash").classList.toggle("hidden", !show);
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
  const goto = target.closest("[data-goto]");
  if (goto) { event.preventDefault(); select(/** @type {HTMLElement} */ (goto).dataset.goto); return; }
  const viewTab = target.closest("[data-view]");
  if (viewTab) { view = Number(/** @type {HTMLElement} */ (viewTab).dataset.view); preview(); return; }
  const node = target.closest("[data-id]");
  if (node) { select(/** @type {HTMLElement} */ (node).dataset.id); return; }
  const doc = target.closest("[data-doc]");
  if (doc) { start = false; currentDoc = /** @type {HTMLElement} */ (doc).dataset.doc; current = null; outliner(); nodes(); props(); preview(); }
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

place();
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
  ? t("ui.schema_ops", { version: DATA.reports[0].schema_version }) : "";
document.getElementById("generated").textContent = DATA.generated_at
  ? t("ui.read_at", { at: DATA.generated_at }) : t("ui.no_report");
document.documentElement.lang = DATA.lang || "en";
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
renderSplash();
if (current) select(current);
else { outliner(); nodes(); props(); preview(); showSplash(true); }
