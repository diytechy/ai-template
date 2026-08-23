## 2026-08-23 — WI-499: "ratification" retires for "approval" across the live kit

Executed the owner's 2026-08-21 ruling ("ratification holds a weight to it
that the semantics here don't need") as a reviewed campaign, not a blind
mass-replace: a case-preserving mechanical rename scoped to `check_vocab.py`'s
own historical/generated carve-out list (the WI's own instruction), followed
by hand review of every diff-shaped surprise the mechanical pass produced —
and it produced several, caught before commit rather than after.

**Site census.** 141 live files changed. Excluded as records, per the WI's
own rule: `docs/ratify/` (the dated re-attestation briefs), and
`docs/requirements/open-items.toml` in full — its 23 RULED rows are history
in the vocabulary they were ruled in, and its one PENDING row (OI-60) uses
"ratified" only in the ordinary-English sense ("confirmed by construction"),
not the kit's retired gate word, so it needed no edit either way.
`docs/log.md`, `docs/log.d/**`, `docs/archive/**`, `docs/reviews/**`,
`docs/plans/**`, `docs/rubrics/**`, `docs/handbacks/**` and the terminal
`docs/work/{complete,cancelled,partial}/` folders (check_vocab's standing
historical carve-outs) were left untouched — history keeps its vocabulary,
the slice-5 recovery's lesson written into the WI's own spec.

**Identifier/CLI renames**, no shim needed (nothing here is a spelling an
adopter's own scripts import): `agent_common.ratification_through` →
`approval_through`; `RATIFICATION_RUNGS`/`RATIFICATION_FALLBACK`/
`LEGACY_RATIFICATION` → `APPROVAL_DIAL_RUNGS` (renamed further than a literal
swap — see the collision below)/`APPROVAL_FALLBACK`/`LEGACY_APPROVAL`;
`trace.py --ratify` → `--approve`; the `ratify-fresh`/`ratify-immutable`
harness steps → `approval-fresh`/`approval-immutable`; WI-503's
`--mint-ratify-brief`/`current_ratify_brief`/`--ratify-immutable` →
`--mint-approval-brief`/`current_approval_brief`/`--approval-immutable`.
`tests/test_ratification_level.py` → `tests/test_approval_level.py`.

**A real naming collision, found and fixed.** `agent_common.py` already had
an off-spine `APPROVAL_RUNGS` dict (OI-30 D3, 2026-08-15), distinct from the
dial's own `RATIFICATION_RUNGS` frozenset. The blind mechanical rename
collapsed both names onto `APPROVAL_RUNGS`; Python's module-level execution
order let the SECOND definition (the off-spine dict) silently win, so
`approval_through` was checking a dial value against the wrong table's keys
(registry names, not rungs) for every value that was not the shipped
default — degrading every non-default dial reading to the conservative
fallback with no warning. Caught by hand-testing the legacy-key migration
against a real bootstrapped scaffold, not by any test (the two assertions in
`test_approval_level.py` that should have caught it had themselves been
silently repointed at the wrong global by the same mechanical pass). Fixed:
the dial frozenset is now `APPROVAL_DIAL_RUNGS`; the pre-existing off-spine
dict keeps the name `APPROVAL_RUNGS` it already had. This is the "verify no
site relied on a ratify-vs-approve distinction" check the spec called for —
just not the kind of distinction its author anticipated.

**A second bug from the same mechanical pass, found and fixed:** three
`Path("docs") / "ratify"` split-literal directory constructions (`trace.py`,
five test files) got their bare `"ratify"` literal swept to `"approve"` even
though the sentinel-protected `"docs/ratify"` single-string form was
correctly preserved elsewhere — `trace.py --approve modified --check` failed
against `docs\approve\CURRENT.md` before this was caught and fixed. A
markdown-relative link (`docs/repo-lock.md`, written as `ratify/...` from a
doc already under `docs/`) had the same defect for the same reason and was
fixed the same way.

**`docs/ratify/` directory: kept its name**, per the WI's own
recommendation — a record home for the immutable dated briefs already there;
renaming it would misdate a record for no gain. Everything that talks ABOUT
the directory (flags, step names, docstrings) now says "approval";
`docs/ratify/README.md` states the decision. `check_vocab.py`'s new
`ratif*`-retirement rule (riding `RETIRED_TAG_RE`, the same enforcer as the
`G*` tags) carries three carve-outs for this one surviving spelling: the
`docs/` lookbehind, a `/` lookahead for the relative-link form, and a quote
lookaround for the split-literal Python idiom.

**The dial migration** (`human_ratification_through` → `human_approval_through`,
adopter-declared config): `bootstrap._migrate_dial_key_name` (new), called
before `_migrate_dial_ordinal` in `migrate_legacy_config` so a repo on BOTH
the retired key name and the retired 0-4 ordinal gets both fixed in one
`--migrate-config` pass. `agent_common.approval_through` reads the old key as
a loud, per-call stderr warning (the WI-493 read-translate-warn precedent)
when the new key is absent. Verified against a real bootstrapped scaffold
(built via `bootstrap.py --dest`, scratchpad, deleted after): the old key
with a rung value, with the retired ordinal, and with both together —
`approval_through` read each correctly and warned each time;
`--migrate-config` rewrote the key (and, where present, the ordinal) in one
pass, value's meaning unchanged. `RESYNC_PACK.md` gained an entry
(`### "Ratification" retires for "approval" across the live kit`, anchored
`[since 7e898d15]`). `docs/process.toml`'s stale `THIS REPO RUNS
EVERY-TIER-HUMAN-HELD` comment — a superseded 2026-08-14 directive
contradicting the live `DevStg-Needs` value — was corrected in the same edit.

**Spine cells.** SR-139's `requirement`/`rationale` cells (the two WI-501
explicitly left for this row) were independently re-checked per WI-501's
coordination note: swept clean by the mechanical pass, no further dirty cell
found. This and 31 other Approved SR/LLR/TC rows carrying the word in
title/requirement/rationale/detail/expected/method prose (pure terminology,
no obligation changed) rode `intake.py snapshot --approves "owner ruling
2026-08-21, docs/log.d/2026-08-21-owner-session-dial-and-folds.md -- WI-499
vocabulary rename"` — the WI-501/OI-53 tracked-repair precedent, the owner's
own ruling as the approval act. Before/after `trace.py --strict
--strict-integrity`: `integrity=0` unchanged, `orphans=7` unchanged (SR-163,
SR-177, SR-181, LLR-164 — all pre-existing, none touched here). No cell was
stopped on: every touched cell was a same-meaning word swap.

**Byte deltas** (`wc -c` before -> after): `CLAUDE.md` 7,831 -> 7,827 (-4);
`AGENTS.template.md` 9,980 -> 9,980 (0); `PROCESS.md` 85,889 -> 85,862 (-27,
watched, shrank); `PROCESS_OPTIONS.md` 177,704 -> 177,666 (-38, watched,
shrank); `byte-budget-guard/SKILL.md` 4,834 -> 4,825 (-9, re-stamped, source
+ both tracked copies). All capped files at or under cap;
`test_bootstrap.py -k "byte_caps or size_budget"`: 2 passed.

**A second real collision, caught by the full suite.**
`test_gate_policy.py::test_gate_authority_stated_at_most_once_per_shipped_file`
reds if the phrase "human approve(s)" appears more than once per shipped
prose file. PROCESS.md's §6 decision-surfacing-dial paragraph had said
"human ratification"/"the human ratifies" — deliberately a DIFFERENT word
than §4's gate-authority claim, per the test's own comment. The rename
collapsed both onto "approval"/"approves", so §6 silently started
re-asserting §4's claim. Reworded §6 to "a human decision"/"the human
decides" (consistent with a phrase §6 already used once) rather than
reverting the rename; same fix in `PROCESS_OPTIONS.md`'s throughput-caution
note ("one human ratifies" -> "one human approves", a second restatement
beside the gate-authority table's own "a human approves each gate") ->
"one approver works the queue". Same class of finding as the
`APPROVAL_RUNGS` collision above: two words for two concepts, made identical
by the rename, caught by an existing structural test rather than by review.

**Module-size ratchet**, three modules crossed baseline (comments +
identifiers, mechanical rename touches both), each re-stamped with a reason
in this commit: `agent_common.py` 2,597 -> 2,627 (+30, the dial-key migration
+ the collision fix); `bootstrap.py` 3,054 -> 3,109 (+55, `_migrate_dial_key_name`);
`check_trajectory.py` 4,637 -> 4,645 (+8, the two carve-out comments).

**Deviations from spec:** none — the spec's four bullets executed as
written; the two collision/split-literal bugs found along the way are
squarely inside "verify no site relied on a ratify-vs-approve distinction",
just not anticipated in that shape.

**Gates.** `check_vocab.py --root . --strict`: clean, 427 live authored
files (0 findings). `check.py --run-steps okf,trajectory-map,status-map,
open-items,trajectory,registry-integrity,derived-stage,skills-sync,
skills-index,prompt-catalog,approval-fresh`: all PASS. `check_docs.py --root
. --stale`: OK — 1025 docs, 1354 links, 0 broken (1 orphan warning,
pre-existing on the unmodified baseline). Smoke tier:
`python -m pytest -q -n auto -m smoke` — 1265 passed, 5 skipped, 22.23s.
`python scripts/check_smoke_budget.py --mode enforce`: 18.5s vs 60s budget —
within. Full suite, run TWICE: the first run (before the PROCESS.md/
PROCESS_OPTIONS.md collision above was found) reddened exactly
`test_gate_authority_stated_at_most_once_per_shipped_file` — 2898 passed, 14
skipped, 1 failed, 1047.81s. After the fix, a clean re-run:
`python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w499b` — **2899 passed,
14 skipped, 0 failed, 1031.22s (0:17:11)**
<!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w499b" rev=7e898d15-dirty -->
(environment note: `sh.exe` on PATH via Git Bash for the environment-gate
test).

Deferred open items: none — the naming collision and the split-literal bug
were both found and fixed inside this session, not deferred; nothing here is
left for the owner to decide.
