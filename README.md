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

## Layout

```
logics/           the Logics corpus: product context, requests, backlog, tasks
  runbook/        the method: nine runbooks, read these first
pipeline/         the chain that produced the delivery, in execution order
tools/            reusable inspection scripts
work/             everything generated -- git-ignored
  in/             source files (STEP, donor blends)
  out/            blend and stl outputs
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
STEP with FreeCAD (`freecadcmd`, installed) would remove most of it, at the cost of a long and
memory-hungry import. Worth doing only when something actually blocks.

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
