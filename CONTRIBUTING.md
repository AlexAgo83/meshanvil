# Contributing

## Getting Started

- Install Blender 4.2 or later. The scripts are run with `-b` (headless) and never need
  the interface.
- The examples assume macOS, where Blender is not on `PATH`:
  `/Applications/Blender.app/Contents/MacOS/Blender`. `MESHANVIL_BLENDER` overrides it.
- Verified platforms: macOS (Blender 5.2, host Python 3.11), Windows (Blender 5.2 installed but
  not on `PATH`, host Python 3.10) and WSL Ubuntu (host Python 3.14, no Linux Blender -- the
  Windows binary is called through `/mnt/c` and paths are translated with `wslpath`). Blender
  reports the same embedded Python 3.13 on all three.
- **Linux is unverified.** No machine with Blender was available to check it. Treat it as
  untested rather than supported until someone runs the fixture there.
- Put your own 3D sources under `work/in/`. Nothing in `work/` is versioned.
- The corpus checks need Node: `npm ci` installs the pinned `logics-manager`. Running the 3D
  operations themselves needs only Blender.

Run an operation through the command, which writes a report:

```bash
./bin/meshanvil list
./bin/meshanvil run scan_defects work/out/demo_source.blend
./bin/meshanvil view            # or --serve, to refresh while a chain is running
```

Or run any script directly, as they all still work standalone:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b work/out/<file>.blend -P tools/list_shells.py
```

## Workflow

- Keep changes focused and commits small, one logical change per commit.
- The runbooks in `logics/runbook/` are the deliverable; the scripts are their residue. A
  procedure that worked belongs in a runbook, with the numbers that verified it and the
  limits it does not cover.
- Record what a change delivers in [`changelogs/`](changelogs/), one file per version.
- Use the existing Logics corpus for product and workflow context. Use
  `logics-manager status`, `lint` and `audit` for workflow state and validation. Do not
  hand-edit Logics status fields, indicators or lineage links.

## House rules that the reviews enforce

- Every geometric claim gets a number. A render confirms a result; it does not establish one.
- Compare the output bounding box against the source. In this project that single check
  caught every failure, while the manifold checks passed throughout.
- Never write to the operator's live scene without being asked, and never save their
  `.blend`.
- No client names, no source file names, no home paths in tracked files or commit
  messages. The repository is public; the sources it is used on are not.
- Host code never imports `bpy`; Blender-side code never imports a host module. The two run
  in different interpreters -- Blender embeds its own -- and talk through files.
- The viewer is plain JavaScript, typed with JSDoc. No framework, no build step: it has to
  open from disk. See `adr_004_target_technology_and_process_model` before adding either.

## Working from the corpus

The specification is in `logics/`, not in this file. `req_000` states the problem, `prod_001` the
product, `adr_001` to `adr_006` the decisions and their reasons, and `task_001` sequences the
slices in the order they must be built. `logics/context-packs/` holds the handoff an
implementation agent reads.

Two rules that are easy to break and expensive to unbreak:

- `meshanvil/` (host) and `meshanvil_engine/` (inside Blender or FreeCAD) never import each
  other. They share a schema, not a module.
- The corpus is checked in CI. `logics-manager sync update-indicators <ref> --touch` after
  editing a document, and never hand-edit indicators, lineage links or generated sections.

## Validation

```bash
make check      # compiles the scripts, runs the publication-hygiene gate
make logics     # lints and audits the corpus with the pinned logics-manager
```

`make check` compiles every script and runs the publication-hygiene gate. It deliberately
does not run Blender: the checks that matter here need a real 3D source, and those are
never in the repository. Run the relevant script on your own file and report the numbers
in the change.
