"""The SPINE ROW vocabulary — what one registry row's cells MEAN, stated once.

THE PAIR THAT HAD TWO HOMES (WI-448 slice 3; census 2026-08-12, `repo-lock.md`
§8.2). `trace.py` ENFORCES the spine and `spine_rules.py` DERIVES its stage from
the same rows, so every question either one asks of a single cell was asked
twice: what `Drafted`/`Approved`/`Founded` mean, which `Verification` methods
decompose to a TC but no LLR, what integer a free-form `Phase` cell parses to,
which `SN-###` tokens a needs registry mentions, and which of them the SRs cite.
Nine duplicated function bodies, held equal by nine `tests/test_rule_sync.py`
pins, because the retired F5 rule licensed the duplication and D-7 could only
CONTAIN the drift rather than remove it.

Those questions are POLICY, not plumbing, and a policy disagreement between
those two modules is a false green or a false red AT A GATE — the exact failure
class the kit exists to prevent (repo-review-2026-07-12b M1 -> WI-099). Owner
ruling D-8 (`OI-16`) replaced F5: the rule lives here, once, and both modules
import it under their existing local names, so no call site moved.

WHY ITS OWN MODULE, AND NOT `registry.py` (the choice, recorded). `registry.py`
is the `docs/work/` SPEC-FOLDER reader — a different registry, a different
carrier, a different consumer set. Folding two unrelated registries into one
file is how a themed package acquires the generic bucket the 2026-08-19 review
(H-09) explicitly forbade this package, and it would have grown the package's
largest module instead of the smallest sensible new one. This module is the
`ladder.py` shape one tier over: a CLOSED VOCABULARY as near-pure data, below
every axis that reads it.

WI-448 SLICE 4 ADDED THE CELL-SHAPE RULES THE PAIR'S NEIGHBOURS ALSO ASKED.
`refs` (the multi-ref cell split) had six homes and `is_example` a third one
outside the pair; `norm_module` — what an IF `Endpoint`, an LLR `Module` cell
and an arch-map node name all reduce to — had two. They are the same KIND of
statement as the rules above (what one cell MEANS), asked by `gen_okf.py`,
`plan_coverage.py`, `plan_artifacts.py`, `schedule.py`, `check_trajectory.py`,
`gen_arch_map.py` and `gen_release_checklist.py` rather than only by the pair.

WI-448 SLICE 5 ADDED THE ROW-WHOLE STATEMENTS THE SCAFFOLDER ALSO HAD TO MAKE.
The per-tier SCHEMA OF RECORD (`REGISTRY_KEYS`) moved down from
`spine_carrier.py`, which now binds it, and the TOML value/line emitter moved
down from `wi_convert.py`, which does the same. Both are the module's one
sentence stated for the ROW rather than for a cell — which keys a row declares,
and how its cells are spelled in the carrier — and both had a reader the carrier
could not serve: `bootstrap.py` may import this package and no other sibling, so
while they lived up there the scaffolder RESTATED them and a `test_rule_sync`
pin held the restatement equal. It now reads them.

WHAT IS DELIBERATELY NOT HERE:

  * `sn_draft_ids` — the tenth duplicate of the pair, and the one that CANNOT
    move. Both copies were a one-line delegation to
    `spine_carrier.draft_ids_from_text`, and this package's one asserted rule is
    that it imports no sibling of `scripts/` (a `kitlib` module reaching for
    `spine_carrier` would smuggle the whole graph into the scaffolder). So the
    duplicate is retired the other way: both modules now BIND the sibling
    function directly, under the same local name, and the copy disappears
    without a home here.
  * `is_drifted`, the maturity tables, and the rung fall-through — each has
    exactly one home already, and `tests/test_rule_sync.py` pins that they keep
    it.

Stdlib only, and import-clean of the rest of `scripts/`, like every module here.
"""

import csv
import io
import re

