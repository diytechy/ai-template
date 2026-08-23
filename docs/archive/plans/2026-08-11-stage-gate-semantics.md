> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# Stage vs gate — the semantics (RULED, SHIPPED, then SUPERSEDED in part)

**Status: RULED 2026-08-12, SHIPPED — and its ladder superseded 2026-08-13 by
OI-21.** Worked out with the owner 2026-08-11 as a proposal; the owner ruled it
the next day and the six-rung ladder plus the inserted implementation rung
shipped. **The half that still stands** is this document's core argument — a gate
is a moment and the repo was using it as a state; `G0` is not a gate; stage and
gate are separate axes; and §5's "a gate is not a pure function of stage", which
the ruling required be kept in any successor. **The half that is superseded** is
the six-rung ladder itself and the `G*` vocabulary it is written in: OI-21 (ruled
2026-08-13) retired the tags entirely for an eight-rung `DevStg-<Label>` ladder
with three `DevBar-<Label>` bars, requirements before architecture, and the
boundary and partition rungs inserted. **Read `docs/process.md` §4 "The stage
ladder" for the live model**; this document is kept as the reasoning that got
there, and its `G*` spellings are historical. The approval-provenance half of the
same conversation was ruled separately and is
[`repo-lock.md`](../../repo-lock.md) §2 **D-10**.

---

## 1. The problem, in one sentence

**A gate is a moment; the repo uses it as a state.** "The repo is at G1" cannot
say whether G1 is ahead or behind, and both readings are live in the tree.

Two consequences, both measured:

- **`docs/gate` contradicts its own header.** It states *"the repo is at gate G
  iff every in-scope SN/SR/LLR/TC meets G's bar"* and then displays `G1` while
  its own basis line says `computed=G0`. 37 drafts do not meet G1's bar, so the
  displayed value is the **floor**, not the claim the header makes.
- **The floor conflates opposites.** A fresh scaffold (nothing exists) and a
  mature repo that reopened a need both read `G1`, and nothing in the value
  distinguishes them.

## 2. G0 is the root error — it is not a gate

There is no threshold you cross to *reach* G0; it is the absence of having
passed G1. A ladder with a phantom rung reads ambiguously by construction. In
stage units the same fact is simply **stage 0**, which needs no apology.

## 3. What the code already does — and it already agrees with the owner

`spine_stage` is *"the tier currently IN PROCESS, 0–4"*, derived separately
precisely because — in `derive_gate`'s own words — *"there is no G that means
'TCs are in process'. Forcing one axis to carry both is how a dial ends up
meaning something subtly different at each of its five reading sites."*

Measured `stage_to_gate`:

```
stage 0 → G1    stage 1 → G1    stage 2 → G2    stage 3 → G2    stage 4 → G3
```

Read as **"the gate you are approaching"**, stages 0–3 are exactly right, and
what the docstring calls *"deliberately lossy"* is not lossy at all — two tiers
sit between each pair of sittings, so two stages share a gate.

**The one exception is at the top, and it is caused by a missing rung.** Stage 4
currently means "done, everything Verified" — G3 *passed* — so `4 → G3` reads
achieved-not-approaching, breaking the pattern.

## 4. The unified model

> **Stages are the tiers of the decomposition. Gates are the subset of stage
> boundaries that require a human to certify.**

Evidence for the discriminator: every gate carries a sign-off row
(`PROCESS.md` 348 / 356 / 371 / 377, recorded in `log.md`'s **Gate Sign-offs**
table). The boundaries that are *not* gates — 0→1 and 2→3 — have no sign-off,
because you draft needs then requirements without a sitting between, and write
designs then tests without one either.

```
stage 0  needs in process
stage 1  requirements in process
   ══ G1 ══  Stakeholder · UX · System Engineer
stage 2  design (LLR) in process
stage 3  tests in process
   ══ G2 ══  System Engineer
stage 4  IMPLEMENTATION in process        ← the proposed new rung
   ══ G3 ══  System Engineer
stage 5  release candidate (checklist being completed)
   ══ G-Release ══  Test Engineer …
stage 6  human evaluation
   ══ G-Final ══  the human's
```

