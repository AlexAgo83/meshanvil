// @ts-check

/** Report text is data from CAD files, never markup. */
export function esc(value) {
  return String(value === null || value === undefined ? "" : value)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function inline(escaped) {
  return escaped
    .replace(/`([^`]+)`/g, (_, code) => `<code>${code}</code>`)
    .replace(/\*\*([^*]+)\*\*/g, (_, bold) => `<strong>${bold}</strong>`);
}

export function mdToHtml(source) {
  const lines = String(source || "").split("\n");
  const out = [];
  let list = null;
  let quote = [];
  let para = [];
  let fence = null;
  const closeList = () => { if (list) { out.push(`</${list}>`); list = null; } };
  const closeQuote = () => { if (quote.length) { out.push(`<blockquote>${quote.join("<br>")}</blockquote>`); quote = []; } };
  const closePara = () => { if (para.length) { out.push(`<p>${para.join(" ")}</p>`); para = []; } };
  const closeAll = () => { closeList(); closeQuote(); closePara(); };
  for (const raw of lines) {
    if (fence !== null) {
      if (raw.trimEnd() === "```") { out.push("</code></pre>"); fence = null; }
      else out.push(esc(raw) + "\n");
      continue;
    }
    const fenceStart = raw.match(/^```/);
    const heading = raw.match(/^(#{1,6})\s+(.*)$/);
    const quoted = raw.match(/^>\s?(.*)$/);
    const bullet = raw.match(/^\s*[-*]\s+(.*)$/);
    const numbered = raw.match(/^\s*\d+\.\s+(.*)$/);
    if (fenceStart) { closeAll(); out.push("<pre><code>"); fence = true; }
    else if (heading) { closeAll(); out.push(`<h${heading[1].length + 1}>${inline(esc(heading[2]))}</h${heading[1].length + 1}>`); }
    else if (quoted) { closeList(); closePara(); quote.push(inline(esc(quoted[1]))); }
    else if (bullet) { closeQuote(); closePara(); if (list !== "ul") { closeList(); out.push("<ul>"); list = "ul"; } out.push(`<li>${inline(esc(bullet[1]))}</li>`); }
    else if (numbered) { closeQuote(); closePara(); if (list !== "ol") { closeList(); out.push("<ol>"); list = "ol"; } out.push(`<li>${inline(esc(numbered[1]))}</li>`); }
    else if (raw.trim() === "") { closeAll(); }
    else { closeList(); closeQuote(); para.push(inline(esc(raw.trim()))); }
  }
  if (fence !== null) out.push("</code></pre>");
  closeAll();
  return out.join("\n");
}
