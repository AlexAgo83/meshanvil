## item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group - Replace each file reference with an icon-only open, copy and reveal group
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 65%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:34:59

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

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- Every site that renders a file today, all in `viewer/viewer.js`: report Input `viewer/viewer.js:491`, report Output `viewer/viewer.js:497`, the Artefact provenance `viewer/viewer.js:519`, the render provenance `viewer/viewer.js:629`, and the `blender <path>` command to delete `viewer/viewer.js:635`. Five call sites, one renderer to replace them.
- The mechanism already in place: `cmdButton(label, full)` (`viewer/viewer.js:698`) builds the button, `copyCommand(button)` (`viewer/viewer.js:705`) copies -- async clipboard first, a hidden textarea plus `execCommand("copy")` where permission is refused (`viewer/viewer.js:722`) -- and one delegated `[data-copy]` handler dispatches every one of them (`viewer/viewer.js:837`). Add controls to that delegation rather than binding listeners per button.
- The opened-from-disk test already exists and is a protocol read, not a probe: `const SERVED = location.protocol !== "file:" && !!DATA.run_token` (`viewer/viewer.js:29`). Reuse it; `adr_007` chose it deliberately over a capability probe.
- `esc()` (`viewer/viewer.js:58`) is the only escaping in the client and `req_000` AC22 requires every report value to pass through it. An icon control still renders a report-supplied path into an attribute, so it is not exempt.
- The `path` label is a hardcoded English literal `<dt>path</dt>` at `viewer/viewer.js:491` and `:497` -- it never went through the catalogue at all. Renaming it to `file` means introducing the key, not editing one.
- `scripts/i18n_check.py:38` discovers used keys by regex over `t("key")` and `data-i18n="key"` across `meshanvil/ viewer/ scripts/ bin/`. An accessible name reaching the DOM by any other route reads as an unused key and fails `make check`.
- Existing CSS hooks to extend rather than invent: `.pathcopy`, `.provenance`, `.command` in `viewer/viewer.css`.

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
