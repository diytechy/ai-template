"""HANDOFF 4.5.3, the second pass of hand edits: what r47c and h47f left
(the prompt's own words;
two READMEs). "Unverified test case" is the alternative 4.5.3 refused, so it
goes too. The prompt's claim that the status is not `Verified` is left as it
stands: correcting it is not vocabulary.
"""

PR = "project-trajectory/prompts/adjudicate-evidence-gap.template.md"

EDITS = [
    (
        "project-trajectory/README.md",
        "draft needs and test cases left red under a claimed implementation",
        "draft needs and evidence gaps (test cases left unaccepted under a claimed implementation)",
    ),
    (
        "project-trajectory/prompts/README.md",
        "| `adjudicate-evidence-gap.template.md` | unverified test cases found by the idle census | yes |",
        "| `adjudicate-evidence-gap.template.md` | evidence gaps found by the idle census | yes |",
    ),
    (PR, "     the effort and drafts the fix-to-green row,", "     the effort and drafts the row that closes it,"),
    (PR, "the census lines, one per unverified TC:", "the census lines, one per evidence gap:"),
    (PR, "so this is every case that is red NOW,", "so this is every gap open NOW,"),
    (
        PR,
        "the kit records no red/green RESULT\n"
        "     for a test case. `Evidence` is a LOCATION (a pytest node, a script path),\n"
        '     never an outcome. So "red" here means exactly one thing',
        "the kit records no pass/fail RESULT\n"
        "     for a test case. `Evidence` is a LOCATION (a pytest node, a script path),\n"
        "     never an outcome. So a gap here means exactly one thing",
    ),
    (
        PR,
        "--- UNVERIFIED TEST CASES (id, verifies, method/expected, evidence LOCATION) ---",
        "--- EVIDENCE GAPS (id, verifies, method/expected, evidence LOCATION) ---",
    ),
    (
        PR,
        "Then DRAFT one fix-to-green row per distinct cause",
        "Then DRAFT one row that closes the gap per distinct cause",
    ),
    (PR, "is exactly the false green the gate exists to prevent.", "is exactly the false pass the gate exists to prevent."),
]
