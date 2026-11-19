S = "project-trajectory/scripts/"
RECIPES = tuple(
    p + "skills/coordinator-cycle/references/recipes.md"
    for p in ("project-trajectory/", ".claude/", ".agents/")
)
LLR = "docs/requirements/low-level-requirements.toml"
IF = "docs/requirements/interfaces.toml"
TC = "docs/test/test-cases.toml"

EDITS = [
    (RECIPES, "verdict not accepted at HEAD, one that owes no act", "verdict not recorded at HEAD, one that owes no act"),
    (RECIPES, "A verdict not accepted files nothing,", "A verdict not recorded files nothing,"),
    (IF, "record_outcome(...) -> (accepted | failed, why | None)", "record_outcome(...) -> (recorded | failed, why | None)"),
    (IF, "when a pending binding is rewritten as accepted or failed", "when a pending binding is rewritten as recorded or failed", 2),
    (LLR, "rewriting the binding as accepted or failed preserves them", "rewriting the binding as recorded or failed preserves them"),
    (LLR, "only a bound verdict whose route recorded accepted and which parses valid",
          "only a bound verdict whose route wrote the outcome recorded and which parses valid"),
    (TC, "rewriting the binding as accepted or failed preserves them", "rewriting the binding as recorded or failed preserves them"),
    (TC, "kept through the outcome rewrite, accepted or failed;", "kept through the outcome rewrite, recorded or failed;", 2),
    (TC, "or an unaccepted SUCCESSOR, leaves the finding unresolved", "or an unrecorded SUCCESSOR, leaves the finding unresolved"),
    ("docs/runtime-flows.md", "alt verdict is unaccepted, owes no act", "alt verdict is unrecorded, owes no act"),
    (S + "acceptance_record.py", "on that reader: an outcome is recorded accepted only by",
                                 "on that reader: an outcome reads `recorded` only through"),
    (S + "coordinator_adjudicate.py", "not accepted there, owes no act, or judged a row", "not recorded there, owes no act, or judged a row"),
    (S + "kitlib/done_when.py", "for every ACCEPTED Done-when verdict under", "for every RECORDED Done-when verdict under"),
    (S + "kitlib/done_when.py",
     "`kitlib.sitting.accepted`, which answers only for a verdict whose binding\n"
     "    records it accepted by the route that ran the call and which parses as",
     "`kitlib.sitting.recorded`, which answers only for a verdict whose binding\n"
     "    holds the outcome `recorded` from the route that ran the call and which parses as"),
    ("tests/test_adjudicate_brief.py",
     "    accepted = ksitting.recorded(text, binding)\n    assert accepted, text\n"
     "    rows = {kind: part[3] for kind, part in accepted.items()}\n"
     "    return parsed, rows, ksitting.judged_rows(accepted)",
     "    recorded = ksitting.recorded(text, binding)\n    assert recorded, text\n"
     "    rows = {kind: part[3] for kind, part in recorded.items()}\n"
     "    return parsed, rows, ksitting.judged_rows(recorded)"),
    ("tests/test_coordinator_adjudicate.py", "through the outcome rewrite, accepted or failed;", "through the outcome rewrite, recorded or failed;"),
    ("tests/test_done_when_blessing.py", "through the holds: recorded ACCEPTED is not enough -", "through the holds: an outcome of RECORDED is not enough -"),
    ("tests/test_snapshot_readers.py", "# The verdict is not accepted at all,", "# The verdict is not recorded at all,"),
    ("tests/test_snapshot_readers.py", 'assert refusal and "ACCEPTED" in refusal', 'assert refusal and "RECORDED" in refusal', 3),
]
