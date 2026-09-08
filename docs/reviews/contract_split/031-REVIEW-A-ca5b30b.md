### REVIEW-A — WI-623 adjudication — Round 31 — 2026-09-07
Verdict: APPROVE
Findings: none.

Worst failure classes tested, in order: unauthorized cell acceptance or approval-snapshot absorption through a RETURN; stale, forged or missing turn/judgment/candidate provenance; truncated continuation or transferred first-approval authority; empty or rebound review input; premature registry mutation, close or coordinator resume. None survived the checks below. Source-review approval, authoring completion and green tests were treated only as inputs, never as semantic acceptance.

Reviewed HEAD: `ca5b30b0c38059e95f31180d3f85d7d482669873`; candidate work commit: `7b9843c8856cfad2eea260fbe8e5b3dfebc9ccdd`; governing non-record identity: `06b1eac7bddac59620fa7ecabdda9b677a5151cf8176f45a6cc6116b479f54d5`. The working tree was clean at entry. I used exactly the owner-authorized retrospective range:

```sh
git diff c492da3dd0e6247610bf0af116305e989d1d17f7...HEAD -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ':(exclude)docs/log.md' ':(exclude)docs/log.d' ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'
```

That range is nonempty and contains one non-record path: `docs/work/queued/WI-623-adjudicate-complete-combined.md`, 758 added lines. Thus the earlier branch-to-itself empty-diff blocker is resolved without changing the selected turn, base, proposal or candidate identity. The current turn record remains `WI-623-c492da3dd0e6247610bf0af116305e989d1d17f7`; its base remains `c492da3dd0e6247610bf0af116305e989d1d17f7`; the payload proposal remains the recomputed base identity `ef6086929ee50393352e6ed98be68d9c1f5e995b18a720c447c594c7d643298e`.

Independent evidence from Git objects and the production parsers/publisher:

- `primary_approval.parse_approval_payload` accepts exactly the top-level keys `version`, `turn`, `base`, `proposal`, and `decision`. There is no acceptance-only `impact` or `absorption` ledger. `_decision_rows` returns 52 unique decisions for the 52-row immutable turn scope, all classified `return`, across 535 before/after cell mappings. Independent registry-blob comparison finds 85 actually changed cells and zero uncovered changed cells. No cell is accepted.
- The committed round-029 ADJUDICATE record names this turn/base/proposal and a truthful whole-scope RETURN. Its evidence commit `25b6c3f8e66ae08262ba0f06c44be3e015843937` writes that judgment; the coordinator's committed session header binds phase `ADJUDICATE`, WI-623, the same primary turn, judgment path, candidate `7b9843c8856cfad2eea260fbe8e5b3dfebc9ccdd`, actual route/model metadata and invocation identity. On reviewed HEAD, `_judgment_records(..., "amendment")` returns exactly one record. Record-only commits through `ca5b30b0` preserve the same governing identity.
- `intake.parse_dispositions` accepts exactly two drafts. The first supersedes WI-623, retains every original prerequisite plus WI-623, names all 52 original IDs, and carries the selected spec's entire Context with only section-boundary newline normalization. It expressly preserves WI-606, the existing IF-175 owner, WI-618/IF-180, all Drafted riders, parent/counterpart rationales, LLR-061/TC-061's conjunctive completion predicate, the LLR-153/154/207 authority split, LLR-167's distinct purposes, PC-BATCH-USES retirement duties, proof limitations and WI-601/WI-603/WI-605 history. The second draft remains the separately scoped ordinary resume/telemetry repair and does not narrow or replace the semantic continuation.
- PROCESS.md section 5's parent-sound/child-authority boundary is preserved: the reviewed range changes no requirement or test registry, interface status, approval snapshot, implementation or regression test. Parent acceptance remains unchanged; IF-090, IF-091, IF-175 and IF-180 retain separate authority. The judgment's row observations and the green instruments do not promote any child, counterpart or interface.
- The real publication projection was exercised in a disposable clone at the exact reviewed candidate, isolating only the independent-review gate that this round supplies while retaining the typed judgment, evidence, turn, map and disposition checks. It completed with `outcome=return`, `statuses={}`, `approves={}`, author/judgment provenance present, and `verification.mode=scope-no-product-bar`. No live registry or `docs/archive/last_approved` file changed. Its staged paths were only the expected mechanical WI-623 close, two successor mints and dependency re-points, id-watermark, and generated `PROJECT_STATE.html`, `docs/status.md` and `docs/stage` bookkeeping. Thus registry Status cells and snapshots remain unchanged; generated status surfaces truthfully reflect the close. No publisher ran in the primary checkout.
- The tracked pause and hand-authored stop instructions are unchanged. `parse_spec_row` reads WI-623 as `queued` with `Deliverable=''`, the expected pre-publication state. The coordinator remains paused; it owns the mechanical Deliverable write and close after this DONE review is logged. No control window, batch deletion, registry mutation, snapshot copy, push or main merge was performed.

