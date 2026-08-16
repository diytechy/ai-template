# Blind derivation — TEAM C (hat-aware variant)

**Date:** 2026-08-16
**Team:** C — the HAT-AWARE variant of the clean-room derivation exercise.

## Input set (the complete set read; nothing else in the repo was opened)

1. `README.md` — the `PROJECT-VISION:` tag and the intro material only (stopped
   before the repo-internals sections).
2. `docs/requirements/stakeholder-needs.toml` — 27 need rows (SN-001…SN-012,
   SN-023…SN-029, SN-033…SN-040) plus the file's prose (maturity rule, the
   empty Draft heading, NG-1).
3. `docs/requirements/external.toml` — the depth-0 frame: 5 entities, 6
   crossings (`B-01`, `B-02`, `B-04`…`B-07`), 3 relationships.
4. `docs/requirements/hats.toml` — the hats roster: 13 hats, 8 of which are
   `always` or tag-reachable today, 5 aspect hats shipped OFF.

No SR/LLR/TC/IF registry, no script, no log, no plan, no git history was read.
No reference out of an allowed file was followed.

## The experimental question

Prior runs derived capabilities from inputs 1–3. This run asks: **what
obligations become derivable when the hats roster is a declared derivation
input?** A hat is a disciplinary lens; a need read *through* a hat can produce
an obligation the need's own text does not state. That is the DO-178C
*derived requirement* class — legitimate, but only when the deriving lens is
named and a rationale given, so a reviewer can accept or reject the lens
rather than the conclusion alone.

## Method and guards

- One row per obligation: `C-<HAT>-<n>`, a single *shall*, in
  capability/artifact-class voice — **no filenames**, because this team does
  not know the implementation. Where a need's own acceptance names a script,
  the derived row deliberately re-states the obligation as a class.
- **Parnas & Clements guard.** Each row must hold for *all* acceptable
  implementations. Rows that would have named a mechanism were re-cast or
  dropped.
- **Second-system guard.** Only what the hat's *charter text* professionally
  demands of a *written* need. Where the roster's charter is too thin, or
  out-of-domain, that is recorded as a finding about the roster rather than
  padded with rows.
- **Corroboration is not derivation.** Where a hat's reading merely restates
  what the need's acceptance already says, the row was dropped and the need is
  noted as text-only for that lens.
- **Conditional rows.** The five aspect hats are tag-gated and silent in this
  repo today. Their rows are marked `[CONDITIONAL — hat silent]`: the lens
  derives them, but under the roster's own grammar the hat can never be put to
  these needs as things stand. That gap is itself finding R-2 below.

---

# Part 1 — Derivations, hat by hat

## hat.SECURITY — `always`

> *What secret, credential, or irreversible action does this touch — and which
> requirement says who may reach it?*

**C-SEC-1** · SN-001 — The scaffolding capability **shall** treat any
pre-existing adopter file at a destination path as an irreversible-loss
hazard: it shall either refuse the write or leave the prior content
recoverable, and shall never overwrite silently.
*Rationale:* the need's "never clobbers" is a promise; the security lens asks
which requirement names the authority for an overwrite, and there is none —
so the only safe reading is that no authority exists.
*Observable:* over a destination containing a file at every kit-owned path,
the run modifies 0 of them without either a non-zero refusal or a recoverable
prior copy.

**C-SEC-2** · SN-006, SN-025, SN-027, SN-029 — The system **shall** carry a
declared inventory of the irreversible actions an unattended run can take, and
each entry **shall** name the policy dial or human authority that permits it.
*Rationale:* the charter's core question ("which requirement says who may reach
it") is unanswerable for an autonomous actor unless the undoable set is
enumerated somewhere a reviewer can read.
*Observable:* every irreversible operation reachable from a launch appears in
the inventory with an authority; with all such authorities withheld, a full run
performs 0 of them.

**C-SEC-3** · SN-026 — Provider credentials **shall** be sourced from the
environment or a secret store only, and **shall not** appear in any tracked
artifact, generated view, or session log the system produces.
*Rationale:* SN-026 requires every model selection to be *logged before
launch*; a selection log is exactly where a credential leaks by accident.
*Observable:* a full run with credentials present produces 0 credential-shaped
tokens across all written artifacts and logs.

**C-SEC-4** · SN-009 — The secrets/privacy detection capability **shall**
report a finding by location and class without reproducing the matched secret
value in any output stream or persisted record.
*Rationale:* a detector that echoes what it caught converts a near-miss into a
second, more durable disclosure — the charter's "spends a secret" applies to
the guard itself.
*Observable:* for every detector class, a planted secret yields a finding whose
full output contains 0 occurrences of the planted value.

**C-SEC-5** · SN-024, SN-026 — Content composed for dispatch to an external
model runner **shall** pass the same secrets bar as governed writes before it
leaves the session, and the inclusion rule for that content **shall** be
declared rather than implicit.
*Rationale:* the frame places model providers outside the system
(EXT-005/REL-003); a brief is an unreviewed egress path that no gate on the
write side covers.
*Observable:* a planted credential inside any file eligible for briefing blocks
dispatch; the eligibility rule is readable as a declared set, not inferred.

**C-SEC-6** · SN-005 — Because the local enforcement floor is bypassable by the
session that holds the checkout, the requirement set **shall** name which
authority may bypass it, and **shall** provide a non-bypassable re-run of the
same bar as backstop.
*Rationale:* the charter demands a requirement naming who may reach an
irreversible action; the frame itself records that a local hook floor is
bypassable, so "enforced by hooks" alone names no authority.
*Observable:* a change committed with the local floor bypassed is rejected by
the hosted re-run of the same bar, in 100% of the bypass cases tested.

**C-SEC-7** · SN-028 — A policy dial that governs a security or privacy gate
**shall** fail toward the gate being ENABLED whenever its value is absent,
unreadable, ambiguous, or of the wrong type.
*Rationale:* the need already requires refusal of duplicates and wrong types;
the security lens adds the *direction* of the failure, which the text leaves
open and which is the whole difference between a safe and unsafe refusal.
*Observable:* with the dial home removed, truncated mid-write, or holding a
wrong-typed value, the guarded action is refused rather than permitted, for
every security-class dial.

**C-SEC-8** · SN-034, SN-035 — A root entry point **shall** classify each
action it can start as reversible or irreversible, and **shall not** start an
irreversible one without an explicit confirmation or a declared authorising
dial.
*Rationale:* a front door that makes the sanctioned path the easy path also
makes an undoable path one keystroke away; the charter demands the authority be
named per action.
*Observable:* every listed action carries a reversibility classification; each
irreversible one requires a distinct confirming input in an interactive run and
a declared dial in a non-interactive one.

