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
tools/build_demo_chain.sh [asset.blend]        # a render-scale subject
tools/build_figurine_chain.sh [asset.blend]    # a small, sound subject
```

Given no argument, each defaults to a hand-modelled subject checked in under
`logics/external/modeles-3D/` -- authored for this project, nothing downloaded, nothing to
license. `tools/make_demo_vehicle.py` and `tools/make_demo_figure.py` build the same kind of
subject from primitives instead, with no donor file at all; generate one and pass it as the
argument to use it in either chain's place. No operation in either chain is specific to one
subject.

The vehicle-scale chain is built to expose defects a render asset typically carries and a
printing pipeline cannot ignore: on the current subject, `scan_defects` finds a real coincident
duplicate unaided, and `solidify` genuinely walls panels that had no thickness (23 of them, 20
already closed, per its own report). The clearest branch is the coarse-voxel one at the end
(006a): a tolerance-based refusal, kept as evidence rather than silently reported. The
walled-vs-unwalled remesh just above it (006 vs 005a) is the same voxel with and without the
wall; whether the unwalled side collapses far enough to be refused too depends on how much
other closed geometry the rest of the subject carries nearby.

The figurine-scale chain is built around a sound, closed, single-object subject reduced to a
small print size. The defect sweep reporting nothing on it is the point: a demonstration where
every check fires on everything never shows that the checks discriminate. Its branch carries
the lesson the vehicle-scale chain cannot: at a subject's real size, an absolute voxel and a
voxel as a fraction of that size feel like the same number; at a small size they do not. Two
voxel sizes both pass every topology and volume check, and only the thin-feature guard -- and
the render -- say that one of them fused a thin feature into the surrounding mass.

`tools/make_demo_scene.py` and `tools/make_guard_fixture.py` are a different job. They generate
subjects whose defects are planted deliberately -- an island smeared along a line, objects
duplicated at identical coordinates, a slab exactly 2 mm thick, a sphere with a single face
removed -- so `scripts/fixture_check.py` can assert that a sweep finds what was built in and
that a guard reads a thickness it already knows. Ground truth and demonstration are different
jobs.

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
