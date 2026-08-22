## item_023_scope_identity_parentage_and_retention_to_one_project - Scope identity, parentage and retention to one project
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:34:51

# AI Context
- Summary: Three namespaces scan the whole report directory: identity allocation, parent resolution by input fingerprint, and prune's retention window. Each has to look at one project only, without weakening the exclusive-create arbitration that keeps two runners in one project apart.
- Keywords: identity allocation, exclusive create, fingerprint parentage, prune retention, namespace scoping
- Use when: touching how an identity is claimed, how a parent is resolved, or how retention decides what to delete.
- Skip when: the change is about what a report contains rather than which reports are considered.
# Problem
- Identity allocation scans the whole report directory, so a second model continued the first model's numbering and took `009` for its first operation.
- Parent resolution matches an input fingerprint against every report on disk, so two projects opened from the same source file would be linked.
- Prune applies its retention window across every report, so one model's activity decides another's artefact deletion.

# Scope
- In:
  - Scope the identity scan, the fingerprint search and the prune window to the active project's report directory.
  - Keep exclusive creation as the arbitration for identity so two runners in one project still cannot collide.
  - Leave already-written reports and their recorded paths untouched.
- Out:
  - Renumbering or rewriting existing reports.
  - Cross-project parentage, even when two projects share a source fingerprint.

# Acceptance criteria
- AC1: The first operation of a project with no reports is `001`, whatever other projects contain.
- AC2: No report in one project resolves as the parent of an operation in another, including when both start from the same source file.
- AC3: Prune considers only the active project's reports and artefacts, and reports what it dropped for that project.
- AC4: Two runners inside one project still cannot claim the same identity.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: The first operation of a project with no reports is `001`, whatever other projects contain.
- request-AC6 -> This backlog slice. Proof: AC2: No report in one project resolves as the parent of an operation in another, including when both start from the same source file.

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
