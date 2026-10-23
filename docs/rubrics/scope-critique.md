# Rubric — Scope critique where a row is born (WI-852)

**Adjudicates:** the scope of one work item as written, at the point it comes
into being: filed by hand, or minted from a lane (a successor draft, a
disposition, a split). It is judged before the row can be claimed.
**Used by:** an independent critic from another model family than the row's
author, rendered from the kit's critique brief by
`review_brief.py critique --rubric docs/rubrics/scope-critique.md`. The artifact
is the spec file and its `specref` target, read beside the registries the S3,
S5 and S6 anchors are judged against (review-churn plan item 12, revision 20):
`docs/requirements/components.toml`, `docs/requirements/interfaces.toml`, the
derived architecture `docs/requirements/components.derived.toml`,
`docs/runtime-flows.md` and `docs/dependencies.md`. Those are registries,
never code; the brief names each, and marks one this repository lacks.

## Intent

The owner's ruling 2 of 2026-10-07 (`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`):
scope is settled where a row is born, by a scope critique, and there is no
lane-size tripwire. A large row may be kept whole on purpose, but that choice
is made once, recorded in the spec, and not re-argued in the lane. The second
question exists because WI-841's verdict file came to release holds and
authorize acts without anyone stating who may write it or what its readers do
with a bad one (`docs/plans/2026-10-07-wi841-retro/PROPOSAL.md` §1 and §2).
S3 to S6, B3 and B4 carry the review-churn plan's owner rulings of 2026-10-11
(`docs/plans/2026-10-11-review-churn/README.md#owner-rulings-2026-10-11`),
cited per anchor. S7 and S2's bounded ruling carry the owner's direction of
2026-10-23: a critique settles a row's scope and never grows it past the
row's intent.

## Anchors

**S1 — Each independently landable deliverable is named.** List every
deliverable that could land on its own. If there is more than one, say which
lands first. The owner may keep them together; the answer is then recorded in
the spec. *Bad:* a Done-when that bundles a mechanism, a new brief class and a
new sitting under one row with no word on which lands first.

**S2 — Authority over a hold, an act or a gate is named.** Say whether any
deliverable gives a file authority over a hold, an act or a gate. If one does,
the spec carries a `## Trust` section before the claim: the file's producer and
what a failed write looks like, every consumer by path, and the ruling for each
input state a supported workflow or the kit's own routes produce (PROCESS.md
§3 "When a guard is owed", linked, not restated). A file a kit script writes
is never malformed by a supported route, so its malformed state is outside
the ruling, as is a hand edit of it (S3). The ruling covers what a model
writes and what a person writes by a supported route, such as a registry.
One ruling the consumers share is preferred to one ruling per consumer.
*Bad:* a verdict file that releases a hold, with no stated reader rule.

**S3 — Coverage is closed** (ruling 1). A promise over an input space is
either an enumerated set with a declared default, or a construction that makes
the space irrelevant: deny by default, or one schema over the whole record.
For an unbounded grammar (shell lines, free text) the spec chooses deny by
default. The answer becomes spec text before the claim, in the Done-when or
the `## Trust` section. A promise reaches only what PROCESS.md §6 "Review
threat model" says a spec's promise reaches, what supported workflows and the
kit's own routes produce: hand-edited kit-written state, hand-chosen name
aliases and sub-second timing windows are outside it unless the spec names
them as inside, and the spec states its bound in those terms. Ask for the
bound, never for coverage of the excluded inputs. *Bad:* a Done-when promising to refuse "any command
that launches a model" with no enumerated set and no default.

**S4 — The planning need** (ruling 9), recorded as the row's `planmode`.
`single` when the row has a `## Trust` section, touches two or more script
families or interface seams, or promises behaviour over an input space; `dual`
only on the existing design-shaping applies-when; `none` for a diff a cheap
test fully specifies, and for a row that only removes code, tests and text,
adding no code path, even where the criteria above say `single`: the plan
step checks a construction, and a deletion constructs none (owner,
2026-10-16). No size threshold.

**S5 — The architectural delta** (item 12, entry point 2). Does the WI add a
state, add a value to a domain, make an output depend on a new input, or cross
a new boundary? Within the row's scope, the spec carries the change. Beyond
it, a refactor row is filed on trunk before the claim.

**S6 — Dependencies are anchored.** Every row this one waits on is in its
`needs`, each with the reason. Any new third-party package, tool or service
has a reviewed row in `docs/dependencies.md` before the build.

**S7 — The scope stays proportionate.** The critique checks the row's scope;
it does not grow it. A recommendation that adds a mechanism (a check, a
refusal, a record or a ledger) names the supported-workflow scenario in
which the row as written fails without it. With no such scenario, the
recommendation is not made. S3's coverage bound, a Done-when gap and an S1
split are not mechanisms under S7. A row whose Done-when changes no
behaviour (a move, an extraction, a deletion) gains no mechanism from its
critique. Work worth doing beyond the row's intent is named as a
separate row to file, never folded into this one. *Bad:* a recommendation
that adds a refusal for a hand-edited kit-written file to a refactor row.

**B1 — A deliverable hidden in prose.** A Context paragraph that commits to
work the Done-when does not list.

**B2 — A split that breaks the minting rule.** A proposed split whose successor
rows would be minted on a work branch rather than filed on trunk before the
claim.

**B3 — A consumer that re-derives a past decision** (ruling 2). A reader that
recomputes a decision from history or from current state, instead of trusting
the record the deciding step wrote in its own commit (PROCESS.md §3).

**B4 — Owner-dependent work not separated** (revision 35). A Done-when that
needs an owner act or credential, mixed with unattended work, with no stated
hold or partial disposition.

## Verdict

One `- [BLOCKER|MAJOR|MINOR] <anchor> -> where/why -> the concrete change ->
@owner` line per finding, each citing an S or a B anchor, then the brief's one
machine line. A finding naming a new failure mode proposes a new `B#` anchor.

Every recommendation is dispositioned before the claim, adopted into the spec
or rejected with a reason (ruling 9), so write each as one concrete change to
the spec, with the scenario that makes it owed in its where/why. Rejection is
the disposition for a recommendation that names no reachable scenario or that
reaches past the row's intent (S7); work past the intent that is worth doing
is filed as its own row (S5). `[TC-HARDEN]` lines and proposed anchors are
not spec recommendations and need no disposition. In every round, severity
is tied to reachability (review-churn item 4): a BLOCKER or MAJOR states a defect in the scope that would reasonably cost
a build or review round in normal use, and a fail-open, data-loss or security
path counts only when a supported workflow or the kit's own routes reach it; a
rare or contrived path is MINOR at most, or dismissed under PROCESS.md §6
"Review threat model". In a confirming round, which checks the adopted dispositions, a new finding is BLOCKER or MAJOR only
if it is fail-open, data loss or a Done-when gap, and a supported workflow or
the kit's own routes reach it; anything else is MINOR. A failed confirmation
keeps its original severity.
