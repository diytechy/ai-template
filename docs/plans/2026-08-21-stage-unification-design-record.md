# The stage unification design record — bar/gate/stage collapse onto one axis

**Status: owner-agreed DIRECTION (2026-08-21), not yet a ruled program.** The
owner: "Agreed this needs a redesign, but I want to be careful with it since
it will be quite large… one of the most important parts of this repository is
to remove duplicity / contain a single owner, and I'm nervous right now this
gate / phase logic is getting spread everywhere." This document is the full
findings summary that conversation asked for — the design record that the
OI-51 ruling and its program row(s) will cite. The three measurement docs
behind it, each with driven demonstrations:

- [2026-08-21-bar-vs-stage-census.md](2026-08-21-bar-vs-stage-census.md) —
  which semantics 91 sites actually check
- [2026-08-21-stage-rekey-deep-check.md](2026-08-21-stage-rekey-deep-check.md)
  — corner cases of at-or-above; the vacant rung; the carrier options
- [2026-08-21-gate-schedule-map.md](2026-08-21-gate-schedule-map.md) — when
  the gate is computed vs read; the stale windows

## 1. The problem, in one file

`docs/gate` carries TWO different numbers that can spell the same word:

- the **value line** — the BAR: the min over every row's bar, floored; "the
  strictness selector; the bar that must next be CLEARED"
- the **`stage=` basis field** — the STAGE: the rung actually in work on the
  eight-rung ladder

On this repo both read `DevStg-Reqs` today, by different arithmetic. On a
settled spine they diverge outright (bar ceilinged at `DevStg-Tests` by the
OI-30 D2 rule; stage reading `DevStg-Release`). And the constant that names
the top bar is `BAR_RELEASE = "DevStg-Impl"` (`check.py:983`) — a name from
one ladder bound to a spelling from the other. The owner's OI-51 confusion
was not a reader error; it is the vocabulary.

## 2. What the measurements established

1. **Semantics split by module, cleanly** (census, 91 sites): 55
   bar/clearance, 27 current-stage, 9 mixed. Everything that selects CHECKS
   is bar-keyed (`check.py` reads the stage nowhere); everything that decides
   RATIFICATION AUTHORITY is already stage-keyed. The owner's preferred rule
   is fully implemented on exactly half the kit.
2. **Stage rung 6 (`DevStg-Impl`) is VACANT** (deep-check, driven): the
   closed Status enum makes `spine_stage`'s Impl discriminator unreachable —
   a legal fully-decomposed spine jumps `DevStg-Tests` → `DevStg-Release`.
   Already pinned "named for the sitting" (`test_ratification_level.py:359`).
3. **Impl vs Release changes NO behavior anywhere** (verified 2026-08-21):
   `DevStg-Release` sits outside the derived bar range entirely — "not
   clearable", no step tagged at it (`derive_gate.py:139-145`,
   `check.py:982`); `DIAL_HOLDS` holds rungs 6 and 7 identically at every
   dial level (driven, all 5 × 8). Only display strings
   (`traj_status.py:367`) and test pins distinguish them. The ladder
   DESCRIBES a distinction nothing ACTS on — so redrawing the top of the
   ladder is behaviorally free.
4. **At-or-above is a valid operator; the raw `stage=` value is not a valid
   operand** (deep-check, nine real corner cases): one Drafted row drops the
   raw stage from ord 7 to as low as ord 0 (tier-dependent, no floor, no
   ex-draft analogue — C-01 reproduced on the stage axis, the WI-473 floor
   typed to bars and unable to help); NO per-phase stage exists (the global
   stage is already a min over phases); a fresh scaffold reads ord 0 (would
   run nothing); `DevStg-Below` raises under ordering; hyphenated labels
   truncate to a DIFFERENT VALID RUNG (the unsafe direction); and
   `DevStg-Impl` is legal on BOTH ladders with different ordinals, so
   neither guard can refuse the other's value. Counterpoint: the feared
   membership→threshold selection change measures at exactly one
   duplicative 1.5 s step.
