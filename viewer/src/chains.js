/** Chain identity: which start a report descends from, so the outliner and the canvas agree.
 *
 *  Kept out of app.js so it can be checked without a DOM: these rules decide what is grouped
 *  and what is drawn, and getting them wrong merges unrelated runs under one name -- or splits
 *  one run into several. Voir adr_007.
 */

/** The source a parentless report starts from. Several operations commonly read the project's
 *  subject directly -- an inspection sweep before anything is transformed -- and none of them
 *  has a parent, so keying each on its own id filed one chain as five. They start from the
 *  same file, which is the thing they actually share.
 *  @param {any} report
 *  @returns {string} */
export function sourceOf(report) {
  return String((report.input || {}).path || "") || report.id;
}

/** The start a report descends from, walking parents until one has none.
 *  @param {Map<string, any>} byId
 *  @param {string} id
 *  @returns {string|null} */
export function rootOf(byId, id) {
  const seen = new Set();
  let report = byId.get(id);
  while (report && report.links && report.links.parent && byId.has(report.links.parent)) {
    if (seen.has(report.id)) break;          // a cycle cannot happen, but it must not hang.
    seen.add(report.id);
    report = byId.get(report.links.parent);
  }
  return report ? sourceOf(report) : null;
}

/** The source card a chain hangs from: the file every parentless report in it reads.
 *
 *  Not a report, and deliberately so. Every chain starts from a file no operation produced,
 *  and until this existed the canvas had nothing to anchor a root to -- four inspections of one
 *  subject drew as four disconnected tiles, which is not what they are. The identity is already
 *  in the reports: they all carry input.path and input.sha256.
 *  @param {any[]} reports  the reports drawn on the canvas
 *  @returns {{key:string, name:string, path:string, sha256:string, role:string, roots:string[],
 *             _x?:number, _y?:number}[]}  _x/_y are filled in by the layout, as on a report. */
export function sourcesOf(reports) {
  const found = new Map();
  const add = (key, card, id) => {
    if (!found.has(key)) found.set(key, { key, roots: [], ...card });
    // The same file can be one report's plain input and another's declared source. Whichever
    // came first, the card keeps the role: a file that some operation said it read as the
    // front three-quarter is that, and an earlier card built from a bare input knows nothing.
    if (card.role && !found.get(key).role) found.get(key).role = card.role;
    found.get(key).roots.push(id);
  };
  for (const report of reports) {
    if (!(report.links && report.links.parent)) {
      const input = report.input || {};
      const key = sourceOf(report);
      add(key, { name: String(input.path || key).split("/").pop() || key,
                 path: String(input.path || ""), sha256: String(input.sha256 || ""), role: "" },
          report.id);
    }
    // A subject read off several files gets a card each, on any report and not only on a
    // parentless one: an operation whose whole job is to read a group had that group nowhere
    // on the canvas, so two images feeding one reading drew as no link at all.
    for (const source of report.sources || []) {
      add(String(source.path || ""),
          { name: String(source.path || "").split("/").pop() || "",
            path: String(source.path || ""), sha256: String(source.sha256 || ""),
            role: String(source.role || "") },
          report.id);
    }
  }
  return [...found.values()];
}

/** The group a report belongs to: its source when it starts a chain, the fork above it when
 *  the parent has more than one child, otherwise whatever group the parent opened.
 *  @param {any} report
 *  @param {Map<string, number>} children
 *  @param {Map<string, string>} groupOf
 *  @returns {string} */
export function groupKey(report, children, groupOf) {
  const parent = report.links && report.links.parent;
  if (!parent) return sourceOf(report);
  return (children.get(parent) || 0) > 1 ? parent : (groupOf.get(parent) ?? sourceOf(report));
}