**C-SEC-9** · SN-002 — Identity in the traceability spine **shall** be
append-only in meaning: a retired identifier **shall not** be re-issued with a
different referent.
*Rationale:* the security reading of a trace spine is that the join *is* the
authorisation record for a gate; recycled ids silently re-point an approval at
work that was never approved.
*Observable:* re-use of any previously retired id is a mechanical finding, and
the retirement record is readable without git archaeology.

## hat.MAINTAINER — `always`

> *Can a reader two years from now tell why this exists, and what would break if
> they deleted it?*

**C-MNT-1** · SN-038 — The purpose record for each supplied file **shall**
state the failure that its removal would cause, not only the requirement id it
maps to.
*Rationale:* an id link satisfies the letter of "why it exists" while leaving
the next reviser unable to tell load-bearing from accident — the exact failure
class this hat listens for.
*Observable:* every inventory entry carries a removal-consequence statement;
entries with a link but no consequence are reported.

**C-MNT-2** · SN-012 — Each opt-in layer **shall** declare, in one home, what
it costs when adopted and what capability is lost when it is not.
*Rationale:* "heavy layers are opt-in" is only maintainable if a later reader
can decide to drop one; without a stated loss, no reviser can safely remove a
layer, so opt-in decays into permanent.
*Observable:* every declared opt-in layer has a purpose plus loss-on-removal
statement; a layer missing either is a finding.

**C-MNT-3** · SN-026, SN-029 — Every policy enum value **shall** have exactly
one normative definition, in one home, and every consumer **shall** read that
definition rather than restate it.
*Rationale:* SN-029's own history records four tables each re-interpreting one
word; the maintainer lens generalises that from an incident to an obligation,
which the need text does not do.
*Observable:* no enum value carries a second, textually different definition
anywhere in the governed artifacts; a duplicate definition is a mechanical
finding.

**C-MNT-4** · SN-028 — Each policy dial **shall** record its default and the
observable consequence of changing it, adjacent to the dial itself.
*Rationale:* one home for the dials solves *where*; it does not solve *why this
value* — a dial whose effect lives only in the session that added it is
undeletable and unchangeable by the next owner.
*Observable:* every key in the dial home has an adjacent default + effect
statement; an undocumented key is reported.

**C-MNT-5** · SN-040 — The partition-rationale record **shall** be
self-contained: readable and re-examinable after every candidate it discusses
has ceased to exist in the tree.
*Rationale:* the need requires the comparison be reproducible; the maintainer
lens adds durability — a rationale that resolves only against transient session
state is exactly the "reason lives only in the session that wrote it" failure.
*Observable:* the record resolves with no reference to any artifact outside the
retained architecture record; a dangling reference is a finding.

**C-MNT-6** · SN-036 — Every declared perspective **shall** be demonstrably
reachable: a perspective whose applicability condition cannot match any real
row **shall** be reported as unreachable, not left silent.
*Rationale:* the strongest form of "why does this exist" for a roster entry is
"has it ever fired"; an unreachable lens is indistinguishable from a deleted
one while still costing every reader attention.
*Observable:* for each declared perspective, either at least one real row
satisfies its condition, or the perspective is flagged unreachable with the
undeclared field named. *(This row's lens indicts the roster it was derived
from — see finding R-1.)*

**C-MNT-7** · SN-023, SN-010 — Every generated view **shall** identify itself
as generated and name the inputs it was generated from.
*Rationale:* a reader two years on must be able to tell a derived surface from
a hand-authored one before editing it; editing a generated file is the single
commonest way this kind of system loses work.
*Observable:* each generated artifact carries a machine-readable
generated-from record; a hand edit to a generated artifact is detectable
without re-running the generator.

**C-MNT-8** · SN-002, SN-037, SN-038 — Where two artifacts must move together,
the pairing **shall** be declared as a named relationship rather than left as a
convention a reviewer is expected to remember.
*Rationale:* SN-037 requires a change to one side of the requirement/interface
pair to include or justify the other; the maintainer lens generalises this — an
undeclared co-move obligation is an undocumented convention, which is precisely
what rots.
*Observable:* each co-move obligation is enumerable; a change touching one side
without the other produces a finding naming both sides.

## hat.TEST-ENGINEER — `always`

> *What mechanical check fails if this is quietly violated — and can that check
> be shown to fail when it should?*

**C-TST-1** · SN-002, SN-004, SN-008, SN-009, SN-010, SN-033, SN-036, SN-037,
SN-038 — Every declared mechanical check **shall** be accompanied by a
known-bad fixture demonstrating that the check fails on a real violation of the
thing it claims to check.
*Rationale:* the charter's second half ("can that check be shown to fail when it
should?") is the whole hat; nine needs each declare a check and none of them
requires the check be proven to bite.
*Observable:* for every declared check, at least one fixture exists on which it
exits non-zero, and the fixture is exercised whenever the check's own logic
changes.

**C-TST-2** · SN-008 — A verdict **shall** enumerate every constituent step
with a three-valued outcome — passed, failed, or could-not-run — and a run in
which any step could not run **shall not** present as a plain pass.
*Rationale:* "a green never hides a skipped check" is the need; the enforcer
question is what makes a hidden skip *detectable*, and a two-valued verdict
cannot express the state that matters.
*Observable:* with any single step's tool removed, the verdict names that step
as could-not-run and the overall outcome is not "pass".

**C-TST-3** · SN-004 — The mapping from gate to required steps **shall** itself
be verified, independently of the steps.
*Rationale:* the enforcer that never looks is here the gate selector: every
step can be correct while the gate requires the wrong subset, and no step-level
test can see that.
*Observable:* a test asserts each gate's required-step set against the declared
table; adding a step to the table without wiring it is caught.

**C-TST-4** · SN-024 — The critique loop **shall** be exercisable end-to-end on
a fixture artifact carrying a seeded, known rubric violation, and **shall** be
shown to produce rework and to terminate.
*Rationale:* a subjective verdict cannot be asserted, but the *machinery* can:
without a seeded violation, a critique loop that always returns "acceptable" is
indistinguishable from one that works.
*Observable:* the seeded fixture drives at least one rework iteration, cites the
seeded anchor id, and the loop terminates within its declared budget.

**C-TST-5** · SN-029 — Each declared failure direction **shall** have its own
test asserting the conservative outcome for that specific failure mode.
*Rationale:* "every failure direction resolves toward more human involvement" is
a claim about a set; a single happy-path test over the set proves nothing about
its members.
*Observable:* one test per enumerated failure mode (unreadable stage,
out-of-range level, wrong-typed dial, absent record), each asserting increased
human involvement.

