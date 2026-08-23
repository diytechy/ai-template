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

**This row feeds the deferred P5 approval (2026-08-13s).** Decision 10 was
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

### SLICE 2 LANDED 2026-08-22 — item 1, the console guard

**Landed.** The 33 remaining `_utf8_console` copies are deleted; every one of
them — plus `bootstrap.py`'s existing alias — now resolves to the single shipped
`kitlib.config.utf8_console`, which slice 1 had already placed. NO new kitlib
module and no `MAPPING` change was needed: the behaviour's theme (console
encoding) was already declared as `config`'s, so joining the existing theme was
the smallest-total-code answer D-8 asks for. 32 scripts take a one-line
`from kitlib.config import utf8_console as _utf8_console`; `agent_common.py`
aliases off the guarded `kitlib.config` import it already carries. The
module-local NAME is preserved, so the three cross-module call sites
(`ct._utf8_console()`, `prompts._utf8_console()`, `ac._utf8_console()`) are
untouched and CLI behaviour is byte-identical. NO DRIFT was found: all 33 bodies
were identical modulo the docstring and one loop-variable name
(`gen_open_items.py` spelled it `stream`, which the shipped home also uses).
Manifest completeness re-verified by bootstrapping a REAL scaffold and importing
all 32 shipped scripts there (`gen_skills_index.py` is kit-authoring, not in
`MAPPING`; verified in-repo).

**Measured** (the slice-1 command, both revisions; `fig:` marker in
`docs/log.d/2026-08-22-wi448-utf8-console.md`): duplicated function-body groups
17 -> 15, redundant copies 47 -> 15, redundant lines 479 -> 194. Every one of
the 15 residual groups is named in items 3 and 4 below — there is nothing left
in the population this row has not already scoped.

### SLICE 3 LANDED 2026-08-23 — item 3, the spine POLICY pair

