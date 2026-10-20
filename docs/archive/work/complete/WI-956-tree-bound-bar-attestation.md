+++
id = "WI-956"
title = "One tree-bound bar attestation names the bar it attests: one grammar and one verifier for a build commit and the landing refresh, written only by a producer that ran that bar"
workstream = "process"
sr_refs = ["SR-156"]
specref = ""
buildtier = "high"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-955"]
+++

## Deliverable

Closed at its landing on 2026-10-20, after its gate, in a headless leg:

- One `Bar-Green:` grammar carrying `bar=<review|landing|no-bar>` and
  `tests=<digest|none>`, one verifier (`kitlib/verdict.py`
  `bar_attestation`, the commit's own tree and first parent, exactly one
  column-0 line) and one tests digest; `refresh_attestation` recognizes
  only a verified `landing` or `no-bar` refresh, so a `review` record is
  never peeled and never makes a lane merge-ready. The old trailer without
  `bar=` is not read.
- One producer (`integrate.py` `_attest_commit`) for the refresh and the
  new `integrate.py attest` verb: it fixes the staged tree before the bar,
  refuses a red bar or one that moves the index or worktree, restores the
  index on every failed write, and joins the line to the message's trailer
  block (`kitlib/provenance.py` `append_trailer`, shared with the loop
  trailer).
- `attest` refuses before the bar when hooks are off, on the branch the
  primary checkout holds, on a dirty worktree (untracked files included),
  below the harness floor, on an undeclared or empty `[bars] review`, and
  on an unreadable message or one carrying the label; it reads the review
  bar and `[product] test` from the attested lane's own declarations.
