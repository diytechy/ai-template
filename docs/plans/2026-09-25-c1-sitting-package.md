# The C1 sitting package — what the owner signs

**Owner ruling, 2026-09-25:** *"I'm good with the recommendations you have laid
out."* That rules §0.1 (b), build first with the arms off, and §0.2 (a), the
headline needs stay Drafted until a complete chain answers each. It also
accepts the text of §1–§4 as written, including the column name `source` and
the stakeholder assignments. The owner will be absent and named a Fable
reviewer as their stand-in for the spine approvals that follow. Those approvals
are recorded as the stand-in's, never as the owner's own signature.

**Status: PREPARED FOR THE SITTING, 2026-09-25; ruled the same day (above).**
Documents only: no script, test, registry row or template changed. It states exactly what
the owner signs at C1 of
[the assumption-tier plan](2026-09-20-validation-gap-and-the-assumption-tier.md)
("AT"; its §11), together with S3 of
[the sister plan](2026-09-23-owner-notes-spine-sessions-and-tests.md) ("SP"),
and the question that decides how the sitting is run.

**How to read it.** §0 is what to decide first: the question, and three things
preparing the package found. §1–§4 are the text you sign. §5 is what gets
built, with its arms off. §6 lists what the sitting commit holds, and §7 what C1
deliberately leaves out.

---

## 0. Decide first

### 0.1 The question: sign the text first, or build first?

Three facts bear on it, each checked against the code:

- **The live registries refuse a key their template does not ship.**
  `tests/test_dogfood_sync.py` fails when "a live row quietly grows a key
  nobody shipped" (`registry_key_drift`). So `system`, `mediates`, the
  stakeholder table, `stakeholder_refs` and the needs' pointer column cannot be
  written into the live files until the schema of record and the templates
  declare them. **Under either option, the rows land after the build.**
- **The frame test belongs to a sitting.** `tests/test_external_frame.py` pins
  the frame's counts, its spent ids and its all-Approved state, and its
  docstring says it "IS EXPECTED TO BE EDITED BY A SITTING and by nothing
  else".
- **Arms off means harmless.** A built but unused cell, an empty new registry
  and a stage arm that is switched off change no derived stage and no gate
  (AT §10.2c).

The precedent is sitting 3 (log Decisions, 2026-08-20a). The owner ruled in
writing, and an agent made the ratifying Status-change commit on that ruling.

| option | how it runs | cost |
|---|---|---|
| **(a) Sign first, then build** | The sitting rules on this text (a Decisions entry). The build lands as ordinary work items. A later commit writes the rows, already Approved, and edits the frame test. | Two acts. The second is a transcription the owner must check against the first, and it edits the frame outside the sitting that owns it. |
| **(b) Build first, arms off; the sitting is one commit (recommended)** | The build lands first and does nothing: new cells declared but unused, new registries empty, arms off. The sitting commit then writes every row and Status value, edits the frame test, raises the id marks and refreshes the snapshots. The owner reviews that one commit before it lands. | AT §11's "nothing is built before the sitting" becomes "nothing is switched on before the sitting". If the sitting changes a structural name, the build is reworked. |

**Recommendation: (b).** It follows Q20's pattern: review with the arms off,
then approve and switch in one commit. The frame changes only in the sitting's
own commit. The owner reviews real rows, rendered and checked by the real tools,
rather than prose. The rework risk is small: every structural name is already
ruled (Q12, Q16, Q19) except the needs' pointer column, which §3.4 proposes and
the owner can confirm with this answer.

### 0.2 Found: approving the two headline needs lowers the stage

