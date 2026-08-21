## run_007_hollow_a_printable_body_for_electronics - Hollow a printable body for electronics
> Status: Active
> Category: other
> Verified: 2026-08-21 (open-bottom shell cut from a 1/10 body; three earlier approaches failed first)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- A printable body must house electronics, batteries or a mechanism, with an access opening.

# Prerequisites
- A watertight printable solid, from run_006.
- Ask what actually blocks the volume before choosing a technique. "The interior details are useless" usually means a structural floor eats the space, not that the wall is too thick.

# What does not work, and why
Three approaches were tried and abandoned. Recording them is the point of this runbook.
- **Solidify with a large inward thickness, to make the body solid before re-hollowing.** Solidify offsets a surface; at 25 mm on a thin detailed skin the offset self-intersects everywhere. The bounding box grew in *both* offset directions (+1 and -1), and recalculating normals changed nothing.
- **Remesh in Sharp mode, expecting it to keep only the outer hull.** It does not: enclosed volume went from 462.0 to 462.1 cm3, the internal cavity survived untouched. Neither Voxel nor Sharp remesh removes interior cavities.
- **Keeping only the ray-visible faces, then thickening them.** Sound in principle, unusable in practice at this mesh density: 4 M rays over 770 k faces left 421 k faces carrying 379 k boundary edges — confetti, not a surface. Growing the selection by rings to close the speckle brought back 83 % of the mesh, defeating the purpose. It would need an order of magnitude more rays, or an ambient-occlusion bake instead of raycasting.

# Procedure that works
1. **Measure where the material actually is**, along the opening axis, inside the footprint you intend to open. Sort the vertex heights in that column and print the distribution. Here the floor structure occupied 4-80 mm and the cabin resumed at 90 mm, with a clean gap between: that gap is where the cut plane belongs.
2. **Boolean DIFFERENCE with a box**, solver EXACT, spanning the opening footprint and rising to just under the gap. One operation removes the floor relief and creates the access opening at the same time.
3. Keep the footprint inboard of anything that must survive: appendages, rails, lower edges.

# Verification
- Free edges must stay 0: an EXACT boolean on a watertight solid keeps it watertight.
- Bounding box unchanged.
- **Count vertices inside the cut region before and after.** It must go to zero. Renders are ambiguous here: looking into an opening shows the inner surface of the far side, which has the same relief as the outer one, and reads as if nothing was removed. The first attempt cut nothing and the render looked identical to the successful one.

# Limits
- The interior surface is still the backside of the outer skin, not a smooth offset. Genuinely smoothing it needs the outer surface isolated cleanly, which none of the three approaches above achieved.
- Material volume removed is small (462.0 to 440.8 cm3) even when the opening is large, because the shell is thin. Judge the result by free space, not by material removed.

# Rollback
- Outputs are new files; the input solid is untouched.

# References
- Input: run_006_turn_a_cad_assembly_into_a_printable_solid
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)
