# WI-887 checkpoint sitting 005 — amendment; first-approval

Re-sits 004 (docs/reviews/wi-887/004-ADJUDICATE-6e7e50f.md) at adc244dff.
004's findings on LLR-140, LLR-207, TC-205 and TC-266 are answered: each cell
now states one admission set, and TC-266's dial-zero assertions are restored.
TC-351's Expected now claims only what its tests show. SR-227 is no longer
amended. The reviewer obligation moved to the new SR-239, which this sitting
judges first, as parent before children.

## amendment

All twelve amended rows changed MEANING, as in 004. Each row's line says
whether I would bless the new text. Three outcomes appear: blessed now,
blessed but held by a registry neighbour, and withheld (for its own text or
for its chain).

- [MEANING] SR-154 AcceptanceCriteria -> only a session minted for the review, over the whole lane, may clear integration -> also the coordinator-recorded final round of the lane's retained final reviewer, under retention on and persistence; iteration rounds never clear, fresh or resumed -> a new admitting actor. BLESS: yes; RE-ANCHORED in this sitting's act.
- [MEANING] SR-156 AcceptanceCriteria -> landing clears only from FRESH sessions; a retained-session review holds -> sessions started fresh, or the coordinator-recorded final round under persistence; iteration rounds and any other retained-session review hold -> a new admitting actor. BLESS: yes; RE-ANCHORED in this sitting's act.
- [MEANING] LLR-045 Detail -> fill the reviewer brief from the override or shipped template -> also resolve the template once per round, shared by brief and retention identity; pass the draw-settled stage to format_scope only for a full brief -> new mechanism. BLESS: yes, but held: its registry also holds the rows withheld below, so it cannot be anchored now.
- [MEANING] LLR-140 Detail -> the gate admits only a fresh full-lane round -> a fresh full-lane round in either mode, or a final round only with retention on and persistence; narrow and retained full rounds never admit -> widened admission, now stated once (004's finding answered). BLESS: yes, held by its registry.
- [MEANING] LLR-207 Detail -> gating_span accepts only a fresh full scope -> format_scope renders full, narrow or final; gating_span admits fresh full in either mode, or final only with retention on and persistence; narrow and retained full never admit -> new kind and admission, stated once (004's finding answered). BLESS: yes, held by its registry.
- [MEANING] LLR-262 Detail -> review_logs yields each log's gating span -> also resolves the final-reviewer mode once per call via reviewer_dials and passes it to every gating_span -> new input to the gate reader. BLESS: yes, held by its registry.
- [MEANING] LLR-269 Detail -> the identity row accounts usage, timing and occupancy -> also session-mode and keep-scope as audit-only columns -> two new recorded columns. Its own text is sound. WITHHELD FOR ITS CHAIN ONLY: the reviewer half now traces to SR-239, which is returned in the first-approval section, and a returned parent withholds its children (spine-authoring in-lane, "approve parents first").
- [MEANING] LLR-270 Title+Detail+Rationale -> retains adjudicator sessions -> also the REVIEW keep: reviewer_dials, review_retention stages, scoped_route, scoped-record rules, the _read_record writer-variant reader -> new mechanism. Its own text is sound. WITHHELD FOR ITS CHAIN ONLY (SR-239).
- [MEANING] LLR-305 Detail -> the request carries no scope, and governing_templates gives the retained-class identity -> the request carries scope, and governing_templates returns the once-resolved reviewer text for REVIEW -> new field and branch. WITHHELD, own defect: since the split, its only parent SR-227 is adjudication-only, so nothing upstream calls for the new REVIEW clause. Read upward, it is scope its parent does not make. Its SR-Refs must name SR-239, as TC-322, which verifies it, already does.
- [MEANING] TC-205 Expected+Method -> only fresh full claim-base scope gates; retained rounds hold -> a final scope in persisted mode can also gate; retained full and narrow rounds hold -> the verified admission set widened, now consistently (004's finding answered). BLESS: yes, held by its registry.
- [MEANING] TC-266 Expected+Method -> the adjudicator dial is inert at 0 (version unread, fresh argv/env, no store, no plan, no warmer) -> the same, plus the reviewer dial shipped off, malformed reviewer settings read off and fresh, and persisted reads fresh at percent 0 -> reviewer clauses added beside the restored adjudicator ones (004's finding answered). WITHHELD FOR ITS CHAIN ONLY: it verifies SR-239.
- [MEANING] TC-322 Expected+Method -> the request carries route, work item, env, template and lease inputs; one identity across retained classes; an edit or override drains -> the request also carries scope; a REVIEW identity is its once-resolved text; an ADJUDICATE identity is "unchanged" -> new verified clause. WITHHELD FOR ITS CHAIN ONLY (it verifies SR-239). A note for the rework: "an ADJUDICATE identity is unchanged" reads only against history. The clauses it replaced (switching classes drains nothing, a class without a template adds nothing) should be stated outright. The edit-and-override drain is still held by TC-267.

VERDICT: MEANING rows=12

The act: `intake.py snapshot --reattests SR-154,SR-156 --verdict` this file. Only system-requirements.toml is copied; SR-227 there is byte-equal to its anchor, and SR-239 stays Drafted. The low-level-requirements and test-cases registries stay unanchored. LLR-045, LLR-140, LLR-207, LLR-262 and TC-205 would be blessed as they stand, but they share a registry with LLR-269, LLR-270, LLR-305, TC-266 and TC-322. Re-sit them all together once SR-239 and LLR-305 are reworked.

## Dispositions answered in the lane (sitting 006 approved and anchored the reworked rows)

```toml
title = "WI-887 spine rework: answer checkpoint 005 (LLR-305's parent; re-sit the SR-239 chain)"
workstream = "process"
sr_refs = ["SR-239", "SR-227"]
needs = ["WI-887"]
safety_class = "ordinary"
buildtier = "strong"
```

Add SR-239 to LLR-305's SR-Refs, since its REVIEW identity and scope clause answers SR-239, not the adjudication-only SR-227. While there, state TC-322's ADJUDICATE clauses outright instead of "unchanged". Re-sit with SR-239's rework (first-approval Dispositions below), so that LLR-045, LLR-140, LLR-207, LLR-262, LLR-269, LLR-270, LLR-305, TC-205, TC-266, TC-322 and TC-351 are judged and anchored in one act.

## first-approval

- [RETURN] SR-239 -> where the reviewer retention dial is above zero, the loop's review content resumes a reviewer only within a lane/claim/phase/iteration-stage key, reads bad or other-keyed records as no session, never warms, retires the iteration session at the full-lane draw, runs that round fresh or on a persisted final reviewer that never resumes an iteration session, fails malformed settings closed, and drains on a template change -> the chain is sound below it: LLR-269, LLR-270 and LLR-045 implement it, TC-266, TC-322 and TC-351 verify it with named tests, and D-001 (pending the owner) is the provenance ruling it rests on -> not ready, for four findings in its own text. (1) A CONDITION THAT EXCLUDES ITS OWN CLAUSE: "read a malformed reviewer setting, or a persisted final reviewer while reviewer retention is off, as retention off and a fresh final reviewer" sits inside "Where the declared reviewer retention dial is above zero". Under that condition "retention is off" can never hold, and whether an ill-typed percent counts as "above zero" is undefined. The fail-closed obligation therefore has no reachable home. It belongs outside the `Where`, as an unconditional clause or as `If the reviewer setting is malformed, or names a persisted final reviewer while retention is off, then ...`. Its AC states the dial-at-zero case but not the malformed one. (2) THE AC OBSERVES OBLIGATIONS THE REQUIREMENT NEVER STATES: gate admission ("only a full-lane round it records as final ... admits", "a retained full round and every iteration round hold") and the audit columns appear in the AC but in no clause of the Requirement. Gate admission already has its home in SR-156 (and SR-154): restating it here gives the rule two homes (§2(a)). Either state the coordinator's final-kind record as this row's own obligation and leave admission to SR-156, or cite SR-156 instead of restating it. (3) A DERIVED ROW NOT FED BACK: the Rationale labels it derived and names its lenses, but omits §2(c)(iii)'s feed-back to SN-025, which SR-227 carries ("Fed back to the need: ..."). (4) SELF-CORRECTION: sitting 004 asked for D-001 to be cited in the Rationale, and trace.py now warns that a decision-id citation is a history frame (process.md §3). Keep the standing reason as prose (the coordinator-written records, not reviewer-authored text, establish final-review provenance) and leave the D-001 account to the log. Also advisory: trace.py notes that SR-239 declares no `Form`.
- [RETURN] TC-351 -> verify that reviewer retention resumes only within its lane, claim, phase and stage; that invalid or other-keyed state mints fresh; that iteration and final reviewers stay separate; that reviewer records are never warmed; and that session-mode and keep-scope are recorded -> 004's finding is answered: the Expected now claims only what its 21 named tests show, and its Verifies follows the in-lane rule that each TC names its LLRs and their SRs -> RETURNED FOR ITS CHAIN ONLY: its text is ready, but its first-named parent SR-239 is returned above, and a returned parent withholds its children's approval. Re-sit it unchanged with SR-239.

OUTCOME: RETURN rows=2

## Dispositions answered in the lane (sitting 006 approved and anchored the reworked rows)

```toml
title = "WI-887 SR-239: reachable fail-closed clause, one home for gate admission, need feed-back; re-sit with TC-351"
workstream = "process"
sr_refs = ["SR-239", "SR-156"]
needs = ["WI-887"]
safety_class = "ordinary"
buildtier = "strong"
```

Spine text only. Move SR-239's malformed/off-setting clause out of the reviewer-dial `Where`, either unconditionally or as an `If ... then` clause, and add the malformed case to its AC. Reconcile the AC with the Requirement: keep in the AC only what the Requirement obliges, and leave gate admission to SR-156 (cite it, or make the coordinator's final-kind record SR-239's own stated obligation). Add the SN-025 feed-back sentence. Replace the D-001 citation frame with standing-reason prose, and consider declaring `Form`. Then re-sit SR-239 and TC-351 for first approval, together with the withheld amendment rows named in the amendment section's Dispositions.

SITTING: JUDGED kinds=amendment;first-approval
