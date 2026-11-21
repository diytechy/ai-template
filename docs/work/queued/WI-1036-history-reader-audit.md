+++
id = "WI-1036"
title = "Audit the kit scripts that read git history, and file a row for each one that recomputes a past decision"
workstream = "process"
sr_refs = []
needs = []
specref = "docs/plans/2026-10-11-review-churn/README.md#2-record-the-decision-at-its-event-checked-at-the-commit"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-21 so the review-churn plan's phase 3 is not lost
(queue-drill hand-off §3.3 N2). This is item 2's third step, "audit the
other history readers": read-only research, not a build. The plan places it
in phase 3.

The rule it applies already exists. A decision a later step depends on is
recorded by the step that makes it, in its own commit, and a later reader
trusts that record and never recomputes it from history (PROCESS.md §3;
item 2, ruled 2026-10-11; the scope-critique rubric's B3). WI-902's reshape
was its first application. No later work item ran the audit. A 2026-08-15
log entry deleted some dead history readers, but that was before the rule
existed.

At filing, 21 kit scripts call `git log`, `rev-list` or `--first-parent`:
`acceptance_record`, `adjudicate_brief`, `agent_brief`, `agent_common`,
`baseline_snapshot`, `check_docs`, `check_privacy`, `check_test_first`,
`check_trajectory`, `derive_stage`, `held_status`, `integrate`,
`kitlib/git`, `kitlib/verdict`, `observation_cadence`, `plan_gate`,
`rejudge`, `retire`, `trace`, `traj_parse` and `trunk_step`. Most
legitimately diff a range.

Settled here:

- **Classes.** Each history call is one of: (a) it diffs or lists a range
  (legitimate); (b) it reads a recorded event's own commit (legitimate,
  since the record is trusted); (c) it recomputes a past decision from
  history or current state (B3). The note gives one line per call site
  saying which class and why.
- **Output.** A note under `docs/reviews/`. For each class (c) site, the
  coordinator files one queued row on trunk at this row's landing, as
  WI-1017's sample filed WI-1018 to WI-1020. The lane does not mint rows on
  its branch.
- **No code changes** in this row.

## Done-when

- [ ] The note, `docs/reviews/2026-11-history-readers/README.md`, lists
      every history call at the lane's base, recounted, with its class and
      one line of reason. A history call is, closed: a `git` invocation
      whose subcommand is `log`, `rev-list`, `blame`, `reflog`,
      `merge-base`, `describe` or `name-rev`, or any invocation carrying
      `--first-parent` or a revision range (`A..B`, `A...B`), made by a
      file under `project-trajectory/scripts/` (the kit's shipped scripts;
      tests, root `scripts/` and hooks are out). `git show` and `git diff`
      at a named revision read one state, not history, and are counted only
      when they take a range.
- [ ] Each class (c) site is named with the decision it recomputes and the
      record that should carry it. The lane files no row; the coordinator
      files one queued row per site on trunk after the merge.
