# Carrier clause-to-proof correspondence

This is an authored evidence map for fresh semantic judgment, not an acceptance
ledger. All referenced tests are real tests in the final source candidate.

| TC-205 refusal class | Directly driven carrier proof |
| --- | --- |
| Forged subject | First-approval fixture `[forged-subject]`: alter only the subject of the real publication; all other proof fields and its tree stay genuine. `_verified_candidate` compares the first line to the shared `_subject` definition. |
| Wrong WI | `test_real_first_approval_snapshot_and_successor_are_one_commit[wrong-WI]`: foreign WI/turn record and carrier name fail against the actual selected candidate. |
| Wrong turn | `test_real_return_publish_and_completion_replay`: replace the actual turn trailer with a foreign turn. |
| Stale proposal | First-approval fixture `[stale-proposal]`: replace the immutable proposal-spec blob binding in the carrier's selection. |
| Stale candidate | Return fixture: replace the candidate with the old base; also copy genuine carrier words onto a later parent. |
| Extra path | First-approval fixture `[extra-path]`: add an unreviewed file to an otherwise real publication. |
| Missing path | First-approval fixture `[missing-path]`: remove the required complete spec. The return fixture separately removes all derived effects. |
| Cross-WI close | First-approval fixture `[cross-WI-close]`: move the genuine closed spec to another WI's terminal path. |
| Malformed successor | First-approval fixture `[malformed-successor]`: replace the genuine successor with invalid spec content. |
| Partial snapshot | First-approval fixture `[partial-snapshot]`: replace only the accepted snapshot with its previous Drafted content, keeping live approval. |
| Unreviewed decision | First-approval fixture `[unreviewed-decision]`: change the completed spec's decision without changing the reviewed candidate. |

Each first-approval variant starts from a successful real publication, preserves
its parent candidate, receipt and actual adjudicator author, changes the named
surface, clears the successful-proof cache and queries the forged commit. It
asserts refusal and then successful cold recognition of the original carrier.
The turn-name variant necessarily changes the corresponding selection path and
fields together. No claim is made that every possible malformed encoding is tested.
These are representative concrete cases for every named class; the general
coverage argument is exact reconstruction, not exhaustive input enumeration.

TC-147 supplies the construction side: `test_scope_and_unjudged_absorption_refuse`,
`test_standing_snapshot_requires_complete_approved_absorption_ledger` and
`test_review_owed_candidate_requires_existing_independent_approve` check the
projection's scope, absorption and independent-review admission. The real
first-approval fixture proves byte-equal snapshot/live state, exact close,
successor and watermark in one commit. Carrier recognition then reruns that
projection and compares the complete tree. The inference that these construction
refusals propagate to recognition follows that shared call path; it is not a
claim those unit cases themselves called the carrier query.

R4: `test_real_return_publish_and_completion_replay[scoped]` and `[required-bar]`
compare every primary file byte before/after a cache-cleared carrier query. This
includes refs, index, worktree, Git objects and FETCH_HEAD, with an index-only
sentinel, unstaged changes over that entry and an untracked file. The required-bar
variant runs real regeneration and check subprocesses inside the disposable
checkout; its deterministic check output joins the exact publication tree.
The test validates the actual query's reconstruction path using small candidate
scripts, not a full product suite or an arbitrary-script sandbox guarantee.

SystemExit: inspection found `_rewrite_toml_statuses` reachable outside the
snapshot-copy exception handler. Valid quoted `status` TOML passes the semantic
Drafted predicate but is conservatively refused by the bare-key writer. The
new `test_unwritable_status_is_a_publication_and_carrier_refusal` reproduced the
process exit, then proves returned refusal for publication and the carrier query.
The helper now returns its diagnostic through its sole production caller; no
additional catch, parser expansion, cache optimization or baseline change.
Existing snapshot-copy SystemExit handling and child-process exit-code handling
remain. This resolves the demonstrated path, not every hypothetical future exit.


## Exact refusal clauses and caller census

The first-approval variants `extra-path`, `missing-path`, `cross-WI-close`,
`malformed-successor`, `partial-snapshot` and `unreviewed-decision`, plus the
return fixture's missing-effects case, are all rejected by `_verified_candidate`'s
`expected != tree` comparison. These are different contractual failure examples
through one shared exact-tree check, not separate verifier branches. In particular,
the decision/snapshot mutations change the carrier, not the candidate seen by
`approval_projection`; their construction-side coverage remains the separately
cited TC-147 tests and the explicitly labelled shared-call-path inference.
`wrong-WI` fails the immutable selected-turn binding; `stale-proposal` fails the
carrier selection's equality with the committed selection. The return fixture's
foreign turn lacks its corresponding selection record; its replaced candidate
and copied-later carrier fail the parent/candidate equality check.

The required-bar variant deliberately uses a deterministic tree-writing check as
an observation instrument. Omitting that check would omit its sentinel and fail
reconstruction. This proves the real bar invocation/replay and read-only primary
boundary using that fixture; it does not claim the production bar writes that file.

The actual [caller census](caller-census.txt), [command and source hashes](caller-census.json)
and [caller context](caller-context.txt) enumerate every literal helper reference
in all Python production source under project-trajectory/scripts. There are only
the definition and `_apply_approval`'s call, which assigns the return and immediately
propagates a nonempty refusal. The retained `_apply_flips` implementation writes
nothing and does not call this helper. The census is about this kit's production
source; it makes no claim about unknown downstream code calling a private helper.

TC-147.Evidence already names all of `tests/test_primary_publication.py`, so it
includes the new unwritable-status test's construction arm. TC-205's explicit
test reference joins its carrier-query arm. No second copy of that test is needed.


## Subsequent subject repair and stronger negative query

The [second source review](round-002/review-result.txt) found a required class the
earlier map omitted: a forged subject. The [isolated reproducer](subject-before.txt)
changed only the subject of a real accepted carrier and incorrectly obtained the
candidate identity. WI-624 resolves that mismatch: `_subject(turn)` is the single
definition used both to construct the publication and to verify its first line.
The new case keeps the tree, parent, turn, receipt and author genuine, so the
refusal cannot be explained by another malformed field. This checks canonical
subject text; it does not treat a copied subject as sufficient evidence.

The intermediate [test result](subject-intermediate.txt) exposed older forged
fixtures now refusing at the earlier subject check. Their subjects were made
canonical so their existing tree/candidate assertions retain discrimination.
The wrong-WI variant also carries that foreign WI's canonical subject before
failing its immutable selection binding. No existing negative assertion was removed.

The status-query regression now observes the real status writer's returned
diagnostic during the query and compares every primary file byte before/after it.
Its canonical subject reaches reconstruction; the observed single writer refusal
distinguishes that path from later missing-receipt rejection.

The complete full-suite run predates this final narrow subject predicate and its
fixture changes. It validates the common-harness initialization and status-return
repair. Final focused primary/verdict/intake tests and architecture/commit checks
validate the subsequent subject change; no second full-suite result is claimed.
