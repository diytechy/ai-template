## 2026-09-02 — WI-579: the verdict carrier, tree identity, and the `adjudication_review` dial

The OI-76 build (ruled 2026-08-31: **B with C and the generated rollup;
governing = TREE IDENTITY**), consolidated with WI-559 DW2 and WI-560 DW1 by
the 2026-09-02 backlog restructure (plan §2.2). The three were built together
because built apart in any order the later lane undoes part of the earlier one:
WI-558 DW2 retires the gate's freshness comparison, WI-560 DW1 builds one
shared freshness definition for the gate *and* the C2 derivation, and WI-559
DW2 only means something once a round carrier exists.

Deferred open items: none. (The open item this row builds is already ruled;
nothing here waits on an owner decision.)

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

(The fragment's deferral declaration is at the top, where it speaks for the
whole file.)

### Review A rework

The three requested corrections were accepted. `review_owed_by_evidence` no
longer scans whatever filenames happen to be on disk: it uses the same
branch-owned committed paths, logged REVIEW-session join and tree-bound parsed
entries as `_verdict_gate`, with a BUILD-session regression asserting both
readers refuse the false approval. `rounds=<N>` now means completed review
cycles represented at the governing tree — the maximum per-phase evidence
count, so REVIEW-A plus REVIEW-B is one cycle and rework starts over — and the
coordinator derives it from that evidence while the gate refuses a mismatched
stamp. LLR-207's rationale was rewritten as a living technical reason with the
historical provenance removed.

Focused verdict-record plus module-size regressions: **34 passed in 4.52s**;
the consolidation kept `agent_loop.py` and `integrate.py` at their existing
ratchet ceilings with no bump.

### The residue that rework left, and the identity dogfooded

Re-reading the changed signature rather than running another test found one
piece of residue: `review_owed_by_evidence` still took a `reviews_dir`
argument. The finding-1 fix replaced the on-disk directory scan with the
branch-scoped committed-path walk, so nothing read it any more — a parameter
naming a directory the function no longer opens, on the very function whose
defect was reading that directory. Dropped, with the now-unused pass-through in
`resume_owed_round`; the caller keeps its own `reviews_dir` local, which the
verdict-path and scoreboard slots still use. No behaviour changes, which is why
it is stated here rather than defended as a fix.

The row's own machinery was then driven over the row's own history, which is
the only end-to-end check available for a rule about trees:

| commit | what it touched | non-record identity |
| --- | --- | --- |
| `0c7cb4eb` close | the work | `e61a3d47…` |
| `f418cba1` rework | the work | `c3296412…` |
| `41b84e93` spec + fragment | `docs/archive/work/` + `docs/log.d/` | `6f314694…` |
| `7098ad21` telemetry | `docs/iteration/` + `docs/reviews/` only | `6f314694…` |

The last line IS the defect class this row exists to kill: a telemetry commit
moved HEAD and left the identity untouched, so it cannot re-owe a served round.
The `41b84e93` change is equally correct and worth stating, because it looks
like a counter-example and is not — a spec file under `docs/archive/work/` is
work, not a record of it, so editing it genuinely does invalidate a verdict.
The round on disk names `0c7cb4e`, whose identity no longer matches the tip;
a fresh round is therefore owed, and the gate says so.
<!-- fig: cmd="python -c \"import sys; sys.path.insert(0,'project-trajectory/scripts'); from kitlib.verdict import tree_identity as t; [print(r, t('.', r)[:8]) for r in ['0c7cb4eb','f418cba1','41b84e93','7098ad21']]\"" rev=7098ad21 -->

