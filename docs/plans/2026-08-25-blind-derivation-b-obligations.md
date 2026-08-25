# WI-508 — Blind architecture derivation, TEAM B

**Axis:** obligations clustered by shared internal signal and shared failure mode.
A module is a cluster of obligations that would all be wrong together.

**Objective held throughout:** serve the declared outputs while minimizing internal
signal overlap and duplicated behaviour — *calls, not lines*.

**Input set:** `VISION.md`, `stakeholder-needs.toml`, `system-requirements.toml`,
`external.toml`, `hats.toml`. Nothing else was read (see §5 for the one
contamination I could not remove).

**Corpus measured:** 75 SR rows, 21 SN rows, 4 boundary crossings (B-01, B-02,
B-04, B-05), 3 external-to-external relationships, 16 hats.

---

## 1. THE MODULE MAP

23 modules, in four bands. Every module below carries a **wrong-together** line —
that line is the axis's evidence for the boundary, and a module without a
convincing one has no reason to exist.

Three of the 23 (M03, M12, M18) are **extracted shared stages**: they exist
because the same behaviour is stated in five to fifteen SR rows, and one home is
the objective's answer. They are where this map's total-behaviour saving is
actually won.

### Band 0 — foundations (read declared text, hand back typed answers)

---

**M01 · Declaration Store**
*Responsibility:* every declared value the system runs on — process policy dials
and the toolchain/capability profile alike — has exactly one home, one parse and
one answer, and a broken, doubly-declared or wrong-typed declaration is refused
rather than defaulted.
*SRs:* SR-031, SR-137, SR-138, SR-007
*In:* declared configuration text (the policy home, the toolchain profile, any
legacy one-word file surviving a migration window); a caller's key request.
*Out:* a typed value; a refusal naming the key and both homes; a migration report
naming what moved and what was left in place.
*Depends on:* M18 (platform-neutral file reading), M03 (refusal rendering).
*Wrong together:* if the grammar narrowing or the type check is wrong, the hooks
and the Python readers disagree about the same dial (SR-031), the shape check
passes a shape only one reader understands (SR-137), the migration deletes a
legacy file whose value never landed (SR-138), and the harness runs a step plan
off a malformed profile (SR-007). One signal — declared text — one failure:
*a policy that reads differently depending on who asked.*
*Hat vocabulary:* SECURITY (`a silent flip of a security gate`), CONSISTENCY (`a
rule the template states one way and the instance another`).

---

**M02 · Registry Carrier & Row Generation**
*Responsibility:* the one representation of every registry row — parse, emit,
convert cell-exactly, mint ids that are never re-issued, and expand a declared
spec cell into registry-valid rows.
*SRs:* SR-147, SR-129, SR-174, SR-024
*In:* registry text; a conversion request; an id request; a permutation spec cell.
*Out:* typed rows; emitted text that re-parses; a cell-exact round-trip verdict; a
newly allocated identity; generated dimensional case rows.
*Depends on:* M18, M03.
*Wrong together:* every one of these fails as *a cell that silently is not what it
was*: a dropped/re-typed cell in a carrier migration (SR-147), a lost cell in the
work-registry conversion (SR-129), an identity handed out twice or re-issued after
a deletion (SR-174), a case set that silently omits a dimension (SR-024). All four
read and write the same signal — the row — and no other module may write one.
*Hat vocabulary:* INTEGRITY-RECOVERABILITY, TEST-ENGINEER (`an enforcer that
passes because it never actually looks`).

---

**M03 · Finding & Severity Contract**  *(owns ZERO SR rows — see §2 and §4/O-1)*
*Responsibility:* the one shape and disposition of every reportable finding —
location attribution (row+cell, or file+line), the declared severity class
(gate / warn / advisory-never-exit), strict-mode escalation, carve-out markers and
exception lists, vacuity when an optional input is absent, and the rule that a
degrade is always named rather than silent.
*SRs:* none. This is the finding, not an oversight in the map.
*In:* a raised finding (class, location, message, replacement vocabulary, declared
severity, applicable carve-outs).
*Out:* a rendered finding line; the run's exit-code contribution.
*Depends on:* nothing.
*Wrong together:* every checker in the map, at once — which is precisely why it is
one module. Eleven SR rows state a fragment of this behaviour as a secondary
clause (SR-149, SR-150, SR-157, SR-158, SR-159, SR-162, SR-163, SR-167, SR-180,
SR-181, SR-182) and not one states it as a subject. SR-158's own acceptance
concedes the dependency: *"A class whose severity is stated at no declaration site
is undeclared, and this row is unsatisfied until it is declared there."*

---

**M18 · Portability & Environment Floor** *(listed in band 0 by dependency; kept
at its number for the coverage table)*
*Responsibility:* the runtime footing every other module stands on — a clean
Python 3.11+ with stdlib plus only ledger-declared dependencies, identical
behaviour across Linux/Windows/macOS, no language-specific token in the shipped
vocabulary, and one way to locate a working interpreter.
*SRs:* SR-034, SR-035, SR-114
*In:* kit source imports; the dependency ledger; platform facts (path separators,
line endings, console encoding, locking, case sensitivity); interpreter candidates.
*Out:* platform-neutral primitives; a resolved interpreter or a clear report that
none resolves; an undeclared-import finding; a language-token finding.
*Depends on:* M03.
*Wrong together:* one platform-specific idiom breaks SR-114 on the platform its
author does not run, invalidates SR-034's clean-3.11 claim in practice, and leaves
SR-035's non-Python adopter unable to pass the shipped checks unmodified. The
frame itself files these together: `external.toml` B-05's note names SR-031,
SR-034, SR-035 and SR-114 as *"package-wide property — a ruled class for a
property of every delivered capability at once."*
*Hat vocabulary:* CROSS-PLATFORM (`a rule that is true only on the author's
platform`), FIRST-RUN-ADOPTER.

### Band 1 — verdicts over tracked state

---

**M04 · Spine Rule Verdict**
*Responsibility:* evaluate the declared rule set over spine and work-registry rows
— joins, integrity, schema, placeholders, requirement form, work-item coherence,
declared scope values, off-spine back-links, and whether a design row's named
realization symbol resolves — and raise a finding per violation.
*SRs:* SR-157, SR-164, SR-015, SR-180
*In:* typed rows (M02); the published rule inventory; the declared strict flag; for
SR-180, the resolution rule off the toolchain profile (M01) and the implementation
units it names.
*Out:* findings (M03).
*Wrong together:* all four are *a broken claim inside the tracked rows that nothing
reports*: an unresolvable join or schema fault (SR-157), a missing or
out-of-vocabulary scope value (SR-164), a budget row whose Refs resolve nowhere
(SR-015), a design row claiming code that does not exist (SR-180). SR-157's own
acceptance declares the rule inventory OPEN — *"A rule added at one of those sites
is in this row's scope by default"* — which is the requirement tier telling the
architecture that these are one module's rules and not four contracts.
*Note:* SR-015 and SR-157 are recorded in the pack as a "deliberate pair" (the
invariant on one row, its checker on another). In this map that pairing dissolves:
one module holds the invariant and the rule that enforces it (see §3, M-dec 13).

---

**M05 · Stage & Approval Authority**
*Responsibility:* derive what stage the project is actually at from artifact states
alone, hold the cumulative human-approval level against that stage, and report an
edit that lowers the derived stage without opening a phase.
*SRs:* SR-049, SR-139, SR-181
*In:* spine artifact state cells (M02); the approval-level dial (M01); the prior
committed state; a tier query.
*Out:* the derived stage value plus its cached basis line (with the pending-
amendment count beside the draft count); a per-tier human-held verdict; a
phase-decrease finding.
*Depends on:* M01, M02, M03.
*Wrong together:* all three are *the project claiming a readiness the tree does not
show*: a hand-set or stale stage (SR-049), a level compared the wrong way or
degrading toward less human involvement (SR-139), a spine edit that regresses the
stage while its rows still claim the settled phase (SR-181). One signal — artifact
states — one failure: the false green SN-008 exists to refuse.
*Hat vocabulary:* SECURITY (`an action nothing can undo with no requirement naming
the authority`), TEST-ENGINEER (`a green that is green because nothing looked`).

