+++
id = "WI-591"
title = "spot-check the clean close of WI-584 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

OUTCOME: STANDS WITH FINDINGS successors=1

Sample spot-check of the GREEN close of WI-584, under `docs/process.toml
[attestation] complete_review = 'sample'`. One question asked. **The close
STANDS** — nothing about the WI-584 merge is reversed, and a spot-check finding
is a successor row, never a reversal. One successor is drafted under
`## Dispositions`.

**What shipped answers what the row asked for.** Checked by driving the shipped
code at this branch's HEAD, not by reading the record that describes it:

- **The (a)/(b) fork was ruled, and (a) is what is built.**
  `baseline_snapshot.refresh_refusal` (:669) computes `scope` as
  `set(SNAPSHOTTED)` under `seed`, else `_authorised_registries(root, approves,
  snapshot)` — literally the function `copy_live` writes from, so the gate and
  the writer can no longer disagree, which was the whole defect. The `snapshot`
  is loaded in `refresh_refusal` itself (:651) rather than left to
  `refresh_ledger`, with the comment naming the direction a `None` would fail in
  (every approved row reads as newly arrived = widest possible scope).
- **The arm the ruling kept unscoped is kept.** `blocked = [...] if scope else
  unauthorised` (:674): an act whose write set is EMPTY is judged over the whole
  ledger, so a no-op refresh over drifted approved text refuses rather than
  exiting 0 in silence. Present, and its own test.
- **`_refresh_targets` passes `seed` through** (:844), which is what makes a
  re-seed over a standing record judge all seven registries instead of one.
- **The named acceptance re-drives at THIS tip, on the live repo.**
  `refresh_refusal('.', {'docs/requirements/low-level-requirements.toml': 'the
  sitting'})` returns `''`. The bare no-flag call still refuses (empty write
  set), listing `CMP-006`, `SR-024`, … So the act the disposition existed to make
  takeable is takeable — the successor condition WI-584 names is genuinely
  released, not merely asserted.
- **The six tests are the six claimed, and the gate is not vacuous.** The
  scoped-approval acceptance, the flip-authorised twin (the commoner path, which
  is why the ruling had to be general), the copies-nothing arm, the re-seed, the
  untouched off-spine mirror, and the residual case — a brand-new row arriving
  already `Approved` anchors its registry with no `Status` move, so an unrelated
  amendment could ride that anchor in, and it is refused. That last one is what
  makes the scoped gate non-vacuous, it asserts over the COPY as well as the
  message, and it is real. The one reworked test
  (`..._named_ref_mutes_ONLY_the_registry_it_names`) states in its docstring WHY
  the removed half was unreachable rather than merely that it was removed.
- **The extraction cleared the bar it was taken for.** `check_complexity.py
  --root .` -> `OK - 199 row(s) over 15, unchanged from baseline.` — no baseline
  bump taken, as claimed.
- **"No spine cell was minted or amended, so no approval brief is owed" holds.**
  No commit in the WI-584 range (`5f1e262a`, `75cdac7d`, `9c8b3ce2`, and the
  batch commits `b0be72c7`/`f4ca1bd5`) touches any file under
  `docs/requirements/` or the test registry.

**THE FINDING: the false header the row asked to have corrected is still there,
and the Deliverable says it was replaced.**

WI-584's `## Context` named this outside the (a)/(b) fork: *"the current message
claims the caller has authorised nothing, which is false, and that alone is
worth correcting under either reading."* Its `## Deliverable` then claims *"the
message now names what the act DOES authorise, **in place of** the header's
false 'nothing in this working tree authorises it'"*.

It was not put in place of it — it was put after it. Driven at this tip through
the shipped scoped arm (a drifted approved `SR` amendment, plus a brand-new
already-`Approved` `SR-999` putting `system-requirements.toml` into the write
set), the refusal reads, in order:

    baseline_snapshot: REFUSED — this refresh would ABSORB approved text into
    the record of what a human blessed, and nothing in this working tree
    authorises it:
      docs/requirements/system-requirements.toml SR-006: Title
    This act DOES authorise system-requirements.toml; the registr(ies) above
    are written anyway (…)

Two sentences of one message, the second contradicting the first.
`_refusal_text` (:682) branches its MIDDLE line on `scope` and leaves the
opening line a constant (:694), so the header is true only on the arm where
`scope` is empty — and false on exactly the arm ruling (a) built. Small, and
textual, and still the specific correction the row said was owed under either
reading; the record asserts it was made. Successor drafted below.

**Not a finding, recorded so the next reader does not re-derive it.** The
unscoped arm can be muted by naming ANY registry — `--approves
interfaces.toml=<ref>` makes `scope` non-empty, so drifted approved `SR` text
stops being listed and the act exits 0. That resembles the silence the arm
exists to prevent, but it is a different case: the act is no longer a no-op, the
writer has been scoped since WI-571 so nothing is absorbed, and the drift stays
visible on the re-attestation brief, which is where ruling (a) deliberately put
it. `..._named_ref_mutes_ONLY_the_registry_it_names` is that case, asserted over
the copy. The line is defensible, not a defect.

**Also immaterial, named rather than left to puzzle a reader.** The Deliverable
says the pre-change refusal listed "seventeen SR rows and four TC rows"; the
`## Context`, authored earlier, reads `test-cases.toml` 3. The registry moved
between the two readings; neither number is load-bearing for the ruling.

**Bar, green: `1528 passed, 8 skipped` and `44.4s vs 60s budget -> within`**
(real output, this worktree, 2026-09-04; interpreter
`/Users/diytechy/Documents/ai-template/.venv/bin/python` — this worktree has no
`.venv` and must not grow one). Pasted in
`docs/log.d/WI-591-spot-check-wi-584.md`, which also records two process notes:
this row's own Deliverable first asserted a bar it had not run — the same class
of defect faulted above, corrected before close — and R-A refuses the
standing-state rule's pre-verification Deliverable commit, so the fill rides
here in the close commit.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-584-the-snapshot-s-scoped-writer-a.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Dispositions

```toml
title = "Stop the snapshot refusal's opening line claiming nothing authorises an act whose next line names what it authorises"
workstream = "process"
buildtier = "quick"
priority = 3
```

`baseline_snapshot._refusal_text` opens every refusal with the constant
"…and nothing in this working tree authorises it:", then — on the scoped arm —
follows it with "This act DOES authorise <registry>…". WI-584 ruled the gate
scoped to the act's write set and added the second sentence, but left the first
one standing, so the arm the ruling built is the arm whose message contradicts
itself in consecutive lines. WI-584's own `## Context` named this header as
false and worth correcting "under either reading", and its `## Deliverable`
states the naming went "in place of" it; driven at the WI-591 tip, it did not.
IN SCOPE: branch the OPENING line on the same `scope` the middle line already
branches on — the empty-write-set arm keeps today's wording, because there the
claim is true; the scoped arm says what is actually wrong, which is that the
listed rows would ride along on an authorisation that does not cover them. Pin
both arms with a test that asserts on the header text, not just on "REFUSED" —
the existing tests pass today precisely because none of them reads the first
line. EXPLICITLY NOT IN SCOPE: the scoping rule itself, the unscoped arm, and
the three-ways-forward paragraph — all ruled and correct; this is the wording
WI-584 said it had already fixed.
