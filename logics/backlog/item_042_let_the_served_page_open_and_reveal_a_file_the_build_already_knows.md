## item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows - Let the served page open and reveal a file the build already knows
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:02:25

# AI Context
- Summary: The server side of open and reveal: a reference the build already owns resolves to a real file, so no page-supplied path ever becomes a subprocess argument, with the rule recorded as an ADR.
- Keywords: closed action set, build-owned reference, host default handler, reveal folder, adr_007 amendment
- Use when: Deciding how the served page is allowed to act on a local file.
- Skip when: Deciding what the controls look like -- item_041 holds that.

# Problem
- Opening a file and revealing its folder are host-system actions the page cannot perform itself, and adr_007's closed command set takes no operator-supplied value, so neither fits the existing `/run` endpoint.

# Scope
- In:
  - A recorded decision (adr_007 amendment or a new ADR) on how a file is named to the server without a page-supplied path reaching a subprocess.
  - The server side: resolving a reference the build owns to a real file, opening it through the host default handler, and revealing its containing folder, per platform.
  - Refusal behaviour for a reference the build does not own, and for a file that no longer exists.
- Out:
  - Opening anything the current build did not already name.
  - Any change to the three existing `/run` commands.

# Acceptance criteria
- AC1: An ADR records the rule and the implementation matches it.
- AC2: Open launches a report's artefact through the host default handler on the platform under test.
- AC3: Reveal opens the containing folder, with the file selected where the platform supports it.
- AC4: A reference the build does not own is refused, and a missing file is refused with a distinguishable result rather than silently doing nothing.
- AC5: Platforms not verified are recorded as unverified.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: An ADR records the rule and the implementation matches it.
- request-AC5 -> This backlog slice. Proof: AC2: Open launches a report's artefact through the host default handler on the platform under test.

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- The endpoint to extend, not duplicate: `make_server()` (`meshanvil/viewer.py:126`) and its `RunHandler.do_POST`. It already implements the four refusals a new route must match -- 404 wrong path, 401 bad or missing `X-Meshanvil-Token`, 400 malformed body or unknown command, 409 a run already in flight (non-blocking `threading.Lock`).
- The allow-list the decision needs already exists as a by-product of the build: `collect()` (`meshanvil/viewer.py:23`) and `with_render_urls()` (`meshanvil/viewer.py:42`) walk exactly the file-bearing fields -- `input.path`, `output.path`, `renders[].path`, `comparisons[].before/after`. The same set the page can name is the set the server can resolve, so the page sends an index into it and never a string.
- Those field names come from `meshanvil_engine/report.py`: input at `:174`, output at `:212`, renders at `:203`, comparisons at `:206`.
- The host-opener platform split is already written once, in `open_in_browser()` (`meshanvil/viewer.py:107`): WSL converts with `wslpath -w` then calls `explorer.exe`, everything else goes through `webbrowser`. Reveal has no equivalent yet -- `open -R` on macOS, `explorer /select,` on Windows, and on Linux only the parent directory opens, with no way to select the file. That asymmetry is what AC5's `unverified` statement is for.
- `in_wsl()` is imported from `meshanvil/engines.py`.

# Decision framing
- Product framing: Not needed
- Architecture framing: Needed: how a file reaches the server without a page-supplied path becoming a subprocess argument -- an amendment to `adr_004_target_technology_and_process_model`'s successor `adr_007_let_the_served_viewer_execute_a_closed_command_set`, or a new decision beside it.

# Links
- Product brief(s): `prod_010_direct_controls_over_the_files_and_results_the_viewer_already_names`
- Architecture decision(s): (none yet)
- Request: `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`
- Primary task(s): `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals`

# Notes
- The open and reveal actions launch host processes, so they land on the same surface `item_053_run_the_viewer_s_closed_command_set_through_the_installed_entry_point` repoints at the installed entry point. Whichever ships second inherits the other's shape.

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
