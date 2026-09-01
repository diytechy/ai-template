#!/usr/bin/env python3
"""Validate the work-item registry — stdlib only.

The registry home is the spec folder `docs/work/` (one file per work item,
status = directory; the CSV home retired at concurrency-restructure Phase 5,
RULING-4). Every rule below reads the same 18-key rows `read_registry_rows`
emits. A stray resurrected `work-items.csv` is itself an integrity ERROR here
— a second, unread encoding of the registry — which is the difference between
this copy of the reader and the scheduler's silent one.

The `SN->SR->LLR->TC` spine answers *what must be true*. A **work item**
(`WI-###`) decomposes *how the work executes*: it delivers SR(s), belongs to a
**workstream** (a mutable grouping category — the legacy `Track` header is still
read), and depends on **predecessor** work items (the DAG edges), moving
`queued -> active -> done`. This is the validation half of the trajectory layer;
the offline dashboard that renders the same registry is generated separately (a
*view*, never a source of truth — the `trace.py` / `gen_arch_map.py` idiom).

Checks (integrity, in the spirit of `trace.py`):
  - `WI-###` id shape + uniqueness — a malformed or duplicated id is an ERROR.
  - every `Predecessors` id resolves to a real work item — an ERROR (a DAG edge
    to a work item that does not exist).
  - the work-item graph is ACYCLIC over its **hard** edges — a cycle is an
    ERROR (a trajectory that depends on itself can never start).
  - a predecessor may be marked **soft** with a `~` prefix (`~WI-013`): an
    advisory-ordering hint, not a blocker. A soft edge must still resolve
    (ERROR if not), but it is excluded from the cycle rule — a cycle that
    exists only through soft edges is a WARN (conflicting hints), never an
    error — and it never constrains readiness.
  - every `SR-Refs` id exists in `system-requirements.toml` — a WARN, not a
    failure (a draft SR referenced ahead of its registry row is legitimate).
  - an OPEN work item's `Title` over `_TITLE_CONCISE_MAX` characters is a WARN,
    never a failure and never a suggestion to reword what is already filed
    (repo-review 2026-08-19 M-03): a Title is a UI label everywhere the
    dashboard renders it, so keep it a concise name and put the rationale in
    the body. Closed rows are excluded (a historical record); findings are
    summarised, not one line per row.

**The registry SSOT rules** (S1; process-options.md "Trajectory /
work-items layer"). The WI `Deliverable` is **backward-only** (what shipped) and
the per-WI `SpecRef` is the forward bridge that lives while the WI is open and
clears at close. Cross-reading the `docs/work/` registry and its SpecRefs
mechanizes two rules:
  - **R-A** — a WI's `Deliverable` is non-empty **iff** its `Status` is
    **terminal** (`done` or `cancelled`; WI-267). An open (draft/queued/active/deferred)
    WI with a filled Deliverable, or a terminal WI with an empty one, is a hard
    **ERROR at every run** (no flag needed): a commit is the agent handoff point,
    so an incoherent WI state launches the next session wrong. (`done` records
    what shipped; `cancelled` records why it never will.)
  - **R-E** — every open WI carries a non-empty `SpecRef` resolving to an in-repo
    target (`path` or `path#anchor`; the path part must exist). A terminal WI is
    exempt (its SpecRef is cleared — R-F).
  - **R-F** (WI-251; WI-267) — the close side R-E leaves unstated: a **terminal**
    (`done`/`cancelled`) WI's `SpecRef` is **empty**, and every live `docs/specs/`
    file (scaffold README/`-000` boilerplate excluded) is cited by at least one
    *open* WI — otherwise it belongs in `docs/archive/specs/` (the specs README
    lifecycle).
R-E and R-F are **WARN by default, ERROR under `--strict`** (wired at DevStg-Tests+). R-B/R-C —
every *open* WI repeated as a token in `status.md` — stay **retired** (WI-180):
status becomes an integrator-generated snapshot, so open-id currency is enforced
by generated freshness, not by copying the registry back into prose. **R-D is
RESTORED, mode-aware (WI-200):** `status.md` is forward-only, so a `done` WI id
lingering there is a finding — WARN plain, ERROR under `--strict` — *except* when
the file carries the kit's generated-block marker (`<!-- BEGIN GENERATED ... -->`,
the `gen_arch_map`/`gen_trajectory` idiom), where it is an integrator snapshot
that cannot accrete prose and the successor freshness check applies. IMPLEMENTED
since WI-234 — `status_forward_only_findings` below, and the stand-down is scoped
to the marked block, not the whole file. `--staged` adds the warn-first **no-validation-delta** checks: the
follow-up-on-a-done-SR ratchet, the **critique-loop ratchet** (WI-068) — a WI
closing on a `Verification=Critique` SR while the latest `docs/reviews/*-CRITIQUE.md`
verdict is CHANGES-REQUESTED, without the staged set touching the TC registry, the
tests dir, or a `docs/rubrics/` file (harden the TC or add a rubric anchor) — and
the **amend-without-flip** warn (WI-316): a staged diff changing the **approved**
cells of an `Approved` spine row without re-blessing it in the same commit
(process.md §7), the write-time discipline commit-message prose never had.
*Approved*, not every cell — the §A5.1 cell split (owner ruling 2026-07-31;
WI-380) rules traceability **traced, not approved**, so a `Module`/`CodeSymbol`/
`TestRefs`/`SN-Refs`/`Verifies` pointer following code that moved does **not**
arm the marker. The traced half is not discarded: it is carried structurally by
`staged_spine_amendments`, which returns both halves per amended row.

**Opt-out and vacuous by default** — the posture of the always-on
`secrets_scan` floor. The check is on unless `docs/process.toml` `[checks]
trajectory_check` reads `false` (or, for the SN-028 migration window, the
legacy `docs/trajectory-check` reads the one word `off`); and an *absent* or *placeholder-only* registry (nothing but
the inert `WI-000` example row) passes vacuously. So a fresh scaffold and a repo
that never adopts the layer both stay green for free — WI is an off-spine
optional registry, like procurement / assets, whose placeholder never blocks a
gate (`trace.py` does not read WI ids at all).

**Architecture-connectivity coverage** (S5/WI-056; process.md §8). This step is
also the views-checker for the interface layer: every module in the arch-map
inventory (`docs/architecture.md`'s generated block) should appear as ≥1 IF-###
endpoint, and a `Contracts: IF-###` docstring citation should match the
registry — both stay **warn-first forever** (never the exit code, at any gate)
and print at the hook. The ruled posture is **opt-out, default-on**: the
coverage warn fires even when `interfaces.csv` is empty or absent — a
multi-module arch-map with no declared seams reads "connectivity undeclared"
instead of passing vacuously. Silenced only by `[checks] interfaces_check =
false`, or a ≤1-module inventory (nothing to connect). The honesty valve for a
deliberate source/sink is a `source`/`sink` token in that module's IF row Notes
(below).

**Seam-TC coverage — WARN plain, ERROR under `--strict` (DevStg-Tests+) since
WI-488 (OI-43 ruled (a)).** Every declared IF seam should be cited by a TC
(`interface_findings` still reports the total uncited count, informationally,
warn-first at every gate); `if_tc_coverage_findings` is the promotable half — it
reports only the seams NOT on the migration allowlist `docs/if-tc-coverage-allow`
(seeded at the population measured when the ruling executed, with a declared
burn-down expectation — never a permanent exemption). Shares the
`interfaces_check` opt-out; `if_tc_allow_hygiene_findings` reports (never
blocks) an allowlist entry that has gone stale (its seam gained a TC, or its id
no longer resolves), so the burn-down is visible rather than silently absorbed.

**How-SW top-view right-sizing** (WI-073/FB5; process-options.md "Component
layer"). The software-architecture diagram's *first view* must show at most
``TOP_VIEW_MAX`` (10) items: top-level components (a `CMP-###` with no `PartOf`
that contains ≥1 arch-map module) plus **uncontained** modules (a module with no
`Component`-tagged LLR). Exceeding the bound is a **finding** — WARN at the
plain/hook run, **ERROR under `--strict` (DevStg-Tests+)** — that drives right-sizing of
the component designations. Membership derives from the AXES join: a `Component`
tag on an LLR row joins its `Module` → `CMP-###`; nesting via the CMP registry's
`PartOf` (a module counts only at its top-level root). Opt-out is the one word
`[checks] components_check = false` (the `interfaces_check` idiom); a repo with ≤10
modules — or no arch-map inventory — passes trivially (the bound, not the
registry, is the rule), so a small or non-adopting repo is never broken.

**Knowledge⇒component coupling** (WI-153; research-knowledge.md §3a, owner-ruled
2026-07-14). The same finding is *armed independent of the bound* once
`docs/knowledge/` holds a real pack: an uncontained arch-map module is then a
finding even below the 10-item bound, because a knowledge pack ties the *what* to
the knowledge behind the *how*, so that web must be robust wherever packs are
enabled. It reuses the existing `Component`-tag join (no new join) and the same
`components_check` opt-out, and is dormant — costing a non-adopter nothing —
until a pack (any `docs/knowledge/*.md` but the `README.md` index) exists.

**Phase archetype + phase-drop detector** (WI-093; derived-gate model §7/§9.3;
re-keyed to the stage axis by WI-498 slice 4). A phase's pre-dev batch is a
first-class WI whose Title carries a phase-anchor tag recording the LADDER RUNG
the phase stands at once it closes (`[v2]-[DevStg-LLReqs]` = requirement
structuring, `[v2]-[DevStg-Impl]` = decomposition + TCs; the retired
`[v2]-[reqs|tests|g1|g2]` spellings are translated on read, never authored).
This step recognizes those anchors and, reading the LIVE per-phase stage through
the common reader (`derive_stage.read` over `docs/stage`), warns when a phase has
**dropped below** the reach its own closed anchor recorded — the signal that new
or reopened content entered and a new phase-anchor WI is due. It ABSTAINS where a
phase's reading is a repo-global rung (`kitlib.stage.REPO_GLOBAL_RUNGS`), saying
so once rather than going silently vacuous. All **warn-first** (never an
exit-code change, at any stage); vacuous on a single-phase repo with no anchors
(the meta case) or where the stage axis cannot be read.

Usage:  python scripts/check_trajectory.py [--root .] [--strict] [--staged]
Exit codes: 0 clean / vacuous / opted-out, 1 a hard error, 2 usage/environment.

Contracts: IF-009, IF-056, IF-082, IF-083, IF-084, IF-138 — the interface seams
this module declares (process.md §8; rows of record in
docs/requirements/interfaces.toml).

Contract IF-009: the work-item registry's verdict, delivered as a CLI. Exit 0 when
    the registry is clean, absent, placeholder-only or opted out; 1 on a hard
    integrity error — a malformed or duplicated `WI-###`, a predecessor that
    resolves to nothing, a cycle over the hard edges, a stray `work-items.csv`,
    or a `Deliverable` that disagrees with `Status` (R-A); 2 on usage or
    environment. R-A gates every run. R-D, R-E, R-F, the promotable seam-TC
    coverage half and the How-SW top-view bound are WARN plain and ERROR under
    `--strict`. Architecture-connectivity coverage, allowlist hygiene, the
    soft-edge cycle warn, the long-Title warn and the phase-drop detector are
    advisory at every stage and never reach the exit code.
Contract IF-056: the derivation-loader surface the dashboard renders THROUGH.
    `gen_trajectory` imports this module and takes `validate`,
    `read_registry_rows`, `load_wis`, `load_known_srs`,
    `read_trajectory_enabled`, `WI_CSV` and `TOP_VIEW_MAX` from it, so the
    registry parse, the validity verdict and the right-sizing bound have one
    home and the render can never disagree with the check. The loaders are
    importable without side effects and the two modules are re-synced together.
Contract IF-082: the same loader surface as taken by `traj_parse`, the dashboard's
    registry/doc/git source layer: `read_rows`, `spine_carrier`, `SR_CSV` and
    `_arch_scan_profile` — the declared source-root profile the How-SW scan
    walks. One parse of the spine registries feeds both validation and the view.
Contract IF-083: the same loader surface as taken by `traj_views`, the
    What/When/How-SW renderer: `read_rows`, `load_seams`, `component_top_view`,
    `_norm_module`, `_split_refs`, `SR_CSV` and `TOP_VIEW_MAX`. The picture and
    the top-view bound this module enforces are computed by one join, so a
    diagram that renders cannot contradict the finding that would fail it.
Contract IF-084: the same loader surface as taken by `traj_status`, the `--status`
    snapshot layer: `load_ifs`, `IF_CSV` and `spine_carrier`. The seam rows the
    generated status block reports are the rows validation reads.
Contract IF-138: the same loader surface as taken by `pending`, the blocked-work
    read model: `read_registry_rows`, `load_wis` and `WI_CSV`. What the owner
    surfaces call blocked is the derivation validation performs, never a second
    opinion about the same rows.
"""

import argparse
import ast
import configparser
import difflib
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# THE SHIPPED SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`, executed
# WI-448): one home for behaviours this module used to spell out itself — the
# declared-policy line reader and the `docs/work/` spec-folder registry reader.
# It replaces the F5 rule, which had licensed those copies unbounded and left
# `tests/test_rule_sync.py` pinning them equal by value. Run as a subprocess
# this script's own dir is sys.path[0] so a plain import resolves; the guard
# covers an in-process import (a test) whose sys.path does not yet carry
# scripts/ — the same sanctioned-sibling idiom the engines use for each other.
try:
    from kitlib import config as _kitconfig
    from kitlib import git as _kitgit
    from kitlib import ladder as _kitladder
    from kitlib import registry as _kitregistry
    from kitlib import spine as _kitspine
    from kitlib import stage as _kitstage
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import config as _kitconfig
    from kitlib import git as _kitgit
    from kitlib import ladder as _kitladder
    from kitlib import registry as _kitregistry
    from kitlib import spine as _kitspine
    from kitlib import stage as _kitstage

# Sibling: the spine's registry carrier. Run as a
# subprocess this script's own dir is sys.path[0] so a plain import resolves;
# the guard covers an in-process import (a test) whose sys.path does not yet
# carry scripts/ — the same sanctioned-sibling idiom trace.py uses for
# trace_text.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# Sibling: THE ACCEPTANCE RECORD (WI-521 slice 1) — the two-tree spine
# comparison and the snapshot mirror, which used to live in this file. Required,
# not optional like `gen_arch_map` below: its findings join the failure set at
# `main`'s aggregation, so a copy of this checker without it would silently stop
# reporting that attested text had drifted, which is the opposite of a vacuity.
# `bootstrap.MAPPING` carries it, so a scaffold gets both or neither.
try:
    import acceptance_record
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import acceptance_record

# Sibling: the arch-map AST walk (`gen_arch_map.scan_inventory`) —
# `arch_inventory`'s source since WI-455 retired the committed
# docs/architecture.md block it used to parse back. OPTIONAL like traj_parse's
# schedule import: a fixture that copies check_trajectory.py alone (the
# hook-scaffold tests) simply has no inventory, which is the same vacuity the
# absent committed map produced before.
try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None

WI_CSV = "docs/requirements/work-items.csv"
# The spec-folder home the CSV above gives way to (Phase 2b of
# docs/concurrency-restructure.md). Declared as a repo-relative POSIX path
# because the git plumbing below passes it as a PATHSPEC; the reader derives
# the same folder from the CSV path via `spec_work_dir`.
WI_WORK = "docs/work"
# Terminal history's home since WI-504 (OI-55 ruled (a)): `complete/`,
# `cancelled/`, `partial/` moved one directory deeper, under the archive. HEAD
# tree reads that must recognise a terminal status (`_head_spec_status_map`)
# scan both prefixes; the CSV-era readers above stay unchanged because they
# already delegate to `kitlib.registry.read_spec_rows`, which unions the two
# roots itself (`spec_roots`).
WI_ARCHIVE_WORK = "docs/archive/work"
SR_CSV = "docs/requirements/system-requirements.toml"
TC_CSV = "docs/test/test-cases.toml"
IF_CSV = "docs/requirements/interfaces.toml"
LLR_CSV = "docs/requirements/low-level-requirements.toml"
CMP_CSV = "docs/requirements/components.toml"
SPECS_DIR = "docs/specs"
# Where R-F sends a spec at close ("close date appended, WI ids noted"), so the
# WI-352 reconciler can still find a terminal WI's spec after its SpecRef clears.
ARCHIVE_SPECS_DIR = "docs/archive/specs"
STATUS_MD = "docs/status.md"

# The How-SW top view is bounded at this many items (top-level components +
# uncontained modules); exceeding it drives right-sizing of the component
# designations (WI-073, FB5 — warn plain, error --strict).
TOP_VIEW_MAX = 10

# An IF-### interface-seam id token (process.md §8). Matched word-bounded so a
# `Contracts: IF-003, IF-004` docstring line (harvested into the arch-map) or an
# id cell yields each id cleanly.
IF_ID_RE = re.compile(r"IF-\d+")

# The declared shared-kernel surface (OI-48 ruled (d), WI-494) — see
# `read_kernel_modules`. The reuse provision's home: a small declared file,
# consistent with the `docs/*-allow` idiom `provenance-allow` and
# `if-tc-coverage-allow` already established, over a `[checks]`-side list —
# a per-entry recorded REASON is the point, and `docs/process.toml` carries
# dials, not reasoned prose.
KERNEL_ALLOW = "docs/kernel-modules-allow"
KERNEL_ALLOW_SEP = " — "

# The seam-TC coverage migration allowlist (OI-43 ruled (a), WI-488) — see
# `read_if_tc_allow`.
IF_TC_ALLOW = "docs/if-tc-coverage-allow"
# The allowlist's machine-readable baseline: how many of its entries are the
# SEEDED population (which shares one reason, stated once in the header). Past
# that count an entry is an addition and must carry its own ` — <reason>`.
IF_TC_SEED_RE = re.compile(r"^#\s*seed-count:\s*(\d+)\s*$")
# A CMP-### component id token (process-options.md "Component layer"). trace.py
# owns CMP integrity; this loader is lenient (skips a malformed id) — it only
# feeds the warn-first top-view coverage.
CMP_ID_RE = re.compile(r"^CMP-\d+$")

# A well-formed work-item id: `WI-` then digits (`WI-001`). The `-000` example
# row matches this shape but is inert (skipped from the graph — see load_wis).
WI_ID_RE = re.compile(r"^WI-\d+$")

# The work-item lifecycle vocabulary (S1). `draft` is thinking-in-progress — the
# ABSENCE of a decision (WI-384); `deferred` is a first-class, queued-but-not-next
# state carrying the decision's recorded reason; `blocked` is parked on a
# named external dependency. `cancelled` (WI-267, spelled `retired` until WI-384)
# is a TERMINAL won't-build row that
# stays in the registry forever with its reason in the `Deliverable` column — a
# deliberate dead-end, NOT an overload of `done` (a `done` WI shipped something; a
# `cancelled` WI deliberately never will). Since Phase 5 status is the spec's
# DIRECTORY (an unknown one is a loader refusal) and `blocked` is DERIVED
# (queued + blockref) rather than a status; the literal stays in these sets so
# in-memory callers keep their meaning, but no loader can produce it.
# "Open" = anything still in flight (not one of the two TERMINAL states).
OPEN_STATUSES = ("draft", "queued", "active", "deferred", "blocked")
# The terminal states: no further build/trace work is owed. Both require a filled
# `Deliverable` (the shipped record for `done`; the cancellation reason for
# `cancelled`) and both must clear their `SpecRef` (R-A + R-F below). `cancelled`
# is deliberately NOT in OPEN_STATUSES / BACKLOG_STALE_STATUSES / the frontier.
TERMINAL_STATUSES = ("done", "cancelled", "partial")

# Backlog-staleness (WI-205) applies to genuinely-in-flight WIs: the open set
# minus `deferred` and `draft` (both re-enter via an owner look — an un-defer, or
# the thinking finishing — which is itself the driven review, so both are
# EXEMPT), plus `blocked` (a WI parked on an external
# dependency is still live work whose cited requirements can drift under it).
# `done`/`cancelled` are terminal and need no re-validation.
BACKLOG_STALE_STATUSES = ("queued", "active", "blocked")

# WI-479 (repo-review 2026-08-19 M-03): a WI Title is a UI label everywhere the
# dashboard renders it — the landing hero's active-work line, the Next-work
# card — and both already clip/disclose past ~140 raw characters rather than
# trust the registry to stay short (gen_trajectory's `_NEXT_WORK_TITLE`). This
# bound is the OTHER half: nudge a Title toward concise AT THE SOURCE, without
# ever failing a gate or asking anyone to reword what is already filed — ten of
# the eleven live (open) titles measured at this WI's filing were multi-sentence
# program narratives, so a validation-only fix would have forced a mass reword
# of owner-authored text. Set a shade under the dashboard's own bound so the
# advisory fires before a reader ever meets the clipped render.
_TITLE_CONCISE_MAX = 120

# The clause both backlog-staleness warns end with. The clock it must clear
# reads the WI's OWN registry spec under docs/work/ (`_spec_row_times`), never
# the SpecRef target — editing the cited doc pushes ITS clock further ahead and
# can never clear the warn. It names the SAME FILENAME because "any reviewed
# edit re-affirms" is false for a Title edit: the Title drives the spec
# filename, and the row clock filters renames out on purpose
# (`_path_commit_time`, row-history mode), so a re-title does not re-date the
# row even when the same commit changed content. WI-362.
BACKLOG_REAFFIRM_HINT = (
    "re-validate the WI against the amended requirement (or re-affirm with a "
    "content edit to the WI's own spec file under docs/work/, keeping its "
    "filename: editing the Title renames the file, and a rename does not "
    "re-date the clock)"
)


# The first non-empty, non-comment line of a declared-policy file, or None
# (absent/empty) — the parse every kit reader shares (hooks, check_privacy.py,
# agent_loop.py). ONE HOME since WI-448: this was one of FIVE literal copies of
# that rule, and `tests/test_rule_sync.py` had to pin them equal by value
# because D-7's F5 ruling licensed the duplication rather than removing it.
# Kept under its own long-standing private name so no call site below moves.
_first_declared_line = _kitconfig.first_declared_line


# One `[checks]` toggle out of `docs/process.toml`, or None when that file has
# nothing to say (fall through to the legacy one-word dial). ONE HOME since
# WI-448 slice 4, and the copy's own stated reason for existing did not describe
# it: this docstring used to argue that the shared package owned the declared-
# LINE rule but not "this module's `[checks]` POLICY — which key, which
# fail-direction, which residual". Only the key is this module's, and it is a
# PARAMETER; the fail-direction and the residual were hardcoded identically in
# `gen_okf.py`'s copy, so nothing module-specific was being encoded and the
# `tests/test_rule_sync.py` equality pin was holding two identical bodies equal.
# Kept under its own long-standing private name so no call site below moves.
_process_check = _kitconfig.process_check


def read_trajectory_enabled(root):
    """Whether the trajectory check is on. `docs/process.toml` `[checks]
    trajectory_check = false` opts out; else (migration window)
    `docs/trajectory-check` with the one word `off`; absent or any other value
    reads on (the safe default), so an ordinary repo runs it without declaring
    anything — opt-out, like `docs/secrets-scan`."""
    declared = _process_check(root, "trajectory_check")
    if declared is not None:
        return declared
    return (
        _first_declared_line(root / "docs" / "trajectory-check") or ""
    ).lower() != "off"


def read_interfaces_check_enabled(root):
    """Whether the architecture-connectivity coverage warns are on (S5/WI-056).
    `docs/process.toml` `[checks] interfaces_check = false` opts out; else
    (migration window) `docs/interfaces-check` with the one word `off`; absent
    or any other value reads on — the ruled opt-out, default-on posture (same
    shape as `trajectory_check`). Default-on means the coverage warn fires even
    with an empty/absent `interfaces.csv`; the off-switch or a ≤1-module
    inventory is the only silence."""
    declared = _process_check(root, "interfaces_check")
    if declared is not None:
        return declared
    return (
        _first_declared_line(root / "docs" / "interfaces-check") or ""
    ).lower() != "off"


def read_components_check_enabled(root):
    """Whether the How-SW top-view right-sizing rule is on (WI-073/FB5).
    `docs/process.toml` `[checks] components_check = false` opts out; else
    (migration window) `docs/components-check` with the one word `off`; absent
    or any other value reads on — the ruled opt-out, default-on posture (same
    shape as `interfaces_check`)."""
    declared = _process_check(root, "components_check")
    if declared is not None:
        return declared
    return (
        _first_declared_line(root / "docs" / "components-check") or ""
    ).lower() != "off"


# Ref cells hold ids separated by ; , or whitespace; empty -> []. ONE HOME since
# WI-448 slice 4 (`kitlib.spine.refs`); this was one of SIX copies of the split,
# one of which had drifted to `[;,]` alone.
_split_refs = _kitspine.refs


def read_rows(path):
    """The CSV rows of `path` as dicts, or [] when the file is absent. Read
    utf-8-sig (adversarial-review F4): a BOM'd registry — the realistic Excel
    round-trip on a Windows-first kit — would otherwise glue the BOM to the
    first column name and silently hide EVERY row from every consumer of this
    loader (the WI graph, the pending projection's spine lines). utf-8-sig
    reads plain utf-8 unchanged."""
    if not path.exists():
        return []
    return _kitspine.csv_rows(path.read_text(encoding="utf-8-sig"))


# --- the spec-folder registry reader: ONE home since WI-448 -------------------
# `docs/work/<status>/WI-###-<slug>.md` — one Markdown spec per work item, its
# STATUS encoded as the DIRECTORY (docs/concurrency-restructure.md §2.1). The
# 270-line reader that used to sit here VERBATIM, and identically in the other
# two of schedule.py, check_trajectory.py and agent_common.py, now lives once in
# `kitlib/registry.py`: owner ruling D-8 (`OI-16`, inversion confirmed
# 2026-08-13) retired the F5 no-shared-module rule that had licensed the copies.
#
# RE-EXPORTED under the names this module has always carried, so no call site
# and no test that reads `check_trajectory.<name>` changes with the move. The names are
# listed one per line rather than star-imported because this module's public
# surface is a fact its readers check, not a wildcard.
WI_COLUMNS = _kitregistry.WI_COLUMNS
SPEC_SCALARS = _kitregistry.SPEC_SCALARS
SPEC_LISTS = _kitregistry.SPEC_LISTS
SPEC_STATUS_DIRS = _kitregistry.SPEC_STATUS_DIRS
SPEC_FENCE = _kitregistry.SPEC_FENCE
SPEC_DELIVERABLE = _kitregistry.SPEC_DELIVERABLE
SPEC_HANDBACK = _kitregistry.SPEC_HANDBACK
SPEC_CONTEXT = _kitregistry.SPEC_CONTEXT
spec_work_dir = _kitregistry.spec_work_dir
spec_files = _kitregistry.spec_files
parse_spec_frontmatter = _kitregistry.parse_spec_frontmatter
parse_spec_status = _kitregistry.parse_spec_status
parse_spec_id = _kitregistry.parse_spec_id
parse_spec_deliverable = _kitregistry.parse_spec_deliverable
parse_spec_row = _kitregistry.parse_spec_row
read_spec_rows = _kitregistry.read_spec_rows


