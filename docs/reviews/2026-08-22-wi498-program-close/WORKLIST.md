# Consolidated worklist — the WI-498 program close

Sources: ROUND-SOL-RAW.md (1 CRITICAL / 9 MAJOR / 1 MINOR) and
ROUND-OPUS.md (0 CRITICAL / 7 MAJOR / 7 MINOR, mutation-verified).
Findings are CLAIMS: confirm each before fixing (both reviewers supplied
repro paths). Group-1 fixes are PROVEN against the reviews' own executed
attacks. One reviewer conflict is adjudicated at W-13.

## Group 1 — the trust-bearing fixes, first

- **W-1 (Sol 1, CRITICAL). A stale committed docs/stage survives a commit
  (working-tree check, index blind).** Fix within the ruled design: the
  freshness/staged story must make the COMMITTED bytes the thing the bar
  vouches for — stricten `staged-divergence` to FAIL (not warn) for the
  declared generated-artifact set when the artifact is modified-but-
  unstaged (or materialize the index for the derived-stage check). Read
  OI-31 first (this gap was recorded there pre-program) and record how
  the fix dispositions it. Prove with Sol's exact scenario: staged
  registry edit + unstaged regenerated docs/stage → the commit must
  REFUSE.
- **W-2 (Opus 1 = Sol 7). Both Release-unreachability pins are evadable
  (mutation-proven twice, two different mutants).** Replace the
  name-grep with a VALUE assertion plus an AST-level guard (no `Return`
  in `spine_stage` may resolve to the top rung — constant, alias,
  `STAGE_ORDER[-1]`, or helper); keep the 128-spine enumeration as the
  second arm. Both reviewers' mutants must now RED: drive each.
- **W-3 (Opus 2 = Sol 4). The blessed amendments include five FALSE
  prose cells, and the approval record mischaracterized them as
  mechanical.** Re-author LLR-142 (rationale), LLR-124 (detail), TC-050
  (expected), TC-141 (method), SR-140 (rationale) against what
  derive_stage/trunk_step actually do (no CLI on spine_rules, docs/gate
  deleted, REGEN_STEPS as shipped). Sanctioned: the DevStg-Needs dial +
  the owner's standing direction to fix; the re-seed rides the ordinary
  snapshot path with the drift brief REGENERATED honestly. Amend the
  slice-5 fragment record to state prose cells WERE rewritten (the
  restraint rule and the diff must stop disagreeing), and add the
  correction note beside the approval fragment's "mechanical" sentence.
  The owner is told plainly in the close report.

## Group 2 — MAJOR mechanical fixes

- **W-4 (Opus 3). The DECLARED_INPUTS ruling never reached the adopter
  recipe.** Rewrite RESYNC_PACK.md's §4 step-ordering paragraph (the
  dial is NOT a derivation input; the ordering rule loses its false
  justification) and correct tests/test_pre_commit_hook.py's `set_dial`
  docstring + its now-purposeless regen call.
- **W-5 (Sol 2). The shipped scaffold parks at DevStg-Boundary forever.**
  Treat placeholder-only frame registries as ABSENT in the derivation
  (consistent with the recorded "absence is an input value" design),
  regenerate the fingerprint semantics accordingly, fix the KICKOFF
  prose claim, and add the unmodified-bootstrap acceptance test Sol
  demanded (real scaffold, no file deletions, spine driven to
  all-Founded → reads Impl).
- **W-6 (Sol 3). A component-only multi-rung drop bypasses the phase
  rule.** Widen the rule's change detection to ALL stage-affecting
  inputs (CMP/BIF cells included); drive Sol's exact counterexample to a
  finding; keep the exemption the ruled pair.
- **W-7 (Sol 6). The dual-carrier fingerprint hole.** Fingerprint the
  carrier-presence vector (all suffixes, not first-hit) and refuse a
  dual-carrier state in input_paths the way spine_carrier refuses it;
  regression: TOML+CSV side-by-side moves the fingerprint and the reader
  re-derives (into the refusal).
- **W-8 (Opus 7). Nothing guards the INVERSE input defect.** Add the
  audit test: run load_spine under a read-trace (or poisoned temp tree)
  and assert every file actually read ⊆ input_paths(root) — the
  permanent-false-green direction closed.
- **W-9 (Sol 8 + Opus 4 + Opus 5). The stale-row census undercounts —
  rebuild it BY VALUE and re-scope WI-501.** Grep docs/gate, derive_gate,
  derived-gate, the 0-4 ordinal and retired CLI modes across ALL registry
  carriers (SN/SR/LLR/TC/IF/PB/CMP). Update WI-501's spec population
  (adds at least TC-051/142/170, SR-139 — the NORMATIVE ordinal cell —
  and any others the sweep finds; note SR-139 also feeds WI-499). Fix
  PB-004 NOW (re-measure on the current hook, the PB-002 precedent —
  Sol 10) and IF-081's contract cell (Drafted, traced — repair inline).
- **W-10 (Sol 5 = Opus 6). The reader-contract sentence overclaims.**
  Qualify the header + docstring: "no SELECTION or RATIFICATION consumer
  can read a stale stage", naming the display bypass; regenerate
  docs/stage.
- **W-11 (Sol 9). Non-reproducible signed totals.** Annotate the three
  unrevisioned slice totals per the established worker-self-report
  convention (label, never manufacture provenance); re-drive ONE full
  suite at HEAD as the close's own figure with a real rev; teach
  check_figures to refuse a `-dirty` rev on NEW fig: markers if cheap
  (else record as its follow-up).

## Group 3 — MINOR sweep

- **W-12 (Opus 8). Two disagreeing translations of the retired tags.**
  Route RETIRED_STAGE_ALIASES through the by-meaning threshold map
  (G2 → Impl-rung arrival) AND extend the legacy-flag warning to name
  the steps a bar-era value no longer selects.
- **W-13 (Sol 11 vs Opus suspicion — ADJUDICATED). The archive edits.**
  Opus diffed every touched archive file: the edits convert DANGLING
  links (their targets deleted with docs/gate) to inline code spans,
  words preserved — forced by the check_docs 0-broken bar. VERDICT:
  decline Sol's restore; record the adjudication in the close record
  with one spot-check re-verified. If the spot-check finds a hunk that
  changed WORDS, escalate to a fix.
- **W-14 (Opus 9/10/11). The deleted axis still taught on live
  surfaces:** traj_panels' two "gate bar" strings (+ regenerate the
  dashboard); PLAN.template/WI-000.template `--gate`/`<G>` →
  `--stage <rung>`; the check.py error message that routes to the
  warning flag.
- **W-15 (Opus 12). `Implements: SR-139` on phase_rule_findings is a
  mis-trace** — remove it; the phase rule's own row is minted by WI-501's
  re-scope or recorded as owed (do not leave the false edge).
- **W-16 (Opus 14). The staleness message states the wrong cause** —
  branch it (inputs-changed vs value-moved).
- **W-17 (Opus 13). The mutable dated ratify brief** — implement the
  CURRENT.md + immutable-dated-brief split if it is genuinely small;
  otherwise mint it as a queued quick WI with Opus's design as the spec.

## Out of scope, recorded

The queued rows (WI-494..502) and the five owner briefs (OI-55..59)
stay untouched except W-9's WI-501 re-scope; records/archives beyond
W-13's adjudication; the four Drafted CMP rows (the owner's separate
act); OWNER_SCRATCHPAD.md.
