import { test } from "node:test";
import assert from "node:assert/strict";
import { rootOf, sourceOf, sourcesOf, groupKey } from "./chains.js";

/** Two independent starts, a fork under the first, and -- the case that broke it -- three
 *  operations reading the same subject directly, none of which has a parent. */
const REPORTS = [
  { id: "001", input: { path: "/work/out/subject.blend" }, links: { parent: null } },
  { id: "002", input: { path: "/work/out/subject.blend" }, links: { parent: null } },
  { id: "003", input: { path: "/work/out/subject.blend" }, links: { parent: null } },
  { id: "004", input: { path: "/work/out/subject.blend" }, links: { parent: "003" } },
  { id: "005", input: { path: "/work/out/subject.blend" }, links: { parent: "003" } },
  { id: "006", input: { path: "/src/other.obj" }, links: { parent: null } },
  { id: "007", input: { path: "/work/out/other_a.blend" }, links: { parent: "006" } },
];
const BY_ID = new Map(REPORTS.map((r) => [r.id, r]));

test("every report resolves to the source its chain starts from", () => {
  assert.equal(rootOf(BY_ID, "004"), "/work/out/subject.blend");
  assert.equal(rootOf(BY_ID, "001"), "/work/out/subject.blend");
  assert.equal(rootOf(BY_ID, "007"), "/src/other.obj");
  assert.notEqual(rootOf(BY_ID, "001"), rootOf(BY_ID, "007"));
});

test("a missing parent stops the walk instead of hanging", () => {
  const lost = new Map([["x", { id: "x", input: { path: "/p" }, links: { parent: "gone" } }]]);
  assert.equal(rootOf(lost, "x"), "/p");
  assert.equal(rootOf(BY_ID, "nope"), null);
});

test("a report with no input falls back to its own id", () => {
  assert.equal(sourceOf({ id: "042", links: { parent: null } }), "042");
});

test("parentless reports on one subject are one chain, not one each", () => {
  const children = new Map();
  for (const r of REPORTS) if (r.links.parent) children.set(r.links.parent, (children.get(r.links.parent) || 0) + 1);
  const groupOf = new Map(), keys = new Map();
  for (const r of REPORTS) {
    const key = groupKey(r, children, groupOf);
    groupOf.set(r.id, key);
    keys.set(r.id, key);
  }
  assert.equal(keys.get("001"), keys.get("002"), "two sweeps of the same subject split into two chains");
  assert.equal(keys.get("002"), keys.get("003"));
  assert.notEqual(keys.get("001"), keys.get("006"), "two subjects must never share a group");
  assert.equal(keys.get("004"), "003", "a fork opens a group under the parent");
  assert.equal(keys.get("007"), keys.get("006"), "a single child stays in its parent's group");
});

test("one source card per file, carrying every root that reads it", () => {
  const sources = sourcesOf(REPORTS);
  assert.equal(sources.length, 2, "two subjects, two source cards");
  const subject = sources.find((s) => s.key === "/work/out/subject.blend");
  assert.deepEqual(subject.roots, ["001", "002", "003"],
    "every parentless report on that file hangs from its card");
  assert.equal(subject.name, "subject.blend", "the card is named after the file, not the path");
  const other = sources.find((s) => s.key === "/src/other.obj");
  assert.deepEqual(other.roots, ["006"]);
});

test("a report with a parent never gets a source card of its own", () => {
  const sources = sourcesOf(REPORTS);
  const claimed = sources.flatMap((s) => s.roots);
  for (const id of ["004", "005", "007"]) {
    assert.ok(!claimed.includes(id), `${id} descends from another report and needs no card`);
  }
});

test("a group of sources draws one card each, all feeding the same report", () => {
  // The reading operation declares the images it was read from. Its own input -- the file
  // that names the group -- is a card too: it is what the chain hangs from.
  const reading = { id: "011", links: { parent: null },
                    input: { path: "/p/work/in/group.txt", sha256: "aa" },
                    sources: [{ path: "/p/work/in/front.png", sha256: "bb", role: "front three-quarter" },
                              { path: "/p/work/in/rear.png", sha256: "cc", role: "rear three-quarter" }] };
  const built = { id: "013", links: { parent: "011" }, input: { path: "/p/work/out/plan.json" } };
  const cards = sourcesOf([reading, built]);
  assert.deepEqual(cards.map((c) => c.name), ["group.txt", "front.png", "rear.png"]);
  assert.deepEqual(cards.map((c) => c.roots), [["011"], ["011"], ["011"]]);
  assert.equal(cards[1].role, "front three-quarter");
  // The child reads the plan, not the images: it must not pick up a card of its own here.
  assert.equal(cards.length, 3);
});

test("the same file read by two operations is one card feeding both", () => {
  const a = { id: "001", links: { parent: null }, input: { path: "/p/g.txt", sha256: "aa" },
              sources: [{ path: "/p/front.png", sha256: "bb", role: "front" }] };
  const b = { id: "002", links: { parent: null }, input: { path: "/p/g.txt", sha256: "aa" },
              sources: [{ path: "/p/front.png", sha256: "bb", role: "front" }] };
  const cards = sourcesOf([a, b]);
  assert.equal(cards.length, 2);
  assert.deepEqual(cards[1].roots, ["001", "002"]);
});

test("a file that is one report's input and another's declared source keeps the role", () => {
  const plain = { id: "001", links: { parent: null }, input: { path: "/p/front.png", sha256: "bb" } };
  const reading = { id: "015", links: { parent: null }, input: { path: "/p/g.txt", sha256: "aa" },
                    sources: [{ path: "/p/front.png", sha256: "bb", role: "front three-quarter" }] };
  assert.equal(sourcesOf([plain, reading])[0].role, "front three-quarter");
  assert.equal(sourcesOf([reading, plain])[1].role, "front three-quarter");
});
