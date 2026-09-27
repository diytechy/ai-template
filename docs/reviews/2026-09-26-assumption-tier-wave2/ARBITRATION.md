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

## Coordinator's rulings (resumed session, 2026-09-26)

Ruled by the coordinator, per the handoff: the governing row text, then the
ruling.

7. **WI-640's follow-up (dc3f8c6b): pre-TOML approvals — BUILDER; the two
   minors — SOL** (`sol-wi640-fix.md`). Approved LLR-257 reports "history
   from before the TOML registries, as unreadable, never as a pass". The
   follow-up narrows that: an approval the TOML history cannot date exactly
   is bounded at or before the cutover commit, settles the order when the
   bound falls at or before the landing, and is otherwise reported unread.
   Sol's case (a TC approved under the CSV carrier, implemented later, the
   cutover last) now reports unread, which the approved row already
   required; it is a disclosed gap, never a false pass. Reading older-carrier
   approvals is a capability no approved row asks for: a possible follow-up,
   not owed. TC-250 is not amended: every clause of its method stays true,
   and the widening is carried by the LLR-257 amendment already in the joint
   adjudication. Owed, in a second follow-up: assert that an unread
   requirement makes `--strict` exit 1, and qualify the README, template and
   RESYNC wording that says every inexact approval is reported unread.

8. **WI-632's follow-up (f6538270): the typed act ledger — SOL, narrowed**
   (`sol-wi632-fix.md`). LLR-239 has the latest act move the anchor. The
   ledger replaced the prose stamp so that anchor rests on a typed carrier,
   and a typed carrier that admits duplicate `seq` values or wrong-typed cells
   silently brings back the defect it was built to remove. Owed, in a second
   follow-up: `parse_acts` fails closed on missing or wrong-typed fields, bad
   row-id syntax and a `seq` that is not unique and strictly increasing; the
   existing ledger is validated before any snapshot mutation; the digest
   coverage test derives its expected set from the implementation's sources.
   Not owed: cross-commit append-only detection, which is hardening of the
   same class as trailer validity (ruling 4). The ledger itself departs from
   the snapshot header's argument against a ledger (design §F8) because the
   review required a typed carrier; it is declared in the module, and the
   owner may rule on it.

9. **WI-636's follow-up (10523f27): the builder's three deviations —
   BUILDER; Sol's three findings — SOL** (`sol-wi636-fix.md`). (a) The
   history check still reads a legacy dial as most-held: approved LLR-249's
   detail prescribes exactly that ("an absent or legacy value reading as the
   most-held rung with no printed warning"), and an approved row outranks the
   review's cross-chain wish for one reader everywhere; the hook, writers and
   slot share `authority.dial_at`/`read_dial`, and the history path errs held
   and is advisory. Unifying it would need an LLR-249 amendment, not owed.
   (b) A merge move counts only when its staged value differs from both
   parents, so a loop refresh that brings in a person's approved status from
   trunk is not refused; the drafted LLR-246 amendment states it. (c)
   Loop-writer commits are recognised by subject pattern plus a well-formed
   trailer; a forged subject only makes a lane more governed. Owed, in a
   second follow-up: the live SN path through `rung_for` (the owed
   DevStg-Needs classification), the RESYNC advice that a person may merge
   a loop lane themselves removed, and the quarantine and mechanical-close
   subjects driven by real-writer tests.

10. **WI-647's follow-up (acbf0d77) — SOL** (`sol-wi647-fix.md`). IF-186
    says no uncommitted edit shapes the bookkeeping commit, and the
    follow-up already runs the scratch tree's committed trunk step for that
    reason; the regeneration's write scope (`_full_scope` over
    `trunk_step.regen_writes()`) still came from the loaded kit, so an
    uncommitted edit to the write table could drop a committed output from
    the commit. Owed: the write scope from the same committed kit whenever
    it runs. Sol did not contest the builder's choices (the HEAD-planned
    scope extended to the mint; a drift refusal after the branch cut leaves
    the branch for the next claim to re-cut; an uncommitted added link
    widens nothing; the TC-145 amendment's home), so they stand.
