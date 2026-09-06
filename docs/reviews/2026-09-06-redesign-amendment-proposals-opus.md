# redesign-amendment-proposals — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `200547f5356a6331d4b45b429c4dfccf1a4361521678ebc29b4d367f0a8cca84`

Tracked invocation: [session log](../iteration/call_7726398ca41a4efd9620ea9fcaf60b85-20260906-100244.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

**CHANGES_REQUESTED**

The packet is largely well-founded: H3 closes a residual `SR-162` names itself ("no SR states it yet"), H5 is precisely the skill's "package-wide property with no home" and correctly refuses a count cap, and the three new rows inherit parent priority. Seven concrete blockers.

**B1 — H4 tightens the mid-phase bar, contradicting the declared cadence it claims to reconcile.** Proposed: "the Full suite at work-item/slice or phase close." CLAUDE.md says a mid-phase WI/slice ends at the *commit* bar and the full unfiltered suite runs once at phase close; the 2026-09-05 close-bar ruling says the declared bar is the close bar. As written, every slice close now owes a ~10-minute suite. *Fix:* delete "work-item/slice or", leaving "the Full suite at phase close".

**B2 — H4 is not acceptance-only; it mints two unowned obligations.** (i) "that case is written failing-first" is a new normative ordering rule no SR carries, arriving in a cell titled a reconciliation. (ii) "a documented cadence exception is recorded rather than treated as a general waiver" is the unwired marker of §5 — no cell, no reader, no gate. *Fix:* drop both clauses from this amendment; if failing-first is wanted, file it as its own need-tier proposal.

**B3 — H1's `tags` change is not metadata-inert.** Hats fire on declared tags (§1a). Adding `legal`/`personal-data` changes SN-026's row in the `hats.py audit` SN × conditional-hat matrix, changes reach counts, and puts two newly-applicable lenses onto SN-026's decomposition — which SN-036/SR-161 require an applicability decision for. So "does not change selectors" is false as stated. *Fix:* replace that sentence, and add one line recording the applicability decision: both newly-reaching lenses are discharged by `SR-175`; no further SR is owed. Separately, `SR-175`'s rationale records that amending SN-026 was the *rejected* option (b), "one rule, one home" — say in one sentence that H1 records the lens (the DO-178C feed-back step, §2c(iii)) and does not move the rule, or a reader will read it as re-litigation.

**B4 — H2 leaves SN-024's attended-path promise unowned while claiming to cover it.** SR-154 applies only "When unattended work reaches integration"; H2's `shall` governs only the acceptance *record*. So "never by the session that authored the artifact" is stated by no SR for the attended path. *Fix:* add a NAMED RESIDUAL sentence to H2's rationale saying so (the pattern SR-162 already uses). Also, `LLR-048` already assembles rubric/intent/artifact under SR-154 — the mechanized half of H2's obligation sits under a different parent. *Fix:* one rationale sentence stating why brief-assembly stays SR-154's, or re-point LLR-048 to both.

**B5 — H3 states three verification methods for one row.** `verification = "Inspection"`, the AC says "reviewed **or attested**", and the prose asks for a "regression [that] should mutate one side's signal meaning". That is §4's verification-coherence smell pre-installed. *Fix:* scope the `shall` to the record, drop "or attested" from the AC (name the judgment as the reviewer's input, not a second method), and delete "regression" from the prose or say "inspection case".

**B6 — H5 implies a fourth record artifact.** Its AC requires "the review record states why", but names no home; three new non-automated Release TCs (H2/H3/H5) also stack manual gates. *Fix:* point H5's record at the decomposition record SR-161 already mandates rather than a new one (consolidate, 0→A→B). Also `process-options.md#proportionality-doctrine` is a wrong path — H4 uses `project-trajectory/PROCESS_OPTIONS.md`.

**B7 — All three rows rest on one unverified permission.** "PROCESS.md:482-487, :718-744" (Inspection SR may be LLR-exempt, TC still required) is load-bearing for H2/H3/H5; I could not verify it here. *Fix:* quote the clause at intake; if it does not hold, each row needs an LLR.

Unverifiable from the supplied set (not blockers, check at intake): `PRODUCT-FITNESS`/`PERFORMANCE` `listens_for` against §2(c2) for H2/H5, and every cited line range.