- `[bars] review` declared in `stack.ini.template` (the kit's commit bar)
  and here (the run menu's smoke action), with no default (D-002 of
  coordinator-2026-10-20, a forced migration in the RESYNC entry).
- Spine: LLR-207, TC-205 and TC-132 amended and re-attested (sitting 010,
  act); LLR-247's and TC-370's traced cells and six interface data cells
  reconciled.

## Context

Review-churn item 13, precondition 2 (corrected in revisions 16 and 18):
the green record is made at the commit and trusted at dispatch. The existing
`Bar-Green:` trailer cannot serve as it stands:

- Only the landing refresh writes it (`integrate.py:refresh`).
- Its verifier is refresh-specific: `kitlib/verdict.py:refresh_attestation`
  demands the `refresh: <branch> onto trunk` subject, the commit's own tree
  and its first parent.
- It names no bar. The summary is free text (`_run_bar`: `bar PASS (N steps,
  tier T)`; the adjudication arm: `no-bar (adjudication, §A5.2)`).
- `verdict.work_tip` peels on it before `refresh`'s `reset --hard`, and
  `_peel_target` / `governing_rev` walk through it. A wrong peel destroys
  committed work.

So a build-round tip carries no record of green. This row builds the one
record both review dispatch and landing check. WI-957 and WI-958 consume it;
P8 later fills its test set from the spine.

**Without P8**, the review bar is the commit bar plus the lane's named tests
(the set `review_brief.py review --tests` names today). The attestation
records which tests, so P8 only changes how the set is chosen.

**Anchor.** SN-004 and SN-008 (approved). SR-156's landing seam runs the
declared bar on the composed tree; LLR-207 (Approved, under SR-156) states
`refresh_attestation` and is amended here. A derived SR for the review-bar
record is drafted TC-first in the lane if the sitting finds LLR-207's
amendment does not carry it.

## Deliverables

1. **One grammar.** The trailer keeps the label `Bar-Green:` and gains two
   required fields: `bar=` from a closed set (`review`, `landing`, `no-bar`)
   and `tests=` (a digest of the sorted named test paths, or `none`). The
   label constant stays in `kitlib/station.py`.
2. **One verifier in `kitlib`.** It takes a commit and returns the verified
   fields, or nothing: the tree and parent must equal the commit's own, the
   bar must be in the set. `refresh_attestation` becomes the refresh subject
   plus this verifier plus `bar` in {`landing`, `no-bar`}; `work_tip`,
   `_peel_target` and `_merge_ready` keep calling it, so a `review`
   attestation is never peeled and never satisfies the merge slot.
3. **One producer**, shared with the refresh (PROCESS.md §3, 0→A→B): stage,
   run the named bar on the staged tree, `write-tree`, commit with the
   trailer, re-verify, else undo. The refresh calls it for `landing` /
   `no-bar`. A new `integrate.py attest --branch <b> --bar review --tests
   <files...> [--message-file <f>]` calls it for `review`: with staged work
   it commits that work carrying the trailer; with nothing staged it writes
   an empty attestation commit on the tip. It refuses a dirty worktree
   (tracked changes not staged, or untracked files not ignored) before
   running anything.
4. **The review bar's one declaration.** A key in `docs/stack.ini` naming the
   review bar's command (proposed `[bars] review`), shipped in
   `stack.ini.template` as the kit's commit bar (`check.py --jobs 0 --tier
   smoke`) and set here to this repository's `[run] smoke` command. The named
   tests run after it through `[product] test`, each lane under its own
   `--basetemp`. See "Calls ruled at filing".
5. **Records.** IF-173's data cell gains `attest`. LLR-207 amended (row
   text at the checkpoint). One RESYNC entry: the grammar change (a lane
   mid-landing re-refreshes) and the new key. The worker brief's sentence
   on `Bar-Green` (`worker.template.md`) names the bar field.

## Trust

The trailer gates the merge slot today and review dispatch after WI-957
and WI-958. Written under [PROCESS.md §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer:** the one producer (deliverable 3), called by `integrate.py
  refresh` and `integrate.py attest`. A failed write is: a red bar (no
  commit; the branch restored), a dirty worktree (refused before the bar), a
  commit refused by a hook (restored), or a committed tree or parent that
  does not verify (undone, as `refresh` does today).
- **Consumers** (`grep -rn "refresh_attestation\|BAR_GREEN\|Bar-Green\|_merge_ready\|work_tip(" project-trajectory/scripts scripts --include=*.py`):
  `kitlib/verdict.py` (`refresh_attestation`, `_peel_target`, `work_tip`,
  `governing_rev`); `integrate.py` (`refresh`, `_merge_ready`);
  `dispatch.py` (the drain, through `_merge_ready`); `kitlib/station.py`
  (the label); `rendering/traj_panels.py` (draws the label only). Later:
  `review_brief.py` (WI-957), `agent_loop.py` (WI-958). Tests:
  `test_integrate_station.py`, `test_verdict_record.py`,
  `test_loop_provenance.py`.
- **Ruling.** No trailer, an unreadable commit, a trailer that does not
  match the grammar, a `bar=` outside the set, or a tree or parent that does
  not verify: not an attestation, in every consumer. A verified attestation
  for another bar than the consumer requires: refused, naming both. No
  consumer runs the bar to decide. The old trailer without `bar=` is not
  read: no legacy path (owner, 2026-10-03); the drain re-refreshes a lane
  that is not merge-ready (`dispatch.py`). The authority binds to the
  commit's own git tree and first parent, the bar name and the tests digest.
  The bound is `refresh_attestation`'s, unchanged: it defeats accident, not
  intent (PROCESS.md §6).
- **The review bar's declaration** (deliverable 4) decides which command
  may produce a `review` attestation, so it carries authority too.
  - *Producer:* a person or agent, editing `docs/stack.ini` by hand in a
    reviewed commit; a re-sync adds it with the shipped value. A failed
    write is a missing key, an empty value, or a file that does not parse.
  - *Reader:* one, through `kitlib/config.py`'s `read_stack_ini` (the one
    parse of the file), called by the shared producer before it runs any
    bar. No other consumer reads the key: the verifier reads only the
    trailer's bar name.
  - *Ruling:* an absent file, section or key, an empty or whitespace-only
    value, or a file `read_stack_ini` cannot read or parse: the producer
    refuses before running anything, naming the file, the key and the
    cause, and writes no commit. There is no default and no fallback to
    `[run] smoke` or `check.py` (D-002).

## Done-when

Each named test fails on the code before the change.
- **The grammar.** The verifier accepts a trailer whose tree and parent are
  the commit's own and whose bar is in the set, and refuses: a wrong tree, a
  wrong parent, a missing or unknown `bar=`, a missing `tests=`, a trailer
  quoted mid-line.
- **The peel stays the refresh's.** `work_tip` and `governing_rev` never
  peel a verified `review` attestation, and still peel a verified refresh;
  `_merge_ready` refuses a branch whose tip carries only a `review`
  attestation.
- **The producer.** `attest` with staged work commits it carrying a
  trailer that verifies; with nothing staged it writes an empty commit that
  verifies; on a red bar it commits nothing and leaves the branch and index
  as they were; on a dirty worktree it refuses before running the bar; on a
  missing review-bar key it refuses, naming the key.
- **The refresh** writes `bar=landing` (or `no-bar` on the adjudication
  arm) through the shared producer, and every existing refresh test passes
  with its fixtures moved to the new grammar.
- **The tests digest** is the same for the same set in any order, and
  differs for a different set.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` clean; LLR-207's amendment is judged at
  the lane's sitting; the RESYNC entry anchors at the landing's parent.

## Scope answers

- **S1.** One deliverable: the grammar, verifier and producer are broken
  alone, and the refresh's move onto them is the consolidation that keeps
  one grammar. Second of P1's four rows, after WI-955. The gates (WI-957,
  WI-958) are split off for containment: this lane's review looks only at
  the record and the peel.
