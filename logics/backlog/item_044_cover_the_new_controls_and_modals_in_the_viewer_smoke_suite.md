## item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite - Cover the new controls and modals in the viewer smoke suite
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:19:03

# AI Context
- Summary: Smoke coverage over the new file controls and modals: the control group and its accessible names, the opened-from-disk degradation, and translated modal content.
- Keywords: viewer smoke, regression coverage, accessible names, degradation check
- Use when: Adding or changing coverage for the viewer's presentation behaviour.
- Skip when: Adding a new test framework -- the existing smoke suite is the target.

# Problem
- The three-control group, the opened-from-disk degradation and the two modals are all presentation behaviour that no existing check would notice regressing.

# Scope
- In:
  - Assertions in `scripts/viewer_smoke.py` for the control group's presence and accessible names, the opened-from-disk degradation, and both modals rendering translated content.
- Out:
  - A new test framework or runner; the existing smoke suite is where this lives.

# Acceptance criteria
- AC1: The smoke suite fails if a file reference loses any of its three controls or its accessible names.
- AC2: The smoke suite fails if a page opened from disk presents Open or Reveal as working controls.
- AC3: The smoke suite fails if either modal shows raw output instead of translated content.

# AC Traceability
- request-AC10 -> This backlog slice. Proof: AC1: The smoke suite fails if a file reference loses any of its three controls or its accessible names.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_010_direct_controls_over_the_files_and_results_the_viewer_already_names`
- Architecture decision(s): (none yet)
- Request: `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`
- Primary task(s): `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
