#!/usr/bin/env node
import { readFile, writeFile } from "node:fs/promises";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { build } from "esbuild";

const dir = await mkdtemp(join(tmpdir(), "meshanvil-viewer-"));
const out = join(dir, "viewer.js");
try {
  await build({
    entryPoints: ["viewer/src/app.js"],
    outfile: out,
    bundle: true,
    format: "iife",
    target: "es2020",
    logLevel: "silent",
  });
  const [expected, actual] = await Promise.all([
    readFile(out, "utf8"),
    readFile("viewer/viewer.js", "utf8"),
  ]);
  if (expected !== actual) {
    await writeFile(out, expected);
    throw new Error("viewer/viewer.js is stale; run `npm run build:viewer`");
  }
  console.log("viewer bundle: ok");
} finally {
  await rm(dir, { recursive: true, force: true });
}
