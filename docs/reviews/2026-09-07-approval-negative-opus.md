# Approval boundary implementation review

Provider: claude-opus-5/high. Reported cost: USD 6.887933500000003. Preparation, outside control window.

Read-only review complete. No files were edited and nothing was committed.

## Scope and snapshot

**Important caveat:** the working tree changed under me three times during this review. `tests/test_baseline_snapshot.py` grew from +39 to +135 lines, a new exemption function `_primary_merge_snapshot_sync` appeared in `acceptance_record.py`, `docs/archive/last_approved/README.md` became modified, and `acceptance_record.py`'s hash changed again on my last check (`16e97473…` → `ebd7f881…`). Findings below are re-verified at the latest tip I could read, but **line numbers may have shifted again** — I cite symbols alongside them. Nothing here is a live-spine approval; this is an implementation review only.

Reviewed: `acceptance_record.py`, `baseline_snapshot.py`, `kitlib/git.py`, `agent_common.py`, `integrate._approval_act_refusal`, `adjudicate_brief.py`, the three prompts + `CATALOG.md`, `PROCESS.md`/`PROCESS_OPTIONS.md`, the three skills, and the four/five edited test modules. I did **not** read `OWNER_SCRATCHPAD.md`.

## Verdict: CHANGES-REQUESTED

## Bar state at this tip

- `python -m pytest -q -n auto -m smoke` → **1690 passed, 8 skipped, 59.9 s** vs the 90 s budget (`check_smoke_budget.py --mode enforce`: *within*).
- `ruff check` → clean.
- **`ruff format --check` → RED.** `docs/stack.ini:46` declares this as the `[product] format` step:
  ```
  Would reformat: project-trajectory/scripts/adjudicate_brief.py
  Would reformat: tests/test_adjudicate_brief.py
  2 files would be reformatted, 242 files already formatted
  ```
- One combined run failed `tests/test_baseline_snapshot.py::test_a_STATUS_MOVE_refresh_is_STAMPED_as_a_Status_move`; it passed in isolation and on re-run, and the collected count changed between runs (285 → 286), so the tree moved mid-run. **Not attributable — the suite has to be re-driven at a frozen tip.**

---

## Findings

### 1. `is_linked_worktree` compares path *strings*, not identity — it falsely refuses the primary checkout — CONFIRMED, high
`project-trajectory/scripts/kitlib/git.py:124-132`

`Path(root).resolve() != primary.resolve()` is a textual comparison. Three false positives, each reproduced on this box:

| `root` passed | result |
|---|---|
| `/tmp/kgtest/primary` (the primary itself) | `False` ✓ |
| `/tmp/kgtest/primary/docs` (a subdirectory) | **`True`** ✗ |
| `/tmp/kgtest/PRIMARY` (case-variant, valid on APFS/NTFS) | **`True`** ✗ |
| `/tmp/kgtest/outer/inner_project` (a dir inside an unrelated repo) | **`True`** ✗ |

Failure scenario: an adopter scaffolds a project into a directory that sits inside another git repo and runs `intake.py snapshot --seed`. `copy_live` (`baseline_snapshot.py:906`) hits `raise SystemExit` **before any mutation** and reports "a linked worktree may not write…", which is false and unactionable. Same root cause makes `staged_snapshot_findings` emit a linked-worktree finding that `trace.py` appends to `findings.integrity`, hard-failing `--strict-integrity` in a legitimate primary checkout. This breaks the stated invariant *"accepted primary synchronization must remain valid."*

`resolve()` follows symlinks but does not case-fold, and the kit is required to run on Windows and POSIX. Fix: compare identity (`os.path.samefile`) or, better, ask git directly — `git rev-parse --git-dir` vs `--git-common-dir` differ exactly in a linked worktree and answer "not a repo" correctly, which also removes the subdirectory case.

