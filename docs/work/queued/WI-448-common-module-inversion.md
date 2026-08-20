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

## Context

**This row feeds the deferred P5 ratification (2026-08-13s).** Decision 10 was
deferred until after this program and the SR re-tier, to be re-taken on
**re-derived** numbers (pack §3's finding puts the violation in the copies: 39
behaviour-home pairs across 16 modules) — and 13s names this row as permitted
to proceed against the provisional CMP-006…009 tags. Record the
post-consolidation duplication figures in the log at close — they are the
deferred decision's basis, and re-deriving them later costs a second
measurement pass. On the MAPPING question sitting-2 §5.3 raised: MAPPING is
B-05 delivered content; whether adding a module obliges an IF-row edit is the
schema row's business under the slimmed IF schema — verify by bootstrapping a
real scaffold (already in scope) and defer the IF-row question to that row.

**Review corroboration and shape guidance (2026-08-19, repo-review triage).**
The 2026-08-19 repository review (H-09, archived at
`docs/archive/repo-review-2026-08-19.md`) independently confirmed the
duplication this row consolidates — five repeated declared-line readers
(`agent_common`, `bootstrap`, `check_privacy`, `check_trajectory`,
`subagent_gate`) and duplicated work-item loaders (`schedule`,
`check_trajectory`) — and asks that the result be a SMALL COPIED PACKAGE with
THEMED modules (registry / config / git / station / views), never one more
generic `common.py`; CLI wrappers stay thin; bootstrap copies the package
atomically and the complete dependency manifest is tested in real scaffolds.
That matches D-8's smallest-total-code direction and is adopted as this row's
shape constraint. The successor decomposition program (WI-483, minted by the
same triage) builds ON this row's consolidated package — its soft edge points
here, so this row's landing decides the package topology first.

