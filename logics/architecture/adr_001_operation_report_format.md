## adr_001_operation_report_format - Operation report format
> Date: 2026-08-21
> Status: Accepted
> Related request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
> Related backlog: `item_001_define_the_operation_report_and_write_one_from_every_operation`
> Related task: `task_001_deliver_the_reviewable_operation_loop`
> Drivers: reviewability without reopening the 3D application, lineage across a branching history, safe pruning of heavy artefacts, agent-readable outcomes
> Reminder: Update status, linked refs, decision rationale, consequences, and follow-up work when you edit this doc.
> Indicators reviewed: 2026-08-21 22:51:20

# Overview
- One JSON envelope per operation, written by a single helper, carrying what was measured, what it was measured against, and what was not checked -- so a result can be reviewed, and a chain of results navigated, from the reports alone.


```mermaid
flowchart TD
  op[An operation runs] --> kind{kind}
  kind -->|transform| tr[before + after + output]
  kind -->|inspection| ins[findings, no output]
  tr --> core[Shared measurement block<br/>objects, vertices, faces, bbox_mm,<br/>shells, non_manifold_edges, volume_cm3<br/>unmeasured = null]
  ins --> core
  core --> helper[Report writer<br/>the only writer]
  helper --> delta[Per-axis bbox delta<br/>computed here, never skipped]
  helper --> warn[warnings as codes<br/>what was NOT checked]
  helper --> fp[input.sha256<br/>lineage and safe pruning]
  helper --> links[links.parent + wiki refs<br/>the history is a tree]
  helper --> state[output.state<br/>present / pinned / pruned]
  delta --> file[work/ops/NNN_name.json]
  warn --> file
  fp --> file
  links --> file
  state --> file
  file --> viewer[Viewer: top-down DAG]
  file --> prune[Pruning: deletes the artefact,<br/>never the record]
```

# Context
- Twelve scripts exist today. Seven transform a file and print measurements before and after; five only measure and produce no output file at all. A format that assumes an input and an output cannot describe the second kind, and inspections are where half the review actually happens.
- The measurements already printed converge on a small core: bounding box in millimetres, volume, shell count, non-manifold edge count, object and vertex counts. Five of the seven pipeline steps print four of those five. The format records what the scripts already compute; it does not ask them to compute something new.
- `pipeline/03_recenter.py` already prints the bounding box before and after, which is the comparison the runbooks name as the check that caught every failure in the delivered chain while the manifold checks passed throughout.
- Prior art in the same house: cm-sim's `transformation-report.json` carries `schema_version`, `created_at`, a source block with a SHA-256 fingerprint and a `read_only` mode, a settings block, before and after mesh blocks, a validation block, and warnings as short codes rather than sentences.
- The history of this work is a tree, not a line. `run_007` records three failed approaches before the one that worked, and those three carry most of the runbook's value. A representation that keeps only what succeeded destroys the more useful half.
- Artefacts are heavy and reports are not: a blend is 200 MB, an STL 68 MB, a report a few kilobytes. Whatever pruning policy arrives later will delete artefacts, never records.

