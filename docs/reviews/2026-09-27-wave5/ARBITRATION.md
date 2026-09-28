# Arbitration — the fifth build wave (2026-09-27)

The session that resumes from
[the wave-4 handoff](../../handoff-2026-09-27-wave4-coordinator.md): spine-acts
batch B, then WI-679, then the remaining groups. Builders work in their own
worktrees; codex Sol reviews each commit read-only (the `sol-*.md` files beside
this one). The coordinator rules where a builder and Sol disagree, where it
disagrees with Sol, and where a queued item asks for a ruling that is not the
owner's, citing the governing text. Rulings a Fable arbiter makes are marked as
such.

1. **Batch B (8a960cf1), the blocker: TC-055 re-attested over a false
   `expected` — SOL.** WI-638 declared `max_age = 90` on TC-055 (wave-4
   ruling 2), so the re-judge checkpoint now re-fires the case on expiry, while
   its unamended `expected` still says the recorded verdict "is a one-time
   judgement that nothing re-fires". The adjudicator saw it and called the
   sentence "the weaker of two true statements". It is not true: the row now
   says both that nothing re-fires it and when it is re-fired. The governing
   text is PROCESS.md §7: an approval blesses the row's TEXT, and the
   amendment brief lets a MEANING row be re-anchored only when its new text is
   one the adjudicator would bless. Approved SR-054's rationale makes the same
   claim ("a recorded one-time judgement rather than a standing
   re-judgement"). **Ruling:** the act is reverted in the lane. The
   coordinator amends TC-055's `expected` and SR-054's `rationale` in place,
   status left Approved, to say the verdict is re-judged when a declared input
   changes or the record expires, never on every commit. SR-054 joins WI-680's
   scope, and the same adjudicator judges both amended cells. Then ONE act is
   re-taken. The adjudicator authored neither amendment, so it stays
   independent of what it judges.

2. **Batch B, major: LLR-205's disposition is too narrow — SOL.** Deleting
   the closing status sentence leaves the rationale calling itself "a live,
   dated finding" with a dated plan citation, and the `detail` narrating the
   state before the table. Both break the spine-authoring skill's
   cell-hygiene rule (a living cell states the system and its standing
   reason, never its history). The rows are returned either way, so no act
   changes. The fold into WI-616 states the whole fix.

3. **Batch B, major: TC-201 and TC-203 approved with changelog prose — SOL.**
   TC-201's method narrates what "now" catches against what "was", and a
   pattern record "BEFORE this table existed"; TC-203's opens "Re-tiered
   into". The adjudicator noted TC-203's and passed it on SR-176's approved
   precedent. An existing approved row with the same defect is a reason to
   fix that row too, not to approve a new one. Both cases verify design rows
   this act returns (LLR-205, LLR-206) for the same class of defect.
   **Ruling:** TC-201 and TC-203 are returned with their design rows and
   rewritten in the same WI-616 part. The act approves 25 rows, not 27.

4. **Batch B, second sitting: the coordinator's TC-055 amendment was itself
   wrong — ADJUDICATOR.** Ruling 1's amended `expected` said the verdict is
   re-judged "only when a declared input changes or the record passes its
   declared max_age". The adjudicator withheld the blessing: the code's first
   trigger (`rejudge.due_cases`, a case with no result on record) is missing,
   and it is TC-055's state at HEAD. It drove `due_cases` to show it, and the
   snapshot refused on TC-055 as it should. The error was the coordinator's.
   **Ruling:** the cell takes the adjudicator's drafted wording, which names all
   three triggers, as a second in-place amendment. The adjudicator re-judges
   it before the one act. The revert of the first act left the snapshot copies
   unequal to the live files at the commit that wrote them (the mirror
   invariant, red under `--strict-integrity`); the re-taken act clears it. Any
   later revert of an act needs the same care.

   The adjudicator also found that the five observation cases the checkpoint
   reports due (TC-036, TC-055, TC-209, TC-210, TC-211, none recorded) have no
   re-judge rows, although three lanes merged after WI-638 declared their
   inputs. The coordinator's hand squash-merges do not run the kit's merge
   checkpoint, so the rows were never minted. That is the hand path bypassing
   the kit's machinery, WI-679's surface, and it is folded there.

5. **WI-679 (f646eff0), the blocker: `sweep --merged` skips the Done-when
   arm silently — SOL, bounded.** The builder's report says the Done-when
   check "stays skipped for hand lanes", because a hand-cut lane has no
   `active/<branch>/` claim on trunk. That is true, but the new design row
   LLR-265 promises the check. `_done_when_drafts` then continues silently
   when it cannot find the claim, and a silent skip reads as a check that ran
   and found nothing. The governing text is the kit's own all-or-nothing rule
   for evidence (`adjudicate_brief`'s rule 2, and LLR-265 as written).
   **Ruling:** `--merged` requires a real range (`--before` differs from
   `--after`). The coordinator's degenerate `--before HEAD --after HEAD` form
   is withdrawn: batching spine acts by hand is not a kit path to serve. The
   Done-when arm runs when `--branch` names a claim it can find. When it
   cannot, it prints one line naming the row and why the arm did not run, and
   LLR-265 says so. It is never silent. The regression drives a changed
   Done-when end to end.

6. **WI-679, major: guard 3 keyed on a judgement's scope, not its outcome —
   SOL.** `judged_absorbed` counts any `consolidate` row's `Adjudicates`,
   whatever the verdict. A judgement that chose `queue` or returned, or one
   cancelled, would make a later hand host read as machine-judged. The same
   defect the builder removed (a mark that claims a judgement nobody made)
   would come back in another form. **Ruling:** a successor is read from a
   judgement that ENACTED a consolidation: its recorded `## Consolidation`
   outcome is `consolidate`, and the absorbed set is the one its drafts name
   (`parse_verdict`, `absorbed_ids`). `{prior}` labels provenance row by row,
   so a mixed hand-and-judged absorption is not all called "by hand". Tests
   cover a `queue` verdict, a returned or cancelled one, and mixed
   absorption.

7. **WI-679, major: the no-race argument is not enforced — SOL.** The
   rewritten guard 1 lets a queued judgement that names no candidate stand,
   because it "cannot run before" a priority-9 consolidation. The scheduler
   does not guarantee that: an operator priority can rank a judgement at or
   above it. Drift would refuse the stale close in the end, but a guard whose
   stated argument is false is the larger defect. **Ruling:** enforce the
   invariant in the guard, not in the scheduler. The census refuses, by name,
   while a queued judgement would sort at or before the consolidation under
   the scheduler's own ordering (reuse it, don't restate it). A regression
   covers equal and higher priority.

8. **WI-679, major: TC-260 and TC-261 do not cover their design rows clause
   by clause — SOL.** Each clause LLR-264 and LLR-265 state gets a test that
   fails if it breaks: the printed digests pair and the refusal's stderr and
   exit 1 (LLR-264); the spot check, the merged adjudication's Dispositions
   draft, the first-approval trigger, the Done-when arm (both branches, per
   ruling 5) and the duplicate-folder refusal (LLR-265). A clause no test can
   reach leaves the row.

9. **WI-679, second round (1b783955) — SOL on both.** Rulings 5 to 8 are
   confirmed implemented. The builder's side fix to `prior_absorbs`, which
   now reads lineage from the successors' `Supersedes`, drops every successor
   that was itself later restructured. The same round made a hand host
   absorbable (ruling 6), so a nested chain is now a live case, and LLR-210's
   and TC-208's "every earlier absorption" would be false of it. **Ruling:**
   an absorption event stays in `{prior}` after its successor is re-absorbed.
   A nested hand chain regression asserts both events and their per-row
   provenance. `sweep --help` describes `--branch` as the merged lane whose
   pre-merge claim is checked.

10. **WI-689 under the owner's pause — COORDINATOR, the owner may
    overturn.** WI-679's end-to-end bullet asks that the kit's census,
    judgement and close run on the live queue. `integrate.py claim` refused
    WI-689: `docs/work/pause` has held the frontier since 2026-09-04, by owner
    direction, and unpausing is "a reviewed deletion commit". That is the
    owner's act, not the coordinator's. **Ruling:** every step the pause
    allows ran through the kit, and nothing was replaced by judgement:
    - the sweep and the census minted the rows (`intake.py sweep --merged`,
      `intake.py consolidate`);
    - an independent Fable adjudicator judged WI-689 from
      `adjudicate_brief.compose`'s consolidate brief, and Codex Sol found the
      verdict SOUND;
    - the close ran `handback._consolidation_close`, the kit's own arm with
      `close_refusal` over the trunk registry, on the hand lane. It was called
      in the same sequence `_archive_one_adjudication_row` uses, pointed at
      `queued/` because nothing was claimed into `active/`.
    Only the claim and the merge slot were replaced by a hand lane and a
    squash-merge plus `sweep --merged`. The pause is left in place, and
    whether it still stands is put to the owner.

11. **WI-616 (3241f337), the blocker: approved LLR-203 made false — SOL.**
    The new LLR-275 and LLR-276 own the SR-163 resolver, classes and policy
    table that LLR-203's detail and rationale say no design row names. The
    builder reported it and stopped, as the brief says. **Ruling:** the
    coordinator grants amendment authority over LLR-203's `detail` and
    `rationale`, in place, status left Approved. The amendment is minimal:
    those mechanisms are now owned by LLR-275 and LLR-276. The merge's sweep
    mints its adjudication.

12. **WI-616, major: LLR-274's tokenization text is not the code's — SOL.**
    Commas are segment boundaries inside a clause, not clause delimiters, and
    TC-273 relies on that. Drafted LLR-274 is re-authored to state clause
    versus segment exactly.

13. **WI-616, major: the SR-184 fix exempts every Inspection row — SOL.** The
    false positive is a row whose SUBJECT is a Critique record. A blanket
    Inspection exemption would also hide a real two-methods row, an
    Inspection row that directs an independent verdict. **Ruling:** the
    suppression is subject-aware, and TC-275 gains the counterexample that
    must still warn.

14. **WI-616, major: three sweep classifications and SN-003's rewrite — SOL.**
    SR-137 ("no dotted keys"), SR-144 ("merges like any other branch") and
    SR-177 ("no threshold") state enforced obligations, not case
    descriptions. They are reclassified as closed normative obligations, and
    the totals are recomputed. SN-003's "a language other than Python" is
    still an open world. **Ruling:** it is bounded to what the kit actually
    offers (a stack the adopter declares a profile for), in the builder's
    words. It is a need, so it goes to the owner's brief, not to an
    adjudicator.

15. **WI-616, major: TC-276 is vacuous about registry ids — SOL.** It passes
    on generic path validation. **Ruling:** the test shows that an id
    selects the registry's support path, and that changing only the named row
    changes its digest, and Drafted TC-276 says so.

16. **WI-616, minor: warn-only is unpinned — SOL.** `absolute_advis` joins
    the never-gates exit-code regression, and a positive advisory is driven
    through `trace.analyze`.

17. **WI-651 (ba72cad8): the need-tier refusal, stopped on approved rows —
    GRANT.** The builder compared the need and stakeholder tiers and showed
    them in the brief, but it stopped before the refresh's refusal and
    `--reattests SN-###` (Done-when bullet 2). Approved LLR-245 and TC-240
    say the needs file "is outside SNAPSHOT_TIERS and stays outside" and
    that a drifted need is not covered. The governing text is the owner's
    OI-91 ruling (a), "fund the detector", which this row realises. Those
    rows state the pre-ruling design, and approved SR-207 already asks that
    "every tier [be] compared with its recorded copy". **Ruling:** the
    coordinator grants amendment authority, in place, status left Approved,
    over LLR-245 and TC-240, over SR-178's requirement where it says needs
    carry "no status cell", and over LLR-173 and its case so that
    `unanchored_findings` covers the need tiers. The merge's sweep mints
    their adjudication. It is the same detector, so it is finished in this
    lane.

18. **WI-616, second round (fd2d5de0): the subject test is token
    co-occurrence — SOL, bounded.** Rulings 11, 12 and 14 to 16 are
    confirmed. The exemption fires on any Inspection requirement containing
    both "Critique" and "record", so "the view links to a Critique record"
    is exempted while its acceptance directs a verdict. A full parse is
    disproportionate for a warn-only advisory. The requirement cell already
    has a subject slot, the text before its `shall` (the EARS form the
    spine-authoring skill prescribes). **Ruling:** exempt only when that
    subject names a Critique record. TC-275 gains the passing-mention
    counterexample, both words present outside the subject, which must warn.

19. **WI-651 (ba72cad8), major: legacy Markdown needs are never compared —
    SOL.** The kit still supports a `stakeholder-needs.md` carrier (WI-671's
    own subject), and the drift comparison loads needs through a reader that
    knows only TOML and CSV, so a Markdown adopter's drifted need reads as no
    drift. One carrier-aware need-tier loader serves both sides, and a
    Markdown scaffold regression covers it.

20. **WI-651, major: LLR-271 and LLR-273 each hold two decisions — SOL.** The
    builder flagged this deviation itself (three ids for five concerns). The
    spine-authoring skill's "one decision per row" governs. **Ruling:** the
    coordinator grants LLR-277, LLR-278 and TC-278. Both rows are split,
    TC-269 and TC-272 re-pointed, and TC-271's stamp and scope clauses split
    into two cases.

21. **WI-651, major: coverage gaps — SOL.** STK drift; Status on all four
    tiers and Phase on SR, LLR and TC (parametrized); and a mixed
    amendment-plus-first-approval act equivalent to batch B's seq 4, so that
    the legitimate case stays legitimate.

22. **WI-651, minor: IF citations and a back-link — SOL.** TC-271 cites
    IF-091 and IF-126, TC-272 cites IF-112, IF-126's note no longer says no
    case cites it, and `load_all` carries `Implements: SR-178, LLR-271`.

23. **Two trivial wording minors, applied by the coordinator at
    integration.** WI-616's test module introduction
    (`tests/test_verification_coherence.py`) still describes the exemption
    broadly, while its tests are correctly bounded (Sol at 3f9bd487: SOUND,
    one minor). WI-657's write-up opening still says the prototype "produced
    every number here", while its narrowed scope sits four lines below (Sol
    at 5c8706da: one minor). Each is a phrase and neither touches behaviour,
    so the coordinator corrects both in the landing commit instead of spending
    a builder round and a review on a sentence.

