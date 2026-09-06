# redesign-p2a — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `468be363a6f3bc7aa69bbf36aab545235382a38706b8f7edf77363509712fcf9`

Tracked invocation: [session log](../iteration/call_c1e26ee786f34805988e7e96e91e0a9b-20260906-102308.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

## CHANGES_REQUESTED

The core approach is right: bounded candidate spans + `tomllib` semantic equality is the correct way to avoid re-matching raw field text, and the uniqueness requirement plus full-dict comparison genuinely defeats the decoys named in the brief (multiline-string namesake, nested `[metadata].needs`, quoted root key, comments — a comment can't put `needs` at line start). Byte preservation is correct: `newline=""` on both the read (`_open_specs`) and the write, edit confined to the value span, `write_text(..., newline=)` is 3.10+ so the 3.11 floor is safe. Split of parse (normalized copy) from edit (raw bytes) is the right seam. Two blockers.

### BLOCKER 1 — the authoritative `_apply_supersedes` has no restore; prevalidation walks a different tree

`_supersede_source_refusal` runs `_apply_supersedes(..., apply=False)` over the pre-mint tree. The real call at `intake.py` `_mint` runs *after* every draft is on disk, so it walks a strictly different population (the new successor specs, and each group reads the previous group's write). Any `ValueError` from `_replace_needs_value` there escapes `_mint` → `intake_after_merge` → the merge slot **with drafts already written and no `git reset --hard`** — the all-or-nothing contract the module docstring and `archive_absorbed`'s arm both assert.

Smallest remedy: give the authoritative call the same treatment as the `archive_absorbed` refusal directly below it —

```python
try:
    _apply_supersedes(root, lineage)
except ValueError as exc:
    ac.git(root, "reset", "--hard", "HEAD")
    ac.git(root, "clean", "-fd", "--", WORK)
    return [], "{}: {}; nothing minted".format(subject_verb, exc)
```

The prevalidation stays as the early, clean-tree rung; this closes the window it structurally cannot cover.

### BLOCKER 2 — the module-size ratchet is knowingly red and undecided

`P2A-EXECUTION.md` reports `intake.py` at 1453 SLOC against a committed 1397 baseline and states the check was not run to green. Per the commit bar, a slice does not close on a check the author knows fails. Decide it inside this slice, not downstream: either compact (`_replace_needs_value`'s comment-free body is already terse; the docstring-light `_supersede_source_refusal` and the `apply=` plumbing are the additions) or take a reviewed baseline bump with the delta stated in the ratchet record. Note the known trap — SLOC ignores comments, so check whether part of `+56` is `ruff format` expansion before buying a bump.

### MINOR 3 — the refusal path is only proved by monkeypatch

`test_an_unwritable_dependency_edit_refuses_before_any_mint_effect` patches `_replace_needs_value` itself, so it proves the ordering (no write, no clean, untracked file survives, no `WI-009`) but never exercises the real locator's failure. That leaves the refusal message and the span-uniqueness logic untested against any actual input. There is a reachable one: a CR-only spec. `_open_specs` normalizes `\r`→`\n` to parse, but `_NEEDS_SOURCE_RE`/the fence regex use `re.M`, whose `^`/`$` anchor only on `\n` — so `fences` is empty, `limit = 0`, and the mint now **hard-refuses** where the old regex silently no-op'd. Add that as the real-input case (or normalize the locator's anchoring and drop the claim).

### MINOR 4 — `apply=` is undocumented on two writers

`_replace_inbound_edges`' docstring still says "Returns the relpaths changed" and never mentions `apply`; `_apply_supersedes` keeps its name while doing nothing. In this module's idiom a flag that decides whether a function writes owes a sentence. One line each; also say in `_supersede_source_refusal` why predicted ids are safe (they only shape the grouping, never the located span).

Not faulted: a malformed spec skipped by `_open_specs` is unchanged behavior, and `_mint`'s existing `git clean -fd -- WORK` on `_write_draft` refusals is pre-existing.
