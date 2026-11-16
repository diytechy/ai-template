"""HANDOFF 4.2 / 10.5 pass 3: approve becomes accept.

The act that takes a row as agreed, its brief, its flags and every name built
on the word: `approval` -> `acceptance`, `approve` -> `accept`, `approves` ->
`accepts`, `approving` -> `accepting`, `approved` -> `accepted`, `approver`
-> `acceptor`, `unapproved` -> `unaccepted`, in snake, kebab, camel-free
names and prose alike (PARTS: underscore and hyphen are edges). Both the old
and the new word begin with a vowel, so articles hold. `--approves` becomes
`--accepts`, `trace.py --approve` becomes `--accept`, the check steps
`approval-fresh` / `approval-immutable` become `acceptance-fresh` /
`acceptance-immutable`, the in-memory act kind "approve" becomes "accept".

The adjudicator's ruling on a row in a first-acceptance sitting is the act,
and its verdict word moves: `- [APPROVE]`, `OUTCOME: APPROVE`,
`APPROVE|RETURN`, `_AUTHORIZING`'s `("APPROVE",)` become ACCEPT (D12).

NOT in this pass:
- D12: a reviewer's verdict keeps APPROVE. The modules that handle review
  rounds are SKIPPED whole and read by hand afterwards (REVIEW_FILES); in
  the other files every rule on the uppercase word names the first-acceptance
  grammar, never `VERDICT: APPROVE`.
- Pass 4: the status `Approved`, the constant `APPROVED`, every quoted
  "approved" string (the status read case-insensitively, the ledger key and
  the cell class: all three become "accepted" together), `last_approved`.
  PARTS here is lower-case and capitalised words other than `Approved`.
- Records and stored values a current script reads: the legacy gate-policy
  value `single-approve` (read by the legacy dial readers until D11), the
  retired dial key `human_approval_through` (read by the legacy readers and
  the migrator), the observation records under docs/test/observations.
- The passed-checks record (10.6) and every "attest": r45d_attest.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

# The modules that handle review rounds and their tests (D12): read by hand.
REVIEW_FILES = [
    "project-trajectory/scripts/kitlib/verdict.py",
    "project-trajectory/scripts/score_reviews.py",
    "project-trajectory/scripts/plan_round.py",
    "project-trajectory/scripts/plan_runner.py",
    "project-trajectory/scripts/plan_gate.py",
    "project-trajectory/scripts/review_brief.py",
    "project-trajectory/scripts/agent_route.py",
    "project-trajectory/hooks/pre-push",
    "project-trajectory/prompts/reviewer.template.md",
    "project-trajectory/prompts/dual-plan-critic.template.md",
    "project-trajectory/prompts/critique.template.md",
    "tests/test_verdict_record.py",
    "tests/test_score_reviews.py",
    "tests/test_plan_round.py",
    "tests/test_plan_gate.py",
    "tests/test_dual_plan_round.py",
    "tests/test_pre_push_hook.py",
    "tests/test_agent_loop_review.py",
    "tests/test_agent_loop_review_gate.py",
    "tests/test_agent_loop_critique.py",
    "tests/test_review_brief.py",
    "tests/test_review_brief_git.py",
    "tests/test_agent_route.py",
    "tests/test_agent_loop_routing.py",
    "tests/test_verdict_rollup_render.py",
    "tests/test_handback.py",
    # the loop's review rounds ("review round approved", "page/approve");
    # its two act-sense lines are hand edits
    "project-trajectory/scripts/agent_loop.py",
]

# Skills whose "approve" is a person's or a critic's, not the act: a user
# approving a plan (antidote) and a vision critic's convergence on two
# consecutive APPROVEs (D12).
OTHER_APPROVALS = [
    "*/skills/antidote/SKILL.md",
    "*/skills/llm-vision-convergence-loop/SKILL.md",
]

SKIP = RECORDS + HAND_ONLY + REVIEW_FILES + OTHER_APPROVALS + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
]

PARTS = {
    "approvals": "acceptances",
    "approval": "acceptance",
    "approves": "accepts",
    "approve": "accept",
    "approving": "accepting",
    "approvers": "acceptors",
    "approver": "acceptor",
    "approved": "accepted",
    "unapproved": "unaccepted",
    "reapproved": "reaccepted",
    "Approvals": "Acceptances",
    "Approval": "Acceptance",
    "Approves": "Accepts",
    "Approve": "Accept",
    "Approving": "Accepting",
    "Approver": "Acceptor",
    "APPROVALS": "ACCEPTANCES",
    "APPROVAL": "ACCEPTANCE",
    "APPROVING": "ACCEPTING",
}

# The adjudicator's ruling in the first-acceptance grammar (D12): every form
# below names that grammar, never the reviewer's `VERDICT: APPROVE`.
REGEX = [
    (r"- \[APPROVE\]", "- [ACCEPT]"),
    (r"\[APPROVE\|RETURN\]", "[ACCEPT|RETURN]"),
    (r"\bAPPROVE\|RETURN\b", "ACCEPT|RETURN"),
    (r"OUTCOME: APPROVE\b", "OUTCOME: ACCEPT"),
    (r'\("APPROVE", "RETURN"\)', '("ACCEPT", "RETURN")'),
    (r'"first-acceptance": \("APPROVE",\)', '"first-acceptance": ("ACCEPT",)'),
    (r'"first-acceptance": "APPROVE"', '"first-acceptance": "ACCEPT"'),
    (r'ruling == "APPROVE"', 'ruling == "ACCEPT"'),
    (r'\("APPROVE", "CLARITY", "MEANING"\)', '("ACCEPT", "CLARITY", "MEANING")'),
    (r'\{"MEANING", "CLARITY", "APPROVE", "RETURN"\}', '{"MEANING", "CLARITY", "ACCEPT", "RETURN"}'),
    (r'elif ruling == "APPROVE"', 'elif ruling == "ACCEPT"'),
    (r"\b([Aa]n) APPROVE row", r"\1 ACCEPT row"),
    (r"\bAPPROVE rows\b", "ACCEPT rows"),
    (r"\bAPPROVE flips\b", "ACCEPT flips"),
    (r"\bAPPROVE OR RETURN\b", "ACCEPT OR RETURN"),
    (r"\b(ruled `?)APPROVE\b", r"\1ACCEPT"),
    (r"\bruling APPROVE\b", "ruling ACCEPT"),
    (r"\bsection APPROVE\b", "section ACCEPT"),
    (r"\bAPPROVE by changing\b", "ACCEPT by changing"),
    (r"\byou APPROVE\b", "you ACCEPT"),
    (r"\bfirst acceptance's APPROVE/RETURN\b", "first acceptance's ACCEPT/RETURN"),
    (r"\b([Aa]n) APPROVE ruling\b", r"\1 ACCEPT ruling"),
]

PROTECT = list(_PROTECT) + [
    # review directories cited by name: docs/reviews/wi-818-owner-verdict
    r"\bwi-?\d+[a-z]?-[A-Za-z0-9_-]+",
    # pass 4: the record's directory, its README template and the status read
    # case-insensitively, the ledger key and the cell class
    r"last[_-]approved",
    r"(?<=[\"'])approved(?=[\"'])",
    # stored values a legacy reader still reads (until D11)
    r"human_approval_through",
    r"single[-_]approv\w*",
    # retired names, spelled as they were: two a test asserts are gone, two
    # named in history notes
    r"(?<![A-Za-z0-9_])(?:_?APPROVAL_RUNG(?:_OF)?|LEGACY_APPROVAL_LEVEL|newest_approval_brief)(?![A-Za-z0-9_])",
    # tests about a REVIEWER's or a critic's verdict (D12), and the evidence
    # cells that cite them
    r"test_a_narrow_approve_at_the_tip_does_not_raise_the_unchanged_rework_page",
    r"test_critique_ratchet_silent_when_verdict_approves",
    r"test_approve_proceeds_and_reviewer_sees_full_range",
    r"test_approved_plans_skip_revision_and_coverage2",
    r"test_routingstate_record_critique_verdict_approved_resets_scope",
    r"test_critique_unparseable_verdict_not_treated_as_approved",
    r"test_a_minor_only_refusal_routes_as_an_approve",
    # pass 4, continued: the ledger key and the cell class in backticks, the
    # ledger key as a TOML key in fixtures and in the prose naming the keys,
    # the validator's labels for it, and the lowercase status value in CSV
    # interface fixtures
    r"(?<=`)approved(?=`)",
    # (TOML fixtures write it after an escaped newline or a quote; prose names
    # it after a comma; a Python variable of the same name is never matched)
    r"(?:(?<=\\n)|(?<=')|(?<=, ))approved(?= = \[)",
    r"(?<=date, )approved(?=, reattested)",
    r"approved (?:not a list|holds a number|missing)",
    r"(?<=,)approved(?=,)",
    # the retired off-spine maturity column `Approval` (WI-442, now `Status`):
    # history notes, and two tests asserting the key never comes back
    r"`[Aa]pproval`",
    r"(?<=[\"'])approval(?=[\"'])",
    r"(?<=`)[Aa]pproval(?=\s*==?\s*\")",
    r"(?<=, )Approval(?==\")",
    r"[Aa]pproval migration",
    r"test_no_surface_names_the_retired_approval_column_as_current",
    # a census test's patterns hunting writes of the status and the retired
    # column (pass 4 reconsiders the value)
    r"status\|approval\|state",
    r"\(\?:approved\|verified",
    # a baseline is "a debt statement, not an approval" (an endorsement, not
    # the act); the phrase is also the stored header of docs/complexity-baseline
    r"(?i:debt statement,? not an approval)",
    r"debt, not an approval",
    r"not an approval, as the baseline",
    # a REVIEWER's or a critic's approval (D12), and a forge's PR approvals
    r"review round approved",
    r"rounds had approved",
    r"whose approve yields",
    r"narrow approve",
    r"critique approval",
    r"reviewer will approve",
    r"honestly-approved",
    r"approved lane",
    r"approved perceptual stamp",
    r'"approve"/"critique"',
    r'"verdict"/"approve"',
    r"watched approving",
    r"unapproved external review copy",
    r"non-approval",
    r"cannot create an approval",
    r"recorded the approval",
    r"bias toward approving",
    r"second-approver-identity",
    r"approval-required",
    r"does not approve, its BLOCKER",
    r"before approving\)",
    r"approval buried the station",
    r"reviewer(?:'s recorded)? verdict(?:\*\*)? approves",
    # a person approving a decision or an adopter's own register, not the act
    r"never to approve",
    r"approved deviation register",
    # dated record file names split over a line break
    r"[A-Za-z0-9_-]*approv[A-Za-z0-9_-]*\.md",
]
