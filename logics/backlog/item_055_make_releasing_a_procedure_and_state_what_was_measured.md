## item_055_make_releasing_a_procedure_and_state_what_was_measured - Make releasing a procedure and state what was measured
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:48:28

# AI Context
- Summary: The ADR superseding `No publication yet`, plus build, verify and release as commands with a dry run, a measured-platform statement, and a README that leads with the engine requirement.
- Keywords: release procedure, adr_004 supersession, dry run, measured platform matrix, readme install section
- Use when: Deciding or performing how a release is made and described.
- Skip when: Publishing an actual release, which this slice does not do.

# Problem
- `adr_004` records `No publication yet` with no successor, so the channel and its consequences are undecided rather than chosen.
- The platform matrix has Linux unverified, and putting a package on an index is an implicit support claim that nothing currently qualifies.
- The README tells a reader to clone the repository.

# Scope
- In:
  - The decision superseding `No publication yet`: the channel chosen, the channels rejected with their reasons, and what installing does and does not include.
  - Build, verify and release as commands rather than remembered steps, with a dry run that publishes nothing.
  - A release stating the platforms it was measured on and naming the unverified ones.
  - A README installation section leading with the engine requirement, then the install command, keeping the from-a-clone route for contributors.
- Out:
  - Publishing an actual release; this slice delivers the decision and the machinery.
  - Verifying Linux, which needs a machine with an engine on it.

# Acceptance criteria
- AC1: An ADR supersedes `No publication yet` and records the channel, the rejected channels and the scope of an install.
- AC2: Building, verifying and releasing are commands, and the dry run publishes nothing.
- AC3: A release states its measured platforms and names the unverified ones.
- AC4: The README's installation section leads with the engine requirement and keeps the contributor route.

# AC Traceability
- request-AC8 -> This backlog slice. Proof: AC1: An ADR supersedes `No publication yet` and records the channel, the rejected channels and the scope of an install.
- request-AC9 -> This backlog slice. Proof: AC2: Building, verifying and releasing are commands, and the dry run publishes nothing.
- request-AC10 -> This backlog slice. Proof: AC3: A release states its measured platforms and names the unverified ones.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)
- Request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
- Primary task(s): `task_025_deliver_an_installable_meshanvil`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
