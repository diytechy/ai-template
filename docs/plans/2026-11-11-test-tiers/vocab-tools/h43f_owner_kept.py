"""HANDOFF 4.3 / 10.4, owner: role uses r43b's KEEP patterns held back.

h43e read the leftover lines after dropping every line whose "owner" sat
inside a KEEP span, and so repeated trap 28 one level down: KEEP's
`(one|each|every|its|...) owner` pattern, written for "ONE OWNER" (a single
home) and "its owner" (a finding's), also holds "one owner sitting", "each
owner and judge surface", "every owner ask" and "its owner asks". The 121
KEEP-held lines outside the interface files were read; these 18 are the role.
"""

S = "project-trajectory/scripts/"

EDITS = [
    ("README.md", "so one owner sitting re-attests", "so one operator sitting re-attests"),
    ("docs/test/test-cases.toml", "each owner and judge surface names the commit",
     "each operator and judge surface names the commit"),
    ("project-trajectory/PROCESS_OPTIONS.md", "a call the owner should see is disclosed",
     "a call the operator should see is disclosed"),
    ("project-trajectory/PROCESS_OPTIONS.md", "the entries the owner should read first, then one",
     "the entries the operator should read first, then one"),
    (S + "agent_policy.py", "a repo whose owner had just asked for two",
     "a repo whose operator had just asked for two"),
    (S + "agent_policy.py", "record until its owner asks for one",
     "record until its operator asks for one"),
    (S + "bootstrap.py", "every owner ask has its brief", "every operator ask has its brief"),
    (S + "check_docs.py", "(every owner ask carries its ", "(every operator ask carries its "),
    (S + "kitlib/decisions.py",
     "`review` is the owner's cell, empty until the operator writes in it.",
     "`review` is the operator's cell, empty until they write in it."),
    (S + "kitlib/decisions.py", "naming the entries the owner should read first",
     "naming the entries the operator should read first"),
    (S + "kitlib/done_when.py", "every owner-ruled `done_when` digest",
     "every operator-ruled `done_when` digest"),
    (S + "intake.py", "one owner row per registry", "one operator row per registry"),
    (S + "trace.py", "(WI-442,\n    owner naming 13m)", "(WI-442,\n    operator naming 13m)"),
    ("tests/test_approval_level.py", "is the one the owner named.", "is the one the operator named."),
    ("tests/test_decision_record.py", "# The owner's cell: any string", "# The operator's cell: any string"),
    ("tests/test_gen_open_items.py", "into the owner's surface)", "into the operator's surface)"),
    ("tests/test_intake.py", "Rendered through the owner surface's own card builder",
     "Rendered through the operator surface's own card builder"),
    ("tests/test_intake_held_act.py", "The one owner row and the one item",
     "The one operator row and the one item"),
]
