# Security Policy

## Supported Versions

meshanvil is pre-1.0. Fixes target the latest commit on the default branch.

| Version | Supported |
| --- | --- |
| `main` (latest) | Yes |
| older commits | No |

## Reporting a Vulnerability

Please do not open public issues for suspected vulnerabilities.

Use GitHub private vulnerability reporting for this repository:

https://github.com/AlexAgo83/meshanvil/security/advisories/new

Include the affected commit, your platform, your Blender version, and the smallest
reproduction you have.

## What this repository is, in security terms

The scripts here run inside Blender, on 3D files you supply. They read and write only
under `work/`, which is not versioned. They open no socket, contact no service, and send
nothing anywhere.

One exception deserves attention: `run_001` describes a bridge that executes
`~/bl_cmd.py` inside a running Blender session on a half-second poll. Anything that can
write that file can run Python in that session with your user's rights. It is armed by
hand, per launch, by pasting one line into the Python Console — it is not a background
service, and it should stay off when you are not using it.

## Handling source files

CAD sources are the sensitive part of this kind of work, not the code. `work/` is
git-ignored on purpose, and file names alone can identify a client or a programme. Keep
them out of commits, out of commit messages, and out of runbook examples. `make hygiene`
fails the build if a home path or a personal path reappears in a tracked file.
