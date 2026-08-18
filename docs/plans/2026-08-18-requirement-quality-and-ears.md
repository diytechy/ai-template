# Requirement quality + the EARS statement pattern (2026-08-18)

**The owner's brief (2026-08-18):** state that requirements use **simple
technical English**, **conform to EARS**, and aim at eight named quality
characteristics — *necessary, singular, unambiguous, complete, verifiable,
feasible, conforming, traceable* — with the "meaning in this repo" column the
brief supplied. Then cross-check the live spine against those definitions and
amend where applicable.

Only one of the eight arrived with wording this repo could not take verbatim:
**Feasible** read "achievable within the Cypress architecture and controller
resources" — a sentence from the embedded project the list came from. The kit is
stack-agnostic ([process.md](../../project-trajectory/PROCESS.md) opening), so it
landed as "achievable within the declared stack, architecture and resource
budget (§9)", which is the same obligation pointed at whatever stack the adopter
declared.

---

## 1. Where each rule landed (and why it landed there)

[`PROCESS.md`](../../project-trajectory/PROCESS.md) §3 is the **only** new home.
That is forced, not chosen: §3 already gated a statement pattern it never wrote
down (the one-`shall` bullet demanded a form the file did not define), so an
adopter was being held to a shape they could not read. The block states the
eight characteristics as a table, the five EARS patterns as a grammar table, and
the split between what a checker settles and what the review does.

| Surface | Change |
|---|---|
| `project-trajectory/PROCESS.md` §3 | The requirement-quality block (+2,664 bytes, flagged + re-stamped in `byte-budget-guard`). The old one-`shall` bullet collapses to a two-line pointer — its enumeration now lives once, in the block. |
| `registries/system-requirements.template.toml` | The `-000` schema row's `requirement` value **is** the EARS grammar now, so an adopter reads the pattern in the file they are filling in. |
| `README.md` | The spine table's SR row, and a "well-formed requirements" bullet under *Why this produces sustainable code* — both linking §3 rather than restating it. |
| `skills/spine-authoring/SKILL.md` | §2 gains **(b2)**: pick the pattern from the obligation, and the three traps (buried condition · near-miss keyword · a condition that is really a response qualifier). §5 gains *the buried condition* as a named failure mode. |
| `scripts/trace_text.py` + `trace.py` | `ears_advisories` — **warn-only**, its own pipe, its own report section and counter. |
| [`enforcement-audit.md`](../enforcement-audit.md) | Two rows: the gating form rules, and the EARS advisory — each with its honest residue named. |
| [`registry-machinery-reference.md`](../registry-machinery-reference.md) | The SR `Requirement` cell row and the advisory-class list. |

**Not touched, deliberately.** `AGENTS.template.md` (9,994 of 10,000 bytes — it
links §3, and restating the rule would cost more than it buys) and
`PROCESS_OPTIONS.md` (the eight characteristics are core, not an opt-in layer).

## 2. Why the EARS rule WARNS and never gates

Which pattern a row *is* — ubiquitous with a qualified response, or event-driven
with the trigger fronted — is a judgement about the obligation, and the same
sentence can be honest in either shape. `SR-006`'s "fail that gate **when** a
required tool is missing" is a response qualifier, not a condition on the row;
fronting it would change the requirement. A gating version would overrule the
author on the one question the author is better placed to answer.

The detector is correspondingly narrow: it reads the **opening** of an SR
`requirement` cell and reports only a condition dressed in a keyword outside
`When`/`While`/`If`/`Where`. A condition buried *after* the `shall` is not
detected, and that is named as the residue in the enforcement audit.

One deliberate difference from the gating form rules beside it: **`Drafted` rows
are in scope.** Those rules skip Draft because an unfinished acceptance
criterion is what Draft means; an opening is finished the moment it is written,
a warn costs a drafter nothing, and both rows this rule found at landing were
Drafted — skipping them would have shipped a guard that had never once fired.

## 3. The cross-check against the live spine

**Method:** every non-example `SR.requirement` opening classified against the
five patterns; the whole population read, not a sample. `LLR` and `TC` are out
of scope by tier — an LLR carries no obligation to pattern (`form_findings`
already refuses a `shall` there) and a TC states a method, not a requirement.

<!-- fig: cmd="python project-trajectory/scripts/trace.py --root ." rev=2026-08-18 -->
**Population: 70 SRs. 68 already conforming** — 66 ubiquitous, 2 event-driven
(`SR-017`, `SR-018`). **2 non-conforming openings**, both `Drafted`, both fixed
here; **1 buried condition** found by hand, fixed here.