def read_registry_rows(path, errors=None):
    """The work-item rows from the one registry home — the spec folder beside
    `path` (`docs/work/`; the CSV home retired at concurrency-restructure
    Phase 5, RULING-4). An absent folder reads as an empty registry.

    This module is the VALIDATOR, so it is the one copy of the reader that
    SPEAKS. Two findings only it raises, both deliberate:

      * **a stray `work-items.csv` is itself a finding.** No reader consumes
        the CSV form any more, so a resurrected file is a second, silently
        ignored encoding of the registry — name it and route to the fix.
      * **a malformed spec is reported, not skipped silently** — the same
        split `load_wis` already draws for a malformed id.

    Findings append to `errors` when a list is given; with none, this degrades
    to the quiet read every other caller wants."""
    if errors is not None and Path(path).exists():
        errors.append(
            "{} present but the CSV registry home retired (concurrency-"
            "restructure Phase 5) — {} is the registry; convert stray rows "
            "with wi_convert.py and delete the file".format(WI_CSV, WI_WORK)
        )
    work_dir = spec_work_dir(path)
    if not work_dir.is_dir():
        return []
    return read_spec_rows(work_dir, on_error=None if errors is None else errors.append)


def registry_home(root):
    """The repo-relative path of the registry home — `docs/work/`, the one
    home since the CSV retired."""
    return WI_WORK


def load_wis(rows):
    """Parse work-item rows into `(wis, integrity_errors)`.

    `wis` are the real, well-formed items that form the graph; the inert `-000`
    example row is skipped (the `trace.py` placeholder rule — an off-spine
    optional registry's placeholder never blocks a gate). Integrity errors
    (malformed or duplicated ids) are collected on the raw rows so a broken id is
    *reported*, never silently dropped.

    Implements: SR-157, LLR-034
    """
    wis, integrity, seen = [], [], set()
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if not wid.startswith("WI-"):
            continue  # blank line / non-WI row
        if not WI_ID_RE.match(wid):
            integrity.append(
                "malformed work-item id {!r} (expected WI-<digits>)".format(wid)
            )
            continue
        if wid in seen:
            integrity.append("duplicate work-item id {}".format(wid))
            continue
        seen.add(wid)
        if wid.endswith("-000"):
            continue  # inert template example row (like trace.py)
        # A `~` prefix marks a soft (advisory-ordering) predecessor edge; a bare
        # WI id is a hard (blocking) edge; a bare `OI-###` id is a hard
        # OPEN-ITEM edge (OI-73), resolved against the open-items registry rather
        # than the WI graph — see `kitlib.spine.split_pred_edges`.
        preds, oi_preds, soft = _kitspine.split_pred_edges(r.get("Predecessors", ""))
        wis.append(
            {
                "id": wid,
                "title": (r.get("Title") or "").strip(),
                "workstream": (r.get("Workstream") or r.get("Track") or "").strip()
                or "other",
                "srs": _split_refs(r.get("SR-Refs", "")),
                "preds": preds,
                "oi_preds": oi_preds,
                "soft": soft,
                "status": (r.get("Status") or "queued").strip().lower(),
                # Backward-only summary (R-A) and the forward bridge (R-E). A
                # legacy CSV without the column reads as "" (DictReader -> None).
                "deliverable": (r.get("Deliverable") or "").strip(),
                "specref": (r.get("SpecRef") or "").strip(),
                "blockref": (r.get("BlockRef") or "").strip(),
            }
        )
    return wis, integrity


def _cycles(wis, pred_map):
    """Cycle strings found by DFS colouring over `pred_map` ([] = acyclic).

    Iterative (explicit stack), not recursive: a work-item registry may encode an
    arbitrarily long dependency chain, and a recursive DFS would raise a raw
    ``RecursionError`` past CPython's ~1000-frame limit — the kit fails on bad
    data with a clear message, never an uncaught traceback. ``stack`` holds
    ``[node, next-pred-index]`` frames and ``path`` mirrors
    their nodes, so a back-edge to a GREY (on-path) node reconstructs the cycle
    exactly as the former recursion did."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {w["id"]: WHITE for w in wis}
    found = []
    for w in wis:
        if colour[w["id"]] != WHITE:
            continue
        stack = [[w["id"], 0]]
        path = [w["id"]]
        colour[w["id"]] = GREY
        while stack:
            node, i = stack[-1]
            preds = pred_map[node]
            if i < len(preds):
                stack[-1][1] += 1
                p = preds[i]
                if colour[p] == GREY:
                    found.append(" -> ".join(path[path.index(p) :] + [p]))
                elif colour[p] == WHITE:
                    colour[p] = GREY
                    stack.append([p, 0])
                    path.append(p)
            else:
                colour[node] = BLACK
                stack.pop()
                path.pop()
    return found


# --- WI-349: physical-line + control-character integrity of the registry rows --
# WRITTEN FOR THE CSV HOME, and its first premise is retired: `staged_findings`
# used to compare `git show HEAD:<work-items.csv>` against the working copy
# LINE-WISE, and this check enforced the assumption that docstring stated. The
# folder registry is read by NAME LISTING, so nothing reads it line-wise any
# more (main() records the same retirement where the WI rows are loaded). What
# survives, and why this stays: the C0-control half below is about a cell being
# TEXT AT ALL — the `9e2008a` backspace case in `_control_findings` — which no
# carrier change touches, and the spine CSVs' own callers/tests still read it.
LINE_BREAK_CHARS = (("\r", "CR"), ("\n", "LF"))
# TAB is deliberately allowed: it is ordinary whitespace inside a quoted cell and
# breaks nothing downstream. Every other C0 control is not text — see below.
_ALLOWED_CONTROLS = "\t"


def _control_findings(cell):
    """`[(label, detail)]` for the integrity violations in one cell.

    Two classes, reported distinctly because the reader's next action differs:

      - **CR / LF** break the one-physical-line rule a CSV-carried registry
        reads (retired for the WI folder registry — see the block comment above);
      - **any other C0 control** is not text at all. Widened here after
        `9e2008a` wrote a literal `0x08` into this very registry: a shell heredoc
        collapsed the `\\b` of a Windows path, so `Git\\bin` became `Git` +
        BACKSPACE and the Deliverable cell went on to claim the remedy reads
        `put C:\\Program Files\\Gitin on PATH` — corrupting the exact string
        WI-326 existed to make actionable. Every gate step passed over it, and
        the CR/LF-only form of this check passed over it too: an adversarial
        review found it by scanning the bytes. A control character is invisible
        in every editor and diff a reader will use, so nothing but a byte-level
        check can see it, which is precisely the argument for the check.
    """
    out = []
    for char, label in LINE_BREAK_CHARS:
        if char in cell:
            out.append(
                (
                    label,
                    "a WI row must be ONE physical line (the staged-close scan "
                    "compares HEAD line-wise, so an embedded break makes it read "
                    "a different set of rows while every other check passes)",
                )
            )
    if out:
        return out  # a break is the more specific diagnosis; do not double-report
    for char in cell:
        if ord(char) < 0x20 and char not in _ALLOWED_CONTROLS or ord(char) == 0x7F:
            out.append(
                (
                    "control character 0x{:02X}".format(ord(char)),
                    "a registry cell is text; a control character is invisible in "
                    "every editor and diff, so it can only ever be found by a "
                    "byte-level check like this one",
                )
            )
            break  # one finding per cell; the fix is the same
    return out


def cell_integrity_errors(rows):
    """Hard-error strings for any registry cell that is not one line of plain text.

    Demonstrated 2026-07-28: a WI row was written with a literal newline inside a
    quoted `Title` cell. It round-tripped through `csv` perfectly, so the full
    trajectory validator reported CLEAN — and the only thing that surfaced it was
    git warning about mixed line endings in the working tree, i.e. luck. What
    such a row actually costs is silent and downstream: `staged_findings` reads a
    *different set of rows* than the loader does (its line-wise HEAD comparison
    splits the row in two), the dashboard renders a broken cell in its detail
    JSON, and the row is invisible to every line-based tool that touches the
    registry.

    ERROR at every run, alongside the malformed/duplicate-id errors rather than
    in the warn-first coherence tier: those two are the same class — a row the
    loader cannot be trusted to have read correctly — as opposed to a coherence
    question about a row it read fine.

    Deliberately scoped to the WI registry: the line-wise comparison is what
    creates the requirement, and it reads only this file. The spine registries
    are `trace.py`'s to police.

    Names the WI id and the COLUMN, because a bare "row 47 is malformed" against
    a 350-row single-line-per-row CSV is not actionable — the cell is what the
    author has to find. Falls back to the 1-based row number when it is the id
    cell itself that is broken.
    """
    errors = []
    for index, row in enumerate(rows, start=1):
        raw_id = str(row.get("WI-ID") or "")
        broken_id = any(char in raw_id for char, _ in LINE_BREAK_CHARS)
        # A truncated id would be worse than no id — it looks like a real one and
        # matches nothing — so a broken id cell reports by row number instead.
        where = (
            "row {}".format(index)
            if broken_id or not raw_id.strip()
            else raw_id.strip()
        )
        for column, value in row.items():
            # DictReader hands back a list under the restkey when a row has more
            # fields than the header, and None as the key; neither is a str.
            cells = value if isinstance(value, list) else [value]
            name = column if isinstance(column, str) else "<extra fields>"
            for cell in cells:
                if not isinstance(cell, str):
                    continue
                for label, detail in _control_findings(cell):
                    errors.append(
                        "{}: {} cell contains a literal {} — {}".format(
                            where, name, label, detail
                        )
                    )
    return errors


def _title_length_warns(wis):
    """`[]` or one summarised WARN string naming how many OPEN work items carry
    a Title over `_TITLE_CONCISE_MAX` characters (WI-479, M-03).

    Scoped to `OPEN_STATUSES` — a closed row is a historical record this
    advisory never asks anyone to reword. Summarised into ONE line (worst-first,
    first 5 named) rather than one line per row — the same call the IF-coverage
    rule elsewhere in this module already made (its `SUMMARISED` comment: N warn
    lines is a check nobody reads)."""
    over = sorted(
        (
            w
            for w in wis
            if w["status"] in OPEN_STATUSES and len(w["title"]) > _TITLE_CONCISE_MAX
        ),
        key=lambda w: -len(w["title"]),
    )
    if not over:
        return []
    shown = ", ".join(
        "{} ({} chars)".format(w["id"], len(w["title"])) for w in over[:5]
    )
    return [
        "{} open work item(s) carry a Title over {} characters — keep the "
        "Title a concise name and put rationale in the body, not the "
        "registry cell{}: {}".format(
            len(over),
            _TITLE_CONCISE_MAX,
            " (first 5 shown)" if len(over) > 5 else "",
            shown,
        )
    ]


def _predecessor_errors(w, ids, known_ois):
    """The dangling-edge ERRORs for one WI's predecessors: a WI edge (hard or
    soft) that names no work item, or an `OI-###` edge (OI-73) that names no
    minted open item. The two edge kinds resolve against different registries —
    the WI id set and the open-items registry — but are the same dangling-edge
    error class."""
    out = []
    for p in w["preds"] + w["soft"]:
        if p not in ids:
            out.append("{}: predecessor {!r} is not a work item".format(w["id"], p))
    for o in w["oi_preds"]:
        if o not in known_ois:
            out.append(
                "{}: open-item predecessor {!r} is not a minted open item "
                "(OI-73 typed edge; check docs/requirements/open-items.toml and "
                "the id-watermark's OI space)".format(w["id"], o)
            )
    return out


def validate(wis, known_srs, known_ois=None):
    """Return the hard-error strings for the work-item graph ([] = clean).

    Dangling `SR-Refs` are WARNED on stderr (a draft SR referenced ahead of its
    row is legitimate), never failed — and only when the SR registry is
    non-empty, so a repo without SRs yet does not spuriously warn. Soft (`~`)
    predecessors must resolve like hard ones, but only **hard** edges are
    subject to the acyclicity ERROR — a cycle that needs a soft edge to close
    is a WARN (conflicting ordering hints), never a failure. An overlong OPEN
    Title also WARNS (never fails) — see `_title_length_warns`.

    A hard OPEN-ITEM edge (OI-73) resolves against `known_ois` — the open-items
    registry read through the spine carrier — not the WI id set: an `OI-###` in
    `Predecessors` that names no minted open item is a dangling edge, the same
    ERROR class as an unknown WI predecessor. `known_ois` is `None` only for the
    non-adopter with no registry, where any OI edge cannot be resolved and is
    left to the scheduler's fail-closed `waiting`; the caller passes the real
    set (see `main`).

    Implements: SR-157, LLR-034
    """
    ids = {w["id"] for w in wis}
    known_ois = known_ois if known_ois is not None else frozenset()
    errors = []

    for w in wis:
        errors.extend(_predecessor_errors(w, ids, known_ois))
        for s in w["srs"]:
            if known_srs and s not in known_srs:
                print(
                    "check_trajectory: WARN - {} references {} "
                    "(not in the SR registry; draft?)".format(w["id"], s),
                    file=sys.stderr,
                )

    for msg in _title_length_warns(wis):
        print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)

    # A hard cycle makes the trajectory unstartable -> ERROR.
    hard_map = {w["id"]: [p for p in w["preds"] if p in ids] for w in wis}
    for cyc in _cycles(wis, hard_map):
        errors.append("dependency cycle: {}".format(cyc))

    # A cycle that only closes through soft edges is a hint conflict -> WARN.
    if not any(e.startswith("dependency cycle") for e in errors):
        both_map = {
            w["id"]: [p for p in w["preds"] + w["soft"] if p in ids] for w in wis
        }
        for cyc in _cycles(wis, both_map):
            print(
                "check_trajectory: WARN - soft-edge cycle (advisory ordering "
                "hints conflict; not a blocker): {}".format(cyc),
                file=sys.stderr,
            )
    return errors


def load_known_srs(root):
    """The set of real SR ids from system-requirements.toml (for the SR-ref warn)."""
    return {
        (r.get("SR-ID") or "").strip()
        for r in spine_carrier.load(root / SR_CSV, "SR-ID")
        if (r.get("SR-ID") or "").startswith("SR-")
    }


#: The open-items registry — read directly through `spine_carrier` (already a
#: dependency) rather than through `trace.open_item_states`, because a
#: `check_trajectory -> trace` import edge would form a new module cycle
#: (`trace` reaches back into `check_trajectory`); the import-cycle ratchet
#: forbids it. The read is the same one `trace.open_item_states` performs.
OPEN_ITEMS_REL = "docs/requirements/open-items.toml"


def load_known_ois(root):
    """The set of minted open-item ids (for the typed OI-edge resolution, OI-73).

    Reads the same registry the readiness gate resolves an OI edge against, so
    the validator's ERROR and the scheduler's `waiting` cannot disagree about
    whether an `OI-###` edge is even real. `None` when the repo carries no
    open-items registry at all (the D-5 absent-vs-empty distinction), which
    `validate` treats as the non-adopter posture rather than failing every OI
    edge."""
    path = Path(root) / OPEN_ITEMS_REL
    if spine_carrier.resolve(path) is None:
        return None
    return frozenset(
        oid
        for r in spine_carrier.load(path, "OI-ID")
        if (oid := (r.get("OI-ID") or "").strip()).startswith("OI-")
        and not oid.endswith("-000")
    )


# Source-file extensions stripped when normalizing a module path, so the arch-map
# name (`scripts/check`), an LLR `Module` cell and an IF endpoint written with
# the full repo path (`project-trajectory/scripts/check.py`) collapse to one key.
# ONE HOME since WI-448 slice 4 (`kitlib.spine`), which also retired the false
# claim this comment carried: it promised the tuple was "kept in sync with
# trace.py._MODULE_EXTS", and `trace.py` has no such name — the sync partner
# named here did not exist. The real second copy was `gen_arch_map.py`'s.
_MODULE_EXTS = _kitspine.MODULE_EXTS
_norm_module = _kitspine.norm_module


def load_ifs(rows):
    """Real (non-`-000`) IF-### interface rows as dicts, each already RESOLVED
    into its two sides — `owner` (one endpoint, possibly `''`) and the far side
    as `requestors` / `consumers` (lists; exactly one is meant to be set — the
    key name is the direction) plus `far`, whichever of the two it is. Lenient — `trace.py` owns IF integrity (malformed ids, owner
    shape); this loader only feeds the warn-first coverage views, so a
    malformed id is simply skipped here.

    `approval` is the tier's ONE maturity field. It replaced `stability` at
    WI-442, which had itself replaced `status` at WI-443 — the same defect twice
    (two columns on one row meaning different kinds of "settled"), fixed the same
    way. `direction`/`this_project`/`counterpart` went at WI-455 (OI-60 ruled
    (a)): flow is no longer a column but the shape of the row, so RESOLUTION
    happens here, once, and every view downstream (this module's connectivity
    credit and declared pairs, `traj_views`' seam graphs) reads the same two
    keys instead of re-deriving the orientation from a flag. Since OI-67 the
    owner side is the row's own `owner` cell, one spelling, nothing derived."""
    out = []
    for r in rows:
        iid = (r.get("IF-ID") or "").strip()
        if not IF_ID_RE.fullmatch(iid) or iid.endswith("-000"):
            continue
        out.append(
            {
                "id": iid,
                "owner": _kitspine.seam_owner(r),
                "requestors": _kitspine.seam_requestors(r),
                "consumers": _kitspine.seam_consumers(r),
                "far": _kitspine.seam_far_side(r)[1],
                "approval": (r.get("Status") or "").strip().lower(),
                "notes": (r.get("Notes") or "").strip().lower(),
            }
        )
    return out


def load_seams(root):
    """`load_ifs` over the live registry — the one call every seam view makes."""
    return load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))


def _contracts_grammar_findings(root):
    """Marker-grammar findings over the declared scan root, or `[]` where the
    tree cannot be read.

    Degrades to silence on a missing `gen_arch_map`, files-mode or an absent
    scan root, exactly as `arch_inventory` does — a detector that crashed in a
    scaffold would be removed from the floor, which is the same outcome as not
    having it."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "contracts_grammar_findings"):
        return []
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    if not src_dir.is_dir():
        return []
    found = []
    for path in sorted(src_dir.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        found.extend(
            gen_arch_map.contracts_grammar_findings(path.name, tree, text.splitlines())
        )
    # The file owners — registries, config, hooks — read through the same
    # grammar (OI-67 slice 2), so a lossy marker in a header is named too.
    if hasattr(gen_arch_map, "file_grammar_findings"):
        for owner, path in _owner_files(root):
            found.extend(gen_arch_map.file_grammar_findings(owner, path))
    return found


def _owner_files(root):
    """`gen_arch_map.owner_files` over the live registry; `[]` when the
    generator is absent or predates the file-owner scan."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "owner_files"):
        return []
    return gen_arch_map.owner_files(root, spine_carrier.load(root / IF_CSV, "IF-ID"))


def _file_owner_declarations(root, out):
    """`{owner: {IF ids}}` declared by the file owners' headers; a header the
    grammar refuses is reported into `out` and read as declaring nothing."""
    declared = {}
    for owner, path in _owner_files(root):
        try:
            ids, _bodies = gen_arch_map.file_contracts(path)
        except gen_arch_map.ContractsGrammarError as exc:
            out.append("{}: {}".format(owner, exc))
            continue
        if ids:
            declared[owner] = set(ids)
    return declared


def arch_inventory(root):
    """`(module_names, {module: {IF ids}}, {module: {imported stems}})` derived
    STRAIGHT from the source tree under the declared arch-map scan root
    (`[paths] src` + `[arch-map] mode`, the same profile check.py reads),
    through `gen_arch_map.scan_inventory` — the one AST walk the map's
    consumers share. Until WI-455 (sitting-2 decision 8) this parsed the
    committed MODULE MAP block back out of `docs/architecture.md`; the
    registries→dashboard re-pointing retired that way-station, so the
    inventory is now the LIVE tree — on a work branch too, which is what
    dissolved the WI-399 committed-vs-disk delta rule (`shipped_modules` and
    the station-first firing gap died with it). `module_names` keep the map's
    grammar (`scripts/check`-style keys relative to the scan root's parent);
    the IF map carries each module's `Contracts: IF-###` docstring
    declarations; the import map carries the internal-import names — the
    cross-CMP rule's edge source (WI-064). Empty when the root is absent,
    files-mode (no parser), or `gen_arch_map` is not beside this script, so
    the coverage layers stay vacuous exactly where the committed map was.

    Implements: SR-159, LLR-067
    """
    if gen_arch_map is None:
        return set(), {}, {}
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return set(), {}, {}
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    names, contracts, imports = [], {}, {}
    for rel, _summary, imps, cons, _rows in gen_arch_map.scan_inventory(
        [src_dir], strict=False
    ):
        names.append(rel)
        if cons:
            contracts.setdefault(rel, set()).update(cons)
        if imps:
            imports.setdefault(rel, set()).update(imps)
    return set(names), contracts, imports


def interface_findings(root):
    """Architecture-connectivity coverage warns (S5/WI-056; process.md §8), all
    warn-first — the caller prints them and they never change the exit code, at
    any gate. Returns the warn strings ([] when opted out or vacuous).

    Ruled opt-out, default-on: fires even with an empty/absent `interfaces.csv`
    (a multi-module arch-map with no declared seams reads "connectivity
    undeclared"); silenced only by `[checks] interfaces_check = false` or a ≤1-module
    inventory (nothing to connect).

    Implements: SR-159, LLR-042
    """
    if not read_interfaces_check_enabled(root):
        return []
    inventory, declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect (or no arch-map yet) — vacuous
    ifs = load_seams(root)
    out = []
    if not ifs:
        return [
            "connectivity undeclared: the {}-module architecture declares no "
            "interfaces — add IF-### rows to {}, or set docs/process.toml "
            "[checks] interfaces_check = false".format(len(inventory), IF_CSV)
        ]

    inv_norm = {_norm_module(m): m for m in inventory}
    inv_norm.pop("", None)
    endpoints, provides, consumes = set(), set(), set()
    sources, sinks = set(), set()
    for r in ifs:
        producer = _norm_module(r["owner"])
        consumer_ns = {_norm_module(c) for c in r["far"]} & set(inv_norm)
        endpoints.update(consumer_ns)
        if producer in inv_norm:
            endpoints.add(producer)
        # The honesty valve: a `source`/`sink` FIRST word in Notes marks the
        # row's own side a deliberate source (consumes nothing) / sink (provides
        # nothing), so it doesn't breed a boilerplate opposite-facing row. Since
        # WI-455 the marked side is named by the ROLE rather than by a column:
        # `source` marks the OWNER, `sink` marks the CONSUMERS — which is what
        # the two words meant when both were read off `ThisProject`.
        marker = r["notes"].split()
        first = marker[0].rstrip(":;,.") if marker else ""
        if first == "source":
            sources.add(producer)
        elif first == "sink":
            sinks.update(_norm_module(c) for c in r["far"])
        # Producer -> consumer credit, read off the resolved sides.
        if producer in inv_norm:
            provides.add(producer)
        consumes.update(consumer_ns)

    for n in sorted(inv_norm):
        module = inv_norm[n]
        if n not in endpoints:
            out.append(
                "connectivity undeclared: module {!r} is in the arch-map but no "
                "IF-### row names it".format(module)
            )
            continue
        if n not in consumes and n not in sources:
            out.append(
                "module {!r} declares no Consumes seam (mark it `source` in its "
                "IF row Notes if it deliberately consumes nothing)".format(module)
            )
        if n not in provides and n not in sinks:
            out.append(
                "module {!r} declares no Provides seam (mark it `sink` in its IF "
                "row Notes if it deliberately provides nothing)".format(module)
            )

    # Seam-TC citation: each declared IF id should be cited by >=1 TC (the rung-2
    # seam-TC rule, and process.md §8's "every interface is backed by an SR and a
    # contract/fixture test").
    #
    # THE ARMING KEY HAS NOW MOVED TWICE, AND THE THIRD SPELLING IS "ALL ROWS".
    # It first read `Status == Active`, which armed EXACTLY the 5 rows already
    # TC-cited — zero findings by construction. WI-443 re-keyed it to
    # `Stability == Stable` (103 of 108 uncited). WI-442 retired `Stability` for
    # `Approval`, and copying the shape forward as `Approval == "approved"` would
    # have reproduced the ORIGINAL tautology in a new column: every row reads
    # `draft` today, so the rule would arm on nothing and report a clean zero.
    #
    # So it arms on EVERY real IF row, and the maturity column drops out of the
    # rule entirely. That is the honest reading of the obligation anyway — an
    # interface is backed by a contract test or it is not; how settled its
    # contract is was never the question — and it is the one spelling that cannot
    # be silently disarmed by a vocabulary change.
    #
    # SUMMARISED, not one line per row, and that is a deliberate ergonomic choice
    # rather than a softening: this function runs in the shipped pre-commit hook,
    # where 103 warn lines is a check nobody reads and therefore a check that does
    # not work. One line carries the count, which is the number that has to fall.
    #
    # STAYS PURE WARN-FIRST, FOREVER, EVEN UNDER --strict — the promotable half
    # split off at WI-488 (OI-43 ruled (a)) into `if_tc_coverage_findings` below,
    # which reports only the seams NOT on the migration allowlist. This line keeps
    # reporting the TOTAL uncited count (allowlisted seams included) so the whole
    # debt stays visible even once the actionable subset goes quiet.
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    uncited = [r["id"] for r in ifs if r["id"] not in tc_cited]
    if uncited:
        shown = ", ".join(uncited[:5])
        out.append(
            "{} IF seam(s) are cited by no TC (a seam should carry a "
            "contract/fixture test, process.md §8){}: {}".format(
                len(uncited), " — first 5" if len(uncited) > 5 else "", shown
            )
        )

    # Marker-grammar honesty (OI-66): the `Contracts:` marker must OPEN its line
    # and parse as an id list, which is what stops prose that DENIES a
    # declaration from making one. Tightening a shipped grammar may not lose an
    # adopter's seams in silence, so both lossy forms — a marker-shaped line
    # whose id list will not parse, and a `Contracts:` carrying ids mid-line —
    # are reported by name. Warn-first: on this repo the count is zero, and on
    # an upgrading repo it is the migration list.
    out.extend(_contracts_grammar_findings(root))

    # Docstring citation: a `Contracts: IF-###` a script declares (harvested into
    # the arch-map) must exist in the registry; and, once the convention is in
    # use, a registry IF whose OWNER declares no matching citation warns too.
    registry_ids = {r["id"] for r in ifs}
    file_declared = _file_owner_declarations(root, out)
    for module, ids in sorted(declared_contracts.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "module {!r} docstring declares Contracts: {} but no such IF-### "
                "row exists".format(module, iid)
            )
    for owner, ids in sorted(file_declared.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "{!r} header declares Contracts: {} but no such IF-### row "
                "exists".format(owner, iid)
            )
    if declared_contracts or file_declared:  # reverse direction, once opted in
        out.extend(
            _owner_exact_findings(
                ifs,
                inv_norm,
                declared_contracts,
                file_declared,
                dict(_owner_files(root)),
            )
        )
    return out


