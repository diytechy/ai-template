## 2026-09-02 — WI-579: the verdict carrier, tree identity, and the `adjudication_review` dial

The OI-76 build (ruled 2026-08-31: **B with C and the generated rollup;
governing = TREE IDENTITY**), consolidated with WI-559 DW2 and WI-560 DW1 by
the 2026-09-02 backlog restructure (plan §2.2). The three were built together
because built apart in any order the later lane undoes part of the earlier one:
WI-558 DW2 retires the gate's freshness comparison, WI-560 DW1 builds one
shared freshness definition for the gate *and* the C2 derivation, and WI-559
DW2 only means something once a round carrier exists.

### What was read before anything was written

- `integrate._verdict_gate` read `docs/reviews/WI-<n>-REVIEW-A.md` per `merged`
  WI and compared that file's last commit TIME against `_last_commit_time` over
  the work tip excluding `docs/reviews` and `docs/log.d`. Nothing in the kit
  writes that file — the plan's finding (a).
- `agent_loop.review_owed_by_evidence` asked a DIFFERENT question — "does any
  round file name HEAD's short sha?" — over a DIFFERENT exclusion set (none).
  That is the double-identical-round class WI-560 DW1 names.
- `ADJUDICATE` is in `agent_loop.NON_BUILD_PHASES`, so `build_bookkeeping` never
  scheduled a round for a committing adjudication, while the gate demanded its
  REVIEW-A anyway. Every adjudication merge was a supervisor stop (plan §0).
- Round files are `docs/reviews/<train>/<NNN>-REVIEW-<X>-<sha7>[-relaxed].md`,
  committed by the reviewer session; the loop commits the session log
  `docs/iteration/<train>-<NNN>-<stamp>.log`, whose `# phase:` header is the
  logged-session anchor finding K needs.
- `score_reviews.latest_phase_verdicts` already existed, its docstring saying
  "the deterministic latest-file-per-phase rule **the integrator gate reads**"
  — and **no caller anywhere**. It was written for this predicate and never
  wired. The new gate uses it rather than growing a second one.

### What was built

1. **`kitlib/verdict.py`** — the verdict record's one home. The non-record tree
   identity (a SHA-256 fold of `git ls-tree -r` with `docs/reviews/`,
   `docs/log.d/` and `docs/iteration/` dropped), the `Review-Verdict:` trailer
   grammar, the round-file / session-log join, and the branch-scoped readers.
   The digest is 64 hex **deliberately not 40**: a 40-hex `tree=` sitting beside
   `Bar-Green: tree=<40 hex>`, which IS a git tree object id, would read as the
   same kind of value and is not one.
2. **`integrate._verdict_gate`**, recomputed over that evidence and decomposed
   into four functions (the first cut scored 13 on the complexity ratchet; a
   bump there was refused, so it was split instead). Freshness retires into
   identity — read at the **work tip**, which is the one thing the identity rule
   inherits verbatim from the comparison it replaces, since a station refresh
   merges the trunk in and would otherwise stale every honest APPROVE.
3. **`[attestation] adjudication_review`** (`never` / `when-minting` /
   `always`, shipped and set `when-minting`) through ONE reader,
   `agent_common.adjudication_review_owed`, consulted by the merge gate and by
   the round scheduler. The phase deliberately STAYS in `NON_BUILD_PHASES` — a
   judgement is not a build, and widening that set would have bought the round
   by asserting something false.
4. **`gen_verdict_rollup.py`** — the rollup dies as a gate input and is reborn
   generated: `docs/stack.ini [generated]`, `trunk_step.py --regen`, a
   `check.py verdict-rollup` freshness step, the hook floor, and
   `_TRUNK_FRESHNESS_STEPS`. **A lane never commits one** (which is why this
   branch carries no `docs/reviews/rollup/` files): the trunk step writes them
   after the merge that brings the round files in.
5. **Migration window and RESYNC entries** — the legacy hand-authored rollup
   still clears the gate, judged by the same identity rule, with a stderr WARN
   naming it.

### Three decisions worth stating, because a successor will re-ask them

