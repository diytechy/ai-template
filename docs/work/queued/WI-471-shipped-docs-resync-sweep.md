+++
id = "WI-471"
title = "Shipped-docs resync sweep — bring the kit's shipped method docs and entry surfaces up to the landed 2026-08 rulings, scoped EXACTLY to the 31 class-A findings of docs/plans/2026-08-17-shipped-docs-staleness-audit.md (two read-only subagent audits, log 2026-08-17i; no general doc-resync WI existed — WI-390/455/452 own only their named slices). The one real job is EXAMPLE.md (§1-§4 + §9 rewritten onto the TOML carrier with legal {Drafted,Approved,Modified} Status cells and an owner key on every IF row — four cells still read the illegal Status=Implemented); the rest is line-level: the PROCESS.md attended/single-ratify/autonomous enum paragraph rewritten to the 0-4 dial + --gate-policy presets (SN-029; the record already calls it rot), ~20 retired CSV/markdown-carrier and Stable/Draft/Verified tokens across the core pair and READMEs, three landed-but-undocumented mechanisms added to PROCESS.md (the hats registry replacing the §1 status.md-hats prose, the external.toml boundary frame at the DevStg-Boundary rung, the last_approved snapshot as the re-attest baseline — mechanism only, the first seed and UNANCHORED arming are sitting-pending), the RESYNC_PACK §3 hats/SN-tags entry a range-selected resync currently never learns of, the SN template's missing tags key (outside the dogfood census, so nothing catches it), README.md's live-dial contradiction (human_ratification_through documented 0, live 4), and the interfaces template stating the 2026-08-17c owner-points-at-design preference. HOLDS, stated so they are not ridden in quietly: every class-B item in the audit doc stays untouched (Modified retirement, chain-rule, IF direction columns, all architecture/check_flows prose, item-15/16/17 subjects); the SN-maturity wording fix RIDES item 6's execution; the edge-SN template sites (SN template kind=edge, EXAMPLE edge table, ADOPTING:188) are BLOCKED ON AN UNRULED KIT-LEVEL QUESTION the audit flags — whether the shipped template follows the instance's OI-18 dissolution — and move only on that ruling. Byte budgets guard the core pair (byte-budget-guard skill; PROCESS.md sized +0.5..1.5 KB, PROCESS_OPTIONS ~neutral); test_dogfood_sync must stay green, and where a fix is one line the adjacent self-stale non-kit surfaces (registry-machinery-reference §1 carrier prose, external.toml header's 5·6·3, the SN header's five-always-hats) may ride the same commit."
specref = "docs/plans/2026-08-17-shipped-docs-staleness-audit.md"
workstream = "docs"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed 2026-08-17 from the owner's question at the desk ("it seems none of
them have been updated for the newer processes, or is there a work item?").
The audit answered both halves: the docs are healthier than feared — the D-9
vocabulary, one-decision tiering, interface doctrine, derived gate and WI
spec-folder carrier all landed in the shipped surfaces, no surface
prematurely adopts an unruled state, AGENTS.template.md owes nothing outside
WI-455's bullets, and 22 of 23 kit skills are clean — and no work item owned
the remainder. This WI is that remainder, and nothing else: the audit doc's
class-A table is the closed finding list, its class-B list is the closed
hold list, and a finding already owned by WI-390 (concurrency prose), WI-455
(architecture prose), WI-452 (resync-helper surfaces), WI-448 or WI-469 is
theirs, not this row's.

### Method notes for the executing session

- Work finding-by-finding against the audit doc's tables; every edit cites
  its ruling (log id) in the session record, none in the shipped prose
  (shipped docs state the method, not this repo's history).
- Run `byte-budget-guard` before and after touching PROCESS.md /
  PROCESS_OPTIONS.md / AGENTS.template.md; run the full
  `test_dogfood_sync.py` after template edits; EXAMPLE.md's §4b Permutations
  snippets are pinned by `tests/test_gen_cases.py` — keep them parsing.
- EXAMPLE.md deserves a closing check: weigh a test pin on its carrier/Status
  teaching (the 3771c003 sweep missed its cells precisely because nothing
  pins them) and file the pin as a finding if not taken.
- The blocked edge-SN sites: if the kit-level ruling arrives mid-session,
  apply it; otherwise leave the sites verbatim and record the block in the
  session log.
