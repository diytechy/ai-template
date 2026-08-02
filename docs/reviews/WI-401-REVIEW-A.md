# WI-401 — REVIEW-A (2026-08-02)

Verdict: APPROVE — I drove the rung end-to-end on my own fixtures, blast-tested
every basis-line reader against the new field, mutated both the dogfood
registry and the rule-sync pin, and re-ran every registered bar. The predicate,
the double-counting seam, the ex-draft counterfactual, the F5 pin, and the
cache-format handling all reproduced exactly as claimed. Findings below,
severity-ordered; none blocks.

Reviewed: branch `wi-401-sn-coverage-becomes-a-gate-rung` at `72587dc1`
(work `38091685` + amended close), trunk `ConcurrencyTrainRewrite`. All
commands run under `/Users/diytechy/Documents/ai-template/.venv/bin/python`
from the worktree. Per the brief, `docs/log.d/` fragments were not read. The
disclosed close amend checks out: reflog shows `5091e054 -> 72587dc1 (amend)`
predating this review, and `git diff 5091e054 72587dc1` is exactly the stale
blob's repair — the Deliverable section restored (+51) and `specref` cleared
(R-F), nothing else.

## What I verified before hunting

**Parser blast radius (the hunt's #1).** Every reader of the basis line was
driven against the NEW shape (`uncovered=` between `modified=` and
`computed=`), not eyeballed. All are `\b`-anchored regexes or `k=v` token
splits — nothing positional — and every field read back correctly:

```
_BASIS_RE drafts,modified: 0 0        _COMPUTED_RE: G3
_PER_PHASE_RE: 1=G3;2=G3;3=G3;4=G3    _EX_DRAFT_RE: G3
window_open(green G3, uncovered=0)            = False  OK
window_open(modified window)                  = True   OK
window_open(draft window, mature ex-draft)    = True   OK
window_open(early repo drafts)                = False  OK
window_open(uncovered-only G0 drop)           = False  OK   <- the documented §8.4 gap, confirmed
check_trajectory.read_derived_phases -> {'1': 3, '2': 3, '3': 3, '4': 3}
traj_status._gate_facts -> all keys incl. uncovered; SN/SR/LLR/TC/per-phase/phase intact
```

`gen_release_checklist.py` does not read the basis line (its only gate mention
is checklist prose). `derive_gate --check`'s legacy value-only path fires only
when no `# basis:` line exists at all — untouched by a field insertion.

**Semantics, on my own fixtures** — a fresh `bootstrap.py` scaffold in scratch,
states built by hand and driven through the real CLIs:

```
A fresh scaffold (-000 only):          uncovered=0 computed=G1            (vacuous G1 holds)
B ratified SN, zero real SRs:          uncovered=1 computed=G1 gate G1    (see finding 3)
C SN-002 ratified, uncited:            drafts=0 uncovered=1 computed=G0 ex-draft=G0, gate G1
D SR-002 cites SN-002:                 uncovered=0 (restored)
E only-citing SR goes Draft:           drafts=1 uncovered=0 computed=G0 ex-draft=G0
F -000 SR is the only citation:        uncovered=1 computed=G0            (no fake coverage)
G uncited SN under the Draft heading:  drafts=1 uncovered=0               (one fact, one rung)
```

State E is the counterfactual reading honestly: the raw view counts the Draft
SR's citation (`uncovered=0`, matching trace's draft-exempt orphan rule — SN-002
is NOT listed) while ex-draft drops the citation with the row and stays G0 —
removing a draft answer fabricates nothing.

**The trace seam, same states.** On state C: `trace.py` default warns
`orphans=3` including `SN SN-002 has no SR`; `--strict` rc=1 (the G2-strictness
listing), `--strict-integrity` rc=0 (orphan is not an integrity finding). On
states E/G the draft-exempt id is listed by NEITHER surface. Gate cap and
itemized listing fire in the same direction on every state — no double-fire, no
contradiction.

**The pin is real.** In a scratch copy I diverged `derive_gate.sn_cited_ids`
(added a `-000` filter) and `test_sn_cited_ids_agrees` went red on the battery
(`Extra items in the left set: 'SN-000'`). The pin compares the two
implementations, not a copy of itself.

**Red-first is real.** New tests against trunk-vintage scripts: 9 failed / 25
passed — the 8 the Deliverable claims (rung fixtures incl. `raw G3 where the
rung demands G0`, the `sn_gate` signature TypeError, `uncovered` KeyErrors, the
rule-sync AttributeError) plus the expected 9th in my hybrid tree
(`test_meta_repo..cache_is_fresh`: the recommitted new-format cache against the
old code — the cache-format change demonstrated in the other direction).

**Dogfood.** `derive_gate --print --root .` reproduces the committed basis line
byte-for-byte (`SN=25 ... uncovered=0 computed=G3`), `--check` rc=0. Scrubbing
SN-014's single citation from a scratch copy of the registries:

```
# basis: SN=25 SR=136 LLR=130 TC=127 drafts=0 modified=0 uncovered=1 computed=G0 ex-draft=G0 ...
derived gate: G1
derive_gate: docs/gate STALE — the derived gate moved but the cache did not.   (rc=1)
```

**Registration.** LLR-147/TC-141 cells are true to the shipped code (I re-ran
their Evidence: `test_derive_gate.py` 26 passed, `test_rule_sync.py` 8 passed);
LLR-147 sits beside LLR-050 (derived-gate computation) under SR-049, CMP-001,
Phase 4, shapes matching the TC-140/LLR-146 conventions. SR-049 untouched is
CORRECT: no ratified cell was edited (`system-requirements.csv` has no diff),
adding child rows is decomposition per the WI-393 precedent, and the WI-341
precedent is on point — SR-049's text never named `ex-draft=` either when that
basis field landed without a Modified flip.

