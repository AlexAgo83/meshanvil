## item_053_run_the_viewer_s_closed_command_set_through_the_installed_entry_point - Run the viewer's closed command set through the installed entry point
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:48:28

# AI Context
- Summary: The served viewer's closed command set runs through the installed entry point instead of a file inside a checkout, with adr_007's guarantees untouched.
- Keywords: entry point subprocess, closed command set, adr_007 guarantees
- Use when: Changing how the viewer invokes the tool.
- Skip when: Changing which commands the viewer may run.

# Problem
- The served viewer's `/run` endpoint launches a file inside a checkout, which an installed tool does not have.

# Scope
- In:
  - Invoking the installed entry point instead of the checkout file, working identically from a clone.
  - Confirming `adr_007`'s guarantees are untouched by the change.
- Out:
  - Widening the closed command set, or changing any of its members.

# Acceptance criteria
- AC1: The closed command set runs from an installed tool and from a clone, with the same result.
- AC2: The closed set, the token check, the single-flight guard and the refusals are unchanged, and no operator-supplied value reaches a subprocess.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: The closed command set runs from an installed tool and from a clone, with the same result.

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
