# TEAM A — outputs-backward derivation

Input set: the five files of `wi508-requirements-pack/` and nothing else.
Corpus measured: **75 SR rows**, 27 SN rows, 16 hats, 11 frame rows (4 entities,
4 crossings B-01/B-02/B-04/B-05, 3 relationships).

## 0. How the axis was run (method, so the map is checkable)

The frame declares exactly **two outward crossings** and **two inward** ones:

| crossing | dir | what crosses |
|---|---|---|
| B-01 | in | governed writes, admitted only through the hook floor |
| B-02 | in | authority — rulings, attestations, Status flips |
| B-04 | out | guardrail verdicts during a session |
| B-05 | out | THE TEMPLATE — the packaged deliverable |

I worked each **outward** crossing backwards to the internal signals it cannot be
produced without, then asked of every signal: *does a second output reach this
same signal by a second path?* Every "yes" is either a merge decision (§3) or a
requirements-level overlap (§4). The inward crossings were used only to fix what
the outward ones consume: B-01 supplies the staged content the B-04 verdict is
computed over, and B-02 supplies the approval level and the acceptance act that
the B-05 harness verdict and the B-02 record are computed over.

Backward from **B-04** (two named verdict classes, hook accept/reject and
subagent allow/deny) the irreducible signals are: a resolved policy dial, a
sensitive-content classification, a registry-rule finding, a repository-history
fact (what is staged / what is outgoing), and a verdict shape. Backward from
**B-05** the package splits into two families that behave completely
differently: the package **as an artifact** (does it exist, land, and hold
package-wide properties) and the **behaviour of the content inside it** (harness,
loop, generators, hooks). Every one of the B-05 content capabilities re-consumes
the same five signals B-04 needs. That single observation is what produced the
foundation layer, and it is the whole yield of this axis.

---

# 1. THE MODULE MAP

**24 modules, in 6 layers.** Layer names are for reading only; the module is the
unit. Every module is stated as: responsibility · SRs owned · in-signals →
out-signals · depends on.

### Layer F — Foundation (signals that more than one declared output needs)

**F1. Declaration Reading**
Responsibility: resolve any declared configuration value — process dial,
toolchain profile, tier table, capability inventory — to a typed answer or a
refusal, from the one home per value, under every reader grammar that must read
it.
Owns: **SR-007, SR-031, SR-137, SR-138**.
In: the declaration files; the legacy one-word files. Out: `value(key) → typed |
REFUSAL(key, both homes)`; a migration report; the two-grammar agreement
property.
Depends on: nothing (deliberately: one of its two grammars must work on a box
with no Python).

**F2. Registry Carrier**
Responsibility: one parse of every registry tier into typed rows, and any
representation change proven cell-for-cell before it becomes authoritative.
Owns: **SR-129, SR-147**.
In: registry files. Out: typed rows (ids, ref arrays, absent-vs-empty
distinguished), the joined SN→SR→LLR→TC graph, parse errors, round-trip verdict.
Depends on: nothing.

**F3. Repository History Facts**
Responsibility: every question answered by reading version control, asked once.
Owns: **SR-111**.
In: the repository. Out: is-a-repo, HEAD-present, staged diff, commit message,
outgoing range, *is this a claimed lane* (from branch history), trunk claim and
queue state, commit SHA/date/author, tree-dirty, recorded high-water mark, prior
committed state of a path.
Depends on: nothing.

**F4. Sensitive-Content Classification**
Responsibility: own the pattern classes and produce findings that identify
themselves by class and location and never by the matched value.
Owns: **SR-017, SR-018, SR-176**.
In: a text region; the privacy/secrets dials (F1); the exempt-identity list.
Out: `finding(class, location)` — the only representation that ever leaves the
module.
Depends on: F1.

**F5. Finding & Verdict Shape**
Responsibility: the one representation of a finding (row+cell or file+line, class,
declared severity) and the one arithmetic from a set of findings to an exit code
(advisory never joins the exit; a strict flag promotes its declared family).
Owns: no SR of its own — see §2. It is the interface every checking module in
Layer V publishes through, and it is named as a module because thirteen SRs
restate its contract (§4 O2).
In: findings. Out: a verdict (exit code + attributed report).
Depends on: nothing.

### Layer A — Authority and the derived state of the spine

**A1. Stage & Approval Authority**
Responsibility: answer "which tier is in process, and is that tier a human's?" —
derive the stage from artifact states alone, cache it with a freshness contract,
carry the pending-amendment count beside the draft count, hold the cumulative
approval level against that stage, resolve every unreadable input toward more
human involvement, and refuse an authoring edit that drops the effective stage
without opening a phase.
Owns: **SR-049, SR-139, SR-181**.
In: typed spine rows (F2); the acceptance-drift signal (A2); the approval-level
dial (F1); prior committed state (F3). Out: `stage`, `per-tier completeness`,
`human_held(tier) → bool`, the freshness verdict, the phase-drop finding.
Depends on: F1, F2, F3, A2.

**A2. Acceptance Record**
Responsibility: what an acceptance record *is* — a byte-identical copy riding the
approval commit — plus the one definition of *movement*, the report of text that
has moved, and the refusal of any record write that is not a copy of live text.
Owns: **SR-140, SR-178, SR-179**.
In: live registry text (F2); the recorded copy; commit identity (F3); the
derived-copy comparison (D1). Out: `drift(row) → moved|still`, `record_write_ok →
bool`, the acceptance report (transition, acting reviewer, commit).
Depends on: F2, F3, D1.

### Layer V — Verdict production (the B-04 and B-05 harness outputs)

