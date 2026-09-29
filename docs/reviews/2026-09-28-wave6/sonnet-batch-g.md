<!-- Claude Sonnet (read-only) cross-review of spine-acts batch G, build/batch-g f1733daa..187c2138: three verdict commits (WI-724, WI-726, WI-728) and one act (seq 9) by an independent Opus adjudicator. -->

187c2138 SOUND

BLOCKER: none

MAJOR: none

MINOR:
- In WI-724's verdict, the LLR-268 line cites only `SR-Refs` as holding. It does not state that LLR-268's own routed pointer cells resolve, as the LLR-266 line does. The substance of the return holds.

**The returns, reproduced against the code:**
- **SR-222:** `session_adapters.py:216`, `:349` (`anthropic`), `:453` (`openai`); opencode names none (`:625`).
- **LLR-266:**
  - `CodexAdapter.prepare` (`:436-438`) adds `--json` and `-o`;
  - no codex `cmd_template` in `docs/agents.toml` (lines 63/71/79) carries `-o`.
- **TC-264:** only claude's case asserts `semconv` (`tests/test_session_service.py:61`); the codex (`113-124`) and opencode (`126-138`) cases assert none.
- **SR-227 / LLR-270:** `session_keep.keep_for` (`524-589`) returns unretained after `lease_wait`, and mint-on-first-launch is the other path. The literal `shall` fails both.
- **LLR-223 / TC-220:**
  - `_classify` (`assumption_rules.py:476-477`) gates `joint` on a non-empty sibling list alone, whatever the disjoint siblings.
  - A read-only in-memory probe classified an SR citing only a disjoint sibling as `joint`, with no unclassified finding.

**The act:**
- No live registry cell changed, and no Status flipped.
- It touches only `docs/archive/last_approved/` (README, `acts.toml`, and the SR copy, which is byte-identical to the live registry).
- A read-only `baseline_snapshot.refresh_refusal` over the LLR and TC registries lists five drifted rows. With the three blessed rows named, it narrows to exactly LLR-223 and TC-220, so leaving the four first approvals unflipped is the brief's own stop case. Over the SR registry with the eight named, there is no refusal.
- `Delivered-With` is in `SPINE_APPROVED_CELLS` (`acceptance_record.py:352`).

**The Dispositions:** in WI-724, `intake.parse_dispositions` returns exactly one draft. It covers every returned row, plus optional items and the carry-over. WI-726 carries no second draft.

**Grammar:**
- The machine lines are `OUTCOME: RETURN rows=9`, `VERDICT: MEANING rows=12` and `VERDICT: MEANING rows=1`.
- Each verdict commit carries its `WI:` trailer.

**Run:** `python -m pytest -q tests/test_assumption_rules.py tests/test_cell_classes.py tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py tests/test_retire.py` → **351 passed in 80.14s**.
