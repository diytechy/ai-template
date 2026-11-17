"""HANDOFF 4.5.3, hand edits after r47c: the census line grammar and the
census's own prose, where "red" meant "not accepted under a claimed
implementation" and "green" meant accepted. The grammar is printed and parsed
live (`evidence_gap_census`, `parse_evidence_gap`), never stored, so its
tests move with it.
"""

C = "project-trajectory/scripts/census.py"

EDITS = [
    # EVIDENCE_GAP_PREFIX's value moved by r47c's REGEX ("red TC " -> "evidence gap ")
    (C, 'ASSUMPTION_GAP_PREFIX = "red assumption TC "', 'ASSUMPTION_GAP_PREFIX = "assumption evidence gap "'),
    (
        C,
        "    until its routing is decided: whether a red assumption-evidence case mints",
        "    until its routing is decided: whether an assumption evidence gap mints",
    ),
    (
        C,
        "# The three statuses this rung does NOT call red, each because another rung",
        "# The three statuses this rung does NOT call a gap, each because another rung",
    ),
    (
        C,
        "# joined — a TC at the top rung is green a fortiori,",
        "# joined — a TC at the top rung is accepted a fortiori,",
    ),
    (
        C,
        "# `Modified` TCs now sees them as red here",
        "# `Modified` TCs now sees them as gaps here",
    ),
    (
        C,
        '    """LLR-159: TEST CASES LEFT RED UNDER A CLAIMED IMPLEMENTATION.',
        '    """LLR-159: TEST CASES LEFT UNACCEPTED UNDER A CLAIMED IMPLEMENTATION.',
    ),
    (
        C,
        "    is closed and the evidence for it is red.",
        "    is closed and the evidence for it is not.",
    ),
    (
        C,
        "    than as a list of red words — anything else is red, which fails toward",
        "    than as a list of gap words — anything else is a gap, which fails toward",
    ),
    (
        C,
        "      Accepted  green, by definition.\n"
        "      Drafted   pre-acceptance; \"not yet green\" is its CORRECT state.\n"
        "      Founded   Accepted plus a demonstration — green a fortiori (D-9 step 8).",
        "      Accepted  no gap, by definition.\n"
        "      Drafted   pre-acceptance; \"not yet accepted\" is its CORRECT state.\n"
        "      Founded   Accepted plus a demonstration — no gap a fortiori (D-9 step 8).",
    ),
    (
        C,
        "    on the premise is closed, and the evidence for the premise is red. A case",
        "    on the premise is closed, and the evidence for the premise is not. A case",
    ),
    (
        C,
        "    nothing, so a case naming only such assumptions is not red.\"\"\"",
        "    nothing, so a case naming only such assumptions is no gap.\"\"\"",
    ),
    (
        C,
        '"built ({}): the premise their argument rests on has no green "',
        '"built ({}): the premise their argument rests on has no accepted "',
    ),
    (
        C,
        '"claims the work; its evidence is not green)".format(',
        '"claims the work; its evidence is not accepted)".format(',
    ),
    # --- tests: the census lines they hand the draft, and a fixture title
    ("tests/test_loop_order.py", '"red TC TC-1 [SR-1] is failed"', '"evidence gap TC-1 [SR-1] is failed"', 2),
    ("tests/test_loop_order.py", '"red TC TC-1 [SR-1;SR-2] is failed"', '"evidence gap TC-1 [SR-1;SR-2] is failed"', 2),
    ("tests/test_adjudicate_brief.py", '"Title": "adjudicate red TC TC-001",', '"Title": "adjudicate evidence gap TC-001",'),
    (
        "tests/test_adjudicate_brief.py",
        "# EXEMPTION — anything outside `dispatch._GAP_EXEMPT_STATUSES` is red — and this fixture",
        "# EXEMPTION — anything outside `dispatch._GAP_EXEMPT_STATUSES` is a gap — and this fixture",
    ),
    # an article PARTS cannot see
    (
        ("project-trajectory/process.toml.template",),
        "#                    a evidence-gap drafting ordinary fix rows,",
        "#                    an evidence-gap drafting ordinary fix rows,",
    ),
    (
        "docs/process.toml",
        "#                    a red-tc drafting ordinary fix rows,",
        "#                    an evidence-gap drafting ordinary fix rows,",
    ),
]
