Reviewed: 5a76f75c830a7da1706faf6b2306ae6d355fd61a

### PLAN-CRITIC (independent Codex session) — Plan decomposition — Round 1, confirming — 2026-10-21

Provenance: fresh non-author reviewer session launched through the supplied coordinator invocation; assigned record: 2026-10-21-leg11/crit1/WI-969-plan-critique-1.md. No provider session id was supplied. This is the one confirming critique, in convergence stance. The invocation's final addendum requires scratch-only recording and no commit; no checkout file was changed.

Artifact inspected: docs/plans/WI-969/plan.md, read directly with git show at the Reviewed commit. This is a text artifact; no image or description proxy was needed. The plan's historical claims were not accepted as evidence. No excluded critique, review, decision, implementer session-note, docs/status.md or docs/log.md file was opened.

Rubric: docs/rubrics/plan-decomposition.md at the Reviewed commit, blob 4f183eb6aa17a459c9b0741391791d03a8f76293; single-plan application and this invocation's stricter confirming-review severity rule.

Intent sources: docs/work/active/wi-969/WI-969-a-disposition-adopts-an-existi.md in full and its specref, docs/work/partial/WI-902-disposition-adopts-existing-successor.md, at the Reviewed commit. Their text from Deliverables onward is byte-identical. SR-148 and SR-220 were read in docs/requirements/system-requirements.toml, with their parents SN-006, SN-008, SN-010, SN-025, SN-027 and SN-029 in docs/requirements/stakeholder-needs.toml. The supplied coverage report and the cited/excluded TC rows in docs/test/test-cases.toml were checked against those obligations.

Rubric adequacy, checked before scoring: adequate for the scoped intent. The needs require tracked-state autonomy, honest gates, navigable records and gated integration; the scoped SR obligations require resolving handbacks and preserving consolidation semantics. DevStg-Tests and B2 require substantive coverage of those obligations through the item's Done-when, rather than treating TC citations as proof. DevStg-Reqs, DevStg-Impl, G4 and B1/B3/B4 test whether that coverage can be built with distinct owners and a truthful dependency order. The single-plan DELTA test additionally requires the new record, grammar and dependent outputs to be carried. No missing anchor or derivation from a permissive TC was identified.

Transfer caveat: the debate/selection evidence comes from QA, mathematics and code with objective verifiers. It does not benchmark plan artifacts; reconciliation for plan quality remains an open research gap. This rubric is an extrapolation, not a proven instrument.

Anchor coverage and judgment:

- DevStg-Reqs: satisfied. P0-P13 identify concrete deliverables and checkable exits. The build rows distinguish pure parsing/validation, lineage corrections, record storage, close production, commit admission and sweep consumption. P7 is substantial but specifies the owning rule, integrations, admission table and concrete checks without leaving a design ruling to the builder.
- DevStg-Tests: satisfied. D1-D23 have substantive delivery and verification steps. The exclusions concern unchanged scheduling, open-item integrity and historical absorption behavior; adoption-specific consolidation refusal remains covered. P2 establishes test evidence before implementation; P3-P8 name the behavior each implementation step turns green, and P11-P13 carry review, adjudication and landing checks.
- DevStg-Impl: satisfied. The declared split reasons explain the multi-coverage: production versus consumption, tests versus implementation, intent versus adjudication, and authored upgrade guidance versus landing re-anchoring. These are distinct deliverables.
- G4: satisfied. Intent precedes tests; parsing and the record cell precede close production; close production precedes commit admission and sweep fixtures; the lineage correction precedes the sweep's full-successor join. The final chain consumes the completed implementation, review results, reconciled spine and landing checks. No missing artifact dependency was identified.
- B1: satisfied. The proposed seams name their nearest existing interfaces and different owners. The shared close-shape reader amends IF-175 rather than introducing a competing close recognizer; the exact relink operation consumes spec_move.exact_relink.
- B2: satisfied. The D citations correspond to concrete outputs and checks, including the real-close regression in P7 and the repository census in P3. The reported 23/23 coverage is supported by the plan's substance.
- B3: satisfied. The record port, intent, test-first step, upgrade guidance, review/checkpoint and landing steps each produce independently checkable artifacts or evidence; none simply repeats another step's completion condition.
- B4: satisfied. The predecessor edges carry the artifacts described above. The tests-only predecessor is justified by the declared test-first process; the checkpoint and landing consume recorded review and adjudication results.

DELTA: within is correct. The adoption block and Adopted cell extend existing data domains; close output, sweep re-pointing and commit admission gain the request/record inputs. P3/P5/P6/P7/P8 carry those changes and P1/P12 carry their contracts. The terminal record adds no workflow state, and the git-tree reads and relink oracle use existing system boundaries.

Independent code check: handback._archive_one_adjudication_row calls spec_move.move_spec, whose inbound-link traversal reaches markdown throughout the repository. kitlib.verdict._closed_wi_ids currently rejects any path outside docs/work/. P7 addresses that real mismatch by injecting the existing byte-exact oracle only into record admission, leaving mechanical_close_attestation without it. Its real-close, altered-relink, wrong-subject and record/request mismatch tests distinguish admission from peel behavior. The squash step separately checks the staged record against the tip and walks the lane commits, rather than borrowing text-then-act's narrower exemption. This is a plan judgment; no implementation tests were run or claimed to pass.

Findings: none.

VERDICT: APPROVE findings=0
