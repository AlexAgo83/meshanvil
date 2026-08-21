# meshanvil

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

## What is being built

The method exists; the tooling around it does not yet. What is specified, and ready to be
implemented, is a loop that makes each operation reviewable:

- one JSON report per operation, carrying its parameters, its measurements before and after, the
  per-axis bounding-box delta, what it did **not** check, and the renders it produced;
- one command that runs a named operation, callable identically by a person, Claude or Codex,
  with exit codes an agent can branch on;
- one local viewer -- a plain page, no framework, no build -- showing the chain as a graph, the
  renders beside the numbers, and two states of the same geometry wiped against each other.

The whole specification lives in `logics/`: `req_000` states the problem, `prod_001` the product,
`adr_001` to `adr_006` the decisions, and `task_001` sequences thirteen slices. Start there, not
here.

## Layout

```
logics/           the corpus: request, product, decisions, backlog, tasks
  runbook/        the method: nine runbooks, read these first
  architecture/   the decisions and why they were taken
  context-packs/  the handoff an implementation agent reads
pipeline/         the chain that produced the delivery, in execution order
tools/            inspection scripts, and the generators for the demo fixture
scripts/          repository gates, run by make
work/             everything generated -- git-ignored
  in/             source files (STEP, donor blends)
  out/            blend and stl outputs
  ops/            operation reports        (once item_001 exists)
  renders/        verification renders
  cache/          ray-visibility results, part lists
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

Pre-1.0. There is no package, no test suite and no CLI yet: what exists is a method, the
scripts that produced one delivery, and the measurements that verify them. `make check`
compiles the scripts and runs the publication-hygiene gate; it does not run Blender,
because every check that means anything needs a real 3D source and sources are never in
this repository. Run the scripts on your own file and read the numbers.

The runbooks are written from one delivery. They are specific on purpose -- a procedure
without its numbers is a blog post -- but a second assembly will bend some of them.

## Demonstration data

`tools/make_demo_scene.py` generates a synthetic housing carrying two real export defects: one
island smeared along a line, and objects duplicated at identical coordinates. `tools/scan_defects.py`
finds them without being told where they are -- a ratio of 2.9 on the smear, four duplicates at
37% of the vertices. `tools/run_demo_chain.py` replays the chain on it, and
`tools/render_fixed_views.py` renders the canonical directions on a camera fixed per subject,
which is what makes two states comparable.

Nothing is downloaded, nothing is licensed, and nothing binary is committed.

## Working rules that earned their place

- Never write to the operator's live scene without being asked; never save their .blend.
- Every geometric claim gets a number. Renders confirm, they do not establish.
- After any boolean, enumerate shells and drop the debris. It always leaves some.
- Compare the output bounding box against the source. That single check caught every failure
  in this project, while the manifold checks passed throughout.
- Name-based selection lies. Naming is a supplier convention; visibility and geometry are
  measurements.

## Reference

- [`CONTRIBUTING.md`](CONTRIBUTING.md) -- how to run things, and the house rules the reviews enforce
- [`SECURITY.md`](SECURITY.md) -- what these scripts touch, and how to report a problem
- [`changelogs/`](changelogs/) -- one file per version