Done-when obligations mapped to evidence:

| Obligation | Evidence |
| --- | --- |
| Validate the real decisions and required evidence | 52/52 unique RETURN decisions; 535 complete mappings; all 85 changed cells covered; one typed, committed ADJUDICATE judgment/session join. |
| Obtain independent review/provenance before publication | This round used the authorized nonempty retrospective range and independently exercised the bound production readers and projection. Coordinator logging remains the mechanical next act. |
| Publish an accepted outcome or truthful RETURN with scoped dispositions | RETURN accepts zero cells, omits acceptance-only ledgers, and parses two complete scoped drafts; the disposable projection succeeds with no registry Status or snapshot effects. |
| Preserve unchanged parents, separate child/interface authority and enduring regressions | No registry, interface, implementation or test path is in the reviewed work range; the full continuation preserves the named authority split and reservations. |
| Coordinator writes Deliverable and closes only on DONE | Live parser reports `queued` and empty Deliverable; no model-side close occurred. The real projection demonstrates the coordinator-owned mechanical close without mutating the primary checkout. |
| Keep the coordinator paused and forbid control-window/batch/push/merge acts | Tracked pause and stop instructions are unchanged; none of the forbidden acts occurred. |

Instruments, each requested command invoked once on the reviewed checkout:

`/Users/diytechy/Documents/ai-template/.venv/bin/python project-trajectory/scripts/check.py --jobs 0`

```text
Check summary (stage DevStg-Tests, tier all):
  PASS  smoke            54.6s
  PASS  registry-integrity 5.0s
  PASS  derived-stage    0.4s
  PASS  vocabulary       3.2s
  PASS  need-form        0.1s
  PASS  privacy          4.1s
  PASS  doc-navigability 3.0s
  PASS  design-flows     0.4s
  PASS  trajectory       9.2s
  PASS  approval-fresh   1.5s
  PASS  skills-index     0.2s
  PASS  prompt-catalog   0.3s
  PASS  verdict-rollup   0.2s
  PASS  staged-divergence 0.5s
  PASS  approval-immutable 0.3s
========================================================
RESULT: PASS
```

The smoke step reported `1696 passed, 4 skipped in 53.96s`; its enforced wall result was `54.6s vs 90s budget -> within`.

`/Users/diytechy/Documents/ai-template/.venv/bin/python project-trajectory/scripts/trace.py --strict-integrity`

```text
Traceability: SN=27 SR=79 LLR=192 TC=194 orphans=0 integrity=0 verified-mechanized=71 verified-demonstrated=4 verified-attested=0 drafts=17 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=168 interface-findings=0 paraphrase-advisories=3. Report -> docs/test/report.md
```

I tried to break the final candidate on acceptance scope, provenance, continuation, authority, review identity and publication effects and found no defect.

VERDICT: APPROVE findings=0
