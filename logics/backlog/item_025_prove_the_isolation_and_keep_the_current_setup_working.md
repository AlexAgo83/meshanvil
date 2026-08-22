## item_025_prove_the_isolation_and_keep_the_current_setup_working - Prove the isolation and keep the current setup working
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: Isolation that is not asserted is lost the first time a path constant moves. Two projects must be run against each other in the self-check, and the browser smoke must fail when the switcher is gone, while the demo chain keeps running unchanged against the installation.
- Keywords: isolation test, self-check, browser smoke, regression guard, backwards compatibility, demo chain
- Use when: adding or changing coverage for path resolution, project isolation, or the viewer switcher.
- Skip when: the change is a product behaviour with no path or project dimension.
# Problem
- Isolation that is not asserted will be lost the first time a path constant is touched.
- The repository is itself a working project and its demo chain must survive the split.
- The existing browser smoke would pass whether or not a switcher exists.

# Scope
- In:
  - Assert that a run in one project leaves another project's reports, renders and artefacts unchanged.
  - Assert that identities restart and that parentage does not cross projects.
  - Exercise the switcher in the browser smoke and fail when it is missing.
  - Keep `tools/build_demo_chain.sh` and the fixture check running against the installation with no argument change.
- Out:
  - A performance or scale benchmark over many projects.
  - New test dependencies when the existing self-check and smoke paths are enough.

# Acceptance criteria
- AC1: One self-check run creates two projects, runs in each, and fails if either one's reports, renders or artefacts changed because of the other.
- AC2: The self-check asserts the first identity of a fresh project is `001` and that no parent link crosses projects.
- AC3: The browser smoke fails when the project switcher is absent, and passes with one project without requiring a second.
- AC4: The demo chain script and the fixture check run unchanged against the installation and still produce their current reports.

# AC Traceability
- request-AC6 -> This backlog slice. Proof: AC1: One self-check run creates two projects, runs in each, and fails if either one's reports, renders or artefacts changed because of the other.
- request-AC8 -> This backlog slice. Proof: AC2: The self-check asserts the first identity of a fresh project is `001` and that no parent link crosses projects.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_004_multi_project_operator_workspaces`
- Architecture decision(s): (none yet)
- Request: `req_003_hold_several_model_projects_side_by_side_and_switch_between_them`
- Primary task(s): `task_017_deliver_multi_project_workspaces_and_the_viewer_switcher`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
