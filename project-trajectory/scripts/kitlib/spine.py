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
import re

__all__ = [
    "LLR_EXEMPT",
    "MODULE_EXTS",
    "load_csv",
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


def load_csv(path):
    """A registry CSV as a list of dict rows, or `[]` when the file is absent.

    `utf-8-sig` because a spreadsheet round-trip leaves a BOM on the first
    header cell, which would otherwise make the id column unaddressable, and
    `errors="replace"` so one mis-encoded cell degrades to a visible replacement
    character rather than crashing a check.

    Contract:
      Inputs:  path: `pathlib.Path` to a registry CSV (may not exist)
      Outputs: list[dict] — the data rows; `[]` if the file does not exist
    """
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


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
