# WI-887 checkpoint sitting 006 — amendment; first-approval

Re-sits 005 (docs/reviews/wi-887/005-ADJUDICATE-adc244d.md) at 4c9a4271b.
Judged top-down: SR-239 first, then the rows that hang from it. Each of 005's
findings is answered:

- SR-239's fail-closed clause is now an `If ... then` outside the dial's `Where`, and its AC carries the malformed case.
- Gate admission is left to SR-156, which the AC now cites.
- The audit columns now appear in the Requirement as well as the AC.
- The SN-025 feed-back is present, the decision-id frame is gone, and `Form` is declared.
- LLR-305 names SR-239.
- TC-322 states its ADJUDICATE clauses outright.

`trace.py --strict` raises no advisory on these rows, and `--strict-integrity` passes.

## amendment

All ten amended rows changed MEANING (as ruled in 004/005), and I would bless every one of them.

- [MEANING] LLR-045 Detail -> fill the reviewer brief from the override or shipped template -> also resolve the template once per round, shared by brief and retention identity, and pass the draw-settled stage to format_scope only for a full brief -> new mechanism. BLESS: yes.
- [MEANING] LLR-262 Detail -> review_logs yields each log's gating span -> also resolves the final-reviewer mode once per call through reviewer_dials and passes it to every gating_span -> new gate input. BLESS: yes.
- [MEANING] TC-205 Expected+Method -> only a fresh full claim-base scope gates; retained rounds hold -> a final scope in persisted mode can also gate; retained full and narrow rounds hold -> the verified admission set widened, consistently. BLESS: yes.
- [MEANING] LLR-140 Detail -> the gate admits only a fresh full-lane round -> a fresh full-lane round in either mode, or a final round only with retention on and persistence; narrow and retained full rounds never admit -> widened admission, stated once. BLESS: yes.
- [MEANING] LLR-207 Detail -> gating_span accepts only a fresh full scope -> format_scope renders full, narrow or final; gating_span admits a fresh full scope, or a final scope only with retention on and persistence -> a new kind and admission, stated once. BLESS: yes.
- [MEANING] LLR-269 Detail -> the identity row accounts usage, timing and occupancy -> also session-mode and keep-scope as audit-only columns -> two new columns, now called for by SR-239's Requirement. BLESS: yes; its chain parent SR-239 is approved in this sitting.
- [MEANING] LLR-270 Title+Detail+Rationale -> retains adjudicator sessions -> also the REVIEW keep (reviewer_dials, review_retention stages, scoped_route pins, scoped-record rules, the writer-variant _read_record) -> new mechanism decomposing SR-239. BLESS: yes; parent approved in this sitting.
- [MEANING] LLR-305 Detail -> the request carries no scope, and governing_templates gives the retained-class identity -> the request carries scope, and REVIEW returns the once-resolved reviewer text -> new field and branch. Its SR-Refs now names SR-239, so it no longer has a clause without a parent (005's finding answered). BLESS: yes.
- [MEANING] TC-266 Expected+Method -> verifies the adjudicator dial is inert at 0 -> the same assertions, plus the reviewer dial shipped off, malformed reviewer settings read off and fresh, and persisted reads fresh at percent 0 -> verified clauses added. BLESS: yes.
- [MEANING] TC-322 Expected+Method -> one template identity across retained classes; edit and override drain -> the request also carries scope; a REVIEW identity is its once-resolved text; an ADJUDICATE identity keeps the retained-class identity (switching drains nothing, and a class without a template adds nothing) -> verified clause added, the ADJUDICATE clauses now stated outright (005's note answered). BLESS: yes. Its edit-and-override drain is held by TC-267.

VERDICT: MEANING rows=10

The act: `intake.py snapshot --reattests LLR-045,LLR-262,LLR-140,LLR-207,LLR-269,LLR-270,LLR-305,TC-205,TC-266,TC-322 --verdict` this file. It runs before the first-approval act because that act's test-cases copy is refused while TC-205, TC-266 and TC-322 are still drifted. The judgement order above is still parent first.

## first-approval

- [APPROVE] SR-239 -> covers the case where the reviewer retention dial is above zero. The loop's review content then resumes a reviewer only across iteration rounds of one lane, claim and phase, under the iteration stage. It reads absent, malformed, misfiled or other-keyed records as no session, never warms a reviewer, and retires the iteration session at the full-lane draw. That round runs fresh, or, under persistence, on one per-lane-and-phase final reviewer that never resumes an iteration session. A template change drains the reviewer, and session-mode and keep-scope are recorded as audit-only columns. If the setting is malformed, or names a persisted final reviewer while retention is off, it reads as off and fresh -> the chain: SN-025 is its labelled derived parent, argued through three named lenses with feed-back. Gate admission lives once, in SR-156, which is cited, not restated. LLR-270 (REVIEW), LLR-269 (audit columns), LLR-045 (template read) and LLR-305 (identity) decompose it. TC-266 holds the off and malformed arms, TC-351 the keyed resume, retire, final and never-warm arms, and TC-322 the identity -> ready. Every Requirement clause has a reachable condition and an AC observation, and no AC clause lacks a Requirement clause.
- [APPROVE] TC-351 -> verify that only its lane, claim, phase and stage resume; that invalid or other-keyed state mints fresh; that iteration and final reviewers stay separate; that reviewer records are never warmed; and that session-mode and keep-scope are recorded -> its 21 named tests are all present in tests/test_session_keep.py. Its Verifies names its LLRs and their SRs, per the in-lane closure rule. Its parent SR-239 is approved above -> ready. 004's over-claim is gone and 005's return was chain-only.

OUTCOME: APPROVE rows=2

The act: flip SR-239 and TC-351 to Approved, and run `intake.py snapshot --approves "docs/requirements/system-requirements.toml=WI-887;docs/test/test-cases.toml=WI-887"` in the same commit.

SITTING: JUDGED kinds=amendment;first-approval
