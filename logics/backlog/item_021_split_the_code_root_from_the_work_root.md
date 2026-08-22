## item_021_split_the_code_root_from_the_work_root - Split the code root from the work root
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:34:51

# AI Context
- Summary: One value answers two questions today: `manifests.root()` locates both the installed code and the operator's work. This separates them and moves every call site to the one it meant, including the job file the engine reads to import its package and place renders.
- Keywords: split, code root, work root, path resolution, job file, engine import, manifests, i18n
- Use when: changing where any path is resolved in the CLI or an engine script, or adding a new directory under the installation or a project.
- Skip when: the change only reads a path already recorded inside a report, or concerns report contents rather than their location.
# Problem
- `manifests.root()` is derived from the module file and is used for both the installed code and the operator's work.
- Roughly fifteen call sites across manifests, runner, viewer, prune, doctor, i18n and logics_bridge mix the two meanings.
- The job file passed to the engine carries one `root`, which the Blender scripts use to import `meshanvil_engine` and to place renders.

# Scope
- In:
  - Introduce a code root and a work root, and move every existing call site to whichever one it actually meant.
  - Carry both roots in the job file so an engine script can import the package and write renders to the right place.
  - Keep the work root defaulting to the code root when nothing else is resolved.
- Out:
  - Choosing or discovering the active project, which is a separate item.
  - Any change to report contents, paths already recorded in reports, or the schema.

# Acceptance criteria
- AC1: Manifest discovery, locale loading, viewer source files and Logics document reads resolve against the installation and keep working when the work root is elsewhere.
- AC2: Reports, sources, renders, the built page and the setup report resolve against the work root.
- AC3: An engine script launched with a work root different from the installation imports `meshanvil_engine` and writes its renders under the work root.
- AC4: With no project resolved, every path is identical to today's.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Manifest discovery, locale loading, viewer source files and Logics document reads resolve against the installation and keep working when the work root is elsewhere.
- request-AC6 -> This backlog slice. Proof: AC2: Reports, sources, renders, the built page and the setup report resolve against the work root.

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
