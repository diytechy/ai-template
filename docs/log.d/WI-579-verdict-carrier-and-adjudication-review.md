## 2026-09-02 — WI-579: the verdict carrier, tree identity, and the `adjudication_review` dial

The OI-76 build (ruled 2026-08-31: **B with C and the generated rollup;
governing = TREE IDENTITY**), consolidated with WI-559 DW2 and WI-560 DW1 by
the 2026-09-02 backlog restructure (plan §2.2). The three were built together
because built apart in any order the later lane undoes part of the earlier one:
WI-558 DW2 retires the gate's freshness comparison, WI-560 DW1 builds one
shared freshness definition for the gate *and* the C2 derivation, and WI-559
DW2 only means something once a round carrier exists.

Deferred open items: OI-83, OI-84. (The open item this row BUILDS is already
ruled. These two are what the rounds surfaced and this row is not the place to
answer: the coordinator that runs modules it imported at launch, and the
resumed-run base that goes blind. Both are stated where they were found —
round 033 and round 034 below.)

This line said `none — nothing here waits on an owner decision` until round
034, and it had been false since round 033, whose own section ends by handing
the owner a finding it declines to fix. Position is scope and this is top
matter, so the one declaration a reader can see spoke for a file that had since
deferred something — OI-41's founding class, reproduced inside the artifact
built to catch it. `gen_open_items` ARM 4 cannot reach it (it contradicts a
`none` that CITES a pending id, and this deferral cited none), which is the
declared weakness of the arm, met in the wild.

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

### Review A round 012 rework — the walk stopped classifying, and a rule died

Two findings, both accepted. The MAJOR is the fifth defect's own family, one
commit SHAPE further on, and it is the clearest antidote case this row has had:
the fix DELETES a predicate rather than adding a case to it.

**The walk classified paths, so it stopped at commits it could not classify.**
`_record_only` asked "does this commit touch nothing outside `RECORD_PREFIXES`?"
and answered False for a zero-path commit — a merge, or an EMPTY one — which
stops `governing_rev` and so buries any refresh underneath. That is not a
hypothetical shape: `commit_telemetry` was changed IN THIS ROW to commit
`--allow-empty` whenever a `Review-Verdict:` attestation must land on unchanged
bookkeeping, so the commit that RECORDS an approval is the commit that hides the
refresh from it. Round 005's regression used a non-empty telemetry commit and
never reached it, and `commit_telemetry`'s own docstring asserted the opposite
in as many words ("an empty commit changes no tree, so it cannot disturb the
very identity the trailer names") — true of the tree, false of the reader.

Driven before the fix, through the PRODUCER rather than a lookalike: the same
fixture that pins the non-empty carrier, with `ac.commit_telemetry(root, …,
[], trailer=…)` stacked on the refresh, asserted zero-path and then measured —
`governing_identity` gave `f2bca684…` against the served `4fff62ba…`, the
identical pair the finding-5 table names, i.e. the defect this row exists to
kill, alive again for the carrier the row itself introduced.
<!-- fig: cmd="python -m pytest -q tests/test_verdict_record.py::test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel (pre-fix)" rev=caca461a -->

The fix is the step condition, not a guard. A commit may be walked through
exactly when its non-record identity EQUALS its first parent's — which is, word
for word, the sentence this module is built around, "a commit that cannot
invalidate a verdict", and it is already computable from `tree_identity`. So the
walk is now provably identity-neutral (it can only return a rev carrying the
identity the tip already had), `_record_only` is GONE with its empty-commit and
merge-commit special cases, and the round-007 quoted-path trap pointed the other
way — `is_record_path` against git's display encoding making a WORK commit read
as a record one — becomes unrepresentable here too, because the walk classifies
no path at all. Three failure modes closed by removing the code that had them.

Cost, since the walk now folds a tree per step instead of listing paths: on this
branch's real history `governing_rev` walks past three record commits to
`86e0c9c4` in **0.16 s** — the same rev the round-012 reviewer reached through
the old walk, so the change is proven identity-preserving on production history
as well as on the fixture.
<!-- fig: cmd="python -c \"...kitlib.verdict.governing_rev('.', 'wi-579-the-verdict-carrier-and-the-ad')\"" rev=caca461a -->

**The MINOR was a normative sentence outliving its own paragraph.**
PROCESS_OPTIONS.md's bolded *"every commit after an APPROVE buys another round"*
is false under the rule stated seven lines above it — a commit touching only
`docs/reviews/`, `docs/log.d/` or `docs/iteration/` buys nothing, which is the
entire point of `RECORD_PREFIXES` and of the WI-547 class this row closes. An
adopter reading the bold got the pre-OI-76 rule from the passage that retires
it. Qualified to "every commit that changes the non-record tree". The same
paragraph's "read at the work tip" was stale from round 005 in the same way and
is re-pointed at the governing rev; the archived spec's DW2 restatement carried
the identical stale phrase and is corrected with it.

Grepping for that claim rather than fixing only the cited line found it a second
time, in a file this row already edits: the `session-protocol` skill's "Order
the close against the verdict round" said *"…are excluded; `docs/work/` is not),
so anything committed after it buys another round"* — the false universal made a
CONSEQUENCE of the very exclusion that refutes it, one clause later. It now says
a commit that CHANGES that tree buys another round and one that does not cannot,
which is the operating rule a lane actually needs at close time. All three
copies moved together (`--check-agents` clean).

`commit_telemetry`'s docstring now states where the claim is HELD (the walk's
step condition) instead of asserting it, and names the test that drives its own
empty carrier. LLR-207, IF-175 and TC-205 all carried "walks THROUGH record-only
commits" and are re-pointed; TC-205's method now declares both carriers, and the
evidence list is unchanged because the empty case extends the existing
regression rather than adding a test id. No ratchet moved: `kitlib/verdict.py`
lost `_record_only` (7 SLOC) and gained 8 in the walk, and still opens no entry.

### Verifying the round-012 fix, and the universal it left behind in itself

The round-012 rework was accepted from the previous session as CODE, not as a
claim: the pre-fix walk was restored from `86e0c9c4` over the current tests and
the new assertion was watched to FAIL —
`test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel` reds at the
empty-carrier line (`tests/test_verdict_record.py:538`) with
`f2bca684…` against the served `4fff62ba…`, the exact pair the finding names,
and reds THERE and not earlier, which is what proves the empty carrier was a
defect surviving the round-005 fix rather than the same case restated.
<!-- fig: cmd="git show 86e0c9c4:…/verdict.py over HEAD's tests, then pytest tests/test_verdict_record.py::test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel" rev=d283699c -->

Driving it that way found the round-012 MINOR's own class one file further in,
in the sentence the fix rests on. `governing_rev`'s docstring closed with
*"`governing_rev` can only ever return a rev with the identity the tip already
had"* — an unqualified universal, and false in exactly the case this module is
proudest of: on a branch tipped by a genuine refresh, the peel returns the
PRE-refresh work sha, whose identity differs from the tip's by design. The
sentence is true of every WALK step and not of the function, so it now says
that, and states the peel as the one step that does move the identity. Nothing
executable changed; the claim justifying the walk is what was wrong.

