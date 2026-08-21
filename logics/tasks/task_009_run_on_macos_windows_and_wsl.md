## task_009_run_on_macos_windows_and_wsl - Run on macOS, Windows and WSL
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:57:02

# AI Context
- Summary: Keep discovery and WSL conversion at the engine boundary; platform claims remain limited to the documented measured matrix.
- Keywords: run, macos, windows, wsl
- Use when: Launching a Windows engine from WSL or changing engine discovery.
- Skip when: Adding unsupported Linux claims or operation-specific behavior.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_011_run_on_macos_windows_and_wsl`

# Acceptance criteria
- AC1: The engine is found without configuration on macOS, on Windows and in WSL, and the override is honoured everywhere.
- AC2: With the host in WSL and the engine a Windows binary, an operation runs end to end and its report is readable from the Linux side.
- AC3: A path is never handed to an engine in a form that engine cannot read, proven by running the fixture from WSL on a repository inside the WSL filesystem.
- AC4: A missing engine is refused with exit code 2 and a message naming the override, on every platform.
- AC5: The viewer opens on macOS, Windows and WSL, using explorer.exe on WSL rather than xdg-open.
- AC6: The Python floor matches what the supported platforms carry, and a version below it is refused with a message naming the version found.
- AC7: The documentation states which platforms were verified, on what, and that Linux was not.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_009_run_on_macos_windows_and_wsl.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_009_run_on_macos_windows_and_wsl.md` after implementation.

# Validation
- `make check` (including simulated WSL engine-path conversion)
- README and CONTRIBUTING verified against the measured platform matrix

# Report
- Confirmed the existing discovery, override, refusal, WSL conversion and explorer opener paths; added a WSL boundary self-check.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
