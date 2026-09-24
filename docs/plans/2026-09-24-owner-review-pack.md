# Owner review pack: re-posed items, reopened decisions, new findings

**Prepared 2026-09-23/24 for the owner's next session. Not a ruling.** It
gathers, in one place, everything the owner still has to decide on the two
plans, with the facts researched since the owner's last answers:

- [the assumption-tier plan](2026-09-20-validation-gap-and-the-assumption-tier.md)
  ("AT"; decisions in its §12.1)
- [the sister plan](2026-09-23-owner-notes-spine-sessions-and-tests.md)
  ("SP"; questions in its §5)

The plans stay authoritative. This pack is a working surface for one review
pass: each answer gets recorded back into the plan's decision table, as before.

**Where the facts came from.** Four read-only research passes (2026-09-23/24):

- a cross-check of an adopter repo, GilbertCore (`C:\Projects\GilbertCore`,
  kit stamp `0fc58fb`, 2026-07-31), against every scoped change;
- a CLI token-usage research pass, with one live fixture per CLI;
- a code-facts pass on the lane-to-trunk path (S9, S11);
- a code-facts pass on S3, S5, S6, S13 and S14.

Key claims were spot-checked against the code before writing this. Anything a
pass could not verify is marked *(unverified)*.

**Suggested order.**

1. **Part A** — four decided items the adopter check reopens.
2. **Part B** — the seven re-posed items.
3. **Part C** — defects found along the way (no decision; file or not).
4. **Part D** — what the kit can learn from GilbertCore (optional reading).

---

## Part A — Decided items the adopter check reopens

Following the plans' convention, a decided answer that new facts overturn is
marked **REOPENED** with a proposed replacement, never silently changed.

### A1. Q16's `system` values mean nothing in an adopter's repo

**What was decided.** Each bundle carries `system = "kit" | "delivery"` (AT
§5.1).

**The problem.** An adopter's `external.toml` describes **its own** system, not
the kit. For GilbertCore that is a robot platform. `system = "kit"` on its
household-user crossing would be false. That breaks the kit's own rule: *a
token the kit mandates into an adopter's cell must mean something in their
repo* (CLAUDE.md). AT §5.1 also states the orientation backwards: *"For an
adopter only the kit frame exists."* For an adopter, the kit in operation is
part of its **enabling** system. The two-frame idea itself transfers well:
GilbertCore's build-package and deployment interfaces are its delivery side,
and its operator and household crossings are its operation side.

| option | consequence |
|---|---|
| **(a) Adopter-neutral values: `system = "operation" \| "delivery"` (recommended)** | Means the same thing in every repo: the system in use, and the system that builds and delivers it. "Kit" stays in this repo's own rows and prose. |
| (b) Keep `kit \| delivery` | False in every adopter repo; violates the copy-ready rule. |
| (c) Make the cell kit-only (not shipped) | Adopters lose a useful split that already fits their data. |

AT §5.1's adopter sentence needs correcting under any option.

### A2. S4's retirement records would be deleted automatically

**What was decided.** Retired rows get a structured fragment in `docs/log.d/`,
lookup-only for agents (SP §1.4).

**The problem.** `trunk_step.py` compiles every top-level `docs/log.d/*.md`
into `docs/log.md` and then deletes the file (`trunk_step.py:182`, `:336-365`).
A retirement fragment would be folded and removed on the next refresh.
"Append-only by check" would then find nothing.

| option | consequence |
|---|---|
| **(a) A subdirectory the fold skips, `docs/log.d/retired/` (recommended)** | The glob is non-recursive, so files there survive. Needs an `orphans-allow` line in the template. Smallest change. |
| (b) Let them fold into `log.md`; the check and renderer read `log.md` | No new path, but "lookup-only" becomes a search through a 60,000-line log. |
| (c) A separate registry file | A new registry, with its own machinery. |

### A3. S2's "design expectation" clashes with "expectation" in the needs tier

**What was decided.** Call LLRs "design expectations" in prose (SP §1.2;
consistent with Q9).

**The problem.** The kit's own needs template already uses the word for needs:
*"a failure-mode expectation"* (`stakeholder-needs.template.toml:16`, `:78`).
GilbertCore has 13 "edge-case expectation" needs. The same word would name two
tiers.

