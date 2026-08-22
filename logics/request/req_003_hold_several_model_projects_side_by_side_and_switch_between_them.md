## req_003_hold_several_model_projects_side_by_side_and_switch_between_them - Hold several model projects side by side and switch between them
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 15:00:06

# AI Context
- Summary: One installation currently owns one work directory, so every model an operator opens shares the same reports, identity counter, retention window and viewer page. This separates the installed code from a project's work, makes each namespace per project, and lets the viewer move between projects.
- Keywords: project isolation, work root, code root, identity allocation, parent resolution, prune retention, viewer switcher, migration
- Use when: touching how a path is resolved in the CLI or the engine job, changing identity allocation or fingerprint parentage, scoping retention, or adding project awareness to the viewer.
- Skip when: the change concerns a single operation's geometry, the report schema, or viewer surfaces that do not read a path or a project.

# Needs
- An operator works on more than one model, and today every one of them writes into the same work directory: `manifests.root()` returns the installation directory and nothing overrides it.
- Reports from unrelated models share one identity counter, so the first operation of a second model was allocated `009` instead of `001`.
- The viewer merges unrelated models: every parentless report lands in one outliner group named after whichever model was scanned first, and the operation count in the top bar adds them together.
- `prune --keep` applies its window across every report in the directory, so retention for one model is decided by activity on another.
- Parent resolution matches an operation's input fingerprint against every report on disk, so two projects starting from the same source file can be linked to each other.
- The operator needs to move between projects in the viewer rather than rebuilding a separate page and opening it by hand.

# Context
- `root()` currently answers two different questions with one value: where the code lives (operation manifests such as `tools/voxel_remesh.op.json`, plus `locales/`, `viewer/` and `logics/`) and where the work lives (`work/ops`, `work/in`, `work/renders`, `work/viewer`, `work/doctor.json`).
- The job file handed to the engine carries a single `root`, which the Blender scripts use both to import `meshanvil_engine` and to locate `work/renders`; splitting the roots has to keep both resolvable.
- Identity allocation is an exclusive-create race over the report directory, so scoping it to a project is a matter of which directory is scanned, not of adding a lock.
- The viewer is a static local page over a generated data file and must stay read-only: switching project cannot start a process, fetch, or write.
- The repository is itself a working project today. The demo chain and `tools/build_demo_chain.sh` run against the installation directory and must keep working untouched.

# Acceptance criteria
- AC1: Code location and work location are resolved separately; manifests, locales, viewer sources and Logics documents come from the installation, while reports, sources, renders, the built page and the setup report come from the active project.
- AC2: An operator can create and select a project without editing a file or exporting a variable in every shell, and the command line reports which project it resolved and from where.
- AC3: Identity allocation, parent resolution by fingerprint, and prune retention are each scoped to the active project; the first operation of a new project is `001` and no report of one project can become the parent of another.
- AC4: The viewer offers a project switcher listing the projects that hold reports, and selecting one shows that project's chain, counts and renders without a rebuild, a server, or any write.
- AC5: The viewer names the active project everywhere it currently names a fixed path, and the operation count, branch count and totals describe that project alone.
- AC6: An installation with no project marker keeps behaving exactly as it does today, `tools/build_demo_chain.sh` included, and an existing work directory is readable without a migration step.
- AC7: A source file outside the active project is still accepted as an operation target, and the read-only refusal that protects the sources directory follows the active project.
- AC8: Automated checks cover the split: a run in one project leaves another untouched, identities restart, and the browser smoke exercises the switcher and fails when it is absent.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_004_multi_project_operator_workspaces`
- Architecture decision(s): (none yet)

# References
- meshanvil/manifests.py
- meshanvil/runner.py
- meshanvil/viewer.py
- meshanvil/prune.py
- meshanvil/doctor.py
- meshanvil_engine/views.py
- viewer/index.html
- viewer/viewer.js
- tools/build_demo_chain.sh
- scripts/viewer_smoke.py

# Backlog
- `item_021_split_the_code_root_from_the_work_root`
- `item_022_resolve_the_active_project_without_an_invisible_setting`
- `item_023_scope_identity_parentage_and_retention_to_one_project`
- `item_024_add_a_project_switcher_to_the_viewer`
- `item_025_prove_the_isolation_and_keep_the_current_setup_working`