def _owner_exact_findings(
    ifs, inv_norm, declared_contracts, file_declared, file_owners
):
    """OWNER-EXACT (OI-67 slice 2): the row's owner is the source that must
    declare it — a module's `Contracts:` line, or a file's header. An id
    declared on some OTHER module used to pass; that is the id-global hole the
    build round named, closed here. Every module in the INVENTORY is judged,
    not only the declaring ones — an owner that declares nothing at all is the
    plainest miss. An `external:` owner has nothing to scan; a directory with
    no README or an owner the tree cannot resolve falls back to the id-global
    read rather than warning about a header nobody could write."""
    out = []
    by_module = {_norm_module(m): ids for m, ids in declared_contracts.items()}
    all_declared = set().union(*declared_contracts.values(), *file_declared.values())
    for r in ifs:
        owner, iid = r["owner"], r["id"]
        if not owner or owner.startswith("external:"):
            continue
        norm = _norm_module(owner)
        if norm in inv_norm:
            if iid not in by_module.get(norm, set()):
                out.append(
                    "IF {} is owned by {!r}, but that module's Contracts: line "
                    "does not declare it — the owner is the one declaration "
                    "site".format(iid, owner)
                )
        elif owner in file_owners:
            if iid not in file_declared.get(owner, set()):
                out.append(
                    "IF {} is owned by {!r}, but that file's header declares "
                    "no Contracts: line naming it — the owner is the one "
                    "declaration site".format(iid, owner)
                )
        elif iid not in all_declared:
            out.append(
                "IF {} is in the registry but no source declares it via a "
                "Contracts: line".format(iid)
            )
    return out


# --- the armed definition gate (OI-67 slice 6) --------------------------------


