## run_012_build_a_recognizable_low_poly_subject_from_primitives - Build a recognizable low-poly subject from primitives
> Status: Active
> Category: other
> Verified: 2026-08-22 (both demo generators built and re-verified against the real chain across several iterations; two geometry defects found and fixed this way)
> Related request: `req_007_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`
> Related backlog: `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`, `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`
> Related task: `task_021_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- A demonstration or fixture needs a recognizable subject (a vehicle, a figure) built from `bpy`/`bmesh` primitives rather than a downloaded or donated file -- no licence to verify, nothing to remove later.
- The generated subject looks wrong -- an unrecognizable blob, a hollow-looking limb, a flap poking past the silhouette -- and the fix has to be geometric, not a texture or shading trick a low-poly flat-shaded render has no room for.
- A ray-based measurement (thin-feature, visibility) on a generated subject reports a number that does not match what the generator's own comments claim it built.

# Prerequisites
- Render after every real change, not just after the script exits clean. A script that runs without error and reports a plausible vertex count still needs its own render checked by eye (`work/renders/*_3q.png` or equivalent) -- a wrong-looking result can run to completion silently.
- Know which reports are honest measurements and which are the generator's own intent. `tools/scan_defects.py`, `tools/voxel_remesh.py` etc. measure the file as it exists; a docstring only states what the author meant to build.

# Procedure
1. **Build a recognizable silhouette by sweeping cross-section rings along the main axis, not by deforming a single box.** A cube stretched and pinched (proportional-edit box modeling, the tutorial-standard approach) fights the tool at every step for an asymmetric profile like a car body. Defining N stations as explicit ring cross-sections (`[(x, -w, z0), ..., (x, w, z0)]`, one per station) and bridging consecutive rings into quads with `bmesh.ops` gives direct control over where the shape narrows, rises, and tapers, and is a handful of arithmetic lines rather than a modeling session. `tools/make_demo_vehicle.py`'s `ring()`/`stations` is this pattern; three earlier attempts (disconnected panels, a single dorsal profile with no side walls) were unrecognizable before this one held.
2. **Keep every panel narrower than the hull it is meant to sit inside of, checked at its own extremes, not just at its centre.** A flat accessory panel (skid plate, belly, roof rack) sized to a fixed fraction of the hull's *widest* station will be wider than the hull at any station it spans that tapers below that width -- it pokes out as a visible sliver past the silhouette there, worst at the narrow ends. Compute or eyeball the hull's width at the panel's own X-extremes before picking the panel's Y half-width, not just at the hull's widest point.
3. **A flat disk cap meets a sphere safely only at the sphere's own equator; anywhere else it leaves an arbitrarily thin sliver.** Two primitives joined without welding (the technique that keeps everything manifold by construction, see below) still touch as two separate surfaces at their contact; a torso cylinder's flat top embedded partway up a head sphere crosses that sphere off-equator, and the crossing is a sliver whose thickness depends on exactly where the disk sits -- not visible by eye at rest scale, but the exact kind of feature a ray-based thin-feature scanner is built to catch. The junction that is dead-on the sphere's own equator (a hip joining a torso's bottom, on this figure) has no such sliver and is safe to leave capped.
4. **Cap what is safe, leave open only the specific junction that is not -- do not blanket-uncap every part sharing a helper function.** The first fix for the sliver above removed end caps from every limb using the same helper, which also removed a visual cue (a capped end reads as a solid limb; an uncapped one renders as a dark hollow tube, obviously wrong at any zoom). Add an argument (`open_end="top"`) so the helper caps by default and only opens the one junction actually proven risky by step 3, rather than making every caller pay for one part's problem.
5. **Before trusting a ray-based thin-feature report, check whether it is measuring the feature or the gap next to it.** A ray-cast thickness scanner finds the nearest opposing surface along a cast direction; four fingers spaced closer than they are thick get measured as the *gap* between two fingers, which is a different (and differently thin) feature than the finger itself. Space repeated thin features apart by several times their own thickness (this figure uses `FINGER_R * 5.0`) so the scanner's nearest hit is guaranteed to be the feature's own opposite wall, not a neighbour's.
6. **Verify a claim the generator's comment makes against the real chain's own numbers, and soften the comment if the chain cannot back it.** "Mostly hidden" survived a session of widening a belly panel trying to reach "never visible" for an interior part; `ray_visibility`'s own grid never confirmed full concealment. The comment, the README, and the build script were all corrected to the claim the measured run actually supports, rather than left asserting a stronger one.

# Verification
- Re-run the full build chain (`build_demo_chain.sh` / `build_figurine_chain.sh` with no argument) after any generator change and diff the reported numbers against the previous run: vertex counts, `thin_feature_mm`, `thin_feature_voxels`, bbox drift, and which ops report `ok` vs `failed`. A script that still runs to completion is not proof the branch behaviour it exists to demonstrate is unchanged.
- Take a fresh 3q render after any geometry change and look at it. A vertex-count and bbox check that matches the previous run does not confirm a visual regression (open pipe ends, a sliver past the hull) is gone -- only the render does.
- Crop and zoom a suspected render artifact before concluding it is geometry. An anti-aliased ridge highlight where two faces meet at a shallow angle can read as a distinct pale sliver at thumbnail size and vanish under a zoomed crop of the same pixels.
- `grep` for a helper function's name after narrowing its use (`uncapped()` -> `half_capped()` for one junction only) to confirm nothing still calls the old blanket version.

# Rollback
- Nothing here writes outside `work/out/` and `work/demo/*` -- a bad generator change is fixed by editing the script and re-running it, not by reverting a destructive operation on a real file.

# Limits to state, not to hide
- These are the shapes this project's two subjects needed (a swept-ring car body, a sphere-and-cylinder figure); a different silhouette may need a different primitive-composition pattern entirely.
- Step 5's spacing rule assumes the scanner casts along a fixed direction set (this project's ray grid); a scanner casting only along the feature's own long axis would not have this failure mode.
- "Recognizable" was judged by eye against a real render, not against a quantitative silhouette metric -- there is no automated check here for "looks like a car."

# References
- The generators themselves: `tools/make_demo_vehicle.py`, `tools/make_demo_figure.py`
- The thin-feature measurement being reasoned about here: `meshanvil_engine/report.py`'s `thin_feature_mm()`
- The same "verify against the real chain, not the generator's own intent" discipline generalized: `run_010_verify_that_a_command_did_what_it_appeared_to_do`
- Related request: `req_007_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`
- Related task: `task_021_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`