---

**M06 · Acceptance Record**
*Responsibility:* record each acceptance as a byte-identical copy riding the same
reviewed commit as the approval, report any text that has moved away from that
copy, and refuse any record written from anything but live text.
*SRs:* SR-140, SR-178, SR-179
*In:* live registry text; the recorded copies; the commit under construction; the
acting reviewer from the commit's own author.
*Out:* an approval record; a drift report (needs included, despite carrying no
status cell); a refusal at the writing commit; a seed refusal on the first record.
*Depends on:* M02 (row text), M03.
*Wrong together:* all three fail as *the baseline lying about what was blessed* —
and the pack's own rationale (SR-140) partitions them as three that fail in
different directions while sharing one signal: the recorded copy. Keeping them in
one module is what makes "the record holds what was actually blessed" decidable
with one comparison instead of three detectors.

---

**M07 · Measurement & Budget Verdict**
*Responsibility:* turn a measured metric into a verdict against its declared
budget, tolerance band or stamped baseline, at the posture that row declares
(gate / warn / report-only), and report a missing measurement as a skip rather
than a pass.
*SRs:* SR-167, SR-182, SR-177
*In:* measured metrics; the run's own recorded telemetry; declared budgets,
tolerances, baselines and per-row postures (M01); the run tier.
*Out:* per-row breach/warn/report verdicts; a named skip where no measurement
exists; the fan-out utilisation lines (lanes configured, lanes occupied, work per
wall-hour).
*Depends on:* M01, M03.
*Wrong together:* all three are *a number that is not being compared to anything*:
a hard-gated breach riding as a tracked number (SR-167), a duplication count with
no baseline to move against (SR-182), machinery justified by throughput that no
instrument measures (SR-177 — whose own rationale says the first run would have
printed `lanes=1`). One behaviour — measure, compare to a declared reference,
dispose per a declared posture — stated three times in the requirements.
*Hat vocabulary:* PERFORMANCE (`a declared budget with no measurement behind it`).

---

**M08 · Derivation Integrity**
*Responsibility:* every derived artifact regenerates byte-stably from tracked
sources alone and offline, the regeneration runs the declared families in
dependency order and commits no partial set, a committed copy that has drifted
from its sources is a finding, and a view whose sources are absent is omitted
rather than emitted empty.
*SRs:* SR-070, SR-173, SR-112, SR-022
*In:* tracked source registries and upstream documents; committed derived copies;
the declared artifact-family dependency graph.
*Out:* regenerated bytes; a drift verdict per artifact; an ordered-run outcome that
stops at the first failure; an omission notice for an absent source.
*Depends on:* M02, M03, M18.
*Wrong together:* all four are *a copy that no longer equals what it claims to be
derived from* — a stale generated view (SR-070), a half-regenerated set that reads
as complete (SR-173), a per-agent skill copy nobody edited (SR-112), a vendored doc
drifted from upstream (SR-022). One signal (source → derived copy), one comparison.
*Consumers of this one comparison, stated in the requirements as if it were theirs:*
SR-049 (stage cache freshness), SR-146 (prompt catalogue `--check`), SR-148 (status
surface freshness gate), SR-158 (stale generated doc). See §4/O-4.

---

**M09 · Architecture Frame Checking**
*Responsibility:* resolve every requirement boundary reference, interface endpoint
pair and signal type against the declared external frame, and report connectivity
gaps between declared components, declared interfaces and the derived module
inventory.
*SRs:* SR-162, SR-159
*In:* frame rows (entities, crossings, relationships); interface rows; component
rows; the derived architecture/module inventory; cross-component imports;
requirement boundary references.
*Out:* hard resolution failures for the strict set; coverage, realization,
endpoint, signal-compatibility and top-view-bound advisories; vacuity where the
optional inventories are absent.
*Depends on:* M02, M03.
*Wrong together:* both are *a promised behaviour whose entry or exit cannot be
located* — an unresolvable crossing citation, an endpoint or signal type missing,
a cross-component edge no declared interface covers, a module resolving to no
endpoint. One signal: the declared frame and the declared seams over it.
*Kept out of M04 deliberately:* if the frame-resolution logic is wrong, SR-162 and
SR-159 are wrong and SR-157's spine joins are untouched. Different signal, so a
different module (§3, S-dec 3).

---

**M10 · Decision Provenance Records**
*Responsibility:* every planning act leaves a machine-readable record of what was
considered and why, checked for completeness — the declared perspectives with an
applicability decision and a produced-or-explicitly-no-finding result, and the
candidate partitions with the objective, constraints, scores, selection and the
human ruling that adopted it.
*SRs:* SR-161, SR-165
*In:* a decomposition or partition act; the declared perspective roster; candidate
partitions and their scores; the human ruling.
*Out:* the record beside the artifacts (in the tracked registry, never session
prose); a finding naming the missing element or the unranked selection.
*Depends on:* M02 (the record is registry rows), M03.
*Wrong together:* both are *a decision whose reason lives only in the session that
made it*: an applicable perspective missing from the record (SR-161), a partition
whose alternatives nobody can re-examine (SR-165). Identical behaviour — write a
structured provenance record, then check the record against a declared inventory
for completeness — over two different inventories.
*Hat vocabulary:* MAINTAINER (`a requirement whose reason lives only in the session
that wrote it`), PRODUCT-FITNESS.

---

**M11 · Authored-Text Honesty**
*Responsibility:* report authored prose that has drifted from what it claims or
speaks a vocabulary the project has retired — dead intra-repo links, a missing or
repeated vision declaration, dangling path/symbol references, a figure without its
provenance, a retired process tag in a live authored surface, and a stakeholder-
need cell written in internal engineering vocabulary — honouring the declared
carve-outs.
*SRs:* SR-158, SR-149, SR-150
*In:* authored prose surfaces and the need `need` cells; link targets; the retired-
vocabulary table and its replacements; carve-out classes, per-line/per-file allow
markers and the reviewed exception list.
*Out:* findings naming file+line or row+phrase (M03).
*Depends on:* M02 (need cells arrive as rows), M03.
*Wrong together:* all three are *a token scan over authored prose with carve-outs*
— and all three fail as the same reader experience: a document that says something
that is no longer true, in words the project no longer uses, to a reader who cannot
check it. Three separate scanners would be three implementations of one behaviour.
*Hat vocabulary:* MAINTAINER (`a second, contradictory definition of the same
word`), PRODUCT-FITNESS (`a need whose subject has moved while its text stayed`).

### Band 2 — composed surfaces

---

**M12 · View Presentation Vocabulary**
*Responsibility:* one declared rendering per concept — type scale step, spacing
rhythm, status/phase/type colour *with* its text or shape cue, node/edge/legend/
detail styling, one interaction idiom per role, accessible name, contrast floor,
and the default-density rule — used by every emitter rather than restated in each.
*SRs:* SR-052, SR-053, SR-054
*In:* a concept token (status, phase, type, node role) and its context.
*Out:* its one rendering, its accessible name, and a contrast-checked pair.
*Depends on:* nothing (leaf).
*Wrong together:* all three fail as *one meaning given two treatments, or given a
treatment a reader cannot perceive*: colour as the only channel (SR-052), a second
vocabulary for an already-styled concept (SR-053), an unreadable density or a
clipped label at real volumes (SR-054). SR-053's failure class is literally the
duplication this module exists to prevent — *"the sweep is closed over every
emitter, so a new emitter joins the bar by existing"* is a requirement asking for
exactly one home.
*Hat vocabulary:* ACCESSIBILITY, CONSISTENCY, UX-DESIGNER, UX-ENGINEER.

---

