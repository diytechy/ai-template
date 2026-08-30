# WI-548 — REVIEW-A (compiled)

The WI-level verdict the merge slot reads (RULING-7), compiled by the
supervising session from the round files below — ordered by commit time,
the governing verdict last. Every line is quoted from its round file;
nothing is judged here that a reviewer did not judge.

## Round 1 — 001-REVIEW-A-7fc69de.md

- [MAJOR] project-trajectory/scripts/agent_loop.py:2965 -> C4's required fake-route regression is UNCOVERED: no changed test drives `probe_route`/`select_with_probe`, so a failing probe can regress into spending a real session on a known-bad route without a test detecting it -> add an end-to-end fake-route test proving a cooled route's non-OK/limit probe is cooled and skipped, a valid `OK` probe proceeds, and a clean route is not probed -> @owner
VERDICT: CHANGES-REQUESTED findings=1

## Round 2 — 001-REVIEW-A-3ae9427.md

- [MAJOR] project-trajectory/scripts/agent_loop.py:3857 -> a REVIEW OWED restart reconstructs only the train range/queue, not `last_impl_family`; the first resumed REVIEW-A therefore treats the builder family as cross-family and writes an unmarked verdict, silently defeating C5's required relaxed-fallback audit trail -> persist/reconstruct the committed build's family before scheduling the owed round, and add the single-family parked/restart regression -> @owner
- [MAJOR] project-trajectory/prompts/reviewer.template.md:25 -> C7 now requires reviewers in this meta-repo to run `python scripts/check.py` and `python scripts/trace.py`, but neither path exists here (the shipped commands are under `project-trajectory/scripts/`), so the required independent harness read fails before the verdict -> render a script-directory slot or use the repo-correct paths and pin the meta-repo prompt execution -> @owner
VERDICT: CHANGES-REQUESTED findings=2

## Round 3 — 001-REVIEW-A-fbcf04d.md

- [MAJOR] project-trajectory/scripts/agent_loop.py:3101 -> `write_review_owed` suppresses every marker-write failure even though that untracked marker is the only durable evidence that the review queue remains open; on restart `worker_endstate(..., review_open=False)` then returns `EXIT_DONE` for the committed WI and reports “review round approved,” so a disk/permission failure after reviewer exhaustion can complete or advance unreviewed work -> make persistence fail closed (do not return `EXIT_REVIEW_OWED` unless the marker is durably written, and add a regression drive that makes the write fail and proves the lane cannot reach DONE) -> @owner
VERDICT: CHANGES-REQUESTED findings=1

## Round 4 — 001-REVIEW-A-2eaf030.md

- [MAJOR] project-trajectory/scripts/integrate.py:1734 -> `_RESIDUE_PREFIXES = ("out/run-logs/",)` declares every ignored child of the directory to be loop residue, so `_shed_declared_residue` unlinks unrelated sole-copy operator evidence before deleting the worktree; a driven `integrate._unload_branch` lane with `out/run-logs/operator-notes.txt` returned `unloaded=True` and left `private_exists=False` -> restrict the declared residue to coordinator-owned stream filenames/metadata (and add a neighboring-foreign-file refusal test) so C6 sheds only streams the loop owns -> @owner
VERDICT: CHANGES-REQUESTED findings=1

## Round 5 — 001-REVIEW-A-c40838c.md

VERDICT: APPROVE findings=0

## Governing verdict

The final round above governs:

    VERDICT: APPROVE findings=0
