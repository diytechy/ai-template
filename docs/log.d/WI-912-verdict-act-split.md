## 2026-10-17 — WI-912: the first build round, stage 1 (P2 to P4)

### Red before green (the plan's "Steps in detail")

The builder (Claude Opus, medium, the `kit-builder` agent) wrote the stage's
tests first and ran them on the lane's base tree, `ace24c85c`, before any
code. Each run used the one fixed basetemp, `-p no:cacheprovider`,
`GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`, at below-normal
priority:

```text
python -m pytest -q -n 2 -p no:cacheprovider --basetemp <wi-912 build-bt> \
  tests/test_adjudicate_act.py \
  "tests/test_routing_and_prompts.py::test_the_act_brief_is_a_shipped_prompt_with_strict_slots"
```

- Red, base tree with the tests only: `1 failed, 2 errors in 1.01s`. The
  routing test failed on `AttributeError: module 'prompts' has no attribute
  'ADJUDICATE_ACT'`; `tests/test_adjudicate_act.py` failed to collect
  (`FileNotFoundError`: the module did not exist).
- Green, the same command after the code: `27 passed in 16.73s`.
- The builder's affected-module run (13 modules): `1 failed, 589 passed,
  1 skipped in 254.99s`, the one failure `test_the_catalogue_on_disk_is_FRESH`
  reading the generated prompt catalogue before its regeneration
  (wi-912 D-003).

The coordinator's re-run, after regenerating the catalogue (committed with
the stage, since the commit hook refuses a stale one; D-003):

```text
python -m pytest -q -n 2 -p no:cacheprovider --basetemp <wi-912 coord-bt> \
  tests/test_adjudicate_act.py tests/test_routing_and_prompts.py tests/test_prompts.py
116 passed in 19.90s
```

### The rows stage 1 needs, at intent

GPT Terra (medium, the lane's retained session) authored LLR-338 (the act
assembler, CMP-008), TC-368, IF-296 (the assembler's call surface), LLR-310's
and TC-192's additions, and the requestor and data additions on IF-175,
IF-287, IF-195, IF-196, IF-124 and IF-113, all `Drafted` where new; its own
checks read `check_trajectory: clean` and `130 passed, 1 skipped`. The
coordinator named IF-296 in the module's contract header and added LLR-338
to its `Implements:` tags (D-003).

## 2026-10-17 — WI-912: the first build round, stage 2 (P5 to P7)

### Red before green

The same builder, the same prefix, red on the committed stage-1 tip
`51ffd81b5` with the stage's tests added:

```text
python -m pytest -q -n 2 -p no:cacheprovider --basetemp <wi-912 build-bt> \
  tests/test_coordinator_act.py \
  "tests/test_adjudicate_brief.py::test_no_judging_brief_orders_an_act" \
  "tests/test_coordinator_adjudicate.py::test_the_identity_covers_the_act_brief_for_an_actable_retained_class" \
  "tests/test_adjudicate_act.py::test_a_two_registry_act_says_which_rows_each_approves_token_covers" \
  "tests/test_adjudicate_act.py::test_a_row_ruled_on_two_lines_is_listed_once"
```

- Red: `35 failed, 11 passed in 31.99s`; the 11 that pass are the nine
  no-marker cases of the trailer line (the negative half the plan expects to
  pass before) and the two pins moved from the judging brief's module.
- Green, the same command after the code: `1 failed, 45 passed in 40.81s`,
  the failure the builder's own test matching the brief's static text; fixed
  to check the listed commands, it passes in the final run below.
- Affected modules, two runs: `3 failed, 659 passed, 1 skipped in 283.51s`
  and `1 failed, 811 passed in 2765.02s` (the loaded box), each failure a
  stale expectation of the removed act text, all re-pointed; the final run
  `tests/test_coordinator_act.py tests/test_adjudicate_act.py
  tests/test_coordinator_adjudicate.py tests/test_routing_and_prompts.py
  tests/test_prompts.py tests/test_module_size_ratchet.py
  tests/test_done_when_blessing.py`: `307 passed in 137.66s`.

### The smoke tier

`tests/test_coordinator_act.py` moved into `SLOW_MODULES` (D-004). Bar pairs
in one window, below-normal priority: with the module in the tier, 140.9 s
(2693 passed) beside the parent's 114.8 s (2651 passed); after the move,
92.2 s (2654 passed) beside 90.6 s (2651 passed).

## 2026-10-17 — WI-912: the first build round, stage 3 (P9, P10)

The texts and the RESYNC entry: PROCESS_OPTIONS' "Who performs the approval
act" (+130 bytes, its byte-budget row restamped), the coordinator-cycle skill
and recipes (source, with the `.claude/skills/` and `.agents/skills/` copies
synced), and the entry anchored `[since ace24c85c]`. No new test, so no red;
the builder's runs over the docs, skill-copy and byte-budget tests read
`287 passed, 1 skipped` and `30 passed`, and both strict lints clean. The
builder's report of the retired-row refusal is recorded as D-005.

### The rest of the change set, at intent

GPT Terra's resumed turn authored the rest of P8 (D-006): SR-231's act turn,
the LLR-306, LLR-167, LLR-305 and LLR-338 additions, the act command's
interface rows, the TC sentences, TC-321's tier, and runtime flow 6. Its
checks read `check_trajectory: clean` and `268 passed, 1 skipped`. The bar
on the set: 2654 passed, 2 skipped; both strict lints clean; budget 52.5 s.
