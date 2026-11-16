"""HANDOFF 10.5 pass 4, hand edits after r45f/r45g.

1. Two status fixtures in a review-round test r45f skips whole (D12): CSV
   rows whose Status cell is the status, not a reviewer's word.
2. A history note r45f's protection missed because its phrase is split over
   a line break: the retired column's rows "both became `approved`".
"""

EDITS = [
    ("tests/test_agent_loop_critique.py", r'"Subjective.","Judged against the rubric.",,S,Critique,Approved\n',
     r'"Subjective.","Judged against the rubric.",,S,Critique,Accepted\n'),
    ("tests/test_agent_loop_critique.py", r'"Objective.","render(x)==y.",,S,Test,Approved\n',
     r'"Objective.","render(x)==y.",,S,Test,Accepted\n'),
    ("tests/test_trajectory_arch.py", "    # `accepted`, so re-keying the rule on `approval == \"approved\"` passed",
     "    # `approved`, so re-keying the rule on `approval == \"approved\"` passed"),
]

# 3. The review-round files r45c and r45f skip whole, swept afterwards for the
#    act's flags and names (trap 31): the reviewer prompt still told a
#    reviewer to run `trace.py --approve`, a flag pass 3 renamed; and one more
#    status fixture.
RT = "project-trajectory/prompts/reviewer.template.md"
EDITS += [
    (RT, "Preserve unchanged parent acceptance and approval and the enduring behavioral regression tests;",
     "Preserve a parent's acceptance criteria and its acceptance unchanged, and the enduring behavioral regression tests;"),
    (RT, "is a DevStg-Reqs/DevStg-Tests approval (a Status-change commit", "is a DevStg-Reqs/DevStg-Tests acceptance (a Status-change commit"),
    (RT, "the batch-scoped approval hierarchy is a REQUIRED input", "the batch-scoped acceptance hierarchy is a REQUIRED input"),
    (RT, "trace.py --approve <phase>` and confirm the approved SN->SR->LLR/TC batch",
     "trace.py --accept <phase>` and confirm the accepted SN->SR->LLR/TC batch"),
    ("tests/test_agent_loop_critique.py", r'"Critic APPROVE",No,,Approved\n', r'"Critic APPROVE",No,,Accepted\n'),
]
