# WI-853 dispute sitting at 695f7bc

## dispute

### SR155

**Scope bound.** PROCESS.md §6's review threat model bounds this sitting to a
normal working environment: the content agents write into the repository,
supported configurations, and regressions of supported behaviour. This finding
concerns registry content this lane authored and needs no compromised or
contrived host, so it is in scope.

**What I observed at 49d5a9a6.**

- SR-155 (`docs/requirements/system-requirements.toml`, `[requirement.SR-155]`)
  is about work *declared as contested planning*. Its requirement and acceptance
  cover a bounded round of two rival plans, cross-critique, coverage comparison,
  arbitration and a SELECT/PAGE outcome. Its rationale says the row is one
  capability with one outcome class. It says nothing about a review round's
  findings, a rework plan, or holding a fix until that plan covers the
  findings.
- The lane ships that obligation in two places:
  - In the skill: `project-trajectory/skills/session-protocol/SKILL.md` §2,
    "dispatch the fix only on exit 0".
  - In LLR-069's new Detail, which is now the traced product behaviour:
    - a review verdict's finding lines become ordered F1..Fn;
    - mixing the declared and verdict forms is malformed;
    - an `F#` exclusion that cites a dispute verdict resolves only on an
      accepted DISMISS (`plan_coverage.finding_clauses`, `ruling_problem`).

  The new TC-069 Expected tests the same behaviour. LLR-069 and TC-069 still
  cite SR-155 alone.
- I looked for another approved SR that states this obligation and found none:
  - SR-154 covers routing reviewers and bounding the rework loop's budget.
  - SR-234 covers composing an adjudication and accepting its verdict, and
    says an accepted dispute verdict authorizes no approval act.
  - SR-235 covers recording an attended review verdict.

  None of them says a rework fix waits until its plan covers every finding, or
  that a coverage gate treats only a DISMISS ruling as resolving a finding.
- PROCESS.md §5's problem-routing chart covers this case: when no row speaks to
  the obligation, it is a **requirement gap**, routed as a new or changed
  SN → SR → LLR, walked through that slice's Reqs/Tests bar.

**Weighing the positions.** The spec's Done-when names "SR-155's chain" as the
rows to amend. That choice was made by hand when the item was filed. It is
evidence of intent, not an approval of parentage. The in-lane amendment sitting
(001) judged LLR-069 and TC-069 MEANING and blessed their text. Its question was
whether the text changed meaning, not whether the parent was right, so it does
not settle this finding. One thing cuts the other way: LLR-069's single-item
and `F#` findings mode already sat under SR-155 before this lane (WI-803). That
earlier stretch does not cure the gap. This lane gives the mode a new purpose,
gating rework dispatch, and a new resolution rule tied to dispute verdicts. The
re-attestation in act 77 records that approved text as blessed while no
approved SR states the obligation it serves. The reviewer and the coordinator
agree on the substance, and so do I.

**Why FIX and not ESCALATE.** Under §6's triage this is not high-risk: no
security, data-loss, crash-safety, money or irreversible step is at stake. The
fix is small: one parent obligation, re-cited by LLR-069 and TC-069. The new or
amended SR is approved by its own tier's authority under the declared dial, so
the owner's signature is not bypassed whichever route the lane takes. A
DISMISS would leave approved, re-attested text tracing to a parent that does
not state it. That is the failure the spine exists to prevent, and it costs
more than the fix.

**On the route (advisory; the lane chooses).** A new Drafted SR fits better
than amending SR-155. SR-155's rationale argues it is one capability with one
SELECT/PAGE outcome class, and widening it to cover ordinary reworked work
would break that claim. The new SR should state the whole findings-coverage
obligation, including the mode that predates this lane, so LLR-069's findings
half has one parent. LLR-069 and TC-069 then cite it alongside SR-155 and go
through the lane's next combined sitting.

RULING: SR155 FIX The obligation this lane ships has no parent SR: a rework fix is dispatched only after the plan covers every review finding as an F# clause, and only an accepted DISMISS resolves one. SR-155 covers contested-planning rounds only, so per PROCESS.md §5's requirement-gap route the lane must author that parent (preferably a new Drafted SR) and have LLR-069 and TC-069 cite it.
