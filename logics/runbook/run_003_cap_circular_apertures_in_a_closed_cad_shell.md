## run_003_cap_circular_apertures_in_a_closed_cad_shell - Cap circular apertures in a closed CAD shell
> Status: Active
> Category: other
> Verified: 2026-08-21 (8 apertures capped on an imported assembly: 4 barrels at 93.0 mm at one end, 4 at 50.0 and 56.7 mm at the other)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- The operator points at round openings in an imported assembly (recessed barrels, sockets, ports) and wants them closed off so the model reads as complete.
- The visible opening is a recess or a tube mouth, not necessarily a topological hole.

# Prerequisites
- Access to the scene, via run_001.
- Never assume the opening is a hole. Run the discrimination step first; it decides which of two very different operations applies.

# Procedure
1. **Discriminate: hole or recess.** On a `bmesh` copy, `bmesh.ops.remove_doubles(dist=0.0005)` (STEP imports arrive with split vertices, which fragments every boundary and makes naive loop-walking useless), then collect edges with `len(e.link_faces) == 1`.
   - Boundary loops of the expected diameter exist -> genuine holes, go to step 2a.
   - Only sub-centimetre boundary loops exist -> the shell is closed and what looks like an opening is a modelled inner wall. Go to step 2b. This was the real case in practice: 28 holes across the whole zone, all under 1 cm2.
2a. **Genuine hole:** `bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)`, or in the UI Edit Mode > Mesh > Clean Up > Fill Holes.
2b. **Recess:** the circle the operator sees is the *sharp edge loop* where the outer wall turns into the tube. Collect edges with `len(e.link_faces) == 2` and `e.calc_face_angle(0) > 0.6`, keep only vertices carrying exactly two such edges, and walk closed cycles through that subgraph. Restricting to degree 2 is what separates concentric loops; plain connected-component grouping merges them and reports garbage (54-180% radius deviation instead of 0.0%).
3. **Qualify each loop.** Compute centre, mean radius and max relative radius deviation. A machined aperture comes out at well under 1% deviation; anything above ~10% is a merged or partial loop, not a circle. Report diameters and centres to the operator and check the count against what they described before creating anything.
4. **Group concentric rims.** A tube mouth yields two loops a few millimetres apart along the axis (the lip thickness). Group by rounded (centre, radius) and keep the outermost rim so the cap sits flush.
5. **Build the cap from the loop's own vertices.** Create a new mesh whose vertices are the loop's world-space points in walk order, with a single n-gon face. Radius, position, plane and tilt are inherited from the part, so nothing is eyeballed. Carry over the source materials, link into the source's collection, and name it distinctly (`CAP_*`).
6. Never edit the supplier part itself. One new object per aperture keeps every cap individually selectable and deletable.

# Verification
- Radius deviation printed per loop must be near zero before any geometry is created.
- The created face's vertex count must equal the detected loop's vertex count.
- Render both sides and both ends of the object. Verify the axis convention by rendering rather than assuming: in the scene handled here `view_axis('LEFT')` framed the front and `('RIGHT')` the rear.
- Count the caps against the operator's own count, and name any extra ones found so they can be rejected explicitly.

# Rollback
- Delete the `CAP_*` objects; source parts were never modified.

# Why not a primitive
An earlier attempt placed UV spheres and cylinders sized from the bezel bounding box and nudged them into position by eye. It cost five render round trips, still protruded through the outer skin, and left a 282 mm rod crossing eight other parts' bounding boxes. Detected geometry beats eyeballed geometry every time: if a circle exists in the mesh, build on its vertices instead of approximating it.

# References
- Execution channel: run_001_drive_a_live_blender_session_from_the_agent
- Related audit method: run_002_audit_symmetry_of_an_imported_cad_assembly
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)
