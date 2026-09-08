### REVIEW-A — WI-623 adjudication — Round 25 — 2026-09-07
Verdict: CHANGES-REQUESTED
Findings:
- [BLOCKER] docs/iteration/contract_split-024-20260907-195258.log:6 -> The final Approval evidence names the 024 judgment, but the committed session is DESIGN-CHECK (also role/prompt-template), with empty primary-turn, judgment and candidate fields. The publisher finds no typed ADJUDICATE judgment at the final candidate; supplying this round's review alone cannot make the proposed direct publication succeed. -> Reconcile the actual invocation and committed provenance through the coordinator under this same pending turn; establish a truthful ADJUDICATE session/judgment/candidate join and bind the Approval evidence to it, then obtain the owed independent review. Do not relabel a DESIGN-CHECK invocation as ADJUDICATE without actual invocation evidence or bypass provenance validation. -> @coordinator
- [MINOR] docs/reviews/contract_split/024-ADJUDICATE-b064550.md:20 -> The statement that each changed-cell set equals its decision map is false: LLR-058 changes only Title, while its map also includes unchanged Detail, CodeSymbol, Status, TestRefs, Module, Phase, Component and SR-Refs. Across the candidate, 535 mapped cells contain 85 actual changes. -> Correct the evidence statement to say that every changed cell is covered by the complete supplied maps, which also retain unchanged cells; preserve all maps and zero acceptance, and keep the corrected judgment/evidence bindings consistent. -> @adjudicator

Worst failure classes tested, in order: unauthorized acceptance or snapshot absorption through RETURN; missing or mismatched judgment/session authority; narrowed continuation or transferred first-approval ownership; an empty or rebound review input; premature publication or coordinator restart. The second class breaks this candidate. Green instruments do not discharge it.

Reviewed HEAD: b954b8f4843aedb86a87f48467063f785dddabd0; candidate work commit: 8f6397da. Governing tree identity: ac29f570d78c5793208f5de7b800dd6b76dbdad997eb569773380a1216f54025. Working tree was clean at entry. Used exactly the owner-authorized range:

```sh
git diff c492da3dd0e6247610bf0af116305e989d1d17f7...HEAD -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ':(exclude)docs/log.md' ':(exclude)docs/log.d' ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'
```

This is nonempty: only docs/work/queued/WI-623-adjudicate-complete-combined.md, 746 added lines. Separately inspected the committed ADJUDICATE judgment records, including final 024 and historical 022, and the coordinator-authored session headers. The owner's authorization resolves the earlier empty-diff permission/input blocker without erasing the earlier CHANGES-REQUESTED records. It does not supply missing adjudicator provenance.

Independent evidence, derived from Git objects and executable publisher paths rather than implementer validation claims:

- Parsed the final Approval with primary_approval.parse_approval_payload. Exactly version/turn/base/proposal/decision are present: no acceptance-only impact or absorption tables. All 52 unique scope rows classify as return. All before/after maps have identical keys; before values name the bound approved registry blob, after values name the bound live blob and match HEAD. Independently parsed both registry versions and confirmed every changed cell is covered: 85 changed cells within 535 supplied cell mappings. Zero cells are accepted. These counts were derived by /tmp/wi623-review25-drive.py against the reviewed HEAD, comparing primary_approval.registry_rows values and counting the payload maps (fig: independent Git-blob comparison at b954b8f4843aedb86a87f48467063f785dddabd0).
- Turn WI-623-c492da3dd0e6247610bf0af116305e989d1d17f7, base c492da3dd0e6247610bf0af116305e989d1d17f7 and proposal ef6086929ee50393352e6ed98be68d9c1f5e995b18a720c447c594c7d643298e match the selected turn and recomputed base tree identity. The turn record blob is unchanged from selection 327481e5 through HEAD: 4aace8e848fa577f2a7b57d74f4423197b6fe659. The spec before Approval is identical to the base except trailing whitespace.
- All evidence references name ancestor a62cc7d734947857ee634dcd15591428fc26c1b0, which writes only the final 024 judgment, whose blob remains identical at HEAD. This establishes artifact identity, but not session authority: primary_approval._judgment_records(root, HEAD, turn, "amendment") returns []; _machine_author returns None. Round 024's committed header identifies DESIGN-CHECK and supplies none of the required three bindings. Earlier ADJUDICATE records do not bind the new governing tree.
- intake.parse_dispositions accepts two drafts. The first supersedes WI-623, retains its SR references and every prerequisite plus WI-623, names every original scope ID and carries the complete original Context byte-for-byte. It preserves WI-606, the IF-175 owner, WI-618/IF-180, all Drafted riders, the LLR-061/TC-061 conjunctive predicate, LLR-167 validity purposes, LLR-153/154/207 allocation, PC-BATCH-USES retirement duties, original parent/counterpart rationales and the stated proof limits. WI-601/WI-603/WI-605 remain restructured history. The second is an ordinary machinery repair draft; it does not replace or narrow the semantic continuation. Its proposed resume repair is not evidence that the current final candidate is publishable.
- Applied PROCESS.md §5 and the live/approved registry distinction, particularly LLR-140, LLR-153, LLR-154 and LLR-207 with TC-147/148/205. IF-090, IF-091 and IF-180 remain Drafted and retain separate authority. The reviewed range changes no requirement registry, approved snapshot, test-case registry, tests, docs/status.md, docs/stage or tracked pause. Parent acceptance and enduring regression tests remain intact. Source-review approval, row observations and passing tests supply no semantic acceptance.

