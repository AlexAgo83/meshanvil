import { test } from "node:test";
import assert from "node:assert/strict";
import { rootOf, sourceOf, groupKey } from "./chains.js";

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