def _declaration_sites(root):
    """`({key: (source_as_written, ids, bodies)}, problems)` — every source in
    the tree that declares a seam, read through the one harvester the
    interface reference uses (`gen_arch_map.scan_contracts`): the modules under
    the declared scan root, keyed by normalized module path (`scripts/check`),
    and the file owners the registry names, keyed by the owner as the registry
    spells it (`docs/stack.ini`, `hooks/pre-commit`). `problems` is
    `[(source, message)]` for every header the contract GRAMMAR refused, so a
    refusal is reported rather than read as "declares nothing" — and, above
    all, rather than DISARMING the gate: the refusal used to be caught for the
    whole scan and answered with `(None, [])`, so one malformed body anywhere
    in the tree silenced every other row's verdict too (adversarial review
    2026-08-29, F1). A refused source is absent from `sites` rather than
    entered as declaring nothing, which would hand its rows to the reverse
    check's warn instead of this gate's finding. A source the scan could not
    READ is deliberately NOT in `problems`: that is the reference's own "could
    not read" list and `arch_inventory`'s skip. `(None, problems)` when there
    is no surface to read — files-mode, an absent scan root, no generator
    beside this script — the `arch_inventory` posture."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "scan_contracts"):
        return None, []
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return None, []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    if not src_dir.is_dir():
        return None, []
    owner_files = _owner_files(root)
    refused = []
    records, _unreadable = gen_arch_map.scan_contracts(
        [src_dir], owner_files, grammar_errors=refused
    )
    file_names = {owner for owner, _path in owner_files}
    sites = {}
    for rel, _summary, ids, bodies in records:
        key = rel if rel in file_names else _norm_module(rel)
        sites[key] = (rel, set(ids), set(bodies))
    return sites, refused


def contract_body_findings(root):
    """THE ARMED DEFINITION GATE (OI-67 slice 6). Every interface row must be
    STATED — declared on its owner's `Contracts:` marker and given a
    `Contract IF-###:` body there — because under the one-owner shape the body
    is the definition's only home: a row with no body is an interface with no
    definition. Returns finding strings; the caller prints them WARN plain and
    promotes them to ERROR under `--strict`, the `if_tc_coverage_findings`
    idiom, sharing its `[checks] interfaces_check` opt-out.

    ONE RULE, FOUR SHAPES. (1) The owner declares the id and states no body —
    "declared, not stated", the reference's own debt line, now a finding.
    (2) An `external:`-owned row is declared and stated by the kit module on
    its FAR SIDE — the consumer that reads the external surface, or the
    requestor that drives it — because the external party's header is not
    ours to write and that module is the one in-tree home of OUR READING of
    the surface; where the far side names several kit modules any one of them
    may state it. (3) A stray declaration — a source declaring an id the
    registry owns to a different in-tree source — because the owner is the
    ONE declaration site and a second copy is a second definition waiting to
    disagree; a far-side module stating an external-owned row is not stray.
    (4) A source whose header the contract GRAMMAR refuses — an empty
    `Contract IF-###:` opener, a body before its marker, a duplicate body, a
    body carrying an HTML comment — because nobody can read what it states:
    its declared rows count as unstated, and the refusal is named once per
    source rather than once per row it takes down with it.

    WHAT STAYS A WARN, on record: an owner that declares NOTHING is the
    owner-exact reverse check's finding (`_owner_exact_findings`, warn-only),
    not this gate's — the ruled rule is "a DECLARED seam with no body", and
    promoting the undeclared case would red every fixture and adopter row
    whose owner has not yet been headed at all, which is the migration list
    rather than a defect in a stated definition. The dodge that leaves —
    never declare, never owe a body — is visible in that warn and in the
    reference's summary line, and is the owner's to promote. Vacuous where
    there is no surface (files-mode, an absent scan root), the
    `arch_inventory` posture; an unreadable source is the reference's own
    list, not a finding here."""
    if not read_interfaces_check_enabled(root):
        return []
    sites, refused = _declaration_sites(root)
    if sites is None:
        return []
    out = [
        "{!r} declares seams but its header is refused by the contract "
        "grammar: {} — its declared rows count as unstated".format(rel, msg)
        for rel, msg in refused
    ]
    ifs = load_seams(root)
    file_names = {owner for owner, _path in _owner_files(root)}

    def site_key(owner):
        return owner if owner in file_names else _norm_module(owner)

    owner_key = {}
    for r in ifs:
        if r["owner"] and not r["owner"].startswith("external:"):
            owner_key.setdefault(r["id"], site_key(r["owner"]))
    external_far = {}
    for r in ifs:
        iid, owner = r["id"], r["owner"]
        if not owner:
            continue  # trace.py's required-cell finding
        if owner.startswith("external:"):
            far = [site_key(e) for e in r["far"] if not e.startswith("external:")]
            external_far[iid] = set(far)
            out.extend(_external_body_findings(sites, iid, owner, far))
            continue
        site = sites.get(site_key(owner))
        if site is None:
            continue  # declares nothing, or unresolvable: the reverse check's warn
        rel, ids, bodies = site
        if iid in ids and iid not in bodies:
            out.append(
                "IF {} is declared by its owner {!r} but states no `Contract {}:` "
                "body there — an interface with no definition".format(iid, rel, iid)
            )
    out.extend(_stray_declaration_findings(sites, owner_key, external_far))
    return out


def _external_body_findings(sites, iid, owner, far):
    """The external arm of `contract_body_findings`: `far` is the row's far
    side as site keys (kit modules only); silent when none faces it or one
    states the body, a finding otherwise."""
    if not far or any(k in sites and iid in sites[k][2] for k in far):
        return []
    declared = [sites[k][0] for k in far if k in sites and iid in sites[k][1]]
    if declared:
        return [
            "IF {} is owned by {!r}; its far side {!r} declares it but states no "
            "`Contract {}:` body — our reading of an external surface is stated "
            "by the kit module that faces it".format(iid, owner, declared[0], iid)
        ]
    return [
        "IF {} is owned by {!r} and no far-side kit module states it — our "
        "reading of an external surface lives in the header of the module that "
        "faces it ({})".format(iid, owner, ", ".join(sorted(far)) or "none named")
    ]


def _stray_declaration_findings(sites, owner_key, external_far):
    """The stray arm of `contract_body_findings`: a source declaring an id the
    registry owns to a different in-tree source, or an external-owned id whose
    far side it is not."""
    out = []
    for key, (rel, ids, _bodies) in sorted(sites.items()):
        for iid in sorted(ids):
            if iid in external_far:
                if key not in external_far[iid]:
                    out.append(
                        "{!r} declares IF {}, an external-owned seam whose far side "
                        "it is not — our reading of an external surface is stated "
                        "by the module that faces it".format(rel, iid)
                    )
                continue
            home = owner_key.get(iid)
            if home is None or home == key or home not in sites:
                continue  # unowned (trace's finding), the owner, or unresolvable
            out.append(
                "{!r} declares IF {}, which the registry owns to {!r} — the owner is "
                "the one declaration site; a second copy is a second "
                "definition".format(rel, iid, sites[home][0])
            )
    return out


# --- seam-TC coverage promotion + its migration allowlist (OI-43 ruled (a),
# WI-488) -------------------------------------------------------------------


def _parse_if_tc_allow_full(text):
    """`(entries, seed, unparsed)` — the whole parse, both halves, the
    `docs/provenance-allow` split (`trace.read_provenance_allow`): `entries`
    and `seed` are exactly `parse_if_tc_allow`'s return (kept as a separate,
    pinned-arity wrapper below since `tests/test_trajectory_arch.py` unpacks
    it as a 2-tuple); `unparsed` is `[(lineno, line)]` for every DECLARING
    line the grammar dropped — not blank, not a `#`-comment, and whose first
    token does not parse as an `IF-###` id — so a malformed entry is reported
    rather than silently read as an empty file
    (`if_tc_allow_parse_findings`)."""
    entries = []
    seed = None
    unparsed = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = IF_TC_SEED_RE.match(line)
            if m and seed is None:
                seed = int(m.group(1))
            continue
        head, _, reason = line.partition(" — ")
        token = head.split()[0] if head.split() else ""
        if IF_ID_RE.fullmatch(token):
            entries.append((token, reason.strip() or None))
        else:
            unparsed.append((lineno, line))
    return entries, seed, unparsed


def parse_if_tc_allow(text):
    """`([(id, reason-or-None), ...] in file order, declared seed count or
    None)` for one allowlist file's TEXT.

    The SEED COUNT is a machine-readable header key, `# seed-count: <int>`,
    naming how many of the entries below are the migration BASELINE — the
    population measured when the promotion was seeded, which shares one reason
    stated once in the header rather than repeated per line. Entries past that
    count are ADDITIONS, and an addition is a judgment someone made, so it
    carries its own ` — <reason>`. A file that declares no seed count has no
    baseline to grow past; every entry is then read as seeded, which is what an
    adopter's freshly-seeded file looks like before it has ever grown.

    `_parse_if_tc_allow_full` is the same parse plus the malformed-line half;
    this wrapper's 2-tuple return is pinned by
    `test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set`, so it stays
    exactly as it was rather than growing a third element."""
    entries, seed, _unparsed = _parse_if_tc_allow_full(text)
    return entries, seed


def read_if_tc_allow(root):
    """`{IF-### id: reason-or-None}` from `docs/if-tc-coverage-allow` — the
    seam-TC coverage migration allowlist. Absent file: empty dict.

    Grammar, deliberately the cheap kind: one non-blank, non-`#`-comment line
    per entry, the first whitespace-run-delimited token an `IF-###` id,
    optionally followed by ` — <reason>`. FAIL-SOFT IN THE LOUD DIRECTION, the
    `docs/provenance-allow` rule: a line whose first token does not parse as an
    IF-### id declares nothing and is dropped, so the worst a malformed entry
    can do is leave the finding it was meant to silence still reported — never
    the reverse.

    AN ADDITION BEYOND THE DECLARED SEED NEEDS A REASON, and a bare one
    SUPPRESSES NOTHING — the same fail-soft-loud direction. The 2026-08-21
    review measured why: a new seam reds `--strict`, and the one-line edit that
    greened it was appending its bare id, which was lexically indistinguishable
    from the 120 seeded lines and produced no hygiene signal, no test failure
    and no reason anyone could review. The list is a burn-down; growth has to
    cost a sentence."""
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return {}
    entries, seed = parse_if_tc_allow(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    out = {}
    for i, (token, reason) in enumerate(entries):
        if seed is not None and i >= seed and not reason:
            continue
        out[token] = reason
    return out


def if_tc_allow_growth(root):
    """`([(id, reason-or-None), ...], seed)` — the entries past the declared
    seed count, and that count (None when the file declares none)."""
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return [], None
    entries, seed = parse_if_tc_allow(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    return ([] if seed is None else entries[seed:]), seed


def if_tc_coverage_findings(root):
    """The PROMOTABLE half of seam-TC coverage (OI-43 ruled (a), WI-488): an IF
    seam cited by no TC — the rung-2 seam-TC rule `interface_findings` already
    reports informationally, in full — becomes an ERROR when it is NOT on the
    migration allowlist `docs/if-tc-coverage-allow`. Returns the finding
    string(s) ([] when clean or opted out); the caller prints them WARN plain
    and promotes them to ERROR under `--strict` (DevStg-Tests+), the
    `component_findings` idiom.

    THE ALLOWLIST IS A MIGRATION DEVICE, NOT A PERMANENT EXEMPTION SURFACE. It
    was seeded at the population measured when the ruling executed (the file's
    own header carries the exact count, command and revision) — the standing
    never-green-by-list-edit rule (session-protocol skill §2) governs every
    entry: adding one to silence a genuinely NEW uncited seam is ACCEPTING what
    it measures, not laundering it, and should carry its own reason. An
    allowlisted seam still counts in `interface_findings`' total; it simply does
    not error here. `if_tc_allow_hygiene_findings` reports — never blocks — a
    listed seam that has since gained a TC, so a shrinking list (the declared
    burn-down) stays visible rather than silently absorbed.

    Opt-out shares `interface_findings`' `[checks] interfaces_check` dial —
    same data, same switch — AND its ≤1-module arch-map vacuity: the promoted
    rule must arm on no MORE than the warn it promotes, so a `files`-mode or
    single-module adopter that never saw this warn does not suddenly see this
    error. Widening scope is a second, unruled change riding a severity one.

    DELIBERATELY UNCLAIMED — this function declares no back-link at all.
    `LLR-042` (`SR-159`) is
    `Approved`, and its own `detail` says the connectivity layer emits its
    findings "without changing exit status" — true of `interface_findings`,
    which this function does not touch, and now FALSE of the seam-TC rule this
    function promotes. Amending an Approved cell overrides attestation (the
    sitting's act, the SR-006/LLR-060 precedent, WI-473); minting a fresh
    Drafted LLR under `SR-159` was considered and declined for the same reason
    that session gave first — `SR-159` is phase 1, and a Drafted child would
    drag that phase's derived bar down as a side effect of unrelated work. So
    the built behaviour is ahead of its requirement on purpose, recorded as
    owed on WI-488's own spec rather than claimed here.
    """
    if not read_interfaces_check_enabled(root):
        return []
    inventory, _declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect — vacuous, the interface_findings gate
    ifs = load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))
    if not ifs:
        return []
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    allow = read_if_tc_allow(root)
    new_uncited = [
        r["id"] for r in ifs if r["id"] not in tc_cited and r["id"] not in allow
    ]
    if not new_uncited:
        return []
    shown = ", ".join(new_uncited[:5])
    return [
        "{} IF seam(s) have no citing TC and are not on the migration allowlist "
        "({}) — cite the seam from a TC, or add a reasoned entry to the "
        "allowlist (process.md §8; OI-43/WI-488){}: {}".format(
            len(new_uncited),
            IF_TC_ALLOW,
            " — first 5" if len(new_uncited) > 5 else "",
            shown,
        )
    ]


def if_tc_allow_hygiene_findings(root):
    """`docs/if-tc-coverage-allow` hygiene (WI-488) — WARN-ONLY, never the exit
    code, not even under `--strict`: unlike a NEW uncited seam, a STALE entry is
    never a defect to fix under pressure. Two shapes:

    - a listed seam has since gained a TC citation — burn-down PROGRESS, so
      pruning the entry is housekeeping, not a fix owed to a red build;
    - a listed id resolves to no live IF-### row (retired/renumbered).

    Kept structurally apart from `if_tc_coverage_findings` so a shrinking
    allowlist can never itself be mistaken for a new finding, and so this
    class can never gate even by an unintended promotion of that function.
    Shares that function's ≤1-module arch-map vacuity: reporting a listed
    seam as stale is meaningless while the coverage rule it tracks never arms.

    DELIBERATELY UNCLAIMED — see `if_tc_coverage_findings`' own note on why no
    back-link declaration names `LLR-042` here.
    """
    if not read_interfaces_check_enabled(root):
        return []
    allow = read_if_tc_allow(root)
    grown, seed = if_tc_allow_growth(root)
    # `grown` is consulted for the early return too: an addition the reader
    # DROPPED (no reason) leaves `allow` empty while the file still grew, and
    # that is exactly the state most worth reporting.
    if not allow and not grown:
        return []
    inventory, _declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []
    ifs = load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))
    all_ids = {r["id"] for r in ifs}
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    out = []
    unknown = sorted(i for i in allow if i not in all_ids)
    if unknown:
        shown = ", ".join(unknown[:5])
        out.append(
            "{} {} entries name no live IF-### row (retired/renumbered){}: {}".format(
                len(unknown),
                IF_TC_ALLOW,
                " — first 5" if len(unknown) > 5 else "",
                shown,
            )
        )
    if grown:
        # GROWTH IS REPORTED EVEN WHEN EVERY ADDITION IS REASONED, because the
        # list's declared direction is DOWN. A reasoned addition is legitimate
        # and still worth a sitting's attention; an unreasoned one suppresses
        # nothing (see `read_if_tc_allow`) and is named here rather than
        # vanishing silently.
        unreasoned = [i for i, reason in grown if not reason]
        out.append(
            "{} {} entr{} stand past the declared seed of {} — the list is a "
            "burn-down, so growth is a sitting's business{}: {}".format(
                len(grown),
                IF_TC_ALLOW,
                "y" if len(grown) == 1 else "ies",
                seed,
                " ({} carr{} no reason and therefore suppress nothing)".format(
                    len(unreasoned), "ies" if len(unreasoned) == 1 else "y"
                )
                if unreasoned
                else "",
                ", ".join(i for i, _ in grown[:5]),
            )
        )
    stale = sorted(i for i in allow if i in tc_cited)
    if stale:
        shown = ", ".join(stale[:5])
        out.append(
            "{} {} entries are now cited by a TC — prune them (burn-down "
            "progress, never a defect){}: {}".format(
                len(stale), IF_TC_ALLOW, " — first 5" if len(stale) > 5 else "", shown
            )
        )
    return out


def if_tc_allow_parse_findings(root):
    """PARSE HONESTY for `docs/if-tc-coverage-allow`, the
    `kernel_allow_parse_findings` idiom (WI-519): a declaring line the grammar
    cannot read is an explicit finding naming it, not a silent drop — the
    other half of "declares nothing" is that it also grants no exemption, and
    a malformed line that still reads like a live entry to a human is the
    state most worth reporting. Reported at the FIRST unparsed line with a
    count, not all of them, for the same reason `provenance_allow_parse_findings`
    does: the fix is the same edit for every one.

    Shares `if_tc_coverage_findings`' `[checks] interfaces_check` opt-out —
    deliberately NOT its ≤1-module arch-map vacuity, unlike that function and
    `if_tc_allow_hygiene_findings`: a malformed line is a fact about the FILE,
    not about whether the tree is currently large enough for the coverage
    rule to have anything to say, the same reasoning
    `kernel_allow_parse_findings` gives for riding only `components_check`
    and not the top-view bound."""
    if not read_interfaces_check_enabled(root):
        return []
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return []
    _entries, _seed, unparsed = _parse_if_tc_allow_full(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    if not unparsed:
        return []
    lineno, line = unparsed[0]
    return [
        "{}:{}: this line DECLARES a seam-TC exception and the grammar cannot "
        "read it ({} such line(s)) — `{}`. An entry's first token is an "
        "IF-### id, optionally followed by ` — <reason>`; a token that does "
        "not parse as IF-### suppresses nothing".format(
            IF_TC_ALLOW, lineno, len(unparsed), line[:80]
        )
    ]


# --- Implements-tag vs CodeSymbol crosscheck (WI-502; OI-53 ruled (d)) --------
# The 2026-08-21 closing review found the CodeSymbol dozen (WI-501) by hand:
# resolve every `Implements:` tag's ENCLOSING def/class and compare it against
# its row's `CodeSymbol`/`Module` claim. This promotes that manual method into
# a continuous warn-first finding, so the next stale batch is measured rather
# than rediscovered by campaign. WARN-FIRST FOREVER by the ruling — no
# allowlist, no `--strict` arm — because it checks a TRACED, not APPROVED,
# cell (process.md §8's `Module`/`CodeSymbol`/`TestRefs` "traced, not
# approved" posture, cited at check_trajectory.py:77) and a mismatch is
# routine drift, not a defect to gate a commit over.
#
# ONE HOME for the AST walk (WI-486): `gen_arch_map.implements_report` builds
# the (tag site -> enclosing symbol) map and the known-symbol-name set; this
# function only compares them against the registry, the way `arch_inventory`
# already consumes `gen_arch_map.scan_inventory` rather than re-walking trees.
_CODESYMBOL_SPLIT_RE = re.compile(r"[/;]|\s\+\s")


def _codesymbol_candidates(cell):
    """A `CodeSymbol` cell's symbol names, trimmed. `CodeSymbol` is authored
    prose-adjacent, not a strict machine grammar — measured across the live
    registry it mixes `/` (`run/classify`), `;` (`tier_legend...; STATUS_GLYPH`)
    and a spaced ` + ` (`PHASE_ACCENTS + _ring_ink`) as the same "and also"
    join, sometimes in one cell. Splitting on all three costs nothing when a
    candidate is real prose rather than a name — an unmatched fragment simply
    never satisfies containment — and undercounts nothing a single-character
    splitter would have caught, so the wider split is the conservative one."""
    return [c.strip() for c in _CODESYMBOL_SPLIT_RE.split(cell or "") if c.strip()]


def _codesymbol_site_finding(
    rid, site, qualname, module_cell, code_symbol_cell, module_ok, known_names
):
    """One `codesymbol_crosscheck_findings` tag site, resolved to a finding
    string or `None` — split out so the caller's loop stays a plain walk
    (C901) and this comparison, the actual rule, reads as one thing. See
    `codesymbol_crosscheck_findings` for the containment/mismatch/unresolvable
    vocabulary this implements."""
    candidates = _codesymbol_candidates(code_symbol_cell)
    if not candidates:
        contained = module_ok and qualname == ""
    else:
        # Containment reads BOTH directions of the dotted path: a cell naming
        # the CLASS (`RoutingState`) is a prefix of a method's qualname, but
        # the registry just as often names the bare METHOD (`stall_verdict`,
        # no `RoutingState.` qualifier) — the rendered map's own `methods` row
        # lists them unqualified, and most live CodeSymbol cells follow that
        # convention. A suffix match covers that shape without opening the
        # door to a coincidental same-named method on an unrelated class:
        # `Foo.stall_verdict` and `Bar.stall_verdict` both satisfy a bare
        # `stall_verdict` cell, which is the map's own granularity limit, not
        # one this rule invents.
        contained = module_ok and any(
            qualname == c or qualname.startswith(c + ".") or qualname.endswith("." + c)
            for c in candidates
        )
    if contained:
        return None
    enclosing = qualname or "(module scope)"
    resolvable = any(
        c == n or n.endswith("." + c) for c in candidates for n in known_names
    )
    if candidates and not resolvable:
        return (
            "{} tag at {} encloses `{}`, but the row's CodeSymbol `{}` does "
            "not resolve to any def/class under the scanned source — "
            "unresolvable, not matched (Module `{}`)".format(
                rid, site, enclosing, code_symbol_cell, module_cell
            )
        )
    return "{} tag at {} encloses `{}`, but the row's CodeSymbol claims `{}` (Module `{}`)".format(
        rid, site, enclosing, code_symbol_cell or "(module-only)", module_cell
    )


def codesymbol_crosscheck_findings(root):
    """Every live LLR's `Implements:` tag site under the declared arch-map
    source surface (`docs/stack.ini` `[paths] src`), checked by CONTAINMENT
    against its row's `CodeSymbol` + `Module` cells: a tag inside
    `RoutingState.note_session` satisfies a cell naming `RoutingState`; a tag
    at module scope satisfies a module-only (empty `CodeSymbol`) cell. Two
    finding shapes, distinguished so a reader (and the regression tests) can
    tell "the cell names a different REAL symbol" from "the cell names
    nothing resolvable at all" (a function-local variable, or a symbol that
    is simply gone) — the WI-429 census defect this crosscheck is built to
    keep from recurring silently:

    - **mismatch**: at least one of the cell's candidate names IS a real
      def/class somewhere in the scanned surface, just not one that contains
      this tag's site.
    - **unresolvable**: none of the cell's candidate names resolve to any
      real def/class anywhere in the surface — the cell cannot be verified,
      and reporting it as a silent match would be the false-quiet defect
      `docs/enforcement-audit.md` item 5 already names for a neighboring
      grammar (`Contracts:`); this rule does not inherit that shape.

    `[]` (vacuous) when `[arch-map] mode = files` (no parser) or the LLR
    registry has no `Module`/`CodeSymbol` cells to compare against. A tag
    naming an id with no live LLR row, or an LLR id with an empty `Module`
    AND `CodeSymbol` (nothing claimed), is silently skipped — orphan/schema
    integrity is `trace.py`'s finding, not this one's."""
    if gen_arch_map is None:
        return []
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    if not src_dir.exists():
        return []
    rows = {}
    for r in spine_carrier.load(root / LLR_CSV, "LLR-ID"):
        lid = (r.get("LLR-ID") or "").strip()
        if not lid.startswith("LLR-") or lid.endswith("-000"):
            continue
        module_cell = (r.get("Module") or "").strip()
        code_symbol_cell = (r.get("CodeSymbol") or "").strip()
        if module_cell or code_symbol_cell:
            rows[lid] = (module_cell, code_symbol_cell)
    if not rows:
        return []
    sites, known_names = gen_arch_map.implements_report([src_dir])
    findings = []
    for rel, tags in sorted(sites.items()):
        file_module = _norm_module(rel)
        for lineno, ids, qualname in tags:
            for rid in ids:
                if rid not in rows:
                    continue
                module_cell, code_symbol_cell = rows[rid]
                declared_modules = {_norm_module(m) for m in _split_refs(module_cell)}
                module_ok = not declared_modules or file_module in declared_modules
                finding = _codesymbol_site_finding(
                    rid,
                    "{}:{}".format(rel, lineno),
                    qualname,
                    module_cell,
                    code_symbol_cell,
                    module_ok,
                    known_names,
                )
                if finding:
                    findings.append(finding)
    return findings


# --- the How-SW top-view right-sizing rule (WI-073/FB5) ------------------------
# The software-architecture diagram's first view is bounded at TOP_VIEW_MAX
# items = top-level components (a CMP with no PartOf that contains ≥1 arch-map
# module) + uncontained modules. Membership derives from the AXES join: a
# `Component` tag on an LLR joins LLR.Module → CMP-###; CMP nesting via PartOf.
# The derivation below is the ONE home for that join — gen_trajectory imports it
# (`ct.component_top_view`) so the render and this rule can never disagree on the
# count. Small stable loaders duplicated per the F5 convention (no sibling import
# into check_trajectory).


def load_cmps(rows):
    """Real (non-`-000`) CMP-### component rows as dicts (id, name, category,
    partof). Lenient — `trace.py` owns CMP integrity; a malformed id is skipped
    here, since this only feeds the warn-first top-view coverage."""
    out = []
    for r in rows:
        cid = (r.get("CMP-ID") or "").strip()
        if not CMP_ID_RE.match(cid) or cid.endswith("-000"):
            continue
        out.append(
            {
                "id": cid,
                "name": (r.get("Name") or "").strip(),
                "category": (r.get("Category") or "").strip(),
                "partof": [p for p in _split_refs(r.get("PartOf", "")) if p],
            }
        )
    return out


def _cmp_roots(cmps):
    """`{cmp id: set(top-level root ids)}` — walk `PartOf` upward to the root(s)
    (a CMP with no real PartOf is its own root). A PartOf parent that names no
    real CMP is ignored (trace.py flags it separately). Cycle-guarded (a `seen`
    frontier), so a pathological PartOf cycle degrades to the CMP itself rather
    than looping."""
    by_id = {c["id"]: c for c in cmps}
    roots = {}
    for c in cmps:
        seen, frontier, out = set(), [c["id"]], set()
        while frontier:
            n = frontier.pop()
            if n in seen:
                continue
            seen.add(n)
            parents = [p for p in by_id.get(n, {}).get("partof", []) if p in by_id]
            if parents:
                frontier.extend(parents)
            else:
                out.add(n)
        roots[c["id"]] = out or {c["id"]}
    return roots


def module_components(root):
    """`{normalized module key: set(real-looking CMP ids)}` from the LLR
    `Component` tags joined on `LLR.Module` — the AXES membership rule (a module
    belongs to the CMP(s) its LLRs are tagged with). Empty when the LLR registry
    has no `Component` column (legacy) or no tags, so it costs a non-adopter
    nothing. The tag set is left unfiltered against the CMP registry here; the
    caller intersects with the real ids (a phantom tag is trace.py's finding)."""
    out = {}
    for r in spine_carrier.load(root / LLR_CSV, "LLR-ID"):
        lid = (r.get("LLR-ID") or "").strip()
        if not lid.startswith("LLR-") or lid.endswith("-000"):
            continue
        tags = {t for t in _split_refs(r.get("Component", "")) if t.startswith("CMP-")}
        if not tags:
            continue
        # `Module` is a `;`-JOINED LIST, and this reader has to split it (WI-429).
        # It did not, and the bug is the D-6 failure mode exactly: an unsplit
        # `a.py;b.py` normalized to one nonsense key, so a row spanning two
        # modules tagged NEITHER of them — silently, because a membership map
        # that is missing an entry reads identically to a module nobody tagged.
        # The kit's other readers of this cell (`check_doc_refs.SPINE_CELLS`,
        # trace's back-link resolution) already split it; this one had not
        # learned the shape, and 2 live rows were losing their tags before the
        # WI-429 repair widened the same cells to 13.
        for part in _split_refs(r.get("Module", "")):
            key = _norm_module(part)
            if key:
                out.setdefault(key, set()).update(tags)
    return out


def component_top_view(root):
    """The How-SW containment derivation (WI-073), shared by the right-sizing
    rule and the dashboard render so the item count and the picture never
    disagree. Returns a dict:
      inventory    `{norm: display}` arch-map modules (empty pre-arch-map)
      cmps         `[cmp dict]` real CMP rows
      by_id        `{cmp id: cmp dict}`
      children_of  `{cmp id: sorted[child cmp ids]}` (PartOf inverted)
      roots_of     `{cmp id: set(top-level root ids)}` (PartOf resolved up)
      module_cmps  `{norm: set(finest real CMP ids tagged on its LLRs)}`
      module_roots `{norm: set(top-level root ids)}` (derived, real modules only)
      top_roots    sorted `[cmp id]` top-level roots containing ≥1 module
      uncontained  sorted `[norm]` inventory modules with no membership
      count        `len(top_roots) + len(uncontained)`

    Implements: SR-159, LLR-049
    """
    names = arch_inventory(root)[0]
    inventory = {}
    for m in names:
        n = _norm_module(m)
        if n:
            inventory.setdefault(n, m)
    cmps = load_cmps(spine_carrier.load(root / CMP_CSV, "CMP-ID"))
    by_id = {c["id"]: c for c in cmps}
    cmp_ids = set(by_id)
    roots_of = _cmp_roots(cmps)
    children_of = {c["id"]: [] for c in cmps}
    for c in cmps:
        for p in c["partof"]:
            if p in by_id:
                children_of[p].append(c["id"])
    for cid in children_of:
        children_of[cid] = sorted(children_of[cid])

    raw = module_components(root)
    module_cmps, module_roots = {}, {}
    top_roots, uncontained = set(), []
    for n in sorted(inventory):
        tags = raw.get(n, set()) & cmp_ids
        module_cmps[n] = tags
        if not tags:
            uncontained.append(n)
            module_roots[n] = set()
            continue
        r = set()
        for c in tags:
            r |= roots_of[c]
        module_roots[n] = r
        top_roots |= r
    return {
        "inventory": inventory,
        "cmps": cmps,
        "by_id": by_id,
        "children_of": children_of,
        "roots_of": roots_of,
        "module_cmps": module_cmps,
        "module_roots": module_roots,
        "top_roots": sorted(top_roots),
        "uncontained": uncontained,
        "count": len(top_roots) + len(uncontained),
    }


def knowledge_packs(root):
    """Real knowledge-pack labels under `docs/knowledge/` (research-knowledge.md
    §3a) — every `*.md` except the scaffolded `README.md` index. Empty (a
    non-adopter, an absent dir, or the index alone) means the knowledge layer is
    not in use, so the knowledge⇒component coupling stays dormant. Sorted for a
    deterministic count/message."""
    d = root / "docs" / "knowledge"
    if not d.is_dir():
        return []
    return sorted(p.stem for p in d.glob("*.md") if p.name.lower() != "readme.md")


# --- the declared arch-map scan profile -------------------------------------
# (The WI-399 committed-vs-disk delta machinery that lived here —
# _has_internal_import / _would_be_inventoried / shipped_modules /
# added_module_findings — RETIRED at WI-455: arch_inventory reads the live
# source tree, so the delta it bridged no longer exists.)


def _stack_ini_get(root, section, option):
    """ONE lenient docs/stack.ini read (absent file / broken profile / missing
    option all → None), shared by `_arch_scan_profile` and `_tests_dir` so the
    idiom has a single home here — check.py owns the loud parse of the same
    profile."""
    ini = root / "docs" / "stack.ini"
    if not ini.exists():
        return None
    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read_string(ini.read_text(encoding="utf-8", errors="replace"))
        if cp.has_option(section, option):
            return cp.get(section, option).strip()
    except configparser.Error:
        pass
    return None


def _arch_scan_profile(root):
    """`(src, mode)` from docs/stack.ini — the same `[paths] src` and
    `[arch-map] mode` check.py hands gen_arch_map — read leniently
    (`_stack_ini_get`): an absent or broken profile degrades to the defaults
    (`src`, `symbols`) rather than crashing a warn-tier rule."""
    return (
        _stack_ini_get(root, "paths", "src") or "src",
        _stack_ini_get(root, "arch-map", "mode") or "symbols",
    )


def _declared_seam_pairs(root):
    """The IF registry's endpoint pairs, normalized and stored BOTH ways — a
    seam is one declared relationship, whichever side authored the row.

    A MULTI-ENDPOINT SIDE IS SEVERAL ENDPOINTS, and every combination is a
    declared pair. `trace.py` has split on `;` since IF-097 (the comment there
    names it); this reader did not, so the two readers of the same cells
    disagreed — 14 of 249 pairs carried an unsplit, non-existent module name as
    an endpoint after WI-469 took the population from one row to seven
    (2026-08-21 review, M-14). Latent, but the failure it sets up is expensive
    in the wrong direction: a real cross-component import whose seam row plainly
    names both modules is reported as having no declared seam, and the cheapest
    fix available to that author is to duplicate or delete a correct row.

    PAIRS ARE TAKEN ACROSS THE ROW'S WHOLE ENDPOINT SET since WI-455, not across
    two named cells. On a row whose consumers are a measured READER SET over one
    medium (`IF-029`, `IF-035`, `IF-037`, `IF-047`, `IF-072`) that is what keeps
    the reader-to-reader pairs the two-cell shape used to produce, now stated as
    what they always were: one declared relationship among all of the seam's
    endpoints."""
    covered = set()
    for r in load_seams(root):
        ends = _norm_endpoints([r["owner"]] + r["far"])
        for a in ends:
            for b in ends:
                if a != b:
                    covered.add((a, b))
                    covered.add((b, a))
    return covered


def _norm_endpoints(endpoints):
    """The normalized module keys of an endpoint list, empties dropped — so a
    blank side contributes no pair, exactly as before. Each entry may itself be
    a `;`-joined cell (`kitlib.spine.seam_endpoints` splits those): an endpoint
    may legitimately contain a space (`external:downstream adopter`) or a
    comma, so `;` stays the only separator."""
    out = []
    for endpoint in endpoints:
        for part in _kitspine.seam_endpoints(endpoint):
            normalized = _norm_module(part)
            if normalized:
                out.append(normalized)
    return out


def _parse_kernel_allow(root):
    """`(entries, unparsed)` for `docs/kernel-modules-allow` — the whole parse,
    both halves, the `docs/provenance-allow` split (`trace.read_provenance_allow`):
    `entries` is `[(normalized module key, reason, lineno)]`; `unparsed` is
    `[(lineno, line)]` for every DECLARING line the grammar dropped, so a
    malformed entry is reported rather than silently read as an empty file
    (`kernel_allow_parse_findings`).

    Grammar: one non-blank, non-`#`-comment line per entry, `<module path> —
    <reason>` (an em dash, space each side — the same separator
    `docs/provenance-allow` uses). A REASON IS REQUIRED, unlike
    `docs/if-tc-coverage-allow`'s migration seed: OI-48's reuse provision is
    a deliberate recorded act every time, never a bare-baseline default, so
    there is no seeded-population exception here. A line with no separator,
    or an empty module or reason on either side of it, DECLARES NOTHING — it
    is dropped (fail-safe: absence of a valid declaration grants no
    exemption) and counted as unparsed."""
    path = Path(root) / KERNEL_ALLOW
    if not path.is_file():
        return [], []
    out, unparsed = [], []
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if KERNEL_ALLOW_SEP not in line:
            unparsed.append((lineno, line))
            continue
        head, reason = line.split(KERNEL_ALLOW_SEP, 1)
        module = _norm_module(head.strip())
        reason = reason.strip()
        if not module or not reason:
            unparsed.append((lineno, line))
            continue
        out.append((module, reason, lineno))
    return out, unparsed


def read_kernel_modules(root):
    """`{normalized module key: reason}` — the declared shared-kernel surface
    (OI-48 ruled (d), 2026-08-21; executed WI-494). Absent file, or a file
    with no parseable entries: empty dict — the FAIL-SAFE DEFAULT the ruling
    requires, since an empty mapping exempts nothing and every edge stays
    policed by the ordinary cross-component rule.

    `_cross_component_scan` treats an import edge whose DESTINATION resolves
    into this set as not a seam at all — neither a finding nor the
    multi-membership advisory — because the module is a declared shared
    kernel: consumed across components BY DESIGN, and re-declaring that fact
    edge-by-edge (the WI-064 seam registry) would restate "everyone imports
    the shared helper" once per caller (OI-48's option (b), priced and
    declined). The exemption is ONE-DIRECTIONAL: an edge OUT of a kernel
    module — a kernel module importing a non-kernel sibling — is not
    exempted here and stays fully policed, because a shared kernel importing
    outward is the one shape a layered system forbids regardless of who
    calls it (WI-448's dedicated bootstrap-manifest test polices the literal
    kitlib case already; this rule polices any OTHER declared kernel the
    same way going forward).

    NEVER A KITLIB HARDCODE — the reuse provision's whole point: any future
    shared module whose real consumers span components takes this same
    declared path, one entry, one recorded reason, a deliberate act rather
    than a default."""
    return {module: reason for module, reason, _ in _parse_kernel_allow(root)[0]}


def kernel_allow_parse_findings(root):
    """PARSE HONESTY for `docs/kernel-modules-allow`, the
    `provenance_allow_parse_findings` idiom: a declaring line the grammar
    cannot read is an explicit finding naming it, not a silent drop — the
    other half of "declares nothing" is that it also grants no exemption,
    and a malformed line that still reads like a live entry to a human is
    the state most worth reporting. Reported at the FIRST unparsed line with
    a count, not all of them, for the same reason `provenance_allow_parse_findings`
    does: the fix is the same edit for every one.

    Shares `component_findings`' WARN-plain / ERROR-under-`--strict`
    promotion and its `[checks] components_check` opt-out — this file is
    part of the components layer, not a spine-integrity surface, so it rides
    that gate rather than the always-on floor `docs/provenance-allow` uses."""
    _entries, unparsed = _parse_kernel_allow(root)
    if not unparsed:
        return []
    lineno, line = unparsed[0]
    return [
        "{}:{}: this line DECLARES a kernel module and the grammar cannot "
        "read it ({} such line(s)) — `{}`. An entry is `<module path>{}"
        "<reason>` and BOTH fields are required — a bare module path or a "
        "missing separator suppresses nothing".format(
            KERNEL_ALLOW, lineno, len(unparsed), line[:80], KERNEL_ALLOW_SEP
        )
    ]


def _classifiable_edges(root):
    """Yield `(src, dst, src_cmps, dst_cmps)` for every internal import edge
    the cross-CMP rules can classify — both endpoints normalized, both carrying
    at least one REAL CMP membership.

    The vacuity guards live here, so every caller inherits them: no arch-map
    `Imports (internal):` lines, no real CMP rows, an endpoint with no
    `Component`-tag membership (coverage is the containment rule's job, not
    this one's), or an import stem that resolves to no/multiple inventory
    modules."""
    names, _contracts, imports = arch_inventory(root)
    if not imports:
        return
    cmp_ids = {c["id"] for c in load_cmps(spine_carrier.load(root / CMP_CSV, "CMP-ID"))}
    if not cmp_ids:
        return
    raw = module_components(root)
    membership = {n: tags & cmp_ids for n, tags in raw.items()}
    # A bare imported stem (`agent_route`) resolves against the inventory's
    # normalized module names (`scripts/agent_route`) by unique-stem match —
    # the same resolution gen_arch_map applied when it emitted the line.
    by_stem = {}
    for m in names:
        n = _norm_module(m)
        if n:
            by_stem.setdefault(n.rsplit("/", 1)[-1], set()).add(n)
    for src in sorted(imports):
        src_n = _norm_module(src)
        src_cmps = membership.get(src_n, set())
        if not src_cmps:
            continue
        for stem in sorted(imports[src]):
            targets = by_stem.get(stem, set())
            if len(targets) != 1:
                continue  # unknown/ambiguous stem — not this rule's finding
            dst_n = next(iter(targets))
            dst_cmps = membership.get(dst_n, set())
            if dst_cmps:
                yield src_n, dst_n, src_cmps, dst_cmps


_SCAN_CACHE = {}


def _cross_component_scan(root):
    """`(findings, advisories)` over the classifiable import edges — the two
    tiers of the cross-CMP rule, computed in ONE pass so they can never disagree
    about which edge is which.

    A **finding** (unchanged since WI-064) is an edge whose endpoint component
    sets are DISJOINT and which no declared IF-### row covers.

    An **advisory** (WI-440, OI-14) is an edge the overlap guard SUPPRESSES only
    because an endpoint is tagged into more than one component: the sets
    intersect, no IF row covers the pair, and `len(cmps) > 1` somewhere. That
    edge would be a finding under a partition where each module belongs to one
    component, so the multi-membership is EVIDENCE ABOUT THE PARTITION (the file
    splits, the shared part is its own component, or the boundary is drawn
    wrong) rather than a licence to stay quiet. Reporting it reverses the
    direction of the old rule, where authoring one more `Component` tag
    monotonically silenced the check — a fail-open the author controls.

    An edge whose endpoints are single-tagged into the SAME component is
    ordinary intra-component wiring and is neither.

    A THIRD, EARLIER exit (OI-48 ruled (d), WI-494): an edge whose
    DESTINATION is a declared shared-kernel module (`read_kernel_modules`) is
    not a seam at all — neither a finding nor the multi-membership advisory.
    Checked before the overlap split, so a kernel module that still carries a
    residual multi-tag is not ALSO advised about (the advisory exists to
    surface undeclared candidates; a module already declared kernel is a
    settled candidate, not an open one). One-directional by construction —
    the exemption keys on `dst_n`, never `src_n`, so an edge OUT of a kernel
    module stays exactly as policed as any other edge.

    ONE scan per run, cached per root: the two public wrappers used to each
    trigger their own scan from `main`, so the two tiers were computed from two
    separate reads of the same registries — the exact could-disagree state this
    function's contract forbids (and a review round demonstrated with a
    mid-run registry change). The cache makes the docstring's "computed in ONE
    pass" literally true for the process's lifetime.
    """
    cached = _SCAN_CACHE.get(str(root))
    if cached is not None:
        return cached
    # `covered` and `kernel` are resolved LAZILY: with zero classifiable edges
    # the old rule never read interfaces.csv (or now kernel-modules-allow) at
    # all, and an unreadable file must not turn a vacuous scan into a crash
    # (review finding, extended to the new surface for the same reason).
    covered = None
    kernel = None
    findings, advisories = [], []
    for src_n, dst_n, src_cmps, dst_cmps in _classifiable_edges(root):
        if covered is None:
            covered = _declared_seam_pairs(root)
        if (src_n, dst_n) in covered:
            continue
        if kernel is None:
            kernel = read_kernel_modules(root)
        if dst_n in kernel:
            continue
        edge = "{} ({}) -> {} ({})".format(
            src_n,
            "/".join(sorted(src_cmps)),
            dst_n,
            "/".join(sorted(dst_cmps)),
        )
        if src_cmps & dst_cmps:
            multi = [m for m, c in ((src_n, src_cmps), (dst_n, dst_cmps)) if len(c) > 1]
            if multi:
                advisories.append(
                    "multi-component module(s) {} suppress the cross-component "
                    "seam rule on import {} — the shared tag, not a declared "
                    "IF-### row, is what silences this edge; split the module, "
                    "give the shared part its own component, or declare the "
                    "seam in {} (advisory only — never the exit "
                    "code)".format(", ".join(multi), edge, IF_CSV)
                )
            continue
        findings.append(
            "cross-component import {} has no declared IF-### seam — declare "
            "the interface row in {} or retag the membership, or set "
            "docs/process.toml [checks] components_check = false".format(edge, IF_CSV)
        )
    _SCAN_CACHE[str(root)] = (findings, advisories)
    return findings, advisories


def cross_component_findings(root):
    """The cross-CMP-edge-without-IF rule (WI-064; the AXES approved model's
    "Enforceability" ruling, process-options.md "Component layer"): an internal
    import edge whose endpoints belong to *different* CMP-### components must be
    covered by a declared IF-### row — an undeclared cross-component coupling is
    a finding, mechanized from the same committed artifacts the other component
    rules read. The CALLER gates the opt-out (`component_findings` shares
    `[checks] components_check`) and the WARN-plain / ERROR-under-`--strict`
    promotion. See `_cross_component_scan` for the tier split (this is tier one)
    and `_classifiable_edges` for the vacuity guards this rule inherits —
    including the DELIBERATE vacuousness for an endpoint carrying no
    `Component` tag, which stays the containment rule's job, not this one's.
    Since OI-48 (WI-494) an edge into a declared shared-kernel module
    (`read_kernel_modules`, `docs/kernel-modules-allow`) is exempted here
    before either tier — see `_cross_component_scan`'s "THIRD, EARLIER exit".

    Implements: SR-159, LLR-067
    """
    return _cross_component_scan(root)[0]


def cross_component_advisories(root):
    """The multi-membership overlap advisory (WI-440, OI-14's third
    do-not-wait): the edges the overlap guard silences because an endpoint
    carries more than one `Component` tag — see `_cross_component_scan`.

    WARN-ONLY, never the exit code, not even under `--strict`: this reports a
    question about the PARTITION, and no partition has been ruled yet, so it
    must not block. Shares `component_findings`' `[checks] components_check`
    opt-out, which the caller does NOT gate for it — this function does."""
    if not read_components_check_enabled(root):
        return []
    return _cross_component_scan(root)[1]


def component_findings(root):
    """The How-SW component-coverage finding(s) (process-options.md "Component
    layer"). Returns the finding strings ([] when opted out or clean). The caller
    prints them WARN plain and promotes them to ERROR under `--strict` (DevStg-Tests+).
    Opt-out via `[checks] components_check = false`. Five rules, all off the arch-map ⇒
    CMP join:

    - **Top-view right-sizing** (WI-073/FB5): vacuous when the arch-map inventory
      has ≤ TOP_VIEW_MAX modules (a small or pre-arch-map repo can never exceed the
      bound — the bound, not the registry, is the rule). Only when the inventory
      itself is larger than the bound do the declared components decide: a
      right-sized handful of top-level CMPs brings the top view back under it.
    - **Knowledge⇒component coupling** (WI-153; research-knowledge.md §3a,
      owner-ruled 2026-07-14): when ≥1 knowledge pack exists the component web is
      *expected* — any arch-map module the CMP join leaves uncontained is a finding
      regardless of the bound, because packs tie the *what* to the knowledge behind
      the *how* and that web must be robust wherever packs are enabled. Arms the
      existing join from pack presence; invents no new join, and is dormant (no
      cost to a non-adopter) until `docs/knowledge/` holds a real pack.
    - (The WI-399 "containment owed where a module is ADDED" delta rule is
      RETIRED — WI-455 made the inventory the LIVE source tree, so a lane's
      added module is simply IN the inventory and the coupling rule above
      fires on it directly; there is no committed-vs-disk gap left to bridge.)
    - **Cross-CMP edges need a declared seam** (WI-064): see
      `cross_component_findings` — an import edge between two components with
      no covering IF-### row. Its warn-only sibling
      `cross_component_advisories` (WI-440) reports the edges a multi-tagged
      endpoint silences; main() prints those, not this function, because they
      must never reach the exit code. An edge into a declared shared-kernel
      module (OI-48 (d), WI-494) is exempted from BOTH before either can fire
      — see `_cross_component_scan`.
    - **Declared-kernel allowlist hygiene** (OI-48 (d), WI-494): see
      `kernel_allow_parse_findings` — a `docs/kernel-modules-allow` line the
      grammar cannot read (missing module, missing reason, or no separator)
      is reported, the same parse-honesty shape
      `if_tc_allow_hygiene_findings` and `provenance_allow_parse_findings`
      use for their own allow-files. A malformed line grants no exemption
      either way (fail-safe), so this rule is reporting, never gating, the
      fail-safe default — it just says so out loud instead of leaving the
      author to notice a seam finding that did not go away.

    Implements: SR-159, LLR-049
    """
    if not read_components_check_enabled(root):
        return []
    view = component_top_view(root)
    out = []
    packs = knowledge_packs(root)
    if packs and view["inventory"] and view["uncontained"]:
        # The module NAMES ride in the finding (capped): the retired WI-399
        # delta message carried them so a lane knew WHICH file to tag, and
        # under the live inventory (WI-455) this rule is that lane's first
        # and only firing point.
        shown = ", ".join(view["uncontained"][:8]) + (
            ", …" if len(view["uncontained"]) > 8 else ""
        )
        out.append(
            "docs/knowledge/ holds {} pack(s) but {} arch-map module(s) are in no "
            "CMP-### component ({}); tag them via LLR `Component` cells in {} so "
            "the knowledge⇒component web is complete, or set docs/process.toml "
            "[checks] components_check = false".format(
                len(packs), len(view["uncontained"]), shown, CMP_CSV
            )
        )
    if len(view["inventory"]) > TOP_VIEW_MAX and view["count"] > TOP_VIEW_MAX:
        out.append(
            "How-SW top view has {} items ({} top-level component(s) + {} "
            "uncontained module(s)) — exceeds the bound of {}; declare CMP-### "
            "components in {} to contain modules (nest with PartOf), or set "
            "docs/process.toml [checks] components_check = false".format(
                view["count"],
                len(view["top_roots"]),
                len(view["uncontained"]),
                TOP_VIEW_MAX,
                CMP_CSV,
            )
        )
    out.extend(cross_component_findings(root))
    out.extend(kernel_allow_parse_findings(root))
    return out


# --- specs act on declared interface boundaries (WI-191) -----------------------
_IF_TOKEN_RE = re.compile(r"\bIF-\d+\b")
_INTERFACES_HEADING_RE = re.compile(r"(?im)^[ \t]*##[ \t]+Interfaces\b.*$")
# The intra-module escape hatch (PROCESS.md §8 scoping): a spec whose WIs act only
# within one module states that instead of inventing a seam.
_INTRA_MODULE_RE = re.compile(
    r"intra-module|single-module|no (?:cross-module )?seam|no interface|no cross-module",
    re.I,
)


def _spec_interfaces_section(text):
    """The body of a spec's `## Interfaces` section (between that heading and the
    next `## ` heading / EOF), or None when the spec has no such heading — the
    unarmed case that keeps the check vacuous-until-armed."""
    m = _INTERFACES_HEADING_RE.search(text)
    if not m:
        return None
    rest = text[m.end() :]
    nxt = re.search(r"(?m)^[ \t]*##[ \t]+", rest)
    return rest[: nxt.start()] if nxt else rest


def _armed_specs(root):
    """The live `docs/specs/` files that are real specs-of-record, sorted.

    The skip rule is a POLICY — the specs README documents the convention in
    prose and `WI-000` is the inert example, so neither is an armed spec — and it
    was stated at both walk sites. WI-344's `spec-scan` block; stating it once
    means a change to what counts as armed cannot land in one checker and not the
    other. Empty (never an error) when there is no specs dir."""
    specs = root / SPECS_DIR
    if not specs.is_dir():
        return []
    return [
        path
        for path in sorted(specs.glob("*.md"))
        if path.name.lower() != "readme.md" and not path.stem.endswith("-000")
    ]


def spec_interface_findings(root):
    """WI-191 — a spec-of-record acts on DECLARED interface boundaries. A spec's
    `## Interfaces` section must cite only IF-### seams that resolve in
    `interfaces.toml` (the one seam home, PROCESS.md §8). WARN plain / ERROR
    under `--strict` (DevStg-Tests+), like `component_findings`; the caller owns
    that promotion.

    THE ANTI-DUPLICATION ARM RETIRED AT WI-442, AND IT IS NOT A SILENT DROP.
    Until decision 4 this function also demanded a rationale on the citation line
    of any `Stability = Experimental` seam — the forced nearest-existing-IF
    search. Its arming input was DELETED: the slimmed tier has one maturity
    field with two values, and neither means what `Experimental` meant ("proposed
    and not yet pinned by a second consumer"). Re-keying onto `approval ==
    "draft"` was the obvious move and is the WRONG one: it silently changes the
    predicate to "not yet approved", which on this repo's registry arms 113 of
    113 rows instead of 5, and it does so at a severity that ERRORS under
    --strict. A rule whose blast radius multiplies twentyfold while its sentence
    stays the same is not the same rule.

    So the arm is GONE rather than approximated, and its loss is a recorded
    finding of the re-tier (log entry, WI-442) with a home at sitting 3: if the
    forced search is worth keeping, it needs a value that means "proposed",
    which is a vocabulary decision (D-9/decision 12), not a checker's to invent.

    **Vacuous-until-armed:** a spec with no `## Interfaces` heading is skipped, so
    existing specs and downstream repos stay green until they adopt the section.
    An armed section that cites no resolvable IF-### AND states no intra-module
    escape (PROCESS.md §8) is itself a finding — an empty-ceremony section."""
    specs = root / SPECS_DIR
    if not specs.is_dir():
        return []
    if_rows = {r["id"]: r for r in load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))}
    out = []
    for path in _armed_specs(root):
        section = _spec_interfaces_section(
            path.read_text(encoding="utf-8", errors="replace")
        )
        if section is None:
            continue  # unarmed — no `## Interfaces` section
        rel = "{}/{}".format(SPECS_DIR, path.name)
        ids = list(dict.fromkeys(_IF_TOKEN_RE.findall(section)))
        if not ids:
            if not _INTRA_MODULE_RE.search(section):
                out.append(
                    "{}: `## Interfaces` cites no IF-### and states no "
                    "intra-module escape — cite the seam(s) the WI acts on, or "
                    "state the intra-module case (PROCESS.md §8)".format(rel)
                )
            continue
        for iid in ids:
            if iid not in if_rows:
                out.append(
                    "{}: `## Interfaces` cites {} which resolves to no row in "
                    "{}".format(rel, iid, IF_CSV)
                )
    return out


