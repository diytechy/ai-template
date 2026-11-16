"""HANDOFF 4.3 / 10.4, owner: hand edits after r43b_owner.py and r43c_owner_iface.py.

Written against the text as it stands after both rule files, and after
`git mv project-trajectory/OWNER_SCRATCHPAD.template.md
project-trajectory/OPERATOR_SCRATCHPAD.template.md`.

1. The scratchpad template's header: the operator's notes as a person, which no
   session reads, delegated or not (the operator's ruling: its header may
   still say it is for a person's notes). The test's assertion follows.
2. PROCESS_OPTIONS.md: the scratchpad note ("a person's scratch") and "the
   final read stays the operator's".
3. STK-01's name: an accepted row reworded in place (D5).
"""

TEMPLATE = "project-trajectory/OPERATOR_SCRATCHPAD.template.md"

EDITS = [
    # 1. the scratchpad template and its test
    (TEMPLATE,
     "# OWNER_SCRATCHPAD — the human owner's private notes\n",
     "# OPERATOR_SCRATCHPAD — the operator's private notes\n"),
    (TEMPLATE,
     "> **For the human owner only.** LLM agents: do **NOT** read, index, summarize,\n",
     "> **For the operator only, as a person.** No session reads it, delegated or\n"
     "> not. LLM agents: do **NOT** read, index, summarize,\n"),
    (TEMPLATE,
     "<!-- Owner notes below. Free-form; nothing here gates a commit. -->",
     "<!-- Operator notes below. Free-form; nothing here gates a commit. -->"),
    ("tests/test_bootstrap.py",
     '    assert "For the human owner only" in text\n',
     '    assert "For the operator only, as a person" in text\n'),
    # 2. PROCESS_OPTIONS.md
    ("project-trajectory/PROCESS_OPTIONS.md",
     "**The operator scratchpad is human scratch, not a working surface.**",
     "**The operator scratchpad is a person's scratch, not a working surface.**"),
    ("project-trajectory/PROCESS_OPTIONS.md",
     "run under `autonomous` rules. The operator's final read\n"
     "  stays the operator's.",
     "run under `autonomous` rules. The final read\n"
     "  stays the operator's."),
    # 3. STK-01
    ("docs/requirements/stakeholder-needs.toml",
     '[stakeholder.STK-01]\nname = "Owner"\n',
     '[stakeholder.STK-01]\nname = "Operator"\n'),
]
