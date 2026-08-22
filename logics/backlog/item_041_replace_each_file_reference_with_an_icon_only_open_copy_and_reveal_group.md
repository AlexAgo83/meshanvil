## item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group - Replace each file reference with an icon-only open, copy and reveal group
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
- Summary: One renderer for every file reference in the viewer, producing three icon-only controls (open, copy path, reveal) with catalogue-resolved accessible names, and retiring the copyable `blender <path>` command.
- Keywords: file reference renderer, icon-only controls, accessible name, path label rename, opened-from-disk degradation
- Use when: Changing how the viewer presents a file it already names.
- Skip when: Deciding what the server does when a control is clicked -- item_042 holds that.

# Problem
- A file reference is shown as its own path text under the label `path`, wrapped in one copy-to-clipboard button, so the two things an operator usually wants -- open it, show me where it is -- have no control at all.
- The render panel routes opening a .blend file through a `blender <path>` command the operator must paste into a terminal.

# Scope
- In:
  - One shared renderer for a file reference, used everywhere the viewer prints one, producing three icon-only controls with catalogue-resolved accessible names.
  - Renaming the `path` label to `file` in both catalogues.
  - Removing the `blender <path>` copy command in favour of the Open control.
  - The opened-from-disk presentation: Copy path unchanged, Open and Reveal not offered as working controls.
- Out:
  - The server side of Open and Reveal -- the item below owns that.
  - Any icon library or new dependency; inline SVG or text glyphs only.

# Acceptance criteria
- AC1: One renderer produces the three-control group and every file reference in the viewer uses it.
- AC2: Each control has an accessible name from the catalogue and no visible text label.
- AC3: No catalogue string labels a file reference `path`.
- AC4: No `blender <path>` command is offered anywhere.
- AC5: On a page opened from disk Copy path works and the other two are not presented as working controls.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: One renderer produces the three-control group and every file reference in the viewer uses it.
- request-AC2 -> This backlog slice. Proof: AC2: Each control has an accessible name from the catalogue and no visible text label.
- request-AC4 -> This backlog slice. Proof: AC3: No catalogue string labels a file reference `path`.
- request-AC6 -> This backlog slice. Proof: AC4: No `blender <path>` command is offered anywhere.

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
