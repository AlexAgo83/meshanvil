## item_002_run_one_named_operation_from_a_single_agent_agnostic_command - Run one named operation from a single agent-agnostic command
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 95%
> Confidence: 90%
> Progress: 75%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-21 22:29:36

# AI Context
- Summary: One command that resolves the Blender binary, runs a named operation headless on a target file, refuses to write to work/in/, and prints the report path.
- Keywords: runner command, operation discovery, headless invocation, source protection, agent-agnostic
- Use when: Changing how an operation is launched, or what an agent has to know to launch one.
- Skip when: Designing the report contents (item_001) or the viewer (item_003); packaging an MCP server, which this slice excludes.

# Problem
- Running an operation today means knowing the Blender binary path, the -b and -P flags, which file to open and which script to pass.
- That invocation is what every agent has to reconstruct, and it is where a wrong file or a missing copy silently ruins the work.
- Nothing enforces that an operation runs on a copy rather than on a source under work/in/.

# Scope
- In:
  - A meshanvil command taking an operation name and a target file, resolving the Blender binary, running it headless and returning the report path.
  - Operation discovery from pipeline/ and tools/, so adding a script adds an operation without registering it anywhere.
  - A refusal to write to work/in/, with a clear message naming the copy to work on instead.
  - A list mode printing the available operations and what each one needs.
  - The two-process contract of `adr_004_target_technology_and_process_model`: a job JSON written by the host, Blender launched on the operation, the report read back from disk. Nothing parsed out of stdout.
  - Host code in stdlib Python only, importing no bpy; engine-side code importing no host module.
  - The execution contract of `adr_005_execution_contract_identity_concurrency_and_exit_codes`: identity allocated by exclusive file creation, parent resolved by fingerprint, sibling suffixes, one writer per target, exit codes 0/1/2/3, and a progress heartbeat for long operations.
  - An operation manifest declaring each operation's parameters -- name, type, default, unit -- read by the runner to parse the command line and recorded resolved in the report.
  - Engine selection: `blender` or `freecad`, each with its own path override, refused with exit code 2 when missing.
- Out:
  - Chaining several operations in one invocation.
  - Any MCP server or agent plugin packaging, which is its own decision later.
  - Installing or locating Blender for the user beyond an environment variable and the documented default.

# Acceptance criteria
- AC1: One command runs a named operation on a given file and prints the path of the report it wrote.
- AC2: The same command works unchanged whether it is typed by hand or run by an agent; nothing in its interface depends on the runtime.
- AC3: Pointing the command at a file under work/in/ is refused with a message naming what to do instead.
- AC4: The Blender binary comes from an environment variable when set, and from the documented default otherwise.
- AC5: The host process imports no bpy and no third-party package; the operation reads its job from a file and no result is parsed out of stdout.
- AC6: An operation still runs under a bare `blender -b <file> -P <script>` without the runner, reporting to stdout when no job is present.
- AC7: Two runners started at the same moment allocate different identities, proven by creating the report file exclusively rather than counting existing ones.
- AC8: Exit code 0, 1, 2 and 3 each mean exactly one thing, and the last line of stdout is the report path whenever one exists.
- AC9: An operation running for minutes emits progress, and a heartbeat older than sixty seconds is reported as stale.
- AC10: Parameters come from the operation's manifest, and the report records the values actually used, defaults included.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: One command runs a named operation on a given file and prints the path of the report it wrote.
- request-AC8 -> This backlog slice. Proof: AC2: The same command works unchanged whether it is typed by hand or run by an agent; nothing in its interface depends on the runtime.

- request-AC19 -> This backlog slice. Proof: AC8: Exit code 0, 1, 2 and 3 each mean exactly one thing, and the last line of stdout is the report path whenever one exists.
- request-AC20 -> This backlog slice. Proof: AC7: Two runners started at the same moment allocate different identities.
- request-AC21 -> This backlog slice. Proof: AC9: An operation running for minutes emits progress, and a stale heartbeat is reported.

# Decision framing
- Product framing: Not needed
- Architecture framing: `adr_004_target_technology_and_process_model`, `adr_005_execution_contract_identity_concurrency_and_exit_codes`

# Links
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): `adr_004_target_technology_and_process_model`, `adr_005_execution_contract_identity_concurrency_and_exit_codes`
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Primary task(s): `task_001_deliver_the_reviewable_operation_loop`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.
