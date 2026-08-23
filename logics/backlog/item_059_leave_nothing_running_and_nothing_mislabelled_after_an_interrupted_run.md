## item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run - Leave nothing running and nothing mislabelled after an interrupted run
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 90%
> Complexity: Low
> Theme: Runner and paths
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 10:21:31

# AI Context
- Summary: Kill the engine on the interrupt path before the report is unlinked, and rename the fallback project rule to the directory it actually returns.
- Keywords: leave, nothing, running, mislabelled, after, interrupted, run
- Use when: working on what an interrupted run leaves behind, or on the rule name the doctor command prints.
- Skip when: adding a run timeout or resume, or changing which directory the fallback resolution returns.

# Problem
- runner.run starts the engine with Popen and waits in watch; on any BaseException it unlinks the report and re-raises without terminating the child, so after an interrupt the engine keeps writing to a path that was just removed while the target lock is released and a second run may start alongside it.
- paths.resolve returns the working directory for its fallback but labels it BY_INSTALLATION, while the module docstring says the installation is the project in that case and code_root returns something else.
- That rule is printed to the operator by the doctor command, so the wrong label is on screen.
- doctor.check also writes it as project.resolved_by into work/doctor.json, which the viewer displays and an agent reads, so the rename changes a machine-readable value; item_010's rule that identifiers are never translated applies to the new name.
- scripts/selfcheck.py already asserts on paths.BY_INSTALLATION by constant, so the rename must follow through there even though the assertion still compiles.

# Scope
- In:
  - Holding the Popen handle so it can be terminated in the existing BaseException path before the report is unlinked and the exception re-raised.
  - Stating in the runner's docstring what an interrupt leaves on disk.
  - Renaming the fallback rule to name the directory actually returned, updating the paths module docstring and any locale string that carries the old name.
  - Selfchecks for the terminated child and for the fallback rule name, with pytest wrappers.
- Out:
  - A run timeout, a resume mechanism, or any change to the heartbeat and its stale warning.
  - Changing which directory the fallback returns; only its name and documentation are in scope.
  - The marker and override rules, which already behave as documented.

# Acceptance criteria
- AC1: Interrupting a run terminates the engine process before the runner re-raises, and the runner's docstring says what the interrupt leaves behind.
- AC2: The fallback rule name and the paths module docstring describe the directory that resolve actually returns, and make i18n stays green.

# AC Traceability
> Shared proof: AC7, AC8
- request-AC6 -> This backlog slice. Proof: AC1: Interrupting a run terminates the engine process before the runner re-raises, and the runner's docstring says what the interrupt leaves behind.
- request-AC7 -> This backlog slice. Proof: AC2: The fallback rule name and the paths module docstring describe the directory that resolve actually returns, and make i18n stays green.
- request-AC8 -> This backlog slice. Proof: AC2: The fallback rule name and the paths module docstring describe the directory that resolve actually returns, and make i18n stays green.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)
- Request: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
- Primary task(s): `task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