**C-TST-6** · SN-007 — The kit's own suite **shall** be shown to turn red on a
seeded defect in the capabilities it claims to cover.
*Rationale:* the suite is the enforcer of every other obligation here; an
enforcer whose own sensitivity is unmeasured is the charter's paradigm failure.
*Observable:* a declared set of seeded defects, one per claimed capability area,
each producing a suite failure.

**C-TST-7** · SN-010, SN-023 — Every freshness contract **shall** be
demonstrated failing on a mutated input, not only passing on a matched one.
*Rationale:* a freshness check that compares nothing passes forever; "cannot
silently rot" is exactly the claim that needs a negative case.
*Observable:* mutating any declared input causes the freshness check to exit
non-zero; mutating an undeclared input does not.

**C-TST-8** · SN-005 — The moment-to-tier table **shall** be shown total over
the triggers that exist: a trigger with no declared tier **shall** be a
finding, not a default.
*Rationale:* "one definition of passing per moment" is falsified silently by a
moment nobody mapped; the enforcer must look at the trigger set, not just the
mapped rows.
*Observable:* every declared trigger resolves to exactly one tier; an unmapped
trigger fails the check rather than selecting a fallback.

## hat.FIRST-RUN-ADOPTER — `tags contains "scripts" | "templates" | "process"`

> *Does this hold for a stranger with only the shipped README and examples — no
> context from this project, no one to ask?*

**C-FRA-1** · SN-001 — Every prerequisite of the scaffolding action **shall**
be checked by the action itself, and a missing prerequisite **shall** produce a
message naming the missing thing and the step that obtains it.
*Rationale:* the charter's named failure is "a step whose prerequisite is never
stated"; a stranger has nobody to ask what version of what was assumed.
*Observable:* for each prerequisite, a machine lacking it yields a typed
non-zero exit whose message names the prerequisite and a remedy.

**C-FRA-2** · SN-003 — The stack-swap capability **shall** ship at least one
worked non-reference-stack instance that runs as shipped.
*Rationale:* "re-point the harness at that stack's tools" is a procedure a
stranger cannot validate without an example; an unexampled procedure is the
charter's "example that does not run as shipped" in its absent form.
*Observable:* a shipped non-reference-stack example completes its declared
harness action from a clean checkout, exercised automatically.

**C-FRA-3** · SN-001, SN-002, SN-036, SN-037, SN-038, SN-040 — A freshly
scaffolded, unfilled repository **shall** either pass its harness or fail with
a message naming exactly which artifact the adopter must fill next.
*Rationale:* a stranger's very first action produces a repo full of blank forms;
an unexplained red at that moment is indistinguishable from a broken kit and is
where adoption is lost.
*Observable:* scaffold-then-check on an untouched destination yields either a
zero exit or a non-zero exit naming a specific unfilled artifact — never an
unexplained failure.

**C-FRA-4** · SN-012 — A minimal adoption path **shall** be declared and
exercised end-to-end, so a stranger can reach a working state without deciding
about any opt-in layer.
*Rationale:* proportionality is unusable if the small path must be reconstructed
by reading every layer's documentation first; the undocumented convention here
is "which parts are actually optional".
*Observable:* a declared minimal path exists, names the layers it omits, and
completes green in an automated run.

**C-FRA-5** · SN-034, SN-035 — The root entry points **shall** be identifiable
from a bare directory listing, by name alone, without consulting any
documentation.
*Rationale:* the need promises a front door; a stranger who must read a guide to
find the front door has been handed a prerequisite nobody stated.
*Observable:* a reader given only the root listing correctly maps each universal
contributor action to exactly one entry, and the naming is asserted mechanically
against the declared action set.

**C-FRA-6** · SN-011 — Each admitted non-stdlib dependency row **shall** state
whether adopting the kit obliges the adopter to install it.
*Rationale:* the need distinguishes shipped-tier from kit-internal
dependencies; a stranger reading a ledger row cannot infer which side it sits
on, and guessing wrong is a broken first run.
*Observable:* every ledger row carries an adopter-impact value from a closed
set; a row missing it is a finding.

**C-FRA-7** · SN-024, SN-026 — When a declared quality mechanism degrades to a
weaker mode, the degrade **shall** be visible in the artifact the reader
consumes, not only in a run log.
*Rationale:* a stranger with one model family gets same-family review; if that
fact lives only in a log they will never open, they will read a corroborating
verdict as an independent one.
*Observable:* every verdict record carries the independence status it was
produced under, readable without opening a log.

**C-FRA-8** · SN-039 — The scope vocabulary **shall** be interpretable by an
adopter from the delivered material alone, stating for each value whether the
row is theirs to keep, the kit's own upkeep, or both.
*Rationale:* a declared closed vocabulary still fails the stranger if its values
only make sense from inside this repository — the classic undocumented
convention.
*Observable:* each vocabulary value ships with an adopter-facing meaning; an
adopter can partition a delivered need set with no repo-specific context.

## hat.UNATTENDED-OPS — `tags contains "unattended" | "loop"`

> *What does this look like at 3am with no human — what happens when its input
> is missing, stale, or half-written?*

**C-UNA-1** · SN-006, SN-025 — Every artifact the loop writes and later reads as
authoritative state **shall** be written such that an interruption leaves either
the complete prior state or the complete new state, never a partial one.
*Rationale:* the charter's named failure "a partial write left behind" is fatal
here specifically because the same file is the resume input — a torn write is
read back as truth.
*Observable:* an interruption injected at every write point leaves a state the
next resume parses successfully; 0 partial-parse outcomes across the injected
set.

**C-UNA-2** · SN-025 — When the derived next-work set is empty, cyclic, or
otherwise ambiguous, the run **shall** halt with a distinct typed outcome rather
than select arbitrarily.
*Rationale:* self-direction with no human means the tie-break *is* the decision;
an arbitrary pick at 3am is an unreviewed scope choice that nobody will ever
notice was made.
*Observable:* empty, cyclic and tied frontiers each produce a distinct exit code
and 0 claims.

**C-UNA-3** · SN-027 — A claim on a work item **shall** be bounded, so that a
lane which dies without releasing it becomes reclaimable without human
intervention.
*Rationale:* the need promises crash recovery from history alone; the ops lens
adds the case history cannot express — a lane that is neither finished nor
dead-and-cleaned, which otherwise deadlocks the frontier until morning.
*Observable:* an abandoned claim is reclaimable after its declared bound, with 0
double-assignments observed across injected mid-lifecycle crashes.

