# Authored H1/H2/H3/H4/H5 amendments

H2, H3 and H5 are authored as Drafted rows: `SR-184`–`SR-186` and `TC-209`–`TC-211`;
`SR-184` uses the direct Inspection route and `LLR-048` remains under `SR-154`.
H1's two subject tags and H4's acceptance cell are also authored under the
owner's execution instruction, after independent review. No approval act, snapshot write, stage advancement or WI state change occurred. Re-attestation remains owed for the amended
Approved rows `SN-007`, `SN-026`, and `SR-162`; the new SRs/TCs await ordinary
first approval, and their behavior and Inspection results remain open. The source findings are [HATS-AND-DECOMPOSITION-REVIEW.md](HATS-AND-DECOMPOSITION-REVIEW.md#h2--sn-024s-rubric-contract-disappears-at-the-sr-tier),
with the live parent cells at `docs/requirements/stakeholder-needs.toml:137-142`
(SN-007), `docs/requirements/stakeholder-needs.toml:174-183` (SN-012),
`docs/requirements/stakeholder-needs.toml:196-205` (SN-024),
`docs/requirements/stakeholder-needs.toml:211-217` (SN-026), and
`docs/requirements/stakeholder-needs.toml:276-285` (SN-037). H1 and H4 below are authored need-tier metadata/acceptance amendments; H2, H3
and H5 are authored Drafted SRs with direct Drafted Inspection TCs.

## H1 — record the legal and data-protection applicability of SN-026

**Disposition: authored a metadata-only amendment to the existing `SN-026`; need-tier re-attestation remains owed.**
Its normative `need` and `acceptance` cells remain byte-for-byte unchanged.
The live tag amendment records two applicable lenses; it does not alter managed
selection, consent, or the provider inclusion rule. The current row is at
`docs/requirements/stakeholder-needs.toml:211-217`; the activating content and
consent surface is `SR-175` at `docs/requirements/system-requirements.toml:941-952`, whose
`hat_refs` already name `DATA-PROTECTION` and `LEGAL`.

Authored changed cell (the other cells in `SN-026`, including `status`, `need`,
`why`, `priority`, and `acceptance`, are retained exactly):

```toml
[need.SN-026]
tags = ["unattended", "loop", "legal", "personal-data"]
```

The tags match the existing roster predicates, `LEGAL` and `DATA-PROTECTION`
(`docs/requirements/hats.toml:125-133`). The tag edit intentionally changes
the SN × conditional-hat applicability matrix: both lenses now reach SN-026.
Under SN-036/SR-161, they use the existing `SR-175` decomposition home; no
further SR is owed for this lens attribution. Its declared-set and
planted-credential obligations remain unimplemented, so the amendment does not claim those obligations are discharged. The H1 execution
slice proves the parsed parent-context path. `SR-175`'s rationale records
amending SN-026 as rejected option (b), “one rule, one home”; this amendment
records the DO-178C feed-back applicability step and leaves the inclusion/
consent rule in SR-175. Authoring the two tags is complete; need-tier re-attestation remains owed. This
does not write an approval snapshot. Any approval act remains on the existing
need-tier path. Provider selection, CI and test tiers are
unchanged.

## H4 — reconcile SN-007's landing promise with declared cadence

**Disposition: authored an acceptance-only amendment to the existing `SN-007`; need-tier re-attestation remains owed.** The prior acceptance (`docs/requirements/stakeholder-needs.toml:137-142`) required
a green whole suite before each change. The authored cell keeps the declared bar
and the Full-suite scaffold/every-script promise; existing process and stack
configuration continue to own tier cadence.

Authored changed cell (the current `need`, `why`, `priority`, and `status` are
retained):

```toml
[need.SN-007]
acceptance = """The declared bar is green before a change lands. The Full-suite run bootstraps a temp scaffold and exercises every delivered script."""
```

This preserves the whole-suite evidence and every-script exercise while leaving
test-tier cadence to its declared source. It reuses `SR-010`'s scaffold
and every-script evidence (`docs/requirements/system-requirements.toml:40-51`) and
`SR-151`/`SR-152`'s hosted invocation and verdict backstop
(`docs/requirements/system-requirements.toml:634-658`); it does not create a second CI selector
or a new test-tier gate. The existing process separately requires test-first implementation at
`project-trajectory/PROCESS.md:491-496` and reports legitimate failing-first
test-definition work honestly; this acceptance amendment does not restate that
ordering rule. No selector, CI, or test-tier change is enabled by this document.

## H2 — record rubric provenance and numbered critique anchors

**Disposition: authored `SR-184` under `SN-024` as a Drafted row; leave `SR-154` and
`SR-155` unchanged.** `SR-154` owns unattended scheduling, family routing, consent,
logging, rework and escalation (`docs/requirements/system-requirements.toml:660-672`), while
`SR-155` owns its narrower contested-planning round. The missing obligation is
the common fresh-review/rubric/anchor record for subjective acceptance,
including attended Critique. The new SR closes SN-024's author-independence
promise at the SR tier: it requires a fresh non-author verdict against the
intent-derived rubric and numbered anchors. Keeping it separate avoids adding
a second independent decision to the broad unattended contract and leaves
family/degradation policy where it already lives.

Authored live row (`SR-184`, still `Drafted`; approval is a separate tier-authority act):

```toml
title = "Critique acceptance records intent-derived rubric anchors"
sn_refs = ["SN-024"]
boundary_refs = ["B-05"]
hat_refs = ["TEST-ENGINEER", "PRODUCT-FITNESS"]
requirement = "Where a delivered capability requires Critique acceptance, the delivered acceptance record shall identify a fresh reviewer session that did not author the artifact, apply a written rubric derived from the applicable SN/SR intent, and record each verdict and finding against numbered rubric-anchor ids."
acceptance_criteria = "A Critique acceptance record identifies the fresh non-author session, names the rubric and its SN/SR intent sources, and ties every verdict and finding to a numbered rubric-anchor id; a rubric copied from the verifying TC without independent derivation from the SN/SR intent is an Inspection finding, as is a missing reviewer, rubric, intent basis or anchor citation; this Inspection checks process and provenance and does not replace the Critique judgment of the produced artifact."
rationale = "Carries SN-024's omitted author-independence, rubric provenance and anchor obligation as one coherent Critique acceptance decision. It applies to attended and unattended Critique acceptance; SR-154 remains the home of the underlying brief, unattended scheduling, consent, family selection and family diversity, degradation and escalation, and SR-155 remains the contested-plan state machine. The attended case does not mandate a second provider family or vendor. LLR-048 already assembles the rubric/intent/artifact brief and LLR-076 already refuses a missing dual-plan rubric; those mechanisms remain under SR-154 rather than being re-homed here. The acceptance record's process/provenance completeness is inspectable, while artifact adequacy remains the independent Critique judgment."
priority = "S"
verification = "Inspection"
status = "Drafted"
phase = 5
```

Existing lower-chain evidence to reuse:
`LLR-048` (`docs/requirements/low-level-requirements.toml:511-520`, `TC-048`,
`tests/test_agent_loop_critique.py`) for the fresh critique brief and
`LLR-076` (`docs/requirements/low-level-requirements.toml:744-753`, `TC-076`, `tests/test_dual_plan_round.py`) for fresh
 dual-plan sessions and missing-rubric refusal. `LLR-048` remains under `SR-154`, while the implementation gap is explicit
rubric derivation from SN/SR intent and per-finding numbered anchor citations
across every Critique path, including attended use. Because
`SR-184` is an Inspection of an acceptance record, it is eligible for a direct
`TC` procedure without inventing an LLR/TC mechanism pair.

The direct TC Inspection should inspect a record whose rubric is copied only
from a permissive TC and whose verdict omits an anchor: it must find both gaps
even when the builder's artifact and all TC assertions pass. Do not mirror the
builder's test suite or assert the same rubric string in two places.
An independent TEST-ENGINEER/PRODUCT-FITNESS review must judge whether the
rubric covers the parent intent and whether anchor citations explain findings.

## H3 — require a coordinated change record at the requirement/interface seam

**Disposition: authored `SR-185` under `SN-037` as a Drafted row; leave mechanical
`SR-162` unchanged.** `SR-162` owns boundary-reference, endpoint and signal-type
resolution (`docs/requirements/system-requirements.toml:766-778`). Its rationale explicitly
leaves the reviewed counterpart-change clause unimplemented. That clause is a
distinct semantic review obligation, so appending a second `shall` and a second
decision to SR-162 would mis-state the existing harness contract.

Authored live row (`SR-185`, still `Drafted`; approval is a separate tier-authority act):

```toml
title = "Coordinated requirement/interface change review"
sn_refs = ["SN-037"]
boundary_refs = ["B-05"]
hat_refs = ["CONSISTENCY", "MAINTAINER", "TEST-ENGINEER"]
requirement = "When a reviewed change alters one side of a requirement/interface relationship, the change record shall identify the affected counterpart and carry the corresponding change or an explicit justification for retaining it."
acceptance_criteria = "For every reviewed change that alters one side of a requirement/interface relationship, the review record names the changed side and affected counterpart, either includes the corresponding change or records an explicit justification; the independent reviewer's semantic decision is recorded and is not discharged by reference-existence tests."
rationale = "Carries the final clause of SN-037 as a separate semantic review obligation because SR-162 already owns the mechanical frame and interface resolution. A citation-only provenance check cannot establish that a changed signal or requirement still means the same thing at its counterpart; the record must expose the decision for an independent review."
priority = "M"
verification = "Inspection"
status = "Drafted"
phase = 5
```

Reuse `LLR-187`
(`docs/requirements/low-level-requirements.toml:1942-1952`) and `TC-182`/
`tests/test_external_frame.py` plus `tests/test_trace_interfaces.py` for the
mechanical joins; `SR-185` needs a direct TC Inspection procedure and
does not need an LLR merely to mirror the resolver. The implementation gap is a
changed-side/counterpart record and its semantic review; the current LLR
expressly says that it cannot report incompatible seam types and that the
change-review rule is unimplemented.

The inspection case should present one side's changed signal meaning while
leaving every id, endpoint and reference resolvable; the result must require
the counterpart record or an explicit justification. Do not duplicate the
existing resolver tests or treat a second successful lookup as semantic
agreement. An independent CONSISTENCY/TEST-ENGINEER review must assess whether
the counterpart really preserves meaning; that judgment is the input to this
Inspection record.

## H5 — add one proportionality SR because no current row owns the decision

**Disposition: authored `SR-186` under `SN-012` as a Drafted row; do not amend an
optional-layer or complexity row.** `SN-012`'s acceptance expressly governs LLR/TC granularity
(`docs/requirements/stakeholder-needs.toml:174-183`), but its existing SRs own optional profiles,
registry rules, architecture checks, performance and complexity. `SR-183`
(`docs/requirements/system-requirements.toml:1028-1040`) measures source-function
complexity, not requirement decomposition. Putting proportionality into
`SR-157`, `SR-159`, or `SR-183` would give a checker or one optional feature a
false ownership of a package-wide authoring decision.

Authored live row (`SR-186`, still `Drafted`; approval is a separate tier-authority act):

```toml
title = "Proportionate requirement decomposition"
sn_refs = ["SN-012"]
boundary_refs = ["B-05"]
hat_refs = ["MAINTAINER", "PRODUCT-FITNESS"]
requirement = "The delivered requirements process shall require each additional child within a required tier to carry an independent decision or verification purpose, and record the stopping decision in the scoped decomposition record, while retaining the required SN-to-SR-to-LLR-to-TC tiers and linking real verification to the existing obligation."
rationale = "Carries SN-012's unowned granularity clause as a process requirement on what the delivered process requires and records. A child that only paraphrases a parent or duplicates another child's verification adds review and maintenance cost without an independent decision. The process records the stopping decision within the required spine; this row does not guarantee adopter behavior beyond that record, and it never permits omitting a required SN→SR→LLR→TC tier or replacing real verification with a count. It does not impose a row-count cap, deletion quota, or new machine gate. Existing process doctrine and the spine-authoring adjudicator questions are the source of the judgment, while mechanism-specific evidence remains with its current SR."
acceptance_criteria = "For a reviewed decomposition, each additional child within a required tier has an independent decision or verification purpose traceable to its parent; when further splitting would only paraphrase or duplicate, the existing scoped decomposition/review record states why the process stops at that independent-value boundary."
priority = "S"
verification = "Inspection"
status = "Drafted"
phase = 5
aspect = "process"
```

No lower-chain row exists for this outcome. A direct `TC` Inspection can read
the same scoped decomposition/review record required by `SR-161`
(`docs/requirements/system-requirements.toml:753-764`), including its
applicability/no-finding fields where that SR applies; an LLR would add no
mechanism and would only mirror the authoring judgment. Reuse
`project-trajectory/PROCESS.md` §3 and
`project-trajectory/PROCESS_OPTIONS.md`'s proportionality doctrine, the
`spine-authoring` questions on one decision/one home and stopping at the
mechanical value boundary, and that existing record as inspection evidence.
The implementation gap is recording the proportionality decision in this
existing scoped surface; no new schema, review form, ratchet, count sensor or
mandatory LLR/TC pair is justified by this authored process row.

The counterexample is a small edit in a repository with every optional layer
disabled that nevertheless receives a chain of paraphrasing LLR/TC rows while
all existing optional-profile checks pass. A mirrored test that merely counts
rows or replays the same decomposition cannot judge independent value. An
independent MAINTAINER/PRODUCT-FITNESS review must decide whether a
child adds a distinct decision or verification value, recorded in that same
scoped decomposition/review surface.

## Direct Inspection TC mapping

The three authored `Inspection` SRs each have one direct Drafted TC. The
procedures live in the durable
[`docs/test/inspection-procedures.md`](../test/inspection-procedures.md), one
section per subject under a stable anchor that carries no packet numbering and
no result state:
[Critique acceptance provenance](../test/inspection-procedures.md#critique-acceptance-provenance-inspection)
(`TC-209`),
[requirement and interface counterpart review](../test/inspection-procedures.md#requirement-and-interface-counterpart-review-inspection)
(`TC-210`) and
[decomposition proportionality](../test/inspection-procedures.md#decomposition-proportionality-inspection)
(`TC-211`), each with a result subsection. Each TC `method` names its
procedure anchor and its `evidence` names the corresponding result anchor.
Those result subsections say `Not executed; reviewer/date/result pending` until
a reviewer records an actual inspection. No passing inspection is claimed.

`SR-184` is LLR-exempt under the direct Inspection route; `LLR-048` and `TC-048`
remain evidence for the existing SR-154 brief mechanism. The governing process
clauses are:

> Every SR → ≥1 LLR (or Analysis/Inspection/Attest); every SR and LLR → ≥1 TC.
> (`project-trajectory/PROCESS.md:482-487`)
>
> Only `Analysis`/`Inspection`/`Attest` SRs are LLR-exempt, and every SR needs
> ≥1 TC regardless of method. (`project-trajectory/PROCESS.md:737-744`)

The authored TCs are `TC-209` for H2, `TC-210` for H3, and `TC-211` for H5.
Their implementation and inspection results remain open.

## Review and sequencing

These are authored Drafted rows and authoring was authorized at this stage.
The existing tier authority separately decides approval and snapshot state after
independent review of the exact wording against the full SN cell, affected SR
rationales, LLR/TC evidence and current work. SR-184 and SR-185 need their
semantic behavior and fresh Inspection records; SR-186 needs its proportionality
record; the direct TCs currently document procedures only. Re-attestation is
owed for amended Approved rows `SN-007`, `SN-026`, and `SR-162`; the new SR/TC
rows need ordinary first approval. The need-tier debt, which no snapshot-drift
check reaches, is carried as an owner decision in
[`docs/requirements/open-items.toml`](../requirements/open-items.toml) (OI-85),
together with the SN-024 question of whether its family-heterogeneity clause
binds attended Critique acceptance; SR-184's rationale no longer answers that
question on its parent's behalf. H1/SR-175 consent or provider-inclusion work
remains open, and none changes the LLR-176/build-surface redaction boundary.

## Opus disposition map

| Review finding | Disposition |
| --- | --- |
| B1 — H4 mid-phase bar | H4 now assigns the Full suite only to phase close; the per-commit bar remains Smoke under the declared moment-to-tier table. |
| B2 — H4 introduced extra obligations | Rejected from H4. Test-first ordering already belongs to `project-trajectory/PROCESS.md:491-496`; cadence exceptions stay in the existing session log, with no new need cell, reader, selector, or gate proposed. |
| B3 — H1 tags affect applicability | Recorded as intentional: the SN × conditional-hat matrix changes, both lenses use SR-175's existing decomposition home, no further SR is owed for attribution, and SR-175's substantive work remains open. The rejected “one rule, one home” option remains owned by SR-175. |
| B4 — H2 attended independence | Closed at the new SR: a fresh non-author Critique verdict uses the intent-derived rubric and numbered anchors for attended and unattended acceptance. Its `Inspection` TC checks process/provenance; Critique remains the artifact-quality judgment. SR-184 remains direct Inspection and LLR-exempt; LLR-048 stays under SR-154. |
| B5 — H3 verification coherence | H3 now has one `Inspection` method, a recorded independent reviewer's semantic decision, and an inspection case rather than a regression or alternative `Attest` path. |
| B6 — H5 record/artifact sprawl | H5 points to the existing scoped decomposition/review record and SR-161 applicability/no-finding record where applicable; its direct TC is one inspection procedure, with no new schema, form, or review session. |
| B7 — direct-TC permission | The governing PROCESS clauses are summarized above with `Inspection` LLR-exemption and all-SR-needs-TC references; SR-184 uses the permitted direct route. |

The [independent closure review](../reviews/2026-09-06-redesign-amendment-closure-opus.md)
returned **APPROVE** for the prior proposal wording packet. That review is a
wording and decomposition review, not approval of the subsequently authored
live rows, their direct Inspection procedures, or their unimplemented behavior.
The final authoring review's corrections are applied to the live rows and to this record;
no Status or approval snapshot is changed.

SR-186 retains the optional `aspect = "process"` because the row is a process obligation; SR-184 and SR-185 omit that optional cell rather than inflating the schema. Hat-Refs follow current `listens_for` clauses: SR-184 uses TEST-ENGINEER and PRODUCT-FITNESS, SR-185 uses CONSISTENCY, MAINTAINER and TEST-ENGINEER, and SR-186 uses MAINTAINER and PRODUCT-FITNESS.
