+++
id = "WI-915"
title = "docs/stack.ini is parsed in one place, and each of its readers keeps its own key case, defaults and failure rule"
workstream = "process"
sr_refs = ["SR-007", "SR-166"]
specref = "docs/plans/2026-10-11-review-churn/README.md#10-one-configuration-file-in-toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-913"]
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator as the review-churn
program's batch row B3 (`docs/handoff-2026-10-11-attended-coordinator.md`,
the queue table). Ruling 10 (revision 4) makes `docs/process.toml` the one
configuration file. Plan item 10's program, step 1, is this row: one shared
loader for today's `docs/stack.ini` in place of its separate parses, a pure
refactor with no format change. The plan's sequence puts it in phase 1. Item
10's steps 3 to 6 (the schema, the move into `process.toml`, routing and
consent, the spec rows) are phase 3, shipped as one RESYNC entry before the
FileBackup re-sync, and this row pre-empts none of them.

Today the file is parsed at 13 `ConfigParser` constructions in 12 files:
`git grep -n 'ConfigParser(' -- project-trajectory/scripts scripts` at
`ff64d366b`. The tests construct 10 more, in 9 files, listed in deliverable 2.
All 13 production sites use the same parser options except key case. They
differ in how they read the bytes:
- four decode rules: a byte-order mark accepted or not, and a stray byte
  replaced or raised;
- two read calls, one of which skips a path it cannot open.

They also end a bad file in four ways. The table in deliverable 2 records each
site as measured at `ff64d366b`, by driving its real function over crafted
files. Hooks, launchers, CI and setup scripts parse nothing: the pre-commit
hook only tests that the file exists
(`project-trajectory/hooks/pre-commit:322`).

## Deliverables

One lane, one landing.

1. **One reader, in `project-trajectory/scripts/kitlib/config.py`** (shipped).
   That module already holds the kit's declared-policy readers:
   - the `process.toml` readers that step 4 builds on;
   - `step_paths` and `step_threshold`, which take the parsed profile;
   - the one-rule-plus-adapters precedent (`first_declared_line` under
     `read_declared` and `read_declared_lower`).

   It is a declared shared-kernel module (`docs/kernel-modules-allow`), already
   imported across CMP-006 to CMP-009. `kitlib/evidence.py`'s `source_paths`
   is one of the 13 sites, not a reader the others share.

   The reader's contract:
   - **Location.** It reads the path it is given, and `docs/stack.ini` is named
     once, beside it. Five sites keep their own path constants' names and take
     the value from it: `check.PROFILE_FILE`, `run_menu.DEFAULT_STACK_INI`,
     `kitlib.evidence.STACK_FILE`, `check_dupes_census.STACK_INI` and
     `scripts/check_smoke_budget.STACK_INI`.
   - **Parse.** Every site's options today: interpolation off, and
     `configparser`'s defaults otherwise.
     - `=` and `:` both delimit.
     - `#` and `;` comment whole lines only, so `src = lib ; note` reads
       `lib ; note`.
     - A duplicate section or key is an error.
     - A `[DEFAULT]` section's keys appear in every section.

     Keys are folded, as at ten sites. The three readers of path- and
     name-keyed sections (`[generated]` twice, and `[run]`) take keys as
     written, as they do today. Key case is the reader's only option.
   - **Bytes.** UTF-8 with an optional byte-order mark, a stray byte read as
     U+FFFD. This is `check.py`'s own rule, already used at six sites (Q1).
   - **Outcomes, closed.**
     - The path names no file: None.
     - The file reads and parses: the parsed profile, the same object type the
       sites use today.
     - Anything else (an unreadable path, any parse error): one error type. It
       carries the parser's message, which names the file (Q2).
   - **Nothing else.** No cache, no defaults, no value checks. Defaults, value
     checks and the failure direction stay with each site.
   - **Back-link.** `Implements: SR-007` (Q3).