**C-UNA-4** · SN-026 — Retry against an external runner **shall** be bounded in
both attempts and total elapsed time, and exhaustion **shall** be a typed end
state.
*Rationale:* "reactive backoff" without a ceiling is the charter's "unbounded
retry" — at 3am an expired credential is indistinguishable from a rate limit,
and one retries forever while the other never succeeds.
*Observable:* with a runner stubbed to refuse every call, the run terminates
within the declared bound and exits the exhaustion code, not a timeout.

**C-UNA-5** · SN-029 — Every stop for a human judgement **shall** append a
durable record naming the decision awaited and where to record it.
*Rationale:* the charter's "a failure that pages nobody": a run that stops
silently at 3am is externally indistinguishable from one that completed, so the
reserved judgement is never made.
*Observable:* every human-held stop produces exactly one durable
awaiting-decision record; the count of stops equals the count of records.

**C-UNA-6** · SN-008, SN-006 — In the unattended path a check that could not run
**shall** be treated as not-passed for gating purposes, with no interactive
fallback available.
*Rationale:* "a green because nothing looked" is the charter's named failure,
and the local lenient degrade the need sanctions has no meaning where no human
requested it.
*Observable:* with any required tool absent, the unattended run's gate outcome
is non-pass and no prompt is issued.

**C-UNA-7** · SN-009 — The always-on secrets floor **shall** run in the
unattended path, and its unavailability **shall** refuse the guarded action
rather than allow it.
*Rationale:* the need's promise is "in every repo without extra setup"; the ops
lens supplies what happens when the guard itself is the missing input — the
silent-degrade case.
*Observable:* with the detection capability unavailable, 0 guarded actions
complete.

**C-UNA-8** · SN-010, SN-023 — A generated surface **shall** carry the
generation moment and an input digest, so staleness is detectable from the
surface itself without re-running the generator.
*Rationale:* at 3am the reader is another automated step; a `--check` exit code
is unavailable to a consumer that only has the artifact.
*Observable:* every generated surface carries both stamps, and a consumer can
determine staleness from the artifact alone.

**C-UNA-9** · SN-005 — A hosted verdict the loop depends on **shall** be
retrievable programmatically, and waiting on one **shall** be a bounded, typed
state.
*Rationale:* a loop that must have a human read a remote page is attended in
practice; unbounded waiting is the charter's unbounded-retry failure wearing a
different coat.
*Observable:* the verdict is obtainable without a human step; a run waiting on
one exits a distinct code at its declared bound.

## hat.CROSS-PLATFORM — `tags contains "scripts" | "launcher" | "shell"`

> *Which of Windows, macOS and Linux breaks this — path separators, line
> endings, console encoding, shell quoting, case sensitivity?*

**C-XPL-1** · SN-034 — Each platform's entry point **shall** be verified by
being executed on that platform, not by being shown to exist.
*Rationale:* the need's acceptance says the entry points *exist* and *launch*;
existence is checkable on one platform and is precisely the rule "true only on
the author's platform, shipped as universal".
*Observable:* every declared entry point is executed to a successful outcome on
each declared platform in an automated matrix.

**C-XPL-2** · SN-011, SN-034 — Line-ending and executable-bit handling for
delivered launchers and hooks **shall** be declared, so a checkout on any
declared platform yields runnable files.
*Rationale:* a shell entry point checked out with CRLF fails to execute with an
error that names nothing useful; this is invisible to a single-platform author.
*Observable:* a checkout performed under each platform's default configuration
yields launchers that execute; 0 interpreter-not-found failures attributable to
line endings or modes.

**C-XPL-3** · SN-001 — The delivered file inventory **shall** contain no two
paths differing only in case, and the scaffolding action **shall** treat path
comparison as case-insensitive when deciding whether a destination is occupied.
*Rationale:* two of the three declared platforms are case-insensitive; a
case-only distinction silently collapses to one file there, and an occupancy
test that is case-sensitive clobbers a file it believed absent.
*Observable:* 0 case-only path collisions in the inventory; an occupancy test
against a differently-cased existing file reports occupied.

**C-XPL-4** · SN-002, SN-010 — Any content digest or textual comparison used in
a freshness or integrity contract **shall** normalise line endings before
comparing.
*Rationale:* otherwise every checkout on one platform reads permanently stale,
which manifests as an unfixable red for exactly one third of adopters.
*Observable:* the same logical content under CRLF and under LF yields an
identical digest and an identical freshness verdict.

**C-XPL-5** · SN-023, SN-034 — Every generated or emitted text artifact
**shall** declare its encoding, and console output **shall** remain legible
under each platform's default console encoding.
*Rationale:* console encoding is named in the charter; a non-ASCII status glyph
that renders as replacement characters turns a status surface into noise on the
platform where the default is not UTF-8.
*Observable:* under each platform's default console configuration, emitted
output contains 0 replacement characters and every generated artifact carries an
explicit encoding declaration.

**C-XPL-6** · SN-027, SN-006 — Isolation and cleanup for parallel lanes **shall
not** assume POSIX file-deletion semantics: removal of a lane's workspace
**shall** succeed or report a typed failure when a file within it is held open.
*Rationale:* deleting an open file succeeds on POSIX and fails on Windows; a
cleanup path tested only on POSIX leaves the frontier permanently blocked on the
other platform.
*Observable:* the crash-and-cleanup path passes on each declared platform, with
lane workspaces reclaimed or a typed failure raised.

**C-XPL-7** · SN-028 — Where two grammars read the policy dials, the
non-Python reading **shall** be exercised under each declared platform's actual
default shell.
*Rationale:* the need pins the two readings equal over adversarial content, but
equality was established under one shell; quoting and word-splitting differ
between shells, and a divergence here silently flips a security gate.
*Observable:* the parity table is green under each declared platform's default
shell, not only the authoring one.

**C-XPL-8** · SN-009 — The detection capability **shall** operate identically on
platform-native path forms, line endings, and non-ASCII filenames.
*Rationale:* a scanner that misses a secret because the staged path used
backslashes is a rule true only on the author's platform, with the worst
possible consequence.
*Observable:* an identical planted secret is detected under each platform's
native path form, both line-ending conventions, and a non-ASCII filename.

## hat.UX-DESIGNER — `always`

> *Who reads this surface, what decision are they making on it, and does the
> layout put that first?*

**C-UXD-1** · SN-023 — The progress-and-connections surface **shall** declare
its reader and the decision it serves, and **shall** answer that decision in its
first screen without interaction.
*Rationale:* the need asks for progress *and* connections in one file — two
different reader questions, and the charter's named failure is a surface that
renders every fact it has instead of the one the reader came for.
*Observable:* the declared primary decision is resolvable within the first
viewport at each declared width, with no scrolling and no interaction.

