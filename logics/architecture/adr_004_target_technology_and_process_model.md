## adr_004_target_technology_and_process_model - Target technology and process model
> Date: 2026-08-21
> Status: Accepted
> Related request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
> Related backlog: `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`
> Related task: `task_001_deliver_the_reviewable_operation_loop`
> Drivers: two Python interpreters that cannot share imports, a viewer that must open with no server, an install cost near zero for someone who came for the 3D
> Reminder: Update status, linked refs, decision rationale, consequences, and follow-up work when you edit this doc.
> Indicators reviewed: 2026-08-23 01:55:34

# Overview
- Stdlib Python on both sides of a process boundary, a JSON job in and a JSON report out, and a viewer that is a plain page reading a generated data file -- no framework, no build step, and no dependency a 3D user has to install beyond Blender itself.

```mermaid
flowchart TD
  agent[Operator or agent] --> cli["bin/meshanvil — host Python 3.11+, stdlib only"]
  cli --> job[work/ops/.job/NNN.json<br/>what to run, on what]
  cli -->|subprocess| bl["Blender -b file -P operation --  --job …"]
  job --> bl
  bl --> mod["meshanvil.report — imported INSIDE Blender<br/>stdlib + bpy/bmesh only"]
  mod --> rep[work/ops/NNN_name.json]
  mod --> ren[work/renders/*.png]
  rep --> data["meshanvil view → work/viewer/data.js"]
  ren --> data
  data --> page["work/viewer/index.html<br/>plain HTML/CSS/JS, opened from disk"]
  cli -.->|--serve, opt-in| srv["http.server on 127.0.0.1:0<br/>only when auto-refresh is wanted"]
  srv -.-> page
```

# Context
- Blender 5.2 embeds Python 3.13.13; the machine this was developed on runs 3.11.15. The two interpreters cannot share an import, a virtualenv or a package. Any code that touches `bpy` runs in Blender's interpreter and nothing else.
- cm-sim already solved the same boundary: a job JSON is written, Blender is launched on a worker script, the worker writes a result JSON, and the worker is documented as "run by Blender, never imported by the UI". That contract is proven in the same house and is reused rather than reinvented.
- The audience is someone who came for 3D work. Every dependency they must install before seeing anything is a reason to stop. Blender is unavoidable; a package manager, a virtualenv and a Node toolchain are not.
- `adr_003` already settled that the viewer only reads. That removes the reason most local tools need a server: there is nothing to post.
- A page opened from disk cannot `fetch` a neighbouring JSON file -- browsers refuse it as a cross-origin request. A classic `<script src>` on the same directory is not subject to that restriction, which is what makes a serverless viewer possible at all.
- The mockup drew the operation graph, the wipe and the whole interface with plain SVG and CSS, no library. It is evidence that the DAG needs no diagramming dependency.

