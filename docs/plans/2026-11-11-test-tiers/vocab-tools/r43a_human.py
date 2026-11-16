"""HANDOFF 4.3 / 10.4: "human" becomes "operator" where it names the role.

The role: who holds a rung, approves, signs, rules, consents, publishes, is
paged or stopped for, resumes a run, owes an act, blesses a text.

Kept (PROTECT, or a whole file in SKIP): "human" meaning a person as such:
a reader ("rendered for a human", "readable for humans"), an observer for the
human verification methods and the release checklist (S4), an audience
beside agents ("AI agents and humans"), nobody present ("3am with no human",
"no human curating"), a person noticing or typing by hand, the log's `Human`
column, the `Vouch` definition, the research notes in docs/knowledge, and
every hyphenated compound not listed in PARTS (human-readable, human-made,
human-verified, human-SR, human-facing, human-reviewed, ...).

Special phrases (VOCABULARY.md 5, S1b): "the human path" and "a human trunk
commit" mean a judged commit as against a scripted one, not the operator, so
they become "the reviewed-commit path" and "a trunk commit". "The owner's
final read is the human's" would read "the operator's final read is the
operator's", so it becomes "the final read is the operator's".

The push value `human` becomes `operator` everywhere it is written; its
meaning widens (trap 14) and the prose around it is reworded by hand.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    # hand-edited in the owner pass: its header still says it holds a person's notes
    "project-trajectory/OWNER_SCRATCHPAD.template.md",
    # research notes about people and machines in general
    "docs/knowledge/decision-routing.md",
    "docs/knowledge/system-decomposition-methods.md",
    "docs/knowledge/traceability-enforcement.md",
    "docs/Inspiration.md",
    # the release checklist: every use is S4, a person exercising the product
    "project-trajectory/scripts/gen_release_checklist.py",
    "tests/test_gen_release_checklist.py",
    # the CI tiers mirror "the human moment": the harness a person runs
    "tests/test_ci_tier_declaration.py",
]

TOKENS = {
    "human_approves_spine": "operator_accepts_spine",
    "human_approves": "operator_accepts",
    "human_holds": "operator_holds",
    "human_held": "operator_held",
    "EXIT_NEEDS_HUMAN": "EXIT_NEEDS_OPERATOR",
    "page_human": "page_operator",
    "STACK_NEEDS_HUMAN": "STACK_NEEDS_OPERATOR",
    "_NEEDS_HUMAN_RE": "_NEEDS_OPERATOR_RE",
    "_needs_human_block": "_needs_operator_block",
    "_HUMAN_OWED": "_OPERATOR_OWED",
    "_HUMAN_OWED_HEAD": "_OPERATOR_OWED_HEAD",
    "human_anchor": "needs_anchor",
    "human_approval_registries": "operator_acceptance_registries",
    "HUMAN_APPROVAL_REGISTRIES": "OPERATOR_ACCEPTANCE_REGISTRIES",
    # test names
    "test_a_failed_stash_stops_for_a_human_and_redraws_nothing":
        "test_a_failed_stash_stops_for_the_operator_and_redraws_nothing",
    "test_critique_budget_exhaustion_pages_human":
        "test_critique_budget_exhaustion_pages_the_operator",
    "test_below_the_human_dial_a_NON_FLIPPABLE_row_is_NAMED_not_skipped":
        "test_below_the_operator_dial_a_NON_FLIPPABLE_row_is_NAMED_not_skipped",
    "test_push_policy_explicit_human_matches_default":
        "test_push_policy_explicit_operator_matches_default",
    "test_scaffold_push_policy_defaults_human":
        "test_scaffold_push_policy_defaults_operator",
    "test_two_top_tier_failures_page_the_human":
        "test_two_top_tier_failures_page_the_operator",
    "test_a_needs_human_worker_hands_back_and_the_run_keeps_going":
        "test_a_needs_operator_worker_hands_back_and_the_run_keeps_going",
}

# Inside longer names too (underscore and hyphen are edges): test names such as
# test_an_unreadable_stage_is_human_held, and the kebab forms in prose.
PARTS = {
    "a_human_held": "an_operator_held",
    "human_held": "operator_held",
    "human_approves": "operator_accepts",
    "human-held": "operator-held",
    "HUMAN-HELD": "OPERATOR-HELD",
    "NEEDS-HUMAN": "NEEDS-OPERATOR",
    "NEEDS_HUMAN": "NEEDS_OPERATOR",
    "PAGE-HUMAN": "PAGE-OPERATOR",
    "page-human": "page-operator",
    "page-the-human": "page-the-operator",
    "stop-needs-human": "stop-needs-operator",
    "needs-human": "needs-operator",
    "ask-the-human": "ask-the-operator",
    "human-owed": "operator-owed",
    "human-set": "operator-set",
    "human-only": "operator-only",
    "human-chosen": "operator-chosen",
    "human-pushed": "operator-pushed",
    "human-decision": "operator-decision",
    "human-launched": "operator-launched",
    "human-provided": "operator-provided",
}

_W = r"(?<![-_A-Za-z0-9])"
_E = r"(?![-_A-Za-z0-9])"

REGEX = [
    # fixed phrases first
    (r"the owner's final read is the human's", "the final read is the operator's"),
    (r"\b([Aa]) human trunk\b", r"\1 trunk"),
    (r"\bhuman trunk commit", "trunk commit"),
    (r"\b([Aa]) human reviewed-commit", r"\1 reviewed-commit"),
    (r"\bthe human reviewed-commit", "the reviewed-commit"),
    (r"THE HUMAN PATH", "THE REVIEWED-COMMIT PATH"),
    (r"\bthe HUMAN path", "the REVIEWED-COMMIT path"),
    (r"\bthe human path", "the reviewed-commit path"),
    (r"\bby human hand", "by the operator's hand"),
    (r"blocking on absent humans", "blocking on an absent operator"),
    (r"\*\*human owner only\*\*", "**operator only**"),
    (r"\bthe human owner's", "the operator's"),
    (r"\bthe human owner\b", "the operator"),
    (r"\bhuman owner\b", "operator"),
    (r"`needs human`", "`needs operator`"),
    (r"keeping human and delegated", "keeping the operator's own and delegated"),
    # "The owner's final read / stays human." (the owner pass drops "owner's")
    (r"\bstays human\.", "stays the operator's."),
    (r"approval stays human,", "approval stays a reviewed-commit act,"),
    # "Approval stays a human / reviewed-commit act": the S1b sense, split over lines
    (r"\b(stays a) human( ?\x22?)$", r"\1\2"),
    (r"\b([Aa]) human commit\b", r"\1 trunk commit"),
    # the word
    (_W + r"humans" + _E, "operators"),
    (_W + r"Humans" + _E, "Operators"),
    (_W + r"human" + _E, "operator"),
    (_W + r"Human" + _E, "Operator"),
    (_W + r"HUMAN" + _E, "OPERATOR"),
    # articles: "a human" -> "an operator", "a human-held" -> "an operator-held"
    (r"\b([Aa]) (?=operator|Operator|OPERATOR)", r"\1n "),
]

# "human" as a person: never rewritten.
KEEP = [
    # an audience beside agents and tools
    r"(?:AI )?agents? (?:and|or) humans?",
    r"[Hh]umans?,? (?:and|or) (?:different )?(?:AI )?(?:agents?|tools?|models?|launchers)",
    r"\((?:or|and) human\)",
    r"human or (?:model|tool)",
    r"A reader — human",
    r"[Cc]omment(?:ing)? for humans",
    r"readab\w* for humans",
    r"humans \*and\* agents",
    r"\bfor humans\b",
    r"human (?:\*\*)?front door",
    r"AI/human|human/AI|human/LLM|human/critic",
    r"[Hh]uman value",
    # observing, exercising the product, the release checklist (S4)
    r"(?:a |the )?human observ\w*",
    r"a human runs it and observes",
    r"human methods?",
    r"the human (?:\*\*)?release checklist",
    r"human release checklist",
    r"human (?:\*\*)?release checklist",
    r"budgets a human must tick off",
    r"reaches a human at DevStg-Release",
    r"budgets meet a human",
    r"a human's checklist",
    r"in-scope human items",
    # Vouch: a person's word
    r"recorded human judgement",
    r"\(human judgment, not a check\)",
    r"a human's judg(?:e)?ment, name",
    r"a human's judgement, name",
    r"only a human can confirm",
    # a reader
    r"(?:[Rr]endered|prose|stamp|text|output|courtesy) for a human",
    r"(?:a|the|ONE|one) (?:document|surface|sentence|bullet|warn|row) a human (?:reads|is scanning)",
    r"a human (?:reading|reads|would|is scanning|can cite|following it|can verify|can open|will see it|does)\b",
    r"(?:free )?prose(?: sections)? a human reads",
    r"bullet a human reads",
    r"human READING",
    r"HUMAN READING",
    r"human's reading",
    r"HUMAN'S reading",
    r"(?:entry|exception|correctly) to a human",
    r"reading, to a human",
    r"to a human while counting",
    r"a human string",
    r"a human `detail`",
    r"human sentence",
    r"arbitrary human text",
    r"something a human can open",
    r"a surface a human is expected to trust",
    r"HUMAN's reference",
    r"human and resolves against nothing",
    r"read by humans deciding",
    # nobody present
    r"with no human\b",
    r"no human (?:is watching|in the loop|curat\w+)",
    r"a human curating",
    r"no human curate",
    r"a human must hand-maintain",
    r"for a human to curate",
    # a person by hand
    r"a human noticing",
    r"a human types",
    r"A HUMAN WRITES",
    r"config a human edits?",
    r"asked a human to re-derive",
    r"the human Priority",
    r"a human states",
    r"a human sitting down",
    r"The human at the",
    r"what a \*\*?human\*\*? needs",
    r"meant a human\s*$",
    r"meant a human needs nothing",
    # the harness a person runs (SN-005)
    r"harness a human runs",
    r"(?:the|no) human moment",
    # the log's Human column and past records
    r"`Human`",
    r"\| Human \|",
    r"hats, Human\.",
    r"did a human actually attend",
    r"a named human certifying",
    r"a human certifying",
    r"NAMED HUMAN approving",
    r"W4 Human & adopter",
    # fixtures
    r"a human edited the record",
    r"record what a human approved",
    # found reading the first dry run
    r"human reviewer reading",
    r"periodic human reading",
    r"the human reader",
    r"the human bar",
    r"HUMAN bar",
    r"a human tick-off",
    r"a human merges them",
    r"summary a human genuinely wants to read",
    r"human half",
    r"human resume surface",
    r"^\s*humans, never a session's input",
    r"human scratch",
    r"how a human verifies",
    r"serves — humans",
    r"human sitting down",
    r"human inspection",
    r"human release\b",
    r"For the human owner only",
    r"authored to a human",
    r"a human should be reading",
    # the same senses, broken over a line end
    r"checkable and a human\s*$",
    r"config a human\s*$",
    r"human front\s*$",
    r"caught only by a human\s*$",
    r"^\s*human rather than by this suite",
]

PROTECT = list(_PROTECT) + KEEP
