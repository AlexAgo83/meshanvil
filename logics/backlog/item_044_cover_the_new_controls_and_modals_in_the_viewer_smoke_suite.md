## item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite - Cover the new controls and modals in the viewer smoke suite
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Low
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:48:56

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

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- `scripts/viewer_smoke.py` injects JavaScript into a headless Chrome and reads the result out of the DOM; there is no framework and adding one is not in scope. Assertions are plain `assert(condition, message)` inside the injected payloads.
- Two passes to extend, and they are different: `SERVED_SMOKE` (`scripts/viewer_smoke.py:12`) runs against a real `meshanvil view --serve` subprocess started in `check_served()` (`scripts/viewer_smoke.py:286`) -- that is where Open, Reveal and the modals belong. The offline pass in `main()` (`scripts/viewer_smoke.py:334`) uses `--dump-dom` on the built page and is where the opened-from-disk degradation belongs.
- `chrome_path()` (`scripts/viewer_smoke.py:269`) locates the binary; with no Chrome the suite skips rather than fails, so a new assertion must not be the only thing proving a criterion.
- The regression precedent to mirror is at `scripts/viewer_smoke.py:94` -- the menu-stays-open-behind-the-splash check added by `task_022`, written as one assertion naming the defect.

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

# Tasks
- `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals`

# Notes
- Task `task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals` was finished via `logics-manager flow finish task` on 2026-08-23.
