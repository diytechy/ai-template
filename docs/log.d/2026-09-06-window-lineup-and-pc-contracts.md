## 2026-09-06 — WI-551 held for the window; Astra/Sol/Luna; PC carries the batch contracts

**WI-551 deferred.** The control ruling's configuration row excludes the
retained adjudicator session-retention patch from the window, but WI-551 sat
dependency-ready at priority 7, the first parallel row the loop would claim.
Moved to `docs/work/deferred/` with a dated note through `spec_move.py`
(one inbound link relinked in BACKLOG-MIGRATION.md). Re-queue at the close.

**OpenAI re-lineup (owner).** Strong = Astra (`gpt-6-astra`, new
OPENAI-ASTRA row), medium = Sol (down from strong), quick = Luna (unchanged);
Terra is catalog-only. All three enabled rows pin
`model_reasoning_effort=medium` in the template so none inherits
`~/.codex/config.toml` (which sets Astra at high). Enable list order:
FABLE, ASTRA, KIMI, OPUS, SOL, GROK, SONNET, LUNA. `agent_route.py --list`
resolves all eight. Astra is not live-probed from this sitting; the launch's
step 1 and the loop's pre-dispatch probe establish it.

**PC carries the batch-contract amendments (codex finding, accepted).** The
PC package as first written bypassed P1A: SR-148, LLR-149 and TC-143 are
Approved and require batch admission, and a deletion record does not
reconcile an approved contract. PC now runs in two ordered steps: first the
batch-specific slice of P1A (amend SR-148/LLR-149/TC-143 and any row the
strict trace or the F-01 candidate list names, through change-intake under
current authority, adjudicated before deletion), then the code and test
retirement. P1A keeps every other amendment for the conditional runner. Not
previously hashed out: F-01 established P1A for the replacement runner, and
PC's earlier wording was mine.

Deferred open items: none.