24. **WI-651, the tail of ruling 17 — GRANT extended.** Ruling 17 granted
    SR-178's requirement cell only. Its rationale and acceptance criteria
    still say needs carry "no Status cell", and LLR-173's detail still says
    "seven registries" and "advisory today". Both are false once the need
    tiers are compared. **Ruling:** the grant extends to those cells, in
    place, status left Approved. The two stale `docs/if-tc-coverage-allow`
    entries (IF-112, IF-126, now cited) are pruned together with the seed pin
    in `tests/test_trajectory_arch.py` that holds them, in one commit.

25. **WI-651, confirmation round (b2ce12f2) — BUILDER on the empty-write
    arm, SOL on the two cells.** Sol reads `refresh_refusal`'s whole-ledger
    arm for an act that copies nothing as exceeding SR-207, now that it also
    sees the need tiers. That arm pre-dates this lane (0ded5c77). Its
    docstring calls it deliberately unscoped: a no-op exiting 0 over a
    rewritten approved row "is the laundering scenario answered with
    silence". It implements approved LLR-245. WI-651 widened the tiers it
    walks, which OI-91's ruling asks for; it did not add the arm. Changing a
    deliberate, approved design is not this lane's scope, so the arm stands.
    If no-op refreshes should pass while a need drifts, that is the owner's
    to ask for as its own item. **SOL** on LLR-158 (`APPROVAL_ACT_CSVS` also
    holds the two assumption tiers) and TC-167 (IF-126 is now cited by
    TC-271): both amended in place under the original grant.

