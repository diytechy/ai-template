## 2026-09-03 — WI-584: the snapshot's refusal scoped to the act it gates

WI-578's disposition left two readings open and told this row to pick one on
the evidence. It picks **(a)**: `refresh_refusal` judges the registries the
refresh will actually WRITE, not the whole ledger.

### The observable, reproduced at this row's tip first

Before touching anything, the exact command the disposition names, against this
worktree (`b8e445ae`):

```
$ refresh_ledger('.')
docs/requirements/low-level-requirements.toml absorbed=9 flips=[]
docs/requirements/system-requirements.toml    absorbed=17 flips=[]
docs/test/test-cases.toml                     absorbed=4 flips=[]

$ refresh_refusal('.', {'docs/requirements/low-level-requirements.toml': 'ref'})
baseline_snapshot: REFUSED — ... nothing in this working tree authorises it:
  docs/requirements/system-requirements.toml SR-024: Rationale
  ... (+12 more) ...
  docs/test/test-cases.toml TC-082: Method
  ...

$ _authorised_registries('.', {…llr…: 'ref'}, load_all('.'))
['docs/requirements/low-level-requirements.toml']
```

Every row in the refusal is in a registry the write set does not contain. The
caller named the one registry it ruled on, and the refusal lists only
registries it did not — while claiming "nothing in this working tree authorises
it", which is false: the LLR ref authorises exactly what the act would write.
(The ledger reads 9 absorbed LLR rows, not the 7 the disposition recorded; two
more drifted between that reading and this tip. Nothing in the ruling turns on
the count.)

### Why (a) and not (b)

`copy_live`'s write set IS the authority set: `_refresh_targets` returns
`_authorised_registries(...)`, i.e. the named registries plus those an
approving `Status` move happened in. So a blocked-but-unwritten registry cannot
be absorbed by the act being refused — the block protects nothing and costs the
act. Choosing (b) would mean unwinding WI-571's scoped writer, which itself
closed a measured path (a spine flip re-sealing off-spine drift into the
record), and would contradict the per-registry contract the refusal text
already states in its own third arm ("authorises the one registry it names").

The false block is also not an `--approves` peculiarity, which is the argument
that settles it. A bare no-flag `intake.py snapshot` carrying an approving
`Status` move in one registry is refused today by drift in a registry it will
never write. That is the same defect on the commoner path, and only (a)
reaches it.

### The arm that survives the scoping

Scoping the gate to the write set makes it vacuous for every act that writes
something — and would make the laundering scenario (rewrite an Approved row,
then refresh) a SILENT no-op: write set empty, nothing copied, exit 0. The
drift would survive, so nothing is laundered, but an exit 0 is the wrong answer
to "you have rewritten blessed text".

So the gate keeps one unscoped arm: **an act whose write set is empty, in a
tree where approved text has drifted, is refused.** A refresh that copies
nothing is not a refresh, and the refusal text is how the caller learns which
drift stands. This is what keeps
`test_a_APPROVED_amendment_with_no_flip_and_no_ref_is_REFUSED` and the
de-approval regression (`test_a_DEAPPROVAL_cannot_authorise_an_unrelated_
approved_amendment`) firing under the new rule rather than being weakened to
fit it.

`seed=True` over a standing record keeps the whole-tree scope it always had:
that act really does write all seven registries, so the global judgement is the
scoped one.

### Out of scope, and stated so

Nothing in `low-level-requirements.toml` changes here, and this row does not
take the re-anchor: a `spine` row is a worker lane, and
`acceptance_record.lane_approval_refusal` refuses a lane that writes
`SNAPSHOT_DIR`. The anchor is the successor condition the trunk-side
amendment-adjudication rung takes once this lands.