# Decision
- **One envelope, two payloads.** Every report carries the same envelope: `schema_version`, `id`, `chain`, `created_at`, `kind` (`transform` or `inspection`), `operation`, `script`, `engine`, `params`, `tool`, `status` (`ok` or `failed`), `input`, `warnings`, `renders`, `links`. A `transform` adds `before`, `after` and `output`; an `inspection` adds `findings` and no output.
- **The core measurement block is shared.** `objects`, `vertices`, `faces`, `bbox_mm` (min and max per axis), `shells`, `non_manifold_edges`, `volume_cm3`. A field the operation did not measure is `null`, never absent and never zero.
- **The bounding-box comparison is computed by the helper, not by the operation.** A `transform` report states the per-axis delta between `before.bbox_mm` and `after.bbox_mm`, and names the axes that moved. No operation can omit the check that catches what the manifold checks miss.
- **Parameters are recorded, resolved.** `params` carries every parameter of the operation with the value actually used, defaults included, each with its unit. Without it two runs of the same operation are indistinguishable on the only thing that differs: a voxel at 6 mm and a voxel at 30 mm produced the whole failure demonstration, and the format could not tell them apart. Operations declare their parameters -- name, type, default, unit -- in a manifest the runner reads to parse the command line and the report reads to record the resolution.
- **The tool records itself.** `tool` carries the meshanvil version, the engine and its version and build hash, and the platform. A remesh does not produce the same mesh across two Blender versions; without this block, numbers from different versions are compared as if they were comparable. With it, the viewer can say so.
- **The engine is named.** `engine` is `blender` or `freecad`. The process model is the same either way -- a job in, a report out -- so a second engine is a different binary, not a different architecture.
- **Inputs are fingerprinted.** `input` carries the path and a SHA-256, as cm-sim does. The fingerprint is what makes lineage verifiable and pruning safe: a report describes a known set of bytes, whether or not those bytes still exist.
- **Unchecked is stated, not implied.** What an operation did not verify goes in `warnings` as a short code (`topology_not_checked`, `source_completeness_not_verified`, `thin_parts_below_ray_grid`), following cm-sim. A code is actionable by an agent; a sentence is not.
- **A failure still reports.** `status: failed` carries the error and the measurements taken before it, because a failed attempt is a branch of the history and not a discarded run.
- **The parent is derived, not declared.** `links.parent` is resolved by fingerprint: the report whose `output.sha256` equals this operation's `input.sha256`. The rule lives in `adr_005_execution_contract_identity_concurrency_and_exit_codes`; the format only records the result, and whether it was derived or overridden.
- **Lineage lives in the file.** `links` carries the parent report id and wiki-style references to the documents involved (`[[run_009_repair_export_defects_in_a_cad_derived_mesh]]`, `[[item_003_read_the_chain_of_operations_in_a_local_viewer]]`). A report opened alone in a text editor stays understandable without the tool that wrote it, and without any index or database.
- **Artefact state is a field from the start.** `output.state` is `present`, `pinned` or `pruned`, with the date when it changed. Retrofitting three fields onto reports already written is a migration worth avoiding for the price of declaring them now.
- **Renders are declared, not discovered.** `renders[]` carries, for each image, its canonical direction, its path and the camera used. `renders[0]` is the tile thumbnail. The viewer never infers a view from a filename.
- **Comparable pairs are declared too.** A `transform` that rendered its input state as well lists the pairs in `compare[]`, one per direction, each naming the two images and the camera they share. Without that declaration there is no comparison, because two images on two cameras prove nothing.
- **Reports are immutable except for artefact state.** Nothing else in a written report is edited afterwards.


# Canonical shapes
A transform, with a comparable pair, taken from the generated fixture:

```json
{
  "schema_version": 1,
  "id": "002",
  "chain": "001",
  "created_at": "2026-08-21T19:12:44Z",
  "kind": "transform",
  "operation": "graft_mirror_island",
  "script": "tools/graft_mirror_island.py",
  "engine": "blender",
  "status": "ok",
  "params": {"target": "trim_R", "mirror_axis": "Y", "weld_tolerance_mm": 0.001},
  "tool": {"meshanvil": "0.1.0", "engine_version": "5.2.0", "engine_build": "fbe6228777e7",
           "platform": "macOS-arm64", "python": "3.13.13"},
  "input":  {"path": "work/out/demo_source.blend", "sha256": "6b2e41c7d90a3f15…", "mode": "copy"},
  "output": {"path": "work/out/demo_fixed.blend", "sha256": "c07d3319ae558b02…",
             "state": "present", "state_changed_at": null},
  "before": {"objects": 1, "vertices": 2406, "faces": 2464, "shells": 4,
             "non_manifold_edges": 0, "volume_cm3": null,
             "bbox_mm": {"min": [-268.0, -247.2, 52.5], "max": [4.4, 127.5, 194.8]}},
  "after":  {"objects": 1, "vertices": 2406, "faces": 2464, "shells": 4,
             "non_manifold_edges": 0, "volume_cm3": null,
             "bbox_mm": {"min": [-268.0, 22.5, 52.5], "max": [-205.1, 127.5, 157.5]}},
  "bbox_delta_mm": {"min": [0.0, 269.7, 0.0], "max": [-209.5, 0.0, -37.3],
                    "axes_moved": ["X", "Y", "Z"]},
  "warnings": ["mirror_symmetry_assumed"],
  "renders": [
    {"view": "3q",    "path": "work/renders/002_trims_3q.png",    "camera": "ortho-3q-fixed", "tile": true},
    {"view": "front", "path": "work/renders/002_trims_front.png", "camera": "ortho-front-fixed", "tile": false}
  ],
  "compare": [
    {"view": "front", "before": "work/renders/001_trims_front.png",
     "after": "work/renders/002_trims_front.png", "camera": "ortho-front-fixed"}
  ],
  "links": {"parent": "001", "parent_source": "fingerprint",
            "docs": ["run_009_repair_export_defects_in_a_cad_derived_mesh"]}
}
```

