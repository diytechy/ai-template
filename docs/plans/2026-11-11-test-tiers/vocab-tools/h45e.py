"""HANDOFF 10.5 pass 3, hand edits: the "attest" leftovers r45d's phrases missed
(trap 28), read one by one. S6 (the act) moves; S7 (a worker's claim, and the
plain verb) takes "claim" / "recorded". Left as written, and listed in
HANDOFF: S1 (the passed-checks record, 10.6), S3 (the method, `Vouch`),
"half-attested" (a lane mid-refresh, S1), and the verdict-artifact list in
PROCESS_OPTIONS (review file, critique, attestation), whose last item could be
either S3 or S6.
"""

EDITS = [
    ("project-trajectory/hooks/pre-commit", "a stale brief is read by an OPERATOR about to\n#                        attest, and",
     "a stale brief is read by an OPERATOR about to\n#                        accept, and"),
    ("project-trajectory/scripts/trace.py", "a stale brief is read by an operator about to\n    attest, and the cost",
     "a stale brief is read by an operator about to\n    accept, and the cost"),
    ("project-trajectory/scripts/gen_open_items.py", "An APPROVED cell that moved owes an\n    attestation; a TRACED one",
     "An APPROVED cell that moved owes an\n    acceptance; a TRACED one"),
    ("project-trajectory/scripts/check_trajectory.py", "it rules that Status stays an\n    # attestation precisely because",
     "it rules that Status stays a\n    # claim precisely because"),
    ("project-trajectory/scripts/spine_rules.py", '"amended after attestation" any more',
     '"amended after acceptance" any more'),
    ("project-trajectory/PROCESS_OPTIONS.md", "rewinding would discard the closed phase's\n  attestation).",
     "rewinding would discard the closed phase's\n  acceptance)."),
    ("project-trajectory/scripts/acceptance_record.py", "`LLR-178`'s attested rationale", "`LLR-178`'s accepted rationale"),
    ("project-trajectory/scripts/intake.py", "BEFORE-side owner (the attested one)", "BEFORE-side owner (the accepted one)"),
    ("project-trajectory/prompts/adjudicate-red-tc.template.md", "has not been attested as passing", "has not been recorded as passing"),
    ("docs/requirements/stakeholder-needs.toml", "amends only if this need is attested.", "amends only if this need is accepted."),
    ("docs/requirements/system-requirements.toml", "re-opens the test case's attestation.", "re-opens the test case's acceptance."),
]
