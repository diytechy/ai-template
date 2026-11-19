+++
id = "WI-1008"
title = "SR-033, SR-223 and SR-225 each state the premise their argument rests on, as an assumption or a waiver"
workstream = "requirements"
sr_refs = ["SR-033", "SR-223", "SR-225"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Filed by hand on 2026-11-18 at the operator's ruling (HANDOFF §11). The joint
requirements read of the same day (§12.6) set each of this repository's eight
joint requirements beside its siblings' arguments. Five are covered by a
sibling's assumption. Three are joint and cite no assumption, and no sibling's
argument covers their own part. Each rests on a premise outside the system that
no row states:

| Row | What it delivers | The premise no row states |
|---|---|---|
| SR-033 | the generated release checklist | the person releasing works through the checklist |
| SR-223 | the guardrails payload vendored for a model | a model follows the guardrails vendored for it |
| SR-225 | the delegated decisions record | a delegated run discloses its decisions truthfully, and the operator reads what is listed |

DA-003 covers the operator's own acceptances, not SR-225's reading. The
boundary gate's joint skip (`8a2e5c686`, SR-205 as amended) lets the three
rows pass, and it stays as built: no check can tell whether a sibling's
argument fits a joint row's part, so the argument has to be written down.

SR-225's second premise depends on where the listing of unseen decisions
lives, which WI-1009 moves off `docs/open-items.html`. Write that assumption
after WI-1009's scope critique has settled the listing's home, or word it so
it does not name the page.

## Done-when

- [ ] SR-033, SR-223 and SR-225 each cite an assumption in `da_refs` that
      states the premise in the table above, or carry a `coincident` waiver
      that argues why none is needed. Each new assumption row states where it
      takes effect, when it holds, its obstacle and a falsifier, and is
      `Drafted`.
- [ ] The three amended rows and any new assumption are listed on
      `docs/open-items.html` for the operator's acceptance act. Their text
      lands; the act is the operator's.
- [ ] `trace.py --strict` and `check_trajectory.py --strict` are clean.
