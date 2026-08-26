# The (e) measuring pass — per-row `contract` verdicts over the 108 non-CLI interface rows

**WI-516**, executing `OI-62`'s ruling (option (e), MEASURE DON'T REWRITE — owner,
2026-08-24; record:
[../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../log.d/2026-08-24-oi62-rule-and-spine-approval.md)).
This document is obligation 1 of that ruling: the per-row verdicts recorded
DURABLY as the follow-on pass's input, one line per row, findable by IF id.
**No `contract` cell was edited by this pass**, and none may be edited on its
authority — the relocation question it feeds is `OI-63`.

The population: the 108 live rows of
[../requirements/interfaces.toml](../requirements/interfaces.toml) that the
`WI-512` CLI pass did not thin (135 live − 27). The comparison figure it is
measured against is `WI-512`'s own
([../log.d/2026-08-24-wi512-contract-generalization.md](../log.d/2026-08-24-wi512-contract-generalization.md)):
**87.7% restatement by characters, 11 of 27 rows (40.7%) carrying a remainder.**

## THE NUMBERS

Reported per family, separately, which is the whole reason the ruling set the
tranche grain: a heterogeneous population must not hide behind one average.
The family split is recovered from the `direction` column `WI-455` shed
(`git show d16ddbb2`), which is where "`Provides` first, then `Consumes`" was
last written down. **All 27 rows `WI-512` thinned were `Provides`**, so
tranche 1 is the 19 `Provides` rows that pass left behind.

| | CLI (WI-512) | tranche 1 · `Provides` | tranche 2 · `Consumes` | combined |
|---|---|---|---|---|
| rows | 27 | **19** | **89** | **108** |
| characters | 7,385 | **10,278** | **33,717** | **43,995** |
| mean chars/row | 273.5 | **540.9** | **378.8** | **407.4** |
| RESTATEMENT | **87.7%** | **75.9%** | **60.8%** | **64.3%** |
| irreducible REMAINDER | 12.3% | **21.2%** | **20.2%** | **20.4%** |
| NON-CROSSING (see below) | — (not a category then) | 2.9% | **19.0%** | 15.3% |
| rows carrying a remainder | 11/27 = **40.7%** | 16/19 = **84.2%** | 55/89 = **61.8%** | 71/108 = **65.7%** |

**The CLI family's number does not generalize, and the direction is the one the
`(d)`-skeptic predicted.** Restatement falls from 87.7% to 64.3%; the share of
rows carrying something real rises from two in five to two in three. Read as the
owner's own question — *how much of what these cells say would be missed once it
is gone* — the answer is **15,690 of 43,995 characters, 35.7%**, against the CLI
family's 12.3%. On a per-row basis it is starker still: only **19 of 108 rows**
(17.6%) are pure restatement end to end, where `WI-512` found 16 of 27 (59.3%).

Two splits inside those numbers, both worth the ruler's attention:

- **`Provides` vs `Consumes` really are different populations.** `Provides` rows
  are longer (541 vs 379 mean) and denser in remainder (21.2%) but almost free
  of non-crossing prose (2.9%). `Consumes` rows carry **19.0% non-crossing** —
  one character in five is neither a crossing fact nor recoverable anywhere.
- **The owner tier is NOT the driver, and that refutes this pass's own working
  hypothesis.** The expectation going in was that requirement-owned rows (no
  `detail` cell to recover from) would carry far more remainder. Measured:
  SR-owned 36 rows, 19.1% remainder; LLR-owned 72 rows, 20.8%. Within noise.
  What the tiers DO differ on is non-crossing prose — 8.6% SR-owned against
  **17.4%** LLR-owned. The extreme individual rows (`IF-127` at 76%, `IF-116` at
  58%) are individual, not a tier effect. Recorded as a refutation rather than
  quietly dropped.

Every headline figure above is the per-row table below, summed — the table is
the derivation, not a copy of one. `rev` stamps the tree the `contract` cells
were read at; this commit edits none of them.

<!-- fig: cmd="python -c \"rs=[l.split('|') for l in open('docs/plans/2026-08-25-if-contract-verdicts.md',encoding='utf-8') if l.startswith('| `IF-')];c=[[int(x) for x in r[2:6]] for r in rs if all(x.strip().isdigit() for x in r[2:6])];print(len(c),[sum(k) for k in zip(*c)])\"" rev=14759fc8 -->

## THE METHOD, stated so the follow-on can re-run it

Every row was READ, never regexed — `WI-512`'s discipline, and the reason this
row was tiered `strong`. Per clause, one of three verdicts.

**RESTATEMENT** — the clause's content is recoverable from a named other home.
Five homes were admitted, and each is held to the code by something:

- **R1 the owner row** — an SR's `requirement`/`acceptance_criteria`, or an
  LLR's `detail`/`module`/`code_symbol`.
- **R2 the module's mechanically harvested surface** — `gen_arch_map.py` scans
  each public symbol's **name, signature (parameter names) and one-line
  docstring summary**, plus the `Contracts: IF-###` line.
- **R3 a committed generated reference or a declared policy home** —
  [../cli-reference.md](../cli-reference.md), `components.derived.toml`,
  `CATALOG.md`, `INDEX.csv`, and the declaration files whose own headers state
  their grammar (`docs/stack.ini`, `docs/process.toml`).
- **R4 the row's own other cells** — `provider`, `consumers`, `component`,
  `req_refs`: the crossing statement itself.
- **R5 the consumed medium's own header** — on a `Consumes` row whose far side
  is a file, that file documents its own schema. This home does not exist for
  the CLI family and is a large part of why `Consumes` restates more.

**IRREDUCIBLE REMAINDER** — a typed crossing fact stated by no such home,
recoverable only by reading an implementation body: precisely the content
`interfaces.toml`'s own header calls *"held to the code by nobody"*.

**NON-CROSSING** — content that is neither recoverable NOR a fact about the
crossing. Two sub-kinds: **M** module internals (which function holds the read,
that an import is lazy) and **X** registry bookkeeping, provenance and argument
(why this row exists, how it differs from its sibling, the incident that
prompted it). This class had no name in `WI-512` because the CLI family barely
carries it, and naming it is this pass's main structural finding — see below.

Character counts for remainder and non-crossing are **spans of the clauses
judged**, not post-edit lengths: `WI-512` could measure its `KEPT` figure by
subtraction because it rewrote the cell, and a pass forbidden to write cannot.
They are therefore accurate to the clause, not to the character, and the
follow-on's authoring pass will move them. The ROW COUNTS are exact.

## THE TAXONOMY — `WI-512`'s three, and seven the population forced

