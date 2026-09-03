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

### What changed, and what it was driven against

`refresh_refusal(root, approves, snapshot, *, seed=False)` now computes the
act's write set — `set(SNAPSHOTTED)` under `seed`, else
`_authorised_registries(root, approves, snapshot)`, the same function the writer
uses — and judges the ledger against it, falling back to the whole ledger when
that set is EMPTY. `_refresh_targets` passes `seed` through. The message gained
a sentence naming what the act DOES authorise (or that it authorises nothing),
because the old header's "nothing in this working tree authorises it" was flatly
false in the case the row exists to fix. Rendering moved to a sibling
`_refusal_text`: the second decision pushed `refresh_refusal` to cognitive 18
and `check_complexity` went RED on it — measured before and after, and the
other four RED functions in that report (`agent_common.commit_telemetry`,
`agent_loop.worker_endstate`, `gen_verdict_rollup.main`, `integrate._verdict_gate`)
are pre-existing and untouched. The extraction cleared it; no baseline bump was
taken.

`snapshot` is also loaded once inside the function when the caller passes None,
rather than left to `refresh_ledger`: the scope decision reads it too, and a
`None` would make `_authorised_registries` read every approved row as newly
arrived — the widest possible scope, which is the direction this function must
not fail in.

Five tests, each confirmed RED against the pre-change module (`git checkout
65f368e7 -- baseline_snapshot.py`, run, restore) and green after:

```
FAILED test_a_named_ref_mutes_ONLY_the_registry_it_names           (reworked)
FAILED test_a_SCOPED_single_registry_approval_COMPLETES_over_unrelated_drift
FAILED test_an_unrelated_drift_cannot_block_a_FLIP_authorised_act_either
FAILED test_an_act_that_would_copy_NOTHING_is_REFUSED_rather_than_silent
FAILED test_a_registry_WRITTEN_for_another_reason_still_gates_its_amendments
FAILED test_a_RESEED_over_a_standing_record_is_judged_over_the_WHOLE_tree
```

Two of those deserve their caveat stated rather than buried. The `copy_NOTHING`
test is red on the old module only for its new message assertion — the refusal
itself already fired there; it pins the surviving arm, it does not claim new
behaviour. And `RESEED` is red partly because the old signature has no `seed`
keyword; its behavioural half is the `refresh_refusal(root) == ""` line above
it, which is a genuine flip.

ONE TEST WAS REWORKED, and the reason matters more than the edit.
`test_a_named_ref_mutes_ONLY_the_registry_it_names` asserted that a ref for the
WRONG registry still produced a refusal NAMING the right one — it pinned the
defect. Its real intent (the pre-WI-571 bug where a bare `--approves`
short-circuited all seven) is preserved and strengthened: it now asserts over
the COPY, which is what could actually launder — the SR's snapshot bytes do not
move and its drift survives in the ledger. The half deleted was a block on an
absorption that cannot happen.

The scoped gate is NOT vacuous, which is the objection to answer directly. A
registry enters the write set without a `flips` entry when a brand-new row
arrives already `Approved` (`_authorised_registries` adds the rel; `flips` is
about existing rows). That copy would land and carry an unrelated approved
amendment with it — `test_a_registry_WRITTEN_for_another_reason_still_gates_
its_amendments` drives exactly that, and it is refused.

### Surfaced, not fixed (separate findings, per the working agreement)

- **`LLR-173` does not name the authority gate at all.** Its `CodeSymbol` reads
  `copy_live/load_all/rows_for/exists/stamp/is_drifted/drifted_cells/
  unanchored_findings` — no `refresh_refusal` — and its Detail says "Three
  refusals are load-bearing" and enumerates the create-refusal, `load_all`'s
  raise and `rows_for`'s sentinel. The authority gate has been a fourth since
  2026-08-20 and WI-571 scoped the writer without amending the row either. This
  is pre-existing and NOT touched here on purpose: the row is `Approved`, and
  adding LLR drift is the opposite of what a row that exists to unblock the LLR
  anchor should do. It is a real gap and wants its own row.
- **The full suite has one inherited RED**, `test_check_docs.py::
  test_meta_repo_has_zero_unexplained_orphans`: `docs/handoff-2026-09-03.md` is
  reachable from no entry root. Committed at `f1cc2767`, an ancestor of this
  lane's base, and re-driven against a detached worktree of the base `794de60d`
  — the identical single orphan, 730 docs there against 732 here. Not this
  lane's, and not fixed here: the two available fixes are linking it from a
  coordination surface this branch may not edit, or adding it to
  `docs/orphans-allow`, which would quietly overrule an owner's own document.
- **The declared `lint` step is RED at the integration base** (three
  pre-existing F401/F841 in `tests/`), already recorded in this branch's WI-589
  fragment; unchanged by this row.

### Out of scope, and stated so

Nothing in `low-level-requirements.toml` changes here, and this row does not
take the re-anchor: a `spine` row is a worker lane, and
`acceptance_record.lane_approval_refusal` refuses a lane that writes
`SNAPSHOT_DIR`. The anchor is the successor condition the trunk-side
amendment-adjudication rung takes once this lands.