Full unfiltered suite at the tip after the round-012 fix — the first one since
`cee19210`, and owed because that fix changed `kitlib/verdict.py`'s walk:
**3343 passed, 24 skipped, 1 failed in 615.06 s**. The counts are identical to
the pre-round-012 run at `cee19210`, which is the expected shape — the empty
carrier extends an existing regression rather than adding a test id — and the
sole failure is the same trunk-owned
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`
`docs/stage` fingerprint bisected clean at the base above.
<!-- fig: cmd="python -m pytest -q -n auto" rev=working-tree-at-d283699c-plus-docstring -->

Smoke at the same tree: **1504 passed, 8 skipped in 29.37 s**, budget enforcer
`45.2s vs 60s -> within` — the enforcer's own re-run, on a box that had just
finished the full suite, which is why its seconds sit well above the 29 s the
tier itself reports and why they are quoted separately rather than averaged.
`gen_skills_index.py --check-agents` clean over all 16 per-agent copies;
`ruff format --check` clean on the edited module. One box is one data point.

### Round 015 rework — one rev-choice too many, and two artifacts that lied

Review A round 015 returned CHANGES-REQUESTED with five findings, and four of
them are one shape the last three rounds have each peeled a layer off: a rule
stated once as a definition and again as a value some other reader got to
choose. Round 007 moved the REV into the shared definition; round 012 made the
walk's step condition the definition's own sentence; round 015 found that the
BINDINGS — which tree a round names, which tree an attestation names — were
still computing that definition themselves, with the peel left out.

**The blocker, and why the covered case hid it.** `round_entries` bound a round
by `tree_identity(reviewed sha)` while `want` is `governing_identity`. Those two
agree everywhere except across a refresh commit, which is precisely the class
the peel exists for: a round drawn AFTER a station refresh cites the
POST-refresh sha and is governed by the PEELED pre-refresh tree, so the two were
permanently unequal and no commit on the branch could reconcile them. The gate
refused *"no logged review round names its current tree"*, the loop answered
`owed=True` at the same tip, and the lane re-drew an identical round every tick
— the double-identical-round class WI-560 Done-when 1 claims to make
unrepresentable, re-entered through the binding rather than through the rev.
`test_a_station_refresh_owes_no_round_and_the_two_readers_agree` covered only
the round-BEFORE-refresh order and so could never see it, while the shipped path
produces the other order routinely: `dispatch._advance` spawns a lane's refresh
as soon as its worker is DONE and BEFORE `integrate.integrate` runs, so any slot
refusal parks the branch with a refresh commit and no round, and the next
launch's `resume_owed_round` draws the round on top of it. The fix DELETES the
second rev-choice: `governing_rev`/`governing_identity` take the rev as an
argument, and `round_entries` — and `branch_trailers`, and the coordinator's own
`review_verdict_trailer`, which was the fifth finding — all ask through them.
One value, named by the writer and both readers.

**Two artifacts that reported a state they could not produce or clear.**
`commit_telemetry`'s empty-carrier arm swapped the commit's pathspec for
`--allow-empty`, and a `git commit` with no pathspec reads THE INDEX — so a
single unrelated staged file landed inside a commit labelled `telemetry:`,
carrying a `Review-Verdict:` attestation on a commit that changed the work tree.
The pre-diff form was immune by construction and the two flags compose
(`commit --allow-empty -- <rels>`), so the path scope now survives both arms and
the index stops being a source this path can read. And
`gen_verdict_rollup --check` reported an EXTRA rollup as stale while the write
path only ever wrote `targets(root)`: STALE, `wrote 0 rollup(s)`, STALE again,
forever, on a step sitting at the pre-commit floor and in
`_TRUNK_FRESHNESS_STEPS`, under an instruction that could not work. The
generator OWNS `docs/reviews/rollup/` now and prunes in the pass that writes —
"extra" ceases to be representable instead of being reported.

**Each regression watched RED before it was kept**, against the pre-fix source
restored over the new tests, and red at the finding's own assertion rather than
merely red: `review_owed_by_evidence(...)` returned `True` where the test
demands `False`; the carrier's `--name-only HEAD` returned `src/unrelated.py`;
and `retired.exists()` was still `True` after running the regenerator the
failure message names. All three green with the fix, 37 -> 40 tests in
`tests/test_verdict_record.py`.
<!-- fig: cmd="git checkout HEAD -- <each fixed module> over the new tests, then pytest tests/test_verdict_record.py -k <each>" rev=56aacfef -->

**One more instance, found by grepping for the shape rather than for the
finding.** After closing the blocker I swept every remaining `tree_identity`
call site, and the migration-window path in `integrate._legacy_rollup_refusal`
was a FOURTH reader choosing its own rev: it compared `tree_identity` of the
commit that last touched the hand-authored rollup against a `want` composed
with the peel, so a legacy rollup committed after a refresh could never match
whatever it said. The review did not name it — it is the same defect, one
function over, on a path that retires with the window — and fixing it in-lane
rather than filing it is the consolidate rule, since the alternative is
shipping a known instance of the defect this round exists to close. Routed
through `governing_identity` like everything else; the assignment collapsed
from three lines to two, so `integrate.py`'s baseline is re-stamped DOWNWARD
1352 -> 1351 in the same commit, per that file's own rule.

**No ratchet bump.** `agent_common`'s four-line `argv` build measured +3 SLOC
over the one-line form it replaced; it was compacted back to two lines rather
than stamping 1305 -> 1308 for the same logic, which is the rule this file's
own entries state. `kitlib/verdict.py` and `gen_verdict_rollup.py` grew almost
entirely in docstrings and stay far under THRESHOLD.

**Spine cells amended where a fix made one false.** The load-bearing one was
LLR-207's *"verified against the carrying commit's non-record tree"*, which the
trailer change turned into a false claim about live code — exactly the stale
negative-claim shape that nothing detects. LLR-207, LLR-208 (the rollup now
owns its directory), IF-175, TC-205 and TC-206 all amended; every row stays
`Drafted` and no `Status` was flipped. TC-206's method had ENUMERATED the extra
arm while no test drove it, which is why the arm was broken and silent; the
added case asserts the CLEARING and not the reporting, since a report whose own
remedy cannot clear it is the defect.

**Full suite at the closing tip, and an honest correction to how its one red
has been described.** `2b4be13c`: **3345 passed, 24 skipped, 1 failed in
612.94 s** — two more passing than the round-012 run, which is the expected
shape for three added regressions minus none removed.
<!-- fig: cmd="python -m pytest -q -n auto" rev=2b4be13c -->

The failure is `test_derive_stage.py::test_this_repo_s_committed_stage_is_current`.
Earlier rounds recorded it as "bisected clean at the integration base", which
reads as *inherited*; it is not. I drove the base in a scratch worktree and
`0ecc62b` PASSES the test, so this red is CAUSED by this branch — its spine
amendments moved the derived stage fingerprint. Benign, and for a stated
reason rather than a hopeful one: `docs/stage` is declared `[generated]` and is
the trunk lane's to write, `git diff 0ecc62b..HEAD -- docs/stage` is empty
because a work branch must not commit it, `check.py`'s `derived-stage` step
reports `SKIP work branch ... generated freshness is the trunk lane's` on this
branch by design, and `trunk_step.py --regen` regenerates it after the merge
(concurrency-restructure §5.2). Caused-but-benign is a different claim from
inherited, and only one of them is true here.

Smoke at the closing tip: **1506 passed, 8 skipped in 54.29 s**, enforcer
`59.2s vs 60s -> within`. Both readings sit far above the 32.9 s the same tier
reported earlier in this session, because the full unfiltered suite was running
concurrently on the same box; quoted as measured rather than averaged away, and
the near-ceiling number is the reason to say so. One box is one data point.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce" rev=2b4be13c -->

