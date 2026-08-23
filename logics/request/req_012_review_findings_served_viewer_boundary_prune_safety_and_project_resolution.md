## req_012_review_findings_served_viewer_boundary_prune_safety_and_project_resolution - Review findings: served viewer boundary, prune safety and project resolution
> From version: 0.1.0
> Schema version: 1.0
> Status: Obsolete
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: General
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 02:47:54

# AI Context
- Summary: Findings from a read-only review of the repository at `3e13ed0`. `make check` and `make logics` both pass; the corpus has no open document. What follows are candidates, ranked by strength of evidence, not committed work.
- Keywords: review, findings, viewer, serve, token, prune, paths, security
- Use when: deciding what to promote into a backlog slice after this review.
- Skip when: looking for the state of an operation, an engine, or a runbook; this doc only covers host-side code.

# Needs

## N1 -- The served viewer hands out its own run token to any unauthenticated caller
`viewer_payload.payload()` puts `run_token` in the payload (`meshanvil/viewer_payload.py:64`).
Two routes then serve that payload with no token check: `GET /api/data`
(`meshanvil/viewer_routes/data.py:9-17`) and the static file `work/viewer/data.js`, which
`viewer.view()` exposes because the whole of `work/` is the served directory
(`meshanvil/viewer.py:33-36`). The token is what gates `POST /run` and `POST /file`.
Observed on a scratch project:

```
GET  /api/data        -> run_token = xAY_iB4fvrvGXiBiHuWYFpyr8W7d4plZ   (no token sent)
GET  /viewer/data.js  -> "run_token": "xAY_iB4fvrvGXiBiHuWYFpyr8W7d4plZ"
POST /run  {"command":"doctor"}  with that token -> 200, exit_code 0
```

`SECURITY.md` states the token is "embedded only in that process's own generated page". That is
no longer true, and `adr_007`'s boundary rests on it.

## N2 -- The listening port is deterministic and no request origin is checked
`viewer_server.stable_port()` derives the port from a SHA-256 of the project path
(`meshanvil/viewer_server.py:14-15`), so the port follows from the project location rather than
being random. `SECURITY.md` still describes "a random port". No handler inspects `Origin`,
`Referer` or `Host`; a cross-origin request is answered normally:

```
curl -H "Origin: http://evil.example" http://127.0.0.1:38965/api/data  -> 200
```

Binding to `127.0.0.1` does not by itself stop a page in the operator's own browser, and with N1
the token is not a second factor. The custom `X-Meshanvil-Token` header does force a preflight,
which is the property currently doing the work; that should be a stated defence rather than an
accident.

## N3 -- `prune` deletes files outside the project root, then crashes reporting them
`prune.candidates()` accepts any absolute `output.path` a report carries and only excludes paths
under `work/in` (`meshanvil/prune.py:11-25`) -- there is no check that the path is inside the
project. `prune.run()` unlinks before `cli.main()` prints, and the print uses
`path.relative_to(project)` (`meshanvil/cli.py:96`), which raises on exactly the paths that were
not contained. Observed with a report whose output path sat one directory above the project:

```
meshanvil prune --keep 0
ValueError: '.../outside.stl' is not in the subpath of '.../proj'
ls .../outside.stl -> No such file or directory      # deleted before the traceback
```

`--dry-run` raises the same `ValueError` without deleting, so the dry run does not warn about the
case it exists to warn about.

## N4 -- Directory listing of `work/` is served unauthenticated
`make_server` uses `SimpleHTTPRequestHandler` over `root/work` with listings left on
(`meshanvil/viewer_server.py:73,101`). `GET /` returns `in/`, `out/`, `ops/`, `renders/`,
`doctor.json`. Path traversal is refused (`/../../etc/passwd` -> 404), so the exposure is bounded
to `work/` -- but `SECURITY.md` names source file paths as the sensitive part of this work, and
enumeration of `work/in` is exactly that. Listings are not needed by the page, which fetches
`/api/data`.

## N5 -- An interrupted run leaves the engine process running
`runner.run()` starts the engine with `subprocess.Popen` and waits in `watch()`; on any
`BaseException` it unlinks the report and re-raises without terminating the child
(`meshanvil/runner.py:204-208`). After Ctrl-C the operator has no report, the identity is
released, and a Blender process is still writing to the path that was just removed. The target
lock is released in the same `finally`, so a second run on the same source is allowed to start
alongside the first.