# --- the phase-anchor archetype + phase-drop detector (WI-093) -----------------
# The derived model (docs/archive/specs/derived-gate-model.2026-07-20.md §7/§9.3)
# structures a phase's pre-dev work as a first-class WI whose Title carries a
# phase-anchor tag. The derived bar DROPPING below a phase's last-closed level is
# the signal that new/reopened content entered and a new phase-anchor WI is due;
# the committed anchor is where phase identity + membership live (a git-history
# walk is rebase-sensitive and carries no membership, §9.3). Both checks are
# WARN-FIRST — like the connectivity coverage, they never change the exit code.
#
# RE-KEYED TO THE STAGE AXIS (WI-498 slice 4, ruled plan §5 item 4). The detector
# used to compare a phase's derived BAR against an anchor's internal level 1/2.
# Both halves moved: the current reading now comes from `docs/stage`'s
# `per-phase-live` field through the common reader, and an anchor's recorded reach
# is a LADDER RUNG. The bar axis is out of this module entirely.
#
# THE ANCHOR VOCABULARY, AND WHY THE LEGACY SPELLINGS ARE TRANSLATED RATHER THAN
# RE-RECORDED. A phase anchor is a WI TITLE — a committed record of what a closed
# work item did — so D-4's refusal to re-point history applies exactly as it did
# at the `g1`/`g2` changeover: the ~20 anchors already in `docs/work/complete/`
# stay spelled as they were, and the read side declares the translation.
#
# THE TRANSLATION IS BY MEANING, NOT BY SPELLING, and the two differ by two rungs
# in both rows — which is precisely the trap the stage/bar spelling overlap sets:
#
#   `[p]-[reqs]` / `[p]-[g1]`  requirement structuring: the phase's SRs are  check_vocab: allow
#                              authored AND approved. `spine_stage` clears its
#                              `any(is_drafted(sr))` test from there on, so what
#                              the phase then stands at is DevStg-LLReqs — NOT
#                              DevStg-Reqs, which is the rung it has just LEFT.
#   `[p]-[tests]` / `[p]-[g2]` decomposition: LLRs and TCs authored and  check_vocab: allow
#                              non-Drafted. That clears the LLReqs and Tests
#                              predicates both, so the phase stands at
#                              DevStg-Impl — NOT DevStg-Tests.
#
# So an anchor records THE RUNG THE PHASE STANDS AT ONCE IT CLOSES (slice 2's
# inversion finding, on this axis: a bar value corresponds to the rung at which it
# was reached). Going forward the canonical spelling IS that rung, verbatim:
# `[<phase>]-[DevStg-LLReqs]`, `[<phase>]-[DevStg-Impl]` — stage vocabulary, no
# second word to keep in step, and any rung is expressible rather than just two.
PHASE_ANCHOR_RE = re.compile(
    r"^\[([^\]]+)\]-\[(g[12]|reqs|tests|DevStg-[A-Za-z]+)\]", re.IGNORECASE
)
# Legacy anchor token -> the rung it recorded. Read side only; never authored.
_ANCHOR_REACH = {
    "reqs": _kitladder.STAGE_LLREQS,
    "g1": _kitladder.STAGE_LLREQS,
    "tests": _kitladder.STAGE_IMPL,
    "g2": _kitladder.STAGE_IMPL,
}


def _anchor_reach(token):
    """The rung a phase-anchor token records, or None when the token is
    rung-shaped but names no rung on the ladder.

    A `DevStg-*` token is matched CASE-INSENSITIVELY by the regex above (titles
    are prose), so it is folded back onto the canonical spelling here rather than
    handed to `require_rung`, which is deliberately exact."""
    lowered = token.lower()
    if lowered in _ANCHOR_REACH:
        return _ANCHOR_REACH[lowered]
    for rung in _kitladder.STAGE_ORDER:
        if rung.lower() == lowered:
            return rung
    return None


def phase_stages(root):
    """`{phase-label: rung-or-DevStg-Below}` — the LIVE per-phase stage, read
    through the common reader (`derive_stage.read`, ruled plan §3), or `{}` when
    the stage axis cannot be read at all.

    THE LIVE READING, NOT THE SETTLED ONE, AND THAT IS THE WHOLE DESIGN. This is
    an EVENT detector: its question is "did new or reopened content enter a phase
    that had closed an anchor?", and a Drafted or re-Drafted row IS that event.
    The headline `stage`/`per-phase` fields exclude drafts by construction — slice
    1's C-01 fix, which exists so one draft cannot collapse SELECTION — so they
    cannot see the event at all, by design. `per-phase-live` is where the drafts
    are, and reading it here is what lets selection stay uncollapsed while
    detection stays sharp. (It also answers slice 3's banked tension: rung 3's
    self-reporting recursion, a Drafted component dropping the reported stage, is
    visible on the live reading even though it no longer moves the effective one.)

    THE IMPORT IS LAZY AND DEGRADES TO VACUOUS. This module runs in the shipped
    pre-commit hook, and the `approval-fresh` lesson (130-REVIEW-A) is that a hook
    which hard-requires a sibling an adopter's tree may not have blocks every
    commit. A fixture that copies `check_trajectory.py` alone therefore loses the
    drop half only — the same vacuity an absent `docs/gate` produced before."""
    try:
        import derive_stage
    except ImportError:  # pragma: no cover - exercised via the sys.path fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        try:
            import derive_stage
        except ImportError:
            return {}
    try:
        record = derive_stage.read(Path(root))
    except (OSError, ValueError):
        # A hand-edited or ladder-stale docs/stage RAISES in `kitlib.stage.parse`
        # (its ruled direction). That is the `derived-stage` step's finding to
        # report, not this advisory detector's to crash the hook over.
        return {}
    return dict(record.get("per-phase-live") or {})


def phase_anchors(wis):
    """`({(phase, rung): wi}, [shape-warnings])` — the phase-anchor WIs parsed
    from Titles, over the canonical `[phase]-[DevStg-<Rung>]` spelling and the
    retired `[phase]-[reqs|tests]` / `[phase]-[g1|g2]` ones the committed anchors
    carry (all translated by `_anchor_reach`). A duplicate (phase, rung) anchor —
    including one spelled each way, which is exactly the collision worth catching
    during a changeover — and an anchor whose predecessors omit the next-lower
    anchor of its own phase, are warned (advisory only)."""
    anchors, warns = {}, []
    for w in wis:
        m = PHASE_ANCHOR_RE.match(w["title"])
        if not m:
            continue
        reach = _anchor_reach(m.group(2))
        if reach is None:
            warns.append(
                "phase anchor {} names [{}]-[{}], which is not a rung on the "
                "stage ladder — expected one of {}".format(
                    w["id"], m.group(1), m.group(2), ", ".join(_kitladder.STAGE_ORDER)
                )
            )
            continue
        key = (m.group(1), reach)
        if key in anchors:
            warns.append(
                "duplicate phase anchor [{}]-[{}] ({} and {})".format(
                    key[0], reach, anchors[key]["id"], w["id"]
                )
            )
            continue
        anchors[key] = w
    # THE PREDECESSOR SHAPE RULE, GENERALIZED. It used to be "a `tests` anchor
    # lists its `reqs` anchor", which was expressible only because there were
    # exactly two levels. On a ladder it is "each anchor lists the next-LOWER
    # anchor of its own phase" — the same rule, stated over whatever rungs the
    # phase actually recorded.
    by_phase = {}
    for phase, reach in anchors:
        by_phase.setdefault(phase, []).append(reach)
    for phase, reaches in by_phase.items():
        ordered = sorted(reaches, key=_kitstage.order)
        for higher, lower in zip(ordered[1:], ordered):
            w = anchors[(phase, higher)]
            lower_id = anchors[(phase, lower)]["id"]
            if lower_id not in (w["preds"] + w["soft"]):
                warns.append(
                    "phase anchor {} ([{}]-[{}]) does not list its "
                    "[{}]-[{}] ({}) as a predecessor".format(
                        w["id"], phase, higher, phase, lower, lower_id
                    )
                )
    return anchors, warns


def phase_findings(root, wis):
    """The phase-archetype + phase-drop warns (WI-093; warn-first). Returns the
    warn strings ([] when vacuous — no anchors, or no readable stage axis, the
    single-phase meta case).

    THE DROP RULE. For each phase with a **done** anchor, take the highest rung
    its closed anchors recorded and compare the phase's current LIVE stage against
    it; below means new or reopened content entered, and a new phase-anchor WI is
    due. The message names the CANONICAL anchor spelling even when the closed
    anchor it read used a retired one, because the WI it is asking for is a NEW
    row.

    THE ABSTENTION, WHICH IS THE ONLY THING HERE THAT IS NOT A DIRECT RE-KEY.
    `kitlib.stage.REPO_GLOBAL_RUNGS` names the three rungs a per-phase reading
    cannot own — they are decided by repo-wide registries and passed whole to
    every per-phase call. A phase sitting on one of them is BELOW its recorded
    reach as a matter of arithmetic while saying nothing whatever about its own
    content: every phase reads the same rung at once, and blaming any one of them
    for "new or reopened content" would be a fabricated attribution. So the
    detector abstains there — and, because the schedule map's standing criticism
    of this detector was that it went VACUOUS SILENTLY when it could not parse the
    cache, it says so once, naming the rung and the phases it stood down for."""
    anchors, warns = phase_anchors(wis)
    live = phase_stages(root)
    # phase -> the highest rung any of its DONE anchors recorded
    closed = {}
    for (phase, reach), w in anchors.items():
        if w["status"] == "done":
            current = closed.get(phase)
            if current is None or _kitstage.order(reach) > _kitstage.order(current):
                closed[phase] = reach
    stood_down = {}
    for phase, reach in sorted(closed.items()):
        cur = live.get(phase)
        if cur is None:
            continue
        if cur in _kitstage.REPO_GLOBAL_RUNGS:
            stood_down.setdefault(cur, []).append(phase)
            continue
        if _kitstage.order(cur) < _kitstage.order(reach):
            warns.append(
                "phase {!r} dropped to {} but its closed [{}]-[{}] anchor recorded "
                "reach {} — new or reopened content entered; open a new "
                "[{}]-[DevStg-<rung>] work item to structure it (derived model "
                "§9.3)".format(phase, cur, phase, reach, reach, phase)
            )
    for rung, phases in sorted(stood_down.items()):
        warns.append(
            "phase-drop detector stood down for phase(s) {}: each reads {}, a "
            "repo-global rung decided by the need/boundary/component registries "
            "rather than by any one phase's content — the comparison against a "
            "closed anchor's recorded reach would be unattributable. It resumes "
            "when the frame settles".format(", ".join(sorted(phases)), rung)
        )
    return warns


# --- SpecRef anchor resolution (WI-354) ---------------------------------------
# R-E resolved only the PATH half of a `doc#anchor` SpecRef, so a row could cite a
# heading that does not exist and read as traceable for days (WI-326 cited a
# truncated `docs/log.md#...` slug from the day it was filed; it surfaced only when
# the close wrote the same string into a markdown LINK, where check_docs rejected
# it at once). The identical reference was enforced in one home and unread in the
# other — the WI-308 doc-refs class, one registry over.
#
# The anchor set comes from check_docs.parse_doc, NOT from a second slugifier here:
# two slug implementations that drift produce false findings on correct rows, which
# is worse than the gap being closed. That is a SIBLING IMPORT, allowed on the same
# ground as gen_trajectory's `check_trajectory` one — both modules are in
# bootstrap.py MAPPING, so they always ship and re-sync together.
#
# The import is LAZY and degrades to None rather than raising: this module runs in
# the SHIPPED pre-commit hook, and the `approval-fresh` lesson (130-REVIEW-A) is that
# a hook which hard-requires a file an adopter's tree may not have blocks every
# commit. Missing check_docs therefore costs the anchor half only — the path half
# is unchanged. Vacuity here is a real risk, so it is pinned by a test that drives
# the check against a KNOWN-BAD anchor rather than by trusting this comment.
_MD_SUFFIXES = (".md", ".markdown")
_ANCHOR_CACHE = {}  # resolved path -> frozenset of anchors, or None when unreadable


def doc_anchors(path):
    """The lowercase anchor slugs `path` exposes, or None when they cannot be
    determined (not a markdown file, unreadable, or check_docs unavailable).

    None means "unknown, do not judge" and is never treated as an empty set — an
    absent sibling must not turn every anchored SpecRef into a finding."""
    key = str(path)
    if key in _ANCHOR_CACHE:
        return _ANCHOR_CACHE[key]
    anchors = None
    if path.suffix.lower() in _MD_SUFFIXES and path.is_file():
        try:
            import check_docs
        except ImportError:  # pragma: no cover - exercised via the sys.path fallback
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            try:
                import check_docs
            except ImportError:
                check_docs = None
        if check_docs is not None:
            try:
                anchors = frozenset(check_docs.parse_doc(path)["anchors"])
            except OSError:
                anchors = None
    _ANCHOR_CACHE[key] = anchors
    return anchors


def nearest_anchor(frag, anchors):
    """The closest existing slug to `frag`, or None. A wrong anchor is nearly
    always a stale or TRUNCATED one rather than an invented one, so the report
    names the near miss — that is what makes the finding actionable instead of
    merely true.

    The prefix pass runs BEFORE difflib because difflib's ratio degrades with the
    LENGTH of the truncation, not with truncation as such — and 131-REVIEW-A
    refuted the stronger claim this docstring used to make. Measured against the
    live docs/log.md anchor set: WI-326's own 44-of-76-char truncation scores
    0.733 and plain `get_close_matches` finds it unaided, so that case does NOT
    justify the branch. A severer truncation does — `2026-07-26--wi-326` returns
    NOTHING from difflib at the 0.6 cutoff while the prefix pass returns the exact
    heading. That measured pair is pinned by a test, so this rationale cannot rot
    into the over-claim it replaced."""
    if not anchors:
        return None
    prefix = [a for a in anchors if a.startswith(frag) or frag.startswith(a)]
    if prefix:
        return sorted(prefix, key=lambda a: (abs(len(a) - len(frag)), a))[0]
    near = difflib.get_close_matches(frag, sorted(anchors), n=1, cutoff=0.6)
    return near[0] if near else None


def specref_findings(root, w):
    """R-E's SpecRef rule for ONE open WI, as a list of messages (the caller tags
    the rule and owns the warn/strict tier).

    Both halves of a `path#anchor` are resolved. Split out of `ssot_findings`
    when the anchor half landed (WI-354): folding it in line took that function
    past the complexity ratchet, and this module is already named as WI-280's
    next decomposition slice, so the rule gets its own unit rather than the
    monolith getting another sanctioned baseline entry.

    Implements: SR-157, LLR-077
    """
    spec = w["specref"]
    if not spec:
        return [
            "{}: open WI has no SpecRef (name its spec-of-record: "
            "docs/specs/WI-###.md or a doc#anchor)".format(w["id"])
        ]
    pathpart, _, frag = spec.partition("#")
    pathpart, frag = pathpart.strip(), frag.strip()
    if not pathpart:
        # A bare `#anchor` names no document, so there is nothing to resolve it
        # against. This returned CLEAN both before and after WI-354 — a hole
        # 131-REVIEW-A found by driving the rule rather than reading it, and the
        # one shape that made "both halves resolve" untrue as written.
        return [
            "{}: SpecRef {!r} has no path — a SpecRef names a document "
            "(docs/specs/WI-###.md or a doc#anchor), not a bare "
            "fragment".format(w["id"], spec)
        ]
    target = root / pathpart
    if not target.exists():
        return [
            "{}: SpecRef {!r} does not resolve to an in-repo file".format(w["id"], spec)
        ]
    if not target.is_file():
        # A directory exists but is not a spec-of-record; `exists()` alone let one
        # through (same review). Measured before landing: no live row names one.
        return [
            "{}: SpecRef {!r} names a directory, not a document".format(w["id"], spec)
        ]
    if not frag:
        return []
    # The anchor half (WI-354). Matching check_docs' link rule exactly — compare
    # lowercased, markdown targets only — so the SAME reference cannot pass as a
    # SpecRef and fail as a link, which is how WI-326's truncated anchor survived.
    anchors = doc_anchors(target)
    if anchors is None or frag.lower() in anchors:
        return []
    near = nearest_anchor(frag.lower(), anchors)
    return [
        "{}: SpecRef {!r} names no such heading in {} ({})".format(
            w["id"],
            spec,
            pathpart,
            "did you mean #" + near + "?"
            if near
            else "no similar heading — the target may have been rewritten",
        )
    ]


def ssot_findings(wis, root):
    """The work-item registry's coherence findings (R-A + R-E) + the
    unknown-status lint, each as `(rule, hard, message)`.

    `hard=True` (R-A only) is an ERROR at every run — the incoherent-handoff
    rule. R-E is warn-first; the caller promotes it to an error under `--strict`.
    Kept OUT of `validate()` so the dashboard renderer (`gen_trajectory`, which
    imports `validate`) shares the same registry read. R-B/R-C (open-WI status
    repetition) are retired (WI-180); R-D's done-id rule is RESTORED separately in
    `status_forward_only_findings` (WI-200), kept out of here so it reads the
    status.md text rather than the registry rows.

    Implements: SR-157, LLR-077
    """
    out = []
    for w in wis:
        st = w["status"]
        # (The `status-vocab` and `blocked-ref` rules retired with the CSV home
        # at Phase 5: status is the spec's DIRECTORY, so an unknown status is a
        # loader refusal before any row exists, and `blocked` is DERIVED as
        # queued+blockref — a queued row without one is simply queued. No row
        # can reach either rule.)
        # R-A: Deliverable non-empty IFF the WI is TERMINAL — with `partial`
        # exempt, and the exemption is the rule working rather than a hole in
        # it. What R-A is FOR is that a terminal row carries a permanent
        # backward record: a `done` WI's Deliverable records what shipped, a
        # `cancelled` WI's records the reason it never will (WI-267).
        #
        # A `partial` close carries that record too, and carries it BETTER: an
        # immutable per-close report under docs/handbacks/ with the commit
        # range, what was and was not delivered, the keep/discard split and who
        # decides it. Demanding a Deliverable cell as WELL would be demanding a
        # second, weaker copy of a record that already exists — and it is
        # unsatisfiable by construction, because SR-144's whole point is that
        # an early close leaves the spec's DEFINITION byte-identical ("scope
        # definitions never change; only whether they were fully delivered").
        # A rule no honest close can satisfy is not a rule; it is a red at
        # every run, and in the loop it is worse than that — the dispatcher's
        # refresh reds, `_refresh_failed` quarantines the lane's work, the
        # retry reds again (the spec move is bookkeeping and exempt from the
        # revert) and the run dies. Driven at review.
        if st in TERMINAL_STATUSES and not w["deliverable"] and st != "partial":
            reason = (
                "records what shipped"
                if st == "done"
                else "records the reason it will not be built"
            )
            out.append(
                (
                    "R-A",
                    True,
                    "{}: status={} but the Deliverable is empty (a {} WI {})".format(
                        w["id"], st, st, reason
                    ),
                )
            )
        elif st not in TERMINAL_STATUSES and w["deliverable"]:
            out.append(
                (
                    "R-A",
                    True,
                    "{}: status={} (open) but the Deliverable is non-empty (an "
                    "open WI's Deliverable is filled only at close)".format(
                        w["id"], st
                    ),
                )
            )
        # R-E: an open WI names a resolvable SpecRef (path or path#anchor).
        if st in OPEN_STATUSES:
            out.extend(("R-E", False, msg) for msg in specref_findings(root, w))

    return out


# --- LLR-160: queue-conflict vetting (the mechanical pre-filter) --------
# Two rows are OPEN AT ONCE and overlap. Nothing here is an error: overlap is
# frequently correct (two rows may legitimately answer one SR from different
# sides), and a checker that cannot tell those apart must not block. What it CAN
# do is refuse to let the overlap be invisible — which is the whole failure this
# rung addresses, a queue that silently grows two rows for one job because
# nobody compared the mint against what was already queued.
#
# The ADJUDICATOR half of the vetting (does this row's scope contradict the
# spine, or another queued row's intent?) is a judgement and lives in the
# `adjudicate-conflict` prompt, run inside the session that minted the row —
# not here. This is deliberately the cheap half.

# Title tokens too common to carry meaning — a shared "the" is not a signal.
_TITLE_STOPWORDS = frozenset(
    {"a", "an", "and", "at", "for", "in", "of", "on", "the", "to", "with"}
)
# Jaccard over title token SETS. 0.8 is deliberately high: this rung's job is to
# catch the same job minted twice (near-identical wording), not to editorialize
# about two rows in the same area. A lower bar turns a useful warn into noise
# that gets ignored, which is worse than not having it.
_TITLE_SIMILARITY = 0.8


def _title_tokens(title):
    """A title's comparable token set: case-folded, punctuation-split,
    stopwords and pure-number tokens dropped (a WI id or a phase number is not
    subject matter).

    Implements: SR-157, LLR-160
    """
    words = re.split(r"[^0-9a-z]+", (title or "").lower())
    return {w for w in words if w and w not in _TITLE_STOPWORDS and not w.isdigit()}


_TITLE_CLIP = 90


def _clip_title(title):
    """A title bounded for a one-line finding: whitespace collapsed, clipped."""
    text = " ".join(str(title or "").split())
    return text if len(text) <= _TITLE_CLIP else text[: _TITLE_CLIP - 1] + "…"


