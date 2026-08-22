## item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision - Build the figurine chain around a sound subject and a size decision
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: Every report in the current demonstration is a defect being found. This chain shows the opposite: a sweep reporting nothing, a size chosen explicitly rather than inherited, and a visibility pass that says nothing is hidden instead of looking blank.
- Keywords: negative control, empty finding, print size, authored size, visibility, deliberate result
- Use when: deciding what the figurine chain runs and how an empty result is presented.
- Skip when: the change is about the voxel branch, which is a separate item.
# Problem
- Every report in the current demonstration is a defect being found, so nothing shows a sweep staying silent.
- The subject is authored at roughly twenty metres tall, which is a scale decision waiting to be made rather than a defect.
- A visibility pass that finds nothing hidden currently reads as an empty result rather than a stated one.

# Scope
- In:
  - Run the defect sweep on the sound subject and keep the empty result as a deliberate step.
  - Set the print size explicitly and record the authored size next to it.
  - Run the visibility pass and keep its nothing-hidden result.
- Out:
  - Running the vehicle's repair steps on a subject that has nothing to repair.
  - Walling a closed body, which hollows it rather than thickening a panel.

# Acceptance criteria
- AC1: The defect sweep reports no finding on this subject, and the viewer shows that as a result rather than a blank panel.
- AC2: The size step states the authored size and the chosen print size, and the chain that follows is measured at the print size.
- AC3: The visibility pass reports that nothing is sealed inside, distinguishable from a pass that was never run.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: The defect sweep reports no finding on this subject, and the viewer shows that as a result rather than a blank panel.
- request-AC3 -> This backlog slice. Proof: AC2: The size step states the authored size and the chosen print size, and the chain that follows is measured at the print size.
- request-AC6 -> This backlog slice. Proof: AC3: The visibility pass reports that nothing is sealed inside, distinguishable from a pass that was never run.

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
