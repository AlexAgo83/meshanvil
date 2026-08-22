## task_005_bridge_reports_into_the_logics_corpus - Bridge reports into the Logics corpus
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-23 00:01:14

# AI Context
- Summary: Keep Logics optional through its JSON CLI: evidence after success, live document metadata for chips, and a runbook scaffold from report facts.
- Keywords: bridge, reports, logics, corpus
- Use when: A report needs explicit corpus evidence or its document links need current metadata.
- Skip when: Running or viewing a chain without a Logics bridge request.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_013_bridge_reports_into_the_logics_corpus`

# Acceptance criteria
- AC1: A successful operation run with `--evidence task:AC` appends a proof record carrying the command, the summary and the report path; without the flag the corpus is untouched.
- AC2: A failed operation records no evidence, and says why.
- AC3: Chips render title, kind and status read from the corpus, and a document that no longer exists renders as missing.
- AC4: A chain can scaffold a runbook prefilled with its operations, parameters, failures and numbers, leaving the procedure to be written.
- AC5: With logics-manager absent, operations, reports and the viewer all work, and each bridge states that it is unavailable.
- AC6: No logics-manager module is imported anywhere; every bridge is a subprocess call returning JSON.

# Plan
- [x] Use `python3 -m logics_manager flow progress task task_005_bridge_reports_into_the_logics_corpus.md --progress <n>%` during multi-wave work.
- [x] Run `python3 -m logics_manager flow finish task task_005_bridge_reports_into_the_logics_corpus.md` after implementation.

# Validation
- `make check`
- `./bin/meshanvil view --no-open`
- `node --check viewer/viewer.js`
- `./bin/meshanvil runbook 002`
- `logics-manager lint --require-status`
- `logics-manager audit --group-by-doc`
- `meshanvil run scan_defects … --evidence task_005_bridge_reports_into_the_logics_corpus:AC1` passed: report evidence appended to this task
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Added the optional JSON subprocess boundary and successful-run evidence hook.
- Viewer document chips now resolve title, kind and status from the corpus and call missing references out.
- `meshanvil runbook 002` created `run_011` with operation parameters, outcomes and measurements; the human procedure remains explicitly unverified.
- End-to-end evidence bridge verified with `005_scan_defects.json`.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_013_bridge_reports_into_the_logics_corpus`
- Related request(s): `req_000_make_every_3d_operation_reviewable_without_reopening_blender`

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `meshanvil run scan_defects work/out/fixture_check_voxel30.blend` | result: /users/alexandreagostini/documents/meshanvil/work/ops/005_scan_defects.json | scan_defects succeeded (objects=2, vertices=11936, faces=12038)
- AC2 | date: 2026-08-22 | command: `meshanvil run voxel_remesh … --evidence task_005:AC1` | result: passed | A failed voxel remesh emitted the refusal notice and left the Evidence count unchanged.

# AC Traceability
- request-AC25 -> This task. Proof: `meshanvil run scan_defects work/out/fixture_check_voxel30.blend --evidence task_005:AC1` appended a proof record carrying the command, the summary and the report path; a failed run emitted the refusal notice and left the Evidence count unchanged.
