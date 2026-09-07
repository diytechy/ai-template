# WI-620 returned proof repair

This source package addresses the published [WI-619 RETURN](../contract_split/014-ADJUDICATE-3e43db9.md).
It supplies authoring and verification, not semantic acceptance. The complete
combined scope and original Context remain assigned to a fresh primary reanchor.
The coordinator remains paused; no control window, batch deletion, push or main merge.

R2: corrected the reversed attribution in
[the original packet](../wi612-authoring/OBLIGATIONS.md): IF-090 remains intake;
IF-091 remains amendment/drafted-row records and lane approval refusal. Neither
interface meaning or Status changes. The continuation explicitly names that file,
resolving the independent review's minor path ambiguity.

R3/R4: [clause-to-proof mapping](PROOFS.md) distinguishes construction checks,
actual carrier mutations, and cold read-only replay. TC-205's Method, Level and
Full tier remain unchanged; its Evidence adds the actual refusal regression.
WI-621 separately owns verification. WI-622 owns the reproduced private writer
return-contract fix. No ratchet baseline, snapshot or registry Status changes.

The initial [reproducer](status-refusal-before.txt) failed with SystemExit through
the real publication path. The helper's sole production caller already consumes
a refusal string. The fix returns that same diagnostic rather than adding catches
or expanding accepted TOML rewrite layouts. The missing-status unit test also
asserts unchanged bytes. [Focused results](refusal-and-carrier-tests.txt) follow.

This is a narrow helper repair with integration-test extensions, not a phase close.
The previous source package's stable full-suite evidence remains historical;
current focused, architecture, smoke-budget and strict checks are recorded here.
The shared test-harness initialization change also receives a fresh full-suite run.
All prior crash/process-loss, explicit residue reconciliation, fixture provenance,
Drafted-rider and separate first-approval reservations remain unchanged.

The wider focused run exposed an existing collection-order dependency in three
primary test modules: sibling imports preceded the common `load_script` setup.
The common harness now initializes the script path before collection. The
existing guarded setup in load_script remains; no per-module workaround was added. The initial collection errors and partial passing results are
preserved in `collection-before.txt`, not reported as a successful run.

The first independent source review requested the missing caller census. Its
full prompt, response and binding are retained in `round-001/`; the exact census
and every observation are resolved in [the review response](REVIEW-RESPONSE.md).

The [second source review](round-002/review-result.txt) found the missing subject
check. WI-624 separately repairs it and is a hard prerequisite of WI-623. The
proof map includes the failing reproducer and stronger negative-query observation.
The full-suite evidence precedes that narrow final predicate; the final focused
results cover the subsequent change. No broader full-suite claim is made.

Final independent [source review](review-result.txt): APPROVE for the exact tree
recorded in [invocation metadata](review-meta.json). The full prompt and actual
provider response are preserved. This is not primary semantic acceptance.
