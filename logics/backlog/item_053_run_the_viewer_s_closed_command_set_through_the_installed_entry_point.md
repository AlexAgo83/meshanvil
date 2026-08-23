## item_053_run_the_viewer_s_closed_command_set_through_the_installed_entry_point - Run the viewer's closed command set through the installed entry point
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Low
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 02:00:17

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
  - Covering the open and reveal actions of `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows` if that slice has already shipped: they launch host processes from the same surface.
- Out:
  - Widening the closed command set, or changing any of its members.

# Acceptance criteria
- AC1: The closed command set runs from an installed tool and from a clone, with the same result.
- AC2: The closed set, the token check, the single-flight guard and the refusals are unchanged, and no operator-supplied value reaches a subprocess.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: The closed command set runs from an installed tool and from a clone, with the same result.

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- The one line: `run_command()` (`meshanvil/viewer.py:116`) runs `[sys.executable, str(paths.code_root() / "bin" / "meshanvil"), *args]` with `cwd=root`. Installed, that file does not exist; `python -m meshanvil` or the console script does.
- `adr_007`'s guarantee lives in the same function and must survive verbatim: the argument list comes from `RUNNABLE` (`meshanvil/viewer.py:20`), the request body only selects a key, and nothing from the page reaches `args`.
- `scripts/selfcheck.py:211` (`check_run_endpoint`) exercises this over a real socket and is the proof the change is behaviour-preserving.
- `scripts/viewer_smoke.py:286` (`check_served`) starts `bin/meshanvil view --serve` by path too -- a second site with the same assumption, in the test harness rather than the product.

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

# Tasks
- `task_025_deliver_an_installable_meshanvil`

# Notes
- Task `task_025_deliver_an_installable_meshanvil` was finished via `logics-manager flow finish task` on 2026-08-23.
