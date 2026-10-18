# WI-927 plan (revision 2): the guard hooks checked by name, installed with consent, refused when occupied

Spec: `docs/work/active/wi-927/WI-927-guard-hooks-by-name.md` (specref
`docs/specs/WI-927.md`, the owner's direction: D-011, D-019, D-021 of
coordinator-2026-10-15). Delivers SR-032 and SR-229. Read in the lane worktree
at `ce808bee8`. This revision answers `docs/plans/WI-927/critique-1.md`.

## What changed from revision 1, and why

**F1 is confirmed on the code.** At `ce808bee8`,
`coordinator_guard._guard_plan` calls `guard_hooks.command_shapes`, and
`hooks_state` and `enable_hooks` call `guard_hooks.merged`
(`coordinator_guard.py` lines 1498-1538). Revision 1's P1 deleted those
helpers and added a test asserting `coordinator_guard` has no `enable_hooks`,
while the consumers and `enable_hooks` changed only in P2. P1's commit would
therefore have broken every hooks route and failed its own new test.

Checking the same path one step further found a second break of the same
kind, which the critic did not name. Revision 1's P2 changed the `hooks`
command's words (`off` becomes `absent`) and removed `--enable`, while the
four dev-setup files that read those words and call `--enable` changed only
in P4. Between those commits:

- all four copies test for `off` (template sh lines 256 and 299, template
  ps1 lines 216 and 251, root sh lines 241 and 246, root ps1 lines 212 and
  217), so the `[note]` line and the offer would vanish;
- each offer would call a flag argparse refuses.

`test_this_repos_readiness_report_names_the_hooks_opt_in` would fail at that
commit.

So the revision does two things:

- **P1 is additive only.** It adds the pure reader beside the old helpers
  and deletes nothing.
- **The producer/consumer replacement is one atomic step, P2.** In one
  commit it covers both sides of the swap:
  - in `coordinator_guard.py`: `hooks_state` over the reading, the install,
    the `hooks` report's four words, `--offer`, and `--enable` removed;
  - every consumer of that CLI: the four dev-setup files and the five tests
    that call `enable_hooks` or `--enable`
    (`tests/test_blackout_window.py` lines 1074, 1075 and 1094;
    `tests/test_run_devsetup.py` lines 359, 1170 and 1171);
  - the deletion of the old helpers, with the deletion assertion.

  Revision 1's P4 (dev-setup) is folded into P2. The take, the spine and the
  resync follow as P3-P5.

Each step now states its green done-condition. Nothing else in the design
changes.

## The architectural-delta answer

DELTA: within

The work item does three of the four.

- It **adds domain values.** The hooks reading's domain goes from
  `{none, on, off}` to `{none, absent, on, occupied}`.
- It makes **an output depend on a new input.** The lease take's answer now
  depends on three things it never read before: the machine-local
  `.claude/settings.local.json`, `.claude/settings.json.example`, and a
  person's answer at a terminal.
- It crosses **a new boundary.** The take reads a file that Claude Code and
  people write, and it reads a terminal.

All of it is inside this item's scope (spec S5), and no other module's
contract has to be refactored first. The rows below carry each change:

- P1: the reading's domain;
- P2: the CLI surface (IF-280) and dev-setup;
- P3: the take's new input and boundary;
- P4: the spine rows.

No sub-component split is needed, and both modules stay where they are:
`kitlib/guard_hooks.py` under CMP-008 by derivation, and the dev-setup
templates under CMP-009.

## What the code reads today (the facts the plan rests on)

