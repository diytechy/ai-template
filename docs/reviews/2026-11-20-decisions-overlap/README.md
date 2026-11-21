# Decisions-record overlap with the spine: the judged sample (2026-11-20)

Which calls in `docs/decisions/*.toml` restate what a spine row already states. Evidence for WI-1013.

**Method.** Each of the 1,193 entries (the `-000` examples left out) was matched to its likeliest LLRs: those under its work item's SRs, those its spec or the entry names, and the two closest by TF-IDF cosine over all LLRs. Entries were banded by their best cosine, and 106 drawn (every band-A entry, a seeded random draw from the rest). Three Claude readers classified each entry against its candidate LLRs, by its main decision, into RESTATES (an LLR states the choice), PARTIAL (an LLR states part; the entry adds a choice no LLR states), DESIGN-BELOW-LLR (a product design choice no LLR states), SCOPE (a reading of the spec, Done-when or a requirement's reach) or PROCESS (the conduct of the run). Band shares were weighted back to the whole.

| Category | Weighted share | About |
|---|---|---|
| PROCESS | 57.5% | 686 |
| SCOPE | 12.3% | 147 |
| DESIGN-BELOW-LLR | 11.1% | 133 |
| RESTATES | 10.3% | 123 |
| PARTIAL | 8.8% | 104 |

Band D (774 entries) had 30 drawn and none RESTATES, so the true RESTATES share could run to about 1 in 6. A RESTATES verdict means a reader of today's LLR already knows the choice; several such LLRs read as written from the entry by the same run.