An inspection: same envelope, `findings` instead of `before`/`after`, and no `output`.

```json
{
  "schema_version": 1, "id": "001", "chain": "001",
  "created_at": "2026-08-21T19:08:02Z", "kind": "inspection",
  "operation": "scan_defects", "script": "tools/scan_defects.py", "engine": "blender",
  "status": "ok",
  "params": {"smear_ratio_threshold": 2.5, "fix": false},
  "tool": {"meshanvil": "0.1.0", "engine_version": "5.2.0", "engine_build": "fbe6228777e7",
           "platform": "macOS-arm64", "python": "3.13.13"},
  "input": {"path": "work/out/demo_source.blend", "sha256": "6b2e41c7d90a3f15…", "mode": "read_only"},
  "measured": {"objects": 12, "vertices": 17956, "faces": null, "shells": null,
               "non_manifold_edges": null, "volume_cm3": null,
               "bbox_mm": {"min": [-268.0, -247.2, -2.0], "max": [259.9, 137.8, 209.6]}},
  "findings": [
    {"code": "smeared_island", "subject": "trim_R", "ratio": 2.9,
     "full_extent_mm": 375.0, "robust_extent_mm": 127.0},
    {"code": "coincident_duplicates", "groups": 4, "objects": 4,
     "vertices": 6636, "share_of_vertices": 0.370}
  ],
  "warnings": ["thin_parts_below_ray_grid"],
  "renders": [],
  "links": {"parent": null, "parent_source": null,
            "docs": ["run_009_repair_export_defects_in_a_cad_derived_mesh"]}
}
```

An operation manifest, read by the runner to parse the command line and by the report to record
what was resolved:

```json
{
  "operation": "scan_defects", "engine": "blender", "kind": "inspection",
  "script": "tools/scan_defects.py",
  "summary": "Sweep a scene for smeared patches and coincident duplicates.",
  "params": [
    {"name": "smear_ratio_threshold", "type": "float", "default": 2.5, "unit": "ratio"},
    {"name": "fix", "type": "bool", "default": false}
  ]
}
```

# Consequences
- The viewer renders the chain as a deterministic top-down DAG from `links.parent`, time running vertically and branches horizontally, rather than a force-directed graph. On ten nodes a physics simulation says less than a tree; it also discards the ordering, which is the most useful axis here. A graph view stays an open question in `prod_001`, to be answered when the node count makes a tree fail.
- Adding an operation means calling the helper, not defining a format. An operation that reports in a shape of its own is a defect.
- The five inspection scripts become first-class: their findings are recorded and navigable instead of scrolling out of a terminal.
- A pruning policy can be written later without touching the format, because `input.sha256` and `output.state` are already there. That policy is its own slice.
- The helper needs the scene both before and after, so operations that save and reopen files must hand it the measurements rather than the paths.
- An operation that wants to be compared must render its input state on the output's camera, which costs one extra render pass and is why `item_005` carries a fixed-camera render mode rather than the per-object framing used today.
- Recording `params` and `tool` costs a few hundred bytes per report and is what makes two reports comparable at all. Any comparison across different `tool.engine_version` values is flagged rather than silently drawn.
- The format is versioned from the first write. `schema_version` is bumped on any change to the shape, and the viewer refuses a version it does not know rather than rendering it wrong.

# References
- Prior art: `transformation-report.json` in the cm-sim printable-preparation flow (schema_version, source fingerprint, warning codes)
- The check the format makes mandatory: `run_006_turn_a_cad_assembly_into_a_printable_solid`, "compare the output bounding box against the source"
- The branching history this format must keep: `run_007_hollow_a_printable_body_for_electronics`, three failed approaches
- Related request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Related backlog: `item_001_define_the_operation_report_and_write_one_from_every_operation`
- Related task: `task_001_deliver_the_reviewable_operation_loop`