Full unfiltered suite re-driven at the tip after the signature change, because
removing a parameter is exactly the edit a grep can miss and `test_agent_loop.py`
is subprocess-heavy and so sits OUTSIDE the smoke tier that guarded the rest of
this session: **3339 passed, 24 skipped, 1 failed in 624.14s** — the same counts
as the rework commit, which is the expected shape for a change that added and
removed no test. The sole failure is the same
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`
trunk-owned `docs/stage` freshness assertion already diagnosed above; no new
failure appeared.
<!-- fig: cmd="python -m pytest -q -n auto" rev=0b1f3b41 -->

### Review A round 007 rework — the two readers, and two ways a rule can be defeated

Four findings, all accepted. Three were about the same thing from different
angles: a rule expressed as a value that something ELSE gets to choose.

**The rev is part of "one definition" (finding 2, MAJOR).** The gate measured
the identity at the peeled work tip and `review_owed_by_evidence` measured it at
`HEAD`, so WI-560 DW1's "one definition, two readers" held for every commit
class except the one the peel exists for — a station refresh. Driven on a
fixture carrying a genuine `Bar-Green`-verified refresh commit, `id(HEAD)`
and `id(work tip)` differ and the pre-fix loop answered `owed=True` while the
gate answered satisfied at the same instant: a resumed lane would draw a
strong-tier round whose file the gate would not even read. The fix is the
construction one, not a guard. `refresh_subject`, `refresh_attestation` and
`work_tip` moved OUT of `integrate` into `kitlib/verdict.py`, where
`governing_identity` composes the peel with the fold, and both readers are now
HANDED the answer instead of each choosing a rev. `integrate` keeps two
re-export lines so its own callers and the station tests are untouched; the
attestation LABEL was already `kitlib.station.BAR_GREEN`, so the writer and the
verifier now share one literal rather than two that must agree. What cannot
invalidate a verdict has two halves — the record PATHS and the refresh COMMIT —
and they now have one owner.

**Newest-wins, expressed as a type (finding 1, MAJOR).** `branch_trailers`
iterated `git log` (NEWEST-first) into `by_tree[tree] = ...`, so a tree carrying
two attestations handed its reader the OLDEST. Driven: two honest rounds at one
governing tree, stamped `rounds=1` then `rounds=2`, made the shipped gate refuse
with *"the attestation and the evidence disagree"* — a false forgery accusation
parking an approved lane at a supervisor stop, which is the OI-76 failure mode
re-created by the cross-check meant to prevent it. It returns the ordered
SEQUENCE per tree now, oldest first, so no reader can silently receive a
superseded stamp; the gate takes `[-1]` and says why. A verdict that FLIPPED at
one tree is a different thing and `flipped` already refuses it, from the
evidence.

**The identity read git's display encoding (finding 3, MINOR).** `fold_listing`
matched `RECORD_PREFIXES` against the raw `git ls-tree` field, and git QUOTES a
path holding a non-ASCII character — `"docs/log.d/WI-401-caf\303\251.md"` —
so the leading quote defeated every `startswith` and the record file folded INTO
the identity. One accented log fragment would silently stale every governing
verdict on the branch. `tree_identity` passes `-z` and `fold_listing` now takes
an already-decoded sequence of entries, so no reader here ever sees the display
form. The digest is unchanged for every tree with no quoted path (this repo has
none: `git ls-tree -r HEAD | grep -c '"'` is 0), so nothing already stamped
moved.

**The banner counted the wrong thing (finding 4, MINOR).** `st.rounds` collects
every COMPLETED round whatever its merged verdict, so *"2 review round(s)
approved"* was the report for a lane that took a CHANGES-REQUESTED round,
reworked, and passed — the same shape as the claim this function was changed to
stop making. It now says what the tally carries: `N review round(s) drawn this
run, latest verdict <word>`, with "this run" stated because the tally is
in-process and the branch's committed round files, not a banner, are what the
merge slot reads.

Each pre-fix predicate was replayed on the same fixtures the new tests build,
so the regressions are known to bite rather than merely pass:

| finding | pre-fix answer | post-fix answer |
| --- | --- | --- |
| 3, accented record path | identity moved `39ec685e…` → `b02ac9a2…` | unmoved |
| 1, two stamps at one tree | `('APPROVE', 1)` vs evidence 2 → refusal | `[('APPROVE',1),('APPROVE',2)]`, merge |
| 2, after a genuine refresh | loop `owed=True`, gate satisfied | both satisfied |
<!-- fig: cmd="scratchpad/drive_prefix.py — replays the pre-fix fold, trailer map and HEAD-measured derivation on the new tests' fixtures" rev=working-tree -->

Three tests were added (`test_a_record_path_is_excluded_whatever_characters_it_holds`,
`test_the_newest_attestation_at_a_tree_governs_the_cross_check`,
`test_a_station_refresh_owes_no_round_and_the_two_readers_agree`) and TC-205's
evidence list was completed — three tests from the round-002 rework
(`round_count`, the round-count contradiction, the derived trailer count) had
never been added to it, so the row under-declared what it drives.

`integrate.py` was re-stamped DOWNWARD 1382 → 1352 by the move;
`agent_loop.py` stays at 2578 (the banner rewrite trades the nested conditional
for a named `note`, which is line-neutral rather than a bump);
`kitlib/verdict.py` is 227 SLOC and still opens no ratchet entry.

### A fifth defect, found by verifying the fourth

Round 007's finding 2 was fixed by lifting the refresh peel into
`kitlib/verdict.py` so both readers are handed one rev. Driving that fix rather
than re-reading it turned up the case it does not cover, and it is the row's own
failure mode.

`work_tip` peels a refresh sitting **literally on the tip**, and it has to: it
is shared with the `reset --hard` in `integrate.refresh`, where peeling one
commit too far destroys committed work — its own docstring says so, from an
earlier round that measured it. `governing_identity` reused that peel. So the
moment anything landed *on top of* a refresh commit, the tip stopped being a
refresh commit, the peel stopped applying, and the identity flipped from the
pre-refresh work tree to the post-refresh one.

The commit that does this in practice is the coordinator's own **telemetry** —
`docs/iteration/`, one of the three `RECORD_PREFIXES` the fold exists to ignore.
It cannot move the identity by itself. It moved it by hiding the refresh:

| state | governing | loop `owed` | gate |
| --- | --- | --- | --- |
| round served, no refresh | `4fff62ba…` | False | merges |
| refresh on the tip (what round 007 tested) | `4fff62ba…` | False | merges |
| **+ one telemetry commit on top** | `f2bca684…` | **True** | **refuses** |

Both readers agree — on the wrong answer. An honest APPROVE is parked at a
supervisor stop by the process writing about itself, which is OI-76 in one
sentence. Round 007's own test lands its refresh last and never commits again,
so it could not see this.
<!-- fig: cmd="scratchpad/drive_peel_depth.py — three states on one two-branch git fixture, pre-fix" rev=863e768e -->

The fix does **not** widen `work_tip`; widening a peel that feeds `reset --hard`
would trade a stale verdict for destroyed work. `governing_rev` is a second,
read-only walk: peel a verified refresh, walk through a record-only commit,
stop at the first work commit. Walking through a record commit cannot change the
answer by itself — the fold drops those paths, so a record commit and its parent
have the same identity by construction — which is why this is not a new rule
about what counts, only what lets the existing rule see past the records.
`_record_only` passes `-z` for the finding-3 reason pointed the other way: a
quoted non-ASCII path would make a WORK commit read as a record one. A merge
commit, an empty commit, and the 64-commit bound all STOP the walk, which
measures at a later rev and so can only ask for more review, never less.

`test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel` pins it with
its opposite (a work commit above the refresh does re-owe, and does refuse), and
was verified to bite: reverting `governing_identity` to `work_tip` fails it on
the identity assertion, `f2bca684…` against the served `4fff62ba…`.

**A figure this session retracted.** Session 010 wrote the round-007 full-suite
line into the archived spec *ahead of the run* and said so plainly in its own
log ("I have not yet done and will not claim until I see it"); the run never
happened before the session ended, and the written number was still sitting
there as uncommitted residue, where nothing distinguishes it from a measured
one. It was retracted, then replaced by the real output:
**3342 passed, 24 skipped, 1 failed in 614.49 s** at `025a0643`, the one
failure being the same trunk-owned `docs/stage` freshness bisected clean at the
base above. The counts the placeholder guessed happened to be right and the
seconds were not; that they were close is not what makes a figure honest.
<!-- fig: cmd="python -m pytest -q -n auto" rev=025a0643 -->

Re-driven after the peel fix, since that is a script change and not a doc one —
full suite at the tip `cee19210`: **3343 passed, 24 skipped, 1 failed in
615.27 s**, the one extra pass being the new regression and the one failure the
same `docs/stage` fingerprint. Smoke at the same tip: 1504 passed / 8 skipped,
29.5 s against the 60 s ceiling. One box is one data point for the seconds.
<!-- fig: cmd="python -m pytest -q -n auto" rev=cee19210 -->
