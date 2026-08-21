## item_009_ingest_a_step_source_through_a_second_engine - Ingest a STEP source through a second engine
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 99%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:09:49

# AI Context
- Summary: A STEP file read by FreeCAD headless and converted to a working mesh, as an operation like any other: same job contract, same report, engine named freecad.
- Keywords: STEP, FreeCAD, second engine, solids, tessellation, ingestion
- Use when: Bringing a CAD source into the chain, or deciding what a non-Blender engine may do.
- Skip when: Anything downstream of the mesh: once ingested, it is an ordinary operation.

# Problem
- The true source of this work is a 508 MB STEP file carrying 1319 closed solids, and Blender cannot read STEP at all.
- Everything fought in the delivered chain came from working off a tessellated export instead: zero-thickness surfaces, split vertices, a flat hierarchy and a resolution frozen at export time.
- FreeCAD 1.0 is installed and can do it headless, but the README named a binary that does not exist on this machine, so nothing about the route was actually verified.

# Scope
- In:
  - An `import_step` operation with `engine: freecad`, run as `/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c <script>`, overridable by MESHANVIL_FREECAD.
  - The same job contract as a Blender operation: a job JSON in, a report JSON out, nothing parsed from stdout.
  - Tessellation parameters recorded in `params` -- linear and angular deviation -- because they are the resolution the export froze and the reason to re-import at all.
  - A report carrying what the source held: solid count, per-solid names where the STEP has them, the hierarchy depth, and the bounding box.
  - A mesh written under work/out/ that the rest of the chain treats as any other input.
  - Progress reporting, since this import is long and memory-hungry: it is the operation that most needs a heartbeat.
- Out:
  - Editing or repairing B-Rep geometry in FreeCAD. It reads and tessellates; the mesh work stays in Blender.
  - Making FreeCAD a requirement for the rest of the tool: an operation whose engine is missing is refused with exit code 2, and every Blender operation keeps working.
  - Assembly constraints, materials, or PMI data from the STEP.

# Acceptance criteria
- AC1: A STEP source is read headless and a mesh is written under work/out/, with no interactive FreeCAD session.
- AC2: The report names `engine: freecad` with its version, and records the tessellation parameters actually used.
- AC3: The report states the number of solids read, and the bounding box of the result against the bounding box of the source.
- AC4: A missing FreeCAD is refused with exit code 2 and a message naming the override, and no Blender operation is affected.
- AC5: The import reports progress, so a caller can tell a slow import from a hung one.

# AC Traceability
- request-AC16 -> This backlog slice. Proof: AC1: A STEP source is read headless and a mesh is written under work/out/, with no interactive FreeCAD session.
- request-AC1 -> This backlog slice, partially. Proof: AC2: the report names its engine and records the parameters used.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_004_target_technology_and_process_model`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_004_target_technology_and_process_model`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.

# Tasks
- `task_010_ingest_a_step_source_through_a_second_engine`
