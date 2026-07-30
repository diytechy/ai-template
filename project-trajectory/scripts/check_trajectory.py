#!/usr/bin/env python3
"""Validate the work-item registry — stdlib only.

The registry home is the spec folder `docs/work/` (one file per work item,
status = directory; the CSV home retired at concurrency-restructure Phase 5,
RULING-4). Every rule below reads the same 17-key rows `read_registry_rows`
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
  - every `SR-Refs` id exists in `system-requirements.csv` — a WARN, not a
    failure (a draft SR referenced ahead of its registry row is legitimate).

**The registry SSOT rules** (S1; process-options.md "Trajectory /
work-items layer"). The WI `Deliverable` is **backward-only** (what shipped) and
the per-WI `SpecRef` is the forward bridge that lives while the WI is open and
clears at close. Cross-reading `work-items.csv` and its SpecRefs mechanizes two
rules:
  - **R-A** — a WI's `Deliverable` is non-empty **iff** its `Status` is
    **terminal** (`done` or `retired`; WI-267). An open (queued/active/deferred)
    WI with a filled Deliverable, or a terminal WI with an empty one, is a hard
    **ERROR at every run** (no flag needed): a commit is the agent handoff point,
    so an incoherent WI state launches the next session wrong. (`done` records
    what shipped; `retired` records why it never will.)
  - **R-E** — every open WI carries a non-empty `SpecRef` resolving to an in-repo
    target (`path` or `path#anchor`; the path part must exist). A terminal WI is
    exempt (its SpecRef is cleared — R-F).
  - **R-F** (WI-251; WI-267) — the close side R-E leaves unstated: a **terminal**
    (`done`/`retired`) WI's `SpecRef` is **empty**, and every live `docs/specs/`
    file (scaffold README/`-000` boilerplate excluded) is cited by at least one
    *open* WI — otherwise it belongs in `docs/archive/specs/` (the specs README
    lifecycle).
R-E and R-F are **WARN by default, ERROR under `--strict`** (wired at G2+). R-B/R-C —
every *open* WI repeated as a token in `status.md` — stay **retired** (WI-180):
status becomes an integrator-generated snapshot, so open-id currency is enforced
by generated freshness, not by copying the registry back into prose. **R-D is
RESTORED, mode-aware (WI-200):** `status.md` is forward-only, so a `done` WI id
lingering there is a finding — WARN plain, ERROR under `--strict` — *except* when
the file carries the kit's generated-block marker (`<!-- BEGIN GENERATED ... -->`,
the `gen_arch_map`/`gen_trajectory` idiom), where it is an integrator snapshot
that cannot accrete prose and the successor freshness check applies (specified in
`status_forward_only_findings`, not yet implemented — no status.md generator
exists). `--staged` adds the warn-first **no-validation-delta** checks: the
follow-up-on-a-done-SR ratchet, the **critique-loop ratchet** (WI-068) — a WI
closing on a `Verification=Critique` SR while the latest `docs/reviews/*-CRITIQUE.md`
verdict is CHANGES-REQUESTED, without the staged set touching the TC registry, the
tests dir, or a `docs/rubrics/` file (harden the TC or add a rubric anchor) — and
the **amend-without-flip** warn (WI-316): a staged diff changing content cells of
a `Verified` spine row without setting the `Modified` re-attest marker
(process.md §7), the write-time discipline commit-message prose never had.

**Opt-out and vacuous by default** — the posture of the always-on
`docs/secrets-scan` floor. The check is on unless `docs/trajectory-check` reads
the one word `off`; and an *absent* or *placeholder-only* registry (nothing but
the inert `WI-000` example row) passes vacuously. So a fresh scaffold and a repo
that never adopts the layer both stay green for free — WI is an off-spine
optional registry, like procurement / assets, whose placeholder never blocks a
gate (`trace.py` does not read WI ids at all).

**Architecture-connectivity coverage** (S5/WI-056; process.md §8). This step is
also the views-checker for the interface layer: every module in the arch-map
inventory (`docs/architecture.md`'s generated block) should appear as ≥1 IF-###
endpoint, each Active seam should be cited by a TC, and a `Contracts: IF-###`
docstring citation should match the registry. All **warn-first** (they never
change the exit code, at any gate) and printed at the hook. The ruled posture is
**opt-out, default-on**: the coverage warn fires even when `interfaces.csv` is
empty or absent — a multi-module arch-map with no declared seams reads
"connectivity undeclared" instead of passing vacuously. It is silenced only by
the one word `off` in `docs/interfaces-check`, or a ≤1-module inventory (nothing
to connect). The honesty valve for a deliberate source/sink is a `source`/`sink`
token in that module's IF row Notes (below).

**How-SW top-view right-sizing** (WI-073/FB5; process-options.md "Component
layer"). The software-architecture diagram's *first view* must show at most
``TOP_VIEW_MAX`` (10) items: top-level components (a `CMP-###` with no `PartOf`
that contains ≥1 arch-map module) plus **uncontained** modules (a module with no
`Component`-tagged LLR). Exceeding the bound is a **finding** — WARN at the
plain/hook run, **ERROR under `--strict` (G2+)** — that drives right-sizing of
the component designations. Membership derives from the AXES join: a `Component`
tag on an LLR row joins its `Module` → `CMP-###`; nesting via the CMP registry's
`PartOf` (a module counts only at its top-level root). Opt-out is the one word
`off` in `docs/components-check` (the `interfaces-check` idiom); a repo with ≤10
modules — or no arch-map inventory — passes trivially (the bound, not the
registry, is the rule), so a small or non-adopting repo is never broken.

**Knowledge⇒component coupling** (WI-153; research-knowledge.md §3a, owner-ruled
2026-07-14). The same finding is *armed independent of the bound* once
`docs/knowledge/` holds a real pack: an uncontained arch-map module is then a
finding even below the 10-item bound, because a knowledge pack ties the *what* to
the knowledge behind the *how*, so that web must be robust wherever packs are
enabled. It reuses the existing `Component`-tag join (no new join) and the same
`docs/components-check` opt-out, and is dormant — costing a non-adopter nothing —
until a pack (any `docs/knowledge/*.md` but the `README.md` index) exists.

**Phase archetype + phase-drop detector** (WI-093; derived-gate model §7/§9.3).
A phase's pre-dev batch is a first-class WI whose Title carries a `[<phase>]-[g<N>]`
tag (`[v2]-[g1]` = requirement structuring, `[v2]-[g2]` = decomposition + TCs).
This step recognizes those anchors and, reading the derived per-phase levels from
`docs/gate`'s `# basis:` line, warns when a phase's derived gate has **dropped
below** the level its own closed `[phase]-[gN]` anchor recorded — the signal that
new or reopened content entered and a new phase-gate WI is due. All **warn-first**
(never an exit-code change, at any gate); vacuous on a single-phase repo with no
anchors (the meta case) or a legacy `docs/gate` with no basis line.

Usage:  python scripts/check_trajectory.py [--root .] [--strict] [--staged]
Exit codes: 0 clean / vacuous / opted-out, 1 a hard error, 2 usage/environment.

Contracts: IF-009, IF-023, IF-077 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv). IF-077 (WI-354) is the ANCHOR-resolution seam: R-E resolves a SpecRef's `#anchor` through check_docs.parse_doc so one slugifier defines an anchor in both homes — a lazy import that degrades to path-only, since this module runs in the shipped pre-commit hook.
"""

import argparse
import configparser
import csv
import difflib
import io
import re
import subprocess
import sys
import tomllib
from pathlib import Path

WI_CSV = "docs/requirements/work-items.csv"
# The spec-folder home the CSV above gives way to (Phase 2b of
# docs/concurrency-restructure.md). Declared as a repo-relative POSIX path
# because the git plumbing below passes it as a PATHSPEC; the reader derives
# the same folder from the CSV path via `spec_work_dir`.
WI_WORK = "docs/work"
SR_CSV = "docs/requirements/system-requirements.csv"
TC_CSV = "docs/test/test-cases.csv"
IF_CSV = "docs/requirements/interfaces.csv"
LLR_CSV = "docs/requirements/low-level-requirements.csv"
CMP_CSV = "docs/requirements/components.csv"
ARCH_MD = "docs/architecture.md"
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
# A CMP-### component id token (process-options.md "Component layer"). trace.py
# owns CMP integrity; this loader is lenient (skips a malformed id) — it only
# feeds the warn-first top-view coverage.
CMP_ID_RE = re.compile(r"^CMP-\d+$")

