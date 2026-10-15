# Row M: phase-0 baseline manifest (review-churn program)

Read-only analysis. Snapshot: trunk `45d867e51` (branch `refactor_again`), lane
`wi-798` at `9437d0a1f`, lane `wi-902` at `d3d301216`. Nothing in any
repository or worktree was written; every file named below lives in this
directory (`M/`).

- `baseline-files.csv`: one row per review file (65 in the chosen cohort, plus
  6 pre-convention rounds kept as an alternate cohort and 1 duplicate, each
  flagged in the `cohort` column).
- `baseline-findings.csv`: one row per finding (74 in the chosen cohort, plus 5
  alternate and 1 duplicate).
- Scripts, in re-run order (Python 3.11, stdlib, git read-only):
  `enumerate.py` (selection, VERDICT parse, finding lines) -> `disputes.py`
  (dispute and sitting records) -> `regress.py` (git blame of each finding's
  cited line at its reviewed sha) -> `redtip2.py` (the lane's own test report
  nearest each reviewed sha) -> `build.py` (joins `classify.py`, the
  hand-judged table, and writes both CSVs) -> `stats.py` (every count below).
  `queue.py` computes the queue measure. Files starting `_` are intermediates.

## 1. Selection rule

**A review round is one `NNN-REVIEW-A-<sha7>[-narrow].md` or
`NNN-REVIEW-B-<sha7>[-narrow].md` file. The cohort is every such file added
under `docs/reviews/` by a trunk commit (history of `45d867e51`, linear: no
merge commits in the window) whose commit date falls in 2026-10-09T00:00:00
to 2026-10-11T23:59:59 -0500, plus every such file added on lane `wi-798` or
`wi-902` after its merge-base with trunk.** Every trunk commit that adds a
review file in the window is a lane's squash landing ("squash of wi-NNN"), so
"added on trunk in the window" means "its WI landed in the window". A
REVIEW-A and a REVIEW-B at one NNN would make one round; the window has no REVIEW-B file (none exists anywhere in the
repository), so rounds = REVIEW-A files here. `ADJUDICATE`, `DISPUTE`, `PLAN`,
`SPINE-CHANGES`, `REJUDGE` and `rollup/` files are not review rounds.

Reproduction (Git Bash, `MSYS_NO_PATHCONV=1`, from the repository root). The
scripts beside this file write their intermediate `_*` files next to
themselves, so copy this folder to a scratch directory and run each copy from
the repository root, in the order section 1 gives:

```sh
RE='/[0-9]{3}-REVIEW-[AB]-[0-9a-f]{7}(-narrow)?\.md$'
git log 45d867e51 --diff-filter=A --name-only --format= \
  --since=2026-10-09T00:00:00-05:00 --until=2026-10-11T23:59:59-05:00 \
  -- docs/reviews/ | grep -E "$RE"                               # 53 files
for b in wi-798 wi-902; do
  git log --diff-filter=A --name-only --format= \
    "$(git merge-base 45d867e51 $b)..$b" -- docs/reviews/ | grep -E "$RE"
done                                                             # 3 + 9 files
# findings: sum the findings=<n> of each file's one VERDICT line (git show <ref>:<path>)  -> 74
```

Timezone and edges: dates are the commit's own `-0500`. `--since/--until`
read the committer date, which equals the author date for every trunk commit
in the range (lane `wi-902` was rebased: its author dates run 06:58 to 11:58,
committer dates 09:59 to 11:59, all on 2026-10-11). The rule is insensitive to
its edges: no `NNN-REVIEW-*` file landed on trunk between 2026-09-06T00:48
and the first in-window one (WI-848, 2026-10-09T08:56:48), and none after
WI-858's landing (2026-10-11T07:50:10). Any start in that gap and any end at
or after 07:50:10 on 10-11, in any timezone, gives the same 65 files.

