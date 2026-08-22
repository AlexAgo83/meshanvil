#!/usr/bin/env node
import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const LIMIT = 300;
const EXCEPTIONS = {
  "viewer/src/app.js": "legacy viewer body, split by screen as the next slices touch each screen",
};

async function files(dir) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...await files(path));
    else if (entry.name.endsWith(".js")) out.push(path);
  }
  return out;
}

let failed = false;
for (const path of await files("viewer/src")) {
  const lines = (await readFile(path, "utf8")).split("\n").length;
  if (lines > LIMIT && !EXCEPTIONS[path]) {
    console.error(`${path}: ${lines} lines exceeds ${LIMIT}`);
    failed = true;
  }
}
if (failed) process.exit(1);
console.log("line budget: ok");
