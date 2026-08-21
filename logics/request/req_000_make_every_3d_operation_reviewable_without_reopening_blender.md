## req_000_make_every_3d_operation_reviewable_without_reopening_blender - Make every 3D operation reviewable without reopening Blender
> From version: 1.0.0
> Schema version: 1.0
> Status: Draft
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# AI Context
- Summary: Each headless operation writes a report carrying its measurements and its bounding-box comparison, one command runs it whatever agent is driving, and a local viewer makes the chain readable without opening Blender.
- Keywords: operation report, bounding-box comparison, headless Blender, local viewer, agent-agnostic command
- Use when: Deciding how an operation records what it did, how it is invoked, or how its result is reviewed.
- Skip when: Working on the geometry of one procedure -- the runbooks in logics/runbook/ hold that, not this request.

# Needs
- Reviewing what an operation did must not require opening Blender and navigating to the affected geometry by hand.
- Every operation must leave behind the measurements that verify it, not only its output file.
- The chain of operations that produced a result must be readable in order, with what changed at each step.
- The bounding-box comparison against the source must be computed and shown for every operation, because that single check caught every failure in the delivered chain while the manifold checks passed throughout.
- An operation must be runnable by any agent from a single command, without a Blender-specific or vendor-specific integration.
- Verification renders must sit next to the numbers they illustrate, so a render is read as confirmation and never as evidence on its own.

# Context
- Today every script prints its measurements to stdout and writes its output under work/. The numbers exist but are lost as soon as the terminal scrolls, and nothing links a result to the operation that produced it.
- The operator's stated pain: having to reopen Blender on every change to see what happened.
- The delivered chain is seven pipeline steps plus ad-hoc tools. Each already computes what a report needs -- shell counts, vertex and face counts, bounding boxes, volumes, non-manifold edge counts -- and throws it away.
- tools/render_views.py already produces orthographic verification renders from four fixed directions and writes them under work/renders/, with no link to the operation that motivated them.
- The repository is public and the sources are not. Reports and the viewer must work from work/, which is git-ignored, and must never require a source file to be committed.
- The intent is to drive these operations from more than one agent runtime (Claude Code and Codex at least), so the contract must be a plain command and a plain JSON file rather than an integration.
- The Logics viewer shipped by logics-manager renders Logics documents; it has no extension point for an operation timeline, so this viewer is local to meshanvil rather than a change to that repository.

# Acceptance criteria
- AC1: Every operation writes one report file under work/ops/ carrying its identifier, the script that ran, the input file, the output file, the measurements before and after, and the paths of any renders it produced.
- AC2: Each report states the output bounding box against the input bounding box, per axis, in millimetres, together with the axes that moved.
- AC3: The seven pipeline steps and tools/scan_defects.py write a report through the same helper, so no operation reports in a format of its own.
- AC4: A single command runs one named operation and writes its report, with no argument that depends on the agent runtime driving it.
- AC5: A local viewer lists the operations in execution order and, for a selected one, shows its measurements, its bounding-box comparison and its renders.
- AC6: The viewer reads only the report files. Opening it requires no Blender process, no build step and no network access.
- AC7: An operation that fails writes a report recording the failure and the measurements taken up to that point, rather than leaving no trace.
- AC8: Reports and renders stay under work/, and the publication-hygiene gate still passes with reports present.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): (none yet)

# References
- pipeline/01_visibility_sort.py
- pipeline/02_printable_envelope.py
- pipeline/06_clean_shells.py
- tools/scan_defects.py
- tools/render_views.py
- tools/list_shells.py
- run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility
- run_006_turn_a_cad_assembly_into_a_printable_solid
- run_009_repair_export_defects_in_a_cad_derived_mesh

# Backlog
- `item_001_define_the_operation_report_and_write_one_from_every_operation`
- `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`
- `item_003_read_the_chain_of_operations_in_a_local_viewer`
