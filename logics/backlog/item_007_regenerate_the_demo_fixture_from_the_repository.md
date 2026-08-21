## item_007_regenerate_the_demo_fixture_from_the_repository - Regenerate the demo fixture from the repository
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: A synthetic scene built by script, carrying real export defects, that the existing sweep finds unaided -- the public fixture and the ground truth the tools lacked.
- Keywords: demo fixture, synthetic scene, ground truth, generated defects, no binary committed
- Use when: Demonstrating or testing the tools without private geometry.
- Skip when: Working on a real assembly: the runbooks cover that, and its data never enters the repository.

# Problem
- The tools were demonstrated on client geometry, which cannot be published and should not be the fixture of a public repository.
- A third-party model would still be a licence to track, a binary to host and a provenance to justify.
- tools/scan_defects.py had no ground truth: nothing in the repository contained a known defect it could be checked against.

# Scope
- In:
  - tools/make_demo_scene.py: a symmetric housing, two trims and four feet, plus two defects built in -- one island smeared along a line, and objects duplicated at identical coordinates.
  - Defects calibrated on the ones observed in practice, so the sweep finds them at a comparable ratio without being told where they are.
  - tools/run_demo_chain.py: the chain replayed on that scene -- dedupe, voxel envelope, a coarse-voxel attempt kept as a failure, an opening cut in the floor.
  - tools/render_fixed_views.py: the canonical directions on a camera fixed for a subject, which is what makes two states comparable.
  - Everything written under work/, nothing binary committed.
- Out:
  - Shipping the generated blends or renders in the repository.
  - Making the demo scene resemble any particular product.
  - A test framework. The fixture is the ground truth; how it is asserted on is its own decision.

# Acceptance criteria
- AC1: A single command regenerates the scene, and the same command twice produces the same geometry.
- AC2: tools/scan_defects.py reports the built-in smear and the built-in duplicates without being pointed at them.
- AC3: The chain replays end to end on the generated scene and prints the measurements each step took.
- AC4: A coarse-voxel attempt is kept as a failure with its numbers, since it is the trap run_006 records.
- AC5: Nothing generated is committed, and the publication-hygiene gate still passes.

# AC Traceability
- request-AC13 -> This backlog slice. Proof: AC2: tools/scan_defects.py reports the built-in smear and the built-in duplicates without being pointed at them.
- request-AC11 -> This backlog slice, partially. Proof: AC3: the chain produces the two states that item_005 compares.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: Not needed
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.