### 2. `intake.py` still mints the removed instruction into every new adjudication spec — CONFIRMED, high
`project-trajectory/scripts/intake.py:804-813` and `:823-828`

The prompts, `PROCESS.md`, `PROCESS_OPTIONS.md` and both skills were rewritten to remove model-side approval/copy. The **mint** was not. Every newly minted first-approval adjudication spec still gets:

> "…either APPROVE (move the rows' `Status` to `Approved` and take the anchoring snapshot, `python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`, in ONE reviewed commit on this lane)… The approval act is YOURS"

and a title reading `"…then approve (flip + snapshot) or return with findings"`.

Mitigating: `agent_loop` line 807 replaces the worker prompt wholesale with `adjudicate_brief.compose`, so this `## Context` does **not** reach the adjudication prompt. But it is durable spec text that the close ritual requires the session to read, and the title reaches the work registry, `status.md` and every banner. A session that follows it is hard-refused at `_approval_act_refusal` and, in a linked worktree, `SystemExit`s out of `copy_live` — a burned lane. This is a straight scope gap in "prompts remove model-side approval/copy."

### 3. The refusal's remedy is now false for the actor it newly refuses — CONFIRMED, medium-high
`project-trajectory/scripts/acceptance_record.py:694-699` (`lane_approval_refusal`)

The message still ends: *"Leave the rows `Drafted`: the first-approval adjudication minted at this merge is what reads the chain, flips and takes the snapshot, on trunk."* An adjudication branch is now refused by this same text and told that the adjudication will do what it just tried — a circular instruction at the one place a stopped session reads.

The deleted `adjudication_approval_refusal` carried an explicit `# THE REMEDY, PER ARM` block for exactly this reason ("a session reading only those learns it is stopped and not what to do"). That discipline was dropped rather than carried across. The new linked-worktree finding (`acceptance_record.py` ~:1083) likewise names no remedy.

### 4. Deleted scope/authority enforcement has no code and no tracked owner — CONFIRMED, medium
`acceptance_record.py` (`adjudication_approval_refusal`, deleted)

Three checks went with it: OUTSIDE-`Adjudicates`-scope, snapshot WIDENED, and approved-WITHOUT-its-anchor. `docs/handoff-2026-09-07.md` step 2 says to *"preserve scope/authority checks at trunk publication."* They are not preserved anywhere — `first_approval_scope` survives with **no runtime caller** (only its own docstrings and `tests/test_acceptance_record.py:358`), and a grep of `docs/work/{queued,active,handback}` finds no WI owning restoration. Meanwhile `adjudicate-first-approval.template.md:47,100` now *promises* the model that "the primary publication gate must stop that widening" — a promise with no implementation behind it.

Related dangling claim: `project-trajectory/scripts/consolidate.py:917-919` still asserts *"The first-approval sibling has enforced exactly this bound since WI-572 (`is OUTSIDE `Adjudicates` scope`)"*. That sibling was deleted in this slice. This is the stale-negative-claim shape — nothing detects it.

### 5. Stale docstring and a now-vacuous test around the removed actor branch — CONFIRMED, medium
`project-trajectory/scripts/integrate.py:1114-1122`, `tests/test_integrate_admission.py:523`

`_adjudication_lane`'s docstring still says *"the approval rung needs the answer BEFORE the bar question exists"* and *"UNREADABLE FRONTMATTER ANSWERS FALSE: … here it makes the branch a work lane whose approval act refuses."* `_approval_act_refusal` (`integrate.py:1129`) no longer calls it at all; its remaining callers are the bar directives and the verdict gate.

Consequently `test_unreadable_actor_frontmatter_fails_toward_the_approval_refusal` passes for a reason unrelated to its name — actor readability can no longer change the outcome, so the "fails toward" property it claims to pin is untestable. Rename/repurpose it or drop it; a green that cannot go red is not coverage.

### 6. The amendment brief asks for a "publication scope" it never derives — CONFIRMED, medium
`project-trajectory/prompts/adjudicate-amendment.template.md:99`

