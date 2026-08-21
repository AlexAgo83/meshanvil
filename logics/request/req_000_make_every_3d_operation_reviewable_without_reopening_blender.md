## req_000_make_every_3d_operation_reviewable_without_reopening_blender - Make every 3D operation reviewable without reopening Blender
> From version: 1.0.0
> Schema version: 1.0
> Status: Draft
> Understanding: 95%
> Confidence: 88%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-21 22:38:39

# AI Context
- Summary: Each headless operation writes a report carrying its measurements and its bounding-box comparison, one command runs it whatever agent is driving, and a local viewer makes the chain readable without opening Blender.
- Keywords: operation report, bounding-box comparison, headless Blender, local viewer, agent-agnostic command
- Use when: Deciding how an operation records what it did, how it is invoked, or how its result is reviewed.
- Skip when: Working on the geometry of one procedure -- the runbooks in logics/runbook/ hold that, not this request.

# Needs
- Reviewing what an operation did must not require opening Blender and navigating to the affected geometry by hand.
- Every operation must leave behind the measurements that verify it, not only its output file.
- The chain of operations that produced a result must be readable in order, with what changed at each step.
- Failed attempts must survive: three failed approaches are recorded in run_007 and they carry most of that runbook's value.
- The generated artefacts must be prunable without erasing the record of what was done, because a blend weighs 200 MB and a report a few kilobytes.
- Two states of the same geometry must be comparable side by side, not only through their numbers: a 30 mm voxel destroys the detail of a part while the volume moves by 3% and every topology check stays green.
- Someone opening the tool for the first time, on an empty work/ops, must be told what to run rather than shown an empty window.
- The tool must be demonstrable without any private geometry, on a scene the repository can regenerate.
- The viewer must never be able to damage anything: it reads, and the command acts.
- The true source is a STEP file that Blender cannot read at all, and re-importing it is what removes the defects the tessellated export introduced. Reading it must be an operation like any other.
- The tool must speak English by default and French on demand, since the repository is public and its author's other work is French.
- Someone arriving with a clone must be taken to a first report: the external tools it needs, which are optional, and what to run when one is missing -- stated before an operation fails deep inside an engine.
- The tool must open on Windows and on WSL, not only on macOS, since that is where the operator's other machines are.
- An agent must be able to drive the tool without parsing prose: an exit code, a report path, and a report that records what was actually run.
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
- AC9: The history is a tree: a report names the report it follows, sibling attempts are visible as siblings, and a failed attempt is kept rather than discarded.
- AC10: Heavy artefacts can be pruned without losing the record. A report survives the deletion of the file it describes and states that the artefact was pruned, with the date.
- AC11: Two states of the same geometry can be compared visually, on the same camera, in each of the canonical views, with the numeric difference shown beside the images.
- AC12: On a first run with no report present, the tool states what it can do, what it found in its environment, and the command that produces the first report. No area of the interface is left blank without an explanation.
- AC13: The demonstration data is generated by the repository, carries real defects, and is found by the existing sweep without being told where they are. No third-party file, no binary committed.
- AC14: The viewer starts no process and writes nothing. Every action it offers is shown as the command that performs it.
- AC15: A report leads to the runbook it applied, and a runbook lists the operations that applied it, both derived from the links already in the reports.
- AC16: A STEP source is ingested headless through a second engine, reported like any other operation, and a missing engine is refused clearly without affecting the rest.
- AC17: Every operator-facing string comes from a catalogue, English by default and French available, with a check that fails when the two drift.
- AC18: A report records the parameters actually used and the versions of the tool and engine that produced it, so two reports are comparable or knowably not.
- AC19: The command returns a distinct exit code for an operation that failed, a command that refused to run, and an engine that died without reporting; the report path is always the last line of its output.
- AC20: Concurrent runs never collide: identities are allocated so two agents cannot obtain the same one, and two operations never write the same target at once.
- AC21: An operation that runs for minutes proves it is alive, so a caller can tell slow from hung.
- AC22: The viewer treats every value read from a report as text, never as markup.
- AC24: Getting from a clone to a first report is guided: every requirement is named with its state and its reason, a missing one is refused before an operation starts rather than from inside it, and each fix is shown as a command for the platform in front of the operator.
- AC23: The tool runs on macOS, on Windows and in WSL, including the case where the host is Linux and the engine is a Windows binary; what was not verified is stated as unverified.

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
- `item_004_prune_heavy_artefacts_without_losing_the_record`
- `item_005_compare_two_states_of_the_same_geometry`
- `item_006_open_on_nothing_first_run_and_environment_checks`
- `item_007_regenerate_the_demo_fixture_from_the_repository`
- `item_008_read_the_method_from_the_reports_runbook_reverse_index`
- `item_009_ingest_a_step_source_through_a_second_engine`
- `item_010_speak_english_by_default_and_french_on_demand`
- `item_011_run_on_macos_windows_and_wsl`
- `item_012_take_the_operator_through_setup_step_by_step`
