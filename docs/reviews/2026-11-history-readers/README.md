# History readers in the kit's scripts (2026-11-21)

Which calls in `project-trajectory/scripts/` read git history, and whether
each one recomputes a past decision. Evidence for WI-1036: the review-churn
plan's item 2, step 3, "audit the other history readers"
(`docs/plans/2026-10-11-review-churn/README.md`, section 2). The rule it
applies is PROCESS.md §3, "Record a decision where it is made": a decision a
later step depends on is recorded by the step that makes it, in its own
commit, and a later reader trusts that record and never recomputes the
decision from history or from current state (the scope-critique rubric's
B3). This note changes no code and files no row. The coordinator files one
queued row per class (c) site on trunk after the merge.

Read at `1aa6c439a` (`refactor_again`, the lane's base).

## What counts

The spec's closed definition: a `git` invocation whose subcommand is `log`,
`rev-list`, `blame`, `reflog`, `merge-base`, `describe` or `name-rev`, or any
invocation carrying `--first-parent` or a revision range (`A..B`, `A...B`),
made by a file under `project-trajectory/scripts/`. `git show` and `git diff`
at a named revision read one state and count only when they take a range.

**Method.** Every git invocation under `project-trajectory/scripts/` was
listed from the source's syntax tree: each call of a git wrapper
(`kitlib.git.git_out`, `git_bytes`, `git_paths`, `agent_common.git`, and the
private wrappers in `bookkeeping`, `check_privacy`, `derive_stage`,
`handback`, `rejudge` and `traj_parse`) and each `subprocess` call whose argv
opens with `"git"`. A call whose argv is built in a variable was resolved by
reading it, and so was each range held in a variable (a recorded
`commit_range`, the loop's train range) back to the call that takes it.
Three greps cross-check the listing; the first found one call the syntax
pass missed, `traj_parse.py:403`, whose argv is joined with `+`:

- `grep -rnE "[\"'](log|rev-list|blame|reflog|merge-base|describe|name-rev)[\"']" --include=*.py project-trajectory/scripts`
- `grep -rn "first-parent" --include=*.py project-trajectory/scripts`
- `grep -rnE '\}\.\.\.?(\{|HEAD)|\+ *"\.\.\.?" *\+' --include=*.py project-trajectory/scripts`

The shell, PowerShell and command templates in that folder make no history
call (`git config`, `git rev-parse`, `git clone` only). Each call is cited at
the line holding its subcommand, or its range for a ranged `diff`; a shared
reader's callers are not counted again.

## Counts

69 history calls in 25 files: 45 class (a), 20 class (b), 4 class (c). Twelve
of them are borderline, marked in the table and explained below or in the
class (c) sections.

At filing the spec named 21 scripts. One of them, `held_status`, makes no
history call: it matched on a docstring that mentions a first-parent delta.
Five files the filing's pattern did not reach call `merge-base` or diff a
range: `agent_loop`, `dispatch`, `handback`, `id_carrier` and
`review_brief`. That gives 25.

## The classes

- **(a) A range or a listing.** The call lists or diffs commits between two
  points, or places one commit relative to another (`merge-base`), to judge
  or show what the range holds now. A check run at the event it decides (a
  commit hook, the merge slot judging the lane it is about to land) is here
  too, even where an earlier step ran the same rule.
- **(b) An event's own commit.** The call reads a commit that is a recorded
  event (a claim, an act, a close, a record's adding commit) or one named
  commit's own message or parents, and trusts what it holds.
- **(c) A recomputed decision.** A later reader rebuilds the outcome of a
  decision an earlier step made by replaying history or reading current
  state, where that step wrote a record, or §3 owes one, that the reader
  does not read.

## The calls

Paths are under `project-trajectory/scripts/`.

| Site | Command | Class | Reason |
|---|---|---|---|
| `acceptance_record.py:1895` | `log --name-only -- docs/archive/last_accepted` | b | Borderline. Finds the commit that last wrote each snapshot file and checks it was a copy of live at that commit: the commit-time mirror rule run again to catch a write that bypassed it, pinned to the writing commit. |
| `adjudicate_brief.py:502` | `log --oneline <commit_range>` | a | Lists the range the partial-close report recorded, as brief evidence. |
| `adjudicate_brief.py:505` | `diff --name-status <commit_range>` | a | The same recorded range's paths. |
| `adjudicate_brief.py:1260` | `log -1 --diff-filter=A HEAD -- docs/work/active/*/WI-n-*.md` | b | Borderline. After the merge, finds the claim commit (the newest that added the spec under `active/`) and reads the claimed Done-when there. |
| `agent_brief.py:254` | `log --oneline <base>..HEAD` | a | The worker brief's list of earlier commits on the branch. |
| `agent_brief.py:256` | `diff --name-status <base>..HEAD` | a | The same range's paths. |
| `agent_brief.py:849` | `log --format=%s <commit_range>` | a | The WI ids in the subjects of the build just made, to decide now whether a critique round is owed. |
| `agent_common.py:773` | `log --format=<trailers> <base>..HEAD` | a | The worker's `WI:` and `Blocked-WI:` trailers over the train's range, each written by the commit that carries it. |
| `agent_common.py:1229` | `log --first-parent --grep=<claim subject> <branch>` | b | `claim_base`: finds the claim commit by its recorded subject and checks its move. |
| `agent_common.py:1269` | `log --first-parent --grep=<claim subject> <trunk tip>` | b | `loop_claimed`: reads the claim commit's own `Loop-Session` trailer. |
| `agent_common.py:1303` | `merge-base <trunk> HEAD` | a | Borderline. `default_base`, the lane's integration base for its evidence ranges; one use of it reads the claimed Done-when there. |
| `agent_loop.py:2093` | `diff --name-only <impl_range>` | a | The reviewed range's paths, for the anti-gaming tripwires. |
| `baseline_snapshot.py:609` | `log -1 -- <snapshot copy>` | b | `stamp`: the commit that last wrote a registry's snapshot copy, which only an act writes; advisory. |
| `baseline_snapshot.py:683` | `log -1 -G<status line> -- <snapshotted registries>` | c | `acceptance_stamp` dates the last acceptance by the last diff touching a status line. See (c) 1. Resolved by WI-1040. |
| `baseline_snapshot.py:2111` | `log -- docs/requirements/assumptions.toml` | c | Borderline. `_risk_first_written` binds a risk no act names to the first commit holding its current value. See (c) 2. Resolved by WI-1041. |
| `baseline_snapshot.py:2155` | `log -- docs/archive/last_accepted/acts.toml` | b | `risk_acceptance_act` walks the act ledger's history for each act's commit and reads the copy recorded there; the ledger's header says git holds each act's commit. |
| `check_docs.py:673` | `log --name-only` | a | Last-change time per path, for the `--stale` doc warning. |
| `check_privacy.py:730` | `log -p <rev_range>` | a | Scans a range the caller names. |
| `check_test_first.py:147` | `rev-list --first-parent <rev>` | a | Trunk's first-parent line, to check the declared start stands on it. |
| `check_test_first.py:178` | `rev-list --first-parent <start>..<rev> -- <older carriers>` | a | Whether the walk would cross registries under an older carrier. |
| `check_test_first.py:278` | `rev-list --first-parent <since>..<rev> -- <registry>` | c | Borderline. `first_acceptance_commits`. See (c) 3. |
| `check_test_first.py:314` | `rev-list --first-parent <rev> -- <test-case and design registries>` | c | Borderline. `_touching`, read by `first_association_commits`. See (c) 3. |
| `check_test_first.py:424` | `log --first-parent -m -p -G<Implements marker> <rev>` | a | Borderline. Where each `Implements:` declaration first appears on trunk, from the line's patches. |
| `check_trajectory.py:1858` | `log --format=<WI trailers> HEAD` | b | `WI:` trailers, each written by its commit, set beside the registry for an advisory that flips nothing. |
| `check_trajectory.py:2187` | `blame --line-porcelain -- <registry>` | a | Last-edit time per row, for the backlog staleness warning. |
| `check_trajectory.py:2274` | `log -1 --format=%ct -- <path>` | a | Last-edit time of a path, for the same warning. |
| `check_trajectory.py:3095` | `log --format=%ct --name-only -- docs/reviews` | a | Last-change time of each critique file, to pick the newest and judge it stale. |
| `check_trajectory.py:3250` | `log --no-merges --grep=Loop-Session:` | b | Borderline. Judges each loop commit's status moves against the dial in its own tree: the held-status rule run again to catch a commit that bypassed it, pinned to that commit. |
| `derive_stage.py:730` | `log -1 --format=%cs` | b | HEAD's own date, stamped beside its short sha in `docs/stage`; one commit, no walk. |
| `dispatch.py:617` | `merge-base <trunk> <branch>` | a | The base of the range whose failed commit-check rounds are counted. |
| `handback.py:309` | `merge-base <branch> <trunk HEAD>` | a | The range the partial-close report records (`commit_range`), written at the close. |
| `handback.py:709` | `diff --name-only <trunk>...<branch> -- docs/reviews` | a | The lane's own delta, to find its adjudication verdict file. |
| `handback.py:1031` | `merge-base <branch> <trunk HEAD>` | a | The base a quarantine reverts the lane to. |
| `id_carrier.py:585` | `merge-base <parent> <lane tip>` | a | The base of the lane's own delta, for the landing's id sweep. |
| `integrate.py:493` | `merge-base --is-ancestor <tip> HEAD` | a | Crashed-claim recovery: the candidate claim commit is not on trunk. |
| `integrate.py:495` | `merge-base --is-ancestor <tip>^1 HEAD` | a | The same: its parent is. |
| `integrate.py:1191` | `merge-base HEAD <branch>` | a | `_lane_base`, the base of the lane's delta for the minted-id rung. |
| `integrate.py:1271` | `merge-base HEAD <branch>` | a | The base of the spine delta the acceptance-act rung judges. |
| `integrate.py:1306` | `log --boundary <HEAD>..<branch>` | a | The lane's commits, for the provenance-trailer rung. |
| `integrate.py:1429` | `rev-list <HEAD>..<branch>` | a | The lane's commits, for the per-commit rungs. |
| `integrate.py:1472` | `log -1 --format=%ct <ref> -- <paths>` | a | `_last_commit_time`: nothing in the repository calls it. |
| `integrate.py:1480` | `log -1 --format=%B <rev>` | b | One commit's own message: the crashed-claim candidate's subject. |
| `integrate.py:1761` | `merge-base --is-ancestor HEAD <branch>` | a | §A2: trunk is already an ancestor of the lane. |
| `integrate.py:2001` | `merge-base HEAD <branch>` | a | The base of the lane's delta for the adjudication-only scope test. |
| `integrate.py:3225` | `merge-base HEAD <branch>` | a | The base for the S9 review-scope check at the slot. |
| `integrate.py:3704` | `log --first-parent --no-merges <since>..HEAD` | a | `audit`: trunk's non-merge commits in a named window. |
| `kitlib/git.py:302` | `merge-base --is-ancestor <head> <tip>` | a | A squash's lane contains trunk's HEAD. |
| `kitlib/git.py:304` | `rev-list <head>..<tip>` | a | The squashed commits each per-commit rule walks. |
| `kitlib/git.py:362` | `log -1 -- docs/work/active/<branch>` | b | Borderline. `claimed_work_branch`, once the close has moved the claim out of the tree: any commit that touched the claim folder. |
| `kitlib/verdict.py:528` | `log -1 --format=%B <rev>` | b | A refresh commit's own subject and `Checks-Passed:` record. |
| `kitlib/verdict.py:604` | `log -1 --format=%B <rev>` | b | `read_passed_checks`: the commit's own `Checks-Passed:` record, checked against its tree and parent. |
| `kitlib/verdict.py:817` | `log -1 --format=%B <rev>` | b | `mechanical_close`: the close commit's own subject. |
| `kitlib/verdict.py:1302` | `log --name-status <base>..<branch> -- docs/iteration` | a | Borderline. Session logs the lane's commits added or rewrote; feeds the failure count and the slot's S9 check. |
| `kitlib/verdict.py:1505` | `log --format=%B <base>..<branch>` | a | The newest verified `commit` record in the lane's range. |
| `kitlib/verdict.py:1539` | `merge-base --is-ancestor <rev> <of>` | a | Orders a recorded failure against the last pass. |
| `kitlib/verdict.py:1599` | `log --name-only <base>..<branch> -- docs/reviews docs/iteration` | a | Borderline. Record paths the lane's own commits touched; feeds the slot's S9 check. |
| `kitlib/verdict.py:1906` | `log --format=%H%B <base>..<branch>` | a | Verdict trailers in the lane's range, a cross-check on the round evidence. |
| `observation_cadence.py:83` | `log --diff-filter=A --name-only <since>..<rev> -- docs/archive/work` | a | Rows closed since an observation's result, for the cadence floor. |
| `plan_gate.py:479` | `rev-list --parents -n 1 <rev>` | b | One commit's parents, to judge it against them. |
| `plan_gate.py:508` | `rev-list <trunk>..<branch>` | a | The lane's commits at the slot. |
| `plan_gate.py:528` | `rev-list <head>..<tip>` | a | A squash's commits. |
| `rejudge.py:314` | `log -1 --diff-filter=A <sha> -- <observation record>` | b | The commit that added an observation result, where its inputs were judged. |
| `retire.py:550` | `log --diff-filter=A --raw -- docs/log.d/retired` | b | The commit that added each retirement record, which by design cannot name its own commit. |
| `review_brief.py:1064` | `merge-base --is-ancestor <base> <sha>` | a | Checks a review range the caller named. |
| `trace.py:1424` | `rev-list --parents -n 1 HEAD` | b | HEAD's parents, the baselines the id watermark is judged against. |
| `trace.py:4311` | `log --format=%s <stamp>..HEAD -- <off-spine registry>` | a | Borderline. WI and OI ids in the subjects since the snapshot copy was written, as an advisory pointer. |
| `traj_parse.py:403` | `log -1 -- <dashboard sources>` | a | The dashboard's "state as of commit" stamp. |
| `trunk_step.py:230` | `log --diff-filter=A -1 -- <fragment>` | b | The commit that added a log fragment, which sets its merge order. |
| `trunk_step.py:240` | `log --diff-filter=A -1 MERGE_HEAD -- <fragment>` | b | The same, during a merge composition. |

## The class (c) sites

### (c) 1. `baseline_snapshot.py:683`, `acceptance_stamp`

- **The decision it recomputes:** when the last acceptance act happened. It
  takes the newest commit whose diff adds or removes a `status =` line in a
  snapshotted registry. Its own docstring grants that this also names a row
  addition or a new draft, and that it answers nothing under the CSV
  carrier.
- **The record that should carry it:** the act ledger,
  `docs/archive/last_accepted/acts.toml`. An acceptance act made through
  `intake.py snapshot` appends an entry with its `date`, and the commit
  that added the entry is the act's own commit, read the way
  `risk_acceptance_act` already reads it (`baseline_snapshot.py:2155`,
  class (b)).
- **Its reader:** the re-acceptance brief's heading (`trace.py:4823`);
  advisory. No LLR names the function.
- **Resolved by WI-1040** (2026-11-21): `acceptance_stamp` is removed. The
  heading reads `baseline_snapshot.last_act`: the act ledger's newest entry
  and the commit that added it, found by `risk_acceptance_act`'s walk.
  When that commit is not in the readable history, the heading names no
  other commit.

### (c) 2. `baseline_snapshot.py:2111`, `_risk_first_written`

- **The decision it recomputes:** which acceptance an assumption's accepted
  risk is bound to, when no acceptance act names the assumption. It walks
  the live registry's history back to the first commit at which
  `accepted_risk` held its current value, and uses that commit as the
  anchor.
- **The record that should carry it:** an acceptance act naming the
  assumption (an entry in `acts.toml` listing its id), the anchor the main
  path of `risk_acceptance_act` reads. Where no act names it, there is no
  acceptance to anchor to, and the reader can say so; the function's own
  message already tells the reader to accept the risk in an act.
- **Borderline:** in the case it covers no record exists by construction, so
  the change is to stop deriving an anchor, not to read one. LLR-239
  (Accepted) states this fallback, so a row against it amends LLR-239.
- **Resolved by WI-1041** (2026-11-21): with no act naming the assumption,
  `risk_acceptance_act` reports the risk unanchored, naming the assumption
  and the act it owes, and walks no history. `_risk_first_written` is
  deleted, and LLR-239's text says so.

### (c) 3. `check_test_first.py:278` and `:314`

The two calls serve one decision, so one row may cover both; the coordinator
decides.

- **The decision they recompute:** when each row was accepted.
  `first_acceptance_commits` (278) finds the commit at which each
  requirement first reads Accepted; `first_association_commits`, through
  `_touching` (314), the commit at which each pair of a test case and a
  requirement it names first reads accepted. Both replay every first-parent
  commit touching the registries and apply the acceptance-act rule
  (`acceptance_record.acceptance_acts_between`) to each commit and the one
  before it.
- **The record that should carry it:** the acceptance act. Each ledger entry
  lists the rows the act accepted and re-accepted, its commit is the one
  that added the entry, and the snapshot copy at that commit holds the
  accepted rows, each test case's `Verifies` included, so the pair can be
  read there too.
- **Borderline, for three reasons.** SR-217 and LLR-257 (Accepted) state the
  replay, so a row amends LLR-257. Acceptances before the ledger's first
  entry (seq 1, 2026-09-27) have no entry: the replay dates them now, and
  the ledger alone would not, so the row must say how they are read (the
  module's "at or before" reading is one shape for it). And whether every
  flip to Accepted since then carries a ledger entry is for that row to
  establish before the ledger is trusted.

## Borderline calls

- **Checks that run a commit-time rule again over history**
  (`acceptance_record.py:1895`, `check_trajectory.py:3250`), classed (b).
  Each judges a past commit as of its own tree, so later state cannot move
  the answer, and no later step consumes what the commit-time rule decided:
  they exist to catch a commit made without the hook. A strict reading of §3 ("never recomputes
  the decision from history") would put them in (c). The commit-time rule
  writes no record of its pass, so there is nothing for them to read
  instead.
- **Claim lookups by path** (`adjudicate_brief.py:1260`,
  `kitlib/git.py:362`), classed (b). Both read evidence of the claim event,
  but find it by a path search rather than from a record that names it.
  The brief's lookup could read a claim revision if the Done-when
  adjudication row the merge mints (`intake.py`, `_done_when_draft`)
  recorded one; that row records only the closed spec. `claimed_work_branch`
  is broader than `agent_common.claim_base`, which reads the same event by
  its subject and checks its move; its docstring states the residual (any
  branch name that ever appeared under `docs/work/active/` reads as claimed).
- **The integration base** (`agent_common.py:1303`), classed (a). Most uses
  take it as a range's base. Some readers of a lane's claim copy
  (`adjudicate_brief._subject_claim`, `plan_gate._claim_base`) read it
  there, at merge-base(trunk, HEAD), not at the recorded claim commit
  (`claim_base`). The two agree unless trunk edits a claimed spec after the
  claim.
- **The slot's review-scope check** (`kitlib/verdict.py:1302` and `:1599`,
  from the slot, over the base `integrate.py:3225` reads), classed (a).
  `kverdict.review_scope_refusal` runs the same S9 rule the loop runs after
  each review session, and its docstring calls it re-derived. It is the
  landing's own decision, made at the merge event over the ranges the
  session logs recorded, so it reads a range, not a later state.
- **The implementation landing** (`check_test_first.py:424`), classed (a).
  It reads where each `Implements:` line first appears on trunk from the
  line's patches. No step records which requirements a landing implements,
  and no decision is rebuilt.
- **The off-spine ruling pointer** (`trace.py:4311`), classed (a). It names
  the rulings that touched a registry from the WI and OI ids in commit
  subjects. It decides nothing (an advisory line), but it reads authority
  from free text.

## Outside the definition

Not listed, by the closed text:

- A `diff` between two named revisions (`diff A B`), such as the two-tree
  rules in `acceptance_record`, `held_status`, `text_then_act` and
  `kitlib/verdict`. Git treats `diff A..B` the same way, but the definition
  counts only the range spelling.
- `for-each-ref --contains` (`kitlib/git.py:479`, `lanes_containing`), which
  walks ancestry but is not one of the named subcommands.
- One-commit reads: `diff-tree <commit>`, `rev-parse <rev>^1`,
  `show <rev>^:<path>`, `cat-file`, `ls-tree`.

Two leftovers for whoever next touches these files: `integrate._last_commit_time`
(listed at `integrate.py:1472`) has no caller, and `traj_parse._git` has no
caller either (it makes no history call).
