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

### SLICE 1 LANDED 2026-08-20 — what shipped, and what this row still owes

**Landed.** `project-trajectory/scripts/kitlib/` exists as a shipped package
with themed modules (`config`, `git`, `registry`), joined `MAPPING` as four
rows, and `bootstrap.py` imports it. The replacing rule is asserted
(`test_bootstrap_imports_only_the_common_package`), the manifest is tested in a
REAL SCAFFOLD (`test_the_common_package_ships_complete`, driven red on a
deleted MAPPING row), and a scaffold was bootstrapped by hand as the standing
lesson requires. Consolidated: the 270-line spec-folder reader (3 verbatim
copies), the declared-line reader (5 copies), `_git_out` (3 copies). The two
`test_rule_sync` equality pins holding the line-reader copies equal are deleted
with the reasoning recorded in their place.

**Measured** (one command, both revisions; `fig:` marker in
`docs/log.d/2026-08-20-program-grind.md`): duplicated function-body groups
24 -> 17, redundant copies 67 -> 48, redundant lines 757 -> 477.

**STILL OWED BY THIS ROW — the reason it is not closed:**

1. **`_utf8_console`, 33 remaining copies** — 264 of the 477 residual redundant
   lines, the single largest item left and more than half of what remains.
   Mechanically trivial across 33 files; held back only to keep slice 1
   reviewable.
2. **`bootstrap`'s OTHER declared duplicate** — `STACK_OI3_ROW` plus its TOML
   row emitter, which the OI-16 blast radius names. Shedding it needs the
   open-items key vocabulary in `kitlib` first. Note that its pin's stated
   premise ("bootstrap runs BEFORE the kit is copied and can import no
   sibling") is exactly what slice 1 overturned, so the comment on
   `test_rule_sync.test_bootstraps_scaffolded_brief_uses_the_converters_own_keys`
   is now stale and must be corrected when the duplicate goes.
3. **The `spine_rules`/`trace` spine-policy pair** — 10 duplicated groups
   (`is_approved`, `is_founded`, `is_drafted`, `sn_all_ids`, `sn_cited_ids`,
   `sn_draft_ids`, `phase_num`, `llr_exempt`, `load_csv`). These are POLICY,
   not plumbing, so they are what `test_rule_sync` pins most carefully;
   consolidating them retires more pins and needs the care slice 1 took.
4. **`is_example`** (the 3-home behaviour whose copies disagreed, one crashing
   on `None`), `_process_check` x2, `_norm_module` x2, `sn_rows` x2,
   `_split_tokens`/`split_refs` x2, and `wi_convert`'s `spec_paths` /
   `work_dir_for` variants of the registry reader.
5. **The `views` theme slot**, named by the adopted shape and deliberately not
   created empty. `station` LANDED 2026-08-20 — not from this row, but from the
   successor decomposition program, which needed the lane-close terminal-outcome
   vocabulary somewhere below both its readers to cut a view-into-coordinator
   import. It took its OWN single-component design row rather than joining this
   package's four-way tag.

**`OI-48` is RULED (d) AND EXECUTED (2026-08-21 / WI-494, 2026-08-22)**: which
component owns the shared kernel is settled. `LLR-181`'s four-way `Component`
tag — true about USAGE, silent about OWNERSHIP — collapses to `CMP-006` alone
(the recorded closest-fit reason: registry.py's bulk within the row's own
module set). The package's real cross-component consumption now rides the
declared shared-kernel surface (`docs/kernel-modules-allow`), OI-48's reuse
provision — never a bare `Component` tag, and never special-cased to kitlib —
so `cross_component_findings` stays live on every edge NOT into a declared
kernel module. `station.py` (item 5, `LLR-182`) is confirmed NOT part of the
kernel declaration: its one cross-component edge is already a declared,
policed seam (`IF-093`), so its tag stays `CMP-008` unmoved. The remaining
consolidation slices below are unblocked.
