+++
id = "WI-462"
title = "The dispatch trio reds on Windows MAX_PATH only under xdist: test_a_needs_human_worker_hands_back_and_the_run_keeps_going, test_a_red_handback_is_reverted_to_a_bar_inert_artefact_and_merges and test_empty_frontier_rung_one_mints_gap_rows_then_drives_them die at `git worktree add` with 'Filename too long' when xdist's deeper tmp nesting pushes the long fixture branch name (wi-402-close-registry-gap-sr-sr-001-has-no-llr) past the default 260-char limit — all three pass together serially (21s, measured 2026-08-15, log 2026-08-15n). Scope: pick and land ONE remedy — shorten the fixture branch/WI names (cheapest, claims nothing about the machine), set core.longpaths in the fixture repos, or declare long-path support a documented machine precondition — with the one-machine humility stated: this is a default-Windows-config observation on one box, not a universal. Do NOT mark the tests skip-on-Windows; they exercise real rungs."
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

**Remedy (a) — the production slug cap — because the branch name is
production-minted, not fixture-made.** `dispatch._branch_for` derives the
branch from the queued spec's filename, which `wi_convert.slugify(title)`
builds under `SLUG_CHARS`; the gap-row titles that trip it come from
production too (`intake._census_drafts` wrapping trace's orphan census).
Measured before choosing: the failing worktree path stood at **259/260
characters — one under the wall** at the old 40-char cap, so this was a
cliff every long-titled WI walks, in every downstream repo on default
Windows, not an xdist curiosity. `SLUG_CHARS` 40→30 leaves ~30 spare at the
observed nesting depth, survives the artificially deep repro, keeps the
WI-id prefix derivable, and no LLR/TC/test pins the slug length. The
fixture-only alternative (`core.longpaths` in test repos) was rejected
because it greens the suite while leaving adopters on the cliff. Comment on
the constant carries the path arithmetic and the one-machine humility;
`slugify`'s docstring now says "SLUG_CHARS characters" so it cannot drift.
Proven serial, `-n auto`, and `-n 2` with deep basetemp. Totals: log
`2026-08-16a`.

## Context

Found at the 2026-08-15 sitting sweep (log `2026-08-15n`). The three tests
passed in every serial run and failed in every `-n auto` full-suite run on
the same tree — the xdist worker tmp directories (`popen-gw*` nesting under
`C:/Projects/.pytest-tmp/...`) add just enough depth that the worktree path
for the long fixture branch crosses MAX_PATH, and `git worktree add` fails
with `Filename too long` / `Could not reset index file`.

The choice between remedies is a real judgement: shortening fixture names
fixes the suite everywhere but silently stops exercising long-name behavior;
`core.longpaths` in fixtures fixes git but not any Python-side path use; a
declared machine precondition is honest but pushes work onto every adopter
of this box's configuration. Whichever lands, state it where the suite's
platform expectations already live (tests/conftest or the docs the stack.ini
declares), not in a comment nobody reads.
