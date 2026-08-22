## item_001_define_the_operation_report_and_write_one_from_every_operation - Define the operation report and write one from every operation
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 95%
> Confidence: 90%
> Progress: 100%
> Complexity: Low
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:13:25

# AI Context
- Summary: One JSON report per operation under work/ops/, written by a single helper, carrying counts, bounding boxes before and after, the per-axis delta, render paths, and a failure path that still reports.
- Keywords: operation report, report writer, bounding-box delta, work/ops, failure report
- Use when: Changing what an operation records, or adding an operation that must report like the others.
- Skip when: Deciding how an operation is invoked (item_002) or displayed (item_003).

# Problem
- Each script prints its measurements to stdout and they are lost when the terminal scrolls.
- Twelve scripts exist, and they are not of one kind: seven transform a file, five only measure and produce no output at all. A format built around an input and an output cannot describe the second kind.
- Nothing links an output file to the operation, the input and the settings that produced it.
- The bounding-box comparison is described in the runbooks as the check that caught every failure, but it is computed by hand, differently, in each script.

# Scope
- In:
  - A report writer helper in tools/, producing work/ops/NNN_<name>.json, with the envelope and the two payloads settled in `adr_001_operation_report_format`.
  - The shared envelope: schema_version, id, created_at, kind (transform or inspection), operation, script, status, input with its SHA-256, warnings, renders, links.
  - The shared measurement block: objects, vertices, faces, bbox_mm, shells, non_manifold_edges, volume_cm3 -- null when the operation did not measure it, never zero and never absent.
  - The per-axis bounding-box delta computed by the helper from before and after, naming the axes that moved, so no operation can skip it.
  - Warnings as short codes rather than sentences, so what was not checked is stated and an agent can act on it.
  - links.parent carrying the report this one follows, and wiki-style references to the documents involved, so the history is a tree readable from the files alone.
  - params carrying every parameter with the value actually used, read from the operation's manifest, and tool carrying the meshanvil, engine and platform versions.
  - engine naming which binary produced the report: blender or freecad.
  - output.state as present, pinned or pruned, with the date it changed -- declared now so no report needs migrating when a pruning policy arrives.
  - A failure path that writes the report with the error and whatever was measured before it.
  - Operations live in tools/ as parameterised scripts with a manifest. `pipeline/` is kept as the record of the delivered chain, hardcoded to it, and is not converted: generalising a step and preserving the step that produced the delivery are two different goals, and the second is worth keeping.
  - Converted so far: scan_defects (inspection, transform when it fixes), voxel_remesh, ray_visibility, list_shells, clean_shells, recenter. Remaining from the delivered chain: the hatch cut, the appendage weld and the box cut, which carry hardcoded coordinates and need a parameter design before they generalise.
- Out:
  - The runner command and the viewer, which are separate slices.
  - The pruning policy itself: this slice declares output.state, item_004 decides what sets it.
  - Any schema migration tooling. schema_version is written from the first report; nothing reads an older one yet.

# Acceptance criteria
- AC1: Running any converted operation leaves exactly one report file under work/ops/, named with its execution order and operation name.
- AC2: The report states the bounding box before and after in millimetres and names the axes that moved, matching what the script prints.
- AC3: An operation raising an exception still leaves a report whose status is failed and which carries the error text.
- AC4: The report writer is the only place a report is written; no script serialises one of its own.
- AC5: An inspection script, which has no output file, produces a valid report of kind inspection carrying its findings.
- AC6: A measurement an operation did not take is null in the report, distinguishable from a measured zero.
- AC7: Every report carries the SHA-256 of its input, and links.parent when it follows another operation.
- AC8: What an operation did not verify appears in warnings as a code, not as prose.
- AC9: Every report records the parameters actually used, defaults included and with their units, and the versions of the tool and the engine that produced it.
- AC10: A written report matches the canonical shapes in `adr_001_operation_report_format` field for field, for a transform and for an inspection.
- AC11: The report names its engine, so a Blender report and a FreeCAD report are distinguishable without reading the script name.

# AC Traceability
> Shared proof: AC3, AC7
- request-AC1 -> This backlog slice. Proof: AC1: Running any of the eight operations leaves exactly one report file under work/ops/, named with its execution order and operation name.
- request-AC2 -> This backlog slice. Proof: AC2: The report states the bounding box before and after in millimetres and names the axes that moved, matching what the script prints.
- request-AC3 -> This backlog slice. Proof: AC3: An operation raising an exception still leaves a report whose status is failed and which carries the error text.
- request-AC7 -> This backlog slice. Proof: AC3: An operation raising an exception still leaves a report whose status is failed and which carries the error text.

- request-AC18 -> This backlog slice. Proof: AC9: Every report records the parameters actually used and the tool and engine versions that produced it.

# Decision framing
- Product framing: Not needed
- Architecture framing: `adr_001_operation_report_format`

# Links
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): `adr_001_operation_report_format`
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Primary task(s): `task_001_deliver_the_reviewable_operation_loop`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Notes
- Task `task_001_deliver_the_reviewable_operation_loop` was finished via `logics-manager flow finish task` on 2026-08-22.
