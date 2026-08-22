## item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects - Generate a vehicle-scale subject that carries the same defects
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 19:01:53

# AI Context
- Summary: A primitive-built body shell (open, no wall thickness), mirrored wheels and a coincident duplicate, generated from code so build_demo_chain.sh has a subject to fall back to with nothing to license.
- Keywords: procedural vehicle, mirror modifier, open shell, coincident duplicate, no donor file
- Use when: changing what defect the vehicle-scale chain demonstrates, or how the subject is built.
- Skip when: the change is about the figurine subject or the chain of operations itself.

# Problem
- fixtures/demo_car.blend is gone, and with it the only subject that exercised unapplied Mirror modifiers, thin-walled panels needing solidify, and a coincident duplicate in one place.
- build_demo_chain.sh has no default to fall back to.

# Scope
- In:
  - A primitive-built body shell (open, no wall thickness), one Mirror-modifier pair (wheels), one coincident duplicate.
  - Wiring build_demo_chain.sh to generate this subject when no argument is given.
  - Verifying the walled-vs-unwalled branch still discriminates by actually running it.
- Out:
  - Matching the removed asset's exact geometry or measurements.
  - A textured or materialed model; the viewer shades from geometry alone.

# Acceptance criteria
- AC1: The generated subject's Mirror modifiers, once applied, change its vertex count.
- AC2: scan_defects finds the coincident duplicate unaided.
- AC3: solidify reports the open body as needing a wall; the closed parts as already closed.
- AC4: The same voxel size on the walled vs unwalled body gives one closed-shell ok and one caught, refused result.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: The generated subject's Mirror modifiers, once applied, change its vertex count.
- request-AC2 -> This backlog slice. Proof: AC2: scan_defects finds the coincident duplicate unaided.
- request-AC4 -> This backlog slice. Proof: AC3: solidify reports the open body as needing a wall; the closed parts as already closed.
- request-AC5 -> This backlog slice. Proof: AC4: The same voxel size on the walled vs unwalled body gives one closed-shell ok and one caught, refused result.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_008_demonstrations_that_own_every_asset_they_run_on`
- Architecture decision(s): (none yet)
- Request: `req_007_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`
- Primary task(s): `task_021_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
