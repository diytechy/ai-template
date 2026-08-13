+++
id = "WI-448"
title = "OI-16 execution (inversion confirmed by the owner 2026-08-13): the common-module program — shared helpers consolidate into one shipped common module (or several themed library files, per D-8's smallest-total-code direction), bootstrap.py imports FROM it, the module joins MAPPING (the single line that is the whole downstream risk surface, and the line the repo has got wrong once). Before landing: assert what has only ever been a comment — the new rule that bootstrap imports the common module and nothing else — and verify by BOOTSTRAPPING A REAL SCAFFOLD, the standing lesson from the schedule.py omission. First slice ~9 files deleting roughly 650 duplicated lines; bootstrap sheds its two declared duplicates and the test_rule_sync pins holding them equal become unnecessary (drift made unrepresentable, not detected). The module-size ratchet fires on the consolidated file and measures the wrong axis by the owner's own correction (function size and complexity, not lines) — re-stamp deliberately with the reason in the log, and file the ratchet-axis question as its own finding. Sequenced after OI-14 part A (component ownership turns import doctrine into a lookup); lands the first OI-27 migration entries for the rename-heavy surface, or the prose ADOPTING section 6 recipe if it executes first."
specref = "docs/requirements/open-items.toml#OI-16"
workstream = "lock-program"
sr_refs = []
needs = ["WI-441", "~WI-447"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++
