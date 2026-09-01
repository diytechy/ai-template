## 2026-09-01 — WI-567: construction-first remedies wired into the reviewer's finding contract

**What shipped.** `project-trajectory/prompts/reviewer.template.md`'s finding-line
contract now requires, for any remedy whose concrete change ADDS a check, guard,
warn, or invariant, one clause naming why the defect cannot be made
*unrepresentable* instead (stricter type, deleted path, single owning boundary).
It cites the vendored `antidote` skill rather than restating it (CLAUDE.md,
"Dogfood the philosophy"). Warn-first by construction: it binds the remedy's
wording, not the verdict — no finding is refused, downgraded, or blocked for
want of the clause. The MINOR/`for clarity` arm and validation at a genuine
trust boundary are explicitly exempt; the target is only a guard that
compensates for a *reachable* bad state the design could have made unreachable.

**The baseline this is measured against (plan §3.5).** Across the 2026-09-01
supervised-unpause run's thirteen REVIEW-A rounds on five rows, exactly **1 of
13** remedies was structural (WI-543 round 2's `delivery_inventory()`, which
made an omitted shipped file unrepresentable); every other finding's remedy was
additive. The clearest accretion trace is the successor invariant, which took a
`brief`-cell guard → a title-prefix guard enforced in two places → a proposed
*third* guard on the same axis (WI-566's `adjudicate:`-with-`amendment` gap),
where a typed obligation cell written at the mint would have retired the whole
class. This row changes what future rounds are ASKED to produce; a later sitting
re-measures the structural-vs-additive split against the 1/13 baseline.

**Adjudicator briefs (plan §3.4) — deliberately NOT widened.** Read all four
`adjudicate_brief.py` templates. None is in the business of reviewing a code
diff and proposing a guard against a reachable bad state: `adjudicate-amendment`
rules meaning-vs-clarity on before/after cells; `adjudicate-disposition` rules
a lane close's keep/discard split and drafts successors; `adjudicate-conflict`
rules queue collisions; `adjudicate-red-tc` names a red case's cause and drafts
a fix-to-green row. Their "concrete change" clauses are dispositions of a typed
question, not defect remedies that accrete guards. Wiring the clause there would
be widening by reflex — this plan's own named failure mode (§3.4). So the
discipline lands only in `reviewer.template.md`.

**Also regenerated / pinned.** `prompts/CATALOG.md` regenerated
(`gen_prompt_catalog.py`) so the `REVIEWER` digest — the join key a session
log's `prompt-sha` names — is not stale. A test in `tests/test_prompts.py` pins
the clause's presence in that module's existing load-bearing-clause style.
