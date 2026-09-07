# Runtime review dispositions — preparation, 2026-09-07

Source review: [independent Opus report](2026-09-07-approval-runtime-opus.md).
These dispositions concern the runtime repair. They approve no live registry
cell, snapshot or disputed preserved-lane judgment. Final verification and
review follow-up remain pending.

| Finding | Disposition |
|---|---|
| M1 repeated completion replay | Fixed by caching only successful exact replay proofs in process, keyed by resolved repository, immutable publication commit and serialized immutable turn. Reachability is still read from Git on each query; no unverified trailer or negative result is cached. A restart independently verifies each publication again. Repeated completion/pending queries and forged/new-binding cases have a regression. |
| M2 widened snapshot write set | Fixed at the shared copier: primary publication supplies `exact_rels` equal to its accepted registry set. The existing copy loop cannot expand that set through unrelated Status flips or newly Approved rows. Legacy manual callers retain their existing selection behavior. Real-carrier tests preserve out-of-scope snapshots while copying the accepted registry. |
| M3 ordinary governing edits refused | Intended boundary under handoff execution step 2: implementation needing governing spine changes hands back to separate exclusive spine authoring. Module allocation is governing; only the explicitly permitted CodeSymbol/TestRefs and Evidence edits remain implementation trace writes. The old SR amendment fixture now declares spine authoring and still proves post-merge amendment intake. The route survives; ordinary work does not gain authority to amend an SR. |
| M4 stale test entry points | Fixtures now patch the extracted helper's actual module and invoke the primary session callback. Both integrator modules ship together in every supported scaffold, so their physical script directory remains identical; the old patch location did not describe a supported distinct-directory deployment. Harness provenance assertions remain. |
| M5 unavailable optional telemetry | The author remains bound to the proven judgment, actual model and coordinator-generated invocation identity. Provider route and provider-specific session identifiers contribute when present; their absence does not fabricate values or prevent a RETURN from supported unmanaged routing. |
| m1 arbitrary consolidation judgment | The publication plan passes its proven current judgment path to primary close. Primary consolidation refuses without that path; it never searches unrelated historical verdicts. |
| m2 unused publication peel | Deleted the unused higher-level wrapper and callback parameter. Ordinary lane identity retains only its verified refresh peel. Publication completion has its own exact verifier. |
| m3 snapshots called unchanged history | Snapshot paths are excluded from the immutable history classification; meaning impact must give them a live disposition matching the publication. |
| m4 interruption during staging | Retained fail-closed residue handling. The Git commit is the authority point: before it, HEAD still contains the queued proposal and pending selection; an interrupted index/worktree may contain the staged projection. Relaunch refuses dirty residue. A supervisor must compare the residue with an independently derived projection at HEAD before restoring that exact candidate. Arbitrary dirty files must never be automatically discarded. This is an explicit recovery limit, not a claim of atomic filesystem writes or seamless resumption after a kill during staging. |
| m5 copier SystemExit | Translated to a normal publication refusal at the copier call boundary, with the temporary candidate-date binding restored. |
| m6 fenced TOML headings | Proposal definition extraction uses the existing fence-aware Markdown reader; a TOML comment beginning with `##` cannot become a document section. The immutable-proposal test covers a fenced heading and still refuses a real proposal edit. |
| m7 repeated judgment identities | The selected evidence is the latest qualifying coordinator log in Git chronology. A same-commit ambiguity refuses rather than relying on filenames. |
| m8 disposable environment | The product bar runs candidate-local scripts with the primary checkout's harness environment, passed explicitly into the disposable projection. |
| m9 schema and migration text | Separately [authored](2026-09-07-approval-contract-schema-launch-authoring.md) and [reviewed](2026-09-07-approval-contract-schema-launch-luna.md) clarification reconciles explicit registry/blob maps and supported launch-time selection. |
| m10 scope classifier | Retain the owner's required existing scope-based verification policy. The exact projection verifier limits actual effects to the reviewed approval, close, parsed successors and regeneration; the existing surface classifier chooses the product bar over that derived output. Broad path classes do not grant the model arbitrary write authority. |

Additional regressions found during preparation cover direct linked-checkout
publication, successful hooks that smuggle staged files into a commit, and
consolidation subject IDs being incorrectly required as registry decisions.
The publisher now validates checkout identity before staging, verifies the
actual committed tree before success and restores its candidate on a mismatch.
Consolidation retains its full bound work-item subject scope and separately
has an empty registry approval scope under its existing typed judgment.

The real scaffold passes its existing generated-content freshness checks after
publication. Regeneration may update informational commit stamps, which those
checks have always excluded; this does not weaken substantive byte comparison.

The broader absorption work remains queued under its existing owner. Brief
rendering of historical verdict/UNJUDGED and history-reader consumption remain
outstanding; this repair does not claim to have completed them.

## Independent follow-up

The [Opus follow-up](2026-09-07-approval-runtime-opus-followup.md) approves the
runtime repair with stated operational limits and finds no launch blocker.
The frozen-copy manifest was verified by the supervisor after that review;
the reviewer correctly disclosed that it did not read the parent manifest.

One factual correction to its launch paragraph: scheduler rank is not admission
order. The actual `_admission` call over the current parsed frontier returns
`admit-exclusive`, `[WI-605]`, after `_judgement_first` moves adjudications
ahead of spine work. The consolidation census returns no draft because existing
adjudications already own the queue. The pure read-only proof is retained in
`out/run-logs/approval-preflight-admission.json`. Thus the supported dispatcher
preserves the interrupted adjudication as the first turn without preselection.

For this supervised retry, never commit or discard dirty primary publication
residue while a turn is pending. Verify it against an independently derived
projection at its original committed candidate before any restoration. The
generic dirty-tree banner is not a recovery instruction for this case. Current
managed routes and the unmanaged default all supply a nonempty model; future
unwired configurations and the remaining history-query cost are follow-ups,
not newly relaxed preconditions or changes to the measured configuration.

## Final owner-only traversal check

The full suite passed before the final two-line spec-mover exclusion. A
synthetic owner-file fixture then demonstrated that close-time inbound relinking
could access private content. The mover now consults the existing shared
owner-only path set before content access; the actual scratchpad was not read.
The mover/publication/structural checks passed (39 tests);
[the independent bounded review](2026-09-07-owner-relink-luna.md) records the
exact approved bytes. This supplements the frozen runtime review without
extending any artifact approval.
