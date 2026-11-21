+++
id = "WI-1024"
title = "An LLR or SR names the interface it constrains, and every interface reaches an executable test through a requirement"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-211"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = ["WI-1023"]
buildtier = "strong"
safety_class = "ordinary"
supersedes = "WI-1015"
priority = 2
planmode = "single"
+++

## Context

Variant F's fourth row (F-4), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F point 3 and decision 2
(revisions 18 and 20: an interface states its form; the LLR or SR that
constrains it states the behaviour and its full dimensional scope), the
SR's optional `constrains` cell (revision 20), F-call 3's per-(TC, LLR)
pair rule with its repeat check in `trace.py --strict` (revision 35), and
F-call 8 (an LLR need not name an interface).

**WI-1015's item 6 lands here** (restructured into F, HANDOFF §3.3 N1).
WI-1015 counted 125 of 268 interface rows with no test case. Under F the
direct IF → TC citation is no longer owed: every interface must reach at
least one executable TC through an LLR or SR whose `constrains` names it,
or a TC whose `verifies` names it. OI-43's direct check (WI-488) and its
147-row allowlist (`docs/if-tc-coverage-allow`) stay until that relation is
populated, then retire; the allowlist measures a different relation, so it
is not the migration list (revision 20).

Today no LLR or SR carries `constrains`; 141 of 401 TCs name an interface in
`verifies`; the SR `permutations` cell is empty on all 138 SRs. The four
`external:`-owned rows need an LLR or SR constraining our reading of the far
side (decision 1).

**The dimensions cell.** An LLR that constrains an interface gains a
`dimensions` cell: the one home of that behaviour's closed input set, in the
`gen_cases` grammar of the SR `permutations` cell, with the out-of-domain
rule stated beside it (revision 20). The SR cell stays for system-boundary
dimensions only. A schema change adopters inherit.

**Placement.** An LLR is placed at the owner component of the interface it
constrains, or of the interface its verifying TC names; WI-1023 built the
second half. Blast radius from a changed interface: the LLRs and SRs that
constrain it or are observed at it, then the TCs verifying those.

**Needs:** WI-1023 (the requirement tiers declare their keys, and placement
is derived there). WI-1022 retired the internal `call` rows first, so no
retiring row is given a requirement.

**Population is this row's.** Each live interface gets its constraining
LLR or SR, proposed by the lane from today's evidence (the LLRs naming the
owner's file, the TCs naming the interface) and judged row by row. Adding a
`constrains` cell to an accepted row is a traced-cell change (OI-14) and
drifts for adjudication; a missing behaviour becomes a new `Drafted` LLR.
WI-1025 then moves contract-body prose into these LLRs.

## Scope answers

- **S1.** Deliverables, in order on one branch: (1) the two cells, the
  derived coverage check (warn-first) and placement; (2) population;
  (3) the check made strict and OI-43's direct check retired. Kept
  together: (3) cannot land before (2), and (1) alone adds a check that
  reports every interface.
- **S2.** No new authority: a trace finding over registries.
- **S3.** `constrains` admits live IF ids only; `dimensions` reuses the
  `gen_cases` grammar and refuses anything it does not parse.
- **S4.** `single`: schema, checks and a population over every interface.
- **S5.** Adds a requirement → interface relation and the behaviour's input
  space; names each LLR re-cut or minted in the Deliverable.
- **S6.** No new package, tool or service.

## Done-when

- [ ] LLR and SR rows accept an optional `constrains` cell (live IF ids)
      and LLR rows an optional `dimensions` cell in the `gen_cases`
      grammar with its out-of-domain rule; registry headers and templates
      state both.
- [ ] A derived check reports each interface that reaches no executable TC
      through a `constrains` link or a TC's `verifies`; one reached only
      through Inspection, Analysis or Attest evidence is reported as such.
- [ ] The per-pair repeat check: a TC naming an interface equal to the one
      every LLR it verifies constrains is a finding in `trace.py --strict`,
      not the commit hook.
- [ ] Every live interface is reached: each has a constraining LLR or SR
      (the four `external:` rows included), or the Deliverable names it as
      retired with its reason. New LLRs are `Drafted`; amended accepted
      rows keep their status, and the Deliverable lists every act owed.
- [ ] The coverage check fails `--strict`; OI-43's direct check and
      `docs/if-tc-coverage-allow` retire, with OI-43's record pointing
      here.
- [ ] Placement and blast radius read `constrains`; the views show it.
- [ ] A RESYNC entry (variant F, after WI-1023's) gives adopters the two
      cells and the coverage rule.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; tests
      are red-before for each finding class; every importer of a changed
      module runs green.
