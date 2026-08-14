# Handoff — the 2026-08-08 mechanized-loop program

**Status:** the program is BUILT, TESTED and COMMITTED. What is open is
**judgement**, not construction. Nothing here is blocked on more code.

This document exists so a fresh session can pick up without re-deriving the
state. It is a *record surface*, not a working one — the working surfaces stay
[`docs/status.md`](../../status.md), the registries, and [`docs/log.md`](../../log.md).

---

## 1. Where things stand

Four commits on `infra/mechanized-loop`, implementing
[`plan-2026-08-08-mechanized-loop.md`](plan-2026-08-08-mechanized-loop.md):

| commit | what |
|---|---|
| `c560f928` | SN-028 — one policy home, `docs/process.toml` |
| `f862cc72` | SN-031/032 — prompts as files; the outcome model becomes terminal |
| `3de2c9bc` | SN-029 — the attestation ledger; ratification as an ordinal |
| `cb9c36ac` | SN-026/030 — loop order, ADJUDICATE routing, prompt audit, spine record |

**Measured bar at the last commit:** full unfiltered suite **2152 passed, 8
skipped**; `check.py` at the derived gate **PASS**; no unsanctioned duplicate
blocks; ruff clean; 380 docs / 1056 links / 0 broken.

**The derived gate is G1 on purpose.** `drafts=33 modified=38`. A `Draft` SN
reads G0, so the gate dropped — the "a new phase is due" signal `docs/gate`
exists to give. The code is built and tested; **the requirements behind it are
proposed, not accepted.**

Spine state by tier:

| registry | Verified | Modified | Draft |
|---|---|---|---|
| system-requirements.csv | 111 | 25 | 10 |
| low-level-requirements.csv | 131 | 6 | 10 |
| test-cases.csv | 128 | 7 | 8 |

---

## 2. THE OPEN DESIGN QUESTION — is `attestations.csv` the right shape?

This is the one to settle first, because SR-140 and part of SN-029 rest on it,
and rejecting it is a legitimate outcome.

### The objection, stated fairly

*Attestation is tracked per requirement row, not in a separate CSV.* That is
correct and still true: `Status = Verified | Modified` on an SR/LLR/TC row is
the attestation STATE, and `derive_gate.py` computes the gate from those cells
alone — it has **zero** references to the ledger. Nothing about how ratification
state is tracked changed. A second registry is in tension with the kit's own
single-source-of-truth doctrine, which it preaches loudly.

Note the word is overloaded three ways, which is part of why this is confusing:

| where | what it is |
|---|---|
| `Status = Verified \| Modified` | **the state** — is this ratified right now? |
| `Verification = Attest` (SR vocabulary) | **a method** — a human attests rather than a test verifying |
| `attestations.csv` | **the event** — what text was accepted, at which commit |

(The collision is why the new dial is `human_ratification_through` and not
"attest level" — a third meaning would have been permanent.)

### What the ledger was introduced to fix

Two gaps, both real, both verified in source:

