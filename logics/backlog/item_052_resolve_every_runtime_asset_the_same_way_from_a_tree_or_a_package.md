## item_052_resolve_every_runtime_asset_the_same_way_from_a_tree_or_a_package - Resolve every runtime asset the same way from a tree or a package
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: High
> Theme: Distribution and installation
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:48:28

# AI Context
- Summary: One repo-first resolution rule replaces the repository-root lookup at every call site, each asset directory is declared in the package, and a build missing one fails.
- Keywords: asset resolution, repo-first fallback, package data, build-time verification
- Use when: Changing where the tool reads manifests, catalogues, viewer sources or the engine package.
- Skip when: Changing what any of those assets contain.

# Problem
- `paths.code_root()` returns the repository root and eleven call sites use it to find manifests, catalogues, viewer sources, the engine package and the runbooks. Installed, that root does not exist.

# Scope
- In:
  - One resolution rule, repo-first with a packaged fallback, replacing the direct use of the repository root at every call site.
  - Declaring each asset directory in the package explicitly, including the client bundle `req_010` introduces.
  - A build-time check that the built package carries every asset the tool reads, failing the build when one is missing.
- Out:
  - Deciding what happens to the runbooks specifically, which has its own slice.
  - Any change to what an asset contains.

# Acceptance criteria
- AC1: One rule resolves every runtime asset and no call site reaches for the repository root directly.
- AC2: The tool finds every asset both from a working tree and from an installed package.
- AC3: A package built without one of its asset directories fails the build with the missing one named.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: One rule resolves every runtime asset and no call site reaches for the repository root directly.
- request-AC4 -> This backlog slice. Proof: AC2: The tool finds every asset both from a working tree and from an installed package.

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
