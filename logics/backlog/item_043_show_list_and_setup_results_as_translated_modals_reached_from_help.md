## item_043_show_list_and_setup_results_as_translated_modals_reached_from_help - Show list and setup results as translated modals reached from Help
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:48:56

# AI Context
- Summary: List operations and Check setup render as translated modals built from structured data instead of raw stdout in a menu dropdown, and both move to the Help menu.
- Keywords: translated modal, structured command result, machine-readable list, menu placement, Help menu
- Use when: Changing how a command's result is presented in the viewer.
- Skip when: Changing what either command computes or reports.

# Problem
- `List operations` and `Check setup` dump raw, untranslated process stdout -- a JSON object in the case of setup -- into a `<pre>` inside the menu dropdown that launched them, which stays open behind it.
- Both rows sit in the File menu though neither acts on the current project.

# Scope
- In:
  - A machine-readable form of the operations list, so the modal renders structured data rather than parsing formatted output.
  - A modal for each result, built from the catalogue in both languages, dismissible like the start screen modal.
  - Closing the launching menu when a modal opens.
  - Moving both rows into the Help menu.
  - The Help menu's `Create a runbook <report-id>` row, which `adr_007` left copy-only because its id is a placeholder with no report behind it: either give it the selected report as a real target, or state in the row why it stays a command to copy.
- Out:
  - Changing what either command does or what it reports.
  - `Preview pruning`, which keeps its current presentation in this slice.

# Acceptance criteria
- AC1: The operations list is available in a machine-readable form and the modal renders from it.
- AC2: Both modals show catalogue-resolved strings in both languages, with no raw stdout and no JSON visible to the operator.
- AC3: Opening either modal leaves no menu open behind it, and it is dismissible like the start screen modal.
- AC4: Both rows are in Help and in no other menu.
- AC5: The `Create a runbook` row either carries a real report id or says why it does not; no row shows a placeholder that looks like a value.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: The operations list is available in a machine-readable form and the modal renders from it.
- request-AC8 -> This backlog slice. Proof: AC2: Both modals show catalogue-resolved strings in both languages, with no raw stdout and no JSON visible to the operator.
- request-AC9 -> This backlog slice. Proof: AC3: Opening either modal leaves no menu open behind it, and it is dismissible like the start screen modal.

- request-AC11 -> This backlog slice. Proof: AC5: The `Create a runbook` row either carries a real report id or says why it does not; no row shows a placeholder that looks like a value.

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- The two rows to move: `viewer/index.html:19` (`data-copy="meshanvil list" data-run="list"`) and `viewer/index.html:21` (doctor), each followed by the `<pre class="cmdout" data-cmdout="...">` at `:20` and `:22` that is the raw dump to remove. The Help menu they move into is `viewer/index.html:41`.
- The modal pattern to copy is `#splash`: markup at `viewer/index.html` (`.scrim`, `role="dialog"`, `aria-modal="true"`, a `data-splash="close"` button) and behaviour in `showSplash(show)` (`viewer/viewer.js:797`), which already force-closes every open `details.menu` at `viewer/viewer.js:810` -- that is AC3, and it exists; reuse it rather than re-solving it.
- Client side today: `runCommand(button)` (`viewer/viewer.js:737`) POSTs `{command}` to `/run` and writes `result.stdout` into `[data-cmdout]` (`viewer/viewer.js:740`). Only the rendering changes; the transport is fine.
- Setup is already structured: `doctor.check(root)` (`meshanvil/doctor.py:64`) returns `{requirements: [{name, class, required, state, path, reason, fix}], ok, project: {name, path, resolved_by}}`, printed as JSON by `meshanvil/cli.py:77`, and the viewer already reads a cached copy through `collect_doctor()` (`meshanvil/viewer.py:58`). The modal can render that shape with no new server work.
- The operations list is the one that is not: `show_list()` (`meshanvil/cli.py:46`) formats columns by hand from `manifests.discover()` (`meshanvil/manifests.py:18`), which already returns a dict keyed by operation carrying `engine`, `kind`, `summary_key`, `params` and `manifest_path`. A machine-readable form is a dump of that dict, not new logic. Note `summary_key` is a catalogue key, so the modal translates it client-side like any other.
- The `Create a runbook <report-id>` row is `viewer/index.html:43`; the real command behind it is `meshanvil/cli.py:81`, which calls `logics_bridge.runbook(work_root, code_root, chain)` and needs a real chain id -- which the page has, in the selected report.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_010_direct_controls_over_the_files_and_results_the_viewer_already_names`
- Architecture decision(s): (none yet)
- Request: `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`
- Primary task(s): `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals`

# Notes
- Task `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals` was finished via `logics-manager flow finish task` on 2026-08-23.
