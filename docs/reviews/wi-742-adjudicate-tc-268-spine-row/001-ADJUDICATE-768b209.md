# ADJUDICATE — WI-742 — first approval of TC-268 at 768b209

Independent adjudication, spine-acts batch K, of the one row the brief marks
`[AWAITING FIRST APPROVAL]`: TC-268. I read SR-227, LLR-270, TC-266 and
TC-267 (all approved) as its chain. I read the brief (`adjudicate_brief`,
first-approval form) in full, and I directed none of the amendments judged
here.

Context, not authority: WI-740 (`git show 3ecef627`) added the method's
opencode clause and its twin test. `Approved` blesses the TEXT; whether the
tests pass is the harness's answer.

- [APPROVE] TC-268 -> the obligation: over `tests/test_session_keep.py`, the case asserts that a keep-warm ping is due only with the dial and its minutes on, for an active ANTHROPIC session idle past the minutes while work is pending, and only on a route whose runner bounds a call to one turn (the opencode twin is never pinged); an adjudication's lease makes a due ping skip, naming the holder; with a blocking launch, the tick returns at once while the ping holds the lease on its own thread, a second tick says so, nothing is committed while the ping runs, and the next tick commits on its own thread; the ping resumes the session, is bounded to one turn, is logged as an ordinary call (role KEEP-WARM, source keep-warm, outcome and occupancy filled), updates the record and releases the lease; a dirty trunk holds the log and says so, a held-lease skip is said once, and a ping in flight at the run's end is recorded over a clean trunk, or over a dirty one is not recorded and its reason is printed and returned; the dirty read is the shared check over a real repository, and the warmer is built from the routing registry with each row's declared environment. -> what the chain shows: Upward: SR-227's "make any keep-warm call one bounded turn that never blocks the scheduler" and "let no two calls use one retained session at once", and LLR-270's KEEP-WARM paragraph, including its newly re-attested clause that a ping is taken only on a route whose adapter bounds one turn. Each clause of the method answers a clause of those rows, and none reaches beyond them. Sideways: TC-266 owns the dial-0 inertness and TC-267 the retention and reset rules. TC-268 owns keep-warm alone and repeats neither of their decisions. Downward, against the code at HEAD: each clause maps to a test: `test_keep_warm_is_due_only_for_an_active_anthropic_session_with_work` and `test_the_dispatcher_keeps_nothing_warm_at_dial_zero` (dial and minutes); `test_keep_warm_pings_only_a_route_whose_adapter_bounds_one_turn` (the new clause); `test_keep_warm_skips_a_session_an_adjudication_holds` and `..._with_its_reason_when_an_adjudication_holds_the_lease`; `test_a_keep_warm_ping_is_one_bounded_turn_off_the_tick_and_recorded_on_it`; `test_a_finished_ping_waits_for_a_clean_trunk_to_be_recorded`; `test_the_run_end_records_a_ping_still_in_flight` and `..._a_finished_ping_only_over_a_clean_trunk`; `test_the_warmer_reads_the_trunk_through_the_shared_dirty_check`; `test_the_dispatcher_builds_its_warmer_from_the_routing_registry`. Pointer cells, each ruled: `Verifies` SR-227 and LLR-270 HOLD. IF-044 (`agent_route.load_registry`, `parse_env`, which the registry-built warmer and its row environment exercise) HOLDS. IF-065 (`agent_common`'s `substantive_working_tree_dirty`, `write_session_log` and `commit_telemetry`, which the dirty-read and commit clauses exercise) HOLDS. `Evidence` names the module holding every case, and `Level` Unit, `Tier` Smoke and `Automated` Yes are consistent with it. Wording: every threshold is named by its dial, and every actor (the dispatcher's tick, the ping's thread, the shared check) is named. Each assertion is observable. The absolutes ("never pinged", "only on a route") range over the routing registry and the kit's own adapters, both closed domains. -> why it is ready: the method is a closed, observable restatement of LLR-270's keep-warm paragraph. With the row flipped, the strict trace gave no `FINDING (requirement form)`.

Observations, not findings:

- The case does not assert that the warmer survives a routing row whose argv
  build is refused. No clause of this method claims that. The defect it would
  catch sits in the code under LLR-270, and WI-741's `## Dispositions` drafts
  its fix together with a test in this evidence module.
- The session-adapter interface row lists `prepare`, `final_text`,
  `raw_usage`, `usage` and `context`, but not the `mint`, `resume`,
  `one_turn` or `bounds_one_turn` methods that the session layer also calls.
  That row is off-spine and Drafted, and it predates this change. Recorded
  only.

Checks I ran at 768b209 (results seen, not claimed):

- `python -m pytest -q -n auto tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider`
  gave **106 passed in 19.76s**.
- **Form gate.** I flipped TC-268 in the working tree and ran
  `trace.py --root . --strict`:
  - There was **no `FINDING (requirement form)` line**.
  - The only new lines against the unflipped run (rc=0) were the expected
    pre-snapshot `approval record` and `integrity` pair for TC-268 (rc=1 from
    those).
  - The flip was restored for this verdict commit.
- **Snapshot pre-check, read-only.** `baseline_snapshot.refresh_refusal` with
  `--approves "docs/test/test-cases.toml=WI-742"` and `--reattests LLR-270`
  returned an empty refusal, so the act is accepted.

The act, in batch K's act commit: TC-268 is flipped `Drafted` -> `Approved`,
and the scoped snapshot is taken with that token, together with WI-741's
re-attestation of LLR-270.

OUTCOME: APPROVE rows=1
