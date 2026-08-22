## item_026_ship_the_figurine_subject_as_its_own_demonstration_project - Ship the figurine subject as its own demonstration project
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Low
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 15:13:22

# AI Context
- Summary: The demonstration asset is one file at a fixed path, assumed to be the only one. A second subject needs the same reduction and provenance record, and its own project so it does not take the vehicle's identity numbering or outliner group.
- Keywords: second subject, strip tool, provenance, project isolation, build command
- Use when: adding a demonstration subject or changing how one is prepared and recorded.
- Skip when: the change concerns the chain run on a subject rather than the subject itself.
# Problem
- The demonstration asset today is a single file at a fixed path, assumed to be the only one.
- A second subject needs the same treatment: reduced to what the pipeline reads, with its origin and licence position recorded.
- Two subjects in one work directory collide on identity, grouping and retention.

# Scope
- In:
  - Reduce the subject with the existing strip tool and record its provenance the way the first one is recorded.
  - Give it its own project directory and its own build command.
  - Keep the vehicle demonstration byte-identical in its own project.
- Out:
  - A subject registry, an asset manager or a download step.
  - Shipping a subject whose origin cannot be stated.

# Acceptance criteria
- AC1: The subject ships reduced to geometry, with a provenance record stating where it came from and what is known about its licence.
- AC2: Building either demonstration leaves the other's reports, renders and artefacts unchanged.
- AC3: Each demonstration rebuilds from one command with no argument the operator has to remember.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: The subject ships reduced to geometry, with a provenance record stating where it came from and what is known about its licence.
- request-AC7 -> This backlog slice. Proof: AC2: Building either demonstration leaves the other's reports, renders and artefacts unchanged.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_005_demonstrations_that_show_the_checks_discriminating`
- Architecture decision(s): (none yet)
- Request: `req_004_demonstrate_on_a_clean_organic_subject_what_the_vehicle_chain_cannot_show`
- Primary task(s): `task_018_deliver_the_figurine_demonstration_project`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_018_deliver_the_figurine_demonstration_project`

# Notes
- Task `task_018_deliver_the_figurine_demonstration_project` was finished via `logics-manager flow finish task` on 2026-08-22.
