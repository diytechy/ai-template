# WI-957 implementation plan: the coordinator's review brief renders only over an attested tip

Spec: `docs/work/active/wi-957/WI-957-coordinator-review-gate.md` (specref:
review-churn README item 13, "Review only a green tip"). Item SRs: SR-235,
SR-146. Planner: fresh session, read-only. Lane worktree:
`C:/Projects/ai-template.wt/wi-957` (tip `64b8d686c`, WI-956 landed beneath it
at `ed84e2510`).

## What the code holds today (read, not assumed)

- `review_brief.py review` is `_cmd_review` -> `lane_commits` -> `Round` ->
  `render_review` -> `_write`. Nothing reads a bar record. A refusal is a
  `BriefError`, which `main` turns into exit 2 and a `review_brief: REFUSED
  — <reason>` line on stderr, before anything is written (IF-289).
- WI-956's one verifier is `kitlib/verdict.py` `bar_attestation(root, rev)`. It
  returns a `BarAttestation(tree, work, bar, tests, summary)` or `None`, and
  `None` covers every failure without a cause: no label line, two label
  lines, a grammar miss, a bar outside `BAR_NAMES`, a `tree=` that is not the
  commit's tree, a `work=` that is not its first parent. `tests_digest(paths)`
  is the one digest; it normalizes `\` to `/` and drops a leading `./`.
- `governing_rev` already defines the walk step the spec names: a commit is
  walked through exactly when `tree_identity(rev) == tree_identity(rev^1)`.
  `tree_identity` folds out `RECORD_PREFIXES` (`docs/reviews/`,
  `docs/log.d/`, `docs/iteration/`). Its loop also peels disposable commits
  (`_peel_target`), and the review gate must not do that: a refresh carries
  `landing` and must be refused as such.
- `integrate.py attest --branch <b> --bar review --tests <paths...>
  [--message-file F]` runs from the primary checkout. It runs `[bars] review`
  (this repo: `run_menu.py smoke`), then the named tests, and commits the
  staged work, or an empty commit when nothing is staged, carrying
  `bar=review tests=<digest>`.
- The cycle text "`git log -1` moved" sits in `coordinator-cycle` SKILL §3,
  Iterate step 1, in three byte-identical copies: `project-trajectory/skills/`,
  `.claude/skills/` and `.agents/skills/` (synced by `bootstrap.py --dest .
  --sync`). The recipes' commit step is §1 (the builder bullet's "you verify
  and commit", the render bullet) and §6 (the commit bar bullet). §4
  (rebasing) has no re-attest step. SKILL §3 Intent step 3 reads "then
  verify, regenerate and commit".
- WI-956's RESYNC entry (`[since be80354d9]`) lists `scripts/integrate.py`,
  `kitlib/verdict.py`, `station.py`, `provenance.py`, `stack.ini.template` and
  `worker.template.md`. It does not list `review_brief.py` and says nothing
  about a review render. So Deliverable 3's "otherwise" applies: **one entry
  is owed**, and `scripts/check_resync.py`, which is in the commit bar,
  enforces it on the code commit.

## The architectural-delta question

The WI **makes an output depend on a new input**. Today the brief and the
exit code of `review_brief.py review` depend only on the spec, the range and
the arguments. After this change they also depend on the reviewed commit's
`Bar-Green:` record and on the commits between it and the attested commit.
It adds no state: the record is WI-956's commit trailer, and no file, marker
or store is added. It adds no value to any domain: the bar set stays
`review|landing|no-bar`, and exit 2 already means "refused, nothing written".
It crosses no new boundary: `review_brief.py` already imports
`kitlib.verdict` (`round_file`, `filing_refusal`) over IF-175, whose
requestor list leaves it out today. That is drift this plan reconciles; it
is not a new seam.

The change sits inside modules this item owns or may amend in place
(`review_brief.py`, `kitlib/verdict.py`) and on interface rows amended in
place (IF-288's contract body, IF-289's refusal list, IF-175's requestors
and data). No refactor outside the lane is needed. The table carries the
change: P3 is the verifier's cause and the walk on IF-175, P4 is the new
input on IF-288/IF-289, and P6 is the records.

DELTA: within

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Spine intent turn, TC-first (Terra, before build round 1): draft the derived SR ("a review starts only on a tree whose review bar is attested green"), its coordinator LLR and two TCs (the render gate; the cycle text), each naming the tests P2 adds | D1; D6; SR-235; SR-146 | no interface: registry rows only, no code seam crossed |  |
| P2 | Test commit: the new tests, each marked strict expected-failure (`xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`), plus the `git_lane` fixture's tip and the two record-commit tests moved onto attested commits (green on today's code, because today's render ignores the trailer). No stub is needed: every new test drives the CLI or reads text, so its red is an assertion on today's code | D1; D2; D3; D4; D5; SR-235; SR-146; TC-333 | IF-288; IF-289 | P1 |
| P3 | `kitlib/verdict.py`: give the one verifier a cause (`read_bar_attestation` returns `(attestation, cause)`; `bar_attestation` becomes its first element, so it stays the one verifier). Add the review walk (`review_attestation(root, rev, tests)` returns `(attested sha, None)` or `(None, cause)`), which checks for a verified `review` record with a matching digest at each rev and steps to the first parent only while non-record identity is unchanged. Extract that step from `governing_rev` into one private helper both walks call. IF-175 cells amended | D2; D3; D4; SR-235 | IF-175 | P2 |
| P4 | `review_brief.py` `_cmd_review`: after `lane_commits` and `Round`, and before `render_review`, call the walk. On a refusal, raise `BriefError` naming the reviewed sha, the cause and the `integrate.py attest --branch <lane> --bar review --tests <the same tests>` command (exit 2, no brief). On success, print one stdout line naming the attested commit and the digest. The IF-288 and IF-289 contract bodies in the module docstring state the refusal. The strict marks come off P2's D2–D4 tests | D1; D2; D3; D4; SR-235; SR-146; TC-333 | IF-288; IF-289; IF-175 | P3 |
| P5 | Cycle text in all three skill copies (`bootstrap.py --dest . --sync`): SKILL §3 Iterate step 1 becomes "the tip carries the review bar's attestation". Intent step 3 and recipes §1 and §6 commit lane work through `integrate.py attest`. Recipes §1 render bullet: `--tests` must be the attested list. Recipes §4: re-attest a rebased tip before its round. The D5 test's mark comes off | D1; D5; SR-235 | no interface: skill text only, no code seam crossed | P4 |
| P6 | Records: IF-175 `requestors` gains `scripts/review_brief` and `data` names the review walk; one RESYNC §4 entry, anchored `[since <trunk base>]`, with `review_brief.py` and `kitlib/verdict.py` to overwrite (a forced migration, flagged); the new LLR's traced `module`/`code_symbol` cells; `Implements:` lines on the new symbols. P3–P6 are one code commit, made through `integrate.py attest` with the lane's named tests, because the attest recipe lands with the refusal | D6; SR-235; SR-146 | IF-175; IF-288; IF-289 | P5 |
| P7 | Landing: re-anchor the RESYNC entry at the landing's parent. The commit bar is green, and `check_trajectory.py --strict` and `trace.py --strict` are clean. The derived SR, the LLR and both TCs are judged at the lane's sitting. Trunk-only regenerations (`docs/interface-reference.md` through the trunk step, the dashboard, the rollups) are left to the landing | D6; SR-235; SR-146; TC-333 | no interface: landing bookkeeping, no code seam crossed | P6 |

Excludes: TC-157; TC-161; TC-192; TC-331 — each verifies an SR-146 arm this item does not touch: prompt templates as loaded, fingerprinted files and the argv transport (TC-157), the adjudicator briefs' evidence (TC-161), the generated prompt catalogue's freshness (TC-192), and the adjudicator and disposition briefs (TC-331). This item changes no prompt template, no catalogue entry and no adjudicator brief. The gate refuses before `prompts.fill` runs, and the reviewer template's text is unchanged. These TCs run unchanged in the full suite at landing and need no amendment.

## Step detail

### P1: spine intent turn (TC-first; Terra, before build round 1)

Requirement prose names no code. This follows the 2026-10-11 ruling, which
the spine-authoring skill applies: capability and artifact-class voice in
every requirement, rationale, acceptance and detail cell. `module` and
`code_symbol` stay as the schema's traced cells, filled at P6.

- **Derived SR (new, Drafted, labelled derived).** `sn_refs = ["SN-004",
  "SN-008"]`, aspect process, nearest existing row SR-235. Intent: "When an
  attended launcher requests a review brief for a lane commit, the delivered
  review content shall render it only when that commit, or a commit beneath
  it from which only review-record changes separate it, carries a verified
  record that the declared review bar and the named test set passed on its
  tree. Otherwise it shall refuse, write no brief, and name the cause and the
  step that makes the record." Acceptance lists the refusal arms: absent,
  unverified (another tree or another parent), malformed, another bar,
  another test set, and a work change above the record. It also lists the two
  render arms. Rationale: review sessions are the metered resource, and
  reviewing a tip a tool already knows is red buys a finding the tool would
  have produced (README item 13). The record is trusted, never re-run (B3).
  The bound is PROCESS.md §6, as the spec's Trust section states it. The SR
  says that WI-958's loop LLR joins it.
- **Coordinator LLR (new, Drafted, CMP-008),** under the new SR. Detail: the
  review render resolves the reviewed commit, then looks for one verified
  review-bar record whose test digest equals the digest of the round's named
  tests. It looks at that commit and at the commits beneath it whose
  non-record identity equals their parent's. It never peels a disposable
  commit. A landing or no-bar record is refused as another bar. The search
  stops at the first commit that changes a non-record path, and at the
  existing walk bound. Every refusal names the reviewed commit, the cause
  (both digests for a test-set mismatch, both values for a tree or parent
  mismatch) and the attest command with the lane and the round's own test
  list. It writes no brief and exits with the refusal code. A rendered brief
  reports the attested commit and its digest on the console. The render never
  runs the bar.
- **TC (new), the render gate** (Integration, Test). It verifies the new SR,
  the new LLR, IF-288 and IF-289, and its evidence is every test P2 adds
  except the cycle-text test.
- **TC (new), the cycle text** (Test, a text pin). It verifies the new SR and
  the new LLR. Its evidence is the P2 test in `tests/test_prompts.py`.
- **TC-333** keeps its meaning, so it is not re-attested. Its tests still
  render, now over an attested fixture tip. Its `expected` sentence, "A
  successful review returns exit 0 and writes only its brief", stays true of
  an attested tip. If the sitting rules the precondition must appear in
  TC-333's text, that amendment becomes a row of this lane's checkpoint, not
  a new plan row.
- No change to SR-235, SR-146 or LLR-313. LLR-313's render, filing and
  lane-commit arms are unchanged. The gate is the new LLR's.
- Terra's prompt follows recipes §1: `CHANGES=none`, `TESTS=` empty. Record
  the Terra session id in `docs/decisions/wi-957.toml`.

### P2: the tests, first (one commit, strict expected-failure marks)

All D2–D4 cases go in `tests/test_review_brief_git.py`, which is already in
`SLOW_MODULES` and already holds the real-git `git_lane` fixture, so
`conftest.py` does not change. A helper `_attest_tip(root, message,
tests=("tests/test_a.py",))` stages, takes `write-tree` and `rev-parse
HEAD`, and commits with `kverdict.format_bar_green(tree, parent, bar,
kverdict.tests_digest(tests), "review bar PASS")`, the writer WI-956 ships.
Variants of the helper produce the bad trailers. Each test asserts exit 2,
an empty `out` directory and a clean `git status`. Each refusal's stderr
must contain `integrate.py attest` and `--bar review`.

| Test (new) | Clause | Red on today's code, at its assertion |
|---|---|---|
| `test_a_tip_with_no_attestation_refuses_naming_the_attest_command` | D2 | today renders: `main(...) == 2` fails (it returns 0) |
| `test_an_attestation_that_does_not_name_the_tip_refuses_naming_the_cause` (parametrized: `tree=` of another staged tree; `work=` of another parent, the rebase and cherry-pick case; a malformed line without `bar=`) | D2 | exit 0, not 2. The cause substrings ("names tree", "first parent", "grammar") are absent too |
| `test_a_landing_attestation_refuses_naming_both_bars` (a verified `bar=landing` on a `refresh:` subject) | D2 | exit 0, not 2. Stderr does not name `landing` and `review` |
| `test_a_review_attestation_for_other_tests_refuses_naming_both_digests` (attested for `tests/test_a.py`, rendered with `--tests tests/test_b.py`) | D2 | exit 0, not 2. Both 64-hex digests are absent from stderr |
| `test_a_matching_review_attestation_renders_and_names_it` (rendered with `./tests\test_a.py`, a different spelling of the same set) | D3 | exit 0 today, but the stdout line naming the attested sha and digest is absent |
| `test_record_only_commits_above_the_attested_one_render` (an empty commit, then a `docs/reviews/` and a `docs/log.d/` commit on top of the attested one) | D3 | the stdout line names the attested commit beneath the tip; today it is absent |
| `test_a_work_commit_above_the_attested_one_refuses` (parametrized: `src/app.py`; `docs/decisions/wi-900.toml`, which is not a record prefix) | D4 | exit 0, not 2 |

These go elsewhere:

- `tests/test_integrate_attest.py::test_the_review_render_accepts_what_attest_writes`
  (D3; the module is in `SLOW_MODULES`). `integ.attest` writes a real `review`
  record on the `attest_repo` lane with `NAMED`. The test adds the lane's
  spec under `docs/work/active/wi-401/`, then calls `review_brief.main(["review",
  "--root", <lane wt>, ..., "--tests", *reversed(NAMED)])`. That proves the
  producer's and the consumer's digests agree whatever the order. Red: the
  stdout attested-commit line is absent.
- `tests/test_prompts.py::test_the_cycle_reviews_only_an_attested_tip` (D5;
  smoke). It reads the shipped SKILL and recipes, whitespace-flattened like
  WI-955's text pins. Each must carry "the tip carries the review bar's
  attestation" and `integrate.py attest`, and neither may carry "`git log -1`
  moved". Red: the old phrase is present.

Existing tests that must keep passing, with fixtures only:
`test_a_review_render_exits_zero_and_writes_only_the_brief`,
`test_the_reading_scope_never_shows_a_record_of_earlier_findings` and
`test_an_ordinary_review_reads_the_decisions_record`. Their tips (the
`git_lane` tip and the two "records" commits, which change `src/app.py`) are
committed through `_attest_tip`. Today's code ignores the trailer, so these
fixture edits are green on both sides of the change. The other existing
tests (`lane_commits` refusals, filing) are untouched. Their refusal order
stays first, because the gate runs after `lane_commits`.

The commit carrying the marked tests runs the bar declared for review. That
bar is the smoke tier, which holds the `test_prompts` pin, plus the lane's
named set, which holds the slow modules. Under item 13 this green is the
red-before. Adding one smoke test may cross `[tiers] max-tests` (2980). If it
does, re-stamp the ceiling in this commit with its reason and record a
decision (recipes §1, wi-927 D-002). Never fold cases to fit.

### P3: the verifier's cause and the review walk (`kitlib/verdict.py`)

- `read_bar_attestation(root, rev)` returns `(BarAttestation | None,
  cause)`. It is today's `bar_attestation` body, with each `return None`
  replaced by a named cause:
  - an unreadable commit;
  - no `Bar-Green:` line at column 0;
  - N label lines;
  - a line outside the grammar;
  - a bar outside `BAR_NAMES`;
  - `tree=<x>` that is not the commit's tree `<y>`;
  - `work=<x>` that is not its first parent `<y>`.

  `bar_attestation` returns `read_bar_attestation(...)[0]`. So there is still
  one verifier, and `refresh_attestation`, `_merge_ready` and every WI-956
  test keep their behaviour.
- `review_attestation(root, rev, tests)` checks the verified record at
  `rev` first:
  - a `review` record with `tests == tests_digest(tests)` returns `(sha,
    None)`;
  - another bar returns a refusal naming the bar found and `review`;
  - a digest mismatch returns a refusal naming both digests.

  With no verified record, it takes one step: to the first parent, when the
  non-record identity is unchanged. Otherwise it refuses with that rev's
  cause and "changes non-record paths over its parent". Reaching
  `_MAX_GOVERNING_WALK` refuses, naming the bound. Disposable commits are not
  peeled, because a refresh is a `landing` record and is refused as one.
- **One step definition.** The identity-equality step moves out of
  `governing_rev`'s loop into one private helper, `_identity_step(root, rev,
  identity)`, which returns `(parent, parent identity)` or `None`. Both walks
  call it. This is a behaviour-preserving extraction, pinned by the existing
  `governing_rev` tests in `tests/test_verdict_record.py` and
  `tests/test_bar_attestation.py`. The walk lives in `kitlib`, not in
  `review_brief.py`, because WI-958's Deliverable 2 asks the same question
  at the loop's draw. It is one answer with two requestors.
- IF-175 `data` gains "the review walk (a verified review record with a
  matching test digest at the commit or beneath it through non-record-only
  commits)"; its `requestors` gain `scripts/review_brief` (P6 writes both
  cells).

### P4: the refusal at the one render route (`review_brief.py`)

- Put a `_review_bar_refusal(root, lane, sha, tests)` call in `_cmd_review`
  after `Round(...)`, so shape refusals such as an empty test list keep their
  order, and before `render_review`. It calls `kverdict.review_attestation`.
  On a cause it raises `BriefError` with: the reviewed sha, the cause, and
  `run "$PY" <scripts>/integrate.py attest --branch <lane> --bar review
  --tests <tests as given> from the primary checkout (staging the work it
  attests, or nothing for an empty attestation commit), then render again`.
- On success, print `review_brief: <sha> renders over the review bar's
  attestation at <attested sha> (tests=<digest>)`.
- `render_review` stays pure. Its in-process smoke tests in
  `tests/test_review_brief.py` stay as they are, and no other caller
  exists: the spec greps, and so did this planner.
- Contract IF-288 (docstring): the `review` sentence gains "and only when SHA,
  or a commit beneath it that only non-record-only commits separate from it,
  carries a verified `bar=review` attestation whose tests digest is that of
  the tests". Contract IF-289 gains "a reviewed commit with no such
  attestation" in the refusal list. The `--tests` help text stays as it is,
  so `docs/cli-reference.md` does not move.
- Remove the strict marks from P2's D2–D4 tests and from the round-trip test.

### P5: the cycle text (one commit with P3, P4 and P6)

Edit `project-trajectory/skills/coordinator-cycle/`, then run `bootstrap.py
--dest . --sync` so `.claude/` and `.agents/` match byte for byte:

- **SKILL §3 Iterate step 1:** "**The tip carries the review bar's
  attestation** before any review: commit lane work through `integrate.py
  attest` with the round's `--tests`, and `review_brief.py review` refuses
  any other tip. A hook-refused commit or a red bar attests nothing, and the
  render then refuses." The "`git log -1` moved" text is removed.
- **SKILL §3 Intent step 3:** "then verify, regenerate and commit through
  `integrate.py attest` (recipes §6)".
- **Recipes §1, builder bullet:** "you verify and commit" becomes "you
  verify and commit through `integrate.py attest`".
- **Recipes §1, render bullet:** `--tests` is the list the tip was attested
  with. A spine-checkpoint commit and a decisions-record commit change
  non-record paths, so attest them (stage them into the next attest, or make
  an empty one) before the round. Round-file and log commits need none.
- **Recipes §4:** after a rebase, attest the rebased tip (nothing staged
  gives an empty attestation commit) before its round, because a rebase
  changes every `work=`.
- **Recipes §6, first bullet:** a lane commit runs the bar through
  `integrate.py attest --branch <lane> --bar review --tests <files>
  --message-file <msg>`, which runs `[bars] review` and the named tests and
  refuses red. A trunk commit still runs `run.cmd smoke` by hand. The
  read-the-summary warning stays.
- Remove the D5 test's mark.
- `docs/handoff-2026-10-06-wave18-coordinator.md:67` also says "`git log -1`
  moved". It is a dated historical handoff, not a live instruction, so it
  stays as written. D5's scope is the skill and recipes.

### P6: records (same commit as P3–P5)

- `docs/requirements/interfaces.toml` IF-175: the requestor and data cells
  as stated under P3. IF-288's and IF-289's `data` cells already cover a
  refusal with no brief, so they stay as they are. Their contract bodies
  change at P4.
- The new LLR's `module` (`review_brief.py;kitlib/verdict.py`) and
  `code_symbol` (`_cmd_review/_review_bar_refusal` and
  `review_attestation/read_bar_attestation`) cells. `Implements: <new SR>,
  <new LLR>` on those symbols.
- **`RESYNC_PACK.md` §4: one entry,** "The attended review brief renders
  only over a review-attested tip [since <trunk base>]". It covers:
  - **What changed:** `review_brief.py review` refuses, with exit 2 and no
    brief, a commit with no verified `bar=review` attestation for its
    `--tests`, walking only through record-only commits.
  - **What to do (a forced migration, flagged):** commit lane work through
    `integrate.py attest` with the same test list the round names before
    rendering, and re-attest after a rebase. `[bars] review` is required
    already, by WI-956's entry.
  - **Overwrite:** `scripts/review_brief.py`, `scripts/kitlib/verdict.py`.
- `docs/runtime-flows.md`: no edit. No flow depicts the attended review
  render. The change is one precondition at one CLI entry and adds no
  participant or message order. Flow 4 (the station) is unchanged: `attest`
  is WI-956's.
- `docs/requirements/components.toml`: no edit. CMP-008 already owns both
  modules, and no module is added.
- Commit through `integrate.py attest --branch wi-957 --bar review --tests`
  with the lane's named set:
  - `tests/test_review_brief_git.py`
  - `tests/test_review_brief.py`
  - `tests/test_integrate_attest.py`
  - `tests/test_bar_attestation.py`
  - `tests/test_verdict_record.py`
  - `tests/test_prompts.py`

  This lane's own round 1 then renders from the lane's copy over this
  attested tip, with the same `--tests` (spec, "Machinery landing alone").

### P7: landing

- Re-anchor the RESYNC entry at the landing's parent.
- Run the commit bar on the staged squash and read the summary lines. Run
  `check_trajectory.py --strict` and `trace.py --strict` before the landing
  commit (R-F escapes the hook).
- The sitting judges the derived SR, the LLR and both TCs.
- Leave `docs/interface-reference.md` and the other trunk-only views to the
  landing regenerations.
- Run the full suite once at landing. That also runs TC-157, TC-161, TC-192
  and TC-331 unchanged.

## Risks and decisions for the coordinator

- **A decisions-record commit is not a record path.** `docs/decisions/` is
  in the identity (`RECORD_PREFIXES` is `docs/reviews/`, `docs/log.d/`,
  `docs/iteration/`). Recording the convergence map before a convergence
  round therefore needs an attest, at the cost of one bar run. Widening
  `RECORD_PREFIXES` would change what a verdict governs, and this item does
  not own that. P2 pins the current behaviour (D4's `docs/decisions` case).
- **A load-induced budget breach refuses `attest`, so it refuses the round.**
  This follows from the ruled bar (a breach FAILS it). No fallback is added.
  Re-measure on a quiet box.
- **The trust bound** is the spec's: a hand-forged trailer is outside the
  promise (PROCESS.md §6). No test is written against it.