**M13 · State View Composition**
*Responsibility:* assemble the reader-facing derived surfaces from the tracked
registries — per-tier completeness, the requirement decomposition, planned and
in-flight work and any declared hold; the component/interface graph with
containment and edge-to-container drawing; and the release-gate checklist with its
warn-tier budget rows.
*SRs:* SR-168, SR-169, SR-033
*In:* typed rows (spine, work, component/interface, budget rows); declared holds;
concept tokens from M12.
*Out:* the composed content of one state view and of the release checklist.
*Depends on:* M02, M12, M07 (budget rows), M08 (which owns whether the emitted
bytes are stable, offline and drift-checked).
*Wrong together:* all three are *a reader having to open a second surface to
answer one question* — progress absent (SR-168), connections absent (SR-169), the
warn-tier budgets read by nobody (SR-033). One signal in (registries), one
audience out (the reviewer at the front door).
*Kept as one module although SR-168 and SR-169 fail independently:* SN-023 demands
**one** file carrying both conjuncts; two modules writing one artifact need a
shared assembler anyway, and that assembler is this module (§3, M-dec 5).

---

**M14 · Harness Bar**
*Responsibility:* one definition of passing per moment — run the required steps of
the bar that is next due, at the tier the declared moment-to-tier table assigns,
failing on a missing required tool rather than skipping it, and carrying that same
exit as the verdict wherever the bar is invoked, including the shipped hosted
workflow.
*SRs:* SR-006, SR-151, SR-152
*In:* the derived stage as strictness selector (M05); the step plan and the
moment-to-tier table (M01); the branch-claim signal from history; each step's
outcome.
*Out:* per-step outcomes with named skips; the run's exit code; the shipped
workflow's declared trigger→tier bindings.
*Depends on:* M01, M05, M03; calls M04, M07, M08, M09, M11 as steps.
*Wrong together:* all three are *the bar meaning something different depending on
where it ran* — a step subset that does not match the tier (SR-006), a hosted
trigger invoking a different entry point or tier (SR-151), a job whose verdict is
not the harness's own (SR-152). SN-005's acceptance names the property in one
phrase: *ONE DEFINITION OF PASSING PER MOMENT*.

---

**M15 · Package Manifest & Materialization**
*Responsibility:* the delivered package's own manifest is the single truth about
what ships, where each file lands, why it exists and how it is refreshed — seeding
per profile without clobbering, stamping its provenance, and holding this
repository's own instance structurally identical to the template it ships.
*SRs:* SR-009, SR-010, SR-011, SR-032, SR-036, SR-111, SR-163, SR-166
*In:* the manifest (source → destination, profile applicability, ownership class);
profile selection; the destination tree's current state; kit provenance (commit,
date, dirty flag); SR/SN rows for the purpose join (M02).
*Out:* written or deliberately skipped files; the version stamp; a green freshly
generated scaffold; the take-wholesale / regenerate / preserve classification for a
re-sync; findings for a destination that did not materialize, a stale entry, an
unmapped file, an unresolved purpose reference, and a template-versus-instance
structural divergence.
*Depends on:* M02, M03, M18; calls M01 (the legacy-config migration pass) and
M16/M17 for what it seeds.
*Wrong together:* every one of these fails when the manifest is wrong or stale — a
profile seeding the wrong set (SR-009), a scaffold that is not green (SR-010), a
re-run that overwrites an adopter's file (SR-011), setup content that does not run
(SR-032), a re-sync with no baseline (SR-111) or the wrong classification (SR-036),
an entry naming a file that no longer ships (SR-163), a declared destination a
fresh scaffold does not carry (SR-166).
*Hat vocabulary:* FIRST-RUN-ADOPTER (`an example that does not run as shipped`),
SECURITY (SR-011's overwrite is the irreversible act), MAINTAINER (SR-163: what
would break if they deleted it).

---

**M16 · Root Entry Points**
*Responsibility:* every declared runnable capability is reachable the same way from
the repository's front door — to an interactive operator, to a direct caller naming
one, and to automated discovery — from one declaration, on every supported
platform, including the two universal contributor actions.
*SRs:* SR-046, SR-160
*In:* the declared capability inventory (M01); the caller's mode (menu / named /
listing); the platform; a resolved interpreter (M18).
*Out:* a machine listing in declaration order; the chosen capability's command and
its exit code; guidance on an absent or empty declaration; the documented single
platform-required step where one click is impossible.
*Depends on:* M01, M18; shipped by M15.
*Wrong together:* both fail as *a sanctioned path that needs a remembered command
or a working guess* — a capability declared and unreachable, a launcher carrying
its own copy of a command, a front door that crashes cryptically with no
interpreter. SR-046's acceptance forbids the duplication in so many words: *"the
platform launchers delegate to the one selector rather than carrying commands of
their own."*
*Hat vocabulary:* CROSS-PLATFORM, FIRST-RUN-ADOPTER.

### Band 3 — actors at the boundary and in the run

---

**M17 · Sensitive-Content Guard**
*Responsibility:* every governed write is scanned before it lands — secret classes
always, identity/PII classes when the dial says so — blocked at the commit and the
push moment, named by class and location and never by the matched value, from a
floor that arms itself as part of developer setup.
*SRs:* SR-017, SR-018, SR-019, SR-020, SR-113, SR-176
*In:* the staged diff, the commit message and the outgoing commit range (B-01); the
author identity and its exemptions; the `secrets_scan` and `privacy_check` dials
(M01); a resolved interpreter (M18).
*Out:* an accept/reject verdict back to the session (B-04); a finding identified by
class and location only; an armed hook floor after setup.
*Depends on:* M01, M18, M03.
*Wrong together:* all six are *a credential or an identity crossing the boundary
because the floor was not there, not armed, or told on itself*: the always-on scan
(SR-017), the dialled second axis (SR-018), the commit moment (SR-019), the push
moment (SR-020), a floor that needed a separate opt-in step and so protected only
the contributors who knew (SR-113), and the control publishing what it protected
(SR-176). One signal (content about to become governed state), one direction of
failure (fail closed).
*Honest limit carried in the requirements themselves:* this floor is local and
bypassable, so its claim only holds paired with the hosted re-run M14 owns — see
§4/O-8.
*Hat vocabulary:* SECURITY, DATA-PROTECTION.

---

**M19 · Work Selection**
*Responsibility:* what an unattended run does next is derived from the tracked
registries and version-control history alone, in one declared precedence order,
deterministically, with holds applied only from the declared approval level and no
hand-curated pointer surface anywhere in the derivation.
*SRs:* SR-148
*In:* tracked registries (M02); git history; per-tier holds (M05); each item's
declared safety/policy/plan-mode inputs.
*Out:* an ordered eligible set; a recorded selection per item (class, source
identifier, hold decision); a stated exclusion reason per excluded item.
*Depends on:* M02, M05, M08 (the status surface it reads is generated and
freshness-gated, never authored).
*Wrong together:* SR-148 is one row, but it is the row with the largest acceptance
in the pack and it is genuinely one decision — *what the next work derives from and
in what order*. Its own rationale records that three rows stating this invariant
were consolidated into one; re-splitting the module would restore exactly the
duplication that consolidation removed.
*Hat vocabulary:* UNATTENDED-OPS, PRODUCT-FITNESS (`work justified by the machinery
it continues rather than by an outcome anyone wants`).

---

**M20 · Run Supervision & Bounding**
*Responsibility:* the run's declared limits and its end states — refuse a broken
footing before starting, never block on a prompt, bound what may be set running,
bound a retry, bound a stall, and end every session in a typed outcome that names
which of those happened.
*SRs:* SR-026, SR-027, SR-028, SR-043, SR-171, SR-172
*In:* footing facts (is this a git repo, is an agent CLI present, is the author
private under privacy-check, is another writer holding the lock); declared limits
(spawn-gate dial, backoff bound, stall limit) from M01; provider error signals;
progress marks; subagent-spawn tool payloads.
*Out:* a typed nonzero refusal at preflight; a typed outcome code per end state; a
surfaced wait so a throttled run is distinguishable from a wedged one; a stall
reported as its own outcome; a spawn allow/defer/deny verdict to the session
(B-04), failing open on its own error while never relaxing the human-held override.
*Depends on:* M01, M03, M18.
*Wrong together:* every one is *a run that stops, hangs or proceeds without saying
which* — the exact failure class UNATTENDED-OPS listens for: `a silent degrade, a
partial write left behind, an unbounded retry, a green that is green because
nothing looked`. SN-006 states the cluster in one sentence: declared limits bound
the workers and the irreversible actions, only a human-provided override may relax
them, and a fault in a limit's own enforcement degrades to a recorded condition
rather than a stopped run. SR-043's fail-open arm and SR-171/SR-172's bounded
degrades are that one policy, applied to three limits.

