# Glossary

The kit's working terms for lanes, sessions and adjudication, each defined once
here. Other docs link to a term rather than restating it. One term names one
concept: where two words were used for the same thing, the entry says which one
is kept.

An entry marked **Planned** describes machinery the kit has designed but not yet
built; its **Today** line says what runs in its place. Read a planned entry as
the vocabulary the next changes are written in, never as a claim about the
current scripts. Links are authored for the scaffolded home (`docs/glossary.md`
beside `docs/process.md` and `docs/process-options.md`).

## Sessions and routing

### ask

**Planned.** The one labelled entry point for a model call. It picks the tier,
family, route, account and session; a caller names only the [kind](#kind).
**Today:** each caller selects its route from the model registry
(`docs/agents.toml`, read by `scripts/agent_route.py`) and launches the session
itself.

### kind

**Planned.** The label an [ask](#ask) call carries: `build`, `plan`,
`plan-dual` (one of a decomposition round's two drafters), `plan-critique`,
`review`, `judge`, `adjudicate`, `author` or `author-review`. Each kind belongs
to one [session family](#session-family) and declares, in the one policy home,
its **eligible families** (a weight per family; a family absent or at weight 0
is not eligible for that kind) and its default tier. Among the eligible
families, every positive weight is a literal share of the draws. **Today:**
routing is per phase (`PLAN`, `BUILD`, `REVIEW-A`/`REVIEW-B`, `CRITIQUE`,
`DESIGN-CHECK`, `ADJUDICATE`, `DUALPLAN-ARBITER`), weighted per registry row in
`docs/agents-enabled`, where a weight of 0 means fallback-only.

### session family

**Planned.** Kinds that share one retention slot and one
[independence](#independence) rule: [plan and build] (`build`, `plan`,
`plan-dual`), [adjudicate] (`adjudicate`, `author`), [adjudication review]
(`author-review` and the post-act final review), [review] (`review`,
`plan-critique`) and [judge] (`judge`). **Today:** only the
[adjudicator](#adjudicator)'s session can be retained (the `[adjudicator]`
table in `docs/process.toml`); every other call starts a fresh session.

### independence

A judgement never runs in a session that authored what it judges. The one
exception is the [adjudicator](#adjudicator)'s final pass over its own spine
draft after an [adjudication reviewer](#adjudication-reviewer) has edited it: it
approves only if it changes nothing. Excluding a **session** is hard. Preferring
another **family** (other than the judged author's, or the builders') is a
ranked preference within the kind's eligible families: it is dropped only when
the eligible families cannot meet it, so a fresh session of an eligible family
is always available, and each unmet preference is logged. One the declared
families make impossible (a kind with a single eligible family) is logged
only; one that availability prevented (a cooldown, an outage) is also listed
for the owner's review. **Planned:** the ranked form. **Today:** reviewers run
in a fresh session, and the different-family filter runs before pins and
weights.

### reset terms

The declared conditions under which a family's next call starts a fresh
session: the context dial's crest (drain, then retire at a clear point), a
changed governing input, a changed CLI version, an unusable session, a lease
that expired unreleased. "Every call" is a value of the terms, not a second
path. **Today:** these terms govern the adjudicator's retained session only;
the per-family form is planned.

### account

**Planned.** A declared login of one CLI, with its own **home** (the CLI's
configuration and credential directory) outside every checkout. A route runs
under an account as `ROUTE@ACCOUNT`, so a second login needs no second registry
row. **Today:** a second account is a second registry row whose `env` points
the CLI at another home (`CLAUDE_CONFIG_DIR`, `CODEX_HOME`).

### strength

How capable and how deliberate a session is: its **tier** (`quick`, `medium`,
`strong`) and its **effort**. Where it is defined today, in the order a call
meets it:

1. the registry row's `tier` in `docs/agents.toml`;
2. the row's effort, set separately in its launch (`CLAUDE_CODE_EFFORT_LEVEL`
   in `env`, `-c model_reasoning_effort` in `cmd_template`);
3. the per-phase default tier, `DEFAULT_PHASE_TIER` in
   `scripts/agent_brief.py` (`AGENT_TIER_MAP` overrides it);
4. each work item's `buildtier`, which pins the build tier;
5. escalation, which only raises the tier, never lowers it;
6. a plan's per-block tier hint (`docs/plan.md`, advisory).

**Planned:** the per-phase default moves into each [kind](#kind)'s declared
tier, and a planning dial may set the tier per item.

## Roles

### adjudicator

The role that rules on spine rows, disputes and dispositions and takes the
approval act, performed by an [adjudicate] session, retained until its
[reset terms](#reset-terms) are met. One term: a retained adjudicator, and an
"independent adjudicator" launched by the loop or by a person's coordinating
session, are this same role under the same rules, not separate roles.

### adjudication reviewer

**Planned.** The [adjudication review] session that edits the adjudicator's
spine drafts and reviews a sitting's writes and the post-act final review.
Never the adjudicator's session; it prefers another family than the
adjudicator's, then than the builders'.

### reviewer

A [review] session judging a build round or a plan. Never retained, and never a
recorded author of what it reviews.

### judge

A [judge] session that re-judges a recorded observation. Never retained. Not
`JUDGE`, the [sitting](#sitting) substate in which the adjudicator acts.
**Today:** the observation re-judge runs as an adjudication brief; its own
family is planned.

### arbiter

Whoever selects among rival plans in a decomposition round. **Planned:** the
drafters select, by concession, never one drafter's vote for its own plan
alone; when each selects its own, the round becomes an open item for the owner,
which offers running an independent third agent of the owner's choosing, only
if the owner picks it. **Today:** two position-swapped arbiter runs must agree
([process-options.md "Dual-plan decomposition"](process-options.md#dual-plan-decomposition)).

## Lanes

### lane state

**Planned.** Where a lane is in its lifecycle, derived from committed evidence
and live ownership on every read, never stored: `PLANNING`, `BUILD`,
`REVIEW_REWORK`, `ADJUDICATION`, `MERGE` or `ARCHIVE`. A state names the stage
whose work is owed next or is running now; after `ARCHIVE` the lane is closed.

- **Substate:** `PLANNING` is `SINGLE` or `DUAL` (`DRAFT`, `CROSS_CRITIQUE`,
  `ARBITRATION`); `ADJUDICATION` runs `LOCK`, `REFRESH`, `RESOLVE`, `JUDGE`,
  `MINT`, `MERGE_ACTION`.
- **Condition:** a fact reported beside the state, such as `PARKED` (a claim
  with no live owner), a review owed or rework owed.

**Today:** no lane state is named; the dispatcher and the integrator read the
same evidence (the work
item's folder, commit trailers, branch refs) each in its own way.

### decision record

A committed decision: an outcome, a verdict, a resolution, a merge action. It
never claims that a process or a lock is live; that is read from the process or
the lock.

### station authority

**Planned.** The one fenced lease every tool write to trunk takes. **Today:**
merges are serialized by the integrator's lock.

### sitting

**Planned.** A lane's `ADJUDICATION` under the [station
authority](#station-authority). Its **sitting record** holds its resolutions,
its [consumption list](#consumption-list) and its [merge
action](#merge-action); its **scope record** lists the rows it may act on.

### consumption list

**Planned.** Every item a sitting must dispose of, each as an open item, a
decision, a successor or no action.

### merge action

**Planned.** `merge`, `merge-partial`, `cancel` or `return`. **Today:** the
outcome folder the lane moved its work item into is the merge intent.

### landing

**Planned.** The one squash commit per lane (a batch of work items lands as
one, naming every item); the lane tip is kept on `archive/lanes`. **Today:** a
lane lands as a `--no-ff` merge of its refreshed branch.

## Planning

### implementation plan, decomposition

The two products of `PLANNING`: an **implementation plan** leads to `BUILD`; a
**decomposition** is a rival-plan round (the `plan-dual` kind) yielding
successor rows. **Today:** the decomposition round exists
([process-options.md "Dual-plan decomposition"](process-options.md#dual-plan-decomposition));
the per-item implementation plan is planned.