**Judgement call: REVIEW-A naming only, not the pre-convention files.** Five
lanes that landed early on 2026-10-09 filed their Codex reviews as
`sol-review-full*.md` (a first line `<sha> SOUND|NOT YET SOUND`, finding
bullets under `## MAJOR`/`## MINOR`, no `VERDICT:` line). I left them out of
the chosen cohort because (a) the measures will be re-run on files the merge
gate and rollup read, and since WI-870 the strict VERDICT reader reads these as
no verdict; (b) the rule is then insensitive to its window edges (above); (c) WI-848's
legacy file is a byte-identical copy of its `001-REVIEW-A-993deee.md`. Their
counts sit beside every measure in section 4 as "base 1".

## 2. Reconciling the two bases

| | WIs | rounds | findings |
|---|---|---|---|
| base 2 (reviewer's added-file window + 2 lanes) | 19 | 65 | 74 |
| this rule (section 1) | **19** | **65** | **74** |
| base 1 (earlier unreproduced pass) | 21 | 69 | 79 |
| + WI-853's two legacy rounds (4 findings) + WI-870's two (1 finding) | **21** | **69** | **79** |
| all 6 non-duplicate legacy rounds (adds WI-869, WI-875: SOUND, 0 findings) | 23 | 71 | 79 |

Base 2 is reproduced exactly by section 1's rule; the plain-git commands give
65 VERDICT lines summing to 74.

Base 1 is reproduced exactly by base 2 plus the pre-convention rounds of
WI-853 (`sol-review-full-r1.md` 3 findings, `sol-review-full.md` 1) and WI-870
(`sol-review-full-r1.md` 1, `sol-review-full.md` 0). The extra rule that
yields exactly that set: *count `sol-review-*.md` reviews too, de-duplicated
by reviewed sha, for lanes claimed after the overnight handoff `f27c66fbc`
(2026-10-09T01:05 -0500)*. Equivalently: move the trunk window's start to
after WI-875's landing (01:01:57). That drops WI-869 (claimed 2026-10-08T23:43,
landed 00:23) and WI-875 (an attended consolidation sitting, landed 01:01),
each one SOUND round with 0 findings. Two other sets also total 21/69/79
(WI-853 + WI-869 + WI-848's duplicate, or WI-853 + WI-875 + the duplicate),
but only by counting the same WI-848 review twice. So I judge base 1 to be the
WI-853/WI-870 version, with a start cut that no stated rule names.

## 3. Definitions as applied

**Classes.** Each finding gets one primary class, the first that applies in
this order, plus every other class that applies as a secondary tag.

- `instrument`: the finding's actionable defect is fully decidable by a
  mechanical rule over the repository at the reviewed sha. Either a declared
  check reports it (named per row), or it is a missing presence/format check
  of the plan's example kind (RESYNC_PACK entry present). When only part of a
  finding is mechanical (stale row text whose CodeSymbol also names a deleted
  symbol), the semantic part decides the primary and `instrument` is a
  secondary tag. I checked the candidates against the code:
  `trace.py` `IF_DATA_MAX = 160` form finding (advisory, trace.py:701);
  `trace.py --strict` singular-requirement gate (dispute 887/008 DB);
  `check_trajectory` connectivity-undeclared warning (commit 016acbd10).
  Things no current check catches: per-token CodeSymbol misses
  (`check_doc_refs` counts them untraced, never a finding), deleted test nodes
  (its `::node` selector is ruled prose), and IF direction per channel
  (trace.py only checks both/neither).
- `open-input`: the triggering input is one more member of a space the spec
  states only by a general rule or not at all: shell grammar forms, malformed
  record/config shapes, credential sources, workstation and platform variants
  (Windows aliasing, cmd lookup, an old Python first on PATH, no Git), git
  history edges (shallow clone), file shapes (undecodable bytes, truncated
  fence). This is not the class when the spec closed the rule exactly and the
  code deviates (WI-884 F1), when the gap is an unimplemented arm on an
  enumerated platform (WI-834 032), or when the case is output, not input
  (WI-834 035 F1).
- `history-rederive`: the code re-derives a fact (consumed, accepted, minted,
  landed) by replaying history or a log (git history, replayed dispositions,
  replayed store markers) instead of reading a record written at the event.
- `spine-text`: requirement-row, Done-when or spec wording, a row/code drift,
  or a wrong or missing trace link.
- `regression`: the finding's cited site, or the code the finding names as
  new, was last changed by an earlier fix round in the same lane. A fix round
  is a rework commit answering a review finding, a dispute ruling or a sitting
  return; the initial build and the spine intent pass are not. Blame evidence
  is in the `site_last_changed_by` column. `regression_basis` records
  `strict` (the fix introduced a failure the earlier code did not have,
  often shown by a tip/base comparison: 14) or `operational` (the fix's own
  new code left the class it was fixing open: 11). Spine text that only lags a
  later code change is not tagged.
- `defect`: any other genuine (or claimed) defect in the change. `process`:
  about the lane procedure, not the change.

**Late.** A finding is late when its file is the lane's review round 2 or
later, ordering the lane's review files by NNN (column `review_ordinal`). A
lane whose first review was narrow (WI-881) starts there. Second count: a
finding in a full-scope review whose immediately preceding review round in
the lane was a narrow APPROVE (column `full_after_narrow_approve`).

**Checkpoint.** A full review reopens a lane after a checkpoint when it has
≥1 BLOCKER/MAJOR finding and either its previous review round was a narrow
APPROVE, or a spine sitting lies between the previous review round (or the
lane start) and it. A spine sitting is an `ADJUDICATE` file with no `RULING:`
line and no "dispute" title; the sittings found are listed in
`after_spine_sitting`.

**Disposition** sources, in order: the dispute ruling (`RULING: <id> FIX|DISMISS`
gives `disputed-FIX`/`disputed-DISMISS`), the lane's decisions record, the
coverage plan (`Excludes:` lines) and the fix commit's message. `escalated` =
the owner ruled the remedy. Each row's `evidence` column cites path:line or
commit. No row is `dismissed` or `unknown`. WI-902 015 F1 is `accepted` per
D-010 but unfixed at the snapshot.

**Red tip.** `red` means the review file or a lane commit message says the
reviewed tree failed its test bar. `green` means a lane commit message reports
the smoke or verification run passing on the reviewed tree, with only
non-code commits (telemetry, filings, sittings, acts) between it and the
reviewed sha. `budget-over` means the results were green but the commit says
the 60 s seconds clause read over (under machine load). `unknown` means
neither. Reviewers' own failures are all attributed by them to their sandbox
(Git sh `CreateFileMapping`, Win32 error 5) or, once (WI-881 006), to the base
commit. Neither counts as red. Column `reviewer_tests` records them.

## 4. Counts (chosen cohort; base 1 in brackets where it differs)

Computed by `stats.py` from the CSVs.

**Cohort.** 65 rounds (38 full, 27 narrow; 36 CHANGES-REQUESTED, 29 APPROVE,
one of them carrying a MINOR), 19 WIs (17 landed in the window, 2 in flight),
74 findings (46 MAJOR, 28 MINOR, 0 BLOCKER). [69 rounds, 21 WIs, 79 findings]

**Primary class** (count; as primary-or-secondary in brackets):

| class | primary | of which late | primary or secondary |
|---|---|---|---|
| instrument | 4 | 2 | 8 |
| open-input | 26 | 19 | 26 |
| history-rederive | 5 | 3 | 7 |
| spine-text | 21 | 9 | 22 |
| regression | 6 | 5 | 25 |
| defect | 11 | 4 | 11 |
| process | 1 | 0 | 1 |
| **total** | **74** | **42** | |

Base 1 adds: defect +3, spine-text +1, open-input +1 (late), giving 27
open-input, 22 spine-text, 14 defect, 43 late, 26 regressions (15 strict).

By WI (primary class; late in the last column):

| WI | instr | open | hist | spine | regr | defect | proc | total | late |
|---|---|---|---|---|---|---|---|---|---|
| WI-798 (in flight) | 0 | 5 | 0 | 5 | 0 | 0 | 0 | 10 | 1 |
| WI-823 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| WI-834 | 0 | 12 | 0 | 5 | 3 | 4 | 0 | 24 | 19 |
| WI-848 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| WI-858 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| WI-880 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 3 | 0 |
| WI-881 | 0 | 0 | 0 | 1 | 2 | 1 | 0 | 4 | 3 |
| WI-882 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| WI-884 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 2 | 0 |
| WI-887 | 1 | 5 | 0 | 3 | 1 | 3 | 0 | 13 | 9 |
| WI-892 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| WI-902 (in flight) | 1 | 3 | 4 | 4 | 0 | 1 | 0 | 13 | 10 |

**Dispositions.** Accepted 58, disputed-FIX 10, disputed-DISMISS 5, escalated
1, dismissed 0, unknown 0. By class: open-input 16 accepted, 7 disputed-FIX,
2 disputed-DISMISS, 1 escalated; spine-text 21 accepted; instrument 2
accepted, 1 FIX, 1 DISMISS (refuted); history-rederive 3 accepted, 2 FIX.
[base 1: accepted 61, FIX 11, DISMISS 6]

**Measures.**

| measure | baseline | how computed |
|---|---|---|
| Review rounds per landed WI | mean **3.12**, median 1 over 17 WIs (53 rounds); distribution 1:9, 2:3, 3:2, 6:2, 20:1 WIs. In flight: WI-798 3, WI-902 9. [19 WIs: mean 3.00, median 2] | count of cohort files per WI, split by `wi_status` |
| WIs needing ≥ 6 review rounds | **4**: WI-834 (20), WI-881 (6), WI-887 (6) landed; WI-902 (9) in flight | same |
| Late findings | **42 of 74** (28 MAJOR) [43 of 79] | `late = yes` |
| Late findings from open input spaces | **19** (15 from landed WIs = **0.88 per landed WI**; 4 in flight). By WI: WI-834 11, WI-887 4, WI-902 3, WI-798 1. [20; 0.84] | `late = yes` and `primary_class = open-input` (no row carries open-input as a secondary tag) |
| Findings in a full review right after a narrow APPROVE | **20** (10 MAJOR) in 10 reviews: WI-834 9, WI-887 6, WI-902 3, WI-881 2. If any earlier narrow APPROVE in the lane counts: 23 | `full_after_narrow_approve = yes` |
| Review findings an instrument would catch | **4** primary: 3 by an existing check (WI-882 F1 form finding, WI-887 007 F6 singular gate, WI-902 014 F1 connectivity warning) + 1 by a missing presence check (WI-823 F1 RESYNC entry, refuted). 3 of the 4 were valid. Partially mechanical (secondary tag only): 4 more | `primary_class = instrument` |
| Full reviews reopening a lane after a checkpoint | **10** full reviews with MAJOR findings: 7 right after a narrow APPROVE (WI-834 012/016/024/028, WI-881 006, WI-887 007, WI-902 008), 3 after a spine sitting only (WI-834 009, WI-880 004, WI-887 010). They carry 22 findings (14 MAJOR; 10 open-input, 7 spine-text). [13: + WI-853 ×2, WI-870 r1, all after a spine sitting] | `full_reopen_after_checkpoint = yes` |
| Review rounds started on a red tip | **1 red** (WI-834 001: commit 73ad57436 says IF-292's channel "reddened the smoke tier since ec95154b", an ancestor of the reviewed sha), **2 budget-over** (WI-834 034n and 035: results green, seconds clause over under load), 42 green, **20 unknown** (16 of them WI-834's, a rebased lane whose round commits carry no test report) | `tip_state` |
| Net queue per week | Over the 3-day window: 16 rows filed + 20 successors minted − 36 closed into `docs/archive/work/` = **0** (0/week). Every minted successor also closed in the window (15 as "already settled"). Counting the 6 closes into `docs/work/{complete,partial}/` too: −6 (−14/week) | `queue.py` (command in its docstring): `A` under `docs/work/{queued,draft}/` (`mint:` subject = minted), `A`/`R` into `docs/archive/work/` |
| Model calls with a recorded usage row | **61** adjudication sittings (54 in landed lanes, 7 in the two in-flight lanes; 16 dispute rulings, 45 spine/census/disposition/Done-when sittings) | `ADJUDICATE-<sha7>.md` files added in the window (61, each with a `.requested` marker) = 61 `ADJUDICATE COMPLETED` telemetry commits on the lane branches = 61 `docs/iteration/call_*.log` session logs, all `phase: ADJUDICATE` with `cost-usd` and `context-used` set. No review call has a usage row. `out/adjudicator/` holds only two retained-session records |

Regressions: 25 findings (24 of them late), 14 strict and 11 operational; 6
are primary `regression` and 19 are secondary tags. History-rederive: 5
primary + 2 secondary, all but one in WI-902 (WI-858 F1 is the other primary).

## 5. Rows that were hard to classify

1. **WI-858 001 F1** (replayed store marker): `history-rederive`, reading the
   marker files as a replayed log with no record of consumption. The other
   choice is `defect` (a replay-safety bug).
2. **WI-902 003n F1** (title match imports an unrelated lineage):
   `history-rederive`, mint identity inferred on replay. The other choice is
   `open-input` (a same-title collision as a registry shape). The order rule
   would make that one primary, so the choice matters: open-input would be 27,
   history-rederive 4.
3. **WI-880 004 F2** (the coordinator workstation's hook opt-in): `process`, a
   landing step on machine-local settings. It is also a Done-when item, so
   `defect` would be defensible.
4. **WI-884 001 F1** (blank line before the `Reviewed:` opener): `defect`,
   because the spec states "first line exactly". The other choice is
   `open-input` (a file shape).
5. **WI-881 002n F1** (late-spawn race): primary `regression`, because its
   site came from build round 2. That round answered a sitting's returns, not
   a review, so it only counts as a fix round under section 3's definition.
6. **WI-798 001 F4, WI-887 007 F2** (malformed values under a general
   "malformed means refuse/fresh" rule): `open-input`, because the rule names
   no members. A reader who takes the general rule as closing the space would
   call them `defect` (2 rows; WI-887's other record-shape findings follow the
   same call).
7. **WI-834 032 F1** (Windows root path lacks the runtime offer): `defect`,
   because the platform was enumerated. The other choice is `open-input`
   (platform variant).
8. **WI-823 F1** is `instrument` although the dispute refuted it: a
   scope-aware RESYNC presence check would have shown that no entry was owed.
9. **WI-834 039 F1**: `strict` regression, assuming the round-1 lexer's
   braces-as-boundaries caused the over-denial. Not proven by a base run.
10. **WI-834 012 F1** is `accepted`, although the lane first parked at its
    round bound (D-016) and resumed on the owner's word (D-018). **WI-834 016
    F2** is `escalated` because the owner ruled its remedy (D-019).
11. The four partial-instrument rows (WI-798 F5/F6, WI-902 010n F3/012n F1)
    stay `spine-text`. A per-token CodeSymbol check plus a test-node check
    would catch only their deleted-name part.

## 6. Comparison with the plan's unreproduced claims

Written after sections 1-5 were final, from `README.md` lines 1-35 and item
1's Evidence paragraph (line 194). No classification was changed after
reading them, and the comparison exposed no misread file.

| plan claim (one analysis pass) | this baseline, base-1 cohort (21/69/79) | chosen cohort (19/65/74) | verdict |
|---|---|---|---|
| 21 WIs, 69 rounds, 79 findings | 21 / 69 / 79 | 19 / 65 / 74 | reproduced; the cohort is base 2 + WI-853 and WI-870's pre-convention rounds (section 2) |
| 4 WIs took 41 of 69 rounds | 834:20 + 902:9 + 887:6 + 881:6 = 41 | 41 of 65 | agrees |
| 43 late findings | **43** | 42 | agrees: the "round 2 onward" rule on the same cohort gives exactly 43. The one-finding gap is WI-853's second review, which only base 1 counts |
| 18 of 43 late from open input spaces | **20** of 43 | 19 of 42 | differs by 2, at a class boundary (below) |
| ~24 spine-text | 22 primary (23 as any tag); 9 of them late | 21 (22); 9 late | close over all findings; far off over late findings |
| ~6 mechanical (instrument) | 4 primary + 4 partial = 8; 2 late | same | brackets ~6 |
| 15 regressions | **15 strict**, 26 under the brief's site-changed rule | 14 strict / 25 | the strict criterion matches exactly; the brief's operational definition gives about 10 more |
| six history findings | 5 primary + 3 secondary = 8 (6 of them in WI-902) | 5 + 2 = 7 | close; WI-902 alone gives six |

Why they differ, as far as the plan's text lets me tell:

- **Scope of the taxonomy.** 18 + 24 + 6 = 48 exceeds 43, so the spine-text
  and mechanical figures cannot be exclusive classes of the 43 late findings.
  They must be counted over all 79 findings, or be overlapping tags. Read over
  all findings, mine agree (22 and 4-8). Read over late findings only, mine
  are 9 spine-text and 2 instrument: most spine-text findings arrive in a
  lane's first full review, and the narrow rounds defer them "for checkpoint".
- **Open input, +2.** The plan's Evidence paragraph names the members:
  WI-834 shell forms, WI-887 store-record shapes, WI-902 history edge cases,
  WI-798's ambient credential source. Mine match on each kind: 8 late WI-834
  shell forms, 4 late WI-887 record or config shapes, 3 late WI-902
  history/file edges, 1 WI-798 source. My extras are workstation members the
  plan's description does not name: WI-834 012 F1, 016 F2, 024 F2 (an old
  Python first on PATH, no Git) and WI-853's reused dispute ids. On the other
  side, the pass may have put some of WI-902's replay findings (002n F1, 003n
  F1, 008 F1) under "history edge cases" where I used `history-rederive`.
  Without the pass's per-finding table, the two-finding gap cannot be pinned.
- **Regressions.** The plan's 15 equals my count of findings where the
  earlier fix introduced a failure the code before it did not have. The
  brief's operational test (the site was changed by an earlier fix) also
  counts incomplete fixes that left their own class open (WI-834's
  shell-reader rounds, WI-887's record reader), which brings it to 25/26. The
  measure should name which of the two it tracks.
- **Instrument.** The plan's item 6 names the RESYNC-presence check, which
  covers WI-823 F1 (refuted on scope), and fixing LLR-292 so `trace.py
  --strict` runs, which covers WI-887 007 F6. My other two are already
  reported by existing checks that nobody gates on (the trace.py form finding,
  the check_trajectory connectivity warning). The four partial rows would need
  per-token CodeSymbol and test-node checks that do not exist.
- **Item 1's "every full review after a WI-834 narrow approval found new open
  input members (016, 024, 028)".** Six full reviews followed a WI-834 narrow
  APPROVE (012, 016, 024, 028, 035, 039). Under my classes, five found an
  open-input member. 035's two MINORs (unrunnable PowerShell command text, a
  latch/blackout instruction clash) are output and feature-interaction
  defects, so "every" holds for 5 of 6.
