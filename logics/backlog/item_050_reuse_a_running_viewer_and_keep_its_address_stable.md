## item_050_reuse_a_running_viewer_and_keep_its_address_stable - Reuse a running viewer and keep its address stable
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:43:05

# AI Context
- Summary: One viewer per project, reused when it is alive and reclaimed when it is not, at an address that does not move between launches -- and serving becomes what `meshanvil view` does by default.
- Keywords: viewer registry, cross-process lock, liveness probe, stable port, serve by default, stale registration
- Use when: Changing what launching the viewer does, or where it can be reached.
- Skip when: Changing what the viewer serves once it is running.

# Problem
- `meshanvil view` builds and opens a page from disk by default and only serves behind `--serve`, so the one mode that can refresh itself is the one nobody gets unless they ask for it.
- Every launch starts a fresh server on port 0, so the address changes each time: an open tab and a bookmark both go stale, and a second `meshanvil view` starts a second process rather than noticing the first.

# Scope
- In:
  - Making the served page what `meshanvil view` produces by default, with the build-and-open-from-disk mode behind an explicit flag.
  - A per-project registry of the running viewer, guarded across processes, with a liveness probe so a registration outliving its process is reclaimed rather than believed.
  - Reusing a live viewer -- open its address, start nothing -- and saying which of the two happened.
  - A stable address per project across launches, and a clear report when it is already taken by something else.
- Out:
  - Running a viewer as a background service or a daemon; it stays a foreground process the operator started.
  - Serving to anything but the loopback address.
  - Any change to what the viewer serves once it is running.

# Acceptance criteria
- AC1: `meshanvil view` with no flag starts a served page, and the build-and-open-from-disk mode stays reachable behind an explicit flag with today's behaviour.
- AC2: With a viewer already alive for this project, the command opens that one, starts no second process, and states which of the two it did.
- AC3: A project's address is the same across launches.
- AC4: A registration left by a viewer that died is reclaimed, not mistaken for a live one.
- AC5: An address already taken by something that is not this project's viewer is reported clearly and never silently reassigned.
- AC6: Two projects can each have a viewer running at the same time without colliding.

# AC Traceability
- request-AC13 -> This backlog slice. Proof: AC1: `meshanvil view` with no flag starts a served page, and the build-and-open-from-disk mode stays reachable behind an explicit flag with today's behaviour.
- request-AC14 -> This backlog slice. Proof: AC2: With a viewer already alive for this project, the command opens that one, starts no second process, and states which of the two it did.
- request-AC15 -> This backlog slice. Proof: AC3: A project's address is the same across launches.
- request-AC16 -> This backlog slice. Proof: AC4: A registration left by a viewer that died is reclaimed, not mistaken for a live one.

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
- Rationale: The default mode and the moving address are what make the live refresh unusable in practice.

# Notes
- Follows `logics-manager`'s viewer registry module: one live viewer per root, a cross-process lock, and a liveness probe that reclaims a stale registration instead of believing it.
