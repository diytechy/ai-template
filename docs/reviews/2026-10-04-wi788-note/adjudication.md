# Adjudication of the WI-788 design-note disputes (cd5ee53d)

**Adjudicator:** Claude Opus 5.5, independent. I wrote none of the note, Sol's
review or the fix round. Under OI-103 Q3 this ruling is final.

**Read:** the README and all four chapters at `cd5ee53d`; `git diff e3754af6
cd5ee53d`; `docs/decisions/wi-788.toml`; the WI-788 spec (B1-B12, risks 1-9, the
2026-10-03 scope); the OI-101 and OI-103 records (`decision` cells verbatim);
the S11 plan §4.1, §4.6, §4.7 and §6; `sol-review.md`; and the code and prompts
cited below.

**Probe:** a scratch repo outside the tree, git 2.49.0.windows.1 (dispute 1).

**Lane:** HEAD `cd5ee53d`, clean before this file was written. Nothing else
was edited.

**Shorthand:**
- `README`, `ch.1` to `ch.4` are the files under
  `docs/plans/2026-10-04-wi788-design/`.
- `WI-788 spec` is
  `docs/work/active/wi-788/WI-788-provider-homes-and-new-routes.md`.
- A bare `:N` is a line in the file last named.
- Script paths under `agent_loop.py`, `plan_runner.py` and `kitlib/` are in
  `project-trajectory/scripts/`.
- `prompts/` is `project-trajectory/prompts/`.

---

## Dispute 1: BLOCKER 2, the owner-commit race

**Question.** Sol says a pre-commit check of the authority leaves a race
between the check and the ref advance, so it does not hold exclusion through
the advance. Is the note right that:
- for tool writers, the check and the advance are now one critical section;
- the owner's own commits are outside the tool, so the hook is advisory for
  them;
- a racing owner commit fails the landing's compare-and-swap rather than
  landing unseen?

**Evidence.**
- **What OI-103 Q1 rules.** The owner's words
  (`docs/requirements/open-items.toml:3818`): "with this design there should be
  nothing running on the trunk, everything should be routed through a WI now
  mechanically, stopping concurrency issues resulting from the tool running.
  Agreed the user might approve an item, but that generally not be done while
  the thread is running."
  - The coordinator's reading (`:3821`) is "nothing the tool runs writes to
    trunk directly", and notes that the owner's approvals rarely happen while
    the loop runs.
  - The writers in option (a) (`:3841`) are all tool writers: claims, mints,
    acts and keep-warm records.
  - Nothing in the ruling asks the kit to exclude a person's own commits.
- **What Sol's finding was aimed at.** At `e3754af6`, one table row read
  "Coordinator and owner commits | the hand path | Not the tool's, so they take
  only the hook's authority check" (`e3754af6`, ch.4 line 147).
  - The coordinator half was a real exemption of a tool writer, and the fix
    removes it: coordinator writes go through a station lane
    (`docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md:124-131`,
    `:172`).
  - Every tool ref advance now re-checks `generation` and swaps the ref while
    holding the mutation lock (`:112-117`).
  - So, for every tool writer, the race Sol names is closed.