- **S2.** `## Trust`.
- **S3.** Closed: the `bar=` set, deny by default; the producer's inputs
  (clean worktree, exit code 0 is green, any other is red). Forged trailers
  and tree-rewriting hooks are outside (the self-check refuses the latter).
- **S4.** `single`: Trust section, an input grammar, two families.
- **S5.** A new value domain on the trailer, a new CLI verb on IF-173, a new
  declared key. No new component; a Drafted IF row only if the plan moves
  the verifier into its own module.
- **S6.** `~WI-955` orders the lane under TC-first; no code dependency. B2
  (WI-914) landed. Nothing third-party. P8 will need this row.
- **B3.** The producer writes the record at the commit; no consumer
  re-derives it.
- **B4.** No owner act in the lane. The forced-migration call below is a
  delegated decision for the owner to confirm or overrule.

## Calls ruled at filing

- **A new required key forces a migration**
  ([coordinator-2026-10-20 D-002](../../../decisions/coordinator-2026-10-20.toml),
  delegated, high-risk, for the owner to confirm or overrule). Adopters
  running the loop get a review dispatch that refuses until the review
  bar's key is declared; the RESYNC entry adds it with the shipped value.
  Reading this repository's `[run] smoke` or `check.py` when the key is
  absent would be a fallback path (owner, 2026-10-03). The key's home is
  `docs/stack.ini`, beside the `[run]` commit bar it names, until item 10's
  one-file migration moves both into `docs/process.toml`.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-20; CHANGES-REQUESTED,
findings=1):

- **MINOR, S2 (the review-bar key's Trust contract): adopted.** The Trust
  section gains "The review bar's declaration": its producer and failed-write
  forms, its one reader (`read_stack_ini`, called by the shared producer),
  and "an absent file, section or key, an empty or whitespace-only value, or
  a file `read_stack_ini` cannot read or parse: the producer refuses before
  running anything".

Confirming round (Codex Sol, medium, convergence stance, 2026-10-20): APPROVE, findings=0; the dispositions above are confirmed.