**The trailer is not an accept path, and that is the whole anti-forgery story.**
Anyone with commit access can type `Review-Verdict: APPROVE …` onto their own
commit, and the self-verification (tree = the carrier's own non-record tree)
will pass, because it is their tree. What a session cannot forge is the
*coordinator's* committed session log. So the ROUND EVIDENCE decides and the
trailer is read as a CROSS-CHECK: a trailer naming the tree under judgement that
contradicts the rounds REFUSES the merge. A design where the trailer alone
cleared the gate was considered and rejected for exactly this reason.

**One review scope per train, so the round evidence is computed once for the
branch and not per WI.** A worker schedules its round only when every assigned
WI is built, over the combined train diff (LLR-140) — a per-WI slice of a round
never existed. The per-WI loop that remains is the migration window's, because
the legacy rollup was per-WI and an adopter's tree still is.

**The rollup names no governing verdict.** Governing is tree identity, a
question about a branch's current tree answerable only against a repository at a
moment. Writing an answer into a checked-in file would recreate exactly the
artifact the ruling retired: a stale summary that reads as authority. Every row
in the rollup is a fact about a FILE, which is also what makes `--check`
deterministic.

### A defect the tests found

Both new readers asked drafts for `safety_class`. `intake.parse_dispositions`
NORMALIZES that cell into `kind` (defaulting an undeclared one to `ordinary`),
so both would have read `None` for every draft and silently waived the round —
`when-minting` would have behaved as `never`. Found by
`test_a_minting_adjudication_still_owes_its_round`, which is the reason that
test asserts the OTHER answer beside the merge-with-no-verdict case.

### Deviations from the spec, stated

- **The rollup is per TRAIN, not per WI.** DW3 says "the per-WI rollup becomes a
  GENERATED artifact". A train IS the review scope (LLR-140) and a per-WI
  granularity would have to invent a slice of a round that does not exist. The
  generated path is `docs/reviews/rollup/<train>.md`; the legacy per-WI path
  stays untouched as the migration window's carrier, which also means the
  generator and the window can never fight over one file.
- **"The supervisor prompt's hand-compile instruction retires in the same
  change" — there is no such in-repo prompt.** Measured: nothing under
  `project-trajectory/prompts/`, `docs/` or the skills carries a hand-compile
  instruction. The live carriers of the retired RULE are
  `.claude/skills/session-protocol/SKILL.md` ("Order the close against the
  verdict round") and PROCESS_OPTIONS.md's "The LLM-gate verdict protocol";
  both are re-pointed from the time comparison to the identity, and the skill
  now says in as many words not to hand-compile the rollup. The instruction the
  Done-when means was carried in the supervisor's own operating notes, outside
  this repo.
- **The ordering rules do NOT retire with the comparison.** DW2 retires the
  *freshness comparison*; "close before the final verdict round, never
  hand-merge trunk" survives unchanged, because under identity a close still
  changes `docs/work/` and so still changes the tree. Restated in those terms
  rather than deleted.

### Bars

Reviewed ratchet bumps, each with its reason at the entry: `agent_common.py`
1272→1305, `agent_loop.py` 2519→2578, `integrate.py` 1298→1382, `check.py`
1163→1177, `bootstrap.py` 1658→1660, and the smoke membership ceiling 1480→1560.
`_verdict_gate`'s complexity bump was REFUSED and the function decomposed
instead.

Smoke tier at the re-stamp: 1505 collected, **1497 passed / 8 skipped**, 25.2 /
27.1 / 27.4 s wall over three warm runs against the 60 s ceiling — the seconds
budget is not touched.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=1ad5d465 -->

Full unfiltered suite at the row's tip, on a quiet box:
**3336 passed, 24 skipped, 1 failed in 605.75 s** — and the one failure is
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`,
which is CAUSED by this row and is the TRUNK LANE'S to clear. `docs/stage` is
declared `[generated]`; a work branch must never commit it (its whole history
is trunk-side claim / mint / refresh commits), `check.py`'s `derived-stage`
step SKIPs on a claimed branch for exactly that reason, and `trunk_step.py
--regen` re-derives it after the merge. Bisected rather than assumed: the test
passes at this branch's integration base `0ecc62bb` in a clean worktree, so it
is this row's spine edits that moved the fingerprint, not an inherited red.
<!-- fig: cmd="python -m pytest -q -n auto" rev=5ea28d6a -->

**A finding this raised, out of scope and not fixed here.** That test has no
lane stand-down. `check.py` learned in WI-141 that a work branch must not
answer for a trunk-owned generated artifact and SKIPs the `derived-stage` step
with a notice; the pytest assertion beside it did not, so **every spine-touching
lane's full-suite run reds on it**, and the honest signal is indistinguishable
from a real staleness. The fix is one guard, not this row's to write.

`ruff format` is clean. `ruff check` reports three pre-existing F401/F841 in
test modules this row did not touch (`test_agent_loop.py`,
`test_trace_hats.py`, `test_trajectory_holdban.py`); `lint` is not a declared
step here, and they are not this row's to fix.

Deferred open items: none — OI-76 is ruled and this row is its build.