2. **The 13 sites read through it.** Each keeps its function, key case,
   defaults and failure rule, as the table below records.
   - The parse options are stated once, at the reader. The site comments that
     restate them point at it instead: `check.py`, `run_menu.py`,
     `trunk_step.py`, `check_doc_refs.py`, `agent_common.py` and
     `scripts/check_smoke_budget.py`.
   - Paths are under `project-trajectory/scripts/` unless shown.

   | # | Site | Reads | Keys | Bytes today | Absent | Bad file today: parse error · unreadable | Moves under Q1 and Q2 |
   |---|---|---|---|---|---|---|---|
   | 1 | `check.py:322` `load_profile` (also `check_readability.py`) | the whole file | folded | sig, replace | None: built-in commands | exit 1 "is malformed" · traceback | unreadable: the "is malformed" exit |
   | 2 | `check.py:1664` `_generated_census` | `[generated]` keys | as written | sig, replace | `[]` | `[]` · `[]` | none |
   | 3 | `agent_common.py:520` `_declared_test_command` (caller `integrate.py:1736`) | `[product] test`, `[paths]`, legacy `[stack] test` | folded | sig, replace | ValueError (the caller tests existence first) | ValueError · ValueError | none (the message names the file) |
   | 4 | `agent_policy.py:1400` `read_agent_loop_config` (`dispatch.py:483`, `agent_loop.py:3915`) | `[agent-loop]` | folded | UTF-8 strict, `read` | `{}` | `{}` · `{}` | BOM, stray byte: the dials are read (were `{}`) |
   | 5 | `check_doc_refs.py:286` `_scan_profile` | `[paths] src`, `[arch-map] mode` | folded | UTF-8, replace | defaults | defaults · traceback | BOM: the declared values (were defaults); unreadable: defaults |
   | 6 | `check_dupes_census.py:94` `_load_baseline` (kit-side only) | `[dupes-census]` | folded | UTF-8 strict, `read` | None | traceback · None | BOM, stray byte: the baseline is read (were tracebacks); unreadable: traceback |
   | 7 | `integrate.py:3211` `_generated_table` | `[generated]` path to kind | as written | sig, replace | `{}` | `{}` · `{}` | none |
   | 8 | `kitlib/evidence.py:92` `source_paths` | `[paths] src`, `tests` | folded | sig, replace | `[]` | `[]` · `[]` | none |
   | 9 | `run_menu.py:116` `load_capabilities` | `[run]` | as written | UTF-8 strict | `[]` | exit 1 "is malformed" · traceback | BOM: listed (was the "is malformed" exit); stray byte: listed (was a traceback); unreadable: the "is malformed" exit |
   | 10 | `trace.py:6382`, inside `_cmd_tests_for` | `[paths] tests` | folded | sig strict, `read` | `tests` | traceback · `tests` | stray byte: the value is read (was a traceback); unreadable: traceback |
   | 11 | `trajectory_arch.py:1241` `_stack_ini_get` (through `_arch_scan_profile`: `check_trajectory.py`, `traj_parse.py`, `trace.py`) | `[paths] src`, `tests`, `[arch-map] mode` | folded | UTF-8, replace | None: defaults | None · traceback | BOM: the declared values (were defaults); unreadable: defaults |
   | 12 | `trunk_step.py:377` `_profile` | `[paths] src` | folded | sig, replace | None | None · traceback | unreadable: None |
   | 13 | `scripts/check_smoke_budget.py:61` `_profile` (this repo's tool) | `[smoke-budget]`, `[product] test`, `[tiers] smoke` | folded | sig strict, `read` | traceback | traceback · traceback | stray byte: the budget is read (was a traceback) |

   Legend for the table:
   - *sig*: UTF-8 with an optional byte-order mark.
   - *replace*: a stray byte reads as U+FFFD; *strict*: it raises.
   - *`read`*: `ConfigParser.read`, which skips a path it cannot open.
   - *traceback*: an uncaught error, exit 1.

   Reached through these functions, and not edited:
   - `check_readability.py` (`check.load_profile`, `check._pget`);
   - `check_trajectory.py`, `traj_parse.py` and `trace.py`'s arch-scan reads
     (`_arch_scan_profile`);
   - `dispatch.py` and `agent_loop.py` (`read_agent_loop_config`);
   - `integrate.py`'s bar refusal (`_declared_test_command`).

   Not parses, and left for step 4:
   - the hook's existence test;
   - `bootstrap.py:1685`, one text replace in a fresh scaffold and the file's
     only writer;
   - `check_figures.py:138`, a line scan;
   - `kitlib/evidence.py:130`, a digest of the file;
   - `kitlib/bootstrap_manifest.py:748`, the template row;
   - the messages and comments that name the file.

   The tests' own constructions are out of scope (Q4), except that
   `tests/test_flag_axis.py:201` stops reaching `configparser` through
   `check`. There are two kinds:
   - Fixture builders, which construct the profile object from text:
     `test_check_harness.py:448` and `:500`, `test_flag_axis.py:201`,
     `test_stack_profile.py:33` and `test_step_path_trigger.py:13`.
   - Readers of the live file or the template: `test_check_smoke_budget.py:54`,
     `test_ci_tier_declaration.py:90`, `test_generated_freshness_wiring.py:88`,
     `test_generated_set.py:24` and `test_smoke_budget.py:39`.
3. **A characterization test** in `tests/test_stack_profile.py`, TC-007's
   evidence file.
   - It drives each of the 13 sites through its real function over these input
     classes: absent; empty; a valid file; the same file with a byte-order
     mark; with a stray non-UTF-8 byte; with a parse error; with an upper-case
     key; with two keys differing only in case; and a directory at the path.
   - The expected outcomes are the table's "today" columns.
   - It is committed first, on the unrefactored code, and passes there. The
     only exceptions are the cells a ruled change moves (Q1, Q2). Those are
     strict expected failures until the refactor commit removes their marks.
   - The three sites that end on an uncaught error today still do. The test
     pins that they raise, not the exception's type.
4. **`project-trajectory/RESYNC_PACK.md`**: one entry.
   - Kit-owned files to overwrite: `scripts/kitlib/config.py`, `check.py`,
     `agent_common.py`, `agent_policy.py`, `check_doc_refs.py`,
     `integrate.py`, `kitlib/evidence.py`, `run_menu.py`, `trace.py`,
     `trajectory_arch.py` and `trunk_step.py`.
   - No setting, registry or record changes, and nothing in an adopter's
     `docs/stack.ini`. The entry names the read changes the coordinator rules
     (Q1, Q2).
   - `check_dupes_census.py` (kept kit-side, WI-821) and
     `scripts/check_smoke_budget.py` are this repo's tooling, so they get no
     entry.

## Done-when

- `git grep -n 'ConfigParser(' -- project-trajectory/scripts scripts` prints
  one line, in `kitlib/config.py`.
  - No other file under those paths imports `configparser`.
  - The parse options are stated only at the reader.
- The characterization test passes. Its first commit, on the unrefactored
  code, passed with only the ruled cells marked.
- Every function in the table keeps its name, and `check.load_profile` keeps
  its `Implements: SR-007, LLR-007, LLR-008` tag. So no LLR `code_symbol` cell
  and no test call site moves (`tests/test_step_path_trigger.py` patches
  `check.load_profile`). `tests/test_flag_axis.py:201` imports `configparser`
  itself instead of reaching it through `check`.
- No requirement, test-case or interface row changes. No `Contract IF-NNN`
  body, CLI help text or generated reference changes.
- `tests/test_module_size_ratchet.py` is re-stamped to the exact new size of
  each touched module it lists: `check.py`, `trace.py`, `integrate.py` and
  `agent_common.py`. `[dupes-census]` is re-stamped too if its reading moves.
  Each re-stamp has its reason in the log.
- `RESYNC_PACK.md` carries the entry in deliverable 4.
- The row lands only after the phase-0 baseline manifest (the handoff's row M)
  is committed on trunk. It lands alone, under the handoff's mechanism-change
  rule: the commit bar, the merge slot and the trunk regen all read through
  the sites it changes.
- The build starts only after the plan gate (WI-913) has landed (S4).
- The bar is green on the landing tip:
  - the smoke tier within its budget;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` with no finding beyond LLR-292's.

## What this leaves to item 10's later steps

No setting moves and no format changes here. Two steps stay theirs:
- step 3's schema: each setting's default and its validation;
- step 4's move into `process.toml`: TOML tables and typed values,
  `[step.smoke]` for `[step:smoke]`, case-sensitive keys, and refusing a
  leftover `docs/stack.ini` by name.

The reader keeps both small:
- **One read site and one named location,** in the module that already reads
  `process.toml`. Step 4 replaces one function's body and puts the refusal in
  one place, not thirteen.
- **One error type.** The sites' failure rules survive the format change as
  written.
- **No defaults or value checks in the reader.** Step 3's schema has no second
  home to reconcile.
- **The same parsed object the sites use today.** Their key access changes
  once, at step 4, to TOML's shapes, not twice.

## Scope answers

- **S1:** one deliverable set, kept together. The reader is useful only once
  every site uses it, and a partial landing would leave step 4 two read
  paths. The characterization test lands first, inside the lane.
- **S2:** no file gains authority.
  - `docs/stack.ini` already declares gates: the plan's product commands and
    `[step:*]` steps, the merge slot's required bar, and the `[generated]` set
    that the trunk audit and the divergence step read.
  - Its producer is the adopter, by hand; bootstrap writes it once, at
    scaffold time.
  - This row changes neither the file nor any reader's rule for an absent,
    unreadable or malformed file:
    - `check.py` refuses a malformed profile.
    - `integrate.py` refuses an absent or empty bar declaration and raises on
      a malformed one.
    - Its `[generated]` allowance reads nothing from a bad file, so it allows
      less.
    - The divergence detector reports nothing, its stated stance.

  The characterization test pins each. No Trust section.
- **S3:** closed by construction, then enumerated. Every site keeps the same
  parser and options, so any text parses the same before and after. Only the
  read can differ. Its classes are deliverable 3's list, with one declared
  default: whatever is neither absent nor parsed is the error type.
- **S4:** `single`, for two reasons:
  - It changes four script families: W1 (`trace`, `trajectory_arch`,
    `kitlib`), W2 (`check`, `check_doc_refs`, `check_dupes_census`), W3
    (`agent_common`, `agent_policy`, `integrate`, `trunk_step`) and W4
    (`run_menu`).
  - It promises behaviour over an input space (S3).

  It builds after the plan gate (G) lands.
- **Architectural delta:** none.
  - **No state.** The reader caches nothing; each call reads the file, as each
    site does today.
  - **No new domain value.** Each site maps the error type onto an outcome it
    already has.
  - **No new input.** The same file. Under Q1, a byte-order mark or a stray
    byte reads as `check.py` already reads it.
  - **No new boundary.** `kitlib/config.py` is already a shared-kernel module
    every component imports. The new import edges point into it:
    `integrate.py`, `kitlib/evidence.py`, and this repo's
    `scripts/check_smoke_budget.py`, as `scripts/check_changed.py` already
    does. It imports only `kitlib.ladder`, so `tests/test_import_layers.py`
    sees no cycle. IF-022, IF-049 and IF-068 (owner `docs/stack.ini`) keep
    their form and consumers.
- **Dependencies:** `needs = []`.
  - The claim waits on nothing. Building waits for G (S4). Landing waits for
    row M and the mechanism-change rule (Done-when).
  - WI-911 (B1) sets how this row's critique and reviews run, not what it
    builds, so it is not an edge.
  - The in-flight lanes (WI-798, WI-902) overlap this row only on the ratchet
    baselines.
  - B2 (WI-914, drafted) edits a `[run]` value in this repo's
    `docs/stack.ini`, not a reader, so there is no overlap.
  - Item 10 step 2's build (the handoff's P7) reads `process.toml` in shell
    and is independent.
  - No third-party dependency: `configparser` is stdlib.
- **B3, B4:** no decision is recorded or re-derived. No owner act or
  credential is needed: no approved row is amended, so there is no act.

## Calls ruled at filing

The coordinator ruled the drafter's seven calls as recommended
(coordinator-2026-10-14 D-004):

- **Q1, bytes:** one decode rule, `check.py`'s (UTF-8, an optional BOM, a
  stray byte read as U+FFFD). It moves the BOM and stray-byte cells at 7
  sites; today a BOM makes the `sym:` reference tier skip silently.
- **Q2, an unreadable path:** the error class, deny by default.
- **Q3:** the reader's back-link is `Implements: SR-007` only.
- **Q4:** the tests' own parses stay out of scope, except
  `test_flag_axis.py:201`.
- **Q5:** the twin section readers wait for step 3's schema.
- **Q6:** IF-022, IF-049 and IF-068's stale notes wait for item 11's rework.
- **Q7:** `sr_refs` stays SR-007 and SR-166.

Q1 and Q2 are the row's only behaviour changes, so it is a refactor plus two
fail-closed corrections, not the pure refactor the handoff named.
