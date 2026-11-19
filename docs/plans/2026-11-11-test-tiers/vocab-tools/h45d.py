"""HANDOFF 10.5 pass 3, hand edits after r45d_attest.py.

1. S7, a worker's claim (VOCABULARY.md 3; HANDOFF 4.2 "claims, records,
   states", proposed and so ruled under D10): a WI's `Status` and a ticked
   Done-when box are CLAIMS, and a `WI:` trailer "does not show the work is
   done". The 2026-07-28 ruling is cited, not quoted, so its words can follow.
2. Forms the dial concept missed (the table `[attestation]` is `[authority]`):
   IF row data naming the tables, TC-?'s "an attestation section", and a
   test docstring's "retired attestation dial key".
3. One sentence r45d made circular ("acceptance closes acceptance"), and a
   plain verb in a TC method ("where they attest ... claim").
"""

CT = "project-trajectory/scripts/check_trajectory.py"

EDITS = [
    # 1. S7
    (CT, "# A WI's `Status` is an ATTESTATION, and the operator ruled 2026-07-28 that it stays",
     "# A WI's `Status` is a CLAIM, and the operator ruled 2026-07-28 that it stays"),
    (CT, '"`WI: {}` trailer — a trailer CLAIMS the WI, it does not "\n'
         '                        "attest the work, so this is a prompt to reconcile, never "',
     '"`WI: {}` trailer — a trailer CLAIMS the WI, it does not "\n'
     '                        "show the work is done, so this is a prompt to reconcile, never "'),
    (CT, "    signals rather than as another branch in `main()`. Spec evidence is an\n    attestation, so a row",
     "    signals rather than as another branch in `main()`. Spec evidence is a\n    claim, so a row"),
    (CT, "# kind: a ticked box IS an attestation, so its disagreement",
     "# kind: a ticked box IS a claim, so its disagreement"),
    ("tests/test_trajectory_specs.py", "# Status stays an ATTESTATION (operator ruling 2026-07-28)",
     "# Status stays a CLAIM (operator ruling 2026-07-28)"),
    # 2. the dial's table
    ("docs/requirements/interfaces.toml", 'data = "TOML tables: attestation, policies, checks, build;',
     'data = "TOML tables: authority, policies, checks, build;'),
    ("docs/test/test-cases.toml", "(b) UNDECLARED: an attestation section without the key",
     "(b) UNDECLARED: an authority section without the key"),
    ("tests/test_bootstrap.py", "The migration's rename of the retired attestation dial key refuses an",
     "The migration's rename of the retired dial key refuses an"),
    # 3. wording
    ("docs/knowledge/co-planning.md", "delta. Operator acceptance closes acceptance per the gate philosophy.",
     "delta. The operator's acceptance closes the round, per the gate philosophy."),
    ("docs/test/test-cases.toml", "where they attest LLR-181/SR-166's materialization claim",
     "where they back LLR-181/SR-166's materialization claim"),
]
