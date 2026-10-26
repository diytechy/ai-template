# Rubric — Architecture decomposition

**Adjudicates:** the decomposition of one component scope, meaning the system
below its system requirements or one component in the tree. The judged parts
are the scope's sub-components, the interfaces at their boundaries with their
value domains, the scope's mode classes, its output × input dependency table
and its recorded stopping point. Each sub-component is judged by the same
anchors at its own depth. A scope can be judged before anything in it is built
(a fresh breakdown), when a work item would change it (the architectural-delta
question), or as it stands (an audit).
**Used by:** an independent critic who is never the scope's author
([README](README.md)). The artifact is the scope's rows and records, never
code: its component rows and their `part_of` links
(`docs/requirements/components.toml`), its interface rows
(`docs/requirements/interfaces.toml`), its runtime flows
(`docs/runtime-flows.md`), its dependency table and stopping record, and the
requirements that constrain its interfaces. Facts about code, such as an
import graph, file sizes, a dependency-matrix clustering or a value-domain
check, come in only as a generated report. A report is evidence for a finding
and never the verdict: a clustering can suggest a grouping, but it never
defines a cut. The `architecture-decomposition` skill is the author's procedure
for producing the artifact. This file is the bar that artifact is judged
against.

## Intent

A scope is well decomposed when each of its boundaries hides a decision that
is likely to change. A change then stays inside one component, a test at a
boundary proves what crosses it instead of sampling it, and each interface
admits few cases. This is Parnas's criterion ("On the Criteria To Be Used in
Decomposing Systems into Modules", 1972): decompose by the decisions each part
hides, not by the steps the processing runs through. Keeping a scope whole, or
rejecting a proposed split, is a valid outcome when the evidence argues for it.
More components is not better. The rubric rests on process.md §4 (requirements
come before architecture; an interface says what crosses, a requirement what
must be achieved; the recursion lives in the component tree), on §8 (one
interface row per owner, far side and kind of information), and on the stopping
rules in `prompts/spine-questions.md` §3. It does not restate them.

## Terms

- **Value domain:** the set of values that may cross an interface, which is
  the interface's form.
- **Closed enumeration:** a domain listed case by case, where each case carries
  only its own data (a sum type).
- **Disjointness and coverage:** no input satisfies two cases, and every input
  satisfies exactly one (SCR; Heitmeyer, Jeffords and Labaw 1996). Use these
  words, not "MECE" or "completeness".
- **Mode class:** a named set of states the system can be in, as a stakeholder
  would name them, with the transitions between them (SCR; Heninger 1980).
  Always write *mode class*, never *mode* on its own.
- **Monitored and controlled quantities:** what the system observes in its
  environment and what it sets there. Requirements speak only of these (Parnas
  and Madey 1995).
- **Information hiding:** a boundary hides a design decision that is likely to
  change (Parnas 1972).
- **Control coupling:** a flag passed across a boundary to choose the
  receiver's behaviour (Stevens, Myers and Constantine 1974).
- **Dependency matrix:** outputs or parts, each set against what it depends
  on. It is uncoupled when diagonal and decoupled when triangular (Steward
  1981; Suh).
- **Input-output relation:** the inputs that influence one output, which is
  the unit a case count multiplies over (Schroeder and Korel 2000).
- **Choice:** one equivalence class of an input (Ostrand and Balcer 1988).
  Cardinalities count choices, not raw values.

What Parnas and Stevens et al. call a *module* is a *component* here, not a
file. *Seam* here means an internal interface, not Feathers's sense of a place
to change behaviour without editing code.

## Anchors

**A1 — Each boundary hides a named decision.** For each sub-component, name
the decision it hides: what could change and stay inside it. To show it, take
two or three changes that the requirements or the environment make likely, and
list the components each one would touch. A good cut keeps most changes inside
one component. A stage of a runtime flow becomes a component only when it also
hides a decision, because ordering on its own is no reason to cut. Cohesion is
judged the same way: the parts of one component change for the same reason.
*Bad:* sub-components named after the steps a request passes through, where
every one of them reads and writes the same shared record, so any change to
that record touches all of them.

**A2 — Every state a stakeholder can name is a mode class, with its
transitions.** List the scope's mode classes. For each state, give its name,
what the system does in it and what moves it on, in the stakeholder's words
and without an invented number, and record them in the runtime flows. A mode
class earns obligations and a flow. Whether it also becomes a component is a
separate question, answered under A1. *Bad:* states that exist only as
combinations of flags in code; one component per state, made only because the
states exist.

