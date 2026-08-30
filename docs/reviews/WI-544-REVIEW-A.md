# WI-544 — REVIEW-A (2026-08-30)

**What this row is:** the disposition of `WI-484`'s `partial` close (report `docs/handbacks/WI-484-wi484-concern-refs-component-view.md`). Its product is a recorded adjudication (ANTHROPIC-OPUS, `opus`, fresh context) and a successor draft; four cross-family REVIEW-A rounds (OPENAI-TERRA, `gpt-5.6-terra` via `codex`) reviewed the lane's diff — rounds 1–3 each found a kit defect at the mint (`_draft_row` dropping `supersedes`; the successor's scope prose never reaching its Context; that prose stripped of Markdown whitespace), all fixed on trunk with tests and merged in by the station refresh, plus two record-side items, all taken. **This file is a compilation** by the supervising session of the delegated unattended run — the merge slot's verdict rung reads a WI-level `REVIEW-A` file for every merged row and nothing in the kit writes one (decisions 21–26 of `docs/decisions-for-review-2026-08-31.md`); the round files are quoted verbatim and the governing machine line is the last line.

## Adjudication — `001-ADJUDICATE-a6a6748.md`

# 001 — ADJUDICATE (independent) — WI-544 disposition of the WI-484 close

Close under judgement: lane `wi484-concern-refs-component-view` closed **WI-484**
as `partial` (reason "worker exit 3"), range `9ab30d641c..0bc7902f6d`, split
`keep=[] discard=[]` decided-by-adjudicator.

`OUTCOME: PARTIAL successors=1`

## Review round 1 — at 05b0cfb7 (OPENAI-TERRA, `gpt-5.6-terra`; `002-REVIEW-A-05b0cfb.md`)

- [BLOCKER] docs/archive/work/complete/WI-544-dispose-the-close-recorded-at.md:55 -> the asserted successor lineage and scope are lost by the actual disposition-intake flow: `_disposition_drafts` produces only generic context and `_draft_row` emits `Supersedes=''` -> preserve `supersedes` and the items-3-and-5 scope in the minted successor, with an end-to-end disposition-mint regression test -> @owner
- [MAJOR] docs/status.md:329 -> the generated ready frontier still calls closed WI-544 ready (and PROJECT_STATE.html reports it as a second active item); `gen_trajectory.py --check` and `--status --check` both fail stale -> regenerate and commit both derived artifacts after the terminal move -> @owner
- [MINOR] docs/iteration/wi-544-dispose-the-close-recorded-at-001-20260830-093126.log:9 -> the added trailing whitespace makes `git diff --check a6a6748a^..HEAD` fail -> remove the trailing space -> @owner

`VERDICT: CHANGES-REQUESTED findings=3`

## Review round 2 — at 4032eca0 (OPENAI-TERRA, `gpt-5.6-terra`; `002-REVIEW-A-4032eca.md`)

- [MAJOR] project-trajectory/scripts/intake.py:1082 -> `_disposition_drafts` replaces the disposition's only full successor-scope text with boilerplate; replaying WI-544 mints a successor that retains `Supersedes=WI-484` but omits its items-3-and-5 boundary, item-7 exclusion, and knowledge-pack rule, silently changing the adjudicated work -> transfer the approved successor-scope text into the minted spec and cover the full `intake_after_merge` WI-544-style replay, not only `_draft_row` -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`

## Review round 3 — at 61a0b29d (OPENAI-TERRA, `gpt-5.6-terra`; `002-REVIEW-A-61a0b29.md`)

- [MINOR] project-trajectory/scripts/intake.py:1025 -> `str.strip()` destroys leading indentation and trailing Markdown whitespace from scope prose that the minted successor must receive verbatim; an isolated WI-544 replay loses an indented first line -> preserve the captured prose exactly (removing only a fence-delimiting newline if needed) and add a full-flow regression using Markdown-significant whitespace -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`

## Review round 4 — at db8e273d (OPENAI-TERRA, `gpt-5.6-terra`; `002-REVIEW-A-db8e273.md`)

_(no findings)_

`VERDICT: APPROVE findings=0`

---

Governing machine line (quoted from `002-REVIEW-A-db8e273.md`):

VERDICT: APPROVE findings=0
