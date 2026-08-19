## 2026-08-18 — OI-31 ruled (b): the `staged-divergence` step, warn-first

**Why.** `check.py` has no staged/index concept. All nine regenerate-and-byte-
compare freshness steps resolve their artifact from the filesystem under
`--root`, so the gate's honest claim is "the artifact **on disk** matches its
regeneration" while every reader takes it to mean "the artifact **about to be
committed** does". Those diverge exactly when an author regenerates and forgets
one `git add`: the hook is honestly green and the committed tree is stale.
Measured at `3b8d306d`, where `PROJECT_STATE.html` was modified in the worktree,
absent from the index, and the committed tree failed the very gate that guarded
it — found only because an adversarial review re-measured a log fragment's claim.

**Owner ruling (OI-31, 2026-08-18): option (b), and explicitly NOT (a).** (a) —
teaching the nine gates to read the staged tree — is recorded as the destination
and is not this change: it would convert nine scripts whose contract is "a pure
function of a directory" into git-object readers, and that contract is what lets
the whole freshness tier be tested against a temp scaffold.

**The step.** `staged-divergence`, built into `check.py` (never a
`docs/stack.ini` `[step:]` — 130-REVIEW-A's lesson: a step the shipped hook
names must ship with the hook), self-invoked as
`check.py --staged-divergence`. It reports every declared `[generated]` artifact
that `git diff --name-only -z` shows modified in the worktree but absent from
the index.

- **The artifact list is a READ, not a copy.** `_generated_census()` parses
  `docs/stack.ini` `[generated]` — the same §5.2 declaration
  `tests/test_generated_freshness_wiring.py` reads to prove every declared
  artifact has an enforcer — with `optionxform = str`, because the keys are
  PATHS and configparser's default lowercasing would make `PROJECT_STATE.html`
  unmatchable (`integrate.py::_generated_paths` reads it the same way, for the
  same reason). This pays off the one real cost the ruling names against (b): a
  second home for the list that would rot at the tenth artifact. A trailing `/`
  is a prefix row; a marker-pair row matches the file.
- **Warn-first, never gating.** The step prints `WARN` and exits 0. The
  promotion the ruling names ("error once it has run clean for a program") is
  `--strict`, which is implemented and deliberately **not** passed by the step —
  the same posture, and for the same recorded reason, as `need-form`'s. Wiring
  it today would wedge every commit of a mid-flight program.
- **The honest gap is in the step's own message and docstring**, not only here:
  it does **not** catch an artifact that was STAGED WHILE STALE — the freshness
  gates read the worktree, so a stale blob in the index passes them and passes
  this; that case needs option (a). A check whose limits are undocumented is how
  the last false green survived.
- **Degrades, never crashes.** Four SKIP exits, each naming its reason: no
  `[generated]` census; no git or not a checkout; a root that is not the
  checkout's top level (so a scaffold nested inside a repo cannot resolve census
  paths against the wrong index); a failing `git diff`.
- **Gates at every bar** and is deliberately **not** in `_TRUNK_FRESHNESS_STEPS`:
  that stand-down exists because a work branch must not COMMIT a regenerated
  artifact, and this step never demands one.

**Wired** into the shipped pre-commit floor — `project-trajectory/hooks/pre-commit`
line 269, appended to the batched `--run-steps` line (now twelve steps) — with
its own entry in the floor's step commentary. Confirmed by running the real hook,
not by reading it.

**Option (c) taken as well, in its one in-lane place.** The hook's remediation
comment said "then re-commit" where the whole gap lives; it now says to STAGE the
regenerated files first, and says why (these steps compare the tree on disk).

**VERIFIED AGAINST THE MEASURED INSTANCE.** `3b8d306d`'s `docs/okf/` inputs no
longer exist (the export dial is off), so the shape was reconstructed in an
isolated clone at `77f6edd1`: stage a registry edit that stales the dashboard,
regenerate the dashboard, leave it unstaged.

```
$ git status --short
 M PROJECT_STATE.html
A  docs/work/queued/WI-499-oi31-reconstruction.md

$ gen_trajectory.py --check                       # the WORKING TREE — what the hook sees
project-state dashboard up to date.                                    EXIT=0

$ git checkout-index -a -f --prefix=$T/ && gen_trajectory.py --check --root $T
project-state dashboard STALE in PROJECT_STATE.html: run `python scripts/gen_trajectory.py`
                                                                       EXIT=1

$ check.py --staged-divergence
  WARN  staged-divergence  1 declared generated artifact(s) modified in the working
  tree but NOT staged — the freshness steps just passed on bytes this commit will
  not contain:
      PROJECT_STATE.html
                                                                       EXIT=0
$ git add PROJECT_STATE.html && check.py --staged-divergence
  ok    staged-divergence  none of the 9 declared generated artifact paths is
  modified-but-unstaged.                                               EXIT=0
```

