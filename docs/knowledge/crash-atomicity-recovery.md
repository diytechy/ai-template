# Crash, atomicity and recovery: what the next reader finds after an interrupted write — DRAFT

> **DRAFT (agent-authored, WI-546, 2026-08-30).** Drafted by the unattended lane so the `hat.INTEGRITY-RECOVERABILITY` roster entry has a `knowledge` value to point at; the owner reviews and cuts at RETURN, per the `hats.toml` header's own rule. This distills THIS repo's accumulated perspective from its own decisions and surfaces — it is not retrieved external research, and its claims are the drafter's reading, not a ratified finding.

This pack is what a reviewer wearing INTEGRITY-RECOVERABILITY looks for HERE. The
charter's question — "interrupted mid-write, what does the next reader find, and
what gets the system back to a state it can name?" — has a repo-specific answer,
because this kit made most durable state a **git-committed artifact** rather than
a file it rewrites in place. That choice is the recovery story, and it is also
where the sharp edges are.

## What this hat looks for here

**A durable artifact rewritten in place with no all-or-nothing boundary.** The
kit's answer, where it is disciplined, is to move the boundary onto an operation
that is already atomic. Two exemplars to hold as the bar:

- The **log-fragment compile** (`trunk_step.py --compile-log`, contract IF-168 in
  `docs/log.d/README.md`). *Every* fragment is validated before *any* is written,
  and the append-then-unlink is stated all-or-nothing, so "a half-compiled log can
  never exist" (`trunk_step.py` module docstring, and the `_problems`/validate-all
  loop). The drop-box shape itself removes the merge-conflict surface: one file
  per session, never two edits to one file end.
- The **claim move** is atomic by being a serial trunk commit, not a filesystem
  trick: `active/<branch>/` appearing IS the claim, and concurrent claims resolve
  by push rejection as compare-and-swap (`docs/concurrency-restructure.md` §2).
  `spec_move._place_moved_file` prefers `git mv` and falls back to a single
  `Path.replace` (an atomic rename) for the untracked case.

**A per-write operation the reviewer might assume is atomic but is not.** Be
honest about the counter-example in this very repo: `baseline_snapshot.copy_live`
mirrors seven registries with a plain `shutil.copyfile` loop — no temp-then-rename,
no cross-file transaction. A crash mid-loop leaves a *partially copied* snapshot.
What saves it is not filesystem atomicity but a **loud read-side guard**: a
registry missing from a standing snapshot is an INTEGRITY error
(`unanchored_findings`, armed at migration step 7), and a snapshot file that will
not parse RAISES rather than reading as empty. The pattern to demand, then, is
not "every write is atomic" but "every non-atomic write has a reader that refuses
the torn state" — `{}` and `None` are opposite claims and the code keeps them so.

**A claim or lock nothing can reclaim once its holder is gone.** SR-144's own
rationale names the deadlock case directly: "a claim a dead lane never releases."
The kit's defenses are (a) the coordinator lock is a *kernel advisory lock*
released on exit **or crash**, with no pid reasoning and no timer
(`agent_common.acquire_lock`), and (b) a dead lane does not silently hold its
work — it closes into a **terminal partial state that merges like any branch**,
carrying one immutable per-close report (SR-144, `system-requirements.toml`).

**A record that is mutable, or that a second write can overwrite.** SR-144 is the
distilled lesson here: five successive dedup mechanisms leaked because each
reconstructed the return event from a MUTABLE proxy; the fix was an *immutable
per-close document*, and the rule refuses a second close of the same event rather
than overwriting the first. Read "a close no one can read is indistinguishable
from a run that finished" as the general test: silence must not be a success
signal. `baseline_snapshot.refresh_refusal` is the same instinct one tier up — a
refresh that would absorb approved text is refused unless a `Status` flip or an
explicit `--approves` ref authorises it, so the record of what a human blessed
cannot be quietly rewritten.

## Application

- **Prefer git-commit atomicity to in-place rewrite.** Crash recovery here is
  "the tree is whatever the last commit says" — the fail-closed integrator ff's
  only on green and refuses on red (`concurrency-restructure.md`), and id
  allocation and claims live in serial trunk commits, so a killed lane leaves no
  torn allocation to reconcile.
- **If a write is not atomic, name the reader that refuses the torn state.** The
  snapshot is the worked example: non-atomic copy, but a parse-or-raise loader and
  an integrity finding for a missing member. A reviewer should ask for the guard,
  not assume the write.
- **A recovery path must exist for the ATTENDED reach of a corruption too.** The
  charter's third listen — "a recovery path written only for the unattended run
  when the same corruption is reachable attended" — means: if a human running the
  same command by hand can produce the torn state, the guard must fire for them,
  not only inside `agent_loop`. The snapshot guards run on the always-on
  `--strict-integrity` floor and the pre-commit hook, which is the right altitude.
- **Silence is never done.** A terminal state with no report is LOUD (SR-144); a
  missing snapshot registry is an error, not "nothing approved". Demand the same
  of any new durable artifact.

## Open questions / bounded here

- The snapshot copy loop is intentionally non-atomic and defended by read-side
  guards only; whether that is the right trade for a *seven-file* record, versus a
  temp-dir-then-rename of the whole snapshot root, is an open design call — not a
  ratified position. Flagged, not fixed.
- The advisory lock is best-effort across hosts (flock over NFS is unreliable) and
  degrades to unguarded on a filesystem that cannot lock (ENOLCK/ENOTSUP). That is
  a stated bound, not a hole to close silently.
- SR-144 carries `hat_refs = ["UNATTENDED-OPS"]` today, not this hat; the
  immutable-record and dead-lane-claim reasoning it encodes is the clearest
  in-repo statement of this hat's concern, and whether its hat_ref should widen is
  an owner call at review.
