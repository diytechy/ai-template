# WI-962 implementation plan: the hooks read the policy through one parse

Planner: a fresh session (Claude Opus), 2026-10-20. Sources read: the spec
`docs/work/active/wi-962/WI-962-hooks-one-tomllib-read.md`, its specref
(`docs/plans/2026-10-11-review-churn/README.md` item 10, "Owner rulings" row
10 and "Resolved (revision 5)"), the three shipped hooks and
`hooks/kit-python.sh`, `scripts/check_privacy.py`, the hook and
process-config test modules, and the SR, TC, LLR, IF and CMP rows below. Code
was read in the lane worktree `C:/Projects/ai-template.wt/wi-962`.

DELTA: within

**The architectural-delta answer.** Yes on three of the four, and every one
is carried by this plan's rows:

- *An output depends on a new input.* `pre-commit` and `commit-msg` exits now
  depend on whether `docs/process.toml` parses (a malformed file refuses
  where today it proceeds), and `commit-msg` and `pre-push` exits depend on
  whether a set `KIT_SCRIPTS_DIR` names a directory (today they fall back).
- *A value is added to a domain.* The hook outcome domain gains the
  "unreadable declaration" and "failed policy read" refusals.
- *A new boundary is crossed.* The hooks stop reading `docs/process.toml`
  (IF-037) and read instead one answer from the kit's privacy checker on
  stdout: a new seam between two CMP-007 endpoints. Nearest existing row:
  IF-043 (`scripts/check_privacy` to `hooks/pre-push`, exit-code, the range
  scan verdict). It falls short because it is an exit-code verdict of a scan,
  consumed by pre-push only; the new seam is a token answer about the
  policy, consumed by all three hooks. P5 adds that row and trims IF-037's
  consumers.
- *No new state.* Nothing is written; the read is made at each hook run.

No sub-component split: the read is a new function and CLI mode on the
checker that already owns the privacy gate, and a new function in the probe
file the three hooks already source. No refactor outside this item is needed.

## The design, decided

**Where the parse lives.** `check_privacy.py` (the spec's recommendation, so
one parser serves SR-031). Its `_process_gate` already reads `[policies]`
with `tomllib`, with `utf-8-sig` for the byte-order mark and the textual
fallback for keys the parser does not place. The plan gives the checker one
loader that the hook answer and `read_privacy_enabled` share, so a hook run
parses the file once.

**The checker side (P2).** In `project-trajectory/scripts/check_privacy.py`:

1. `_load_process_toml(root)`: one read of `docs/process.toml`, returning one
   of: absent (no path exists at all); loaded (the parsed table); unreadable
   with the message (`OSError`, including a directory at that path,
   `UnicodeDecodeError`, `tomllib.TOMLDecodeError`). "Absent" is
   `not path.exists()`, not `not path.is_file()`, so a directory at the path
   is unreadable rather than absent.
2. `_process_gate(root, key, loaded=None)` and `read_privacy_enabled(root,
   loaded=None)` take the loaded result instead of re-reading. Their answers
   do not change. An unreadable file still reads ON in the checker, which
   cannot refuse. The hook refuses before any checker scan runs, so the D-006
   refusal comes from the hook's read and the checker's fail-closed posture
   stays as it is.
3. `read_privacy_review(root, loaded=None)`: the new Python reader of the
   unwired-reviewer posture (none exists today, per the spec). It returns
   `warn-unwired` only when `[policies] privacy_review` is the string
   `"warn-unwired"` exactly. Any other value under `[policies]`, including a
   wrong type, is `require`. A key the text declares but `tomllib` does not
   place under `[policies]` (a multi-line-string decoy, a wrong section) is
   `require`, the same fail-closed posture `_process_gate` takes. With no key
   at all, the legacy `docs/privacy-review` answers through
   `_first_declared_line` (exactly `warn-unwired` opts down). Absent
   everywhere, the answer is `require`.
