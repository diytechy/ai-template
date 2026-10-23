# WI-961 dispute sitting at 90ff4c3

DISPUTE: findings=F1

## F1: a kill during a log's write leaves a torn log that refuses every retry

**The finding's mechanism is real.** At this range `agent_common.write_session_log` writes straight to the final name with `path.write_text` (`project-trajectory/scripts/agent_common.py:1597`). `session_service.record` reaches it for both the lane and the spool targets (`session_service.py:708`). If a process is killed between the file's creation and the end of the write, it leaves a file named `call_<invocation-id>-*.log` whose header has no `# ---` terminator. `log_meta_text` already reports that state as `terminated=False`, and its docstring names it ("a log whose write was cut short has none"). Plan decision 5 refuses the invocation on an unterminated header, so the torn log would block that invocation until someone removes it by hand.

**The scenario is outside the promise.** Under PROCESS.md §6, a spec's promise reaches only what supported workflows and the kit's own routes produce. A sub-second timing window lies outside it unless the spec names it as inside. The window here is far below a second. I measured it: a header-complete log with a usage-summary body like the one plan D3 composes is 1,375 bytes, and `write_session_log` takes a mean of 0.85 ms per call over 200 writes. That figure includes the redaction pass and `mkdir`, so the actual write is shorter still. A kill that tears the file has to land inside that slice of a run that otherwise spends its time reading transcripts.

The spec does not name the in-write kill. Its Trust section gives two failure states:
- "a log spooled for some invocations and not others (killed mid-run)": a kill between writes;
- "a spool write that raises".

The Done-when holds the first: "A run killed after some logs were spooled, then re-run, ends with each invocation recorded once." The plan's `test_a_run_killed_after_some_logs_then_rerun_records_each_invocation_once` drives exactly that, with `record` raising on its third call. A raising write could tear a 1.4 KB file only if the disk filled partway through it, which is a host condition. On the kit's routes, a write that raises fails at the open, and leaves no partial file to discover.

**Refusing a torn log is the spec's own ruling.** Trust says: "An unreadable earlier log: the command refuses, rather than re-count or skip." A torn log is an unreadable earlier log. The torn-log test therefore pins stated behaviour, not a defect. The path also fails closed and loud: the command exits 1 and names the log, and every other invocation is still recorded. It is not a fail-open path, does not lose data silently, and leaves no Done-when item undelivered, so it is not a convergence-class finding that must be FIX.

**The cost doesn't change the outcome.** The proposed fix, an atomic publish through the shared writer, is cheap. But it changes a writer every caller shares, to cover a window the spec does not promise. §6 says a cheap fix for a contrived scenario is still DISMISS.

**What the lane may record.** The lane may record the non-atomic writer next to its existing note on `write_session_log` under "Observed elsewhere, not changed here". It owes no code for this.

RULING: F1 DISMISS out-of-scope the torn log needs a kill inside a ~1 ms write of a 1.4 KB log, a sub-second timing window PROCESS.md §6 puts outside the promise; the spec's named kill (between writes) is covered by the plan's rerun test, and refusing an unreadable earlier log is the spec's own Trust ruling, fail-closed and named
