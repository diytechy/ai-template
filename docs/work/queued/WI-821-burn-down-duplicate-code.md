+++
id = "WI-821"
title = "Burn down the duplicate-code census: one home per shared stage, readers first"
workstream = "process"
specref = "docs/plans/2026-09-28-duplicated-stage-detection.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 at the owner's direction ("Related to
cleanup, you can file that / integrate that as you recommend"). WI-624's research
([plans/2026-09-28-duplicated-stage-detection.md](../../plans/2026-09-28-duplicated-stage-detection.md)
§7) and the standing census left duplicates "for the owner's burn-down decision";
WI-545 closed with them unfiled. This row is that burn-down, by the 0→A→B rule
(PROCESS.md §3): extract the shared stage once, never patch each copy.

The census (`check_dupes_census.py`, warn-only by the D-7 ruling, its baseline in
`docs/stack.ini [dupes-census]` downward-only and re-stamped by hand with a reason)
reads 5 groups / 5 copies / 52 lines against a stamped 0/0/0, on 2026-10-04:

- `agent_common.read_toml_text` and `kitlib/spine._toml_tables`: the same TOML read;
- `check_trajectory.read_rows` and `gen_release_checklist.load_csv`: the same CSV
  read;
- `frame_rules._entries` and `kitlib/spine.seam_endpoints`;
- `_is_docstring`, twice;
- `human_approves` and `human_approves_spine`, which the research judged deliberate
  (§7).

The research also names near-copies the census cannot see (a renamed constant or
one changed flag hides a copy from an exact-body census):

- two open-items readers sharing their load, skip and status-filter stages
  (`check_trajectory.approval_brief_findings`, `trace.ruled_open_item_texts`), the
  owner's A→B→C / A→B→D shape exactly;
- `plan_artifacts.parse_plan_wis`, the plan-table parser's F5-era copy;
- two `_clip`s;
- `trace.if_note_advisories`, a near-copy of `trace_text.cite_advisories`;
- `trunk_step`'s two argv builders, differing by one flag;
- `spec_move.rewrite_text` and `trunk_step.rebase_links`;
- the four small M0 copies.

**Not in this row:** the bar vocabulary's two tables (`intake.normalize_bar`,
`integrate._normalize_bar`) go to WI-817, which already retires their aliases. The
WI-788 dual-path census (D1 to D18) is WI-799, WI-816 and WI-817's.

**Sequencing.** It needs no row, and touches different code from the lane-lifecycle
program, except `trunk_step` (WI-800 adds the usage harvest there). If WI-800 is in
flight, take the two `trunk_step` items last, after a refresh.

## Done-when

- Each census group and each named near-copy above either has ONE home, every
  former copy calling it (readers first: TOML, CSV, open items), or is recorded as
  deliberate with its reason. The `human_approves` pair stays as the research
  judged it, unless the build finds otherwise and says why.
- `check_dupes_census.py --root .` reads 0/0/0, or the remaining deliberate groups
  only, and `docs/stack.ini [dupes-census]` is re-stamped down by hand with the
  before and after readings and the reason, per its own convention. The census
  stays warn-only (D-7).
- Behaviour is unchanged. Each merged stage has a test that pins the shared
  behaviour, and duplicated POLICY, if any is found, gets the behavioural pin
  `tests/test_rule_sync.py` exists for.
- The complexity ratchets do not rise (a merge that grows a module past its
  baseline is decomposed, not re-stamped up).
- Whether `check_dupes_census.py` ships to adopters (it is absent from the
  bootstrap `MAPPING`, flagged by the 2026-08-29 complexity-pushback review) is
  decided and recorded: either mapped with a RESYNC entry, or recorded as this
  repo's sensor only.
- The row's test bar: its affected modules' tests plus the smoke tier.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry only if a shipped module's interface changes or the census
  ships; otherwise none, with the reason.
