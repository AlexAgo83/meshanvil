## run_011_chain_002 - Chain 002
> Status: Archived
> Category: other
> Verified: Report facts captured; human procedure not yet verified
> Related request: req_000_make_every_3d_operation_reviewable_without_reopening_blender
> Related backlog: item_013_bridge_reports_into_the_logics_corpus
> Related task: task_005_bridge_reports_into_the_logics_corpus
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- Use this draft to turn chain `002` into a reviewed operating procedure.

# Prerequisites
- The source, Blender and the report chain must be available locally.

# Procedure
- Complete the human procedure from the captured report facts below; this scaffold does not claim one is verified.

# Verification
- Compare the next run against the measurements and failure recorded below.

# Rollback
- Keep the source unchanged and discard only generated work outputs when the procedure is revised.

# References
- Related request: req_000_make_every_3d_operation_reviewable_without_reopening_blender
- Related backlog: item_013_bridge_reports_into_the_logics_corpus
- Related task: task_005_bridge_reports_into_the_logics_corpus

## Report facts
- `002` `scan_defects` (ok): params `{"fix": true, "min_extent_mm": 50.0, "smear_ratio_threshold": 2.5}`; measurements `{"bbox_mm": {"max": [259.904, 137.772, 209.567], "min": [-268.0, -247.246, -1.977]}, "faces": 18112, "non_manifold_edges": null, "objects": 12, "shells": null, "vertices": 17956, "volume_cm3": null}`
- `003` `voxel_remesh` (failed): params `{"keep_largest": false, "max_bbox_drift_mm": 0.0, "render": false, "smallest_input_extent_mm": 64.0, "voxel_mm": 30.0}`; measurements `{"bbox_mm": {"max": [259.859, 133.558, 208.944], "min": [-265.11, -140.778, -0.89]}, "faces": 614, "non_manifold_edges": 0, "objects": 1, "shells": 1, "vertices": 616, "volume_cm3": 22235.14}`
- `003a` `ray_visibility` (ok): params `{"directions": 42, "grid": 40, "rays": 67200}`; measurements `{"bbox_mm": {"max": [259.904, 137.772, 209.567], "min": [-268.0, -247.246, -1.977]}, "faces": 11424, "non_manifold_edges": null, "objects": 8, "shells": null, "vertices": 11320, "volume_cm3": null}`
