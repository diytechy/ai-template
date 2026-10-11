# WI-887 checkpoint sitting 004 — amendment; first-approval

Judged at 6e7e50fe3 from the cells in the composed request, read against the
lane's code and tests only where a cell names a symbol or a test.

## amendment

Every amended row changed MEANING: each one adds a behaviour, admission or
verification clause the attested text did not carry. For each row the line
also says whether I would bless the new text. Five rows I would not: SR-227,
LLR-140, LLR-207, TC-205 and TC-266. Because each of the three registries
holds at least one of those five, no registry can be re-anchored in this
sitting (see the act note at the end of this section).

- [MEANING] SR-154 AcceptanceCriteria -> only a session minted for the review, over the whole lane, may clear integration -> also a round the coordinator recorded as final for the lane's retained final reviewer, where retention is on and persistence is selected; iteration rounds never clear, fresh or resumed -> a new admitting actor (the resumed final reviewer) is added. BLESS: yes. It agrees with SR-156 and LLR-207's new final kind. Its registry is held by SR-227.
- [MEANING] LLR-045 Detail -> fill the reviewer brief from the override or shipped template -> also review_template / review_round_templates resolve the template once per round and share that text between the brief and the retention identity; the draw-settled stage goes to format_scope only for a full brief -> new mechanism and a new stage-passing rule. BLESS: yes. The symbols exist (agent_brief.py). TC-351 and TC-205 carry its arms.
- [MEANING] LLR-262 Detail -> review_logs yields each log's gating span -> also reads the final-reviewer mode once per call through reviewer_dials and passes it to every gating_span -> new input to the gate reader. BLESS: yes.
- [MEANING] TC-205 Expected+Method -> only fresh full claim-base scope gates; retained-session rounds hold -> a final scope in persisted mode can also gate; Method adds the persisted-final boundary -> the verified admission set widened. BLESS: NO. Expected now contradicts itself. Its unchanged clause "narrow-only and retained-session rounds ... hold the gate" is unqualified, but the added clause lets a persisted final round, which is a retained session, gate. The Method was corrected to "retained-session full rounds and narrow rounds hold", but the Expected was not.
- [MEANING] SR-156 AcceptanceCriteria -> landing clears only from FRESH sessions; a retained-session review holds -> sessions started fresh, or the coordinator-recorded final round of the lane's retained final reviewer under persistence; iteration rounds and any other retained-session review hold -> a new admitting actor. BLESS: yes. Its registry is held by SR-227.
- [MEANING] LLR-140 Detail -> the gate is restricted to a full-lane round from a fresh logged reviewer session -> appends "accepts ... or, in persisted-final-reviewer mode, a round whose session log records final" -> widened admission. BLESS: NO. The cell now states the gate's admission set twice, and the two statements disagree: "restricted to a FULL-LANE round from a fresh logged reviewer session" remains unqualified earlier in the same cell. A builder or test author can implement either one.
- [MEANING] LLR-207 Detail -> gating_span accepts only a full scope from a freshly minted session -> appends: format_scope renders final for a full round under the final stage; gating_span admits final in persisted mode -> new scope kind and admission. BLESS: NO. It has the same self-contradiction as LLR-140: "gating_span accepts only a full scope from a freshly minted session" is left standing beside the new sentence that admits `final`. The old sentence must be replaced, not appended to.
- [MEANING] LLR-269 Detail -> the identity row accounts usage, timing and occupancy -> also session-mode (fresh/resumed) and keep-scope columns, audit-only -> two new recorded columns. BLESS: yes. This matches agent_common.py's header and session_service.py.
- [MEANING] SR-227 Title+Requirement+AcceptanceCriteria+Rationale -> retention covers adjudications only -> reviewer retention with iteration/final stages, keyed records, no warming, a fresh-or-persisted final reviewer, gate admission rules and audit logging -> a whole new capability class. BLESS: NO, for four findings. (1) BURIED CONDITION AND WRONG SCOPE: the reviewer obligations sit inside "Where the declared ADJUDICATOR retention dial is above zero, the delivered ADJUDICATION content shall ...", so read literally they apply only when the adjudicator dial is on, and they bind adjudication content rather than the loop's reviewer. The reviewer clause's own lower-case "where the declared reviewer retention dial" is the buried-condition trap (§2 b2). The reviewer obligation needs its own fronted `Where` (or its own row, §2(a)). (2) A CONTRADICTION WITH ITS SIBLINGS AND WITH ITSELF: the AC says each review session log records "its reviewed range as audit data that no gate or scheduler reads". The log's reviewed range is the `# review-scope:` / `# commits:` record, and the gate does read it (LLR-207 gating_span, LLR-262 review_logs/scope_offenders). The same AC also says admission depends on "a full-lane round the coordinator records as final", which is that same record. Only session-mode and keep-scope are audit-only. (3) ".;" punctuation splice at "another home.; and," and no terminal full stop. (4) The final-reviewer evidence reading this AC encodes is lane decision D-001, which is high_risk and pending the owner. The resolution should say so in the Rationale, so an overrule is traceable to the rows it moves.
- [MEANING] LLR-270 Title+Detail+Rationale -> keep operation retains adjudicator sessions -> also REVIEW: reviewer_dials as one reader, review_retention stages, scoped_route pins, scoped-record rules, _read_record admitting only writer variants -> new mechanism. BLESS: yes. The symbols exist. TC-266 and TC-351 carry the arms (subject to the TC-266 finding below).
- [MEANING] LLR-305 Detail -> the request carries no scope; governing_templates gives the retained-class identity -> the request carries scope; for REVIEW, governing_templates returns the once-resolved reviewer text -> new field and branch. BLESS: yes.
- [MEANING] TC-266 Expected+Method -> verifies the template is inert, this repo's enabled dial has the same shape, and at dial 0 the runner version is not read, argv and env equal a fresh session's, no store is written, the loop's plan is None and the dispatcher builds no keep-warm -> verifies reviewer and adjudicator dials are shipped off, malformed config reads off/fresh, dial 0 plans nothing, and persisted reads fresh at percent 0 -> the verified clause set changed. BLESS: NO. The amendment DROPS verification of attested LLR-270 / SR-227 clauses without saying where they moved: "plan_keep returns None before reading the runner version", "the launch equals a fresh session's" (no resume flag, ambient environment) and "keep_warmer builds no warmer". Those are SR-227's dial-zero "no resume argument ... no keep-warm call made". No other TC Method names them: TC-268 states keepwarm_due, not the warmer build, and TC-329 states only the store. The tests still exist (test_at_dial_zero_an_adjudication_launches_exactly_as_a_fresh_session, test_the_dispatcher_keeps_nothing_warm_at_dial_zero, test_the_shipped_dial_is_off_and_this_repo_shares_its_structure), so this is a cell regression, not a code one: the reviewer clauses should be added beside the adjudicator ones, not in place of them.
- [MEANING] TC-322 Method -> runs the five retained-class identity cases -> also runs the reviewer-identity case and asserts the request carries scope and a review identity is its own once-resolved template -> new verified clause. BLESS: yes, with a note: its unamended Expected still describes only the retained-class identity and under-claims the review identity and scope the Method now checks. That is an under-claim, not a false one, but it is worth aligning when TC-205/TC-266 are reworked.

