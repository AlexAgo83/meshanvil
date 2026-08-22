## item_051_declare_the_package_and_give_the_tool_a_real_entry_point - Declare the package and give the tool a real entry point
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
- Summary: A package declaration with a console entry point replacing the sys.path insertion, and one source for the version.
- Keywords: package declaration, console entry point, single-sourced version, contributor clone route
- Use when: Making the tool runnable from an install rather than a checkout.
- Skip when: Finding runtime assets, which item_052 owns.

# Problem
- There is no package declaration, and `bin/meshanvil` finds its own package by inserting the repository root into `sys.path` -- which only works because the entry point lives inside the tree it imports.
- The version is a literal in the package with nothing keeping a declared version in step with it.

# Scope
- In:
  - A package declaration with a console entry point calling the existing CLI.
  - Single-sourcing the version so the declared one and the reported one cannot diverge.
  - Keeping `bin/meshanvil` working from a clone for contributors.
- Out:
  - Asset resolution, which the next slice owns.
  - Publishing anything to an index.

# Acceptance criteria
- AC1: Installing the built package into a clean environment puts a working command on PATH.
- AC2: The install pulls no third-party runtime dependency.
- AC3: The declared version and the reported version come from one source.
- AC4: `./bin/meshanvil` still runs from a clone with nothing installed.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Installing the built package into a clean environment puts a working command on PATH.
- request-AC2 -> This backlog slice. Proof: AC2: The install pulls no third-party runtime dependency.
- request-AC6 -> This backlog slice. Proof: AC3: The declared version and the reported version come from one source.
- request-AC11 -> This backlog slice. Proof: AC4: `./bin/meshanvil` still runs from a clone with nothing installed.

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- `bin/meshanvil` is 12 lines: a Python floor check (3.10), `sys.path.insert(0, parent.parent)`, then `from meshanvil.cli import main`. The entry point is `meshanvil.cli:main`, which already returns an exit code -- nothing about the CLI needs to change for a console script to call it.
- The version literal is `VERSION = "0.1.0"` in `meshanvil/__init__.py:6`, next to `SCHEMA_VERSION = 1`. It reaches the page through the payload (`meshanvil/viewer.py:96`) and is asserted by the smoke suite as `/^v\d+\.\d+\.\d+$/` (`scripts/viewer_smoke.py:115`), so a change of source has a visible consumer.
- `package.json` already declares `"version": "0.1.0"` independently -- a third place, and today nothing keeps the three in step.
- Nothing in `meshanvil/` imports anything outside the standard library; the runtime-dependency claim is checkable, not aspirational.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)
- Request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
- Primary task(s): `task_025_deliver_an_installable_meshanvil`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