def queue_conflict_findings(wis):
    """LLR-160, mechanical half: pairs of OPEN rows that overlap.

    Three signals, warn-only, each named with both row ids so the message is
    actionable without opening the registry:

      near-duplicate title  Jaccard >= 0.8 over title token sets — the same job
                            minted twice, which is what a mint that never
                            compared against the queue produces.
      shared SR-Refs        two open rows answering the same requirement. Often
                            correct; worth seeing.
      shared SpecRef        two open rows pointing at ONE spec document. This is
                            the sharpest of the three: a spec is a row's
                            definition, so two open rows sharing one is either a
                            duplicate or a split that never got written down.

    Deterministic order (sorted by the id pair), and each pair is reported once
    per signal, never once per direction.

    Implements: SR-157, LLR-160
    """
    open_rows = [
        w for w in wis if (w.get("status") or "").strip().lower() in OPEN_STATUSES
    ]
    tokens = {w["id"]: _title_tokens(w.get("title")) for w in open_rows}
    out = []
    for i, a in enumerate(open_rows):
        for b in open_rows[i + 1 :]:
            first, second = sorted((a["id"], b["id"]))
            ta, tb = tokens[a["id"]], tokens[b["id"]]
            union = ta | tb
            if union and len(ta & tb) / len(union) >= _TITLE_SIMILARITY:
                out.append(
                    "{} and {} are both open with near-identical titles - one "
                    "job minted twice? ({!r} / {!r})".format(
                        first,
                        second,
                        # CLIPPED. A WI title in this repo is routinely a
                        # multi-thousand-character paragraph, so interpolating
                        # two raw ones produced a ~6 KB stderr line per pair —
                        # a warn nobody reads is a warn that does not exist.
                        _clip_title(a.get("title")),
                        _clip_title(b.get("title")),
                    )
                )
            shared_srs = sorted(set(a.get("srs") or ()) & set(b.get("srs") or ()))
            if shared_srs:
                out.append(
                    "{} and {} are both open and both answer {}".format(
                        first, second, ";".join(shared_srs)
                    )
                )
            spec = (a.get("specref") or "").split("#", 1)[0]
            if spec and spec == (b.get("specref") or "").split("#", 1)[0]:
                out.append(
                    "{} and {} are both open and share one spec of record ({})".format(
                        first, second, spec
                    )
                )
    return sorted(out)


def spec_lifecycle_findings(root, wis):
    """The spec-lifecycle close-side rule **R-F** (WI-251) — the mechanical half
    of the close ritual R-E's open half leaves unstated: *Deliverable filled,
    `SpecRef` cleared, spec archived* (the `docs/specs/` README lifecycle). The
    one-sided enforcement is how this repo accreted 137 done rows with live
    SpecRefs before the rule existed. Two findings, both message-only (the
    caller tags `R-F` and owns the warn-plain / error-under-`--strict`
    promotion, the R-E warn tier — so a rotting spec surface cannot reach a
    green DevStg-Tests/DevStg-Impl gate while a plain commit stays warn-first):

      - a **terminal** WI (`done` or `cancelled`, WI-267) whose `SpecRef` is still
        set — the terminal transition clears it (the Deliverable + log carry the
        backward record; a `cancelled` row's reason lives in its Deliverable);
      - a **live** `docs/specs/` file cited by no *open* WI — archive it to
        `docs/archive/specs/` (close date appended, WI ids noted) or point an
        open WI at it. A shared effort doc therefore archives only when its
        last open citer closes; `deferred`/`blocked` are open, so their specs
        stay, but `cancelled` is terminal, so a cancelled WI keeps no live spec. The
        scaffold boilerplate (README, any `-000` exemplar) is excluded by the
        `spec_interface_findings` idiom.

    Vacuous on a fresh scaffold (no done-with-SpecRef rows; only excluded
    boilerplate in `docs/specs/`). Whether the archived spec's durable content
    actually landed in a spine/architecture home first is the recorded
    Reviewer-tier gap (enforcement-audit.md).

    Implements: SR-157, LLR-097
    """
    out = []
    open_cited = set()
    for w in wis:
        spec = w["specref"]
        if not spec:
            continue
        if w["status"] in OPEN_STATUSES:
            open_cited.add(spec.split("#", 1)[0].strip())
        elif w["status"] == "partial":
            # LLR-161: a `partial` row's SpecRef STAYS. R-F exists so a closed
            # row stops pointing at a live spec-of-record that a reader would
            # take as current — but partial work continues by MINTING A
            # SUCCESSOR, and the successor's `supersedes` lineage is worth
            # nothing if the thread it continues has already been cut. The spec
            # is still the record of what was asked for; only the delivery
            # question is closed.
            open_cited.add(spec.split("#", 1)[0].strip())
        elif w["status"] in TERMINAL_STATUSES:
            out.append(
                "{}: status={} but SpecRef {!r} is still set (a terminal WI clears "
                "the SpecRef and archives the spec to docs/archive/specs/ — "
                "the {}/README.md lifecycle)".format(
                    w["id"], w["status"], spec, SPECS_DIR
                )
            )
    for path in _armed_specs(root):
        rel = "{}/{}".format(SPECS_DIR, path.name)
        if rel not in open_cited:
            out.append(
                "{}: live spec cited by no open WI (archive it to "
                "docs/archive/specs/ with the close date appended and the "
                "WI ids noted, or point an open WI's SpecRef at it)".format(rel)
            )
    return out


# --- WI-352: the completion reconciler ----------------------------------------
# A WI's `Status` is an ATTESTATION, and the owner ruled 2026-07-28 that it stays
# one rather than becoming derived: the evidence a deriver would read is the `WI:`
# commit trailer, but a trailer means "a commit CLAIMS this WI", not "the work is
# right" (WI-336's code landed while its row correctly stayed `queued`, because a
# review had refuted three of its claims — a deriver would have flipped it), and
# `draft`/`deferred`/`blocked`/`cancelled` are decisions, not outcomes. What was missing is
# not derivation but RECONCILIATION — the shape every other declared-vs-computed
# pair here already has (`spine_rules --check` recomputes and fails on drift;
# every generator carries `--check`). So this compares the declared cell against
# the completion evidence and reports DISAGREEMENT, never auto-flipping: an
# auto-flip would re-create exactly the false completion that WI-336 and
# `40c92f6` were both corrections of.
_DONE_BOX_RE = re.compile(r"^\s*[-*]\s+\[[xX]\]")
_OPEN_BOX_RE = re.compile(r"^\s*[-*]\s+\[ \]")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# Checkboxes live under a "Done-when" heading by overwhelming convention (281 of
# 296 across every live and archived spec; re-derived by
# test_done_when_holds_the_overwhelming_majority_of_checkboxes rather than
# trusted here). The rest are migration checklists,
# which are STEPS rather than completion evidence and must not count — counting
# them would make a kit-version-bump doc read as an unfinished WI.
_DONE_WHEN_RE = re.compile(r"^\s*(?:\d+[.)]\s*)?done[- ]when\b", re.IGNORECASE)


def _done_when_boxes(text):
    """`(ticked, unticked)` counted only within the spec's Done-when SECTION.

    Section, not "everything until the next heading": a Done-when that subdivides
    keeps its boxes, while a SIBLING heading at the same level ends it. That
    distinction is load-bearing — `docs/specs/WI-321.md` carries WI-324's
    remaining boxes under a sibling `## Split off, deliberately` heading, and
    folding those in would attribute one WI's unfinished work to another."""
    ticked = unticked = 0
    depth = None  # the Done-when heading's level, while we are inside its section
    for line in text.splitlines():
        heading = _HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            if _DONE_WHEN_RE.match(heading.group(2)):
                depth = level
            elif depth is not None and level <= depth:
                depth = None  # a sibling or shallower heading closes the section
            continue
        if depth is None:
            continue
        if _DONE_BOX_RE.match(line):
            ticked += 1
        elif _OPEN_BOX_RE.match(line):
            unticked += 1
    return ticked, unticked


def _own_spec(root, wid, archived=True):
    """A WI's OWN spec as `(path, rel)`, or `(None, None)`.

    Name-identified only — `docs/specs/WI-###.md`, then the archived
    `docs/archive/specs/WI-###.<date>.md` — and deliberately NOT whatever the
    `SpecRef` points at. A SpecRef may name a SHARED effort doc (WI-324 cites
    `docs/specs/WI-321.md`) or a non-spec record (`docs/log.md`,
    `docs/reviews/*.md`), and boxes in either are not attributable to the citing
    WI. Reading them anyway is how a reconciler invents a disagreement: measured
    here before this rule existed, following SpecRef reported WI-324's work
    "FINISHED" out of ticks WI-321 had made.

    `archived=False` restricts to the LIVE spec — the standing check's scope, for
    the reason recorded in `completion_reconciliation_findings`."""
    live = root / SPECS_DIR / "{}.md".format(wid)
    if live.is_file():
        return live, "{}/{}".format(SPECS_DIR, live.name)
    if not archived:
        return None, None
    archive = root / ARCHIVE_SPECS_DIR
    if archive.is_dir():
        matches = sorted(archive.glob("{}.*.md".format(wid)))
        if matches:
            return matches[-1], "{}/{}".format(ARCHIVE_SPECS_DIR, matches[-1].name)
    return None, None


def _wi_trailer_claims(root):
    """WI ids named by a `WI:` trailer on a commit reachable from HEAD.

    `None` off-git (no repo, or git unavailable), so the trailer signal is a
    silent no-op there rather than a finding — the stance every other git-reading
    check in this module takes."""
    out = _git(
        root, ["log", "--format=%(trailers:key=WI,valueonly,separator=,)", "HEAD"]
    )
    if out is None:
        return None
    return {
        token.strip()
        for token in out.replace("\n", ",").split(",")
        if re.fullmatch(r"WI-\d+", token.strip())
    }


def _live_spec_boxes(root, wid):
    """`(rel, ticked, unticked)` for a WI's own LIVE spec, or `None` when it has
    none. The one place a Done-when tally is read, so the standing check and the
    close-time check can never answer "is this finished" from different counts."""
    path, rel = _own_spec(root, wid, archived=False)
    if path is None:
        return None
    ticked, unticked = _done_when_boxes(
        path.read_text(encoding="utf-8", errors="replace")
    )
    return rel, ticked, unticked


def completion_reconciliation_findings(root, wis):
    """Disagreements between a WI's declared `Status` and its completion evidence,
    as `(kind, message)` pairs — the kind lets the caller tier them without
    pattern-matching on human-readable prose.

      - **spec-says-finished** — an OPEN row whose own spec has at least one
        ticked Done-when box and none left unticked. The WI-328 shape: six boxes
        ticked across six commits on 2026-07-27, the row still `queued` a day
        later, and because it was `SafetyClass=spine` the scheduler serialized the
        whole project behind finished work while the session told the owner a
        shipped migration was awaiting approval.
      - **spec-says-unfinished** — a `done` row whose own **live** spec still has
        unticked boxes and which no open WI cites (the same "no open citer" test
        R-F uses to decide when a spec may be archived).
      - **trailer-claims-it** — an OPEN row named by a `WI:` trailer on a commit
        reachable from HEAD.

    **Why the done side is scoped to LIVE specs**, measured rather than assumed:
    run over the archive it produced **40** findings (36 with no box ticked at
    all, 4 partly ticked) and neither class was actionable. Some are a self-referential terminal box (`Commit bar green; row
    done, spec archived` — untickable at the moment you would tick it); the rest
    are closes that never ticked. For a WI closed weeks ago, whose Deliverable and
    log entry carry the record, the only available action is cosmetic — and a
    check whose recommended action is "nothing" is a wall of warns, which is
    exactly how WI-308 recorded that a check earns its own ignore. The live window
    is where the disagreement is still resolvable, and the CLOSING COMMIT is where
    it is resolvable and visible at once: `staged_completion_findings` owns that
    moment. The 38 are real record-keeping debt, filed rather than suppressed.

    A fourth signal the row asked for — a `done` row with an empty `Deliverable` —
    is deliberately NOT reimplemented: **R-A already makes it a hard ERROR at every
    run**, strictly stronger than this tier, and a second weaker copy of a live
    rule is the duplication this kit's working agreement forbids.

    Never auto-flips. Vacuous until armed: no specs and no trailers, no findings.
    """
    out = []
    open_cited = {
        w["specref"].split("#", 1)[0].strip()
        for w in wis
        if w["status"] in OPEN_STATUSES and w["specref"]
    }
    for w in wis:
        boxes = _live_spec_boxes(root, w["id"])
        if boxes is None:
            continue
        rel, ticked, unticked = boxes
        if w["status"] in OPEN_STATUSES and ticked and not unticked:
            out.append(
                (
                    "spec-says-finished",
                    "{}: status={} but its spec {} reports the work FINISHED ({} "
                    "Done-when box(es) ticked, none left) — close the row or "
                    "untick what has not shipped; nothing here flips it for "
                    "you".format(w["id"], w["status"], rel, ticked),
                )
            )
        elif w["status"] == "done" and unticked and rel not in open_cited:
            out.append(
                (
                    "spec-says-unfinished",
                    "{}: status=done but its live spec {} still has {} unticked "
                    "Done-when box(es) and no open WI cites it — tick what "
                    "shipped or reopen the row".format(w["id"], rel, unticked),
                )
            )

    claims = _wi_trailer_claims(root)
    if claims:
        for w in wis:
            if w["status"] in OPEN_STATUSES and w["id"] in claims:
                out.append(
                    (
                        "trailer-claims-it",
                        "{}: status={} but a commit reachable from HEAD carries a "
                        "`WI: {}` trailer — a trailer CLAIMS the WI, it does not "
                        "attest the work, so this is a prompt to reconcile, never "
                        "a reason to close".format(w["id"], w["status"], w["id"]),
                    )
                )
    return out


def tier_completion_findings(findings):
    """Split reconciler findings into `(warn_only, gated)`.

    The tier is a property of the SIGNAL, so it is decided here beside the
    signals rather than as another branch in `main()`. Spec evidence is an
    attestation, so a row disagreeing with its own ticked boxes is a
    contradiction between two homes for one fact and belongs at the gate. A `WI:`
    trailer is not: it means "a commit CLAIMS this WI", which is the very
    argument the owner's 2026-07-28 ruling uses to keep Status declared — so it
    warns and never joins the exit code.

    DEVIATION from the WI row, which asked for the whole reconciler at the
    warn-plain / error-under-`--strict` tier. Taken on the row's own reasoning:
    WI-336's code landed while its row CORRECTLY stayed `queued`, a review having
    refuted three of its claims. An error-under-strict trailer rule blocks the DevStg-Impl
    gate for the length of that rework, and the only ways out are a false close
    or an untracked exception."""
    warn_only = [msg for kind, msg in findings if kind == "trailer-claims-it"]
    gated = [msg for kind, msg in findings if kind != "trailer-claims-it"]
    return warn_only, gated


def staged_completion_findings(root):
    """The close-time half of the reconciler (WI-352): a staged commit flipping a
    WI to `done` while its own spec still carries unticked Done-when boxes.

    This is the moment the standing check cannot reach, and the one that matters
    most. `40c92f6` exists because a box was ticked before it was true; WI-334 is
    the mirror, closed 2026-07-27 with five boxes never ticked — and by the time
    either is visible to a gate run the spec has been archived and only a cosmetic
    fix is left. Here the spec is still live, the author is still inside the
    change, and both homes for "is this finished" can be made to agree in one
    commit.

    Warning strings ([] when not applicable), a silent no-op off-git — the same
    shape as `staged_findings` and `critique_ratchet_findings`."""
    staged = _staged_wi_registry(root)
    if staged is None:
        return []
    _, cur_map, head_map = staged
    out = []
    for wid, _cur in _newly_closed(cur_map, head_map):
        boxes = _live_spec_boxes(root, wid)
        if boxes is None:
            continue
        rel, ticked, unticked = boxes
        if unticked:
            out.append(
                "{}: this commit closes it, but its spec {} still has {} unticked "
                "Done-when box(es) ({} ticked) — tick what shipped in THIS commit, "
                "or record in the log why the row closes without them; once the "
                "spec is archived only a cosmetic fix is left".format(
                    wid, rel, unticked, ticked
                )
            )
    return out


# --- status.md forward-only enforcement (WI-200; restores WI-180-retired R-D) --
# A word-bounded `WI-###` id token, so a `done` id embedded in status.md prose
# (a "CLOSED (WI-142)" narrative, a bullet) is found wherever it appears.
_WI_TOKEN_RE = re.compile(r"\bWI-\d+\b")
# The kit's generated-block marker idiom: gen_arch_map / gen_trajectory splice
# content between `<!-- BEGIN GENERATED ... -->` / `<!-- END GENERATED ... -->`
# HTML comments (arch_inventory reads the same `BEGIN GENERATED` sentinel). Its
# presence in status.md means the file is an integrator-generated snapshot.
_STATUS_GENERATED_RE = re.compile(r"<!--\s*BEGIN GENERATED", re.IGNORECASE)


def status_forward_only_findings(root, wis):
    """The status.md forward-only rule (WI-200) — restores the WI-180-retired R-D
    done-id check in a mode-aware form. `docs/status.md` holds only what must
    happen **next**; a closed WI's record lives in `docs/log.md`. So a `done` WI
    id appearing as a token in status.md is a finding — WARN plain, ERROR under
    `--strict` (DevStg-Tests+), the pre-WI-180 severity (the caller owns that promotion, the
    `spec_interface_findings` pattern).

    A repo-state rule evaluated every run (like R-A cross-reads the registry +
    status.md), not a staged-diff rule — under `--jobs N` only the serialized
    integrator publishes to the shared branch, so the invariant holds at every
    published tree.

    **Mode-aware (WI-180's direction preserved, not reversed):** when status.md
    carries the kit's generated-block marker (`<!-- BEGIN GENERATED ... -->`,
    spliced by `gen_trajectory.py --status`, WI-234) the rule stands down ONLY
    inside the marked block — its freshness is the `status-map` byte-compare
    step's job. The hand-authored remainder is exactly where done-ids accrete,
    so the token rule keeps policing it: a whole-file stand-down left the
    forward-only discipline enforced by nothing on a hybrid file (repo-review
    2026-07-21 H-5; the pre-WI-234 "no status.md generator exists yet" wording
    this docstring carried was stale).

    Only ids whose registry Status is `done` flag; open (queued/active/deferred/
    blocked) ids and unknown ids do not (an unknown id is R-E-adjacent). Vacuous
    when status.md is absent or the registry is placeholder-only (no real WIs ->
    no done ids); the `[checks] trajectory_check = false` opt-out is the caller's (it
    returns before any check runs). Returns finding-message strings.

    Implements: SR-157, LLR-075
    """
    path = root / STATUS_MD
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    if _STATUS_GENERATED_RE.search(text):
        # Hybrid file: exempt the generated block(s) only (see the docstring);
        # the hand-authored remainder stays policed.
        kept, skipping = [], False
        for line in text.splitlines():
            if "<!-- BEGIN GENERATED" in line:
                skipping = True
            if not skipping:
                kept.append(line)
            if "<!-- END GENERATED" in line:
                skipping = False
        text = "\n".join(kept)
    done_ids = {w["id"] for w in wis if w["status"] == "done"}
    if not done_ids:
        return []
    present = sorted(set(_WI_TOKEN_RE.findall(text)) & done_ids)
    return [
        "{}: a `done` work-item id appears in {} — status.md is forward-only; a "
        "closed WI's record belongs in docs/log.md, not here (scrub the token, or "
        "make status.md a generated snapshot)".format(wid, STATUS_MD)
        for wid in present
    ]


# The terminal WON'T-INTEGRATE predecessor states a hard edge can never be
# satisfied by (OI-73 arm 4): `cancelled` (WI-267) AND `partial` — a lane that
# stopped early moves its spec to the terminal `partial/` and NEVER integrates
# `done` (LLR-161), so a live WI hard-depending on one waits forever exactly as
# it would on a cancelled row. `partial` was the WI-541 -> WI-540 strand that
# waited invisibly and was repaired by hand; extending this finding is the
# validator net that makes such a strand reported rather than silent.
_DEAD_PRED_STATES = ("cancelled", "partial")


def dead_dependency_findings(wis):
    """Surface a live WI that hard-depends on a terminal predecessor (WI-267,
    extended to `partial` by OI-73).

    A `cancelled` or `partial` WI is terminal — it will never integrate `done`,
    so an open successor whose hard edge points at it can NEVER become ready. The
    conservative decision (WI-267 design-decision 3) is to SURFACE the dead edge
    rather than let a terminal predecessor silently "satisfy" the dependency the
    way `done` does: the owner must re-home the successor's edge (an OI-70/OI-73
    close now REPLACES inbound edges at the mint, so a strand minted through that
    path never reaches here) or cancel it too. The scheduler already refuses to
    schedule such a WI (schedule.hard_preds_satisfied requires `done`, not merely
    terminal); this makes the same dead edge visible in the validator. WARN
    plain, ERROR under `--strict`. Soft (`~`) edges are advisory and never gate
    readiness, so they are exempt. Vacuous until a registry actually leaves a
    still-depended-on WI terminal.
    """
    by_id = {w["id"]: w for w in wis}
    out = []
    for w in wis:
        if w["status"] not in OPEN_STATUSES:
            continue
        dead = sorted(
            p for p in w["preds"] if by_id.get(p, {}).get("status") in _DEAD_PRED_STATES
        )
        if dead:
            out.append(
                "{}: open WI hard-depends on terminal WI(s) {} — a "
                "cancelled/partial predecessor never integrates `done` and so "
                "never satisfies a hard dependency; re-home the edge or close "
                "this WI too".format(w["id"], ";".join(dead))
            )
    return out


# (run_state_findings — the WI-115 stale-end-state warn over docs/run-state —
# retired at concurrency-restructure Phase 5 with the dispatcher that wrote
# that file; a stale parked state is unrepresentable when no file declares
# one.)


# `git -C <root> <args>` stdout on success, else None (git absent, not a repo,
# no such object). Every staged-mode git call degrades to None so the
# no-validation-delta warn is a silent no-op outside a git checkout.
#
# WI-521 slice 1 folded the BODY into `kitlib.git.git_out`, the declared one home
# for this pattern (`check.py` already aliases it the same way). It had been a
# fourth copy that the D-8/`OI-16` consolidation missed, and the reason it was
# missed is the `stdin` argument — it feeds a batch command (`cat-file
# --batch-check`), which is how the committed-mirror scan asks about many blobs
# in ONE subprocess instead of two per file, and that made it look like a
# different function rather than the same one. `stdin` is now a parameter there,
# defaulting to no input, so the two spellings are one.
_git = _kitgit.git_out


def _blame_row_times(root, rel_path):
    """`{row-id: committer-time-epoch}` for a registry, via a single
    `git blame --line-porcelain`. Returns {} on ANY git failure — no repo, an
    untracked/uncommitted file, an unparseable blame — so the backlog-staleness
    warn degrades silently off-git (never a false warn, never a crash). One
    subprocess per file keeps the cost bounded (WI-205: ≤2 blames).

    THE ROW'S SHAPE IS THE CARRIER'S, and getting that wrong is silent. Under
    CSV a row is ONE line whose leading field (up to the first comma) is its id.
    Under TOML a row is a TABLE spanning many lines, its id in the `[tier.ID]`
    header, and its time is the NEWEST commit over those lines — an amendment
    can touch any one of them. Read with the CSV rule a TOML registry yields a
    map keyed by `[requirement.SR-001]` and `title = "..."`, which no caller
    ever looks up: every lookup misses, the compare never fires, and the
    staleness warn passes because it found nothing to check."""
    live = spine_carrier.resolve(Path(root) / rel_path)
    if live is None:
        return {}
    blamed = spine_carrier.stem(rel_path) + live.suffix
    out = _git(root, ["blame", "--line-porcelain", "--", blamed])
    if out is None:
        return {}
    return (_blame_toml_times if live.suffix == ".toml" else _blame_csv_times)(out)


def _blame_lines(porcelain):
    """`(committer_time, content)` per blamed line, in file order — the shared
    walk both carrier readers need. `--line-porcelain` repeats the full commit
    header for every line, so a `committer-time <epoch>` header always precedes
    its `\\t<content>` line."""
    committer_time = None
    for line in porcelain.split("\n"):
        if line.startswith("committer-time "):
            try:
                committer_time = int(line[len("committer-time ") :].strip())
            except ValueError:
                committer_time = None
        elif line.startswith("\t"):
            yield committer_time, line[1:]
            committer_time = None


def _blame_csv_times(porcelain):
    """One CSV line is one row; its id is the leading field."""
    times = {}
    for committer_time, content in _blame_lines(porcelain):
        token = content.split(",", 1)[0].strip()
        if token and committer_time is not None:
            times[token] = committer_time
    return times


_TOML_ROW_HEADER = re.compile(r"^\s*\[[A-Za-z_][\w-]*\.([A-Za-z]+-\d+)\]\s*$")


def _blame_toml_times(porcelain):
    """One TOML table is one row; its time is the NEWEST commit over its lines,
    the table header included. Newest rather than the header's own time, because
    an amendment edits a VALUE line and leaves the header untouched — taking the
    header's time would date every amended row to its creation and report
    nothing as stale."""
    times, current = {}, None
    for committer_time, content in _blame_lines(porcelain):
        header = _TOML_ROW_HEADER.match(content)
        if header:
            current = header.group(1)
        if current is None or committer_time is None:
            continue
        times[current] = max(times.get(current, committer_time), committer_time)
    return times


def _path_commit_time(root, rel_path, row_history=False):
    """The committer time (epoch int) of the last commit to touch `rel_path`, via
    `git log -1 --format=%ct`, or None (no repo, an untracked path, no history) —
    the SpecRef-target half of the staleness compare, degrading silently like
    `_blame_row_times`.

    `row_history=True` asks the question `git blame` answers for a CSV row, for a
    registry where one row is one FILE: *when was this work item's content last
    edited*, across the renames its status changes are. It adds two flags, and
    the pair was MEASURED rather than reasoned about, because the obvious single
    flag does not work:

      * `--follow` alone still answers 2000 for a spec created at t=1000 and
        `git mv`d at t=2000 — the rename commit touches the new path, so `-1`
        stops there whether renames are followed or not. `--follow` is what lets
        the log reach PAST the move at all, but on its own it changes nothing
        about the answer.
      * `--diff-filter=AM` alone also answers 2000 — without rename detection the
        move looks like an Add of the new path.
      * Together they answer **1000**: the pure rename is filtered out as `R`,
        and `--follow` carries the search back to the file's real last edit.

    A commit that moves AND edits the spec answers 1000 as well — git scores it
    `R<similarity>`, and `--diff-filter=AM` drops it like any other rename. That
    is the accepted blind spot (WI-362, owner ruling 2026-07-29: name it, do not
    build rename detection): re-affirmation must be a content edit at the SAME
    path, because a Title edit renames the spec file. Only a rewrite large enough
    to defeat rename detection reads as `A` and re-dates, so the re-dating of a
    renamed path is a similarity heuristic and never something to rely on.

    Without both, every status move silently resets the row's staleness clock —
    the trap docs/concurrency-restructure.md §7 names, though not by this cause.
    `--follow` accepts exactly one pathspec, which is why the folder mode pays
    one `git log` per OPEN row rather than one per registry."""
    args = ["log", "-1", "--format=%ct"]
    if row_history:
        args += ["--follow", "--diff-filter=AM"]
    out = _git(root, args + ["--", rel_path])
    if out is None:
        return None
    out = out.strip()
    if not out:
        return None
    try:
        return int(out)
    except ValueError:
        return None


