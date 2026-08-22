## req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls - Turn the viewer's file references and command rows into direct, translated controls
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:48:55

# AI Context
- Summary: A file the viewer names becomes something to open or locate rather than a string to copy, and a command's result becomes a translated panel instead of raw stdout -- both without a new dependency or an open execution surface.
- Keywords: file controls, open and reveal, icon-only affordance, translated result modal, closed action set, Help menu
- Use when: Deciding how the viewer presents a file reference or the result of a command it can run.
- Skip when: Deciding what an operation measures or reports -- adr_001 and req_000 hold that, not this request.

# Needs
- Wherever the viewer shows a file it calls it `path` and prints the path itself -- a single copy-to-clipboard button carrying the whole string (report Input, report Output/Artefact, render provenance). The operator's actual intent is almost never 'I want this string': it is 'open this file', 'show me where it sits', and only sometimes 'give me the text'. One control serves the rarest of the three.
- The render panel offers `blender <path>` as a command to copy and paste into a terminal. Opening a .blend file is what the host system's file association already does; asking the operator to open a terminal to do it is a longer route to the same place.
- `List operations` and `Check setup` run for real on a served page (adr_007) but their result is dumped as raw process stdout into a `<pre>` inside the still-open menu dropdown: untranslated, unstyled, and shown in a container sized for a menu row. `Check setup` in particular prints a JSON object at the operator.
- Both rows sit in menus that do not describe them: `List operations` under File and `Check setup` under File, while both are reference material about the tool and its environment rather than actions on the current project.

# Context
- adr_007 closed the set of commands a served page may run to three fixed argument lists and stated the rule that makes it safe: `no operator-supplied value ever reaches the subprocess`. Opening or revealing a file is by nature parameterised by a file, so it cannot join that set as-is. The shape that preserves the rule is an allow-list the *server* owns: the build already knows every file the page can name (report inputs, outputs, renders), so the page can send an identifier into that set and never a path -- surfaced here as the decision to record, not pre-decided.
- A page opened from disk has no server to reach. Under adr_007 that is not a degraded case to work around but the baseline: the Open and Reveal controls have nothing to call there and must be absent or visibly unavailable, with Copy path still working exactly as it does today.
- `meshanvil doctor` already emits a machine-readable object and the viewer already reads a cached copy of it from `work/doctor.json` for the start screen; `meshanvil list` prints formatted text only. A modal that translates a result should read structured data, not scrape a subprocess's stdout -- which likely means `list` gains a machine-readable form rather than the page learning to parse its columns.
- Icon-only controls are an accessibility surface, not just a smaller button: each needs an accessible name from the catalogue (adr on i18n applies -- no inline English), and the icon set has to stay dependency-free like the rest of the viewer, so inline SVG or text glyphs, not an icon font.

- This request should land after `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`, which splits `viewer/viewer.js` into modules and introduces a built client bundle. Implementing this one first would rewrite the same code twice.

# Acceptance criteria
- AC1: Every place the viewer labels a file reference calls it `file`, not `path`, in both catalogues, and no label reads `path` where a file is meant.
- AC2: Every file reference the viewer shows (report Input, report Output/Artefact, render provenance, and any other) offers the same three controls -- Open, Copy path, Reveal -- rendered as icons with no visible text label, each carrying an accessible name resolved from the string catalogue.
- AC3: On a served page, Open launches the file through the host system's default handler and Reveal opens the containing folder with the file selected where the platform supports it; both are verified on the platform under test and the platforms not verified are stated as unverified.
- AC4: On a page opened from disk, Copy path behaves exactly as it does today and Open and Reveal are not offered as controls that appear to work -- absent or explicitly shown as unavailable, never silently inert.
- AC5: A decision is recorded (an amendment to adr_007 or a new ADR) covering how a file reaches the server without an operator-supplied path becoming a subprocess argument, and the implementation matches it.
- AC6: No `blender <path>` command is offered for copying anywhere in the viewer; opening a report's artefact goes through the Open control of AC2.
- AC7: `List operations` and `Check setup`, run from a served page, present their result in a modal built from structured data, with every operator-facing string resolved from the catalogue and available in both languages -- no raw process stdout and no JSON shown to the operator.
- AC8: Opening either modal closes the menu it was launched from, and the modal is dismissible by the same means as the start screen modal.
- AC9: `List operations` and `Check setup` are both reached from the Help menu and appear in no other menu.
- AC11: The Help menu's `Create a runbook <report-id>` row -- left copy-only by `adr_007` because its id is a placeholder with no report behind it -- either carries a real report id or states in the row why it does not; no row shows a placeholder that reads as a value.
- AC10: `scripts/viewer_smoke.py` covers the new controls and modals so the behaviour cannot silently regress: the three-control group's presence and accessible names, the opened-from-disk degradation, and both modals rendering translated content rather than raw output.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_010_direct_controls_over_the_files_and_results_the_viewer_already_names`
- Architecture decision(s): (none yet)

# References
- viewer/index.html
- viewer/viewer.js
- viewer/viewer.css
- meshanvil/viewer.py
- meshanvil/cli.py
- meshanvil/doctor.py
- meshanvil/manifests.py
- locales/en.json
- locales/fr.json
- scripts/viewer_smoke.py
- adr_003
- adr_007

# Backlog
- `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`
- `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows`
- `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`
- `item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite`
