# 122-REVIEW-A — adversarial review of WI-322 (retire open-items.md)

**Subject:** `41b228a` (parent `f232c98`) — the owner decision surface becomes a
registry + a generated view. Reviewed against
[rubrics/code-review-adversarial.md](../rubrics/code-review-adversarial.md).

**Reviewer:** an independent Opus session that did not write the change, working
in an isolated clone pinned at `41b228a` (the live tree advanced to `910edac`
mid-review; the reviewer left it untouched).

**Method:** R2 honoured throughout — every finding is driven against the real
shipped code path over purpose-built temp repos, not read off the diff. Four of
the implementer's five claims were verified independently (byte-identical
markdown across the `reattest_model` extraction, on both baselines and across
`changed`/`added`/`removed`/no-baseline states; four guards mutation-proven to
bite; a fresh scaffold green; both retargeted lints correct in both directions).
**The fifth was refuted.**

## VERDICT: CHANGES-REQUESTED findings=10

- [BLOCKER] `agent_dispatch.py:3430` / `:1452` — the unattended loop regenerates
  the surface with no `--since`, discarding the baseline the file declares.
  Driven: the committed view collapsed from **43 chain-row diffs to 18**, two
  attestation sections emptied, the stamp blanked — and `--check` returned **0**.
  The spec's own Hazard #1, realised in the one place it matters.
- [MAJOR] `tests/test_gen_open_items.py:271` — the theme drift guard's
  `assert value.lower() in gi.CSS.lower()` sits OUTSIDE the token loop, and
  `THEME` is a test-only mirror nothing renders from. Nine of twelve emitted
  tokens were rewritten (dark `--text:#444444`) and the guard stayed green.
- [MAJOR] `gen_open_items.py:318` — the whole-section empty state claims "no
  Draft or Modified **spine row**" while the model selects **SRs only**: a Draft
  LLR/TC under a Verified SR is invisible AND actively denied. It is also the one
  empty state that prints no baseline and no check-the-baseline rider.
- [MAJOR] `gen_open_items.py:576` — `write_text` newline-translates, so a
  registry cell holding a CRLF is written `\r\r\n` and read back `\n\n`: the view
  fails `--check` **immediately after being generated**, permanently. The sibling
  generator already carries the `open(..., newline="\n")` fix.
- [MAJOR] `tests/test_dogfood_sync.py:46` — the new registry is absent from
  `REGISTRIES`, so its shipped template header is the only one not locked to its
  live counterpart. A drifted header renders "the owner queue is empty" for a
  registry holding two pending decisions, exit 0.
- [MAJOR] `work-items.csv:321` — WI-322 recorded `done` while
  `check_trajectory --strict` was red (module in no component). Remediated by
  `910edac`; the durable fix is process.
- [MINOR] `gen_open_items.py:277` — `md_inline` emits a raw `<a href>` with no
  scheme allow-list; an agent-authored cell can ship a `javascript:` URL.
- [MINOR] migration has no detector — a resynced adopter keeps a dead
  `open-items.md` carrying a block nothing regenerates, with every gate green.
- [MINOR] `check_docs.py:668` — `_OI_HEADING_RE` is dead after the S-3 retarget.
- [MINOR] `gen_open_items.py:251` — `word_diff` drops whitespace-only opcodes, so
  a whitespace edit renders neighbours fused ("a  b" → "ab").

**Done-when: 3 UNCOVERED** — V4 (the collapse toggle is never executed), V8
(baseline on *every* section fails for the whole-section-empty case), V10
(Draft/Modified LLR/TC rows never surface).

Full findings, the driven commands and their real output are reproduced in the
session record: [log.md](../log.md), 2026-07-26.
