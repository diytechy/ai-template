e3754af6 NOT YET READY

## BLOCKER

1. **The proposed squash exemption contradicts risk 6.**  
   docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md:399 and :663; README.md:300.  
   The note first requires text/snapshot separation against each commit’s parent, then recommends exempting the trunk squash as a “replay.” That squash introduces both changes against its trunk parent. Checking archived lane commits does not enforce the coupling rule at the commit making the trunk change. Q-8 reopens OI-101 Q2 without identifying the exemption as a change to that ruling. Reconcile squash landing and trunk separation before presenting an executable design.

2. **The authority preserves a tool-writer bypass and waits under the lock.**  
   docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md:76, :110 and :147; docs/decisions/wi-788.toml, D-016.  
   Coordinator commits are classified alongside the owner’s commits as “not the tool’s,” although the coordinator is an agent executing tool writes. That exempts an existing writer from OI-103 Q1’s WI-and-merge requirement. A pre-commit check also leaves a race between checking authority and advancing the ref; it does not hold exclusion through advancement. Separately, the sitting explicitly waits up to 1,200 seconds while holding authority, contrary to the recorded Q2 rule. D-016 cannot settle these authority exceptions as implementation choices.

3. **The author exclusions prohibit the ruled spine-authoring flow.**  
   docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md:113; 4-adjudication-mint-landing.md:294, :317 and :368.  
   `ask` excludes every author’s family, and act authorization requires an adjudicator family different from every author of the scoped rows. But OI-101 Q1 explicitly lets the adjudicator draft those rows and later approve on an unchanged pass. The stated exception is not carried into either mechanism. The adjudication reviewer also authors edits before serving as the retained final reviewer. With the current two-family enabled pool, blanket exclusions can leave no eligible family. Define the exact judged scopes and implement the recorded exception consistently in routing, session reuse and act admission.

4. **PAGE recovery tries to resume a terminal parent.**  
   docs/plans/2026-10-04-wi788-design/3-planning-tiering.md:259 and :262.  
   PAGE hands the parent back, then adds an OI dependency to “hold” that parent and promises a later `round-2`. Today handback moves it to terminal `partial/`; schedule explicitly never reclaims it and requires a successor. See project-trajectory/scripts/handback.py:449 and project-trajectory/scripts/schedule.py:680. The note itself says terminal parents are never re-admitted. Owner resolution therefore has no schedulable recipient. Specify successor allocation, evidence transfer and the successor’s dependency edges.

5. **The decisions-note exclusion rests on a false code premise.**  
   docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md:174; docs/decisions/wi-788.toml, D-014.  
   S9 does not restrict every judge to a verdict file: its current reader selects REVIEW-A/B only, at project-trajectory/scripts/kitlib/verdict.py:189 and :944. The observation re-judge explicitly commits an observation record as well as its verdict, at project-trajectory/prompts/adjudicate-rejudge.template.md:43–56. Moving rejudge into `[judge]` while withholding its decisions note can leave it owing a record at landing without instructions to produce one. Distinguish verdict-only calls from judgment calls that write other evidence.

## MAJOR

1. **The graph is acyclic but its successor contracts are not dependency-complete.**  
   docs/plans/2026-10-04-wi788-design/README.md:261; 4-adjudication-mint-landing.md §11.  
   Concrete failures:
   - S788-station-authority requires *every* tool writer to pass through MERGE, before S788-landing supplies that operation and S788-mint moves intake’s remaining writers.
   - S788-spine-authoring requires exhausted rows to be minted, but does not depend on S788-mint.
   - S788-retire-legacy-config-and-carriers requires in-lane adjudication without depending on the sitting that supplies it.
   
   Simply adding the first missing dependencies creates a cycle because landing already depends on authority. Redistribute the writer moves and acceptance criteria into independently landable slices. Each row also needs an explicit review bar; the common declaration currently specifies tests only.