Real publication-path probes:

1. approval_projection(..., require_provenance=False) returns outcome=return, statuses={}, approves={}, with all 52 return findings. This intentionally provenance-free diagnostic is not publication authorization. Calling the real _apply_approval with that zero-effect plan leaves Git status unchanged; its Status loop and snapshot-copy branch do not execute.
2. Unmodified approval_projection(..., require_provenance=True) and primary_publication.derive_tree(..., import_objects=False) both refuse: `candidate lacks its required independent review phases`. No publication was performed.
3. To test whether this review alone could remove the hold, temporarily replaced only primary_approval._review_refusal with a no-op in the diagnostic Python process, retaining every judgment/evidence check. Both approval_projection(require_provenance=True) and the real disposable-clone derive_tree path then refuse: `primary approval: REFUSED — evidence ref 'a62cc7d734947857ee634dcd15591428fc26c1b0' has no typed judgment bound to this turn and candidate`. Restored the function afterward. No repository source, provenance record or approval was changed. This is the decisive reproduction of the blocker, not a fabricated successful publication.

The RETURN acceptance projection has no registry Status or snapshot effects. Successful publication would still perform the explicitly expected mechanical WI close, successor mint, watermark and generated-surface updates; it is not a promise of zero bookkeeping writes. Full successful publication of this actual candidate cannot be certified because its provenance fails. The coordinator remains paused: tracked docs/work/pause and the stop instructions in docs/status.md are unchanged. No coordinator, control window, push, merge or publisher was started.

Done-when obligations (spec's carried completion clause at line 85):

| Obligation | Evidence / disposition |
| --- | --- |
| Validate real decisions and required evidence | Scope/maps pass; final typed judgment/session provenance fails as finding 1 demonstrates. |
| Independent review/provenance before publication | This independent round rejects publication; logging it cannot repair the missing ADJUDICATE join. |
| Accepted outcome or truthful RETURN with scoped dispositions | RETURN has zero accepted cells and complete dispositions; the atomic publisher remains held. No acceptance-only ledgers are required for this outcome. |
| Coordinator writes Deliverable and closes only on DONE | The queued spec and empty/absent Deliverable remain appropriate; no model-side close was attempted. Completion is not claimed. |
| Preserve parents, separate child/interface authority and regression tests | Registry/snapshot/test paths unchanged; full original Context and all reservations carried into the continuation. |
| Remain paused, with no control window, push, main merge or batch deletion | Pause and status instructions retained; no such operation performed. |

Instruments, each requested command invoked once on the reviewed checkout:

`/Users/diytechy/Documents/ai-template/.venv/bin/python project-trajectory/scripts/check.py --jobs 0`

```text
Check summary (stage DevStg-Tests, tier all):
  PASS  smoke            55.8s
  PASS  registry-integrity 5.6s
  PASS  derived-stage    0.4s
  PASS  vocabulary       3.4s
  PASS  need-form        0.1s
  PASS  privacy          4.3s
  PASS  doc-navigability 2.9s
  PASS  design-flows     0.4s
  PASS  trajectory       9.9s
  PASS  approval-fresh   1.6s
  PASS  skills-index     0.2s
  PASS  prompt-catalog   0.2s
  PASS  verdict-rollup   0.2s
  PASS  staged-divergence 0.3s
  PASS  approval-immutable 0.2s
========================================================
RESULT: PASS
```

`/Users/diytechy/Documents/ai-template/.venv/bin/python project-trajectory/scripts/trace.py --strict-integrity`

```text
Traceability: SN=27 SR=79 LLR=192 TC=194 orphans=0 integrity=0 verified-mechanized=71 verified-demonstrated=4 verified-attested=0 drafts=17 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=168 interface-findings=0 paraphrase-advisories=3. Report -> docs/test/report.md
```

Additional validation: the harness smoke step reported `1696 passed, 4 skipped in 55.31s`; its enforced wall budget reported `55.7s vs 90s budget -> within`. Targeted `pytest -q -n auto tests/test_primary_approval.py tests/test_primary_publication.py tests/test_primary_adjudication.py` reported `60 passed in 31.33s`, including finite RETURN projection and actual publication/replay regression fixtures. `check_docs.py --root . --stale` exited zero: `1570 doc(s), 2524 intra-repo link(s), 0 broken (1 orphan warning(s))`. These checks do not establish semantic acceptance or repair missing real-session provenance.

Record-only commit: only this verdict is committed. Hooks are disabled for this invocation to honor the requested once-only instruments and verdict-only scope; the hook invokes check.py again and requires a generated rollup edit. No candidate check is waived into approval, and rollup/session bookkeeping remains the coordinator's responsibility.

VERDICT: CHANGES-REQUESTED findings=2
