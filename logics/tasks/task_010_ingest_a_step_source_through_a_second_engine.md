## task_010_ingest_a_step_source_through_a_second_engine - Ingest a STEP source through a second engine
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
> Indicators reviewed: 2026-08-23 00:01:15

# AI Context
- Summary: FreeCAD receives the normal job file, writes an STL and report directly, and owns its import heartbeat without a Blender-side import.
- Keywords: ingest, step, source, through, second, engine
- Use when: Bringing a STEP source into `work/out/` for normal mesh operations.
- Skip when: Repairing geometry or making FreeCAD a global runtime requirement.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_009_ingest_a_step_source_through_a_second_engine`

# Acceptance criteria
- AC1: A STEP source is read headless and a mesh is written under work/out/, with no interactive FreeCAD session.
- AC2: The report names `engine: freecad` with its version, and records the tessellation parameters actually used.
- AC3: The report states the number of solids read, and the bounding box of the result against the bounding box of the source.
- AC4: A missing FreeCAD is refused with exit code 2 and a message naming the override, and no Blender operation is affected.
- AC5: The import reports progress, so a caller can tell a slow import from a hung one.

# Plan
- [x] Use `python3 -m logics_manager flow progress task task_010_ingest_a_step_source_through_a_second_engine.md --progress <n>%` during multi-wave work.
- [x] Run `python3 -m logics_manager flow finish task task_010_ingest_a_step_source_through_a_second_engine.md` after implementation.

# Validation
- `make check`
- `./bin/meshanvil list` exposes `import_step` with `engine: freecad`
- Missing source refusal exits 2 before any engine is launched
- `tools/make_step_fixture.py` + `meshanvil run import_step work/in/fixture_box.step` passed with FreeCAD 1.0.2: one solid, 40×30×20 mm bounds and `work/out/fixture_box_step.stl`
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Added the FreeCAD job command, `import_step` manifest and headless script with progress, source solid count, bounds and recorded tessellation parameters.
- Corrected the source-read-only guard: only FreeCAD STEP ingestion may read `work/in/`; all Blender operations remain refused there.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_009_ingest_a_step_source_through_a_second_engine`
- Related request(s): `req_000_make_every_3d_operation_reviewable_without_reopening_blender`

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `meshanvil run import_step work/in/fixture_box.step` | result: passed | FreeCAD 1.0.2 imported the generated STEP box headlessly and wrote work/out/fixture_box_step.stl.
- AC3 | date: 2026-08-22 | command: `meshanvil run import_step work/in/fixture_box.step` | result: passed | The import report recorded one solid and a 40×30×20 mm source/result bounding box.

# AC Traceability
- request-AC16 -> This task. Proof: `meshanvil run import_step work/in/fixture_box.step` imported the generated STEP box headlessly through FreeCAD 1.0.2 and wrote a normal report; a missing engine is refused with exit code 2 without affecting other operations.