__all__ = [
    "LLR_EXEMPT",
    "MODULE_EXTS",
    "load_csv",
    "csv_body",
    "csv_reader",
    "csv_rows",
    "norm_module",
    "refs",
    "is_example",
    "is_drafted",
    "is_approved",
    "is_founded",
    "llr_exempt",
    "phase_num",
    "sn_all_ids",
    "sn_cited_ids",
    "SPINE_TIER_KEYS",
    "OFFSPINE_KEYS",
    "REGISTRY_KEYS",
    "toml_string",
    "toml_value",
    "toml_fields",
]

# SR Verification methods with no code to decompose, so they need a TC but no
# LLR: the orphan rule exempts them and the LLReqs rung does not hold open for
# them. Critique is NOT here — its artifact is produced by code, only its
# acceptance is subjective.
#
# A FROZENSET, WHICH SETTLES A REAL DISAGREEMENT BETWEEN THE TWO COPIES: this
# was a `set` in `spine_rules.py` and a `tuple` in `trace.py`. Both answer `in`
# identically, so the value pin (`set(TRACE.LLR_EXEMPT) == set(GATE.LLR_EXEMPT)`)
# was structurally blind to it — the same shape as the comment-only drift the
# spec-folder extraction found. Immutable is the right answer for a closed
# vocabulary a shared kernel hands out: a caller that mutated the `set` copy
# would have moved the gate for every other reader in the process.
LLR_EXEMPT = frozenset({"Analysis", "Inspection", "Attest"})


def csv_body(text):
    """The CSV text with its leading `#`-comment PREAMBLE removed — the header
    ROW is the first line that is neither a comment nor blank.

    A registry CSV may open with the same `#` declaration header a TOML or INI
    registry carries (the `Contracts:` marker and `Contract IF-###:` bodies of
    the interface shape): `performance-budgets.csv` is such an owner.
    `csv.DictReader` knows nothing of comments and would take the first `#`
    line as the header row, which makes every real column — `PB-ID` first —
    unaddressable in every reader at once. Only LEADING comment lines are
    dropped: a `#` opening a data line, or one inside a quoted multi-line
    cell, is data and stays. A BOM is stripped first, for the reason
    `spine_carrier.rows_from_text` states: a BOM'd header glues to the first
    column name and every row hides.

    A BLANK LINE BELONGS TO THAT PREAMBLE, and dropping it is the same rule
    rather than a second one: a hand-written header block ends with a blank
    line before the columns, and leaving it in hands `csv.DictReader` the BLANK
    line as its header row — every real column unaddressable again, the exact
    failure this function exists to prevent, one line further down. Only the
    LEADING run is dropped: a blank line AFTER the header row is `csv`'s own
    business and is untouched. An all-comment, all-blank or empty file still
    yields no rows."""
    lines = text.lstrip("\ufeff").splitlines(keepends=True)
    i = 0
    while i < len(lines) and (
        not lines[i].strip() or lines[i].lstrip().startswith("#")
    ):
        i += 1
    return "".join(lines[i:])


def csv_reader(text):
    """`csv.DictReader` over `csv_body(text)` — the ONE way a kit reader turns
    registry CSV text into rows, so a header-carrying registry reads
    identically everywhere; callers that need `fieldnames` take this one."""
    return csv.DictReader(io.StringIO(csv_body(text)))


def csv_rows(text):
    """`csv_reader(text)` as a list."""
    return list(csv_reader(text))


def load_csv(path):
    """A registry CSV as a list of dict rows, or `[]` when the file is absent.

    `utf-8-sig` because a spreadsheet round-trip leaves a BOM on the first
    header cell, which would otherwise make the id column unaddressable, and
    `errors="replace"` so one mis-encoded cell degrades to a visible replacement
    character rather than crashing a check. Read through `csv_rows`, so a
    leading `#` declaration header is a header and never the header row.

    Contract:
      Inputs:  path: `pathlib.Path` to a registry CSV (may not exist)
      Outputs: list[dict] — the data rows; `[]` if the file does not exist
    """
    if not path.exists():
        return []
    return csv_rows(path.read_text(encoding="utf-8-sig", errors="replace"))