**C-UXD-2** · SN-008 — A verdict and every qualification of that verdict
**shall** be presented as one visual unit.
*Rationale:* "a reader can believe a green" is a *presentation* claim as much as
a mechanical one; a caveat placed below the fold is not read, and an unread
caveat is a false green in practice.
*Observable:* no run produces a verdict whose skip, degrade or could-not-run
qualification is separated from it by a scroll or a second surface.

**C-UXD-3** · SN-004 — A gate failure **shall** lead with the failing item and
the next action, with supporting detail below it.
*Rationale:* the reader of a failure has exactly one decision — what to fix; a
log-first presentation makes them search for it, which is the charter's failure
exactly.
*Observable:* the first lines of any failure output contain the failing item's
identity and a remediation, ahead of any supporting log.

**C-UXD-4** · SN-029, SN-026 — A stop-for-human notice **shall** name exactly
one required judgement and where to record it.
*Rationale:* the reader arrives with one question — "what do you need from me";
a notice that summarises the run's state instead is a surface answering a
question nobody asked.
*Observable:* every stop notice contains exactly one stated required judgement
and one stated recording location.

**C-UXD-5** · SN-025 — A generated status surface **shall** visually separate
what the machine has already decided from what awaits a human.
*Rationale:* the reader's decision on a self-directing run is solely "is
anything waiting on me"; interleaving derived facts with pending judgements
buries the only actionable class.
*Observable:* awaiting-human items occupy a distinguishable region whose count
is visible without interaction.

**C-UXD-6** · SN-002 — Traceability output **shall** foreground the exceptions —
orphans, malformations, duplicates — ahead of, or independently of, the full
join.
*Rationale:* nobody reads a trace matrix to enjoy it; the decision is "is
anything unlinked", and a full matrix as the primary output is the paradigm case
of rendering every fact.
*Observable:* exceptions are obtainable as the leading output; a run with 0
exceptions does not require reading the matrix to establish that.

**C-UXD-7** · SN-035 — A menu of actions **shall** be ordered by a declared
rationale and **shall** visually distinguish the irreversible entries.
*Rationale:* a menu is a layout; an alphabetical list of a dozen actions with a
destructive one adjacent to a routine one puts the reader's most consequential
decision at the same weight as their least.
*Observable:* the ordering rationale is declared and checkable against the
action inventory; every irreversible entry is distinguished by a non-colour
means as well as any colour.

**C-UXD-8** · SN-010 — Every document **shall** state its audience and purpose
in its opening unit.
*Rationale:* "navigable" is a property of arrival, not only of links resolving;
a reader landing mid-corpus decides in seconds whether this is their document.
*Observable:* a check reports any governed document whose opening unit lacks an
audience-and-purpose statement.

## hat.UX-ENGINEER — `always`

> *Does this hold up at the real widths, themes and content volumes — and what
> does it do when the data is empty, huge, or malformed?*

**C-UXE-1** · SN-023 — The rendered surface **shall** be verified *as rendered*
across a declared matrix of widths and themes; verification by inspecting the
generator's output alone **shall not** satisfy its acceptance.
*Rationale:* this is the charter's named failure verbatim — a view verified only
by reading its generator. A generator can emit correct markup that renders
unusably.
*Observable:* one rendered capture per matrix cell, at minimum the narrowest and
widest declared widths and each declared theme, retained as the acceptance
evidence.

**C-UXE-2** · SN-023 — The surface **shall** remain usable at empty, typical and
pathological data volumes: the primary content **shall not** be clipped,
overlapped, or pushed off-screen, and the page **shall not** scroll
horizontally.
*Rationale:* the charter names empty and huge explicitly; a dashboard tested
only against today's data volume degrades invisibly as the project it reports on
grows, which is the one condition guaranteed to occur.
*Observable:* at zero rows, typical rows, and an order-of-magnitude above
typical, the primary decision remains resolvable, with 0 horizontal page scroll
and 0 clipped primary elements.

**C-UXE-3** · SN-023 — Malformed or partial input **shall** render as a visible,
labelled defect region; it **shall NOT** render as an empty section
indistinguishable from "nothing to report".
*Rationale:* the charter names malformed data; the specific hazard for a *status*
surface is that a parse failure and a clean state look identical, so a broken
input reads as good news.
*Observable:* with a corrupted input row, the affected region displays a labelled
error; an empty-but-valid input and a malformed input are visually distinct.

**C-UXE-4** · SN-010, SN-023 — A surface's staleness **shall** be visible on the
surface itself, in the region the reader is already looking at.
*Rationale:* the freshness contract protects the *pipeline*; the rendered
artifact is read by a human who never runs the check, and a stale surface that
looks current is worse than an absent one.
*Observable:* a surface generated from superseded inputs displays its staleness
within the first viewport at every declared width.

**C-UXE-5** · SN-034, SN-035 — Console output is a rendered view: it **shall** be
verified at real terminal widths and under each platform's default console
configuration.
*Rationale:* the charter's "real widths" is not HTML-specific; a status table
that assumes 200 columns is unreadable in the default terminal every adopter
actually has.
*Observable:* emitted output remains legible with correct alignment at 80
columns on each declared platform, verified from captured output rather than
from the formatting code.

**C-UXE-6** · SN-024 — A perceptual verdict **shall** be rendered upon the
artifact as a reader receives it; a critique whose evidence is the artifact's
source **shall** be refused.
*Rationale:* SN-024 requires an independent critical eye but never says what the
eye must look at; an independent reviewer reading a generator reproduces the
exact failure this hat exists to catch, with an approval stamp attached.
*Observable:* every perceptual verdict record cites rendered evidence; a record
citing only source is rejected by the loop.

## hat.SAFETY — `tags contains "safety"` · **[CONDITIONAL — hat silent]**

> *How can this harm a person, property or the environment if it behaves
> incorrectly, and what requirement bounds that harm?*

**C-SAF-1** · SN-009 — The classes of person-harm this system can cause
**shall** be enumerated, and each **shall** name the requirement that bounds it.
*Rationale:* the need already frames a leaked private identity as
near-irreversible; the safety lens reframes that from a security event to a harm
to a specific person, which is a different question — *whose* harm, bounded by
*what*.
*Observable:* an enumerated harm-class list, each entry naming a bounding
requirement; a class with no bound is a finding.

**Roster finding (SAFETY).** Beyond C-SAF-1 the charter is **out of domain**, not
thin. Its harm vocabulary — person, property, environment — has one reachable
referent in a developer-process kit (identity exposure) and no others; the
irreversible-action hazards it might otherwise reach are already the SECURITY
charter's explicit subject. Deriving further rows here would require stretching
the charter past what it says, which the second-system guard forbids. **1 row.**

## hat.LEGAL — `tags contains "legal"` · **[CONDITIONAL — hat silent]**