# Decision
- **Host side: Python 3.11 or later, standard library only.** `bin/meshanvil` is the entry point. No third-party runtime dependency, no virtualenv required, no packaging step to try the tool. `subprocess`, `json`, `hashlib`, `argparse`, `http.server` cover everything the runner needs.
- **Blender side: a module imported inside Blender, `bpy`/`bmesh` plus stdlib.** The report writer lives there because only Blender can measure the scene. It must never be imported by the host process, and the host must never import `bpy`.
- **The boundary is a file, not a pipe.** The host writes a job JSON, launches `blender -b <file> -P <operation> -- --job <path>`, and reads the report the operation wrote. stdout stays human output; nothing is parsed out of it. A crashed Blender leaves a job and no report, which is a diagnosable state rather than a truncated stream.
- **The process model takes more than one engine.** Blender cannot read STEP, and the true source of this project is a 508 MB STEP file. FreeCAD 1.0 is installed and runs a script headless -- as `/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c <script>`, on Python 3.11.13, not as the `freecadcmd` name the README claimed. Since the boundary is a job file and not an import, a FreeCAD operation is the same contract with a different binary: `engine` names it, `MESHANVIL_FREECAD` overrides its path, and everything downstream is unchanged.
- **Operations stay ordinary Blender scripts.** They keep running under a bare `blender -b file -P script`, with the report writer degrading to stdout when no job is present. The runner is a convenience over them, never a prerequisite.
- **The viewer is written in plain JavaScript, typed with JSDoc and checked by `tsc --checkJs --noEmit`.** Types where they pay -- the report contract -- without a bundle, without an emitted artefact, and without breaking a page opened from disk. The house precedent agrees: the Logics viewer's own sources are plain `.js` modules bundled to an IIFE; its TypeScript serves the VS Code extension, not the viewer.
- **No React, and the trigger to revisit is written down.** The viewer's state is five values -- selected operation, workspace, image view, compare view, wipe position -- across six render functions with no cross-invalidation. React earns its keep when state outgrows manual invalidation: combined filters, multi-selection, a virtualised list over thousands of operations. Any of those arriving is the moment to port, not before.
- **The migration path is known, so the decision is cheap to reverse.** Sources move to `.ts`, esbuild bundles them `--format=iife`, and the page keeps loading a classic script. A module build would not: `<script type="module">` is refused from `file://` by the same policy that blocks a `fetch` of a neighbouring JSON, which would cost the serverless viewer.
- **The viewer is a plain page: HTML, CSS and JavaScript, no framework and no build.** `meshanvil view` writes `work/viewer/data.js` -- the reports as one assignment -- next to a static `index.html`, then opens it. It works from `file://`, offline, with no process left running.
- **A server is opt-in.** `meshanvil view --serve` starts `http.server` bound to `127.0.0.1` on port 0 for auto-refresh while a chain is running. It serves `work/` read-only. That is the only mode that keeps a process alive.
- **The graph is drawn with our own SVG.** Bezier links between absolutely positioned nodes, as the mockup already demonstrates. Mermaid stays for `Export chain as Mermaid`, which produces diagram text for a Logics document and renders nothing here.
- **Publication decision superseded by `adr_008_python_package_distribution_and_runtime_assets`.** This ADR originally chose no PyPI package, no npm package and no installer; `adr_008` now chooses a Python package while keeping the npm devDependency for contributor tooling only.
- **Cross-platform, on a measured matrix.** macOS: Blender 5.2 with Python 3.13.13, host Python 3.11.15, FreeCAD 1.0 on 3.11.13. Windows: Blender 5.2 installed but not on PATH, host Python 3.10.4. WSL Ubuntu: host Python 3.14.4, no Linux Blender, the Windows binary reachable through /mnt/c. Linux: unverified, no machine with Blender available to check it.
- **The Python floor is 3.10, not 3.11.** It was declared before the platforms were measured; Windows carries 3.10.4 and nothing the host needs -- `json`, `subprocess`, `hashlib`, `argparse`, `http.server` -- requires more. The floor follows the machines rather than the machines following the floor.
- **Engines are located, then overridden.** The macOS bundle, the Windows install directory, a binary on PATH, each superseded by `MESHANVIL_BLENDER` or `MESHANVIL_FREECAD`. A missing engine is exit code 2 with a message naming the override.
- **Paths are translated at the engine boundary, not before.** When the host runs in WSL and the engine is a Windows binary, every path in the job is converted with `wslpath` on the way in and back on the way out. Verified: the Windows Blender runs from WSL both on a script under `C:` and on a script inside the WSL filesystem reached through a `\\wsl.localhost` UNC path, reporting the same Python 3.13.13 in both.
- **The viewer is opened by the platform's own opener, and WSL is the exception.** `wslview` is absent there and `xdg-open` has no browser behind it; `explorer.exe` is what works.
- **Amendment, 2026-08-23: the served viewer is now the default.** `meshanvil view` starts the loopback server, reuses a live viewer for the same project when one answers its liveness probe, and keeps the opened-from-disk snapshot behind `meshanvil view --file`. The snapshot still writes `work/viewer/data.js` and still opens with no server.
- **Amendment, 2026-08-23: auto-refresh is delivered with stdlib polling and browser primitives.** The server exposes `/api/data` for the current payload and `/api/events` as a server-sent event stream carrying component names, not report data. The client refetches the payload and rerenders; when `EventSource` is unavailable it falls back to a self-throttling timer. There is no websocket and no file-watching dependency.
- **Amendment, 2026-08-23: the client has a build step.** Source lives under `viewer/src/`, esbuild bundles it to the committed classic script `viewer/viewer.js`, and `make check` fails if the bundle is stale. This exercises the migration path this ADR already named. The rejected alternative was a hand-written concatenator in Python: it would be more local code to own than the devDependency it avoids.