26. **WI-655 (f78d875f), major: two DA placements — SOL.** DA-005's premise
    (a hosted verdict the operator reads) lands on B-09, not the
    governed-write crossing B-01. SR-157 only reports declared rule
    violations and does not rest on DA-001's premise that resolved rows are
    semantically trustworthy, so its citation goes and SR-157 takes an honest
    `coincident` reason.

27. **WI-655, major: four `boundary_refs` re-points break the builder's own
    rule — SOL, bounded.** SR-146 still requires shipped prompt files (B-05
    stays), SR-156 spans serial integration writes (B-01) as well as the
    runner (B-10), SR-170 governs writes through B-01, and SR-215 files a work
    item through B-01. `boundary_refs` is a multi-valued traced cell. **Ruling:**
    each SR lists every crossing its approved text names. Splitting a row
    would amend approved requirement text, which this lane's grant excludes,
    as it did for SR-139. A frame-spanning SR that results is named as a
    remaining advisory, not split here.

28. **WI-655, major: TC-279 does not evidence DA-011 — SOL.** DA-011's
    antecedent (the readability measures report no worsening) is never
    established by a sample of arbitrary parts, and the case declares none of
    what its judgement reads. **Ruling:** the smaller honest remedy.
    Re-author Drafted DA-011 to the spine map's D5 premise (the sampled
    reader's result generalizes beyond the sample), and declare the source
    tree and the linked registries as TC-279's inputs so a change stales it.