def _spec_paths(work_dir):
    """`{wid: repo-relative POSIX path}` for every spec under `work_dir`, keyed
    off the FILENAME's id prefix. Reading the id from the name rather than the
    frontmatter costs no file reads and cannot disagree with the parsed row —
    `parse_spec_row` refuses a spec whose two ids differ."""
    out = {}
    for path in spec_files(work_dir):
        wid = "-".join(path.name.split("-")[:2])
        out[wid] = "{}/{}".format(WI_WORK, path.relative_to(work_dir).as_posix())
    return out


def _spec_row_times(root, work_dir, wids):
    """`{wid: committer-time-epoch}` for the named specs — the folder-registry
    counterpart of `_blame_row_times`, one `git log -1` per id, asking the
    blame-equivalent question (`_path_commit_time(row_history=True)`) so a status
    MOVE does not re-date a row that nobody re-validated.

    Only the ids the caller actually examines are looked up: the whole point of
    the blame form was one subprocess for the whole registry, and per-file logs
    over a 350-item backlog would trade that for 350. Degrades to a missing key
    (never a crash or a false warn) exactly like the blame form."""
    paths = _spec_paths(work_dir)
    times = {}
    for wid in wids:
        rel = paths.get(wid)
        if rel is None:
            continue
        when = _path_commit_time(root, rel, row_history=True)
        if when is not None:
            times[wid] = when
    return times


def _wi_row_times(root, open_wis):
    """`{wid: committer-time}` for the open WIs: one `git log` per open spec —
    a folder registry has no rows to blame. (The CSV-home `git blame` half
    retired with the CSV at Phase 5.)"""
    return _spec_row_times(
        root, spec_work_dir(root / WI_CSV), [w["id"] for w in open_wis]
    )


def _declared_packs(root):
    """`{CMP-ID: [pack token]}` — the Knowledge cells that resolve to a REAL
    pack file (`docs/knowledge/<name>.md`, or a direct path, with or without
    the `.md`). A Knowledge token that resolves to nothing (a skill name, a
    planned pack) is not a citation debt, so it never arms the warn."""
    packs = {}
    for r in spine_carrier.load(root / CMP_CSV, "CMP-ID"):
        cid = (r.get("CMP-ID") or "").strip()
        if not cid:
            continue
        resolved = []
        for token in _split_refs(r.get("Knowledge") or ""):
            candidates = (token, token + ".md", "docs/knowledge/" + token + ".md")
            if any((root / cand).is_file() for cand in candidates):
                resolved.append(token)
        if resolved:
            packs[cid] = resolved
    return packs


def _spec_text_for(work_dir, wid):
    for path in spec_files(work_dir):
        if path.name.startswith(wid + "-"):
            try:
                return path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                return None
    return None


def knowledge_pack_findings(root, wis):
    """The WI-388 pack-citation warn (consumer 3 of the intake context block)
    — WARN-ONLY, never the exit code, not even under --strict (advisory is
    the block's contract): a hand-authored OPEN spec (queued/active) whose
    rows' components declare knowledge packs the spec never cites is building
    blind on rows whose how-knowledge is recorded. The join is the same
    LLR.Component -> CMP.Knowledge join `intake.context_block` makes,
    re-derived here under this module's F5 independence (the shipped hook
    imports no sibling). A minted row's `## Context` block cites the packs at
    mint, so minted rows satisfy the rule by construction — the warn reaches
    exactly the hand-authored residue. A pack is cited by its full token or
    its basename; vacuous with no CMP Knowledge cells or no resolving pack."""
    packs = _declared_packs(root)
    if not packs:
        return []
    sr_comps = {}
    for r in spine_carrier.load(root / LLR_CSV, "LLR-ID"):
        comp = (r.get("Component") or "").strip()
        if comp in packs:
            for sr in _split_refs(r.get("SR-Refs") or ""):
                sr_comps.setdefault(sr, set()).add(comp)
    findings = []
    work_dir = spec_work_dir(root / WI_CSV)
    for w in wis:
        if w["status"] not in ("queued", "active"):
            continue
        comps = sorted({c for sr in w["srs"] for c in sr_comps.get(sr, ())})
        owed = sorted({p for c in comps for p in packs[c]})
        if not owed:
            continue
        text = _spec_text_for(work_dir, w["id"]) or ""
        cited = any(p in text or Path(p).name in text for p in owed)
        if not cited:
            findings.append(
                "{}: component(s) {} declare knowledge pack(s) {} the spec "
                "never cites — read them before building (WI-388 context; "
                "advisory)".format(w["id"], ", ".join(comps), "; ".join(owed))
            )
    return findings


def backlog_staleness_findings(root, wis):
    """WI-205 — the backlog-staleness warn (warn-only, the WI-129 checker stance).

    Approving amended SN/SR/LLR/TC content never touches the open WI rows that
    cite it, so an incomplete backlog can silently drift out of sync with the
    requirement state it was filed against. For each open WI (queued/active/
    blocked — `deferred` and `done` are exempt) this compares when its registry
    row last changed against when each cited source last changed, and warns when a
    source is STRICTLY NEWER: the WI needs a driven re-validation against the
    amended requirement. Re-affirming is deliberately cheap — a content edit to
    the spec at the SAME path (frontmatter or body) re-dates the row and clears
    the warn (a *driven look*, not ceremony). Cited sources: each `SR-Refs` id (a
    row of system-requirements.toml) and the `SpecRef` target file.

    SAME PATH is a real limitation, not a turn of phrase, and the warn text says
    so. The row clock reads `--follow --diff-filter=AM` (`_path_commit_time`,
    row-history mode) so that a pure status MOVE cannot re-date a row nobody
    re-validated — the flag pair MEASURED at Phase 2b — and that filter drops a
    rename whatever else the commit did. Since the Title drives the spec
    FILENAME, re-titling a WI renames its file and does NOT clear the warn: a
    genuine re-affirmation carried by a Title edit reads as no re-affirmation at
    all. That is the accepted blind spot of the trade (WI-362, owner ruling
    2026-07-29: state it in the warn, do not build rename detection) — pinned by
    tests/test_wi_folder_loaders.py so changing it has to be deliberate.

    THE SOURCE CLOCK IS LINE-GRANULAR, WHICH THE CELL-CLASS SPLIT IS NOT, and
    that is a second stated limitation rather than a bug to be quietly widened.
    `_blame_row_times` takes the NEWEST commit over a row's lines; a `git blame`
    line time cannot tell an approved cell from a traced one, so writing an
    INFORMATIVE cell re-dates the row and warns every WI that cites it.
    MEASURED (WI-484 phase 2, 2026-08-22): the `hat_refs` backfill wrote 55 SR
    cells and raised seven such warns; at phase 5 one survived — `SR-163`, whose
    newest line is its `hat_refs = [...]`. Two fixes were examined and NEITHER
    is small (recorded so the next reader does not re-derive them):
    line-attribution of the blame to approved-class keys needs a quote-state
    parser for multi-line TOML values AND would silence a re-pointed
    `SN-Refs`/`Boundary-Refs`, which is traced but scope-BEARING — the exact
    change a citing WI most needs to re-validate against; and recomputing the
    clock through `split_changed_cells` over a rev range is exact but replaces
    this check's bounded cost (≤2 blames) with git work per open WI and
    inherits the amendment scan's approved-only population. Which traced cells
    are staleness-bearing is a new classification, i.e. a ruling, not a patch.
    Stated here on the WI-362 precedent (owner ruling 2026-07-29: name the blind
    spot, do not build the detection).

    NEVER joins the exit code — not even under `--strict` (a warn-tier checker
    feature mints no SR and gates nothing, WI-129/132; the caller prints these and
    keeps them out of `errors`). Best-effort and silent off-git: no git, an
    untracked registry, or an uncommitted (not-yet-in-HEAD) WI or SR row simply
    yields no comparison for the affected item — never a false warn. Bounded cost:
    at most two `git blame`s (the WI + SR registries) plus one `git log -1` per
    distinct SpecRef path of an open WI. In the spec-folder registry there are no
    registry ROWS to blame — each work item is its own file — so the WI half
    costs one `git log -1 --follow` per OPEN item (the only rows this check
    examines), never one per work item."""
    open_wis = [w for w in wis if w["status"] in BACKLOG_STALE_STATUSES]
    if not open_wis:
        return []
    wi_times = _wi_row_times(root, open_wis)
    if not wi_times:
        return []  # off-git / the registry is untracked — no basis to compare
    sr_times = _blame_row_times(root, SR_CSV)
    spec_time = {}  # SpecRef path -> commit time, memoized (bounds the git logs)
    out = []
    for w in open_wis:
        wi_time = wi_times.get(w["id"])
        if wi_time is None:
            continue  # the WI row is not yet in HEAD — no basis, skip silently
        for sr in w["srs"]:
            t = sr_times.get(sr)
            if t is not None and t > wi_time:
                out.append(
                    "{}: cites {} amended after the WI row was last touched — "
                    "{}".format(w["id"], sr, BACKLOG_REAFFIRM_HINT)
                )
        pathpart = w["specref"].split("#", 1)[0].strip()
        if pathpart:
            if pathpart not in spec_time:
                spec_time[pathpart] = _path_commit_time(root, pathpart)
            t = spec_time[pathpart]
            if t is not None and t > wi_time:
                out.append(
                    "{}: its SpecRef {} changed after the WI row was last touched "
                    "— {}".format(w["id"], pathpart, BACKLOG_REAFFIRM_HINT)
                )
    return out


# Mirror of wi_convert.SLUG_CHARS, duplicated here DELIBERATELY: this module is
# stdlib-pure with no wi_convert import, and adding one would mint a new
# cross-component seam just to read a number. tests/test_rule_sync.py pins the
# two equal, so drift is detectable rather than representable (the WI-462
# adversarial round's F3: the cap governs only the MINTED filename path, and a
# hand-filed spec could re-open the Windows MAX_PATH cliff unwatched).
_SLUG_CHARS_MIRROR = 30


def branch_length_findings(root):
    """Warn-only (2026-08-16b adversarial round, F3): a PRE-BRANCH spec whose
    filename stem exceeds what the minted path guarantees. dispatch derives the
    git branch from the on-disk stem VERBATIM (never re-slugified), so
    wi_convert.SLUG_CHARS caps only specs that were minted — a hand-filed
    queued/draft/deferred spec with a longer slug walks the same Windows
    MAX_PATH cliff WI-462 closed (measured there at 259/260 characters).
    Terminal and active states are exempt: their branch either exists already
    or never will. Never joins the exit code, even under --strict — the same
    warn-tier contract as every advisory in this module (WI-129/132)."""
    out = []
    for state in ("queued", "draft", "deferred"):
        d = Path(root) / "docs" / "work" / state
        if not d.is_dir():
            continue
        for p in sorted(d.glob("WI-*.md")):
            m = re.match(r"(WI-\d+)-", p.stem)
            if not m:
                continue  # the filename-carries-its-id rule reports that shape
            ceiling = len(m.group(1)) + 1 + _SLUG_CHARS_MIRROR
            if len(p.stem) > ceiling:
                out.append(
                    "{}: filename stem is {} chars (ceiling {}) — dispatch "
                    "derives the git branch from this stem verbatim, and past "
                    "the minted cap (wi_convert.SLUG_CHARS) a hand-filed name "
                    "re-opens the Windows MAX_PATH cliff WI-462 closed; "
                    "shorten the slug, keep the id prefix".format(
                        m.group(1), len(p.stem), ceiling
                    )
                )
    return out


def holdbyrename_findings(root):
    """A `docs/work/active/<branch>/` claim directory with NO matching git
    branch ref — the exact signature of a HOLD-BY-RENAME, which OI-70 BANS: a
    lane that must stop CLOSES PARTIAL (the only sanctioned stop), it is never
    parked by renaming its ref (`git branch -m ... -HELD`) while its claim stays
    on trunk. That mismatch is also the phantom head the scheduler/dispatcher
    disagree over: the row reads `ready` off the claim while the dispatcher
    silently skips it (no ref to resume), so the frontier's head is a lane the
    loop can never take.

    The claim-dir basename IS the branch short name (`integrate.claim` cuts
    `refs/heads/<branch>` for `active/<branch>/`), so the match is exact and the
    finding has no false-positive class: a lane mid-work always has its ref, and
    a closed lane has moved its specs out of `active/` — the only ref-less
    active claim is a rename-hold or a stranded leftover, both of which OI-70
    resolves by closing the lane.

    WARN at the commit bar, ERROR under `--strict` (the DevStg-Impl gate) — the
    warn-plain / error-under-strict tier the rest of this module's promotable
    findings ride (no new branch in `main`). Degrades silently off-git (a
    checkout with no history has no refs to match), the module's warn-tier
    contract."""
    active = Path(root) / WI_WORK / "active"
    if not active.is_dir():
        return []
    # Off-git: nothing to say. `rev-parse --git-dir` answers None only when git
    # cannot answer at all, so it separates "no repository" (degrade silently)
    # from "ref absent" (the finding) — which a per-ref `--verify` alone cannot,
    # since both return None.
    if _git(root, ["rev-parse", "--git-dir"]) is None:
        return []
    out = []
    for d in sorted(p for p in active.iterdir() if p.is_dir()):
        if not any(d.glob("WI-*.md")):
            continue  # an empty dir is a claim-machinery leftover, not a hold
        branch = d.name
        if (
            _git(root, ["rev-parse", "--verify", "--quiet", "refs/heads/" + branch])
            is None
        ):
            out.append(
                "hold-by-rename: claim directory {}/active/{}/ has no matching "
                "branch ref refs/heads/{} — a lane parked by renaming its ref is "
                "BANNED (OI-70): close it PARTIAL through the kit's own path (the "
                "handback report; nothing else), or delete the stranded claim. "
                "As it stands the scheduler reads this lane ready off the claim "
                "while the dispatcher can never resume it".format(
                    WI_WORK, branch, branch
                )
            )
    return out


def _tests_dir(root):
    """The declared tests root (docs/stack.ini [paths] tests), default `tests` —
    the surface a real validation-logic change would touch."""
    return _stack_ini_get(root, "paths", "tests") or "tests"


def _wi_status_map(rows):
    """`{wid: {"status", "srs"}}` for the real (non-`-000`) rows of a WI CSV."""
    out = {}
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if WI_ID_RE.match(wid) and not wid.endswith("-000"):
            out[wid] = {
                "status": (r.get("Status") or "queued").strip().lower(),
                "srs": _split_refs(r.get("SR-Refs", "")),
            }
    return out


def _head_spec_status_map(root):
    """`{wid: {"status", "srs": []}}` at HEAD in the folder registry, or None when
    HEAD carries no `docs/work` (so the caller falls back to the CSV at HEAD).

    Derived from `git ls-tree -r --name-only HEAD` PATHS ALONE — no blob is
    read. In this registry the directory IS the status, so the tree listing
    already answers the whole question the CSV needed a `git show` and a parse
    for; one subprocess, no content, no size dependence on the backlog.

    One honest limit remains, benign for the close ratchets that consume this:
    `srs` is empty, because SR-Refs are content too. `_staged_wi_registry` fills
    that from the WORKING TREE, where the same file is unchanged unless this very
    commit touched it. (The second limit is GONE with WI-384: `archive/` used to
    collapse `done` and `cancelled` behind a frontmatter key no tree listing can
    read, so a HEAD-cancelled item read `done`. Each terminal now has its own
    directory, so paths alone answer shipped-or-cancelled exactly.)"""
    out = _git(
        root, ["ls-tree", "-r", "--name-only", "HEAD", "--", WI_WORK, WI_ARCHIVE_WORK]
    )
    if not out or not out.strip():
        return None
    prefixes = (WI_WORK + "/", WI_ARCHIVE_WORK + "/")
    statuses = {}
    for name in out.splitlines():
        name = name.strip()
        prefix = next((p for p in prefixes if name.startswith(p)), None)
        if prefix is None or not name.endswith(".md"):
            continue
        parts = name[len(prefix) :].split("/")
        status = SPEC_STATUS_DIRS.get(parts[0]) if len(parts) > 1 else None
        wid = "-".join(parts[-1].split("-")[:2])
        if status is None or not WI_ID_RE.match(wid) or wid.endswith("-000"):
            continue
        statuses[wid] = {"status": status, "srs": []}
    return statuses or None


def _chain_untouched(root, staged_names, *extra_dirs):
    """Whether the staged change set leaves the VALIDATION CHAIN alone.

    The shared tail of both no-validation-delta ratchets: a close that touches
    neither the TC registry nor the tests dir landed the fix in the code and not
    in what judges it. `extra_dirs` widens what counts as the chain for a caller
    that accepts another kind of evidence (the critique ratchet also accepts a
    rubric anchor), which is the ONLY way the two sites differed — so the shared
    rule lives here and the difference stays visible at the call."""
    prefixes = (_tests_dir(root).rstrip("/") + "/",) + tuple(extra_dirs)
    return not any(name == TC_CSV or name.startswith(prefixes) for name in staged_names)


def _staged_wi_registry(root):
    """`(staged_names, cur_map, head_map)` for a commit that stages the WI
    registry, or `None` when there is nothing for a `--staged` check to say.

    The preamble every close-time check re-derived: the staged name set, the
    HEAD copy of the registry, and both status maps. `None` covers all three
    no-op cases uniformly — no git context, no registry change staged (so
    nothing was closed here), and no HEAD copy (first commit / file absent) — so
    a caller degrades silently off-git without restating the reason.

    Extracted for WI-344, forced early by WI-352 adding a fourth copy. The
    reason is F5's own boundary and outlives the tool that once flagged it: the
    F5 sanction buys cross-SCRIPT copy-ability, so it never licenses a fourth
    copy of the same preamble INSIDE one module. (The duplication census that
    reported this one was torn down in D-7/WI-426; the extraction stands.)
    (The CSV-home line-diff half retired with the CSV at Phase 5;
    `_staged_spec_registry` is the one implementation.)"""
    staged = _git(root, ["diff", "--cached", "--name-only"])
    if staged is None:
        return None
    staged_names = set(staged.splitlines())
    return _staged_spec_registry(root, staged_names, spec_work_dir(root / WI_CSV))


def _staged_spec_registry(root, staged_names, work_dir):
    """`_staged_wi_registry`'s folder-registry half.

    "The registry changed" becomes "a spec under `docs/work/` is staged", read
    with `--name-status` so a RENAME is visible as one record: a status change in
    this registry IS a rename, and `R<score>  queued/WI-360-x.md
    complete/WI-360-x.md` is exactly what a CLOSURE looks like. The closure SET is
    still derived by `_newly_closed` from the two status maps rather than from
    the `R` records — one home for that fact, and it stays correct even when git
    reports a move as an unpaired delete + add (rename detection is a heuristic;
    the status maps are not).

    HEAD status comes from the tree listing (`_head_spec_status_map`); a HEAD
    with no `docs/work/` at all (a repo's first registry commit) has nothing a
    close-time check can compare, so it degrades to None. (The CSV `git show`
    fallback for the 2c migration commit retired with the CSV home at Phase 5
    — that commit is history now.) HEAD `srs` are filled from the WORKING TREE
    row of the same id: in this registry one work item is one file, so a
    commit that closes A leaves B's SR-Refs untouched, and reading them from
    disk costs nothing. What that cannot see is a commit closing A while also
    editing B's SR-Refs; it would judge A against B's *new* refs. That is a
    narrower blind spot than a silent no-op, which is what "paths alone" would
    otherwise buy here."""
    changed = _git(
        root,
        ["diff", "--cached", "--name-status", "--", WI_WORK, WI_ARCHIVE_WORK],
    )
    if changed is None or not changed.strip():
        return None
    cur_map = _wi_status_map(read_spec_rows(work_dir))
    head_map = _head_spec_status_map(root)
    if head_map is None:
        return None
    for wid, head in head_map.items():
        head["srs"] = cur_map.get(wid, {}).get("srs", [])
    return staged_names, cur_map, head_map


def _newly_closed(cur_map, head_map):
    """The WI ids this staged change flips to `done`, with their current rows —
    the transition all three close-time ratchets key off."""
    return [
        (wid, cur)
        for wid, cur in cur_map.items()
        if cur["status"] == "done" and head_map.get(wid, {}).get("status") != "done"
    ]


def staged_findings(root):
    """The no-validation-delta warn (S0 ruling #2 corollary; warn-first).

    When a commit **closes** a WI (queued/active/deferred → done) that is a
    *follow-up* on an SR a previously-`done` WI already delivered (a shared
    `SR-Ref`), yet the staged change set touches neither the TC registry nor a
    file under the tests dir, the fix landed in the code but not the validation
    chain — so the same failure can recur. Returns warning strings ([] when not
    applicable). Compares the staged WI SPEC REGISTRY — the `docs/work/`
    directory-as-state tree `_staged_wi_registry` reads — against its HEAD
    version via git; any missing git context makes it a silent no-op (the hook
    has git; a gate run does not, and pays nothing). The registry has no CSV
    home to line-split any more: a status change is a RENAME between status
    directories, so both maps come from name listings (`--name-status` staged,
    `ls-tree` at HEAD) and never from parsing a row.

    Known false-positive, accepted at the WI-271 retirement (owner ruling
    2026-07-29): a follow-up WI whose chain change landed in its BUILD commit
    warns on its bookkeeping-only close commit — a moment's investigation, the
    lesser evil against a missed paper-close. Un-defer trigger: reopen (fresh
    WI) only if that noise erodes the signal — operators reflexively
    dismissing the warn. The footprint-aware widening is designed and ready in
    docs/archive/specs/WI-271.2026-07-29.md."""
    staged = _staged_wi_registry(root)
    if staged is None:
        return []
    staged_names, cur_map, head_map = staged

    prev_done_srs = {}  # SR id -> the done WI(s) that already delivered it
    for wid, h in head_map.items():
        if h["status"] == "done":
            for sr in h["srs"]:
                prev_done_srs.setdefault(sr, set()).add(wid)

    followups = []
    for wid, c in cur_map.items():
        was = head_map.get(wid, {}).get("status")
        if c["status"] == "done" and was != "done":
            shared = sorted(sr for sr in c["srs"] if sr in prev_done_srs)
            if shared:
                followups.append((wid, shared))
    if not followups:
        return []

    tests_prefix = _tests_dir(root).rstrip("/") + "/"
    if not _chain_untouched(root, staged_names):
        return []
    return [
        "{}: closes as a follow-up on {} (already delivered by a done WI) but "
        "the change set touches neither {} nor {} — the validation chain did "
        "not change (the fix must land in the chain, not just the code)".format(
            wid, ";".join(shared), TC_CSV, tests_prefix
        )
        for wid, shared in followups
    ]


# --- the acceptance record -------------------------------------------------
# WI-521 slice 1: the two-tree spine comparison and the snapshot mirror moved
# VERBATIM to the `acceptance_record` sibling (677 lines) — see that module's
# docstring for the boundary and why the requirements themselves asked for it.
# What is re-exported here is every name that block defined, under its former
# spelling, so no caller moved: `main` below still aggregates the four warn
# families, `intake.py` still reads `SPINE_CSVS`/`SPINE_TRACED_CELLS` and calls
# `staged_spine_amendments`/`staged_snapshot_findings`, `baseline_snapshot.py`
# still calls `split_changed_cells`/`_spine_rows_at`, and `trace.py` still calls
# `committed_snapshot_findings`. The private names are re-exported too, because
# the tests that pin this tier already reach them by their old spelling and a
# rename is not what this slice is measuring.
SPINE_CSVS = acceptance_record.SPINE_CSVS
SPINE_TABLE = acceptance_record.SPINE_TABLE
SPINE_COLUMN = acceptance_record.SPINE_COLUMN
SPINE_TRACED_CELLS = acceptance_record.SPINE_TRACED_CELLS
SPINE_APPROVED_CELLS = acceptance_record.SPINE_APPROVED_CELLS
HAT_REFS_CELL = acceptance_record.HAT_REFS_CELL
SNAPSHOT_DIR = acceptance_record.SNAPSHOT_DIR
SNAPSHOT_README = acceptance_record.SNAPSHOT_README
_APPROVED_TEXT = acceptance_record._APPROVED_TEXT
_spine_stem = acceptance_record._spine_stem
_spine_carriers = acceptance_record._spine_carriers
_spine_rows_at = acceptance_record._spine_rows_at
_spine_revs = acceptance_record._spine_revs
_snapshot_survives = acceptance_record._snapshot_survives
_snapshot_write_revs = acceptance_record._snapshot_write_revs
spine_cell_class = acceptance_record.spine_cell_class
traced_cells = acceptance_record.traced_cells
split_changed_cells = acceptance_record.split_changed_cells
staged_spine_amendments = acceptance_record.staged_spine_amendments
staged_spine_findings = acceptance_record.staged_spine_findings
staged_hat_refs_findings = acceptance_record.staged_hat_refs_findings
staged_snapshot_findings = acceptance_record.staged_snapshot_findings
committed_snapshot_findings = acceptance_record.committed_snapshot_findings


# The critique-loop ratchet (WI-068). A `Verification=Critique` SR and its latest
# CRITIQUE verdict file (`docs/reviews/*-CRITIQUE.md`, the S8 verdict format), in
# BOTH naming generations — serial `NNN-CRITIQUE.md` and the branch-scoped
# `WI-<n>-CRITIQUE.md` replacing it (concurrency-restructure §5.4, and
# `_latest_critique_file`, which reads both).
RUBRICS_DIR = "docs/rubrics/"
REVIEWS_DIR = "docs/reviews"
CRITIQUE_VERDICT_RE = re.compile(
    r"^\s*VERDICT:\s*(APPROVE|CHANGES-REQUESTED)\s*(?:findings\s*=\s*(\d+))?",
    re.I | re.M,
)

