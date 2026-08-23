+++
id = "WI-499"
title = "Retire the word 'ratification' for 'approval' across the live kit (owner-ruled 2026-08-21) - reviewed campaign, records untouched"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed the owner's 2026-08-21 ruling ("ratification holds a weight to it
that the semantics here don't need") as a reviewed campaign: a case-preserving
mechanical rename over a scope derived from `check_vocab.py`'s own historical/
generated carve-out list (the WI's own instruction — "match check_vocab.py's
existing retired-vocabulary pattern"), followed by hand review of every
diff-shaped surprise the mechanical pass produced.

**Site census.** 141 live files changed. `docs/ratify/` (dated briefs) and
`docs/requirements/open-items.toml` (ruled rows are records; the one pending
row, OI-60, uses "ratified" in its ordinary-English sense — "confirmed by
construction" — not the kit's gate vocabulary, and is left as-is) were the
records excluded per the WI's own rule. `docs/log.md`, `docs/log.d/**`,
`docs/archive/**`, `docs/reviews/**`, `docs/plans/**`, `docs/rubrics/**`,
`docs/handbacks/**` and the terminal `docs/work/{complete,cancelled,partial}/`
folders (check_vocab's standing historical carve-outs) were left untouched —
history keeps its vocabulary. `check_vocab.py --root . --strict`: 0 findings
across 428 live authored files (the `ratif*` word family joins its
`RETIRED_TAG_RE`, riding the same enforcer as the `G*` tags, with a carved-out
exception for the literal `docs/ratify/` path in all its spellings — the one
string, the split-literal `Path("docs") / "ratify"` idiom, and a
markdown-relative `ratify/...` link).

**Identifier/CLI renames** (loud-shim discipline not needed — nothing here
ships as a spelling an adopter's own scripts import, so a plain rename is the
WI-498 discipline's own answer for this class): `agent_common.ratification_through`
→ `approval_through`; `RATIFICATION_RUNGS`/`RATIFICATION_FALLBACK`/
`LEGACY_RATIFICATION` → `APPROVAL_DIAL_RUNGS`/`APPROVAL_FALLBACK`/
`LEGACY_APPROVAL` (see the naming-collision note below); `trace.py --ratify`
→ `--approve`; the `ratify-fresh`/`ratify-immutable` harness steps →
`approval-fresh`/`approval-immutable`; WI-503's `--mint-ratify-brief`/
`current_ratify_brief`/`--ratify-immutable` → `--mint-approval-brief`/
`current_approval_brief`/`--approval-immutable`. One test file renamed:
`tests/test_ratification_level.py` → `tests/test_approval_level.py`.

**A real naming collision the mechanical pass caused, found and fixed.**
`agent_common.py` already had an OFF-SPINE `APPROVAL_RUNGS` dict (OI-30 D3,
2026-08-15) distinct from the dial's own `RATIFICATION_RUNGS` frozenset; the
blind rename collapsed both onto `APPROVAL_RUNGS`, and Python's module-level
execution order meant the SECOND definition silently won — `approval_through`
was checking dial values against the wrong table's keys (registry names, not
rungs) for every value that was not the shipped default, degrading every
non-default dial reading to the fail-closed fallback with no warning. Caught
by hand-testing the legacy-key migration against a real scaffold (below), not
by any test — a genuine "site relies on a distinction" case the WI's own
premise-check called for. Fixed by renaming the dial frozenset to
`APPROVAL_DIAL_RUNGS`, leaving the pre-existing off-spine `APPROVAL_RUNGS`
dict exactly as it was named before this WI. `tests/test_approval_level.py`'s
two assertions that had silently started reading the wrong global (and
therefore no longer proved anything about the dial vocabulary) were repointed.

**`docs/ratify/` directory: kept its name**, per the WI's own recommendation —
it is a record home for the immutable dated re-attestation briefs already
there; renaming it would misdate a record for no gain. Everything that talks
ABOUT the directory (flags, step names, docstrings) now says "approval";
`docs/ratify/README.md` states the decision explicitly. `docs/ratify/CURRENT.md`
was regenerated (it is a generated view, not hand-edited) after the source
registry cells it quotes were renamed.

**The dial migration** (`human_ratification_through` → `human_approval_through`):
`bootstrap._migrate_dial_key_name` (new), called before `_migrate_dial_ordinal`
in `migrate_legacy_config` so a repo on BOTH the retired key name and the
retired 0-4 ordinal gets both fixed by one `--migrate-config` pass.
`agent_common.approval_through` reads the old key as a loud, per-call fallback
(the WI-493 read-translate-warn precedent) when the new key is absent.
Verified against a REAL bootstrapped scaffold (scratchpad, deleted after):
wrote the old key with a rung value, a retired-ordinal value, and both at
once; `approval_through` read each correctly and printed the expected
warning each time; `--migrate-config` rewrote the key (and, where present,
the ordinal) in one pass, leaving the value's MEANING unchanged. A
`RESYNC_PACK.md` entry (`### "Ratification" retires for "approval"...`,
anchored `[since 7e898d15]`) documents the same procedure for adopters.
`docs/process.toml`'s stale `THIS REPO RUNS EVERY-TIER-HUMAN-HELD` comment
(a superseded 2026-08-14 directive contradicting the live `DevStg-Needs`
value) was corrected in the same edit.

**Spine cells.** SR-139's `requirement`/`rationale` cells (the WI-501
coordination note asked this row to independently re-check for a possible
third/fourth dirty cell): re-checked — the mechanical rename swept the two
cells WI-501 had explicitly left for this row (`requirement`/`rationale`
carried "ratification"/"ratifies"/"ratifying"); no further dirty cell found.
This and every other Approved spine cell the mechanical pass touched (32 SR/
LLR/TC rows carrying the word in title/requirement/rationale/detail/expected/
method text — pure terminology, no obligation changed) rode this session's
`intake.py snapshot --approves` under the owner's own 2026-08-21 ruling as
the approval act (the WI-501/OI-53 tracked-repair precedent). Before/after:
`trace.py --strict --strict-integrity` — `integrity=0` unchanged; no new
orphan or citation-frame finding. No cell was stopped on: every touched cell
was a same-meaning word swap, not a fact in question.

**Byte deltas** (byte-budget-guard convention; `wc -c` before → after):
`CLAUDE.md` 7,831 → 7,827 (-4, headroom 673/8,500); `project-trajectory/AGENTS.template.md`
9,980 → 9,980 (0); `project-trajectory/PROCESS.md` 85,889 → 85,862 (-27,
watched, shrank — the §6 decision-surfacing-dial wording had to move off
"human approval"/"the human approves" once the rename made it collide with
§4's gate-authority claim, `test_gate_policy.py`'s restatement-dedup
tripwire; see below); `project-trajectory/PROCESS_OPTIONS.md` 177,704 →
177,666 (-38, watched, shrank — same collision, one throughput-caution
sentence reworded); `project-trajectory/skills/byte-budget-guard/SKILL.md`
4,834 → 4,825 (-9, headroom 175/5,000; re-stamped, source + both tracked
copies). `tests/test_bootstrap.py -k "byte_caps or size_budget"`: 2 passed.

**A second real collision, caught by the full suite, not by review.**
`test_gate_policy.py::test_gate_authority_stated_at_most_once_per_shipped_file`
reds if the phrase "human approve(s)" appears more than once per shipped
prose file — one canonical gate-authority claim (§4), referenced elsewhere.
The word rename collapsed two PREVIOUSLY-DISTINCT phrasings into the same
words: PROCESS.md §6 said "the driver pauses for human ratification" and "the
human ratifies even medium calls" for the UNRELATED decision-surfacing dial
(explicitly not the gate-authority claim, per the test's own comment); once
"ratification"/"ratifies" became "approval"/"approves", both sentences
silently started asserting the SAME claim the test guards against duplicating.
Reworded §6 to "a human decision" / "the human decides" (§6's own existing
phrasing already used "human decision" once, so this is now internally
consistent) rather than reverting the rename. Same root cause in
PROCESS_OPTIONS.md's throughput-caution note ("one human ratifies" → "one
human approves", now a second restatement of §4's claim beside the
gate-authority table's own "a human approves each gate"); reworded to "one
approver works the queue". This is the SAME class of finding as the
`APPROVAL_RUNGS`/`APPROVAL_DIAL_RUNGS` collision above — a site that relied
on two DIFFERENT words for two different concepts, which the rename made
identical without a human noticing until an existing structural test caught
it.

**Module-size ratchet** (a mechanical rename touches comments/identifiers
across many scripts, and three modules crossed a line-count baseline; each
re-stamped with a reason in the same commit, per the ratchet's own rule):
`agent_common.py` 2,597 → 2,627 (+30); `bootstrap.py` 3,054 → 3,109 (+55);
`check_trajectory.py` 4,637 → 4,645 (+8).

**Deviations from spec:** none in scope — the spec's four bullets are all
executed as written. The naming-collision fix above was not anticipated by
the spec but is squarely inside "verify no site relied on a ratify-vs-approve
distinction" (the collision WAS such a site, just not the kind the spec's
author expected).

**Gates.** `check_vocab.py --root . --strict`: clean (428 live files). Full
`check.py --run-steps okf,trajectory-map,status-map,open-items,trajectory,
registry-integrity,derived-stage,skills-sync,skills-index,prompt-catalog,
approval-fresh`: all PASS. `check_docs.py --root . --stale`: OK, 1025 docs,
1354 links, 0 broken (1 orphan warning — pre-existing on the unmodified
baseline, unrelated to this WI). Smoke tier
(`python -m pytest -q -n auto -m smoke`): 1265 passed, 5 skipped, 19-22s
across runs, well under the 60s budget (`check_smoke_budget.py --mode
enforce` confirmed). Full suite, run twice: the first run reddened exactly
one test (the PROCESS.md/PROCESS_OPTIONS.md collision below) — 2898 passed,
14 skipped, 1 failed; after the fix, **2899 passed, 14 skipped, 0 failed,
1031.22s (0:17:11)**. See the session log fragment for both pasted runs.

Deferred open items: none — both collisions (the `APPROVAL_RUNGS` naming
collision and the gate-authority-restatement collision) were found and fixed
inside this session, not deferred; nothing here is left for the owner to
decide.

## Context

Owner ruling (2026-08-21, in-session): "ratification holds a weight to it
that the semantics here don't need" — the kit's vocabulary unifies on
**approval**. The ruling is the direction; this row is the reviewed
campaign, NOT a blind mass-replace, because the slice-5 recovery proved
exactly what a mechanical sweep does to records.

Scope, in the WI-498 sweep's proven shape:

- **Live prose and instructing surfaces** (PROCESS.md, PROCESS_OPTIONS.md,
  skills, templates, README, docstrings): ratification/ratify → approval/
  approve, reviewed line by line. One semantic check per site: the kit
  already uses "Approved" as a Status value and "approval" for the human
  gate — verify no site relied on a ratify-vs-approve distinction (if one
  genuinely does, keep it and record it; the owner's premise is that none
  should).
- **Code identifiers and CLI surface**: `agent_common.ratification_through`
  and friends, `trace.py --ratify` and its `ratify-fresh` step,
  `docs/ratify/` (the directory is a RECORD home — the directory may keep
  its name or move with a redirect note; decide by the records rule below),
  test names. Renames land with the same alias discipline WI-498 used
  (loud shims where an adopter-facing spelling changes).
- **The dial key `human_ratification_through`** is adopter-declared config:
  rename to `human_approval_through` with the bootstrap migration path
  (the WI-493/`migrate_legacy_config` precedent), a loud legacy-key read,
  and a RESYNC_PACK entry.
- **Records untouched**: docs/log.md, docs/log.d fragments, docs/archive/**,
  closed WI specs, ruled OI rows, ratify records under docs/ratify/ —
  history keeps its vocabulary (the slice-5 recovery's reverted-hunks
  lesson: a rename must never rewrite a record of the past). check_vocab
  gains the retired-spelling entry for LIVE surfaces only.
- Byte-capped docs measured before/after (byte-budget-guard convention).
  Scaffold-surface changes verified by BOOTSTRAPPING A REAL SCAFFOLD;
  full RESYNC entries.