def refs(value):
    """Split a multi-ref cell (';', ',' or whitespace separated) into ids.

    SIX HOMES BEFORE WI-448 SLICE 4, and one of them had drifted: this exact
    body stood in `check_trajectory._split_refs`, `gen_okf.split_refs`,
    `plan_coverage.split_refs`, `plan_artifacts._split_tokens`,
    `schedule._split_refs` and here. `plan_coverage`'s copy had split on `[;,]`
    alone (B10, part-A census 2026-08-13), so a whitespace-separated pair in an
    LLM-authored plan cell read as ONE garbage token and matched nothing — the
    same splitting defect class as the SN-001/SN-002 orphan bug OI-12 records.
    A pin repaired that copy; this module retires the copies instead."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


# Source-file extensions stripped when normalizing a module path, so an IF
# endpoint written with the full repo path
# (`project-trajectory/scripts/check.py`), an LLR `Module` cell and an arch-map
# node name (`scripts/check`) all collapse to one key.
MODULE_EXTS = (".py", ".sh", ".ps1", ".ts", ".js", ".go", ".rs", ".cmd")


def norm_module(path):
    """A module path reduced to a naming-convention-neutral key: strip a leading
    `project-trajectory/`, any source extension, and a trailing `/__init__`.

    A CELL RULE, which is why it is here rather than in a module-identity home
    of its own. Every call site normalizes a registry cell or a path it is about
    to compare against one — an IF row's `Endpoint`/`ThisProject`/`Counterpart`,
    an LLR row's `Module`, or the source file those cells are claiming. THREE
    modules asked it — `check_trajectory.py`, which enforces those rows,
    `gen_arch_map.py`, which draws them, and `trace_text.py`, whose endpoint
    predicate WI-464 had already pulled out of `trace.py` — and
    `check_trajectory`'s copy carried a comment promising it was "kept in sync
    with `trace.py._MODULE_EXTS`", a home that DOES NOT EXIST, so the promise
    named nobody while its real partners went unmentioned. That is the
    declared-line pattern again: a prose claim of equivalence with no referent.

    The `MODULE_EXTS` spelling above is `trace_text.py`'s, not the two private
    `_MODULE_EXTS` ones, and that is deliberate: the census hashes a body's AST
    including the NAME it loads, so the third copy scored as a different
    function for as long as it spelled the constant differently.

    Contract:
      Inputs:  path: str | None — a module path in any of the three spellings
      Outputs: str — the normalized key ('' for an empty/None input)
    """
    p = (path or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/") :]
    for ext in MODULE_EXTS:
        if p.endswith(ext):
            p = p[: -len(ext)]
            break
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p


def seam_endpoints(cell):
    """The endpoints of one IF endpoint cell, split on `;` ONLY.

    An endpoint may legitimately contain a space (`external:downstream
    adopter`) or a comma, so `;` is the only separator — and a `Consumers` cell
    is a LIST in the carrier, joined on `;` by `spine_carrier.value_to_cell`,
    so the same split reads it back."""
    return [e.strip() for e in (cell or "").split(";") if e.strip()]


# The closed `channel` vocabulary (OI-67 ruled (a)): what crosses the seam,
# typed. `exit-code` and `env` are the finite-alphabet kinds; the rest are
# unbounded. A dial read from a config file is `file` (the medium is the
# file; `data` names the key); a source tree walked by AST is `file`.
IF_CHANNELS = frozenset(
    {"cli", "exit-code", "stdout", "file", "call", "env", "git", "bytes"}
)


def seam_owner(row):
    """An IF row's OWNER-side endpoint — the providing thing, read off the cell
    (OI-67 ruled (a), 2026-08-29).

    ONE SPELLING, the same one `consumers` uses: a module path, a file or
    directory path, or an `external:` party. Nothing is derived — the
    `owner` -> LLR -> `Module` join that `seam_provider` ran until this ruling
    retired with the id-typed owner it read, because a design row's module IS
    the providing thing and a derivable cell was a second spelling of it.

    Contract:
      Inputs:  row: dict — one IF row under today's column names
      Outputs: str — the owner endpoint, or '' when the cell is absent (the
               required-field rule's finding, never this reader's)
    """
    return (row.get("Owner") or "").strip()


def seam_requestors(row):
    """The sides that put information INTO the surface the owner defines —
    they call the function, invoke the CLI, set the env var, write the file."""
    return seam_endpoints(row.get("Requestors"))


def seam_consumers(row):
    """The sides that take what the owner emits — they read the file, the exit
    code, the stdout."""
    return seam_endpoints(row.get("Consumers"))


def seam_far_side(row):
    """`(inbound, endpoints)` — the row's far side and which way the
    information runs. THE KEY NAME IS THE DIRECTION: a row names `requestors`
    (information flows far side -> owner) or `consumers` (owner -> far side),
    exactly one, so one row is one direction by construction rather than by
    discipline. A row naming both or neither is `trace.py`'s finding; this
    reader answers the requestors first so a malformed row still draws one
    way rather than none."""
    requestors = seam_requestors(row)
    if requestors:
        return True, requestors
    return False, seam_consumers(row)


def is_example(rid):
    """The `-000` placeholder-row convention: a template row, nobody's finding."""
    return (rid or "").endswith("-000")