- **What remains is the owner's commit (`:132-138`). Both writes are already
  compare-and-swap.** In the scratch repo:
  - A pre-commit hook that advanced `main` by `git update-ref refs/heads/main
    <new> <old>` made the owner's `git commit` fail (exit 128, "cannot lock ref
    'HEAD': is at <landing> but expected <base>").
  - After an owner commit, the landing's `git update-ref refs/heads/main <new>
    <old>` failed the same way (exit 128).
  - So the check-to-advance window lets neither write overwrite the other.
  - The landing keeps `bookkeeping.py` as its install (ch.4 `:171`). That
    install re-checks HEAD before it installs, and restores its writes on a
    lost swap (`project-trajectory/scripts/bookkeeping.py:48`, `:73-77`).
- **A person's git cannot be fenced.** `--no-verify` and a bare `update-ref`
  bypass any hook.
  - So the kit cannot hold exclusion through the owner's own advance. The
    hook's refusal is the most it can do there.
  - The landing's swap makes the remaining race safe.
  - Requiring more would be a new rule, not OI-103 Q1.
- **The defect: the note gives two contradictory answers to one event.** When
  the landing's swap fails on a foreign commit:
  - ch.4 `:136-138` says the lane re-runs `REFRESH` inside its own authority,
    and a session retakes any stale act (S11 Q6);
  - ch.4 `:156-158` says "Under full coverage that refusal is unreachable. If it
    is reached, it exposes a defect ... The fix moves that writer; it does not
    add a retake path."

  The owner's commits are uncovered by design, so the refusal is reachable by
  design, and whoever builds the landing's failure handler cannot follow both
  passages.
- **The retake is the ruled answer, not a new fallback.** S11 Q6 is ruled ("a
  session retakes a stale act", `docs/plans/2026-10-03-s11-in-lane-adjudication.md:328`).
  S11 §4.1 already named the retake for a trunk act that lands first (`:172`).
- **No row tests the retake.** S788-landing's Done-when stops at the failed
  swap (ch.4 `:688`).

**Ruling: AMEND.**
- The note's position stands. Sol's request is not upheld for the owner's own
  commits:
  - for every tool writer, the check and the advance are one critical section;
  - the owner's commit is outside the tool under OI-103 Q1's own words;
  - a racing owner commit cannot land unseen and cannot be overwritten.
- The note must give one answer to a failed swap.

**Required change.**

(a) In `docs/plans/2026-10-04-wi788-design/4-adjudication-mint-landing.md`,
replace lines 152-158:

```
**When the authority replaces S11 §4.1's freshness rung:** only once every
writer in §3 has moved (B3, B11). The proof needs no new rung. The landing's
compare-and-swap and today's ancestor check (`integrate.py:1648`, `:2731`)
refuse any trunk move the authority did not make, naming the foreign commit.
Under full coverage that refusal is unreachable. If it is reached, it exposes
a defect: a writer the authority does not cover. The fix moves that writer; it
does not add a retake path.
```

with:

```
**When the authority replaces S11 §4.1's freshness rung:** only once every
writer in §3 has moved (B3, B11). The proof needs no new rung. The landing's
compare-and-swap and today's ancestor check (`integrate.py:1648`, `:2731`)
refuse any trunk move the authority did not make, naming the foreign commit.
The landing has one answer to that refusal, whoever moved trunk: the lane
re-runs `REFRESH` inside its own authority, and a session retakes any stale
act (S11 Q6). Under full coverage only the owner's own commit (above) can
cause it. A foreign commit the tool made exposes a defect, a writer the
authority does not cover; the fix moves that writer (the writer census,
S788-dual-pickup) and adds no second answer for it.
```

(b) In the same file, S788-sitting's Done-when: after line 709
(`  - a rejected final review drops the act;`), insert:

```
  - a landing whose swap fails on a foreign trunk commit re-enters `REFRESH`
    under the same authority, and a stale act is retaken by a session;
