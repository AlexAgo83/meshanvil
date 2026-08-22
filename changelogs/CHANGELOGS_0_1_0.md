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

### Method, continued
- `run_010_verify_that_a_command_did_what_it_appeared_to_do`: six silent failures collected in
  one session -- an unmatched zsh glob aborting a cleanup, an exit code eaten by a pipe, an
  unquoted variable that zsh does not split, a value collapsing across four nested shells, a
  `\b` anchor undefined in the ERE `git grep` uses, and a Blender bounding box read from a
  stale cache. Each one produced a wrong conclusion that a single proof line would have caught.

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

### Specification, ready to implement
- `req_000` with 25 acceptance criteria, `prod_001`, and thirteen backlog slices sequenced by
  `task_001` in the order they must be built -- the report first, since every other slice reads
  what it writes.
- Six decisions with their reasons: `adr_001` the report format, with canonical JSON shapes for a
  transform, an inspection and an operation manifest; `adr_002` the logics-manager dependency;
  `adr_003` a viewer that reads while the command acts; `adr_004` the target technology, the
  process model and the repository layout; `adr_005` identity, concurrency, exit codes and the
  progress heartbeat; `adr_006` the bridges into the corpus.
- Platform matrix measured rather than assumed: macOS, Windows and WSL verified, Linux stated as
  unverified for want of a machine with Blender on it.

### Demonstration fixture
- `tools/make_demo_scene.py` generates a synthetic scene with two real export defects, calibrated
  on the ones observed in practice, so `tools/scan_defects.py` finds them unaided. That is the
  ground truth the sweep never had.
- The chain is replayed through the runner, and renders use the canonical directions on a
  fixed camera, which is what makes two states comparable. (Superseded by
  `tools/build_demo_chain.sh` and `tools/build_figurine_chain.sh`, which run the same idea
  through `bin/meshanvil` instead of a standalone script.)

### Repository
- MIT licence, security policy, contributing guide.
- `make check`: compiles every script and runs the publication-hygiene gate, which fails
  when a home path or an identifying name reappears in a tracked file.

## Notes
- Pre-1.0 and honest about it: no packaging, no test suite. Every check that means
  anything needs a real 3D source, and sources are never in this repository.