**A3 — Every boundary interface has a closed value domain.** Each interface at
a boundary states its form. Where the values are finite the form is an
enumeration; otherwise it is one declared schema. A call states its typed
request and answer, without symbol names. Check the form for disjointness and
coverage. Keep the two kinds of UNKNOWN apart. An unknown *problem state* is a
real case, and it needs declared behaviour. An *out-of-domain input* is
rejected where it enters, after it has been converted once into the closed
domain ("parse, don't validate", King 2019). A single catch-all that serves
both purposes makes coverage trivially true and hides the missing cases. The
form belongs to the interface; the behaviour across it belongs to the
requirement that constrains it (process.md §4). *Bad:* an interface whose form
is "a status string"; a domain {OK, ERROR, OTHER} whose OTHER has no declared
behaviour.

**A4 — Boundaries sit where dependencies are sparse or an intermediate value
is narrow.** The scope carries an output × input dependency table. For each
output it lists the inputs that output depends on, with the scope's own mode
class among them, and counts each input in choices. A case count multiplies
those choices; an import count or an interface-row count is never a case count.
Each cell names its evidence, and a blank cell says whether it means proven
independence or unknown. An audit may rely on generated reports of the scope
as built; a fresh design has only the requirements and the proposed
interfaces. A question the supplied evidence cannot answer is recorded as *not
supplied* or *not assessable*, and is never read as a defect. A cut earns its
place in one of two ways:
(a) the groups it separates share few cells, so "this output ignores that
input" becomes structural instead of a claim;
(b) an output reaches some of its inputs only through a narrow intermediate
value, so the case count becomes a sum instead of a product. For example,
inputs of 4, 4 and 3 choices give 48 cases together. If the first two reach
the output only through a two-valued intermediate, the split gives
16 + 2 × 3 = 22.
Without (b), splitting does not shrink a component's total case count, because
one suite still covers the union of what its outputs need. What a split adds
in that case is proof and a smaller blast radius, and the finding says which
of the two it means. A gain under (b) holds only when the intermediate is the
whole channel, with no side path. *Bad:* a cut whose two sides read nearly the
same inputs; a narrow intermediate that one side also bypasses.

**A5 — No control coupling across a boundary.** No flag crosses a boundary to
choose what the receiver does. Two booleans that are never both true are one
domain (A3). A product of flags is right only where the dimensions really are
independent (orthogonal regions, Harel 1987), and the form then says so. Below
a component's boundary, in its code, the `deep-module-design` skill applies.

**A6 — Interfaces at every boundary, and each meaning in one interface.**
Before judging a boundary, state the scope's ownership model for a file that
several components' rows name: one implementation owner, several obligation
allocations, or a declared kernel role. Requirement allocation is not
implementation ownership. Every kind of information that crosses a boundary of the scope, in each
direction, has its own interface row (process.md §8). Inside a component,
interfaces are optional. A definition that several parts of the scope read,
such as a record, a verdict or a schedule, has one owner. If a cut puts that
definition's readers in different components, the definition becomes one
boundary interface with every reader on its far side. It is not split or
copied, and the cut counts it as a cost (A7). Handoffs through files, the
environment or subprocesses are crossings too. An import graph does not show
them, so the flows and the interface rows must.

**A7 — Candidate cuts are compared on evidence, with their costs.** Where more
than one cut is plausible, compare every candidate, including keeping the
scope whole, on three things:
- the decisions it hides (A1);
- the dependency cells it removes, or the intermediate value it narrows (A4);
- what it costs, counted under four heads:
  - *crossings:* the existing interface rows the cut newly crosses, the new
    endpoint crossings, the shared schema definitions that become boundary
    interfaces (A6) and the new semantic surfaces, each counted separately,
    with the unknown remainder stated;
  - *invariants:* which invariants the cut preserves, and how: transaction
    scope, lock order, failure and retry ownership, durable effects. A cut
    that breaks one carries the repair as a cost; the break is weighed with
    the rest, not raised on its own as an objection to splitting a stage;
  - *enforceability:* the access constraints that make the boundary hold, and
    the boundary tests that establish them;
  - *migration:* obligations to re-place, and a migration plan wherever
    approved rows or tests would change. A file move is counted only when the
    cut needs it.