29. **WI-655, minor: IF-030's shared waiver — SOL.** Its data is the whole
    documentation tree, not one registry format. It gets its own
    `coincident` reason.

30. **WI-655, minor: the census test checks the model, not the brief —
    SOL.** It renders the assumptions approval brief and asserts that TC-279
    appears on it.

31. **The re-judges (ef5184cf), blocker: TC-055's pass is unearned — SOL.**
    TC-055's approved Method asks for "a fresh, family-heterogeneous CRITIQUE
    session", and the adjudicator is the same model family as the rendering
    code's authors. Disclosure is not the degraded path SR-154 allows, which
    requires a cross-family draw to be configured and unavailable, with the
    selection logged before launch. Here a cross-family judge (Codex Sol) was
    available. **Ruling:** the same-family observation record is dropped in
    the lane before merge. Nothing on trunk records it, so nothing is
    softened. Its verdict file stays as the record of a session that did not
    qualify. Codex Sol critiques the same 30-shot matrix against
    `docs/rubrics/dashboard-usability.md` in a second verdict, and the
    coordinator records that result through the kit's writer, naming Sol as
    the judge. TC-209 and TC-210's passes and both NEEDS-JUDGEMENT calls stand
    (Sol: earned, honest). The two NEEDS-JUDGEMENT rows, WI-684 (TC-036) and
    WI-688 (TC-211), stay open with their owed act stated. Closing them would
    make every later merge re-mint them, because the checkpoint suppresses a
    second draft only while a row is open. The two surface findings fold
    into them. TC-036's `inputs` omit `RESYNC_PACK.md`, where the procedure
    lives (WI-684). `docs/test/inspection-procedures.md` hand-restates
    results inside a declared input while the observation writer is the one
    authority (WI-688, whose owed act re-runs a procedure there).

