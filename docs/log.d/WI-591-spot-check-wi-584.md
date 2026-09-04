## 2026-09-04 — WI-591: spot-check the clean close of WI-584

Sampled close review under `docs/process.toml [attestation] complete_review =
'sample'`. Nothing was alleged against WI-584; the question asked is the single
one the row states — does what shipped answer what the row asked for? A finding
here is a successor row, never a reversal.

**Verdict: the close STANDS WITH ONE FINDING.** One successor is owed, drafted
under this row's `## Dispositions`.

**What was checked, by driving the shipped code rather than reading the record
that describes it** (interpreter
`/Users/diytechy/Documents/ai-template/.venv/bin/python` — this worktree has no
`.venv` and must not grow one):

- **The ruling is (a) and the gate is scoped to the writer.**
  `baseline_snapshot.refresh_refusal` (:669) builds `scope` as
  `set(SNAPSHOTTED)` under `seed`, else `_authorised_registries(root, approves,
  snapshot)` — the same function `copy_live` writes from — and blocks only
  `unauthorised` pairs inside it. The `snapshot` is loaded in `refresh_refusal`
  itself (:651) rather than left to `refresh_ledger`, with a comment naming the
  failure direction a `None` would take (widest possible scope). Correct as
  claimed.
- **The unscoped arm survives.** `blocked = [...] if scope else unauthorised`
  (:674) — an empty write set is judged over the whole ledger, so a no-op
  refresh over drifted approved text refuses instead of exiting 0. Present as
  ruled, and its own test.
- **`_refresh_targets` passes `seed` through** — `refresh_refusal(root,
  approves, snapshot, seed=seed)` at :844. Correct.
- **The named acceptance re-drives at THIS tip.**
  `refresh_refusal('.', {'docs/requirements/low-level-requirements.toml': 'the
  sitting'})` returns `''`; the bare call still refuses (empty write set, whole
  ledger), listing `CMP-006`, `SR-024`, … So the act the disposition existed to
  make takeable is takeable, on the live repo, not just in a fixture.
- **The six tests exist and are the six claimed.** In
  `tests/test_baseline_snapshot.py`: `..._SCOPED_single_registry_approval_
  COMPLETES_over_unrelated_drift`, `..._unrelated_drift_cannot_block_a_FLIP_
  authorised_act_either`, `..._act_that_would_copy_NOTHING_is_REFUSED_rather_
  than_silent`, `..._registry_WRITTEN_for_another_reason_still_gates_its_
  amendments`, `..._RESEED_over_a_standing_record_is_judged_over_the_WHOLE_
  tree`, `..._SCOPED_refresh_leaves_the_UNTOUCHED_offspine_mirror_GREEN`; plus
  the reworked `..._named_ref_mutes_ONLY_the_registry_it_names`, whose docstring
  states WHY the removed half was unreachable rather than merely that it was
  removed. The non-vacuity case the Deliverable promised (a row arriving already
  `Approved` anchors its registry without a `Status` move) is a real test, and
  it asserts over the COPY as well as the message.
- **The extraction cleared the complexity bar with no baseline bump.**
  `check_complexity.py --root .` -> `OK - 199 row(s) over 15, unchanged from
  baseline.`
- **"No spine cell was minted or amended here, so no approval brief is owed"
  holds.** No commit in the WI-584 range (`5f1e262a`, `75cdac7d`, `9c8b3ce2`,
  and the batch commits `b0be72c7`/`f4ca1bd5`) touches any file under
  `docs/requirements/` or the test registry.

**THE FINDING: the false header the row asked to have corrected is still
there — and the Deliverable says it was replaced.**

WI-584's `## Context` named this explicitly, outside the (a)/(b) fork: *"the
current message claims the caller has authorised nothing, which is false, and
that alone is worth correcting under either reading."* Its `## Deliverable`
then claims *"the message now names what the act DOES authorise, **in place
of** the header's false 'nothing in this working tree authorises it'"*.

It was not put in place of it. It was put after it. Driven at this tip through
the shipped scoped arm (a drifted approved `SR` amendment plus a brand-new
already-`Approved` `SR-999` putting `system-requirements.toml` in the write
set), the refusal reads, in order:

    baseline_snapshot: REFUSED — this refresh would ABSORB approved text into
    the record of what a human blessed, and nothing in this working tree
    authorises it:
      docs/requirements/system-requirements.toml SR-006: Title
    This act DOES authorise system-requirements.toml; the registr(ies) above
    are written anyway (…)

Two sentences of one message, the second contradicting the first. `_refusal_text`
(:682) branches its MIDDLE line on `scope` and leaves the opening line a
constant (:694), so the header is right only on the arm where `scope` is empty —
and wrong on exactly the arm the ruling built. This is small and it is textual,
but it is the specific correction the row said was owed under either reading,
and the record asserts it was made. Successor drafted below.

**Not a finding, recorded so the next reader does not re-derive it.** The
unscoped arm can be muted by naming ANY registry: `--approves interfaces.toml=
<ref>` makes `scope` non-empty, so drifted approved `SR` text is no longer
listed and the act exits 0. That looks like the silence the arm exists to
prevent, but it is not the same case — the act is no longer a no-op, the writer
has been scoped since WI-571 so the drift is not absorbed, and the drift stays
visible on the re-attestation brief, which is where ruling (a) deliberately put
it. `test_a_named_ref_mutes_ONLY_the_registry_it_names` is that case, asserted
over the copy. The line is defensible; it is not a defect.

**Also immaterial, named rather than left to puzzle a reader.** The Deliverable
says the pre-change refusal listed "seventeen SR rows and four TC rows"; the
`## Context`, authored earlier, reads `test-cases.toml` 3. The registry moved
between the two readings. Neither number is load-bearing for the ruling.