The chosen cut states why it beats the others. A cut that departs from the
stages a stakeholder would name is not a failure. A cut the evidence does not
argue is one. A comparison the supplied evidence cannot settle (A4) ends in
*insufficient evidence for approval*, naming the evidence that is missing.

**A8 — The stopping point is recorded, under the descent rule that fits the
leaf.** Each leaf of the tree records why it is not split further
(process-options.md, "(d2) Record the stopping boundary"). Two rules apply:
one for the obligations a scope carries, one for its components.

*Requirement (obligation) descent.* Each candidate child obligation is put to
four tests:
1. *A describable state.* Can the stakeholder name the state, what the system
   does in it and what moves it on, in their own words and without inventing a
   number? If so, descend into obligations: the state is a mode class (A2) and
   earns requirements and a flow. Whether it becomes a component is A1's
   question.
2. *An invented number.* Is the only new content a value that the stakeholder
   could neither state nor source today, one they would pick only after seeing
   the implementation (a gap in pixels, a font size)? Then stop. The parent
   keeps the quality, verified by a rubric or an attestation, and the value
   lives in code or configuration. A binary floor ("no two wires overlap") is
   a describable state and stays. So does a number the stakeholder can source,
   such as one set by a standard.
3. *A paraphrase.* Stop (process.md §3, "Decompose, don't paraphrase").
4. *No pass/fail of its own.* Stop (`prompts/spine-questions.md` §3, "Record
   the stopping boundary").

*Component descent.* A component leaf stops when no information-hiding cut
pays its way after the A1/A4/A7 comparison. Sub-decisions that are testable
on their own do not by themselves force a cut: a component can hold several
and still rightly stay whole, when a cut would cost more than the isolation
it buys.

*The stopping record* names the candidate children, the evidence, the
remaining uncertainty and what would trigger a revisit, and, for an
obligation, the test that stopped it. A leaf without a record, or a record
that cites a rule which does not hold, is a finding.

**B1 — A product of booleans standing in for one domain.** *Tell:* an
interface or a mode class carries two or more flags, and some of their
combinations are documented as impossible or are never handled. For example,
the flags `at_hub`, `on_truck`, `delivered` and `lost` admit 16 combinations,
but a parcel is only ever in one of four places. A closed enumeration of four
cases (A3) replaces them.

**B2 — One meaning carried by two interfaces.** *Tell:* two interface rows
whose forms describe the same fact under different owners, or a consumer that
recomputes from raw inputs something another interface already emits. The two
drift apart, and a test of one proves nothing about the other.

**B3 — An under-decomposed component.** *Tell:* the component's own runtime
flow hands work between stages through internal seams that no rule requires.
Its dependency matrix falls into two or more clusters with few edges between
them. The changes it usually receives each touch only one of those clusters.
Its description lists its parts instead of naming a decision it hides. Calling
a component under-decomposed is a finding only when it comes with a candidate
cut argued under A7.

**B4 — A processing-step split.** *Tell:* the sub-components are the steps of
a flow, and each depends on the same representation of the data, so changing
that representation touches every one of them. Parnas's own example is a
keyword-in-context index. Cut into input, circular shift, alphabetizing and
output, every part shares the line store's format. Cut around the decisions
each part hides (how lines are stored, how shifts are represented, how order
is computed), a change of format stays in one part.

## Verdict

Write one `- [BLOCKER|MAJOR|MINOR] <anchor> -> where/why -> the concrete
change -> @owner` line per finding, citing an A or a B anchor, and then the
brief's one machine line. Each finding names its evidence: the rows, flow steps
or table cells it reads, or a generated report. The concrete change is a cut,
an interface edit, a mode class or a stopping record. It never rewrites a
requirement. Work beyond the scope becomes a candidate row filed through change
intake (process.md §5), because the critic edits no spine row
([README](README.md)). A finding that names a new failure mode proposes a new
`B#` anchor (the accumulation rule, [README](README.md)).

Severity follows the cost in normal use. A BLOCKER or MAJOR is a defect that
would reasonably force a later re-cut of rows already approved or tests
already written: a boundary that hides no decision, a domain without coverage,
or a shared definition split across components. A missing term, record or
table cell that the rest of the artifact makes recoverable is MINOR. A finding
that only a contrived scenario reaches is dismissed under process.md §6,
"Review threat model". An artifact that keeps its scope whole earns an APPROVE
when A1, A4 and A7 argue for it.