---

**M21 · Session Dispatch & Brief Composition**
*Responsibility:* one resolution of what runs for a given phase and tier, one
rendering of the reviewable prompt it is handed, and one declared rule for what
repository content may be composed into it — with the selection and the render
recorded before launch.
*SRs:* SR-040, SR-146, SR-175
*In:* the in-process phase and tier; the declared per-phase command templates and
the roster row resolved for this phase (the roster and consent state come from
M22's policy, the resolution happens here); shipped prompt template files and their
slots; brief-eligible content under the declared inclusion rule.
*Out:* a launched session; a session record naming the template used, the
fingerprint of what it rendered to, and the selection logged *before* launch; a
refusal on an unknown or unfilled slot or a missing shipped template.
*Depends on:* M01, M08 (the prompt catalogue's freshness), M03.
*Wrong together:* all three are *content leaving for an external runner that nobody
reviewed and no record identifies*: an unreviewable prompt assembled in source
(SR-146), an implicit inclusion rule (SR-175), a phase silently falling back to the
wrong command (SR-040). One signal (what is composed and dispatched), one failure
class: an unreviewed egress path.
*Hat vocabulary:* SECURITY (C-SEC-5, cited in SR-146/SR-175), DATA-PROTECTION,
LEGAL.

---

**M22 · Independent Adjudication**
*Responsibility:* the policy of independence — how many verdicts a piece of work
needs, that they come from sessions that did not author it, drawn from a different
model family wherever one is configured and only while the consent surface is
present, how rival plans are compared and arbitrated, and when a non-converging
round escalates through the declared approval level.
*SRs:* SR-154, SR-155
*In:* the work under review or the row marked for contested planning; the declared
review policy; the declared (family × model × tier) roster and the consent surface;
declared budgets; the approval level (M05).
*Out:* verdicts from non-authoring sessions; a selected decomposition filed
atomically as registry-valid rows (M02); a documented same-family degrade, never a
silent skip; a page through the declared approval level.
*Depends on:* M21 (which launches each session), M02, M05, M01.
*Wrong together:* both fail as *a second opinion that was never independent, or
never happened, and nothing said so* — a reviewer from the author's own family, a
silent skip when only one family is routable, a fallback to a single uncontested
plan. Both carry the same five behaviours (roster resolution, cross-family
preference, pre-launch logging, bounded iteration, escalation); two modules would
be five duplications.
*Hat vocabulary:* UNATTENDED-OPS; SN-024's *"an implementer session cannot judge
its own output."*

---

**M23 · Lane & Integration Seam**
*Responsibility:* ready work runs on bounded, mutually isolated lanes and every
lane narrows back to the integration branch through one serial, fail-closed seam —
which is also the only actor permitted to write the shared derived surfaces — with
every lane close, including a terminal one, leaving one immutable report.
*SRs:* SR-156, SR-144, SR-170
*In:* claims and branch heads; trunk history; the configured lane ceiling; the
declared pause signal; the composed tree.
*Out:* a merged integration branch or a parked red candidate with the queue stopped
loudly; a drained, merged stop under a pause; one immutable per-close report naming
outcome, reason, commit range and keep/discard split; regenerated shared surfaces
(by calling M08) committed only here.
*Depends on:* M02 (identity, rows), M08 (ordered regeneration), M14 (the bar it
runs on the composed tree), M03.
*Wrong together:* all three are *authoritative state left in a condition no reader
can name*: a half-integrated trunk or a claim a dead lane never releases (SR-156),
a close nobody can read or a second close overwriting the first (SR-144), a
parallel writer clobbering a shared derived surface (SR-170). One signal — claim
and branch state reconstructed from version-control history alone — one failure
direction: fail closed, recover from history.
*Hat vocabulary:* INTEGRITY-RECOVERABILITY (`a claim or reservation nothing can
reclaim once its holder is gone`), UNATTENDED-OPS.

---

### Module count, defended

**23 modules for 75 obligations** — mean 3.3 SRs each, largest 8 (M15), three
modules at 2 and one at 1 (M19).

Against the objective:

- **No module fuses unrelated responsibilities.** Every module above names one
  signal it reads or writes and one failure direction. The map's widest module
  (M15, 8 SRs) is wide because eight obligations read the same manifest and fail
  together when it is stale — not because eight capabilities were stacked.
- **The count is held DOWN by three extracted stages, not by fusion.** M03
  (findings/severity), M12 (presentation vocabulary) and M18 (portability floor)
  each replace between 3 and 15 restatements of one behaviour. Remove them and the
  map is 20 modules with the same total behaviour stated many times over — a
  smaller module count and a strictly larger system. This is the "calls, not
  lines" discriminator applied directly.
- **Where a merge would have bought a smaller count, it is recorded and refused
  with a reason** — §3 lists ten refusals, each naming the wide interface the split
  narrows (fail-open vs fail-closed limits, ordinal arithmetic vs git-copy
  mechanics, transport vs review policy, three disjoint checker signals).
- **A reader holds four bands, not 23 names:** declared inputs (M01, M02, M03,
  M18) → verdicts over tracked state (M04–M11) → composed surfaces (M12–M16) →
  actors at the boundary and in the run (M17, M19–M23).

---

## 2. COVERAGE, BOTH DIRECTIONS

### Every SR to exactly one owning module

| SR | Module | SR | Module |
|---|---|---|---|
| SR-006 | M14 Harness Bar | SR-152 | M14 Harness Bar |
| SR-007 | M01 Declaration Store | SR-154 | M22 Independent Adjudication |
| SR-009 | M15 Materialization | SR-155 | M22 Independent Adjudication |
| SR-010 | M15 Materialization | SR-156 | M23 Lane & Integration Seam |
| SR-011 | M15 Materialization | SR-157 | M04 Spine Rule Verdict |
| SR-015 | M04 Spine Rule Verdict | SR-158 | M11 Authored-Text Honesty |
| SR-017 | M17 Sensitive-Content Guard | SR-159 | M09 Architecture Frame Checking |
| SR-018 | M17 Sensitive-Content Guard | SR-160 | M16 Root Entry Points |
| SR-019 | M17 Sensitive-Content Guard | SR-161 | M10 Decision Provenance |
| SR-020 | M17 Sensitive-Content Guard | SR-162 | M09 Architecture Frame Checking |
| SR-022 | M08 Derivation Integrity | SR-163 | M15 Materialization |
| SR-024 | M02 Registry Carrier | SR-164 | M04 Spine Rule Verdict |
| SR-026 | M20 Run Supervision | SR-165 | M10 Decision Provenance |
| SR-027 | M20 Run Supervision | SR-166 | M15 Materialization |
| SR-028 | M20 Run Supervision | SR-167 | M07 Measurement & Budget |
| SR-031 | M01 Declaration Store | SR-168 | M13 State View Composition |
| SR-032 | M15 Materialization | SR-169 | M13 State View Composition |
| SR-033 | M13 State View Composition | SR-170 | M23 Lane & Integration Seam |
| SR-034 | M18 Portability Floor | SR-171 | M20 Run Supervision |
| SR-035 | M18 Portability Floor | SR-172 | M20 Run Supervision |
| SR-036 | M15 Materialization | SR-173 | M08 Derivation Integrity |
| SR-040 | M21 Session Dispatch | SR-174 | M02 Registry Carrier |
| SR-043 | M20 Run Supervision | SR-175 | M21 Session Dispatch |
| SR-046 | M16 Root Entry Points | SR-176 | M17 Sensitive-Content Guard |
| SR-049 | M05 Stage & Approval | SR-177 | M07 Measurement & Budget |
| SR-052 | M12 Presentation Vocabulary | SR-178 | M06 Acceptance Record |
| SR-053 | M12 Presentation Vocabulary | SR-179 | M06 Acceptance Record |
| SR-054 | M12 Presentation Vocabulary | SR-180 | M04 Spine Rule Verdict |
| SR-070 | M08 Derivation Integrity | SR-181 | M05 Stage & Approval |
| SR-111 | M15 Materialization | SR-182 | M07 Measurement & Budget |
| SR-112 | M08 Derivation Integrity | SR-113 | M17 Sensitive-Content Guard |
| SR-114 | M18 Portability Floor | SR-129 | M02 Registry Carrier |
| SR-137 | M01 Declaration Store | SR-138 | M01 Declaration Store |
| SR-139 | M05 Stage & Approval | SR-140 | M06 Acceptance Record |
| SR-144 | M23 Lane & Integration Seam | SR-146 | M21 Session Dispatch |
| SR-147 | M02 Registry Carrier | SR-148 | M19 Work Selection |
| SR-149 | M11 Authored-Text Honesty | SR-150 | M11 Authored-Text Honesty |
| SR-151 | M14 Harness Bar | | |

**Count check:** 75 SR rows in the pack, 75 assignments, no id assigned twice.
Per module: M01=4, M02=4, M03=0, M04=4, M05=3, M06=3, M07=3, M08=4, M09=2, M10=2,
M11=3, M12=3, M13=3, M14=3, M15=8, M16=2, M17=6, M18=3, M19=1, M20=6, M21=3,
M22=2, M23=3. Sum = 75.

### SRs that resisted single ownership — 11, each with the reason

1. **SR-006** — one row carrying three modules' knowledge: the step plan and
   missing-tool refusal are M14's, the *freshness* steps it skips are M08's
   artifacts, and the branch-claim signal that decides the skip is M23's lifecycle
   fact. Assigned to M14 because the observable is the bar's own exit; the other
   two enter as calls.
2. **SR-043** — its signal (a tool-spawn payload intercepted inside a model
   harness) belongs to no other obligation in the pack, and it fails **open** while
   every other guard in the map fails closed. Assigned to M20 on failure-mode
   kinship (SN-006's supervision sentence), not on signal kinship. Alternative: its
   own module, or M17. Recorded as a judgement in §5.
3. **SR-113** — sits exactly between M15 (it is setup content that ships) and M17
   (it is the floor's arming). Assigned to M17 so hook-path/arming knowledge has
   one home and setup calls it; the opposite call duplicates that knowledge.
4. **SR-148** — owned by M19 but constrains four other modules by its own text: it
   forbids a pointer surface (M08/M13), reads holds (M05), reads rows (M02) and
   git history (M23). It is a cross-module invariant wearing a requirement's
   clothes. No split proposed: splitting it restores the duplication its own
   rationale says was consolidated away.
5. **SR-163** — its universe is the manifest (M15) but its work is a
   `file → SR → SN` join, which is M04's kind of rule. Assigned to M15 because it
   shares the *stale-manifest* failure with SR-166; it calls M02 for the join.
6. **SR-166** — reads as M15's, but half of it (this repository's instance
   structurally matching the template it ships) is a **package-wide** property of
   exactly the class `external.toml` B-05 names for SR-031/034/035/114. It is
   arguably M18's or a sixth-capability owner's. Assigned to M15; flagged.
7. **SR-176** — the finding is produced by M17's scanner but becomes durable in
   M21's session record. Assigned to M17 (a finding that never carries its value
   cannot leak downstream), with the seam to M21 named explicitly.
8. **SR-177** — reports on M23's fan-out from telemetry M20/M21 record, but its
   behaviour is measure-and-compare. Assigned to M07.
9. **SR-173** — states an ordering and atomicity guarantee about a regeneration
   run that only M23 is permitted to invoke (SR-170). Assigned to M08 because the
   artifact-family dependency graph must have exactly one owner; M23 calls it.
10. **SR-150** — a rule about one registry cell (M04's signal) implemented as a
    phrase scan over authored prose (M11's behaviour). Assigned to M11 on the
    behaviour; the alternative is recorded in §5.
11. **SR-031 vs SR-137** — the pack records that these two rows already both
    claimed the two-grammars-agree observable and had **textually diverged**. In
    this map the question dissolves (one module owns both), but it is evidence of
    the requirement-level overlap named in §4/O-5.

### Modules owning no SR — exactly one, and it is the finding

**M03 · Finding & Severity Contract.** It is not an invented capability: eleven SR
rows state fragments of it (SR-149, SR-150, SR-157, SR-158, SR-159, SR-162,
SR-163, SR-167, SR-180, SR-181, SR-182), and one of them (SR-158) declares itself
*unsatisfied* until the contract is declared somewhere. Under a per-capability
decomposition this module never appears and its behaviour is written eleven times.
Under this axis it appears immediately, with no owner — which is the answer to the
question the axis was assigned: **this obligation is owned by nobody.** The
remedy is a new SR whose subject is the finding/severity/vacuity contract, not a
different map (proposed shape in §4/O-1).

---

## 3. THE OBJECTIVE APPLIED, DECISION BY DECISION

Each decision names the duplicated behaviour a merge removes, or the wide
interface a split narrows.

### Merges

**M-dec 1 · Toolchain profile folded in with the policy dials (M01).**
Candidates: "process dial reader" (SR-031, SR-137, SR-138) and "stack profile
reader" (SR-007). Both implement the identical behaviour: read a declared file,
type it, refuse a broken one, be the single home so a swap edits only the
declaration. Merging removes a second parse-and-refuse implementation, a second
"one home" rule, and a second refusal vocabulary. The interface stays narrow —
`value(key) → typed value | refusal` — and the caller never learns the file shape,
the two-grammar constraint, or the migration window. *Evidence the split would be
arbitrary:* the pack shows one declared profile carrying the CI moment-to-tier
table (SR-151), the capability inventory (SR-046), a duplication baseline
(SR-182), the symbol-resolution rule (SR-180) and the harness commands (SR-007) —
five unrelated tables, one grammar.

**M-dec 2 · Legacy-config migration into M01, not into the scaffold.**
SR-138's shall names the scaffold generator as the runner. Assigning ownership
there would put the dial vocabulary, the target shape and the never-delete-what-
you-did-not-write rule into a second module. M15 *calls* the migration. Removes:
a duplicate copy of the dial vocabulary.

**M-dec 3 · Three drift checkers into one (M08: SR-070 + SR-112 + SR-022).**
All three are `regenerate/compare a copy against its source and report the
difference`, differing only in what the source is (registries, one neutral skill
source, an upstream doc). Merging removes two implementations of the comparison,
two staleness vocabularies and two refresh commands. Four further rows (SR-049,
SR-146, SR-148, SR-158) then *call* it instead of restating it — see §4/O-4.

**M-dec 4 · Ordered, all-or-nothing regeneration (SR-173) into M08, not M23.**
The seam is the only permitted invoker (SR-170), which tempts an assignment to
M23. Refused: the declared dependency order is knowledge about the artifact
family graph, and M08 already owns that graph. Putting it in M23 duplicates the
graph. *Calls, not lines:* M23 calls `regenerate_all()`; it does not know the
order.

**M-dec 5 · SR-168 + SR-169 + SR-033 into one composer (M13).**
SR-168 and SR-169 fail independently (the pack says so) — but SN-023 requires one
file carrying both, so two owner modules would both write one artifact and would
need a shared assembler underneath. That assembler *is* this module. Merging SR-033
(the release checklist) removes a second "assemble a reader-facing artifact from
registry rows" implementation.

**M-dec 6 · SR-052 + SR-053 + SR-054 into a shared vocabulary (M12), not into the
emitters.** SR-053's own failure class — *one meaning given two treatments* — is
the duplication cost. If each emitter owns its scale, palette, encodings and
idioms, the behaviour is copied per emitter and the uniformity bar becomes an
audit instead of a property. One home makes SR-053's *"a new emitter joins the bar
by existing"* mechanically true. Also narrows the emitters' interface: they ask
for a *concept token*, never a colour.

**M-dec 7 · The hosted bar (SR-151, SR-152) into M14, not into its own module.**
SN-005's acceptance names the property: *ONE DEFINITION OF PASSING PER MOMENT*. A
separate hosted-CI module would be a second home for "what passes at moment M",
which is exactly the duplication SN-005 forbids. Removes: a second moment-to-tier
reading and a second step-outcome vocabulary.

**M-dec 8 · SR-154 + SR-155 into one adjudication policy (M22).**
Both rows independently carry roster resolution, cross-family preference,
log-before-launch, bounded iteration and escalation through the approval level.
Two modules = five duplicated behaviours. The contested-planning round is a
specialisation of "obtain verdicts from sessions that did not author the work",
not a second capability.

**M-dec 9 · One dispatch resolver extracted from SR-040 and SR-154 into M21.**
SR-040 resolves a phase to a command template; SR-154 resolves a phase and tier to
a roster row and logs the selection. Two resolvers decide what runs for one phase
(§4/O-6). M21 owns the single resolution and the pre-launch record; M22 owns the
*policy* the resolution is asked to satisfy (independence, family preference,
count). Removes one resolver; narrows M22's interface to
`need_verdicts(work, policy) → verdicts`.

**M-dec 10 · SR-046 + SR-160 into one entry-point contract (M16).**
The requirements demand the merge outright: *"the platform launchers delegate to
the one selector rather than carrying commands of their own"* (SR-046). Two
launcher families each carrying commands is the duplication; one selector with
platform delegates is the minimum.

**M-dec 11 · The interpreter probe into M18, called by both M16 and M17.**
SR-160's shall states it for launchers; SR-019/SR-020's rationales state the same
behaviour as hook machinery, and SR-160 records the split explicitly (*"It spans
two audiences … and parts along that line"*). One probe, two callers. Removes a
second "run a candidate, report clearly, do not crash cryptically"
implementation — a duplication the requirements consciously accepted.

**M-dec 12 · Permutation expansion (SR-024) into M02.**
A standalone case generator would re-implement row shaping and validation. M02 is
already the only module permitted to write a registry row, so expansion of a
declared spec into registry-valid rows lands there. Same argument admits SR-155's
atomic filing of selected children as a *call* on M02, not a second row writer.

**M-dec 13 · Identity allocation (SR-174) into M02, not M23.**
The id space (shapes, uniqueness, the recorded high-water mark) is M02's. If M23
allocated, the id space would have two owners and non-reuse would live away from
the mark that proves it. The seam's contribution is only the *restriction* that it
is the sole caller — which is SR-170's clause, already in M23. Same reasoning
retires the pack's "deliberate pair" of SR-015 (the PB invariant) and its checker
under SR-157: one module holds both, so the pair collapses to one statement.

**M-dec 14 · SR-158 + SR-149 + SR-150 into one authored-text scanner (M11).**
All three are `scan authored prose for a class of dishonesty, honour declared
carve-outs and an exception list, report at a declared severity`. Three modules =
three scanners, three carve-out mechanisms, three severity treatments. SR-150's
signal is a registry cell rather than a doc file, which is the counter-argument
recorded in §5 — the behaviour won.

**M-dec 15 · SR-161 + SR-165 into one provenance recorder (M10).**
Structurally identical: write a machine-readable record of a planning act, then
check that record for completeness against a declared inventory (the perspective
roster; the candidate/objective/score set) and report the missing element.
Merging removes a second record writer and a second completeness checker. The
inventories differ; the behaviour does not.

**M-dec 16 · SR-163 into M15 with SR-166.**
Both fail when the manifest is stale — SR-166 when a declared destination does not
materialize, SR-163 when an entry names a file that no longer ships. Ownership
follows the shared failure, and the SR→SN join is a call on M02.

**M-dec 17 · SR-113 into M17.**
The floor arms itself; setup calls it. The alternative (M15 owns the arming) puts
hook-path knowledge in two modules, and SR-113's whole point is that a floor
requiring a separate step protects only those who knew about the step.

**M-dec 18 · SR-167 + SR-182 + SR-177 into one measurement verdict (M07).**
All three are `take a measurement, compare it against a declared reference (budget,
tolerance band, stamped baseline, or nothing at all), dispose per a declared
posture`. The postures differ — gate, warn-only, report-only-with-no-target — but a
posture is a *parameter*, not a module. Three modules would be three comparators
and three skip/absence conventions. Note the merge is only safe because M03 owns
severity: without it, folding a gating row and a never-gating row together would
smuggle a disposition decision into the comparator.

**M-dec 19 · SR-043 into M20.**
SN-006 states one supervision policy covering all three of this module's limits:
*declared limits bound the workers it may set running and the actions it takes that
cannot be undone … a fault in the machinery that carries a limit degrades to a
recorded condition, not to a stopped run.* Spawn bounding (SR-043), retry bounding
(SR-171) and stall bounding (SR-172) are one policy applied three times, and a
reader comparing fail-open (SR-043) against fail-closed (SR-027) wants them in one
place. Recorded as a judgement — the signal is genuinely different.

### Splits refused-to-merge

**S-dec 1 · M03 extracted out of every checker.**
Narrows: each checker's interface becomes `raise(finding)` instead of `raise,
classify, tier, escalate, carve out, and decide the exit code`. Removes: up to
eleven implementations of severity and exit-code composition. This is the single
largest total-behaviour saving in the map and it is invisible from a
per-capability axis.

**S-dec 2 · M05 (stage & approval) vs M06 (acceptance record) kept apart.**
Merged, one interface would expose ordinal arithmetic over a rung table, git-
commit-riding byte-copies, a drift comparison and a write-time refusal. The pack's
own SR-140 rationale partitions the three record obligations from the two
authority ones on the same reasoning: *a record that exists and rides its commit
while nothing compares live text against it satisfies one row and not the other.*

**S-dec 3 · M04 vs M09 vs M11 kept as three checkers.**
Disjoint signals — spine rows; frame/interface/component rows plus imports;
authored prose. If the frame-resolution logic is wrong, M09's obligations are wrong
and M04's joins are untouched, which is the wrong-together test failing. A single
"checks" module would present a wide interface whose callers must name the rule
family anyway, and would fuse three inventories that are versioned separately.

**S-dec 4 · M21 (transport) vs M22 (policy) kept apart.**
Merged, one interface exposes prompt-slot rendering *and* "how many independent
reviewers" — an implementer changing the review count would be editing the module
that renders briefs. Split, M22 states the policy and M21 answers `launch(phase,
tier, brief)`.

**S-dec 5 · M17 (fail closed) vs M20's spawn gate (fail open) kept apart.**
Both return a verdict to a session at B-04, which tempts a "session guardrails"
merge. Refused: their fail-safe directions are opposite, so the merged module would
have to expose the direction as a caller-visible parameter — a wide interface over
a thin implementation, precisely inverted from the deep-module rule. The shared
part (emit a verdict) is thin and already covered by M03's finding shape.

**S-dec 6 · M19 (what is next) vs M23 (how it lands) kept apart.**
They fail independently and read different signals (registry precedence vs claim/
branch state). Merged, a caller wanting "the next item" would traverse lane state
to get it.

**S-dec 7 · M14 (bar) vs M07 (measurement) kept apart.**
Merged, the bar carries budget/tolerance/baseline arithmetic and a per-row posture
table. Split, the bar runs a step and reads its exit; M07 decides what a number
means.

**S-dec 8 · M16 (entry points) vs M15 (materialization) kept apart.**
Launchers are shipped files (so M15 seeds them), but "every declared capability is
reachable identically by three kinds of caller" is a *behaviour*, not a file. Merged,
the manifest module would own an interactive selector.

**S-dec 9 · M01 (parse) vs M05 (ordinal semantics) kept apart.**
Merged, the declaration store would own the rung ordering and the fail-safe
direction of an approval comparison. Split, M05's interface is `is_held(tier) →
bool` and its callers (M19, M22) never see a dial.

**S-dec 10 · M02 (representation) vs M04 (rules) kept apart.**
SR-157's acceptance keeps the rule inventory open by design. If rules lived in the
carrier, adding a rule would touch the representation — the change-amplification a
deep module exists to prevent.

---

## 4. OVERLAPS FOUND IN THE REQUIREMENTS THEMSELVES

Fourteen. The first three are the package-wide properties the axis was pointed at:
*a secondary clause in many rows and the subject of none.*

**O-1 · The finding/severity/exit-code contract has no subject.**
Clause in: SR-149, SR-150, SR-157, SR-158, SR-159, SR-162, SR-163, SR-167,
SR-180, SR-181, SR-182 (eleven). Subject of: nothing. Each row invents its own
phrasing — *"warns by default and fails under --strict"* (SR-149, SR-150),
*"advisory classes never change the exit code"* (SR-157), *"the declared warn-or-
gate severity for each class"* (SR-158), *"warn-first with --strict gating"*
(SR-159), *"each as an advisory"* (SR-162), *"the declared warning-to-gating
policy"* (SR-163), *"never gating"* (SR-182). SR-158's acceptance admits the hole
outright. **Proposed shape of the missing row:** *the delivered harness shall
render every finding it raises through one declared contract — location
attribution, a severity class from a closed vocabulary, one strict-mode escalation
rule, declared carve-out markers, and an exit code composed only from the gating
classes.* Every one of the eleven rows then cites it instead of restating it.

**O-2 · "Naming the at-fault row and cell" is stated fifteen times.**
SR-137, SR-138, SR-144, SR-149, SR-150, SR-157, SR-158, SR-159, SR-162, SR-163,
SR-164, SR-165, SR-180, SR-181, SR-182. One behaviour — attribute a finding to a
location — with fifteen phrasings. Same home as O-1.

**O-3 · "Every degrade is named, never silent" is stated eight times and owned
nowhere.** SR-006 (*"reporting SKIP(missing) rather than silently passing"*),
SR-138 (*"named in the report"*), SR-152 (*"no silently skipped required step"*),
SR-154 (*"never a silent skip … never a silent model swap"*), SR-167 (*"a reported
skip, never a silent pass"*), SR-173 (*"skipped with a stated reason"*), SR-180
(*"reported as skipped-with-reason"*), SR-043 (*"fails open (allow) and is
logged"*). This is SN-008's honesty property, and it is the single most-restated
obligation in the pack. It belongs beside O-1 as the same contract's second half.

**O-4 · Derived-copy drift: subject of SR-070, restated by six rows.**
SR-112 (skill fan-out drift), SR-022 (vendored-doc drift), SR-049 (stage cache
freshness), SR-146 (prompt catalogue `--check`), SR-148 (status surface
freshness-gated), SR-158 (stale generated doc under the staleness check). One
behaviour — recompute from tracked sources and compare against the committed copy
— with seven statements and at least three distinct trigger vocabularies
(`--check`, "freshness contract", "staleness check", "detectable and refreshed by
one command"). A minimal map states it once (M08) and the rest cite it.

**O-5 · "Read from a declaration, never a literal" is the subject of SR-031/
SR-137 for policy dials only, and a clause in ten more rows.**
SR-007 (toolchain), SR-043 (dial + override), SR-046 (capability inventory),
SR-139 (level), SR-148 (approval level, declared inputs), SR-151 (moment-to-tier
table), SR-167 (budgets/tolerances), SR-171 (*"the retry count and interval come
from a declared value, never a literal"*), SR-172 (stall limit), SR-180
(resolution rule off the profile), SR-182 (stamped baseline). The property is
identical; only the namespace differs. Related and separately documented in the
pack: SR-031 and SR-137 both claimed the two-grammars-agree observable and had
**already textually diverged** — a live instance of the defect, recorded and
half-fixed.

**O-6 · Two resolvers decide what runs for one phase.**
SR-040 (per-phase command template, falling back to the single declared command)
and SR-154 (a (family × model × tier) row resolved per in-process phase and tier,
cross-family preferred, logged before launch). Neither row cites the other. Both
determine the invocation for one phase; a minimal map resolves once (M-dec 9).

**O-7 · The interpreter probe has two homes by explicit decision.**
Stated in SR-160's shall for launchers and in SR-019/SR-020's rationales as hook
machinery, with SR-160 recording the split as deliberate (*"it spans two
audiences … and parts along that line"*). Under the objective this is one
behaviour with two callers, not two obligations (M-dec 11).

**O-8 · The claim the pair exists to make has no row.**
SR-019 states the local half and says it discharges *"no unchecked write enters
governed state"* only as a pair; SR-152 states the hosted half and points back;
B-04's note in `external.toml` carries the argument. The pair-level claim itself
is the subject of no row — it is a clause in two and a note in the frame.

**O-9 · "Generated artifacts belong to trunk" is encoded four times.**
SR-170 (only the serial seam writes them), SR-173 (ordered, no partial set),
SR-006 (a claimed work branch skips freshness *because* generated artifacts are
trunk-only), SR-148 (the status surface is generated and freshness-gated). Four
rows each re-deriving one placement rule.

**O-10 · All-or-nothing durable writing appears five times with five mechanisms.**
SR-144 (immutable per-close report; refuse a second close; restore every report a
refused multi-close wrote), SR-140 (byte-identical copy riding its approval
commit), SR-179 (refuse a write that is not a copy of live text), SR-173 (commit
no partial set), SR-155 (file selected children atomically). INTEGRITY-
RECOVERABILITY is ruled `always` and its failure class is exactly this; no row
takes the property as its subject.

**O-11 · Vacuity ("an absent optional input costs nothing") is a clause in eight
rows and the subject of none.** SR-009, SR-070, SR-157, SR-159, SR-162, SR-167,
SR-173, SR-180. SN-012 is the parent need; no SR states the property. Same home as
O-1 (the disposition of a check with nothing to look at).

**O-12 · The frame itself concedes the gap this axis found.**
`external.toml` B-05's note lists the capabilities the crossing decomposes into and
adds a **sixth**: *"package-wide property — a ruled class for a property of every
delivered capability at once, which is why SR-031, SR-034, SR-035 and SR-114 each
stay one row in it rather than one per capability."* That is the boundary registry
recording, in advance, that a per-capability decomposition has nowhere to put these.
Two more rows belong in that class and are not listed: **SR-166** (template-versus-
instance structural parity) and **SR-163** (every shipped file maps to an outcome).

**O-13 · Deliberate invariant/checker pairs restate one behaviour across two rows.**
SR-015 (the PB back-link invariant) with SR-157 (the checker that polices it),
recorded in the pack as an *"on-purpose split, not an echo"*. The split is honest
at the requirement tier and is pure duplication at the module tier: the module that
knows the invariant is the module that checks it (M-dec 13).

**O-14 · Two obligations inside one row, flagged by the row itself.**
SR-171 records the question openly: *"Whether surfacing is instead a decision that
fails independently of the retry — a split rather than one obligation — is an open
question for the sitting."* Related: SR-026's acceptance had **minted** two
requirements its shall never stated, which is why SR-171 and SR-172 exist at all.
The pack contains a live example of an acceptance cell growing an obligation, and
one that was caught.

### Obligations present in the needs or the frame with no SR subject at all

- **SN-037's last clause** — *"A reviewed change that alters one side of the
  requirement/interface relationship must include or explicitly justify the
  corresponding change on the other."* SR-162 names it as a **NAMED RESIDUAL** and
  declines it; no other row states it.
- **SN-024's rubric mechanism** — *"a written rubric derived from the SN/SR intent
  (not the possibly-lax TC); the verdict cites numbered rubric anchor ids"*. SR-154
  obtains a critique verdict from a non-authoring session; SR-052/SR-053/SR-054 are
  titled *(rubric-adjudicated)* and carry bars, not the rubric's derivation rule.
  Nothing states where the rubric comes from or that anchor ids must be cited.
- **SN-005's mirror clause** — *"Per-agent configs only mirror the floor, never
  replace it."* No SR forbids a per-agent configuration replacing the floor.
- **SN-012's proportionality doctrine** — *"the proportionality doctrine governs
  LLR/TC granularity."* No SR states it; SN-012 otherwise enters only as the
  vacuity clause of O-11.
- **SN-036's adequacy half** — SR-161 records coverage and provenance and
  explicitly leaves adequacy *"with the independent review"*; SR-154 supplies an
  independent review only for **unattended** work reaching integration. An attended
  decomposition's adequacy review has no row.

---

## 5. HONESTY

### What I recognised, and the contamination I could not remove

I recognise this system's *class* immediately — a requirement-traceability process
kit — and I must disclose something stronger than recognition. **My harness
injected two descriptions of this repository into my context before your brief
arrived:** a project `CLAUDE.md` (naming `project-trajectory/`, `PROCESS.md`,
`docs/status.md`, `docs/log.md`, `scripts/`, `tests/`, the dashboard generator,
`agent-resume`, `docs/process.toml`, `docs/stack.ini`) and a memory index (naming
`agent_loop.py`, `trace.py`, `bootstrap.py`, concurrency work, and past
derivations). I did not read a single file from `C:\Projects\ai-template`, and I
used no path outside the pack directory — but I cannot claim I was blind to the
system's existence or to some of its filenames, and pretending otherwise would be
the exact dishonesty this exercise is built to detect.

How I handled it: **no module in §1 is named after any file, script or directory
in that injected material**, and no assignment in §2 was made because I recall
where something lives. The clusters were built by reading all 75 SR rows, tabling
their signals and their `hat_refs`/`listens_for` failure classes, and grouping on
those two columns. Two specific temptations I refused: (a) B-05's `carries` cell
enumerates delivered script names, and it would have been trivial to make that list
the module list — I did not, and my map deliberately does not align with it (that
enumeration is the *boundary-output* axis, and it is the other team's starting
point, not mine); (b) `external.toml` names a six-way capability decomposition, and
I used only its *sixth* item (the package-wide-property class) and only as
corroboration of a finding I had already reached from the SR clause counts.

### Every place I leaned on a concrete artifact name in a requirement cell

Each is used as **evidence that an obligation and a signal exist**, never as a
module assignment.

1. **`docs/stack.ini`** — named in SR-151 (`[ci-tiers]`), SR-182 (`[dupes-census]`),
   SR-046 (the capability set) and implied by SR-007/SR-180. This is my **largest
   lean**: seeing five unrelated tables cited from one declaration is what convinced
   me the toolchain profile and the policy dials are one behaviour with two
   namespaces (M-dec 1). Without it I would still have merged, but on the weaker
   ground of shared behaviour alone.
2. **`docs/stage`** — SR-006 (*"the strictness selector cached in docs/stage"*),
   SR-049, SR-181. Evidence that the derived stage is a *cached signal with a
   freshness contract*, which is why M05 hands out both a value and a basis line.
3. **`docs/work/active/<branch>/` claim** — SR-006. Evidence that a claim is a
   fact recoverable from branch history, supporting M23's "reconstruct from history
   alone" boundary.
4. **`docs/archive/last_approved/`** — SR-140. Evidence that the acceptance record
   is a *whole-file copy set*, not a ledger — which is why M06 owns three rows
   rather than being a column on M05.
5. **`docs/agents.toml` + `docs/agents-enabled`** — SR-154. Evidence of two
   distinct signals (a roster of pair-rows; a consent surface whose *presence* is
   the switch), which is why M22's interface takes both.
6. **`check_privacy` prints the matched value and writes nothing** — SR-176's
   rationale. Evidence that the scanner produces the finding and something else
   makes it durable; it decided SR-176 → M17 with a named seam to M21.
7. **`tests/test_bootstrap.py`, `tests/test_dogfood_sync.py`,
   `tests/test_ci_tier_declaration.py`** — SR-166, SR-151. Evidence that manifest
   materialization, template/instance parity and the tier declaration are pinned
   separately; it kept SR-166 in M15 rather than dissolving it into M18.
8. **LLR/TC ids cited inside rationales** — LLR-008, LLR-014/TC-014, LLR-021,
   LLR-029/LLR-030, LLR-136, LLR-142, LLR-163, TC-170. Used only as evidence that a
   sub-obligation exists and has *how many parents*. LLR-021 is load-bearing for
   O-7/M-dec 11 (one probe, two parent rows). TC-170's *"asserts `git status
   --porcelain` is NON-EMPTY"* is why M08's guarantee is stated as *commits no
   partial set* rather than *leaves none behind*.
9. **`check.py`, `bootstrap.py` + MAPPING, `agent_loop.py`, `check_vendored.py`,
   `gen_cases.py`, `gen_release_checklist.py`, hooks, launchers** — B-05's
   `carries` cell. Used only to confirm that the capability classes those names
   stand for are real obligations. **Not** used as a module list (see above).
10. **`spine_carrier.py`, `hats.py`, `spine_rules.py`, `derive_stage.py`,
    `bootstrap.copy_if_new`, `RESYNC_PACK`** — named in the pack's own file
    headers and rationales. Used as evidence that a single reader exists per
    registry (supporting M02's one-carrier boundary) and that seeded-then-preserved
    is a distinct materialization class (M15's ownership classification).
11. **`docs/plans/…` and `docs/archive/specs/…` citations** (the C-SEC-5, C-DPR-2,
    C-PRF-1, C-MNT-7, C-UNA-3/5 clause homes; the parallel-dispatch spec). Used only
    as evidence that a hat clause exists behind a row — never followed, never read.

### Judgements the requirements did not determine

Twelve, each with the alternative I rejected:

1. **SR-043 → M20** (run limits) rather than its own module or M17. Alternative:
   a spawn-gate module of its own; the signal genuinely differs from M20's, and I
   merged on SN-006's single supervision sentence instead.
2. **SR-113 → M17** rather than M15. Alternative: setup content owns its own
   wiring, at the cost of hook-path knowledge in two modules.
3. **SR-176 → M17** rather than M21. Alternative: the session-record writer owns
   redaction — arguably closer to where the durable copy is actually made.
4. **SR-150 → M11** rather than M04. Alternative: signal-based ownership (it is a
   registry cell). Behaviour won over signal here, and only here.
5. **SR-024 → M02** rather than a standalone generator. Alternative: a small case-
   generator module; rejected because it would re-implement row shaping.
6. **SR-174 → M02** rather than M23. Alternative: the seam allocates, since it is
   the only actor that may.
7. **SR-173 → M08** rather than M23. Alternative: the seam owns its own
   regeneration order.
8. **SR-177 → M07** rather than M23. Alternative: the fan-out reports on itself.
9. **SR-163 → M15** rather than M04. Alternative: it is a join rule like any other.
10. **SR-033 → M13** rather than M07. Alternative: the budget module emits its own
    checklist section.
11. **M03 declared a module rather than a convention.** Alternative: call it a
    coding convention and leave the eleven rows as they are — which is the status
    quo the derivation is criticising.
12. **Granularity: 23 rather than ~12.** A 12-module map is reachable by merging
    M05+M06, M04+M09+M11, M14+M07, M15+M16, M21+M22 and M19+M23. Every one of those
    merges is refused in §3 with a named wide interface; none of them removes a
    single behaviour, which is the objective's own test.

Two further judgements about the *shape* of the answer: I placed M12 (presentation
vocabulary) as a module rather than a data table because SR-053's *"closed over
every emitter"* clause needs an owner that can refuse a value; and I treated
SR-148 as a whole module rather than distributing its clauses, because its own
rationale records that distributing them is what produced the duplication it was
consolidated to remove.

### Moments I was tempted to look at the live system

Three, all refused. **(a)** SR-157's acceptance defers to *"the rule inventory the
delivered checkers themselves publish"* — the derivation would be sharper if I knew
how many rules that is, and I chose to state the openness as the reason M04 and M02
must stay apart (S-dec 10) instead. **(b)** Deciding whether "the harness" and "the
checkers" are one actor or several: the SR text calls both *the delivered harness*
and I could have settled it in one glance; I settled it on the wrong-together test
instead, which gave M14 as a step *runner* and M04/M09/M11 as step *contents*.
**(c)** SR-159's *"generated architecture inventory"* — I do not know what produces
it, so M09 declares it as an input signal without an owner in this map; if it is
generated from the component registry it is M08's output, and I flag that as the one
loose edge in the dependency graph. Mechanically, my working directory *is* the live
repository and every relative path would have landed inside it; I used absolute
paths into the pack directory for all five reads and made no other file access.