> *What licence, contract or regulation constrains this, and does the
> decomposition record which obligation each part discharges?*

**C-LEG-1** · SN-038, SN-001 — Every delivered file **shall** resolve to a
declared licence under which the adopter receives it, and the boundary between
kit-licensed content and adopter-owned output **shall** be machine-checkable.
*Rationale:* the vision statement makes a precise legal promise — the copied kit
stays under its grant, the adopter's produced artifacts are theirs. That
promise is only true if the partition is derivable from the delivery, and
SN-038's inventory is the natural carrier that its own text does not require to
carry it.
*Observable:* every inventoried file resolves to exactly one licence
classification; a file with none, or with two, is a finding.

**C-LEG-2** · SN-011 — Each admitted non-stdlib dependency row **shall** record
the dependency's licence and its compatibility with the grant under which the
kit is redistributed.
*Rationale:* the ledger's declared fields are technical (what it replaces, why
hand-rolling is worse); the legal lens asks the question a redistributor must
answer and the row cannot — the charter's "a dependency whose licence terms
nothing states", exactly.
*Observable:* every ledger row carries a licence and a compatibility verdict; a
row missing either is a finding.

**C-LEG-3** · SN-026, SN-024 — The terms under which repository content may be
transmitted to an external model provider **shall** be recorded per declared
provider, and the decomposition **shall** state which part discharges that
obligation.
*Rationale:* the frame declares model providers external and shows repo content
crossing to them; provider terms constrain that flow, and the charter's named
failure is an obligation assumed to be someone else's.
*Observable:* each declared provider row carries a transmission-terms reference;
a provider enabled without one is a finding.

## hat.DATA-PROTECTION — `tags contains "personal-data"` · **[CONDITIONAL — hat silent]**

> *What personal data does this touch, on what basis, for how long, and who can
> reach it?*

**C-DPR-1** · SN-009 — The personal-data classes in scope **shall** be declared
as a closed, readable set, distinct from the secrets classes.
*Rationale:* the need bundles "secret or private identity" into one floor plus
one gate; the protection lens separates them — a credential and a person's
identity have different bases, different retention, and different people who may
reach them.
*Observable:* the declared class set is enumerable and each entry is classified
credential or personal data; an unclassified class is a finding.

**C-DPR-2** · SN-009 — A record of a personal-data finding **shall** itself
carry a retention limit and an access rule.
*Rationale:* the detection record is the one artifact guaranteed to contain the
personal data it reports on, often in a durable, widely-readable place — the
charter's "personal data crossing a boundary with no retention limit or access
rule", created by the control itself.
*Observable:* every persisted finding record carries a retention bound and an
access rule; an unbounded one is a finding.

**C-DPR-3** · SN-026, SN-024 — The basis on which repository content containing
personal data may be transmitted to an external model runner **shall** be
declared, together with what is excluded.
*Rationale:* authorship metadata — names, addresses, timestamps — is personal
data present throughout a repository's history, and the frame shows repository
content briefed to an external provider. Nothing in any need states a basis for
that crossing.
*Observable:* a declared basis and an exclusion rule exist per provider; content
outside the inclusion rule is provably not transmitted.

**C-DPR-4** · SN-006 — The preflight condition concerning a private author
identity **shall** state what identity data it reads, where that reading is
retained, and who can reach it.
*Rationale:* a check that inspects author identity is itself processing personal
data; the charter asks the same four questions of a guard as of a feature.
*Observable:* the identity data read, its retention, and its reachability are
each declared; retention beyond the run is justified or absent.

## hat.ACCESSIBILITY — `tags contains "a11y"` · **[CONDITIONAL — hat silent]**

> *Can someone using a keyboard, a screen reader, or a low-vision setting
> complete this — and is that stated as a requirement rather than hoped for?*

**C-ACC-1** · SN-023 — The progress-and-connections surface **shall** be fully
operable and fully legible without a pointing device, and its information
**shall** be available to assistive technology.
*Rationale:* the need names a reviewer as its reader and describes only what
renders; the charter's named failure is acceptance stated purely in terms of a
sighted mouse user, which is what SN-023's acceptance is.
*Observable:* every interactive element is keyboard-reachable and
keyboard-operable; the declared primary content is programmatically
determinable.

**C-ACC-2** · SN-008, SN-004 — A verdict, gate outcome or status **shall not**
be conveyed by colour alone.
*Rationale:* "a reader can believe a green" names the system's most important
signal by its colour; if colour is the only channel, the signal does not exist
for a substantial class of readers — including under a monochrome terminal or a
printed record.
*Observable:* every status distinction is recoverable from text or shape with
colour removed, on every surface that carries one.

**C-ACC-3** · SN-023, SN-034 — Rendered surfaces **shall** meet declared
contrast and minimum-size thresholds under every declared theme, and text
**shall** remain readable when the reader's scale is increased.
*Rationale:* this is where perceptual *legibility* becomes a stated threshold
rather than a judgement; the UX pair's charters demand the surface hold up, but
neither names a measurable floor.
*Observable:* declared contrast ratio and minimum-size floors met across every
theme; content remains readable and unclipped at the declared enlarged scale.

**C-ACC-4** · SN-024 — A perceptual rubric **shall** include non-visual
completion criteria.
*Rationale:* a rubric is where taste becomes a requirement; a rubric written in
purely visual anchors institutionalises the sighted-mouse-only acceptance for
every future critique, permanently, under the authority of an independent
review.
*Observable:* every perceptual rubric contains at least one non-visual anchor;
a rubric without one is refused.

## hat.PERFORMANCE — `tags contains "perf"` · **[CONDITIONAL — hat silent]**

> *What is the declared budget here, measured on what, and what happens when it
> is exceeded?*

**C-PRF-1** · SN-027 — The parallel fan-out **shall** declare the throughput
improvement it exists to deliver, measured against the serial semantic, and that
measurement **shall** be repeatable.
*Rationale:* this need's entire justification is throughput — "a frontier that
advances one item at a time idles for no reason" — and it declares no budget
whatsoever. Under the charter this is a speed claim with nothing behind it, and
the machinery's considerable cost is unjustifiable without it.
*Observable:* a declared improvement target measured on a declared workload;
a run failing to meet it is reported rather than silently accepted.

**C-PRF-2** · SN-012, SN-007 — The per-change verification bar **shall** carry a
declared wall-time budget, and exceeding it **shall** be a reported condition.
*Rationale:* "small changes stay cheap" is a performance claim about process
cost; a bar that silently grows past a contributor's patience is abandoned or
bypassed, which converts a performance regression into a correctness one.
*Observable:* a declared budget for the per-change tier; a run exceeding it
emits a reported condition rather than merely taking longer.