| Row | Status | Was | Now | Pattern |
|---|---|---|---|---|
| `SR-154` | Drafted | "**Before** unattended work integrates, the delivered loop content shall obtain…" | "**When** unattended work reaches integration, …" | event-driven |
| `SR-155` | Drafted | "**For** work declared as contested planning, the delivered loop content shall produce…" | "**Where** work is declared as contested planning, …" | optional-feature |
| `SR-043` | Modified | "A PreToolUse subagent-spawn gate shall, **during an unattended run**, refuse…" | "**While** an unattended run is in progress, the delivered subagent-spawn gate shall refuse…" | state-driven |

`SR-043` also dropped `PreToolUse` from its subject. The hook-event binding is
not lost — it lives in `LLR-040`'s `detail`, in `IF-020`'s contract and in
`external.toml`'s crossing, which is where §3's artifact-altitude rule puts it. No row's obligation changed, and no `status` moved (`SR-043` was
already `Modified`, the other two `Drafted`).

**The advisory therefore lands at zero-to-zero**, which is this repo's shipping
bar for a new rule: measured over the real population first, its finds cleared
in the same change, so it guards rather than handing anyone a cleanup list.

### What the cross-check found and did NOT fix

- **`SR-140` carries 3 `shall`** — a *Singular* violation, and a **pre-existing
  gating finding** `trace.py` already reports. [`status.md`](../status.md) names
  "the `SR-140` split" as one of two work items owed before the ratify brief
  regenerates, and the row is `Approved`: splitting it mints ids and moves
  attestation, which is the sitting's act, not this pass's. Recorded, not
  touched.
- **Complete (units/thresholds)** — not mechanized, and not proposed for
  mechanization. The existing `ac_advisories` warns on a comparative with no
  pinned predicate, which is the checkable corner of it; the rest is the
  consistency review's, and §3 now says so in as many words.
- **Necessary / Feasible** — unchanged position: the review's, no proxy metric.
  This is the same refusal `form_findings` already records (the readability-score
  refusal), now stated in the master rather than only in a docstring.

## 4. The external framework — what it is, and the three nuggets

The owner supplied `requirements-framework-usage-1.0.0` (HarmAalbers'
`claude-requirements-framework`) to mine. **It is a homonym, not a peer.** Its
"requirements" are *workflow preconditions* — hook-enforced gates on an agent
session (`commit_plan`, `pre_commit_review`, `adr_reviewed`), satisfied with
`req satisfy <name>` and stored per branch under `.git/`. It has nothing to say
about requirements *engineering*: no EARS, no quality characteristics, no
traceability tiers. Adopting its model wholesale would be a category error, and
most of its surface duplicates machinery this kit already has — its three-layer
config cascade (global → project → local) is this kit's already-ruled dial
ladder (CLI flag > `AGENT_*` env > `stack.ini` > code default).

Three things in it are worth keeping, and only one costs anything:

1. **The scope-lifetime vocabulary** — `session` · `branch` · `permanent` ·
   `single_use` — is a clean way to say what a satisfied precondition is good
   *for*. This kit already has all four without naming them: the per-commit
   floor is `single_use`, an attestation is `branch`-scoped until the
   snapshot-drift rule re-opens it, a derived gate holds until a row changes.
   **Kept as vocabulary only** — recorded here, not minted into the process,
   because naming an axis the kit already implements four ways would be the
   *unwired marker* failure the `spine-authoring` skill warns about.
2. **Fail-open vs fail-closed, stated as a deliberate split.** The framework
   fails **open** everywhere ("errors don't block Claude"). This kit fails
   **closed** at the verification layer (a missing tool fails the gate and is
   never a silent pass — `SR-006`) and **open** at exactly one place, the tool
   gate (`SR-043`: "fail open on any error so a broken gate never wedges the
   tools"). That asymmetry was already right and already written into both rows;
   the comparison confirms it rather than changing it. Worth knowing it is a
   position, not an accident.
3. **Their checklist bar** — *concise, actionable, ordered, 5–10 items* — is the
   same instinct as an acceptance criterion that states an observable condition
   and its threshold. No change owed: the
   [2026-08-17 acceptance-form ledger](2026-08-17-acceptance-form-ledger.md)
   already moved 50 cells onto a stricter version of it (exact boundaries,
   pass/fail conditions, edge cases).

**Explicitly rejected: auto-satisfaction via skills** (running `arch-review`
auto-satisfies four requirements). That is precisely the move
[`status.md`](../status.md) forbids under "never revert a real fix, or sanction a
check, to green a step" — a gate discharged by the act of running the thing that
was supposed to be judged. The kit's `Attest` is human-held and recorded
*because* it cannot be earned by completion.
