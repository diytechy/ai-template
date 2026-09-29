<!-- Claude Sonnet (read-only) cross-review of spine-acts batch H, build/batch-h 3e8a87d2..852cd35c: two verdict commits (WI-730, WI-731) and one act (seq 10) by an independent Opus adjudicator. -->

852cd35c SOUND

BLOCKER: none

MAJOR: none

MINOR: none

**The returns, reproduced:**
- **SR-222 / LLR-268:** `agents.template.toml:32` routes codex to third-party providers via `model_providers`, yet `CodexAdapter.provider = "openai"` (`session_adapters.py:453`).
- **SR-227:**
  - "the declared bound" names nothing declared: `lease_wait=120.0` is a code default (`session_keep.py:538`), and `[adjudicator]` declares no bound;
  - the reason is printed only to stderr;
  - `test_an_adjudication_waits_out_a_keep_warm_lease_then_runs_unretained` asserts no reason.
- **LLR-223:** an in-process probe gave:
  - a disjoint sibling plus a waiver → `coincident`, with no contradiction advisory;
  - joint with DA-Refs and a waiver → `joint`, with the contradiction advisory;
  - SR-193 and TC-220 scope the contradiction to the joint class.

**The act:**
- It changes four files: the `last_approved` README, `acts.toml` (seq 10), the TC copy, and TC-262's Status in the live registry.
- The TC copy is byte-identical to the live registry.
- `refresh_refusal` refuses the LLR registry (on LLR-223 alone, once LLR-222 and LLR-286 are named) and the SR registry (on SR-177 alone, once SR-193 is named), and accepts TC with TC-220 and TC-222. So a TC-only act is what both briefs prescribe.

**The Dispositions:**
- `intake.parse_dispositions` returns exactly one draft in WI-731, with no refusal.
- Its seven items cover the seven returns.
- It states the carry-over: the first approvals of LLR-267, LLR-269 and LLR-270; the re-attestations of LLR-222, LLR-286 and SR-193; and TC-267, which item 4 re-opens.

**Grammar and trailers:**
- The machine lines are `VERDICT: MEANING rows=7` and `OUTCOME: RETURN rows=9`.
- The WI trailers are present on every commit.
