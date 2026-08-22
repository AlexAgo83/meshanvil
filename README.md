<img src="docs/img/icon.png" alt="MeshAnvil icon" width="64" align="left" />

# meshanvil

<br clear="left"/>

[![CI](https://github.com/AlexAgo83/meshanvil/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexAgo83/meshanvil/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-111827.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-F5A623.svg)](changelogs/CHANGELOGS_0_1_0.md)
[![Status](https://img.shields.io/badge/status-pre--1.0-8A5A25.svg)](#engineering-honesty)
[![Blender](https://img.shields.io/badge/Blender-headless-EA7600?logo=blender&logoColor=white)](https://www.blender.org/)

**Driving a 3D application with an agent, and checking what it did.**

Using AI on 3D work. The method lives in `logics/runbook/`; the code is the residue.

The problem this project works on: a CAD assembly of several hundred to a few thousand parts,
authored for manufacturing, has to become a single closed body a printer will accept. Nothing
about that assembly was made for printing — surfaces have no thickness, parts interpenetrate,
half the geometry is internal hardware nobody will ever see. The runbooks record what worked,
what failed, and how each claim was checked.

The working assumption throughout: an agent driving a 3D application is only as good as the
measurements it takes. Renders are how you get fooled.

![The viewer: a chain graph, a render, and the findings a defect sweep found unaided.](docs/img/viewer-vehicle-defect.png)

## What it needs

Blender 4.2 or later. That is the only requirement to run an operation -- the floor comes from
the operators the pipeline calls, `bpy.ops.wm.stl_export` among them. FreeCAD 1.0 is optional
and needed only to read a STEP source. Node is for contributors, to check the corpus, and never
to run an operation.

Verified on macOS (Blender 5.2), Windows (Blender 5.2, not on `PATH`) and WSL Ubuntu (no Linux
Blender; the Windows binary is called through `/mnt/c` with paths translated). Linux is
untested. `MESHANVIL_BLENDER` and `MESHANVIL_FREECAD` override the discovered paths.

Before the first operation, run `./bin/meshanvil doctor`. It writes `work/doctor.json` with
the discovered engines, their versions, the exact platform-specific override command, and the
writability and free space of `work/`.

## Reopening this

Blender is at `/Applications/Blender.app/Contents/MacOS/Blender` (not on PATH). Everything
runs headless on a copy:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b work/out/<file>.blend \
  -P tools/list_shells.py
```

To drive the operator's open Blender session instead, see
`run_001_drive_a_live_blender_session_from_the_agent`. They arm the bridge once per launch by
pasting one line into the Python Console; after that, writing `~/bl_cmd.py` executes there
within half a second and `~/bl_out.txt` carries the output back. Heavy work stays headless so
their interface never freezes.

## What it does

Every operation follows the same loop, whether typed by a person or run by an agent:

- **`meshanvil run <operation> <source>`** writes one JSON report -- parameters, measurements
  before and after, the per-axis bounding-box delta, what the operation did **not** check, and
  the renders it produced -- with exit codes an agent can branch on.
- **`meshanvil view`** builds a local viewer over those reports -- a plain page, no framework, no
  build step. The outliner groups the chain by fork, not by parent, so a branch reads as a
  branch. The node graph places each report by its parent depth. Selecting one shows its render
  beside its numbers, and the Compare workspace wipes its before and after against each other.
  A runbook is readable straight from its list, applied or not.
- **`meshanvil list`**, **`doctor`**, **`init`**, **`runbook`** and **`prune`** round out the
  command: what an operation takes, whether the engines are found, turning a directory into a
  project, writing a runbook from a chain, and dropping heavy artefacts a report still points to.

The method behind the loop -- what to measure, what a render cannot tell you, how a claim gets
checked -- lives in `logics/runbook/`; the code above is its residue. `req_000` through `req_005`
in `logics/request/` record why each decision was made, all closed. Read the runbooks first, not
this file, if you're about to repeat the work.

## Layout

```
logics/           the corpus: request, product, decisions, backlog, tasks
  runbook/        the method: read these first
  architecture/   the decisions and why they were taken
  context-packs/  the handoff an implementation agent reads
pipeline/         the chain that produced the delivery, kept as its record
meshanvil/        the command: run, view, doctor, init, runbook, prune
tools/            the operations: parameterised scripts, each with a manifest beside it
viewer/           the page source, copied into a project's work/viewer/ at build time
scripts/          repository gates, run by make
fixtures/         the two demonstration subjects and their provenance
work/             everything generated -- git-ignored, one tree per project
  in/             source files (STEP, donor blends)
  out/            blend and stl outputs
  ops/            operation reports
  renders/        verification renders
  cache/          ray-visibility results, part lists
  viewer/         the built page for this project
  demo/           the two demonstrations, as sibling projects (see below)
```

`work/` is ignored deliberately. Committing a 27 MB blend and a 73 MB stl once took the repo
to 147 MB; the history had to be rewritten. Keep binaries out, or set up Git LFS first.

## Current state

A printable hollow body at 1/10 of the source assembly.

- 279.0 x 168.7 x 155.2 mm, one shell, 0 non-manifold edges, 438.7 cm3 of material
- centred on X and Y, sitting on z = 0
- transparent panels filled in, open barrels capped, thin parts re-imported from a donor file
- 190 x 110 mm access hatch in the floor, 78 mm of clearance, for electronics
- the four protruding round sub-assemblies made solid with the body; one pair welded by a
  6 mm pin hidden inside a recess

Known limits: the interior surface is the backside of the outer skin, not a smooth offset
(three approaches failed, all recorded in `run_007`); the stl is undecimated at 68 MB; styling
features narrower than the 8 mm voxel were erased by the remesh.

## Inputs

Two sources, both under `work/in/`, neither versioned.

**A STEP export**, 508 MB, CATIA V5R2025, AP203, **1319 closed solids**. The true source.
Everything fought in the delivery above stems from working off a tessellated export instead:
zero-thickness surfaces, split vertices, flat hierarchy, fixed resolution. Re-importing from
STEP with FreeCAD would remove most of it, at the cost of a long and memory-hungry import.
FreeCAD 1.0 is installed and runs headless as `/Applications/FreeCAD.app/Contents/MacOS/FreeCAD
-c <script>` on Python 3.11 -- not as `freecadcmd`, which this repository claimed and which does
not exist here.

**A tessellated donor blend**, 2109 objects, 5.59 M vertices. Lower quality, and it carried one
export defect: a single patch of 45 vertices smeared across 1.9 m. Repaired by grafting the
mirrored twin island — see `run_009`. The same sweep found 186 exactly coincident duplicate
objects (3.2% of the vertices) and no other smear in the file. A ray pass over the repaired
donor puts 1637 of its 1923 objects, half the vertex mass, out of sight from every exterior
direction: internal hardware, useless for a printed skin. Beware the converse — thin parts come
out "never seen" only because they fall through the ray grid.

## Engineering honesty

Pre-1.0, and no package on an index yet -- clone it, run `./bin/meshanvil`. `make check`
compiles the scripts, type-checks the viewer, runs `scripts/selfcheck.py` (host logic, no
Blender needed) and the hygiene gate. It does not run Blender: every check that means
anything needs a real 3D source, and sources are never in this repository. `scripts/
fixture_check.py` and `scripts/viewer_smoke.py` do need it -- they run against a generated
fixture, not against your data, so they stay out of `make check` and out of CI. Run the
scripts on your own file and read the numbers.

The runbooks are written from one delivery. They are specific on purpose -- a procedure
without its numbers is a blog post -- but a second assembly will bend some of them.

## Projects

One installation serves several subjects. A project is a directory holding its own reports,
sources, renders and viewer page:

```
meshanvil init ~/projects/cobra
cd ~/projects/cobra
meshanvil run scan_defects work/in/cobra.blend
meshanvil view
```

The active project is found by walking up from the working directory for a `.meshanvil`
marker, the way a version control tool finds its own. That keeps the choice visible: the
working directory is on screen and it decides where a run lands. `MESHANVIL_PROJECT` overrides
it for a caller that has no working directory to speak of, and `meshanvil doctor` states which
project it resolved and which rule chose it.

Identity numbering, parentage by fingerprint and prune retention are each scoped to one
project: the first operation of a new project is `001`, and two projects opened from the same
source file are never linked to each other.

With no marker anywhere above, the installation is the project. That is what this repository
has always been, so nothing that worked before needs a migration.

The viewer reads every project in the neighbourhood at build time and shows one, with a
chooser in the top bar when there is more than one. It selects rather than combines: two
unrelated chains in one graph would merge their outliner groups and sum totals across subjects
that share nothing.

## Demonstration data

Two demonstrations, sibling projects under `work/demo/`, so the viewer can offer both:

```
tools/build_demo_chain.sh          # the vehicle
tools/build_figurine_chain.sh      # the figurine
```

`fixtures/demo_car.blend` is a roadster modelled for rendering. Nothing in it was planted: it
carries half a body held in Mirror modifiers, panels with no thickness, three parts never
visible from outside, a uniform 1.6x oversize and a coincident duplicate, and each step of its
chain is where one of those surfaces. Its branch is the part worth reading. Two siblings, same
parent, same voxel, one step apart: one remeshes a walled body into a single closed shell, the
other remeshes the bare panels into 714 fragments with the body gone. The one that destroyed
the car reports `ok`.

![A 12 mm voxel remesh that ate the bodywork down to the chassis skeleton -- status `ok`, and the measurements panel shows the volume collapsing.](docs/img/viewer-vehicle-destroyed.png)

`fixtures/demo_figure.blend` is a sculpting base mesh, and its job is to be sound. The defect
sweep reports nothing on it, which is the only way to show that the sweeps discriminate rather
than firing on everything. It is authored at 20 741 mm tall -- an interchange file declares no
unit, so the size is a decision, and `recenter` is where that decision is recorded. At 180 mm
it is a figurine.

Its branch carries the lesson the vehicle cannot. The vehicle is remeshed at its real size,
four metres long, where a voxel in millimetres and a voxel as a fraction of the subject feel
like the same number. On a 180 mm figurine they do not. Its fingers measure 1.5 mm, so:

| voxel | across a finger | shells | non-manifold | volume lost | status |
|---|---|---|---|---|---|
| 0.5 mm | 3.0 | 1 | 0 | 0.1% | ok |
| 1.5 mm | 1.0 | 1 | 0 | 1.3% | ok |

Both pass every topology and volume check. One keeps the fingers and the other fuses them into
mittens, and the only thing that says so before you look at the render is the thin-feature
guard, which warns below two voxels across. A voxel size is a fraction of the subject, and the
checks that pass do not measure feature loss.

![The 1.5 mm branch: status `ok`, `thin_feature_voxels: 1` in the parameters panel -- one voxel across a finger, below the two-voxel floor.](docs/img/viewer-figurine-thin-feature.png)

`tools/make_demo_scene.py` and `tools/make_guard_fixture.py` are a different job. They generate
subjects whose defects are planted deliberately -- an island smeared along a line, objects
duplicated at identical coordinates, a slab exactly 2 mm thick, a sphere with a single face
removed -- so `scripts/fixture_check.py` can assert that a sweep finds what was built in and
that a guard reads a thickness it already knows. Ground truth and demonstration are different
jobs.

See `fixtures/PROVENANCE.md` for where the two subjects come from and what is known about
their licence.

## Working rules that earned their place

- Never write to the operator's live scene without being asked; never save their .blend.
- Every geometric claim gets a number. Renders confirm, they do not establish.
- After any boolean, enumerate shells and drop the debris. It always leaves some.
- Compare the output bounding box against the source. That single check caught every failure
  in this project, while the manifold checks passed throughout.
- Name-based selection lies. Naming is a supplier convention; visibility and geometry are
  measurements.
- A command that printed nothing is not a command that found nothing. Make the steps whose
  failure would be silent print a proof line -- see `run_010`.

## Reference

- [`CONTRIBUTING.md`](CONTRIBUTING.md) -- how to run things, and the house rules the reviews enforce
- [`SECURITY.md`](SECURITY.md) -- what these scripts touch, and how to report a problem
- [`changelogs/`](changelogs/) -- one file per version
