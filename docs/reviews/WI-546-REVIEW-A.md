# WI-546 — REVIEW-A (2026-08-30)

**What this row is:** the successor to `WI-484` drafted by the `WI-544` disposition — the two items the owner delegated for the unattended run (the `hats.toml` `knowledge` value-pass and the 17 approved-cell `Rationale` attribution deletions), both drafted for the owner's review at return. Built by ANTHROPIC-OPUS; the review rounds below were drawn by the supervising session (the lane's build sessions wrote no `WI:` trailer, so the loop scheduled none — decision 31 of `docs/decisions-for-review-2026-08-31.md`), cross-family, fresh context, on the third family while OpenAI sat at its usage limit. **This file is a compilation:** the merge slot's verdict rung reads a WI-level `REVIEW-A` file and nothing in the kit writes one (decision 7); every finding and machine line is quoted verbatim from its round file, and the governing line is last.

## Round 1 — at 03d171e (`007-REVIEW-A-03d171e.md`)

- [MINOR] tests/test_hats.py:904 -> `(ROOT / value).is_file()` accepts an absolute or escaping `knowledge` value (the actual changed test passes with `C:\\Windows\\System32\\cmd.exe`), so the new value-pass guard can approve a file outside the repository rather than the WI-required `docs/knowledge/` pack -> require each value to be a repo-relative `docs/knowledge/*.md` path whose resolved target remains below `ROOT`, then check that target exists -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`

## Round 2 — at 5ad854b (`007-REVIEW-A-5ad854b.md`)

- [MINOR] tests/test_hats.py:907 -> The new `docs/knowledge/`-only assertion admits `docs/knowledge/../status.md` (the real test body printed `traversal: ACCEPTED`), so the WI-546 value-pass remains false-green for a non-pack path. -> Resolve the target and require it to be below `(ROOT / "docs" / "knowledge").resolve()`, with an adversarial traversal value that must fail. -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`

## Round 3 — at 8c48742 (`007-REVIEW-A-8c48742.md`)

_(no findings)_

`VERDICT: APPROVE findings=0`

## Round 4 — at cd92c74 (`007-REVIEW-A-cd92c74.md`)

- [MINOR] docs/requirements/system-requirements.toml:947 -> for clarity: SR-175 says its obligation is derived from “the lenses named above,” but this change removed every preceding lens name, disconnecting the DATA-PROTECTION/LEGAL/SECURITY Hat-Refs from their stated rationale -> name the three lens arguments in the stand-alone rationale without restoring the redundant `Hat-derived` attribution -> @owner
- [MINOR] tests/test_hats.py:439 -> the WI-546 knowledge-value Done-when is UNCOVERED: neither changed test asserts that each live path-form `knowledge` value resolves to a pack nor that the five new packs remain DRAFT; the actual CLI accepts and emits a nonexistent path -> add a live-roster regression assertion for the populated path targets and the five draft headers -> @owner

`VERDICT: CHANGES-REQUESTED findings=2`

---

Governing machine line (quoted from `007-REVIEW-A-cd92c74.md`):

VERDICT: CHANGES-REQUESTED findings=2