def is_drafted(row):
    """A row in the pre-approval `Drafted` state.

    Exempt from the child-completeness orphan rules (a Drafted SR needs no
    LLR/TC) and from the `--require-verified` criterion, so a requirement can
    live in the live spine while it is being drafted — and it HOLDS ITS RUNG
    OPEN on the derivation side, which is the same fact seen from the other end.

    `Status` is a CLOSED vocabulary since D-9 step 1 and reached the ruled ladder
    at steps 7/8: `{Drafted, Approved, Founded}`. Matched case-insensitively on
    the stripped cell — the one Status-casing rule (process.md §4) — which all
    three predicates here share.

    Contract:
      Inputs:  row: a registry row mapping (a missing `Status` reads as absent)
      Outputs: bool
    """
    return (row.get("Status") or "").strip().lower() == "drafted"


def is_approved(row):
    """The `Approved` state: the row's TEXT is blessed by a human.

    RENAMED FROM `is_verified` AT D-9 STEP 5, and the rename carries a RULING.
    `Verified` made TWO claims at once — the text is approved AND the evidence
    passed — and the second was a hand-set cell asserting a test run nobody
    re-ran. `Approved` says only that the text is blessed; whether the tests
    pass is the harness's answer (`kitlib.evidence`). `Planned` folded into this
    same value at the same act (OI-30 D1).

    Contract:
      Inputs:  row: a registry row mapping
      Outputs: bool
    """
    return (row.get("Status") or "").strip().lower() == "approved"


def is_founded(row):
    """The ladder's TOP rung: settled AND the artifacts the row calls for EXIST.

    Armed for the spine at D-9 step 8 the way it armed for CMP at the registry
    status unification — the word becomes legal, no live cell moves to it. It
    reads ABOVE `Approved`, so arming it can never LOWER a derived reading. The
    DISCHARGE is computed per tier elsewhere; this reads the cell, like its two
    siblings.

    Contract:
      Inputs:  row: a registry row mapping
      Outputs: bool
    """
    return (row.get("Status") or "").strip().lower() == "founded"


def llr_exempt(row):
    """SR `Verification` method in `LLR_EXEMPT`, matched on the STRIPPED cell.

    The stripping is load-bearing and was once a live divergence: review 017
    caught the two former copies disagreeing on a whitespace-padded valid method
    (one stripped, one did not), which is a false green on one surface and a
    false red on the other for one registry state.

    Contract:
      Inputs:  row: an SR row mapping
      Outputs: bool
    """
    return (row.get("Verification") or "").strip() in LLR_EXEMPT


def phase_num(row):
    """The integer a row's free-form `Phase` cell digit-parses to (`v2`->2).

    None when the cell is blank or holds no digits. The ONE phase-parse the kit
    uses, so a downstream repo that kept `vN` labels parses identically wherever
    the phase doctrine (process.md §4) is applied.

    Contract:
      Inputs:  row: a registry row mapping
      Outputs: int | None
    """
    m = re.search(r"\d+", (row.get("Phase") or ""))
    return int(m.group()) if m else None