## N6 -- The SSE endpoint is unauthenticated and holds one thread per connection forever
`/api/events` loops without exit while the socket is open (`meshanvil/viewer_routes/events.py:31-55`)
on a `ThreadingHTTPServer` with no connection cap. Every tab, and every browser reconnect, keeps a
thread and re-stats every report and runbook once a second. No token is checked, so anything that
can reach the port can pin threads.

## N7 -- `paths.resolve()` falls back to the working directory while calling it the installation
The module docstring says "With no marker anywhere above, the installation is the project"
(`meshanvil/paths.py:16-17`), but the fallback returns `Path.cwd()` labelled `BY_INSTALLATION`
(`meshanvil/paths.py:55`), which is not `code_root()`. Observed from an unmarked scratch
directory: `resolve() -> (.../scratchpad/nomarker, 'installation')` while
`code_root()` pointed at the checkout. Since this value decides where a destructive run lands,
the label and the doc should agree with the behaviour, whichever one is meant.

# Context
- Validation run for this review, all green at `3e13ed0`: `make check` (byte-compilation, `tsc --noEmit`,
  viewer bundle + line budget, `pytest -q` 21 passed, i18n 214 keys/2 languages, hygiene) and
  `logics-manager health` (124 docs, 0 issues, 0 open, 0 stale).
- Findings N1-N4 and N7 were reproduced against a scratch project under the session scratchpad, not
  against this repository's `work/`. N5 and N6 are read from the code; neither was executed.
- Host-side Python is ~1.9k lines and is covered by `scripts/selfcheck.py` through thin `pytest`
  wrappers. The engine-side code -- `tools/` and `pipeline/`, 2099 lines -- has no automated check
  beyond byte-compilation. The Makefile says so deliberately (`fixture` needs Blender and stays out of
  CI), so this is recorded as a known shape of the project, not as a defect.
- Not a defect, a taste note: `viewer/src/app.js` is 962 lines against a 300-line budget it is
  explicitly excepted from (`scripts/check_line_budget.mjs`), with the exception naming its own exit
  ("split by screen as the next slices touch each screen"). The exception is doing what it says.
- `markdown.js` escapes before it applies inline markup, and every `innerHTML` site in `app.js`
  passes user-facing text through `esc()`. Render URLs are interpolated into `src="..."` after
  `esc()`, which escapes quotes but not schemes; those values come from reports written by the
  engine, so nothing was found to exploit it.
- `SECURITY.md` was last touched at commit e092ff8, `viewer_server.py` at commit 79aeead. N1 and N2 read as
  the document falling behind the code rather than as a decision that was made.

# Acceptance criteria
- AC1: `run_token` is not readable without already holding it -- neither from `/api/data` nor from
  any static file under the served directory -- and the `POST /run` and `POST /file` boundary is
  reachable only by the page the server itself generated.
- AC2: `SECURITY.md` and `adr_007` describe the boundary that the code actually implements: how the
  port is chosen, what the token proves, and what a cross-origin request gets.
- AC3: `prune` refuses, or clearly reports, any output path outside the project root, and neither
  `prune` nor `prune --dry-run` can end in an unhandled traceback.
- AC4: An interrupted `meshanvil run` leaves no engine process behind, and what it leaves on disk is
  stated.
- AC5: Each accepted finding leaves one runnable check behind in `scripts/selfcheck.py`, so the
  behaviour is held by the suite that already gates CI.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

Out of scope: the engine-side geometry code, the viewer's visual design, and the `~/bl_cmd.py`
bridge described in `run_001`, which is armed by hand and already documented as such.
Risk: N1-N4 touch `adr_007`'s boundary, so a slice that changes them supersedes part of that
decision rather than merely implementing it.

# Companion docs
- Product brief(s): `prod_007_a_served_viewer_that_can_run_what_it_already_shows`
- Architecture decision(s): `adr_007_let_the_served_viewer_execute_a_closed_command_set`

# References
- `meshanvil/viewer_server.py`
- `meshanvil/viewer_payload.py`
- `meshanvil/viewer_routes/data.py`
- `meshanvil/viewer_routes/events.py`
- `meshanvil/prune.py`
- `meshanvil/cli.py`
- `meshanvil/runner.py`
- `meshanvil/paths.py`
- `SECURITY.md`

# Backlog
- none

# Links
- Superseded by: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