| Entry | Band | Category | LLR | Why |
|---|---|---|---|---|
| coordinator-2026-10-11#D-004 | A | RESTATES | LLR-270 | LLR-270 states per-call markers, publish-then-apply, clock-first readers, no StoreBusy, pending reset, retire_scope publisher id. |
| coordinator-2026-10-14#D-015 | A | RESTATES | LLR-248 | Chosen reading (claim or any marked loop-writer commit makes a loop lane) is LLR-248's stated definition; borderline scope. |
| coordinator-2026-10-14#D-017 | A | RESTATES | LLR-248 | Window closes at unmarked one-parent same-tree re-claim with exact subject; stated verbatim in LLR-248. |
| coordinator-2026-11-01#D-006 | A | RESTATES | LLR-361 | Field copied, legacy reads unknown not empty, commit-bound plus monotone boundary: all stated by LLR-361. |
| wi-790#D-012 | A | RESTATES | LLR-299 | LLR-299: report row when no cited item pending or absent, 'a row citing none included'. |
| wi-791#D-009 | A | RESTATES | LLR-245 | LLR-245 states verdict_rel normalization and _refuse_verdict refusing absolute paths outside repository. |
| wi-806#D-003 | A | RESTATES | LLR-302 | LLR-302: a path, cell or row counts only when it differs from every parent. |
| wi-806#D-004 | A | RESTATES | LLR-302 | LLR-302 states the SQUASH_MSG exemption: ancestor tip, byte-equal registries, judge HEAD..tip commits. |
| wi-818#D-007 | A | RESTATES | LLR-304 | LLR-304 states statement scanner, comment keeping, NaN re-parse check, migrate_decisions.py home. |
| wi-818#D-012 | A | RESTATES | LLR-303 | LLR-303 module cell names kitlib/decisions.py and kitlib/git.py; detail gives overrule_sync_lines' reader signature. |
| wi-818#D-014 | A | RESTATES | LLR-303 | Surrogateescape decode, UnreadableBlob before git, unread path left alone: all in LLR-303. |
| wi-818#D-015 | A | RESTATES | LLR-284 | LLR-284 names kitlib.decisions.missing_record_refusal, refused-name-as-absent, and both refusal forms. |
| wi-834#D-003 | A | RESTATES | LLR-318 | Keeping wait_out_blackout via blackout_at and routing every loop launch through through_blackout is LLR-318 verbatim. |
| wi-834#D-017 | A | RESTATES | LLR-047 | LLR-047 and LLR-320 state launcher resolves interpreter, hands it to readiness op, which never searches. |
| wi-835#D-012 | A | RESTATES | LLR-306 | Exclusive empty reservation, refusal of existing path, no read after failed call, empty-is-missing, pre-launch cleanup: all in LLR-306. |
| wi-841#D-017 | A | PARTIAL | LLR-277 | LLR-277 states tier_carriers/tier_rows_from_text home; acceptance_record routing every tier through them is unstated. |
| wi-842#D-006 | A | PROCESS |  | Main choice is how the run refreshed skill mirrors (byte copy plus check, not bootstrap --sync). |
| wi-880#D-002 | A | SCOPE | LLR-326 | Scopes SR-032's install clause to this repository's dev setup, excluding shipped templates. |
| wi-911#D-016 | A | SCOPE | LLR-311 | Folds the dismissal-language fix into this lane, not a successor row; the fix text itself is LLR-311's. |
| wi-927#D-010 | A | SCOPE |  | Reads Done-when ratchet line as met via Trust note, leaves SR-229 to sitting; checkpoint reconcile record. |
| wi-961#D-015 | A | SCOPE | LLR-355 | Answered a sitting return by amending LLR-355/IF-306 text instead of changing code behaviour. |
| coordinator-2026-10-04#D-010 | B | PROCESS |  | Commit grouping: regenerated open-items.html rides each pause commit to keep the hook green. |
| coordinator-2026-10-10#D-004 | B | RESTATES | LLR-322 | LLR-322: committed settings hold no guard group; install consented, machine-local, bound to running interpreter. |
| coordinator-2026-10-10#D-022 | B | PROCESS |  | Accepts verdict despite refused brief, closes by hand, files kit gaps: run handling of tool refusal. |
| coordinator-2026-10-15#D-021 | B | RESTATES | LLR-322 | LLR-322: without a terminal the lease take refuses and names the consent step. |
| wi-798#D-004 | B | DESIGN-BELOW-LLR |  | CLI flag rename (--route, no --family alias) and sign-in line format; no LLR states either. |
| wi-798#D-008 | B | PARTIAL | LLR-305 | Competing-credential refusal stated by LLR-305; per-CLI withheld variable lists stated by no LLR. |
| wi-834#D-001 | B | RESTATES | LLR-322 | LLR-322 states the shipped inert example and the consented install of only its guard groups. |
| wi-834#D-007 | B | PARTIAL | LLR-320 | Terminal-only offers and exit codes stated; offered item list, no setup.sh chaining, Windows stdin rule not. |
| wi-835#D-011 | B | RESTATES | LLR-306 | LLR-306: runs only from a claimed lane worktree, otherwise refuses before launch; helper choice is minor. |
| wi-835#D-013 | B | RESTATES | LLR-305 | LLR-305 states exactly the documented claude/codex sign-in answer pairs; everything else unknown. |
| wi-835#D-015 | B | RESTATES | LLR-306 | Creating missing parents, refusing uncreatable parent, leaving created directories on refusal: LLR-306 states each. |
| wi-841#D-002 | B | PARTIAL | LLR-309 | Three hold points and read bases are stated (LLR-309/307); worker_endstate as home is not, now contradicted. |
| wi-841#D-003 | B | RESTATES | LLR-307 | LLR-307 states bound_items tick/evidence reading and sha256:<16 hex> digest over id and items. |
| wi-841#D-015 | B | RESTATES | LLR-307 | LLR-307 states claim_copy absent releases, unreadable holds at dispatch, hand close, merge, refuses mint. |
| wi-841#D-021 | B | RESTATES | LLR-310 | Kinds bound in <verdict>.requested at reservation, one parser: LLR-310 and LLR-306 state it. |
| wi-841#D-027 | B | RESTATES | LLR-278 | Row-level ruling coverage whether or not act names verdict; named verdict must authorize: LLR-278. |
| wi-846#D-005 | B | SCOPE |  | Owner ruling moves lockless marker and contention work out of WI-846 into WI-858. |
| wi-850#D-002 | B | SCOPE |  | Chose which Done-when remedy (SR-224 approval, not demotion) and how SR-224 text reads. |
| wi-853#D-003 | B | RESTATES | LLR-069 | LLR-069: exclusion resolves only when cited accepted DISMISS ruling rules that finding; otherwise a finding. |
| wi-918#D-007 | B | PROCESS |  | Convergence map of review round findings to fixes before the gate. |
| wi-927#D-006 | B | PROCESS |  | Review round 1 findings triage and fix-round planning. |
| wi-961#D-007 | B | RESTATES | LLR-347 | LLR-347 states finish-notice finality (task notification or spawner tool result); session transcript never finished. |
| wi-963#D-014 | B | RESTATES | LLR-364 | Narrowed settlement rule arms (i) and (ii) are LLR-364's detail verbatim. |
| wi-963#D-019 | B | SCOPE | LLR-364 | Scopes Done-when item 5 via Trust section to keep pass record bound; F2 text later in LLR-364. |
| wi-982#D-004 | B | SCOPE | LLR-360 | Which row to amend: add sentences to LLR-360 rather than narrow TC-399; plan left unedited. |
| coordinator-2026-10-04#D-002 | C | PROCESS |  | Recovering from an out-of-order claim after a hook refusal by resetting and redoing commits. |
| coordinator-2026-10-07#D-003 | C | PROCESS |  | Session conduct under latched guard: mint only, claim nothing, hand back lease. |
| coordinator-2026-10-10#D-002 | C | SCOPE |  | Row split decision: WI-847 stays one row with stated build order. |
| coordinator-2026-10-14#D-002 | C | SCOPE |  | Splitting batch row B1 into WI-911 and WI-912 at filing. |
| coordinator-2026-10-14#D-012 | C | DESIGN-BELOW-LLR |  | Data shape: adoption record as a declared Adopted column with one strict reader; LLR-345 omits storage. |
| coordinator-2026-10-16#D-009 | C | DESIGN-BELOW-LLR |  | Bar step order (lints, docs, budget last with sole timed tier run) stated by no LLR. |
| coordinator-2026-10-20#D-004 | C | SCOPE |  | Filing a queue item as two rows with dependency edges and deferred amendments. |
| coordinator-2026-11-01#D-007 | C | PARTIAL | LLR-362 | Adopted MINOR's floor (larger of carrier and trunk mark) is in LLR-362; spine-author prompt Done-when item is not. |
| wi-788#D-024 | C | PARTIAL | LLR-144 | Partial close and quarantine shape stated; choosing them for a lane owing a return at fourth sitting not. |
| wi-790#D-018 | C | RESTATES | LLR-298 | LLR-298 reads open-items registry through either carrier; LLR-299 matches SpecRef under either spelling. |
| wi-798#D-002 | C | DESIGN-BELOW-LLR |  | Repo routing config uses weight 0 per phase instead of new grammar value; no LLR states it. |
| wi-798#D-005 | C | DESIGN-BELOW-LLR |  | When the login status probe runs (retained only) and home-exists check; LLR-305 states probe form only. |
| wi-818#D-008 | C | RESTATES | LLR-283 | Blank note is a finding; review_queue and newly_overruled still read it overruled: LLR-283. |
| wi-838#D-002 | C | RESTATES | LLR-270 | LLR-270: observation lands only while record carries the call's own lease, else store moved on. |
| wi-841#D-013 | C | RESTATES | LLR-262 | LLR-262: covering SUCCESSOR mints only its Done-when part's drafts, refusing repeated or missing Dispositions. |
| wi-841#D-018 | C | RESTATES | LLR-278 | LLR-278: every carrier path of authorized registry, deleted obsolete copy included, authorized; others WIDENED. |
| wi-841#D-024 | C | PARTIAL | LLR-306 | Success criterion stated in LLR-306; one shared call_succeeded and plan['call_ok'] plumbing not. |
| wi-852#D-002 | C | SCOPE |  | WI-852 stays render-only; filed round files gain no merge authority. |
| wi-875#D-001 | C | PROCESS |  | Coordinator chose to run a consolidation round at owner request despite recent judging. |
| wi-881#D-004 | C | PARTIAL | LLR-026 | LLR-026 states unopenable member raises; closing job via active-process limit before snapshot is unstated. |
| wi-911#D-019 | C | PROCESS |  | Triage of three reviewers' gate findings: adopt, defer, or reject each. |
| wi-912#D-011 | C | PROCESS |  | Run ordering: rebase between judging and act turns to exercise verdict crossing a rebase. |
| wi-921#D-002 | C | PROCESS |  | Accepts critique MAJOR and revises plan before second critique. |
| wi-925#D-007 | C | PROCESS |  | Review round 1 triage, stand-in reviewer, regrading findings to checkpoint, fix-round planning. |
| wi-943#D-004 | C | DESIGN-BELOW-LLR |  | Refusal message wording: bless-mark remedy appended only for refused amendment rows; no LLR states it. |
| wi-960#D-005 | C | SCOPE |  | Gitignore template gap ruled outside P3's surface, left to next leg's decision. |
| wi-963#D-005 | C | PROCESS |  | Review round 1 triage and pre-checkpoint builder stage planning. |
| wi-966#D-004 | C | PROCESS |  | Commit build stage as built rather than hold for D-005's fix. |
| wi-978#D-018 | C | RESTATES | LLR-363 | Fix rule (landing-brought retirement record refuses live id; parent-held pair passes) is LLR-363's sentence. |
| wi-982#D-005 | C | PROCESS |  | Review round triage: a MINOR costs no fix round; checkpoint follows. |
| coordinator-2026-10-04#D-009 | D | PROCESS |  | Claims whole ready batch under one scoped unpause. |
| coordinator-2026-10-05#D-003 | D | PROCESS |  | Rebase timing and smoke-ceiling note joined without a re-stamp. |
| coordinator-2026-10-08#D-005 | D | PROCESS |  | Environment handling: coordinator set token-file variable for the lane's own sittings. |
| coordinator-2026-10-10#D-009 | D | PROCESS |  | Smoke-tier membership ceiling re-stamped once on trunk. |
| coordinator-2026-10-10#D-010 | D | SCOPE |  | Work-item dependency edge: WI-884 needs WI-847 only, not WI-800. |
| coordinator-2026-10-10#D-016 | D | PROCESS |  | Consolidation read and queue reordering of WI-823 before unattended run. |
| coordinator-2026-10-15#D-001 | D | PROCESS |  | Deferring row filing to next session for context budget. |
| coordinator-2026-10-20#D-007 | D | PROCESS |  | Claim ordering: WI-962 ahead of P2-P6 queue rows. |
| coordinator-2026-10-22#D-001 | D | PROCESS |  | Headless leg claim selection, no re-critique, not batching WI-850. |
| coordinator-2026-11-03#D-004 | D | PARTIAL | LLR-366 | Q1 in LLR-366, Q2 in LLR-367; Q3 (check_test_first untouched) and row filing stated nowhere. |
| wi-788#D-026 | D | SCOPE |  | Restructured successor rows' dependency edges and review bars to avoid a cycle. |
| wi-798#D-011 | D | DESIGN-BELOW-LLR |  | Import placement: agent_route imported inside scoped_route rather than new kitlib module. |
| wi-823#D-002 | D | PROCESS |  | Land on existing gate without another full-lane round since reviewed tree unchanged. |
| wi-842#D-004 | D | PARTIAL | LLR-300 | Hand-back refusal naming operator's release is in LLR-300; extracting shared helpers _not_holder/_promptless is not. |
| wi-849#D-001 | D | PROCESS |  | Dispatches build rounds before Done-when sitting judges amended text. |
| wi-866#D-002 | D | PROCESS |  | Repairing duplicate act seq after rebase without bypassing the hook. |
| wi-878#D-004 | D | PROCESS |  | Round numbering after a prior leg's unfiled reviewer launches; stand-in reviewer recorded. |
| wi-884#D-008 | D | SCOPE | LLR-313 | Keeps review_refusal because LLR-313 names it; removal needs row text, deferred to checkpoint. |
| wi-892#D-003 | D | PROCESS |  | Deferred-import window ceiling re-stamped 32 to 33 rather than restructure imports. |
| wi-912#D-013 | D | PROCESS |  | Gate review triage: MINORs routed to follow-ups, no post-gate fix. |
| wi-927#D-004 | D | DESIGN-BELOW-LLR |  | Message wording on hook pickup by running sessions, plus module move; LLR-322 states neither wording. |
| wi-931#D-008 | D | PROCESS |  | Convergence map of round findings to evidence before the gate. |
| wi-946#D-007 | D | PROCESS |  | Rebase conflict resolution delegated to builder; review-round accounting. |
| wi-955#D-003 | D | PROCESS |  | Fix round run as one builder dispatch in two stages, skipping release step. |
| wi-955#D-006 | D | PROCESS |  | Gate verdict recorded; lane lands alone and WI-956 rebases. |
| wi-956#D-009 | D | PROCESS |  | Convergence map of findings before the uncounted gate. |
| wi-967#D-003 | D | PROCESS |  | Review round triage: regrade MAJOR to checkpoint spine text, fix MINORs before checkpoint. |
| wi-976#D-015 | D | PROCESS |  | Gate finding disposition: MINOR listed as owner follow-up, not reverted. |
| wi-993#D-003 | D | DESIGN-BELOW-LLR |  | Accepts per-range title dedup residual instead of item-by-item dedup; no LLR states it. |
| wi-996#D-003 | D | PROCESS |  | Recovery after machine crash: stash, rebase, keep crashed builder's partial build. |
