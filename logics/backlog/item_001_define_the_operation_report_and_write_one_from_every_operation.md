## item_001_define_the_operation_report_and_write_one_from_every_operation - Define the operation report and write one from every operation
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: One JSON report per operation under work/ops/, written by a single helper, carrying counts, bounding boxes before and after, the per-axis delta, render paths, and a failure path that still reports.
- Keywords: operation report, report writer, bounding-box delta, work/ops, failure report
- Use when: Changing what an operation records, or adding an operation that must report like the others.
- Skip when: Deciding how an operation is invoked (item_002) or displayed (item_003).

# Problem
- Each script prints its measurements to stdout and they are lost when the terminal scrolls.
- Nothing links an output file to the operation, the input and the settings that produced it.
- The bounding-box comparison is described in the runbooks as the check that caught every failure, but it is computed by hand, differently, in each script.

# Scope
- In:
  - A report writer helper in tools/, taking the scene before and after and producing work/ops/NNN_<name>.json.
  - Report fields: identifier, script, timestamp, input path, output path, object and vertex counts before and after, bounding box before and after in millimetres, per-axis delta, shell count, non-manifold edge count, volume when meaningful, render paths, and a free-form measurements object for what is specific to one operation.
  - A failure path that writes the report with the error and whatever was measured before it.
  - The seven pipeline steps and tools/scan_defects.py calling the helper.
- Out:
  - The runner command and the viewer, which are separate slices.
  - Any schema versioning beyond a schema_version field.

# Acceptance criteria
- AC1: Running any of the eight operations leaves exactly one report file under work/ops/, named with its execution order and operation name.
- AC2: The report states the bounding box before and after in millimetres and names the axes that moved, matching what the script prints.
- AC3: An operation raising an exception still leaves a report whose status is failed and which carries the error text.
- AC4: The report writer is the only place a report is written; no script serialises one of its own.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Running any of the eight operations leaves exactly one report file under work/ops/, named with its execution order and operation name.
- request-AC2 -> This backlog slice. Proof: AC2: The report states the bounding box before and after in millimetres and names the axes that moved, matching what the script prints.
- request-AC3 -> This backlog slice. Proof: AC3: An operation raising an exception still leaves a report whose status is failed and which carries the error text.
- request-AC7 -> This backlog slice. Proof: AC4: The report writer is the only place a report is written; no script serialises one of its own.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): (none yet)
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Primary task(s): `task_001_deliver_the_reviewable_operation_loop`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