def sn_all_ids(text):
    """The SN id UNIVERSE: every `SN-###` token anywhere in a needs registry.

    A WHOLE-TEXT scrape, so a prose mention counts exactly like a table row —
    the sharp edge `registry-machinery-reference` §2.1 records (an approved,
    uncited prose mention caps the derived stage through the coverage rung).
    `-000` placeholders excluded. This scrape decides which ids BOTH the gate
    derivation and the itemized orphan listing run their rules over, which is
    why it may have only one definition.

    Contract:
      Inputs:  text: the needs registry's raw text, under EITHER carrier
      Outputs: set[str]
    """
    return {u for u in re.findall(r"\bSN-\d+\b", text) if not is_example(u)}


def sn_cited_ids(srs):
    """Every SN id cited by >=1 SR row's `SN-Refs` cell — the coverage set.

    No filtering here, deliberately: `-000` rows are excluded by the CALLER's
    row filter, and a Drafted SR's citation is IN the set (the raw view; the
    ex-draft counterfactual re-runs this on the non-draft subset rather than
    special-casing it here).

    Contract:
      Inputs:  srs: iterable of SR row mappings
      Outputs: set[str]
    """
    # THE `Implements: SR-049, LLR-147` TAG CAME WITH THIS BODY AND WAS REMOVED
    # ON ARRIVAL. LLR-147's CodeSymbol is `spine_stage/sn_cited_ids` on
    # `spine_rules.py`, and `spine_stage` — the rung fall-through that reads this
    # set — did NOT move; carrying the tag here would claim a row about the
    # coverage rung for the primitive it consumes, and `check_trajectory`'s
    # symbol check says so. No sibling module in this package carries a tag:
    # `LLR-197` claims the whole module, which is the right grain for a
    # vocabulary whose eleven names are one decision.
    return {x for r in srs for x in refs(r.get("SN-Refs"))}


# ---------------------------------------------------------------------------
# THE SCHEMA OF RECORD — which keys each registry tier declares.
#
# MOVED HERE FROM `spine_carrier.py` at WI-448 slice 5, unchanged. It is the
# same KIND of statement as everything above — what one registry row's cells
# MEAN — stated for the row as a whole instead of for one cell, and its readers
# are the whole kit rather than the carrier: `tests/test_dogfood_sync.py` checks
# every template and live registry against it, and the SCAFFOLDER writes a row
# under it (`bootstrap.append_stack_checklist` files the non-Python profile's
# `OI-3` brief). That last reader is why the move was owed rather than merely
# tidy: `bootstrap.py` may import this package and no other sibling, so while
# the schema lived in the carrier the scaffolder could only RESTATE the keys and
# have a test hold the restatement equal. Now it reads them.