1. **The SANCTIONED amendment path reached no consumer.** The baseline for
   "what text was attested" was derived by walking git for the newest commit
   where the row still read `Verified`. That is sound only if every amendment
   flips Status in the same commit — but `check_trajectory.staged_spine_amendments`
   *deliberately ignores* rows whose Status moved in that commit ("a deliberate
   call this does not second-guess"). So amend-text-and-flip-to-`Modified`-in-one-commit,
   the blessed path, was invisible, and a derived baseline could point at a
   commit whose text already carried an unratified change.
2. **SNs have no Status cell at all.** `stakeholder-needs.md` is not in
   `SPINE_CSVS`. There was no per-row mechanism to extend, so stakeholder prose
   had no anchor by any path.

### What it has cost so far

- **Zero real rows.** Only the `ATT-000` example. It is machinery with no data.
- It drove the **largest single module bump in the program** —
  `check_trajectory.py` +272 lines, making it the kit's largest module and the
  first WI-280 decomposition candidate.
- **Three of the eight BLOCKERs** the reviews found were in its own rungs
  (deleting the ledger silenced all three checks at once; a ledger row
  anchoring a nonexistent id read as perfectly clean; the append-only guard's
  rev-range arm is wired only for the staged case).

### The alternative that was NOT taken

**Narrow the detector instead of adding a registry.** Make
`staged_spine_amendments` stop ignoring same-commit Status moves — i.e. treat
amend+flip as a record to be examined rather than a deliberate exit. Then the
git-derived baseline becomes sound again and no second home is needed.

- **Costs:** the SN-prose anchor. SNs still have no Status cell, so gap 2 stays
  open with no other candidate mechanism. It also re-opens the question that
  exit was written to close — the seam exists to avoid flagging a deliberate,
  correctly-marked amendment as a finding.
- **Wins:** one home for one fact; ~272 lines and three BLOCKER-class rungs
  never exist; nothing new to keep fresh.

### A third option, if the sitting wants the middle

Keep the digest, drop the separate registry: put `TextDigest` and
`AcceptedCommit` as **columns on the spine rows themselves**. That keeps
one-row-one-home and still catches drift — but it is a schema change across
three F5-synced loaders, and it still leaves SNs (no row, no columns) unsolved.

### What to do

SR-140 and SN-029 are `Draft` and sit in the re-attest brief. **Ratifying,
amending, or rejecting them is the sitting's call.** If rejected, the removal is
mechanical: delete `attestations.csv` + its template, the three rungs in
`check_trajectory.py`, `trace._ledger_baseline`, `intake attest`, and the
scaffold rows — the ordinal and the spine-stage axis do not depend on it.

---

## 3. What the P0 sitting owes

The plan's §10 reserves ratification for a human sitting. It is unheld.

1. **Ratify / amend / reject SN-028..032** and their decomposition
   (SR-137..146, LLR-155..164, TC-150..157) — all `Draft`.
2. **Settle §2 above** (the ledger's shape).
3. **Work the combined re-attest brief:**
   [`docs/ratify/2026-08-08-mechanized-loop.md`](../../ratify/2026-08-08-mechanized-loop.md)
   — 25 `Modified` SR sections, each showing only its CHANGED cells,
   before/after. This combines the 21 rows already owed from 2026-08-07 with
   the rows this program amended.
4. **Then `intake.py attest`** the accepted set, so the ledger anchors it — *if*
   the ledger survives §2.

**Why those rows are `Modified`:** the program originally added 10 SRs, 10 LLRs
and 8 TCs and amended *nothing*, so ~19 `Verified` rows still described
machinery retired underneath them (`hand_back`, `## Handback`,
`docs/gate-policy`, `attended`/`single-ratify`, two TCs citing renamed tests).
A `Verified` row whose text is false is the worst thing this registry can carry.
They were amended and flipped to `Modified` — the state that says a fresh
ratification is owed.

---

## 4. Open work items (all `queued`, none blocked)

Ready frontier, in scheduler order:

| id | rank | what |
|---|---|---|
| **WI-390** | 0 (exclusive) | concurrency-v2 program close — pre-existing, not this program's |
| **WI-415** | 6 | process-tab ff-wording + the 390px legibility observation — pre-existing |
| **WI-422** | 6 | **measured dead-symbol sweep** (filed by this program) |
| **WI-423** | 6 | **decide the six unfolded check toggles** (filed by this program) |
| **WI-424** | 6 | **route the adjudicator briefs** (filed by this program) |

### WI-424 is the one with teeth

The four adjudicator templates (`adjudicate-amendment`, `-disposition`,
`-conflict`, `-red-tc`) are authored, shipped, catalogued — and **consumed by
nothing**. `agent_loop.route_session` composes every non-review session from the
generic worker prompt, so an adjudication row routes to the right model at the
right tier with the right cross-family rule and then receives an *implementer's*
instructions. The judge is briefed as a builder.

It was filed rather than fixed because it needs two decisions:

1. **The discriminator** — which brief a row wants is a typed fact the row does
   not carry. Either a new frontmatter key (honest, but a schema change across
   three F5-synced loaders) or derivation from `SpecRef` (free, but infers
   rather than declares).
2. **The slots** — each brief demands assembled EVIDENCE (`{baseline}`,
   `{mechanical}`, `{open_rows}`, `{spine}`, `{digests}`, `{evidence}`). Those
   are real derivations. **A half-filled brief is worse than the generic
   prompt**: a judge's brief with hollow sections reads as an investigation that
   was done and found nothing. That is the WI-418 rule this program just
   generalized, and it should not be broken by the pass that closed it.

Current cost is bounded and visible: a worse brief, not a wrong verdict path.

---

## 5. Known residue (deliberate, warn-only, not regressions)

None of these gate anything. Recorded so a fresh session does not treat them as
new.

- **3 dangling doc refs**, all pre-existing historical records:
  `docs/next-wi` (retired, explained in place) and `tests/test_stdlib_only.py`
  ×2 inside closed WI records.
- **7 declared figures missing provenance**, all in `WI-419`/`WI-420` records
  written before the `fig: cmd=… rev=…` convention was enforced.
- **~10 `check_trajectory` warns** — connectivity/seam advisories that predate
  this program.
- **The dual-plan hats are not in `prompts.KIT_PROMPTS`**, so
  `dual-plan-{planner,critic,arbiter}.template.md` are absent from `CATALOG.md`
  and from the per-session `prompt-sha` telemetry. Tracked in IF-100's Notes;
  it is a coverage gap in the audit trail, not a broken path.
- **The append-only ledger guard's rev-range arm is wired only for `--staged`.**
  A ledger rewrite committed with hooks bypassed passes the full checker. Fixing
  it properly needs a decision about how far back to compare; folded into §2's
  question, since it is moot if the ledger goes.
- **`intake` and `dispatch` are now mutually dependent** (`dispatch` imports
  `intake` at module scope; `intake` imports `dispatch` lazily). No cycle at
  runtime, but neither is independently copyable any more — worth a look if the
  F5 rule is ever extended to them.

---

## 6. Environment notes (this machine)

Two settings the suite needs here, learned the hard way:

- **`GIT_CONFIG_NOSYSTEM=1`** — Git-for-Windows sets a system `core.autocrlf=true`
  that breaks the CRLF relay test.
- **`--basetemp=C:/t<n>`** — a short path; the default temp path blows MAX_PATH
  in the scaffold bootstrap tests.
- Use `.venv/Scripts/python.exe` (3.12). A system `python3` on PATH is 3.8,
  below the kit's declared 3.11 floor, and will fail with confusing errors.
- **Do not run two pytest sessions concurrently against the same basetemp** —
  it produces phantom failures that look like real regressions. Several
  mid-program "failures" were this.

---

## 7. If you want the full narrative

[`docs/log.md`](../../log.md)'s entry for 2026-08-08 records the program, all three
review rounds, and the eight BLOCKERs with their before/after behaviour. The
short version: **every blocker the reviews found was the new machinery quietly
wrong in the PERMISSIVE direction** — the privacy gate failing open on a
comment decoy, the shipped default self-ratifying its own final gate,
`keep_nondependent` overriding a human-held stop, a minted row that could never
be scheduled. That is the direction this kit's entire gate discipline exists to
prevent, and it is the pattern to hunt for in anything built on top of this.

One of those was found only because a *third* review looked: the cross-parser
test that exists to catch the privacy bug **carried its own stale copy of the
reader** — the exact defect its own docstring warns about, and the warning did
not save it.
