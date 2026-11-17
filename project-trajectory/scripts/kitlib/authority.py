"""Acceptance authority: which rung a registry's status cells are accepted into,
whether a declared acceptance level holds that rung for an operator, and what the
dial a chosen tree declares is.

WHY IT IS A MODULE OF ITS OWN (LLR-249). Every reader that asks "does the dial
hold this rung" asks it here: the loop's own writers before they commit, the
pre-commit `held-status` step, the merge slot, and the HISTORY CHECK, which
reads each past commit's own tree. None of them may reach for the coordinator's
primitives to ask a question about a string and a table, so the comparison,
the rung tables and the dial reader live here, below all of them, and
`agent_common` re-exports the tables under the names every caller already uses.
One table, one reader and one comparison, so the loop's refusal and the
history's report cannot disagree about which rung is held.

THE RUNG MAPS, and the fail-safe they share:

  * `ACCEPTANCE_RUNGS` keys the OFF-SPINE registries that carry a status cell by
    their stem. The association is existing fact (`spine_rules` gates the
    Boundary rung on the frame and the Arch rung on the components), not a new
    declaration. The assumptions registry sits at the frame's rung: an
    assumption lands on a boundary crossing, and is accepted with the frame it
    lands on.
  * `SPINE_ACCEPTANCE_RUNGS` keys the spine registries by path stem. It is also
    the mint's table (which Drafted rows a merge hands an adjudicator), so it
    names only what the mint asks about.
  * `NEEDS_REGISTRY` is the one file that carries two tiers: the needs (a spine
    tier) and the stakeholder list (an off-spine one). Both are accepted at
    `DevStg-Needs` - `spine_rules` derives that rung while a need is still
    drafted - so `rung_for` answers it for the file without widening the
    mint's table.
  * A registry none of them names is held (`rung_for` answers None and every
    caller reads None as the operator's), because a status nobody has associated
    with a rung is one nobody has released.

THE DIAL, READ ONE WAY: `dial_from_config(policy)` reads `[authority]
operator_accepts_through` from a parsed policy file, and anything absent,
wrong-typed or unrecognised reads as the MOST-held rung, silently. Every
reader runs it: `agent_common.acceptance_through` over the working file, the
history check over each past commit's tree, and `dial_at(root, rev)`, THE LIVE
READER, over the tree a writer, the pre-commit step or the merge slot names,
never a primary checkout's working file, where an uncommitted operator edit
could strengthen or weaken the judgement of a tree built from HEAD. Spellings
older than the current vocabulary are not read (D11): the vocabulary migrator
rewrites the ones a repository stores, and an unmigrated dial holds every
rung, which only ever asks the operator for more.

Pure data and comparisons over `kitlib.ladder`, plus one git read (`dial_at`,
through `kitlib.git`); no argv, and nothing printed.

Contracts: IF-195 — the interface seam this module declares (process.md §8;
row of record in docs/requirements/interfaces.toml).

Contract IF-195: the acceptance-authority vocabulary, by importer.
    `ACCEPTANCE_RUNGS` (off-spine registry stem -> rung) and
    `SPINE_ACCEPTANCE_RUNGS` (spine registry path stem -> rung) are the one pair
    of tables; `rung_for(registry)` maps a registry path, stem or bare name to
    its rung - the needs file, both of its tiers, to `DevStg-Needs` - or None
    when nothing maps it, which every caller reads as held.
    `dial_from_config(policy)` returns the `[authority]
    operator_accepts_through` rung of a parsed policy, `DevStg-Below` included,
    or the most-held rung for anything absent, wrong-typed or unrecognised,
    printing nothing; `dial_at(root, rev="HEAD")` returns that rung for `rev`'s
    tree, or the index's when `rev` is None, printing nothing, and the
    most-held rung when nothing is declared or git cannot answer.
    `holds_under(dial, rung)` is True when the dial holds the rung for an
    operator: never at `DevStg-Below`, always for an unrecognised dial or rung,
    otherwise when the rung sits at or below the dial on the ladder.
"""

import tomllib

from . import git as _git
from . import ladder, stage

# THE OFF-SPINE MAP (operator ruling OI-30 D3, 2026-08-15; moved here from
# agent_common by LLR-249, which re-exports it). Keyed by the registry's stem.
ACCEPTANCE_RUNGS = {
    "external": ladder.STAGE_BOUNDARY,
    "interfaces": ladder.STAGE_ARCH,
    "components": ladder.STAGE_ARCH,
    "assumptions": ladder.STAGE_BOUNDARY,
}

