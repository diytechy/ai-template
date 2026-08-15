## 2026-08-14 — WI-451 slice 2, act 7: the top-down read's mechanical half CLOSED (19 cells, 12 rows), two crossing attributions revised and flagged

Act 6's re-iteration produced nine ranked findings. This act closes the four
that carry no decision in them, leaving the owner a clean five-item ruling list
instead of a mixed bag. Drafted by two independent agents over non-overlapping
row sets, then adjudicated, applied and re-verified by the author — every
proposed `old` cell asserted byte-equal against the live tree before any write,
which caught one stale draft and refused it rather than overwriting.

**Closed (full detail in
[plans/2026-08-14-wi451-slice2-ledger.md](../plans/2026-08-14-wi451-slice2-ledger.md)):**

- **M2 — "declared" was a floating referent** in the three new harness parents.
  Each acceptance now NAMES its declaration sites, found by reading the code
  rather than asserted: `trace.py`'s `ID_PATTERNS`/`REQUIRED_FIELDS`/
  `ENUM_FIELDS` and its four flag families, `trace_text.py`'s gating-vs-advisory
  split, `check_trajectory.py`'s R-rules and `TOP_VIEW_MAX`, the `[checks]`
  opt-out pair, `check.py`'s `doc-navigability` step and `stack.ini`'s
  `[step:doc-refs]`/`[step:figures]`. **Not narrowed** — each cell keeps its
  general clause verbatim, labels the sites "the current set", and closes with
  "a rule added at one of those sites is in scope by default", so naming adds
  precision instead of shrinking the obligation.
- **M5 — SR-165 was a placeholder.** Rewritten with a concrete home
  (`components.toml`, where `trace.py` already runs `component_findings`); the
  unfalsifiable *"a reviewer reproduces the recorded scores"* becomes *"the
  recorded ranking recomputes from the record's own objective, constraints and
  scores"*, plus a reported selection the scores do not rank first absent a
  recorded human override. `Verification` Inspection → **Test**, because that
  check is genuinely mechanical — which OWES an LLR+TC before the row leaves
  `Draft`, recorded in the ledger rather than silently incurred.
- **M5 — two dead acceptance clauses.** SR-154's *"review substance scoring
  never rewards length"* verified no clause of its own shall (LLR-046/TC-083
  already carry it). SR-164's *"when the field lands"* conditioned acceptance on
  the row's own implementation, so it could never fail — measured dead (the SN
  schema carries `acceptance/kind/need/priority/why`; **zero** rows carry
  `scope`). It now fails honestly.
- **M5 — `sn_refs` inflation.** SR-153 sheds SN-024 (it only READS a plan-mode
  classification), SR-155 sheds SN-023 (comparing rival plans ON interface
  coverage consumes those declarations, it does not deliver the dashboard).
  **Orphan safety was verified twice independently** — by the drafting agent and
  by the author, before either removal — SN-024 keeps 5 citers, SN-023 keeps 5.
- **L1 — SR-035's TITLE was the wrong cell**, claiming an OS-portability
  obligation that is SR-114's while its requirement/rationale/acceptance are all
  about language-specific tokens. Retitled; rewriting the requirement toward the
  title would have duplicated SR-114.
- **L1 — `external.toml`'s B-05 note listed FIVE capability buckets** where
  ruling `2026-08-14c` declared six. The frame's own note had been contradicting
  a ruling the registry was already using. Extended, naming SR-031/034/035/114.
- **A false claim in a rationale the author wrote:** SR-154 called itself
  SN-026's *"only surviving SR-level carrier"* while SR-155 cites SN-026 too.
  Corrected to state what is true and what is actually distinct about each row.

**TWO CROSSING ATTRIBUTIONS REVISED — applied, and flagged for the owner to
overrule.** `trace.py` checks that a `Boundary-Refs` value RESOLVES, never that
it is the RIGHT crossing, so nothing mechanical would catch either reading:

- **SR-137 `["B-01","B-02"]` → `["B-01","B-04"]`** — B-02 carries *"rulings,
  attestations and Status flips"* and this row contains none; its shall is about
  the dial file's HOME and SHAPE, so its observables are the config edit
  arriving through the hook floor and the refusal going back out. The contrary
  reading (declaring a policy dial IS an authority act) is coherent, which is
  exactly why it is flagged rather than buried.
- **SR-139 `["B-02"]` → `["B-02","B-05"]`** — B-02 stays; B-05 joins because
  half the observable, a declared auditable level-to-gate mapping, is delivered
  package content.

**Five findings remain, all needing an owner ruling** (the missing B-05 package
observable; the SN-025 loop-selection duplication across SR-148/153/059;
SR-031 vs SR-137 stating one observable twice and already diverging; four rows
that escaped demotion; three needs with zero textual coverage despite
`orphans=0`). None is mechanical, and each is the same *kind* of call as
sitting-3's §0.3 ledger.

Bar: `pytest -q -n auto` → **2491 passed, 11 skipped** (full suite);
`trace.py --strict --strict-schema` → `orphans=0 integrity=0 schema-findings=0
form-findings=2` (the two recorded waivers); `check_docs` OK.
