# Construction-first remedies: wire the antidote doctrine into the reviewer's finding contract

**Status:** plan of record for the row minted against it. Authored 2026-09-01
from the supervised-unpause run's measured review/rework interplay (the log's
2026-09-01 entry; delegated decisions 47–51).

## 1. The problem, measured

Across thirteen REVIEW-A rounds on five rows, **one** remedy was structural.
Every other finding's remedy was additive — "wire the checker", "extend the
invariant", "add a regression test", "add a warn". The exception is WI-543
round 2, which demanded the delivered universe be *enumerated and diffed*
rather than checked; the result (`bootstrap.delivery_inventory()`) makes an
omitted shipped file **unrepresentable** instead of detected, and it is the
healthiest change in the run.

The clearest accretion trace is the successor invariant:

1. It gated on the `brief` cell. WI-552 round 1 found the cancelled arm is
   brief-less by design, so the guard was blind to it.
2. The fix re-keyed it to a **title-string prefix**
   (`intake.owes_successor`, `title.startswith("dispose:")`), enforced in
   **two** places — `handback.close_adjudication` and
   `intake._disposition_drafts` — the second because an agent may self-close
   past the first.
3. WI-566's round then found the predictable consequence: an `adjudicate:`
   title carrying an `amendment` brief slips **both** guards. The remedy
   proposed for that was "extend the invariant (or a warn)" — a third guard
   on the same axis.

The construction alternative is visible in the code and nobody in the chain
proposed it: `intake._close_drafts` **knows** which arm it is minting (an
explicit `outcome == "cancelled"` branch), encodes that fact into a title
string, and omits the typed cell — after which two guards sniff it back out
by prefix. A typed obligation cell written at the mint, which the close
cannot drift from, retires the whole class.

**Why the bias persists — it is economic, not intellectual.** Complying with
a finding costs the lane zero extra rounds; disputing one costs a round and
risks another CHANGES-REQUESTED. Implementers in this run were otherwise
discriminating (WI-552's two MINORs were queued rather than patched inline —
`intake._OI_ID_RE` is still dead at intake.py:304; WI-566's rework refused a
remedy outright and *proved* with `parse_dispositions` that it would halt the
merge sweep). The asymmetry is in what the reviewer is asked to produce, so
that is where to fix it.

## 2. What this is NOT

- **Not new doctrine.** The rule already ships: the vendored `antidote`
  skill (`scope: kit`) — "What is the smallest change that makes this fix
  unnecessary?" — with PROCESS.md §3's 0→A→B rule as its repo-scale form.
  State it once, reference it; do not restate it in the prompt
  (`CLAUDE.md`, "Dogfood the philosophy").
- **Not a gate.** No finding is refused, downgraded, or blocked for lacking
  the justification. Warn-first doctrine: the discipline is on the remedy's
  *wording*, not on the verdict or any exit code.
- **Not "reviewers must design the fix."** Naming why construction is
  unavailable is cheap; specifying the structural change is not the
  reviewer's job when it exceeds the diff's scope.
- **Not an argument against guards.** Validation at trust boundaries stays
  (the antidote skill says so itself, and the kit's own fail-closed reads —
  an absent OI is NOT satisfied — are correct by construction, not
  defensive accretion). The target is the guard that compensates for a
  *reachable* bad state the design could have made unreachable.

## 3. Done-when

1. `project-trajectory/prompts/reviewer.template.md`'s finding-line contract
   requires, for any remedy that adds a check, guard, warn, or invariant,
   one clause naming why the defect cannot be made unrepresentable instead
   (stricter type, deleted path, single owning boundary) — citing the
   `antidote` skill rather than restating it. The MINOR/`for clarity` arm
   and trust-boundary validation are explicitly exempt.
2. `project-trajectory/prompts/CATALOG.md` regenerated
   (`gen_prompt_catalog.py`); the `REVIEWER` digest is the join key a
   session log's `prompt-sha` names, so a stale catalog is a red bar.
3. A test in `tests/test_prompts.py` pins the clause's presence, in that
   module's existing style (it already guards 33 prompt-template
   properties).
4. The same discipline reaches the adjudicator briefs if and only if it
   applies there — read `adjudicate_brief.py`'s templates before deciding;
   do not widen by reflex, which would be this plan's own failure mode.
5. Recorded so the effect is measurable: the fragment states the
   structural-vs-additive remedy split of the 2026-09-01 run (1 of 13) as
   the baseline a later sitting re-measures against.

## 4. Evidence trail

The run's rounds are under `docs/reviews/wi-543-*`, `wi-552-*`, `wi-553-*`,
`wi-563-*`, `wi-566-*`; the interplay analysis and the accretion trace are
in the log's 2026-09-01 supervised-unpause entry and decisions 47–51. The
amendment-arm gap named in §1 step 3 is recorded there as an unfiled kit
finding and is NOT this row's to fix — this row changes what future rounds
are asked to produce.
