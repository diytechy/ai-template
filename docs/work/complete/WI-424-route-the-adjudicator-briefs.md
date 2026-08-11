+++
id = "WI-424"
title = "Route each ADJUDICATE session to its own adjudicator brief - the four templates are authored, shipped, catalogued, and consumed by NOTHING. SN-032 moved the loop's prompts into files and authored four adjudicator briefs (adjudicate-amendment, adjudicate-disposition, adjudicate-conflict, adjudicate-red-tc); SN-026 gave adjudication rows their own routed phase, tier and cross-family rule. The seam between them was never built: agent_loop.route_session composes EVERY non-review session from the generic worker prompt, so an adjudication row routes to a strong cross-family model and then receives an implementer's instructions. The judge is briefed as a builder. TWO THINGS THIS ROW MUST DECIDE, and the second is why it was not done inside the program that found it. (1) THE DISCRIMINATOR: which of the four briefs a row wants is a typed fact, and the row does not currently carry it - the options are a new frontmatter key (honest, but a schema change across three F5-synced loaders), or derivation from the SpecRef cell (a spine CSV means amendment, a terminal spec means disposition, test-cases.csv means red TC), which costs nothing but infers rather than declares. Prefer the declared field unless the schema cost is real. (2) THE SLOTS: each brief demands assembled EVIDENCE - adjudicate-amendment wants {baseline} and {rows}, adjudicate-conflict wants {mechanical}, {open_rows}, {spine} and {digests}, adjudicate-disposition wants {report} and {evidence}. Those are real derivations (a baseline diff via trace._attested_baseline, the queue-conflict findings, a spine excerpt), and a half-filled brief is WORSE than the generic prompt: a judge's brief with hollow sections reads as though the evidence was looked for and found wanting. Fill every slot faithfully or leave the template unrouted. Done when: an adjudication row's session provably receives its own brief (fake-CLI prompts.txt capture, one test per template), the typed verdict line each brief demands is written to the declared path, and no slot is filled with a placeholder."
workstream = "scripts"
specref = "project-trajectory/prompts/README.md"
buildtier = "strong"
safety_class = "ordinary"
+++

## Context

Found by the FINAL adversarial review of the 2026-08-08 mechanized-loop program
(and independently by that program's own P4/P5 review agent), as MAJOR: *"all
four adjudicator templates are dead assets; every non-review session, including
`ADJUDICATE`, receives the generic worker template."* Verified — the four
`prompts.ADJUDICATE_*` constants have zero references outside `prompts.py`, and
`agent_loop.route_session` calls `worker_prompt` unconditionally on the
non-review branch.

**Why this was filed rather than fixed in that pass.** The program's own §8
scoped *authoring* the templates, and authoring is what shipped. Wiring them
needs the two decisions in the title, and the second one has teeth: the whole
point of these briefs is that **a judge's brief never contains the claim under
judgement** (the generalized WI-418 rule, `prompts/README.md`). A brief whose
`{evidence}` slot is filled with something thin does not fail loudly — it reads
as a completed investigation that found nothing, which is the most expensive
way for this machinery to be wrong.

Until this lands, the cost is bounded and visible: adjudication rows route to
the right MODEL at the right TIER with the right cross-family rule, and get an
implementer's prose. That is a worse brief, not a wrong verdict path — the
disposition's own `## Context` still carries the outcomes and the READ-IT-FIRST
instruction that intake derives.