2. **Cancellation and crash recovery remain contradictory or unassigned.**  
   docs/plans/2026-10-04-wi788-design/1-state-evidence-recovery.md:192 and §8; 4-adjudication-mint-landing.md:93 and §11.  
   Chapter 1 correctly establishes that refresh refuses dirty work and preserves agent judgment. Chapter 4 instead says cancellation makes the next refresh discard uncommitted sitting writes, without specifying process termination or prior U1 harvest. F1’s interrupted-refresh recovery is deferred to landing, but landing’s scope and Done-when never include it. F2’s incomplete-unload retry likewise lacks an assigned recovery contract. B1 requires recovery at these boundaries, not merely detection.

3. **The return bound lacks an executable exhaustion outcome for upheld defects.**  
   docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md:179, :277 and :306.  
   Every upheld dispute returns the lane; lane-work bar failures return it too; a fourth sitting may not return. The exhaustion language explains dropping acts and minting unsettled spine rows, but does not explain an upheld code defect at that boundary. Specify the terminal outcome and successor treatment without waiving the red bar or leaving the lane stranded.

4. **Per-item squash landing does not settle existing multi-item lanes.**  
   docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md:326 and :584.  
   Today the dispatcher intentionally batches several spine WIs onto one branch and one worker, including shared re-attestation windows: project-trajectory/scripts/dispatch.py:30–34. The provider preserves per-WI outcomes, yet landing promises one squash per item, each equal to the final attested tree. No batching retirement or commit-partition policy explains how that works. This affects both landing identity and recovery for mixed outcomes.

5. **Provider research does not yet settle the required account and stream contracts.**  
   docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md §5 and :543; README.md:98.  
   Named gaps include Claude/Codex free-plan availability and limits, Claude login isolation on Windows, Gemini’s exact statistics fields and stdin delivery, and whether a pinned FreeLLMAPI model changes serving family through failover. Untested routes are permitted, but undocumented adapter fields and unresolved account isolation leave builders guessing. Complete the documentation-derived contracts and state precisely what remains a live-verification obligation.

6. **U1 needs invocation-level usage attribution, not only row deduplication.**  
   docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md:315 and :351.  
   Codex usage is thread-cumulative, as both the note and project-trajectory/scripts/session_adapters.py:480 confirm. Transcript/export recovery also includes earlier invocations of retained sessions. Keying ledger rows by invocation id prevents duplicate rows but does not prevent counting previous usage again. Specify usage scope, per-invocation cursors or baselines, and recovery attribution across resumed calls.

7. **The closing matrix and required gap inventory are incomplete.**  
   docs/plans/2026-10-04-wi788-design/README.md §“The amend / preserve / retire matrix”; 4-adjudication-mint-landing.md:346.  
   These earlier-review inventory items receive no explicit fate anywhere in the note: SR-173, LLR-137, LLR-220, LLR-246, TC-218, IF-123, IF-129, IF-228 and IF-242. They include regeneration, off-spine approval coverage, held-status writer enforcement and checkpoint reads—relevant to this redesign. D1–D6’s affected cells are also explicitly left unverified. The decisions gap supplies counts and categories, but not the requested list of missing-record lanes. B12’s matrix and gap-list obligations remain unfinished.

## MINOR

1. **Session-slot keys contradict each other within chapter 2.**  
   docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md:226 and :236.  
   Slots are first keyed by family/scope, “never by route,” then keyed by `route@account`. Resolve the wording so implementers do not restore the per-route retention split.

2. **Some checkpoint questions need no new owner decision.**  
   docs/plans/2026-10-04-wi788-design/README.md:293–295.  
   Q-1 can flag the already-directed migration; Q-2 is an implementation location choice; Q-3’s Gemini option reopens the documentation-only ruling. Separate required provisioning/spend authorization from routine choices and already-settled policy.

3. **The index overstates its arbiter evidence.**  
   docs/plans/2026-10-04-wi788-design/README.md:297; 3-planning-tiering.md:100 and :112.  
   “Always picked its own family” drops chapter 3’s explicit uncertainty for DP-003. Agreement between arbiter runs and zero ports also does not establish that arbitration changed no selection outcome. Preserve those distinctions in the owner’s first-read summary. The requested WI-199 research remains acknowledged as unfinished at README.md:320.

## Verified

