## task_010_ingest_a_step_source_through_a_second_engine - Ingest a STEP source through a second engine
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 88%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:58:43

# AI Context
- Summary: FreeCAD receives the normal job file, writes an STL and report directly, and owns its import heartbeat without a Blender-side import.
- Keywords: ingest, step, source, through, second, engine
- Use when: Bringing a STEP source into `work/out/` for normal mesh operations.
- Skip when: Repairing geometry or making FreeCAD a global runtime requirement.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_009_ingest_a_step_source_through_a_second_engine`

# Acceptance criteria
- AC1: A STEP source is read headless and a mesh is written under work/out/, with no interactive FreeCAD session.
- AC2: The report names `engine: freecad` with its version, and records the tessellation parameters actually used.
- AC3: The report states the number of solids read, and the bounding box of the result against the bounding box of the source.
- AC4: A missing FreeCAD is refused with exit code 2 and a message naming the override, and no Blender operation is affected.
- AC5: The import reports progress, so a caller can tell a slow import from a hung one.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_010_ingest_a_step_source_through_a_second_engine.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_010_ingest_a_step_source_through_a_second_engine.md` after implementation.

# Validation
- `make check`
- `./bin/meshanvil list` exposes `import_step` with `engine: freecad`
- Missing source refusal exits 2 before any engine is launched
- Real STEP import remains pending a local non-versioned STEP source

# Report
- Added the FreeCAD job command, `import_step` manifest and headless script with progress, source solid count, bounds and recorded tessellation parameters.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