`WI-512` named three remainder kinds: **a written artifact, a fail-loud
guarantee, an exclusion in a comparison**. The ruling invited extension where
the population demands it. It demands it, and honesty first requires saying
that four of the seven were **already latent in `WI-512`'s own kept clauses** —
its stated taxonomy did not cover all eleven of its own rows (`IF-014`'s
idempotence, `IF-016`'s network-gated posture, `IF-044`/`IF-053`'s purity,
`IF-010`'s library-seam designation). So this is the taxonomy catching up, not
a new phenomenon.

| | kind | in WI-512? | exhibit here |
|---|---|---|---|
| **A** | a written artifact / named medium | yes (`IF-001`) | `IF-061`, `IF-047` |
| **B** | a fail-loud guarantee (refusal, cap, vacuity direction) | yes (`IF-015`) | `IF-122`'s three-way ladder, `IF-072`'s fail-soft-in-the-safe-direction |
| **C** | an exclusion or negative claim | yes (`IF-011`) | `IF-125` "never `copy_live`", `IF-059`'s redaction boundary, `IF-129`'s one-way import |
| **D** | a typed shape or wire format | latent (`IF-010`) | `IF-060`'s `FAIL -` line grammar, `IF-107`'s int-vs-string phase coercion, return tuples throughout |
| **E** | a closed vocabulary the consumer must speak | **new** | `IF-058`'s six step types, `IF-097`'s `KIT_PROMPTS`, `IF-099`'s `{slot}` |
| **F** | a CONSUMER-side obligation | **new** | `IF-115`, `IF-124`, `IF-050`, `IF-116` |
| **G** | a posture: purity, idempotence, determinism, network-gating | latent (`IF-014`/`IF-016`/`IF-044`) | `IF-036`, `IF-039`, `IF-098` |
| **H** | a compatibility guarantee | **new** | the `agent_loop` re-exports, `IF-076`'s byte-identical finding strings |
| **I** | the counterparty's own calling convention | **new** | `IF-134`/`IF-135` — how *git* invokes a hook |
| **M/X** | non-crossing (internals; bookkeeping/argument) | **new class, not a remainder kind** | `IF-112`, `IF-082`–`IF-085` |

**F is the category that decides `OI-63`.** A consumer-side obligation is a rule
binding the READER — *"a row that declares a brief this seam cannot compose must
be held for a human"* (`IF-115`, whose own `notes` say it *"would otherwise be
recorded nowhere"*). A provider-side contract header cannot state it; the
provider is not the party bound. Any relocation that assumes one destination
will strand this class.

## THE STRUCTURAL FINDINGS

**1. Eighteen rows carry a remainder of ZERO and are still long.** `IF-082`,
`IF-083`, `IF-084`, `IF-085` and `IF-138` say in their own text that their
contract is another row's (`IF-056`'s or `IF-071`'s) and then spend 110–250
characters explaining why the row exists at all. `IF-112` spends 330 of its 468
characters on the phantom-`SN-000` defect narrative of the carrier it replaced.
`IF-093`, `IF-136`, `IF-137`, `IF-106`, `IF-108`, `IF-111`, `IF-120` are the
same shape. **This is the largest single class of removable content in the
population and relocation is not what fixes it** — a contract header would
inherit the changelog. What fixes it is the field that already exists and is
used ONCE in 135 rows: `rationale` (`IF-141`). An independent mechanism agrees:
`trace.py`'s "Contract argues" advisory fires on **27 rows**, and its "over
ceiling" advisory on **30**, both drawn entirely from this population.

**2. `IF-117` is a second demonstrated rot exhibit, and the `(d)` tripwire
structurally cannot reach it.** Three false claims in one cell: *"the committed
module map is a PUBLIC-API view"* — present tense for `docs/architecture.md`,
RETIRED at `WI-455`; *"the `sym:` tier keeps reading the artifact"* — false,
`load_symbol_oracle` reads `scan_inventory` and says so in its own docstring;
*"41 of this repo's 149 live LLR rows"* — the registry holds **184**. The path
arm stays silent because `docs/architecture.md` is a legitimate
[declared absence](../declared-absences); the symbol arm sees no symbol; a stale
COUNT is invisible to both. Recorded as a measurement. **`OI-61`'s (c) is NOT
re-raised here** — that was ruled out of this row's scope, and this line is the
evidence a future raiser would use, not the raise.

**3. Two further stale claims, neither reached by the tripwire.** `IF-057`
names `system-requirements.csv` as a live source; the carrier is TOML (the
filename has no directory segment, so the path arm never fires). `IF-061`
describes a `work-items.csv` dual-write home this repo no longer carries —
live-but-dormant compatibility code rather than rot, so it is flagged as stale
rather than dead.

**4. One contradiction between a cell and its owner.** `IF-115` says a row whose
brief cannot be composed *"must be held for a human, never dispatched with the
worker assignment"*; `LLR-167`'s `detail` says *"A refusal falls back to the
worker assignment and PRINTS why."* One of the two is wrong. Not adjudicated
here — this pass writes no cell — but the follow-on must not relocate a clause
that contradicts the row it would be relocated toward.

**5. One fact lives in two cells.** The Windows prompt-in-argv refusal is stated
in both `IF-041` and `IF-064`.

**6. Two opaque citations.** `IF-090`'s *"ruled decision 2"* and `IF-094`'s
*"the ruled A1/A8 tables"* name rulings a reader cannot reach from the cell.
This is `IF-080`'s class — a true-looking phrase naming nothing symbolic.

**7. The relocation target has no committed generated home for these classes.**
The CLI family's relocation worked because `gen_arch_map.py --cli-doc` produces
`docs/cli-reference.md`, a COMMITTED artifact with a `check.py` freshness step.
The module symbol inventory has no equivalent: the committed module map retired
at `WI-455` and `docs/stack.ini`'s `[generated]` section declares no successor.
A contract-header convention therefore needs a generated reference AND its
freshness gate built, not just a docstring line adopted — see `OI-63`'s blast
radius.

## THE `(d)` TRIPWIRE TRIAGE — five ambiguous findings, folded into tranche 1

Re-run live at this pass: **7 findings over 5 rows**, unchanged from `WI-512`'s
initial count. `IF-055` is the known real rot and is left standing per this
row's scope. The other five, each with a concrete disposition:

| row | token | verdict | disposition |
|---|---|---|---|
| `IF-038` | `SUBAGENT_GATE` | **FALSE POSITIVE.** An ENV VAR name. `subagent_gate.py` reads it (`"SUBAGENT_GATE=allow override (human-set)"`) and `SR-043` names the override in its own text. | Teach the ALL-CAPS arm that a token also resolves when it appears as an environment-variable key in the declared source surface. |
| `IF-072` | `SCAFFOLD_OMISSIONS` | **FALSE POSITIVE.** A real symbol in `tests/test_dogfood_sync.py`, which is outside `[paths] src` but IS named in this row's own `consumers` cell. | Widen the resolution surface to modules the row's own endpoint cells name. A row declares its own surface; the rule should read it. |
| `IF-061` | `docs/plans/DP-NNN-` | **FALSE POSITIVE.** An id template, not a path; it fires because `docs/` is a real directory. | Decline a path token containing an id placeholder (`NNN`, `###`, angle-bracketed). |
| `IF-132` | `registries/source` | **FALSE POSITIVE.** An English gloss — *"registries/source to dashboard"* — the same class as the already-declined `identity/PII`. It survived because `registries` looks directory-shaped, but no `registries/` exists at the repo root. | Require the first segment to be a real directory AT THE ROOT, not anywhere. |
| `IF-143` | `scripts/x`, `project-trajectory/scripts/x.py` | **FALSE POSITIVE.** `x` is a metavariable in a worked example of the two naming conventions. | Weakest case for a rule change: the honest fix is AUTHORING — the row should use the angle-bracketed placeholder shape the checker already declines. Left as a note; this pass edits no cell. |

**The rule is worth keeping and worth narrowing.** One true positive in seven
findings is a 14% precision that would train a reader to ignore it; four of the
five declines above are principled and mechanical. And the deeper limit is
finding 2: the class that actually bit this registry twice (`IF-055`,
`IF-117`) includes forms — a stale count, a present-tense claim about a retired
artifact — that no token grammar reaches.

## THE PER-ROW VERDICTS

One line per row, keyed by IF id. `chars` is the live `contract` length;
`restated`/`remain`/`non-x` are characters; `cats` are the taxonomy letters
above, with non-crossing letters after a semicolon.

### Tranche 1 — the 19 non-CLI `Provides` rows

| row | chars | restated | remain | non-x | cats | verdict |
|---|---|---|---|---|---|---|
| `IF-020` | 189 | 189 | 0 | 0 | — | LLR-040 detail is a strict superset - stdin payload, the process.toml dial, permissionDecision/exit 2, fail-open. Nothing left over. |
| `IF-058` | 370 | 231 | 139 | 0 | E,B,G | Symbols from code_symbol; caps/agreement/JSON-round-trip from LLR-070. KEPT: the six-value step vocabulary, RoundCapError + the exact cap numbers, 'pure'. |
| `IF-061` | 573 | 404 | 91 | 78 | A;X | LLR-074 covers stability, mapped predecessors, empty Deliverable, line endings. KEPT: the three written artifact paths. STALE: the legacy work-items.csv dual-write clause describes a home this repo no longer carries. |
| `IF-050` | 325 | 175 | 150 | 0 | F | LLR-186 states the record, the fields, the fingerprint and --check. KEPT: the CONSUMER-side rule - every reader goes through kitlib.stage.read_stage and re-derives rather than trusting the copy. A producer-tier owner structurally cannot state it. |
| `IF-064` | 773 | 560 | 158 | 55 | B,D,H;X | LLR-026 covers argv/stdin routing, the no-wedge invariant, codex last-message. KEPT: the Windows .cmd/.bat refusal, both typed return tuples, the agent_loop re-export guarantee. |
| `IF-065` | 713 | 576 | 137 | 0 | D,H | Owner is SR-026, a requirement row with no module surface; the symbol enumeration is recoverable from the harvested inventory. KEPT: the lock descriptor's one-namespace-per-process siting, the re-export guarantee. |
| `IF-066` | 596 | 422 | 174 | 0 | D,E,B,H | LLR-076 covers the round, the fresh sessions, the honest page. KEPT: the (SELECTED|PAGE, detail) return, the one runtime-nonresponse fallback, the re-export list. |
| `IF-074` | 658 | 607 | 51 | 0 | A | LLR-118 is a near-verbatim superset, stamp and masking included. KEPT: the refs/llm/* namespace that does not transport with clone/push. |
| `IF-076` | 671 | 408 | 203 | 60 | G,H;X | Owner is SR-157; the gating-vs-advisory split is in its own acceptance and the four predicates are harvested symbols. KEPT: purity, and the byte-for-byte finding-string stability the three golden files assert. |
| `IF-080` | 659 | 599 | 0 | 60 | ;X | LLR-140 is one of the largest detail cells in the registry and covers the whole refusal ladder, the fail-closed bar read and the audit window. Nothing left over. Non-crossing: the SS1.2/SS2.3 programme citation. |
| `IF-081` | 459 | 365 | 94 | 0 | B | trunk_step is in the generated CLI reference and REGEN_STEPS order is declared verbatim in docs/stack.ini. KEPT: the all-or-nothing compile with fragment deletion, and the red-lane-halts-claiming consequence. |
| `IF-090` | 555 | 515 | 0 | 40 | ;X | LLR-153 is a superset down to the dedup idempotency and the bookkeeping-commit shape. Non-crossing: 'ruled decision 2' resolves to nothing a reader can reach. |
| `IF-097` | 564 | 456 | 108 | 0 | E,F | LLR-162 states load/fill/digest/preflight almost verbatim. KEPT: KIT_PROMPTS as the only vocabulary a caller may use - a module constant, not a harvested symbol. |
| `IF-102` | 862 | 708 | 154 | 0 | D,C | LLR-166 covers the inverse mapping, the sentinels and both raises. KEPT: load()'s file-order DictReader-shaped return, and the -000 filter EXCLUSION (this layer does not apply it). |
| `IF-115` | 816 | 490 | 326 | 0 | D,F | LLR-167 covers Brief-cell selection and the never-partial assembler. KEPT: the whole CALLER-side fail-closed obligation, which the row's own notes say is recorded nowhere else. NOTE: it also CONTRADICTS LLR-167's 'a refusal falls back to the worker assignment'. |
| `IF-123` | 495 | 441 | 54 | 0 | D | LLR-173 is an exhaustive superset of the refusals. KEPT: load_all's (stem, id col) key shape and stamp's (rev, date) tuple. |
| `IF-134` | 307 | 221 | 86 | 0 | I,B | SR-019 carries the --no-verify bypass and the pair claim; LLR-019 is one line. KEPT: git's own calling convention (invoked with no arguments) and the named-check-on-stderr guarantee. |
| `IF-135` | 310 | 67 | 243 | 0 | I,B | SR-020 states only the scan and the block; LLR-020 is one line. KEPT: git's argv/stdin calling convention, the stderr range naming, and the --no-verify bypass (which SR-020, unlike SR-019, does not carry). The least-recoverable row of the tranche. |
| `IF-140` | 383 | 371 | 12 | 0 | D | LLR-199 is a superset and the emitted artifact is itself a committed generated file. KEPT: 'LF, no clock'. |

### Tranche 2 — the 89 `Consumes` rows

| row | chars | restated | remain | non-x | cats | verdict |
|---|---|---|---|---|---|---|
| `IF-021` | 141 | 141 | 0 | 0 | — | Pure crossing statement over a published medium; the tier enumeration is the registries' own names. |
| `IF-022` | 185 | 185 | 0 | 0 | — | SR-007 states the toolchain list verbatim; the [step:*] shape is declared in docs/stack.ini itself. |
| `IF-023` | 384 | 332 | 52 | 0 | B | KEPT: a stray legacy CSV is its own integrity finding. NOTE: 'the `## Interfaces` section of the doc' has no resolvable referent. |
| `IF-059` | 482 | 374 | 108 | 0 | C | The three hat keys ride --prompt-map in the CLI reference. KEPT: the two-file read IS the redaction boundary - a negative security claim SR-155 does not carry. |
| `IF-060` | 544 | 338 | 206 | 0 | D,B | LLR-069 states the 0/1/2 exit ladder and the absent-registry note. KEPT: the FAIL- line grammar the consumer parses, the empty-implicated fail-closed rule, and the typed record projected onto STEP_COVERAGE. |
| `IF-057` | 294 | 228 | 66 | 0 | B | KEPT: registries absent = unvalidated with an honest note, never findings. STALE: names `system-requirements.csv`; the live carrier is TOML. |
| `IF-024` | 320 | 202 | 0 | 118 | ;M | The registry read and the AST inventory are both the crossing. Non-crossing: which function holds the read is module internals. |
| `IF-025` | 136 | 136 | 0 | 0 | — | Pure crossing statement. |
| `IF-026` | 93 | 93 | 0 | 0 | — | Pure crossing statement, the shortest non-CLI row at 93 characters. |
| `IF-028` | 432 | 310 | 22 | 100 | D;X | KEPT: the sym:<module>.<name> reference grammar. Non-crossing: the retired-parse history and the IF-117 sibling note. |
| `IF-029` | 160 | 134 | 26 | 0 | D | KEPT: mermaid sequence blocks as the read format. |
| `IF-030` | 134 | 134 | 0 | 0 | — | Pure crossing statement; --stale is in the generated CLI reference. |
| `IF-031` | 115 | 115 | 0 | 0 | — | Pure crossing statement. |
| `IF-032` | 134 | 134 | 0 | 0 | — | SR-017 carries the always-on floor and the dial. The legacy one-word file names are declared absences, honoured through the migration window - legacy vocabulary, not rot; the row simply never names the one policy home its sibling IF-038 does. |
| `IF-033` | 97 | 97 | 0 | 0 | — | Pure crossing statement. |
| `IF-034` | 88 | 88 | 0 | 0 | — | Pure crossing statement, 88 characters - the shortest row in the population. |
| `IF-035` | 93 | 93 | 0 | 0 | — | The frontmatter field set is the generated INDEX.csv's own columns. |
| `IF-036` | 119 | 103 | 16 | 0 | G | KEPT: network-gated. SR-022 states only the drift detection. |
| `IF-037` | 496 | 384 | 70 | 42 | C;X | SR-026 carries 'the generated status surface never a session input'; SR-031 carries one-parse-one-answer. KEPT: the `## Current State` excerpt narrowing. Non-crossing: the retired docs/run-state note. |
| `IF-038` | 176 | 176 | 0 | 0 | — | SR-043 states the dial, its three values, the override and fail-open. Complete restatement - and a (d) tripwire row. |
| `IF-039` | 138 | 121 | 17 | 0 | G | KEPT: idempotent skip - the WI-512 IF-014 class. |
| `IF-040` | 216 | 216 | 0 | 0 | — | LLR-006 covers the step plan; the cell elides the step list and points at the hook file rather than copying it. An exemplary short row. |
| `IF-041` | 274 | 152 | 60 | 62 | B;X | KEPT: the Windows prompt-in-argv refusal. NOTE: that same clause is also carried by IF-064 - one fact in two cells. |
| `IF-042` | 143 | 143 | 0 | 0 | — | LLR-002 is a superset. |
| `IF-043` | 144 | 144 | 0 | 0 | — | LLR-017 + SR-020 cover it. |
| `IF-045` | 271 | 271 | 0 | 0 | — | The column set and the legacy-Provider read are the consumed medium's own schema; SR-154 carries the absent-enable-list arm. |
| `IF-047` | 213 | 121 | 92 | 0 | A,D,G | Owner SR-154 states the routing obligation, not this read. KEPT: the scoreboard artifact, the VERDICT machine line, the decayed-tally posture. |
| `IF-049` | 159 | 159 | 0 | 0 | — | The [run] grammar is docs/stack.ini's own; SR-046 carries the description arm. |
| `IF-051` | 139 | 139 | 0 | 0 | — | Pure crossing statement. |
| `IF-052` | 378 | 164 | 96 | 118 | B;M | KEPT: absent docs/stage omits the tab and the repo renders byte-identically (SR-070 carries that rule but is not in this row's refs). Non-crossing: the _stage_value/process_panel call path. |
| `IF-054` | 333 | 293 | 40 | 0 | D | SR-148 carries the fail-closed safety arm. KEPT: the Priority=>0 / Exclusive=>empty defaults. |
| `IF-055` | 410 | 333 | 77 | 0 | G,B | KEPT: the library stays side-effect-free; the unclassified/non-ordinary refusal. ROT (already known, not fixed here): SCHED_* names no symbol - the (d) tripwire's founding exhibit. |
| `IF-056` | 768 | 288 | 150 | 330 | B,F;X | LLR-049 answers only for the top-view rule. KEPT: the never-disagree guarantee and the ship-and-resync-together obligation. Non-crossing: 330 characters distinguishing this row from IF-071 and naming its three split siblings. |
| `IF-068` | 383 | 335 | 0 | 48 | ;X | The precedence ladder and the retired jobs dial are both stated verbatim in docs/stack.ini's own [agent-loop] header. |
| `IF-070` | 166 | 120 | 46 | 0 | D | The census grammar is the census file's own. KEPT: the pytest-cov JSON field path. |
| `IF-071` | 785 | 220 | 198 | 367 | B;X | KEPT: the empty-frontier degradation and the one-ranker guarantee. Non-crossing: 367 characters on where the guarded import lives and how this row differs from IF-056 and IF-085. |
| `IF-072` | 705 | 335 | 140 | 230 | B;X | LLR-038 + SR-158 carry the untraced reclassification. KEPT: fail-soft in the safe direction - a malformed entry can never silence real rot. A (d) tripwire row. |
| `IF-073` | 545 | 317 | 228 | 0 | C,B | The column set is open-items.toml's own header. KEPT: a ruled row is deliberately NOT rendered, and the absent-registry empty queue. |
| `IF-075` | 768 | 312 | 66 | 390 | H;X | Owner LLR-001 answers for trace's orphan set, not for reattest_model. KEPT: the byte-identical-across-extraction proof. Non-crossing: 390 characters of extraction argument and component-tagging rationale. |
| `IF-077` | 622 | 221 | 258 | 143 | B,F;X | KEPT: the one-slugifier never-disagree guarantee, the lazy-import degradation, the ship-together obligation. Non-crossing: the pre-commit-hook reasoning and the IF-056 cross-reference. |
| `IF-078` | 241 | 183 | 24 | 34 | H;X | LLR-136 states write_spec_file as the single writer. KEPT: CSV mode byte-unchanged. |
| `IF-079` | 272 | 238 | 34 | 0 | B | SR-129 carries the round-trip. KEPT: --verify never writes either live home. |
| `IF-082` | 413 | 213 | 0 | 200 | ;X | The contract is explicitly IF-056's, said so in the cell. Zero remainder; half the cell explains why the row exists. |
| `IF-083` | 316 | 206 | 0 | 110 | ;X | The contract is explicitly IF-056's. Zero remainder. |
| `IF-084` | 402 | 227 | 0 | 175 | ;X | The contract is explicitly IF-056's. Zero remainder; the tail is a pointer to IF-138. |
| `IF-085` | 463 | 213 | 0 | 250 | ;X | The contract is explicitly IF-071's, degradation clause included. Zero remainder. |
| `IF-087` | 260 | 126 | 134 | 0 | D,B | LLR-038 covers the walk and the GENERATED skip. KEPT: the linguist-generated prefix skip and the two-checks-agree guarantee. |
| `IF-088` | 459 | 260 | 105 | 94 | B;X,M | LLR-198 states owner_cards as the model minus the pause. KEPT: the never-disagree guarantee. Non-crossing: the plan-doc citation and the deferred-import note. |
| `IF-089` | 467 | 306 | 113 | 48 | D,B;X | KEPT: the call parameters (phase unfiltered, require_verified on) and 'the dispatcher itself never mints'. |
| `IF-091` | 305 | 217 | 88 | 0 | C | LLR-158 states the return shape verbatim. KEPT: only the routed traced subset mints, the rest silent by ruling. |
| `IF-092` | 317 | 192 | 125 | 0 | D,B | KEPT: the 18-column schema, self-verifying at write, ConvertError as the all-or-nothing refusal input. |
| `IF-093` | 536 | 370 | 0 | 166 | ;X | LLR-182 is a near-total superset, OUTCOME_DIRS immutability and the re-export included. Zero remainder. |
| `IF-094` | 278 | 208 | 30 | 40 | D,G;X | KEPT: rank order; constants only, no call, no write. Non-crossing: 'the ruled A1/A8 tables' resolves to nothing a reader can reach from the cell. |
| `IF-098` | 290 | 71 | 219 | 0 | D,C,G | Owner LLR-162 is the provider's row and says nothing about this consumption. KEPT: the (key,file,slots,digest) tuple, the 'and nothing else' exclusion, render()'s purity. 75% irreducible - the highest fraction in the tranche. |
| `IF-099` | 489 | 158 | 241 | 90 | E,B,D,F;X | KEPT: the WORKER/REVIEWER/CRITIQUE keys, the never-at-import caching rule, and the single-brace {slot} vocabulary that is also every override file's contract. |
| `IF-100` | 350 | 304 | 46 | 0 | E | LLR-162 + SR-146 carry the strict slot rules. KEPT: the three dual-plan template keys, which the row's own notes confirm are absent from CATALOG.md. |
| `IF-101` | 487 | 165 | 182 | 140 | D,B,F;X | Owner LLR-002 answers for trace's integrity floor and never mentions the watermark. KEPT: the return shape, the raise-rather-than-degrade rule, and the caller's bump-in-the-same-commit obligation. |
| `IF-104` | 505 | 268 | 237 | 0 | B,E | KEPT: resolve()-first so an absent registry SKIPS the tier cleanly, and the scanned Evidence-class cell set. |
| `IF-105` | 414 | 279 | 135 | 0 | C | KEPT: the one consumer needing no column vocabulary - under TOML an id is the table key, so this seam reads keys and nothing else. |
| `IF-106` | 492 | 282 | 0 | 210 | ;X | Zero remainder; the whole tail is the argument for reading through the carrier. |
| `IF-107` | 463 | 273 | 190 | 0 | D | KEPT: Phase arrives as an INT from TOML and a string from CSV, rendered to the same cell text - a type-coercion fact LLR-166 does not carry. |
| `IF-108` | 494 | 264 | 0 | 230 | ;X | Zero remainder; the tail is the feeds-a-model-not-a-check argument. |
| `IF-109` | 546 | 306 | 110 | 130 | D;X | KEPT: the SR Verification cell the critique gate keys on, and the verbatim prose lift. |
| `IF-110` | 455 | 300 | 155 | 0 | B,F | KEPT: this seam is the read half of a read-modify-write (the Modified->Verified flip), so the carrier must answer both consistently. |
| `IF-111` | 512 | 347 | 0 | 165 | ;X | folded_needs is a harvested symbol. Zero remainder; the tail is the phantom-SN-000 incident history. |
| `IF-112` | 468 | 138 | 0 | 330 | ;X | Zero remainder. 330 of 468 characters are a defect narrative about the markdown carrier this seam replaced - the clearest exhibit in the population of a cell used as a changelog. |
| `IF-113` | 697 | 432 | 90 | 175 | F;X | LLR-162 states the PromptError. KEPT: the caller turns it into a REFUSAL to dispatch. |
| `IF-114` | 561 | 166 | 155 | 240 | B,E;X | KEPT: the listed TC cell set and the every-cell-REQUIRED refusal (a dash would read as 'checked, not applicable'). |
| `IF-116` | 760 | 272 | 443 | 45 | D,B,F;X | Owner LLR-002 again silent on the watermark. KEPT: both mint formulae, the raise-rather-than-degrade rule, and the caller-side bump ordering. 58% irreducible on a 760-character cell - the largest single remainder in the registry. |
| `IF-117` | 724 | 424 | 0 | 300 | ;X,R | ROT, three ways, and unreached by the (d) tripwire: 'the committed module map' is present-tense for docs/architecture.md, RETIRED at WI-455 (and a declared absence, which is why the path arm stays silent); 'the sym: tier keeps reading the artifact' is false - load_symbol_oracle reads scan_inventory; and '149 live LLR rows' is stale, the registry holds 184. The exclusion clause it carries is therefore not remainder: it contrasts against something that no longer exists. |
| `IF-118` | 593 | 303 | 90 | 200 | B;X | LLR-166 states the raise. KEPT: the consumer-side fail-closed half. Non-crossing: the '0 pending decisions' narrative. |
| `IF-119` | 553 | 208 | 150 | 195 | D,B;X | KEPT: the CSV branch's own header check, and unparseable-is-an-ERROR-never-an-empty-pool. |
| `IF-120` | 371 | 171 | 0 | 200 | ;X | Zero remainder; the tail is the SN-008 silent-skip argument. |
| `IF-122` | 541 | 331 | 210 | 0 | B | KEPT: the three-way ladder - unreadable REFUSES loudly, present-but-zero-cells reports VACUOUS, absent stays the clean skip. LLR-166 carries only the first. |
| `IF-124` | 473 | 248 | 225 | 0 | F,D | KEPT: the whole consumer-side refusal (with no snapshot the brief HOLDS and names a first-approval question), and the omitted-date render arm. |
| `IF-125` | 374 | 169 | 205 | 0 | C,B | KEPT: the READ-half-only exclusion (never copy_live) and the vacuous-by-absence direction. |
| `IF-126` | 314 | 152 | 162 | 0 | C,B | Same shape as IF-125. KEPT: never copy_live; an absent snapshot is the clean pre-signing skip. |
| `IF-127` | 472 | 95 | 360 | 17 | B;M | Owner SR-140 with no design row answerable - the row's own notes say so. KEPT: the one-model-two-renderers guarantee and the empty-model refusal. 76% irreducible - the highest fraction in the population. |
| `IF-128` | 483 | 393 | 90 | 0 | D | LLR-166/LLR-173 carry both refusals and the resolver reuse. KEPT: the carrier-STRIPPED stem join across a carrier change. |
| `IF-129` | 437 | 332 | 105 | 0 | C | LLR-158 is a superset of the return shape and the structural exclusions. KEPT: the one-way import guarantee - no back-import from check_trajectory. |
| `IF-131` | 503 | 190 | 48 | 265 | D;X | KEPT: the (rel, summary, imports, contracts, rows) record shape. Non-crossing: the retired-map contrast, correctly tensed but now inert. |
| `IF-132` | 327 | 195 | 54 | 78 | D;X | KEPT: the >=1-public-function filter. A (d) tripwire row. |
| `IF-133` | 439 | 379 | 60 | 0 | B | LLR-166 carries the raise. KEPT: the consumer's VACUOUS print. |
| `IF-136` | 478 | 446 | 0 | 32 | ;X | LLR-150 is a near-verbatim superset, 'reports outcomes, decides none' included. Zero remainder. |
| `IF-137` | 444 | 414 | 0 | 30 | ;X | LLR-144 is a superset, 'every lane ends in a merge' included. Zero remainder. |
| `IF-138` | 398 | 233 | 0 | 165 | ;X | The contract is explicitly IF-056's. Zero remainder. |
| `IF-141` | 156 | 148 | 8 | 0 | D | LLR-183 states the derivation verbatim. KEPT: 'sorted'. The ONE row in the registry carrying a `rationale` cell - the schema's own home for the argument every other row puts in `contract`. |
| `IF-142` | 346 | 346 | 0 | 0 | — | keep_examples is a harvested signature parameter; the -000 convention is the kit's declared one. Zero remainder. |
| `IF-143` | 396 | 138 | 138 | 120 | D,B;X | KEPT: the two module-naming conventions the normalizer reconciles, and the one-normalizer guarantee. A (d) tripwire row. |

## Cross-review addendum (2026-08-25, after the close)

An owner-requested cross-family second opinion (`OPENAI-SOL`, record:
[../reviews/2026-08-25-oi63-brief-round/](../reviews/2026-08-25-oi63-brief-round/RESUME.md))
re-summed this document's table EXACT, re-verified both rot exhibits, and
AGREED on 12 of 15 spot-checked rows. No verdict line above is edited; the
three DISAGREE rows are flagged here as re-adjudication candidates for the
follow-on pass, with the reviewer's evidence:

- `IF-050` - the kept clause "every consumer reads it through
  kitlib.stage.read_stage" is a FALSE UNIVERSAL: `kitlib/stage.py`'s own
  "WHO THE FRESHNESS GUARANTEE COVERS" block states the display surfaces
  (`traj_parse._stage_value`, `traj_status._stage_facts`) deliberately parse
  the recorded file directly. Verified in-tree at adjudication. The clause is
  a correction candidate, not a relocation candidate as written.
- `IF-061` - "legacy work-items.csv rows via dual-write" describes a retired
  mechanism as live (CSV append retired at `plan_artifacts.py`); the live
  compatibility guarantee (allocation over ids in both homes) should be split
  from the rot before its class is settled.
- `IF-098` - part of the 219-character remainder (the returned tuple, the
  purity claim) is recoverable from `catalog_rows()`/`render()`'s public
  docstrings (an R2 surface); plausibly only the negative "and nothing else"
  and the never-disagree guarantee remain. Needs remeasurement.

The reviewer also holds that class F (consumer-side obligation) is an
ownership axis over clauses rather than a clause kind - `IF-116` is `D,B,F`,
`IF-124` is `F,D` - and that a provider-side header CAN state a caller
precondition (what it cannot do is keep the consumer synchronized). OI-63
carries that qualification where it bears on the options.

## WI-522 disposition addendum (2026-08-25) — the non-crossing cleanup, executed

`OI-63` is RULED option (d) (owner, 2026-08-25; record:
[../log.d/2026-08-25-owner-rulings-oi63-oi64.md](../log.d/2026-08-25-owner-rulings-oi63-oi64.md)):
*"move information to rationale to clean up the contract text itself before
further shuffle."* `WI-522` is that pass, and this section is its record so the
placement re-ask reads ONE document. **RESTATEMENT and REMAINDER clauses were
not touched** — that is what "before further shuffle" bounds — and no verdict
line above is edited.

**The verdict line was the starting claim, not the instruction.** All 46
`nonx > 0` rows were re-read and re-judged at the CLAUSE before anything moved,
which is why two come back as not-non-crossing at all and why the characters
actually moved differ from the estimate: the verdicts are accurate to the
clause, not to the character, by their own statement.

### The destination has a declared grammar, and it decided eight rows

`rationale` is the schema's own home for the argument, and the kit template
states its grammar: *"the ARGUMENT, never the CITATION … no work-item id,
ruling, sitting, review-round or open-item reference, decision id, edit verb or
date stamp"*. So a non-crossing span that is a bare CITATION — a programme id, a
ruling id, a plan-doc pointer, a dated amendment — cannot move there without
importing a violation into the destination, and deleting it was not ruled. Those
rows are FLAGGED and left exactly as they were. Every cell written by this pass
was checked against the mechanical detector
(`trace_text.provenance_tokens(cell, reason=True)`): **0 tokens over 36 cells.**

**Two findings the executor owes the owner, from checking the destination before
writing into it at scale:**

1. **Nothing lints `rationale` on an IF row.** `trace.IF_REASON_CELLS` is
   `("Notes", "SignalNote")`; `trace_text`'s three provenance column tables name
   SN/SR/LLR/TC/CMP/EXT and no IF tier; no cap, no render and no reader touches
   the cell by name (`IF_CONTRACT_MAX` is `Contract`-scoped and deliberately
   so). The grammar the template declares for this cell is enforced by the
   author and nothing else — the same "the largest pocket is the layer the rule
   cannot see" shape `if_note_advisories`' own docstring names one cell over.
   This pass moved 7,335 characters into that cell and held itself to the
   grammar voluntarily.
2. **An empty `rationale` is a HARD refusal**, not a warning: `spine_carrier`
   raises on an empty-string cell at every live read. A row either carries the
   key or omits it.

### The dispositions, per row

`nonx` is the verdict's estimate above. `before`/`after` are live `contract`
characters; `=` means the cell was not edited. `rat` is the characters written
into `rationale`.

| row | nonx | before | after | rat | disposition |
|---|---|---|---|---|---|
| `IF-061` | 78 | 573 | = | - | **RE-JUDGED** — **NOT non-crossing, and the cross-review was right to flag it.** The 78-character span splits in two, verified in-tree: `legacy work-items.csv rows via dual-write` is ROT — `plan_artifacts.py` records the CSV append (`_registry_header`/`_append_csv_rows`) as retired at Phase 5 — while `ids allocated over BOTH homes` is LIVE, and `_existing_wi_nums` reads the stray CSV and the spec folder both. A stale claim is a correction, not a relocation; a live compatibility guarantee is class H remainder. Nothing moved; the rot is FLAGGED below. |
| `IF-064` | 55 | 773 | 722 | 186 | **MOVED** — the `split out of agent_loop` extraction provenance. The re-export guarantee (class H) stays. |
| `IF-076` | 60 | 671 | 561 | 165 | **MOVED** — the `split out of trace.py` provenance and `which is what makes the split provably behaviour-preserving`. Re-judged WIDER than the verdict's 60 characters — the second clause is the same class as the first. |
| `IF-080` | 60 | 659 | = | - | **FLAGGED** — the whole non-crossing span is CITATION and no argument: `concurrency-restructure SS1.2/SS2.3`, plus `RULING-7` and `RULING-6` naming two of the checks. `rationale`'s declared grammar refuses a ruling id or a programme citation, so the clause cannot be moved there; deletion was not ruled. Left in place, flagged. |
| `IF-090` | 40 | 555 | = | - | **FLAGGED** — `ruled decision 2` is a decision citation that, as the verdict already found, resolves to nothing a reader can reach. It cannot enter `rationale` and deletion was not ruled. Left in place, flagged. |
| `IF-024` | 118 | 320 | 181 | 186 | **MOVED** — the siting clause — which function holds the registry read, and that the module inventory arrives via traj_parse.sw_modules over gen_arch_map.scan_inventory. |
| `IF-028` | 100 | 432 | 231 | 199 | **MOVED** — the retired-parse succession and the IF-117 sibling contrast (`two oracles for two questions`). |
| `IF-037` | 42 | 496 | 450 | 104 | **MOVED** — the retired dispatcher-era `docs/run-state` note. The exclusion it explains (`No next-work or run-phase pointer is read`) stays: that is a class C remainder. |
| `IF-041` | 62 | 274 | 210 | 115 | **MOVED** — the `because the OS may reparse it via cmd.exe` argument. The refusal itself stays. |
| `IF-052` | 118 | 378 | 246 | 130 | **MOVED** — the `_stage_value` / `process_panel` call path (M). |
| `IF-056` | 330 | 768 | 379 | 380 | **MOVED** — 330+ characters distinguishing this row from IF-071 and naming the three split siblings. |
| `IF-068` | 48 | 383 | 332 | 106 | **MOVED** — `so the agent-resume launchers need no dial copies`. The retired jobs dial stays — the verdict reads it as R3 restatement of `docs/stack.ini`'s own header, and restatement is out of this pass's scope. |
| `IF-071` | 367 | 785 | 404 | 409 | **MOVED** — the guarded-import siting, the IF-085/IF-056 contrasts and the derived-once attribution. The one-ranker guarantee was re-cast into the crossing sentence it qualifies rather than lost. |
| `IF-072` | 230 | 705 | 436 | 272 | **MOVED** — `the seam exists because a second reader needs the same facts` and the whole shared-home argument. Side effect, disclosed: this carries the `SCAFFOLD_OMISSIONS` token out of `contract`, so the (d) tripwire's already-adjudicated false positive on this row stops firing. |
| `IF-075` | 390 | 768 | 388 | 384 | **MOVED** — the extraction argument and the component-tagging argument, 370 characters. The byte-identical proof stays. |
| `IF-077` | 143 | 622 | 455 | 243 | **MOVED** — the pre-commit-hook reasoning and the IF-056 cross-reference. |
| `IF-078` | 34 | 241 | = | - | **RE-JUDGED** — **NOT non-crossing.** `the folder half of IF-061's write seam` names which half of a two-row write seam this row holds — a scope narrowing on the crossing statement itself, the same idiom IF-082–IF-085 use. Left in place. |
| `IF-082` | 200 | 413 | 282 | 179 | **MOVED** — `this row exists because a seam is declared per importing module and the import moved`. `The CONTRACT is IF-056's` STAYS — a pointer to the row of record is the crossing statement's own scope, not bookkeeping. |
| `IF-083` | 110 | 316 | 271 | 152 | **MOVED** — the `as HELD by the split sibling that now carries the import` frame. Same reading as IF-082. |
| `IF-084` | 175 | 402 | 190 | 316 | **MOVED** — the split-sibling frame plus the pending-owner-actions relocation note and its IF-138 pointer. |
| `IF-085` | 250 | 463 | 418 | 146 | **MOVED** — the split-sibling frame. The guarded-import siting is this row's own crossing and stays. |
| `IF-088` | 94 | 459 | 413 | 52 | **MOVED+FLAGGED** — `Deferred import, paid only at an exit banner` MOVED. `(docs/concurrency-v2.md §A4, the 2026-08-01 amendment)` NOT moved — it carries a date stamp, which `rationale` refuses; left in place, flagged. |
| `IF-089` | 48 | 467 | = | - | **FLAGGED** — `(docs/concurrency-v2.md §A4 ladder rung 1 / §A5.2)` is a bare plan-doc citation carrying no argument. Left in place, flagged. |
| `IF-093` | 166 | 536 | 424 | 108 | **MOVED** — `instead of drifting as folklore` — the argument for reading the vocabulary from its own module. |
| `IF-094` | 40 | 278 | = | - | **FLAGGED** — `the ruled A1/A8 tables` — a ruling citation naming tables the cell gives no route to. Left in place, flagged. |
| `IF-099` | 90 | 489 | 367 | 151 | **MOVED** — the `because a missing template must be a named PREFLIGHT refusal` argument. The never-at-import rule stays. |
| `IF-101` | 140 | 487 | 327 | 159 | **MOVED** — `Shared rather than duplicated because the mint and the checker must agree on what an id is`. |
| `IF-106` | 210 | 492 | 264 | 227 | **MOVED** — the whole read-through-the-carrier argument (bundle drift rather than silence). |
| `IF-108` | 230 | 494 | 268 | 225 | **MOVED** — the feeds-a-MODEL-not-a-check asymmetry argument. |
| `IF-109` | 130 | 546 | 417 | 128 | **MOVED** — `A cell lost in translation would either skip a required round or narrow what the model was told`. |
| `IF-111` | 165 | 512 | 343 | 168 | **MOVED** — the phantom-`SN-000` incident and the `which is why the seam is declared` conclusion it carries. |
| `IF-112` | 330 | 468 | 129 | 338 | **MOVED** — 330 characters — the clearest changelog exhibit in the population. It moves rather than being flagged because it argues: the heading-arm failure mode IS what breaks without this seam. |
| `IF-113` | 175 | 697 | 450 | 252 | **MOVED** — `whose both-ways strictness is load-bearing HERE rather than merely tidy` and the thin-evidence-section argument. The `PromptError` → REFUSAL rule stays. |
| `IF-114` | 240 | 561 | 307 | 308 | **MOVED** — the carrier-cutover argument and the dash-reads-as-not-applicable argument. The every-cell-REQUIRED refusal stays. |
| `IF-116` | 45 | 760 | 649 | 104 | **MOVED** — `Shared rather than duplicated for IF-101's reason`. Both mint formulae and the caller-side bump ordering stay. |
| `IF-117` | 300 | 724 | = | - | **FLAGGED** — **ROT, not relocatable.** Three false claims re-verified at this pass: `the committed module map is a PUBLIC-API view` is present-tense for `docs/architecture.md`, retired; `the sym: tier keeps reading the artifact` is false (`load_symbol_oracle` reads `scan_inventory`); `149 live LLR rows` is stale against 187 live today. Moving false text into `rationale` would launder rot into a new home. The row is a CORRECTION candidate; correction was not ruled here. Left in place, flagged. |
| `IF-118` | 200 | 593 | 390 | 244 | **MOVED** — the `0 pending decisions` incident narrative. The fail-closed rule it justifies was re-stated in the crossing sentence rather than lost. |
| `IF-119` | 195 | 553 | 339 | 308 | **MOVED** — the declared-header-is-a-carrier-property argument and the `{} reads as a consent decision` argument. Both refusals stay. |
| `IF-120` | 200 | 371 | 161 | 209 | **MOVED** — the `SN-008` silent-skip argument. |
| `IF-127` | 17 | 472 | = | - | **FLAGGED** — `Imported LAZILY.` is 16 characters of module internal whose standing REASON already lives in this row's own `notes` (`keeps trace off the import path of the loop modules`). Moving the bare fact would put it in a third cell of the same row. Left in place, flagged as a de-duplication for the re-ask. |
| `IF-131` | 265 | 503 | 265 | 273 | **MOVED** — the retired-map contrast and the one-walk-one-grammar continuity argument. |
| `IF-132` | 78 | 327 | 187 | 147 | **MOVED** — the retired-parse replacement clause. Side effect, disclosed: this carries the `registries/source` token out of `contract`, so the (d) tripwire's already-adjudicated false positive on this row stops firing. |
| `IF-136` | 32 | 478 | = | - | **FLAGGED** — `(docs/concurrency-v2.md §A4.2)` is a bare plan-doc citation. Left in place, flagged. |
| `IF-137` | 30 | 444 | = | - | **FLAGGED** — `(docs/concurrency-v2.md §A3)` is a bare plan-doc citation. Left in place, flagged. |
| `IF-138` | 165 | 398 | 356 | 129 | **MOVED** — the read-model-carries-the-import frame. |
| `IF-143` | 120 | 396 | 263 | 133 | **MOVED** — `a second reconciliation would be a second answer waiting to disagree`. The one-normalizer guarantee stays. |

### The buckets

| disposition | rows |
|---|---|
| **MOVED** — M/X clauses left `contract` for `rationale` | **35** |
| **MOVED + FLAGGED** — part moved, a dated citation left in place | **1** (`IF-088`) |
| **FLAGGED** — citation-only or rot; not movable, deletion not ruled | **8** (`IF-080`, `IF-089`, `IF-090`, `IF-094`, `IF-117`, `IF-127`, `IF-136`, `IF-137`) |
| **RE-JUDGED not non-crossing** | **2** (`IF-061`, `IF-078`) |
| total | **46** |

### The measurement, taken not estimated

| | before | after |
|---|---|---|
| `contract` characters over the 108-row population | 43,995 | **37,859** (−6,136, **−13.9%**) |
| `contract` characters over the 36 edited rows | 18,611 | **12,475** (−6,136, **−33.0%**) |
| rows carrying a `rationale` | 1 | **37** |
| `rationale` characters | 156 | **7,491** (+7,335) |
| `trace.py` "Contract argues" advisory | 27 rows | **17 rows** |
| `trace.py` over-ceiling (500) advisory | 30 rows | **17 rows** |
| all `IF` row advisories from `trace.py` | 67 | **42** |

<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict-integrity" rev=bad71010 -->

**The moved text got LONGER than the text removed** — 7,335 characters written
against 6,136 removed, +1,199. A clause cut from the middle of a contract
sentence has to become a sentence to stand alone in a reason cell; that is
authoring, and it is disclosed rather than netted out. `OI-63`'s brief sized the
non-crossing population at **6,715** characters over 46 rows: **6,136 of it left
`contract`** (91.4%), and the remaining **679** is the ten rows flagged or
re-judged above.

**THE RESIDUAL 17 ARE NOT 17 ROWS STILL ARGUING — read the count with this.**
Every one of the 17 surviving "Contract argues" fires was classified against the
committed tree, and **all 17 are FALSE POSITIVES**: four are a temporal or
flag-name `since` (`the one home since Phase 5` on `IF-023`/`IF-024`/`IF-079`,
`a --since render` on `IF-074`), and the other thirteen are `X rather than Y`
stating a **class B fail-loud guarantee or a class C exclusion** — the two
remainder kinds `WI-512` itself named. `IF-101`/`IF-116`'s *"raising on an
absent or malformed mark rather than degrading to zero"*, `IF-122`'s
*"REFUSES loudly rather than scanning as empty"*, `IF-114`'s *"refuses rather
than rendering a dash"*, `IF-102`'s *"RAISING when both exist rather than
resolving by precedence"*: a contrast is the natural English for a fail-loud
guarantee, and the connective heuristic cannot tell it from an argument. So the
27 → 17 drop IS real cleanup, and the 17 that remain measure the SHAPE of a
kept remainder rather than any argument left in the cell — precision **0 of
17** on the cleaned population, the same shape as the (d) tripwire's 1-in-7.
Whoever rules the placement question should not read the residue as work
outstanding.

**Two advisory drops are NOT rot repairs and must not be read as any.** The
(d) tripwire's already-adjudicated false positives on `IF-072`
(`SCAFFOLD_OMISSIONS`) and `IF-132` (`registries/source`) stop firing only
because those tokens rode their clauses into `rationale`, which the arm does not
scan. Live tripwire findings after this pass: `IF-055`'s `SCHED_*` (the known
real rot, untouched) and `IF-143`'s two placeholder paths.

### The three cross-review re-adjudications

- **`IF-050` — the reviewer is RIGHT, and it is out of this pass's scope.**
  `kitlib/stage.py`'s own "WHO THE FRESHNESS GUARANTEE COVERS" block states that
  `traj_parse._stage_value` and `traj_status._stage_facts` deliberately parse the
  recorded file directly, so the cell's *"every consumer reads it through
  kitlib.stage.read_stage"* is a FALSE UNIVERSAL — the honest sentence names the
  SELECTION/APPROVAL consumer class, which is what that block does. Verified
  in-tree at adjudication. But a false universal is a CORRECTION, not a
  relocation: the clause is crossing content that is wrong, not non-crossing
  content in the wrong cell. `nonx` stays 0, no span moved, and the correction
  is owed to whoever rules the placement re-ask.
- **`IF-061` — the reviewer is RIGHT, and it changes the row's class.** See its
  table row above: the span splits into a live compatibility guarantee (class H
  remainder) and rot. `nonx` re-judged **78 → 0**.
- **`IF-098` — the reviewer is RIGHT, and here is the remeasurement asked for.**
  Of 290 characters: `(key, file, slots, digest)` per shipped prompt (47) and
  `render()` is pure (18) both appear in `catalog_rows()`'s and `render()`'s
  harvested one-line summaries — R2, confirmed by running
  `gen_arch_map.scan_inventory` over the declared source root — so they are
  RESTATEMENT, not remainder. The crossing statement is 46. What survives as
  remainder is the `and nothing else` exclusion (16) and the never-disagree
  guarantee (65): **81 characters, against the 219 recorded.** The trailing
  `--check`-and-write-path clause (85) counts as remainder only because R2 is
  defined as the HARVESTED SUMMARY and the summary truncates — `render()`'s full
  docstring states it. So 81 on the strict reading, 166 on the pass's own R2
  definition, against 219 recorded. `nonx` stays 0 and nothing moved.

### Flagged for the owner — deletion candidates, NOT deleted

Deletion was not ruled, so every one of these is still in its cell. Each is
non-crossing content `rationale` cannot legally take:

- **Bare plan-doc / programme citations:** `IF-080`
  (`concurrency-restructure SS1.2/SS2.3`, plus `RULING-6`/`RULING-7` naming two
  of its checks), `IF-088` (`docs/concurrency-v2.md §A4, the 2026-08-01
  amendment`), `IF-089` (`§A4 ladder rung 1 / §A5.2`), `IF-136` (`§A4.2`),
  `IF-137` (`§A3`).
- **Citations that resolve to nothing a reader can reach** — the `IF-080` class
  the measuring pass named as finding 6: `IF-090` (`ruled decision 2`),
  `IF-094` (`the ruled A1/A8 tables`).
- **Rot, needing correction rather than relocation:** `IF-117` (three false
  claims, re-verified here), `IF-061` (`legacy work-items.csv rows via
  dual-write`, retired at Phase 5).
- **A row-internal duplicate:** `IF-127`'s `Imported LAZILY.`, whose standing
  reason already sits in the row's own `notes`.

One more, found while reading and belonging to no bucket: **`IF-082`, `IF-083`
and `IF-084` carry `wI-280` in `notes`** — a work-item id the citation-frame
detector misses because `_WI_TOKEN_RE` is case-sensitive. Reported, not fixed:
it is a detector question, not this row's.

### What this pass did NOT do

No `contract` cell lost a restatement clause or a remainder clause. No row's
`status` moved (all 135 read `Drafted`, checked before the first edit). No
kit-side file, script or test changed — the placement question, the contract
header convention, and the `rationale` lint gap above are all still open.
