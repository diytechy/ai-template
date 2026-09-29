<!-- Claude Sonnet (read-only) review of WI-740, build/wi-740 a297b9ff..6f57faf3. Built by Codex Sol; committed by the coordinator. -->

6f57faf3 SOUND

BLOCKER: none

MAJOR:
1. **The one-turn capability is inferred, not declared.** `project-trajectory/scripts/session_adapters.py:243-248` infers it by method identity (`type(self).one_turn is not PlainAdapter.one_turn`).
   - It classifies all four shipped adapters correctly: only `ClaudeAdapter` overrides `one_turn`.
   - But it is a proxy. A future adapter overriding `one_turn` for another reason would be reported as bounding.
   - A declared attribute would state the decision directly.
   - Not a defect in this diff. Flagged for the adjudicator to weigh.
   - *Coordinator: accepted as built. The adjudicator's draft required that "a runner gaining a one-turn bound later needs no second edit", which is what the inference delivers, and every shipped adapter classifies correctly. The trade-off is recorded for WI-740's adjudication.*

MINOR: none. The `code_symbol` insertion placement follows the repo's established practice.

**Checks:**
- **`KeepWarmer.__init__`** computes `self.routes` once, through `adapter_for(...).bounds_one_turn()` over each row's built argv. `take_warm_lease` filters `due` by `routes` before the store lock or any lease write, so a non-bounding route takes no lease and starts no ping.
- **Retention, resume, drain and retirement** are untouched.
- **The tick** stays non-blocking.
- **The registry edits:** LLR-270's `detail` and TC-268's `method` match the draft character for character. `code_symbol` gains the real symbol in the right group. The statuses are unchanged (LLR-270 Approved, TC-268 Drafted), and only five files changed.
- **The twin test** (`test_session_keep.py:553-575`) fails without the fix, by inspection: before it, the opencode row was in `routes`.

**Run:** `python -m pytest -q -n 2 tests/test_session_keep.py tests/test_session_service.py tests/test_session_adapters.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py -p no:cacheprovider` → **111 passed in 20.32s**.