# THE PER-TIER SCHEMA: which keys each tier declares, keyed by its id column.
# STATED, never derived — and the reason is the one the ordered CSV header used
# to provide for free.
#
# Under CSV the live file declared its own schema in a header, so a template
# that quietly dropped a column diverged from something. TOML has no header and
# an absent key IS an empty cell, so a column no row happens to use does not
# exist in the file at all — and a rule that compares only the template against
# the live registry cannot see the template DROP such a key. `permutations` is
# exactly that today: declared by the template, used by no live SR. Deriving
# this map from either side would re-create the hole, because the side that
# dropped the key would also drop it from the derivation.
#
# So it is a third leg, and it is the DURABLE one: the schema of record that
# both the template and the live registry are checked against
# (tests/test_dogfood_sync.py). Adding a column to a tier is a reviewed edit
# here first — which is the same discipline `spine_carrier.SPINE_COLUMN` (the
# key -> column-name map, which stays with the carrier that reads columns)
# already carries, for the same reason.
SPINE_TIER_KEYS = {
    # THE NEED TIER, post-unification. `status` is the ONE maturity field (the
    # `kind`/`attestation`/`amended` trio it replaced is deleted, not renamed).
    # `tags` is OPTIONAL — ten of twenty-seven live rows carry none, and an
    # `always` hat reaches a need without one — but it is DECLARED, which is
    # the whole point: the template shipped without it precisely because no
    # schema named the tier.
    "SN-ID": (
        "status",
        "tags",
        "need",
        "why",
        "priority",
        "acceptance",
    ),
    # `hat_refs` is OPTIONAL on both row tiers that declare it, and the absence
    # semantics are stated here because they are the whole difference between a
    # useful cell and a lie: an ABSENT `hat_refs` means NOT RECORDED, never "no
    # perspective reached this row". Nothing may read a blank as a negative claim,
    # which is why the checker's coverage arm is a warn-only count and never a
    # finding (WI-484 / OI-32 phase 1).
    "SR-ID": (
        "title",
        "sn_refs",
        "boundary_refs",
        "hat_refs",
        "requirement",
        "rationale",
        "acceptance_criteria",
        "permutations",
        "priority",
        "verification",
        "status",
        "phase",
        "aspect",
    ),
    "LLR-ID": (
        "sr_refs",
        "hat_refs",
        "title",
        "module",
        "code_symbol",
        "detail",
        "rationale",
        "test_refs",
        "status",
        "component",
        "phase",
    ),
    "TC-ID": (
        "verifies",
        "level",
        "method",
        "tier",
        "parameters",
        "expected",
        "automated",
        "evidence",
        "status",
        "phase",
    ),
}

# The same third leg for the batch-2 registries — the SAME rule, not a second
# one (repo-lock §8.1: "reuse that shape rather than invent a second one").
# `tests/test_dogfood_sync.py` checks template, live registry and this schema
# against each other for every entry of REGISTRY_KEYS, so adding a column to
# `open-items` or `agents` is a reviewed edit HERE first, exactly as it is for a
# spine tier.
OFFSPINE_KEYS = {
    "OI-ID": (
        "title",
        "status",
        "raised",
        "one_line",
        "decision",
        "blast_radius",
        "options",
        "recommendation",
        "wi_refs",
        "ruled_date",
        "ruling_ref",
    ),
    "Id": (
        "family",
        "model",
        "version",
        "tier",
        "cmd_template",
        "env",
        "notes",
    ),
    # WI-443 / OI-14 part B. `signal` and `rationale` are NEW (nothing in the
    # registry typed a signal at all before this pass, and the why had nowhere
    # in the row to go, so it squatted in `contract`); `status` is GONE.
    # WI-442: `stability` is GONE and `approval` is the one maturity field; the
    # two `interface_*_external` keys are the DIRECTIONAL tie-back an IF row
    # carries ONLY when it realizes a boundary crossing (owner naming, 13m). An
    # IF row that realizes nothing carries neither — which is how the registry
    # says "internal seam" without a column claiming it.
    # WI-455 executed the held removal (OI-60 ruled (a), 2026-08-23):
    # `direction` is GONE (flow is provider→consumers, read off the two cells
    # below), `this_project`/`counterpart` are GONE, and the seam's two sides
    # are `provider` (OPTIONAL — omitted wherever `owner`→LLR→`module` derives
    # it uniquely) and `consumers` (a LIST, required).
    # THE ROW IS ONE OWNER, ITS CONSUMERS AND A TYPED STATEMENT (OI-67 ruled
    # (a), 2026-08-29): `owner` is the providing THING — a module path, a file
    # or directory path, or an `external:` party, the same spelling `consumers`
    # uses — never a requirement id; `channel` is the closed vocabulary of what
    # crosses; `data` the optional short alphabet. `provider`, `req_refs`,
    # `signal` and `signal_note` LEFT the row at that ruling, and `contract`
    # left with them once every definition had moved into its owner's
    # `Contract IF-###:` body: a row still carrying any of the five is
    # `trace.py`'s strict finding.
    "IF-ID": (
        "owner",
        "requestors",
        "consumers",
        "channel",
        "data",
        "rationale",
        # OPTIONAL, and its EMPTINESS is the ordinary answer: "this seam is
        # verified in its own right". Filled, it names the parent whose tests
        # cover a low-level seam — a `TC-###` or an `LLR-###` — which is the
        # position the `Verification` vocabulary cannot state (OI-61's
        # sub-question, sanctioned 2026-08-23). Warn-first that it resolves.
        "verified_by",
        "carried_by",
        "version",
        "status",
        "interface_from_external",
        "interface_to_external",
        "component",
        "notes",
    ),
    "CMP-ID": (
        "name",
        "category",
        "knowledge",
        "status",
        "standing",
        "superseded_by",
        "part_of",
        "notes",
    ),
    # WI-442 — the depth-0 frame's three tiers, all on `external.toml`. Each
    # gets its own schema entry for the same reason every other tier does: the
    # three-leg drift rule (tests/test_dogfood_sync.py) compares template, live
    # registry and THIS map per id column, so a column added to crossings
    # cannot leak into entities.
    "EXT-ID": ("name", "class", "description", "status", "absorbs", "notes"),
    "B-ID": ("entity", "direction", "carries", "status", "absorbs", "notes"),
    "REL-ID": ("from", "to", "kind", "flow", "status", "absorbs", "notes"),
}
REGISTRY_KEYS = dict(SPINE_TIER_KEYS, **OFFSPINE_KEYS)


