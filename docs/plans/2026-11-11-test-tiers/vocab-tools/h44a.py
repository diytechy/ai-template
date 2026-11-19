S = "project-trajectory/scripts/"
SIT = S + "kitlib/sitting.py"
ACT = S + "adjudicate_act.py"
BRF = S + "adjudicate_brief.py"

EDITS = [
    # --- kitlib/sitting.py
    (SIT, "`write_binding` is its one writer and `accepted`/`recorded_at` the one",
          "`write_binding` is its one writer and `recorded`/`recorded_at` the one"),
    (SIT, "reason)` for a verdict `recorded_at` does not read as accepted. A dispute",
          "reason)` for a verdict `recorded_at` does not read as recorded. A dispute"),
    (SIT, '    "accepted",\n    "recorded_part",', '    "recorded",\n    "recorded_part",'),
    (SIT, "# that ran the call records `accepted` (its own validation passed) or `failed`.\n"
          'OUTCOMES = ("pending", "accepted", "failed")',
          "# that ran the call writes `recorded` (its own validation passed) or `failed`.\n"
          'OUTCOMES = ("pending", "recorded", "failed")'),
    (SIT, "# --- acceptance is a RECORDED fact (WI-841 round 11) --------------------------",
          "# --- the outcome is a RECORDED fact (WI-841 round 11) -------------------------"),
    (SIT, "which is how the route that ran the call records `accepted` or `failed`.",
          "which is how the route that ran the call writes `recorded` or `failed`."),
    (SIT, "def accepted(text, binding_text):", "def recorded(text, binding_text):"),
    (SIT, "    rulings, `kitlib.verdict.row_rulings`) for a verdict whose binding records it\n"
          "    ACCEPTED by the route that ran the call and which `parse` reads as valid\n"
          "    against that binding's brief and requested kinds; None for anything else -\n",
          "    rulings, `kitlib.verdict.row_rulings`) for a verdict whose binding holds the\n"
          "    outcome `recorded`, written by the route that ran the call, and which `parse`\n"
          "    reads as valid against that binding's brief and requested kinds; None for anything else -\n"),
    (SIT, "kinds, never an error). A verdict's acceptance is the recorded fact, never\n"
          "    an inference from its text.",
          "kinds, never an error). A verdict's outcome is the recorded fact, never\n"
          "    an inference from its text."),
    (SIT, 'if not bound or bound[2] != "accepted":', 'if not bound or bound[2] != "recorded":'),
    (SIT, "in a recorded verdict (`accepted`), or None.", "in a recorded verdict (`recorded`), or None."),
    (SIT, "found = accepted(text, binding_text) or {}", "found = recorded(text, binding_text) or {}"),
    (SIT, '"""`accepted` for the verdict file at', '"""`recorded` for the verdict file at'),
    (SIT, "return accepted(*_texts_at(root, rev, verdict_path))", "return recorded(*_texts_at(root, rev, verdict_path))"),
    (SIT, "the identities the binding of an ACCEPTED\n", "the identities the binding of a RECORDED\n"),
    (SIT, "verdict `accepted` does not read as accepted binds nothing",
          "verdict `recorded` does not read as recorded binds nothing"),
    (SIT, "if not accepted(*texts):", "if not recorded(*texts):"),
    (SIT, '"the verdict {} is not accepted at {}"', '"the verdict {} is not recorded at {}"'),
    (SIT, "a recorded parsed verdict (`accepted`) rules in a way", "a recorded parsed verdict (`recorded`) rules in a way"),
    (SIT, "the ONE reader of what an\n    recorded verdict authorizes", "the ONE reader of what a\n    recorded verdict authorizes"),
    (SIT, "the verdict is\n    not accepted, or it does not", "the verdict is\n    not recorded, or it does not"),
    (SIT, "must name one `recorded_at` reads as accepted at", "must name one `recorded_at` reads as recorded at"),
    (SIT, '"the adjudication\'s act names a verdict no route recorded ACCEPTED, or "',
          '"the adjudication\'s act names a verdict no route RECORDED, or "'),
    (SIT, "part (`judged_rows`), of an ACCEPTED\n", "part (`judged_rows`), of a RECORDED\n"),
    (SIT, '"entry point, whose binding records it accepted.{}"', '"entry point, whose binding records the outcome.{}"'),
    # --- adjudicate_act.py
    (ACT, "Exactly the rows each accepted part rules to", "Exactly the rows each recorded part rules to"),
    (ACT, "the brief class an accepted,\n    actable verdict's binding records", "the brief class a recorded,\n    actable verdict's binding records"),
    (ACT, "Why the verdict at `rel` is not accepted at `rev`", "Why the verdict at `rel` is not recorded at `rev`"),
    (ACT, 'if outcome != "accepted":\n        return "the verdict {}\'s binding records the outcome {}, not accepted".format(',
          'if outcome != "recorded":\n        return "the verdict {}\'s binding records the outcome {}, not recorded".format('),
    (ACT, "def _accepted(root, rev, rel):", "def _recorded(root, rev, rel):"),
    (ACT, "every accepted part authorizes", "every recorded part authorizes"),
    (ACT, "when it is refused: not\n    accepted there, of a class", "when it is refused: not\n    recorded there, of a class"),
    (ACT, "found, why = _accepted(root, rev, rel)", "found, why = _recorded(root, rev, rel)"),
    (ACT, "found = _accepted(root, rev, rel)[0] if rel else None", "found = _recorded(root, rev, rel)[0] if rel else None"),
    # --- adjudicate_brief.py
    (BRF, "ran was ACCEPTED or FAILED, in the verdict's binding, committed in its own\n"
          "    bookkeeping commit; returns `(outcome, why)`, `why` None when accepted.\n"
          "    ONE RULE for both routes (the coordinator's entry point and the loop):\n"
          "    accepted only when the CALL succeeded",
          "ran is RECORDED or FAILED, in the verdict's binding, committed in its own\n"
          "    bookkeeping commit; returns `(outcome, why)`, `why` None when recorded.\n"
          "    ONE RULE for both routes (the coordinator's entry point and the loop):\n"
          "    recorded only when the CALL succeeded"),
    (BRF, 'outcome = "failed" if why else "accepted"', 'outcome = "failed" if why else "recorded"'),
    # --- plan_coverage.py / plan_gate.py
    (S + "plan_coverage.py", 'if bound[2] != "accepted":', 'if bound[2] != "recorded":'),
    (S + "plan_gate.py", 'if bound[2] != "accepted":', 'if bound[2] != "recorded":'),
    (S + "plan_gate.py", "finding the cited accepted\n", "finding the cited recorded\n"),
    # --- runtime flow diagram
    ("docs/runtime-flows.md", "Coord->>Verdict: validate and record recorded verdict",
                              "Coord->>Verdict: validate the verdict and record its outcome"),
]