5. **The "clearance-needing" behaviors reduce to events + one derivation
   rule** (owner's insight, verified against the census's own four):
   - the phase-drop detector compares the current per-phase level against a
     RECORDED ANCHOR — downward-movement event detection over history, not
     a second axis;
   - `tier_signal`/`_gate_moved` is a two-point delta between git trees —
     same, and currently BROKEN (always-False since the derived-gate
     migration; queued as WI-497);
   - the ratification acts' "clearance" half is the TRANSITION RECORD (the
     reviewed Status-change commit already is one); their selection is
     already stage-keyed;
   - the OI-30 D2 ceiling is a DERIVATION constraint ("the top rung requires
     evidence, not statuses"), which is exactly the owner's stated Release
     rule, moved inside the derivation.
   Nothing requires a separate bar VOCABULARY: every A-column site is a
   selector (at-or-above replaces it), an event detector (history of one
   value replaces it), or a derivation rule.
6. **The gate is a committed cache and its scheduling is sound ON TRUNK**
   (schedule map): one writer (`derive_gate.py`, production-called only by
   `trunk_step.regen` on the trunk lane), freshness enforced at all three
   bars by a `--check` that RECOMPUTES from the live registries — no green
   run or commit lands stale on trunk. Readers: 2 protected, 6
   windowed-but-self-correcting, 1 broken (WI-497), 1 dead
   (`read_declared`, documented as the gate's reader, called on it
   nowhere). Two latent windows, both inert at this repo's dial 4: claimed
   work branches SKIP the freshness step by design (falsifying
   `spine_stage_of`'s written trust invariant), and `agent_loop`/`dispatch`
   hoist the stage once per run while their own merges regenerate it
   beneath them.
7. **"All test cases passing" has NO evidence source today**, at four
   independent points: the TC schema carries no outcome key BY RULING
   ("whether the tests pass is the harness's answer, not a cell's");
   `docs/test/`'s reports are gitignored; `coverage.json` is opt-in,
   gitignored, deleted per run; no junit/json-report exists anywhere. The
   evidence carrier is the real build inside the redesign; the
   discriminator swap itself is cheap.

## 3. The DevStg enum: where the vocabulary is sourced

The owner asked for the list and its homes. The strings appear **648 times
across 64 files** under `project-trajectory/` alone (plus this repo's own
docs/ instance). The DEFINITIONS — the places that state what the
vocabulary IS — are:

| Home | What it defines | Form |
|---|---|---|
| `derive_gate.py:552-574` | `STAGE_NEEDS`…`STAGE_RELEASE`, `STAGE_ORDER` (the eight-rung ladder), `STAGE_OF`, `STAGE_DESC` | the intended SSOT for the STAGE axis |
| `derive_gate.py:151-171` | `BAR_BELOW/REQS/TESTS/RELEASE` as ORDINALS 0-3 + `BAR_NAMES` ordinal→string + its own `BAR_ORDER` | the BAR axis, ordinal form |
| `check.py:983-985` | `BAR_REQS, BAR_TESTS, BAR_RELEASE = "DevStg-Reqs", "DevStg-Tests", "DevStg-Impl"` + `BAR_ORDER` + `GATES` | LITERAL RESTATEMENT — string constants duplicated, incl. the Release-name/Impl-value bind |
| `agent_common.py:554-565` | `LADDER_RUNGS` — the eight rung strings as a literal frozenset ("restated here and pinned equal to `derive_gate.STAGE_ORDER` by tests") + `DIAL_HOLDS` + `APPROVAL_RUNGS` | LITERAL RESTATEMENT, held by pin |
| `derive_gate.py:1000-1017` | `STAGE_BAR` — the stage→bar crossing table | pinned by a test, called by NOTHING in production (census runner-up finding) |
| `check_vocab.py:100-109` | the alias-resolution tables (`G3`, `G-Release`, `DevBar-Release` → current spellings) | the migration shim from the PREVIOUS vocabulary generation |

Held together by: `tests/test_ratification_level.py` (pins the restatements
equal), `check_vocab.py` (polices retired spellings in prose), and the
2026-08-18 one-vocabulary rename's conventions. Everything else — the other
~60 files — CONSUMES the strings (step `gates=` tags in `stack.ini` +
template, `docs/gate` + `gate.template`, `process.toml` dials, PROCESS.md §4
prose, skills, RESYNC entries, WI spec `bar:` lines, test fixtures).

**The single-owner verdict the owner asked for:** the VALUES being widely
consumed is unavoidable and fine; the SEMANTICS being defined in four code
homes (plus a crossing table and an alias shim), held equal by test pins
rather than by one import, is exactly the accreted duplication this repo's
own doctrine refuses — it predates `kitlib`, and the D-7-era pins-over-
extraction choice is what left it this way. The redesign's cheapest
structural win is independent of everything else: ONE enum home (the
`kitlib` package WI-448 created is the sanctioned landing), everyone
imports it, the pins retire because drift becomes unrepresentable — the
same move the WI-448 close already executed for the declared-line readers.

## 4. The agreed design direction

One axis, one vocabulary, one owner. The shape (each element traced to the
finding that motivates it):

1. **`derive_stage` replaces `derive_gate`; `docs/stage` replaces
   `docs/gate`.** The headline value is the EFFECTIVE STAGE. Eight readers
   re-key in one commit (the deep-check's Q3 prices the carrier options;
   `check.py` hard-exits on unknown values, so the flip is loud, never
   silent). The comment-scrape reader retires.
2. **The effective stage is DESIGNED, not the raw field** (finding 4):
   per-phase (none exists today), draft-excluded (the ex-draft analogue —
   "the stage the settled spine has earned", drafts reported beside it,
   never silently lowering selection), floored, `DevStg-Below` and
   fresh-scaffold cases defined. This is slice 1; everything hangs off it.
3. **Selection is at-or-above the effective stage** (the owner's rule).
   Each step's `gates=` membership set is re-derived deliberately into a
   from-stage threshold — mostly mechanical, one step's meaning genuinely
   moves (`registry-integrity`, measured duplicative).
4. **The ladder re-discriminates** (findings 2, 3, 7): all-Founded → the
   repo is IN `DevStg-Impl`; `DevStg-Release` requires ALL TEST CASES
   PASSING — reachable only from the evidence carrier, which must be built
   (the OI-30 D2 "harness driver", stage-axis half; `spine_stage`'s own
   docstring already owes the swap). Until the carrier exists, Release is
   simply unreachable — honest, and matches the owner's intent. The D2
   guard survives intact as a derivation rule: no status cell can ever
   claim the evidence passed.
5. **The event detectors re-express over stage history** (finding 5): the
   phase-drop detector compares against recorded per-phase anchors; the
   tier signal is a two-point delta of the committed file (and gets FIXED —
   WI-497). No "clearance" vocabulary remains.
6. **One enum home in `kitlib`** (§3): the ladder, its order, its
   descriptions; `check.py`/`agent_common`/`check_vocab` import it; the
   equality pins retire; `STAGE_BAR` and the bar constants are deleted with
   the axis.
7. **Migration**: RESYNC_PACK entries (adopters re-key `docs/gate`,
   `gates=` tags, `bar:` spec lines); a `check_vocab` alias generation maps
   the retired bar spellings — which CANNOT be mechanical where spellings
   are shared across the two old axes (deep-check Q3), so the sweep is
   reviewed, not scripted; PROCESS.md §4 and the skills re-teach the single
   vocabulary; WI-493 (the dial re-key to DevStg strings, deferred) folds
   in.

**Care constraints the owner set, recorded:** it will be QUITE LARGE — run
it as a program row with slices, each slice ending green at the commit bar;
the corner-case list in the deep-check is the acceptance checklist for
slice 1 (each of the nine becomes a driven test); the duplication VERDICT
(§3) means slice ordering should put the one-enum-home extraction early,
since every later slice touches the vocabulary and should touch it in one
place. Findings that ride along regardless of the program: WI-497 (the
broken tier signal), the dead `read_declared`, the branch-lane trust
invariant mismatch (re-document vs arm — the owner's call, still open).

## 5. What this record is not

Not a ruled program: OI-51 is still PENDING, and this direction supersedes
the narrow (a)-vs-(e) framing there — the ruling should land on THIS shape
(with or without the three-tag interim protection, the owner's call). Not a
spec: the program row(s) minted at ruling carry the executable slices. Not
a claim that the current system is broken: on the trunk the gate contract
holds and every stale read self-corrects; what this record establishes is
that the two-axis vocabulary is duplicated, partially vacant, behaviorally
indistinguishable at its top, and confusing to its owner — and that one
designed axis can carry everything it does.