# THE SPINE MAP (operator ruling 2026-09-01, WI-572; moved here with its sibling).
# Keyed by the registry's path stem, the key `spine_carrier.stem` produces.
SPINE_ACCEPTANCE_RUNGS = {
    "docs/requirements/system-requirements": ladder.STAGE_REQS,
    "docs/requirements/low-level-requirements": ladder.STAGE_LLREQS,
    "docs/test/test-cases": ladder.STAGE_TESTS,
}

# The needs file's path stem: both of its tiers, the needs and the stakeholder
# list, are accepted at the needs rung.
NEEDS_REGISTRY = "docs/requirements/stakeholder-needs"

DIAL_KEY = "operator_accepts_through"

# Every rung at or below the top one is held: the conservative end.
MOST_HELD = ladder.STAGE_RELEASE

# Where a tree declares its dial.
POLICY_PATH = "docs/process.toml"


def rung_for(registry):
    """The rung `registry`'s status cells are accepted into, or None when no
    map names it — which every caller reads as HELD. Accepts a path under
    either carrier, a path stem, or a bare stem such as `"external"`."""
    path = str(registry or "").strip().replace("\\", "/")
    stem = path[: -len(".toml")] if path.endswith(".toml") else path
    stem = stem[: -len(".csv")] if stem.endswith(".csv") else stem
    if stem in SPINE_ACCEPTANCE_RUNGS:
        return SPINE_ACCEPTANCE_RUNGS[stem]
    name = stem.rsplit("/", 1)[-1].lower()
    if name == NEEDS_REGISTRY.rsplit("/", 1)[-1]:
        return ladder.STAGE_NEEDS
    return ACCEPTANCE_RUNGS.get(name)


def _is_dial(value):
    return isinstance(value, str) and (
        value.strip() in ladder.LADDER_RUNGS or value.strip() == stage.BELOW
    )


def dial_from_config(policy):
    """`[authority] operator_accepts_through` from a parsed policy file, as a
    rung or `DevStg-Below`; the most-held rung for anything else, silently.
    THE resolution every reader runs (`dial_at`,
    `agent_common.acceptance_through`, the history check), so the pre-commit
    step, the writers, the slot, the coordinator and the history report cannot
    disagree about what a dial means. Any value that is not a rung or
    `DevStg-Below` is MALFORMED and reads as the most-held rung, never a best
    guess, because every wrong guess fails toward less operator involvement.

    Implements: SR-208, SR-210, LLR-246, LLR-249
    """
    table = policy.get("authority") if isinstance(policy, dict) else None
    value = table.get(DIAL_KEY) if isinstance(table, dict) else None
    return value.strip() if _is_dial(value) else MOST_HELD


def dial_at(root, rev="HEAD"):
    """THE LIVE DIAL OF A CHOSEN TREE: the rung `rev`'s committed tree declares,
    or the INDEX's when `rev` is None (`dial_from_config`), printing nothing.

    Read from git, never from a working file, because every live question about
    the dial is a question about a TREE: the tree a writer is about to commit
    onto, the commit a hook is about to make, the trunk a lane merges into. An
    uncommitted edit in a primary checkout is none of those, and reading it let
    an operator's half-made edit release (or hold) a commit built from HEAD. A
    policy file git cannot show, or that does not parse, declares nothing, and
    the answer is the most-held rung, so no git, no repository and an unknown
    rev all fail toward the operator.

    Implements: SR-208, LLR-246
    """
    prefix = ":" if rev is None else "{}:".format(rev)
    text = _git.git_out(root, ["show", prefix + POLICY_PATH])
    try:
        policy = tomllib.loads(text.lstrip("﻿")) if text else {}
    except tomllib.TOMLDecodeError:
        policy = {}
    return dial_from_config(policy)


def holds_under(dial, rung):
    """Does `dial` hold `rung` for an operator? Nothing at `DevStg-Below`; every
    rung at or below the dial otherwise; and an unrecognised dial or rung is
    HELD, because the only safe answer to "I do not recognise this" is "the
    operator accepts it".

    Implements: SR-210, LLR-249
    """
    if dial == stage.BELOW:
        return False
    if dial not in ladder.LADDER_RUNGS or rung not in ladder.LADDER_RUNGS:
        return True
    return ladder.stage_ord(rung) <= ladder.stage_ord(dial)
