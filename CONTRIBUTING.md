# Contributing

## Getting Started

- Install Blender 4.2 or later. The scripts are run with `-b` (headless) and never need
  the interface.
- The examples assume macOS, where Blender is not on `PATH`:
  `/Applications/Blender.app/Contents/MacOS/Blender`. On Linux or Windows, use your own
  path; nothing else changes.
- Put your own 3D sources under `work/in/`. Nothing in `work/` is versioned.
- The corpus checks need Node: `npm ci` installs the pinned `logics-manager`. Running the 3D
  operations themselves needs only Blender.

Run any script on a copy:

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

## Validation

```bash
make check      # compiles the scripts, runs the publication-hygiene gate
make logics     # lints and audits the corpus with the pinned logics-manager
```

`make check` compiles every script and runs the publication-hygiene gate. It deliberately
does not run Blender: the checks that matter here need a real 3D source, and those are
never in the repository. Run the relevant script on your own file and report the numbers
in the change.