**V1. Harness Step Plan**
Responsibility: decide which steps run for the bar being asked for, run them,
turn a missing required tool into a failure rather than a skip, honour the one
sanctioned lenient degrade, skip the freshness family on a claimed lane with a
stated reason, and aggregate step outcomes into one exit.
Owns: **SR-006**.
In: the bar requested; the stage (A1); the toolchain profile (F1); is-claimed-lane
(F3); step verdicts (V2–V5, D1, M1). Out: the harness verdict.
Depends on: F1, F3, F5, A1.

**V2. Enforcement Floor**
Responsibility: the agent-neutral floor at the moment of an act — which checks
run at which git hook, the spawn-gate decision, the honest statement that a local
floor is bypassable, and the hosted re-run that is its other half.
Owns: **SR-019, SR-020, SR-043, SR-151, SR-152**.
In: staged content / outgoing range (F3); classifications (F4); registry-rule
findings (V3); the record-write verdict (A2); the spawn dial and launcher-held
override (F1); the moment-to-tier table (F1). Out: **B-04** accept/reject and
allow/deny; the shipped workflow's declared trigger→tier→entry-point contract.
Depends on: F1, F3, F4, F5, V1, V3, A2.

**V3. Spine Rule Checks**
Responsibility: every rule whose source signal is the spine and work registries —
joins, integrity, schema, placeholders, requirement form, work coherence, the
declared scope value, package-coverage mapping, and whether a design row's named
realization symbol resolves in a unit it names.
Owns: **SR-157, SR-163, SR-164, SR-180**.
In: typed rows and the join (F2); the shipped-file inventory (P1); the resolution
rule from the toolchain profile (F1); the source tree. Out: findings.
Depends on: F1, F2, F5, P1.

**V4. Architecture Frame Checks**
Responsibility: every rule whose source signal is the declared frame — boundary
references, interface endpoint pairs and the discrete/variable signal vocabulary,
connectivity gaps, uncovered crossings, the top view's bound.
Owns: **SR-159, SR-162**.
In: frame, component and interface rows (F2); the generated architecture
inventory (G1). Out: findings, vacuous where an inventory is absent.
Depends on: F2, F5, G1.

**V5. Authored-Prose Checks**
Responsibility: every rule whose source signal is authored prose — intra-repo
links, the single vision declaration, dangling path/symbol references, figure
provenance, retired process vocabulary, and stakeholder-language purity — each at
its declared severity, with the declared carve-outs.
Owns: **SR-149, SR-150, SR-158**.
In: prose surfaces; need cells (F2); the staleness signal (D1). Out: findings.
Depends on: F2, F5, D1.

**M1. Measurement & Budget Verdicts**
Responsibility: the one path from a measured number, through a declared baseline
or budget, to a declared response — and the invariant that a measurement row
stays traceable to what it constrains.
Owns: **SR-015, SR-033, SR-167, SR-177, SR-182**.
In: measured metrics; declared budgets, tolerances and stamped baselines (F1);
run telemetry (U1). Out: per-row breach/warn/skip findings; the release-gate
checklist content; the fan-out utilisation report.
Depends on: F1, F2, F5, U1.

### Layer D — Derived artifacts

**D1. Derived-Copy Integrity**
Responsibility: the one answer to "does this committed derived copy still equal
what its declared sources would produce now?", plus the properties a derived
artifact must hold — offline, self-contained, byte-stable, and omitted rather
than emitted empty when its source registry is absent.
Owns: **SR-022, SR-070, SR-112**.
In: declared sources; the committed copy. Out: `equivalent(copy, sources) →
bool + delta`; the refresh action; the omission decision.
Depends on: F2, F5.

**G1. State View Composition**
Responsibility: what the state view must *show* — completeness, the requirement
decomposition to its leaves, planned and in-flight work, any declared hold, and
the components-and-interfaces graph with containment, edge-to-container drawing,
and a stated empty view.
Owns: **SR-168, SR-169**.
In: typed rows and the join (F2); stage and per-tier completeness (A1); work
rows; component/interface rows. Out: the emitted views; the architecture
inventory V4 checks.
Depends on: F2, A1, G2, D1.

**G2. View Presentation Vocabulary**
Responsibility: the single declared token set and interaction idiom every emitter
renders through — type scale, spacing rhythm, status/phase/type colour with a
non-colour cue, node/edge/legend/panel styling, one idiom per node role,
keyboard reachability and accessible naming, the contrast floor, and the
collapse-by-default density rule.
Owns: **SR-052, SR-053, SR-054**.
In: a concept to render. Out: tokens, names, focus order, collapse decision.
Depends on: nothing.

**G3. Decomposition Coverage & Provenance**
Responsibility: prove that a decomposition covered the space it declared —
expand a declared dimensional spec into concrete cases, and leave a
machine-readable record of the declared perspectives or candidate partitions,
each element of which is reportable when missing.
Owns: **SR-024, SR-161, SR-165**.
In: the declared perspective roster; the declared objective, constraints and
scores; a permutation spec. Out: concrete cases; the provenance record; missing-
element findings.
Depends on: F2, F5.

### Layer U — Unattended operation

**U1. Run Lifecycle**
Responsibility: how a run starts, survives and ends — headless resume with stdin
closed, preflight refusal of a broken footing, one writer per checkout, typed
outcome per end state, bounded backoff on a declared transient limit, and a
stall ended as its own outcome.
Owns: **SR-026, SR-027, SR-028, SR-171, SR-172**.
In: footing facts (F3); declared limits (F1); the assignment and committed
trailer evidence. Out: typed outcome codes; the run surface (wait visible, stall
distinct); per-session telemetry.
Depends on: F1, F3.

**U2. Work Selection**
Responsibility: what the next work derives from and in what order, deterministically
— and that no hand-curated pointer surface participates.
Owns: **SR-148**.
In: typed registry rows (F2); history (F3); `human_held(tier)` (A1). Out: the
ordered eligible set; the recorded class/source/hold per selection; exclusion
reasons.
Depends on: F2, F3, A1.

