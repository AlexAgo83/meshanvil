## item_043_show_list_and_setup_results_as_translated_modals_reached_from_help - Show list and setup results as translated modals reached from Help
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:19:03

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
- Out:
  - Changing what either command does or what it reports.
  - `Preview pruning`, which keeps its current presentation in this slice.

# Acceptance criteria
- AC1: The operations list is available in a machine-readable form and the modal renders from it.
- AC2: Both modals show catalogue-resolved strings in both languages, with no raw stdout and no JSON visible to the operator.
- AC3: Opening either modal leaves no menu open behind it, and it is dismissible like the start screen modal.
- AC4: Both rows are in Help and in no other menu.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: The operations list is available in a machine-readable form and the modal renders from it.
- request-AC8 -> This backlog slice. Proof: AC2: Both modals show catalogue-resolved strings in both languages, with no raw stdout and no JSON visible to the operator.
- request-AC9 -> This backlog slice. Proof: AC3: Opening either modal leaves no menu open behind it, and it is dismissible like the start screen modal.

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