# Layout and the import rule

```
bin/meshanvil            entry point, host side, stdlib only
meshanvil/               host package: runner, manifests, doctor, viewer generation
  engine/                launch, path translation, discovery
meshanvil_engine/        imported INSIDE Blender or FreeCAD: report writer, measurements
  report.py              the only writer of a report
pipeline/                the delivered chain, ordinary engine scripts
tools/                   inspection scripts and the fixture generators
viewer/                  index.html, viewer.css, viewer.js -- copied next to work/viewer/data.js
work/                    everything generated, never versioned
```

- **The engine side is reached by path, not by installation.** The runner passes the repository
  root in the job; an operation begins with
  `sys.path.insert(0, job["root"])` and then `from meshanvil_engine import report`. Blender's
  interpreter knows nothing about the repository otherwise, and nothing is ever installed into it.
- **An operation run without the runner still works**: no job means no root, and the report writer
  falls back to printing to stdout, which is how the twelve existing scripts behave today.
- `meshanvil/` never imports `meshanvil_engine`, and `meshanvil_engine/` never imports `meshanvil`.
  They share a schema, not a module.

# Consequences
- The file boundary earns its keep a second time on WSL: nothing is parsed from a stream that crosses two operating systems, only a file that both sides can read once its path is translated.
- Someone with Blender installed can clone and run an operation with no other setup. That is the acceptance bar for the install cost, and it is checkable.
- Three interpreters now: the host on 3.11+, Blender on 3.13, FreeCAD on 3.11. None of them import each other. The rule generalises rather than complicates: engine code imports its engine, host code imports neither.
- Two codebases in one repository with a hard rule between them: `tools/` and `pipeline/` import `bpy`, `bin/` and the host module never do. A host module importing `bpy` is a defect, and it is cheap to check.
- The report writer cannot use anything Blender does not ship. No `pydantic`, no schema library: validation is a function.
- The serverless viewer duplicates the report data into `data.js`. For a chain of tens of operations that is kilobytes; renders stay referenced by path, not inlined, so the page stays small. If a chain ever makes that file heavy, `--serve` already exists as the answer.
- That answer is now the default mode because it is the only one that can stay current. The file snapshot remains the offline fallback and compatibility path; it is no longer the normal workflow for watching reports land.
- The event stream's idle bound is explicit in code: each poll sleeps at least 1 second and otherwise at least 20 times the signature-scan cost. The browser smoke covers the fallback path by disabling `EventSource` and proving a report written after page load appears without a reload.
- `--serve` is no longer only that answer: `adr_007_let_the_served_viewer_execute_a_closed_command_set` adds one endpoint to this same server, so a served page can run a closed set of commands a `file://` page can only copy. The bind address, the opt-in nature, and the read-only file serving this ADR decided are unchanged; the new endpoint is additional surface on the same process, not a second one.
- Correction to `adr_002`: the vendored Mermaid bundle is no longer what draws the chain, since the graph is our own SVG. The dependency stands on the pinned CLI and the viewer conventions; Mermaid is now only an export format.
- Type checking runs in `make check` once the viewer exists, on the same footing as the Python compile step. The configuration lands with the code it checks, not before: a `tsconfig.json` checking nothing is a file that only ever gets stale.
- The report contract is authored in Python and typed again in JSDoc. That duplication is deliberate and small; if the two drift, the fixture catches it, because the viewer reads reports the fixture produced.
- Choosing plain JavaScript here diverges from cts, which is React and Vite. The reason is the constraint those repositories do not have: a page that must open from disk with no server and no build.
- No packaging means no version pinning for users and no installation story. Acceptable while the audience is one person and the value is the method, not the distribution. It becomes a decision to revisit the day someone else wants to run it.

# References
- The boundary contract this reuses: the cm-sim Blender worker, job JSON in and result JSON out
- The read-only constraint it builds on: `adr_003_the_viewer_reads_the_command_acts`
- The report it carries: `adr_001_operation_report_format`
- Related request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Related backlog: `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`
- Related task: `task_001_deliver_the_reviewable_operation_loop`
