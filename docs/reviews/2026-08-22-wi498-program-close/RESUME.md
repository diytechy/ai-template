# The WI-498 program close is ITERATED — resume state for the next session

The iterate pass COMPLETED. All 17 WORKLIST items are dispositioned —
**14 FIXED, 1 ADJUDICATED (W-13), 1 QUEUED as a new row (W-17 → WI-503), and
one half of W-5 REFUTED on measurement** — across nine logical commits:

```
3c030ef7  review: promote the staged-divergence step to an error
b34c15fe  review: pin the Release rung by value and by AST, not by constant name
092cf56c  review: re-author the five Approved prose cells the sweep left FALSE
e0644327  review: re-stamp the open-items baseline after the re-seed commit
e3954548  review: read a placeholder-only frame registry as NOT ADOPTED
78447926  review: sweep the DECLARED_INPUTS ruling into the adopter-facing recipe
8fa694cc  review: attribute a stage decrease to EVERY stage-affecting input
8885a30a  review: close both directions of the declared-input contract
3ecde26c  review: rebuild the stale-row census BY VALUE and re-scope WI-501
3c27291c  review: the MINOR sweep — the reader contract, the aliases, …
```

**Nothing is pushed and nothing is merged**, per the brief.

## The Group-1 proofs, in one paragraph each

- **W-1 (the round's only CRITICAL)** — Sol's tree was reproduced before the
  fix: a staged registry edit plus a regenerated-but-unstaged `docs/stage`
  passed the whole bar (`WARN`, exit **0**), so the commit would carry the
  edited registry beside the OLD derived stage. OI-31 had ruled the promotion
  trigger in advance — warn-first, "an error once it has run clean for a
  program" — and this was that program, so the plan step now passes `--strict`.
  The new test drives `--run-steps`, not the bare flag, because the defect was
  never in the detector: it was in the wiring, and a test of the flag alone
  stayed green through the entire defect. It FAILS against `HEAD`'s `check.py`.
- **W-2** — both reviewers' Release-producer mutants were injected into
  `spine_stage` one at a time. **The shipped pins PASSED both** (Opus's mutant
  also left 50 ladder tests green); **the rebuilt pins FAIL both.** The pin now
  asserts on the VALUE and then stops grepping altogether: an AST walk demands
  every `Return` be provably a rung below the top, so a literal, a subscript, an
  attribute alias, a call and a conditional are all refused.
- **W-3** — the five falsified prose cells were re-authored against semantics
  read out of the live code first, and the re-seed rode the ordinary machinery:
  `intake.py snapshot` **REFUSED** the bare refresh and named **exactly those
  five cells**, which is the independent confirmation that nothing else moved.
  The warrant is recorded by `--approves` in the snapshot's new `README.md`
  stamp, and the drift brief regenerated to "No spine row differs". Both records
  that disagreed with the diff — the slice-5 restraint bullet and the approval
  fragment's "mechanical" sentence — carry corrections in place.

## What the owner should be told plainly

**The highest-authority act in the range blessed text that was false.**
`ac121647` characterized four amendment groups as "all of them the mechanical
`derive_gate` → `spine_rules` re-pointing", and the owner's written approval
("Approve the spine changes, I have reviewed what was there") was given against
that characterization. It was true of the EDIT and false of its EFFECT: three of
the four groups carried PROSE cells, and the token substitution left five
ratified cells asserting a CLI that does not exist, a regen step that is not
one, and `docs/gate` as a live input in the commit that deleted it. The cells
are repaired and the record now says so, but **what that act blessed was not
what its record claimed**, and that is the owner's to weigh.

## Next session, in order

1. **WI-501 is re-scoped and is the next real work.** The census was rebuilt BY
   VALUE across all eight registry carriers and the population is **three times
   the banked figure**: 22 rows / 37 dirty cells, **18 of them `Approved`**,
   against a banked "six plus SR-148 as a seventh". Nine rows neither reviewer
   named are in the spec now. Read its `## Context` before starting — it names
   the three sharpest rows (**SR-139**, whose damage is in the NORMATIVE
   requirement cell and which also feeds WI-499; **TC-170**, a Smoke/automated
   row inside the "70 mechanized" basis whose method its own test does not
   assert; **TC-051**, a dangling EVIDENCE pointer as well as stale prose) and
   says which cells were already repaired at the close so they are not done
   twice.
2. **WI-503 is newly minted and queued** (watermark 502 → 503): the
   re-attestation brief splits into a regenerated `CURRENT.md` plus dated briefs
   that are immutable once minted. Opus's design is the spec. Assessed as NOT
   quick — it moves a gate that fails CLOSED because a human is about to attest,
   the `[generated]` census row the staged-divergence detector reads, the
   scaffold file lists and a RESYNC entry.
3. **W-15's successor row is owed.** `Implements: SR-139` was removed from
   `phase_rule_findings` (a false back-link inflating a ratification
   requirement's coverage), so the phase rule is deliberately ROWLESS until
   WI-501 mints the SR that carries its obligation.
4. **Two adopter-facing behaviour changes shipped and both have RESYNC
   entries** — the staged-divergence promotion, and placeholder-only frame
   registries reading as NOT ADOPTED. The second RAISES an adopter's derived
   stage, which is the correction, and the entry says what to re-run.

## Conditions the next session will meet

- **The C: volume is FULL.** It was at 100% / 0 bytes free when this close
  began. The 887 MB pip cache was purged (regenerable, and the only thing
  safely reclaimable by an agent) which bought ~1.9 GB — enough for batched test
  runs and **not** enough for one unfiltered `pytest -n auto`, which bootstraps
  hundreds of temp scaffolds. Two attempts died on `OSError: [Errno 28] No
  space left on device` and reported large false failure counts; every sampled
  failure passed in isolation. **This needs a human with space to reclaim**
  before a single-process full-suite figure can be produced here again.
- The full suite WAS run in four sequential batches at `-n 6` with a cleaned
  `--basetemp`: **2838 passed, 14 skipped, 0 failed** — labelled as a batched
  total, not a single-process one.
- Two harmless pre-existing conditions, both recorded in the close fragment:
  `docs/open-items.html` is necessarily stale for exactly one commit after any
  approval re-seed; and `tests/test_derive_stage.py` is collection-order
  dependent (`from kitlib import …` before `conftest.load_script` seeds
  `sys.path`) — the previously "latent" banked finding now has a concrete repro.

## Gates at `3c27291c`

| gate | result |
| --- | --- |
| full suite (4 batches, `-n 6`) | **2838 passed, 14 skipped, 0 failed**, ≈797 s |
| smoke (`-n auto -m smoke`) | 1368 passed, 5 skipped, 67.23 s |
| `check.py --jobs 0` | **RESULT: PASS** |
| `check_trajectory.py --strict` | clean — 500 work items, 464 done (93%) |
| `trace.py --strict-integrity` | `integrity=0`, orphans=15, 70 mechanized |
| `derive_stage.py --check` | `docs/stage up to date (DevStg-Arch)` |
| `check_vocab.py --strict` | clean, 425 live authored files |
| `check_docs.py --stale` | 992 docs, 1342 links, **0 broken** |

Byte-budgeted files were not touched. `check.py`'s module-size ratchet was
re-stamped twice (2127 → 2140 → 2184), each with its reason at the stamp. No
check was edited to green a step: the three test expectations that changed were
each PINNING the defect under repair.
