ACT = "project-trajectory/scripts/adjudicate_act.py"

# `_accepted` cannot become `_recorded`: adjudicate_act.py already has a
# `_recorded(root, rev)` for another thing (handoff trap 12).
EDITS = [
    (ACT, "def _recorded(root, rev, rel):", "def _recorded_verdict(root, rev, rel):"),
    (ACT, "found, why = _recorded(root, rev, rel)", "found, why = _recorded_verdict(root, rev, rel)"),
    (ACT, "found = _recorded(root, rev, rel)[0] if rel else None", "found = _recorded_verdict(root, rev, rel)[0] if rel else None"),
    ("docs/requirements/low-level-requirements.toml", "_unrecorded_reason/_accepted/_tier", "_unrecorded_reason/_recorded_verdict/_tier"),
]
