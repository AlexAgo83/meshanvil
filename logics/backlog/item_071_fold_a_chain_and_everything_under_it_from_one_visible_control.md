## item_071_fold_a_chain_and_everything_under_it_from_one_visible_control - Fold a chain and everything under it, from one visible control
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Viewer usability and live state
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-25 00:04:57

# AI Context
- Summary: Fold was keyed on the group rather than the chain, and a chain's branches are separate groups: folding a chain leaves its branches on screen with nothing above them. Every group header is also a button, so a branch offers a control for something nobody thinks of as foldable, and the chevron reuses the per-row dim so a control reads as decoration.
- Keywords: outliner fold, chain versus branch, orphaned branch rows, fold affordance, aria-expanded, groupKey
- Use when: Changing how the outliner groups or hides rows, or adding any control to a group header.
- Skip when: The work is about the canvas rather than the outliner -- folding does not change what the node editor draws.

# Problem
- Fold was implemented per group, and a chain's branches are separate groups, so folding a chain leaves its branches visible with nothing above them.
- Every group header is a button, including branch headers, which offers a control for something an operator has no reason to fold on its own.
- The chevron uses the same dim as the per-row triangles, so a control reads as decoration.

# Scope
- In:
  - Folding keyed on the chain rather than the group, so a chain's branches fold with it.
  - Branch headers rendered as plain headings again, with no fold control and no button semantics.
  - A fold control that is legible against its own row, with aria-expanded agreeing with the glyph.
  - Checks: the fold rule in viewer/src where it can be proved without a DOM, and the rendered result in scripts/viewer_smoke.py.
- Out:
  - Persisting fold state across reloads.
  - Folding individual reports or any other level of the tree.
  - Reordering or restyling the outliner beyond the fold control itself.

# Acceptance criteria
- AC1: Folding a chain header hides that chain's rows and the rows of every branch that descends from it; the branch headers themselves are hidden with it.
- AC2: Unfolding restores exactly the rows that were hidden, and the row count returns to what it was.
- AC3: Only chain headers carry a fold control; a branch header is not a button and has no chevron.
- AC4: The control's colour and size distinguish it from the per-row triangles, and aria-expanded matches the glyph in both states.
- AC5: The browser smoke fails if folding a chain leaves any row of one of its branches visible.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Folding a chain header hides that chain's rows and the rows of every branch that descends from it; the branch headers themselves are hidden with it.
- request-AC2 -> This backlog slice. Proof: AC2: Unfolding restores exactly the rows that were hidden, and the row count returns to what it was.
- request-AC3 -> This backlog slice. Proof: AC3: Only chain headers carry a fold control; a branch header is not a button and has no chevron.
- request-AC9 -> This backlog slice. Proof: AC4: The control's colour and size distinguish it from the per-row triangles, and aria-expanded matches the glyph in both states.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)
- Request: `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`
- Primary task(s): `task_029_deliver_the_viewer_s_fold_refresh_payload_and_annotation_work`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
