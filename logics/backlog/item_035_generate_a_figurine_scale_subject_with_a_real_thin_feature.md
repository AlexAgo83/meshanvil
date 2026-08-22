## item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature - Generate a figurine-scale subject with a real thin feature
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: A primitive-built standing figure, sound by construction, with a finger thin enough to trigger the thin-feature guard at print scale and not at a finer voxel -- generated from code so build_figurine_chain.sh has a subject to fall back to with nothing to license.
- Keywords: procedural figure, thin-feature guard, closed by construction, no donor file
- Use when: changing what the figurine-scale chain measures, or how the subject is built.
- Skip when: the change is about the vehicle subject or the chain of operations itself.

# Problem
- fixtures/demo_figure.blend is gone, and with it the only subject that stayed sound under scan_defects while carrying a thin feature for the voxel-size lesson.
- build_figurine_chain.sh has no default to fall back to.

# Scope
- In:
  - A primitive-built standing figure, closed by construction (individually closed parts, joined without welding).
  - A finger thin enough to trigger the thin-feature guard at one voxel size and not another, once recentred to print scale.
  - Wiring build_figurine_chain.sh to generate this subject when no argument is given.
- Out:
  - An articulated or realistically sculpted figure.
  - Matching the removed asset's exact height or finger measurements.

# Acceptance criteria
- AC1: scan_defects reports no finding on the generated subject.
- AC2: Recentred to a print size, a finer voxel passes the thin-feature guard and a coarser one triggers it.
- AC3: README and the build script describe the generated subject's real, measured properties, not asserted ones.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: scan_defects reports no finding on the generated subject.
- request-AC4 -> This backlog slice. Proof: AC2: Recentred to a print size, a finer voxel passes the thin-feature guard and a coarser one triggers it.
- request-AC5 -> This backlog slice. Proof: AC3: README and the build script describe the generated subject's real, measured properties, not asserted ones.
- request-AC6 -> This backlog slice. Proof: AC3: README and the build script describe the generated subject's real, measured properties, not asserted ones.

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