With the rung inserted, the rule is uniform and needs no exception:
**`stage_to_gate(s)` = the next gate you must pass.** State and event stop
competing — you are *in* a stage, you *pass* a gate — and the strictness
selector and the approaching gate are the same value for a good reason: you are
held to the bar you are trying to clear.

### Why the missing rung matters more than it sounds

`derive_gate.py:344-345`:

```python
if not all(is_verified(r) for r in srs):
    return STAGE_TC          # stage 3
return STAGE_DONE            # stage 4
```

Once every TC is written and non-draft, the repo sits at **stage 3 — "TCs are
in process"** — and stays there for the **entire implementation period**. The
axis labels the longest phase of a project with the name of a phase that
already finished.

### Inserting at 4 is safe

`spine_stage` is the axis `human_ratification_through` is compared against
(`agent_loop.py:2872` — `human_holds(docs, spine_stage_of(root))`). Renumbering
is normally a live-policy hazard, but ratification tiers are **0–3**
(SN/SR/LLR/TC) and implementation is not a ratification tier. Inserting at 4
shifts only `STAGE_DONE`. This repo runs `human_ratification_through = 0`; the
template ships `4`.

## 5. Keep, so the model does not overclaim

**A gate is not a pure function of stage.** G1's bar includes "non-goals
captured" and UX sign-off; G2's includes "key runtime flows diagrammed". None
of that is derivable from which tier is in process — which is why
`stage_to_gate` is documented as *"a reader's reconciliation, not a second
source of truth."* Keep that sentence in any ruling, or someone will later try
to derive the gate from the stage and silently drop the human half.

## 6. What the same conversation exposed

- **No gate has ever been driven at its own boundary.** `log.md`'s Gate
  Sign-offs table records G1, G2 **and** G3 all `MET 2026-07-07` — the day
  Thread 47 self-adoption started and the spine was first authored. They were
  stamped at adoption, not certified at a boundary.
- **The "hats" have no mechanical existence.** In the scripts, "Stakeholder"
  appears only as a *tier label* (`"Stakeholder needs (SN)"`), never as a
  reviewer role. The roles live in `PROCESS.md` prose and as column headers.
  §8.3 item 5 already filed the roster gap; what this adds is **where** to
  inject it.
- **WI-424's adjudicator seam is the natural carrier.** It already provides a
  declared discriminator, evidence assembly that *refuses* rather than
  half-fills, a typed verdict validated before a session may close, and
  fail-closed routing for a declared-but-uncomposable brief. A gate sign-off is
  that shape — a named role, a declared bar, assembled evidence, a typed
  verdict. A fifth template, or one parameterized by hat, reuses all of it.
- **The Gate Sign-offs table already distinguishes hat from human** (four role
  columns plus a separate `Human` column). Any mechanization must fill the role
  columns and leave `Human` reachable only by a human, or the record loses the
  ability to answer "which gates did a person actually look at?"

## 7. Blocking defect — fix before ruling

**`docs/specs/derived-gate-model.md` does not exist.** It is cited **21 times**
— including by four live kit scripts (`derive_gate`, `check`,
`check_trajectory`, `trace`), five test modules, and **`PROCESS_OPTIONS.md`,
which ships to adopters**. It was archived to
[`../archive/specs/derived-gate-model.2026-07-20.md`](../../archive/specs/derived-gate-model.2026-07-20.md).

The document that *defines* these semantics is unreachable from the code that
implements them, which is a fair explanation for the drift. **Restore or
repoint it first** — a ruling written into a document nobody can reach is not a
ruling.

## 8. Proposed sequence

1. Restore the model doc (or repoint all 21 citations).
2. Rule the semantics into it: stage = state, gate = the approaching certified
   boundary, `G0` retired, the implementation rung added.
3. Sweep the assertions — `docs/gate`'s header, `status.md`'s "Active gate",
   the README's "the **active** gate", `PROCESS.md`, `PROCESS_OPTIONS.md`.
4. The hats/adjudicator half is its own WI, ruled with §8.3 item 5.

**Also stale and unrelated to the ruling:** the README's *"a `Status=Modified`
row … derives G2 until the sitting blesses it"* goes false the moment D-9
migrates, since `Modified` leaves the vocabulary. It belongs on step 7's sweep
list.
