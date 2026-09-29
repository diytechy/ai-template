<!-- Claude Sonnet (read-only) cross-review of spine-acts batch J, build/batch-j 349eef9d..bdc4fed3: WI-737's verdict and act (seq 12) by an independent Opus adjudicator. -->

bdc4fed3 SOUND

BLOCKER: none

MAJOR: none

MINOR:
- **A mislabelled citation.** The verdict's SR-227 reading 1 cites "skill §2: a sound requirement violated by code needs a fix". The sentence is real, but it lives in `project-trajectory/skills/spine-authoring/SKILL.md:86` (the adoption section), not in §2. The substance is unaffected.
- **A stretch in reading 1.** It folds "runner version" into "the inputs it judges under change". SR-227's acceptance lists them separately. The reading is defensible, because LLR-270 and TC-267 implement and test the runner-version drain (`session_keep.py:92`, `cli_version`), but a future reader could contest it. It is not load-bearing.

**The keep-warm gap is real:**
- `keepwarm_due` and `due_routes` (`session_keep.py:737-772`) select on `family == "ANTHROPIC"` only.
- Only `ClaudeAdapter.one_turn` (`session_adapters.py:366-371`) adds `--max-turns 1`.
- `KeepWarmer._start` (`session_service.py:448-542`) builds the ping from the row's own `cmd_template`.
- No shipped ANTHROPIC route runs anything but `claude`.

`Approved` blesses TEXT only (brief line 11), so a successor build item, not a return, is consistent with the brief.

**The four "wording" readings:** the three states (`:77-79`) and the tombstone and lease handling (`:262-273`, `:469-484`, `:716-731`) support them.

**The act:**
- It makes exactly three Status flips and no other cell moves.
- Both archive copies are byte-identical to the live registries.
- `acts.toml` seq 12 is correct.
- `refresh_refusal` accepts the act.

**The Dispositions:**
- `intake.parse_dispositions` gives `refusal=None`.
- LLR-270's and TC-268's anchors each occur exactly once.
- The scope is narrow: the code, LLR-270, TC-268 plus a test, with an out-of-scope list.

**Grammar and trailers:** `OUTCOME: APPROVE rows=3`, with the trailers present.

**Run:** `python -m pytest -q -n auto tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider` → **105 passed in 16.93s**.