**The close tree's generated surfaces.** `gen_trajectory --check` and
`--status --check` read STALE at HEAD (the frontier still names WI-401). I
chased this to ground before grading it: that is the DESIGNED §5.2 stand-down —
work branches never regenerate the trunk's derived views; `check.py` SKIPs
`trajectory-map`/`status-map` on a claimed branch, and integrate's station
refresh regenerates then bars with `--trunk-lane`. The WI-393 precedent's
refresh commit (`c806965f`) shows exactly this frontier-row drop
(`docs/status.md | 1 -`) landing trunk-side. The work commit's committed regen
surface (gate/dashboard/status/okf/arch-map rows) matches the WI-393 merged
work commit file-for-file, and the `docs/gate` recommit specifically was forced
by the format change (the dogfood cache test — see red-first above). Not
findings. (`gen_arch_map --check` rc=1 in my environment reproduces identically
on trunk — pre-existing/environmental, a stand-down step on branches, not
chargeable here.)

**Mechanical.** Full suite on the close tree: `1870 passed, 6 skipped in
297.90s (0:04:57)`. Smoke: `620 passed, 2 skipped in 15.50s` — the close
message's exact figures. `check_trajectory --strict` rc=0 (378 done),
`check_doc_refs --strict` rc=0, `check_figures --strict`: `OK - 23 declared
figure(s)`, `gen_okf --check`: up to date. Spot-checked figures: the census
figure reproduces live (`SN=25 ... uncovered=0`). Ratchet: `wc -l trace.py` =
2909, exact against the re-stamped baseline, reason names the WI
(`1 passed`). Dupes census: `test_dupes_census_audit` 12 passed over the
re-fingerprinted `e933a42ec7f5` row. `ruff check` + `ruff format --check`
clean on every changed py file. docs/work delta is WI-401-only
(`D active/... / A complete/...`).

## Findings

**1. MINOR — the §8.3 exhibit misquotes the cache it ships beside: two
surfaces in one tree disagree on the same `as-of` stamp.**
`docs/registry-machinery-reference.md:361` shows

```
# basis: SN=25 SR=136 LLR=129 TC=126 drafts=0 modified=0 uncovered=0 ... (as-of d35c3b93)
```

while the committed `docs/gate` in the same tree reads `LLR=130 TC=127` under
the identical `as-of d35c3b93` stamp. The exhibit was captured mid-WI, before
the LLR-147/TC-141 registration rows landed, and not refreshed at close. It is
illustrative prose (no `fig:` marker owed, no checker compares it), but a
reference doc quoting a generated line that its own tree contradicts is
exactly the drift class the kit preaches against. Fix: paste the final
committed cache line.

**2. MINOR — the cannot-contradict promise also rests on the SN id-universe
scrape, and that duplicate is NOT pinned.** Both files scrape which SN ids
exist with the same whole-text one-liner (`derive_gate.py:278`,
`trace.py:1847`: `re.findall(r"\bSN-\d+\b", text)` minus `-000`), but
`test_rule_sync` pins only `sn_draft_ids` and `sn_cited_ids` — if the two
scrapes ever diverge, the gate and the listing CAN disagree about which ids the
rules run over, the exact WI-099 class the new pin exists to prevent. The
duplication predates WI-401, but WI-401 is what made the "both surfaces read
the same state" promise load-bearing in code comments and §8.1. A sharp edge
of the same scrape, worth a downstream-facing sentence: an SN id mentioned in
ratified PROSE (not a table row) and cited by no SR now caps the gate at G0,
where before it only made a strictness listing — both surfaces agree (the seam
holds), but the scrape's teeth grew. Fix: a third `test_rule_sync` pin (the
scrape is two identical lines today) and half a sentence in §2.1 or §8.1.

**3. MINOR — `uncovered=N` can be nonzero with nothing capped, and the doc's
"the count behind the coverage rung's G0 cap" overstates that corner.** Driven
(state B): a ratified SN with ZERO real SRs reads `uncovered=1 computed=G1` —
`_raw_level`'s vacuous branch (`if not srs: return G1`) returns before the rung
ever runs, so there is no G0 for the count to be "behind". The runnable
outcome is identical either way (G1) and the operative claim — `computed=G0`
with `drafts=0` names its cause — held in every state I drove, so this is
doc precision, not behavior: §8.3 and the `compute()` comment describe the
count as the cap's cause, when it is really "ratified SNs no SR cites"
(which the requirements-drafting corner legitimately shows without a cap).
Arguably the count being visible there is a feature; say so in half a clause.

**4. OBSERVATION — handoff: this WI's reference-doc amendment newly trips
WI-402's SpecRef-clock WARN.** `check_trajectory` on the close tree warns
`WI-402: its SpecRef docs/registry-machinery-reference.md changed after the WI
row was last touched — re-validate`. Trunk carries only the pre-existing
WI-389/WI-390 warns, so this one is caused by WI-401's (in-scope, demanded)
§8 edits. Warn-tier, correct behavior, not a defect — but the close does not
mention it, and the integrator should re-affirm WI-402 against the amended doc.

**5. OBSERVATION — the two smoke figures differ in skip-split, not substance.**
The spec's watched figure records `smoke 616 passed / 6 skipped` at
`rev=38091685`; the close message and my rerun both read `620 passed /
2 skipped`. Same 622-test universe — the delta is 4 environment-conditional
skips flipping to passes, not appearing/vanishing tests. Recorded here so the
differing numbers are never read as a false figure.

VERDICT: APPROVE findings=5