**C-PRF-3** · SN-001 — The scaffolding action **shall** declare a completion
budget on a declared reference environment.
*Rationale:* "in one command" is a usability promise with a time dimension; a
first run whose duration is unbounded is where a stranger concludes the tool has
hung.
*Observable:* a declared budget on a declared reference environment, measured in
the automated matrix.

**C-PRF-4** · SN-023 — Generation and rendering of the status surface **shall**
carry declared budgets at the declared maximum data volume.
*Rationale:* the same volume growth that breaks the layout (C-UXE-2) breaks the
generation time; a surface regenerated on every change has a cost that scales
with the project it reports on.
*Observable:* declared generation and first-render budgets, measured at the
declared maximum volume.

---

# Part 2 — Cross-cutting analysis

## 2.1 Row census

| Hat | Reachable today | Rows | Character of the yield |
|---|---|---|---|
| SECURITY | yes (`always`) | 9 | Authority-naming and fail-direction; strongest on the autonomous needs |
| MAINTAINER | yes (`always`) | 8 | Durability of rationale; strongest on the newest needs (SN-036…SN-040) |
| TEST-ENGINEER | yes (`always`) | 8 | The meta-layer: every declared check needs a proof it bites |
| FIRST-RUN-ADOPTER | yes (tags) | 8 | Stranger-completeness; strongest on SN-001/003/012/034 |
| UNATTENDED-OPS | yes (tags) | 9 | Torn state, unbounded waits, silent stops |
| CROSS-PLATFORM | yes (tags) | 8 | Encoding, case, deletion semantics, shell variance |
| UX-DESIGNER | yes (`always`) | 8 | Decision-first layout across *all* surfaces, incl. console |
| UX-ENGINEER | yes (`always`) | 6 | Rendered-not-generated verification; volume and malformed states |
| SAFETY | no (silent) | 1 | Out of domain — see finding R-3 |
| LEGAL | no (silent) | 3 | Licence partition of the delivered package |
| DATA-PROTECTION | no (silent) | 4 | The needs it most obviously governs are unreachable to it |
| ACCESSIBILITY | no (silent) | 4 | Where measurable legibility actually lands |
| PERFORMANCE | no (silent) | 4 | Budgets for claims made entirely in speed terms |
| **Total** | | **80** | 64 reachable · 16 conditional |

## 2.2 The UX-quality question, answered explicitly

**Asked:** does `hat.UX-ENGINEER`, reading SN-023 (a reviewer sees progress and
connections from one dashboard-like file), derive perceptual quality
obligations — legibility, findability, consistency?

**Answer: partly, and the split is instructive.**

- **Legibility — YES, but only conditionally and without a threshold.** The
  charter's "real widths, themes and content volumes" plus "empty, huge, or
  malformed" derives C-UXE-1/2/3: the surface must be *verified as rendered*,
  must not clip or overflow, and must not present malformed data as a clean
  empty state. That is legibility as *robustness*. It does **not** derive
  measurable legibility — contrast ratio, minimum text size, behaviour under
  reader enlargement. Those need a charter that names human perception rather
  than data conditions, and in this roster that charter is ACCESSIBILITY's
  (C-ACC-3) — **which is switched off**. So the roster's answer to "is it
  readable" today is "it doesn't overflow".
- **Findability — YES, but from the OTHER hat.** UX-ENGINEER's charter is
  entirely about conditions the view must survive; it says nothing about what
  the view should say first. Findability comes from UX-DESIGNER — "does the
  layout put that first" and "a surface that renders every fact it has instead
  of the one the reader came for" — yielding C-UXD-1 (declared reader, declared
  decision, first viewport) and C-UXD-6. The pairing works: the roster's two UX
  hats partition cleanly into *priority* (designer) and *robustness*
  (engineer), and each derives what the other cannot.
- **Consistency — NO. Neither hat derives it.** No charter in this roster names
  cross-surface or cross-state coherence: the same fact rendered the same way in
  two places, one status vocabulary across the console and the dashboard, one
  visual treatment for one meaning. UX-DESIGNER asks about a *single* surface's
  priority; UX-ENGINEER asks about a *single* surface's conditions; MAINTAINER
  reaches one-definition-per-enum (C-MNT-3) but that is about *definitions*, not
  *presentation*. This is the clearest hole in the roster (finding R-4).

**Net:** hats do change what a need yields, materially — SN-023 read blind
without hats yields "render both graphs, keep them fresh"; read through the UX
pair it additionally yields a declared reader, a first-viewport decision, a
rendered-evidence acceptance, a volume matrix, and a malformed-vs-empty
distinction. But the roster's perceptual coverage stops at the boundary of
*measurable human perception*, and everything past that boundary sits behind a
tag nobody sets.

## 2.3 Obligations multiple hats derive independently (strong)

These arrived from separate charters without borrowing each other's reasoning.
Independent convergence is the best evidence a derived requirement is real
rather than an artifact of one lens.

1. **Verify the rendered thing, not its generator.** UX-ENGINEER (C-UXE-1) +
   TEST-ENGINEER (C-TST-1: an enforcer that never looks) + ACCESSIBILITY
   (C-ACC-1). Three charters, one obligation.
2. **Every enforcer must be shown to fail.** TEST-ENGINEER (C-TST-1) +
   UNATTENDED-OPS ("a green that is green because nothing looked", C-UNA-6) +
   MAINTAINER (an unproven check cannot be safely retired, C-MNT-1).
3. **A degrade must be visible in the artifact a human reads, not only in a
   log.** UNATTENDED-OPS (C-UNA-5) + UX-DESIGNER (C-UXD-2) + FIRST-RUN-ADOPTER
   (C-FRA-7). Notably each hat reaches it about a different degrade —
   human-stop, skipped check, same-family review.
4. **Fail closed on unreadable policy.** SECURITY (C-SEC-7) + UNATTENDED-OPS
   (C-UNA-6/7). Same rule, two independent reasons: authority and 3am.
5. **Enumerate the irreversible actions and name an authority for each.**
   SECURITY (C-SEC-2) + SAFETY (C-SAF-1, conditional) + UX-DESIGNER (C-UXD-7,
   arriving at the same inventory from the layout question).
6. **Console output is a first-class view.** CROSS-PLATFORM (C-XPL-5, encoding)
   + UX-ENGINEER (C-UXE-5, width) + UX-DESIGNER (C-UXD-3, failure-first).
7. **One declared home per policy meaning, with reachability proven.**
   MAINTAINER (C-MNT-3/6) + TEST-ENGINEER (C-TST-8, an unmapped trigger is a
   finding not a default).
