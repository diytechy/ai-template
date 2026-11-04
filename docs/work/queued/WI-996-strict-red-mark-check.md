+++
id = "WI-996"
title = "A removed red mark is proven red by the lane's last review record, no red mark lands, and `[bars] red_mark` declares the mark"
workstream = "process"
sr_refs = ["SR-156"]
specref = "docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages"
needs = ["WI-995", "OI-125"]
buildtier = "medium"
safety_class = "ordinary"
planmode = "single"
priority = 5
+++

## Context

P8's three rows (WI-992's filing, the review-churn plan's item 13): row 1 is WI-994, row 2 WI-995 and row 3 WI-996; "row N" below names them so.

**What the plan rules.** Review-churn item 13 (ruled as a whole in
revision 35; mechanism from revisions 20 and 23) proves a test's red-before
with a strict expected-failure mark. The tests-first commit lands each new
test under the mark. Its review-bar attestation records the bar it passed,
so that green bar is the red-before: a strictly marked test passes the bar
only by failing at an assertion. The code commit removes the marks. "A
commit-versus-parent check confirms that each removed mark was present in
the parent, that the parent carries a green attestation of the review bar,
and that the test now passes under the same bar. That is a static check,
light enough for ruling 6's commit-bar command; the bar itself is the
execution." The Python reference is
`@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`.
Other stacks supply their equivalent, restricted to assertion failures. The
owner accepted `[bars] red_mark` as a required key, a forced adopter
migration stated in a RESYNC entry (OI-120 Q2 (a), 2026-11-02).

**Where `[bars]` lives (re-measured).** `[bars]` is not in
`docs/process.toml`. Its sections are `attestation`, `policies`, `checks`,
`adjudicator`, `reviewer`, `coordinator` and `build`
(`grep -n "^\[" docs/process.toml`). The section is in `docs/stack.ini`
(line 1360) and in `project-trajectory/stack.ini.template` (line 254). Each
holds exactly one key, `review` (`grep -n "^\[bars\]" -A8` on both files).
Item 10's fold of `stack.ini` into `process.toml` is not queued. So this row
adds the key where the section lives now, and the fold moves the whole
section later. `[bars]` has one parse site,
`integrate._review_bar_command` (`grep -rn '"bars"'
project-trajectory/scripts` returns only `integrate.py:3001`). Its contract
text is IF-022's, in `docs/stack.ini`'s header (lines 11 to 26), and
`docs/interface-reference.md` is regenerated from it.

**What exists today (re-measured).**

- **Marks in this repository: none.** The whitespace-stripped Python
  reference appears 0 times across the 306 files under `tests/` (269
  `test_*.py`), checked with a `pathlib` count run under the repository's
  `.venv` with `-I`. The one `xfail(strict=True` text under `tests/` is
  `tests/test_prompts.py:308`. It is a clause literal split across two
  string literals, pinning WI-955's skill text, so it is not a mark.
- **The order is text only.** WI-955 put the tests-first order and the
  mark into the coordinator-cycle skill
  (`project-trajectory/skills/coordinator-cycle/SKILL.md:194-205`, with the
  `.claude` and `.agents` copies). It says "committed alone before the
  code". It does not say that the commit goes through `attest`, and nothing
  checks the order.
- **Callers of `attest`.**
  - The coordinator calls it by hand: `integrate.py attest --tests <files>`
    (recipes §6).
  - The agent loop calls it in two places, both with an empty test set:
    `agent_loop.py:2498` (`attest_build`) and `:3384` (the draw).
  - The attestation records only a digest of the test set (`tests=`,
    `kverdict.tests_digest`), not the list.
- **Lane-local history is already read.** `kverdict._last_review_green(root,
  branch, base)` already finds the newest verified `review` attestation in
  `base..branch` (`red_rounds` reads it). `integrate._lane_base` names the
  lane's base, with a fail-closed refusal.
- **Fixtures that declare `[bars]`.**
  - `tests/conftest.py` `declare_review_bar` is called five times from
    `test_agent_loop_review.py` (twice), `test_agent_loop_review_gate.py`
    and `test_agent_loop_worker.py`.
  - `tests/test_integrate_attest.py` writes the section inline (its refusal
    table, lines 225 to 227, and line 258).
  - `tests/test_integrate_station.py:224` writes it inline.
  - `tests/test_check_smoke_budget.py:490` reads `[bars] review` and is
    unaffected.
