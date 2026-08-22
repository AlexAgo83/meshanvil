## item_036_commit_the_two_hand_modelled_demo_assets_as_project_fixtures - Commit the two hand-modelled demo assets as project fixtures
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: (unfilled: replace before this doc is used)
- Keywords: commit, two, hand, modelled, demo, assets, project, fixtures
- Use when: (unfilled: replace before this doc is used)
- Skip when: (unfilled: replace before this doc is used)

# Problem
- logics/external/modeles-3D/ is gitignored, so the two hand-modelled demo assets exist only on this machine; a fresh clone or CI run falls back to the from-primitives generators and never sees them.

# Scope
- In:
  - Moving both .blend files to a committed path (fixtures/ or equivalent) with author/rights noted wherever the project already records that for committed assets.
  - Updating both build scripts' default-asset resolution order to check the committed path first.
- Out:
  - Any change to the assets' own geometry -- that is the render-quality and glass-pane items below.

# Acceptance criteria
- AC1: Both .blend files are tracked in git at a committed path.
- AC2: `tools/build_demo_chain.sh` and `tools/build_figurine_chain.sh`, run with no argument on a clean checkout, use the committed asset.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Both .blend files are tracked in git at a committed path.

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
