#!/usr/bin/env node
import { build } from "esbuild";

await build({
  entryPoints: ["viewer/src/app.js"],
  outfile: "viewer/viewer.js",
  bundle: true,
  format: "iife",
  target: "es2020",
  logLevel: "silent",
});