**U3. Session Dispatch**
Responsibility: compose and launch one session — the per-phase command template,
the reviewable prompt file with strictly filled slots, the digest catalogue and
per-session fingerprint, and the declared inclusion rule for everything
dispatched to an external runner.
Owns: **SR-040, SR-146, SR-175**.
In: phase; the command templates and reviewer dial (F1); brief-eligible content;
the classifier (F4); the catalogue freshness signal (D1). Out: a launched
session; the session record; the dispatch refusal.
Depends on: F1, F4, D1.

**U4. Independent Judgement Rounds**
Responsibility: obtain a judgement from sessions that did not author the work —
review/critique verdicts and contested planning rounds alike — resolved from the
declared agent roster only while the consent surface is present, preferring a
cross-family draw, logging every selection before launch, bounded, and escalating
a non-converging round through the approval level.
Owns: **SR-154, SR-155**.
In: the roster and consent surface (F1); the work under judgement; `human_held`
(A1). Out: the verdict or the selected decomposition as registry-valid rows; the
selection log; the escalation.
Depends on: F1, A1, U3, F2.

**U5. Lane Isolation & Integration Seam**
Responsibility: everything that is true only of the serial trunk actor — bounded
isolated lanes narrowing to one fail-closed seam on the composed tree, pause and
drain, crash recovery from history alone, the immutable per-close terminal
record, exclusive authorship of the shared derived artifacts, ordered
all-or-nothing regeneration, and work-item identity allocated at most once and
never re-issued.
Owns: **SR-144, SR-156, SR-170, SR-173, SR-174**.
In: history and claim state (F3); the declared bar (V1); the high-water mark
(F3); the regeneration dependency order (D1, G1). Out: the landed tree; the
close record; the regenerated shared artifacts; the allocated identity.
Depends on: F3, V1, D1, G1, F5.

### Layer P — The package as an artifact

**P1. Scaffold & Re-sync**
Responsibility: put the declared package on the ground — seed only the artifacts
a chosen profile uses, skip an existing file unless overwrite is asked for,
produce a scaffold that runs green with no edit, wire the process floor from the
developer setup, integrate a re-sync without clobbering filled-in files, and fail
when a manifest destination does not materialize or the instance diverges
structurally from the template it ships.
Owns: **SR-009, SR-010, SR-011, SR-032, SR-036, SR-113, SR-166**.
In: the shipped-file manifest; the chosen profile (F1); the kit-version stamp
(F3); the migration pass (F1); the copy comparison (D1). Out: the scaffold; the
re-sync result; materialization findings; the manifest as a declared inventory
(consumed by V3).
Depends on: F1, F3, D1.

**P2. Root Launchers**
Responsibility: the front door — every declared runnable capability reachable the
same way by an interactive operator, a direct caller and automated discovery,
from one declaration, on every supported platform, and both universal contributor
actions present at the root, each starting in one step or documenting the one
platform-required step, reporting clearly when no interpreter resolves.
Owns: **SR-046, SR-160**.
In: the capability declaration (F1); the interpreter probe. Out: the listing, the
menu, the delegated run and its exit code.
Depends on: F1.

**P3. Portability Envelope**
Responsibility: the package-wide properties that must hold in an environment
nobody here controls — standard-library-plus-ledger imports only, no
language-specific token in the shipped scheme, and the declared OS × version
matrix.
Owns: **SR-034, SR-035, SR-114**.
In: the package's own files; the dependency ledger. Out: undeclared-import
findings; token-scan findings; the matrix declaration.
Depends on: F5.

## Defence of the count

**24 modules, 75 SRs, mean 3.1 SRs per module, no module over 7.**

The count is defended against the objective — *serve the declared outputs while
minimizing internal signal overlap and duplicated behaviour, calls not lines* —
by naming the map it beats.

The obvious small map is the six-way one the frame itself hands over: B-05's
`notes` decomposes the package into *harness verdict, scaffold + MAPPING,
unattended loop, generators, hook floor, package-wide property*. Six modules
reads better and **scores worse**, because each of those six independently
consumes the same five foundation signals: a declared value, a typed registry
row, a history fact, a sensitive-class finding, and a derived-copy comparison.
Six carriers × five behaviours is thirty implementations of five behaviours. My
Layer F plus D1 exists to delete twenty-five of them. The module count went up;
the *behaviour* count went down, which is the axis the objective names.

The count is also defended in the other direction. I did not split per SR (that
would be 75 modules and no compression), and I did not split the three rule
families further even though each contains rules of visibly different kinds —
because a rule family's reason to change is *the shape of the signal it reads*,
and V3/V4/V5 read three different shapes (typed registry rows, frame/interface
rows, authored prose). Splitting V3 into "joins" and "schema" would give two
modules with identical dependencies and identical change triggers: two names for
one boundary.

Every module's interface is narrower than its implementation. The sharpest cases:
F1's callers ask for a typed value and never learn that two grammars read the
file; F4's callers ask "is this text clean?" and never learn a pattern class;
D1's callers ask "is this copy current?" and never learn a source list; A1's
callers ask "is this tier a human's?" and never perform the stage-versus-level
comparison themselves.

---

# 2. COVERAGE, BOTH DIRECTIONS

## Forward: every SR to exactly one owning module

