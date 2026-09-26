# Arbitration — the assumption tier's second build wave (2026-09-26)

Disputes between the integrator and codex Sol's chain reviews (the `sol-*.md`
files beside this one), ruled by a Fable arbiter, read-only. Each ruling names
the governing text, the fix and the commit it belongs in. The integrator
applied every ruling except where noted.

1. **TC-229's tier (WI-632) — INTEGRATOR.** D31 as the builder brief
   operationalises it ("no scaffold, no subprocess, no git") and SLOW_MODULES
   (subprocess/scaffold-heavy); TC-229's approved method says "exercised in a
   temporary directory" at Smoke, written beside TC-230's "on a scaffold …
   registered as slow", Full; D31's own list of slow modules names
   `test_observation_writer`, not `test_observation_record`. Temp-directory
   I/O is what many Smoke modules do. No fix, no amendment. TC-222 differs in
   kind (it initialises and commits a git repository): Full, a slow module and
   a drafted TC amendment, in WI-629's commit, as both sides agreed.

2. **WI-631's red-TC census (LLR-231) — INTEGRATOR.** LLR-231 asks only that
   `census.red_tc_census` counts assumption evidence apart; TC-227 and SR-197
   agree. Whether the dispatch seam should mint rows from the assumption half,
   and of what kind, no row states. The decisive reason to defer: the red-TC
   rung is structurally dead in any conformant repo (`_TC_NOT_RED` spans the
   whole closed Status vocabulary; an owner judgement item on re-arming it is
   pending). Fix: one docstring line in `gap_census` saying the assumption
   half is not on the dispatch seam, plus a routing follow-up item once the
   rung is ruled on. No amendment.

3. **WI-630's composition point (LLR-214 vs IF-190) — INTEGRATOR on
   placement, SOL on the test.** Approved LLR-214 says the gap advisory "is
   composed by trace.analyze into the warn pipe"; IF-190 is Drafted, and an
   approved detail outranks a Drafted row's rationale sentence. Fix in WI-630:
   reword IF-190's rationale (the entry point owns the classified findings;
   the two reach reports ride the seam as checker-composed advisories) and add
   a test driving `trace.analyze` that fails if either advisory leaves the
   warn pipe. No amendment.

4. **WI-636's merge-slot rule (SR-208, SR-209, LLR-248) — a third option;
   trailer validity — INTEGRATOR.** The slot sees commits, not processes, so
   an ownership rule is needed and an amendment is unavoidable. Keep lane
   ownership, amended: (i) a lane is the loop's if its claim OR any
   loop-writer commit in its range carries the trailer; (ii) both rungs are
   armed whoever runs the slot (drop `_loop_trailer_refusal`'s
   `loop_session() is None` gate; hooks are opt-in, D30); (iii) every commit
   of a loop lane is judged, and a person's commit there carries the trailer
   or moves to their own lane; (iv) commits before the lane's first marked
   loop-writer commit are exempt from the trailer rung only. Code and the two
   exemption tests in WI-636; drafted amendments to SR-209's acceptance,
   LLR-246 and LLR-248 (SR-208 unchanged). Validity: SR-209 defines "valid"
   as present and well-formed, and no session set exists to check against;
   hardening is a follow-up, not owed.

5. **WI-640's association timing (SR-217) — INTEGRATOR on the build, SOL on
   the gap.** SR-217 defines a test case's approval per test case; no row
   says when a test case becomes a requirement's, and the build takes tip
   membership and discloses it. SN-042's acceptance already says "defined and
   approved", so association is the need's intent, and the fix belongs in
   SR-217 (a requirement's test case is approved at the earliest commit where
   it reads approved AND names the requirement or one of its design rows),
   not in SN-042's owner-reserved text. `first_approval_commits` already
   parses rows on both sides of every registry commit, so it is one condition
   in the same walk. No semantic code change until adjudicated.
   **Integrator's deviation:** the arbiter suggested drafting the SR-217 /
   LLR-257 / TC-250 amendment into the registry now; because SR-217 carries
   SN-042's test-first rule, which the owner reserved (D6/D20), the proposed
   wording is recorded for the owner in the handoff instead.

6. **WI-631's empty acceptance rule (LLR-233, TC-228) — INTEGRATOR
   (empty-as-absent), keeping Sol's whitespace strengthening.** The carrier
   rule: an absent key IS an empty cell (`kitlib/spine.py`); an explicit `""`
   is refused at live load (`spine_carrier` `empty_value_findings`);
   migration drops empty and whitespace-only cells. LLR-233 and TC-228 were
   written under that rule, so "empty" means absent. Judging key presence
   would admit a third state and, on the still-read CSV carrier, fail every
   model-less observation row and make the optional sampling model mandatory.
   Fix: restore value-based `_present`, keep the census docstring half; tests
   for `""` with a size (size-without-rule failure), whitespace with and
   without a size ("AcceptanceRule is empty"), and `""` alone (valid, not
   model-declared). No amendment.

**Missed by both (arbiter):** the red-TC census rung fires nowhere today; and
WI-636's two slot rungs were armed inconsistently (held-status for anyone,
trailer only under the loop marker), which located the defect in the trailer
gate rather than the ownership model.