- `kitlib/guard_hooks.py` (117 lines, 50 SLOC by the ratchet's census) holds
  seven functions: `guard_groups`, `bind`, `command_shapes`, `merged`,
  `_split_interpreter`, `_owns` and `_without_guard`.
- `coordinator_guard.py` is 954 SLOC. It imports `guard_hooks` (lines 151 and
  158). `_guard_plan` calls `command_shapes`; `hooks_state` and
  `enable_hooks` call `merged`.
- `tests/test_module_size_ratchet.py`'s `BASELINE` holds **no entry for
  either module**. Both are under `THRESHOLD = 1000`, and kitlib modules are
  watched only for crossing it (`test_the_census_sees_inside_packages`). See
  the note on D25 below.
- `coordinator_guard.hooks_state` returns `none`, `on` or `off`. `on` means
  "`merged` would change nothing". `enable_hooks` merges. `_hooks_main` backs
  `hooks --example E [--enable]`. `take(root, session_id, transcript)` never
  reads the hooks.
- Both dev-setup templates and this repo's two copies read the state through
  the `hooks` command and map any failure to `none`:
  - the sh copies: `2>/dev/null) || HOOKS="none"`;
  - the template ps1: `KitReading` returns `""` on a non-zero exit;
  - this repo's ps1: `catch { $hooks = "none" }`.

  Each offer fires on `off`, asks in the shell, and then calls `--enable`.
- The callers of the old surface outside `coordinator_guard.py` are tests
  only:
  - `tests/test_blackout_window.py` lines 1074 and 1075 call `enable_hooks`,
    and line 1094 calls `hooks --enable`;
  - `tests/test_run_devsetup.py` line 359 calls `hooks --enable`, and lines
    1170 and 1171 call `hooks("--enable")`.
- Interactive tests:
  - POSIX drives dev-setup with `pty.openpty()` (`_at_a_terminal`,
    `test_a_denial_changes_no_configuration_or_credential`, skipped on
    Windows).
  - Windows drives a real hidden console with `CONSOLE_TYPIST` and
    `_at_a_console` in `tests/test_run_devsetup.py`. The helper writes key
    events with `WriteConsoleInputW` and skips when the host gives a new
    console no interactive session.
  - `test_run_devsetup` and `test_onboard_devsetup` are in
    `tests/conftest.py`'s `SLOW_MODULES`. `test_blackout_window` and
    `test_coordinator_guard` run in the smoke tier.

## Design decisions the builder follows

1. **The reading is pure and lives in `kitlib/guard_hooks.py`.**
   `read_state(example, settings)` returns `Reading(word, problems)`.
   - **Inputs.** `example` is the parsed example object, or a
     `Problem(text)` when the file could not be read or parsed. `settings` is
     the parsed settings object, `None` when the file is absent, or a
     `Problem`.
   - **The guard events** are the keys of `guard_groups(example)`. If there
     are none, the word is `none`. An unreadable example reads `occupied`,
     with the problem named.
   - **A command is the guard's by name.** After the interpreter word
     (`_split_interpreter`, kept for `bind`), its last two words must be a
     path whose base name, quotes stripped, is `coordinator_guard.py`,
     followed by `hook`. The interpreter word itself is not checked.
   - **`absent`:** every guard event is missing or `[]`, and the settings
     and their `hooks` have the expected shapes.
   - **`on`:** each guard event holds exactly one group, whose `hooks` list
     holds exactly one entry, and that entry is a command that is the guard's
     by name. The group's `matcher` and other keys are not compared, so a
     matcher-only change still reads `on` (deliverable 6).
   - **`occupied`:** everything else. `problems` names:
     - each event with a non-guard command (quoted);
     - each event with more than one group or entry;
     - each missing guard event while others are present;
     - each shape fault from the Trust list: not JSON, not an object,
       `hooks` not an object, an event value not a list, a group without a
       `hooks` list, a command not a string, and an OS error on read.
   - **Untouched:** non-guard events and every other key are never
     inspected.
   - **`refusal_text(path, reading)`** formats the one complaint every route
     prints: the file, each problem, and the fix ("move those hooks to
     another settings file, such as your user `~/.claude/settings.json`, or
     remove them, then run again").
   - **Deleted in P2, not P1:** `command_shapes`, `merged`, `_owns`,
     `_without_guard`, and `_split_interpreter`'s ownership use. The module
     docstring is rewritten in P2.
2. **The file side stays in `coordinator_guard.py`.**
   - **`hooks_state(root, example)`** reads both files and returns the
     `Reading`. An absent example reads `none`, as today. `OSError` and
     `ValueError` become `Problem`s, never exceptions.
   - **`install_hooks(root, example, interpreter=None)`** acts only from
     `absent`, and it is the only writer.
     - It writes `settings["hooks"][event] = [bind(g, interpreter) ...]` for
       each guard event, keeping every other key and event.
     - It writes through `write_atomic`, as today.
     - It then re-reads with `hooks_state` and returns that `Reading`.

     `enable_hooks` and `_guard_plan` are deleted.
   - **`consent_install(root, example, ask)`** is the one consented install
     that both first runs use:
     - at `none` or `on` it returns the reading and asks nothing;
     - at `occupied` it returns the refusal;
     - at `absent` with `ask is None` (no terminal) it returns the
       no-terminal refusal;
     - at `absent` with a terminal it asks one question: "Write the
       coordinator's Claude Code hooks into the machine-local
       .claude/settings.local.json? [y/N] ". This is today's offer, with
       "merging" reworded as "writing" and "keeping any hooks already there"
       dropped, since the slot is empty. Only an answer that starts with `y`
       or `Y` is a yes. A no, an empty line or EOF writes nothing;
     - after a yes, it installs and succeeds only when the re-read reads
       `on`. Otherwise it returns a refusal naming the file and the error:
       the `OSError` text, or the re-read's problems.
   - **`_terminal_ask`** is `input()` behind `sys.stdin.isatty() and not
     os.environ.get("CI")`, the same test dev-setup's `interactive` uses.
     EOF reads as `""`. `main` passes it, or `None` when there is no
     terminal.
3. **The CLI** (IF-280):
   - `hooks --example E` stays the read-only report. It prints the word on
     stdout. At `occupied` it also prints `refusal_text` on stderr and exits
     1 (IF-281's "1 on a refusal").
   - `--enable` is removed, so argparse refuses it with exit 2.
   - `hooks --example E --offer` runs `consent_install` with the terminal
     asker, and it is what dev-setup's offer calls. Without a terminal it
     asks nothing and writes nothing.

   **The consent question lives once, in Python, for both routes.** That is
   the single-source rule the kit preaches, and the Trust section rules the
   consent answer once. The alternative was considered and rejected: keep
   `read`/`Read-Host` in each shell and add a non-interactive `--install`
   flag. It keeps four copies of the question, and it ships a CLI that writes
   the settings with no terminal answer behind it.

   **This goes beyond D29's literal text.** IF-280's data cell does more than
   drop `[--enable]`: it reads `hooks --example E [--offer]`. The checkpoint
   sitting judges it.
4. **The take** (`coordinator_guard.take(root, session_id, transcript=None,
   ask=None)`).
   - **When it reads.** After the session-id check and **before the lease
     lock is taken** (so no lock is held while a person is asked), it runs
     `consent_install(root, root/".claude/settings.json.example", ask)`. It
     returns any refusal unchanged and writes no lease and no event.
   - **Where it reads.** The hooks are read at the `root` the take is given:
     `--root`, or else `CLAUDE_PROJECT_DIR`, the session's project directory.
     Those are the settings Claude Code loads for that session.
   - **The no-terminal refusal:** "the coordinator's Claude Code guard hooks
     are not installed in <file>, and no terminal can consent here: run
     dev-setup at a terminal (the bare `run`, or its install tier) and answer
     yes, then take again."
     - The template's install tier is `--baseline`/`-Baseline`; this repo's
       copy calls it `--install`/`-Install`.
     - The text names "the bare `run`", which is right in both, and names
       both tier spellings.
   - **Not changed:** the successor's take (`on_session_start`, `_install`).
     It runs from the hooks themselves, so they are already installed.
5. **Hooks written mid-session** (deliverable 3's check).
   - Claude Code's hooks reference ("configuration safety") says hooks are
     snapshotted when a session starts. A direct edit to a settings file
     takes effect in the running session only after it is reviewed in
     `/hooks`.
   - So after an interactive install the take goes on and adds: "the hooks
     guard Claude Code sessions started from now on; this running session
     applies them only after a restart or a review in its /hooks menu."
   - The builder re-checks that page at build time and records its URL and
     wording in the lane report. The message stays true even if a newer CLI
     applies hooks immediately.
6. **dev-setup** (both templates and this repo's two copies, in P2).
   - **The report** runs `hooks --example E` and **keeps its exit code and
     stderr**. It does not use the stdout-only `KitReading` for this; that
     helper is unchanged for its other callers. The lines are:
     - exit 0 with `on`: `[ok]`;
     - exit 0 with `absent`: `[note]`, naming the offer, as today's `off`
       line does;
     - exit 0 with `none`: no line, as today;
     - any non-zero exit or empty stdout: one `[missing] coordinator Claude
       Code hooks: <the reader's stderr, or "the hooks reader printed
       nothing">`, counted in `missing`. The occupied refusal reaches the
       report this way, with its file, events, commands and fix.
   - **The other steps go on.** The `--for-run` exit rule (runtime only) is
     unchanged.
   - **The offer.** `offer_hooks`, `OfferHooks` and `Offer-Hooks` run only at
     `absent` at an interactive terminal. They call `hooks --example E
     --offer` with the terminal inherited, never captured. The outcomes:
     - exit 0 and the next reading `on`: "Switched on …";
     - exit 0 with `absent` (declined): "- skipped the coordinator hooks;
       nothing was changed". Python prints it, so the D3 pin's string is
       kept;
     - non-zero: `[missing]` with the stderr.
7. **Size.** `coordinator_guard.py` must stay at or under 1000 SLOC, the
   ratchet's threshold; it has no BASELINE entry to bump.
   - It loses `_guard_plan`, `enable_hooks` and the merge call. It gains
     `install_hooks`, `consent_install` and `_terminal_ask`, about +25 net.
   - If the census reads over 1000, the builder moves `install_hooks` and
     `consent_install` whole into `kitlib/guard_hooks.py` and states it in
     that module's docstring. That is a decomposition, never a bump.

**On D25's "the ratchet's entry shrinks".** No such entry exists today (see
the facts above). The plan delivers the clause's substance instead: no merge
or ownership code, pinned by a test. The lane report gives the census for
`kitlib/guard_hooks.py` before and after. The new reading may leave that
figure above 50 SLOC. The plan surfaces the clause to the checkpoint sitting
as mis-premised, and does not invent an entry.

**Runtime flows.** `docs/runtime-flows.md` draws no sequence for the lease
take or for dev-setup's hooks offer. Flow 5 draws the guard hooks only at the
blackout window. The take's new read of the settings, the consent and the
install form one actor's local sequence with no second process, so no flow is
added. The sitting may ask for one.

**Components.** `docs/requirements/components.toml` is unchanged. No module
is added or removed, so CMP-008 and CMP-009 keep their membership.
`components.derived.toml` is regenerated at landing.

## Steps

Each row is one commit. Its green done-condition is in its detail section.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The pure four-state reading added to `kitlib/guard_hooks.py` beside the old helpers; nothing deleted, no consumer changed | D1; D6; D7; D8; D9; SR-032; TC-345 | intra-module: `kitlib/guard_hooks` is `coordinator_guard`'s own decomposed helper, no declared seam |  |
| P2 | One atomic producer/consumer swap: `coordinator_guard.py` over the reading (`hooks_state`, `install_hooks`, `consent_install`, the four-word report, `--offer`, `--enable` removed); all four dev-setup files moved to the new words and `--offer`, with the reader-failure `[missing]` line; every test caller of `enable_hooks`/`--enable` migrated; the merge and ownership helpers and `enable_hooks` deleted with the deletion assertion | D2; D3; D4; D5; D10; D17; D18; D19; D21; D22; D23; D24; D25; F1; SR-032; TC-345; TC-343 | IF-280; IF-281 | P1 |
| P3 | The lease take reads the hooks before the lock: goes on at `none`/`on`, refuses at `occupied` and without a terminal at `absent`, asks at a terminal, refuses a failed install | D11; D12; D13; D14; D15; D16; SR-229; SR-032; TC-345; TC-316 | IF-280; IF-281; IF-277 | P2 |
| P4 | Spine rows for the checkpoint sitting: LLR-322, TC-345 and IF-280 amended, LLR-300's detail and `code_symbol`, SR-229 checked, SR-032 unchanged | D26; D27; D28; D29; D30; D31; D32; SR-229; SR-032; TC-345 | IF-280 | P3 |
| P5 | `RESYNC_PACK.md` entry, docstrings and generated surfaces, the bar on the landing tip | D33; D20; SR-032; SR-229; TC-032; TC-315; TC-316; TC-317; TC-339; TC-342; TC-343; TC-344; TC-345; TC-350 | IF-280; IF-281 | P4 |

**Why P2 is one large step.** Revision 1 split it into the Python side (old
P2) and the shell side (old P4). That split is what F1 and the second break
found above are about: the CLI's words and flags are a contract, and its
producer and its consumers must change in the same commit or the tree between
them is red. P2 is therefore the smallest step that keeps every commit green.
Its tests are named per file below. The builder may commit it in work order
inside the lane, but its first commit to pass the bar is the whole swap.

## Step detail: what each changes, the tests it adds, and what each fails on before the change

### P1: the reading, added (`project-trajectory/scripts/kitlib/guard_hooks.py`)

**Change.** Decision 1's reader only. Add `read_state`, `Reading`, `Problem`,
`is_guard_command` and `refusal_text`.

- **Kept untouched:** `command_shapes`, `merged`, `_owns`, `_without_guard`,
  `bind` and `guard_groups`. `coordinator_guard.py` still calls them, and
  nothing in it changes.
- **Docstring:** only a paragraph is added, naming the reader as the coming
  replacement for the merge. The full rewrite is P2's.

**Tests**, in `tests/test_coordinator_guard.py`, in-process (smoke tier):

- `test_the_hooks_reading_is_none_absent_on_or_occupied`, parametrized. Each
  case fails before because `read_state` does not exist. The cases:
  - `none`: the example has no guard group;
  - `absent`: settings `None`, `{}`, `{"permissions": {...}}`, and guard
    events present as `[]`;
  - `on`: the example's bare-`python` commands, a bound `"C:/x/python.exe"`
    path, and a changed matcher;
  - `occupied`, each naming its problem:
    - the mixed PreToolUse group (D6);
    - two groups on Stop (D7);
    - SessionEnd missing while the others are present (D8);
    - a `Problem("Expecting value…")` (D9);
    - a zero-byte file's parse `Problem`;
    - the remaining shape faults: not an object, `hooks` a list, an event a
      dict, a group without `hooks`, a command `7`, and an unreadable-example
      `Problem`.
- `test_a_user_command_ending_in_the_guards_name_reads_as_the_guards`. It
  pins the residue the spec states once: a user command whose last words are
  the guard's file name and `hook`. It fails before for the same reason.

**Green done-condition (P1's commit).** `run.cmd smoke` passes inside its 60
s budget. The two new tests pass. Every existing test is unchanged and
passes, including `tests/test_blackout_window.py` and
`tests/test_run_devsetup.py` run by file, because no consumer changed. The
deletion assertion is **not** in this step.

### P2: the atomic swap (`project-trajectory/scripts/coordinator_guard.py`, `project-trajectory/scripts/kitlib/guard_hooks.py`, `project-trajectory/scripts/dev-setup.template.sh`, `project-trajectory/scripts/dev-setup.template.ps1`, `scripts/dev-setup.sh`, `scripts/dev-setup.ps1`)

**Change.** Decisions 2, 3 and 6, plus decision 1's deletions, all in one
commit.

- **`coordinator_guard.py`:**
  - `hooks_state` reads through `read_state`;
  - adds `install_hooks`, `consent_install` and `_terminal_ask`;
  - `_hooks_main` prints the four words, exits 1 at `occupied`, gains
    `--offer` and loses `--enable`;
  - deletes `_guard_plan` and `enable_hooks`;
  - updates the IF-280 and IF-281 contract paragraphs in the module
    docstring.
- **`kitlib/guard_hooks.py`:** deletes `command_shapes`, `merged`, `_owns`
  and `_without_guard`, and rewrites the docstring around one rule: checked
  by name, never shared.
- **The four dev-setup files:** the report and the offer of decision 6, each
  in its file's own idiom. The template's `--baseline` and this repo's
  `--install` naming stay as they are.
- **Rebases:** the wi-798 lane edits the same templates. Whichever lands
  second rebases (spec S6).

**Tests in `tests/test_coordinator_guard.py`** (smoke tier):

- `test_guard_hooks_holds_no_merge_or_ownership_code` (D25). The module has
  none of `merged`, `command_shapes`, `_owns` or `_without_guard`, and
  `coordinator_guard` has no `enable_hooks` or `_guard_plan`. It fails
  before: all six exist. It lands in the same commit as the deletions.

**Tests in `tests/test_blackout_window.py`** (smoke tier):

- **Inverted:** `test_the_hook_opt_in_merges_and_keeps_existing_hooks`
  becomes `test_a_user_command_beside_the_guards_reads_occupied_and_nothing_is_written`
  (D6, D10). It keeps the same fixture and drops the two `enable_hooks`
  calls at lines 1074 and 1075. It asserts:
  - `hooks_state(...).word == "occupied"`, naming `echo
    user-audit-notification` and the `ruff check …coordinator_guard.py`
    command;
  - `consent_install`, given an `ask` that answers `y`, is never asked,
    returns the refusal, and leaves the file byte for byte unchanged;
  - `guard.main([... "hooks", "--example", src])` exits 1 with the text on
    stderr;
  - the committed `settings.json` is untouched.

  It fails before: today the state reads `off` and `enable_hooks` merges.
- `test_each_occupied_shape_refuses_and_writes_nothing`, in-process,
  parametrized over D7, D8 and D9 at `consent_install` and at the `hooks`
  CLI. It fails before because there is no `occupied`:
  - a second group or a missing event merges;
  - an unparseable file returns the old parse message with no events named.
- **Edited:** `test_the_hook_opt_in_with_no_guard_hooks_changes_nothing`
  (D18).
  - The `--enable` argument at line 1094 is removed.
  - It still asserts `none` and no `.claude` directory.
  - It adds that `guard.take(root, …)` with that example returns `None` and
    records the holder.

  The take half fails before only through the edit, so it is a pin.
- `test_the_hooks_command_refuses_enable` (D19). `guard.main([...,
  "--enable"])` raises `SystemExit(2)`. It fails before: the flag is
  accepted.
- `test_an_absent_install_binds_every_group_and_keeps_other_keys` (D2 at the
  function level). The settings are absent, `{}`, or `{"permissions":…,
  "hooks": {"Notification": [...]}}`. After `consent_install(...,
  ask=yes)`:
  - all eight guard events hold one group bound to `sys.executable`;
  - `permissions` and `Notification` are unchanged;
  - the reading is `on`.

  It passes before only through `enable_hooks`, so it is a pin.
- `test_a_declined_or_empty_or_eof_answer_writes_nothing_and_asks_again`
  (D3 at the function level). The answers are `n`, `""` and EOF (`ask`
  raises `EOFError`, which reads as `""`). No file is created, and the next
  call asks again. It pins today's behaviour.
- `test_an_on_file_is_left_byte_for_byte_and_nothing_is_asked` (D4 at the
  function level). It also covers the bare-`python` form, read by name. It
  fails before for the bare form only: today a bare command reads `off` and
  `--enable` rewrites it.
- **Kept unchanged:** `test_a_scaffold_keeps_the_machine_local_settings_out_of_git`
  (D22) and
  `tests/test_coordinator_guard.py::test_the_guard_hooks_are_this_repos_opt_in_not_its_tracked_settings`
  (D23). They read only `guard_groups`, which is unchanged.

**Tests in `tests/test_run_devsetup.py`** (`SLOW_MODULES`):

- **Kept, one call changed:**
  `test_an_installed_hook_denies_with_an_older_python_first` (D21).
  - The `hooks --enable` subprocess at line 359 is replaced by the consented
    install's write, `install_hooks(root, example)`, called in-process: the
    write a yes leads to, bound to this interpreter as before.
  - Its assertions are unchanged.
- **Rewritten:** `test_the_hooks_command_reports_and_switches_on` (lines
  1170 and 1171) becomes
  `test_the_hooks_command_reports_each_state_and_writes_nothing` (D19). A
  subprocess runs the read-only report:
  - `absent`, after which no file has been created;
  - `on`, after an in-process `install_hooks`;
  - `occupied`, with exit 1 and stderr naming the event;
  - `none`;
  - the file's bytes are unchanged across report runs.

  It fails before: today the report prints `off`, never `absent`.
- `test_a_failing_or_silent_hooks_reader_is_reported_missing_never_none`
  (D17), parametrized:
  - over `{template-sh, template-ps1, root-sh, root-ps1}`, with the ps1
    cases skipped off Windows;
  - over `{exit 1 with stderr "boom-927", exit 0 printing nothing}`.

  A copy of the dev-setup runs `--check`/`-Check` in a tree whose
  `coordinator_guard.py` is a stub that misbehaves that way, with the
  example present. It asserts:
  - exactly one `coordinator Claude Code hooks` line;
  - that line is `[missing]` and names `boom-927` (or "printed nothing");
  - the missing count includes it.

  It fails before: each copy maps the case to `none` and prints no line.
- `test_at_a_terminal_a_yes_installs_every_guard_group_keeping_other_keys`
  (D2 end to end, the offer's own install driven through dev-setup),
  parametrized over a settings file that is absent, `{}`, or
  permissions-only.
  - POSIX: `_at_a_terminal` on the scaffold's `dev-setup.sh --for-run`, with
    `y` for the hooks offer and `n` for the rest.
  - Windows: `_at_a_console` on the template and root ps1 `-ForRun`.

  It asserts the eight events, bound to the handed interpreter, with the
  other keys kept. It is a pin: today's merge passes it with `{}`.

  **A zero-byte file is not "empty" here.** It is not JSON, so by the Trust
  ruling it reads `occupied`. Today `_read_json` raises on it too, so the pin
  could not pass with it. The plan reads "empty" as `{}`, and P1 pins the
  zero-byte file as `occupied`. The sitting may rule otherwise.
- **Kept:** `test_a_denial_changes_no_configuration_or_credential` (D3).
  - Its `skipped the coordinator hooks` assertion still holds, because
    Python prints the same text.
  - A second dev-setup run in the same test still offers the hooks, so the
    next run asks again.
- `test_an_on_file_is_unchanged_and_not_offered_at_a_terminal` (D4 end to
  end, POSIX pty). The bytes are equal before and after, and the output has
  no `Write the coordinator's` prompt. It is a pin.
- `test_an_occupied_slot_is_reported_and_never_offered` (D5 at dev-setup),
  over the four occupied shapes.
  - It runs `--check` on every host, plus the POSIX pty `--for-run`
    answering `y`.
  - It asserts a `[missing]` line naming the events and commands, no hooks
    prompt, unchanged bytes, and the run going on to its later sections.

  It fails before: today the mixed case reads `off` and the offer merges.
- **Amended:** `test_this_repos_readiness_report_names_the_hooks_opt_in`
  (D24).
  - It still asserts exactly one line. That line is `[ok]`, the `[note]`
    naming where the offer is made, or a `[missing]` naming the
    move-or-remove fix.
  - These are the four states. `none` cannot occur here, because this repo
    ships the example.

  It fails before: `[missing]` is not an accepted form, and today's `off`
  wording differs.
- **Unchanged and run:**
  `test_the_standalone_check_at_a_terminal_offers_and_writes_nothing` and
  `test_at_a_terminal_each_missing_item_is_offered_consent_first` (TC-343).

**Green done-condition (P2's commit).** All of these hold on the same
commit:

- `run.cmd smoke` passes inside 60 s;
- `tests/test_coordinator_guard.py`, `tests/test_blackout_window.py`,
  `tests/test_run_devsetup.py` and `tests/test_onboard_devsetup.py` pass,
  run by file with `-n auto`, because the slow dev-setup modules are where
  this step's consumers live;
- `git grep -n "enable_hooks\|--enable\|merged(\|command_shapes"` over
  `project-trajectory/scripts`, `scripts` and `tests` finds no hooks-route
  caller;
- the module-size ratchet test passes.

### P3: the take (`coordinator_guard.take`, `main`)

**Change.** Decisions 4 and 5. The new signature is `take(root, session_id,
transcript=None, ask=None)`.

- Existing callers pass three arguments. Their roots hold no example, so
  they read `none` and behave as today.
- The `test_session_keep` lookup count is unaffected, because the reading
  spawns no git.

**Tests**, in `tests/test_coordinator_guard.py`, in-process unless a bullet
says otherwise:

- `test_with_the_hooks_absent_and_no_terminal_the_take_refuses_naming_dev_setup`
  (D12). The example is present, the settings absent, and `ask=None`. It
  asserts:
  - the refusal names `dev-setup`, `run` and "answer yes";
  - `_load(lease_dir)` is `{}`, and there is no `events.jsonl` line;
  - no settings file is created.

  The same case runs through the CLI subprocess in
  `tests/test_coordinator_guard_e2e.py` (`_guard_cli(root, "take")`, whose
  stdin is not a terminal) and exits 1. It fails before: the take never
  reads the hooks, and it records the holder.
- `test_the_take_goes_on_at_on_and_at_none` (D13). It is a pin, and the
  existing take tests also keep passing.
- `test_an_occupied_slot_refuses_the_take` (D14), on the mixed group. The
  refusal names the file, the event and the command; no holder is recorded;
  the bytes are unchanged. It fails before: the take records the holder.
- `test_at_a_terminal_the_take_asks_installs_and_takes_after_a_yes_and_refuses_after_a_no`
  (D15, in-process with an injected `ask`).
  - After a yes, the holder is recorded, the reading is `on`, and the
    success text names the next-session caveat.
  - After a no, there is a refusal, no holder and no file.

  It fails before: `take` has no `ask` and never asks.
- The same at a real terminal, in `tests/test_run_devsetup.py` (D15 end to
  end), where the pseudo-terminal helpers already live:
  - **POSIX:** `test_the_cli_take_at_a_pseudo_terminal_asks_and_installs`
    runs `coordinator_guard.py --root R take --session S` with
    `pty.openpty()` on stdin and CI unset. It is fed `y\n`, then `n\n` on a
    fresh root. It is skipped on Windows.
  - **Windows:** `test_the_cli_take_at_a_windows_console_asks_and_installs`
    reuses `_at_a_console`. It passes `sys.executable` as the "script" and
    `[guard path, "--root", R, "take", "--session", S]` as its args.
    `CONSOLE_TYPIST` types `y\r`, then `n\r`, into a real hidden console
    (`CREATE_NEW_CONSOLE`), where Python's `sys.stdin.isatty()` is true. It
    skips, as the helper does, when the host gives the console no
    interactive session. It is skipped off Windows.

  Each fails before: the take never asks.
- `test_a_consented_install_whose_write_fails_refuses_the_take` (D16).
  `monkeypatch` replaces `write_atomic` in two ways:
  - (a) with one that raises `OSError("disk full")`;
  - (b) with one that writes `"{"`, a partial file.

  Each case refuses, records no holder, and names
  `.claude/settings.local.json`. Case (a) also names the error, and case (b)
  names the re-read's parse problem. It fails before: there is no install in
  the take.

**Green done-condition (P3's commit).** All of these hold on the same
commit:

- `run.cmd smoke` passes inside 60 s;
- the new tests pass;
- every existing take test in `tests/test_coordinator_guard.py` and
  `tests/test_coordinator_guard_e2e.py` (TC-316) passes unchanged;
- `tests/test_run_devsetup.py` passes by file.

### P4: spine rows (judged at the lane's checkpoint sitting)

These are drafts for the spine author; the sitting judges them.

- **LLR-322** (`docs/requirements/low-level-requirements.toml`):
  - **title:** "Coordinator guard hooks are read by name and installed only
    with consent".
  - **detail:**
    - The guard hooks' state over the shipped example and the machine-local
      settings is one of none, absent, on or occupied, with each guard event
      checked by the guard's command name.
    - At absent, the developer-setup offer and the lease take each install
      the example's guard groups only after a terminal yes. The install is
      bound to the running interpreter and keeps every other key and event,
      and each route goes on only when a re-read reads on.
    - Without a terminal, the take refuses and names the consent step.
    - At occupied, every route writes nothing and names the file, events,
      commands and fix. A failed reader is reported missing, never none.
    - No re-enable path exists.
    - The repo-specific sentences are kept: the committed settings hold no
      guard group; the inert example declares every served group; the report
      names the state and the offer's location.
  - **rationale:** "Coordinator hooks change a contributor's interactive
    environment, so an explicit opt-in leaves a declined setup reversible."
    The clause "preserves existing configuration" is dropped.
  - **code_symbol:** `offer_hooks/OfferHooks/Offer-Hooks;hooks_state/install_hooks/consent_install/take;guard_groups/bind/read_state/is_guard_command/refusal_text`.
- **TC-345** (`docs/test/test-cases.toml`). Method, expected and evidence are
  rewritten to the P1-P3 cases:
  - **method:** read the four states over the Trust shapes; drive the
    consent at both routes (function, pseudo-terminal, Windows console); run
    the failed-write, reader-failure, no-guard and older-Python cases.
  - **expected:** the Done-when outcomes.
  - **evidence:** lists the new and renamed test node ids, and drops the old
    names `test_the_hook_opt_in_merges_and_keeps_existing_hooks` and
    `test_the_hooks_command_reports_and_switches_on`.
  - **tier:** stays `Smoke`, because the in-process cases are in the smoke
    tier. The pty and console cases are in `SLOW_MODULES`
    (`test_run_devsetup`).
- **IF-280** (`docs/requirements/interfaces.toml`, Drafted): the data cell's
  last alternative reads `hooks --example E [--offer]` (decision 3,
  flagged).
- **LLR-300:**
  - **detail:** gains one sentence: "take first reads the guard hooks' state
    and records no holder unless it reads none or on, or a terminal consent
    installs them and the re-read reads on; without a terminal at absent, or
    at occupied, it refuses naming the consent step or the hooks to move."
  - **code_symbol:** `hooks_state/enable_hooks` becomes
    `hooks_state/consent_install`.
  - The WI-834 grammar-removal row and WI-926 edit the same row. Whichever
    lands second rebases.
- **SR-229** (`docs/requirements/system-requirements.toml`). Its acceptance
  goes to the sitting unchanged.
  - Its admission list governs the *claim* routes. It does not read as an
    exhaustive list of the *take's* refusals: it already omits the take's
    held-by-another refusal, which LLR-300 carries.
  - So the plan proposes no edit, and the sitting rules on it.
- **SR-032:** unchanged.
- `docs/requirements/components.toml` and `docs/runtime-flows.md` are
  unchanged (see above).

**Green done-condition (P4's commit).** `check_trajectory --strict` and
`run.cmd smoke` pass with the amended rows.

### P5: resync, docs, generated surfaces and the bar

- **`project-trajectory/RESYNC_PACK.md`:** one `### … [since <sha>]` entry
  covering the five items of deliverable 7:
  - `--enable` deleted;
  - the consented install at both first runs (`hooks --offer` and the take);
  - the take's no-terminal refusal, and how to consent;
  - `occupied`, and how to move one's own hooks;
  - a matcher-only change still reads `on`; to change more, remove the
    installed guard groups and run the consented install again.

  The entry also lists the kit-owned files to overwrite
  (`scripts/coordinator_guard.py`, `scripts/kitlib/guard_hooks.py`, and
  `scripts/dev-setup.template.*` as the adopter's dev-setup, per the pack's
  rule), and states that no registry or setting migrates.
- **`project-trajectory/scripts/kitlib/bootstrap_manifest.py`:** its comment
  on `guard_hooks` is reworded. The manifest entry is kept.
- **Regenerated:**
  - `docs/cli-reference.md`, which drops `--enable` and gains `--offer`;
  - `components.derived.toml`, `PROJECT_STATE.html` and the rest of the
    landing regen list, per the coordinator-cycle skill.
- **WI-897's queued row:** the coordinator amends it on trunk before its
  claim (deliverable 6). This lane does not edit it, and the RESYNC entry
  records the change.
- **The bar:**
  - `run.cmd smoke` at each commit, which runs the in-process cases;
  - `check_trajectory --strict` before the landing commit;
  - the full suite (`python -m pytest -q -n auto`) on the landing tip. It
    runs every TC verifying SR-032 or SR-229: TC-032, TC-315, TC-316,
    TC-317, TC-339, TC-342, TC-343, TC-344, TC-345 and TC-350. Only TC-345
    changes. TC-316's take tests are P3's regression net.

  The real output is pasted into the lane report.
- **D20:** the four kept tests are confirmed present, under their original
  names, in TC-345's evidence.

**Green done-condition (P5, the landing tip).** The full unfiltered suite is
green, `check_trajectory --strict` is clean, and the regenerated surfaces are
committed.

## Risks and open points for the critic and the sitting

1. **IF-280 gains `[--offer]`**, beyond D29's "drops `[--enable]`"
   (decision 3).
2. **D25's ratchet entry does not exist.** The census figure is reported,
   and the clause is flagged as mis-premised.
3. **A zero-byte settings file reads `occupied`.** The plan reads "empty" in
   D2 as `{}`.
4. **The take's no-terminal refusal names both install-tier spellings**,
   because the template and this repo differ.
5. **The "next session" caveat** rests on Claude Code's documented hook
   snapshot. The builder re-confirms it.
6. **Soft collisions to rebase over:** WI-926 also edits
   `coordinator_guard.take` and LLR-300, and the wi-798 lane edits the
   dev-setup templates. P2 now touches the templates, so the wi-798 rebase
   meets P2's commit.
7. **P2 is large.** It is the smallest step that keeps the CLI contract's
   producer and consumers in one green commit (see "Why P2 is one large
   step").