VERDICT: MEANING rows=13

The act: none can be taken in this sitting. The rows I would bless (SR-154, SR-156, LLR-045, LLR-262, LLR-269, LLR-270, LLR-305, TC-322) each share a registry with a row I return: SR-227 in system-requirements, LLR-140 and LLR-207 in low-level-requirements, TC-205 and TC-266 in test-cases. The snapshot refuses a copy while any drifted approved row in it is not named, and naming a returned row would bless text I ruled unfit. So every drifted row here stays unanchored until the returned rows are reworked and re-sat. The re-sitting can re-attest the eight blessable rows together with the reworked five.

## Dispositions answered in the lane (sitting 006 approved and anchored the reworked rows)

```toml
title = "WI-887 spine rework: answer checkpoint 004's amendment returns (SR-227, LLR-140, LLR-207, TC-205, TC-266)"
workstream = "process"
sr_refs = ["SR-227", "SR-156", "SR-154"]
needs = ["WI-887"]
safety_class = "ordinary"
buildtier = "strong"
```

Spine text only; no code change is called for. SR-227: give the reviewer obligation its own fronted `Where the declared reviewer retention dial is above zero` (or split it into its own SR) so it neither depends on the adjudicator dial nor binds "adjudication content"; restrict the AC's audit-only claim to the session-mode and keep-scope columns, stating that the `# review-scope:` record is the coordinator's gating record; repair the ".;" splice; cite lane decision D-001 (pending the owner) in the Rationale. LLR-140 and LLR-207: replace, not append to, the sentences that restrict the gate / gating_span to fresh full scopes, so each cell states one admission set. TC-205: qualify Expected's "retained-session rounds ... hold" to "retained full and narrow rounds hold" to match its Method. TC-266: keep the dial-zero adjudicator assertions (runner version not read, argv and environment equal a fresh session's, no keep-warm built, this repository's dial shares the template's structure) beside the new reviewer assertions; align TC-322's Expected with its Method while there. Then re-sit these five together with SR-154, SR-156, LLR-045, LLR-262, LLR-269, LLR-270, LLR-305 and TC-322, which this sitting would bless as they stand.

## first-approval

- [RETURN] TC-351 -> verify that reviewer retention resumes only within one lane, claim, phase and stage; that invalid or other-keyed state mints fresh; that iteration and final reviewers stay separate; that reviewer records are never warmed; and that the audit fields grant no gate authority -> the chain: SR-227 (returned in this sitting's amendment section, finding 2 being the very audit/gate clause this TC claims), LLR-269 and LLR-270; 21 cited tests, all present in tests/test_session_keep.py -> not ready. Its Expected claims "audit fields grant no gate authority", but none of its 21 cited tests asserts it. The two audit tests (test_two_iteration_rounds_resume_one_review_session, test_an_unretained_call_logs_a_fresh_unscoped_session) show that the columns are WRITTEN, not that the gate ignores them. The claim is also built on SR-227's AC wording, which is returned. Either cite a test that shows the gate's answer unchanged when only session-mode/keep-scope differ, or narrow the Expected to what the tests show. It cannot be anchored in any case while TC-205 and TC-266 hold test-cases.toml.

OUTCOME: RETURN rows=1

## Dispositions answered in the lane (sitting 006 approved and anchored the reworked rows)

```toml
title = "WI-887 TC-351: bind its audit-only claim to a test, then re-sit for first approval"
workstream = "process"
sr_refs = ["SR-227"]
needs = ["WI-887"]
safety_class = "ordinary"
buildtier = "strong"
```

Add a case to TC-351's Evidence asserting that a REVIEW log differing only in `session-mode`/`keep-scope` gets the same gate answer from `kverdict.gating_span`/`review_logs` (or drop "audit fields grant no gate authority" from Expected), keeping the Expected consistent with SR-227's reworked AC. Re-sit with the amendment rework above, so test-cases.toml is anchored in one act.

SITTING: JUDGED kinds=amendment;first-approval
