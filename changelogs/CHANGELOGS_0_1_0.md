# meshanvil 0.1.0
Release date: 2026-08-21

First public cut. The method exists and has been exercised end to end on one delivery;
the packaging around it is new.

## Added

### Method
- Nine runbooks in `logics/runbook/`, each with its trigger, procedure, the measurements
  that verify it, and the limits it does not cover: driving a live Blender session from an
  agent, auditing symmetry, capping circular apertures, transferring parts between two
  exports, selecting the outer envelope by ray visibility, turning a CAD assembly into a
  printable solid, hollowing it, welding disconnected shells, and repairing export defects.
- `run_009_repair_export_defects_in_a_cad_derived_mesh`: locate a defect by bounding box,
  isolate it to a connected island, graft the mirrored twin island rather than rebuilding
  a whole side, then sweep the file for the same class of defect.

### Code
- `pipeline/`, the seven steps of the delivered chain, in execution order.
- `tools/`, reusable inspection scripts: shell enumeration, symmetry check, ray probes,
  box counting, verification renders.
- `tools/scan_defects.py`: sweeps a scene for smeared patches (full bounding box against
  the 5th-95th percentile bounding box) and for coincident duplicate objects (confirmed by
  a hash of world-space coordinates). `-- --fix` removes the duplicates.

### Product direction
- `req_000` opens the reviewable operation loop: one report per operation, one
  agent-agnostic command, one local viewer for the chain -- with `prod_001` as its brief
  and four slices under `task_001`.
- `adr_001_operation_report_format` settles the report shape from a study of what the
  twelve existing scripts already measure and from cm-sim's `transformation-report.json`:
  one envelope with two payloads (transform and inspection), a shared measurement block,
  the bounding-box delta computed by the writer rather than by the operation, warnings as
  codes, lineage as a parent id plus wiki-style references, and an artefact state declared
  from the first report so no pruning policy needs a migration.

### Repository
- MIT licence, security policy, contributing guide.
- `make check`: compiles every script and runs the publication-hygiene gate, which fails
  when a home path or an identifying name reappears in a tracked file.

## Notes
- Pre-1.0 and honest about it: no packaging, no test suite. Every check that means
  anything needs a real 3D source, and sources are never in this repository.
