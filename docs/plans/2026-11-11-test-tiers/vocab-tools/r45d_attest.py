"""HANDOFF 4.2 / 10.5 pass 3, continued: "attest" where it names the act.

"Attest" names seven things (VOCABULARY.md 3). This file moves only S6, the
acceptance itself: "attested text", "attestation scope / depth / model /
window / ledger / cards", "post-attestation amendment", "owes an
attestation", "re-opens attestation", "about to attest", "unattested drift",
`_attestation_cards`, `_unattested_rows`, the open-items card id `<row>-attest`
and its format keys, and two test names. Anchored on phrases, never the bare
word, because the same files also name:

- S1, the passed-checks record (`integrate.py attest`, "bar attestation",
  "a verified review attestation", "an unattested tip"): 10.6. The modules
  built on it are SKIPPED whole.
- S3, the method (`Vouch`): "critique or attestation", "an attestation, a
  demonstration", "gate-attested". Ruled and swept earlier; a few leftovers
  are listed in HANDOFF, not moved here.
- Retired names, spelled as they were: the SN-029 ledger (`attestations.csv`,
  `attestation_findings`, ...), `_attested_baseline`, the stamp
  `attestation-baseline`, the need fields `attestation`/`amended`, the
  `RE-ATTESTATION PENDING` convention. The two ratchet files are history and
  are skipped.
- S7, a worker's claim ("a ticked box IS an attestation"): hand edits (h45d).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

# Built on the passed-checks record (S1), or history: not this pass.
S1_FILES = [
    "project-trajectory/scripts/integrate.py",
    "project-trajectory/scripts/kitlib/verdict.py",
    "project-trajectory/scripts/kitlib/station.py",
    "project-trajectory/scripts/kitlib/red_mark.py",
    "project-trajectory/scripts/review_brief.py",
    "project-trajectory/scripts/review_set.py",
    "project-trajectory/scripts/agent_loop.py",
    "project-trajectory/scripts/agent_brief.py",
    "project-trajectory/scripts/agent_common.py",
    "project-trajectory/prompts/worker.template.md",
    "project-trajectory/process.toml.template",
    "project-trajectory/stack.ini.template",
    "docs/stack.ini",
    "docs/runtime-flows.md",
    "*/skills/coordinator-cycle/SKILL.md",
    "tests/conftest.py",
    "tests/integrate_fixtures.py",
    "tests/golden/worker-prompt-one-row.txt",
    "tests/test_integrate_*.py",
    "tests/test_bar_attestation.py",
    "tests/test_agent_loop_review_gate.py",
    "tests/test_agent_loop_worker.py",
    "tests/test_verdict_record.py",
    "tests/test_review_brief*.py",
    "tests/test_red_mark*.py",
    "tests/test_hooks_on_*.py",
    "tests/test_check_smoke_budget.py",
    "tests/test_prompts.py",
    "tests/test_traj_panels.py",
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
]

SKIP = RECORDS + HAND_ONLY + S1_FILES + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
]

TOKENS = {
    "_attestation_cards": "_acceptance_cards",
    "_unattested_rows": "_unaccepted_rows",
    "test_empty_attestation_state_names_only_what_it_checked": "test_empty_acceptance_state_names_only_what_it_checked",
    "test_an_operator_held_tier_surfaces_an_attestation_instead_of_dispatching": "test_an_operator_held_tier_surfaces_an_acceptance_row_instead_of_dispatching",
}

# A pass-1 leftover: `re_attestation` was a part, its plural was not.
PARTS = {
    "re_attestations": "re_acceptances",
}

_NOUNS = (
    "text|prose|content|cells?|rows?|row's|spine|requirement|need|baseline|SR|LLR|"
    "chain|premises|requirement text"
)

REGEX = [
    # the act's past participle on what it took as agreed
    (r"\battested (" + _NOUNS + r")\b", r"accepted \1"),
    (r"\bATTESTED (" + _NOUNS + r")\b", r"ACCEPTED \1"),
    (r"\balready-attested\b", "already-accepted"),
    (r"\bseparately attested\b", "separately accepted"),
    (r"\b(the operator|nothing) attested\b", r"\1 accepted"),
    (r"\bafter it was attested\b", "after it was accepted"),
    (r"\bwhich cells are attested\b", "which cells are accepted"),
    (r"\battested, BOM'd\b", "accepted, BOM'd"),
    (r"\bBOM'd attested\b", "BOM'd accepted"),
    # the act's noun
    (r"\bpost-attestation\b", "post-acceptance"),
    (r"\b([Aa]ttestation|ATTESTATION) (scope|depth|regime|model|window|ledger|cards?|surface|brief|briefs|quotes|carve-out|STATE)\b",
     lambda m: {"attestation": "acceptance", "Attestation": "Acceptance", "ATTESTATION": "ACCEPTANCE"}[m[1]] + " " + m[2]),
    (r"\battestation-(quoting|card)\b", r"acceptance-\1"),
    (r"\*attestation\* depth\b", "*acceptance* depth"),
    (r"\b(owes|owe|keeps) (an|its) attestation\b", r"\1 \2 acceptance"),
    (r"\bowes attestation\b", "owes acceptance"),
    (r"\bre-opens (no |the requirement's |the row's )?attestation\b", r"re-opens \1acceptance"),
    (r"\boverrides attestation\b", "overrides acceptance"),
    (r"\bescapes attestation\b", "escapes acceptance"),
    (r"\bsecond attestation\b", "second acceptance"),
    (r"\bwrongly-kept attestation\b", "wrongly-kept acceptance"),
    (r"\brow's attestation is now\b", "row's acceptance is now"),
    (r"\ba pending attestation\b", "a pending acceptance"),
    (r"\bbroken attestation\b", "broken acceptance"),
    (r"\b([Oo])perator attestation\b", r"\1perator acceptance"),
    (r"\brulings, attestations and\b", "rulings, acceptances and"),
    (r"\b(past|an) attestation (makes|is never)\b", r"\1 acceptance \2"),
    (r"\brewriting an attestation\b", "rewriting an acceptance"),
    (r"\bre-word a past attestation\b", "re-word a past acceptance"),
    (r"\bnever-reword rule for attestations\b", "never-reword rule for acceptances"),
    (r"\bthey are attestations\b", "they are acceptances"),
    (r"\battestations are not re-worded\b", "acceptances are not re-worded"),
    (r"\ban attestation asks\b", "an acceptance asks"),
    (r"\ban attestation, traced ones\b", "an acceptance, traced ones"),
    (r"\bmoment of an ATTESTATION, and attestation happens\b", "moment of an ACCEPTANCE, and acceptance happens"),
    (r"\battestation must not carry\b", "acceptance must not carry"),
    (r"\bthe attestation cards\b", "the acceptance cards"),
    (r"\bthe attestation/acceptance page\b", "the acceptance page"),
    (r"\boperator-held attestation still drains\b", "operator-held acceptance row still drains"),
    (r"\bnon-attesting\b", "outside acceptance"),
    # the act's verb
    (r"\babout to attest\b", "about to accept"),
    (r"\bABOUT TO ATTEST\b", "ABOUT TO ACCEPT"),
    (r"\battest FROM\b", "accept FROM"),
    (r"\bthat attest most often\b", "that accept most often"),
    (r"\bpermitted to attest\b", "permitted to accept"),
    (r"\battesting — an operator blessing\b", "accepting — an operator blessing"),
    # text no act took as agreed
    (r"\bunattested (drift|row|rows|change)\b", r"unaccepted \1"),
    (r"\bdrifts unattested\b", "drifts unaccepted"),
    (r"\bcopy unattested\b", "copy unaccepted"),
    (r"\bEVERY unattested\b", "EVERY unaccepted"),
    (r"\babsorbed an unattes", "absorbed an unaccep"),
    # the open-items card: its id, the page's format keys and their values
    (r'-attest"', '-accept"'),
    (r'"attest": len\(model\)', '"accept": len(model)'),
    (r"\{attest\} SR chain", "{accept} SR chain"),
    (r"\{attestations\}", "{acceptances}"),
    (r"\battestations=\(", "acceptances=("),
    (r"\bunattested = _unaccepted_rows", "unaccepted = _unaccepted_rows"),
    (r"\bin unattested if\b", "in unaccepted if"),
    (r"\bif scope else unattested\b", "if scope else unaccepted"),
]

PROTECT = list(_PROTECT) + [
    # retired names and stamps, spelled as they were
    r"_attested_baseline",
    r"attestation-baseline",
    r"attestations?\.csv",
    r"test_attestation_(?:digest|ledger)",
    r"SN-029's separate attestation ledger",
    r"RE-ATTESTATION[ -]PENDING",
    r"`(?:kind|attestation|amended)`(?:/`(?:attestation|amended)`)*",
    r"`ruling` / `retired` / `(?:attestation|amended)` / `(?:attestation|amended)`",
    r"record each attestation",
    r"no `attestation`, no `amended`",
    # the method (S3): ruled earlier, leftovers listed in HANDOFF
    r"critique or attestation",
    r"an attestation, a demonstration",
    r"a rubric or an attestation",
    r"gate-attested",
    # the passed-checks record (S1) where it sits in a shared file
    r"unattested (?:tip|owed round)",
    r"[Uu]nattested review",
    r"\battest(?:ation)? (?:route|step|command|commit)",
]
