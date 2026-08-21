## item_003_read_the_chain_of_operations_in_a_local_viewer - Read the chain of operations in a local viewer
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 95%
> Confidence: 90%
> Progress: 50%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:13:25

# AI Context
- Summary: A static local page over work/ops/: operations in execution order, and for one of them its measurements, its per-axis bounding-box comparison and its renders side by side.
- Keywords: local viewer, operation timeline, verification renders, static page, no build step
- Use when: Changing how an operator reviews what an operation did.
- Skip when: Anything that runs or edits geometry -- the viewer only reads reports.

# Problem
- Reviewing an operation means reopening Blender and navigating to the affected geometry, which is slow enough that the review is skipped.
- The measurements and the renders exist separately, so the render is read on its own -- exactly the mistake the runbooks warn against.
- There is no view of the chain: which operation ran before this one, and what it changed.
- The history is a tree, not a line: `run_007` records three failed approaches before the one that worked, and a flat list cannot show that they were siblings.

# Scope
- In:
  - Built: `meshanvil view` generates work/viewer/data.js beside the page, opens it, and `--serve` starts a stdlib server on 127.0.0.1 for auto-refresh. The JSDoc types are checked by `make types`, and a report produced by a different engine version than the rest of its chain is flagged rather than compared silently.
  - A static local page rendering the chain as a deterministic top-down DAG built from links.parent: time vertical, branches horizontal, status and the axes that moved shown per node.
  - Failed operations rendered as branches that are kept, not as errors to dismiss.
  - The wiki-style references a report carries followed as links, so a report leads to the runbook it applied and back.
  - A detail view for one operation: its measurements, its bounding-box comparison against the input, and its renders next to the numbers they illustrate.
  - Reading report files directly from work/ops/ with no build step and no server requirement.
  - Rendering the DAG with the Mermaid bundle vendored by the logics-manager dependency, so the page stays offline without a CDN and without a copy of our own (see `adr_002_depend_on_logics_manager_and_reuse_its_structure`).
  - The local-server conventions the Logics viewer already proved: bound to 127.0.0.1, --port 0, read-only, refreshed on an interval.
  - An image editor beside the graph: the selected operation's renders shown large, one per canonical direction, with the path and camera of the one on screen.
  - The tile thumbnail named as what it is -- the operation's first render -- so its provenance is never a guess.
  - Menus that name the available actions and show the command each one runs, never executing anything (`adr_003_the_viewer_reads_the_command_acts`).
  - Every value read from a report escaped before it reaches the page: object names, paths and findings come from CAD files and are data, never markup.
  - A visible signal when two reports were produced by different tool or engine versions, so their numbers are not compared silently.
  - Plain JavaScript typed with JSDoc, checked by `tsc --checkJs --noEmit` and wired into `make check`, with the report contract as the typed surface.
  - An empty state that explains how to produce the first report.
- Out:
  - Editing, re-running or triggering operations from the viewer.
  - A force-directed graph view. On this node count a physics layout says less than a tree and discards the ordering; it stays an open question in prod_001 until a tree measurably fails.
  - A 3D viewport. The renders an operation produced are what is shown.
  - Integration into the Logics viewer, and reuse of its browser-host and stylesheet: they render workflow documents, and an operation timeline is not one.
  - The before/after comparison (item_005), the first-run screen (item_006) and the runbook reverse index (item_008), which are their own slices.
  - A framework and a build step. `adr_004_target_technology_and_process_model` records why, and what would make it worth revisiting.

# Acceptance criteria
- AC1: Opening the viewer with reports present renders them as a top-down DAG in execution order, with each node's status.
- AC5: Two operations sharing a parent are shown as siblings, and a failed one is kept in the tree rather than hidden.
- AC6: The selected operation's renders are shown large, one per canonical direction, with the path and camera of the one displayed.
- AC7: No menu entry runs anything: each shows the command that performs the action.
- AC8: The viewer sources type-check under `tsc --checkJs --noEmit`, and the check runs in `make check`.
- AC9: The page loads with no build step and no module script, so it opens from disk as well as from the opt-in server.
- AC10: A report field containing markup renders as text, proven by a report whose object name contains angle brackets.
- AC11: Two operations produced by different engine versions are shown as such rather than compared silently.
- AC2: Selecting an operation shows its measurements, its per-axis bounding-box comparison and its renders on one page.
- AC3: The viewer opens with no Blender process running, no build step and no network access.
- AC4: With no reports present the viewer states how to produce one instead of failing.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: Opening the viewer with reports present lists them in execution order with each one's status.
- request-AC6 -> This backlog slice. Proof: AC2: Selecting an operation shows its measurements, its per-axis bounding-box comparison and its renders on one page.
- request-AC8 -> This backlog slice. Proof: AC3: The viewer opens with no Blender process running, no build step and no network access.

- request-AC22 -> This backlog slice. Proof: AC10: A report field containing markup renders as text.

# Decision framing
- Product framing: Not needed
- Architecture framing: `adr_002_depend_on_logics_manager_and_reuse_its_structure`

# Links
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): `adr_002_depend_on_logics_manager_and_reuse_its_structure`, `adr_003_the_viewer_reads_the_command_acts`, `adr_004_target_technology_and_process_model`
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Primary task(s): `task_001_deliver_the_reviewable_operation_loop`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
