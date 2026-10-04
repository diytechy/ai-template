# Review brief: WI-788 readiness (read-only; do not modify any file)

You are an independent reviewer for the ai-template repo (cwd). Do NOT read, cite or act on `OWNER_SCRATCHPAD.md`. Do not edit, create or delete any file; this is a read-only review.

## The artifact under review

`docs/work/queued/WI-788-provider-homes-and-new-routes.md` (a work-item spec, status queued, buildtier strong). Its half 1 is a research + design note under `docs/plans/` plus `docs/glossary.md`, which STOPS for the owner before any build. The spec records the owner's words, the owner's direction on gaps (second pass) and the owner's rulings on nine design risks.

The next session will write the half-1 design note from this spec. Before that starts, the owner wants to know: **is every question that needs an OWNER decision already answered, so the design note can be written without stopping to ask?** Anything the owner must still rule on must surface now as an open item.

## What to do

1. **Separate the two kinds of question.** For each item the design note must settle, classify it as:
   - (R) research/design the note can settle itself (probes, docs, code reading, a proposal the owner later approves at the checkpoint), or
   - (O) a decision only the owner can make, where writing the note without the answer would force a guess, or would make the note propose something that contradicts a standing ruling without the owner having said so.
   List every (O) item that is NOT already answered in the spec.
2. **Check internal consistency.** Do the owner's later rulings (second pass, nine risks) contradict or leave ambiguous anything in the earlier sections (original Done-when, "Scope widened")? Examples to test, not a limit: the five session families vs the "one labelled entry point" kinds (build, review, judge, author, author-review) — do they map 1:1, and where do REVIEW-A/B, CRITIQUE, DESIGN-CHECK, ADJUDICATE, plan_runner fall? Retained adjudication-reviewer vs S10 "reviewers never" — has the owner explicitly ruled the narrowing, or only implied it? The spine-authoring flow's approval act — is it ruled, or left as an "option"? Risk 6 "may need removing on trunk too" — decided or open? Risk 5 fallback (wait ~20 min then run a fresh non-replacing session) vs risk 7 "no fallback modes" — is that a contradiction the owner must resolve? Builder-retention shipped default ("reset every call") vs "retained by default" in the widened scope. Whether this repo's own dial stays as is.
3. **Verify the spec's factual claims against the code**, citing file:line. In particular: the route `env` cell merge and the agent_loop comment naming CLAUDE_CONFIG_DIR / CODEX_HOME / GEMINI_API_KEY; `session_adapters.py` adapter set; `retain_for` value and where it lives; `lease_wait = 120`; `keep_for` returning None rather than re-minting under lock contention; `context_reset_pct = 0` meaning reset every time; `ClaudeAdapter.context` and the fixture `tests/golden/sessions/claude-stream-json.jsonl`; session logs under `docs/iteration/` carrying role/provider/roster-row/commits; the snapshot refusal message's "amend-plus-flip is approval" allowance; `agent_loop` `route_intent` / `last_impl_family`; `agent_route.select` and `docs/agents-enabled` weights; the line range `agent_loop.py:2580-2850`; the dual paths listed in risk 7 (legacy one-word config fallback, CSV and TOML carrier dual support, the legacy open-item reader in `needs` / TC-253). Flag any claim that is wrong or stale, because the note would build on it.
4. **Look for unasked questions** the owner would need to answer: e.g. scope/size (should WI-788 be split — provider routes vs session-family/entry-point redesign vs glossary — given its breadth and a single owner checkpoint?), authorization for live probes/recordings and any spend (SuperGrok/xAI, Google, FreeAI accounts the owner must provision), secrets handling, which accounts this repo itself will run, the spine (SR-222 and whatever else covers routes/adapters), and the effect on the paused loop (`docs/work/pause` exists).
5. **Spec hygiene**: note any structural issue in the spec file itself (e.g. section placement relative to how `project-trajectory/scripts/kitlib/registry.py` parses `## Deliverable`, `## Context`, and the Done-when section; the empty trailing `## Deliverable`).

## Output format (your final message)

- `VERDICT:` READY (no unanswered owner decisions) or NOT-READY.
- `OPEN ITEMS FOR THE OWNER:` numbered; each with the question as the owner should see it, why it blocks or would force a guess, the options you see, and your recommendation. Only (O) items.
- `FACT CHECK:` each claim checked → CONFIRMED / WRONG / STALE / UNVERIFIABLE, with file:line evidence.
- `INCONSISTENCIES:` within the spec.
- `RESEARCH ITEMS (R):` brief list, for completeness.
- `SPEC HYGIENE:`
Be concrete and terse. Findings are claims: back each with evidence.
