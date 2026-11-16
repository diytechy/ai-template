"""HANDOFF 10.5 pass 3, hand edits after r45c_accept.py.

1. The review-round modules r45c skips whole (D12): only their act-sense
   lines move, read one by one. The first-acceptance grammar in
   kitlib/verdict.py is the adjudicator's ruling (ACCEPT); "the approval
   level" is the dial (acceptance level); "the operator's to approve" is the
   act. Everything else there is a reviewer's or a critic's APPROVE and stays.
2. Names those files share with renamed code: `_approval_act_refusal`
   (test_plan_gate) and the two tests named for "the approval level", one of
   them cited by an evidence cell the rules already renamed.
3. check_vocab's `ratif*` suggestions: its quoted "approval"/"approved" are
   protected in r45c (the retired column), so the table is finished here.
4. Wording: an article the old text already had wrong ("a approve brief"),
   "--accept accepts", and "an accepted ACCEPT verdict" (the §4.4 "recorded
   verdict" sense, missed then).
5. D12's glossary entry: **approve**, the reviewer's verdict.
"""

AGENT_LOOP = "project-trajectory/scripts/agent_loop.py"
AGENT_ROUTE = "project-trajectory/scripts/agent_route.py"
PLAN_ROUND = "project-trajectory/scripts/plan_round.py"
PLAN_RUNNER = "project-trajectory/scripts/plan_runner.py"
VERDICT = "project-trajectory/scripts/kitlib/verdict.py"
VOCAB = "project-trajectory/scripts/check_vocab.py"
GLOSSARY = "project-trajectory/GLOSSARY.md"

EDITS = [
    # 1. act-sense lines in the skipped review-round modules
    (AGENT_LOOP, "declaring how far an operator approves", "declaring how far an operator accepts"),
    (AGENT_LOOP, "    operator's to approve? `operator_held` answers it once;",
     "    operator's to accept? `operator_held` answers it once;"),
    (AGENT_ROUTE, "Is the tier in process still the operator's to approve (`operator_held`)",
     "Is the tier in process still the operator's to accept (`operator_held`)"),
    (AGENT_ROUTE, '"operator-held tier: surface the block for approval"',
     '"operator-held tier: surface the block for acceptance"'),
    (PLAN_ROUND, "    approval level (SN-029).", "    acceptance level (SN-029)."),
    (PLAN_RUNNER, "for the caller to map onto its approval level).", "for the caller to map onto its acceptance level)."),
    (PLAN_RUNNER, "the caller maps it onto the declared approval level's failure semantics",
     "the caller maps it onto the declared acceptance level's failure semantics"),
    (PLAN_RUNNER, '"declared approval level in docs/process.toml (the "',
     '"declared acceptance level in docs/process.toml (the "'),
    (VERDICT, '"first-acceptance": ({"- [APPROVE]": "APPROVE", "- [RETURN]": "RETURN"}, "RETURN"),',
     '"first-acceptance": ({"- [ACCEPT]": "ACCEPT", "- [RETURN]": "RETURN"}, "RETURN"),'),
    (VERDICT, "amendment's MEANING/CLARITY, a first approval's APPROVE/RETURN); a row",
     "amendment's MEANING/CLARITY, a first acceptance's ACCEPT/RETURN); a row"),
    ("tests/test_dual_plan_round.py", "a recorded verdict carries approval authority.",
     "a recorded verdict carries acceptance authority."),
    ("tests/test_agent_loop_review_gate.py", "escalating through the declared approval level:",
     "escalating through the declared acceptance level:"),
    ("tests/test_agent_loop_critique.py", '"set the loop-held approval level"',
     '"set the loop-held acceptance level"'),
    # 2. names shared with renamed code
    ("tests/test_plan_gate.py", '    "_approval_act_refusal",', '    "_acceptance_act_refusal",'),
    ("tests/test_agent_route.py", "def test_failure_action_keyed_to_the_approval_level():",
     "def test_failure_action_keyed_to_the_acceptance_level():"),
    ("tests/test_plan_round.py", "def test_page_action_maps_the_approval_level_and_fails_safe():",
     "def test_page_action_maps_the_acceptance_level_and_fails_safe():"),
    # 3. check_vocab's ratif* suggestions
    (VOCAB, '# "approval". The `ratif*` word family', '# "approval", and since 2026-11-16 on "acceptance". The `ratif*` word family'),
    (VOCAB, '    "ication": "approval",', '    "ication": "acceptance",'),
    (VOCAB, '    "ied": "approved",', '    "ied": "accepted",'),
    (VOCAB, '    "iable": "approvable",', '    "iable": "acceptable",'),
    (VOCAB, """'{} (WI-499 retired "ratif*" for "approv*")'""",
     """'{} (WI-499 retired "ratif*"; the act is now "accept*")'"""),
    (VOCAB, """'accept/acceptance (WI-499 retired "ratif*" for "approv*")'""",
     """'accept/acceptance (WI-499 retired "ratif*"; the act is now "accept*")'"""),
    # 4. wording
    ("project-trajectory/scripts/acceptance_record.py", "DevStg-Tests -> a\n# accept brief and four review rounds",
     "DevStg-Tests -> an\n# acceptance brief and four review rounds"),
    ("docs/requirements/low-level-requirements.toml", "--accept accepts DA and SUR id",
     "--accept takes DA and SUR id"),
    ("tests/test_held_status_git.py", "Backed by an accepted APPROVE verdict", "Backed by a recorded ACCEPT verdict"),
    # 5. D12's glossary entry
    (GLOSSARY, """approval ceremonies are outside the kit.

### Vouch""", """approval ceremonies are outside the kit.

### approve

A [reviewer](#reviewer)'s verdict on a build round or a plan, written
`VERDICT: APPROVE` against `CHANGES-REQUESTED`, and a critic's in a critique.
It judges work: it takes no row as agreed and moves no `status`. The act on a
row is [accept](#accept); an adjudicator's ruling on a row in a
first-acceptance sitting is `ACCEPT`.

### Vouch"""),
]
