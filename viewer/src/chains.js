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
