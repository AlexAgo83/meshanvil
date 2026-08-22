## item_019_restore_the_reviewed_first_run_splash_and_compare_split_layout - Restore the reviewed first-run splash and Compare split layout
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 02:21:09

# AI Context
- Summary: Restore the reviewed splash surface and Compare split treatment without changing the local read-only viewer boundary.
- Keywords: restore, reviewed, first, run, splash, compare, split, layout
- Use when: Implementing or testing Start splash, template cards, check/fix guidance, compare labels or wipe handle.
- Skip when: Work is only about graph layout, property sections or operation rendering.

# Problem
- The current Start flow is a simpler panel rather than the reviewed splash surface.
- The comparison image editor works but does not fully match the mockup split layout and metadata treatment.

# Scope
- In:
  - Start opens a splash-style surface with template command cards, recent-chain empty state, checks and fix commands.
  - Compare uses a split body with handle, labels, metadata and the existing native range interaction.
  - No-report and no-comparison states are explicit.
- Out:
  - Persisting first-run dismissal.
  - Pixel-perfect screenshots as committed golden files.

# Acceptance criteria
- AC1: The Start control opens and closes a splash surface with no blank columns or panels.
- AC2: The splash lists starter template commands, recent-chain absence and environment or doctor state with fix guidance.
- AC3: The Compare surface exposes before/after labels, a visible handle and a native control that remains draggable and keyboard-adjustable.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: The Start control opens and closes a splash surface with no blank columns or panels.
- request-AC4 -> This backlog slice. Proof: AC2: The splash lists starter template commands, recent-chain absence and environment or doctor state with fix guidance.
- request-AC6 -> This backlog slice. Proof: AC3: The Compare surface exposes before/after labels, a visible handle and a native control that remains draggable and keyboard-adjustable.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_003_strict_local_viewer_mockup_parity_closure`
- Architecture decision(s): (none yet)
- Request: `req_002_close_the_remaining_local_viewer_mockup_parity_gaps`
- Primary task(s): `task_016_deliver_remaining_viewer_mockup_parity_gaps`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