| SR | Module | SR | Module |
|---|---|---|---|
| SR-006 | V1 | SR-149 | V5 |
| SR-007 | F1 | SR-150 | V5 |
| SR-009 | P1 | SR-151 | V2 |
| SR-010 | P1 | SR-152 | V2 |
| SR-011 | P1 | SR-154 | U4 |
| SR-015 | M1 | SR-155 | U4 |
| SR-017 | F4 | SR-156 | U5 |
| SR-018 | F4 | SR-157 | V3 |
| SR-019 | V2 | SR-158 | V5 |
| SR-020 | V2 | SR-159 | V4 |
| SR-022 | D1 | SR-160 | P2 |
| SR-024 | G3 | SR-161 | G3 |
| SR-026 | U1 | SR-162 | V4 |
| SR-027 | U1 | SR-163 | V3 |
| SR-028 | U1 | SR-164 | V3 |
| SR-031 | F1 | SR-165 | G3 |
| SR-032 | P1 | SR-166 | P1 |
| SR-033 | M1 | SR-167 | M1 |
| SR-034 | P3 | SR-168 | G1 |
| SR-035 | P3 | SR-169 | G1 |
| SR-036 | P1 | SR-170 | U5 |
| SR-040 | U3 | SR-171 | U1 |
| SR-043 | V2 | SR-172 | U1 |
| SR-046 | P2 | SR-173 | U5 |
| SR-049 | A1 | SR-174 | U5 |
| SR-052 | G2 | SR-175 | U3 |
| SR-053 | G2 | SR-176 | F4 |
| SR-054 | G2 | SR-177 | M1 |
| SR-070 | D1 | SR-178 | A2 |
| SR-111 | F3 | SR-179 | A2 |
| SR-112 | D1 | SR-180 | V3 |
| SR-113 | P1 | SR-181 | A1 |
| SR-114 | P3 | SR-182 | M1 |
| SR-129 | F2 | SR-137 | F1 |
| SR-139 | A1 | SR-138 | F1 |
| SR-140 | A2 | SR-144 | U5 |
| SR-146 | U3 | SR-147 | F2 |
| SR-148 | U2 | | |

Count check: F1 4 · F2 2 · F3 1 · F4 3 · F5 0 · A1 3 · A2 3 · V1 1 · V2 5 ·
V3 4 · V4 2 · V5 3 · M1 5 · D1 3 · G1 2 · G2 3 · G3 3 · U1 5 · U2 1 · U3 3 ·
U4 2 · U5 5 · P1 7 · P2 2 · P3 3 = **75**.

## SRs that resisted single ownership (13)

Each is assigned above; this is the honest record of what the assignment cost.

1. **SR-017, SR-018** — the *classes* are F4's and the *refusal* is V2's. A
   reader asking "who blocks my commit" lands on V2 and finds the row owned
   elsewhere. Assigned F4 because the class list is what changes; the refusal
   arm is stable.
2. **SR-179** — the rule fires *at the commit that writes the record*, which is
   V2's moment, but everything it must know (what a recorded copy is, deletion
   versus wholesale replacement) is A2's. Assigned A2 so V2 stays a module that
   knows nothing about acceptance records; V2 calls A2 for the verdict.
3. **SR-043** — the dial vocabulary is F1's, the fail-open direction is the
   row's own, the verdict surface is V2's. Assigned V2.
4. **SR-006** — three of its clauses are other modules' signals wearing V1's
   voice: the tier selector is A1's stage, the claimed-lane signal is F3's
   branch-history read, and the freshness steps it skips are D1's.
5. **SR-148** — the widest resistance in the corpus. Work ordering (U2), human
   holds (A1), the generated-and-freshness-gated status surface (D1/G1), and
   *"a fresh scaffold ships no pointer / no live surface reads one"* which is a
   package-content obligation (P1/V3). Assigned U2 for the ordering invariant;
   the pointer-absence clause genuinely lives in the package.
