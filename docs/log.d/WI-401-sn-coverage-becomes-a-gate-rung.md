## 2026-08-02 — WI-401: SN coverage becomes a gate rung

**Summary.** Owner ruling 2026-08-01 (dispatcher-flow review Q2): SN→SR
linkage was not a gate input — `derive_gate.py` read SNs only as draft-or-not,
so a ratified need no SR answers left the derived gate untouched, orphaning
only in `trace.py` at G2 strictness. The rung: in `_raw_level`, a **ratified
SN cited by zero SR `SN-Refs` caps the raw level at G0** (an unanswered need
has not earned G1; the runnable value still floors to G1). A draft SN already
capped at G0 via the existing rung, so the new rung bites only the
ratified-and-uncovered case. Census here at landing: SN=25, uncovered=0 —
25/25 covered, the rung lands green exactly as the spec measured
<!-- fig: cmd="python project-trajectory/scripts/derive_gate.py --print --root ." rev=38091685 -->.

**Deliverables.**

- **The rung** (`project-trajectory/scripts/derive_gate.py`): `sn_gate` takes
  the cited set — Draft ⇒ G0 (the existing rung, the only one that fires on a
  draft); ratified-and-cited ⇒ G3 (never caps); ratified-and-uncited ⇒ G0.
  `_raw_level` rebuilds the cited set from the rows in scope, so the ex-draft
  counterfactual drops a Draft SR's citation with its row — removing a draft
  answer never fabricates coverage (fixture-pinned).
- **The F5 duplicate, pinned:** the SN-Refs parse is the named `sn_cited_ids`
  on BOTH sides (trace's inline `sr_sn_refs` comprehension became the same
  function; derive_gate stays self-contained, never importing the join
  engine), held equal by `tests/test_rule_sync.py::test_sn_cited_ids_agrees` —
  the phase_num/LLR_EXEMPT pattern.
- **The double-counting seam, kept and documented** (both code sides +
  `docs/registry-machinery-reference.md` §2.1/§6/§8.1/§8.3/§8.4): this rung is
  the *gate input* on ratified SNs; trace.py's `SN … has no SR` stays the
  *itemized listing* at G2 strictness; a Draft SN is exempt from both (one
  fact, one rung); both read the same cited set, so the pair cannot contradict
  on one registry state — verified by the draft-SN fixture (`uncovered=0`
  while the draft rung drops the gate).
- **Cache format:** the compared basis line gains `uncovered=N` between
  `modified=` and `computed=` — the spec's counts-change-shape branch, handled
  as the cache-format change it is: `docs/gate` regenerated and recommitted in
  the work commit (the dogfood cache test red on the old format, green after);
  downstream repos pass through by rerunning the generator once. Readers are
  unaffected (`traj_status` parses k=v generically; `check.py`'s
  `_BASIS_RE`/`_EX_DRAFT_RE` untouched).
- **Registration** (the WI-393 build-time precedent): LLR-147 + TC-141 under
  SR-049 (CMP-001, Phase 4); SR-049's Verified row untouched — no Modified
  flip owed, the new rows carry the rung.

**Deviations from spec.** None material. Judgment calls recorded: (1)
`window_open` does NOT read `uncovered` — an uncovered-SN G0 opens the same
suppressed-step window but warns nowhere; documented as an honest gap in §8.4
rather than built (outside the ruling's scope). (2) In the RAW view a Draft
SR's citation counts as coverage (matching trace's orphan exemption — the
draft itself already drops the gate); only the ex-draft view re-parses the
non-draft subset.

**Bookkeeping, reasons in place:** trace.py size baseline 2895 → 2909 (+14:
the named parse + the two seam comments; reviewed bump). Dupes census
`5a474f5d87b5` → `e933a42ec7f5` (spine-loader class: the sanctioned block grew
to span `sn_draft_ids` + `sn_cited_ids` in both files — same class, count 20
unchanged).

**Byte budgets:** AGENTS.template.md / PROCESS.md / PROCESS_OPTIONS.md all
untouched.

**Watched, measured on the work commit 38091685 (clean tree):** red first — 8
failed, 26 passed on the claim tree (the rung fixtures read raw G3 where the
rung demands G0, the `sn_gate` signature, the rule-sync pin), then green.
Smoke tier 616 passed / 6 skipped in 9.73s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=38091685 -->;
full suite 1866 passed / 10 skipped in 0:04:51
<!-- fig: cmd="python -m pytest -q -n auto" rev=38091685 -->;
`check_trajectory` / `check_doc_refs` / `check_figures` all rc=0 under
`--strict`; `derive_gate --check` rc=0 on the recommitted cache;
`check_docs --stale` stays at the pre-existing trunk red of 4 broken links
(the same WI-070/WI-173/WI-288 record lines, none added by this branch).
