## item_055_make_releasing_a_procedure_and_state_what_was_measured - Make releasing a procedure and state what was measured
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 75%
> Complexity: Medium
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:49:59

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

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- The sentence to supersede is in `adr_004`'s Decision list: "No publication yet. No PyPI package, no npm package, no installer. The repository is cloned and run. The npm devDependency remains for the corpus tooling only, as `adr_002` decided."
- The measured matrix is in the same ADR and is what AC3 reports: macOS with Blender 5.2 on Python 3.13.13 and host 3.11.15, Windows with Blender 5.2 not on PATH and host 3.10.4, WSL Ubuntu with host 3.14.4 reaching the Windows binary through `/mnt/c`, and Linux unverified with no machine carrying Blender to check it.
- `README.md:140` is the line to rewrite: "Pre-1.0, and no package on an index yet -- clone it, run `./bin/meshanvil`." The engine requirement it must lead with is already stated at `README.md:126`.
- `.github/workflows/ci.yml:22` is `npm ci`, `:23` `make check`, `:24` `make logics`. A release job builds on that, and `make logics` gating the corpus is the precedent for gating the package the same way.
- `logics-manager release status` reports this project as `not_configured` (no `logics/release/contract.json`); `logics-manager release discover --write` produces a draft. That is the corpus side of AC2, separate from building the package itself.

# Decision framing
- Product framing: Not needed
- Architecture framing: Needed: `adr_004_target_technology_and_process_model`'s `No publication yet` has to be superseded with the channel chosen, the channels rejected, and the scope of an install.

# Links
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)
- Request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
- Primary task(s): `task_025_deliver_an_installable_meshanvil`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.