The derived stage treats an Approved need that no Approved requirement cites as
unfinished work at the needs rung (`spine_rules.spine_stage`: *"an
APPROVED-BUT-UNCITED SN is DevStg-Needs"*). No Approved SR realizes either
headline need in its own text. The nearest candidates are SR-006, SR-007,
SR-049 and SR-182, and they state gate steps, the toolchain declaration, stage
derivation and a duplication count. Measured on the live spine with the real
code:

```
today                                                  DevStg-Tests
SN-041 and SN-042 added, Approved                      DevStg-Reqs    (every phase reads DevStg-Needs; the fold floors it)
SN-041 and SN-042 added, Drafted                       DevStg-Tests
both Approved, each cited by an Approved SR that has
  no design or test rows yet                           DevStg-LLReqs
```

<!-- fig: derived="derive_stage._effective over spine_rules.load_spine(docs) at c3134d78, with the two ids added to sn_ids (and, for the third line, sn_draft; for the fourth, two Approved SR rows copied from SR-182 and citing them)" -->

A drop to DevStg-Reqs deselects `smoke`, `design-flows` and `trajectory`
(compare `check.py --stage DevStg-Reqs --list` with `--stage DevStg-Tests
--list`). That is the regression Q20 exists to keep out of every committed tree.
The fourth line shows that approving a requirement alone does not cure it:
the stage holds only once each need is answered by a whole approved chain,
meaning a requirement with its design rows and its test cases.

AT §11 says C1 approves the two needs "with the needs". Following the plans'
convention, that sentence is **REOPENED** here, with this proposed replacement:

| option | consequence |
|---|---|
| **(a) Land both needs Drafted, with their stakeholder and pointer cells; each flips to Approved in the commit that approves the first complete chain answering it (recommended)** | No committed tree reads a drop. The owner rules on the text now, and the Status flip is signed together with the chain that answers the need. |
| (b) Approve them, and derive and approve a whole chain for each at the sitting | Pulls requirement, design and test authoring into the sitting, where no adjudicator has read the chains it approves. |
| (c) Approve them and accept the drop until their chains land | The regression Q20 ruled out, held open for as long as two chains take to write. |

### 0.3 Found: the plan's frame counts predate Q28

AT §5.6 counts "Entities 4 → 4 … Bundles 4 → 6", written before Q28 drew hosted
CI. With hosted CI the frame has **5 entities, 7 bundles and 1 relationship**,
and the new ids are `EXT-006`, `EXT-007`, `B-09`, `B-10` and `B-11`
(`docs/id-watermark`: `EXT = 5`, `B = 8`). This is a correction, not a decision.

### 0.4 Found: Q14's dial move belongs in the sitting commit

Q14 decided *"move the dial to DevStg-Boundary at the sitting"*. AT §11 does not
list it under C1, and C4 runs *"under the moved dial"*, which is consistent with
moving it at C1. This package puts it in the sitting commit (§4). Its
enforcement (§10.2h) is not built, and is needed before C4.

---

## 1. The frame: `external.toml` after the sitting

### 1.1 What changes

| row | change | `system` |
|---|---|---|
| `EXT-001` Development session | **narrowed** to the computer and the working copy; gains `mediates = "EXT-006"` | — |
| `EXT-002` Template | unchanged | — |
| `EXT-003` Adopter | **dropped**; id spent (AT §5.5) | — |
| `EXT-005` Model provider | description re-worded: invoked across `B-10` | — |
| `EXT-006` Human operator | **new**, `operational` | — |
| `EXT-007` Hosted CI | **new**, `interoperating` (Q28) | — |
| `B-01` governed writes in | gains `system` | operation |
| `B-02` authority in | **re-pointed** to `EXT-006`; gains a note | operation |
| `B-04` guardrail verdicts out | note re-worded: the re-run crosses `B-11` | operation |
| `B-05` the Template out | note uses the renamed class, *cross-cutting* (Q6) | delivery |
| `B-09` read out | **new**, the old `B-03` content, returned | operation |
| `B-10` model runner in/out | **new**, `REL-003` promoted | operation |
| `B-11` hosted CI in/out | **new**; absorbs the cut `B-06` and `B-07` | operation |
| `REL-001` | **dropped**, merged into `REL-002`; id spent | — |
| `REL-002` | **shrunk** to Transition | — |
| `REL-003` | **dropped**, promoted to `B-10`; id spent | — |

**Spent after the sitting:** `EXT-003`, `EXT-004`; `B-03`, `B-06`, `B-07`,
`B-08`; `REL-001`, `REL-003`, `REL-004`. The watermark rises to `EXT = 7` and
`B = 11`; `REL` stays at 4.

**One crossing each for the model runner and hosted CI.** Both are drawn
`inout`. The cut hosted-CI frame used two crossings, `B-06` in and `B-07` out,
and splitting `B-11` the same way is the alternative. One crossing per party
matches `B-10` and keeps each exchange in one row.

### 1.2 The rows

Rows not shown (`EXT-002`, and `B-01` apart from its new cell) are unchanged.

```toml
[entity.EXT-001]
name = "Development session"
class = "operational"
mediates = "EXT-006"
description = """The computer and the working copy in its hands: shell, editors, OS, git client, Python and the test runner. Writes reach the system through it, whether a person types them or an agent CLI makes them, and the system's verdicts come back through it. The session HOLDS the checkout; the system owns the governed state those edits become once admitted through the hook floor."""
status = "Approved"
absorbs = "v1 EXT-001; dissolved into it: v1 EXT-005 (git), EXT-007 (OS/filesystem/Python), EXT-008 (test+coverage toolchain)"
notes = """It mediates for the human operator (EXT-006): an outcome landing on its crossings can be one that operator experiences. Who holds authority is policy, declared by the approval dial, not a property of this party."""

[entity.EXT-005]
name = "Model provider API(s) / CLI(s)"
class = "interoperating"
description = """The model services and command-line runners behind every model in use, the primary builder and the adversarial reviewers alike. The kit's own loop invokes them across B-10; a person may also drive one directly, and its writes then arrive through the development session."""
status = "Approved"
absorbs = "v1 EXT-004 merged with the external-reviewer CLI at 13o"
notes = """A model CLI is just a model CLI, whether primary or secondary."""

[entity.EXT-006]
name = "Human operator"
class = "operational"
description = """The person who operates the kit: writes to the system through the development session, holds approval authority, and reads the spine and the views generated from it."""
status = "Approved"

[entity.EXT-007]
name = "Hosted CI"
class = "interoperating"
description = """A remote runner that invokes the declared bar on a push, pull request or schedule, across the OS x Python matrix the job declares, and reports the job verdict and step log."""
status = "Approved"
notes = """Outside this system's design control: it may or may not honour the workflow it is handed. That is what makes it an external party; the obligation the system can carry stays on the shipped workflow (B-05 content)."""

[boundary.B-01]
# unchanged, plus:
system = "operation"

[boundary.B-02]
entity = "EXT-006"
direction = "in"
system = "operation"
carries = """Authority: rulings, attestations and Status flips - the distinguished input the process advances on."""
status = "Approved"
absorbs = "v1 BIF-005/M-11"
notes = """No port of its own: authority arrives as content on B-01's write path. The system can observe that a Status cell changed, not that a person judged."""

[boundary.B-04]
entity = "EXT-001"
direction = "out"
system = "operation"
carries = """Guardrail verdicts during a session: hook-floor accept/reject and subagent_gate PreToolUse allow/deny."""
status = "Approved"
absorbs = "v1 BIF-012/X-07, and the verdict halves of BIF-006 and BIF-026"
notes = """The honest limit belongs in this crossing's SR: a local hook floor is bypassable (git commit --no-verify), so "no unchecked write enters governed state" rests on this verdict at the moment of the act PLUS a re-run of the same bar away from that bypass. Where hosted CI is configured, that re-run crosses B-11. The system holds no design control over whether the runner honours the workflow it is handed, so the obligation it carries stays on the shipped workflow (B-05 content, SR-151 and SR-152)."""

[boundary.B-05]
# carries and absorbs unchanged; plus:
system = "delivery"
notes = "The largest bundle in the frame, and legitimate as one under §3R: a single shall against it is permitted BECAUSE the decomposition is stated in the component details. The delivered capabilities it breaks down into are: harness verdict, scaffold + MAPPING, unattended loop, generators, hook floor, and cross-cutting property -- the sixth being a ruled class for a property of every delivered capability at once, which is why SR-031, SR-034, SR-035 and SR-114 each stay one row in it rather than one per capability."

[boundary.B-09]
entity = "EXT-006"
direction = "out"
system = "operation"
carries = """Read: the spine and the views generated from it - the project-state dashboard, the open-items page, the status surface, the derived stage and the console reports."""
status = "Approved"
absorbs = "v1 BIF-007-out/M-10, BIF-008/M-03, BIF-009/M-19, BIF-010/M-09, BIF-011/M-08 - the former B-03 set, held by REL-002 while the views were not system outputs"

[boundary.B-10]
entity = "EXT-005"
direction = "inout"
system = "operation"
carries = """The loop invoking a model runner: the prompt and brief out; the output, exit code and commits back; and the runner's limits - rate limit, expired authorization, model retirement."""
status = "Approved"
absorbs = "REL-003 (v1 BIF-023/M-15 and BIF-024/M-14)"
notes = """The backoff obligation stays a requirement on the loop content that makes the call."""

[boundary.B-11]
entity = "EXT-007"
direction = "inout"
system = "operation"
carries = """A hosted run of the declared bar: the trigger and the declared OS x Python matrix in; the job verdict and step log out."""
status = "Approved"
absorbs = "EXT-004's cut crossings B-06 (trigger in) and B-07 (verdict out)"

[relationship.REL-002]
from = "EXT-002"
to = "EXT-001"
kind = "hands-off"
flow = """Transition: the Template installed into an operating environment, this repository's own or an adopter's - the only lifecycle hand-off between the delivery frame and the operation frame."""
status = "Approved"
absorbs = "REL-001 (the Template adopted into the Adopter's repository), merged when EXT-003 was dropped"
```

### 1.3 The file's header

- **THE FIELDS** gains two entries:
  - `mediates` on entity rows: *OPTIONAL — the `EXT-###` whose writes this
    party carries into the system and to whom it shows the system's verdicts.*
  - `system` on boundary rows: *CLOSED vocabulary, `operation` (the system in
    use) | `delivery` (the system that builds and delivers it) — the
    system-of-interest this crossing belongs to.*
- **ROW IDS** lists every spent id (§1.1) where it now names only `B-03`.
- **FLIP AUTHORITY** loses *"this repo runs `DevStg-Needs`-held only, so
  DevStg-Boundary is NOT held"*. The paragraph already says to read the dial
  rather than assume it, and after §4 that sentence would be false.

---

## 2. The rulings reversed

### 2.1 For the Decisions entry

Each row is a ruling AT §5.2 traces, with the text that replaces it.

| ruling | what it said | replacement |
|---|---|---|
| **13k** | the human and the loop are one entity; *"who-holds-authority is policy and record, never an entity split"* | The human operator is an entity of its own (`EXT-006`), and the development session (`EXT-001`) mediates for it. Who holds authority stays policy and record (the approval dial): the split is of parties, not of authority. |
| **13n** | the delivery frame: using the guardrails does not make them inputs | The depth-0 view draws two systems-of-interest: the kit in operation, and the system that builds and delivers it. Each crossing declares which it belongs to (`system`). What the kit does while it runs, including its writes, verdicts and rendered views and the runner it invokes, crosses the operation frame. |
| **13u** | `B-03` removed; the generated surfaces are *"not system outputs"* | The generated views are outputs of the kit in operation, read by the human operator across `B-09`. `B-03` stays spent. |
| **`REL-002`**'s flow and notes | self-adoption; invoking `agent-resume` is *"NOT an input"* | `REL-002` is Transition only: the Template installed into an operating environment, absorbing `REL-001`. |
| **`REL-003`** | model providers *"touch the SESSION, never the system"* | The loop's invocation of a model runner crosses the operation frame at `B-10`. Two parts survive: 13o's single entity for primary and reviewer CLIs, and the backoff obligation on the loop content. |
| **Hosted-CI cut** (2026-08-16q) | `EXT-004`, `B-06` and `B-07` cut: *"a hosted runner is an ADOPTER's boundary"* | **Partly reversed.** Hosted CI is drawn as `EXT-007`, with one crossing, `B-11`. Design control survives as the reason SR-151 and SR-152 constrain the shipped workflow rather than a runner's behaviour. Being outside design control is what makes a party external; it is not a reason to leave the party undrawn. The cut ids stay spent. |
| **13o**'s `B-08` | the vendored-doc check *"would be run by the development environment"* | **Reason corrected, not redrawn.** The check fetches a pinned upstream URL, which is not a `B-01` write, so 13o's reason was incomplete. The upstream is not drawn until a repository vendors something (Q28). `B-08` stays spent. |

### 2.2 Rows elsewhere that restate a reversed ruling

These rows become false when the rulings fall. None is in a file the sitting
edits, and all sit on rungs the dial does not hold.

| row | cell | what it says now |
|---|---|---|
| LLR-051, LLR-056, LLR-057, LLR-139 | `detail` | the surface is part of *"the adopted toolkit's generated project-state view (REL-002 output), not a system output"* |
| LLR-124 | `detail` | *"an adopted-toolkit output surface (REL-002), not a system-under-development output"* |
| SR-151, SR-152 | `rationale` | the re-run *"has no crossing of its own"*; the `REL-003` precedent |
| SR-175 | `rationale` | *"the no-design-control reading the frame applies to external actors at REL-003 and the B-06/B-07 cut"* |
| IF-041 | `notes` | invoking an agent CLI *"crosses no boundary of this system"* |

**Recommendation:** file one sweep work item at the sitting. It amends these
rows as Drafted changes through the ordinary adjudication route. The SR and LLR
cells are approved content, so they re-attest, and a separate item keeps that
batch out of C2. Tying IF-041 back to `B-10` is extension work (AT §9) and is
not part of the sweep.

---

## 3. Stakeholders and needs

### 3.1 The stakeholder rows

In `stakeholder-needs.toml`, approved at the sitting as a human-held act (AT
§6.2). Every stakeholder's party is the human operator: an adopting team is
the human operator of the kit in its own repository (AT §5.5).

The plan's row has a name, a party and a status. This package adds
`description`, as entity rows have, because a bare name such as "Reviewer" does
not say which outcomes the stakeholder owns.

```toml
[stakeholder.STK-01]
name = "Owner"
description = """Holds approval authority over the repository, sets its policy and design constraints, and runs it unattended where that is enabled."""
party = "EXT-006"
status = "Approved"

[stakeholder.STK-02]
name = "Adopting team"
description = """A team that adds the kit to its own repository and works under it there."""
party = "EXT-006"
status = "Approved"

[stakeholder.STK-03]
name = "Reviewer"
description = """A person deciding whether to trust what the process reports and what ships, by reading the spine, the verdicts and the generated views."""
party = "EXT-006"
status = "Approved"

[stakeholder.STK-04]
name = "Contributor"
description = """A person developing this repository: setting it up, changing it and keeping it to its own standard."""
party = "EXT-006"
status = "Approved"
```

### 3.2 Which stakeholder owns each need

`stakeholder_refs` is a traced cell (AT §10.2k), so writing it re-attests no
need. Each need gets one stakeholder unless its text names two; none does. Each
assignment is a judgment for the owner to correct.

| stakeholder | needs | reading |
|---|---|---|
| `STK-01` Owner | SN-005, SN-006, SN-025, SN-026, SN-028, SN-029, SN-033, SN-036, SN-041, SN-042 | the policy, the unattended run and the constraints. SN-006, SN-025 and SN-029 are stated about an agent, but the outcome, a walk-away run worth having, is the owner's. SN-033 is any stakeholder reading the needs, and the owner is the one who signs them. |
| `STK-02` Adopting team | SN-001, SN-003, SN-004, SN-009, SN-011, SN-012, SN-027, SN-038, SN-039 | the needs stated about "a team" or "an adopter" |
| `STK-03` Reviewer | SN-002, SN-008, SN-010, SN-023, SN-024, SN-037, SN-040 | the needs stated about "a reviewer", "a reader", or a stakeholder seeing and explaining the system |
| `STK-04` Contributor | SN-007, SN-034, SN-035 | the people maintaining and setting up the repository |

### 3.3 The vision's two headline needs

Drafted under §0.2(a). Both reach the MAINTAINER and TEST-ENGINEER hats, which
apply `always`, so neither needs a tag. Both pass `check_need_form.py --strict`
as written (run against a scratch copy holding the two rows).

```toml
[need.SN-041]
status = "Drafted"
priority = "M"
stakeholder_refs = ["STK-01"]
source = ["README.md#objective-o1"]
need = """**Scope: template (adopters + this repo).** A person reading a project's code or analytics long after it was written can understand what each part does and why it exists, and can change one part without having to understand or rework unrelated parts."""
why = """The vision promises code and analytics that stay readable and correct over the long run. Code that only its author can follow gets rewritten instead of changed, each rewrite drops behavior nobody wrote down, and each later change costs more than the one before."""
acceptance = """A reader new to a sampled part of the code can say what it does and why it exists from the code and the records linked to it, without asking its author. Each change is measured against the project's declared readability and structure measures before it is accepted, and a change that worsens one is reported with the part it worsens."""

[need.SN-042]
status = "Drafted"
priority = "M"
stakeholder_refs = ["STK-01"]
source = ["README.md#objective-o3"]
need = """**Scope: template (adopters + this repo).** The owner can rely on every required behavior being checked by tests written from its requirement before the behavior was built, rather than by tests written afterwards to fit what was built."""
why = """Tests written after the code tend to describe what the code does instead of what was required, so a passing run stops being evidence that the requirement is met, and the approval gates stop meaning what the vision promises."""
acceptance = """Each requirement's test cases are defined and approved before its implementation is accepted, and the project record shows that order for every requirement; an implementation accepted ahead of its test cases is reported."""
```

Two points for the owner's reading:

- **SN-041's acceptance reports; it does not refuse.** A worsening change is
  reported rather than blocked, following SN-012's proportionality. A gating
  mode is a requirement-tier decision, as SR-183 already frames complexity.
- **SN-042's "every requirement" ranges over a closed domain**, the registered
  requirements, so it is the kind of absolute S1 accepts.

### 3.4 The needs' pointer column

| aspect | proposal |
|---|---|
| **name** | `source`. `provenance` would contradict PROCESS.md §3's own rule, *"No provenance in a living registry cell"*. `catalog`, GilbertCore's name, describes one kind of source. |
| **shape** | a list of repository-relative link targets with anchors, e.g. `["README.md#objective-o1"]`; each must resolve to a file and an anchor |
| **rule** | exempt from the provenance rule, joining PROCESS.md §3's pointer columns (`Module`, `CodeSymbol`, `TestRefs`, `Evidence`) |
| **class** | traced, like `SN-Refs`: a pointer, not approved content (Q23's condition, §5 B6) |
| **scope** | optional. Only SN-041 and SN-042 carry it at C1; the existing needs gain it when the census of prose constraints is ruled (S3). |

---

## 4. The dial

`docs/process.toml`: `human_approval_through = "DevStg-Boundary"` (Q14).

- **What it changes.** The frame, and from C2 the assumption and surrogate rows,
  become human-held by policy rather than by convention. Today nothing
  automated writes an off-spine `status` cell, so the change is to the
  declaration, not to behaviour.
- **What it does not do.** It does not stop an automated path by itself. The
  dispatcher's off-spine approval axis *"DEFAULTS FALSE AND EVERY CALLER IN THIS
  MODULE PASSES THE DEFAULT"* (AT §10.2h). That enforcement is needed before
  C4, where the first assumption rows are approved.
- **What it stales.** Two comments paraphrase the old value: the block above
  the dial in `docs/process.toml` (*"THIS REPO RUNS `DevStg-Needs`-HELD
  ONLY"*) and the `external.toml` header (§1.3). Both are rewritten in the
  same commit to point at the dial instead of restating it. A search of the
  tests found none that pins the live value: the one test that reads the live
  `docs/process.toml` (`tests/test_rule_sync.py`) checks its `[checks]` table.
  The sitting commit's bar is the real check.

---

## 5. The build, arms off

Built before the sitting under §0.1(b), after it under (a). The items are AT
§10.2a–c and f, plus S3's column. Nothing here writes a row this repo relies on.

| # | what | where (AT anchors) | adopter cost |
|---|---|---|---|
| **B1** | Frame cells: `system` (closed vocabulary, expected on every boundary row; a missing one is a warn-first finding) and `mediates` (optional; resolves to an `EXT` row) | schema of record (`kitlib/spine.py`); carrier maps (`spine_carrier` / `migrate_carrier`, pinned as inverses); `external.template.toml`'s `-000` rows; resolution in `trace.py` (§10.2a) | schema on resync, deferred |
| **B2** | `assumptions.toml`, a new registry with an applies-when (only where `external.toml` exists): `[assumption.DA-###]` and `[surrogate.SUR-##]` | `DECLARED_INPUTS` (`kitlib/stage.py`), `bootstrap.MAPPING`, snapshot tiers (`baseline_snapshot`), `TOML_REGISTRIES` and its floor, the id spaces `DA` and `SUR` (`trace._offspine_ids`), carrier maps, schema, template, and resolution of `effect_at`, `realized_by`, `emulates` (§10.2b). Ships **empty** here; rows are C2. | template content |
| **B3** | Stage arms present and **off**: the Boundary predicate reading assumption and surrogate rows, and the needs rung reading stakeholder rows; switched on in C4's commit | `spine_rules`, `derive_stage` (§10.2c). Where the switch lives is the build's to settle. | none while off |
| **B4** | The stakeholder list: `[stakeholder.STK-##]` (`name`, `description`, `party`, `status`) and SN `stakeholder_refs` | the same machinery as B2, on `stakeholder-needs.toml`, including the id space `STK`, resolution to `STK` and `EXT` rows, and a status read per tier, since the file then holds two approvable tiers (§6.2, §10.2f) | schema on resync, deferred |
| **B5** | The need `source` column | schema, carrier, template, link validation, rendering (the approval brief and the dashboard's need detail), dogfood sync, and the provenance-rule exemption in `trace.py` and PROCESS.md §3 (S3) | schema on resync, deferred |
| **B6** | Classification, Q23's condition | `acceptance_record.py`'s table: `stakeholder_refs` and `source` traced; a stakeholder's `name`, `description` and `party` approved content. Mirrored in `registry-machinery-reference.md` §10. | none |
| **B7** | Prose | the concept's home is `PROCESS_OPTIONS.md`, since `AGENTS.template.md` has about 20 B of headroom (§10.4); the resync entries stay deferred until the model is firm and must name the adopter prerequisites (§12.8) | — |

**Suggested filing**, once §0.1 is answered: three work items, one each for B1,
for B4–B6, and for B2–B3, with B7 riding the item whose change it describes.
WI-612 lands first if intake's mint is to run in the primary checkout with
uncommitted edits present.

---

## 6. The sitting commit

One reviewed commit, made on the trunk side as the approval act must be, on the
owner's written ruling:

- [ ] `external.toml`: the rows of §1.2 and the header of §1.3.
- [ ] `stakeholder-needs.toml`: `STK-01`…`STK-04` Approved; `stakeholder_refs`
      on all 27 needs (§3.2); SN-041 and SN-042 Drafted (§3.3).
- [ ] `docs/process.toml`: the dial and its comment (§4).
- [ ] `docs/id-watermark` through `trace.py --bump-ids`: `EXT = 7`, `B = 11`,
      `SN = 42`, `STK = 4`.
- [ ] `tests/test_external_frame.py`: 5 entities, 7 crossings, 1 relationship;
      the spent ids of §1.1 asserted absent; its docstrings; the all-Approved
      pin unchanged.
- [ ] `tests/test_dogfood_sync.py`: the `REL-ID` bite-proof plants into
      `[relationship.REL-001]` of the live file and asserts the plant landed,
      so it must move to `REL-002`.
- [ ] `tests/test_hats.py`: the FIRST-RUN-ADOPTER docstring stops naming
      `EXT-003` as a live entity. Its `speaks_for` waits for "Hats per piece".
- [ ] The approval act's snapshot refresh for both edited registries.
- [ ] A log fragment with the Decisions entry: the reversals (§2.1), the
      approvals, the dial.
- [ ] The sweep work item of §2.2, filed.
- [ ] Regenerated derived views; the commit bar, and `trace.py --strict` and
      `check_trajectory.py --strict`, run and pasted.

---

## 7. Not in C1

- **SR cells** (`da_refs`, `coincident`, `form`) and **re-pointing SR
  `boundary_refs`** to the new bundles: C2. AT §5.1 calls the re-pointing
  sitting work. Doing it in C2 touches each SR once, with the rest of its new
  cells. The dashboard SRs (SR-052, SR-053, SR-054, SR-168, SR-169) are the
  first batch, and SR-139, which sits in both frames, is split there.
- **Assumption and surrogate rows**: C2. The mockup's eight DAs and three
  surrogates (`mockups/`) are a starting point, not signed text.
- **TC cells, the DA brief, enforcement of the dial, loop provenance,
  row-level refusal, result records**: C3–C4 (§10.2d, e, g–l).
- **Re-tying IF rows** (IF-041 to `B-10`, the 41 whose far side was the
  adopter) and the dashboard's own IF row: the extension (AT §9, §10.3).
- **Rendering the two frames.** The dashboard draws the new rows in today's
  single view until a renderer change is filed. The mockup still renders
  `system = "kit"`.
- **`speaks_for` on hats**: "Hats per piece", after C1.
- **The census of the remaining prose constraints**: published later for its
  own ruling (S3).

---

## What the owner answers

1. **§0.1:** (a) sign first, or (b) build first with the arms off.
   Recommended: (b).
2. **§0.2:** land the two headline needs Drafted until a complete chain answers
   each (a), approve them with whole chains written at the sitting (b), or
   accept the drop (c). Recommended: (a).
3. **§1–§4:** the text, signed as written or with edits, including the column
   name `source` (§3.4) and the stakeholder assignments (§3.2).
