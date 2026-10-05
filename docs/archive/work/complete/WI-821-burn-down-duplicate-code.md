+++
id = "WI-821"
title = "Burn down duplicate code (one home per shared stage) and make the consolidation census section-aware"
workstream = "process"
specref = ""
sr_refs = ["SR-220"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

One home per shared stage, by the 0→A→B rule: the TOML read (`kitlib.config.read_toml_text`), the plan-table walk (`kitlib.registry.plan_table_rows`), the list-cell split (`kitlib.spine.seam_endpoints`), the leading-docstring test (`ast.get_docstring`), the open-items status filter (`kitlib.spine.open_items_at`, which keeps duplicate rows in carrier order), the citation-advisory sweep (`trace_text.cite_advisories`, the IF advisory keeping its own sentence), and the fragment link rebase through `spec_move`. Behaviour and every finding's wording are unchanged. The census falls from 5/5/52 to 2/2/32: the deliberate `human_approves` pair and the CSV-reader pair deferred to WI-817, stamped as the baseline (D-001, which the independent adjudicator ACCEPTED in `docs/reviews/wi-821-dupe-burn-down/dispute-1-ruling.md`). The consolidation census's commissioning signal reads specrefs as specs of record (`kitlib.registry.shared_spec`), so two sections of one plan no longer pair. Rows: LLR-210 detail and TC-314 method amended, ruled MEANING and re-attested in the lane (act seq 35; verdicts 001, returned, and 002); traced `code_symbol` and `evidence` cells follow the moves on eight LLR and eleven TC rows. Codex 6.1 Sol: two rounds (two MAJORs and a MINOR in round 1, one fixed, one to the adjudicator). Decisions: `docs/decisions/wi-821.toml`.

## Context

Filed by hand by the coordinator on 2026-10-04 at the owner's direction ("Related to
cleanup, you can file that / integrate that as you recommend"). WI-624's research
([plans/2026-09-28-duplicated-stage-detection.md](../../../plans/2026-09-28-duplicated-stage-detection.md)
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

**The consolidation census's commissioning signal is anchor-blind** (owner,
2026-10-04: "Yes please add it to WI-821's"). `consolidate._commissioning_docs`
strips the anchor from a row's specref, so every row cut from one plan counts as
"commissioned by the same document", even when each names its own section. Run
read-only on 2026-10-04, the census clustered all twenty-two lane-lifecycle rows
(WI-797 to WI-818) on that signal alone, and a real census run would mint one
`consolidate` judgement over an owner-approved split. `check_trajectory`'s
shared-spec rule already treats sections as specs (`kitlib.registry.shared_spec`:
two anchors in one file are two specs; no anchor covers the whole file). The
commissioning signal should read specrefs the same way. The module-overlap signal
is out of scope: it is real, and the graph orders those rows.

**The CSV-read pair waits on WI-817.** `check_trajectory.read_rows` and
`gen_release_checklist.load_csv` read CSV; WI-817 retires the non-TOML carriers
(D6), which may remove one or both readers outright. Take that group after WI-817,
or drop it if WI-817 removes it, rather than merging code about to be deleted.

**Not in this row:** the bar vocabulary's two tables (`intake.normalize_bar`,
`integrate._normalize_bar`) go to WI-817, which already retires their aliases. The
WI-788 dual-path census (D1 to D18) is WI-799, WI-816 and WI-817's.

**Sequencing.** It needs no row, and touches different code from the lane-lifecycle
program, except `trunk_step` (WI-800 adds the usage harvest there). If WI-800 is in
flight, take the two `trunk_step` items last, after a refresh. The census fix lands
before WI-810 folds consolidation into the mint step (WI-810 needs this row), so
WI-810 rebuilds on the section-aware rule.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

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
- The consolidation census's commissioning signal compares specrefs as
  `kitlib.registry.shared_spec` does (sections are specs; an anchor-less specref
  covers the whole file), one rule rather than a second reading beside it. Tested:
  rows naming two sections of one plan do not pair on it; rows naming the same
  section, or one naming the whole file, still do; the open-item edge is
  unchanged. LLR-210's "commissioned by one plan document" is amended to match and
  passes adjudication of that row, on whichever adjudication path is the one path
  when this row lands. Re-run read-only on the queue, the census no longer
  clusters the lane-lifecycle rows on that signal.
- Whether `check_dupes_census.py` ships to adopters (it is absent from the
  bootstrap `MAPPING`, flagged by the 2026-08-29 complexity-pushback review) is
  decided and recorded: either mapped with a RESYNC entry, or recorded as this
  repo's sensor only.
- The row's test bar: its affected modules' tests plus the smoke tier.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry only if a shipped module's interface changes or the census
  ships; otherwise none, with the reason.