```

---

## Dispute 2: BLOCKER 3, the same-family adjudication reviewer

**Question.** With two enabled families, the note draws the adjudication
reviewer (author-review) as a second session of the adjudicator's family
(ch.2 `:128-130`). Is that "the rule's preference order, recorded per call",
or a second path under risk 7?

**Evidence.**
- **The owner's independence rule has a preference in it.** "Never the
  authoring session; preferably another family" is the standing rule. SR-154's
  approved text already says "drawn from a different model family wherever one
  is configured, degrading only to the documented same-family mode"
  (`docs/requirements/system-requirements.toml`, SR-154 `requirement`).
- **Risk 7 forbids something else** (`docs/work/active/wi-788/WI-788-provider-homes-and-new-routes.md:426`):
  a degenerate or legacy mode wrapped around a single point of failure.
  - A ranked selection whose unmet preference is recorded is one rule with one
    code path. Only the inputs change, namely the enabled pool.
  - The integrator is right on the principle. It is not a second path.
- **The spec states the preference against the adjudicator.** The spec's
  reading of "independent" (WI-788 spec `:299-301`) is "always a different
  session, and preferably family, from the adjudicator it checks". The note says
  the same twice:
  - its own family table (ch.2 `:45`: "Never the adjudicator's session, and
    preferably another family");
  - its glossary (README `:157`).
- **The step-2 table adds a second preference, and the example sacrifices the
  wrong one.**
  - Row `:124` excludes "the adjudicator's and builders' families where the
    pool allows" and says nothing about which yields first.
  - The example (`:128-130`) yields the adjudicator-family preference and keeps
    the builder-family one.
  - In the two-family pool {X builder, Y adjudicator}, the spec's preference
    (not Y) is satisfiable by X. So "preference unmet" is a choice, not a
    limit of the pool.
- **The note's choice also gives the weaker chain.**
  - The final review judges "the adjudicator's ADJUDICATE and MINT ranges
    only" (ch.2 `:126`; ch.4 `:327-336`), not its `author` ranges.
  - So under the note's order, the adjudicator's own drafted spine text is read
    before the act only by a second Y session and by its own unchanged pass. No
    other family reads it, in this repo's actual pool.
  - Under the other order (author-review X), every approved byte is read by
    another family before the act:
    - the builder's text (X) by the adjudicator (Y), who adopts it and holds
      the act;
    - the adjudicator's drafts (Y) by the author-review (X);
    - the author-review's edits (X) by the adjudicator's unchanged pass (Y).
  - The builder-family preference costs little to drop here, because the
    builder's bytes already had their cross-family read from the adjudicator.
    The author-review can only edit; it cannot act.
- **Act admission is unaffected** (ch.4 `:358`: the adjudicator's family must
  differ from the build and plan authors, and its session from every
  author-review session). Neither condition involves the author-review's
  family.
- **Scope of the feasibility claim.** "Every kind has an eligible draw"
  (`:130`) holds for a lane built by one family.
  - Today's implementer swap moves the build to the other family within one
    lane (`project-trajectory/scripts/agent_loop.py:618-621`), and ch.3 §4.7
    keeps it (the swapped family replans and builds).
  - Such a lane's build ranges carry both families, so the hard family
    exclusions of `review` (`:120`) and `adjudicate` (`:125`) leave no draw in a
    two-family pool.
  - This is the failure Sol's BLOCKER 3 names, in another instance. I note it
    under the blocker check and do not rule on it here.

**Ruling: AMEND.**
- The integrator's principle is upheld:
  - "preferably another family" is a ranked preference inside the one rule,
    with the unmet preference recorded per call;
  - same family with a different session is within the owner's rule and
    SR-154's documented mode, not a risk-7 path.
- The order is wrong. The adjudicator-family preference, which the spec, the
  family table and the glossary all state, binds first. The builders'
  families yield first.

**Required change.** In
`docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md`:

(a) Replace line 124:

```
   | author-review | the adjudicator's `author` ranges, and the builder text they adopt | the adjudicator's session always; the adjudicator's and builders' families where the pool allows (the owner's "preferably another family" is the rule's preference order, recorded per call) |
