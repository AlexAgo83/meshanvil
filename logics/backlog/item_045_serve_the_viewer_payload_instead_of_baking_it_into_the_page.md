## item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page - Serve the viewer payload instead of baking it into the page
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 70%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:08:22

# AI Context
- Summary: The payload comes from a route on the served page and from the generated file only when the page was opened from disk.
- Keywords: payload route, build-time snapshot, opened-from-disk fallback
- Use when: Changing where the page's data comes from.
- Skip when: Changing what the payload contains.

# Problem
- The payload is written into `work/viewer/data.js` when the command runs, so the page is a snapshot: reloading it cannot show a report that landed afterwards.

# Scope
- In:
  - A route that returns the payload the build already computes.
  - The client reading that route when it is served, and the generated file when it is not.
  - Keeping the generated fallback file exactly as it is for a page opened from disk.
- Out:
  - Response caching, ETags and conditional requests -- not yet worth their code at this payload size.
  - Any change to the payload's contents.

# Acceptance criteria
- AC1: A served page renders from the route, not from the generated file.
- AC2: A page opened from disk renders exactly as it does today.
- AC3: A report rendered before and after this change is identical, compared against a baseline captured before any code in this request was touched.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: A served page renders from the route, not from the generated file.
- request-AC12 -> This backlog slice. Proof: AC2: A page opened from disk renders exactly as it does today.

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- What bakes it: `build()` (`meshanvil/viewer.py:68`) assembles the payload dict and writes `window.MESHANVIL = {...}` into `work/viewer/data.js` at `meshanvil/viewer.py:101`. The client reads it once into a single const at `viewer/viewer.js:21`.
- One consumer disappears with the change: `view()` (`meshanvil/viewer.py:184`) counts reports by re-reading `data.js` and string-splitting on `"= "` (`meshanvil/viewer.py:184`). With the payload a return value, that parse of a file the same function just wrote goes away.
- The served root is `root/"work"`, not `work/viewer` -- deliberately, so renders under `work/renders/` are reachable (`meshanvil/viewer.py:193` states why). A payload route lives under that root, so its path must not collide with a real file there.
- The payload already includes every project, every catalogue and the doctor snapshot, so the route returns what `build()` returns; nothing new is computed.

- The baseline AC3 compares against does not exist in the repository: `work/` is gitignored and empty on a fresh clone. Capture it first, before editing anything -- `python3 scripts/fixture_check.py` writes reports into `work/ops` (it needs Blender; `/Applications/Blender.app/Contents/MacOS/Blender` by default, `MESHANVIL_BLENDER` to override), then `meshanvil view --no-open` builds the page. Keep the resulting `work/viewer/data.js` outside the tree as the reference. Captured after the work has started, this criterion proves nothing.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Primary task(s): `task_024_deliver_the_live_viewer_and_the_module_structure`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
