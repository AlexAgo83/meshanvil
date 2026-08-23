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
under `work/`, which is not versioned. By default they open no socket, contact no
service, and send nothing anywhere. Two opt-in exceptions deserve attention.

**`meshanvil view --serve`** starts an HTTP server bound to `127.0.0.1`, opt-in and
off unless you pass the flag. It serves `work/` read-only, with directory listings
refused, and it exposes a closed `POST /run` endpoint for exactly three fixed,
argument-free commands (`list`, `doctor`, `prune --dry-run`) plus `POST /file` for
server-owned file ids already named by the current reports. No path or command string
supplied by the page becomes a subprocess argument.

Every request must carry a loopback `Host` matching the port the server actually bound;
a present `Origin` must also be this same loopback server origin. Bad or missing Host
headers and foreign Origins are refused before routes or static files run, which blocks
cross-origin and DNS-rebinding use of the local page. The port may be derived from the
project or chosen by the OS with port 0; either way the check uses the bound socket's
actual port.

`/run` and `/file` also require a random token generated fresh for that server process.
That token proves the request came from the generated page after the origin guard passes;
it is not a secret from local processes because served viewer data is readable from the
served tree and `/api/data`. A missing or mismatched token is refused before an action
starts, and only one command runs at a time. See
`adr_007_let_the_served_viewer_execute_a_closed_command_set` for the full boundary and
why it supersedes `adr_003`'s original refusal to execute anything. `--serve` is meant
for one operator on their own machine; it is not designed to be exposed beyond
`127.0.0.1`.

`run_001` describes a second, unrelated bridge: executing `~/bl_cmd.py` inside a running
Blender session on a half-second poll. Anything that can write that file can run Python in
that session with your user's rights. It is armed by hand, per launch, by pasting one line
into the Python Console — it is not a background service, and it should stay off when you
are not using it.

## What a report contains

An operation report records the path and SHA-256 of what it read and wrote, the parameters it
ran with, and the measurements it took. Paths are the sensitive part: a file name can identify a
client or a programme even when the geometry never leaves the machine. Reports live under
`work/`, which is not versioned, and a report shared outside should be read before it is sent.

## Handling source files

CAD sources are the sensitive part of this kind of work, not the code. `work/` is
git-ignored on purpose, and file names alone can identify a client or a programme. Keep
them out of commits, out of commit messages, and out of runbook examples. `make hygiene`
fails the build if a home path or a personal path reappears in a tracked file.
