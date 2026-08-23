/** Chain identity: which start a report descends from, and whether that start is legitimate.
 *
 *  Kept out of app.js so it can be checked without a DOM: these three rules decide what the
 *  outliner groups and what the canvas draws, and getting them wrong merges unrelated runs
 *  under one name. Voir adr_007.
 */

/** The root a report descends from, walking parents until one has none.
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
  return report ? report.id : null;
}

/** A start reads a source file. One that reads a .blend is an artefact nothing claims to have
 *  produced -- an orphan, and naming it a chain would hide how it got there.
 *  @param {any} report
 *  @returns {boolean} */
export function isOrphan(report) {
  if (report.links && report.links.parent) return false;
  return /\.blend$/i.test(String((report.input || {}).path || ""));
}

/** The group a report belongs to: its own id when it starts a chain, the fork above it when
 *  the parent has more than one child, otherwise whatever group the parent opened.
 *  @param {any} report
 *  @param {Map<string, number>} children
 *  @param {Map<string, string>} groupOf
 *  @returns {string} */
export function groupKey(report, children, groupOf) {
  const parent = report.links && report.links.parent;
  if (!parent) return report.id;
  return (children.get(parent) || 0) > 1 ? parent : (groupOf.get(parent) ?? report.id);
}
