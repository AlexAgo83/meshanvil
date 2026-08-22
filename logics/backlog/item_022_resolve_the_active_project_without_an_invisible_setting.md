## item_022_resolve_the_active_project_without_an_invisible_setting - Resolve the active project without an invisible setting
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: Nothing today depends on the working directory, so a project has to be chosen somehow. A marker walked up from the current directory keeps that choice visible; an environment variable alone would hide where a destructive run lands.
- Keywords: project resolution, marker walk-up, working directory, override, init command, doctor visibility
- Use when: deciding which project a command acts on, creating a project, or surfacing the active project to the operator.
- Skip when: the caller already holds an explicit work root and only needs to use it.
# Problem
- Nothing today depends on the working directory: the tool behaves the same wherever it is launched from.
- An environment variable alone would make the destination of a run invisible, which is the failure mode this project exists to prevent.
- The operator needs to create a project and know which one is active before running anything destructive.

# Scope
- In:
  - Resolve the project by walking up from the working directory for a marker, with an explicit override for non-interactive runs.
  - Add a command that creates the marker and the work directories for a new project.
  - Report the resolved project and how it was resolved in the setup check and on the command line.
- Out:
  - A registry of known projects stored outside the projects themselves.
  - Prompting, interactive selection or shell integration.

# Acceptance criteria
- AC1: Running from inside a project directory resolves that project; running with no marker anywhere above resolves the installation, as today.
- AC2: An explicit override selects a project for one invocation without depending on the working directory.
- AC3: The setup check states which project is active and which rule resolved it, and the viewer's environment panel shows the same.
- AC4: A target file outside the active project is accepted, and the sources directory that is refused as a write target is the active project's.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: Running from inside a project directory resolves that project; running with no marker anywhere above resolves the installation, as today.
- request-AC6 -> This backlog slice. Proof: AC2: An explicit override selects a project for one invocation without depending on the working directory.
- request-AC7 -> This backlog slice. Proof: AC3: The setup check states which project is active and which rule resolved it, and the viewer's environment panel shows the same.

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