8. **Content leaving to an external model runner needs a declared inclusion
   rule.** SECURITY (C-SEC-5) + DATA-PROTECTION (C-DPR-3) + LEGAL (C-LEG-3).
   Three charters, three different reasons, one boundary control.

## 2.4 Needs no hat's reading enriches (text-only)

- **SN-037 (boundary/interface coverage) — text-only.** Its acceptance is
  already fully mechanical, self-enforcing, and states its own findings
  classes. The only hat that touches it is TEST-ENGINEER, and only through the
  generic C-TST-1 obligation that applies to every declared check. No hat's
  *domain* adds substance. This is a compliment to the need, not a criticism.
- **SN-033 (needs readable by a stakeholder) — text-only in practice.** The
  obvious lens is UX-DESIGNER (a need cell is a reading surface), but every
  candidate obligation — report the row and the phrase, keep a reviewed
  exception list — is already stated in the acceptance. Corroboration, not
  derivation. Two rows were drafted here and dropped under the guard.
- **SN-039 (scope vocabulary) — thinly enriched.** One row only (C-FRA-8), and
  a weak one: the vocabulary must mean something to a stranger.
- **SN-040 (partition rationale) — thinly enriched.** One row (C-MNT-5), on
  durability of the record.

Conversely, the most hat-enriched needs are **SN-023** (5 hats, 11 rows),
**SN-009** (5 hats, 8 rows) and **SN-026** (5 hats, 6 rows) — all three being
needs whose text describes a *mechanism* while their consequences reach into
several disciplines at once.

## 2.5 Findings about the roster itself

**R-1 · The roster, read through its own MAINTAINER and TEST-ENGINEER hats,
indicts itself.** C-MNT-6 says a declared perspective whose condition can never
match a real row must be reported as unreachable rather than left silent. The
roster's own header confesses precisely that defect having occurred once
(a hat keyed on a field the composer does not declare). The obligation is
therefore not hypothetical — it is derived, from the roster, about the roster,
and the roster currently has no mechanism for it. *(The header also states that
nothing gates on a hat today, so nothing would catch a recurrence.)*

**R-2 · The gating level is wrong for derivation-time use — the largest
finding.** Every hat's `applies_when` evaluates fields of a *work item* at
decomposition time (`tags` = Workstream + SafetyClass). Stakeholder-need rows
carry no tags at all. So a hat can only ever read a need *indirectly*, through
whatever work item happens to reference it, and only if that item was tagged.
The consequence is severe and specific:
- DATA-PROTECTION cannot read SN-009 — the repository's privacy need.
- ACCESSIBILITY cannot read SN-023 — the repository's only rendered surface.
- PERFORMANCE cannot read SN-027 — the need whose entire rationale is speed.
In each case the hat that most obviously governs the need is the one hat
guaranteed not to see it. If hats are to be a *derivation* input (this run's
premise), the roster needs either a need-level applicability field or a rule
that a hat applies to a need whose subject matter matches its charter,
independent of any work item's tags.

**R-3 · The header's two-kinds-of-silence taxonomy is missing a third kind.**
It distinguishes silent-by-design (tag-gated, opt-in) from silent-by-defect
(an unsatisfiable predicate). SAFETY is neither: its predicate is fine and its
opt-in is deliberate, but its charter's failure class — harm to person,
property, environment — has essentially no referent in a developer-process kit.
It is **silent-by-domain**. A reader who switches on the `safety` tag expecting
coverage would get one derivable row (identity exposure) and a lot of ceremony,
which is exactly what SN-036 was admitted to prevent. Recommend the roster
either record SAFETY as domain-inapplicable-here-but-shipped-for-adopters, or
cut it from *this* repo's roster and keep it in the shipped template.

**R-4 · No hat carries a consistency / coherence charter.** See §2.2. Nothing
in the roster asks "is this rendered the same way as the same thing elsewhere".
Given the kit has at least three status-bearing surfaces (a dashboard, an
open-items view, console reports) plus a dogfooding obligation between template
and instance, this is a real gap, and it is the gap most likely to produce the
drift that a reader experiences as untrustworthiness.

**R-5 · No hat carries an integrity/recoverability charter independent of the
unattended tag.** Atomic writes, bounded claims, and crash recovery
(C-UNA-1/3) all arrive through UNATTENDED-OPS, which is tag-gated. An
*attended* session that half-writes a registry gets no lens at all, even though
the corruption is identical.

**R-6 · There is no stakeholder or product-fitness hat.** All thirteen charters
are engineering-side. Nothing asks "does this actually serve the stated
vision", "is this need still the need", or "who asked for this". The roster is
therefore excellent at hardening a decomposition and blind to a decomposition
that is faithfully hardening the wrong thing. SN-033 — the one need explicitly
about a stakeholder's own comprehension — ends up text-only (§2.4) for exactly
this reason: no hat professionally owns it.

**R-7 · The `always` set is well chosen.** Not every finding is a criticism:
MAINTAINER, TEST-ENGINEER and SECURITY produced 25 rows between them across
essentially every need, and the UX pair partitions cleanly (§2.2). The four
`always` engineering hats plus the two tag-reachable ops hats carry 80% of the
total yield. The roster's problems are at its edges (the five aspect hats and
the gating level), not at its centre.

## 2.6 The three most surprising hat-derived obligations

1. **C-PRF-1 — the throughput need with no throughput budget.** SN-027's entire
   justification is speed ("a frontier that advances one item at a time idles
   for no reason"), it commissions the most complex machinery in the system
   (lanes, worktrees, a serialised integrator, crash recovery), and it declares
   no measurement of the improvement it exists to deliver. The one hat whose
   charter is exactly "what is the declared budget here, measured on what" is
   switched off. Read through PERFORMANCE, the need is unfalsifiable as written.
2. **C-DPR-3 — authorship metadata crosses to model providers with no declared
   basis.** The frame places model providers outside the system and shows
   repository content briefed to them. Repository content includes commit
   authorship — names and email addresses — which is personal data by any
   reading. No need states a basis, a boundary or an exclusion for that
   crossing. The paired finding C-DPR-2 is sharper still: the *privacy finding
   record itself* is the one artifact guaranteed to contain the personal data it
   reports, and nothing bounds its retention.
3. **C-MNT-6 / R-1 — the roster indicts itself.** Reading SN-036 through
   MAINTAINER derives "a declared perspective that can never fire must be
   reported, not left silent" — an obligation the hats file's own header records
   having violated once, with no mechanism to catch a recurrence, in a repo
   where nothing gates on a hat at all.

*Runner-up:* **C-ACC-2** — the system's single most important signal, the one
SN-008 exists to make believable, is named by its colour. If colour is its only
channel, "a reader can believe a green" is false for a substantial class of
readers before any mechanical question is asked.
