+++
id = "WI-1036"
title = "Audit the kit scripts that read git history, and file a row for each one that recomputes a past decision"
workstream = "process"
sr_refs = []
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1036`, cut from `refactor_again` at
`1aa6c439a`, with the commit hooks on. No code changed. The specref (the
review-churn plan's item 2) is cleared at close, as a terminal row's is.

- `7047e36c8`: the note, `docs/reviews/2026-11-history-readers/README.md`.
- The close-out commit after it: this Deliverable, the move to `complete/`,
  the log fragment and the regenerated views.

**What the note holds.** Every history call under
`project-trajectory/scripts/` at `1aa6c439a`, by Done-when 1's closed
definition: 69 calls in 25 files, each with its file and line, its git
command, its class and one line of reason. 45 are class (a), reading a
range; 20 are class (b), reading an event's own commit; 4 are class (c),
recomputing a past decision. Twelve are marked borderline, each with why.
<!-- fig: derived="the counts the note docs/reviews/2026-11-history-readers/README.md declares, read at 1aa6c439a by the method its 'What counts' section states" -->
The note states its method (a syntax-tree listing of every git invocation,
cross-checked by three greps it quotes), the three classes as applied, and
what the closed definition leaves out (a two-revision `diff A B`,
`for-each-ref --contains`, one-commit reads).

**The recount.** The spec named 21 scripts at filing. `held_status` makes
no history call (it matched on a docstring), and five files call
`merge-base` or diff a range: `agent_loop`, `dispatch`, `handback`,
`id_carrier` and `review_brief`. That gives 25.

**The class (c) sites, for the coordinator's rows** (the note's "The class
(c) sites" section gives each one's decision and record in full):

1. `baseline_snapshot.py:683`, `acceptance_stamp`: dates the last
   acceptance from the last diff touching a status line; the act ledger's
   newest entry and the commit that added it should carry it. No LLR names
   the function.
2. `baseline_snapshot.py:2111`, `_risk_first_written`: binds an accepted
   risk no act names to the first commit holding its current value; an
   acceptance act naming the assumption should carry it. Borderline. LLR-239
   (Accepted) states the fallback, so its row amends LLR-239.
3. `check_test_first.py:278` and `:314`: replay the registries' history to
   find when each row, and each test case's pair with a requirement, was
   accepted; the acceptance act's ledger entry and the snapshot copy at its
   commit should carry it. The two calls serve one decision, so one row may
   cover both. Borderline. SR-217 and LLR-257 (Accepted) state the replay, so
   the row amends LLR-257.

**Tests.** The row changes no code, so the runs reduce to the strict lints
and the commit hook, on the note's tree:

- `trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=138
  LLR=348 TC=401 orphans=0 integrity=0`.
- `check_trajectory.py --root . --strict`: exit 0, `check_trajectory:
  clean (1036 work item(s), 906 done (87%), 35 cancelled, graph acyclic).`
- The commit hook passed on `7047e36c8`.

`run_menu.py smoke` was not run: the hook did not ask for it, and the
builder's brief drops it for a row that changes no code.

**Byte deltas.** No budgeted or byte-watched file was touched. The note is
new, 20,496 bytes.

**Acts owed.** None by this row. A row the coordinator files against
LLR-239 or LLR-257 amends an Accepted LLR and will owe its own act.

**Review (2026-11-21, round 1, over `1aa6c439a..c49af216d`):** the
coordinator's hand-built brief (the kit-change rubric, the spec at the tip,
the diff with the generated views excluded), asking for spot-checks of the
call sites and a recount. OpenAI Sol (low): APPROVE, no findings. Gemini
Argon (low), by file reference, timed out at 900 seconds inside opencode's
own start-up (its log stops at `init`, before any model call), so Sol
reviewed alone (queue-drill HANDOFF §6). The coordinator's rulings on the
builder's two questions: the two `check_test_first.py` calls take one row,
since they serve one decision; the two re-run checks stay in class (b).

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

- [x] The note, `docs/reviews/2026-11-history-readers/README.md`, lists
      every history call at the lane's base, recounted, with its class and
      one line of reason. A history call is, closed: a `git` invocation
      whose subcommand is `log`, `rev-list`, `blame`, `reflog`,
      `merge-base`, `describe` or `name-rev`, or any invocation carrying
      `--first-parent` or a revision range (`A..B`, `A...B`), made by a
      file under `project-trajectory/scripts/` (the kit's shipped scripts;
      tests, root `scripts/` and hooks are out). `git show` and `git diff`
      at a named revision read one state, not history, and are counted only
      when they take a range.
- [x] Each class (c) site is named with the decision it recomputes and the
      record that should carry it. The lane files no row; the coordinator
      files one queued row per site on trunk after the merge.
