# Cross-check of the third Fable revision

**Source:** `9f938edd6f558fb47803d95cd7de22d66f372358`, compared with
`360a075a`, 2026-09-05. This review checks Claude's edits and incorporates the
owner's subsequent adopter requirement. It does not launch another model
review, implement the runtime, change live authority or remove the pause.

**Verdict:** keep the smaller direction with the qualifications below. The
additive smoke step and minimum metrics writer are reasonable P0 proposals,
but their claims must remain narrower than full regression coverage or complete
billing. The active documents have been reconciled; historical Fable reviews
and the earlier hats sweep remain unchanged by this sitting.

## 1. Dispositions

| Third-review item | Assessment | Correction or retained direction |
|---|---|---|
| C1: custom smoke step instead of a selector | **Partly valid.** The current DevStg-Tests plan has no product step and the existing custom-step grammar supports the proposal. | Additive baseline only. Several integration suites are excluded from smoke. Adding a check need not amend SN-007, but calling smoke fulfillment of its whole-suite promise would. Preserve the existing WI bar/changed-behavior evidence and the unresolved cadence review. |
| C1: decide an expected-red exclusion marker later | **Not a settled solution.** Excluding a failing test changes selection; the existing smoke convention partitions tests by module. | Review the specific test-definition evidence and its transition to implementation acceptance before changing selection. No ad hoc marker or permission to relabel a regression. |
| C2: one ruling agenda | **Valid, incompletely applied.** The designated agenda still recommended objective_refs and the larger metrics contract, and P0 still said to extend inadequate measurement automatically. | Reconcile that agenda and P0 with the selected prose-only, minimum-record and targeted-repair directions. No duplicate decision authority. |
| O1: prose-only objectives | **Valid simplification.** The optional reference carrier can wait. Calling it a new approval tier was inaccurate; its real cost was schema maintenance. | Keep prose anchors and ordinary purpose review. Mark carrier sections explicitly deferred, including their old implementation checklist. Adopter semantic review is still needed without a carrier. |
| O2: minimum invocation record | **Valid scope cut with a necessary limit.** Raw values cannot safely feed a control comparison without known meaning. | Keep counter scope, unknown coverage and stable invocation/result identity. Defer delta/child aggregation by excluding non-comparable values from totals, not by blindly summing them. No new billing service or general replay engine. |
| O2: defer spool/recovery work | **Valid for P0 machinery; not a waiver of P5 correctness.** Existing results can be reread, and the proposal still promises a row for failed calls. | Use the existing retained result/log carrier; report missing data honestly. Protect the frozen reviewed tree before enabling P5, with concrete storage chosen in that experiment. |
| O3: extend FIRST-RUN-ADOPTER | **Valid alternative to this reviewer's separate upgrading hat.** Both questions must remain explicit. | Keep the existing ID and include first-use and existing-adoption compatibility. This is this repo's roster choice, not a prohibition on new hats for adopters. |
| O3: route H2–H5 through the disposition map | **Valid sequencing.** Those are observed missing clauses, not an instruction to mint a fixed number of SRs. | Preserve each obligation or obtain its explicit amendment/retirement. H6 remains implementation debt, H7 carrier reconciliation. Fewer rows alone does not dispose of either. |
| O4: reconciliation only for overlapping slices | **Valid.** The active wording still required the full procedure for each slice. | Make a brief overlap check first; require the detailed worksheet only for overlapping queued/active/preserved work. |
| GAP-1: insufficient evidence defaults to targeted repair | **Valid operating posture.** It does not turn an inconclusive result into proof of success. | Report insufficient evidence, keep replacement closed and allow independently justified repairs. Another measurement window requires a ruling. |
| GAP-2: exempt any diff outside scripts/tests from timed smoke | **Not adopted; too broad as stated.** A process dial, stack command, dependency manifest, hook or prompt can change behavior without touching either directory. | A future documentation-only rule must identify inert prose and retain applicable checks for behavior-bearing inputs. This review does not change CLAUDE.md, skills or the budget. |
| GAP-3: contradictory reviewers | **Valid with scope qualification.** Opposing decisions about the same criterion need the existing bounded dispute path. | Carry round/reviewer provenance. A new finding on new content, or an old finding already fixed, is not automatically a dispute or another mandatory arbitration. |
| GAP-4: coverage judgments are one reader's review | **Valid.** | Keep source inspection distinct from independent blind derivation and implementation-test evidence. |

## 2. Checked counterexamples and evidence

- `check.py --stage DevStg-Tests --list` currently prints fourteen process
  steps and no product step. `check.extra_steps` accepts `command` and
  `from-stage`, defaulting to a product step. No live stack edit was needed to
  verify that grammar.
- [tests/conftest.py](../../tests/conftest.py) lists `test_integrate`,
  `test_integrate_admission`, `test_integrate_station` and `test_integrate_unload`
  in SLOW_MODULES. C1's broken-integrator example is therefore not generally
  solved by smoke. No planted source regression or station run was performed.
- If a provider returns cumulative conversation usage 100 then 150, summing
  the two raw values reports 250 rather than the 150 conversation total.
  Recording raw values is fine; treating them as two invocation costs is not.
  This is a semantic counterexample, not a claim about a particular CLI format.
- P0 consumes aggregate/comparable cost and token evidence, so it already needs
  to distinguish non-additive or unknown values. A small minimum record can
  preserve that distinction without implementing cumulative arithmetic.
- The designated CROSSCHECK-BRIEF §3 still said optional objective_refs after
  the active VISION-OBJECTIVES header deferred it. IMPLEMENTATION P0 still said
  to extend inadequate measurement while EXECUTION-DETAILS required a ruling.
  Both contradictions were in the reviewed commit, and are reconciled here.

The third review's statement that all historical reviews were unchanged is
also qualified: that commit added a dated addendum to the second review. This
follow-up preserves that addendum and makes no stronger hash claim about prior
versions. Its Worktrunk corrections are retained; no new external-tool trial
or station-adapter evidence is claimed.

## 3. The additional adopter obligation

[ADOPTER-REVALIDATION.md](ADOPTER-REVALIDATION.md) is the single plan home for
the owner's addition: reassess the roster against each adopter's vision and
context, potentially derive new hats, discover genuinely missing SNs and
rederive affected SRs. It distinguishes new stakeholder outcomes from
hat-derived constraints, and both from implementation debt under a sound SR.

The workflow applies to initial adoption and materially affected upgrades or
project changes. It preserves adopter ownership, existing approvals and work,
and permits a reasoned no-change result. It is neither an automatic bulk mint
nor a mandatory full rederivation on every kit update. P0/P1 defines it; P10
ships guidance and exercises populated adopter examples.

## 4. Review limits

This is a diff/source cross-check of planning documents. It verifies internal
consistency and grounds the selected counterexamples; it does not prove P5,
all provider formats or semantic adequacy of an adopter's eventual needs.
Validation and commit results are recorded in the session log fragment. Live
vision, hats, SN/SR rows, method, process dials and queue remain unchanged.
