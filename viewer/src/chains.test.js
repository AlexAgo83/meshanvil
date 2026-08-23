import { test } from "node:test";
import assert from "node:assert/strict";
import { rootOf, isOrphan, groupKey } from "./chains.js";

/** Two independent starts, a fork under the first, and an orphan reading a work artefact. */
const REPORTS = [
  { id: "001", input: { path: "/src/derived-mesh.stl" }, links: { parent: null } },
  { id: "002", input: { path: "/work/out/a.blend" }, links: { parent: "001" } },
  { id: "002a", input: { path: "/work/out/a.blend" }, links: { parent: "001" } },
  { id: "003", input: { path: "/work/out/b.blend" }, links: { parent: "002a" } },
  { id: "006", input: { path: "/src/p3d.obj" }, links: { parent: null } },
  { id: "007", input: { path: "/work/out/c.blend" }, links: { parent: "006" } },
  { id: "008", input: { path: "/work/out/orphan.blend" }, links: { parent: null } },
];
const BY_ID = new Map(REPORTS.map((r) => [r.id, r]));

test("every report resolves to the start it descends from", () => {
  assert.equal(rootOf(BY_ID, "003"), "001");
  assert.equal(rootOf(BY_ID, "007"), "006");
  assert.equal(rootOf(BY_ID, "001"), "001");
  assert.equal(rootOf(BY_ID, "008"), "008");
});

test("a missing parent stops the walk instead of hanging", () => {
  const lost = new Map([["x", { id: "x", links: { parent: "gone" } }]]);
  assert.equal(rootOf(lost, "x"), "x");
  assert.equal(rootOf(BY_ID, "nope"), null);
});

test("a start reading a work artefact is an orphan, one reading a source is not", () => {
  assert.equal(isOrphan(BY_ID.get("008")), true);
  assert.equal(isOrphan(BY_ID.get("001")), false);
  assert.equal(isOrphan(BY_ID.get("006")), false);
  assert.equal(isOrphan(BY_ID.get("002")), false, "a report with a parent is never an orphan");
});

test("each start opens its own group instead of sharing one", () => {
  const children = new Map();
  for (const r of REPORTS) if (r.links.parent) children.set(r.links.parent, (children.get(r.links.parent) || 0) + 1);
  const groupOf = new Map();
  const keys = new Map();
  for (const r of REPORTS) {
    const key = groupKey(r, children, groupOf);
    groupOf.set(r.id, key);
    keys.set(r.id, key);
  }
  assert.equal(keys.get("001"), "001");
  assert.equal(keys.get("006"), "006");
  assert.equal(keys.get("008"), "008", "the orphan must not land in another chain's group");
  assert.notEqual(keys.get("001"), keys.get("006"), "two starts must never share a group");
  assert.equal(keys.get("002"), "001", "a fork opens a group under the parent");
  assert.equal(keys.get("007"), "006", "a single child stays in its parent's group");
});
