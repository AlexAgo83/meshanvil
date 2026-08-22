## item_038_make_report_file_paths_and_commands_into_real_clickable_controls - Make report file paths and commands into real, clickable controls
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 60%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 23:15:12

# AI Context
- Summary: (unfilled: replace before this doc is used)
- Keywords: report, file, paths, commands, real, clickable, controls
- Use when: (unfilled: replace before this doc is used)
- Skip when: (unfilled: replace before this doc is used)

# Problem
- The render panel's 'Open in Blender' command, the Artefact section's written-file path, and other file references throughout the viewer are plain text a person has to select and retype or paste into a terminal by hand.
- The File-menu-stays-open-behind-the-splash defect (already fixed inline this session) has no regression coverage.

# Scope
- In:
  - A consistent pattern for file-path and command controls (button or link) applied everywhere the viewer currently prints one, respecting the file://-vs-served distinction already established.
  - A viewer-smoke assertion that opening the splash from the File menu leaves no menu open behind it.
- Out:
  - Extending the served command set (covered by the start-screen item above).

# Acceptance criteria
- AC1: The render panel's Blender-open command and the Artefact section's file path are both real controls, not plain text.
- AC2: Every other file path the viewer prints follows the same pattern.
- AC3: `scripts/viewer_smoke.py` (or equivalent) asserts no `details.menu` stays open after the splash opens from it.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: The render panel's Blender-open command and the Artefact section's file path are both real controls, not plain text.
- request-AC6 -> This backlog slice. Proof: AC2: Every other file path the viewer prints follows the same pattern.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_009_a_viewer_that_acts_on_what_it_shows_not_just_displays_it`
- Architecture decision(s): (none yet)
- Request: `req_008_make_the_viewer_s_start_screen_runbooks_and_file_references_actionable`
- Primary task(s): `task_022_deliver_the_viewer_actionability_pass`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