Read the complete spec, all five note files, decisions record, OI-101/OI-103 decision cells, S11 plan, earlier Sol review and repo guidance. Code checks confirmed the retained-home override, missing dual pickup, plain-call attribution gap, dirty-refresh refusal, exact-tree Bar-Green verification, approval-scope refusal and unsupported-filesystem lock fallback. The twenty-row graph has no cycle. Documentation validation found zero broken links. HEAD remained e3754af6; staged and working diffs stayed empty. No test suite or live model probe was run.

## Commands

Repeated file reads and searches are grouped below; inline Python programs were passed on stdin and created no files.

| Command | Summary |
|---|---|
| `Get-Content CLAUDE.md` | Read governing repo guidance. |
| `Get-Content .agents/skills/antidote/SKILL.md; Get-Content .agents/skills/session-protocol/SKILL.md` | Read applicable review/session guidance. |
| `git status --short; git show --stat e3754af6` | Clean worktree; confirmed design commit and eight changed files. |
| `Get-Content` of WI-788, PROCESS.md, status.md, README.md and wi-788.toml | Read spec, process, working context, index and delegated calls. |
| Numbered `Get-Content ... \| ForEach-Object ...` reads | Read complete chapters; supplemented WI-788:280–875 and :568–592, PROCESS.md:145–1020, and OI records:3732–3787 / :3813–3830. |
| `Get-Content docs/plans/2026-10-03-s11-in-lane-adjudication.md` | Read plan and all seven recorded rulings. |
| `Get-Content docs/reviews/2026-10-04-wi788-widened/sol-review.md` | Read prior findings and required inventory. |
| `$env:GIT_CEILING_DIRECTORIES = 'C:/Projects/ai-template.wt'; C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_docs.py --root . --stale` | Exit 0: 2017 docs, 3401 links, 0 broken; 1 orphan warning and staleness hints. |
| `rg -n` searches across planning, scheduling, integration, bookkeeping and dispatch modules | Located PAGE, terminal-state, allocator, locking and batching behavior. |
| Inline `python.exe -B -` reader: service, retention, schedule, station, bookkeeping and preflight ranges | Confirmed current lifecycle/account premises. |
| Inline `python.exe -B -` reader: integrate, acceptance, OpenCode adapter and plan-round ranges | Confirmed refresh, tree identity, scope and stream behavior. |
| `rg -n` searches for escalation, usage scope, recording, index callers and lock handling | Located relevant implementations; confirmed index writer has no caller. |
| Inline `python.exe -B -` reader: adapters, loop, decisions, handback and PROCESS | First attempt stopped on an out-of-range line; next stopped on console encoding; corrected bounded UTF-8 reader succeeded. |
| Inline `python.exe -B -` TOML/graph probe | Read selected registry contracts; verified twenty successors and no cycle. |
| `Get-Content docs/agents-enabled; Get-Content docs/agents.toml` | Confirmed current enabled pool contains Anthropic and OpenAI families. |
| `rg -n` for review-scope, rejudge and observation writes; `rg --files project-trajectory/prompts` | Confirmed S9’s limited phase domain; one searched design-check filename was absent. |
| Numbered verdict.py read; `Get-Content project-trajectory/prompts/adjudicate-rejudge.template.md` | Confirmed observation rejudge writes beyond its verdict. |
| `rg -n` for batching and matrix IDs | Confirmed multi-WI lanes. Initial Windows wildcard-path searches failed; corrected directory/`-g` searches succeeded. |
| Inline `python.exe -B -` inventory probe | Confirmed the nine named prior-review IDs are absent from the note. |
| `rg --files C:/Projects/ai-template.wt/review-tmp -g '*ch3*' -g '*baseline*'` | Searched for research-probe artifacts; returned existing scratch paths. |
| `rg -n 'WI-199\|WI-209' docs/archive/work -g '*.md'` | Located archived planning records. |
| `Get-Content docs/archive/work/complete/WI-199-coordinator-dual-plan-wiring-agent-loo.md` | Read WI-199’s original delivered behavior. |
| Numbered session_keep.py:657–700 read | Checked retained-call bookkeeping and compaction handling. |
| `git rev-parse HEAD; git diff --exit-code; git diff --cached --exit-code` | HEAD e3754af6; both diffs empty. |
| Repeated `git status --short` / `git status --porcelain=v1` | Worktree remained clean. |