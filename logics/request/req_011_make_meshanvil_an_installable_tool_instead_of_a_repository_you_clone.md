## req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone - Make meshanvil an installable tool instead of a repository you clone
> From version: 0.1.0
> Schema version: 1.0
> Status: Draft
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:48:27

# AI Context
- Summary: Packages meshanvil so it is installed once and used in any project directory: an entry point, one asset-resolution rule that works from a tree or a wheel, a build that fails when the package is missing part of itself, and the decision superseding adr_004's `No publication yet`.
- Keywords: python index, console entry point, repo-first asset resolution, package data, release procedure, unverified platforms, adr_004 supersession
- Use when: Deciding how meshanvil is obtained, installed, or released.
- Skip when: Deciding what the tool does once it is running.

# Needs
- `adr_004` records `No publication yet. No PyPI package, no npm package, no installer. The repository is cloned and run.` That was the right call pre-1.0 and it is still the state today: the only way to get meshanvil is to clone it and run `./bin/meshanvil`, which asks an operator who wants to prepare a model for printing to first acquire a source tree.
- `bin/meshanvil` reaches its own package by inserting the repository root into `sys.path`. That works only because the entry point sits inside the tree it imports from, so there is no shape in which the tool is installed once and used from anywhere.
- `paths.code_root()` returns the repository root and eleven call sites depend on it to find operation manifests, string catalogues, the viewer's sources, the engine package and the runbooks. Installed rather than cloned, that root does not exist, and every one of those lookups has to come from somewhere else.
- The served viewer's `/run` endpoint launches `code_root()/bin/meshanvil` as a subprocess -- a file path inside a checkout. An installed tool has an entry point, not that file.
- The version is a literal in `meshanvil/__init__.py` with nothing that would keep a package's declared version and it in step.
- `logics_bridge` reads runbooks from `code_root()`, which today is this repository's own `logics/` corpus. What an installed meshanvil should show in its runbook workspace has never been decided, because until now the installation and the corpus were the same directory.

# Context
- Distribution channel: the host is Python 3.10 or later, standard library only, no runtime dependency of any kind. A Python index is the channel that matches what the thing is; an isolated-tool installer gives an isolated environment and a command on PATH without asking the operator to think about virtual environments. npm is not a candidate and `adr_002` already fixed its role -- nothing in the runtime is JavaScript, so shipping through npm would mean either bundling a Python or requiring one anyway.
- The installation-versus-project split in `paths.py` already assumes this shape: one installation serving several project directories, each holding its own reports. The model for an installed tool is written; only the packaging is missing.
- `logics-manager` has already solved the same asset problem and is the reference: a repo-first resolution that prefers the working tree when it looks like one and falls back to the packaged copy otherwise, so a fresh clone runs with no build and a wheel runs from what it carries. Its packaging declares each asset directory explicitly rather than relying on a glob to have caught them.
- The real installation cost is Blender, several gigabytes the operator installs themselves, and `meshanvil doctor` already exists to report it. No distribution choice removes that, which is an argument for the tool's own installation being the trivial part rather than a second obstacle.
- Timing: this should land after `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds` and `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`. That request restructures the client and the host modules and introduces a built client bundle, so packaging before it would package a layout that is about to change and a viewer that cannot refresh itself.
- Honesty about platforms is part of publishing, not separate from it: the measured matrix has Linux unverified, with no machine carrying Blender available to check it. Putting a package on an index is an implicit promise of support, so what is unverified has to be stated where an installer will read it.

# Acceptance criteria
- AC1: The tool is installed from a built package into an environment that is not a checkout, and its command is available on PATH and runs.
- AC2: Installed, the tool has no third-party runtime dependency; installing it pulls nothing but itself.
- AC3: Every asset the tool reads at runtime -- operation manifests, string catalogues, the viewer's sources and its built bundle, the engine package -- is found both from a working tree and from an installed package, resolved by one rule rather than per call site.
- AC4: A built package is verified to actually carry those assets before it can be published; a missing asset fails the build rather than being discovered by an operator at first run.
- AC5: The served viewer runs its closed command set through the installed entry point rather than a file path inside a checkout, with `adr_007`'s guarantees unchanged: the same closed set, the same token, the same single flight, and still no operator-supplied value reaching a subprocess.
- AC6: The package's declared version and the version the tool reports come from one source; they cannot disagree.
- AC7: A decision is recorded on what an installed meshanvil offers in place of this repository's own corpus -- runbooks shipped, absent, or read from the project -- and the runbook workspace matches it rather than failing or showing an empty pane with no explanation.
- AC8: `adr_004`'s `No publication yet` is superseded by a decision recording the channel chosen, the channels rejected and why, and what installing does and does not include.
- AC9: Publishing is a repeatable procedure, not a sequence someone remembers: building, verifying and releasing are commands, and a release states the platforms it was measured on and names the ones that are unverified.
- AC10: The README's installation section describes installing the tool, keeps the from-a-clone route for contributors, and states the Blender requirement before the install command rather than after it.
- AC11: Working from a clone is unchanged for a contributor: `make check` and the smoke suites run against the working tree with nothing installed.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)

# References
- bin/meshanvil
- meshanvil/paths.py
- meshanvil/viewer.py
- meshanvil/i18n.py
- meshanvil/manifests.py
- meshanvil/runner.py
- meshanvil/logics_bridge.py
- meshanvil/__init__.py
- package.json
- Makefile
- README.md
- .github/workflows/ci.yml
- adr_002
- adr_004
- adr_007

# Backlog
- `item_051_declare_the_package_and_give_the_tool_a_real_entry_point`
- `item_052_resolve_every_runtime_asset_the_same_way_from_a_tree_or_a_package`
- `item_053_run_the_viewer_s_closed_command_set_through_the_installed_entry_point`
- `item_054_decide_what_an_installed_meshanvil_offers_in_place_of_this_repository_s_corpus`
- `item_055_make_releasing_a_procedure_and_state_what_was_measured`