# A well-formed work-item id: `WI-` then digits (`WI-001`). The `-000` example
# row matches this shape but is inert (skipped from the graph — see load_wis).
WI_ID_RE = re.compile(r"^WI-\d+$")

# The work-item lifecycle vocabulary (S1). `deferred` is a first-class,
# queued-but-not-next state carrying a recorded reason; `blocked` is parked on a
# named external dependency. `retired` (WI-267) is a TERMINAL won't-build row that
# stays in the registry forever with its reason in the `Deliverable` column — a
# deliberate dead-end, NOT an overload of `done` (a `done` WI shipped something; a
# `retired` WI deliberately never will). Since Phase 5 status is the spec's
# DIRECTORY (an unknown one is a loader refusal) and `blocked` is DERIVED
# (queued + blockref) rather than a status; the literal stays in these sets so
# in-memory callers keep their meaning, but no loader can produce it.
# "Open" = anything still in flight (not one of the two TERMINAL states).
OPEN_STATUSES = ("queued", "active", "deferred", "blocked")
# The terminal states: no further build/trace work is owed. Both require a filled
# `Deliverable` (the shipped record for `done`; the retirement reason for
# `retired`) and both must clear their `SpecRef` (R-A + R-F below). `retired` is
# deliberately NOT in OPEN_STATUSES / BACKLOG_STALE_STATUSES / the ready frontier.
TERMINAL_STATUSES = ("done", "retired")
KNOWN_STATUSES = ("queued", "active", "done", "deferred", "blocked", "retired")