# The registry names its DESTINATION carrier; `spine_carrier.resolve` picks
# whichever of the two is live (repo-lock §8.1).
OPEN_ITEMS_REL = "docs/requirements/open-items.toml"
# A phase anchor appearing anywhere in a brief cell — the canonical
# `[<phase>]-[DevStg-<Rung>]` spelling (WI-498 slice 4) and the retired
# `[<phase>]-[reqs|tests]` / `[<phase>]-[g1|g2]` ones the committed briefs carry.
# Kept a SEPARATE pattern from PHASE_ANCHOR_RE because that one is anchored to the
# start of a Title and this one matches mid-cell; the accepted TOKEN SET is the
# same, and is held equal to it by a test rather than by this comment.
APPROVAL_ANCHOR_RE = re.compile(
    r"\[[^\]\[]+\]-\[(?:g[12]|reqs|tests|DevStg-[A-Za-z]+)\]", re.IGNORECASE
)
# The brief satisfies the rule only by naming an approval/hierarchy VIEW — a
# bare `trace.py --approve` command mention no longer counts (WI-146 REVIEW-A): a
# command can be unexecuted or wrong-scope, so it is not proof the generated view
# exists and is carried in the brief. WI-322 moved briefs from markdown sections
# to registry ROWS, so the proof is a path/link token in the cell rather than a
# markdown link — the rule is the same, its evidence shape follows the source.
# `ratif` stays in the token set deliberately (WI-499): the generated view still
# lives under `docs/ratify/` — the directory kept its name as a record home even
# though the retired-vocabulary rename covers everything else — so a real link
# still reads `docs/ratify/CURRENT.md` / `docs/ratify/<date>-*.md`. `approv` is
# matched too, for a link authored against the word the kit uses everywhere else.
APPROVAL_VIEW_RE = re.compile(
    r"(?:ratif|approv|hierarch)\w*[^\s]*\.(?:md|html|csv)|\]\([^)]*(?:ratif|approv|hierarch)[^)]*\)",
    re.IGNORECASE,
)


def approval_brief_findings(root):
    """Warn-first brief lint (WI-146b): an open-items row whose decision is a
    phase-anchor approval should point at the batch-scoped approval
    hierarchy view (`trace.py --approve <phase>`) instead of hand-copying registry
    rows. WARN only — never a gate fail (the house stance for prose surfaces,
    WI-129/132).

    Reads `docs/requirements/open-items.toml` since WI-322 retired the markdown
    surface; the brief text is the row's prose cells. Vacuous when the registry
    is absent or carries no approval brief, so a repo without the surface
    pays nothing."""
    path = root / OPEN_ITEMS_REL
    if spine_carrier.resolve(path) is None:
        return []
    out = []
    for row in spine_carrier.load(path, "OI-ID"):
        oid = (row.get("OI-ID") or "").strip()
        if not oid.startswith("OI-") or oid.endswith("-000"):
            continue
        if (row.get("Status") or "").strip().lower() != "pending":
            continue
        body = " ".join(
            (row.get(k) or "")
            for k in ("OneLine", "Decision", "BlastRadius", "Options", "Recommendation")
        )
        # `approv` (not `ratif`, WI-499): live prose no longer uses the retired
        # spelling, so a freshly-authored row's own text is the "this decision
        # is about a human approval" signal now.
        is_approval = APPROVAL_ANCHOR_RE.search(body) and re.search(
            r"approv", body, re.IGNORECASE
        )
        if not is_approval or APPROVAL_VIEW_RE.search(body):
            continue
        out.append(
            "{}: a phase-anchor approval brief should name the batch-scoped "
            "hierarchy view (generate it with `trace.py --approve <phase>`) instead "
            "of hand-copying registry rows ({})".format(oid, OPEN_ITEMS_REL)
        )
    return out


def _load_critique_srs(root):
    """SR ids whose Verification is `Critique` (system-requirements.toml). Empty
    makes the critique ratchet vacuous — a repo with no perceptual SR pays
    nothing."""
    out = set()
    for r in spine_carrier.load(root / SR_CSV, "SR-ID"):
        sid = (r.get("SR-ID") or "").strip()
        if (
            sid
            and not sid.endswith("-000")
            and (r.get("Verification") or "").strip() == "Critique"
        ):
            out.add(sid)
    return out


def _latest_critique_verdict(root):
    """`(verdict, findings)` of the latest CRITIQUE file (`_latest_critique_file`,
    the shared selection rule), or `(None, 0)`. The verdict file is not WI-tagged,
    so 'latest overall' is the honest proxy for 'the in-scope critique' (a recorded
    gap — the loop critiques one scope at a time, so the newest verdict is live)."""
    f = _latest_critique_file(root)
    if f is None:
        return None, 0
    try:
        text = f.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, 0
    m = CRITIQUE_VERDICT_RE.search(text)
    if not m:
        return None, 0
    return m.group(1).upper(), int(m.group(2) or 0)


def critique_ratchet_findings(root):
    """The lax-TC ratchet for the critique loop (WI-068; warn-first, the same
    no-validation-delta idea as `staged_findings`). When a staged commit **closes**
    a WI whose `SR-Refs` include a `Verification=Critique` SR, the latest CRITIQUE
    verdict is CHANGES-REQUESTED with findings, yet the staged set touches **neither**
    the TC registry, the tests dir, **nor** a `docs/rubrics/` file, the fix landed in
    the artifact but not the validation chain — so the same 'shipped it because
    nothing judged it' can recur. Returns warning strings ([] when not applicable).
    Any missing git context makes it a silent no-op, like `staged_findings`.

    Implements: SR-157, LLR-084
    """
    critique_srs = _load_critique_srs(root)
    if not critique_srs:
        return []
    verdict, findings = _latest_critique_verdict(root)
    if verdict != "CHANGES-REQUESTED" or findings <= 0:
        return []
    staged = _staged_wi_registry(root)
    if staged is None:
        return []
    staged_names, cur_map, head_map = staged

    closing = []
    for wid, c in _newly_closed(cur_map, head_map):
        shared = sorted(sr for sr in c["srs"] if sr in critique_srs)
        if shared:
            closing.append((wid, shared))
    if not closing:
        return []

    tests_prefix = _tests_dir(root).rstrip("/") + "/"
    if not _chain_untouched(root, staged_names, RUBRICS_DIR):
        return []
    return [
        "{}: closes on Critique-verified {} while the latest CRITIQUE verdict is "
        "CHANGES-REQUESTED ({} finding(s)), but the change set touches neither {}, "
        "{}, nor {} — harden the TC or add a rubric anchor (the fix must land in "
        "the chain, not just the artifact)".format(
            wid, ";".join(shared), findings, TC_CSV, tests_prefix, RUBRICS_DIR
        )
        for wid, shared in closing
    ]


# The render surface a perceptual (Verification=Critique) SR is judged against —
# WI-243. The dashboard GENERATOR (`gen_trajectory.py`, located beside this
# checker so the path resolves under `--root` in this repo and a downstream
# scaffold alike) plus the optional meta-only render recipe. A change to either
# after the latest CRITIQUE means the approved perceptual stamp judged an older
# render, so the critique should re-fire.
_RENDER_RECIPE_REL = "scripts/dashboard-shots/shoot.mjs"


# WI-280 split the dashboard generator into `gen_trajectory.py` (the facade:
# HTML_TEMPLATE + build_html) plus the `traj_*.py` siblings that hold every
# emitter. The render surface is the WHOLE family — after the split, a change
# that alters the rendered pixels lands in a sibling far more often than in the
# facade, so watching the facade alone would have silently retired this warn.
_RENDER_SURFACE_GLOB = "traj_*.py"


def _render_surface_paths(root):
    """Repo-relative render-surface paths that EXIST under `root`: the co-located
    dashboard generator `gen_trajectory.py`, its WI-280 `traj_*.py` split siblings
    (which hold the emitters), and the render recipe if the repo carries one. A
    downstream without the meta-only recipe pays nothing for it; an unlocatable
    generator yields no path (the check then stays silent).

    Accepted warn-first boundary: layout-affecting values the family IMPORTS from
    modules OUTSIDE it (e.g. a display constant defined in this checker) are NOT
    watched — folding them in would fire the warn on every unrelated edit to those
    modules. The surface is the generator family + recipe themselves; a render
    change that lands only in an externally-imported constant is a known,
    tolerated miss."""
    out = []
    here = Path(__file__).resolve().parent
    gen = here / "gen_trajectory.py"
    try:
        rel = gen.relative_to(root)
        if gen.is_file():
            out.append(rel.as_posix())
        # The split siblings live beside the facade; sorted so the warn's path
        # list is deterministic.
        for sib in sorted(here.glob(_RENDER_SURFACE_GLOB)):
            out.append(sib.relative_to(root).as_posix())
    except ValueError:
        # the checker is not under root (unusual) — try the kit's two homes.
        for cand in (
            "project-trajectory/scripts",
            "scripts",
        ):
            if (root / cand / "gen_trajectory.py").is_file():
                out.append(cand + "/gen_trajectory.py")
                out.extend(
                    sorted(
                        (root / cand / s.name).relative_to(root).as_posix()
                        for s in (root / cand).glob(_RENDER_SURFACE_GLOB)
                    )
                )
                break
    if (root / _RENDER_RECIPE_REL).is_file():
        out.append(_RENDER_RECIPE_REL)
    return out


def _critique_git_times(root, names):
    """`{filename: committer-time-epoch}` for the `docs/reviews` critique files git
    has history for, from ONE `git log --format=%ct --name-only` over the directory:
    the log walks newest-first, so the FIRST sighting of a path is its last-touched
    time — what `_path_commit_time` answers per path. {} on any git failure, the
    silent degrade every git call here makes. Batched rather than one
    `_path_commit_time` per file because this runs at the commit bar and the
    reviews dir only grows: 20 critiques cost ~1.3s in per-path subprocesses
    here, ~0.1s as one call, whatever the count."""
    out = _git(root, ["log", "--format=%ct", "--name-only", "--", REVIEWS_DIR])
    if out is None:
        return {}
    times = {}
    when = None
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.isdigit():  # a %ct header line; a path line never is
            when = int(line)
            continue
        # `--name-only` prints REPO-root-relative paths, which need not equal
        # `root`-relative ones — match on the directory suffix, which also drops
        # the train-scoped `docs/reviews/<train>/` files (a deeper head).
        head, _, name = line.rpartition("/")
        if when is not None and head.endswith(REVIEWS_DIR) and name in names:
            times.setdefault(name, when)
    return times


def _latest_critique_file(root):
    """The LATEST `docs/reviews/*-CRITIQUE.md` path by last-change TIME, or None —
    the single selection rule shared by `_latest_critique_verdict` and the WI-243
    staleness check.

    Selection is by time, not by name, and the glob accepts BOTH naming
    generations: the historical serial `NNN-CRITIQUE.md` and the branch-scoped
    `WI-<n>-CRITIQUE.md` that replaces it (docs/concurrency-restructure.md §5.4 —
    a next-number counter is a race under concurrency). The two do not sort
    against each other at all, so the old highest-number rule could not survive
    the mix; it was also wrong on its own terms, a fresh critique filed under a
    LOWER number losing to a stale higher-numbered one. The ladder, per file:
    (1) the committer time of the last commit to touch it (`_critique_git_times`,
    one batched `git log`); (2) its filesystem mtime, when git answers nothing —
    uncommitted evidence, or a scaffold that is no git repo at all; (3) its
    filename, greatest wins, as the final tie-break, so equal times still select
    ONE file deterministically (two critiques in one commit, the batch case).
    Both time rungs are wall-clock epochs, so a committed and an uncommitted file
    still compare meaningfully. What time does NOT answer is SCOPE: the verdict
    file is still not matched against the WI under judgement — the recorded proxy
    `_latest_critique_verdict` documents."""
    d = root / REVIEWS_DIR
    if not d.is_dir():
        return None
    files = sorted(d.glob("*-CRITIQUE.md"))
    if not files:
        return None
    git_times = _critique_git_times(root, {p.name for p in files})

    def _when(path):
        t = git_times.get(path.name)
        if t is None:
            try:
                t = path.stat().st_mtime
            except OSError:
                t = 0
        return (t, path.name)

    return max(files, key=_when)


def critique_staleness_findings(root):
    """The perceptual re-fire finding (WI-243; git-time staleness like
    `backlog_staleness_findings`). A `Verification=Critique` SR is judged by a
    human/critic look recorded in `docs/reviews/*-CRITIQUE.md`, and that verdict
    never re-fires on its own — so once the dashboard *render surface* changes,
    the approval stamp is judging an older render. When a render-surface path (the
    co-located `gen_trajectory.py`, plus the render recipe if present) last
    changed STRICTLY AFTER the latest CRITIQUE evidence, flag that the perceptual
    gate is stale and the dashboard critique should be re-run against the current
    render. Returns finding strings ([] when not applicable).

    TIERED severity (set by the caller): WARN at the commit bar, ERROR under
    `--strict` (the DevStg-Impl gate) — fail-closed per the owner's 2026-07-20 ruling, a
    stale render surface cannot reach a green gate; main() routes it through the
    strict-promotable findings loop (the R-E warn tier). Silent off-git
    and vacuous when the repo declares no perceptual SR (so a downstream repo
    without a `Verification=Critique` SR — none ship — pays nothing at either
    tier), carries no CRITIQUE evidence, or exposes no locatable render surface.
    Bounded cost: one `git log -1` for the evidence plus one per render-surface
    path (≤ 2 here). By construction (git-time, not a render diff) it fires on ANY
    commit touching a render-surface path — a data-only or comment-only edit to the
    generator flags even with zero visual change — the false-positive-over-
    false-negative trade the sibling `backlog_staleness` also makes."""
    critique_srs = _load_critique_srs(root)
    if not critique_srs:
        return []
    evidence = _latest_critique_file(root)
    if evidence is None:
        return []
    try:
        ev_rel = evidence.relative_to(root).as_posix()
    except ValueError:
        ev_rel = REVIEWS_DIR + "/" + evidence.name
    ev_time = _path_commit_time(root, ev_rel)
    if ev_time is None:
        return []  # uncommitted / off-git evidence — no basis, silent
    newer = [
        rel
        for rel in _render_surface_paths(root)
        if (_path_commit_time(root, rel) or 0) > ev_time
    ]
    if not newer:
        return []
    return [
        "{} (Verification=Critique) last judged by {} but the dashboard render "
        "surface changed after it ({}) — re-run the dashboard critique against the "
        "current render (the shoot.mjs matrix) and record a fresh "
        "docs/reviews/*-CRITIQUE.md".format(
            ";".join(sorted(critique_srs)), ev_rel, ";".join(newer)
        )
    ]


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="promote the registry coherence rules R-E (open-WI SpecRef resolves) "
        "and R-F (done WI clears SpecRef; a live spec has an open citer) "
        "from WARN to ERROR (wired at gate DevStg-Tests+; R-A always fails regardless)",
    )
    ap.add_argument(
        "--staged",
        action="store_true",
        help="run ONLY the warn-first no-validation-delta check over the staged "
        "commit (needs git; a silent no-op outside a git checkout)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if not read_trajectory_enabled(root):
        print(
            "check_trajectory: off (docs/process.toml [checks] trajectory_check) "
            "— nothing to check."
        )
        return 0

    # --staged is the commit-time no-validation-delta warn only: never blocks,
    # never re-runs the full validation (the trajectory step already did). The
    # warns, in the order they print (the count is deliberately not stated — it
    # went stale twice): the follow-up-on-a-done-SR ratchet, the critique-loop
    # ratchet (a WI closing under a CHANGES-REQUESTED critique without hardening
    # the chain), the WI-316 amend-without-flip warn (attested spine prose
    # changed without a fresh blessing) and its WI-484 Hat-Refs arm (the
    # substance moved, the perspective record did not), the mirror invariant
    # below, and the WI-352 close-time
    # completion warn (the row flips to `done` while its spec still has unticked
    # Done-when boxes — the only moment that disagreement is cheaply fixable,
    # since archival leaves nothing but a cosmetic edit).
    if args.staged:
        for w in (
            staged_findings(root)
            + critique_ratchet_findings(root)
            + staged_spine_findings(root)
            # ...and its second arm (WI-484 phase 5, OI-33's residue): the same
            # amendment set read for a row whose PERSPECTIVE cell stayed put
            # while its substance moved. Silent on a traced-only edit, which is
            # the regression the phase-2 backfill measured on a line-blamed
            # neighbour check.
            + staged_hat_refs_findings(root)
            # The MIRROR INVARIANT (snapshot design §F3): a commit that touches
            # the `last_approved` snapshot must leave every touched file
            # byte-identical to its live counterpart. This is the replacement
            # for the co-mutation guard D-1's anchor half would have needed —
            # and it is a stronger rule, because it makes "the only way to write
            # the snapshot is to copy the live file" a decidable property rather
            # than a convention. Vacuous until a snapshot exists.
            + staged_snapshot_findings(root)
            + staged_completion_findings(root)
        ):
            print("check_trajectory: WARN - {}".format(w), file=sys.stderr)
        return 0

    # Architecture-connectivity coverage (S5/WI-056; process.md §8) — warn-first,
    # never an exit-code change (even under --strict). Runs before the WI vacuity
    # return so a repo with modules + seams but no work items is still covered;
    # vacuous under [checks] interfaces_check = false or a ≤1-module arch-map.
    # ...and the multi-membership overlap advisory (WI-440; OI-14's third
    # do-not-wait) shares this WARN-ONLY loop rather than the component block
    # below: it reports the cross-component edges a multi-tagged endpoint
    # SILENCES, which is a question about the PARTITION rather than a defect in
    # the edge, and no partition has been ruled — so it must never join the exit
    # code, not even under --strict, which the component block would do.
    # ...and the seam-TC-coverage allowlist HYGIENE advisory (WI-488) shares it
    # for the same reason: a stale (now-covered, or now-retired) allowlist entry
    # is never itself a defect, so it must never join the exit code either — the
    # PROMOTABLE half of seam-TC coverage is `if_tc_coverage_findings`, below,
    # deliberately kept out of this loop.
    for w in (
        interface_findings(root)
        + cross_component_advisories(root)
        + if_tc_allow_hygiene_findings(root)
        + codesymbol_crosscheck_findings(root)
    ):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    # Approval-brief hierarchy-view lint (WI-146b) — warn-first prose-surface
    # check: a `[phase]-[g1|g2]` approval brief should link the generated
    # batch-scoped hierarchy view. Vacuous without an approval brief.
    for w in approval_brief_findings(root):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    # How-SW top-view right-sizing (WI-073/FB5) — WARN plain, ERROR under --strict
    # (DevStg-Tests+). Runs before the WI vacuity return too (the bound is a property of the
    # arch-map inventory + the component registry, independent of work items), so
    # a repo with a big arch-map and no CMP rows still trips even with no WIs.
    comp_errors = []
    for msg in component_findings(root):
        if args.strict:
            comp_errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)

    # Seam-TC coverage promotion (OI-43 ruled (a), WI-488) — WARN plain, ERROR
    # under --strict (DevStg-Tests+), the component_findings idiom. Runs here
    # (not in the wi-scoped block below) for the same reason component_findings
    # does: the finding is a property of the arch-map + interfaces + TCs, not of
    # the WI registry, so a repo with no work items still gets it.
    if_tc_errors = []
    # ...and the armed definition gate (OI-67 slice 6) rides the same
    # severity: a row with no stated body is an interface with no definition.
    for msg in (
        if_tc_coverage_findings(root)
        + if_tc_allow_parse_findings(root)
        + contract_body_findings(root)
    ):
        if args.strict:
            if_tc_errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)

    # The one registry home (Phase 5): `docs/work/` specs. Any finding about
    # the REGISTRY ITSELF — a malformed spec, or a stray resurrected CSV — is
    # an integrity error, the same tier as a malformed id. (WI-349's
    # physical-line cell check retired with the CSV home: nothing reads the
    # folder registry line-wise, so a Deliverable body's newline is the format
    # working as designed; `cell_integrity_errors` survives for the spine
    # CSVs' own callers/tests.)
    registry_errors = []
    wi_rows = read_registry_rows(root / WI_CSV, registry_errors)
    wis, integrity = load_wis(wi_rows)
    integrity = registry_errors + integrity
    if not wis and not integrity:
        arch_errors = comp_errors + if_tc_errors
        if arch_errors:
            for e in arch_errors:
                print("check_trajectory: ERROR - {}".format(e), file=sys.stderr)
            print(
                "check_trajectory: {} architecture finding(s).".format(
                    len(arch_errors)
                ),
                file=sys.stderr,
            )
            return 1
        print(
            "check_trajectory: clean (no work items — placeholder-only or absent "
            "registry; vacuously clean)."
        )
        return 0

    # Phase archetype + phase-drop detector (WI-093) — WARN-FIRST, never an
    # exit-code change (like the connectivity coverage). Vacuous on a single-phase
    # repo with no `[phase]-[g*]` anchors (the meta case).
    for w in phase_findings(root, wis):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    errors = (
        comp_errors
        + if_tc_errors
        + integrity
        + validate(wis, load_known_srs(root), load_known_ois(root))
    )
    # Specs act on declared interface boundaries (WI-191) — WARN plain, ERROR
    # under --strict (DevStg-Tests+); vacuous until a spec adopts an `## Interfaces` section.
    for msg in spec_interface_findings(root):
        if args.strict:
            errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)
    # status.md forward-only (WI-200; the mode-aware R-D restoration) — WARN plain,
    # ERROR under --strict (DevStg-Tests+); yields to a status.md generated-block marker.
    for msg in status_forward_only_findings(root, wis):
        if args.strict:
            errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)
    # Backlog-staleness (WI-205) — an open WI whose cited SR row or SpecRef target
    # was amended AFTER the WI row was last touched is re-flagged for a driven
    # re-validation. WARN-ONLY: it never joins the exit code, not even under
    # --strict (the WI-129 warn-tier-checker stance); silent off-git.
    # ...and the pack-citation warn (WI-388, consumer 3 of the intake context
    # block) rides the same WARN-ONLY tier: never the exit code even under
    # --strict — advisory is the block's contract, and minted rows satisfy it
    # by construction (their ## Context cites the packs), so it reaches
    # exactly the hand-authored residue.
    # ...as does LLR-160's queue-conflict pre-filter: overlap between
    # two OPEN rows is frequently correct, so this rung's whole contribution is
    # making it visible. Never the exit code, not even under --strict — a
    # checker that cannot tell a legitimate split from a duplicate must not
    # block on the difference.
    for msg in (
        backlog_staleness_findings(root, wis)
        + knowledge_pack_findings(root, wis)
        + queue_conflict_findings(wis)
        + branch_length_findings(root)
    ):
        print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)
    # The SSOT coherence layer: R-A is always an error; R-E, the
    # unknown-status lint are WARN unless
    # --strict promotes them.
    findings = ssot_findings(wis, root)
    # Dead dependency (WI-267): an open WI hard-depends on a cancelled (terminal
    # WON'T-BUILD) predecessor it can never see satisfied. WARN plain, ERROR under
    # --strict — same warn-tier as R-E (no new branch in main).
    findings.extend(("dead-dep", False, msg) for msg in dead_dependency_findings(wis))
    # Perceptual re-fire (WI-243) — a Verification=Critique SR whose latest CRITIQUE
    # evidence predates a dashboard render-surface change is judging an older render.
    # WARN at the commit bar; **fail-closed under --strict** (the DevStg-Impl gate) per the
    # owner's 2026-07-20 ruling — a stale render surface cannot reach a green gate.
    # hard=False rides the same warn-plain / error-under-strict tier as R-E,
    # so main() gains no branch. Vacuous when no perceptual SR / evidence / render
    # surface (a downstream repo without a Verification=Critique SR — none ship —
    # pays nothing), silent off-git, and opt-out via [checks] trajectory_check.
    findings.extend(
        ("perceptual-stale", False, msg) for msg in critique_staleness_findings(root)
    )
    # Spec-lifecycle close side (WI-251, rule R-F) — done WI with a live SpecRef,
    # or a live docs/specs file no open WI cites. Same warn-plain / error-under-
    # --strict tier (no new branch in main); the R-E open-half's closing
    # counterpart.
    findings.extend(("R-F", False, msg) for msg in spec_lifecycle_findings(root, wis))
    # Hold-by-rename ban (WI-553, OI-70) — a ref-less `active/<branch>/` claim
    # directory. Same warn-plain / error-under-strict tier as R-E/R-F (no new
    # branch in main); silent off-git.
    findings.extend(
        ("hold-by-rename", False, msg) for msg in holdbyrename_findings(root)
    )
    # Completion reconciliation (WI-352) — the declared `Status` cell against the
    # spec's Done-when boxes and the `WI:` trailers. WARN plain, ERROR under
    # --strict, the same warn tier as R-E/R-F, EXCEPT the trailer signal.
    #
    # DEVIATION from the WI row, which asked for the whole reconciler at that
    # tier, taken on the row's OWN argument: it rules that Status stays an
    # attestation precisely because a trailer means "a commit claims this WI",
    # not "the work is right", and cites WI-336 — code landed, row correctly left
    # `queued`, a review having refuted three of its claims. Under an
    # error-under-strict trailer rule that legitimate state blocks the DevStg-Impl gate
    # for as long as the rework takes, and the only ways out are to close the row
    # falsely or to carry an untracked exception. Spec evidence is different in
    # kind: a ticked box IS an attestation, so its disagreement with the row is a
    # contradiction between two homes for one fact and belongs at the gate.
    warn_only, gated = tier_completion_findings(
        completion_reconciliation_findings(root, wis)
    )
    for msg in warn_only:
        print("check_trajectory: WARN - completion {}".format(msg), file=sys.stderr)
    findings.extend(("completion", False, msg) for msg in gated)
    for rule, hard, msg in findings:
        line = "{} {}".format(rule, msg)
        if hard or args.strict:
            errors.append(line)
        else:
            print("check_trajectory: WARN - {}".format(line), file=sys.stderr)
    if errors:
        for e in errors:
            print("check_trajectory: ERROR - {}".format(e), file=sys.stderr)
        print(
            "check_trajectory: {} error(s) in {}.".format(
                len(errors), registry_home(root)
            ),
            file=sys.stderr,
        )
        return 1

    done = sum(1 for w in wis if w["status"] == "done")
    # WI-267: `cancelled` (terminal WON'T-BUILD) rows are counted SEPARATELY,
    # never folded into `done`; surfaced only when present so the line stays
    # unchanged for the common no-cancellation registry.
    cancelled = sum(1 for w in wis if w["status"] == "cancelled")
    cancelled_note = ", {} cancelled".format(cancelled) if cancelled else ""
    print(
        "check_trajectory: clean ({} work item(s), {} done ({}%){}, graph "
        "acyclic).".format(len(wis), done, round(100 * done / len(wis)), cancelled_note)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