| option | consequence |
|---|---|
| **(a) A different name for the LLR tier (recommended)** | Candidates: "design commitments", "design rules", "design detail". No clash in either repo. |
| (b) Keep "design expectation" and rename the needs usage | Touches the needs template and every adopter's needs prose. |
| (c) Keep both | One word, two tiers. |

### A4. Rig rows can't describe an adopter's stand-ins (Q6, AT §5.3)

**What was decided.** Rigs are `[rig.RIG-##]` rows with `emulates = "EXT-###"`,
an external party.

**The problem, twice over.**

1. **Scope.** GilbertCore's stand-ins mostly emulate **its own** parts: a
   simulated plant for the robot and household, a software-in-the-loop runtime,
   a simulated world standing in for the servo bus, camera and IMU drivers. An
   `EXT` id can't name any of them. The plan defers internal assumptions
   (AT §10.1), yet its own robotics example (*"the contact model grips like the
   real gripper"*) is internal.
2. **The word.** In GilbertCore "rig" means the **real** hardware (the stereo
   rig, the tabletop rig, the bench rig). A row saying a rig emulates the rig
   reads backwards.

| option | consequence |
|---|---|
| **(a) Widen and rename (recommended)** | `emulates` may name an entity, component or interface, and may list several; add a field naming the interface the stand-in plugs into. Rename the row kind to `standin` (or `surrogate`). |
| (b) Widen only | Fixes scope; the word still reads backwards in hardware projects. |
| (c) Keep, and build the design-tier assumption space first | The internal case waits for a later id space. |

**Two smaller naming notes from the same check.** `form = "package-wide"`
misreads where "package" means a software package; `system-wide` or
`cross-cutting` doesn't. And AT uses "standing" for two different things: the
assumption's validity (`active | falsified`) and its evidence
(`assumed | specified | monitored | sampled`). The evidence ladder wants its
own word.

---

## Part B — The re-posed items, with facts

### B1. S11 — one trunk commit per work item: the facts argue against squashing

**Where it stood.** Leaning (i): squash the lane on merge, with the
adjudicator's reviewed commit setting a merge flag.

**What the code shows.**

- **Squash contradicts an owner ruling in force.** RULING-6: *"Product changes
  reach the trunk only through the integrator's merge, made `--no-ff` so merges
  are distinguishable in history. Mechanized: a check flags any non-merge trunk
  commit…"* (`concurrency-restructure.md:224-230`). The audit
  (`integrate.py:2897`) would flag every squash commit, and the dispatcher
  treats a failing audit as fatal (`dispatch.py:780-782`).
- **It breaks two live code paths.** Lane cleanup uses `git branch -d`, which
  refuses a squash-merged branch (`integrate.py:2071-2074`), and a partial close
  records lane commit ranges that stop resolving once the lane is gone
  (`kitlib/station.py`, `adjudicate_brief.py:303-331`). An approved LLR
  (LLR-140) and interface IF-080 specify `--no-ff`.
- **The kit has recorded this hazard itself** (RESYNC_PACK: *"Do not squash
  away an active lane's claim history"*; repo-lock D-1).
- **Even squashed, a work item is three trunk commits:** claim, merge, and the
  post-merge intake mint (for example WI-580: `1af07567`, `dc36375f`,
  `48fbcaa5`).
- **The claim can't fold in.** The merge queue, crash-resume and the frontier
  all read the claim from trunk. "One lane" isn't declared anywhere; the
  template ships `lanes = 2`.
- **The merge trigger is already mechanical.** *"The outcome is not a flag
  anyone sets: it IS the folder the branch moved its specs into"*
  (`integrate.py:21-28`). A separate flag would be a second signal for one fact.
- **The adjudicator isn't on a build lane.** A build lane merges on its review
  verdict; approval of its Drafted rows happens later in a separate
  adjudication work item (the 2026-09-01 ruling), and a non-adjudication lane
  that flips Status is refused (`integrate.py:1129-1168`).

| option | consequence |
|---|---|
| **(a) Keep `--no-ff`; read trunk with `git log --first-parent` (recommended)** | Trunk already reads as one merge per work item (plus its claim and mint), with the lane's detail one level down. No ruling changes, nothing breaks. If the claim and mint commits are the noise, a dashboard or log view can group them by work item. |
| (b) Squash, with an explicit RULING-6 amendment | Needs: amending RULING-6, LLR-140 and IF-080; reworking cleanup and partial-close records; keeping lane refs (for example `refs/lanes/*`) so hash-keyed records resolve; a RESYNC entry. |
| (c) A machine approval writer | Unchanged: its own ruling under OI-45. |

**Your stated goal was one commit per work item on the working branch.**
Option (a) gives that view without rewriting history. If you want the trunk's
*actual* commit count reduced, it has to be (b), and it's a large change.

### B2. S9 — "verify, don't isolate": what the check keys on, and who verifies

**Decided:** reviewers commit in the lane; a check refuses a reviewer commit
that touches anything but its verdict file.

**Facts.**

- **Reviewers already commit their own verdicts**, so OI-76 is untouched
  (`reviewer.template.md:41`).
- **Nothing on a commit reliably names its role.** Every commit has the same
  author; subjects are free-form (an ADJUDICATE commit was titled `review:`);
  reviewers carry no trailer.
- **What *is* reliable:** the coordinator records each session's phase and its
  exact commit range (`# phase:`, `# commits: before..after`) in the session
  log (`agent_loop.py:4014-4019`). The check can key on that: for a REVIEW
  session, the range must add exactly its verdict file.
- **No dirty-tree check runs per session.** Leftover edits from a reviewer
  could be committed by the next build session under its name.
- **Who does "the final pass" on a build lane?** Your model has the adjudicator
  verify before the merge, but no adjudicator touches build lanes today. The
  existing merge ladder (`_merge_refusal`) is the natural place for a
  mechanical re-check.

**To decide.**

| question | recommendation |
|---|---|
| Key the check on the coordinator's recorded session range and phase (not on authors, subjects or trailers)? | Yes. |
| Run it twice: right after each review session, and again at merge from the committed session logs? | Yes. The second makes it evidence, not trust. |
| On a build lane, is the "final pass" the merge ladder's mechanical check (no adjudicator), or should build lanes gain an adjudicator step? | The merge ladder. Adding an adjudicator to every build lane is a much larger change. |

### B3. S13 — builder bias and Done-when

**Re-posed:** the planner writes Done-when before the build, and a lane that
edits its own Done-when is flagged.

**Facts.**

- **No role owns writing Done-when, and most work items lack one.** 11 of the
  18 open work items have no identifiable Done-when list. There is no PLAN
  session in the lane loop. Today Done-when is written by owner-directed
  sessions, copied during consolidation, or written by builders.
- **Builders do move it, occasionally.** Of every commit ever made: 14 commits
  across 10 work items edited their own Done-when text in their own lane, most
  in July. Three changed its meaning: WI-120 weakened an item and ticked it;
  WI-228 redefined one; WI-580 narrowed one and was caught by review
  (REVIEW-A round 008, MINOR) and reverted.
- **Ticking with evidence is the normal convention**, so a naive "Done-when
  changed" check would fire on every tick.
- **A precedent exists for the flag:** amended approved spine text already
  mints an adjudication row at merge (`intake.py:2188`).

| option | consequence |
|---|---|
| **(a) Two rules (recommended)**: every claimable work item has a Done-when, written before claim by whoever files it; at merge, compare its item text at claim vs merge (ticks and trailing evidence stripped) and flag any change to the reviewer and adjudicator | Closes the gap the history shows; follows an existing precedent; no new role. |
| (b) The flag only | Catches movement, but 11 of 18 items have nothing to move. |
| (c) A dedicated planning session per work item | A new strong-tier session per item; the plan's earlier review found this neither cheap nor independent. |

### B4. S6 — observation tests at checkpoints

**Re-posed:** triggers evaluated only at checkpoints; "changed since last
judged" by a stored digest; one record shared with the assumption tier.

**Facts.**

- **Only five tests are non-automated** (TC-036, TC-055, TC-209, TC-210,
  TC-211), and none has a machine-readable "last run". Dates survive only in
  prose. TC-036 has never been judged; TC-211 can't pass until the SR-161
  producer exists.
- **Work-item merge is a real, serial event:** `integrate_one` merges, then
  runs post-merge intake inside the held slot, which already compares
  before/after trees (`integrate.py:2766`). A "due for re-judgement" mint fits
  there.
- **The digest idea already exists:** consolidation's `Digests` cell, *"a
  judged queue state is never judged again"* (`consolidate.py:34-39`).
- **Phase close is not a code event.** Nothing detects that a phase closed.
  **Release** is human-invoked and has never run here.

| option | consequence |
|---|---|
| **(a) Checkpoints = work-item merge and release (recommended)** | Both are real events. Phase close joins later if it gets a defined trigger. |
| (b) Also define a phase-close command | Adds a new event to the process. |

### B5. S3 — design constraints as needs: the size of it

**Facts.**

- Of the 27 needs, about 9 are mainly the owner's design constraints and about
  7 are outcomes with a constraint embedded (a judgment count).
- **About 25–30 constraints stated in prose have no need row.** The largest
  gap is the vision's own two headline promises, **readable, maintainable
  code** and **test-first**, which have no need row at all. Others:
  - one fact, one home;
  - right-size the solution;
  - scope is a promise;
  - fail loudly;
  - no provenance in living cells;
  - ask, don't assume;
  - edit conservatively;
  - the commit bar is results and seconds.
- **The provenance anchor needs its own column.** Both the `need` and `why`
  cells are ruled out for pointers (PROCESS.md's provenance rule), so it must be
  a pointer column declared exempt from that rule, as `Module` and `Evidence`
  already are.
- **GilbertCore already has one:** a `Catalog` column citing a needs catalog.
  S3's column should be general enough to take it.

| option | consequence |
|---|---|
| **(a) Proceed at the assumption-tier sitting, starting with the vision's two headline promises, as a general "provenance" pointer column (recommended)** | A sizeable authoring and re-attestation batch, but it closes the biggest gap first. |
| (b) Only the ~9 constraint needs that already exist get a provenance cell | Cheap, but leaves the vision's headline promises unowned. |

### B6. S8 — token telemetry: the research result

**Facts** (live fixtures from all three CLIs, 2026-09-23):

- **Every CLI can emit structured usage** without losing the final text:
  - Claude: `--output-format stream-json`, already used.
  - codex: `exec --json`, which works together with `-o`.
  - opencode: `run --format json`.
- **The codex and opencode routes throw it away today.** On a successful codex
  call, `run_session` replaces the captured stream with the `-o` text, so every
  usage field is blank. Only 27 of 188 codex logs hold any token line, all from
  failed sessions.
- **The three CLIs disagree on what "input tokens" means.** Claude and opencode
  count cached tokens separately; codex counts them inside input. One column
  would hold two incompatible numbers.
- **The published schema is the OpenTelemetry GenAI conventions**
  (`gen_ai.usage.input_tokens`, `…cache_read.input_tokens`,
  `…cache_write.input_tokens`, `…output_tokens`,
  `…reasoning.output_tokens`). Caveat: every name is still *Development*
  status, and in June 2026 they moved to a new repository that has no releases
  yet, so the kit should pin a commit. It has no cost or context-occupancy
  field; those stay kit fields.
- **Prior art reads the same local files the kit could** (ccusage, tokscale).
  None publishes a session-record schema of its own.

**Recommended decision:**

- adopt the OTel GenAI names, pinned to a commit, in their "inclusive" form;
- store fresh input as a derived field and keep raw usage verbatim;
- add provider and CLI columns;
- keep billed tokens and context occupancy in separate columns;
- add `--json` to the codex route and `--format json` to the opencode route;
- keep OTel exporters optional.

This lands in S7's record step.

### B7. S5 and S14 — smaller items

**S5, module-scoped inner loop.** Builders are told nothing about which tests
to run while iterating.

- **By file name,** "run `tests/test_<module>*.py` first" finds a test for 61
  of 82 modules, but only about 11% of the tests that exercise a module. For
  shared libraries it's close to zero.
- **A map derived from the spine** (a module's LLRs, then the TCs verifying
  them, then their evidence files) covers all 82.
- **Recommendation:** option (d), an inner loop only, using the spine-derived
  map, with the smoke bar unchanged before every commit.

**S14, operation count.**

- **What exists:** the only executed-path measure today is wall-clock time. The
  kit's performance-budget rows (`performance-budgets.csv`) already declare
  pinned commands, with a comparator (`check_perf.py`) and a baseline protocol.
- **What fits:** counting executed calls with `cProfile` over one of those
  declared commands, as a warn-only trend in `check_perf.py`. That needs no new
  comparator, dependency or gate.
- **The limit:** instruction-level counting (closer to "clock cycles") needs
  Python 3.12+, above the kit's 3.11 floor.
- **Recommendation:** keep it parked as research. If pursued, it is one more
  performance-budget metric, never a gate.

---

## Part C — Defects found along the way

These are **not** decisions; they are bugs or gaps in the current kit that the
research surfaced. Each can be filed as a work item.

| # | defect | evidence |
|---|---|---|
| C1 | **Context occupancy is computed wrong.** It divides *cumulative* billed tokens (every step's re-sent context, plus output) by the window, so the index shows readings up to **34,836%**. Occupancy is the latest request's prompt size divided by the window. | `agent_loop.py:3253` `family_context_telemetry`; `docs/iteration_index.md` "Ctx %" column |
| C2 | **codex and opencode usage is never recorded** (B6). Claude's `reasoning-tokens` is always blank (the parser reads a field no CLI emits), and `reported-model` goes blank when a background model appears beside the main one. | `agent_session.py:536-538`, `:617-621` |
| C3 | **The loop can act on an uncommitted verdict.** `read_verdict` reads the verdict file from disk whether or not it was committed, so the loop can route on a verdict the gate can't see. | `agent_loop.py:1072-1085` |
| C4 | **A later session could rewrite an earlier review round's verdict file.** The train's own review folder is excluded from the implementer-touch check, and the gate reads round files at the branch tip. *(read, not driven)* | `verdict.py:854`; `integrate.py:1460-1468` |
| C5 | **The reviewer brief points at an empty folder.** It names "the docs/specs spec-of-record", but `docs/specs/` holds only the README and the example here. Specs now live in the work-item files. | `reviewer.template.md:39` |
| C6 | OI-76 says the verdict trailer rides "the round's own commit"; the code puts it on the coordinator's next commit (and says so). The ruling text and the code disagree. | `log.md:54643-54656`; `verdict.py:70-71` |
| C7 | `docs/agents.toml` records opencode 1.17.18 as tested; 1.18.29 is installed. | `agents.toml` OPENCODE notes |

---

## Part D — What the kit can learn from GilbertCore (optional)

GilbertCore's household-safety needs are verified only in simulation, which is
exactly the gap the assumption tier addresses. The assumption tier fits a
physical robot better than it fits the kit. GilbertCore already does several
things the plan only proposes:

1. **A mechanical check that a stand-in plugs into the real interface.** CI
   compares the simulated and real graphs, and only whitelisted edge nodes may
   differ. The plan asserts this for rigs but never checks it.
2. **Gate on the characterized simulation, not the idealized one.** CI runs
   suites both ways and gates on the characterized one: a concrete use of a
   fidelity delta.
3. **Record once, replay on every commit.** A dated hardware capture is
   processed by tree-bound automated tests. The plan's result record should
   allow "tree-bound result over a dated recorded input", not force it into
   *sampled*.
4. **An honest "blocked: hardware absent" result.** The plan's evidence states
   have no "due, but the rig or hardware isn't attached".
5. **Machine-readable operating envelopes.** 40 of 44 SRs carry a
   `Permutations` envelope. `holds_when` could optionally use that grammar,
   which argues against retiring the layer AT §10.5 calls dormant.
6. **For the guard rule (S15):** list "a device or sensor" as a trust boundary.

**The pre-existing gap.** GilbertCore is 2,260 kit commits behind, with 113 of
152 dated resync entries still to take. It has no `external.toml`, TOML spine,
closed Status vocabulary, snapshot or `docs/stage` yet. So none of the scoped
changes collide with live content today: they land on top of that resync. Two
consequences for the plans:

- `assumptions.toml` needs an applies-when: only where `external.toml` exists,
  with the "unclassified SR" warning conditional on it (otherwise all 44 of
  GilbertCore's SRs warn with no way to fix it).
- The resync entries for C1, C3 and E must name their prerequisites by pack
  anchor.

No id prefix or cell name collides, and every kit-owned script there is
byte-identical to the kit at its stamp, so the session-service work arrives as
a plain overwrite.
