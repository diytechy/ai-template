# Handoff: vocabulary migration, then the functional changes

Written 2026-11-11 for two readers, and revised later the same day. The
operator reviews it and writes a decision into each `Operator:` line. The next
session reads it cold, with no access to the conversations that produced it,
cuts a branch and makes the changes.

It sits beside two files. `README.md` is the review this work came from;
sections are cited as README §N. `VOCABULARY.md` is the census behind §4: what
each old word names today, with the identifiers and the files.

**The words in this file.** It is written in the vocabulary that §4 settles:
"operator" for the person in charge (formerly "owner"), and "accept" for both
approve and attest. A name in backticks is spelled as it is on disk today
unless a table gives its new spelling. `README.md` still uses the old words.

## §1. Where things stand

| | |
|---|---|
| Repository | `C:\Projects\ai-template`, trunk `refactor_again`, at `7fa851f33` |
| Primary checkout | untouched by this work |
| This work | worktree `C:\Projects\ai-template-wt-test-tiers`, branch `proposal/test-tiers`, **committed locally, not pushed**: 90 changed files, 5 new files |
| Interpreter | `C:\Projects\ai-template\.venv\Scripts\python.exe` (the worktree has no venv) |
| How it was run | from outside the repository root, on purpose, so the repository's own skills and workflow did not drive it. No work item, no lane claim |

The branch holds two things (README, "How to review this branch"):

1. **A prototype of change-scoped checks**: `run.cmd iterate`, a 16-test
   canary set, 22 tests. Repo-local; no shipped file.
2. **A rename of three settings** and the words around them, with its
   `RESYNC_PACK.md` entry and a new Checks section in the shipped glossary.

Verified: the unfiltered suite passed after the rename apart from one
line-count ratchet, since fixed; the modules the later edits touch were re-run
green; the four strict lints pass. The record is README §5.

Three things the next session must know before touching the branch:

- **It is committed with the commit hook bypassed,** at the operator's direction
  on 2026-11-11: this is a maintenance branch, and the standard conventions
  (hooks, lane claims, work items) are set aside for it. That permission was
  given for this branch. Ask before applying it to another.
- **The hook would have refused it.** Three floor steps (`cli-reference`,
  `interface-reference`, `trajectory-map`) report stale generated views,
  because help text, contract text and a dashboard panel were reworded. The
  views are still stale in the commit. They regenerate with
  `trunk_step.py --regen` when the work reaches trunk; a claimed lane is
  exempt from those steps and an unclaimed branch is not.
- **It is not pushed.** The commit protects the work from a removed worktree,
  not from the machine.
- **To discard it all:** `git worktree remove --force
  C:\Projects\ai-template-wt-test-tiers`, then `git branch -D
  proposal/test-tiers`.

**The revision of 2026-11-11.** A second session settled the vocabulary with
the operator (§2, §4) and the question of old records (D3, §5). It rewrote
this file and added `VOCABULARY.md`. It changed nothing else on the branch.

**The third session, 2026-11-11.** It recorded the operator's answers to D4
to D11, cut the migration branch, traced the questions §5 left open, and began
the migration. §9 is its record: what is done, what the traces found, and the
decisions it raises (D12 to D18). Read §9 before §5; where they differ, §9 is
later. **A session taking over starts at §10, the runbook, and §11 lists what
waits on the operator.**

**The fourth session, 2026-11-11.** It recorded the operator's answers to D12
to D18, the name for D6 and §4.5.1, put a § sign in every numbered heading so
that a search for "§4.5.1" finds it, committed the migration so far as a
checkpoint, and went on with §10.4. §9.7 is its record.

**The fifth session, 2026-11-11 into 11-12.** It read the result of the fourth
session's test run, fixed what it found, committed "human" to "operator", and
applied "owner" to "operator". §9.8 is its record; §10.4 is done apart from
its checks, and §10.5 is next.

| | |
|---|---|
| Migration work | worktree `C:\Projects\ai-template-wt-vocabulary`, branch `maint/vocabulary`, cut from `proposal/test-tiers` at `b5ea4d29c`. The branch may commit with the hook bypassed (D14). Checkpoint `6d8291fb6` holds everything §9.1 lists; `d45bab5a5` holds "human" to "operator" (§9.7, §9.8); not pushed |
| This file and `VOCABULARY.md` | still uncommitted in the `proposal/test-tiers` worktree, which holds no other change |

## §2. Decisions the operator has made

From the first session:

- The 16-test canary set is accepted as a first cut.
- `[bars]` does not belong in `docs/stack.ini`, and the word means nothing
  from outside. Renamed and re-homed (README §12).
- `red_mark` was ambiguous. Now `[product] expected_failure_marker`.
- `red_rounds_max` did not say what happens at the limit. Now `[build]
  stop_lane_after_consecutive_commit_check_failures`.
- A shipped contract changing is not a reason to hold back. Re-syncs are fine;
  clarity and right placement in the template come first.
- One word for one thing across the whole kit, in agreement with the glossary.
- The remaining vocabulary work goes on its own branch (the operator had no
  strong view; the first session's recommendation).
- The overnight runner should be removed (§6, item B8).
- This is a maintenance branch. It does not follow the repository's standard
  conventions, and its commit bypassed the hook.

From the second session, on the vocabulary. The tables are in §4.

- **Accept replaces both approve and attest.** An operator accepts outcomes.
  At the pace projects now move nobody can approve every nuance, and a
  project's own approval ceremonies are not visible to the kit.
- **Operator replaces both owner and human** for whoever performs the
  reserved acts. The word is chosen so that the operator can delegate those
  acts to an LLM session.
- **The tooling can never know whether a person acted.** Every field or value
  that controls who may do what says operator. "Human" may appear only in
  prose, to state an intent.
- **`OWNER_SCRATCHPAD.md` becomes `OPERATOR_SCRATCHPAD.md`.** Its header may
  still say it is for a person's notes.
- **The record that checks passed is the passed-checks record,** not an
  acceptance, and it says which checks passed.
- **The requirement field `verification` becomes `verification_method`.**
- **The `Attest` method becomes `Vouch`.** "Sign-off" was considered; the
  hats' sign-offs at stage gates already use it.
- **The core tooling does not stay backwards compatible.** What is required
  is a clear path from an older template set to the current one: re-sync
  instructions an LLM follows, or purpose-built migration tooling (D3, §5).

## §3. What the operator is asked to decide

Each item has a recommendation. Write the decision on its `Operator:` line.

**D1. Keep this branch?** Recommended: yes, as the base the next branch is cut
from.
Operator: yes. Committed 2026-11-11 with the hook bypassed; the three generated
views were not regenerated.

**D2. The terms in §4.**
Operator: ruled 2026-11-11 for §4.1 to §4.4, apart from the rows marked
"proposed" there (D10). The earlier drafts in §4.5 are still open; each has
its own line.

**D3. Old records.** Several renames change a format that is already stored:
commit trailers, session-log headers, registry values, config keys.
Operator: ruled 2026-11-11. No compatibility readers in the core tooling. Old
data is migrated at the re-sync, by a purpose-built migrator for stored values
and by the session for prose. Formats in git history are cut cleanly (§5).

**D4. Names of existing tests.** Test functions named for an old word: 178
for approve, 113 for attest, 44 for owner, 17 for human, in four files named
the same way. For bar and red, 100 evidence entries in 20 test-case rows name
such a test, in 12 files. Recommended: rename the files and functions along
with the code, and update the evidence cells in the same change, since a
half-renamed suite is the inconsistency the operator asked to remove. The
cheaper alternative is to leave existing test names and apply the vocabulary
to new tests only.
Operator: agreed 2026-11-11, as recommended. Files, functions and evidence
cells move in the same change as the code.

**D5. Accepted rows whose text uses an old word.** Changing accepted text is
an amendment. For bar and red it is 13 rows (README §12). For the words of
§4 it is far more: of 904 accepted rows, 196 hold attest, owner or human in
their text, and 286 hold one of those or approve. Both are upper bounds, since
some uses stay (§4.3). Recommended: amend the wording on the migration branch
and let the landing mint the adjudication rows, each a wording-only change. At
this size one acceptance act covering all the wording-only changes may be
better than a row per amendment; whether the tooling allows that was not
checked.
Operator: ruled 2026-11-11, against the recommendation. Change the text for
consistency. The meaning is the same, so it is not an amendment: no
adjudication rows and no re-acceptance. The acceptance record's copy of each
row therefore moves with the row, in the same change (§5).

**D6. What a commit must pass.** `[required-checks] commit` is `"smoke"`
today. Recommended: `"iterate"`, together with D7.
Operator: the recommendation is fine, 2026-11-11. The operator asked whether
another term had been in use for it. Four were: `iterate` (the suite and the
command), "change-scoped checks" (§1 here, and the commit subject), "inner
loop" (the README's title) and "focused" (the README's word for the
selection). One is to be kept before B1 is built; the suite's name is open
until the operator picks.
Operator, on the name, 2026-11-11 (fourth session): **iterate**. The operator
asked whether this was the canary set. It is not: the canary set is the fixed
part (16 tests, one per capability, run on every commit), and `iterate` is the
whole commit check: the lints, the tests the change names, and the canary set.
"Canary set" stays the name of the fixed part; "change-scoped checks", "inner
loop" and "focused" retire.

**D7. What a landing must pass.** Today a hand landing runs the smoke tier and
the unfiltered suite runs once per leg. Recommended: the unfiltered suite once
per landing, declared as `[required-checks] landing` with a reader.
Operator: the recommendation is fine, 2026-11-11.

**D8. The overnight runner.** Recommended: remove the launcher (the first row
of the table in B8) with the migration, and decide the other three rows with
B9.
Operator: agreed 2026-11-11. The launcher can be stripped out.

**D9. Order.** Recommended: vocabulary first (§4, §5), then the functional
changes in the order of §6.
Operator: agreed 2026-11-11.

**D10. The rows marked "proposed" in §4.** The operator saw them on
2026-11-11 and raised no objection, but did not rule on them one by one: the
table name `[authority]`, the verb `record-checks`, "recorded verdict" as a
name, "admit" for merge admission, "operator ruling" in citations, and the
names for the party `EXT-006` and for a product's operators. Recommended: as
written.
Operator: agreed 2026-11-11, as written. Every row marked "proposed" in §4.2
to §4.4 is now ruled.

**D11. The legacy readers already in the core scripts.** Twelve tables read
spellings older than this migration (`VOCABULARY.md` §9), and no adopter on
this machine holds the intermediate ones. By D3 they belong in the migrator.
Recommended: a separate change after the vocabulary, so that this one stays
reviewable.
Operator: agreed 2026-11-11. Migration tooling is its own kind of thing and
is not part of the core; the legacy readers leave the core scripts for it, in
a separate change after the vocabulary.

## §4. The vocabulary

The shipped glossary (`project-trajectory/GLOSSARY.md`) says one term names
one concept, and that an entry states which word is kept where two were used.
The old words break that rule in both directions. "Attest" names seven
things, "owner" seven and "human" eight, and both new words were already in
use. So the tables below go by thing, not by word. `VOCABULARY.md` has the
identifiers and files behind each row.

The **State** column says **ruled** (the operator decided it on 2026-11-11, or
it follows directly from a ruling in §2) or **proposed** (D10). D10 was
agreed as written later the same day, so a row that still reads "proposed" is
ruled. §4.5 is separate: its drafts each wait on their own `Operator:` line.

### §4.1 Glossary entries, drafted

Five entries. The glossary's Checks section already holds seven from this
branch: required checks, commit checks, landing checks, gate checks, check
suite, expected-failure marker, commit-check failure cap.

**operator**

> The role that holds the kit's reserved acts: accepting rows on an
> operator-held rung, ruling open items, confirming or overruling delegated
> decisions, the final read, the push. A person, or a session that person has
> delegated to, with the delegation and its scope recorded. Never a session
> the loop or a launcher started; that is the one line the tooling enforces.
> Formerly "the owner" and "the human", two words for one role; **operator**
> is kept.

**accept**

> The act that takes a row as agreed. Its `status` moves from `Drafted` to
> `Accepted`; after an amendment the row is **re-accepted** and its status
> does not move. The operator takes the act on an operator-held rung, and an
> independent adjudicator on a released one. Accepting a row takes it as an
> outcome to build on. It does not claim that every nuance was reviewed, and
> it says nothing about tests passing. Formerly "approve", "attest" and
> "re-attest", three words for one act; **accept** is kept. A project's own
> approval ceremonies are outside the kit.

