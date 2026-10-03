# Sonnet cross-review — spine-acts batch N, round 2 (build/wi-766 at b84b6223)

Reviewer: Claude Sonnet 5.5 (read-only). Range `eb709653..b84b6223`, answering
[sonnet-batch-n-r1.md](sonnet-batch-n-r1.md).

b84b6223 NOT YET SOUND

Verdicts and addenda hold; r1's four MAJORs and its MINORs are closed in substance;
both specs parse (WI-767 closes cleanly with no Dispositions: `owes_successor` False).

**MAJOR**
1. TC-307 gets "No text change", so `staged_drafted_rows` never mints it into the
   first-approval adjudication and the carry-list omits it: it would stay Drafted.
2. The two adjudications the merge mints are unordered; a first-approval sitting
   run first is refused its LLR/TC registry copies while LLR-254, LLR-255 and the
   drifted TC rows are unattested.
3. LLR-255's sentence swap leaves the next sentence's "naming that command"
   ambiguous (the checklist names only the release command); its title is stale.
4. The gate-advance step has no anchoring LLR clause and no verifying TC, though
   it alone makes SR-215's "when a stage gate is checked" true at the gate.

**MINOR**: the new TC's "prints one warning" (the fixture has three rubric-less
cases); TC-247's naming assertion needs a fixture case with a `Rubric`; TC-248's
"both modules" is one module, and its release-trigger clause is covered only by
`test_trigger_waits_for_closed_work_floor`; the mirror-sync step is unnamed and the
RESYNC entry unanchored; a warn-only absolute-terms advisory moves to SR-215.

**Verified:** every replacement cell against the code at `30ee386b` (rejudge,
observation_cadence, intake `_cmd_rejudge`/`mint_rejudge`, gen_release_checklist);
`trace_text`/`absolute_terms` over an in-memory patched registry clear the SR-215
CRITIQUE-instrument finding with no new gating findings (advisories 307 before and
after); R2 holds; the new TC's Full tier matches `test_rejudge`'s slow placement;
the gate-advance insertion point is unique in the kit skill and both mirrors;
`verdict_refusal` None for both verdict files.