4. `hook_policy_answer(root)`: one load, then exactly one of five tokens:
   - `refuse=unreadable`: the file is present but unreadable or unparseable.
     The parser's or OS message goes to stderr, prefixed
     `check_privacy: docs/process.toml:`.
   - `refuse=mixed`: `_process_gate(root, "privacy_check", loaded) is not
     None` and `docs/privacy-check` is present. This is today's hook rule
     (the broad textual "declared" test plus the legacy file's presence), so
     the decoy shapes behave as today. Only the privacy-check pair is mixed
     at the hooks, as today and as the Trust ruling states.
   - `privacy=off`: the review posture is moot (D6's second sentence).
   - `privacy=on review=require`
   - `privacy=on review=warn-unwired`
5. CLI: `--hook-policy` joins the existing mutually exclusive mode group and
   is dispatched before the "both layers OFF, nothing to check" early return.
   It writes the token with `sys.stdout.write(token)`, with **no trailing
   newline**. On Windows a text-mode `print` writes `\r\n` to a pipe, and
   Git-for-Windows `sh` keeps the `\r` in `$(...)`, so the hook would refuse
   every answer. Exit 0 on any token. An uncaught exception exits nonzero,
   and the shell refuses that (D5).
6. Function and header comments: `# Implements: SR-031, LLR-021` on
   `hook_policy_answer` and `read_privacy_review`. A `Contract IF-<new>:`
   line goes in the module header beside its existing contract lines, so the
   new IF row's definition gate finds its home. The `_process_gate` and
   `_text_declares` docstrings that describe "a pure-sh `grep -E` in the
   hooks" are reworded: the hooks now ask this reader, and the textual
   fallback stays only until the shape-rule row (spec S1) retires it.

**The probe side (P3).** `project-trajectory/hooks/kit-python.sh` gains
`kit_policy <hook> <commit|push>`, defined after `kit_python` and called
right after it. In order:

1. **One scripts-directory rule** (pre-commit's today, now for all three
   hooks). If `KIT_SCRIPTS_DIR` is set, the directory is resolved (absolute
   as given, else under `$REPO_ROOT`), and a path that is not a directory
   refuses with **no fallback**. If it is unset, `scripts` then `Scripts`.
   If none is found, refuse. The refusal text keeps every phrase the
   existing tests assert ("cannot find the kit scripts dir", "REFUSING the
   <commit|push>", "KIT_SCRIPTS_DIR in the delegating wrapper", "re-run
   bootstrap", "git config --unset core.hooksPath"). The loop variable is
   `sd`, never `cand`: `tests/test_run_devsetup.py` `_launcher_search`
   unpacks exactly one `for cand in` line from this file.
2. **One read.** `if ! KIT_POLICY=$("$PY" "$SCRIPTS_DIR/check_privacy.py"
   --root "$REPO_ROOT" --hook-policy); then` refuse, naming the read and its
   failure. This is explicit, because `set -e` is suspended inside a
   function called in an `||` list.
3. **Exact tokens only.** A `case "$KIT_POLICY" in` covers the five tokens
   (each refusal returns 1 after printing):
   - `privacy=off`: sets `KIT_PRIVACY=off`.
   - `privacy=on review=require`: sets `KIT_PRIVACY=on` and
     `KIT_REVIEW=require`.
   - `privacy=on review=warn-unwired`: sets `KIT_PRIVACY=on` and
     `KIT_REVIEW=warn-unwired`.
   - `refuse=mixed`: prints the one mixed refusal for all three hooks. It
     names `docs/process.toml`, `docs/privacy-check` and the
     `bootstrap.py --migrate-config --dest .` migrator, in pre-commit's
     current wording with the hook name as `$1`.
   - `refuse=unreadable`: names `docs/process.toml`, says the parser's
     message is printed above, and says to fix the file (the fixing commit
     passes because the hook reads the working tree).
   - `*)`: names the answer and refuses as outside its tokens.
4. Bash 3.2 and POSIX discipline: no `${VAR:-word}` with a quote in `word`
   (the WI-909 shape `test_shell_portability` refuses), no `[[`, no
   `local`, no arrays.

**The hooks (P4).** They lose their text reads and their own
scripts-directory blocks, and call `kit_policy` once, directly after
`kit_python`:

- `hooks/pre-commit`: delete `_ptoml_body`, `process_declares`,
  `mixed_config_refusal` and its call (56-93) with their comment block
  (44-55), and the scripts-directory block (101-131). Add `kit_policy
  pre-commit commit || exit 1` after line 99.
- `hooks/commit-msg`: delete 29-74 and the scripts-directory block (91-120).
  Add `kit_policy commit-msg commit || exit 1` after line 89.
- `hooks/pre-push`:
  - Delete `find_scripts_dir` (59-74), the `PROCESS_TOML`/`PRIVACY_FILE`
    variables, `_ptoml_body`, `process_declares` and the pre-probe mixed
    refusal (76-118). Also delete `privacy_declared_true` (126-148), the
    scripts-directory refusal (150-160) and the `privacy_review` read
    (201-220).
  - Add `kit_policy pre-push push || exit 1` after line 124.
  - Line 162 becomes `if [ "$KIT_PRIVACY" = off ]; then`, so anything but
    an exact `off` takes the review path and the hook fails closed.
  - `review_policy="$KIT_REVIEW"` replaces the removed block.
  - The header and dump `echo` texts that name `docs/privacy-check` or
    `docs/privacy-review` as the live home are reworded to "the privacy
    gate" or the `[policies]` key. They are messages, not reads; rewording
    them only stops them misdirecting.

The mixed refusal therefore moves after the interpreter probe in all three
hooks. On a machine with no Python 3.11+, the interpreter refusal names the
fix (spec Deliverable 2).

## The plan table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Tests first: the new and rewritten hook-read tests, red on today's code | D1; D2; D3; D4; D5; D6; D7; D9; SR-031; SR-019; SR-020; TC-031; TC-021; TC-019; TC-020 | IF-134; IF-135; IF-037; Proposed: the hook-policy answer seam, nearest IF-043 (a pre-push-only exit-code scan verdict, not a token answer about the policy for all three hooks) | |
| P2 | Checker: one loader, the review reader, the token answer and its --hook-policy CLI | D4; D5; D6; SR-031; TC-031 | IF-037; IF-043; Proposed: the hook-policy answer seam, nearest IF-043 (exit-code scan verdict to pre-push only; the new seam is a stdout token set for all three hooks) | P1 |
| P3 | Probe: kit_policy in kit-python.sh with one scripts-dir rule, one read, exact tokens | D3; D5; D7; D8; SR-019; SR-020; SR-031; TC-021 | IF-134; IF-135; Proposed: the hook-policy answer seam (requestor side), nearest IF-043 as in P2 | P2 |
| P4 | Hooks: delete every text read and the per-hook scripts blocks; call kit_policy once after kit_python | D2; D3; D5; D6; D7; SR-019; SR-020; SR-031; TC-019; TC-020; TC-021 | IF-134; IF-135; IF-043; IF-197 | P3 |
| P5 | Records: SR-031, TC-031, LLR-021, TC-021 amended; IF-037 consumers trimmed; the new IF row; Flow 3; two prose claims corrected | D10; SR-031; SR-019; SR-020; TC-031; TC-021 | IF-037; Proposed: the new hook-policy answer row itself, nearest IF-043 (exit-code verdict of a scan, consumed by pre-push alone) | P4 |
| P6 | RESYNC entry for the forced changes | D11; SR-031; SR-019; SR-020 | IF-134; IF-135 | P4; P5 |
| P7 | Verify and land: targeted slow modules, one scaffold bootstrap, commit bar, strict lints, regenerated artifacts | D8; D9; D12; SR-031; SR-019; SR-020; TC-019; TC-020; TC-021; TC-031 | IF-134; IF-135; IF-037 | P5; P6 |

Every SR of the item (SR-031, SR-019, SR-020) is cited by rows. Every TC
verifying one of them (TC-019, TC-020, TC-021 and TC-031, the whole set the
test-case registry returns for those three SRs) is named by rows. No clause
is excluded.

**Why a clause appears in more than one row.** This is a stated split, not
duplicated scope:

- P1 writes a clause's test, red.
- P2, P3 and P4 build the checker, the probe and the hook part of that one
  behaviour. A hook clause (D5, D6, D7) needs all three layers.
- P7 runs the guards and the bootstrap that D8 and D9 name.

No two rows build the same thing.

## P1: the tests, and what each fails on before the change

D1 binds the tests this item adds or rewrites. Each fails on today's tree for
the reason given. Two existing guards are run, not added, and cannot fail
before because they pin a property today's code already has. They are named
as such under P7: `tests/test_shell_portability.py` for D8, and the TC-021
probe tests.

`tests/test_process_config.py` (slow tier, `conftest.SLOW_MODULES`; its
comment "the hooks' `sh` reader run as a subprocess per shape" becomes "the
real pre-push hook driven per shape"):

- **Deleted**, because the functions they extract are gone:
  `sh_privacy_declared_true`, `_extract_function`,
  `test_the_hook_sh_and_tomllib_agree_on_every_shape`,
  `test_an_unparseable_file_reads_ON_in_both_readers`,
  `test_a_shape_the_hooks_cannot_follow_is_refused_and_still_reads_ON`,
  `test_both_hooks_carry_the_same_reader_byte_for_byte`, and the
  `sh_privacy_declared_true` line of
  `test_the_legacy_arm_still_works_with_no_toml_at_all`. Its Python
  assertion stays, and its hook half joins the table below.
- **New helper `hook_privacy_answer(tmp_path)`.** It drives the **real**
  shipped hook, not an extracted function, in a minimal git repo:
  - `.githooks/pre-push` and `.githooks/kit-python.sh` are copied
    byte-for-byte from `KIT/hooks`, and `KIT_SCRIPTS_DIR` is set to the
    POSIX form of the absolute `KIT/scripts`.
  - One commit, authored by the noreply identity `test_pre_push_hook` uses,
    with the lint-identity variables pinned to its `FAKE_USER`.
    `REVIEW_CMD` is unset and no `privacy.reviewcmd` is configured.
  - One push line for HEAD against the zero sha.
  - Answers: `off` when the hook exits 0 with no review demand; `on` when
    it refuses with "FAILING CLOSED"; `refused:<stderr>` for a policy
    refusal.
  - It runs under `skip_without_env_gates("posix-shell", "git")`.
- **`test_the_shipped_hook_and_the_checker_agree_on_every_shape`**, the D4
  pin. It is parametrized over the adversarial table: the existing `SHAPES`
  rows (trailing-comment decoys both ways, BOM, CRLF, commented decoy,
  similar key, absent), plus the `NON_GREPPABLE` shapes (dotted key, inline
  table, multi-line string, wrong section), each in a **true and a false
  variant**, plus wrong-type rows (`privacy_check = "false"`,
  `privacy_check = 0`). It asserts `hook_privacy_answer` equals
  `check_privacy.read_privacy_enabled`, and the `expected` column where
  given.
  - Fails before on the `multiline-string-false` (`note = """\nprivacy_check
    = false\n"""`) and `wrong-section-false` (`[attestation]\nprivacy_check
    = false`) rows. There today's hook reads OFF (its keyed grep sees a
    provably-`false` line) while the checker reads ON (the textual fallback),
    a live fail-open divergence the current table never drove because its
    non-greppable rows are all `true`.
- **`test_every_hook_refuses_an_unreadable_policy_file[hook x case]`** (D5).
  The hooks are `pre-commit`, `commit-msg` and `pre-push`, each with its
  probe copied in the same minimal repo. The cases are `malformed`
  (`[policies\n...`), `uppercase-TRUE`, `bare-word`, `undecodable` (bytes
  `b"\xff\xfe[policies]\n"`), and `directory` (a directory at
  `docs/process.toml`). Each hook must exit nonzero, name
  `docs/process.toml`, and for `malformed` carry the parser's message.
  - Fails before: today `pre-push` with no reviewer reads these as ON and
    refuses for the reviewer, not the file. `commit-msg` and `pre-commit`
    run past the read, and no "cannot be read or parsed" text exists.
- **`test_every_hook_refuses_a_mixed_config_with_one_text`** (D5).
  `[policies] privacy_check = false` plus `docs/privacy-check`. All three
  hooks refuse, naming `docs/process.toml`, `docs/privacy-check` and
  `--migrate-config`, and their refusal texts are identical once the hook
  name is removed.
  - Fails before: `pre-push`'s mixed text differs from the other two today
    (pre-push lines 114-116 against pre-commit 86-89).
- **`test_every_hook_refuses_a_failed_or_foreign_policy_answer[hook x
  stub]`** (D5). `KIT_SCRIPTS_DIR` names a temp directory holding a stub
  `check_privacy.py`: one exits 3, one writes `privacy=maybe`, one writes
  nothing, one writes `privacy=off\r`. Each hook must refuse and name the
  read.
  - Fails before: today `pre-push` runs the stub as its range scan and
    passes on exit 0, `commit-msg` and `pre-commit` die on the missing
    `check.py` without the read's refusal text, and no hook reads such an
    answer at all.
- **`test_the_mixed_refusal_runs_after_the_interpreter_probe[hook]`** (D3,
  behavioural). Mixed config plus the no-interpreter `PATH` stand-in the
  TC-021 tests use. Each hook must refuse naming dev-setup and 3.11, and
  must not print the mixed text.
  - Fails before: today the mixed refusal runs first (pre-commit 93,
    commit-msg 74, pre-push 113).
- **`test_the_hook_answer_and_the_checker_agree_in_process`**, the
  in-process pin of the same table. `check_privacy.hook_policy_answer(root)`
  maps to `read_privacy_enabled(root)` on every D4 row, and
  `refuse=unreadable` on every unreadable case.
  - Fails before: `hook_policy_answer` does not exist.

`tests/test_pre_push_hook.py` (slow tier):

- **`test_the_review_posture_follows_the_one_parse[case]`** (D6), on the
  scaffold `repo` fixture with no reviewer wired.
  - Privacy on:
    - `privacy_review = "warn-unwired"` warns and proceeds.
    - `"require"`, the typo `"warn-unwried"`, `privacy_review = 1` and
      `privacy_review = "WARN-UNWIRED"` refuse with "FAILING CLOSED".
    - The key removed from `[policies]`, with no legacy file, refuses.
    - The key removed, with legacy `docs/privacy-review` reading
      `warn-unwired`, warns and proceeds. With legacy `require`, it refuses.
    - Decoys appended to the scaffold file refuse: `[decoy]\nprivacy_review
      = "warn-unwired"`, and `[decoy]\nnote = """\nprivacy_review =
      "warn-unwired"\n"""`.
  - Privacy off: with `privacy_review` absent, `"require"`, `1` or a typo,
    the push proceeds.
  - Fails before on both decoy rows. Today's grep finds `privacy_review =
    "warn-unwired"` on a non-comment line in another section or inside a
    string, and warns and proceeds where the parse reads `require` (a
    fail-open). The other rows are the table's controls.
- **`test_pre_push_refuses_a_kit_scripts_dir_naming_a_missing_directory`**
  (D7). Scaffold `scripts/` present, `KIT_SCRIPTS_DIR=nope-not-here`: the
  push must refuse with the scripts refusal text.
  - Fails before: `find_scripts_dir` (pre-push 64-74) falls back to
    `scripts/` and the push passes.

`tests/test_pre_commit_hook.py` (slow tier):

- **`test_every_hook_refuses_a_kit_scripts_dir_naming_a_missing_directory[hook]`**
  (D7). Scaffold with `scripts/` present, `KIT_SCRIPTS_DIR=nope-not-here`,
  for `pre-commit` and `commit-msg`. Each must refuse and pass
  `_assert_names_the_scripts_refusal`.
  - Fails before on `commit-msg`: lines 102-109 fall back to `scripts/` and
    the commit passes. `pre-commit` is the control that already refuses.

`tests/test_shell_portability.py` (smoke tier: the structural pins stay in
the commit bar):

- **`test_no_hook_reads_the_policy_as_text`** (D2). In each of
  `hooks/pre-commit`, `hooks/commit-msg`, `hooks/pre-push` and
  `hooks/kit-python.sh`, every non-comment line that names `process.toml`,
  `privacy-check` or `privacy-review` must be an `echo` or `printf` message
  line. No `grep`, `sed`, `awk`, `head`, `cat`, `[ -f` or redirect may touch
  them.
  - Fails before: `_ptoml_body`/`process_declares` call sites, pre-push 81-82
    and 145-146, and 209-219.
- **`test_each_hook_runs_the_one_read_once_after_the_probe`** (D3,
  structural). Each hook has exactly one `kit_policy <its name>` call line,
  after its `kit_python <its name>` line. `kit-python.sh` holds exactly one
  `--hook-policy` invocation and exactly one `for cand in` line. No hook
  names `--hook-policy` or `KIT_SCRIPTS_DIR` itself.
  - Fails before: no `kit_policy` exists, and every hook resolves
    `KIT_SCRIPTS_DIR` itself.

`tests/test_bootstrap.py` (slow tier):

- **`test_a_fresh_scaffold_ships_the_probe_and_commits_through_its_hooks`**
  (D9). Bootstrap a scaffold and check that `.githooks/kit-python.sh`,
  `pre-commit`, `commit-msg` and `pre-push` are byte-equal to `KIT/hooks`
  and that the probe defines `kit_policy`. Then `make_minimal_project`,
  `git init`, `pin_autocrlf`, `core.hooksPath .githooks`, `git add -A` and
  `git commit -m "feat: first"`: the commit must succeed through both
  commit hooks.
  - Fails before: the shipped probe has no `kit_policy`.

## P2 to P4: the build

Laid out under "The design, decided" above. Each step turns its tests in P1
green:

- P2 turns `test_the_hook_answer_and_the_checker_agree_in_process` green.
- P3 and P4 together turn every hook-driven test and both structural pins
  green.

## P5: the records

Amendments to approved rows follow the kit's approved-row amendment rule (the
builder reads the `spine-authoring` skill and
`docs/registry-machinery-reference.md` before editing). They are judged at
the lane's sitting (D10). No row names code, per the 2026-10-11
"requirements never reference code" ruling.

- **SR-031** (`docs/requirements/system-requirements.toml`).
  - `acceptance_criteria` becomes the Done-when draft, verbatim: "Every
    enforcer reads the same value for the same dial through one parse; the
    hooks' and the checkers' answers agree over the adversarial file-shape
    table, the trailing-comment decoy included, and an unreadable
    declaration refuses at the hooks rather than reading a default."
  - `coincident` drops "the two delivered reader grammars returning the
    same answer" for: "Every enforcer reading the same value for the same
    dial through one parse, the hooks' and the checkers' answers agreeing
    over that adversarial table with the trailing-comment decoy included,
    and an unreadable declaration refusing at the hooks, is that pinned
    equality, a property of the delivered code with no outside party in
    it."
  - The `requirement` text already says "one parse, one answer" and stays.
- **TC-031** (`docs/test/test-cases.toml`).
  - `method`: "Drive each shipped commit and push hook over the adversarial
    file-shape table and compare its answer with the checker's for every
    shape; drive an unreadable declaration and a mixed one through each
    hook; run the policy suites: every enforcer reads one value per dial."
  - `evidence` gains `tests/test_process_config.py` before the two suites it
    names.
- **LLR-021** (`docs/requirements/low-level-requirements.toml`).
  - `detail` keeps its probe sentences and appends: "After the interpreter
    check, the probe resolves the kit scripts directory once for all three
    hooks: an override that names no directory refuses with no fallback;
    with none named, the default directory in either case; none found
    refuses. It then asks one parse of the declared policy, once per hook
    run, for a closed answer: the privacy gate off; on with the unwired
    reviewer required; on with it warned; a mixed declaration; or an
    unreadable one. A hook acts only on an exact answer; a mixed or
    unreadable declaration, a failed read or any other answer refuses the
    commit or push, naming the cause."
  - `sr_refs` gains SR-031, since the read it now carries serves that
    row. This is flagged for the sitting as the one parent change.
- **TC-021**, because it verifies LLR-021 and LLR-021 gains obligations.
  - `method` gains: "drive each hook with a scripts override naming a
    missing directory, with an unreadable or mixed declaration, and with a
    policy answer that fails or falls outside its set; inspect that each
    hook makes the one read once, after the probe."
  - `expected` gains the matching refusals.
  - `evidence` gains the P1 test ids in the D3, D5 and D7 bullets.
  - D10 does not list TC-021. It is added because an LLR whose only TC
    does not exercise its new sentences is a coverage hole. The sitting
    judges it with the others.
- **IF-037** (`docs/requirements/interfaces.toml`). `consumers` drops
  `hooks/pre-commit`, `hooks/commit-msg` and `hooks/pre-push`: they no
  longer read the file, they read the checker's answer. The `data` cell
  ("one key = value per line") is the shape-rule row's (spec S1) and stays.
- **The new IF row** (CMP-007, `Drafted`, its id taken through the kit's
  mint, never by hand):
  - `owner`: `scripts/check_privacy`.
  - `requestors`: `hooks/pre-commit`, `hooks/commit-msg` and
    `hooks/pre-push`.
  - `channel`: `stdout`.
  - `data`: "one answer, no newline: privacy=off | privacy=on
    review=require | privacy=on review=warn-unwired | refuse=mixed |
    refuse=unreadable (cause on stderr); a nonzero exit or any other answer
    is refused by the hook".
  - `rationale`: the three hook gates need one parse's answer rather than
    their own reading of the file.
  - `notes`: intra-component.
  - The checker's module header gains the matching `Contract IF-<id>:`
    line (P2).
- **Components** (`docs/requirements/components.toml`). No new component:
  CMP-007's notes already cover the shipped hooks and `check_privacy`. The
  derived view (`components.derived.toml`) is regenerated at landing, not
  hand-edited.
- **Runtime flows** (`docs/runtime-flows.md`, Flow 3).
  - A `Probe as kit-python.sh (LLR-021)` participant is added. The hook
    asks it for the interpreter, the scripts directory and the policy
    answer.
  - One `alt` returns REFUSE for an unavailable scripts directory, a mixed
    or unreadable declaration, or a failed or foreign answer
    (SR-019/SR-020/SR-031).
  - The `Priv->>Policy` arrow is labelled as the one parse
    (SR-031/LLR-021, LLR-031).
- **Two prose claims corrected**, because each states hook behaviour this
  item removes:
  - `project-trajectory/PROCESS_OPTIONS.md` line 56 ("the git hooks read
    the privacy dials in pure sh, so a Python-less box still fails closed")
    becomes "the shape is checked; since the hooks refuse without Python
    3.11 they read the privacy dials through one parse". The
    `byte-budget-guard` skill runs before and after the edit.
  - The root `README.md` line 489 gets the same correction.
  - Not edited here: the `process.toml.template` and `docs/process.toml`
    header comments and their "KEYED-GREPPABLE" lines. They document the
    shape rule itself, which stays in force until the spec's S1 successor
    row deletes it with them. So does `agent_policy.config_conflicts`'
    "while the git hooks keep acting on the text" string. The plan names
    these three as that row's hand-over.

## P6: the RESYNC entry

A new `project-trajectory/RESYNC_PACK.md` §3 entry, anchored at the lane's
trunk base as the commit bar requires: "### The hooks read the policy through
one parse; a malformed policy file refuses [since <trunk-base sha>]".

- **What changed.** The three hooks and their probe read
  `docs/process.toml` and the legacy `docs/privacy-check` and
  `docs/privacy-review` through one call to the checker, after the
  interpreter check, instead of with `grep`. All three hooks share one
  scripts-directory rule.
- **Forced changes.**
  - A present but unreadable or unparseable `docs/process.toml` now
    refuses every commit and push, naming the file and the parser's
    message, where it read as privacy ON. Fix the file; the fixing commit
    passes, because the hook reads the working tree.
  - `commit-msg` and `pre-push` now refuse a `KIT_SCRIPTS_DIR` naming a
    missing directory, as `pre-commit` already did. Fix the delegating
    wrapper.
- **Also observable.** `privacy_review` counts only under `[policies]`. A
  copy in another section or inside a string no longer opts down (the
  stricter direction).
- **Kit-owned files, overwrite:** `hooks/pre-commit`, `hooks/commit-msg`,
  `hooks/pre-push`, `hooks/kit-python.sh` (each shipped as `.githooks/*`,
  `kitlib/bootstrap_manifest.py:768`), and `scripts/check_privacy.py`.
- **Adopter-merged files:** none. No registry, setting or record format
  changes.

## P7: verify and land

- Run the slow modules this item touches, by name: `tests/test_process_config.py`,
  `tests/test_pre_push_hook.py`, `tests/test_pre_commit_hook.py`,
  `tests/test_bootstrap.py`, `tests/test_run_devsetup.py` (the
  `kit-python.sh:hooks` search pair) and `tests/test_meta_repo_hook.py`
  (this repo's wrappers set `KIT_SCRIPTS_DIR=project-trajectory/scripts`,
  which still resolves). Paste the output.
- **D8:** `tests/test_shell_portability.py` over the edited
  `kit-python.sh`. This is an existing guard, which passes before because
  the file parses today; it runs here as the bash 3.2 regression check
  rather than as a D1 test.
- **D9:** one scaffold bootstrap by hand as well as the P1 test. Bootstrap
  into a temp directory, set `core.hooksPath .githooks`, and commit through
  the shipped hooks. Then check one push-hook refusal on a malformed
  `docs/process.toml`.
- The derived artifacts the commit floor's freshness steps name are
  regenerated per the `coordinator-cycle` landing recipe:
  `docs/interface-reference.md` for the IF edits, the component view and
  the trajectory map (`gen_arch_map --src`).
- **D12, on the landing tip:** the commit bar (`run.cmd smoke`) is green
  within its 60 s budget, and
  `project-trajectory/scripts/check_trajectory.py --strict` and
  `project-trajectory/scripts/trace.py --strict` are clean, with their
  output pasted. The smoke tier gains only the two structural pins in
  `test_shell_portability.py`. Each hook run gains one interpreter spawn
  for the read, and no smoke test drives a hook.

## Risks the builder should watch

- **Windows CR in the token** (P2 item 5). The answer is written without a
  newline. The `privacy=off\r` stub case pins that the shell does not
  silently accept a near-token.
- **`set -e` inside `kit_policy`.** It is suspended under `||`, so every
  failure path needs its explicit `return 1`.
- **The decoy class** named in the specref's trade-off: a gate that reads
  off from text a parser reads as on. After this item no hook holds text;
  the D4 table and the D2 structural pin are its guard.
- **WI-817 overlap** (spec S6). It edits `check_privacy.py` and retires the
  legacy branches. If it lands second, it deletes them from
  `_load_process_toml`'s callers in one place.