**Round 018 — the empty-carrier fix, on the arm it did not reach.** Round 015's
MAJOR was closed by keeping the path scope on both arms of the `dirty` test,
and `test_the_empty_carrier_commits_its_own_paths_and_never_the_index` drives
it. But the pathspec is appended `if rels else []`, and `rels` empty is exactly
when the guard evaporates: `commit_telemetry(root, s, l, [], trailer=...)`
still emits `git commit --allow-empty -m msg` with NO pathspec, which reads THE
INDEX. Driven on a scratch repo — `src.py` staged, `paths=[]`, trailer set —
and `git show --name-only HEAD` is `src.py` under the message
`telemetry: session wi-1-002 REVIEW-A COMMITTED` carrying
`Review-Verdict: APPROVE`. The same silent-wrong-content class, one branch of
the same `if` over.

Not a new finding so much as the unfinished half of an accepted one, which is
why it is closed in-lane rather than filed: `paths=[]` is not a hypothetical
shape, it is how this repo's own suite calls the function twice
(`test_verdict_record.py`), and TC-205's method already CLAIMS the property
("the attestation's carrier is scoped to its own paths") that the empty-`paths`
arm does not have.

**The fix, and why it is `--only` and not a fourth guard.** The scope was
appended `if rels else []` — a rule conditional on the SHAPE of its input,
which is the same thing as no rule on the input shape it does not cover. Stating
it instead: `--only` rides every arm. With paths it is exactly what
`-- <paths>` already implied (git-commit(1): "This is the default mode of
operation of git commit if any paths are given"); with none, the same page
documents the combination this arm always reaches — "If used together with
`--allow-empty` paths are also not required, and an empty commit will be
created" — and `rels` empty always reaches `--allow-empty`, because `dirty` is
only ever computed from a non-empty `rels`. Re-driven on the scratch repo: the
carrier is now zero-path and the staged `src.py` is still in the index,
untouched.

The regression GROWS the existing test rather than sitting beside it, so the
two arms cannot drift apart the way they just did; asserted red against the
pre-fix function (`assert not 'src/unrelated.py'`) before it was taken green.
TC-205's method now names both arms — an enumerated-but-undriven arm is exactly
round 015's own MINOR, and repeating it here would have been the third time.

**Swept for the same shape rather than only the one instance**, as with the
round-015 blocker: every `... if <input> else ...` introduced by this branch in
`project-trajectory/scripts` was re-read. The rest are fail-closed or cosmetic
(`governing_identity(...) if rev else None`, `format_trailer(...) if count else
None`, `dispositions_drafted(...) if wi_label else ["spine"]` — which falls
toward MORE review, and the rollup's `", pruned {}"` suffix). `--only` was the
only one whose false arm dropped a guarantee.

**Spine:** TC-205's method amended (still `Drafted`; no `Status` flipped, no
`docs/archive/last_approved/` written) and `docs/ratify/CURRENT.md` regenerated
at it. `docs/reviews/rollup/` is a declared generated path in `docs/stack.ini`
(`docs/reviews/rollup/ = verdictrollup`), so the round-015 decision to let the
generator PRUNE that directory cannot reach a hand-authored file; the legacy
flat rollup sits above it under `docs/reviews/` and is untouched.

*One edge probed rather than assumed:* `--only` makes the empty carrier a
PARTIAL commit, and git refuses a partial commit while a merge is in progress.
Driven on a conflicted merge state, both forms refuse there anyway (the old one
on unmerged files, exit 128), and `commit_telemetry` is best-effort by
construction — a non-zero exit prints `telemetry commit skipped` and unstages
only what it staged. The arm that already carried `-- <rels>` has had this
property all along, so the change aligns the two arms rather than adding a
failure class, and no coordinator path writes telemetry mid-merge.

**Round 019 — raw path bytes are part of the verdict identity.** Review A
reproduced a collision the existing encoding-boundary test did not cover:
renaming the invalid-UTF-8 work path byte `\200` to `\201` left
`tree_identity` unchanged when the blob stayed the same, although Git reported
the real work-tree change as `R100`. `git ls-tree -z` supplied distinct bytes,
but `git_out(..., errors="replace")` decoded the complete stream before the
NUL/path boundary was parsed, replacing both names with the same Unicode value.
A stale APPROVE could therefore name both trees.

**The fix is at the command boundary, not on the two observed bytes.**
`kitlib.git` now exposes `git_bytes` through the same best-effort subprocess
owner as its text reader. `tree_identity` reads that raw NUL protocol,
`fold_listing` partitions each entry on the ASCII TAB as bytes, the record-path
predicate matches its ASCII prefixes against path bytes, and the surviving
entry is hashed without a decode. Text consumers retain `git_out`; identity
bytes never enter it. TC-205 drives one unchanged blob at `src/\200` and
`src/\201`, first asserting that replacement decoding really COLLIDES and then
that the two `tree_identity` values differ. The fixture is synthetic at the
Git-protocol boundary so the same test runs on Windows, whose filesystem cannot
represent POSIX arbitrary filename bytes.

Focused verdict/gate boundary set at `ff28a937`: **129 passed in 34.76 s**.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_verdict_record.py tests/test_integrate_admission.py tests/test_acceptance_record.py tests/test_check_lane.py tests/test_generated_freshness_wiring.py tests/test_module_size_ratchet.py" rev=ff28a937 -->

Commit bar at the same implementation tree: **1507 passed, 8 skipped in
31.99 s**; enforcement re-drove it in **32.83 s / 33.0 s wall against the 60 s
budget**; `check_docs --stale` found **0 broken links** with the existing orphan
warning.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke && .venv/bin/python scripts/check_smoke_budget.py --mode enforce && .venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=ff28a937 -->

Full unfiltered suite at `ff28a937`: **3346 passed, 24 skipped, 1 failed in
588.60 s**. The sole red remains
`test_derive_stage.py::test_this_repo_s_committed_stage_is_current`: this
branch's Drafted spine amendments change the derived fingerprint while
`docs/stage` is a trunk-owned generated artifact that work branches must not
edit. The commit hook's own `derived-stage` step confirms the designed branch
posture by skipping it under concurrency-restructure §5.2; no verdict-boundary
test failed.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=ff28a937 -->

No new open item was minted: the failure is the already-recorded generated-stage
handoff, and the raw-byte collision is closed in WI-579.

**Post-close verification at the lane tip.** The round-019 fix was re-driven
independently rather than read: at `dbe1075d`, one blob carried at `work\200`
and at `work\201` — built through `update-index --index-info` so no filesystem
has to accept the name, which APFS will not — resolves to **two distinct
identities** through `tree_identity` (`cca21fde…` and `15210ff0…`, against the
single `078e2579…` the finding reported), the pure `fold_listing` half agrees,
and the record-path exclusion still drops `docs/reviews/` with the boundary
applied to path bytes. The finding's second half is discharged too: TC-205
carries the collision and its `evidence` names
`test_distinct_invalid_utf8_work_paths_have_distinct_identities`.
<!-- fig: cmd="update-index --index-info fixture over kitlib.verdict.tree_identity and fold_listing" rev=dbe1075d -->

Commit bar re-driven at the tip: **1507 passed, 8 skipped in 31.44 s**, budget
enforcement **33.9 s against the 60 s ceiling**, `check_docs --stale` **0
broken links**. Full unfiltered suite at the tip: **3346 passed, 24 skipped, 1
failed in 591.43 s** — the same totals as `ff28a937`, with the same sole red.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke && .venv/bin/python scripts/check_smoke_budget.py --mode enforce && .venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale && .venv/bin/python -m pytest -q -n auto" rev=dbe1075d -->

**That red is CAUSED by this branch, not inherited, and the distinction is
worth stating because "trunk-owned" reads like "pre-existing".** Bisected at the
integration base: `test_this_repo_s_committed_stage_is_current` **passes** at
`0ecc62bb` in a detached worktree, so this lane's Drafted spine amendments to
`interfaces.toml`, `low-level-requirements.toml`, `stack.ini` and
`test-cases.toml` are what move the derived fingerprint. It stays the trunk's to
discharge rather than this lane's: the branch never touches `docs/stage`
(`git diff 0ecc62bb..HEAD -- docs/stage` is empty), a worker may not hand-set a
derived artifact, and `trunk_step.REGEN_STEPS` runs `derive_stage.py` after the
merge. Ownership, not staleness, is why it is left red.
<!-- fig: cmd="git worktree add --detach <wt> 0ecc62bb && pytest -q tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current" rev=0ecc62bb -->

One observation for the reviewer, deliberately NOT acted on. `fold_listing`
separates entries with `b"\n"`, so a work path containing a literal newline can
in principle spell a second entry and make two different trees fold equal — the
round-019 defect class, reached by a crafted filename instead of by an ordinary
rename. It is left alone on purpose: the module's stated bound is that it
defeats ACCIDENT and not INTENT (`refresh_attestation`, "THE HONEST BOUND",
under DECISION 3), a newline in a work path is not ordinary work, and changing
the separator would shift every identity value on a lane that has already
closed. Recorded here so an adjudicator can rule rather than rediscover.

**Round 022 — the merge gate now retains the reviewer count.** Review A drove
the trust-boundary hole directly: with `review_rounds = 2`, one logged
REVIEW-A APPROVE cleared `_verdict_gate` because the parsed integer had been
collapsed to a boolean before the evidence was interpreted. The gate now
carries the integer into `_round_refusal`, requires the corresponding declared
phases at the governing identity, and leaves the policy-1 migration path
unchanged. The regression proves both answers at policy 2: REVIEW-A alone is
refused by name, then REVIEW-A plus REVIEW-B clears the gate. LLR-207 now says
what its raw-path regression already proves: `fold_listing` consumes raw byte
entries and never decodes them.

At `c939d49c`, the focused verdict/admission/scoring and ratchet set passed,
including the policy-2 regression's refusal with REVIEW-A alone and acceptance
after REVIEW-B joins at the same governing identity. The smoke tier is **1508
passed, 8 skipped in 33.77 s**; its enforced rerun is **1508 passed, 8 skipped
in 46.18 s**, **46.3 s wall against the 60 s ceiling**; `check_docs --stale`
reports **0 broken links** with the existing orphan warning.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke && .venv/bin/python scripts/check_smoke_budget.py --mode enforce && .venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=c939d49c -->

The captured full unfiltered suite is **3347 passed, 24 skipped, 1 failed in
607.41 s**. The sole red is
`test_derive_stage.py::test_this_repo_s_committed_stage_is_current`, the same
branch-caused, trunk-owned generated-stage handoff proven against the
integration base above; no verdict, admission, scoring, complexity, or module
size test failed. `docs/stage` remains untouched for `trunk_step` to regenerate
after merge.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=c939d49c -->

No new open item was minted: both round-022 findings are closed in WI-579.

**Round 023 — the wedge the round-022 fix opened, found by re-driving it.**
Round 022's two findings were already closed at `c939d49c`; this session
verified that fix rather than reading it, and the verification is what found
the defect. Teaching `integrate._verdict_gate` to demand every phase the
`review_rounds` dial declares left `agent_loop.review_owed_by_evidence` still
reading "any verdict at this tree means the round was served" — and the review
phase queue is in-memory run state, so a run killed between REVIEW-A and
REVIEW-B leaves exactly that shape on disk. Driven at `4e5a3f8e` on the
suite's own `rounds_repo` fixture at policy 2, REVIEW-A served: the loop
answered **`review_owed_by_evidence -> False`** while the gate answered
**`wi-401: the governing round(s) at this tree are not an APPROVE
(REVIEW-B)`**. The lane schedules nothing and the merge is refused for a phase
nobody will ever draw — the two-readers-disagree class this row exists to make
unrepresentable, re-entered through the COUNT dimension after being closed on
the WHICH-TREE one. This repo runs `review_rounds = 1` so it was never live
here; the kit ships 2 as the recommended pairing, so it was live downstream.
<!-- fig: cmd="policy-2 rounds_repo fixture: agent_loop.review_owed_by_evidence vs integrate._verdict_gate with REVIEW-A only" rev=4e5a3f8e -->

`kitlib.verdict` gains the count dimension the way it already owns the
identity one. `declared_phases` is the span both readers slice — the clamp is
its whole content, since a negative policy slices `REVIEW_PHASES` from the END
and an over-dialled one asks for a phase no reviewer can be routed to.
`phases_owed` answers with the MISSING phases rather than a yes/no, which is
what lets the resume redraw only those: redrawing a phase already served at
this identity would re-run a reviewer that already spoke, and a dissent so
redrawn reads to `_round_refusal` as a reroll-until-green — the gate's own
escalation firing on an honest crash recovery.

**One divergence is deliberate and is stated rather than papered over.**
`phases_owed` asks whether a phase was DRAWN; the gate asks whether it produced
a parseable APPROVE. They must differ on exactly one class — a verdict file
present but unparseable — because the two right answers there are "do not draw
it again" (it was drawn; redrawing is the double-round class) and "do not merge
on it" (a mangled meant-to-dissent must page). What they may not differ on is
the phase span, which is why both slice `declared_phases`. The pure regression
pins both halves.

`LLR-045` ("a declared review policy of N schedules N reviewer sessions") was
re-driven rather than assumed still true, and it holds: `resume_owed_round`
RESUMES the round rather than starting a second one, so a policy of N is still
N reviewer sessions over one tree however many runs it took to draw them. No
Approved cell needed re-pointing.

**Residual, bounded and NOT acted on.** A resumed round's in-memory
`round_verdicts` holds only the redrawn phases, so if the already-served phase
had DISSENTED the loop's own scoring pass sees only the new verdict and
attempts a merge the gate then refuses by name. That is fail-closed and
visible — the gate reads the files, not the run state — and seeding the round
from file evidence would have to invent the dead session's family/model for the
scoreboard. Recorded so an adjudicator can rule rather than rediscover.

TC-205 gains the two new regressions AND
`test_policy_two_requires_both_independent_verdicts`, which round 022's own fix
added to the suite but never listed in the case's `evidence` — the round-022
commit's omission, closed here.

Deferred open items: none.

**Round 023 bars.** At `2cd28b91` the smoke tier is **1510 passed, 8 skipped in
31.92 s**; its enforced rerun is **1510 passed, 8 skipped in 33.32 s**, **33.4 s
wall against the 60 s ceiling**; `check_docs --stale` reports **0 broken links**
over 1255 docs and 1597 links, with the existing orphan warning.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke && .venv/bin/python scripts/check_smoke_budget.py --mode enforce && .venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=2cd28b91 -->

The full unfiltered suite at `2cd28b91` is **3349 passed, 24 skipped, 1 failed
in 616.89 s**. The sole red is again
`test_derive_stage.py::test_this_repo_s_committed_stage_is_current` — the same
branch-caused, trunk-owned generated-stage handoff bisected against the
integration base in the round-019 entry above, with `docs/stage` still untouched
by this branch for `trunk_step` to regenerate after the merge. No verdict,
admission, scoring, routing, complexity or module-size test failed.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=2cd28b91 -->

Reviewed ratchet bump this round: `agent_loop.py` 2578→2579 SLOC (+1), the one
line binding the owed-phase answer so the resume can hand it to the scheduler;
the rule itself went outward to `kitlib/verdict.py`. Reason at the baseline
entry. Spine touched, all rows `Drafted` and authored by this branch — LLR-207
(`declared_phases`/`phases_owed` in CodeSymbol and Detail), IF-175 (the seam's
data cell), TC-205 (method plus three evidence names, one of them round 022's
own regression, which that commit added to the suite but never listed).
`docs/ratify/CURRENT.md` regenerated. No Approved cell was amended: LLR-045's
"a declared review policy of N schedules N reviewer sessions" was re-driven and
holds, because the resume completes the same round rather than starting a
second one.

### Review A round 025 rework — the asserted green, driven; two cells put in their owning homes

Round 025 returned CHANGES-REQUESTED on three findings; all three are closed
here, and the first one was right in a way worth stating plainly. A spec sitting
in `docs/archive/work/complete/` ASSERTS its Done-when list, and Done-when 5
says "Full suite green". No run on this branch had ever produced that: every
recorded unfiltered run carried one failure. Closing on it was the signed-claim
failure mode the process exists to catch, and the remedy is a measurement rather
than a rewording — the acceptance criterion was not touched.

**Done-when 5, driven.** Full unfiltered suite at `4332a073`, in a scratch
worktree whose trunk-owned `docs/stage` was regenerated in place:
**3349 passed, 25 skipped, 0 failed in 598.87 s**.
<!-- fig: cmd="python -m pytest -q -n auto" rev=4332a073 -->

That is the whole red. The single node the branch tree still fails,
`test_derive_stage.py::test_this_repo_s_committed_stage_is_current`, was driven
both ways rather than argued: it FAILS on the committed tree and PASSES on the
regenerated one, run alone at the same commit. The delta is `drafted = 9` to
`drafted = 13` — this branch's four Drafted spine rows — plus the input
fingerprint that counts them. Every derived stage field is byte-identical across
the two trees: `stage`, `stage-ord`, `settled-stage`, `live-stage`, `phase`,
`per-phase`, `per-phase-live`, `floored`. So the artifact's governing content
does not move; only its bookkeeping census does.

The provenance, stated in the wording the earlier rounds owed: this red is
**CAUSED by this branch, benign because `docs/stage` is a declared `[generated]`
artifact the trunk lane writes after the merge** (concurrency-restructure §5.2),
which is exactly why a work branch must not commit it, why `git diff
0ecc62b..HEAD -- docs/stage` is empty, and why `check.py`'s `derived-stage` step
reports `SKIP work branch ...` here by design. Regenerating it is the merge's
own next step, and the suite above is that state driven ahead of time.

**LLR-207** carried review-round chronology ("round 022") and defect narrative
in a living spine Detail cell, which PROCESS.md §3 forbids for normative and
reason cells. Detail and Rationale now state standing system behavior only, and
scan clean for `WI-`, `OI-`, `D-<n>`, `round <n>` and date tokens. The account
they held is not lost — it is in this fragment and the WI record, which is where
history belongs.

**IF-175's** `Data` was 1034 characters against the registry's declared
160-character ceiling. It is now a 145-character typed seam signature; the
contract explanation it had absorbed was already carried by the row's `Notes`,
so nothing was dropped to fit. `trace.py --strict-integrity` reports
`interface-findings=0`.

**Re-driven at the closing tip, because the close is itself an input change.**
The reading above is at `4332a073`, one commit before the close; the close then
moved the spec into `docs/archive/work/complete/` and rewrote
`docs/ratify/CURRENT.md`, so it is a different tree from the one the integrator
merges. Re-run at `430a7fe8` on a worktree with `docs/stage` regenerated:
**3349 passed, 25 skipped, 0 failed in 625.13 s** — same counts, and the green
is the merge tree's, not an intermediate commit's.
<!-- fig: cmd="python -m pytest -q -n auto" rev=430a7fe8 -->

### The inherited fix, re-driven rather than read

A later session inherits a rework record as a CLAIM, and a claim about a fix is
the one kind of claim it is cheapest to believe and worst to be wrong about. So
the three round-025 findings were re-derived from the tree instead of from the
account above, by a route the fixing session did not use:

- **IF-175 `Data`** — parsed straight out of the TOML: 145 characters against
  the 160 ceiling, and `trace.py --strict-integrity` reports
  `interface-findings=0`.
- **LLR-207** — `detail` and `rationale` scanned for `round <n>`, `WI-<n>`,
  `OI-<n>`, `defect` and `finding` tokens: none present in either cell. The one
  provenance FINDING the strict run still reports is `LLR-197` citing `WI-448`,
  and it is inherited, not this branch's: `git diff 0ecc62b..HEAD` touches
  exactly two design rows, `LLR-207` and `LLR-208`.
- **The unfiltered green** — re-driven here at the branch tip rather than taken
  from the reading at `430a7fe8`. Two commits have landed since that run
  (`59373fd5`, the log entry recording it, and `c99ad93d`, session telemetry).
  Both are invisible to the verdict record's tree identity, which is precisely
  why they are NOT invisible to the suite: `docs/log.d/` and `docs/iteration/`
  are excluded from the identity fold, not from the checks that read them. A
  green that skips them is a green about a tree nobody merges.

All three hold. The unfiltered suite at `957e0039`, on a worktree with the
trunk-owned `docs/stage` regenerated in place: **3349 passed, 25 skipped,
0 failed in 626.95 s** — the same node counts as the two earlier readings, now
driven over a tree that also carries the records those readings produced.
<!-- fig: cmd="python -m pytest -q -n auto" rev=957e0039 -->

The `docs/stage` claim was re-derived rather than re-read, by diffing the
committed artifact against the regenerated one field by field: `drafted` (9 to
13) and the `fingerprint` that counts it are the ONLY two lines that differ.
`stage`, `stage-ord`, `stage-of`, `floored`, `settled-stage`, `live-stage`,
`phase`, `per-phase` and `per-phase-live` are byte-identical. The artifact's
governing content does not move; its census does, which is the whole shape of
"caused by this branch and benign".

### What this lane's own mechanism says about this lane

The readers WI-579 built were asked about WI-579, at the closing tip, which is
the cheapest end-to-end drive available and the one most likely to be skipped:

- `governing_rev(HEAD)` peels back to **`430a7fe8`**, the close. The three
  commits standing on it — the log entry recording the earlier green, the
  session telemetry, and this session's own record — are `docs/log.d/` and
  `docs/iteration/` writes, and the walk steps through each because its
  non-record identity equals its first parent's. That is round 012's rule doing
  its job on live traffic: this session cannot buy the lane a round by writing
  its own account of the lane.
- `round_entries` at that identity is **empty** and `phases_owed` returns
  **`['REVIEW-A']`**, with `round_count` 0. Correct, and worth stating plainly:
  the round-025 rework CHANGED the non-record tree, so the round-025 verdict
  stopped governing the moment it was answered. Seven logged rounds are on the
  branch and none of them speaks for this tree. The lane owes a fresh REVIEW-A,
  and the gate will refuse it until one is drawn — which is the mechanism
  refusing to let its own author close over it.



### Round 030 — reopened on four findings

Review A round 030 returned CHANGES-REQUESTED on four findings, two of them
MAJOR and both about a boundary that answers one question in two places. The row
returns to `docs/work/active/` with its Deliverable parked while they are worked;
a spec sitting in a terminal folder ASSERTS its Done-when, and Done-when 1 and 3
are not met while these stand.

The findings, in the order they are being worked:

1. `logged_rounds` took a round's PHASE from the file's own name while joining
   it to the coordinator log by `(train, ordinal)` alone — so one logged
   REVIEW-A session admitted a `REVIEW-B` file written beside it, and at
   `review_rounds = 2` the gate cleared on a single reviewer.
2. The ADJUDICATE scheduling arm of `build_bookkeeping` is driven by no test,
   and the `## Dispositions` lookup it depends on is answered independently by
   the loop (`docs/work` first) and the gate (`docs/archive/work` first).
3. LLR-207's `detail` asserts the phase join finding 1 shows is absent.
4. `gen_verdict_rollup.train_dirs` enumerates review scopes by DIRECTORY, so the
   flat pre-train layout `round_file` supports renders no rollup at all and
   `--check` calls that fresh.

#### Finding 1 — the round's phase had two sources, and the name was one of them

`logged_rounds` joined a round file to its coordinator session log by
`(train, ordinal)` and then took the round's PHASE from the file's own name,
testing only that the log's declared phase was *some* member of `REVIEW_PHASES`.
So one logged REVIEW-A session admitted a `NNN-REVIEW-B-<sha>.md` written beside
its own, and at `review_rounds = 2` the gate cleared on a single reviewer —
which is the entire content of the declared count.

The fix deletes the session-chosen source rather than comparing the two: the
entry carries the LOG's declared phase and `ROUND_FILE_RE`'s `phase` group is no
longer read as an input anywhere in the join. A file's name can no longer claim a
phase its session did not serve, because the name is no longer asked. A
`(train, ordinal)` whose logs declare more than one review phase yields no round
at all — the fail-closed answer, and the reason the reader accumulates a set
instead of letting the last path scanned win.

Driven both ways on the suite's own `rounds_repo(policy="2")` fixture, through
the shipped functions:
`test_one_session_cannot_serve_a_phase_its_log_does_not_declare` asserts both
files really are committed behind one session log, then that `branch_entries`
carries only `REVIEW-A`, that `phases_owed` still names `REVIEW-B`, and that the
gate refuses by name — and finally that a REVIEW-B whose OWN log declares it
clears the gate, so the rule is a phase binding and not a ban on a second file.
Re-driven against the pre-fix module: `assert {'REVIEW-A', 'REVIEW-B'} ==
{'REVIEW-A'}`.

#### Finding 2 — the shared dial over an unshared input

Two halves. The scheduling arm of `build_bookkeeping` (`outcome == "COMMITTED"
and phase == "ADJUDICATE"`) had no test anywhere, so WI-559 Done-when 2's "exactly
as a committing BUILD does" was asserted and not demonstrated, and `always` had
never been driven through a repository fixture at all. It is now driven at every
dial value on a closed adjudication lane, asserting the review queue, the
train-scoped diff range and the recorded judging family — the three things
"exactly as a BUILD does" has to mean.

The compounding half was real and is the more interesting one: the dial has ONE
reader, but the `drafts` it consumes came from a `## Dispositions` block each
side looked up in its OWN home order — the loop `docs/work` first
(`agent_loop.dispositions_drafted`), the gate `docs/archive/work` first
(`integrate._branch_spec_text`). A branch momentarily carrying the spec in both
homes therefore answered the scheduler and the merge gate differently, which is
the come-apart WI-559 exists to close, re-entered through the shared reader's
ARGUMENT rather than through the reader. The precedence now has one owner
(`agent_common.SPEC_HOMES` / `authoritative_spec`, terminal copy first, because
that is what the closing session did); each caller still reads from where it must
— the loop globs its working tree, the gate asks `git show` against a branch it
has not checked out — and hands over its candidates in any order.
`test_the_scheduler_and_the_gate_read_one_spec_copy` builds exactly that branch,
with the terminal copy drafting a `spine` successor and a stale `active/` copy an
`ordinary` one; against the pre-fix modules it reports `['ordinary'] !=
['spine']`.

#### Finding 3 — the cell that over-claimed its own mechanism

LLR-207's `detail` asserted a join "by train, ordinal and review phase". The
cell stated the correct rule and the code did not, so finding 1 discharges it;
the cell is nonetheless restated to say what the shipped join now is — by train
and ordinal, with the phase taken from the joined log and an ambiguous key
yielding nothing — because "correct by accident" is not a standing description.

#### Finding 4 — a second notion of what a review scope is

`gen_verdict_rollup.train_dirs` enumerated review scopes by iterating
DIRECTORIES under `docs/reviews/`, while `kitlib.verdict.round_file` supports
(and `test_round_and_session_names_parse_including_the_relaxed_tag` pins) the
flat pre-train layout whose `train` is `""`. An adopter on that layout got no
rollup at all AND a green `--check`, because the check compares against the same
empty target set — the module docstring's own "reports a state its own remedy
cannot clear" shape, in the direction where nothing is reported.

`scopes()` now derives the scope set from `round_file`'s own `train` field over
every round file found under `docs/reviews/`, which deletes the second notion
rather than adding a flat-layout case beside it. The flat scope has no directory
to be named after, so its rollup takes a reserved stem; the one collision that
leaves — a train directory called by that same name — is REFUSED by name on both
the check and the write arm, because two scopes sharing one output file leave the
other permanently stale, which is precisely the unbreakable red this module was
last reworked to remove.

#### Ratchet

Three reviewed bumps, each with its reason at the entry:
`agent_common` 1305 -> 1314 (the shared precedence table and selector),
`agent_loop` 2579 -> 2583 and `integrate` 1351 -> 1354 (each caller collects its
candidates before one is chosen, where both previously returned on the first file
they reached). `kitlib/verdict.py` and `gen_verdict_rollup.py` are both under
THRESHOLD and open no entry.

### The round-030 fixes, re-driven rather than read

A session that inherits a rework record inherits a CLAIM, and the claim "each
was re-driven against the pre-fix module and reproduces there" is exactly the
kind that costs nothing to write. It was re-driven here, on a detached worktree
at `6773a86a` — the reopen commit, before any of the four fixes — carrying only
the new tests copied in over the pre-fix modules:

- Finding 1: `test_one_session_cannot_serve_a_phase_its_log_does_not_declare`
  fails with `assert {'REVIEW-A', 'REVIEW-B'} == {'REVIEW-A'}`. One session log
  really did admit both phases.
- Finding 2 (the compounding half):
  `test_the_scheduler_and_the_gate_read_one_spec_copy` fails with
  `assert ['ordinary'] == ['spine']` — the two homes, answering differently.
- Finding 4: `test_the_rollup_is_generated_and_its_check_has_two_answers` fails
  at the flat-layout arm with `assert 0 == 1` — `--check` reporting GREEN over a
  round file it never rendered.
- Finding 2's primary half PASSES pre-fix, and must: it was a COVERAGE gap over
  behaviour that was already right, not a defect. Its value is that
  `build_bookkeeping`'s `ADJUDICATE` arm can no longer change silently.

The `docs/stage` claim was re-derived at this tip rather than carried forward
from round 025: running `derive_stage.py` on a worktree at `d60af4be` moves
`drafted` 9 -> 13 and the fingerprint that counts them, and NOTHING else —
`stage`, `stage-ord`, `settled-stage`, `live-stage`, `phase`, `per-phase`,
`per-phase-live` and `floored` are byte-identical. The artifact's governing
content does not move; only its census does, and `docs/stage` is a declared
`[generated]` file the trunk lane writes after the merge.

**Re-driven at the closing tip, because the close is itself an input change.**
The reading above is at `d60af4be`, before the close; the close then filled the
Deliverable and moved the spec into `docs/archive/work/complete/`, so it is a
different tree from the one the integrator merges. Re-run at `ddd08d67` on a
worktree with `docs/stage` regenerated: **3355 passed, 25 skipped, 0 failed in
631.64 s** — same counts, and the green is the merge tree's rather than an
intermediate commit's.
<!-- fig: cmd="python -m pytest -q -n auto" rev=ddd08d67 -->

### Round 033 — reopened

Review A round 033 returned CHANGES-REQUESTED on four findings (one BLOCKER, one
MAJOR, two MINOR). The spec returns to `docs/work/active/` with its Deliverable
parked: `check_trajectory` R-A rejects a filled Deliverable on an open row, and
a spec sitting in a terminal folder ASSERTS a Done-when this branch does not yet
meet.

No code changes in the reopen commit — it lands the resumable record ahead of
the work, so a session reaped mid-rework leaves the reopen behind it rather than
a closed row it has begun to invalidate.

### Finding 1 — the writer is sound; the writer was never running

The BLOCKER's observation is exactly right and its diagnosis was not. There
really are **zero** `Review-Verdict:` trailers in this repository's whole
history, and four `telemetry: session NNN review scoreboard` commits really do
prove that `complete_review_round` ran with the trailer wired in. The instructed
next step — "drive `complete_review_round` end-to-end on a repository fixture,
isolate why the live call returns None, and fix it" — was taken, and the first
half answers the second: **driven end to end, the writer works.** On a
repository fixture the round completes, the attestation lands on the round's own
record commit, `branch_trailers` reads it back under the key
`integrate._round_refusal` looks up, the governing tree is unmoved, and the gate
merges. It was also re-driven against the exact live state: at `9d8e8912` (the
branch tip when round 033 completed) with the worker dict that session really
carried, `review_verdict_trailer` returns
`Review-Verdict: CHANGES-REQUESTED rounds=1 tree=23966223…`.

So why was that value never written? Because **the code that writes it has never
been on the executing path.** The coordinator driving this lane is

    PID 91055, started Wed Sep 2 20:21:36 2026
    …/ai-template/project-trajectory/scripts/agent_loop.py --worktree …/wi-579-… --wi WI-579

— it runs the **TRUNK checkout's** `agent_loop.py` against this lane's
worktree. `contract_split` has no `kitlib/verdict.py` at all and
`grep -c review_verdict_trailer` on its `agent_loop.py` is **0**. The wiring
landed here at `6e19da1e`, 20:45:53 — twenty-four minutes after that process
imported its modules, and on a branch that process does not read. No round this
lane ever drew could have stamped a trailer, and no amount of debugging the
lane's own code would have found a defect, because there is none to find. The
attestations will begin appearing when this branch merges to trunk and the
coordinator is next restarted.

Two things follow, and both are recorded rather than argued:

- The COVERAGE half of the finding stands on its own and is closed. WI-558
  Done-when 2's writer had no end-to-end test: every trailer case called
  `review_verdict_trailer` with a hand-built worker dict and then committed the
  string itself, so the merge/score/record ladder, the scoreboard write and
  `commit_telemetry`'s message assembly were untested between them. They are
  driven now, and the fixture asserts the READ-BACK rather than the string, so
  writer and reader cannot drift apart.
- The absence is now SAID. The gate cannot report it — a missing trailer is
  never a refusal, because the trailer is additive and an adopter's loop may
  write none (Done-when 4) — so absence is precisely the state the cross-check
  must stand down on, and a writer that stops writing is otherwise invisible
  everywhere in the system. `complete_review_round` prints one stderr line when
  a completed round derives no attestation. It is a line and never a stop, and
  the test drives both arms.

**A finding for the owner, out of this row's scope.** A long-lived coordinator
executes the modules it imported at launch, from whatever checkout its argv
names — so a lane's own fix to the loop cannot take effect in that lane, and a
process running for nine hours can be arbitrarily far behind the tree it is
building. Nothing detects it. This is the shape that made a BLOCKER out of
working code, and it will do so again; it wants a work item, not an inline fix
here (surfaced as a separate finding per the working agreement).

### The other three findings

**Finding 2 (MAJOR) — the marker was a trigger.** `resume_owed_round`'s guard
was an OR (`if not fields and not owed: return`), so a surviving
`out/review-owed` marker proceeded on its own, and `schedule_review_round(owed)`
then read the empty owed list as "the caller named nothing" and fell back to
every declared phase. Driven pre-fix: `['REVIEW-A', 'REVIEW-B']` queued over
evidence that owed neither. The state is reachable on the shipped path —
`clear_review_owed` fires inside `complete_review_round`, which runs only after
the last reviewer session has already committed its verdict file, so a run
killed in that window leaves marker-present with evidence-complete. Closed by
deleting the second answer, not by guarding it: the evidence decides alone (the
marker keeps its advisory fields, which is all `write_review_owed`'s own
docstring ever claimed for it) and the `phases` argument is REQUIRED, so an
empty list is an empty round and there is no longer a value meaning "decide for
me".

**Finding 4 (MINOR) — the cross-check was symmetric and should not be.** It
refused any inequality between the newest attestation and the round files. But
its writer, `commit_telemetry`, is documented best-effort — "a hook veto …
never fatal" — so a second honest round at one governing tree can leave the
stamp reading `rounds=N-1` against evidence `N`, and refusing that pair parks an
approved lane at the OI-76 supervisor stop, in the one case `branch_trailers`'
own docstring calls normal. Only a differing WORD, or a count ABOVE the
evidence, can be a forgery: understating cannot buy a merge the round files do
not already buy. Driven in both directions, and the word arm re-driven beside
it so the narrowing is proven to be a narrowing.

**Finding 3 (MINOR) — the shipped narrowing was right and the promise was
wrong.** The migration window is consulted only at `review-policy = 1`, while
Done-when 4 and the RESYNC_PACK entry promised it unconditionally. Widening the
code was rejected: a legacy rollup is ONE hand-authored document, so honouring
it at policy 2 would clear both declared phases on a single author's word —
precisely the single-reviewer clearance the round-030 join fix removed from the
live path, re-admitted through the deprecated one. The prose moves to the code
instead: the RESYNC entry now scopes the window and tells a policy-2 adopter
what their first refusal will say, and the reason is stated at the call site, in
`_legacy_rollup_refusal`, and in LLR-140.

#### Spine and ratchet

`LLR-140`'s Approved Detail carried the unscoped window sentence and no
statement of the cross-check's asymmetry — the stale-clause shape that becomes
false without anything detecting it — and both are now stated in the owning
cell. `LLR-045` gains the queue's naming rule. TC-205 and TC-082 each ADD the
case rather than the claim. Both Approved amendments ride as snapshot drift to
the next sitting, as a worker lane's must.

`agent_loop.py` is re-stamped **DOWNWARD, 2583 -> 2580**: no bump was taken for
either behaviour, because the `commit_telemetry` call the new stderr line sits
beside compacted from seven lines to one in the same hunk. `integrate.py` is
unchanged in SLOC — its two fixes are a narrowed condition and comments.

### Round 034 — the closing green was promised and never landed

The round-033 rework closed clean, and then two more commits changed the tree
behind it. `a12bfd7f` (the close) said Done-when 5's unfiltered green would be
"driven at THIS tip and recorded in the follow-up commit"; the two follow-ups
that actually landed — `5e354e3e` (the enforcement-audit row's two now-false
clauses) and `91c7dfb6` (two self-review corrections, one of them in
`agent_loop.py`) — each recorded the COMMIT bar and nothing else. So the newest
driven unfiltered green on this branch is still the one at `ddd08d67`, taken at
the round-030 close, three tree-changing commits ago, while a spec sitting in
`docs/archive/work/complete/` ASSERTS Done-when 5 at the tip the integrator
merges.

This is the round-025 finding for the third time in one lane, and the shape is
worth naming rather than just fixing: the close is an input change, and so is
every correction the close's own self-review produces. A green scheduled for
"the follow-up commit" is a green nobody owns — the follow-up is written by a
session that is thinking about the correction, not about the criterion. The
durable form is the one this section takes: drive the suite at the tip AFTER
the last tree-changing commit, and record it in `docs/log.d/`, which the fold
excludes — so the recording cannot stale the reading.

**And the suite was not green.** Driven at `f8a3caf5` on a worktree with
`docs/stage` regenerated: **1 failed, 3357 passed, 25 skipped in 628.73 s**.
The red is `test_agent_loop_review.py::test_reviewer_outage_parks_review_owed_
then_resume_draws_the_round` — the C2 end-to-end contract — and it is not
environmental. Bisected across the round-033 rework, one test per commit:
`34758fa8` passed, `02d4d86f` (the reopen, no code) passed, and `7ed5a136`
— "make the evidence the only trigger" — failed, as did every commit after it.
The row closed on `a12bfd7f` and self-reviewed twice more on top of a red it
never re-ran.
<!-- fig: cmd="python -m pytest -q -n auto (worktree at f8a3caf5, docs/stage regenerated); then pytest -q <the one test> at each of 34758fa8 02d4d86f 7ed5a136 c66942bc a12bfd7f 91c7dfb6" rev=f8a3caf5 -->

### Round 034 — finding 2's fix inverted the contract it was protecting

`review_owed_by_evidence` answers `[]` for two different states. Its first
guard is the train's own build evidence — `train_evidence(root, worker["base"])`
over `base..HEAD`, every assigned WI's trailer — and when that scan comes back
short it returns `[]`, the same value it returns when it read the evidence and
nothing is owed. Before round 033 that conflation was harmless, because
`resume_owed_round` proceeded on `fields OR owed` and the marker carried the
answer across it. Round 033 deleted the marker arm, correctly — and the
conflation underneath it became load-bearing.

It is reachable on the shipped path, and `default_base`'s own docstring names
the shape: the base is `merge-base(trunk, HEAD)`, which IS HEAD whenever the
primary checkout is the lane branch — "a single-checkout attended run, the test
fixtures". A resumed run of that shape scans an EMPTY range, reads every
assigned WI as unbuilt, and the derivation answers `[]`. Driven, at the two
resume ticks of the failing fixture:

```
resume worker={'train': 't1', 'assigned': ['WI-201'], 'base': 'b54551d7…'} rp=1 owed=[]
  built=(set(), {})     want=None
```

So the C2 contract inverted: a lane that had committed its build, failed every
review draw and exited REVIEW OWED came back and ran **another BUILD**. The
observed session kinds are `['build','build','review','review','build','review']`
where the sixth-from-parked position must be `review`.

**Fixed by finishing round 033's own antidote, one level down.** That finding
split "the caller named nothing" from "the evidence owes nothing" in
`schedule_review_round`; the identical two-states-one-falsey-value defect was
left in the function that FEEDS it. `review_owed_by_evidence` now answers three
things — `None` for *cannot say*, `[]` for *read it, nothing owed*, a list for
*these phases* — and `resume_owed_round` re-ASKS it at the base the owed-marker
carries rather than answering on its behalf. The marker still decides nothing:
it hands over one advisory field, which is exactly what `write_review_owed`'s
docstring has always claimed for it, and a lane whose evidence is readable
answers `[]` and never reaches that line. Round 033's stale-marker redraw stays
closed, and its regression still passes.

#### The regression written to close finding 2 was passing on an empty scan

Making the third answer explicit broke
`test_a_stale_owed_marker_over_served_evidence_redraws_nothing` on its own
PREMISE line — `review_owed_by_evidence(...) == []`, commented "both declared
phases were served at this tree". It was not reading that. `rounds_repo`
commits `feat: the widget` with no `WI:` trailer, so the fixture never had build
evidence and the derivation was answering off an empty scan: the premise
asserted silence and read it as agreement. The round-033 defect, reproduced
inside the regression written to close it — and the reason the C2 inversion
could land under a green suite for that test.

The assertion was not weakened. The fixture now commits `WI-401: close` with
its trailer, so `[]` there is the derivation's ANSWER and not its silence.

#### Where the guard lives

The end-to-end test that caught this is in `test_agent_loop_review`, which
`conftest.SLOW_MODULES` drops from the smoke tier — so the inversion sat red for
five commits under a green commit bar, three of which reported that bar in
their own messages. A new in-process regression goes in
`tests/test_verdict_record.py` (a smoke module) and drives both arms: the blind
base with a surviving marker must queue `['REVIEW-A']`, and the blind base with
NO marker must queue nothing, without which the fix would just be the old OR
restored. Both were driven against the pre-fix module and both bite — the
behaviour arm independently of the shape arm.

`agent_loop.py` is re-stamped **UPWARD, 2580 -> 2583**: one condition, one
binding, one re-ask, re-measured after `ruff format` at each shape, with the
reason at the ratchet entry.

**Two owner findings, and this session queued them rather than narrating
them.** `OI-83` is round 033's — a long-lived coordinator executes the modules
it imported at launch, which is how working code was reported as a BLOCKER.
`OI-84` is round 034's root cause: this fix closes ONE symptom at its call
site, and three readers of the same blind range are left standing —
`worker_exit`'s DONE banner reports nothing built, `schedule_review_round`
never draws a fresh round on a complete train, and `current_assignment_wi`
reads every assigned WI as remaining and can re-claim one already built. Fixing
the base itself is a wider change than this row's remainder and belongs to
whoever rules OI-84.

Deferred open items: OI-83, OI-84.

#### Done-when 5, driven at the tip the integrator merges

Full unfiltered suite at `566b40e6` — the close commit, with `docs/stage`
regenerated on the worktree: **3359 passed, 25 skipped, 0 failed in 608.65 s**.
Two more tests than the red run and no failures: the C2 end-to-end contract is
back, and the new in-process pair covers it inside the smoke tier.
<!-- fig: cmd="python -m pytest -q -n auto (worktree at 566b40e6, docs/stage regenerated)" rev=566b40e6 -->

Recorded HERE and not in the Deliverable, deliberately. `docs/log.d/` is outside
the non-record tree identity, so this commit cannot move the tree the reading
names; a paragraph added to the spec would. That is the whole content of the
round-033 lesson — its close promised the green "in the follow-up commit", and
every follow-up that could carry it was also a commit that invalidated it.

### Round 036 — recursive ownership of generated rollups

REVIEW-A found one remaining mismatch between the generated-rollup contract and
its implementation: `_extra` scanned only direct children, so
`docs/reviews/rollup/nested/stale.md` was invisible to both `--check` and the
write path. The root cause was the owned-output enumeration itself, not either
caller. It now walks `*.md` recursively; the regression drives stale detection,
regeneration, deletion, and the subsequent fresh check on a nested output.

Deferred open items: OI-83, OI-84.

Full unfiltered suite at `6d1101db`, on a detached worktree with the trunk-owned
`docs/stage` regenerated in place: **3359 passed, 25 skipped, 0 failed in
603.38 s**. The primary work branch remained clean and its generated artifact
was not edited.
<!-- fig: cmd="python -m pytest -q -n auto (detached worktree at 6d1101db, docs/stage regenerated)" rev=6d1101db -->
