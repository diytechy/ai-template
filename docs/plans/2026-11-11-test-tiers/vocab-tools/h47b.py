"""HANDOFF 4.5.2, after n47a's `gate` -> `stage`: the summary names the stage."""

EDITS = [
    (
        "project-trajectory/scripts/integrate.py",
        '", gate " + stage if stage else ""',
        '", stage " + stage if stage else ""',
    ),
]