**human** (a usage rule for the glossary's preamble)

> The tooling cannot know whether a person acted. No field, value, flag or
> exit code that controls who may do what says "human"; those say operator.
> "Human" appears only in prose, where it states that a person is intended.

**Vouch**

> The verification method for what no check can establish, such as a
> playtest, a creative review or a physical action: the operator's recorded
> word that the requirement is met, naming who and when. It rests on trust,
> and the trace report counts it apart from mechanized results so that an
> audit sees how much does. Declared as `verification_method = "Vouch"`.
> Formerly `Attest`; **Vouch** is kept.

**passed-checks record**

> The line in a commit message recording that a named set of checks passed on
> a named tree: `Checks-Passed: tree=<sha> work=<sha>
> checks=<commit|landing|none> tests=<digest|none> <summary>`.
> `integrate.py record-checks` writes it for the commit checks and the station
> refresh writes it for the landing checks; the merge slot re-derives both ids
> from git before it trusts one. It is a script's record of a result. Nobody
> decides anything, so it is not an acceptance. Formerly the "bar
> attestation", written `Bar-Green: ... bar=<review|landing|no-bar>`;
> **passed-checks record** is kept, and a trailer in the earlier form is not
> read.

- Renames: trailer key `Bar-Green` to `Checks-Passed`; field `bar=` to
  `checks=`; values `review` to `commit`, `landing` unchanged, `no-bar` to
  `none`; CLI `attest --bar review` to `record-checks --checks commit`.
- What it says about the checks: which set, on which tree and work commit, a
  digest of the tests derived for the row, and a one-line summary.
- Alternatives: `Checks-Green:` keeps the green idiom that §4.5.6 retires.
  `Verified:` reads as a row status.

### §4.2 Attest and approve become accept

| The thing | Today | New | State |
|---|---|---|---|
| A row's status once taken | `Approved` | `Accepted` | ruled |
| The act | approve, approval act, first approval, the verdict `APPROVE`, "attestation" | accept, acceptance act, first acceptance, `ACCEPT`, acceptance | ruled |
| Repeating it after an amendment | re-attest, `--reattests`, `reattest_model`, "Re-attestation brief" | re-accept, `--reaccepts`, `reaccept_model`, "Re-acceptance brief" | ruled |
| The act's other flag and its ledger keys | `--approves`; `approved` and `reattested` in `acts.toml` | `--accepts`; `accepted` and `reaccepted` | ruled |
| The copy the act records | `docs/archive/last_approved/`; called the "approval record", the "approval stamp" and the "acceptance record" | `docs/archive/last_accepted/`; acceptance record | ruled |
| The dial | `human_approval_through` | `operator_accepts_through` | ruled |
| The table the dial sits in | `[attestation]` | `[authority]`: it holds seven keys and one is about acceptance; its reader is already `kitlib/authority.py` | proposed |
| The work-item class that closes an acceptance window; the brief kind | `safety_class = "attestation"`; `brief = "first-approval"` | `"acceptance"`; `"first-acceptance"` | ruled |
| Names built on the old words | `is_approved`, `last_approved`, `approval-fresh`, `approval-immutable`, `_unattested_rows`, card id `<row>-attest`; 158 names with `approv` and 73 with `attest` in the scripts | likewise | ruled |
| The script-written record that checks passed | "bar attestation", `integrate.py attest --bar review`, `BarAttestation`, `bar_attestation`, `review_attestation`, `refresh_attestation`, log phase `ATTEST` | passed-checks record, `integrate.py record-checks --checks commit`, `PassedChecks`, phase `CHECKS` | ruled; the verb is proposed |
| The requirement field naming the method | `verification` | `verification_method` | ruled |
| The method that rests on someone's word | `Attest`, `ATTESTED_METHODS`, `attested_verified`, "mechanized / demonstrated / attested", `attested-by=` | `Vouch`, `VOUCHED_METHODS`, `vouched_verified`, "mechanized / demonstrated / vouched", `vouched-by=` | ruled |
| A worker's claim, and the plain verb | "does not attest the work" | claims, records, states | proposed |
| The constant naming the retired dial key | `LEGACY_ATTESTATION_KEY` | `LEGACY_DIAL_KEY`, which already exists | proposed |

Test cases have their own free-text `method` column, describing what the test
does. It is not the method field above and is left alone.

### §4.3 Owner and human become operator

| The thing | Today | New | State |
|---|---|---|---|
| The role | owner; `owner-ruled`, `owner-held`, `owner-only`, `pending-owner-actions`, `owner_cards`, `OWNER_ONLY_PATHS`, `{{OWNER_PROMPT}}`, "HELD FOR THE OWNER" | operator; `operator-ruled`, `operator-held`, and so on | ruled |
| Its verdict on a delegated decision | `owner = "confirmed"` or `"overruled"`, `OWNER_KEY`, `OWNER_VALUES`, `owner_state` | `operator = …`, `OPERATOR_KEY`, `OPERATOR_VALUES`, `operator_state` | ruled |
| Who holds the act on a rung | `human_held`, `human_holds`, `human_approves`, `human_approves_spine`; the mode `human-held`, against `loop-held`; `HUMAN-HELD` | `operator_held`, `operator_holds`, `operator_accepts`, `operator_accepts_spine`; `operator-held`; `OPERATOR-HELD` | ruled |
| Escalation: stop or page | `EXIT_NEEDS_HUMAN` (7), `NEEDS-HUMAN`, `PAGE-HUMAN`, `page-human`, `page_human()`, `stop-needs-human` | `EXIT_NEEDS_OPERATOR` (still 7), `NEEDS-OPERATOR`, `PAGE-OPERATOR`, `page-operator`, `page_operator()`, `stop-needs-operator` | ruled |
| Push authority | `push = "human"` | `push = "operator"` | ruled |
| The status file's list of asks | `Needs <human>`, `human-owed` | `Needs <operator>`, `operator-owed` | ruled |
| The notes file | `OWNER_SCRATCHPAD.md` and its template | `OPERATOR_SCRATCHPAD.md`; the header still says it holds a person's notes and that sessions do not read it | ruled |
| The launcher's override note | `(human-set)` | `(operator-set)` | proposed |
| The stakeholder in this repository's spine | `STK-01` "Owner" | "Operator"; an accepted row, so an amendment | proposed |
| Citations of past rulings in live code and prose, about 330 | "owner ruling D-8", "(owner, 2026-10-14)" | "operator ruling"; records keep their words | proposed |
| A judged commit as against a scripted one; trunk as against a lane | "the human path", "a human trunk commit" | "a reviewed commit", "a trunk commit". Not "operator": the code says a session is expected here | proposed |

What keeps its word:

| Word | Where it stays | Why | State |
|---|---|---|---|
| human | the scratchpad's header; the definition of `Vouch`; the log's `Human` column; the asset provenance value `human-made` | prose and labels that state an intent or an origin; none controls anything | ruled |
| human | the release checklist's "Human-verified requirements" and "needs a human to exercise the real product" | the same reason | proposed |
| human | `human-readable`, `humanized` | plain English | |
| owner | the `owner` key on interface rows (258 here), `seam_owner`, `owner_files`, `OWNER-EXACT` | the providing side of an interface, a schema key ruled earlier (OI-67) | |
| owner | a lock or claim holder, the single home of a rule, the def that owns a docstring, the accountable hat, `-> @owner` on a finding line | ordinary English | |
| owner | `OWNER/REPO` in clone URLs; the licence | external terms | |

### §4.4 Words that were already taken

"Accept" must now mean one thing, so its other named uses move. "Operator"
gains a meaning the kit's frame and templates used differently.

| Existing meaning | Today | Becomes | State |
|---|---|---|---|
| A script recorded that the adjudicator's verdict parsed | "accepted verdict", `outcome = accepted`, `accepted_at`, `accepted_identities`, `unaccepted_refusal` | "recorded verdict", `outcome = recorded`, `recorded_at`, `recorded_identities`, `unrecorded_refusal` | moving is ruled; the names are proposed |
| The final read at release | "Acceptance" in `LOG.template.md` and `PROCESS.md` | "final read"; the dial is already `final_review` | ruled |
| Merge admission | "never an accept path", "accepted-on-train" | "admit", "admitted" | proposed |
| Acceptance criteria, acceptance, acceptance rule | the registry columns `acceptance_criteria`, `acceptance`, `acceptance_rule` | unchanged: standard requirement terms, stored in every adopter | ruled |
| Accepted risk | the column `accepted_risk` | unchanged: the same act accepts it | proposed |
| The acceptance record | `acceptance_record.py` | unchanged, and now its only name | ruled |
| Acceptor | the gate-advance skill; labels in `docs/gate-policy.md` | unchanged: the operator or the adjudicator | proposed |
| Whoever runs the kit's tools | "operator override", `operator-notes` | unchanged: the same role | proposed |
| The party in this repository's frame | `EXT-006` "Human operator", the party behind all four stakeholders | "Person"; an accepted row, so an amendment | proposed |
| A stakeholder of the adopter's product | "operator" in `stakeholder-needs.template.toml`, `STATUS.template.md` and the hats' "operator time" | "product operator" | proposed |
| A sub-agent that "judges nothing" | "a Claude operator sub-agent" in the coordinator's recipes | reword | proposed |

About a fifth of the code's uses of "accept" are plain English ("the parser
accepts both forms"). Reword the ones a reader could take for the act.

### §4.5 Bar and red: the earlier drafts

Drafted by the first session and not yet ruled, apart from the passed-checks
record in §4.1, which replaces its first entry. The two words name more
things than the Checks section covers: scripts and tests hold 219 distinct
names carrying "bar" or "red", 2,709 occurrences. Below is one draft for each
remaining thing. `Alternatives` lists other names considered. The drafts name
other entries in plain words; link them when they go into the glossary.

#### §4.5.1 failed-checks record

> The two header lines a build's session log carries when its
> commit checks failed: the build commit they refused and a
> one-line summary. The commit-check failure cap
> counts these since the last passed-checks record. Formerly the "red record";
> **failed-checks record** is kept.

- Renames: headers `# bar-red:` and `# bar-summary:` to `# checks-failed:`
  and `# checks-summary:`; `red_rounds` to `failed_rounds`; `red_record`,
  `format_red_record`, `parse_red_record` likewise; `EXIT_RED_CAP` to
  `EXIT_CHECK_FAILURE_CAP`; `red_cap_check` to `failure_cap_check`.
- Alternatives: "failure record" is shorter but does not say what failed.

Operator: as drafted, 2026-11-11 (D16). "Test" was considered and refused:
the checks include lints, the record already has a `tests=` field, and `Test`
is a verification method.

#### §4.5.2 landing stage

> The stage a work item pins its landing checks to. A row
> claimed to deliver evidence at a stage is checked at that stage even if the
> repository's derived stage moves while its lane is in flight. Declared in
> the work item as `landing_stage`. Formerly the item's `bar`; **landing
> stage** is kept.

- Renames: the work-item key `bar` to `landing_stage`; `WI_BARS`,
  `_lane_bar_directives`, `_declared_bar_or_refusal`, `bar_gate`.
- Scope: no live work item declares the key; 31 archived ones do, with values
  `DevStg-Reqs`, `DevStg-Tests`, `DevStg-Impl`. The migrator rewrites
  the key in those files, and no reader for `bar` is kept (D3).
- Alternatives: `checks_stage`; `gate`, which the kit already uses for the
  stage gates and would overload.

Operator:

#### §4.5.3 evidence gap

> A test case that is not accepted although every requirement it verifies is
> cited by a work item recorded done: the work is closed and its evidence is
> not. The gap census names each one, and the landing mints an adjudication
> row for it. Formerly a "red TC"; **evidence gap** is kept.

- Renames: `red_tc_census`, `parse_red_tc`, `red_tc_values`,
  `RED_TC_PREFIX`, `ADJUDICATE_RED_TC`, `_TC_NOT_RED`.
- Why this word: the census that finds them is already the gap census.
- Alternatives: "unproven test case"; "unverified test case", which collides
  with the row status Verified.

Operator:

#### §4.5.4 commit-check settings (the reader of the two declared values)

Not a glossary term: a code name. `kitlib/red_mark.py` holds the reader for
the commit checks' suite and the expected-failure marker, and the marker's
counting rules.

- Proposed: module `kitlib/expected_failure.py`; class `Bars` to
  `CommitCheckSettings`, with fields `commit_checks` and `marker` in place of
  `review` and `red_mark`; `read_bars` to `read_commit_check_settings`. In
  `kitlib/config.py`, `red_rounds_max()` to `commit_check_failure_cap()`.
- Registry: LLR-368 binds the module and these symbols; LLR-343 binds
  `red_rounds_max`.

Operator:

#### §4.5.5 stage, not bar, for the retired dial

Not a new term. The kit once had a "bar" dial for stage thresholds and
retired it for the stage ladder (`DevStg-*`). The word survives in readers of
the retired spelling and in a few live names.

- Proposed: live names say stage or rung (`sr_bar` and `sn_bar` to `sr_stage`
  and `sn_stage`, `maturity_bar` to `maturity_stage`, `stage_to_bar` and
  `normalize_bar` likewise, the dashboard's "rung bar" to "rung strip" if it
  names the graphic). Names that exist only to read the retired spelling keep
  the retired word and say so (`_LEGACY_BAR_THRESHOLD`, `_RETIRED_BARS`,
  `RETIRED_STAGE_ALIASES`, the `DevBar-*` aliases).
- Needs a look by whoever does it: `trace.py` and `kitlib/config.py`, to
  confirm each `*_bar` name is the stage and not something else.

Operator:

#### §4.5.6 failed, not red, in running prose

Not a glossary term: a usage rule for the glossary's preamble.

> A run of checks **passes** or **fails**. "Red" and "green" are not used for
> either, except once, where `process.md` names the red, green, refactor
> cycle.

- Applies to prose, comments and messages. For test names see D4.

Operator:

#### §4.5.7 minimum or standard, not bar, for a threshold

Not a glossary term. Where "bar" is plain English for a threshold ("the
shipped bar", "raise the bar"), write the specific thing: minimum, standard,
level. 109 lines of shipped prose hold the bare word; 32 are in the
coordinator's recipes (see B8, which may remove them).

Operator:

## §5. Doing the migration

Cut a new branch from this one.

**Order.** Glossary first. Then §4.4, because it frees the words the others
reuse; then §4.2, §4.3 and §4.5, one concept at a time. Within a concept,
stored values before names that only code sees. Run the checks below after
each concept, not at the end.

**No compatibility readers (D3).** The core scripts read the new spellings
only. Getting an older repository there has four parts.

*1. A migrator for stored values.* One purpose-built script that rewrites the
values below in place and is safe to run twice. It ships, so that an adopter's
re-sync runs it, and it is the one home for knowledge of the old spellings.
The kit has three precedents: `bootstrap.py --migrate-config`,
`migrate_carrier.py` and `migrate_decisions.py`. Decide whether to extend one
or add a fourth. `bootstrap.py` may not import kit modules, which is why it
carries its own copies of literals.

| Stored value | Becomes | Where it is stored |
|---|---|---|
| `status = "Approved"` | `"Accepted"` | every registry: 904 rows here, and four adopters |
| the column `verification` (CSV `Verification`) | `verification_method` | system requirements |
| the method `Attest` | `Vouch` | 18 cells in four adopters, none here |
| `[attestation]`, `human_approval_through` | `[authority]`, `operator_accepts_through` | `docs/process.toml`; only the kit's own checkouts have one |
| `push = "human"` | `push = "operator"` | `docs/process.toml`; the one-word file `docs/push-policy` in three adopters |
| `owner = "confirmed"` or `"overruled"` | `operator = …` | `docs/decisions/*.toml`: 52 keys in 16 files here |
| `approved`, `reattested` | `accepted`, `reaccepted` | `docs/archive/last_approved/acts.toml`: 181 entries |
| `docs/archive/last_approved/` | `docs/archive/last_accepted/` | the directory |
| `OWNER_SCRATCHPAD.md` | `OPERATOR_SCRATCHPAD.md` | the root; the kit's checkouts and gilbert |
| `Needs <human>` | `Needs <operator>` | `docs/status.md`; no adopter has the heading yet |
| `safety_class = "attestation"`, `brief = "first-approval"`, `bar = "DevStg-*"` | `"acceptance"`, `"first-acceptance"`, `landing_stage = …` | work-item front matter: 1, 36 and 31 files, all archived |
| `outcome = accepted` | `outcome = recorded` | `*.requested` files under `docs/reviews/` |
| `{{OWNER_PROMPT}}` | `{{OPERATOR_PROMPT}}` | prompt templates, and any adopter's override |

All ten adopters on this machine are on July kits (`VOCABULARY.md` §8). They
hold none of the intermediate spellings, but they do hold the one-word policy
files, `G1` to `G3` and `gates =`, which `bootstrap.py --migrate-config` folds
today. The migrator writes the new names when it folds them.

The last four rows are records. Migrate a record only if a current script
still reads it; leave the rest as written.

*2. A detector that refuses.* `check_vocab.py` is the kit's vocabulary check
and already refuses `G1`, `DevBar-*` and every form of "ratify". Add the old
stored spellings, so that a repository that skipped the migrator fails with
the fix named and does not read a key as absent. The case that matters most:
a scratchpad left under its old name silently loses the protections that seven
scripts give it by name. Three things to know about the check:

- It is one regex on word boundaries, and an underscore is a word character,
  so it does not fire inside a snake-case name. `human_approval_through` needs
  its own pattern.
- "Owner" and "human" cannot be refused outright, because some senses stay
  (§4.3). Refuse the compounds.
- Records are exempt through `EXEMPT_GLOBS`, and stay so.

*3. A clean cut for git history.* The passed-checks record and the
failed-checks headers live in commit messages and lane logs, which no
migration reaches. Write and read the new form only. A lane cut before the
change re-runs its commit checks once and gets a record in the new form. One
lane worktree existed on 2026-11-11 (`wi-902`). Every reader found reads a
lane against its base, and none walks landed history (`VOCABULARY.md` §3);
confirm that before relying on it. The kit made the same cut when the trailer
gained `bar=`.

*4. The session, for prose.* Prose, comments, messages and the text of
accepted rows are changed by the session, by concept, reading every changed
line (trap 10). §4.3 and §4.4 say which uses stay.

**The re-sync entry** tells an adopter's session to run the migrator, what the
detector refuses until it has, and which edits are left to it: its own prose,
its own prompt overrides, and the amendments to its accepted rows. It is the
only place an adopter learns the path, so it carries the old-to-new tables of
§4.

**Not traced. Do these before building the migrator.**

- How the `held-status` step (`check.py`, `held_status.py`) treats a commit
  that moves every status cell from `Approved` to `Accepted`. The migrator has
  to pass it or be recognised by it.
- Whether anything guards `acts.toml` against a rewrite. A search of
  `check.py` and `check_trajectory.py` found nothing; the file's own header
  says do not edit.
- Whether renaming `last_approved/` disturbs the comparisons made against it.
- Which records a current script still reads: archived work items, and the
  `*.requested` files.
- The dated briefs in `docs/ratify/` are immutable by check
  (`approval-immutable`). Leave them and the directory name alone;
  `CURRENT.md` regenerates.

**Registry edits the renames force.**

- Design rows that bind a renamed module or symbol. For bar and red there are
  11: LLR-152, 154, 159, 167, 188, 207, 231, 341, 343, 344, 368. Those binding
  the names of §4.2 to §4.4 are not listed yet; `trace.py --strict` names each
  one when its symbol stops binding. These are traced cells; editing them is
  not a text amendment.
- Evidence cells: every renamed test function or file (D4). Up to 55 cells
  cite a test named for attest, approve, owner or human.
- The accepted rows of D5. For bar and red: SN-005, SR-221, SR-241, LLR-207,
  260, 291, 343, 344, 368, TC-132, 375, 376, 417.
- Baselines keyed by function name: `docs/complexity-baseline` and the
  module-size ratchet (trap 2) are re-keyed in the same change.

**Checks to run after each concept.** All from the worktree root.

```
python project-trajectory/scripts/trace.py --strict
python project-trajectory/scripts/check_trajectory.py --strict
python project-trajectory/scripts/check_docs.py --root . --stale
python scripts/check_resync.py
python project-trajectory/scripts/check.py --path-triggered
python -m ruff format --check project-trajectory/scripts tests
python -m ruff check project-trajectory/scripts tests
python -m pytest -q -p no:cacheprovider -n 6 <the modules the change names>
```

Then the unfiltered suite once at the end (33 to 45 minutes on this box).

**Traps the first session walked into.** Each cost a failed run.

1. *One-home tests.* `test_stack_profile.py` fails any script that parses
   `docs/stack.ini` itself. Use `kitlib.config.read_stack_ini`.
2. *Exact line counts.* `test_module_size_ratchet.py` pins the code-line
   count of nine modules, in both directions. A reworded message that wraps
   onto a new line fails it. Keep such edits line-neutral; do not re-stamp.
3. *Tags and evidence must agree.* A new test carrying `Implements: TC-NNN`
   must be added to that test case's evidence cell, or
   `check_trajectory.py --strict` refuses.
4. *Byte budgets.* `CLAUDE.md` and three shipped files have stamped sizes in
   `skills/byte-budget-guard/SKILL.md`. Any edit to them needs the table
   re-stamped, and the skill's own row with it.
5. *Skill mirrors.* `.claude/skills` and `.agents/skills` are byte-identical
   copies of `project-trajectory/skills`. Copy after every edit.
6. *Dogfooded copies.* `docs/specs/README.md` must match its shipped
   template. A sweep that skips `docs/specs` breaks `test_dogfood_sync.py`.
7. *The prompt catalogue.* Editing a prompt template makes
   `project-trajectory/prompts/CATALOG.md` stale. Regenerate with
   `gen_prompt_catalog.py`; the hook checks it on every commit.
8. *A re-sync entry is required* for any change under `project-trajectory/`,
   anchored `[since <trunk base sha>]`. `check_resync.py` refuses without it.
9. *A `[product]` key cannot be appended.* Insert it under the existing
   header. Appended after another section it parses and reads as undeclared.
10. *Automated word replacement breaks grammar and over-reaches.* It turned
    "the docs/gate BAR axis" into "CHECKS axis", which was the retired dial
    and not a check. Replace by concept, and read every changed line.
11. *The box is shared.* Other projects' agent sessions run on it. The same
    test tier read 234 s and 417 s minutes apart. Never run two timing runs
    at once; prefer counts and CPU-seconds.

Traps found by the second session, not yet walked into:

12. *The new words were already in use.* "Accept" has ten named meanings and
    "operator" five (`VOCABULARY.md` §6). Free a word before reusing it:
    `_unattested_rows` cannot become `_unaccepted_rows` while
    `unaccepted_refusal` still means a verdict.
13. *"Owner" and "human" each keep some senses* (§4.3). A sweep of either
    word is wrong.
14. *Two settings change meaning, not only spelling.* `push = "operator"`
    lets a delegated session push, where `"human"` excluded even an attended
    one; the launcher's override note likewise. The operator ruled this (§2).
    Reword the prose around each (`bootstrap.py`, `process.toml.template`,
    `subagent_gate.py`).
15. *The method's definition has two loose ends.* `Manual` is defined as "a
    human procedure that isn't `Attest`", and `bootstrap.py` scaffolds an
    `LLM-Attest` line that contradicts the separation from `Critique`. Fix
    both in the same change.
16. *A row can read as "criteria met".* `status = "Accepted"` sits beside
    `acceptance_criteria` on the same row. The glossary entry has to say that
    accepting a row says nothing about tests passing.

## §6. Functional changes, in order of value

These come from the review (README §§3, 7, 9, 11) and from the operator's
feedback since. None is made on this branch. Figures marked (reviewer) were
produced by a reviewing sub-agent and spot-checked, not recomputed.

**B1. Make the inner loop cheap and the landing deep.** The operator's first
complaint. Set `[required-checks] commit = "iterate"`. Give `landing` a
reader and run the unfiltered suite once per landing, on the staged squash.
Replace the hand-landing line in the coordinator recipes that runs the smoke
tier. Evidence: 69% of 1,489 lane commits change no source or test file and
still run 3,499 tests; a median of 10 attestations per lane (reviewer); for
the commits that do run tests, the selection's median is 111 test functions.
Depends on D6, D7. Proposed prose: README §8.

**B2. Stop one lint re-reading history.** `check_trajectory.py --strict`
takes two to five minutes; with its walk over every loop commit stubbed and
one scan computed once it took 12.9 s. The commit hook runs the same script,
so each commit pays twice. Cache the per-commit answer by commit id, or move
the report to the audit. Both files are shipped and one is in the line-count
ratchet. README §7. Until this lands, B1 saves less than it should.

**B3. Retire the smoke tier's bookkeeping.** Once commits run a selection,
the in-process tier is only the fallback. Remove `SLOW_MODULES`, `max-tests`,
`[smoke-budget]` and its roughly 900 lines of stamp history, and the nested
whole-tree collection inside `test_smoke_budget.py`. 73 commits have changed
`max-tests`.

**B4. Build a scaffold once per worker.** The `scaffold` fixture runs
`bootstrap.py` as a subprocess for each of about 500 tests, 4 to 5 s each on
this box. Copy a prebuilt one. The largest single cut to the landing checks,
and it also shrinks the canary set's 30 to 40 s.

**B5. Change the prose that only adds tests.** Nothing in the method merges
or retires a test. Proposed wording for six passages and one new rule is in
README §8. Operator ruling needed: reviewers will read it as weakening.

**B6. CI.** Jobs have a 20-minute timeout for a suite that takes 33 minutes or
more locally, and the root conftest halves the worker count even with the CPU cap
off. A review of 2026-11-05 reports no green run since 2026-10-14; this
session could not check, since `gh` is not installed. Check the Actions tab
first. Then run the iterate checks on push and the matrix nightly or on a
pull request, as the shipped template already does.

**B7. Scope the commit hook by what changed.** It runs 34 checks and about
41 interpreter launches on every commit, records-only ones included
(reviewer). `check.py` already has the `paths =` machinery.

**B8. Remove the overnight runner.** The operator's view: it was only ever for
long-running changes to this repository, and a dedicated session started
outside the repository root does that better.

| Set | What | Size |
|---|---|---|
| The launcher | `scripts/coordinator/overnight_legs.py`, `headless-leg.md`, `coordinator-relaunch.{cmd,sh}` | 773 lines; 40 test functions in 3 test files (1,217 lines) |
| The coordinator's other repo-local tools | the rest of `scripts/coordinator/`: `codex_call.py` and five small scripts | about 1,300 lines; 29 test functions in 3 test files |
| The coordinator's shipped guard | `coordinator_guard.py`, `kitlib/guard_hooks.py` | 2,036 lines; 85 test functions in 2 test files |
| Its prose | the `coordinator-cycle` skill and its recipes, `kit-builder.md` | 22,800 words; 7 test files pin it |

  The launcher is mentioned in the system requirements, the design rows and
  the test cases (four lines between them), in `docs/runtime-flows.md`,
  `docs/stack.ini`, `kitlib/provenance.py` (which recognises its commits)
  and four test modules besides its own. Removing it retires those rows,
  which is an amendment. Not sized here, because it was not traced: whether
  the session, adjudication and usage modules (`session_service.py`,
  `session_keep.py`, `session_adapters.py`, `adjudicate_brief.py`,
  `adjudicate_act.py`, `usage_ingest.py`; about 7,700 lines and 400 test
  functions) serve only this coordinator or the shipped loop too. That
  question is B9's.

**B9. Separate the kit from the machinery that builds it.** About half of
`project-trajectory/scripts` by line count is the unattended multi-agent
station and its own record-keeping, and 127 of 130 modules ship to every
adopter in one flat list (reviewer). An adopter who wants the three stated
goals needs none of it. Only 25 import edges run from the traceability core
into it (reviewer). Cut those and give bootstrap a real install profile.
This is a smaller decision than open item OI-130 and worth more: the
re-score there shows one partition winning under every objective, and none
addresses the 19 duplicated policy behaviours.

**B10. End the standing pause.** `docs/work/pause` is a one-day review hold
from 2026-09-04. Every claim since costs three commits.

**B11. Stop committing the dashboard.** `PROJECT_STATE.html` is in 2,041 of
4,717 commits, and about 95% of the files under `docs/` are records that the
link checks re-read on every run (reviewer).

**B12. Give the ratchets headroom or delete them.** The line-count ratchet
is 2,107 lines for 4 tests and has been edited in 410 commits (reviewer). It
taxes every edit and its baselines rose anyway.

**B13. Fix what the kit says about itself.** `CLAUDE.md` gives the suite as
"~10 min" (it is 33 or more) and says the lane refresh runs the full checks
in the merge slot (the lane history holds 367 commit attestations and no
landing one). `docs/gate-policy.md` contradicts `docs/process.toml` on the
approval dial (reviewer). "No commit bypasses" the hooks, while three shipped
scripts commit without them (reviewer).

**B14. Push.** Trunk is 16 commits ahead of its remote. The unsquashed lane
history is 4,586 commits ahead of its remote, whose tip is 2026-10-05. The
machine crashed on 2026-11-07. `origin/HEAD` is still `main`, last touched
2026-07-17.

## §7. Getting the template onto other repositories

The operator's goal is a template that forces interlinked documentation and
layered architecture, with hooks matched to need. The order below is this
session's suggestion for reaching a kit that can be applied elsewhere.

1. **Vocabulary** (§4, §5), so that what an adopter reads is consistent.
2. **Cheap inner loop** (B1, B2), so that working in the kit is not the
   bottleneck for everything after.
3. **Core and station apart** (B9, B8), so that an adopter installs the part
   the vision describes. This is the step that decides how much of the rest
   an adopter ever sees.
4. **Two of the three goals are the least enforced today** (README §11).
   Layering is "no import cycles" plus an ordering among five modules, and
   two of its instruments cannot see inside packages. The commit hook
   ignores the stage ladder, and formatting blocks from the first commit
   while lint and tests arrive at the seventh rung of eight. Decide what the
   kit should enforce for an adopter on day one, and make the hook do that.
5. **A first-day pass on a clean machine.** A review of 2026-11-05 simulated
   one: 183 minutes of required reading, a documented setup command that
   fails on Ubuntu, and four refused commits (reviewer, not re-run here).
6. **Then re-sync the pilots.** Two downstream repositories are evident,
   `gilbert` and `FileBackup`; FileBackup's re-sync has been owed since
   2026-10-02 and is blocked on known kit defects (reviewer).

Operator, on this order:

## §8. For the next session

- Start outside the repository root, as both sessions did, unless the
  operator says otherwise. The repository's `CLAUDE.md` and skills describe a
  workflow the operator has chosen not to use for this work.
- Never read `OWNER_SCRATCHPAD.md`, under that name or as
  `OPERATOR_SCRATCHPAD.md` once it is renamed. It holds the operator's private
  notes.
- Work in a worktree. Leave the primary checkout alone.
- Commit only when the operator asks. The operator allowed bypassing the hook
  on this maintenance branch; confirm before doing the same on the next one.
- The operator's decisions are on the `Operator:` lines above. An empty line
  means undecided: ask, do not assume the recommendation.
- Use the new words with the operator and in anything new you write. The
  operator does not want compatibility code in the core tooling: do not
  propose alias readers.
- This file, `README.md` and `VOCABULARY.md` are the whole record. The
  measurements behind them were taken in a temporary directory and are not
  kept.

## §9. The third session: the migration begun

Written 2026-11-11 by the session that started the migration. It works in
`C:\Projects\ai-template-wt-vocabulary` on `maint/vocabulary`. Nothing there is
committed (D14).

### §9.1 What is done

| Step | State |
|---|---|
| The five glossary entries of §4.1 | written into `project-trajectory/GLOSSARY.md`: a "Human" rule in the preamble, **operator** under Roles, a new Rows section with **accept** and **Vouch**, **passed-checks record** under Checks. The older entries still use the old words; each is swept with its concept |
| §4.4, "recorded verdict" | done. `kitlib.sitting.accepted` and its four siblings are `recorded…`; the outcome value is `recorded`; prose, tests and three bound symbol cells follow. `adjudicate_act._accepted` became `_recorded_verdict`, because `_recorded` was already another function there (trap 12 in practice) |
| §4.4, final read, merge admission, EXT-006, product operator, the sub-agent | done by hand, 21 edits. The final read's label is "Final read"; a merge is "admitted" and a trailer is "never an admission path"; EXT-006 is "Person" |
| The migrator | `project-trajectory/scripts/migrate_vocabulary.py`, with its first step: `outcome = accepted` to `recorded` in every `*.requested` binding. Run on this repository: 202 files rewritten, 2 `failed` left, a second run finds nothing. It has no tests, no manifest row and no spine rows yet (§9.4) |
| Checks after §4.4 | `run.cmd iterate` without its lints, over the whole change: 3,225 passed, 66 skipped, 3 failed in 25 minutes. Two failures were this session's own doing (it edited a script during the run; see the traps below) and pass when re-run. The third was `docs/stage`, stale after the registry edits; regenerated, and it passes. `ruff`, `trace.py --strict`, `check_docs.py --stale`, `check_resync.py`: clean. `check_trajectory.py --strict`: one error, the migrator is in no component (§9.4) |
| §4.2, the method and its field | applied: `Attest` is `Vouch`, `verification` is `verification_method` (row key and CSV header `VerificationMethod`). 420 lines by rule in 88 files, then 45 sentences by hand. Trap 15 is closed: `Manual` is "a procedure a person carries out, whose result another could repeat", and "LLM-Attest" is a delegated `Vouch`. The migrator has the registry step for both carriers, with 16 tests, and has rewritten the record's copy of the system requirements here. `trace.py --strict` is clean. Its 56 test modules were running when this was written |

| §4.2 and §4.3, the dial | applied: `[attestation]` is `[authority]`, `human_approval_through` is `operator_accepts_through`, `LEGACY_ATTESTATION_KEY` is `LEGACY_DIAL_KEY`. 290 lines by rule in 73 files. The readers of older spellings (the 0-4 ordinal, the older key name, the gate-policy enum) still read them, now inside the renamed table, until D11's change. The note in the policy template that explained why the key was not called "attest level" is removed. "attestation" as a work-item safety class is untouched: it moves with the act. Its 82 test modules and `check_trajectory.py --strict` were running when this was written |
| The migrator, continued | a third step: the policy file's table and dial key, by line edit proved by a second parse (an inline or dotted table is refused, not guessed). 22 tests. Its manifest row is in. Its spine rows are written as `Drafted`: SR-247, LLR-369, TC-427, component CMP-006, with the id watermark raised. `docs/stage` now reads settled `DevStg-Impl`, live `DevStg-Reqs`, which is what three drafted rows in phase 6 mean; the operator's acceptance of them is owed (D18) |

Traps this session walked into:

17. *A script edited while tests run fails them.* The loop under test notices
    that a file under `project-trajectory/scripts` changed after it was
    imported, and stops with exit 11 ("coordinator Python changed"). Editing
    any script there during a run, even one no test imports, fails whichever
    loop tests are in flight.
18. *`docs/stage` carries a fingerprint of the registries.* Any registry edit
    stales it and `test_this_repo_s_committed_stage_is_current` fails. Run
    `derive_stage.py` after each concept; the stage itself has not moved.
19. *A lowercase key hides beside the capitalised one.* The TOML key and the
    row key of one field are spelled differently (`verification`,
    `Verification`). A rule written for one misses the other: three sites here
    (`kitlib/spine.py`, `spine_carrier.py`, one test).
20. *A name inside a Python string literal has no word edge.* In
    `"...\nverification = ..."` the letter before the name is the `n` of the
    escape, and a rule anchored on a line start or a word boundary misses it.
    Eight fixtures were missed that way. `vapply.py` now counts an escape as
    an edge; a regex rule has to allow for it itself.
21. *A field name has more forms than its quoted one.* The column also
    appears as a Python keyword argument (`dict(row, Verification="Test")`),
    in the messages that name it (`has Verification='x'`) and in prose
    (`Verification=Critique`). Eleven tests failed before these were found.
22. *Dogfooded copies sit under exempt directories.* `docs/rubrics/README.md`
    and `docs/rubrics/rubric-000.md` must equal their templates byte for byte,
    and no sweep reaches `docs/rubrics`. Re-copy after a template changes.
23. *The skills index is generated.* `INDEX.csv` comes from each `SKILL.md`'s
    front matter (`gen_skills_index.py --skills project-trajectory/skills`).
    Edit the front matter, then regenerate; a hand edit of the index is undone.
24. *The rename tools list files with `git ls-files`.* A new file is invisible
    to them until `git add -N` marks it.
25. *A shorter name can shrink a ratcheted module.* `[authority]` let the
    formatter join one three-line call in `bootstrap.py`, and the exact
    line-count ratchet fails in that direction too (D17).

One reading of §4.4 was changed. "Operator time" in the performance hat's
question is the operator's own time, beside "provider usage": the cost of
running the kit, not a stakeholder of an adopter's product. It is left as it
is. "Product operator" was applied to the two templates that list whom a
product serves.

### §9.2 What the traces found

Three read-only traces answered the questions under "Not traced" in §5.

**The passed-checks record can be cut cleanly.** Every reader of the trailer
reads one lane's own commits, or walks first-parent from its tip for at most
64 steps. None reads landed history: no squash landing on trunk carries the
trailer, and no census or dashboard reads it. No lane is in flight (`wi-902`
closed partial on 2026-10-20). Two things follow.

- The trailer and the failed-checks headers move in one change. If
  `Bar-Green:` is renamed while `# bar-red:` is still read, a lane's old
  passing records stop resetting its failure count, and every old failure
  counts again. Renamed together, both become unreadable and the count restarts
  at zero. So §4.5.1 has to be ruled with the passed-checks record (D16).
- `agent_common.write_session_log` keeps its own list of the header keys. It
  must change with `format_red_record`, or the record is dropped silently.

**The acceptance record cannot move in one commit, and cannot pass the hook.**

- The record is nine files under `docs/archive/last_approved/`: a README, the
  ledger `acts.toml` (181 entries, no digests or commit ids) and seven
  byte-for-byte copies of registries. Drift is a cell-by-cell comparison of a
  live row with its copy, `status` and the traced cells left out.
- *Text then act.* A commit that touches the record may change no cell but
  `status` in the spine tiers. So the rewording of rows is one commit and the
  move of the record is the next.
- *The mirror rule.* A copy written in a commit must equal its live file in
  that commit, and renaming the directory writes all seven. So the migration
  leaves every copy equal to live. That is how D5 is carried out, with no act
  recorded. It also absorbs any drift that was already pending (D13).
- *The added-entry rule* compares the staged ledger with the ledger at HEAD.
  After the rename there is none at that path, so all 181 entries read as new.
- These three are commit-time rules. The migration commit is refused by them
  whatever is done, short of readers for the old path, which D3 rules out. It
  is committed with the hook bypassed, and the standing checks must then be
  clean on the committed tree. An adopter meets the same refusal, so the
  re-sync entry has to say so.
- `intake.py snapshot` must not be run between the code rename and the record
  move. It would read every row as never accepted and write a 904-row act.
- Stored digests go stale. 18 observation records under
  `docs/test/observations/` digest a row with its `status`, so the status
  rename stales them. 29 bindings hold a digest of a row's accepted text, so
  rewording stales those; that matters only to an act not yet taken.
- Readers of history that will see the cut: `check_test_first.py` re-dates
  every first acceptance to the migration commit (a warning unless strict);
  `loop_held_status_findings` judges each old loop commit by the dial in its
  own tree, and with the dial renamed reads all 235 as most-held (advisory
  noise, and the walk B2 wants gone).

**Which old records are still read.**

| Record | Read by a current script | So |
|---|---|---|
| `outcome = accepted` in 202 bindings | yes: two readers sweep every binding, and a test reads a real one | migrated (done) |
| `owner =` in `docs/decisions` (52 keys, 16 files) | yes: every record is read | migrate. The commit that does it trips `ruling-sync`, which reads both trees through the key and sees three overrules as new |
| `bar` inside the `## Dispositions` blocks of 15 archived work items | yes: a bare `intake.py sweep` parses them and refuses an unknown key | migrate with §4.5.2 |
| `bar` in the front matter of 16 archived work items | no | leave |
| `safety_class = "attestation"` (1 file), `brief = "first-approval"` (36 files), archived | no | leave |
| `"first-approval"` in `[adjudicator] retain_for`, `docs/process.toml` | yes, and the census missed it: an unmigrated value silently stops retention | migrate |
| The kind `first-approval` in 77 bindings and 76 verdict files; the ruling `APPROVE` in those verdicts | only for an act not yet taken | leave as written (D15) |
| Dated briefs in `docs/ratify/` | no; a check refuses any edit to them | leave. Only `CURRENT.md` and one golden file follow the generator's wording |
| `Needs <human>` | warn-only, and this repository's status file has no such heading | the scaffold's bullet and the reader's pattern change; nothing stored here |

### §9.3 The order for §4.2 and §4.3, revised

1. The method and its field: `Attest` to `Vouch`, `verification` to
   `verification_method` (row key `VerificationMethod`, which is also the CSV
   header). Applied (§9.1). The CSV carrier is live (the tests write CSV
   registries), so the migrator renames the header and the two values in CSV
   and TOML alike.
2. The dial: `[attestation]` to `[authority]`, `human_approval_through` to
   `operator_accepts_through`. Applied (§9.1). The readers of older spellings
   stay where they are, reading inside the renamed table, until D11's change;
   `bootstrap.py --migrate-config` writes the new names when it folds them.
3. The passed-checks record, with §4.5.1 once it is ruled.
4. Re-attest to re-accept, then approve and attest to accept, with `status`
   and the record moved by the migrator as its last step.
5. Owner and human to operator.

About 22,000 occurrences of the four old stems sit on the live surface, in 674
files. Identifiers are renamed by exact token and prose by phrase rules; every
changed line is read before the next concept starts.

### §9.4 Owed before the branch is finished

- The migrator's remaining steps: `status` and the acceptance record, the
  ledger keys, `push`, `retain_for`, the decisions key, the Dispositions
  blocks, the scratchpad's name. Its design row and test case grow with each.
- The re-sync entry, carrying the tables of §4 and the commit instructions of
  §9.2.
- The detector in `check_vocab.py` (§5, part 2).
- Byte budgets: `AGENTS.template.md` has 8 bytes of headroom under its cap,
  and "operator" is three bytes longer than "owner" or "human". It will need
  trimming, not only a re-stamp.
- The nine line-ratcheted modules, re-checked after `ruff format` re-wraps.
- The unfiltered suite, once.

### §9.5 Decisions raised

**D12. A reviewer's verdict on a round.** `APPROVE` is stored with two
meanings. An adjudicator's ruling on a row in a first-acceptance sitting is
the act of §4.2 and becomes `ACCEPT`. A reviewer's `VERDICT: APPROVE` or
`CHANGES-REQUESTED` on a build round or a plan is a judgement of work, not an
act on a row; it is stored in every review file and `Review-Verdict:` trailer.
Recommended: keep `APPROVE` for the review verdict and give it a glossary
entry, so that "accept" and "approve" each name one thing. Review-verdict
lines are untouched until this is ruled.
Operator: agreed 2026-11-11. The reviewer is the one approving, so `APPROVE`
stays for the review verdict, with its own glossary entry distinct from
**accept**.

**D13. The drift already pending.** `CMP-006`'s `notes` cell was amended on
2026-09-03 (WI-587) and never re-accepted. Three record copies differ from
live today: that cell, three evidence cells (traced, not drift) and the
interface rows (all `Drafted`). The migration makes every copy equal to live.
Recommended: absorb it, and have the migrator name every accepted cell it
absorbs so that the operator sees what was taken.
Operator: agreed 2026-11-11, as recommended.

**D14. Committing on `maint/vocabulary`.** Recommended: yes, with the hook
bypassed as on the last branch, in two commits (rewording, then the record),
since the kit's own rules refuse the migration otherwise (§9.2).
Operator: agreed 2026-11-11. The branch may commit with the hook bypassed.

**D15. Old first-acceptance verdicts.** Recommended: leave the verdict files
and the kind token in their bindings as written. They then read as not
recorded, which matters only to a lane in flight, and there is none.
Operator: agreed 2026-11-11.

**D16. §4.5.1 with the passed-checks record.** The seven lines of §4.5 are
still empty, and §4.5.1 cannot wait for the rest (§9.2).
Operator: §4.5.1 as drafted, 2026-11-11. The operator asked where §4.5.1 was
defined (the headings carried no § sign, so a search missed them; they do
now) and whether "Vouch" or "test" fitted better. Neither: `Vouch` replaces
only the method sense of "attest" (`VOCABULARY.md` §3, S3); the
passed-checks record replaces S1, a script's record that checks ran. §4.5.2
to §4.5.7 are still open.

**D17. The line-count ratchet.** Nine modules have their code-line count
pinned exactly. "Operator" is three characters longer than "owner" or
"human" and "acceptance" two longer than "approval", so the formatter will
re-wrap lines in all nine, and `bootstrap.py` has already shrunk by two. No
logic changes. Recommended: re-stamp the nine baselines once, at the end of
the migration, each with the reason "vocabulary migration: the formatter
re-wrapped renamed lines"; the alternative is to contort each wrapped line
back to its old count.
Operator: agreed 2026-11-11, as recommended.

**D18. Three drafted rows.** The migrator's requirement, design row and test
case (SR-247, LLR-369, TC-427) are `Drafted`. All three sit on rungs the dial
releases, so the kit would hand them to an independent adjudicator; on this
branch the operator can accept them directly. Recommended: read them once the
migrator is complete (its design row grows with each step), then accept.
Operator: agreed 2026-11-11, as recommended.

### §9.6 The tools

The inventory and rule-application scripts, and one rule file per concept, are
in `vocab-tools/` beside this file. `vapply.py RULES.py --dry --review OUT`
shows every line a rule file would change; without `--dry` it writes them. It
refuses when a new name is already in use. `hand.py EDITS.py` applies exact
hand edits and writes nothing unless every one matches. `inv.py` counts and
lists the old words on the live surface, leaving out the records named in
`common.py`. Added by the fourth session: `compact.py REVIEW` shrinks a review
file to each changed span with a little context, which is what makes a
thousand-line review readable; `article_scan.py WORD [--fix]` finds an article
left at a line end before a word that now needs "an"; `absorbed.py REGISTRY`
names the accepted cells a record copy would absorb (D13).

### §9.7 The fourth session: "human" becomes "operator"

Written 2026-11-11, later the same day. It recorded the answers to D12 to D18,
committed the work so far as checkpoint `6d8291fb6` (D14), and applied the
"human" half of §10.4.

| Step | State |
|---|---|
| Checkpoint commit | `6d8291fb6` on `maint/vocabulary`, hook bypassed: everything §9.1 lists. Not pushed |
| "Human" to "operator" | `r43a_human.py`: 1,050 lines in 157 files by rule, then `article_scan.py --fix` for 14 articles split over a line end ("needs a / operator"), then `h43a.py` (23 hand edits) and `h43b.py` (2). The role sense moves; the person sense stays (below) |
| Identifiers | `operator_held`, `operator_holds`, `operator_accepts`, `operator_accepts_spine`, `EXIT_NEEDS_OPERATOR` (still 7), `page_operator`, `NEEDS-OPERATOR`, `PAGE-OPERATOR`, `page-operator`, `stop-needs-operator`, `operator-held` / `OPERATOR-HELD`, `operator-owed`, `(operator-set)`, `Needs <operator>` with `_NEEDS_OPERATOR_RE` and `STACK_NEEDS_OPERATOR`; ten test names, and their evidence cells with them |
| The push value | `push = "operator"` everywhere it is written. Trap 14's rewording is done: the default now reads "the operator pushes, or a session they delegated the push to; never the loop, and never an agent merely asked mid-session" in the policy template, `docs/process.toml`, `PROCESS.md`, `PROCESS_OPTIONS.md`, `bootstrap.py`, the gate-advance skill, `security-review.md` and two comments |
| The migrator | a value map in the policy step, `POLICY_VALUES`: `push = "human"` to `"operator"` in `[policies]` only, by line edit proved by the re-parse; an inline table or a multi-line string is refused. 2 tests more; LLR-369, TC-427 and SR-247 extended |
| The acceptance record | the copy of `system-requirements.toml` made byte-identical to live (see below) |
| Regenerated | `docs/stage`, `prompts/CATALOG.md`, `skills/INDEX.csv`, `docs/open-items.html` (stale since the checkpoint; `gen_open_items.py --check` is a floor step) |

**Where "human" stays.** In prose that means a person as such: a reader
("rendered for a human", "readable for humans"), an observer under the human
verification methods and the release checklist, an audience beside agents
("AI agents and humans"), nobody present ("3am with no human", "no human
curating"), a person noticing or typing, the log's `Human` column, the `Vouch`
definition, "the human half" of the release, the research notes in
`docs/knowledge`, and every compound not renamed (`human-readable`,
`human-made`, `human-verified`, `human-SR`, `human-facing`, `human-reviewed`,
`HUMAN_METHODS`, `human_srs`). About 230 lines; `r43a_human.py`'s `KEEP` list
is the record of each phrase. "The human path" and "a human trunk commit"
became "the reviewed-commit path" and "a trunk commit" (§4.3); "the owner's
final read is the human's" became "the final read is the operator's".

**The push value's fold.** §10.4 said `bootstrap.py --migrate-config` must
write the new value when it folds the one-word `docs/push-policy`. It was left
writing the file's word as it is, and the migrator respells it: the re-sync
runs the fold, then the migrator. That keeps the earlier spelling in one home
(D3, D11) and adds no legacy knowledge to the core. The re-sync entry must say
so, in that order.

**The record copy, and why it moved early.** The checkpoint commit wrote the
record's copy of `system-requirements.toml` (the migrator renamed its field),
so the mirror rule now judged that commit: `trace.py --strict` reported the
copy as not byte-identical to the live file at `6d8291fb6`. Before the commit
the check looked at an older commit and passed, which is why §9.1 recorded
`trace.py --strict` clean. The fix is the rule's own remedy, done without an
act: the copy was made a byte copy of live, so the next commit writes it equal.
`absorbed.py` named what that takes into the record (D13): SR-247 (new,
`Drafted`), and in 15 accepted rows only the cells this migration reworded
(SR-026, 028, 043, 139, 140, 148, 165, 181, 208, 209, 210, 228, 231, 233, 234,
235). The same comparison at `b5ea4d29c` finds no drift, so nothing earlier
was absorbed. The other six copies differ from live but no commit has written
them; they move at the record step as planned. **Rule for later concepts:** a
commit that writes any record copy must write it equal to live.

Traps found:

26. *A checkpoint commit changes what the mirror rule judges.* The check reads
    the last commit that wrote each copy. Uncommitted, a copy rewritten by the
    migrator passes; committed, it fails unless it equals live.
27. *An article at a line end.* The article rule works per line, so "a" ending
    one line before "human" on the next stays "a". `article_scan.py` lists
    such pairs in the changed files and `--fix` mends them. Run it after every
    rule file whose new word starts with a vowel and the old one did not.
28. *A keep pattern can hold back the role.* "The one document a human reads"
    was kept as the reader sense and is the operator's ruling surface. After
    applying, list what is left (`inv.py lines`) and read it as carefully as
    what changed.

### §9.8 The fifth session: "owner" becomes "operator"

Written 2026-11-12. It found the fourth session's test run still in flight,
waited for it, fixed what it showed, committed the "human" half, and applied
the "owner" half of §10.4.

**The fourth session's run** (245 modules, `vocab-tools/s43a_tests.txt`):
7,243 passed, 172 skipped, 30 failed, in 37 minutes on a loaded box.

| Failures | Cause | Done |
|---|---|---|
| 24 in `test_overnight_legs_git`, 1 in `test_prereq_toolchain` | the run was started from PowerShell, whose PATH has no `sh` (trap 29) | re-run from Git Bash: 32 passed, 1 skipped |
| `test_csv_header::test_ONE_reader_is_a_census_not_a_claim` | real: the migrator's CSV step took a registry's first record as its header row, so a `Verification` header under a `#` declaration preamble was never renamed | `_csv_preamble` measures the preamble as `kitlib.spine.csv_body` drops it, and its bytes are kept; one test; the census names the migrator as an exception, and each exception's own words now sit in `RAW_CSV_ARGUED` (trap 30). `h43n_csv_preamble.py` |
| `test_smoke_budget` | the smoke tier collected 3,568 tests against a budget of 3,550: the migrator's 26 in-process cases | re-stamped 3,550 to 3,720 in `docs/stack.ini`, with a stamp note in the house form |
| `test_module_size_ratchet` | `bootstrap.py` 1,599 to 1,597, and now `agent_loop.py` 2,531 to 2,535 | D17: re-stamp at the close |
| `test_capped_doc_baselines_match_the_real_sizes` | `CLAUDE.md` and `AGENTS.template.md` (9,999 of 10,000) | re-stamp at the close (§10.7 item 6) |

**Committed:** `d45bab5a5`, "human" to "operator" with the fixes above, hook
bypassed (D14). It wrote the record's copy of `system-requirements.toml`
equal to live, and `trace.py --strict` then reported `integrity=0`.

**"Owner" to "operator", applied, not committed:**

| Step | What |
|---|---|
| `r43b_owner.py` | re-run dry first: identical to the fourth session's reviewed run apart from four `docs/stack.ini` lines shifted by the stamp note. Applied: 1,662 lines in 241 files |
| `r43c_owner_iface.py` | 20 lines in 7 interface files, after adding `OWNER_KEY` and `OWNER_VALUES`, which r43b's skip had kept out of `interfaces.toml`'s data cells (trap 31) |
| `h43c.py` | the scratchpad template's header ("For the operator only, as a person. No session reads it, delegated or not.") and its test; `PROCESS_OPTIONS.md` ("a person's scratch", "The final read stays the operator's"); `STK-01` "Operator" |
| `h43d_iface.py` | 23 role sentences in the interface files: the five of §10.4 and eighteen more found by reading every "owner" in them, including the decisions key named by its spelling in IF rows |
| `h43m_migrator.py` | the migrator's decisions-record and scratchpad steps from the draft, with five tests, `STEPS` entries, and SR-247, LLR-369 and TC-427 extended. `tc427_evidence.py` re-run: 25 tests |
| `h43e_owner_left.py` | 116 edits in 78 files: the role uses still left after all of the above (trap 28), out of 271 lines read. Citations without a comma, "owner" opening a line after an article, capitals ("OWNER TEXT"), the decisions key in prose, templates and messages, and the pending-actions read model's text |
| renames | `git mv` of the scratchpad template. The root scratchpad was renamed by the migrator, unread, and staged as a rename |
| migrator run | 52 keys in 16 decisions records; the scratchpad; a second `--check` finds nothing |
| regenerated | `docs/stage`, `prompts/CATALOG.md`, `skills/INDEX.csv`, `docs/open-items.html` |
| checks | `ruff format`, `ruff check`, `trace.py --strict` (integrity 0), `check_trajectory.py --strict`, `check_docs.py --stale`, `check_resync.py`: clean. Skill mirrors identical. The unfiltered suite: see below |

**What keeps "owner"**, read and left: an interface's providing side (every
`owner` key, the `Owner` column, `seam_owner`, `owner_files`, `new_owner`,
`_fold_owner`, `_resolve_owner_path`, `owner_as_written`); a need's owner ("a
need with no named owner", "the need owner sees it"); a hat, module or
function that owns a question or a rule ("no suitable owner", "ONE OWNER", "the
§A5.1 owner", "pin that owner"); the debt owner of the ratchet; a claim holder
(`_owner` in `review_set.py`); `@<owner>` on a finding line; the record heading
`## Owner route` in the coordinator's recipes; and test data shaped like
records (run names in `test_decision_overrule.py`, "Owner ruled." in
`test_done_when_blessing.py`, fixture log text, sample rationale in
`test_trace_rules.py`). `migrate_vocabulary.py` and its tests name the earlier
spellings on purpose. The glossary's older entries are §10.7 item 2.

**Records not touched:** the prose of `docs/decisions/*.toml`, the dated
log fragments' file names, and `docs/status.md`. The pending-actions block is
rendered into `open-items.html`, not into `status.md`, so its new wording
needs no record edit.

Traps found:

29. *A suite started from PowerShell has no `sh`.* The posix-shell gate skips
    147 tests and fails 25 more (`shutil.which("sh")` is None in the
    overnight-legs fixtures). Start suites from Git Bash, or put
    `C:\Program Files\Git\bin` on PATH first.
30. *A census can pin its one exception's words.* `test_csv_header` checked
    every exception for two phrases only `migrate_carrier.py` contains. A
    second exception needs its own words (`RAW_CSV_ARGUED`).
31. *Skipping a file for its prose skips its identifiers too.* r43b skipped the
    interface files because "the owner" there is the providing side, and so
    missed `OWNER_KEY` in an IF row's data cell. After a rule file with a
    skip list, scan the skipped files for its `TOKENS` and `PARTS`.

## §10. Runbook: finishing the migration

Written 2026-11-11 for the session that takes over, which has none of the
earlier conversations. Follow it in order. §11 lists what waits on the
operator; everything else here can be done without asking.

### §10.1 Before touching anything

- Start in `C:\Users\Peter`, outside both worktrees.
- Edit code only in `C:\Projects\ai-template-wt-vocabulary` (branch
  `maint/vocabulary`). This file lives in the other worktree,
  `C:\Projects\ai-template-wt-test-tiers`; update it there as you go.
- Python is `C:\Projects\ai-template\.venv\Scripts\python.exe`. Run the kit's
  scripts from the vocabulary worktree's root.
- **Commit with the hook bypassed** (`git commit --no-verify`), which the
  operator allowed on this branch (D14). Commit at the end of each concept,
  once its checks are green apart from the known failures of §10.2. The
  rewording may take several commits; the move of the acceptance record must
  be a commit of its own, after all of them (§9.2). Never push. Never run
  `git checkout`, `git restore`, `git stash` or `git clean` over uncommitted
  work.
- Never open `OWNER_SCRATCHPAD.md` (or `OPERATOR_SCRATCHPAD.md` once renamed).
- **Edit no file under `project-trajectory/scripts` while a test run is in
  flight** (trap 17). Start a run, then work only in `vocab-tools/` and in
  this file until it reports.
- Use the new words with the operator and in everything you write.
- The tools in `vocab-tools/` have the vocabulary worktree's path written into
  them (`ROOT`). Run them from anywhere:
  `python <vocab-tools>\vapply.py <vocab-tools>\RULES.py --dry --review out.txt`.

### §10.2 The state you inherit

**Superseded by §9.8 for the current state.** As of the fifth session:
committed through `d45bab5a5` ("human"); "owner" applied and checked,
uncommitted; next is §10.5. The rest of this section is the state the third
session left.

Applied in the worktree, uncommitted: the glossary entries; all of §4.4; the
method `Vouch` and the field `verification_method`; the dial and its table;
the migrator with three steps, 22 tests, a manifest row and three `Drafted`
spine rows. §9.1 has the detail.

**The last run, over the `Vouch` follow-ups and the whole dial change** (82
test modules, the list in `vocab-tools/s34_tests.txt`): 2,951 passed, 78
skipped, 2 failed, in 22 minutes. Both failures are known and wait for the
end of the migration:

| Failure | Meaning |
|---|---|
| `test_module_size_ratchet`: `bootstrap.py` 1599 to 1597 | D17. Leave it until the operator rules |
| `test_bootstrap::test_capped_doc_baselines_match_the_real_sizes`: `CLAUDE.md` table says 8,018, file is 8,025 | the byte-budget table is re-stamped once, at the close (§10.7 item 6); `CLAUDE.md` will change again before then |

After that run one thing was fixed and re-checked: `check_trajectory.py
--strict` had 20 errors, every migrator test "tag without evidence". A test
tagged `Implements: TC-427` has to be named in that test case's evidence
cell, node by node; the file's path is not enough (trap 3).
`vocab-tools/tc427_evidence.py` rewrites the cell from the test file; run it
whenever a migrator test is added. With that, `trace.py --strict` and
`check_trajectory.py --strict` both exit 0. One warning is left for the
migrator: it is in the architecture map and no interface row names it.

The unfiltered suite has not been run on this tree. To repeat the run above:

```
$f = Get-Content <vocab-tools>\s34_tests.txt
python -m pytest -q -p no:cacheprovider -n 10 @f
python project-trajectory/scripts/check_trajectory.py --strict
```

If a later run shows a test still feeding `human_approval_through`,
`[attestation]`, `Verification` or `verification =`, it is a form the rules
missed: fix it by hand and add the form to the rule file, so the record stays
true. Do not start the next concept on a red tree.

### §10.3 The loop for each concept

1. **Inventory.** `inv.py tokens STEM` lists every identifier holding a stem
   with counts by area; `inv.py lines REGEX [GLOB]` and `inv.py snip REGEX`
   show the lines. Classify each identifier by what it names (§4, and
   `VOCABULARY.md` for the senses).
2. **Rule file.** Copy the shape of `r42_s4_dial.py`. `TOKENS` renames whole
   identifiers; `PARTS` renames a word inside snake or kebab names (use it for
   test function names); `REGEX` is for phrases. Import `RECORDS`, `HAND_ONLY`
   and `PROTECT` from `common.py` and put them in `SKIP` and `PROTECT`.
3. **Dry run, and read every resulting line.** `--dry --review out.txt`. Look
   for a wrong sense, a broken article ("an recorded", "a operator"), a
   record's file name, and another tool's own flag. Fix the rules and repeat
   until the output is clean.
4. **Apply.** Without `--dry`. If it stops with `ALREADY IN USE`, read every
   use of the new name; pass `--force` only when it is the same thing.
5. **Hand edits.** Whatever needs a sentence rewritten goes in an `h*.py` file
   for `hand.py`, written against the text as it stands after step 4.
6. **Look for the forms a rule misses** (traps 19 to 21): the lowercase TOML
   key beside the capitalised row key, a keyword argument, a message that
   names the field, a name after `\n` inside a string literal.
7. **Regenerate.** `derive_stage.py`; `gen_prompt_catalog.py`;
   `gen_skills_index.py --skills project-trajectory/skills`; copy
   `project-trajectory/rubrics/*.template.md` over their twins in
   `docs/rubrics/` if a template changed; copy each edited skill to
   `.claude/skills` and `.agents/skills` if the rules did not already reach
   all three.
8. **Check.** `ruff format` then `ruff check` over `project-trajectory/scripts`
   and `tests`; `trace.py --strict`; then the test modules the change touched
   (take the list from the review files:
   `Select-String '^=== (tests/test_\S+\.py)' out.txt`), plus
   `test_migrate_vocabulary`, `test_dogfood_sync`,
   `test_generated_freshness_wiring`, `test_complexity_ratchet`,
   `test_module_size_ratchet`, `test_derive_stage`.
9. **Stored values.** If the concept renames something a file stores, add a
   step to `migrate_vocabulary.py` and tests for it, add its symbols to
   LLR-369's `code_symbol` cell, extend that row's `detail` and TC-427's
   `method`, and run the migrator on this repository. Keep each function at a
   complexity of 10 or less (`test_complexity_ratchet`).
10. **Record it.** Add a row to §9.1, any new trap to the list under it, and
    copy the rule files into `vocab-tools/`.

### §10.4 Owner and human become operator (§4.3)

**Done (fifth session), apart from its commit.** "Human" is committed in
`d45bab5a5`; "owner" is applied and checked (§9.8). What follows is the plan
as the fourth session left it, kept for the record of what was decided.

**Progress (fourth session).** "Human" is applied (§9.7) and was under test
when this was written: 245 modules, the list in `vocab-tools/s43a_tests.txt`,
built by taking every changed test file, every test that
names a changed script, and the six standing modules. "Owner" is prepared and
NOT applied: `r43b_owner.py` (everything outside the interface files, anchored
on prose context; its dry run of 1,662 lines in 241 files was read in full and
refined once, `review_diff.py` showing the refinement), `r43c_owner_iface.py`
(citations and renamed symbols inside the interface files only), and the two
migrator steps drafted in `vocab-tools/migrator_owner_steps.draft.py`
(decisions key, scratchpad name; to be added to `migrate_vocabulary.py`, with
tests, a `STEPS` entry each, and LLR-369, TC-427 and SR-247 extended). Hand edits still to write: the
scratchpad template's header and `test_bootstrap`'s assertion of it; the
scratchpad note in `PROCESS_OPTIONS.md` ("a person's scratch"); "The owner's
final read / stays the operator's" (`PROCESS_OPTIONS.md:541`, to "The final
read"); `STK-01` "Owner" to "Operator"; three sentences in `interfaces.toml`
(lines about 705, 2070 and 2244: the dial file the owner edits, the owner's
approval brief, the decisions record the owner edits in place). After the
rules: `git mv` both scratchpad files without opening the root one, run the
migrator, then a split-line scan for "the / owner" as for "a / human".

Fully ruled; nothing here waits on the operator. The bare word "owner" is on
about 2,900 lines in 313 files and names several things, so it is the largest
reading job left.

**Identifiers that name the role, and move:**

| Today | Becomes |
|---|---|
| `OWNER_SCRATCHPAD` (and both file names) | `OPERATOR_SCRATCHPAD` |
| `OWNER_ONLY_PATHS`, `OWNER_PROMPT`, `{{OWNER_PROMPT}}` | `OPERATOR_…` |
| `OWNER_KEY`, `OWNER_VALUES`, `owner_state`, `_owner_findings` (the verdict on a delegated decision) | `OPERATOR_KEY`, `OPERATOR_VALUES`, `operator_state`, `_operator_findings` |
| `owner_cards`, `owner_card` | `operator_cards`, `operator_card` |
| kebab compounds: `owner-held`, `owner-ruled`, `owner-only`, `pending-owner-actions`, `owner-owed`, `owner-confirmed`, `owner-overruled`, `owner-facing`, `owner-review`, `owner-decision`, `owner-verdict`, and the one-off `owner-<participle>` forms | `operator-…` |
| `owner-approved`, `owner-attested`, `owner-accepted` | `operator-accepted` |
| test names about an owner ruling, the owner's act, the owner surface, an owner row, the scratchpad | rename with `PARTS`, and update the evidence cells that cite them |

**Identifiers that do not name the role, and stay:** `owner_files`,
`_owner_files`, `seam_owner`, `_file_owner_declarations`, `file_owners`,
`_owner_exact_findings`, `owner-exact`, `OWNER-EXACT`, lowercase `owner_key`
(in `trajectory_arch.py`), `owner_node`, `ownerless`, `_ID_OWNER_RE`,
`owner-of-record`, `id-shaped-owner`, `owner-side`, `single-owner`,
`one-owner`, every `ownership` form, `CODEOWNERS`, `debt-owner`, `owner_hat`,
and the `owner` key on every interface row. Test names about an interface's
owner stay too (`test_an_owner_reached_…`, `test_seam_owner_…`,
`test_every_owner_is_one_thing_…`, `test_owner_files_…`).

**Not yet read; look before deciding:** `OWNER_WINDOW`, `OWNER_EDITS`,
`OWNER_DIALS`, `OWNER_STATUS`, `owner_content`, `assert_owner_edits_untouched`,
`leave_owner_edits`, `new_owner`, `owner_at`, `owner_as_written`,
`_no_owner_account_homes`, `_no_owner_token_file`, `OwnerDraftRetitle`,
`_one_owner_row`, `_owner_rows`, `_fold_owner`, `_resolve_owner_path`,
`_owner`, `_owners`, `owner-cleanup`, `owner-registry`, `session-owner`, and
`tests/test_bookkeeping.py` (49 uses, likely the files a repository owns as
against the kit's).

**Prose.** In these files "the owner" is usually an interface's providing
side, so keep the prose rules off them and read them by hand:
`docs/requirements/interfaces.toml`, `trajectory_arch.py`, `gen_arch_map.py`,
`kitlib/spine.py`, `spine_carrier.py`, `migrate_carrier.py`,
`rendering/traj_views.py`, `INTERFACES.template.md`,
`registries/interfaces.template.toml`, `MULTI_REPO.md`,
`tests/test_trace_interfaces.py`. Everywhere else "the owner", "the owner's",
"an owner" and "owner ruling" are the role. A lock or claim holder, the one
home of a rule, and the owner of another system keep the word (§4.3's
keep-list).

**Add to `PROTECT` first:** `\bwi-?\d+[a-z]?-[A-Za-z0-9_-]+` (directory names
under `docs/reviews`, such as `wi-818-owner-verdict`) and link fragments such
as `#the-owner-accepts-…`.

**Human.** The senses are in `VOCABULARY.md` §5 and the names in §4.3:
`human_held`, `human_holds`, `human_approves`, `human_approves_spine`,
`human-held`, `HUMAN-HELD`; `EXIT_NEEDS_HUMAN` (the number stays 7),
`NEEDS-HUMAN`, `PAGE-HUMAN`, `page-human`, `page_human`, `stop-needs-human`;
`Needs <human>` with `_NEEDS_HUMAN_RE` and `STACK_NEEDS_HUMAN`; `human-owed`;
`(human-set)`. "A human" becomes "an operator": fix the article. What stays is
listed in §4.3: `human-readable`, `humanized`, `human-made`, the log's `Human`
column, `HUMAN_METHODS` and `human_srs`, and prose that says a person is
meant. "The human path" and "a human trunk commit" become "a reviewed commit"
and "a trunk commit", not "operator".

**Stored values for the migrator:**

- `push = "human"` to `"operator"` in `[policies]`: a value map for the policy
  step. Its meaning widens (trap 14); reword the prose around it in
  `bootstrap.py`, `process.toml.template` and `subagent_gate.py`.
  `bootstrap.py --migrate-config` folds the one-word `docs/push-policy` file
  and must write the new value.
- `owner =` to `operator =` in `docs/decisions/*.toml`, 52 keys in 16 files.
  Every record is read, so all move. The commit that does it trips the
  `ruling-sync` check, which reads both trees through the key and sees three
  overrules as new; that is one more reason the migration commits bypass the
  hook. The prose of those records stays as written.
- `OWNER_SCRATCHPAD.md` to `OPERATOR_SCRATCHPAD.md`: here, `git mv` without
  opening it. Seven scripts protect the file by name
  (`VOCABULARY.md` §4). The migrator renames it; the detector must refuse a
  file left under the old name, because it would silently lose that
  protection.
- `{{OWNER_PROMPT}}` in prompt templates and any override of one.

**Accepted rows this touches:** `STK-01` "Owner" becomes "Operator". By D5 it
is edited in place.

**Byte budget.** `project-trajectory/AGENTS.template.md` is at 9,992 bytes
under a cap of 10,000, and each "operator" adds three. Trim elsewhere in that
file to pay for it, then re-stamp the table in
`skills/byte-budget-guard/SKILL.md` (and that skill's own row). `CLAUDE.md`,
`PROCESS.md` and `PROCESS_OPTIONS.md` have stamped baselines in the same table.

### §10.5 Then: the act (§4.2)

Do it in four passes. D12 is ruled: a reviewer's verdict keeps `APPROVE`, so
in every pass leave it alone, and add a glossary entry for it (**approve**,
the reviewer's verdict on a round or a plan, distinct from **accept**). Leave
alone: `VERDICT: APPROVE`, `APPROVE|CHANGES-REQUESTED`, `Review-Verdict:`,
`VERDICT_APPROVE`, "a critic `APPROVE`", and the code in `kitlib/verdict.py`,
`score_reviews.py`, `plan_round.py`, `plan_runner.py`, `plan_gate.py` that
handles review rounds. An adjudicator's ruling on a row
(`_AUTHORIZING = {"first-approval": ("APPROVE",) …}` in `kitlib/sitting.py`,
and `adjudicate_act.py`) is the act and becomes `ACCEPT`.

1. **Re-attest to re-accept.** `reattest_model`, `reattest_lines`,
   `parse_reattests`, `reattested_between`, `reattest_scope_refusal`,
   `verdict_reattest_block`, the `_REATTEST_*_H` headings, the in-memory kind
   `"reattest"`, the flag `--reattests` (to `--reaccepts`), `--approves` (to
   `--accepts`), "Re-attestation brief". The ledger keys are stored; they move
   in pass 4.
2. **The kind and the class.** `first-approval` to `first-acceptance`
   everywhere live (about 400 uses), with `FIRST-APPROVAL`,
   `ADJUDICATE_FIRST_APPROVAL` and the prompt file
   `adjudicate-first-approval.template.md` (rename it with `git mv`, then
   regenerate the catalogue). `safety_class` `"attestation"` to `"acceptance"`
   in `schedule.py`, `dispatch.py` and their tests. Stored:
   `"first-approval"` in `[adjudicator] retain_for` of `docs/process.toml`
   needs a migrator step. Old verdict files and bindings keep the old kind
   (D15).
3. **Approve and attest to accept.** `PARTS` does most of it: `approved` to
   `accepted`, `approval` to `acceptance`, `approve` to `accept`, `approves`,
   `approving`, `approver` to `acceptor`, `unapproved`, `unattested`. Both old
   and new words begin with a vowel, so articles hold. Read every line that
   could be a review verdict or a project's own approval ceremony. What was
   "attestation" in the sense of the checks record is not this pass; it is
   §10.6. Free a name before reusing it (trap 12): check each new name with
   the collision report.
4. **`status`, the record and the ledger**, last, through the migrator:
   - add `status` / `Status` with `Approved` to `Accepted` to `VALUES`;
     rename the status literal's homes in the code (§9.2's trace lists them:
     `kitlib/spine.py:547` and `:584`, `acceptance_record.py:581`,
     `spine_rules.py`, `trace.py:678-696`, `census.py:130`, `intake.py`,
     `spine_carrier.py`, `migrate_carrier.py`, `gen_release_checklist.py`,
     `traj_parse.py`);
   - rename `SNAPSHOT_DIR` to `docs/archive/last_accepted` (homes:
     `baseline_snapshot.py:249`, `acceptance_record.py:1732`,
     `kitlib/bootstrap_manifest.py:190`) and the ledger keys `approved`,
     `reattested` to `accepted`, `reaccepted` in every reader and writer;
   - a migrator step that moves the directory, renames the two keys in each
     `[[act]]` entry of `acts.toml`, and writes each registry copy equal to
     its live file, printing every accepted cell that differed beforehand
     (D13 decides whether it absorbs or refuses when one does);
   - 18 files under `docs/test/observations/` hold `judged = sha256:…` over a
     row with its `status`. Read `record_observation.py:240-248` and decide
     whether the migrator recomputes them; this was not traced;
   - **never run `intake.py snapshot` between the code rename and the record
     move**: it would write a 904-row act;
   - `check_test_first.py` and `check_trajectory.loop_held_status_findings`
     read history and will see the cut (§9.2). Decide for each whether a tree
     without the new names is simply not judged.

   Row wording and the record cannot share a commit (§9.2). Keep the work so
   that it can be committed as: everything except the record, then the
   record.

### §10.6 Then: the passed-checks record, with §4.5.1

D16 is ruled: §4.5.1 as drafted, so the names below and §4.5.1's are settled.
The glossary entry for the passed-checks record is written; add one for the
failed-checks record (§4.5.1's draft). Nothing here is applied yet.

| Today | Proposed |
|---|---|
| trailer `Bar-Green: … bar=<review\|landing\|no-bar>` | `Checks-Passed: … checks=<commit\|landing\|none>` |
| `BarAttestation`, `bar_attestation`, `read_bar_attestation`, `format_bar_green`, `_ATTEST_RE` | `PassedChecks`, `passed_checks`, `read_passed_checks`, `format_passed_checks`, `_PASSED_CHECKS_RE` |
| `review_attestation`, `refresh_attestation`, `mechanical_close_attestation` | `commit_passed_checks`, `refresh_passed_checks`, `mechanical_close_passed_checks` |
| `integrate.py attest --bar review`; `attest`, `_attest_commit`, `_attest_message`, `_attest_preflight`, `_AttestPlan` | `integrate.py record-checks --checks commit`; `record_checks`, `_record_checks_commit`, and so on |
| `attest_build` (`agent_loop.py`), `attest_refusal` (`kitlib/red_mark.py`), `_ATTEST_STEP` | `record_build_checks`, `record_checks_refusal`, `_RECORD_CHECKS_STEP` |
| log phase `ATTEST`; labels `ATTEST GREEN`, `ATTEST RED` | `CHECKS`; `CHECKS PASSED`, `CHECKS FAILED` |
| `test_bar_attestation.py`, `test_integrate_attest.py`, fixture `attest_repo` | `test_passed_checks.py`, `test_integrate_record_checks.py`, `checks_repo` |

Rename the failed-checks headers in the same change (§9.2), and the key list
in `agent_common.write_session_log` with them. Write and read the new form
only. The glossary's "commit checks" entry still describes the old command;
rewrite it here.

### §10.7 Closing the branch

1. The rest of §4.5, as the operator rules each line.
2. The glossary's older entries, by hand: "the owner" in *independence* and
   *arbiter*, "takes the approval act" in *adjudicator*, "approves only if it
   changes nothing" in *independence*.
3. Plain "accept" in the code where a reader could take it for the act
   (§4.4's last paragraph). Candidates noted: test names such as
   `test_a_well_formed_verdict_is_accepted_and_parsed`, and "adoption …
   accepted" in `test_handback.py` and `test_disposition_adoption.py`.
4. The detector (§5, part 2): add the old stored spellings to
   `check_vocab.py`, compounds only for "owner" and "human", a separate
   pattern for snake-case names, and the scratchpad's old file name.
5. The re-sync entry in `project-trajectory/RESYNC_PACK.md`: the tables of §4,
   "run `migrate_vocabulary.py`", what the detector refuses, the two commits
   and why they bypass the hook, and what is left to the adopter's session.
6. Byte budgets re-stamped; the nine ratcheted modules (D17); the complexity
   baseline re-keyed for renamed functions (`docs/complexity-baseline`).
7. The four strict lints, then the unfiltered suite once (33 to 45 minutes).
8. D11's change, separately: the twelve legacy tables leave the core for the
   migrator.
9. Then §6, in order. B1 is ruled (D6, D7), the suite's name included
   (`iterate`); B8's launcher is ruled out (D8).

## §11. What waits on the operator

**Ruled on 2026-11-11 by the fourth session's operator answers:** D6's name
(`iterate`), D12 (`APPROVE` stays for a review verdict), D13 (absorb, naming
each cell), D14 (commit with the hook bypassed), D15 (leave as written), D16
with §4.5.1 (as drafted), D17 (re-stamp once at the end), D18 (accept the
migrator's rows once it is complete). Nothing blocks the runbook now.

**Still open:**

| | Blocks | Until then |
|---|---|---|
| §4.5.2 to §4.5.7 | those renames, in §10.7 item 1 | skipped; nothing else depends on them |
| D18's act itself: the operator reads and accepts SR-247, LLR-369, TC-427 | the live stage returning to `DevStg-Impl` | the rows stay `Drafted` until the migrator is complete |
| §7, the order for reaching other repositories | nothing in this runbook | |

**Needs no answer unless the operator disagrees:** the reading of "operator
time" in §9.1.

## §12. The sixth session: triage, the test-run crash, and what the operator ruled

Written 2026-11-16. **A session taking over reads this section first**, then
§10 for the vocabulary runbook. It is updated as work lands; the last entry
of §12.6 is the current state.

### §12.1 What the operator asked for

Review every recent audit of the kit, find what still applies and what is
unscheduled, and finish the kit so that downstream repositories can use it,
HomeHub first (its open items and requirements). Codex usage is spent:
cross-family review goes through `opencode run -m opencode-go/deepseek-v4.1-flash`.
The operator asked for care against over-design: fix what a real adoption or
a reproduced first-day run hit, prefer removing or quieting to adding
mechanism, and leave alone findings that would reverse an earlier ruling.

### §12.2 Rulings taken on 2026-11-15 and 2026-11-16

| | Ruling |
|---|---|
| Working mode | Continue on `maint/vocabulary` as maintenance work: no lanes, hook bypassed (D14 extended by the operator). Commit when a unit is done; never push |
| Order | Vocabulary before the adopter-facing fixes. **Revised 2026-11-16:** the operator will confirm the vocabulary direction before any further rename, so §10.5, §10.6 and §4.5.2 to §4.5.7 are ON HOLD. Work that does not depend on them goes ahead |
| OI-130, the partition | **Accepted: P5 is the depth-0 partition**, on the re-score's evidence (`docs/plans/2026-11-11-oi130-rescore/`). Q1 (b), a fresh ruling dated 2026-11-16; Q2 as the re-score states it: OI-14's objective, its constraint measured as straddle, cut as the tie-breaker, no override |
| WI-999, the derivation record | Build it. Without it traceability is incomplete. If it is optional at all, it is on by default with a setting to turn it off |
| §4.5.2 to §4.5.7 | Not ruled. The operator asked whether "stage" means the development stage or is confused with something else (§12.4) |
| Full-suite runs | Be very careful: they have slowed the machine to a crawl and crashed VS Code. See §12.3 before running one |

### §12.3 Why a test run crashed the machine, and how to run one safely

**Cause, measured 2026-11-16.** The user environment variable
`PYTEST_DEBUG_TEMPROOT` is `C:\Projects\.pytest-tmp`, which is inside the
folder VS Code has open (`C:\Projects`, about 150 repositories). Each test
scaffolds a kit into its temp directory. VS Code's Python extension answers
every new `.py` file with a fresh `rg --files` walk of the whole workspace, at
normal priority and outside the test run's CPU cap.

| Sample (`tests/test_trace.py`, 2 workers, 55 s) | File events under `C:\Projects` | `rg` processes started | Tests finished |
|---|---|---|---|
| Variable as set | 9,286 | 755 (137 at once) | 7 |
| Variable unset (`env -u PYTEST_DEBUG_TEMPROOT`) | 62, all git lock files | 0 | 23 |

With 6 workers the count reached 434 `rg` processes and was still climbing,
with python near 0% CPU: the tests were starved by the scans they caused. The
root conftest's 50% CPU cap and below-normal priority were working throughout;
they cannot reach processes VS Code starts. Memory (64 GB) and disk were idle.

**Until the variable is changed, every pytest run on this machine starts with
`env -u PYTEST_DEBUG_TEMPROOT`** (Git Bash) so that temp files go to
`%TEMP%`. The kit's own log (2026-07) already records runs "with
`PYTEST_DEBUG_TEMPROOT` unset" for a different reason: a dot-named temp root
makes `test_gen_arch_map` fail.

**Waits on the operator:** change or delete the user variable. It was not
changed by this session, because it is machine configuration and the reason it
was set is not recorded.

**Not done, on purpose:** a lock against concurrent runs and a lower worker
count. Neither addresses the measured cause. Revisit only if a run with the
variable unset still troubles the machine.

The measuring scripts are not kept; the method is: a `FileSystemWatcher` on
`C:\Projects` plus a count of `rg.exe` every half second.

### §12.4 "Stage" (the operator's question on §4.5.2 and §4.5.5)

In the kit "stage" means the development stage: the rung on the `DevStg-*`
ladder that `docs/stage` records (`PROCESS.md` §4, "A stage is a STATE").
`landing_stage`, `sr_stage` and `maturity_stage` would all mean that. Three
other uses exist, and the glossary has no entry for the word:

- "staged", git's index: `staged_spine_amendments`, `staged-divergence` and
  about 50 more names. The usual git word; no change proposed.
- The glossary's *lane state* entry: "A state names the stage whose work is
  owed next". Here it means a step of a lane, not a development stage.
- `PROCESS.md` §3, "extract the shared stage": a step of a pipeline in code.

Proposed, for the operator: a glossary entry for **stage** (the development
stage, and nothing else); "step" in the two sentences above; and for §4.5.2
the key name `checks_stage` in place of `landing_stage`, because "landing
stage" reads as a step of landing. `check.py --stage` already uses the word
this way.

### §12.5 The triage (2026-11-15)

Full findings are in the session's reports, summarised here. Nothing in this
list is fixed unless §12.6 says so.

- **`codex/simplify-spine-resync`** (`d091418e1`): complete; merges cleanly.
- **`origin/rolling_review`** (`04488d5cd`): none of its adopter-facing
  findings (its §9 and §14 items 1, 3, 5) is fixed or filed. About 25 of its
  §13 findings would reverse a ruling and are left alone.
- **The downstream conversion of 2026-11-12** (13 repositories, records in
  `C:\Projects\spine-conversion-2026-11-12\` and each `-wt-spine` worktree's
  `SPINE_CONVERSION_GAPS.md`): 24 kit findings, 16 confirmed in the code, none
  with a work item.
- **Trunk `refactor_again`** (`3e7a3a6ee`): no open claims. 13 queued rows;
  WI-1003 to WI-1006 owe a scope critique. The review-churn plan's phase 3
  (items 5, 10 steps 3 to 6, 11, 12's builds) is ruled and has no rows. The 60
  folders under `docs/work/active/` are empty leftovers.
- **HomeHub** does not use the kit. Its `open-items.md` (940 KB, sections A to
  G, numbered by hand) maps to the kit as: A to the open-items registry; C, D
  and E to work items; F and G to the log.

**The adopter-facing batch** (no ruling needed), in the order to do it:

1. From real conversions: the advisory flood when no stakeholder is accepted
   (13 repositories); the contract reader that understands only `#` and
   Markdown comments (8); interface rows left unchecked without saying so
   (8); `check_docs` reporting the kit's own generated report as an orphan
   (7); `--strict-schema` exiting 0 with findings; `migrate_carrier` marking
   needs `Approved` by default; `.gd` missing from the source extensions; the
   boundary gate ignoring `delivered_with`.
2. From the first-day run: `sh scripts/setup.sh` under dash; the CI template's
   depth-1 checkout; the undocumented regeneration commands behind three
   refused commits; example rows moving the stage to Impl; `pytest.ini`
   shadowing `pyproject.toml`; docs pointing at a dashboard that is never
   generated; five different "what next" commands; two guards that fire on a
   first-day tree.

### §12.6 Progress log

- **2026-11-15.** Committed what both worktrees held uncommitted:
  `maint/vocabulary` `dfb281b0a` ("owner" to "operator", with two dogfooded
  lines the sweep missed) and `proposal/test-tiers` `40847887f` (this file,
  `VOCABULARY.md`, `vocab-tools/`).
- **2026-11-16.** A full-suite run on `dfb281b0a` died at 7% when the session
  ended; §12.3 is what was found. **The unfiltered suite has still not passed
  on `dfb281b0a`.**
- **2026-11-16, merges.** `maint/vocabulary` now holds `proposal/test-tiers`
  (this file), `codex/simplify-spine-resync` and trunk `3e7a3a6ee`, at
  `8ac37acf0`. The two RESYNC entries on the branch are re-anchored at the new
  base and `check_resync` passes. After a merge of trunk, `check_resync`
  judges the branch from the new merge base: re-anchor again each time.
- **2026-11-16, in flight when this was written.**
  - The unfiltered suite on `8ac37acf0`, 8 workers, variable unset, with a
    watchdog that stops the run if `rg.exe` passes 40 or free memory falls
    under 6 GB. A first attempt was stopped by the watchdog for a reason of
    this session's own making: `git worktree add` under `C:\Projects` wrote
    thousands of `.py` files and set off the same scans. **Do not create or
    check out a worktree under `C:\Projects` while tests run.**
  - Two fix branches cut from `8ac37acf0`, each worked by an Opus sub-agent
    and to be merged back into `maint/vocabulary` after a DeepSeek review:
    `maint/fix-conversion` in `C:\Projects\ai-template-wt-fix-a` (§12.5 list
    1, without the `migrate_carrier` default and the `delivered_with` gate,
    which change what rows mean and wait on the operator) and
    `maint/fix-first-day` in `C:\Projects\ai-template-wt-fix-b` (§12.5 list
    2). Neither edits `RESYNC_PACK.md`; one entry for both is written at the
    merge.
- **Not started:** recording OI-130's ruling in `open-items.toml` with the
  rows that cite it (WI-999, WI-1001); building WI-999; the scope critiques
  owed on WI-1003 to WI-1006; everything on hold in §12.2.
- **2026-11-16, the unfiltered suite on `8ac37acf0`:** 8,026 passed, 29
  skipped, 4 failed, in 27 min 16 s (8 workers, variable unset, started from
  Git Bash). No `rg.exe` ran at any point and free memory never fell under
  38 GB, so §12.3's cause is confirmed on a whole run. The four failures:

  | Test | Meaning | Owed |
  |---|---|---|
  | `test_capped_doc_baselines_match_the_real_sizes` | `CLAUDE.md` stamped 8,018, is 8,037; `AGENTS.template.md` stamped 9,992, is 9,999 | re-stamp at the close (§10.7 item 6) |
  | `test_module_sizes_exactly_match_the_committed_baseline` | `agent_loop.py` 2531 to 2535, `intake.py` 1955 to 1957, `bootstrap.py` 1599 to 1597 | D17, at the close |
  | `test_the_one_non_literal_site_in_the_kit_is_lf` | a pinned line number in `gen_open_items.py` moved 1670 to 1672 with the "owner" sweep | re-stamp with the others |
  | `test_check_harness.py::test_jobs_parallel_plan_matches_sequential` | failed under the full run, passes alone (45 s) | nothing; it is sensitive to load. Re-run it alone after any full run that shows it |

  The three stamps are re-done once, after the two fix branches merge, since
  those change sizes again.
- **2026-11-16, OI-130 recorded.** `maint/vocabulary` `d6e2d30cc`: the item
  reads `ruled`, WI-999 drops its `needs` and states the record's cells
  (`objective = "minimize cut"`, scores P5 140, P3 152, P4 235, no override),
  and `docs/log.d/2026-11-16-operator-rules-oi130.md` carries the ruling.
  WI-999 is not built yet.
- **2026-11-16, both fix branches are built** and wait on their DeepSeek
  review, then the merge into `maint/vocabulary`, one RESYNC entry for both,
  the regenerated views and the re-stamps.
  - `maint/fix-conversion` (7 commits, tip `cea6779cd`): the advisory flood
    is one count line while no stakeholder is accepted; contract headers are
    read in `//`, `/* */`, PowerShell and batch comments and behind a BOM;
    `check_trajectory` says how many interface rows its contract gate could
    not check; `check_docs` ignores the generated `docs/test` reports;
    `--strict-schema` says when its findings do not fail the run (the exit
    code is pinned by TC-189 and stays); `--no-placeholders` reads parsed
    rows; `.gd` is a source extension. Skipped: the first-day architecture
    warning, because no threshold is right for seams that are not imports.
  - `maint/fix-first-day` (10 commits, tip `53d2f3a00`): `bash`, not `sh`,
    for the setup scripts; `fetch-depth: 0` in the CI template; one first
    command everywhere (`check.py` with no `--stage`); the dashboard
    sentences say when the file appears; no `pytest.ini` beside a
    `pyproject.toml` that configures pytest; `trunk_step.py --regen` writes
    the okf bundle the commit check asks for, and the README template names
    the commands to run after editing a registry; two first-day noise lines
    gone.
  - **For the operator, from these two:**
    1. SR-195 and LLR-227 say each unreachable need is reported by name.
       While no stakeholder is accepted they are now reported as a count.
       Either the rows gain that sentence or the change is undone.
    2. Accepting a first real chain moves the stage to Impl, where the
       shipped `-000` rows and the example flow then fail the checks. Hold
       the stage at Reqs while examples remain (which also holds back the
       adopter's own tests), or keep the failure and tell adopters in the
       README note to delete the examples when they accept their first
       chain? This session recommends the README sentence.
    3. `trajectory_arch.py` passed 1,000 code lines (989 to 1,012), so the
       line-count ratchet wants a first baseline entry for it.
- **2026-11-16, both fix branches reviewed and merged.** `maint/vocabulary`
  is at `99166f01d`. DeepSeek (`opencode-go/deepseek-v4.1-flash`) reviewed
  each diff and asked for changes on both:
  - Conversion: the count line was swallowing gate advisories that have
    nothing to do with stakeholders ("cites no assumption", "not approved").
    Fixed in `6e5bcf5ba`: only the reach-caused lines fold; the line no longer
    claims every need is unreachable.
  - First day: the CI template and both setup scripts ran `pip install -e .`
    for any `pyproject.toml`, which fails on one that holds only tool
    settings. Fixed in `f34c74874`: they install only when the file declares
    `[project]` or `[build-system]`.
  - Declined as cases nobody hit: a kit checkout missing its own
    `pytest.ini`; `sh ./scripts/setup.sh` beside `sh scripts/setup.sh`.
  - A DeepSeek review given the repository takes 20 to 30 minutes and reads
    widely. Tell it to answer from the diff and cap its tool calls.
- **In flight:** a Sonnet sub-agent in the vocabulary worktree re-stamps the
  line-count ratchet, the byte-budget table and the pinned line number, and
  writes one RESYNC entry for both fix branches. After it: one more
  unfiltered suite run (§12.3's recipe) to confirm the branch.
- **Still owed before `maint/vocabulary` can be trunk:** the generated views
  (`trunk_step.py --regen`: dashboard, CLI and interface references, the
  status snapshot); `docs/status.md`'s resume text, which still describes the
  queue before OI-130 was ruled; and everything on hold in §12.2.
- **2026-11-16, the branch passes whole.** `maint/vocabulary` at `97207bd0c`:
  the unfiltered suite ran **8,045 passed, 29 skipped, none failed**, in
  26 min 2 s (8 workers, variable unset, no `rg.exe` at any point). Before it:
  - `5c6cc4dc7` re-stamped eight line-count baselines, the byte-budget table
    and the pinned line number. `trajectory_arch.py` has its first baseline
    entry (1,012); decomposing it is left to the operator. The ratchet's
    header asks for the reason of a bump in the work item's log; this branch
    has no work item, so the reasons are in the entries' comments only.
  - `1f75f680e` added one RESYNC entry for both fix branches.
  - `97207bd0c` moved `check.py`'s empty-plan line into `_say_empty_plan`,
    because the first-day fix had taken `main` from 15 to 16 on the
    complexity census.
- **State for whoever resumes.** All four worktrees are clean. Nothing is
  pushed. `maint/fix-conversion` and `maint/fix-first-day` are merged and
  their worktrees (`C:\Projects\ai-template-wt-fix-a`, `-fix-b`) can be
  removed. Next in order: build WI-999 (ruled, §12.2); then the operator's
  answers on the vocabulary (§12.2, §12.4) and on the three points at the end
  of the fix-branch entry above; then §10.5 onward.
- **2026-11-16, WI-999 is built and merged.** `maint/vocabulary` is at
  `6e24ff593` (four commits from `maint/wi-999`, built by an Opus sub-agent in
  `D:\ai-template-wt-wi999`, a worktree outside the VS Code workspace so that
  creating it starts no scans).
  - CMP-006 holds the record as OI-130 ruled it; CMP-007, 008 and 009 cite
    it. `component_findings` reports absent, incomplete, malformed and
    inconsistent records; `[checks] components_check = false` still turns the
    pass off. Ten tests; TC-166's evidence names them. One RESYNC entry (a
    forced migration). The row is in `docs/archive/work/complete/` with its
    review box open.
  - The acceptance act is seq 182 in `docs/archive/last_approved/acts.toml`:
    it copied `components.toml` only, and beside the new cells it absorbed
    CMP-006's `notes` change pending since August (D13).
  - DeepSeek's review raised two points, both of them the row's own stated
    design and so not changed: an empty list in a cell is refused by the
    carrier (the row's "Trust" section says so; "no constraints" is written
    `"none"`), and the holding row's findings name the rows that cite it
    (also "Trust").
  - `trajectory_arch.py` is now 1,132 code lines (pin re-stamped).
  - **For the operator:** LLR-172's detail still says "NOT BUILT YET" and
    TC-166's method still names `trace.py`'s component pass. Both are accepted
    text, so correcting them is an acceptance act.
  - A confirming unfiltered suite run on `6e24ff593` was started; its result
    is the next entry.
