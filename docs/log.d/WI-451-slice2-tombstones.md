## 2026-08-14 — WI-451 slice 2, act 1: the 26 supersession tombstones DELETED per D-4 — this entry is their forwarding home

Ruling `2026-08-14b` (sitting-3 §0.3 rows 1–2) executed: the 26
supersession-bookkeeping SR rows are deleted, not marked — *"a registry states
what IS; git is the history"* — following the SR-039 precedent (2026-08-11).
**SR 149 → 123 · TC 149 → 147**; the orphan set is unchanged at 9 (SR-148's
missing LLR/TC + SN-034…SN-040), so the deletion orphaned nothing.
<!-- fig: cmd="python project-trajectory/scripts/trace.py --strict # Traceability: SN=27 SR=123 LLR=152 TC=147 orphans=9 integrity=0" rev="this commit's tree" -->

**The forwarding map — every spent id and where its obligation lives now**
(chains through other tombstones are resolved to live rows; the three chained
cases are marked ⛓):

| Deleted id | Title (was) | Live replacement rows |
|---|---|---|
| SR-037 | Work-item registry validation | SR-067, SR-068, SR-069 |
| SR-038 | Offline project-state view | SR-070, SR-071, SR-072 |
| SR-044 | Declared-interface connectivity | SR-073…SR-078 |
| SR-045 | Heterogeneous implementer/reviewer scheduling | SR-079…SR-083 |
| SR-047 | Subjective-quality critique loop | SR-084, SR-085, SR-086 |
| SR-048 | How-SW top view bounded and containerized | SR-087, SR-088 |
| SR-051 | Tiered drill-down views | SR-089…SR-092 |
| SR-058 ⛓ | Deterministic safety classification | SR-093, SR-094, SR-132 (via SR-095) |
| SR-061 | Parallel-by-default dispatcher | SR-132 |
| SR-062 | Change-train continuation | SR-132 |
| SR-063 ⛓ | Atomic serialized integration | SR-132 (via SR-096/097/098) |
| SR-064 ⛓ | Crash safety and git-as-authority recovery | SR-132 (via SR-099/100/101) |
| SR-065 | Parallel-execution telemetry and downstream migration | SR-132 |
| SR-066 | Dual-plan decomposition round | SR-102…SR-108 |
| SR-095 | Safety-aware traincar packing | SR-132 |
| SR-096 | Atomic CAS integration | SR-132 |
| SR-097 | Serialized blocked disposition | SR-132 |
| SR-098 | Durable publication intent | SR-132 |
| SR-099 | Git evidence enumeration | SR-132 |
| SR-100 | Ownership-state reconstruction | SR-132 |
| SR-101 | Lifecycle-boundary recovery | SR-132 |
| SR-117 | Atomic traincar reservation and lane leasing | SR-132 |
| SR-118 | Traincar build and review shape | SR-132 |
| SR-119 | Release on early train end | SR-132 |
| SR-120 | Blocked-constituent disposition | SR-132 |
| SR-121 | Gated downstream migration to the parallel default | SR-132 |

All 26 ids are SPENT FOREVER (the id watermark's committed mark carries their
headroom; `docs/id-watermark` untouched, per the precedent).

**The follow-through the ruling named, executed in the same act:**

- **`sn_refs` coverage re-checked:** the eight SNs the tombstones cited
  (SN-002/006/008/010/012/023/024/025) each retain live citing SRs — the
  thinnest, SN-025, keeps 10 — and `trace.py`'s orphan set is bit-identical
  before and after. No need lost its anchor.
- **Citing IF rows:** IF-053 and IF-054 drop dead `SR-095` from their
  `sr_refs` (three live refs remain each). **IF-055 is re-pointed to SR-132
  rather than deleted** — a recorded per-row reason: unlike the SR-039 case,
  IF-055 declares a live seam (`integrate.py` imports `schedule.py` today),
  and the tombstone text's own instruction is that implementation links
  *"shall cite the replacement rows"*; deleting the row would un-declare a
  real interface. This is the same edit IF-053/054 received, not an exemption.
- **`trace.py`'s supersession machinery retired by ruling:**
  `sr_supersession_findings`, `_supersession_targets`,
  `_supersession_cycle_findings`, `_llr_supersession_findings` (~110 lines)
  and their integrity-floor call deleted; the SR-tier `superseded_by` carrier
  key (`spine_carrier.SPINE_TIER_KEYS`) and the `SupersededBy` entry in
  `check_trajectory.SPINE_RATIFIED_CELLS` retired with it. The CMP registry's
  own `PartOf`/`SupersededBy` rule is SEPARATE and stays (still-owed item,
  repo-lock D-4 — that section now records this deletion as DONE). The six
  pinning tests in `tests/test_trace_rules.py` (the WI-229/WI-364 block,
  ~207 lines) retired with the machinery.
- **TC-099 retired by ruling — and TC-133 with it, by the same class:** the
  ruling named TC-099 (the frozen-migration-map inspection); TC-133 is the
  same evidence class for the Phase-5 set and ALL FIFTEEN of its `verifies`
  targets are in the deleted class, so keeping it would leave a test case
  verifying nothing. Recorded here as the ruling's necessary extension, not a
  silent one.
- **Live prose re-pointed to successors:** `score_reviews.py` (SR-096→SR-132),
  `agent_loop.py` (SR-062→SR-132 ×2, SR-096→SR-132), `schedule.py` header
  (SR-095 dropped), `check_need_form.py`'s example id + its test
  (SR-101→SR-102), the OKF panel test (SR-038→SR-070). `docs/enforcement-audit.md`
  drops the retired enforcer row; `docs/registry-machinery-reference.md`
  §12.9 and the SR-column tables record the retirement.
- **Deliberately left:** the 31 `rationale` cells in surviving SR rows that
  cite their composite ancestors as decomposition provenance ("formerly
  carried by SR-044") — 30 of the 31 are census DEMOTES whose text is
  rewritten when they land as LLRs in this same slice, and the ids are spent,
  so the references are unambiguous history until then. OI-18's evidence
  prose (`open-items.toml`, `status = "ruled"`) cites SR-064/099/100/101
  as the record of a ruling already executed — a closed record, not
  re-worded, per the same doctrine that forbids rewriting history.
  `migrate_carrier.py` keeps its `SupersededBy` column mapping: it is the
  one-shot CSV→TOML converter and an adopter's legacy CSV may legitimately
  carry the column; `test_rule_sync`'s inverse pin holds because
  `spine_carrier.SPINE_COLUMN` keeps the key for the CMP tier.