- **`check_test_first.py` is untouched.** It is the warn-only `test-first`
  step (SR-217, IF-198). It reads the approval order of test-case rows
  against the code's landing from trunk history. That is a different
  question from a test's red-before, and this row does not change it (see
  "Not in this row").

**The anchor.** SR-156 is the anchor ("a finished branch reaches the
integration branch only through the serial seam with the declared bar green
on the composed tree"). Both arms extend the one attestation producer that
LLR-207 states under SR-156. A strictly marked test passes the bar while it
is red, so a landing tree holding a mark is not green in SR-156's sense.
Neither SR-156 nor LLR-207 states the red-before obligation today. The
change set's spine authoring at intent decides between a new LLR under
SR-156 beside LLR-207 and a labelled derived SR. This row does not write
requirement text.

## Scope

`integrate.py attest` gains the strict-mark check: a static comparison,
before the bar runs, of the lane's staged tree against the tree of the
lane's last review attestation. Each test file whose count of the declared
red mark rises must be in the round's test set. Each test file whose count
falls must also be in that set, and the last review attestation must be
over the same test set. The refresh refuses any landing tree whose tests
root still holds the mark. The mark is declared once, as `[bars] red_mark`
beside `[bars] review`. The key is required: if it is absent or empty,
`attest` and the refresh both refuse and name it. There is no default.
Third of P8's three rows (WI-992, OI-120 Q2 (a)). The coordinator
substitutes `WI-995` with row 2's filed id.

## The rule (S3: closed)

**The declaration.** `[bars] red_mark` is read with `[bars] review` through
one parse of `docs/stack.ini`. It is read from the same tree as
`[bars] review`: the lane's staged checkout at `attest`, and the tree the
refresh bars at the refresh. A value that is non-empty after stripping is
the mark's text. Every other state refuses, naming `docs/stack.ini
[bars] red_mark` and the cause:

- the file is absent;
- the file does not parse;
- the section is absent;
- the key is absent;
- the value is empty.

The refusal comes before any bar runs. There is no default and no fallback
to another key. The test files are the paths under `[paths] tests`,
resolved as the harness resolves it (one home).

**Counting.** A file's mark count is the number of non-overlapping
occurrences of the declared text in the file's bytes. ASCII whitespace is
removed from both the file and the text before counting, so a formatter
that wraps the call's arguments still counts. Bytes are counted, never
decoded, so no file is undecodable.

**The attest arms.** The reference is the newest commit in the lane's own
range (`_lane_base`..HEAD) that carries a verified `review` attestation. If
no commit in the range carries one, the reference is the lane base, which
carries no review record. The compared paths are the test files that
differ between the reference's tree and the staged tree. A rename counts
as a deletion plus an addition. Write m0 for a file's count at the
reference and m1 for its count in the staged tree; an absent file counts 0.
T is the round's test set, the set the new attestation's `tests=` digest
covers. "T names P" means that an entry of T, normalized as `tests_digest`
normalizes (a backslash to `/`, a leading `./` dropped), equals P. A node
id (`P::name`) or a directory does not name P.

| State of test file P | Ruling |
|---|---|
| m1 = m0 (0 = 0 included) | not judged |
| m1 > m0: marks added, or a new file that carries marks | passes when T names P. Otherwise refused, naming P: the bar would not run its marked tests, so their red is unproven |
| m1 < m0, and P is present in the staged tree: marks removed | passes when the reference carries a verified `review` attestation whose tests digest equals T's, and T names P. Otherwise refused, naming P and which condition failed: no review record stands for the marked tree, the record is for another test set, or the set does not name P |
| m1 < m0, and P is absent from the staged tree (deleted or renamed away) | not judged here: the test is gone, its TC loses its tagged file, and row 2's partial-set refusal names that |
| git cannot read the range, the reference's tree or the staged tree | refused, naming the read: an unread delta is not an empty one |

Removing a mark therefore needs three things:

- the mark was present at the last tree the lane attested;
- that tree's green bar ran the marked file under the strict mark, which is
  the red-before;
- the new bar runs the file unmarked over the same test set, which is the
  green-after.

A plain commit between two attestations is judged at the next attestation,
because the reference is the last attested tree, not HEAD.

**The landing arm.** The refresh, on the tree it bars and before the bar
runs, refuses when any file under the tests root has a mark count above 0.
It names each file and its count. This applies to both refresh bars
(`landing` and `no-bar`). A tree with no marks passes. Unreadable files
refuse as above. Marks are therefore never on trunk. That keeps the attest
arms' compared paths the lane's own, even after a merge-refresh brings
trunk in.

**What the bar already does.** A mark left on a test that now passes is the
bar's to refuse: an unexpected pass under a strict mark fails it. An error
that is not an assertion failure also fails it. The check does not judge
either case.

## Not in this row

- **Tagging tests, and the reader of the tags:** row 1.
- **Deriving the review test set, and refusing an empty or partial set or a
  code row that names no SR:** row 2. After row 2, T is that derived set.
- **Requiring a new test to carry a mark.** A characterization test is
  unmarked, and its adequacy witness is judged by the reviewers. Inspection,
  Analysis and Attest TCs carry their own evidence (item 13's typed
  evidence).
- **Retiring `check_test_first.py`.** The plan's text says its history read
  "retires into the commit check". It judges test-case approval order,
  which this check does not replace. Retiring it would remove a shipped step
  and its `[checks] test_first_since` key, a third adopter migration that
  OI-120 did not accept. OI-125 Q3 ruled (a) (2026-11-03): it stays.
- **Moving `[bars]` into `process.toml`:** item 10's fold.
- **The pre-commit hook:** unchanged (see S-answers).
- **The review render (`review_brief.py`), the merge slot and
  `handback.py`:** unchanged. The render and the slot trust the
  attestations, which now carry this check. A partial close whose tree
  holds marks is refused at its refresh, and it quarantines through the
  existing arm (`handback.quarantine` takes any lane, red or not).

## Pre-answered critique

**S1, the deliverables.** There are five:

- (a) the declaration and its refusal;
- (b) the attest arms;
- (c) the landing arm;
- (d) the procedure text (the coordinator-cycle order through `attest`,
  and one sentence in PROCESS.md §4 "DevStg-Impl");
- (e) the RESYNC entry.

(a) alone is a dead key. (b) needs (a). (c) needs (a), and (b)'s compared
paths stay lane-own only while (c) keeps trunk free of marks. (d) and (e)
describe (a) to (c) once they are built. They land in one lane, in the
order (a), (b), (c), (d), (e). (c) could be filed as its own row. The cost:
until it lands, a partial close can put a marked test on trunk, where the
bar reads it green, and a lane that later merge-refreshes and attests is
refused for a file it never touched.

**S2, trust.** Two authorities are given. The `[bars] red_mark`
declaration now gates `attest` and the refresh. The last review attestation
now licenses removing a mark. See `## Trust`.

**S3, closed coverage.** The input spaces are:

- the declaration's states (five refusals, one accepted state);
- the per-file count transitions (the table above);
- the reference's states (a verified record in the range, or none);
- the landing tree's count (0, or above 0).

Each is enumerated, and git failures refuse. The coverage bound is in the
Done-when.

**S4, planmode.** `single`. The row has a `## Trust` section, touches two
seams (IF-022's declaration; the attest and refresh verbs of IF-154 and
IF-173) and promises behaviour over the input spaces above.

**S5, the architectural delta.** No new state, no new boundary.

- **New inputs to existing outputs.** `attest`'s verdict now depends on
  `[bars] red_mark`, `[paths] tests` and the lane's last review
  attestation's tree and digest. The refresh's verdict now depends on the
  declaration and the landing tree's test files.
- **New values in existing domains.** IF-022 gains the key. The refusal
  sets of both verbs gain the mark refusals.
- **Where the code goes.** The counting and the per-file rule fit one
  stack-neutral pure function over two trees, which both arms call. A new
  kitlib module would keep `integrate.py`'s ratchet (`tests/
  test_module_size_ratchet.py`, 1802) to the call sites. That is the plan's
  choice, not this row's.

**S6, dependencies.** `needs` is row 2. Both attest arms read "the round's
test set", and the loop passes an empty one today (`agent_loop.py:2498`,
`:3384`). Before row 2 derives the set, every loop build that adds a mark
would be refused, which counts as red toward `[build] red_rounds_max`. The
plan also places the marked tests in "the smoke tier plus the lane's scoped
set". Row 2 needs row 1, so row 3 lands last. No new package.

**S7, proportion.** Two mechanisms are added beyond the plan's sentence.

- **The landing arm.** The scenario where the row fails without it is the
  supported partial close above.
- **The last-attested reference instead of HEAD.** The scenario where a
  HEAD-only check fails is the supported route wi-957 D-001 recorded: a
  code commit made by a plain commit, then an `attest` with nothing staged.
  Compared against HEAD, that removal is never judged.

Nothing else is added.

**Where it runs, and why not the hook.**

- **It runs in `attest`.** `attest` is the only producer of the review
  record that the review render requires (SR-241), and it runs the commit
  bar on the staged tree with its parent at hand. That is the commit-time,
  commit-against-reference form, and it is "light enough for the commit-bar
  command".
- **The hook cannot run it.** The hook sees neither the round's test set
  nor an attestation.
- **The ruling keeps it out of the hook.** Ruling 6 keeps the pre-commit
  hook as it is ("commits stay light").
- **The review render needs nothing new.** A tip without an attestation
  cannot be reviewed (SR-241), so a commit that bypasses `attest` reaches
  review only through a later `attest`, which judges it.
- **The landing arm runs in the refresh**, the producer of the landing
  record that the merge slot trusts (B3: the slot reads the record and
  never re-derives it).

## Done-when

- [ ] `[bars] red_mark` is declared in `project-trajectory/stack.ini.template`.
      The value is `pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`,
      with no `@`, so a `pytest.param(..., marks=...)` mark counts too. Its
      comment says:
      - it is required, with no default;
      - it is matched with whitespace ignored;
      - on another stack, the value is that stack's strict expected-failure
        form restricted to assertion failures. Jest's `test.failing`
        accepts any thrown error, so it is wrapped in a project helper that
        re-throws anything but an assertion failure, and the helper's call
        text is declared. A stack with no such form writes that helper.
      - every adopter declares it, including one that never marks a test.

      `docs/stack.ini` declares the same value, and IF-022's contract text
      (the header of `docs/stack.ini`) names the key and its refusal.
      `docs/interface-reference.md` is regenerated.
- [ ] One parse reads `[bars] review` and `[bars] red_mark`, from the tree
      each verb runs on. Each of the five refusal states in "The
      declaration" refuses `attest` before any bar runs, and refuses the
      refresh before its bar, naming `docs/stack.ini [bars] red_mark` and
      the cause. A test drives each state.
- [ ] `attest` judges the staged tree against the reference by the table in
      "The attest arms". A test drives each row:
      - added marks, named and unnamed;
      - removed marks: with a matching record; with no record in the range
        (the reference is the base); with a record over another test set;
        with T not naming P;
      - a deleted marked file;
      - a removal by a plain commit followed by an empty `attest`;
      - a formatter-wrapped mark;
      - an unreadable range.

      An unchanged count is not judged. Every refusal leaves the branch and
      the index as they were (the existing `attest` contract).
- [ ] The refresh refuses a tree whose tests root holds a mark, naming each
      file and count. This holds on both `landing` and `no-bar`. A tree with
      no marks refreshes exactly as today.
- [ ] Every fixture that declares `[bars]` also declares `red_mark`:
      `tests/conftest.py` `declare_review_bar`,
      `tests/test_integrate_attest.py` and `tests/test_integrate_station.py`.
      The build re-greps `tests/` for `[bars]` and `stack.ini` writers and
      lists them in its decisions record. The tests that check the rule
      build the mark's text from the declaration or by concatenation, so
      `tests/` never holds it whole and this repository's own landing arm
      stays at 0.
- [ ] The coordinator-cycle skill (`project-trajectory/skills/coordinator-cycle/SKILL.md`,
      Intent step 2, and `references/recipes.md` §6, with the `.claude`
      and `.agents` copies synced) says:
      - the tests-first commit goes through `integrate.py attest` with a
        test set that names each marked file;
      - the code commit that removes the marks names the same set;
      - a refresh refused for a mark ends in the code commit or a
        quarantine.

      `tests/test_prompts.py`'s clause pins follow the text.
      `project-trajectory/PROCESS.md` §4 "DevStg-Impl" gains one sentence:
      in a lane, the failing test is proven by the mark `[bars] red_mark`
      declares, attested before the code and removed by it, and never
      landed. Byte-budget-guard is run and its delta reported.
- [ ] RESYNC_PACK: one entry anchored at a trunk commit. Under **What
      changed**, it covers `attest`'s mark check, the refresh's landing arm
      and the required key. Under **What to do**:
      1. Add `[bars] red_mark` to `docs/stack.ini`, with the Python
         reference or your stack's form (the template comment). Without it,
         `attest` and the refresh refuse, naming the key. There is no
         default.
      2. Search your test root for the declared text. A file that already
         carries it must lose it before your next landing refresh.
      3. In-flight lanes carry the key only after a rebase or refresh onto
         the trunk that has it. Until then their `attest` refuses.

      **Kit-owned files to overwrite:** `scripts/integrate.py`, the new or
      changed `scripts/kitlib/` module, and `stack.ini.template`. This is
      the forced adopter migration OI-120 Q2 (a) accepted.
- [ ] Landing consequence, stated in the lane's decisions record: every
      lane cut before this row lands refuses at `attest` until it carries
      the key. `git worktree list` shows one lane today, `wi-902`.
- [ ] Coverage bound: the promise reaches the trees, declarations and
      attestations that supported workflows and the kit's own routes
      produce, as `project-trajectory/PROCESS.md` §6 "Review threat model"
      bounds a spec's promise:
      - `attest` and the refresh over a lane;
      - a plain commit followed by `attest`;
      - a merge-refresh;
      - a partial close;
      - a declaration written from the template or by hand through the
        documented key.

      Outside it:
      - hand-edited attestation trailers;
      - a stub written to raise an assertion error so that an assertion-free
        test "fails" (owner, item 13: adequacy review judges strength);
      - a mark spelled in a form other than the declared text (a test whose
        mark is not the declared text is unmarked to this check, and the
        bar runs it as an ordinary test);
      - a trunk commit made outside a landing.

      A rebase replaces the lane's earlier attestations, so the reference
      becomes the new lane base. Marks added and removed before the rebase
      are then not judged, and the pre-rebase review rounds stand as their
      record.
- [ ] `check_test_first.py` and its `[checks] test_first_since` key are
      unchanged; the mark check does not replace its judgement of test-case
      approval order (OI-125 Q3 (a)).
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Trust

This row gives two files authority over a gate: the `[bars] red_mark`
declaration, and the lane's last `review` attestation. Their authority is
over `attest` (which gates the review render) and the refresh (which gates
landing). Guards follow `project-trajectory/PROCESS.md` §3, "When a guard
is owed".

**Producers.**

- **The declaration** is person-written. Bootstrap copies the template
  value into a new scaffold, and an adopter adds the key at re-sync by the
  RESYNC entry. No kit script writes it after bootstrap, and no model is
  routed to write it.
- **The attestation** is written only by `integrate._attest_commit`, the
  one producer, and verified by `kverdict.read_bar_attestation`. A failed
  write leaves no record: the producer restores the tip and the index. So
  the only states are a verified record, or no record.

**Consumers** (found by grepping `"bars"`, `_review_bar_command`,
`integrate.attest`, `_last_review_green` and `Bar-Green` across
`project-trajectory/scripts`, `scripts` and `tests`).

| Consumer (path) | Reads | Ruling |
|---|---|---|
| `project-trajectory/scripts/integrate.py` `attest` (preflight, then the arms) | the declaration, `[paths] tests`, the lane's last review attestation and its tree, the staged tree, T | the declaration's five refusals, then the attest table |
| `project-trajectory/scripts/integrate.py` `refresh` | the declaration, `[paths] tests`, the tree it bars | the declaration's five refusals, then the landing arm |
| `project-trajectory/scripts/agent_loop.py` `attest_build` and the draw (`:2498`, `:3384`) | `attest`'s answer | unchanged: any refusal is red (its docstring), so a mark refusal or a missing key counts toward `[build] red_rounds_max` and closes partial at the cap, as an undeclared `[bars] review` does today |
| `project-trajectory/scripts/review_brief.py` (the render gate, SR-241) | the tip's review record | unchanged: a record exists only where `attest` passed the check |
| `project-trajectory/scripts/integrate.py` merge slot (`_merge_ready`) | the landing record | unchanged: a landing record exists only where the refresh passed the landing arm |
| `project-trajectory/scripts/handback.py` `quarantine` | the lane's diff against its base | unchanged: it reverts marked tests with the rest, so the refresh that follows passes the landing arm |
| `project-trajectory/skills/coordinator-cycle/` (procedure) | the order | replaced text (Done-when) |

**Input states.**

- **The declaration's states** are the five refusals and one accepted
  state in "The declaration". An accepted value that occurs in no file is
  not an error: nothing is marked.
- **The reference's states:**
  - a verified `review` record in the range: its tree and its tests
    digest are read;
  - none in the range: the base, with no record, so every removal refuses;
  - a range git cannot list: refused.

  The reference's tree is never re-barred: the record is trusted as the
  deciding step wrote it (B3).