The same state under the hook's exact twelve-step floor line reports
`PASS  staged-divergence` with the WARN body — warn-first, confirmed end to end.

**Tests** (`tests/test_check_harness.py`, five cases): the positive
(regenerated-but-unstaged → named, `--strict` → exit 1), clean tree → silent,
modified AND staged → silent, non-git directory → SKIP/exit 0 (plus a
no-census SKIP), and `--strict` alone refused. The fixture declares a census
(`HOUSE_DASHBOARD.html`, a prefix row, a marker row) that **no kit script
knows**, so a hardcoded artifact list could not produce the finding — the
"read, not copy" claim is what the positive case measures. **Bite proved by
mutation**, both directions: `hits = []` fails the positive case
(`assert 'WARN' in out` → "none of the 3 declared…"), and removing the census
filter (`_declared_generated → True`) fails it on the undeclared `notes.md`
appearing. Tree restored after each; 13/13 green before and after.

They live in `test_check_harness.py` rather than beside the census in
`test_generated_freshness_wiring.py`, which is the more natural home: they build
real git repos and that module is in the SMOKE tier, whose membership budget
(`docs/stack.ini [smoke-budget] max-tests`) is a shared dial this lane did not
own. A pointer comment at the census names where they went.

**RESYNC_PACK.md** §3 gains one entry, "Your pre-commit hook gains a
`staged-divergence` step" `[since 4b8f9ab4]` — anchored at the preceding commit
per §3's convention, since the landing SHA is not knowable while writing it.

**Ratchet.** `check.py` 1884 → **2096 MEASURED** (+212), re-stamped in
`tests/test_module_size_ratchet.py` with the reason at the entry: ~55 lines are
mechanism, the rest is the recorded WHY — the ruling's own honest gap and the
three wiring decisions. Trimmed once before stamping (2086 → 2084) by merging
the step comment's opening into the pointer at `staged_divergence()`. The
COMPLEXITY ratchet is untouched: `main()` sat at its baseline and the two new
branches took it 16 → 18, so they were decomposed into `_divergence_mode()`
rather than re-stamped, which is the ratchet's stated rule.

**`PROCESS_OPTIONS.md` deliberately untouched.** That file holds opt-in layers,
each with an *applies-when*. This step has none: it is unconditional, self-
degrading, dial-free and adds no new artifact or registry column. Its
documentation is the hook's floor commentary, `check.py`'s usage block and the
re-sync entry. Editing a byte-watched core doc to say "this always runs" would
be paying the budget for no reader.

**Verification.**

```
$ ./.venv/bin/python -m pytest -q tests/test_check_harness.py \
    tests/test_generated_freshness_wiring.py tests/test_pre_commit_hook.py \
    tests/test_bootstrap.py tests/test_module_size_ratchet.py \
    tests/test_complexity_ratchet.py tests/test_resync_pack.py \
    tests/test_dogfood_sync.py
159 passed, 2 skipped in 79.96s (0:01:19)

$ ./.venv/bin/python -m pytest -q -n auto -m smoke
1201 passed, 7 skipped in 33.80s

$ ./.venv/bin/ruff format --check project-trajectory/scripts/check.py \
    tests/test_check_harness.py tests/test_generated_freshness_wiring.py \
    tests/test_module_size_ratchet.py
4 files already formatted
$ ./.venv/bin/ruff check <the same four>
All checks passed!            # (test_module_size_ratchet's pre-existing F601
                              #  duplicate `bootstrap.py` key is another lane's,
                              #  verified against HEAD before touching the file)
```

**Reported, not changed.**

- The divergence step matches a marker-pair row (`docs/status.md`) on the whole
  FILE, so a hand edit to the non-generated part of `status.md` left unstaged is
  reported too. Correct-but-broad; narrowing it would mean parsing the marked
  region out of two trees, which is option (a)'s work.
- It sees only TRACKED modifications. A generated artifact that was never
  `git add`ed at all is invisible to `git diff --name-only`; the shape that
  actually happened is the forgotten re-`add`, so the untracked case is left
  with the staged-while-stale one for the destination.