**Landed.** The ten duplicated groups the `trace.py`/`spine_rules.py` pair
carried consolidate into a NEW themed module, `kitlib/spine.py` — the spine ROW
vocabulary — which joins `MAPPING`, the kit README, the package roster,
`RESYNC_PACK.md` §3 and takes `LLR-197`/`TC-193` at `CMP-006`, both
`Drafted`: approving them here would have forced a `last_approved` refresh in
the same act, and that refresh would have absorbed this slice's LLR-147 Detail
amendment — laundering the re-attestation it owes. The amendment stays visible
in `docs/ratify/CURRENT.md` for the owner's sitting. Nine
`test_rule_sync` equality pins are deleted with the reasoning recorded in their
place, three more were trimmed of the limb that became a call to one object
twice, and two replacements landed: an IDENTITY pin (the deletion's warrant) and
three by-VALUE batteries holding the half of the retired pins that was never
about sameness. Every former name is re-exported from its original module, so
CLI behaviour is byte-identical.

**Chosen against `kitlib/registry.py`** deliberately: that module is the
`docs/work/` SPEC-FOLDER reader — a different registry, carrier and consumer set
— and folding the spine's row rules in would have grown the package's largest
module into the generic bucket the adopted H-09 shape constraint forbids.

**NO KERNEL DECLARATION, and that is the sanctioned answer, not a silenced
finding:** every consumer of the new module is `CMP-006`, the component
`LLR-197` tags it, so no cross-component edge exists for
`docs/kernel-modules-allow` to cover. `station.py`'s deliberate absence is the
precedent; the WI-440 multi-membership advisory surfaces the module if that
changes.

**ONE COPY DISAGREEMENT FOUND.** `trace.LLR_EXEMPT` was a `tuple`,
`spine_rules.LLR_EXEMPT` a `set`; the pin compared `set(a) == set(b)`, so the
type never entered the assertion — structurally blind, the slice-1 shape again.
The one home is a `frozenset`, and the type is now pinned. `sn_draft_ids` is the
one member that could NOT move — its body delegates to `spine_carrier`, which
this package may not import — so its duplicate is retired the other way: both
modules bind the sibling function directly, and the two wrappers disappear.

**Measured** (the slice-1 command, both revisions; `fig:` marker in
`docs/log.d/2026-08-23-wi448-spine-policy-pair.md`): duplicated function-body
groups 15 -> 6, redundant copies 15 -> 6, redundant lines 202 -> 76. The
`[dupes-census]` baseline is re-stamped down to match, and `trace.py`'s
module-size ratchet down 5460 -> 5373.

### SLICE 4 LANDED 2026-08-23 — item 4, the residual groups; census 0/0/0

**Landed.** All six groups the standing census reported, plus four copies it
could not see, take existing themed homes — **no new `kitlib` module, no
`MAPPING` change**, which is the smallest-total-code answer D-8 asks for and the
answer slice 2 gave for the console guard. `_process_check` (2 homes) joins
`kitlib/config.py`, the theme that already owns declared-policy files. The
multi-ref cell split (6 homes), the `-000` placeholder test (`is_example`'s
third home, the one slice 3 left standing) and the module-path key
`norm_module`/`MODULE_EXTS` (4 homes) join `kitlib/spine.py`, the theme that
already owns what a registry row's cells MEAN. The shared `k = v` block
renderer joins `kitlib/evidence.py` as `render_fields`, taking the differing
`FIELDS` and `_fmt` as arguments (`stage.py` already imports `evidence.py`, so
the direction is unchanged). `wi_convert`'s two spec-folder readers re-export
`kitlib/registry.py`'s — the WI-504 both-roots union is untouched, because that
is a READER concern and `wi_convert` is the WRITER. The two root-relative
need-row wrappers could NOT enter `kitlib` (they delegate to `spine_carrier`, a
sibling this package may not import) and are retired the way slice 3 retired
`sn_draft_ids`: the carrier grows `needs_for_root` and both modules bind it
directly. CLI behaviour is byte-identical; every former name is re-exported
under its original spelling.

**Six `test_rule_sync` equality pins retire** with the reasoning recorded in
their place; four replacements land — two IDENTITY pins (the deletions' warrant)
and two by-VALUE batteries, including a NEW one for the module key, which had
four homes and no pin at all.

**THREE FINDINGS, all recorded in the log fragment.** (a) A copy's stated reason
for existing did not describe the copy: `_process_check`'s docstring claimed the
`[checks]` POLICY — "which key, which fail-direction, which residual" — was the
module's, but the key is a PARAMETER and the other two were hardcoded
identically in both bodies. (b) `check_trajectory._MODULE_EXTS` promised it was
"kept in sync with `trace.py._MODULE_EXTS`", a name `trace.py` has never
carried — a sync claim with no referent, while its real second copy went
unmentioned. (c) THE CENSUS IS BLIND to a copy that renames the constant it
reads: `norm_module`'s fourth home spelled the tuple `MODULE_EXTS` where two
others spelled it `_MODULE_EXTS`, and the census hashes the body AST including
the loaded NAME, so three homes scored as two. Not fixed — widening the hash to
ignore loaded names would group functions that genuinely read different tables.

**Measured** (`check_dupes_census.py`, both revisions; `fig:` marker in
`docs/log.d/2026-08-23-wi448-residual-groups.md`): duplicated function-body
groups 6 -> 0, redundant copies 6 -> 0, redundant lines 76 -> 0. The
`[dupes-census]` baseline is re-stamped down to `0/0/0` — empty for the first
time since OI-58 armed it, and a READING rather than a floor: the check stays
armed and warn-first, so a future duplicate re-appears as a WARN against zero.
`check_trajectory.py`'s module-size ratchet is re-stamped down 4791 -> 4765.

**Deferred deliberately:** item 2 did not ride. Every home this slice touched is
a cell-shape or declared-policy-file theme; the open-items key vocabulary landed
nowhere near it, and taking it would have meant inventing a theme to carry one
constant.

**STILL OWED BY THIS ROW — the reason it is not closed:**

1. ~~**`_utf8_console`, 33 remaining copies**~~ — **LANDED 2026-08-22** (slice 2,
   above). Was 268 of the residual redundant lines, the single largest item.
2. **`bootstrap`'s OTHER declared duplicate** — `STACK_OI3_ROW` plus its TOML
   row emitter, which the OI-16 blast radius names. Shedding it needs the
   open-items key vocabulary in `kitlib` first. Note that its pin's stated
   premise ("bootstrap runs BEFORE the kit is copied and can import no
   sibling") is exactly what slice 1 overturned, so the comment on
   `test_rule_sync.test_bootstraps_scaffolded_brief_uses_the_converters_own_keys`
   is now stale and must be corrected when the duplicate goes.
3. ~~**The `spine_rules`/`trace` spine-policy pair**~~ — **LANDED 2026-08-23**
   (slice 3, below).
4. ~~**`is_example`**, `_process_check` x2, `_norm_module` x2, `sn_rows` x2,
   `_split_tokens`/`split_refs` x2, and `wi_convert`'s `spec_paths` /
   `work_dir_for` variants~~ — **LANDED 2026-08-23** (slice 4, above). Census
   0/0/0.
5. ~~**The `views` theme slot**~~ — **NOT OWED WORK, and the honest reading is
   recorded rather than the slot left ambiguous.** This item records two facts,
   neither of which is a deliverable. `station` LANDED 2026-08-20 from the
   successor decomposition program (WI-483), which needed the lane-close
   terminal-outcome vocabulary below both its readers to cut a
   view-into-coordinator import; it took its own single-component design row
   rather than joining this package's tag, and nothing about it is outstanding
   here. `views` is a theme the adopted H-09 shape NAMES and the package roster
   deliberately leaves uncreated, on its own stated rule that an empty module is
   a worse statement than an absent one. Creating it would be the defect, not
   the close. Nothing to build; the slot is filled if and when a render helper
   needs a home below two consumers.

**AFTER SLICE 4 THIS ROW OWES EXACTLY ONE THING: item 2.** It is not closed
because that item is real executable work (the `STACK_OI3_ROW` duplicate and its
TOML row emitter, the open-items key vocabulary it needs in `kitlib` first, and
the stale-premise comment correction the spec ties to it), not because anything
else on this list is unresolved.

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