```

with:

```
   | author-review | the adjudicator's `author` ranges, and the builder text they adopt | the adjudicator's session always; then two ranked preferences, the adjudicator's family first and the builders' families second, a preference dropped only when the pool cannot meet it and the unmet one recorded per call (the owner's "preferably another family", stated against "the adjudicator it checks") |
```

(b) Replace lines 128-130:

```
   **With today's two-family pool** (builder family X, the other Y): review Y,
   adjudicate Y, author-review a second Y session (preference unmet, recorded),
   final review X. Every kind has an eligible draw.
```

with:

```
   **With today's two-family pool** (builder family X, the other Y): review Y,
   adjudicate Y, author-review an X session (the builder-family preference
   unmet, recorded), final review a fresh X session that authored nothing in
   the sitting. Every approved byte is then read by another family before the
   act: the builder's by the adjudicator, the adjudicator's drafts by the
   author-review, the author-review's edits by the adjudicator's unchanged
   pass. Every kind has an eligible draw for a lane built by one family.
```

---

## Dispute 3: BLOCKER 5, extending the S9 check

**Question.** The fix extends S9 to CRITIQUE and plan-critique, so those kinds
skip the decisions note (ch.2 `:194-197`; D-014). It assumes their briefs commit
only a verdict, and did not check them. Is that assumption, and the mechanism,
right?

**Evidence.**
- **CRITIQUE commits only its verdict.**
  - It writes its verdict to `{verdict}`
    (`project-trajectory/prompts/critique.template.md:24`).
  - It may propose `[TC-HARDEN]` lines inside that verdict, and it "NEVER
    edit[s] the spine or the artifact" (`:39-41`).
  - It ends: "commit that verdict file ... and stop" (`:44-46`).
- **plan-critique and the arbiter commit nothing.**
  - Both briefs end "One block, nothing else"
    (`project-trajectory/prompts/dual-plan-critic.template.md:65-77`;
    `project-trajectory/prompts/dual-plan-arbiter.template.md:78-80`).
  - The runner, not the session, writes the critic's block as
    `critique-of-<plan>.md` (`project-trajectory/scripts/plan_runner.py:490-492`).
  - The integrator's premise about the briefs therefore holds, and the policy
    is right: none of these kinds can owe a decisions record.
- **The mechanism as worded is false.** "S788-ask extends its phase list" names
  only half of S9. S9 has two parts:
  - **The phase set** `REVIEW_PHASES` (`project-trajectory/scripts/kitlib/verdict.py:189`,
    read at `:944`). The live arm runs only for a review (`agent_loop.py:2460-2463`).
  - **The verdict-file identity.** `scope_offenders` (`kitlib/verdict.py:822-842`)
    treats as the session's own file only what `round_file` parses.
    `ROUND_FILE_RE` admits only `REVIEW-[A-Z]` names (`:219-222`).
- **A phase-list change alone breaks CRITIQUE.** CRITIQUE's verdict is
  `<n>-CRITIQUE-<sha7>.md` (`project-trajectory/scripts/agent_loop.py:1703-1705`).
  It is not a round file, so it would count as an offender, and every CRITIQUE
  range would be refused.
- **Widening `REVIEW_PHASES` itself is worse.** It also drives:
  - `is_review` (`agent_loop.py:2866`);
  - the review-policy ceiling (`:3766`);
  - the owed review phases (`kitlib/verdict.py:1174`).

  CRITIQUE would then become an owed review round.
- **plan-critique has no verdict file of its own**, so the S9 rule that fits it
  is an empty range.
- **The hedge "If a build finds a brief ..." (`:201-202`) is now answered.**
  It defers to the build a check that this adjudication has made.

**Ruling: AMEND.**
- The policy stands. CRITIQUE, plan-critique and the arbiter are verdict-only
  kinds and skip the note; judge gets it.
- The mechanism must be stated correctly, so that the build does not refuse
  every CRITIQUE or turn CRITIQUE into a review round.

**Required change.** In
`docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md`:

(a) Replace lines 194-197:

```
   - **That rule is S9's**, and today it reads REVIEW-A/B only
     (`kitlib/verdict.py:189`, `:944`). S788-ask extends its phase list to
     CRITIQUE and plan-critique (and arbitrate under Q-5 (b)); those kinds then
     skip the note, because their calls are recorded by their verdicts.
```

with:

```
   - **That rule is S9's.** Today it covers REVIEW-A/B only, in two parts: the
     phase set `REVIEW_PHASES` (`kitlib/verdict.py:189`, read at `:944`; the
     live arm runs only for a review, `agent_loop.py:2460-2463`) and the
     verdict-file identity (`scope_offenders` through `round_file`, whose
     `ROUND_FILE_RE` admits only `REVIEW-[A-Z]` names, `kitlib/verdict.py:219-222`,
     `:822-842`). S788-ask gives S9 its own phase set and leaves
     `REVIEW_PHASES` alone (it also drives `is_review`, `agent_loop.py:2866`,
     and the owed review phases, `kitlib/verdict.py:1174`). Each added kind's
     verdict file is stated:
     - **CRITIQUE** commits only its verdict
       (`prompts/critique.template.md:24-46`), named `<n>-CRITIQUE-<sha7>.md`
       (`agent_loop.py:1703-1705`); S9 admits exactly that file, in both arms.
     - **plan-critique**, and arbitrate under Q-5 (b), end in one block and
       commit nothing (`prompts/dual-plan-critic.template.md:65-77`,
       `prompts/dual-plan-arbiter.template.md:78-80`); the runner writes the
       block (`plan_runner.py:490-492`), so S9 admits an empty range.

     Those kinds then skip the note, because their calls are recorded by their
     verdicts.
```

(b) Delete lines 201-202:

```
     If a build finds a brief that asks a verdict-only kind to commit anything
     else, that kind gets the note instead of the S9 entry.
```

---

## Blocker check (Sol's five BLOCKERs at `cd5ee53d`)

1. **BLOCKER 1, squash vs risk 6: RESOLVED.**
   - The conflict is no longer presented as settled design. It is put to the
     owner as a collision of OI-101 Q2 with OI-103 Q4, and each option names the
     ruling it amends.
   - Locations: ch.4 §7 `:471-488`, §6 `:371-373`; README Q-8 `:328` and change
     26 `:139`; D-027.
2. **BLOCKER 2, the authority: RESOLVED**, subject to dispute 1's amendment.
   - Coordinator writes go through a station lane (ch.4 `:124-131`, `:172`;
     README change 25 `:138`).
   - Every tool ref advance is a compare-and-swap inside the critical section
     (ch.4 `:112-117`).
   - The leases are waited for while holding nothing, and the authority gets
     one non-blocking try (ch.4 `:70-85`; README `:56-69`; ch.2 `:160-174`).
   - D-016 is amended, and the pause file goes to the owner (README Q-12 `:332`).
3. **BLOCKER 3, judged scopes and B10: RESOLVED as Sol traced it**, subject to
   dispute 2's amendment.
   - There is an exact judged-scope table per kind (ch.2 `:113-130`).
   - B10's exception is carried identically into routing, session reuse (ch.2
     `:147-153`) and act admission (ch.4 `:358`), and stated once at ch.4
     `:441-444`.
   - One instance of the failure Sol named remains: after today's implementer
     swap (`agent_loop.py:618-621`), a lane's build ranges carry both families.
     The `review` and `adjudicate` rows (ch.2 `:120`, `:125`) then leave no
     draw in the two-family pool.
   - The note must settle that case. Dispute 2's principle (sessions excluded
     hard, families as ranked and recorded preferences) is the one-rule way
     to do it.
4. **BLOCKER 4, PAGE: RESOLVED.**
   - The parent closes `partial`.
   - `MINT` mints the open item and a successor decomposition row, carrying
     `source`, the parent's round evidence and `needs` on the open item and the
     parent. The owner's ruling becomes its Done-when.
   - Locations: ch.3 §4.6 item 5 `:263-281`; README `:47-49`; D-023.
5. **BLOCKER 5, the decisions-note exclusion: RESOLVED**, subject to dispute
   3's amendment.
   - Verdict-only kinds are distinguished from judgment calls that write other
     evidence.
   - Judge gets the note, because the re-judge commits an observation record
     (`prompts/adjudicate-rejudge.template.md:43-56`).
   - Locations: ch.2 step 8 `:191-205`; D-014.

RULING: 0 upheld for the note, 0 for the reviewer, 3 amended
