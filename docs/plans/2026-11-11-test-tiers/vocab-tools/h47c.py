"""HANDOFF 4.5.2, two comments naming the key by its earlier spelling.

Applied before this file, with the Edit tool: intake.py's comment above
`WI_CHECKS_STAGES` re-wrapped after h47a lengthened one line.
"""

P = "project-trajectory/scripts/"

EDITS = [
    (
        P + "check_vocab.py",
        "tables that let an adopter's `--gate G2`, `gates = G2 G3` and `bar: G3` keep",
        "tables that let an adopter's `--gate G2`, `gates = G2 G3` and `checks_stage = G3` keep",
    ),
    (
        P + "kitlib/bootstrap_manifest.py",
        "    # the retired `G*` tags (their WI `bar:` values, their `stack.ini` `gates=`,",
        "    # the retired `G*` tags (their WI `checks_stage` values, their `stack.ini` `gates=`,",
    ),
]
