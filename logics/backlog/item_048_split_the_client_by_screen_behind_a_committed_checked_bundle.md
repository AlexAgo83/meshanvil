## item_048_split_the_client_by_screen_behind_a_committed_checked_bundle - Split the client by screen behind a committed, checked bundle
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 70%
> Complexity: High
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:08:22

# AI Context
- Summary: Client sources split by screen behind a committed bundle with a staleness check and an enforced per-file line budget, and the ADR that makes the build step legal.
- Keywords: client modules by screen, bundler, committed bundle, staleness check, line budget, adr_004 amendment
- Use when: Changing how the client's code is divided or built.
- Skip when: Changing what the client renders.

# Problem
- `viewer/viewer.js` is 908 lines covering every screen, so every viewer slice edits the same file, and nothing says when it is too big.
- A page opened from disk cannot load ES modules, so splitting the client requires a build step, which `adr_004` currently rules out.

# Scope
- In:
  - Client sources split by screen rather than by layer, with a small shared state seam and a shared constants module.
  - A bundler producing a committed, readable bundle, plus a check that fails when the committed bundle no longer matches its sources.
  - A per-file line budget enforced in `make check`, with a registry of justified exceptions.
  - The ADR amendment recording both the build step and the delivered auto-refresh, naming the rejected hand-written-concatenator alternative.
- Out:
  - Any framework, reactive runtime or state library.
  - Client-side unit tests, which stay out until a client module carries real logic.
  - Any change to what the client renders.

# Acceptance criteria
- AC1: No client source file exceeds the stated budget, or it is in the registry with its reason.
- AC2: The bundle is committed and a check fails when it is stale against its sources.
- AC3: A page opened from disk still works with no build tool present on the machine.
- AC4: The ADR records the build step, the delivered auto-refresh, and the rejected alternative.
- AC5: The rendered page is unchanged.

# AC Traceability
- request-AC6 -> This backlog slice. Proof: AC1: No client source file exceeds the stated budget, or it is in the registry with its reason.
- request-AC7 -> This backlog slice. Proof: AC2: The bundle is committed and a check fails when it is stale against its sources.
- request-AC8 -> This backlog slice. Proof: AC3: A page opened from disk still works with no build tool present on the machine.

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- Sizes as they stand: `viewer/viewer.js` 908 lines, `viewer/viewer.css` 288, `viewer/index.html` 129.
- What ships is a literal tuple: `build()` copies exactly `("index.html", "viewer.css", "viewer.js", "icon.png")` (`meshanvil/viewer.py:72`). A bundle under a new name is not shipped until it is in that tuple.
- `tsconfig.json` sets `include: ["viewer/*.js"]` with `checkJs` and `noEmit`. Sources moving into a subdirectory means that glob moves with them, and the committed bundle has to be excluded or `make types` checks the same code twice and reports duplicate-symbol noise.
- The toolchain today is two devDependencies -- `@grifhinz/logics-manager` and `typescript` -- and `make types` runs `npx --no-install tsc --noEmit`, so CI depends on `npm ci` having installed everything. A bundler joins that list on the same terms.
- `adr_004` already wrote the escape clause this slice invokes: it names the migration as sources moving and esbuild bundling `--format=iife`, and states why a module build is refused -- `<script type="module">` is blocked from a page opened from disk by the same policy that blocks fetching a neighbouring JSON. The ADR amendment is exercising a path the ADR itself described, which is worth saying in it.

# Decision framing
- Product framing: Not needed
- Architecture framing: Needed: `adr_004_target_technology_and_process_model` rules out a build step and promises an auto-refresh that was never built; both have to be reopened, together with the served page becoming the default mode.

# Links
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Primary task(s): `task_024_deliver_the_live_viewer_and_the_module_structure`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
