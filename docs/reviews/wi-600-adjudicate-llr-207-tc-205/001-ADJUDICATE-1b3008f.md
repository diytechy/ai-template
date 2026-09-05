# ADJUDICATE — WI-600 — first approval at 1b3008f

The only question: is each row ready to be APPROVED as it stands? `Approved`
blesses the TEXT. It claims no test passed — but a cell that describes a
mechanism the code does not have is not blessable text, so every clause was
driven against the shipped module rather than read for plausibility.

Scope: two rows, `LLR-207` (`low-level-requirements.toml`) and `TC-205`
(`test-cases.toml`), both `Drafted`, both Phase 5, both under the already-
`Approved` `SR-156`. Everything else shown — SR-156, LLR-138/140/145/150/151,
TC-131/132/139/144/145 — is chain evidence and was read as such; no cell of
any of them is touched.

What was verified independently, not taken from the chain:

- **Every `CodeSymbol` exists.** All 22 names in LLR-207's cell resolve in
  `project-trajectory/scripts/kitlib/verdict.py` (checked mechanically, zero
  missing), and `mechanical_close_subject` / `mechanical_close_order`, which
  the cell names as the writer's shared composers, are in
  `kitlib/station.py:142,149`.
- **Every clause of the Detail was read against the code**, not summarised:
  `fold_listing`'s byte-native record-prefix boundary and TAB split;
  `tree_identity`'s `-z --full-tree`; `refresh_attestation`'s three verified
  names (own tree, first parent, branch-owned subject); `_closed_wi_ids`'s
  one-source-branch, paired-move, `A`/`D`-refuses / `M`-rides-free rule and its
  `mechanical_close_order` return; `mechanical_close_attestation`'s exactly-one-
  parent, `--no-renames`, exact-composed-subject comparison; `_peel_target` as
  the one home of the two disposable classes and `work_tip` deliberately NOT
  going through it; `governing_rev`'s identity-equals-parent step condition;
  `logged_rounds`' log-owns-the-phase join and its more-than-one-phase = no
  round; `round_entries`' governing (not raw) binding; `declared_phases`'
  `max(0, required)` clamp; `phases_owed`'s drawn-not-parsed answer;
  `round_count`'s largest-per-phase; `branch_trailers`' per-tree oldest-first
  sequence with the carrier verified at its governing identity. The trailer
  grammar in the cell matches `TRAILER_RE` exactly, including the 64-hex tree
  and the two-word enum.
- **Every `Evidence` citation exists.** 56 node ids across 4 files; zero
  missing. `tests/test_verdict_record.py` — 75 passed in 48.28s on this tip.
- **The `Tier` argument was re-derived at its root, not accepted.** 9 of the 56
  citations sit outside `test_verdict_record`, in `test_integrate_admission`,
  `test_integrate_station` and `test_handback` — all three present in
  `tests/conftest.py` `SLOW_MODULES`, so `-m smoke` deselects them and `Full`
  is the cheapest tier at which the whole cited set runs.
- **Three of the Method's sharpest claims were opened and read**, because a
  Method that describes arms a suite does not contain is the failure mode this
  rung exists to catch: the two-row batch close IS seeded in non-canonical
  order and DOES assert the reversed order composes a different subject
  (`test_verdict_record.py:1782`); the empty close IS a real `--allow-empty`
  commit, IS asserted refused at `mechanical_close_attestation`, and the gate
  assertion beside it is the stated CONSEQUENCE (still merges), not a refusal
  the cell claims and the test lacks (`:1834`); the invalid-UTF-8 arm DOES
  assert the fixture collides under replacement decoding before asserting the
  identities differ (`:130`).
- **No `WI-`/`OI-`/review-round citation** in either cell — the marker hazard
  that makes a cell cite a record a downstream reader can never open.

Read sideways: LLR-207 and LLR-140 are not one decision twice. LLR-140 owns
`integrate.py`'s gate — which refusals fire and under what policy — while
LLR-207 owns `kitlib/verdict.py`, the definition both the gate and the loop's
round scheduler read. `IF-175` declares that seam and explicitly refuses to
restate the disposable-class list, naming LLR-207 as its home, so the two
rows point at each other without either restating the other.

One observation recorded and deliberately NOT a finding: LLR-207 states the
walk ends at "depth bounds" (`_MAX_GOVERNING_WALK`, `_MAX_REFRESH_PEEL`) and
no cited test drives a history deep enough to hit one. That is a guard against
pathological hand-made history whose failure direction the cell itself states
(stopping measures at a later rev, so it can only ask for MORE review). An
unexercised safe-direction guard is not an unclosed obligation, and the same
shape is already blessed in this chain at LLR-140/TC-132.

- [APPROVE] LLR-207 -> a builder must ship one module that answers, for both the merge gate and the loop's round scheduler, what tree a verdict governs (a byte-native fold excluding `docs/reviews/`, `docs/log.d/`, `docs/iteration/`), which commits may be peeled or walked through to reach it (two verified machine-authored classes; the read-only walk and the destructive reset peel kept separate), which round files count as evidence (joined to a coordinator session log that owns the phase), and how many phases and cycles that evidence buys — with the self-verifying trailer a cross-check that refuses an OVERSTATED count and stands down on an understated one -> parent SR-156 demands a fail-closed serial seam whose verdict rung is real; sibling LLR-140 consumes this definition at the gate and LLR-150/151 never touch it; `IF-175` declares the seam and defers the class list here by name; TC-205 verifies it and cites 56 arms that exist -> ready: every clause restates as an obligation a builder could fail, every named symbol exists and reads as the cell describes it, the fail-toward-REVIEW direction is stated for each verification arm rather than assumed, and the one deliberate deferral (off-git answers left to each requestor's own declared direction) is the seam row's stated position, not a gap this cell opened.
- [APPROVE] TC-205 -> a test author must drive the identity's exclusion BOTH ways (record path in, work path out) through git's real encoding boundary, the trailer grammar's round-trip and its three malformed shapes, the gate on a real two-branch fixture with the implementer-authored round and the two-logs ambiguity refused by name, BOTH disposable peels and each of their six refusal arms with every other clause satisfied, the writer driven against the verifier through `handback.close_adjudication`, both carriers of the attestation including the zero-path one obtained by calling its producer, both orders of refresh and round, the dial at both the gate and the scheduler, and the shared definition in both its dimensions (which tree, how many phases) -> it verifies SR-156, LLR-207 and IF-175, and its arms map onto LLR-207's clauses one for one; nothing LLR-207 states about the identity, the two peels, the join, the span, the count or the trailer is left without an arm -> ready: `Automated`/`Level`/`Tier` are unambiguous, `Expected` states an observable condition, every cited node id resolves, the cited suite is green on this tip, and the `Full` tier is justified by the cited set's own membership rather than by the majority of its files — labelled on the under-claiming side, with the tier-vs-marker independence stated rather than glossed.

OUTCOME: APPROVE rows=2

## Dispositions

None. Both rows state what the machinery actually does, at a granularity a
builder could fail and a reader could check, and there is nothing here I would
decline to bless.
