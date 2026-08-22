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
> Indicators reviewed: 2026-08-23 00:19:03

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
