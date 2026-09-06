# oi85-record-closure-structured — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `fc1d9eaccfced4695a7798114eb47a2a9cb835ec6985a30c86e5a84e17c20c64`

Tracked invocation: [session log](../iteration/call_1603bfd28a3d4d3c9fa678845717bdf6-20260906-160650.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

{
  "verdict": "APPROVE",
  "findings": [],
  "basis": "FRESH REVIEW IDENTITY. Attended Critique on the human-chosen Opus5/high route; assigned identity docs/reviews/2026-09-06-oi85-record-closure-structured-opus.md, which the launcher binds to a fresh invocation log. This context did not author the record, the prompts, the PROCESS_OPTIONS text, the skill text or the rubric, and did not produce the prior Critique — that review was read only as finding history, never as author self-assessment. No provider session id was supplied by the invocation, so none is stated (G1's never-invented rule). Tools were disabled: I judged the supplied text only. I ran no test, executed no code, and read neither the P9R source diff nor the registries beyond the excerpts supplied; TC-209/210/211, LLR-198, LLR-187 and TC-182 text was not supplied, so the H5 stopping decision is judged from the record's own descriptions of those procedures. No verifying TC text was supplied and none was assumed.\n\nRUBRIC AND ITS REVISION. docs/rubrics/change-review-records.md, content digest SHA256 81a0de90c98ad2dac0b9774fd94c611181fc49bfde083cc22c52d1fb1ac31f8a. INTENT SOURCES, as supplied: SN-024 (independent critical eye against a written rubric, never the authoring session; human chooses the reviewer for attended acceptance), SN-037 (boundary-located promises; a reviewed change altering one side carries or justifies the counterpart), SN-012 (right-sized process; proportionality governs LLR/TC granularity); SR-184, SR-185, SR-186 (Drafted, Verification=Inspection), with SR-154, SR-162, SR-070, SR-168 and SR-170 read as the adjacent Approved homes, plus LLR-035/079/124/130 and IF-011/IF-164.\n\nRUBRIC-AGAINST-INTENT CHECK, performed before scoring. G1<-SR-184's identity/rubric/anchor duties incl. zero-finding coverage; G2<-SR-184's TC-copy failure clause and SN-024's \"not the possibly-lax TC\"; G3<-SR-185 and SN-037's final clause incl. \"resolving two IDs alone cannot establish agreement\"; G4<-SR-186/SN-012 incl. required-tier retention and the no-quota constraint; G5 derives from SR-186's \"delivered process shall require ... and record\" plus SN-012's abandonment rationale. Two permissiveness risks tested. (i) G1 defers unattended family heterogeneity to the approved routing contract: SN-024 as now worded itself scopes heterogeneity to the unattended path, and SR-154 (Approved, Verification=Test) carries family diversity, pre-launch selection logging, documented degradation, bounded rework and escalation — a stronger enforcer, not a silent drop. (ii) G3 could be read as satisfiable by naming any counterpart, but its own last clause forces an independent judgment of the reason, which I performed rather than accepting the citation. The rubric is not TC-derived (no TC text exists in the brief). I propose no new B# anchor: I found no failure mode outside B1-B5.\n\nANCHOR-BY-ANCHOR JUDGMENT (all five judged; coverage recorded because the verdict has zero findings).\n\nG1 - PASS. The critique prompt now carries the attended identity instruction the prior F2 found missing, in the same place as the coordinator one: \"In coordinator use ... in attended use, you are a human-chosen fresh reviewer who did not produce it\", and at recording time \"identify the human-chosen reviewer and sitting/review record supplied by the invocation ... include a provider session id only when the invocation supplies one, and never invent hidden metadata\". PROCESS_OPTIONS:1253-1263 states the same in doctrine. This review reconstructs from that: fresh non-author session, named rubric digest, named SN/SR intent sources, anchors judged.\n\nG2 - PASS. Unchanged and still adequate: the critique prompt orders the derivation check before scoring (\"check that the rubric independently covers the supplied SN/SR intent. A rubric copied from a permissive TC without that derivation is a finding; propose the missing numbered anchors instead of approving against it\"), which is the operative form of SR-184's \"a record whose rubric is copied from the verifying TC without independent derivation ... fails\". A populated provenance field alone would not have carried it.\n\nG3 - PASS; prior F1 cleared. The H3 paragraph now names the changed sides (LLR source pointers for the rendering implementation; IF-011's description completed for its already-public text-status mode) AND the requirement-side counterparts the prior review found absent: IF-011 -> LLR-035 -> SR-168 and SR-070, with the paired IF-164 -> LLR-198 -> SR-168. One explicit decision is recorded for them: descriptive-only, SR-168/SR-070 asserted behavior unchanged, counterparts retained. I judged that reason rather than resolving ids. It holds against the supplied cells: LLR-035 (Approved) already states \"its status block via --status\" and LLR-130 (Approved) already \"Implements stale/missing --check\", so IF-011's data cell (\"0 clean or vacuous / 1 invalid registry, stale HTML, or stale status snapshot under --check\") describes behavior two Approved rows already assert, and SR-070's AC (\"a committed copy that has drifted from its sources fails its freshness contract while a current one passes\") is the requirement it realizes. IF-164's retention reason (\"still names traj_status as the status writer\") verifies against its owner cell; LLR-124's \"trunk_step --regen runs gen_trajectory --status\" is a delegation, not a contradicting writer claim. I considered and rejected a MINOR for not enumerating LLR-130/LLR-079 as counterparts: neither module set is touched by the move, both hang off the named SR-070, and SN-037/SR-185 speak at the requirement/interface tier the record uses. Source-level truth of \"already-public\" is outside my scope by the brief and is separately reviewed; within the excerpts it is corroborated, not merely asserted.\n\nG4 - PASS; prior F3 cleared. The stopping decision is recorded in the existing scoped record with three distinct acceptance questions (SR-184 Critique record provenance, SR-185 counterpart agreement, SR-186 proportionate decomposition), three different SN parents, and per-TC purposes (TC-209 normal/missing-provenance/TC-copied-rubric; TC-210 semantic agreement vs valid references; TC-211 redundant child while preserving required tiers) that the parent sentences do not perform. The previously uncited premise is now cited and the citations verify against the supplied PROCESS.md: 482-487 carries \"Every SR -> >=1 LLR (or Analysis/Inspection/Attest); every SR and LLR -> >=1 TC\", and 737-744 carries \"only Analysis/Inspection/Attest SRs are LLR-exempt\" with \"Every SR needs >=1 TC row regardless of method\". The tier clause now reads with the \"required by that method\" qualifier PROCESS_OPTIONS (d2) and the spine-authoring skill use, so an inspector can check B4's omitted-tier class from the record. No row-count target, no deletion quota, no new gate. I tested one rubric-external concern and did not raise it: SR-184/SR-186 each carry a multi-clause shall, but single-shall discipline is not a rubric anchor, the rationales argue the clauses as one coherent decision, and Approved precedent (SR-154, SR-162) is materially more compound - raising it would relitigate an argued decision, not expose a defect.\n\nG5 - PASS; prior F2 and F4 cleared. F2: the critique template splits recording by path and adds the missing-route case verbatim - \"if no write/commit route is supplied, return this same verdict content through the invoking route for the launcher or human to record at the assigned path\" - closing with \"in attended use, follow the invoking route for its recording and stop\". I am the executing test of that instruction and found it followable as delivered; the capital W in \"In coordinator use, Write your verdict to {verdict}\" preserves the contiguous \"Write your verdict to (\\S+)\" substring the fake-CLI harness discriminates on, so the edit did not break the coordinator path to fix the attended one. F4: the reviewer template's counterpart/decomposition paragraph is now one unwrapped line matching that file's single-line convention; the two mid-phrase newlines the dispatcher note warns about are gone, and the note's DO-NOT-RE-WRAP rule is no longer self-contradicted. The critique template's wrapped body is that file's pre-existing convention and the edits match it. The wider chain remains followable and honest: PROCESS_OPTIONS 1253-1263, 2003-2007 and (d2) 124-129, the spine-authoring stopping-boundary rule, the reviewer prompt's counterpart clause and the planner Notes contract (\"a row count is not evidence of proportionality\") introduce no new schema, machine gate, row-count sensor or required LLR layer; missing evidence stays visible (procedures read \"Not executed; reviewer/date/result pending\", no passing inspection claimed, SR-162 re-attestation still owed, SR-175 consent/provider-inclusion work still open). SR-161's general machine perspective-record producer is referenced with the \"where that SR applies\" qualifier and is not claimed implemented; I did not treat that gap as passed and it is not load-bearing for the supplied stopping decision.\n\nSCOPE DISCIPLINE AND WHAT AN APPROVE MEANS HERE. I manufactured no ids and demanded no new schema, field, form or automaton. I judged the record's process, provenance and recorded decisions - not the adequacy of the produced implementation, not the truth of source-level behavior, and not the Drafted rows' approval, which remains a separate act by the tier authority. Zero findings means I tried each anchor against the corrected text and could not make one bite, not that no anchor was applied."
}


## Retained review subject excerpt

Recorded by the invoking session after the verdict. The H2/H3/H5 subject below
is copied from the actual review packet, before later execution-result summaries
were appended. Its SHA256 is `30ef63c80a936e08b4e04deaa9175f5e316028a013e9ab5eb375fc8c4febc474`.
The complete amendment document supplied to both Critique and Inspection had
SHA256 `dedff3e3672fa0178ec4a2c317beb02850a34327ecbc3de3d5212ee0a93e115d`.
This retained excerpt is review evidence, not a second normative process.

```text
## Implementation review subject (2026-09-06)

H2/H3/H5 now use the existing process and review carriers. PROCESS_OPTIONS
states the common Critique provenance, counterpart decision and proportionality
rules; the critique and reviewer prompts carry the actionable instructions.
The spine-authoring skill supplies the decomposition question, and the planner's
existing Notes record the stopping decision. No new schema, machine gate,
row-count sensor or required LLR layer is introduced.

For H3, P9R changes the LLR source pointers for the rendering implementation
and completes IF-011's description of its already-public text-status mode.
The requirement-side chain is IF-011 (`docs/requirements/interfaces.toml:318-324`)
→ LLR-035 (`docs/requirements/low-level-requirements.toml:378-387`) → SR-168
(`docs/requirements/system-requirements.toml:846-858`) and SR-070
(`docs/requirements/system-requirements.toml:370-388`); the paired
status surface is IF-164 (`docs/requirements/interfaces.toml:675-683`) →
LLR-198 (`docs/requirements/low-level-requirements.toml:1980-1989`) → SR-168.
The decision is descriptive-only: the SR-168/SR-070 asserted behavior remains
unchanged while the interface description records the existing status mode.
The command remains `gen_trajectory.py`, its HTML and status checks retain
exit 0/1, and IF-164 still names `traj_status` as the status writer. Retaining
those counterparts preserves the supported calling convention; moving the
private HTML implementation is not a reason to change a consumer's command.
The independent review must judge this semantic argument against the actual
source and interface cells; a successful reference lookup is insufficient.

For H5, the stopping decision is the three distinct acceptance questions:
SR-184 owns Critique record provenance, SR-185 owns counterpart agreement,
and SR-186 owns proportionate decomposition. TC-209 applies normal, missing
provenance and TC-copied rubric cases; TC-210 distinguishes semantic agreement
from valid references; TC-211 challenges a redundant child while preserving
required tiers. Those procedures supply verification the parent requirement
sentences do not perform. PROCESS.md requires every SR to have an LLR or a
method that is explicitly LLR-exempt, and every SR and LLR to have a TC
(`project-trajectory/PROCESS.md:482-487`); it states that only
Analysis/Inspection/Attest SRs are LLR-exempt while every SR still needs a TC
(`project-trajectory/PROCESS.md:737-744`). Because SR-186 selects
Verification=Inspection, its selected verification method permits this direct
SR→TC link while retaining every tier required by that method; another LLR
would duplicate these review judgments without defining a separate mechanism.
Further splitting is not justified by another label for the same question.
Existing mechanical evidence stays with SR-154/SR-162 and their
children. This is a scoped decision, not a quota for other projects.
```