The RELEASED bullet now demands *"record the exact row decision, authority basis and publication scope in this verdict."* But `ADJUDICATE-AMENDMENT` has no `{registries}` or `{approves_rows}` slot (`CATALOG.md:21`). The first-approval path derives that mapping precisely so the session doesn't reconstruct it (`adjudicate_brief.py:810-816`: *"Keep the mapping derived here rather than leaving the session to reconstruct it"*). The amendment path now does the opposite.

The same edit also deleted the only instruction covering *"a row's new text is NOT one you would bless"* (previously: draft the corrective work in `## Dispositions`). Line 104's retained sentence covers a different case — don't rewrite a row you are judging — so the drafts-not-mints trigger for the amendment path lost its only entry point.

### 7. The shipped kit now documents a publisher that does not exist — CONFIRMED, medium
`project-trajectory/PROCESS_OPTIONS.md:464-465`; `skills/gate-advance/SKILL.md:138-141`; `skills/spine-authoring/SKILL.md:19-26`

Present tense, no marker: *"Mechanical publication applies an accepted first approval"*, *"The mechanical publisher copies accepted content in the approval commit"*. Nothing implements it, and the old mechanism is removed. For a kit whose templates must stay copy-ready, an adopter cloning this today has **no path by which a spine row reaches `Approved` through the loop** — and the docs give them no way to know that. Needs an explicit "not yet implemented — approve by hand in the primary checkout" until the publication slice lands.

### 8. `worker.template.md` states a per-WI rule with no signal and no enforcer — CONFIRMED, medium
`project-trajectory/prompts/worker.template.md:45`

> "A spine-authoring WI may author `Drafted` rows and amend governing cells within its declared scope; an implementation WI must return a needed change to governing SN/SR/LLR prose as a handback…"

Neither term is a declared value (`safety_class` is `ordinary|spine|adjudication`); the WORKER template carries no slot naming the class (`CATALOG.md:28`) and `assignment_block` does not expose it; and no check refuses an implementation WI that amends an LLR. The previous rule ("a lane may amend any cell of any row") was uniform and needed no classifier. This one is a new prose rule with an undefined term and zero detectors.

### 9. The linked-worktree guard fires only in the `git add`→`git commit` window — CONFIRMED, medium
`acceptance_record.py` ~:1070-1081 (`staged_snapshot_findings`), pinned by `tests/test_baseline_snapshot.py::test_a_linked_worktree_reading_a_committed_snapshot_delta_is_not_a_write`

The new arm is gated on `head is None`, so the **committed** view (`committed_snapshot_findings`) never reports it. The stated invariant covers *staged* writes and is met — but the same docstring in this function argues at length why a staged-only rule is the wrong shape: *"the gap between them was a working laundering step — a forged copy committed with the hook bypassed was seen once."* The pre-commit hook runs the staged pass with `|| true`. The real backstop is `_approval_act_refusal` at the merge slot, which does refuse the branch; that should be stated where the gate is read, and the new test's name should say "the committed view does not check" rather than implying the read was judged safe.

### 10. Test gaps — CONFIRMED, medium
- **No positive control.** Nothing asserts `copy_live` still *succeeds* in the primary of a repo that has a linked worktree. `test_a_clean_copy_satisfies_the_mirror_invariant` uses a tree with no worktrees, so the guard is never exercised in its allow direction — this is exactly the gap that leaves finding 1 undetected.
- **No fail-open pin.** `is_linked_worktree` returns `False` when git is unreadable, which the off-git seed path depends on. Untested and undocumented — and it is the opposite fail direction from `lane_approval_refusal`'s stated "an unread delta is not an empty one."
- **No unit test for the new shared reader.** `tests/` has `test_kitlib_ladder.py`, `test_kitlib_secret_classes.py`, `test_kitlib_stage.py`, `test_kitlib_station.py` — there is no `test_kitlib_git.py` for `worktree_records` / `primary_worktree_root` / `is_linked_worktree`.
- **`== []` assertions may be reading silence.** `test_only_an_exact_primary_merge_may_stage_snapshots_in_a_linked_worktree` and `test_primary_snapshot_sync_does_not_reapprove_pending_worker_wording` both assert `staged_snapshot_findings(linked) == []` without first asserting that the merge actually staged a path under `docs/archive/last_approved/`. If it staged none, the green means nothing. Add the premise assertion.
- **The invariant is asserted at the producer, not the gate.** Nothing drives `trace.py --strict-integrity` end-to-end to prove the linked-worktree finding changes the exit code.

