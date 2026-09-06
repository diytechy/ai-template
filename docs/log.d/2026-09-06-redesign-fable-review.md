## 2026-09-06 — Independent review of the redesign implementation, repairs, control ruling

Owner-requested review of `22b21b06` / `77612fb2` / `875a64b7` at tip
`875a64b7`, by Fable 5.1 with three reviewer subagents (runtime, continuation
code, spine/docs) after the Opus rounds. Findings ranked in
[the review](../reviews/2026-09-06-redesign-fable-review.md); each finding's
outcome in [the dispositions](../reviews/2026-09-06-redesign-fable-dispositions.md);
the segment summarised in the
[execution record](../ai-template-redesign-2026-09-05-codex/EXECUTION-RECORD.md#independent-review-and-repair-segment-2026-09-06-fable-51).

**Owner rulings (2026-09-06), recorded in the
[control decision](../ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06):**
Short control (8 completed WIs or 2 active days; 12 coordinator hours and
US$100, whichever first); code frozen from the launch commit; insufficient
evidence resolves to targeted repair with no automatic second window; the
launch act is the reviewed deletion of the pause file. Restart at merge: the
fresh-process design stands and the launchers relaunch on exit 11 (bounded at
50), because nothing about the drained stop needed a human — the launcher was
a plain `exec` with nothing above it. Relaunches are not interventions.

**Repairs landed (each with a regression that failed first):** the durable
base keeps `merge-base(trunk, HEAD)` for a linked lane and uses the claim
commit only in the single checkout (finding 1: a trunk merge into a lane had
made trunk's `WI:` trailers read as the lane's own); the code-drift scan skips
non-regular `*.py` entries and a failed launch capture disables detection with
one warning instead of crashing twelve entry points at import (finding 2);
launchers and their templates relaunch on exit 11 (finding 3); Ctrl-C in an
attached sitting persists a complete `call_` record, `outcome: INTERRUPTED`
(finding 4); R-E judges a `#fragment` on a TOML registry as a row id, the
reader homed in `kitlib.spine` (finding 8; `check_trajectory.py` reviewed
+5 SLOC, 2331 → 2336, for the call site and message — the reader and hint are
in the shared package, not here); the old-kit resync test runs its kit
assertions without Node (finding 10); SR-184's rationale no longer disclaims
SN-024's family clause and its acceptance states the observable without naming
its method (findings 12, 16); Inspection carriers named by subject (finding
14). The restart drain's treatment of non-boundary exits is retained by design
(finding 5); a narrower change was tried and reverted because it would run the
dispatcher's stale code in the merge slot.

**Carried, not fixed here:** OI-85 — re-attest SN-007 and SN-026 as amended,
rule whether SN-024's family-heterogeneity clause binds attended Critique
acceptance (recommendation: qualify to the unattended path), and decide
whether to fund the parked SN drift detector (finding 11: the need tier has
no snapshot arm, so the debt lived only in prose). P2a's in-array comment loss
and parse-error skip are stated in its record (finding 9). The
design-replacement rule's four homes are recorded, not consolidated (15).

**Process note.** Two fix subagents died mid-task on the account's session
limit; their partial edits stayed in the tree and were finished by hand. One
of them had changed `dispatch.py` before dying; that change was reverted after
review rather than kept because it was already written.

**Validation.** Full unfiltered suite at the repaired tree before its last
one-line correction: `1 failed, 3593 passed, 22 skipped in 694.32s` — the one
red was this sitting's own base rule returning a short HEAD sha for a
claimless single checkout (`test_a_single_checkout_worker_keeps_the_terminal_refusal`);
the fallback was restored to merge-base and that test, the two base-rule
tests, and the worker/review/drift modules re-ran green (`84 passed`). No
second full run is claimed for that correction. Commit bar on a quiet box:
`1674 passed, 4 skipped in 58.83s`; enforced wall `59.0s vs 60s budget ->
within`, exit 0. Ratchets green after the reviewed +5 restamp. Strict
trajectory, trace (`orphans=0 integrity=0 schema-findings=0`), derived stage,
check_docs (0 broken; the standing report.md orphan) and diff whitespace
clean. <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" then ".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=875a64b7+fable-review-repairs; scratch outputs in the session, exact tails quoted here -->

**Not changed:** no need cell, approval, snapshot, policy dial, queue state,
pause file or push. The control window has not started.