# ---------------------------------------------------------------------------
# HOW A ROW'S CELLS ARE SPELLED IN THE TOML CARRIER — the emitter, once.
#
# `tomllib` is read-only by design (PEP 680 omitted a writer), so the kit writes
# its own; before WI-448 slice 5 it wrote its own THREE TIMES. Two of those were
# the same rule with different blast radii — `wi_convert`, which writes a
# `docs/work/` spec's `+++` frontmatter (that registry's row), and
# `bootstrap._toml_scalar`, which writes `docs/process.toml` keys and the
# scaffolded `OI-3` brief row. `bootstrap`'s copy escaped the backslash and the
# quote and stopped there, so a cell carrying a TAB or any other control
# character would have emitted a basic string `tomllib` then REFUSES — a
# scaffold writing a file it cannot read back. The one home is the careful one;
# the careless copy is gone rather than pinned equal to it.
#
# THE THIRD HOME STAYS, and the difference is real rather than tolerated:
# `migrate_carrier.toml_scalar` promotes a long or newline-bearing cell to a
# MULTI-LINE basic string, which is what makes the spine's prose cells readable
# in the file at all. That is a different rule about the same syntax, with one
# home and one caller (the one-shot CSV -> TOML conversion), and folding it in
# here would put a line-length policy inside the emitter every writer shares.

# Escapes exactly what TOML basic strings require: the backslash, the closing
# quote, and every control character. The named shorthands are used where TOML
# defines them and the \\uXXXX form covers the rest, so nothing is left to the
# parser's discretion. Verified by re-parsing every emitted file with tomllib.
_TOML_ESCAPES = {
    "\\": "\\\\",
    '"': '\\"',
    "\b": "\\b",
    "\t": "\\t",
    "\n": "\\n",
    "\f": "\\f",
    "\r": "\\r",
}


def toml_string(value):
    """`value` as a TOML basic string, escaped so tomllib reads it back exactly.

    Contract:
      Inputs:  value: str
      Outputs: str — the quoted literal, escapes included
    """
    out = ['"']
    for ch in value:
        escaped = _TOML_ESCAPES.get(ch)
        if escaped is not None:
            out.append(escaped)
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\u{:04x}".format(ord(ch)))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def toml_value(value):
    """`value` as TOML: bool, int, an array of basic strings, or a basic string.

    Contract:
      Inputs:  value: bool | int | list | tuple | anything str-able
      Outputs: str — the TOML literal
    """
    if isinstance(value, bool):  # guard: bool is an int subclass in Python
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(toml_string(v) for v in value) + "]"
    return toml_string(value)


def toml_fields(pairs):
    """One row's cells as `key = value` lines, in the order given.

    Contract:
      Inputs:  pairs: iterable of (key, value)
      Outputs: str — the block, every line newline-terminated
    """
    return "".join("{} = {}\n".format(k, toml_value(v)) for k, v in pairs)
