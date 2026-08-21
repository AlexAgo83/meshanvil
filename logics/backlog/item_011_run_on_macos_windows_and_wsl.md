## item_011_run_on_macos_windows_and_wsl - Run on macOS, Windows and WSL
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 95%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 00:57:02

# AI Context
- Summary: One tool on macOS, Windows and WSL, with the engine located per platform, paths translated when the two sides of WSL disagree, and Linux stated as unverified rather than claimed.
- Keywords: cross-platform, WSL, path translation, engine discovery, Python floor
- Use when: Touching how the engine is found or launched, or how a path crosses a platform boundary.
- Skip when: Working on what an operation measures, which is platform-independent.

# Problem
- The tool assumes macOS: the documented Blender path is an application bundle, and nothing else was ever tried.
- Measured on the operator's own machines, the assumptions do not hold. On Windows, Blender 5.2 is installed but not on PATH, and the system Python is 3.10.4 -- below the 3.11 floor adr_004 declared. In WSL Ubuntu the Python is 3.14.4 and there is no Linux Blender at all: only the Windows binary is reachable, through /mnt/c.
- WSL is the case that actually bites. Running the Windows binary from WSL works -- verified, with the script on C: and with the script inside the WSL filesystem through a \\wsl.localhost UNC path, Blender reporting Python 3.13.13 in both -- but every path handed to it must be a Windows path, and every path it writes must be read back on the Linux side.
- Opening the viewer differs per platform, and the usual assumption is wrong on WSL: wslview is absent, xdg-open exists but has no browser behind it, and explorer.exe is what actually works.
- Linux has no datapoint. The second machine available carries no Blender at all, so nothing about Linux has been verified.

# Scope
- In:
  - Engine discovery per platform: the macOS bundle, the Windows install directory, a binary on PATH, each overridable by MESHANVIL_BLENDER and MESHANVIL_FREECAD.
  - A refusal that names the override when no engine is found, with exit code 2 as adr_005 requires.
  - Path translation at the boundary: when the host runs in WSL and the engine is a Windows binary, every path in the job is converted with wslpath before the engine sees it, and converted back when read.
  - Opening the viewer per platform: the system opener on macOS and Linux, explorer.exe on WSL.
  - A Python floor set to what the platforms actually carry, checked at startup with a message naming the version found.
  - The measured matrix recorded where a contributor will find it, including what is unverified.
- Out:
  - Linux support claimed as verified. It is written as unverified until a machine with Blender exists to run the fixture on.
  - Installing an engine, or shipping one.
  - Windows-native make targets. make is for contributors; the tool itself runs from the command entry point.
  - Network paths, mapped drives, and anything under a UNC root other than the WSL one.

# Acceptance criteria
- AC1: The engine is found without configuration on macOS, on Windows and in WSL, and the override is honoured everywhere.
- AC2: With the host in WSL and the engine a Windows binary, an operation runs end to end and its report is readable from the Linux side.
- AC3: A path is never handed to an engine in a form that engine cannot read, proven by running the fixture from WSL on a repository inside the WSL filesystem.
- AC4: A missing engine is refused with exit code 2 and a message naming the override, on every platform.
- AC5: The viewer opens on macOS, Windows and WSL, using explorer.exe on WSL rather than xdg-open.
- AC6: The Python floor matches what the supported platforms carry, and a version below it is refused with a message naming the version found.
- AC7: The documentation states which platforms were verified, on what, and that Linux was not.

# AC Traceability
- request-AC23 -> This backlog slice. Proof: AC2: With the host in WSL and the engine a Windows binary, an operation runs end to end and its report is readable from the Linux side.
- request-AC19 -> This backlog slice, partially. Proof: AC4: A missing engine is refused with exit code 2 and a message naming the override.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_004_target_technology_and_process_model`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_004_target_technology_and_process_model`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.

# Tasks
- `task_009_run_on_macos_windows_and_wsl`
