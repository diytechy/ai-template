+++
id = "WI-1024"
title = "An LLR or SR names the interface it constrains, and every interface reaches an executable test through a requirement"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-211"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = ["WI-1023"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
supersedes = "WI-1015"
+++

## Context

Variant F's fourth row (F-4), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F point 3 and decision 2
(revisions 18 and 20: an interface states its form; the LLR or SR that
constrains it states the behaviour and its full dimensional scope), the
SR's optional `constrains` cell (revision 20), F-call 3's per-(TC, LLR)
pair rule with its repeat check in `trace.py --strict` (revisions 18 and
35), and F-call 8 (an LLR need not name an interface).

**WI-1015's item 6 lands here** (restructured into F, HANDOFF §3.3 N1).
WI-1015 counted 125 of 268 interface rows with no test case. Under F the
direct IF → TC citation is no longer owed: every interface must reach at
least one executable TC through an LLR or SR whose `constrains` names it,
or a TC whose `verifies` names it. OI-43's direct check (WI-488, tagged
LLR-042) and its 147-row allowlist (`docs/if-tc-coverage-allow`) stay until
that relation is populated, then retire; the allowlist measures a different
relation, so it is not the migration list (revision 20).

Today no LLR or SR carries `constrains`; 141 of 401 TCs name an interface in
`verifies`; the SR `permutations` cell is empty on all 138 SRs. The four
`external:`-owned rows need an LLR or SR constraining our reading of the far
side (decision 1).

**The dimensions cell.** An LLR that constrains an interface states that
behaviour's closed input set in a `dimensions` cell, in the `gen_cases`
grammar of the SR `permutations` cell, with its out-of-domain rule beside
it (revision 20). The SR cell stays for system-boundary dimensions only. A
schema change adopters inherit.

**Placement and blast radius.** An LLR is placed at the owner component of
each interface it constrains, or of the interface its verifying TC names
(WI-1023 built the second half). An SR is not placed. Blast radius from a
changed interface: the LLRs and SRs that constrain it or are observed at
it, then the TCs verifying those. The build brief's component context is
WI-1029's.

**Population is this row's.** Each live interface gets its constraining
LLR or SR, proposed by the lane from today's evidence (the LLRs naming the
owner's file, the TCs naming the interface) and judged row by row. A
missing behaviour becomes a new `Drafted` LLR. WI-1025 then moves
contract-body prose into these LLRs.

## Scope answers

- **S1.** Deliverables, in order on one branch: (1) the cells, the derived
  coverage check (warn-first) and placement; (2) population; (3) the check
  made strict and OI-43's direct check retired. Kept together: (3) cannot
  land before (2), and (1) alone adds a check that reports every interface.
- **S2.** No new authority: a trace finding over registries.
- **S3.** The cells' grammar is closed (Done-when 1); anything else is a
  finding.
- **S4.** `single`: schema, checks and a population over every interface.
- **S5.** Adds a requirement → interface relation and the behaviour's input
  space. Re-cut LLRs (text only, drifting): LLR-042 (OI-43's direct
  coverage slice), LLR-199 (placement in the component view), and the
  placement LLR WI-1023 writes; every LLR given `constrains` and
  `dimensions` is a traced-cell amendment, listed in the Deliverable.
- **S6.** `needs` WI-1023: the requirement tiers declare their keys there,
  and LLR placement is derived there. WI-1022 (transitive) retired the
  internal `call` rows first, so no retiring row is given a requirement. No
  new package, tool or service.

## Done-when

- [ ] **The cells.** LLR and SR rows accept an optional `constrains` cell:
      a list of one or more live `IF-NNN` ids, written like `sr_refs`. An
      LLR carrying `constrains` must carry `dimensions` (one string in the
      `gen_cases` grammar, which refuses what it does not parse) and
      `out_of_domain` (one sentence: what the interface does with an input
      outside the dimensions, either refused at the boundary or a declared
      state its form names); both are absent on an LLR without
      `constrains`. A dead id, an empty list, or a missing or unparsable
      companion cell is a finding. Registry headers and templates state
      the three cells.
- [ ] A derived check reports each interface that reaches no executable TC
      through an LLR's or SR's `constrains` or a TC's `verifies`; one
      reached only through Inspection, Analysis or Attest evidence is
      reported as such.
- [ ] **The repeat check, per pair.** For a TC naming an interface in
      `verifies`, the name is redundant for a verified LLR or SR when that
      row's `constrains` includes the interface. The check is a finding in
      `trace.py --strict` (not the commit hook) only when the name is
      redundant for every LLR and SR the TC verifies.
- [ ] Every live interface is reached: each has a constraining LLR or SR
      (the four `external:` rows included), or the Deliverable names it as
      retired with its reason. Every LLR given `constrains` carries its
      `dimensions` and `out_of_domain`. New LLRs are `Drafted`; amended
      accepted rows keep their status and show as drift, which does not
      fail `--strict`. The Deliverable lists every act owed for automated
      adjudication; the lane holds for none.
- [ ] The coverage check fails `--strict`; OI-43's direct check and
      `docs/if-tc-coverage-allow` retire, with OI-43's record pointing
      here.
- [ ] LLR placement, blast radius (from LLR and SR `constrains`), the
      component views (`gen_components`) and the dashboard's architecture
      view read `constrains`; interface coverage counts LLR and SR
      `constrains` alike.
- [ ] A RESYNC entry (variant F, after WI-1023's) gives adopters the three
      cells and the coverage rule.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; tests
      are red-before for each finding class and for the per-pair rule's
      mixed case (one verified LLR constrains the named interface, another
      does not); every importer of a changed module runs green.