6. **SR-163** — walks the manifest (P1's artifact) through the spine join
   (V3's). Assigned V3, with P1 publishing the inventory.
7. **SR-166** — first clause is manifest materialization (P1); second clause,
   "this repository's own instance carrying the structure of the template it
   ships", is a two-copies-must-agree comparison, i.e. D1's primitive under
   another name. Assigned P1; the comparison is a call into D1.
8. **SR-070** — an artifact-integrity row carrying one *composition* clause
   ("omitting a view whose source registries the repository does not carry").
   Assigned D1; G1 asks D1 whether to emit.
9. **SR-176** — the redaction invariant belongs to the finding type (F4) but the
   one durable carrier the row names is the loop's transcript (U3). Assigned F4
   precisely so U3 cannot hold a second class list — which is the divergence the
   row itself reports (§4 O12).
10. **SR-111** — a version-control fact (F3) written into a scaffold artifact
    (P1). Assigned F3; see §5 for the judgement.
11. **SR-138** — dial vocabulary and the never-delete-an-unwritten-value rule
    (F1), run by scaffolding and re-sync (P1). Assigned F1.
12. **SR-160** — the row itself states that its obligation spans the git hooks
    and the root launchers and *parts along that line*, keeping the launcher
    half and leaving the hook half elsewhere. That is one behaviour with two
    declared homes; assigned P2 and reported as an overlap (§4 O7).
13. **SR-114** — portability (P3) whose acceptance defers its evidence surface
    to SR-152 (V2). Assigned P3.

## Modules owning no SR (1)

**F5 (Finding & Verdict Shape).** This is the one invented module and I am not
hiding it. It exists because thirteen SRs each restate its contract (§4 O2) and
none states it *as* an obligation — there is no row saying "a finding names its
row and cell, carries a declared severity, and an advisory never changes the exit
code" in general. The corpus therefore has a **hole**: the property every
checking row assumes is stated nowhere and can be violated by a new checker
without failing any row. Either F5 is a real module and the corpus is missing its
requirement, or F5 dissolves into V1 as an implementation detail and thirteen
rows keep re-stating it. I keep F5 and file the missing row as a finding.

**Thin ownership, declared:** F3 owns only SR-111 and V1 owns only SR-006. F3 is
the closer call — it survives on one row while nine SRs consume it. That is
itself a corpus finding: the history-fact vocabulary is load-bearing and
unstated.

---

# 3. THE OBJECTIVE APPLIED, DECISION BY DECISION

Format: decision · what it removes or narrows, in the objective's terms.

## Merges (each removes a duplicated behaviour)

**D-M1 · Toolchain profile + process dials + capability inventory → one reader
(F1).** SR-007 refuses a malformed profile; SR-137 refuses a wrong-typed or
out-of-range dial; SR-139 refuses an out-of-range level toward the conservative
end; SR-046 exits 1 on an absent capability declaration. That is *one* behaviour
— read a declaration, refuse rather than default — implemented four times. The
merge deletes three of the four. It does **not** widen the interface: a caller
still asks for one value and gets a typed answer or a refusal; the two grammars
and the two files stay inside. Alternative rejected: one module per declaration
file, which keeps the refusal behaviour duplicated per file for no gain.

**D-M2 · The two representation converters → F2.** SR-129 (work registry) and
SR-147 (spine) both require a conversion proven cell-for-cell before authority
moves, and SR-147's own reasoning cites SR-129's lesson. Separate modules means
two cell-exact round-trip verifiers. The merge removes one.

**D-M3 · Secret classes + PII classes + record redaction → F4.** SR-017 and
SR-018 differ only in *which classes and under which dial*; SR-176 constrains
what a finding may contain. Splitting scanning from redaction is what produced
the divergence SR-176 already reports (the redaction set lacks the PII classes
the scanner has). Merging makes the class list one thing and redaction a property
of the finding *type*, so no consumer can print a value it was never handed.

**D-M4 · Local hooks + spawn gate + hosted re-run → V2.** SR-019 states in its
own text that it discharges its claim only *as a pair* with SR-151/SR-152. Two
modules for the two halves means the moment→bar mapping is read at the hook and
again at CI, which is exactly the drift SN-005's "one definition of passing per
moment" forbids. Merging gives that table one reader. SR-043 joins because it is
the same output (B-04) produced at the same instant by the same kind of decision.

**D-M5 · Derived stage + approval level + phase-drop rule → A1.** Three callers
(U2's holds, A2's attestation, V1's tier selection) each need *stage compared to
level*. As separate modules each caller performs the comparison, and SR-139's own
wording — "a **separately** derived spine stage" — actively invites a second
derivation path. The merge turns three comparisons into one call, `human_held(tier)`.
This is the merge that most directly answers my axis's question (§4 O11).

**D-M6 · Record + drift report + write refusal → A2.** SR-178 states that *what
counts as movement* is "one definition with one home". Three modules would give
that definition three homes: the recorder (which rows to copy), the reporter
(which cells moved) and the refuser (byte-identical to what). Merged, movement is
defined once and the three arms are three entry points.

**D-M7 · Vendored-doc drift + generator freshness + skill fan-out → D1.** *The
headline merge of this derivation.* SR-022, SR-070 and SR-112 are three
statements of one behaviour — recompute from declared sources, compare to the
committed copy, respond — and four further rows consume the same comparison
(SR-049's cache check, SR-146's catalogue `--check`, SR-158's stale-generated-doc
class, SR-166's template-versus-instance clause, SR-178's record drift). Left
split, this behaviour is implemented at least seven times, once per artifact
family, and every implementation gets to disagree about what "unchanged" means.
Merged, it is one predicate with seven callers, and the *response* (refresh,
report, refuse, omit) stays with each caller where it differs. This is the single
largest total-behaviour reduction in the map.

**D-M8 · Every measured-number verdict → M1.** SR-167 (breach against budget or
tolerance band around a committed baseline), SR-182 (count against a stamped
baseline, never gating), SR-177 (report with no target), SR-033 (warn-tier, never
fails) and SR-015 (the row's back-link invariant) are one pipeline: measure →
compare to a declared baseline → apply the row's declared response. Four separate
homes means four baseline comparisons and four gating postures, which is exactly
how a "never gating" row acquires a gate by accident. Merged, the posture is a
declared field, not code.

**D-M9 · Review/critique routing + contested planning → U4.** SR-154 and SR-155
share four behaviours verbatim: a fresh session that did not author the work, a
bounded round, a preferred cross-family draw, and escalation through the approval
level on non-convergence. Splitting duplicates all four. Merged, the *occasion*
(review a change / arbitrate two rival plans) is a parameter.

**D-M10 · Perspective record + partition record + case expansion → G3.** SR-165's
own reasoning describes itself as "the SR-161 form applied to the partition
instead of the perspective set" — two rows, one record schema, one "a missing
element is a finding" rule. SR-024 joins as the third instance of the same
responsibility: prove that a declared space was covered rather than sampled. The
merge removes one record schema and one missing-element checker.

**D-M11 · Lane lifecycle + seam + exclusive writer + ordered regeneration +
identity → U5.** SR-144, SR-156, SR-170, SR-173 and SR-174 all presuppose one
predicate — *am I the serial actor operating on the merged tree?* Five modules
means that predicate is computed five times, and it is precisely the predicate
whose disagreement produces a half-integrated authoritative state. The SRs are
correctly split (they fail independently); the *module* is one because the
failure they each prevent has one cause.

**D-M12 · Scaffold, re-sync, dev-setup and materialization → P1.** SR-009, 010,
011, 032, 036, 113 and 166 all walk the same shipped-file manifest with different
verbs (seed, skip, verify green, wire, merge, materialize). Seven modules means
seven manifest walkers. This is the widest module in the map at 7 SRs, and it is
justified because the *inventory* is the shared signal, not because the verbs are
similar.

## Splits (each narrows a wide interface)

**D-S1 · Presentation vocabulary split out of view composition (G2 from G1).**
SR-053 requires that "a new emitter joins the bar by existing" and SR-052 that
"the pass is the full sweep of every emitted view". Neither is satisfiable if
each emitter carries its own tokens: a new emitter would arrive outside the bar
by default. Split, an emitter's interface shrinks to "ask for a token, an
accessible name, a collapse decision" and the bar is a property of the
dependency, not of a review. The wide interface this narrows is real: without the
split every emitter must know the whole design system.

**D-S2 · Classification split out of the enforcement floor (F4 from V2).** Three
consumers need classification and only one of them is a git hook (the dispatch
composer and the durable-record writer are not). Keeping classification inside
the floor forces the other two to either import a hook or re-implement the
classes — which is what SR-176 records as already having happened.

**D-S3 · Declaration reading split out of every consumer (F1).** The dual-grammar
requirement is stated as an *equality property between two readers*. That
property can only be tested where both readers live. Split out, the property has
a home; left distributed, the equality test has no subject.

**D-S4 · Registry parsing split out of rule checking (F2 from V3/V4/V5).**
SR-147 states that a structured carrier turns three integrity rules into
properties of the parse — a duplicate id becomes a decode error. That reduction
only happens if exactly one module parses. The split also narrows V3's interface
from "text and a grammar" to "typed rows".

**D-S5 · History facts split out (F3).** Nine SRs read version control. Without
the split each invents its own question shape, and two of them — SR-006's
"is this a claimed lane" (from branch history) and SR-170's "was this written
from a work branch" — are the *same* question asked two ways. Split, they are one
call with one answer.

**D-S6 · Three rule modules, not one checker (V3/V4/V5).** A single "checker"
module would reach a lower module count and score worse under the objective: it
fuses three unrelated input shapes, so adding a prose rule would require knowing
the registry schema. The split is drawn exactly where the source signal changes.
SR-159's acceptance independently draws the same line, carving SR-162's endpoint
and signal cells out of SR-157's generic checker.

**D-S7 · Work selection split from run lifecycle (U2 from U1).** SR-148 is one
precedence invariant; SR-026/027/028/171/172 are footing and end states. Fused,
the lifecycle module would need the whole registry join to start a run, and
"add a selection class" would touch exit-code handling.

**D-S8 · Step plan split from the rules it runs (V1 from V3/V4/V5/M1/D1).** V1
owns *which steps and what the exit means*; the rules own *what a violation is*.
Fused, adding a rule edits the exit arithmetic — the change-amplification the
objective is written against.

**D-S9 · Independent judgement split from session dispatch (U4 from U3).** U3
changes when a runner's invocation surface changes; U4 changes when the
adjudication protocol changes. Fusing them would put a model-CLI concern and a
governance concern behind one interface.

**D-S10 · Launchers split from scaffold (P2 from P1).** P1's caller is an
adopting repository; P2's caller is a person or a discovery tool. They change for
different reasons (what ships / how a platform starts a process).

## Merges considered and rejected

- **SR-158 into D1.** Only one of SR-158's five classes (stale generated doc) is
  a derived-copy comparison; links, vision tags, dangling references and figure
  provenance are not. Merging would drag four unrelated rules into the freshness
  module. Recorded instead as a *call* from V5 into D1.
- **A1 into V1.** The stage is consumed by four modules, not just the harness;
  putting it inside the harness would make the loop and the dashboard depend on
  the harness to learn what tier they are in.
- **M1 into V1.** The measurement pipeline's inputs (telemetry, baselines) and
  its change trigger (what a breach does) are unrelated to step planning; the
  merge would add a whole input family to V1's interface for no removed
  behaviour.
- **P3 into P1.** Portability properties are checks over the package's own
  source, not acts of placing it; fusing them would mean a scaffold run and an
  import audit share a module because they share a noun.

---

# 4. OVERLAPS FOUND IN THE REQUIREMENTS THEMSELVES

Thirteen. Ordered by how much duplicated behaviour a minimal map removes.

**O1 · Derived-copy currency is stated eight times.**
`SR-070` (freshness contract) · `SR-022` (vendored-doc drift) · `SR-112`
(per-agent skill fan-out drift) · `SR-049` (stage cache `--check`) · `SR-146`
(prompt catalogue `--check` stale) · `SR-158` (stale generated doc) · `SR-178`
(live text moved from the recorded copy) · `SR-166` (template versus this
instance's structure). One behaviour — *recompute from declared sources, compare
to the committed copy* — under five different names (freshness, drift,
staleness, byte-identical, structural divergence). A minimal map states it once.
This is the direct answer to my axis's question: two declared outputs (the
package's generated artifacts at B-05 and the authority record at B-02) need the
same intermediate signal and reach it by different paths.

**O2 · The finding/severity/exit contract is restated thirteen times.**
`SR-157` `SR-158` `SR-159` `SR-162` `SR-163` `SR-164` `SR-149` `SR-150` `SR-167`
`SR-180` `SR-181` `SR-182` `SR-015`. Each independently says some version of
"report naming the row and cell, warn by default, gate under `--strict`,
advisory never changes the exit code". No row states the contract itself, so it
is a shared behaviour with no home — see §2's F5 note. **A missing requirement,
not just a duplication.**

**O3 · The stage/tier signal is consumed as if it were four signals.**
`SR-049` (derive and cache) · `SR-006` ("the strictness selector cached in
docs/stage") · `SR-139` ("a **separately** derived SPINE STAGE") · `SR-148` ("the
earliest incomplete spine tier") · `SR-181` (the *effective* stage) · `SR-168`
(per-tier completeness). Five consumers, three different names for one value, and
one row's wording (`SR-139`'s "separately derived") explicitly licenses a second
derivation path. If any two of these derive independently, the harness and the
dashboard can disagree about what tier the project is in — the produced-twice
failure my axis is built to find.

**O4 · Refuse-rather-than-default is stated five times.**
`SR-007` (malformed profile, non-integer coverage) · `SR-137` (wrong-typed or
out-of-range dial "refused, never defaulted") · `SR-139` (out-of-range level
refused loudly) · `SR-148` (missing or contradictory declared inputs fail closed
for that item) · `SR-046` (absent or empty capability declaration exits 1). The
only genuine variable is the fail-safe *direction*, which is a per-caller
parameter, not five behaviours.

**O5 · Measured-value-versus-baseline is stated four times with four postures.**
`SR-167` (budget and tolerance band → red) · `SR-182` (stamped baseline →
warn-only, "a gating change here is a new requirement") · `SR-177` (telemetry →
report, no target) · `SR-033` (warn-tier budgets → never fails). One pipeline,
four homes; the posture belongs in a declared cell.

**O6 · The one-definition-of-passing-per-moment table has four readers.**
`SR-006` (the steps of the gate that must next be passed) · `SR-019` (the local
floor) · `SR-151` (per-trigger tier from the declared moment-to-tier table) ·
`SR-152` (the harness's own exit as the job's). SN-005's acceptance names this as
*one* definition; four rows each reach for it.

**O7 · The interpreter probe is duplicated by explicit ruling.**
`SR-019`/`SR-020` (probe as machinery under the hooks) and `SR-160` (the same
probe stated again for the launchers, and the row says so: it "spans two
audiences … and parts along that line"). The requirements chose to duplicate
rather than share. Under the objective this is a merge candidate: one
"locate a working interpreter by running a candidate and report clearly"
behaviour with two callers.

**O8 · The serial-actor predicate is presupposed by five rows.**
`SR-144` `SR-156` `SR-170` `SR-173` `SR-174`, plus `SR-006`'s claimed-lane
freshness skip and `SR-170`'s cross-reference to it. All need *am I the serial
trunk actor on the merged tree / is this a work branch*, and `SR-006` derives it
from branch history while `SR-170` derives it from the seam. Two paths, one fact.

**O9 · Sensitive-class scanning has four sites and a recorded divergence.**
`SR-017`/`SR-018` (hook floor) · `SR-020` (push range) · `SR-175` (dispatch
block, "on the same scanner the transcript path already runs") · `SR-176`
(durable-record redaction). `SR-176` itself reports that the redaction set does
**not** contain the PII classes the gate adds — i.e. the duplicated signal has
*already* diverged in the field. Strongest available evidence that this overlap
class is not theoretical.

**O10 · The one-home dial property is claimed by two rows that had already
diverged.** `SR-031` and `SR-137` both claimed the two-grammars-agree observable;
the corpus records that the texts diverged, that only `SR-031`'s named the
trailing-comment decoy which made the privacy gate fail **open**, and that the
duplicate clause was struck. The residue is that both rows still range over the
same mechanism and must be read together. A second instance of the same class:
`SR-140`/`SR-178`/`SR-179` share one "what counts as movement" definition across
three rows, held together only by prose.

**O11 · Provenance-record shape stated twice.** `SR-161` (perspectives) and
`SR-165` (candidate partitions) — `SR-165`'s own text calls itself "the SR-161
form applied to the partition instead of the perspective set". One record schema,
one missing-element rule, two rows.

**O12 · Independent-fresh-session judgement stated twice.** `SR-154` and `SR-155`
each carry: a session that did not author the work, a bounded round, a preferred
cross-family draw, and escalation through the approval level. Four shared
behaviours, two rows.

**O13 · The shipped-file manifest is walked by five rows.** `SR-009` (seed by
profile) · `SR-010` (green) · `SR-011` (skip existing) · `SR-163` (every file
maps to an outcome) · `SR-166` (every named destination materializes). The rows
partition their *questions* carefully — `SR-166`'s own text negotiates the
boundary with `SR-163` at length — but all five traverse one inventory, and two
of them (`SR-163` presence, `SR-166` landing) needed a paragraph of prose to keep
from contradicting each other. That prose is the cost of the overlap.

**Two structural findings offered with the same weight as the map:**

- **The corpus states no requirement for its own most-restated contract** (O2).
  Thirteen rows assume a finding/severity/exit protocol that no row owns, so a
  new checker can violate it without failing anything.
- **The corpus has no row for the history-fact vocabulary** that nine rows
  consume (F3's thin ownership). Both gaps have the same shape: a shared
  behaviour that every consumer restates and no row states.

---

# 5. HONESTY

## Recognition, and a contamination I could not remove

I recognise this system. More than that: **the project instructions injected into
my context before your brief describe this repository by name and name several of
its files** (a process document, a scripts directory, a dashboard generator, a
trace checker, a spine carrier, test files, config files). That injection is not
something I could decline, and it is a real weakening of the blindness contract
that you should weigh when comparing my map to Team B's.

What I did about it:

- I read **nothing** outside the five pack files. No Glob, no Bash, no Read
  outside `wi508-requirements-pack/`. My two Grep calls both carry an explicit
  path into the pack directory (one over `system-requirements.toml` to count the
  SR ids, one over the pack directory to count SN/hat/frame rows). Nothing in
  this session touched `C:\Projects\ai-template`.
- Every module name in §1 is a **functional responsibility phrase**, and I
  checked each one against the names present in the injected instructions to make
  sure I had not reproduced a filename or a script name as a module name. None
  matches.
- I did not use recalled structure. The concrete check on this: my map disagrees
  with the grouping I would have produced from recall in at least four places —
  the harness is three rule modules plus a step planner plus a measurement
  module rather than one checker; classification is separated from the hook
  floor; the derived-copy comparison is a module rather than a per-generator
  flag; and the stage and the approval level are one module rather than two.
  Each of those is argued in §3 from the requirement text alone.

## Concrete artifact names I leaned on (every one)

Each of these appears inside a requirement cell, so it could not be stripped. In
every case I treated it as **evidence that an obligation exists**, never as a
module assignment.

| Name, and where it appears | What I took from it | What I refused to take |
|---|---|---|
| B-05 `carries` naming six delivered script contracts, and `notes` naming six delivered capability classes | That the package decomposes into roughly six capability families — used as a *check* on my coverage, to confirm no output family was unserved | The six as a module list. My map has 24 modules and deliberately does not mirror the six; §1's count defence explains why that grouping scores worse |
| `docs/stage` (SR-006, SR-049) | That the stage is a **cached derived value with a freshness contract** and that the harness's step plan reads it — the dependency V1→A1 | Any file layout; I named the signal, not the file |
| `docs/stack.ini` `[ci-tiers]` (SR-151), `[dupes-census]` (SR-182), and "the capability set is declared once in docs/stack.ini" (SR-046) | That the toolchain profile, the moment-to-tier table, a measurement baseline and the capability inventory are **the same declared surface** — this is the direct evidence for merge D-M1 | Whether that surface is one file or several. I merged the *reader*, not the files |
| `docs/agents.toml` and `docs/agents-enabled` (SR-154) | That roster declaration and consent are two separate signals, both read before routing | Their formats |
| `docs/archive/last_approved/` (SR-140) | That the acceptance record is a **whole-file copy at a location**, which is what makes A2's mirror comparison a derived-copy comparison (dependency A2→D1) | Its path as a module |
| `check_privacy`, "the transcript path", "three composers" (SR-175, SR-176) | That the classifier already has multiple consumers and that they have diverged — the evidence for merge D-M3 and overlap O9 | The function names |
| `bootstrap.py` MAPPING (SR-036, SR-163, SR-166) | That a **declared shipped-file inventory** exists and is shared by the scaffold and the coverage check — evidence for O13 and for P1 publishing the inventory to V3 | The script name as a module |
| `tests/test_bootstrap.py`, `tests/test_dogfood_sync.py` (SR-166) | That materialization and template-versus-instance structure are two separately observable properties | Nothing structural |
| `interfaces.toml`, `external.toml`, `spine_carrier.py`, `hats.py`, `derive_stage.phase_rule_findings` (SR-162, SR-181, registry headers) | That the frame, the interface rows and the spine share one carrier and one reader — evidence for F2 and for the V3/V4 split | The reader names |
| `git commit --no-verify` (SR-019, SR-152) | That the local floor is bypassable **by design** and that the hosted re-run is its declared other half — the whole argument for merge D-M4 | — |

## Judgements the requirements did not determine

1. **SR-111 → F3 rather than P1.** The row says the *scaffold generator* records
   the stamp, which reads like P1 ownership. I assigned F3 because the row's
   entire content is version-control vocabulary (commit SHA, date, dirty tree),
   and under the deep-module criterion the scaffold should write a value it did
   not compute. Alternative: assign to P1 and let P1 know git. Cost of my choice:
   F3's SR ownership rests on this one row, which I flag rather than hide.
2. **SR-024 → G3.** A permutation-case generator sits uneasily beside two
   provenance-record rows. I grouped them under "prove a declared space was
   covered rather than sampled". Alternative: a standalone case generator (a
   25th module owning one SR), or fold it into F2 as a registry-authoring
   utility. I chose the responsibility over the noun; a reviewer could reasonably
   reverse this.
3. **One reader for the toolchain profile and the process dials (D-M1).** The
   pack never says whether these are one file. If they are two files with two
   audiences, my merge is still defensible (one refusal behaviour) but weaker.
4. **Three rule modules rather than one or five.** The cut by *source signal* is
   mine. SR-159's acceptance supports it; nothing mandates it.
5. **SR-179 → A2 rather than V2**, and **SR-017/018 → F4 rather than V2**. Both
   are "knowledge versus moment" calls. I consistently gave ownership to the
   module that holds the *knowledge* and made the moment a caller. A map that
   consistently chose the moment instead would be internally coherent too.
6. **SR-163 → V3 rather than P1**, on the grounds that its verdict is a spine
   join. The manifest argument for P1 is real.
7. **F5 kept as a module with no SR.** The alternative was to fold it into V1 and
   declare no invented modules. I kept it because folding hides the missing
   requirement that O2 identifies, and the brief values the requirements finding
   as much as the map.
8. **The phase-drop rule (SR-181) → A1 rather than V3.** It is an authoring-time
   check like V3's rules, but it consumes the stage derivation and the prior
   committed state, so putting it with the derivation removes a second stage
   computation.
9. **U5 at five SRs and P1 at seven.** Both are near my self-imposed width limit.
   I accepted them because in each case a single shared signal (the serial-actor
   predicate; the shipped-file inventory) is what holds the group together. If
   either module later grows a second shared signal, it should split.

## Moments I was tempted

- Twice, strongly: when SR-166 named two test files and when SR-151 named a
  pinning test, a single read would have told me whether my P1/V3 split matched
  what exists. I did not look, and the split above stands or falls on the
  requirement text.
- Once, weakly: I wanted to check whether the toolchain profile and the process
  dial home are the same file, because merge D-M1 rests on it. I recorded the
  uncertainty as judgement 3 instead.
- I also note the working directory of this session **is** the live system. The
  contract held: no tool call in this session read from it.

## Blindness breach

**None by tool.** One by context, disclosed above and not removable by me: the
project instructions describing this repository were injected before your brief.
Everything in §§1–4 is derived from the pack; the injected material was used only
in the negative, as a list of names to avoid.