# Backlog-staleness (WI-205) applies to genuinely-in-flight WIs: the open set
# minus `deferred` (a deferred WI re-enters via an owner un-defer, itself the
# driven look, so it is EXEMPT), plus `blocked` (a WI parked on an external
# dependency is still live work whose cited requirements can drift under it).
# `done`/`retired` are terminal and need no re-validation.
BACKLOG_STALE_STATUSES = ("queued", "active", "blocked")


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII work-item title / path can't raise UnicodeEncodeError on a legacy
    Windows cp1252 console (same guard as check.py / check_privacy.py)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _first_declared_line(path):
    """The first non-empty, non-comment line of a declared-policy file, or None
    (absent/empty) — the parse every kit reader shares (hooks, check_privacy.py,
    agent_loop.py)."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def read_trajectory_enabled(root):
    """Whether the trajectory check is on. `docs/trajectory-check` with the one
    word `off` opts out; absent or any other value reads on (the safe default),
    so an ordinary repo runs it without declaring anything — opt-out, like
    `docs/secrets-scan`."""
    return (
        _first_declared_line(root / "docs" / "trajectory-check") or ""
    ).lower() != "off"


def read_interfaces_check_enabled(root):
    """Whether the architecture-connectivity coverage warns are on (S5/WI-056).
    `docs/interfaces-check` with the one word `off` opts out; absent or any other
    value reads on — the ruled opt-out, default-on posture (same shape as
    `docs/trajectory-check`). Default-on means the coverage warn fires even with
    an empty/absent `interfaces.csv`; the off-switch or a ≤1-module inventory is
    the only silence."""
    return (
        _first_declared_line(root / "docs" / "interfaces-check") or ""
    ).lower() != "off"


def read_components_check_enabled(root):
    """Whether the How-SW top-view right-sizing rule is on (WI-073/FB5).
    `docs/components-check` with the one word `off` opts out; absent or any other
    value reads on — the ruled opt-out, default-on posture (same shape as
    `docs/interfaces-check`). Like that reader there is no scaffolded file:
    absence reads on, so a repo that never declares anything is still bounded."""
    return (
        _first_declared_line(root / "docs" / "components-check") or ""
    ).lower() != "off"


def _split_refs(cell):
    """Ref cells hold ids separated by ; , or whitespace; empty -> []."""
    return [t for t in re.split(r"[;,\s]+", (cell or "").strip()) if t]


def read_rows(path):
    """The CSV rows of `path` as dicts, or [] when the file is absent. Read
    utf-8-sig (adversarial-review F4): a BOM'd registry — the realistic Excel
    round-trip on a Windows-first kit — would otherwise glue the BOM to the
    first column name and silently hide EVERY row from every consumer of this
    loader (the WI graph, the pending projection's spine lines). utf-8-sig
    reads plain utf-8 unchanged."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


# --- the spec-folder registry reader (duplicated per the F5 rule) -------------
# `docs/work/<status>/WI-###-<slug>.md`: one Markdown spec per work item, its
# STATUS encoded as the DIRECTORY (docs/concurrency-restructure.md §2.1, Phase
# 2b). The reader emits rows carrying the SAME 17 keys `csv.DictReader` yields
# for `work-items.csv`, so the dual-read happens at the ROW level, once, here —
# `load_wis` and every consumer past it never learn which home is authoritative.
# The format's definition is `scripts/wi_convert.py` (`parse_spec` /
# `status_from_location`), which materializes the folder; this is its read half.
#
# Copied VERBATIM across schedule.py, check_trajectory.py and agent_common.py
# per the kit's F5 rule — a shared module was rejected (owner ruling
# 2026-07-12) so each script stays independently copy-able, and the one real
# risk of N parsers, DRIFT, is closed by tests/test_wi_loader_sync.py rather
# than by extraction (WI-291).
WI_COLUMNS = (
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "CritiqueBudget",
    "CritiqueExhaustion",
    "Priority",
    "Exclusive",
    "BlockRef",
    "EstTokens",
    "SafetyClass",
    "PlanMode",
)
SPEC_SCALARS = (
    ("Title", "title"),
    ("Workstream", "workstream"),
    ("SpecRef", "specref"),
    ("BuildTier", "buildtier"),
    ("CritiqueBudget", "critique_budget"),
    ("CritiqueExhaustion", "critique_exhaustion"),
    ("Priority", "priority"),
    ("Exclusive", "exclusive"),
    ("BlockRef", "blockref"),
    ("EstTokens", "est_tokens"),
    ("SafetyClass", "safety_class"),
    ("PlanMode", "planmode"),
)
SPEC_LISTS = (("SR-Refs", "sr_refs"), ("Predecessors", "needs"))
# Directory -> Status. `archive/` holds BOTH terminal states and the frontmatter
# `disposition` key tells them apart; `active/<branch>/` sits one level deeper,
# so the status is the FIRST path component, never the file's parent directory.
SPEC_STATUS_DIRS = {
    "archive": "done",
    "queued": "queued",
    "deferred": "deferred",
    "active": "active",
}
# The inert EXAMPLE spec's filename prefix (the `-000` rule, applied to the
# folder home): scaffolded documentation, never a registry entry that decides
# which home is authoritative.
SPEC_EXAMPLE = "WI-000-"
SPEC_FENCE = "+++"
SPEC_DELIVERABLE = "\n## Deliverable\n\n"


def spec_work_dir(csv_path):
    """The `docs/work` folder that replaces the registry CSV at `csv_path` — its
    `docs/` directory plus `work`, derived from the one path each caller already
    declares rather than from a second constant that could disagree with it."""
    return Path(csv_path).parent.parent / "work"


def spec_files(work_dir):
    """Every `<status>/WI-*.md` spec under `work_dir`, sorted by path; `[]` when
    the folder is absent or holds none. An empty answer is what leaves the CSV
    authoritative, so a stray file sitting DIRECTLY in `work_dir` — which has no
    status directory above it — deliberately does not count as a registry."""
    work_dir = Path(work_dir)
    if not work_dir.is_dir():
        return []
    return sorted(p for p in work_dir.rglob("WI-*.md") if p.parent != work_dir)


def parse_spec_frontmatter(text, relpath):
    """`(data, body)` for one spec file: the TOML frontmatter between the `+++`
    fences, parsed, and everything after the closing fence, verbatim."""
    lines = text.split("\n")
    if not lines or lines[0] != SPEC_FENCE or SPEC_FENCE not in lines[1:]:
        raise ValueError(
            "{}: no closed `{}` frontmatter fence".format(relpath, SPEC_FENCE)
        )
    close = lines.index(SPEC_FENCE, 1)
    try:
        data = tomllib.loads("\n".join(lines[1:close]))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(
            "{}: frontmatter is not valid TOML — {}".format(relpath, exc)
        ) from None
    return data, "\n".join(lines[close + 1 :])


def parse_spec_status(relpath, data):
    """The Status a spec's LOCATION encodes, checked against its `disposition`.

    `archive/` holds both terminal states, so the two ways location and
    frontmatter can disagree — an unknown disposition, and a retirement filed
    outside `archive/` — are refusals, never silent coercions. A directory
    nobody declared is a refusal too: dropping it into `queued` would silently
    reclassify work, which is the catch-all shape this kit refuses on sight."""
    parts = relpath.split("/")
    status = SPEC_STATUS_DIRS.get(parts[0]) if len(parts) > 1 else None
    if status is None:
        raise ValueError(
            "{}: {!r} is not a status directory (the spec form knows only {})".format(
                relpath, parts[0], ", ".join(sorted(SPEC_STATUS_DIRS))
            )
        )
    disposition = data.get("disposition")
    if disposition is None:
        return status
    if disposition != "retired":
        raise ValueError("{}: unknown disposition {!r}".format(relpath, disposition))
    if status != "done":
        raise ValueError("{}: a retired spec belongs in archive/".format(relpath))
    return "retired"


def parse_spec_id(relpath, data):
    """The work-item id, which must be a non-empty string AND must be the one
    the filename carries — two homes for one fact, so they are compared here
    rather than trusted apart."""
    wid = data.get("id")
    if not isinstance(wid, str) or not wid:
        raise ValueError("{}: frontmatter carries no string `id`".format(relpath))
    if not relpath.split("/")[-1].startswith(wid + "-"):
        raise ValueError(
            "{}: filename does not carry its own id {!r}".format(relpath, wid)
        )
    return wid


def parse_spec_deliverable(relpath, body):
    """The Deliverable cell a spec body carries, verbatim ("" when absent).

    The long cell lives in the BODY precisely because body text needs no
    escaping: it may hold newlines, quotes and markdown. This format owns the
    whole body shape, so anything that is neither empty nor one
    `## Deliverable` section is a malformation rather than free prose."""
    if not body:
        return ""
    if not body.startswith(SPEC_DELIVERABLE) or not body.endswith("\n"):
        raise ValueError(
            "{}: body is neither empty nor one `## Deliverable` section".format(relpath)
        )
    return body[len(SPEC_DELIVERABLE) : -1]


def parse_spec_row(text, relpath):
    """`(row, order)` for one spec file — a 17-key row shaped exactly like the
    CSV's. Raises ValueError NAMING the file on any malformation: invalid TOML, a
    missing or non-string `id`, an id the filename disagrees with, a directory
    that is not a status, or a body that is not the single `## Deliverable`
    section this format owns."""
    data, body = parse_spec_frontmatter(text, relpath)
    row = dict.fromkeys(WI_COLUMNS, "")
    row["WI-ID"] = parse_spec_id(relpath, data)
    row["Status"] = parse_spec_status(relpath, data)
    row["Deliverable"] = parse_spec_deliverable(relpath, body)
    for column, key in SPEC_SCALARS:
        if key in data:
            row[column] = str(data[key])
    for column, key in SPEC_LISTS:
        if key in data:
            row[column] = ";".join(str(v) for v in data[key])
    order = data.get("order")
    return row, order if isinstance(order, int) else None


def read_spec_rows(work_dir, on_error=None):
    """The spec folder's rows in REGISTRY order — by the explicit `order` key,
    then by numeric id, which is the order the converter reproduces.

    A malformed spec is reported to `on_error` (a callable taking one message)
    and skipped; with no sink it is skipped SILENTLY. That mirrors the split this
    kit already draws over the CSV — a broken registry is the validator's job to
    report, not the scheduler's to crash on. Files are read with universal
    newlines, so a spec checked out CRLF parses identically to one checked out
    LF (the WI-337 lesson: line endings are a property of the checkout)."""
    parsed = []
    for path in spec_files(work_dir):
        relpath = path.relative_to(work_dir).as_posix()
        try:
            row, order = parse_spec_row(path.read_text(encoding="utf-8"), relpath)
        except (ValueError, OSError, UnicodeDecodeError) as exc:
            if on_error is not None:
                on_error(str(exc))
            continue
        parsed.append((order is None, order or 0, _spec_id_number(row["WI-ID"]), row))
    parsed.sort(key=lambda item: item[:3])
    return [item[-1] for item in parsed]


def _spec_id_number(wid):
    match = re.search(r"\d+", wid or "")
    return int(match.group()) if match else 0


# --- end of the F5-duplicated spec-folder reader ------------------------------


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
    *reported*, never silently dropped."""
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
        # A `~` prefix marks a soft (advisory-ordering) predecessor edge; the
        # bare id is a hard (blocking) edge — see the module docstring.
        preds, soft = [], []
        for p in _split_refs(r.get("Predecessors", "")):
            if p.startswith("~"):
                soft.append(p[1:])
            else:
                preds.append(p)
        wis.append(
            {
                "id": wid,
                "title": (r.get("Title") or "").strip(),
                "workstream": (r.get("Workstream") or r.get("Track") or "").strip()
                or "other",
                "srs": _split_refs(r.get("SR-Refs", "")),
                "preds": preds,
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
# `staged_findings` compares `git show HEAD:<work-items.csv>` against the working
# copy LINE-WISE and documents the assumption in its own docstring — "a WI row is
# one physical line (no embedded newlines)". Nothing enforced it, which is the
# enforcement-audit question asked of a rule the code already relies on.
LINE_BREAK_CHARS = (("\r", "CR"), ("\n", "LF"))
# TAB is deliberately allowed: it is ordinary whitespace inside a quoted cell and
# breaks nothing downstream. Every other C0 control is not text — see below.
_ALLOWED_CONTROLS = "\t"


def _control_findings(cell):
    """`[(label, detail)]` for the integrity violations in one cell.

    Two classes, reported distinctly because the reader's next action differs:

      - **CR / LF** break the one-physical-line rule the staged-close scan reads;
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


def validate(wis, known_srs):
    """Return the hard-error strings for the work-item graph ([] = clean).

    Dangling `SR-Refs` are WARNED on stderr (a draft SR referenced ahead of its
    row is legitimate), never failed — and only when the SR registry is
    non-empty, so a repo without SRs yet does not spuriously warn. Soft (`~`)
    predecessors must resolve like hard ones, but only **hard** edges are
    subject to the acyclicity ERROR — a cycle that needs a soft edge to close
    is a WARN (conflicting ordering hints), never a failure."""
    ids = {w["id"] for w in wis}
    errors = []

    for w in wis:
        for p in w["preds"] + w["soft"]:
            if p not in ids:
                errors.append(
                    "{}: predecessor {!r} is not a work item".format(w["id"], p)
                )
        for s in w["srs"]:
            if known_srs and s not in known_srs:
                print(
                    "check_trajectory: WARN - {} references {} "
                    "(not in the SR registry; draft?)".format(w["id"], s),
                    file=sys.stderr,
                )

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
    """The set of real SR ids from system-requirements.csv (for the SR-ref warn)."""
    return {
        (r.get("SR-ID") or "").strip()
        for r in read_rows(root / SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    }


# Source-file extensions stripped when normalizing a module path, so the arch-map
# name (`scripts/check`) and an IF endpoint written with the full repo path
# (`project-trajectory/scripts/check.py`) collapse to one key. Kept in sync with
# trace.py._MODULE_EXTS (a small stable helper duplicated per the F5 convention —
# check_trajectory must stay import-free of the joined-spine engine).
_MODULE_EXTS = (".py", ".sh", ".ps1", ".ts", ".js", ".go", ".rs", ".cmd")


def _norm_module(path):
    """A module path reduced to a naming-convention-neutral key: strip a leading
    `project-trajectory/`, any source extension, and `/__init__`."""
    p = (path or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/") :]
    for ext in _MODULE_EXTS:
        if p.endswith(ext):
            p = p[: -len(ext)]
            break
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p


def load_ifs(rows):
    """Real (non-`-000`) IF-### interface rows as dicts. Lenient — `trace.py` owns
    IF integrity (malformed ids, SR-Ref resolution); this loader only feeds the
    warn-first coverage views, so a malformed id is simply skipped here."""
    out = []
    for r in rows:
        iid = (r.get("IF-ID") or "").strip()
        if not IF_ID_RE.fullmatch(iid) or iid.endswith("-000"):
            continue
        out.append(
            {
                "id": iid,
                "direction": (r.get("Direction") or "").strip().lower(),
                "this": (r.get("ThisProject") or "").strip(),
                "counterpart": (r.get("Counterpart") or "").strip(),
                "status": (r.get("Status") or "").strip().lower(),
                "notes": (r.get("Notes") or "").strip().lower(),
            }
        )
    return out


def arch_inventory(root):
    """`(module_names, {module: {IF ids}}, {module: {imported stems}})` parsed
    from `docs/architecture.md`'s generated MODULE MAP block — the committed
    arch-map artifact (the same block `gen_trajectory.sw_modules` reads for the
    How-SW view, and `gen_arch_map` writes). `module_names` are the
    ``### `name``` headers; the IF map harvests the
    `Contracts (interfaces): IF-###, ...` line `gen_arch_map` emits from a
    module's `Contracts:` docstring; the import map harvests the
    `Imports (internal): `a`, `b`` line (bare backticked module stems — the
    cross-CMP rule's edge source, WI-064). A small stable parser duplicated per
    the F5 convention (sw_modules also collects symbols; this one collects the
    Contracts citations) — keep the header/line grammar in sync with
    `gen_arch_map.build_map`. Empty when the doc/block is absent, so the
    coverage layers are vacuous pre-arch-map."""
    md = root / ARCH_MD
    if not md.exists():
        return set(), {}, {}
    names, contracts, imports, current, inside = [], {}, {}, None, False
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
        if "BEGIN GENERATED MODULE MAP" in line:
            inside = True
            continue
        if "END GENERATED" in line:
            inside = False
            current = None
            continue
        if not inside:
            continue
        m = re.match(r"^### `([^`]+)`", line)
        if m:
            current = m.group(1)
            names.append(current)
        elif current and line.strip().startswith("Contracts (interfaces):"):
            contracts.setdefault(current, set()).update(IF_ID_RE.findall(line))
        elif current and line.strip().startswith("Imports (internal):"):
            imports.setdefault(current, set()).update(re.findall(r"`([^`]+)`", line))
    return set(names), contracts, imports


def interface_findings(root):
    """Architecture-connectivity coverage warns (S5/WI-056; process.md §8), all
    warn-first — the caller prints them and they never change the exit code, at
    any gate. Returns the warn strings ([] when opted out or vacuous).

    Ruled opt-out, default-on: fires even with an empty/absent `interfaces.csv`
    (a multi-module arch-map with no declared seams reads "connectivity
    undeclared"); silenced only by `docs/interfaces-check: off` or a ≤1-module
    inventory (nothing to connect)."""
    if not read_interfaces_check_enabled(root):
        return []
    inventory, declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect (or no arch-map yet) — vacuous
    ifs = load_ifs(read_rows(root / IF_CSV))
    out = []
    if not ifs:
        return [
            "connectivity undeclared: the {}-module architecture declares no "
            "interfaces — add IF-### rows to {}, or set docs/interfaces-check: "
            "off".format(len(inventory), IF_CSV)
        ]

    inv_norm = {_norm_module(m): m for m in inventory}
    inv_norm.pop("", None)
    endpoints, provides, consumes = set(), set(), set()
    sources, sinks = set(), set()
    for r in ifs:
        this_n, cp_n = _norm_module(r["this"]), _norm_module(r["counterpart"])
        for n in (this_n, cp_n):
            if n in inv_norm:
                endpoints.add(n)
        # The honesty valve: a `source`/`sink` FIRST word in Notes marks
        # ThisProject a deliberate source (consumes nothing) / sink (provides
        # nothing), so it doesn't breed a boilerplate opposite-direction row.
        marker = r["notes"].split()
        first = marker[0].rstrip(":;,.") if marker else ""
        if first == "source":
            sources.add(this_n)
        elif first == "sink":
            sinks.add(this_n)
        # Producer -> consumer roles: Consumes flips the endpoints so the
        # producing/consuming credit lands on the right module either way.
        producer, consumer = (
            (cp_n, this_n) if r["direction"] == "consumes" else (this_n, cp_n)
        )
        if producer in inv_norm:
            provides.add(producer)
        if consumer in inv_norm:
            consumes.add(consumer)

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

    # Seam-TC citation: each Active IF id should be cited by >=1 TC (the rung-2
    # seam-TC rule, finally checkable now that trace reads the IF tier).
    tc_cited = set()
    for r in read_rows(root / TC_CSV):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    for r in ifs:
        if r["status"] == "active" and r["id"] not in tc_cited:
            out.append(
                "IF {} is Active but cited by no TC (a seam should carry a "
                "contract/fixture test)".format(r["id"])
            )

    # Docstring citation: a `Contracts: IF-###` a script declares (harvested into
    # the arch-map) must exist in the registry; and, once the convention is in
    # use, a registry IF whose module declares no matching citation warns too.
    registry_ids = {r["id"] for r in ifs}
    for module, ids in sorted(declared_contracts.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "module {!r} docstring declares Contracts: {} but no such IF-### "
                "row exists".format(module, iid)
            )
    if declared_contracts:  # reverse direction only "where sensible" — once opted in
        all_declared = set().union(*declared_contracts.values())
        for r in ifs:
            if r["id"] not in all_declared:
                out.append(
                    "IF {} is in the registry but no script declares it via a "
                    "Contracts: docstring line".format(r["id"])
                )
    return out


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
    for r in read_rows(root / LLR_CSV):
        lid = (r.get("LLR-ID") or "").strip()
        if not lid.startswith("LLR-") or lid.endswith("-000"):
            continue
        tags = {t for t in _split_refs(r.get("Component", "")) if t.startswith("CMP-")}
        if not tags:
            continue
        key = _norm_module(r.get("Module", ""))
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
    """
    names = arch_inventory(root)[0]
    inventory = {}
    for m in names:
        n = _norm_module(m)
        if n:
            inventory.setdefault(n, m)
    cmps = load_cmps(read_rows(root / CMP_CSV))
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


def cross_component_findings(root):
    """The cross-CMP-edge-without-IF rule (WI-064; the AXES ratified model's
    "Enforceability" ruling, process-options.md "Component layer"): an internal
    import edge whose endpoints belong to *different* CMP-### components must be
    covered by a declared IF-### row — an undeclared cross-component coupling is
    a finding, mechanized from the same committed artifacts the other component
    rules read. The CALLER gates the opt-out (`component_findings` shares
    `docs/components-check`) and the WARN-plain / ERROR-under-`--strict`
    promotion.

    Vacuous by construction when any input is absent (never-breaking): no
    arch-map `Imports (internal):` lines, no real CMP rows, an endpoint with no
    `Component`-tag membership (coverage is the containment rule's job, not
    this one's), or an import stem that resolves to no/multiple inventory
    modules. A pair is covered when any real IF row's normalized
    `(ThisProject, Counterpart)` matches the edge's endpoints in either
    direction — a seam is one declared relationship, whichever side authored
    the row."""
    names, _contracts, imports = arch_inventory(root)
    if not imports:
        return []
    cmp_ids = {c["id"] for c in load_cmps(read_rows(root / CMP_CSV))}
    if not cmp_ids:
        return []
    raw = module_components(root)
    membership = {n: tags & cmp_ids for n, tags in raw.items()}
    covered = set()
    for r in load_ifs(read_rows(root / IF_CSV)):
        a, b = _norm_module(r["this"]), _norm_module(r["counterpart"])
        if a and b:
            covered.add((a, b))
            covered.add((b, a))
    # A bare imported stem (`agent_route`) resolves against the inventory's
    # normalized module names (`scripts/agent_route`) by unique-stem match —
    # the same resolution gen_arch_map applied when it emitted the line.
    by_stem = {}
    for m in names:
        n = _norm_module(m)
        if n:
            by_stem.setdefault(n.rsplit("/", 1)[-1], set()).add(n)
    out = []
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
            if not dst_cmps or (src_cmps & dst_cmps) or (src_n, dst_n) in covered:
                continue
            out.append(
                "cross-component import {} ({}) -> {} ({}) has no declared "
                "IF-### seam — declare the interface row in {} or retag the "
                "membership, or set docs/components-check: off".format(
                    src_n,
                    "/".join(sorted(src_cmps)),
                    dst_n,
                    "/".join(sorted(dst_cmps)),
                    IF_CSV,
                )
            )
    return out


def component_findings(root):
    """The How-SW component-coverage finding(s) (process-options.md "Component
    layer"). Returns the finding strings ([] when opted out or clean). The caller
    prints them WARN plain and promotes them to ERROR under `--strict` (G2+).
    Opt-out via `docs/components-check: off`. Three rules, all off the arch-map ⇒
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
    - **Cross-CMP edges need a declared seam** (WI-064): see
      `cross_component_findings` — an import edge between two components with
      no covering IF-### row."""
    if not read_components_check_enabled(root):
        return []
    view = component_top_view(root)
    out = []
    packs = knowledge_packs(root)
    if packs and view["inventory"] and view["uncontained"]:
        out.append(
            "docs/knowledge/ holds {} pack(s) but {} arch-map module(s) are in no "
            "CMP-### component ({}); tag them via LLR `Component` cells so the "
            "knowledge⇒component web is complete, or set docs/components-check: "
            "off".format(len(packs), len(view["uncontained"]), CMP_CSV)
        )
    if len(view["inventory"]) > TOP_VIEW_MAX and view["count"] > TOP_VIEW_MAX:
        out.append(
            "How-SW top view has {} items ({} top-level component(s) + {} "
            "uncontained module(s)) — exceeds the bound of {}; declare CMP-### "
            "components in {} to contain modules (nest with PartOf), or set "
            "docs/components-check: off".format(
                view["count"],
                len(view["top_roots"]),
                len(view["uncontained"]),
                TOP_VIEW_MAX,
                CMP_CSV,
            )
        )
    out.extend(cross_component_findings(root))
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


def _proposed_rationale_present(section, iid):
    """True when at least one line citing `iid` carries rationale text beyond the
    id and the `Proposed` marker — a PRESENCE check (whether the rationale is
    *honest* and truly names the nearest seam is the Reviewer/critique gap, the
    spec-interface-hygiene rubric B1)."""
    for line in section.splitlines():
        if iid not in line:
            continue
        residue = _IF_TOKEN_RE.sub("", line)  # drop the id + any nearest-IF ids
        residue = re.sub(r"(?i)proposed|[-*•·:()\[\].,;]", "", residue)
        if len(residue.strip()) >= 8:
            return True
    return False


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
    `interfaces.csv` (the one seam home, PROCESS.md §8), and a cited
    `Status=Proposed` seam must carry a non-empty rationale on its citation line
    (the forced nearest-existing-IF search that is the anti-duplication
    mechanism). WARN plain / ERROR under `--strict` (G2+), like
    `component_findings`; the caller owns that promotion.

    **Vacuous-until-armed:** a spec with no `## Interfaces` heading is skipped, so
    existing specs and downstream repos stay green until they adopt the section.
    An armed section that cites no resolvable IF-### AND states no intra-module
    escape (PROCESS.md §8) is itself a finding — an empty-ceremony section. The
    honesty of a rationale and whether a Proposed contract near-duplicates an
    existing seam are the recorded Reviewer-tier gaps (enforcement-audit.md)."""
    specs = root / SPECS_DIR
    if not specs.is_dir():
        return []
    if_rows = {r["id"]: r for r in load_ifs(read_rows(root / IF_CSV))}
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
            row = if_rows.get(iid)
            if row is None:
                out.append(
                    "{}: `## Interfaces` cites {} which resolves to no row in "
                    "{}".format(rel, iid, IF_CSV)
                )
            elif row["status"] == "proposed" and not _proposed_rationale_present(
                section, iid
            ):
                out.append(
                    "{}: cites Proposed seam {} with no rationale — name the "
                    "nearest existing IF-### and why it does not suffice (the "
                    "anti-duplication search, PROCESS.md §8)".format(rel, iid)
                )
    return out


# --- the [phase]-[g*] archetype + phase-drop detector (WI-093) -----------------
# The derived-gate model (docs/specs/derived-gate-model.md §7/§9.3) structures a
# phase's pre-dev work as a first-class WI whose Title carries a `[<phase>]-[g<N>]`
# tag (g1 = requirement structuring, g2 = decomposition + TCs). The derived gate
# DROPPING below a phase's last-closed level is the signal that new/reopened
# content entered and a new phase-gate WI is due; the committed anchor is where
# phase identity + membership live (a git-history walk is rebase-sensitive and
# carries no membership, §9.3). Both checks are WARN-FIRST — like the connectivity
# coverage, they never change the exit code, at any gate.
GATE_FILE = "docs/gate"
PHASE_ANCHOR_RE = re.compile(r"^\[([^\]]+)\]-\[g([12])\]")
_GATE_LEVEL = {"G0": 0, "G1": 1, "G2": 2, "G3": 3}
_PER_PHASE_RE = re.compile(r"per-phase=(\S+)")


def read_derived_phases(root):
    """`{phase-label: gate-level-int}` parsed from the `# basis:` line of the
    generated docs/gate (derive_gate.py's hybrid cache — read the committed value,
    never recompute here). Empty when docs/gate is absent or a legacy hand-set gate
    with no basis line, so the drop detector is then vacuous. The basis format is
    derive_gate.basis_line's `per-phase=<label>=G<n>;...` (a shared contract)."""
    path = root / GATE_FILE
    if not path.exists():
        return {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("# basis:"):
            m = _PER_PHASE_RE.search(s)
            if not m or m.group(1) == "(none)":
                return {}
            out = {}
            for pair in m.group(1).split(";"):
                if "=" in pair:
                    label, gate = pair.rsplit("=", 1)
                    if gate in _GATE_LEVEL:
                        out[label] = _GATE_LEVEL[gate]
            return out
    return {}


def phase_anchors(wis):
    """`({(phase, gate): wi}, [shape-warnings])` — the `[phase]-[g*]` anchor WIs
    parsed from Titles. A duplicate (phase, gate) anchor, and a `-g2` whose
    predecessors omit its `-g1`, are warned (advisory only)."""
    anchors, warns = {}, []
    for w in wis:
        m = PHASE_ANCHOR_RE.match(w["title"])
        if not m:
            continue
        key = (m.group(1), int(m.group(2)))
        if key in anchors:
            warns.append(
                "duplicate phase-gate anchor [{}]-[g{}] ({} and {})".format(
                    key[0], key[1], anchors[key]["id"], w["id"]
                )
            )
            continue
        anchors[key] = w
    for (phase, gate), w in anchors.items():
        if gate == 2 and (phase, 1) in anchors:
            g1 = anchors[(phase, 1)]["id"]
            if g1 not in (w["preds"] + w["soft"]):
                warns.append(
                    "phase-gate anchor {} ([{}]-[g2]) does not list its "
                    "[{}]-[g1] ({}) as a predecessor".format(w["id"], phase, phase, g1)
                )
    return anchors, warns


def phase_findings(root, wis):
    """The phase-archetype + phase-drop warns (WI-093; warn-first). Returns the
    warn strings ([] when vacuous — no anchors and no per-phase drop data, the
    single-phase meta case). The drop detector reads the derived per-phase levels
    from docs/gate's basis: for each phase with a **done** `[phase]-[gN]` anchor
    (its recorded closed level), if the current derived level for that phase is
    below N, new/reopened content dropped it — warn to open a new phase-gate WI."""
    anchors, warns = phase_anchors(wis)
    derived = read_derived_phases(root)
    closed = {}  # phase -> highest gN whose [phase]-[gN] anchor is done
    for (phase, gate), w in anchors.items():
        if w["status"] == "done":
            closed[phase] = max(closed.get(phase, 0), gate)
    for phase, level in sorted(closed.items()):
        cur = derived.get(phase)
        if cur is not None and cur < level:
            warns.append(
                "phase {!r} dropped to G{} but its closed [{}]-[g{}] anchor recorded "
                "level G{} — new or reopened content entered; open a new "
                "[{}]-[g*] work item to structure it (derived-gate model §9.3)".format(
                    phase, cur, phase, level, level, phase
                )
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
# the SHIPPED pre-commit hook, and the `ratify-fresh` lesson (130-REVIEW-A) is that
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
    monolith getting another sanctioned baseline entry."""
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
    """The work-items.csv coherence findings (R-A + R-E) + the unknown-status
    lint, each as `(rule, hard, message)`.

    `hard=True` (R-A only) is an ERROR at every run — the incoherent-handoff
    rule. R-E is warn-first; the caller promotes it to an error under `--strict`.
    Kept OUT of `validate()` so the dashboard renderer (`gen_trajectory`, which
    imports `validate`) shares the same registry read. R-B/R-C (open-WI status
    repetition) are retired (WI-180); R-D's done-id rule is RESTORED separately in
    `status_forward_only_findings` (WI-200), kept out of here so it reads the
    status.md text rather than the registry rows."""
    out = []
    for w in wis:
        st = w["status"]
        # (The `status-vocab` and `blocked-ref` rules retired with the CSV home
        # at Phase 5: status is the spec's DIRECTORY, so an unknown status is a
        # loader refusal before any row exists, and `blocked` is DERIVED as
        # queued+blockref — a queued row without one is simply queued. No row
        # can reach either rule.)
        # R-A: Deliverable non-empty IFF the WI is TERMINAL. A `done` WI's
        # Deliverable records what shipped; a `retired` WI's records the reason it
        # will never be built (WI-267) — either way the terminal row carries its
        # permanent backward record, and an open row's Deliverable is filled only
        # at close.
        if st in TERMINAL_STATUSES and not w["deliverable"]:
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


def spec_lifecycle_findings(root, wis):
    """The spec-lifecycle close-side rule **R-F** (WI-251) — the mechanical half
    of the close ritual R-E's open half leaves unstated: *Deliverable filled,
    `SpecRef` cleared, spec archived* (the `docs/specs/` README lifecycle). The
    one-sided enforcement is how this repo accreted 137 done rows with live
    SpecRefs before the rule existed. Two findings, both message-only (the
    caller tags `R-F` and owns the warn-plain / error-under-`--strict`
    promotion, the R-E warn tier — so a rotting spec surface cannot reach a
    green G2/G3 gate while a plain commit stays warn-first):

      - a **terminal** WI (`done` or `retired`, WI-267) whose `SpecRef` is still
        set — the terminal transition clears it (the Deliverable + log carry the
        backward record; a `retired` row's reason lives in its Deliverable);
      - a **live** `docs/specs/` file cited by no *open* WI — archive it to
        `docs/archive/specs/` (close date appended, WI ids noted) or point an
        open WI at it. A shared effort doc therefore archives only when its
        last open citer closes; `deferred`/`blocked` are open, so their specs
        stay, but `retired` is terminal, so a retired WI keeps no live spec. The
        scaffold boilerplate (README, any `-000` exemplar) is excluded by the
        `spec_interface_findings` idiom.

    Vacuous on a fresh scaffold (no done-with-SpecRef rows; only excluded
    boilerplate in `docs/specs/`). Whether the archived spec's durable content
    actually landed in a spine/architecture home first is the recorded
    Reviewer-tier gap (enforcement-audit.md)."""
    out = []
    open_cited = set()
    for w in wis:
        spec = w["specref"]
        if not spec:
            continue
        if w["status"] in OPEN_STATUSES:
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
# `deferred`/`blocked`/`retired` are decisions, not outcomes. What was missing is
# not derivation but RECONCILIATION — the shape every other declared-vs-computed
# pair here already has (`derive_gate --check` recomputes and fails on drift;
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
    refuted three of its claims. An error-under-strict trailer rule blocks the G3
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
    `--strict` (G2+), the pre-WI-180 severity (the caller owns that promotion, the
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
    no done ids); the `docs/trajectory-check: off` opt-out is the caller's (it
    returns before any check runs). Returns finding-message strings."""
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


def dead_dependency_findings(wis):
    """Surface a live WI that hard-depends on a `retired` predecessor (WI-267).

    A `retired` WI is a terminal WON'T-BUILD row — it will never integrate
    `done`, so an open successor whose hard edge points at it can NEVER become
    ready. The conservative decision (WI-267 design-decision 3) is to SURFACE
    the dead edge rather than let a retired predecessor silently "satisfy" the
    dependency the way `done` does: the owner must re-home the successor's edge
    or retire it too. The scheduler already refuses to schedule such a WI
    (schedule.hard_preds_satisfied requires `done`, not merely terminal); this
    makes the same dead edge visible in the validator. WARN plain, ERROR under
    `--strict`. Soft (`~`) edges are advisory and never gate readiness, so they
    are exempt. Vacuous until a registry actually retires a still-depended-on WI.
    """
    by_id = {w["id"]: w for w in wis}
    out = []
    for w in wis:
        if w["status"] not in OPEN_STATUSES:
            continue
        dead = sorted(
            p for p in w["preds"] if by_id.get(p, {}).get("status") == "retired"
        )
        if dead:
            out.append(
                "{}: open WI hard-depends on retired WI(s) {} — a retired "
                "predecessor is terminal and never satisfies a hard dependency; "
                "re-home the edge or retire this WI too".format(w["id"], ";".join(dead))
            )
    return out


# (run_state_findings — the WI-115 stale-end-state warn over docs/run-state —
# retired at concurrency-restructure Phase 5 with the dispatcher that wrote
# that file; a stale parked state is unrepresentable when no file declares
# one.)


def _git(root, args):
    """`git -C <root> <args>` stdout on success, else None (git absent, not a
    repo, no such object). Every staged-mode git call degrades to None so the
    no-validation-delta warn is a silent no-op outside a git checkout."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _blame_row_times(root, rel_path):
    """`{row-id: committer-time-epoch}` for a registry CSV, via a single
    `git blame --line-porcelain`. Each physical CSV row is one blame line whose
    leading field (up to the first comma) is its id; the id maps to the committer
    time of the commit that last touched that line. Returns {} on ANY git failure
    — no repo, an untracked/uncommitted file, an unparseable blame — so the
    backlog-staleness warn degrades silently off-git (never a false warn, never a
    crash). One subprocess per file keeps the cost bounded (WI-205: ≤2 blames)."""
    out = _git(root, ["blame", "--line-porcelain", "--", rel_path])
    if out is None:
        return {}
    times = {}
    committer_time = None
    for line in out.split("\n"):
        # --line-porcelain repeats the full commit header for every line, so a
        # `committer-time <epoch>` header always precedes its `\t<content>` line.
        if line.startswith("committer-time "):
            try:
                committer_time = int(line[len("committer-time ") :].strip())
            except ValueError:
                committer_time = None
        elif line.startswith("\t"):
            token = line[1:].split(",", 1)[0].strip()
            if token and committer_time is not None:
                times[token] = committer_time
            committer_time = None
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
        and `--follow` carries the search back to the file's real last edit. A
        commit that moves AND edits the spec (the ordinary close) still answers
        2000, which is correct — that is the driven look the warn asks for.

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


def backlog_staleness_findings(root, wis):
    """WI-205 — the backlog-staleness warn (warn-only, the WI-129 checker stance).

    Ratifying amended SN/SR/LLR/TC content never touches the open WI rows that
    cite it, so an incomplete backlog can silently drift out of sync with the
    requirement state it was filed against. For each open WI (queued/active/
    blocked — `deferred` and `done` are exempt) this compares when its registry
    row last changed against when each cited source last changed, and warns when a
    source is STRICTLY NEWER: the WI needs a driven re-validation against the
    amended requirement. Re-affirming is deliberately cheap — any reviewed edit to
    the WI row re-dates its blame and clears the warn (a *driven look*, not
    ceremony). Cited sources: each `SR-Refs` id (a row of system-requirements.csv)
    and the `SpecRef` target file.

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
                    "re-validate the WI against the amended requirement (or touch "
                    "the row to re-affirm)".format(w["id"], sr)
                )
        pathpart = w["specref"].split("#", 1)[0].strip()
        if pathpart:
            if pathpart not in spec_time:
                spec_time[pathpart] = _path_commit_time(root, pathpart)
            t = spec_time[pathpart]
            if t is not None and t > wi_time:
                out.append(
                    "{}: its SpecRef {} changed after the WI row was last touched "
                    "— re-validate the WI against the amended requirement (or touch "
                    "the row to re-affirm)".format(w["id"], pathpart)
                )
    return out


def _tests_dir(root):
    """The declared tests root (docs/stack.ini [paths] tests), default `tests` —
    the surface a real validation-logic change would touch."""
    ini = root / "docs" / "stack.ini"
    if ini.exists():
        cp = configparser.ConfigParser(interpolation=None)
        try:
            cp.read_string(ini.read_text(encoding="utf-8", errors="replace"))
            if cp.has_option("paths", "tests"):
                return cp.get("paths", "tests").strip() or "tests"
        except configparser.Error:
            pass
    return "tests"


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

    Two honest limits, both benign for the close ratchets that consume this:
    `archive/` collapses `done` and `retired` (the disposition lives in the
    frontmatter, which is a blob), so a HEAD-retired item reads `done` — both are
    terminal, so `_newly_closed` cannot be fooled either way; and `srs` is empty,
    because SR-Refs are content too. `_staged_wi_registry` fills that from the
    WORKING TREE, where the same file is unchanged unless this very commit
    touched it."""
    out = _git(root, ["ls-tree", "-r", "--name-only", "HEAD", "--", WI_WORK])
    if not out or not out.strip():
        return None
    prefix = WI_WORK + "/"
    statuses = {}
    for name in out.splitlines():
        name = name.strip()
        if not name.startswith(prefix) or not name.endswith(".md"):
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

    Extracted for WI-344 (docs/dupes-allow `staged-close-scan`), forced early by
    WI-352 adding a fourth copy: the census fails closed on a same-file
    duplication, and the F5 sanction buys cross-SCRIPT copy-ability, so it never
    covers one. (The CSV-home line-diff half retired with the CSV at Phase 5;
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
    archive/WI-360-x.md` is exactly what a CLOSURE looks like. The closure SET is
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
    changed = _git(root, ["diff", "--cached", "--name-status", "--", WI_WORK])
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
    applicable). Compares the staged WI CSV against its HEAD version via git;
    any missing git context makes it a silent no-op (the hook has git; a gate
    run does not, and pays nothing). Line-splitting the HEAD CSV is safe here —
    a WI row is one physical line (no embedded newlines).

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


# The three spine registries the staged amend-without-flip warn (WI-316) watches,
# each with its id column. The SN needs file has no Status cell (section-as-state)
# — a changed ratified SN rides its SR chain's Modified — so it is not listed.
SPINE_CSVS = (
    ("docs/requirements/system-requirements.csv", "SR-ID"),
    ("docs/requirements/low-level-requirements.csv", "LLR-ID"),
    ("docs/test/test-cases.csv", "TC-ID"),
)


def staged_spine_findings(root):
    """The amend-without-flip warn (WI-316; warn-first, `--staged` only).

    A staged diff that changes the CONTENT cells of a spine row whose Status
    reads `Verified` in both HEAD and the stage has amended attested prose
    without setting the `Modified` re-attest marker (process.md §7) — the
    write-time discipline the old RE-ATTESTATION-PENDING commit-message prose
    never had. One warning per amended row, naming the changed cells. Returns
    [] when not applicable; any missing git context is a silent no-op, like
    staged_findings. Rows are parsed with the csv module over the full staged /
    HEAD file text (spine cells are long; never line-split). A NEW row (id not
    in HEAD) is not an amendment; a row whose Status moved (to Modified, Draft,
    Planned, anything) made a deliberate call this warn does not second-guess."""
    staged = _git(root, ["diff", "--cached", "--name-only"])
    if staged is None:
        return []
    staged_names = set(staged.splitlines())
    if not any(p in staged_names for p, _ in SPINE_CSVS):
        return []

    def _index_rows(csv_path, id_col):
        """{id: row} of the INDEX version (`git show :path` — equals HEAD when
        the file is not staged), or {} when unreadable."""
        text = _git(root, ["show", ":" + csv_path])
        if text is None:
            return {}
        # F4: a committed BOM survives `git show`; strip it or the header glues
        # to the id column and the guard silently disables (fails OPEN).
        text = text.lstrip("﻿")
        return {
            r[id_col]: r
            for r in csv.DictReader(io.StringIO(text))
            if r.get(id_col) and not r[id_col].endswith("-000")
        }

    # The attestation unit is the SR: an amended child whose OWNING SR flips in
    # this same commit is the sanctioned amend+flip path, so only rows whose
    # unit stays unflagged warn. Owner resolution uses the staged (index) state.
    idx_srs = _index_rows(*SPINE_CSVS[0])
    idx_llrs = _index_rows(*SPINE_CSVS[1])

    def _flagged_sr(sid):
        status = ((idx_srs.get(sid) or {}).get("Status") or "").strip().lower()
        return status in ("modified", "draft")

    def _owners(csv_path, row):
        if csv_path == SPINE_CSVS[0][0]:
            return [row.get("SR-ID")]
        if csv_path == SPINE_CSVS[1][0]:
            return [
                x.strip() for x in (row.get("SR-Refs") or "").split(";") if x.strip()
            ]
        owners = []
        for x in (row.get("Verifies") or "").split(";"):
            x = x.strip()
            if x.startswith("SR-"):
                owners.append(x)
            elif x.startswith("LLR-") and x in idx_llrs:
                owners.extend(
                    y.strip()
                    for y in (idx_llrs[x].get("SR-Refs") or "").split(";")
                    if y.strip()
                )
        return owners

    out = []
    for csv_path, id_col in SPINE_CSVS:
        if csv_path not in staged_names:
            continue
        head_text = _git(root, ["show", "HEAD:" + csv_path])
        staged_text = _git(root, ["show", ":" + csv_path])
        if head_text is None or staged_text is None:
            continue  # first commit / newly added registry — nothing attested yet
        head_text = head_text.lstrip("﻿")  # F4, as above
        staged_text = staged_text.lstrip("﻿")
        head_rows = {
            r[id_col]: r
            for r in csv.DictReader(io.StringIO(head_text))
            if r.get(id_col) and not r[id_col].endswith("-000")
        }
        for row in csv.DictReader(io.StringIO(staged_text)):
            rid = (row.get(id_col) or "").strip()
            head = head_rows.get(rid)
            if not rid or rid.endswith("-000") or head is None:
                continue
            head_status = (head.get("Status") or "").strip().lower()
            cur_status = (row.get("Status") or "").strip().lower()
            if head_status != "verified" or cur_status != "verified":
                continue
            if any(_flagged_sr(s) for s in _owners(csv_path, row) if s):
                continue  # the attestation unit flips in this commit — sanctioned
            changed = sorted(
                k
                for k in set(head) | set(row)
                if k != "Status" and (head.get(k) or "") != (row.get(k) or "")
            )
            if changed:
                out.append(
                    "{}: content cell(s) {} amended while Status stays Verified "
                    "and no owning SR is flagged — a post-attestation amendment "
                    "owes the Modified re-attest marker (process.md §7); flip "
                    "the owning SR in this commit, or the sitting never sees "
                    "the change".format(rid, ", ".join(changed))
                )
    return out


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

OPEN_ITEMS_CSV = "docs/requirements/open-items.csv"
# A `[<phase>]-[g1|g2]` bracketed anchor appearing anywhere in a brief cell.
RATIFY_ANCHOR_RE = re.compile(r"\[[^\]\[]+\]-\[g[12]\]")
# The brief satisfies the rule only by naming a ratification/hierarchy VIEW — a
# bare `trace.py --ratify` command mention no longer counts (WI-146 REVIEW-A): a
# command can be unexecuted or wrong-scope, so it is not proof the generated view
# exists and is carried in the brief. WI-322 moved briefs from markdown sections
# to registry ROWS, so the proof is a path/link token in the cell rather than a
# markdown link — the rule is the same, its evidence shape follows the source.
RATIFY_VIEW_RE = re.compile(
    r"(?:ratif|hierarch)\w*[^\s]*\.(?:md|html|csv)|\]\([^)]*(?:ratif|hierarch)[^)]*\)",
    re.IGNORECASE,
)


def ratify_brief_findings(root):
    """Warn-first brief lint (WI-146b): an open-items row whose decision is a
    `[phase]-[g1|g2]` ratification should point at the batch-scoped ratification
    hierarchy view (`trace.py --ratify <phase>`) instead of hand-copying registry
    rows. WARN only — never a gate fail (the house stance for prose surfaces,
    WI-129/132).

    Reads `docs/requirements/open-items.csv` since WI-322 retired the markdown
    surface; the brief text is the row's prose cells. Vacuous when the registry
    is absent or carries no ratification brief, so a repo without the surface
    pays nothing."""
    path = root / OPEN_ITEMS_CSV
    if not path.is_file():
        return []
    out = []
    for row in read_rows(path):
        oid = (row.get("OI-ID") or "").strip()
        if not oid.startswith("OI-") or oid.endswith("-000"):
            continue
        if (row.get("Status") or "").strip().lower() != "pending":
            continue
        body = " ".join(
            (row.get(k) or "")
            for k in ("OneLine", "Decision", "BlastRadius", "Options", "Recommendation")
        )
        is_ratification = RATIFY_ANCHOR_RE.search(body) and re.search(
            r"ratif", body, re.IGNORECASE
        )
        if not is_ratification or RATIFY_VIEW_RE.search(body):
            continue
        out.append(
            "{}: a [phase]-[g1|g2] ratification brief should name the batch-scoped "
            "hierarchy view (generate it with `trace.py --ratify <phase>`) instead "
            "of hand-copying registry rows ({})".format(oid, OPEN_ITEMS_CSV)
        )
    return out


def _load_critique_srs(root):
    """SR ids whose Verification is `Critique` (system-requirements.csv). Empty
    makes the critique ratchet vacuous — a repo with no perceptual SR pays
    nothing."""
    out = set()
    for r in read_rows(root / SR_CSV):
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
    Any missing git context makes it a silent no-op, like `staged_findings`."""
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
# after the latest CRITIQUE means the Verified perceptual stamp judged an older
# render, so the critique should re-fire.
_RENDER_RECIPE_REL = "scripts/dashboard-shots/shoot.mjs"


def _render_surface_paths(root):
    """Repo-relative render-surface paths that EXIST under `root`: the co-located
    dashboard generator `gen_trajectory.py` and the render recipe if the repo
    carries one. A downstream without the meta-only recipe pays nothing for it;
    an unlocatable generator yields no path (the check then stays silent).

    Accepted warn-first boundary: layout-affecting values the generator IMPORTS
    from sibling modules (e.g. a display constant defined in this checker) are NOT
    watched — folding them in would fire the warn on every unrelated edit to those
    modules. The surface is the generator + recipe themselves; a render change that
    lands only in an imported constant is a known, tolerated miss."""
    out = []
    gen = Path(__file__).resolve().with_name("gen_trajectory.py")
    try:
        rel = gen.relative_to(root)
        if gen.is_file():
            out.append(rel.as_posix())
    except ValueError:
        # the checker is not under root (unusual) — try the kit's two homes.
        for cand in (
            "project-trajectory/scripts/gen_trajectory.py",
            "scripts/gen_trajectory.py",
        ):
            if (root / cand).is_file():
                out.append(cand)
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
    the Verified stamp is judging an older render. When a render-surface path (the
    co-located `gen_trajectory.py`, plus the render recipe if present) last
    changed STRICTLY AFTER the latest CRITIQUE evidence, flag that the perceptual
    gate is stale and the dashboard critique should be re-run against the current
    render. Returns finding strings ([] when not applicable).

    TIERED severity (set by the caller): WARN at the commit bar, ERROR under
    `--strict` (the G3 gate) — fail-closed per the owner's 2026-07-20 ruling, a
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
        "from WARN to ERROR (wired at gate G2+; R-A always fails regardless)",
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
        print("check_trajectory: off (docs/trajectory-check) — nothing to check.")
        return 0

    # --staged is the commit-time no-validation-delta warn only: never blocks,
    # never re-runs the full validation (the trajectory step already did). Three
    # warns: the follow-up-on-a-done-SR ratchet, the critique-loop ratchet
    # (a WI closing under a CHANGES-REQUESTED critique without hardening the
    # chain), the WI-316 amend-without-flip warn (attested spine prose
    # changed without the Modified re-attest marker), and the WI-352 close-time
    # completion warn (the row flips to `done` while its spec still has unticked
    # Done-when boxes — the only moment that disagreement is cheaply fixable,
    # since archival leaves nothing but a cosmetic edit).
    if args.staged:
        for w in (
            staged_findings(root)
            + critique_ratchet_findings(root)
            + staged_spine_findings(root)
            + staged_completion_findings(root)
        ):
            print("check_trajectory: WARN - {}".format(w), file=sys.stderr)
        return 0

    # Architecture-connectivity coverage (S5/WI-056; process.md §8) — warn-first,
    # never an exit-code change (even under --strict). Runs before the WI vacuity
    # return so a repo with modules + seams but no work items is still covered;
    # vacuous under docs/interfaces-check: off or a ≤1-module arch-map.
    for w in interface_findings(root):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    # Ratification-brief hierarchy-view lint (WI-146b) — warn-first prose-surface
    # check: a `[phase]-[g1|g2]` ratification brief should link the generated
    # batch-scoped hierarchy view. Vacuous without a ratification brief.
    for w in ratify_brief_findings(root):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    # How-SW top-view right-sizing (WI-073/FB5) — WARN plain, ERROR under --strict
    # (G2+). Runs before the WI vacuity return too (the bound is a property of the
    # arch-map inventory + the component registry, independent of work items), so
    # a repo with a big arch-map and no CMP rows still trips even with no WIs.
    comp_errors = []
    for msg in component_findings(root):
        if args.strict:
            comp_errors.append(msg)
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
        if comp_errors:
            for e in comp_errors:
                print("check_trajectory: ERROR - {}".format(e), file=sys.stderr)
            print(
                "check_trajectory: {} architecture finding(s).".format(
                    len(comp_errors)
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

    errors = comp_errors + integrity + validate(wis, load_known_srs(root))
    # Specs act on declared interface boundaries (WI-191) — WARN plain, ERROR
    # under --strict (G2+); vacuous until a spec adopts an `## Interfaces` section.
    for msg in spec_interface_findings(root):
        if args.strict:
            errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)
    # status.md forward-only (WI-200; the mode-aware R-D restoration) — WARN plain,
    # ERROR under --strict (G2+); yields to a status.md generated-block marker.
    for msg in status_forward_only_findings(root, wis):
        if args.strict:
            errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)
    # Backlog-staleness (WI-205) — an open WI whose cited SR row or SpecRef target
    # was amended AFTER the WI row was last touched is re-flagged for a driven
    # re-validation. WARN-ONLY: it never joins the exit code, not even under
    # --strict (the WI-129 warn-tier-checker stance); silent off-git.
    for msg in backlog_staleness_findings(root, wis):
        print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)
    # The SSOT coherence layer: R-A is always an error; R-E, the
    # unknown-status lint are WARN unless
    # --strict promotes them.
    findings = ssot_findings(wis, root)
    # Dead dependency (WI-267): an open WI hard-depends on a retired (terminal
    # WON'T-BUILD) predecessor it can never see satisfied. WARN plain, ERROR under
    # --strict — same warn-tier as R-E (no new branch in main).
    findings.extend(("dead-dep", False, msg) for msg in dead_dependency_findings(wis))
    # Perceptual re-fire (WI-243) — a Verification=Critique SR whose latest CRITIQUE
    # evidence predates a dashboard render-surface change is judging an older render.
    # WARN at the commit bar; **fail-closed under --strict** (the G3 gate) per the
    # owner's 2026-07-20 ruling — a stale render surface cannot reach a green gate.
    # hard=False rides the same warn-plain / error-under-strict tier as R-E,
    # so main() gains no branch. Vacuous when no perceptual SR / evidence / render
    # surface (a downstream repo without a Verification=Critique SR — none ship —
    # pays nothing), silent off-git, and opt-out via docs/trajectory-check.
    findings.extend(
        ("perceptual-stale", False, msg) for msg in critique_staleness_findings(root)
    )
    # Spec-lifecycle close side (WI-251, rule R-F) — done WI with a live SpecRef,
    # or a live docs/specs file no open WI cites. Same warn-plain / error-under-
    # --strict tier (no new branch in main); the R-E open-half's closing
    # counterpart.
    findings.extend(("R-F", False, msg) for msg in spec_lifecycle_findings(root, wis))
    # Completion reconciliation (WI-352) — the declared `Status` cell against the
    # spec's Done-when boxes and the `WI:` trailers. WARN plain, ERROR under
    # --strict, the same warn tier as R-E/R-F, EXCEPT the trailer signal.
    #
    # DEVIATION from the WI row, which asked for the whole reconciler at that
    # tier, taken on the row's OWN argument: it rules that Status stays an
    # attestation precisely because a trailer means "a commit claims this WI",
    # not "the work is right", and cites WI-336 — code landed, row correctly left
    # `queued`, a review having refuted three of its claims. Under an
    # error-under-strict trailer rule that legitimate state blocks the G3 gate
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
    # WI-267: `retired` (terminal WON'T-BUILD) rows are counted SEPARATELY, never
    # folded into `done`; surfaced only when present so the line stays unchanged
    # for the common no-retired registry.
    retired = sum(1 for w in wis if w["status"] == "retired")
    retired_note = ", {} retired".format(retired) if retired else ""
    print(
        "check_trajectory: clean ({} work item(s), {} done ({}%){}, graph "
        "acyclic).".format(len(wis), done, round(100 * done / len(wis)), retired_note)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
