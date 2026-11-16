"""HANDOFF 4.3 / 10.4: "owner" becomes "operator" where it names the role.

"Owner" names several things (VOCABULARY.md 4). Only sense 1, the role in
charge, moves. The others keep the word: an interface row's providing side
(the `owner` key, `Owner` column, `seam_owner`, `owner_files`, "the owner is
the providing thing"), a lock, lease-holder or claim holder, the single home
of a rule, the def that owns a docstring, the accountable hat (`owner_hat`,
`-> @owner`), `OWNER/REPO`, `CODEOWNERS`, a debt owner.

THE RULES ARE ANCHORED, NOT A WORD SWAP. Code names a variable `owner` in
several senses (`owner = ends[0]`, `for owner, name in ...`), so the bare
word is never rewritten. Prose is reached through its context: "the owner",
"an owner", "owner's", "owner ruling", "owner directive", and the nouns the
role governs ("owner queue", "owner surface", ...). Whatever bare "owner" is
left is listed after the run and read by hand.

The interface files are SKIPPED whole: there "the owner" is nearly always the
providing side. They are read by hand for role uses afterwards.

The decisions key: `owner = "confirmed" | "overruled"` becomes `operator =`
in code, templates and tests; the stored records under docs/decisions are the
migrator's, and their prose keeps its words.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

INTERFACE_FILES = [
    "docs/requirements/interfaces.toml",
    "project-trajectory/scripts/trajectory_arch.py",
    "project-trajectory/scripts/gen_arch_map.py",
    "project-trajectory/scripts/kitlib/spine.py",
    "project-trajectory/scripts/spine_carrier.py",
    "project-trajectory/scripts/migrate_carrier.py",
    "project-trajectory/scripts/rendering/traj_views.py",
    "project-trajectory/INTERFACES.template.md",
    "project-trajectory/registries/interfaces.template.toml",
    "project-trajectory/MULTI_REPO.md",
    "tests/test_trace_interfaces.py",
    "tests/test_migrate_carrier.py",
    "tests/test_gen_arch_map.py",
    "tests/test_interface_owner_reach.py",
    "tests/test_seam_resolution.py",
]

SKIP = RECORDS + HAND_ONLY + INTERFACE_FILES + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    # its header is hand-edited: it still says it holds a person's notes
    "project-trajectory/OWNER_SCRATCHPAD.template.md",
    "project-trajectory/LICENSE",
]

TOKENS = {
    "OWNER_SCRATCHPAD": "OPERATOR_SCRATCHPAD",
    "OWNER_ONLY_PATHS": "OPERATOR_ONLY_PATHS",
    "OWNER_PROMPT": "OPERATOR_PROMPT",
    "OWNER_KEY": "OPERATOR_KEY",
    "OWNER_VALUES": "OPERATOR_VALUES",
    "owner_state": "operator_state",
    "_owner_findings": "_operator_findings",
    "owner_cards": "operator_cards",
    "owner_card": "operator_card",
    "OWNER_WINDOW": "OPERATOR_WINDOW",
    "OWNER_EDITS": "OPERATOR_EDITS",
    "OWNER_STATUS": "OPERATOR_STATUS",
    "OWNER_DIALS": "OPERATOR_DIALS",
    "leave_owner_edits": "leave_operator_edits",
    "assert_owner_edits_untouched": "assert_operator_edits_untouched",
    "OwnerDraftRetitle": "OperatorDraftRetitle",
    "d002_owner": "d002_operator",
    "_no_owner_token_file": "_no_operator_token_file",
    "_no_owner_account_homes": "_no_operator_account_homes",
    "_one_owner_row": "_one_operator_row",
    "_owner_rows": "_operator_rows",
    "_assert_no_owner_row": "_assert_no_operator_row",
    "owner_content": "operator_content",
    "RETURN-TO-DRAFT-that-pages-the-owner": "RETURN-TO-DRAFT-that-pages-the-operator",
    # test names about the role
    "test_an_owner_ruling_binding_the_digest_releases_and_an_unseen_one_does_not":
        "test_an_operator_ruling_binding_the_digest_releases_and_an_unseen_one_does_not",
    "test_a_verdict_reattestation_stays_listed_on_the_owner_surface":
        "test_a_verdict_reattestation_stays_listed_on_the_operator_surface",
    "test_only_the_owners_recorded_clear_or_the_successor_unlatches":
        "test_only_the_operators_recorded_clear_or_the_successor_unlatches",
    "test_owner_cards_is_pending_items_minus_the_pause":
        "test_operator_cards_is_pending_items_minus_the_pause",
    "test_reopening_the_same_session_with_both_drains_needs_the_owners_clear":
        "test_reopening_the_same_session_with_both_drains_needs_the_operators_clear",
    "test_the_owner_surface_reads_the_model_not_the_render_facade":
        "test_the_operator_surface_reads_the_model_not_the_render_facade",
    "test_the_owners_brief_and_open_items_name_each_registrys_own_copy":
        "test_the_operators_brief_and_open_items_name_each_registrys_own_copy",
    "test_the_owners_release_frees_the_lease_and_is_recorded":
        "test_the_operators_release_frees_the_lease_and_is_recorded",
    "test_a_declared_deferral_must_name_a_row_the_owner_has_still_to_rule":
        "test_a_declared_deferral_must_name_a_row_the_operator_has_still_to_rule",
    "test_a_dial_releasing_every_rung_leaves_the_owner_a_stated_empty_ask":
        "test_a_dial_releasing_every_rung_leaves_the_operator_a_stated_empty_ask",
    "test_a_dirty_owner_scratchpad_does_not_stop_the_drive":
        "test_a_dirty_operator_scratchpad_does_not_stop_the_drive",
    "test_a_held_meaning_verdict_mints_one_owner_row_and_one_pending_item":
        "test_a_held_meaning_verdict_mints_one_operator_row_and_one_pending_item",
    "test_an_owner_edit_while_the_regeneration_is_blocked_survives_and_refuses":
        "test_an_operator_edit_while_the_regeneration_is_blocked_survives_and_refuses",
    "test_clarity_or_a_released_rung_mints_no_owner_row":
        "test_clarity_or_a_released_rung_mints_no_operator_row",
    "test_node_adopter_upgrade_preserves_populated_owner_content":
        "test_node_adopter_upgrade_preserves_populated_operator_content",
    "test_owner_scratchpad_dirty_at_start_injects_nothing":
        "test_operator_scratchpad_dirty_at_start_injects_nothing",
    "test_scaffolds_owner_scratchpad": "test_scaffolds_operator_scratchpad",
    "test_substantive_dirty_drops_owner_scratchpad":
        "test_substantive_dirty_drops_operator_scratchpad",
    "test_the_claim_never_rewrites_a_dirty_owner_scratchpad_naming_its_spec":
        "test_the_claim_never_rewrites_a_dirty_operator_scratchpad_naming_its_spec",
    "test_the_merge_slot_reads_past_a_dirty_owner_scratchpad":
        "test_the_merge_slot_reads_past_a_dirty_operator_scratchpad",
    "test_the_owner_act_is_never_listed_as_a_sessions_own":
        "test_the_operator_act_is_never_listed_as_a_sessions_own",
    "test_the_owners_scratchpad_is_never_planned_or_rewritten":
        "test_the_operators_scratchpad_is_never_planned_or_rewritten",
    "test_the_shipped_template_entry_leaves_the_owner_key_unset":
        "test_the_shipped_template_entry_leaves_the_operator_key_unset",
    "test_worker_endstate_owner_scratchpad_stays_done":
        "test_worker_endstate_operator_scratchpad_stays_done",
}

# Kebab compounds of the role (hyphen and underscore are edges).
PARTS = {
    "owner-held": "operator-held",
    "Owner-held": "Operator-held",
    "owner-ruled": "operator-ruled",
    "owner-only": "operator-only",
    "Owner-only": "Operator-only",
    "Owner-reserved": "Operator-reserved",
    "owner-reserved": "operator-reserved",
    "pending-owner-actions": "pending-operator-actions",
    "PENDING-OWNER-ACTIONS": "PENDING-OPERATOR-ACTIONS",
    "pending-owner-action": "pending-operator-action",
    "Pending-owner-action": "Pending-operator-action",
    "pending-owner": "pending-operator",
    "owner-owed": "operator-owed",
    "owner-confirmed": "operator-confirmed",
    "owner-overruled": "operator-overruled",
    "owner-facing": "operator-facing",
    "owner-review": "operator-review",
    "owner-decision": "operator-decision",
    "owner-verdict": "operator-verdict",
    "owner-approved": "operator-accepted",
    "owner-attested": "operator-accepted",
    "owner-accepted": "operator-accepted",
    "owner-authored": "operator-authored",
    "owner-visible": "operator-visible",
    "owner-editing": "operator-editing",
    "owner-edited": "operator-edited",
    "owner-driven": "operator-driven",
    "owner-directed": "operator-directed",
    "owner-triaged": "operator-triaged",
    "Owner-raised": "Operator-raised",
    "owner-gated": "operator-gated",
    "owner-registry": "operator-registry",
    "owner-cleanup": "operator-cleanup",
    "nowhere-owner": "nowhere-operator",
}

# Nouns the role governs: "owner X" -> "operator X".
_NOUNS = (
    "rulings?|directives?|direction|decisions?|verdicts?|queue|surfaces?|views?|acts?|"
    "rows?|looks?|gates?|asks?|cards?|signatures?|registry|sections?|approvals?|"
    "sittings?|reads?|edits?|notes|scratchpad|feedback|confirmation|overrule|"
    "blessing|signing|sign-off|time|attention|pages?|page|brief|briefs|item|items|"
    "reviews?|outcome|key|line|account|token|home|work|commits?|draft|clear|release"
)

REGEX = [
    # the decisions key, its value literal and its readers
    (r'OPERATOR_KEY = "owner"', 'OPERATOR_KEY = "operator"'),
    (r'\bowner = "(confirmed|overruled)"', r'operator = "\1"'),
    (r'"owner": entry\.get\(OPERATOR_KEY\)', '"operator": entry.get(OPERATOR_KEY)'),
    (r'entry\["owner"\]', 'entry["operator"]'),
    (r'\["D-001"\]\["owner"\]', '["D-001"]["operator"]'),
    (r'class="pill">owner = ', 'class="pill">operator = '),
    (r'\\nowner = "(confirmed|overruled)"', r'\\noperator = "\1"'),
    (r"\bowner#cleanup", "operator#cleanup"),
    # the decisions key named in prose
    (r"`owner` key", "`operator` key"),
    (r"\bowner key\b", "operator key"),
    (r"its `owner` says", "its `operator` says"),
    (r"whatever `owner` says", "whatever `operator` says"),
    (r"carry\s+`owner`", "carry `operator`"),
    (r"(an absent or unrecognized|an unrecognized|beside an) `owner`", r"\1 `operator`"),
    (r"`owner` the raw value", "`operator` the raw value"),
    (r"\bThe owner's verdict\b", "The operator's verdict"),
    # a brief marker and a minted title
    (r"HELD FOR THE OWNER", "HELD FOR THE OPERATOR"),
    (r"\bowner act: ", "operator act: "),
    # citations: "(owner, 2026-10-04)", "owner ruling D-8"
    (r"\(owner, (?=20\d\d)", "(operator, "),
    # prose only: a call such as `norm_module(owner)` follows a name
    (r"(?<![\w.])\(owner\)", "(operator)"),
    (r"\b([Oo])wner (" + _NOUNS + r")\b", lambda m: ("O" if m[1] == "O" else "o") + "perator " + m[2]),
    (r"\bOWNER (RULING|DIRECTIVE|ACT|SURFACE|QUEUE|VIEW)", r"OPERATOR \1"),
    # articles and possessives
    (r"\b(the|The|an|An) (owners'|owners|owner's|owner)(?![-\w])", None),
    (r"\b(THE|AN) (OWNER'S|OWNERS|OWNER)(?![-\w])", None),
    (r"\bowner's\b", "operator's"),
    (r"\bOwner's\b", "Operator's"),
    (r"\bowners'", "operators'"),
    (r"\bOWNER'S\b", "OPERATOR'S"),
]

_SWAP = {
    "owner": "operator", "owners": "operators", "owner's": "operator's",
    "owners'": "operators'", "OWNER": "OPERATOR", "OWNERS": "OPERATORS",
    "OWNER'S": "OPERATOR'S",
}


def _article(m):
    return "{} {}".format(m[1], _SWAP[m[2]])


# Fill the two article rules with the function above.
REGEX = [
    (pat, _article) if repl is None else (pat, repl) for pat, repl in REGEX
]

# The decisions key in fixtures written through a format string: only these two
# files build decisions entries that way (the same shape builds interface rows
# in traj_fixtures.py and test_assumption_gate.py, which keep `owner`).
SCOPED = [
    ("tests/test_decision_overrule.py", r'\bowner = "\{\}"', 'operator = "{}"'),
    ("tests/test_decisions_to_review.py", r"\bowner = \{\}", "operator = {}"),
    ("tests/test_decisions_to_review.py", r"\\nowner =", r"\\noperator ="),
]

# "Owner" in a sense that stays, outside the skipped interface files.
KEEP = [
    # an interface row's providing side
    r"[Oo]wner is the providing",
    r"[Oo]wner(?:'s)? (?:names?|naming|named|cell|column|endpoint|side|module|path)\b",
    r"`[Oo]wner` (?:is the providing|\(a path)",
    r'\bowner = "(?!confirmed"|overruled"|\{\}")',
    # found reading the first dry run: the interface sense in prose
    r"lives in the owner's",
    r"owner's own header",
    r"another owner's",
    r"What the owner\s*$",
    r"the owner and its far side",
    r"an owner, its far side",
    r"into the owner on a",
    r"module owner",
    r"the owner's contract",
    r"[Tt]he owner is the (?:one|ONE)\b",
    r"an owner the tree cannot resolve",
    r"[Aa]n owner that declares",
    r"a source that is not the owner",
    r"CSV owner's",
    r"the owner is one THING",
    r"the owner is the row's own cell",
    r"read the owner off the row",
    r"the owner is not `Req-Refs`",
    r"Markdown owner's",
    # a module or function that owns something, and a gate's owner
    r"gate had an owner",
    r"single-owner",
    r"the owner never decides what",
    r"Its owner's parser",
    r"cannot be imported here — the owner",
    r"\"Owner\"",
    r"Owner=",
    r"(?:one|ONE|every|each|which|whose|that) [Oo]wner\b",
    r"\b(?:an|the) owner (?:of the wrong|that|reach|reaches|reached|naming|named|should|defines|plugs|emits|endpoint)",
    r"into the owner's surface",
    r"the owner's `Contract",
    r"the owner's current version",
    r"(?:the|an) owner's header",
    r"(?:INTO|through|references) the owner\b",
    r"names that owner",
    r"(?:id|module)-shaped owner",
    r"matches no owner",
    r"OWNER, ITS CONSUMERS",
    r"the row is one owner",
    r"owner-local",
    r"file[- ]owners?",
    # a holder, a single home, the owning def, the accountable hat, external
    r"(?:lock|lease|claim|debt|code|registry|roster|rule|seam)'?s? owners?",
    r"owner of (?:the|a|that|this|its) (?:lock|lease|claim|file|rule|module|def|docstring|function)",
    r"owner of (?:another|the other) (?:system|repo)",
    r"\bits owner\b",
    r"\btheir owners?\b",
    r"-> @owner",
    r"OWNER/REPO",
    r"CODEOWNERS",
    r"[Oo]wner hat",
    r"owner_hat",
    r"session-owner",
    r"owner-feedback-20\d\d-\d\d-\d\d",
    r"\bwi-?\d+[a-z]?-[A-Za-z0-9_-]+",  # directory and ref names (wi-818-owner-verdict)
    r"#[a-z0-9-]*owner[a-z0-9-]*",  # link fragments
]

PROTECT = list(_PROTECT) + KEEP