32. **WI-655, confirmation round (063e4225) — SOL on SR-174, applied by the
    coordinator.** Rulings 26 to 30 are confirmed, and Sol found nine of the
    builder's extra re-points honest. The builder asked whether SR-174 (work
    item id allocation) crosses B-01. It does: it allocates and permanently
    reserves ids through trunk-side registry mints, a governed state write.
    That is one traced cell, so the coordinator sets `boundary_refs =
    ["B-01"]` at integration, as ruling 23 did for wording.

33. **WI-615 (e520b6e6..307d795d), the blocker: three shipped behaviours no
    row claims — SOL.** The per-model guardrail payload selection (a new
    file-read seam), `gen_skills_index --check`'s description floor (a new
    exit arm under approved LLR-025 and TC-025), and whole-directory skill
    materialization (IF-035 still declares only `SKILL.md`). The builder
    found no honest parent and minted nothing. Wave-4 ruling 5 governs:
    untraced shipped behaviour is the defect the kit exists to prevent, and
    "no parent" is answered by a labelled derived requirement (the
    spine-authoring skill's rule (c)), not by leaving it untraced. **Ruling:**
    the coordinator grants SR-223 (derived, only if no approved SR honestly
    parents a behaviour), LLR-279 to LLR-281, TC-289 to TC-292, IF-253 and
    IF-254. It also grants amendment authority, in place, status left
    Approved, over LLR-025 and TC-025 (the floor's exit arm) and over IF-035's
    row and Contract body (companion files).

34. **WI-615, major: `delivery_inventory` is never exercised, and two
    in-process tests sit in slow modules — SOL.** A planted companion-file
    assertion drives `delivery_inventory`, and the pure regressions move to
    fast modules and are traced as Smoke (D31), each red first.

35. **WI-615, minor: AGENTS.template.md lost "versioned releases" — SOL.**
    The byte payment dropped the qualifier that makes `DevStg-Release`
    conditional, which PROCESS.md states. It is restored within the
    10,000-byte cap, and the row is re-stamped.

36. **WI-615, fix round (51c9de2f) — SOL on both.** Rulings 34 and 35 are
    confirmed, and so are SR-223 (derived, honest) and LLR-279 under SR-112.
    Two points remain. The description floor still hangs on SR-112, which
    obliges checked per-agent copies and says nothing about whether a
    description is adequate. The builder itself wrote "by ruling, not by
    fit", and that is the silent parenting of a derived obligation the
    spine-authoring skill forbids. And IF-019 is the INDEX.csv file seam,
    while PROCESS.md makes a CLI's exit code an interface row of its own.
    **Ruling:** the coordinator grants SR-224 for the floor as a labelled
    derived requirement. LLR-281 and TC-291 claim it, and IF-254 carries
    `--check`'s whole exit contract (`channel = "exit-code"`). LLR-025 and
    TC-025 go back to their approved text, reverting this lane's amendments,
    and IF-019 returns to the file seam.
