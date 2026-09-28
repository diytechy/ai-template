# ADJUDICATE — WI-717 — amendment of approved LLR-177 and TC-172 at d7e1be0e

Independent adjudication of two approved rows whose text moved after it was
attested, amended in place by WI-620 under the amendment authority ruling 54
granted, so that they name the session-log header path. The one question: did
each amendment change the requirement's MEANING or only its CLARITY. Judged
from the before/after cells the kit's amendment brief rendered
(`adjudicate_brief.compose`, anchor `docs/archive/last_approved` copied at
6763d08d for the LLR and TC registries), with the live rows re-read from the
registries and the anchor's copies diffed by hand. The brief renders LLR-177
`Detail` and TC-172 `Method`; TC-172's `Evidence` also moved (a traced cell,
silent by ruling) and is read below because the coordinator asked for it. The
amending session is not a witness: the arbitration file was context only.

- [MEANING] LLR-177 Detail -> before: `write_session_log` passes every TRANSCRIPT through `redact_secrets` before the tracked log is written, substitutes each `_SECRET_RES` shape with `[REDACTED]`, and the header reports the finding as class plus count; an unknown shape passes through; the raw stream stays in gitignored `out/run-logs/`; the PII/identity classes are the row's build debt -> after: the same, AND every header VALUE (a verbatim raw-usage line can carry a runner's result text) passes through the same redaction, and the count line reports the findings of BOTH paths -> not the same obligation: a builder who redacted the transcript alone acted correctly on the old text and fails the new one, since a credential inside a header value now has to be substituted and counted. The new text is true of the code at HEAD: `agent_common.write_session_log` (2680-2790) calls `redact_secrets` on the transcript, then on each header value in turn, sums `hits` into one `redacted` count and writes the one `# redacted: N credential-shaped token(s)` line. The reason the obligation widened is real and standing — `session_adapters._claude_raw` keeps claude's whole result event verbatim in `raw-usage`, and that event carries the result text — so the amended text is one I would bless. The unchanged tail (the gap stated as build debt) stands as it was attested.
- LLR-177 `SR-Refs` SR-176 (routed, not rendered by the brief; ruled here as the coordinator asked, added in the correction round of ruling 59) -> HOLDS: SR-176 ("Any durable record the delivered kit produces of a secrets or privacy finding shall identify the finding by its class and location, never by the matched value"; acceptance: a planted value appears 0 times in any tracked artifact, the durable trace names class and location, the one durable path is the transcript's redaction seam) is exactly what the widened Detail decomposes — the session-log HEADER is part of the tracked artifact SR-176's acceptance names, so redacting header values and counting them by class is the parent's obligation reaching a second cell of the same file, not a new one; the pointer is unchanged by the amendment and its Hat-Refs SECURITY, a design row's own lens beside the parent's DATA-PROTECTION, still answers for the mechanism.
- [MEANING] TC-172 Method -> before: plant three credential shapes in a transcript, write the log, and assert each appears 0 times in the tracked file, `[REDACTED]` stands in its place, ordinary lines survive, and the header names the finding by class and count ("# redacted: 3 ..."), never by value; PII classes deliberately untested -> after: the same, THEN plant a credential in a header value (a raw-usage line carrying result text) and assert it appears 0 times, `[REDACTED]` stands in the header, the count line names it and the transcript survives; and through the session service, a credential inside a runner's result line never reaches the committed header -> not the same method: a test that satisfied the old Method does not satisfy the new one, which adds two arms and a second entry point (the service). `Evidence` moved with it, from one pointer to three: `tests/test_agent_loop.py::test_session_log_redacts_credential_shapes` (the original arm), `tests/test_agent_loop.py::test_session_log_redacts_credential_shapes_in_header_values` (1708: plants `sk-ant-api03-…` in a `raw-usage` header value, asserts it is absent from the whole text, `[REDACTED]` and `# redacted: 1 credential-shaped token(s)` in the header, `clean transcript` intact) and `tests/test_session_service.py::test_a_credential_in_a_raw_usage_line_is_redacted_in_the_log_header` (626: drives `session_service.call` over a claude-shaped result carrying the key in its result text and asserts the committed header holds `[REDACTED]` and `# raw-usage: [`). Each pointer resolves and passes at HEAD; the Method's arms and the evidence's assertions match one to one. `Verifies` SR-176;LLR-177 is unchanged and HOLDS (SR-176's planted-value observable, LLR-177's detail contract). Tier Full stays honest (`test_agent_loop` is in `SLOW_MODULES`; the service module is smoke, which a Full case may cite). The amended text is one I would bless.

Both rows are on rungs the declared gate authority has released, so the
re-attestation is this session's, taken in its own reviewed commit after this
verdict: `python project-trajectory/scripts/intake.py snapshot ... --reattests
LLR-177,TC-172`, the rows' `Status` left `Approved`. A scratch run of that
exact command over the intended flips of batch F was accepted (3 registries
copied, `RE-ATTESTED: LLR-177, TC-172`) and reverted before this file was
written; no other approved row in the three registries has drifted approved
text (LLR-026's `Module` moved under WI-620, a traced cell the snapshot copies
without a re-attest, by the WI-388 ruling).

Bar I produced: the three `Evidence` pointers ran green inside `python -m
pytest -q -n 4 tests/test_session_adapters.py tests/test_session_service.py
tests/test_session_keep.py tests/test_retire_dashboard.py
tests/test_agent_loop.py::test_session_log_redacts_credential_shapes
tests/test_agent_loop.py::test_session_log_redacts_credential_shapes_in_header_values
-p no:cacheprovider` — **117 passed in 72.92s**.

VERDICT: MEANING rows=2
