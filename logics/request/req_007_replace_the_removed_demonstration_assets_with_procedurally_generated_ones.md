## req_007_replace_the_removed_demonstration_assets_with_procedurally_generated_ones - Replace the removed demonstration assets with procedurally generated ones
> From version: 0.1.0
> Schema version: 1.0
> Status: Draft
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# AI Context
- Summary: The two demonstration assets were removed with every trace of them, over an unverified licence; this request rebuilds both from primitives instead, so no future demonstration subject ever needs a licence check again.
- Keywords: procedural generation, demonstration assets, no donor file, thin-feature guard, coincident duplicate
- Use when: changing what either demonstration subject is built from, or adding a defect either chain relies on.
- Skip when: the change is about the chain of operations itself, not the subject it runs on.

# Needs
- The two demonstration assets (a downloaded vehicle model, a downloaded character sculpt) were removed along with every trace of them, because their licence was never verified. Both `build_demo_chain.sh` and `build_figurine_chain.sh` were left with no bundled example to default to.
- The demonstrations exist to carry specific, verifiable lessons -- a coincident duplicate, unapplied Mirror modifiers, a destructive remesh that a real check catches, a thin feature a voxel size can erase -- and a replacement subject has to carry the same class of properties, not just resemble the old one visually.
- `tools/make_demo_scene.py` already proves the pattern for the ground-truth fixtures: build a subject from primitives, in a script, so nothing is downloaded and nothing needs a licence. The two demonstrations had never used that pattern for themselves.

# Context
- A procedural subject is measured the same way any other input is measured in this project: run it through the real chain and read the real reports, not asserted from the generator's own intentions.
- A flat cylinder cap meeting a sphere anywhere but its own equator leaves an arbitrarily thin sliver at the crossing -- found the hard way while tuning the figurine's thin-feature guard, and worth a runbook entry once repeated.
- Full concealment of an interior part behind an open-bottomed shell is not guaranteed by construction; the vehicle generator reports what it can honestly claim (mostly hidden) rather than a stronger claim it cannot verify.

# Acceptance criteria
- AC1: `tools/make_demo_vehicle.py` generates a render-scale subject from primitives with, verified by running it through the real chain: an unapplied Mirror modifier that changes vertex count when baked, at least one panel with no wall thickness that solidify has real work to do on, and one coincident duplicate that scan_defects finds unaided.
- AC2: The same walled-vs-unwalled voxel_remesh branch used before still discriminates on the generated subject: the walled body reports ok as one closed shell, and the unwalled remesh is caught and refused rather than passing silently.
- AC3: `tools/make_demo_figure.py` generates a figurine-scale subject from primitives that scan_defects reports no finding on, and that carries a genuinely thin feature (a finger) thin enough that a coarser voxel size triggers the thin-feature guard while a finer one does not, once recentred to a print size.
- AC4: Neither generator downloads or bundles a third-party file; both regenerate from code alone, and running either produces the numbers documented rather than asserted.
- AC5: `build_demo_chain.sh` and `build_figurine_chain.sh` fall back to their matching generator when no asset argument is given, and still accept any `.blend` in its place.
- AC6: README's Demonstration data section and both build scripts describe what the generated subjects actually do, including the vehicle's interior part being mostly, not guaranteed, hidden -- no claim the generators cannot back with a measured run.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_008_demonstrations_that_own_every_asset_they_run_on`
- Architecture decision(s): (none yet)

# References
- tools/make_demo_vehicle.py
- tools/make_demo_figure.py
- tools/build_demo_chain.sh
- tools/build_figurine_chain.sh
- tools/make_demo_scene.py
- README.md

# Backlog
- `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`
- `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`