### 11. Extraction dropped the rationale that justified the shared home — CONFIRMED, low-medium
`kitlib/git.py:94-121` vs the deleted `agent_common.worktree_records` / `primary_worktree_root`

Lost: "branch is `None` when that worktree is detached"; "`[]` when git cannot answer — **each caller chooses its own fail direction**"; and the whole `primary_worktree_root` why (a dispatched worker reaching the durable cross-train iteration aggregate, and the local-dir fallback "so a draw never crashes"). The WI-263 ordering guarantee survives; the rest has no home now.

Two silent behavior changes, neither noted: missing-git now returns `[]` instead of raising `FileNotFoundError` (an improvement, but it is the fail direction the old docstring *claimed* and did not have), and `stdin=subprocess.DEVNULL` is no longer passed.

---

## What I confirmed as sound

- `copy_live`'s refusal is the **first statement**, before any mutation — invariant met.
- The staged linked-worktree finding is emitted **before** the byte-comparison loop and is independent of identity, so a byte-identical staged copy still fails `--strict-integrity` — invariant met (subject to finding 9's window).
- Every WI branch, adjudication included, is now refused for `Status` flips and snapshot deltas: `_approval_act_refusal` no longer reads `metas` or the actor, and `merge_approval_refusal` takes no actor/scope argument that could become permission. Pinned by the rewritten `test_an_adjudication_lane_cannot_land_its_flip_and_snapshot` and `…cannot_use_the_no_flip_snapshot_bypass`.
- `_primary_merge_snapshot_sync` (the late-arriving exemption) is tight in the directions I probed: `MERGE_HEAD` must be an ancestor of the *primary's* HEAD, the staged snapshot tree must be byte-equal to that source, no snapshot path may have moved worker-side since the merge base, and each source path must have mirrored live at the commit that wrote it. `_git(...) is None` correctly reads `--is-ancestor` and `--quiet` exit codes (success returns `""`, not `None`), and every unreadable question fails closed. One redundancy: the `if head is not None: return False` at its head is dead — the only caller already gates on `head is None`.
- `CATALOG.md` digests match `prompts.catalog_rows()` exactly; all five byte-budget stamps in `byte-budget-guard/SKILL.md` match `wc -c`.
- No live registry row names `adjudication_approval_refusal`, so its deletion strands no `CodeSymbol` cell. `SR-140`'s "copy rides the same reviewed commit as the approval" remains satisfiable — a human in the primary can still run `intake.py snapshot`.
- The brief-side empty-scope refusal (`adjudicate_brief.py:736`) survives, so `docs/registry-machinery-reference.md:793` is still true.

## Scope limits I did not treat as defects

New primary-turn publication is not implemented and is not claimed. The consequence worth stating: at this tip an adjudicator's `APPROVE` moves nothing, so rows stay `Drafted` and `docs/stage` cannot advance until the publication slice lands. The mint is per-merge-delta (`_released_drafted_rows`), so already-ruled rows are **not** re-minted — I checked; there is no re-adjudication runaway here. Spine-cell amendments (LLR-140/152/153/154/158/167/207, TC-146/147/148/153/161/205) are handed back by design and I did not judge them.
