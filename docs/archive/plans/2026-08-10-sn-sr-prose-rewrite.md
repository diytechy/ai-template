> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# SN / SR prose legibility rewrite — a sitting-ready proposal

**Status: PROPOSAL. Nothing here is executed.** No registry row was edited to
produce this document. It exists to be ruled on at the P0 sitting's part 2, row
by row, and then executed as one batch.

**Mandate.** [`repo-lock.md`](../../repo-lock.md) §8.3 item (1): *"SNs written from
the end-user's perspective, around accessible end-user interfaces, plain
language, no implementation references."* The seven challenge notes recorded
with that item are treated as binding constraints, not commentary.

---

## Review record

**Reviewed 2026-08-11 by gpt-5.6-sol (codex, medium effort), adversarial brief.
Verdict on revision 1: NOT safe to hand to the owner sitting as-is — 12 required
corrections.** This is revision 2. Every finding was re-verified independently
against the repo before being accepted; two were refuted in part, and one
reviewer finding led to a **third defect neither pass had found** (SR-126,
below).

**Round 2 — verification pass, same reviewer, 2026-08-11.** Scope-limited to
whether the 12 corrections actually landed. Result: corrections 1–3, 5, 6, 8,
9, 11 verified applied (six qualifier rows sampled word-level, all clean);
four residuals found and fixed in this revision by the coordinator — the
"three fail §B.0" conflation (correction 4), SR-082's acceptance-cell
ambiguity (correction 7), the `gate_policy` site count (correction 10, settled
at 10 token lines + 2 live-interface lines), and the correction-12 disposition
recorded as an accepted block rather than a defined interface. The dispositions
in the table below reflect the post-round-2 state.

| # | correction | disposition |
|---|---|---|
| 1 | Reclassify or restore every laundered qualifier | **APPLIED** — all 12 caught rows restored verbatim; none defended |
| 2 | SN-028 form (i) must retain `single`/`hand-edited`/`machine-read`/`bare [section]`/canonical file/parser agreement/migration interface | **APPLIED** — and the internal inconsistency the reviewer caught (form (i) already dropping what form (ii) claimed to drop) is fixed |
| 3 | Exact full replacement cells for every SR; no "lead + clauses" outlines | **APPLIED** — 17 rows with exact text and a word-delta ledger; **13 rows dropped from the batch** rather than presented as outlines |
| 4 | Obligation-coverage matrix for every form-(ii) re-homing | **APPLIED** — §B.0; two re-homings (SN-005, SN-007) fail the matrix and are blocked. SN-011's form (ii) is blocked on *separate* grounds: its coverage rows PASS, but revision 1's form (ii) invented a stricter obligation than either the need or SR-034 states, and is withdrawn (round-2 correction — the earlier "three fail §B.0" claim conflated the two failure modes) |
| 5 | Fix invalid receiving targets (superseded SR-044; SN-005 CI; SN-007 per-change coverage) | **APPLIED, and escalated** — SR-044 replaced; SN-005's CI obligation and SN-007's per-change coverage have **no receiving SR at all**, which is a decomposition gap, not a prose problem |
| 6 | Withdraw SR-018 as a defect | **APPLIED — reviewer confirmed correct.** Verified: `check_privacy.py` falls back to `docs/privacy-check`, and all three shipped hooks read it |
| 7 | Mark SR-085/SR-108/SR-082/SR-125 CANNOT VERIFY | **APPLIED in full at round 2.** Revision 2 held SR-082 out on the ground that its Requirement cell says "the **retired** three-value enum" explicitly; the round-2 verification pass countered that SR-082's *acceptance* cell separately says "page according to gate policy" — the same ambiguous phrase as the other three. Accepted: **SR-082 is CANNOT VERIFY as a stale-text claim** on its acceptance cell, while its Requirement-cell legibility rewrite in §E.1 stands conditional on the sitting confirming the drain-dial reading |
| 8 | Keep SR-040 as confirmed | **APPLIED** — kept, and its replacement text now also carries the migration-window clause the reviewer's SR-018 evidence established |
| 9 | Promote SR-002/SR-147 to current corrections | **APPLIED with a precision fix** — the cutover is **staged, not committed** (`git status`: `A` on the TOML, `D` on the CSV, `interfaces.csv` still `UU`). They are corrections owed **with the cutover commit**, which is stronger than "forward-looking" and more precise than "already stale" |
| 10 | `PROCESS_OPTIONS.md` `gate_policy` on the consequence list | **APPLIED; count settled at round 2.** **10 distinct lines** carry the literal `gate_policy` token (11 occurrences — line 27 carries it twice). Two further lines (364, 371) carry the hyphenated `--gate-policy` flag and `docs/gate-policy.md` — the flag is a *live, sanctioned* interface (repo-lock §5: it "still takes the WORD but translates it"), so those two are not enum residue and revision 2's "12 sites" overcounted. The `test_rule_sync.py` pin does **not** cover the prose doc (see below) |
| 11 | Resolve "SN always human-attested" before admitting the draft SR | **APPLIED** — flagged for explicit owner ruling; the draft SR is not presented as adoptable until it is ruled |
| 12 | Define the Linux double-click interface | **APPLIED** — marked **CANNOT VERIFY** for Linux in items 2 and 3. Round-2 note: the verifier observed no Linux interface was *defined*; blocking via CANNOT VERIFY was the review's own offered alternative and is the recorded disposition. Defining a Linux desktop contract (if wanted) is the owner's call at the sitting |

**Verification of correction 10, since the coordinator asked for the
reconciliation — count settled at round 2.** The reviewer's core claim is
**confirmed**: `project-trajectory/PROCESS_OPTIONS.md` carries the literal
`gate_policy` token on **10 distinct lines** (11 occurrences; line 27 twice),
including operative instructions ("a reviewed commit that edits
`[attestation] gate_policy` in `docs/process.toml`"). Two further sites
(lines 364, 371) carry the hyphenated `--gate-policy` flag and
`docs/gate-policy.md`; the flag is a live, sanctioned interface that
"still takes the WORD but translates it" (repo-lock §5), so those two are
not enum residue — revision 2's "12 sites" conflated them in. The anti-drift pin does **not**
reach it: `tests/test_rule_sync.py::test_the_retired_enum_key_is_no_longer_shipped`
reads exactly one file —

```python
text = (KIT / "process.toml.template").read_text(encoding="utf-8")
```

— so it pins the **template** and is silent on the prose doc that tells an
adopter how to use it. The pin is doing what it says; its scope is just narrower
than its name suggests. **This ships downstream and reads as operative process.**

**What the review's method surfaced that neither pass had found — SR-126
(§E.4).** Chasing correction 4 through the registry turned up
**SR-126 (`Verified`): *"trace.py shall fail under --strict when any spine row's
normative text cites a work item or a process doc… **a script name, artifact
path, rubric or sibling spine id does not**."*** The kit has **already ruled that
script names in spine normative text are permitted**. §8.3 item 1, read as a
mechanical rule, contradicts a live Verified requirement. That is a genuine
conflict for the sitting and it is now §E.4.

**Carrier note.** Quoted "current text" is from the committed registries at
`HEAD` (`git show HEAD:docs/requirements/system-requirements.csv`,
`git show HEAD:docs/requirements/stakeholder-needs.md`), verified identical to
the staged TOML cell-for-cell on every row quoted. The cutover is **staged and
uncommitted**; `HEAD` still carries CSV.

---

## A · Principles applied

Five rules, derived from §8.3 item 1 and the
[PROJECT-VISION](../../../README.md#vision).

1. **The stakeholder is the grammatical subject.** A need says what a *person*
   can do, not what the kit *is*. Today 9 of 18 core needs open with "The kit…",
   "The process…", "Documentation…" or "Every policy dial…" — the product as
   subject.
2. **No implementation reference inside the Need text.** No script name, file
   path, CLI flag, environment variable or module. **⚠ This rule is in direct
   conflict with SR-126 as ruled — see §E.4. It cannot be adopted as written
   without amending SR-126.**
3. **One need = one genuine stakeholder desire.** The sitting's demotion test,
   applied at authoring time — with the caveat §C now carries: it is a
   **precedent, not a semantic proof**.
4. **Acceptance intent stays measurable, and never weakens.** Revision 1 broke
   this rule in 12 rows. The reviewer caught all 12. Every one is restored
   verbatim below; **none is defended**.
5. **Right-sized prose.** Need cells run 16–34 words today (SN-029 excepted at
   59). The legibility failure is concentrated in the **acceptance-intent
   cells** — 148 words (SN-029), 109 (SN-028), 78 (SN-027), 72 (SN-026).

### The challenge-2 tension

§8.3 challenge 2 is correct: *"no implementation references" conflicts with
today's acceptance-intent cells.* The cited names are what make the acceptance
*checkable*. So each affected row is presented in two forms:

- **(i) Minimal legibility rewrite** — subject, voice and structure fixed; the
  mechanical citation **stays**. Cheap, safe, blessable row-by-row.
- **(ii) Full plain-language form** — the citation moves to a named SR.
  **Only available where the obligation-coverage matrix in §B.0 passes.**

**Revision-2 change:** revision 1 asserted that "form (ii) is never a net
deletion." The reviewer disproved that on five rows. It is now a *tested claim*,
not an assertion — §B.0 tests it: two re-homings (SN-005, SN-007) **fail** and
are blocked, and SN-011's form (ii) is blocked on separate grounds — its
coverage rows pass, but the proposed text invented a stricter obligation than
either the need or SR-034 states, so it is withdrawn rather than matrix-failed.

---

## B.0 · Obligation-coverage matrix for form (ii)

Every clause form (ii) removes from an SN, and the row that must already carry
it. **A re-homing is only approvable where the verdict is PASS.**

| SN | clause removed by form (ii) | proposed receiving row | verified? | verdict |
|---|---|---|---|---|
| SN-001 | `bootstrap.py --dest` produces a green scaffold | **SR-010** — *"bootstrap.py shall produce a scaffold whose harness runs green immediately after generation"* | yes | **PASS** |
| SN-001 | re-sync never clobbers the repo's own files | **SR-011** (*"skip an existing file on a re-run unless --force"*) + **SR-036** (*"without clobbering the adopter's filled-in files"*) | yes | **PASS** |
| SN-002 | `trace.py --strict` zero orphans | **SR-001** | yes | **PASS** |
| SN-002 | malformed/duplicate id fails | **SR-002** | yes | **PASS** |
| SN-003 | toolchain declared once in `docs/stack.ini` | **SR-007** — *"so a stack swap edits only that file"* | yes | **PASS** |
| SN-003 | non-Python profile omits Python-only artifacts | **SR-009** (*Conditional scaffold profiles*) | yes | **PASS** |
| SN-004 | `check.py --gate GN`; missing tool fails | **SR-006** | yes | **PASS** |
| **SN-005** | enforcement floor is git hooks | SR-019 + SR-020 | yes | PASS |
| **SN-005** | **enforcement floor is CI running the *same* harness** | **none found** | **no** | **🚫 FAIL — BLOCKED** |
| SN-006 | resumes from `docs/status.md`; typed code at each end state; preflight refuses a broken footing | **SR-026** + **SR-028** + **SR-027** | yes | **PASS** |
| **SN-007** | **a change to a script is covered by a test** | SR-010 requires a green scaffold and that *the meta-suite runs every script*; it does **not** require per-change coverage | **no** | **🚫 FAIL — BLOCKED** |
| SN-008 | missing tool fails; `--lenient` is the one sanctioned degrade | **SR-006** | yes | **PASS** |
| SN-008 | no-stub detector at its gate | **SR-016** | yes | **PASS** |
| SN-008 | privacy/secrets floor at its gate | **SR-017** | yes | **PASS** |
| SN-009 | always-on secrets floor over diff/message/outgoing range | **SR-017** | yes | **PASS** |
| SN-009 | PII classes when the dial is on; author exemptions | **SR-018** | yes | **PASS** |
| SN-010 | broken link / missing vision tag fails | **SR-012** | yes | **PASS** |
| SN-010 | **every generated artifact carries a `--check` freshness contract** | ~~SR-041~~ (references only — **reviewer correct**). Corrected set: **SR-012** (`--stale`) + **SR-023** (arch map `--check`) + **SR-042** (OKF `--check`) + **SR-122** (dashboard freshness) | partial | **⚠ CONDITIONAL** — the four named artifacts are covered; "*every* generated artifact" is a universal no single row asserts |
| SN-011 | ledger row names what it replaces / why / the ruling; undeclared import fails | **SR-034** | yes | **PASS** |
| SN-011 | CI matrix green on three platforms | **SR-114** | yes | **PASS** |
| SN-023 | ~~SR-044~~ — **superseded stub; reviewer correct.** Corrected: **SR-073…SR-078** (dashboard cluster) + **SR-122** | yes | **PASS** (target fixed) |
| SN-024 | rubric-adjudicated critique, fresh cross-family session, bounded rework, escalation | **SR-086** + **SR-084** + **SR-085** | yes | **PASS** |
| SN-025 | derive next work from the WI DAG, not prose; deterministic order; generated status | **SR-059** + **SR-057** | yes | **PASS** |
| SN-026 | pair-row registry + consent surface; cross-family preference; documented degrade; logged selection | **SR-079** + **SR-080** | yes | **PASS** |
| SN-027 | worker ceiling, serial integrator, `--jobs 1`, pause drain, crash recovery | **SR-057** + **SR-132** + **SR-131** | yes | **PASS** |
| SN-028 | one policy home + checked shape + refusal | **SR-137** | yes | **PASS** |
| SN-028 | migration converts and deletes legacy files | **SR-138** | yes | **PASS** |

**Three findings fall out of this matrix that are not prose problems at all:**

1. **SN-005's CI obligation is undecomposed.** The need says the enforcement
   floor is *"git + CI running the same harness a human runs"*. SR-019 and
   SR-020 cover the hooks. **No SR requires CI to run the same harness.**
   SR-114's acceptance names a CI matrix, but for *OS portability*, not as the
   enforcement floor. A `Verified` need is half-covered.

   > **Measured 2026-08-11, on the owner's question of whether this is
   > mechanically verifiable at all — the obligation is TRUE and shipped
   > today, and the cheap half is checkable.** The kit's reference CI
   > `project-trajectory/ci/check.yml` runs `scripts/check.py`, and says why
   > in its own header: *"It runs the SAME harness you run locally … so a
   > green CI means exactly what a green local run means — no second,
   > drifting definition of 'passing'."* `bootstrap.py`'s MAPPING copies it
   > to `.github/workflows/check.yml`, and **this repo dogfoods it** —
   > `.github/workflows/test.yml` runs `python
   > project-trajectory/scripts/check.py --jobs 0` as "Run the kit's own gate
   > (docs/gate)", alongside the full suite and the smoke-budget enforcement.
   > So CI already does more than the smoke tier.
   >
   > **What is cheaply checkable** is the property that actually carries the
   > need: *one definition of passing*. A test asserting the shipped
   > `ci/check.yml` invokes `check.py` — a stdlib string search, no YAML
   > parser (F-6's rule) — pins it at the artifact the kit controls, and the
   > same one line dogfoods this repo's own workflow. **Nothing pins it
   > today, measured:** the existing tests pin the workflow's *triggers* and
   > *shape* — `test_push_policy` asserts `ci/check.yml` carries the
   > `"llm/**"` pattern, `test_bootstrap` asserts the file is copied, that
   > actions are pinned, and that at least three jobs exist ("expected at
   > least test/smoke-budget/gate") — but **no assertion reads a `run:`
   > line**. The gate job could be renamed or gutted to run something else
   > and every test stays green. That is a one-line gap, and closing it is
   > what would make SN-005's CI clause enforced rather than merely true.
   >
   > **What is NOT worth mechanizing**, and should be said in the row rather
   > than attempted: proving CI and local agree on *all* inputs (an
   > equivalence claim you can only settle by running both), and anything
   > about an **adopter's** copy — their file after copy-in, the same D-7
   > doctrine that governs a removed check. **Recommendation: reform, don't
   > delete.** Narrow the acceptance to the single-entry-point property the
   > kit can hold, mint the small SR + TC under it, and let the adopter half
   > stay advisory.
2. **SN-007's per-change coverage obligation is undecomposed.** *"a change to a
   script is covered by a test exercised end-to-end"* has no SR requiring
   per-change coverage.

   > **OWNER RULED, 2026-08-11: strike the clause.** *"I'm fine with removing
   > the prose … which doesn't have coverage today. That's not really
   > sustainable anyways."* So the fix is a **deletion, not a new SR** — the
   > need stops claiming per-change coverage. Note what this makes true, which
   > is the argument for it: **SN-007's own acceptance cell already states the
   > sustainable version** (*"The suite bootstraps a temp scaffold and runs
   > every script; `pytest -q` green is required before each change lands"*) —
   > a gate on the *suite* at each change, never a per-change coverage proof.
   > The Need cell was over-claiming against its own acceptance, so striking
   > the clause makes the row self-consistent rather than weakening it. Lands
   > with the prose batch at the sitting (a lone edit to a ratified need would
   > open a re-attest window outside the batched one — §F).
3. **SN-010's "every generated artifact" is a universal with four instances.**
   Either an SR should assert the universal, or the need should name the class
   it actually covers.

   > **CENSUSED 2026-08-11 on the owner's question — "what other generated
   > artifacts are also in git?" — and the answer changes the finding. There
   > are TEN, not four, and the universal is FALSE by exactly two.**
   >
   > | committed generated artifact | freshness check | where it runs |
   > |---|---|---|
   > | `docs/architecture.md` | `gen_arch_map --check` | pre-commit + `check.py` {G3} |
   > | `docs/okf/` (~470 files) | `gen_okf --check` | pre-commit + {G3} |
   > | `PROJECT_STATE.html` | `gen_trajectory --check` | pre-commit + {G3} |
   > | `docs/status.md` (generated block) | `gen_trajectory --status --check` | pre-commit + {G3} |
   > | `docs/gate` | `derive_gate --check` | pre-commit + **{G1,G2,G3}** |
   > | `docs/open-items.html` | `gen_open_items --check` | pre-commit + {G3} |
   > | `docs/ratify/*.md` | `trace --ratify modified --check` | pre-commit + {G2,G3} |
   > | `docs/id-watermark` | no flag — folded into `trace.py`'s default analyze path | every `trace.py` run (so checked *more* often, not less) |
   > | `.claude/`+`.agents/` skill copies | `gen_skills_index --check-agents` | pre-commit + {G3} |
   > | **`project-trajectory/prompts/CATALOG.md`** | `--check` EXISTS and works | **NOWHERE** 🚫 |
   > | **`project-trajectory/skills/INDEX.csv`** | `--check` EXISTS and works | **NOWHERE** 🚫 (only the *different* `--check-agents` mode is wired) |
   >
   > Both gaps are **declared** `[generated]` in `docs/stack.ini` (lines 318,
   > 319) and both have a working, passing `--check` — they are simply not
   > invoked by `check.py`, the pre-commit hook, or either CI workflow. So
   > this is not a prose problem at all: **the need is right and the harness
   > is two lines short of honouring it.** Filed and executed as its own WI
   > rather than reworded — narrowing SN-010 to match a weaker reality would
   > have deleted a true obligation to protect a wiring omission, which is
   > backwards.
   >
   > Two entries are legitimately special and stay as they are:
   > `docs/gate` (already the strictest, checked at every gate) and
   > `tests/test_module_size_ratchet.py` (declared generated but hand-stamped
   > measurement data by design — its own comment says so). Not committed and
   > therefore out of scope: `docs/test/report.md` (gitignored, rewritten on
   > every `trace.py` run, never a source of truth read from history) and
   > `docs/release-checklist.md` (absent here; and it is the one generator
   > with **no `--check` mode at all**, worth knowing before anyone commits
   > one).

**These three should go to the sitting as decomposition findings regardless of
whether any prose is rewritten.** They were found by the reviewer's coverage
challenge, and they are worth more than the prose pass that surfaced them.

---

## B · Per-SN rewrite table

**Counts (revision 2).**

| tier | rows | form (i) PRESERVING | form (i) CHANGING | form (ii) blocked |
|---|---|---|---|---|
| Core needs | 18 | **18** | 0 | 3 (SN-005, SN-007, SN-011) |
| Edge-case expectations | 10 | **10** | 0 | 0 |
| Draft needs | 1 | 1 | 0 | 0 |
| **Total** | **29** | **29** | **0** | **3** |

> **What changed from revision 1.** Revision 1 claimed 26 preserving / 3
> changing. The reviewer showed 12 of the "preserving" rows had dropped a
> qualifier — so the real revision-1 figure was **17 preserving / 12
> changing**, and the document was mis-stating its own risk by a factor of
> four. Revision 2 restores every dropped qualifier verbatim instead of
> reclassifying, which is why form (i) is now genuinely 29/29. **Form (ii) is
> where the risk actually lives**, and §B.0 now prices it.

Format: **NOW** (verbatim) → **PROPOSED** → **RESTORED** (what revision 1 dropped
and revision 2 puts back).

### Core needs

**SN-001** · form (i) PRESERVING

- **NOW:** "A team can drop the kit into a new or existing repo and get a working
  gated, requirement-traced process without hand-building the tooling."
- **PROPOSED:** "An adopting team can add this process to a new or existing
  repository and get a working gated, requirement-traced process, without
  hand-building the tooling."
- **RESTORED:** revision 1 added *"the same day"* — an invented time bound with
  no clause behind it. **Deleted.** The rewrite is now a subject change only.

**SN-002** · form (i) PRESERVING

- **NOW:** "The trace from need → requirement → design → test is **mechanically
  verified**, not manually asserted: every requirement links to a need and a test
  before a gate."
- **PROPOSED:** "A reviewer can trust the chain from need to requirement to
  design to test because it is **mechanically verified**, not manually asserted:
  every requirement links to a need and a test before a gate."
- Reviewer sampled this row and found no dropped obligation.

**SN-003** · form (i) PRESERVING

- **NOW:** "The kit is **stack-agnostic** — a non-Python project uses it by
  re-pointing the harness at that stack's tools, with Python only as the
  reference."
- **PROPOSED:** "A team in any language can use this process: it is
  **stack-agnostic**, and a non-Python project adopts it by re-pointing the
  harness at that stack's tools, with Python only as the reference."
- Reviewer sampled this row and found no dropped obligation.

**SN-004** · form (i) PRESERVING

- **NOW:** "Progress advances only through **explicit approval gates**
  (G1→G2→G3→…), and a gate passes only when its mechanical bar is met."
- **PROPOSED:** "A team advances only through **explicit approval gates**
  (G1→G2→G3→…), and a gate passes only when its mechanical bar is met."
- **RESTORED:** revision 1 wrote *"The repo owner decides when work advances"*,
  which **assigns the approver role to the owner** — an authority claim the
  current need does not make. **Deleted**; the predicate is now verbatim.

**SN-005** · form (i) PRESERVING · **form (ii) 🚫 BLOCKED**

- **NOW:** "AI agents and humans work from the **same playbook**, with the
  process enforced **agent-neutrally** (git hooks + CI), not by trusting any one
  agent."
- **(i) PROPOSED:** "AI agents and humans work from the **same playbook**, and
  the process is enforced **agent-neutrally** — by git hooks + CI — not by
  trusting whichever agent showed up."
- **(ii) BLOCKED.** §B.0: SR-019 and SR-020 carry the *hooks*; **no SR carries
  the CI half.** Form (ii) would delete an obligation with nowhere to land.
  Not offered. **Mint the missing SR first, or keep form (i) permanently.**

**SN-006** · form (i) PRESERVING

- **NOW:** "An agent can run **unattended** and resume from repo text alone; such
  a run never blocks on a prompt and fails clearly."
- **PROPOSED:** "An agent can run **unattended** and resume from repo text
  alone; such a run never blocks on a prompt and fails clearly."
  *(Need cell already satisfies the style bar — no change proposed.)*
- **Acceptance (ii):** "The run resumes from the tracked status surface, exits a
  **typed code** at each end state, and refuses a broken footing — no agent CLI,
  not a git repo, a private author under privacy-check — rather than hanging."
- **RESTORED:** revision 1 softened *"typed code"* to "a **named** outcome" and
  *"repo text alone"* to "repository-written state". **A name is not a typed
  exit code.** Both restored verbatim.

**SN-007** · form (i) PRESERVING · **form (ii) 🚫 BLOCKED**

- **NOW:** "The kit's **own** changes stay traceable and tested — a change to a
  script is covered by a test exercised end-to-end against a real scaffold."
- **(i) PROPOSED:** "The people maintaining this kit hold it to its own
  standard: its **own** changes stay traceable and tested — a change to a script
  is covered by a test exercised end-to-end against a real scaffold."
- **(ii) BLOCKED.** §B.0: SR-010 requires a green scaffold and that the suite
  runs every script; **nothing requires per-change coverage.** Not offered.

**SN-008** · form (i) PRESERVING · structural flag

- **NOW:** "Gates are **honest** — a green never hides a skipped check, a stub,
  or an unmet criterion."
- **PROPOSED:** "A reader can believe a green: gates are **honest**, and a green
  never hides a skipped check, a stub, or an unmet criterion."
- **Structural flag (unchanged from revision 1):** the acceptance cell cites
  **SR-006** — a need citing its own child. Recommend deleting the token in
  either form; the join already carries the link.

**SN-009** · form (i) PRESERVING

- **NOW:** "A committed **secret or private identity** is caught before it
  publishes, in **every** repo, without extra setup."
- **PROPOSED:** "A team is protected from publishing a **secret or private
  identity**: it is caught before it publishes, in **every** repo, without extra
  setup."

**SN-010** · form (i) PRESERVING · form (ii) ⚠ CONDITIONAL

- **NOW:** "Documentation stays **navigable and honest** — links resolve, the
  vision is declared once, and generated views cannot silently rot."
- **PROPOSED:** "A reader can navigate the documentation and trust it:
  **navigable and honest** — links resolve, the vision is declared once, and
  generated views cannot silently rot."
- **Form (ii) conditional** per §B.0: the *"every generated artifact"* universal
  is asserted by no single SR. Either restrict the need's wording to the covered
  class, or mint the universal — **an owner call, not a prose call.**

**SN-011** · form (i) PRESERVING · **form (ii) 🚫 BLOCKED**

- **NOW (Need):** "The kit's scripts run on a **clean Python 3.11+ with minimal,
  argued dependencies** — stdlib by default, a non-stdlib dependency admitted
  only through a reviewed ledger row — on Windows and POSIX (and macOS)."
- **(i) PROPOSED:** "An adopting team can run every check on a **clean Python
  3.11+ with minimal, argued dependencies** — stdlib by default, a non-stdlib
  dependency admitted only through a reviewed ledger row — on Windows and POSIX
  (and macOS)."
- **(ii) BLOCKED.** Revision 1's form (ii) said adopter checks *"stay
  dependency-free"*. **The reviewer is right that this is stricter than both the
  current need and SR-034**, which permit ledger-declared dependencies and set
  the shipped tier at stdlib-**preferred**, not stdlib-only. A legibility pass
  that *tightens* an obligation is the same defect as one that loosens it.
  **Withdrawn.**

**SN-012** · form (i) PRESERVING

- **NOW:** "The process is **right-sized**, not ceremony for its own sake —
  small changes stay cheap, and heavy layers are opt-in."
- **PROPOSED:** "A team can keep small changes small: the process is
  **right-sized**, not ceremony for its own sake — small changes stay cheap, and
  heavy layers are opt-in."

**SN-023** · form (i) PRESERVING · receiving target corrected

- **NOW:** "A reviewer can see the project's progress **and how its parts
  connect** from one dashboard-like file."
- **PROPOSED:** unchanged — the Need cell already satisfies the style bar.
- **Correction:** revision 1 named **SR-044** as a form-(ii) receiving row.
  **SR-044 is a superseded stub** whose own text commands active references to
  cite SR-073…SR-078. **The reviewer is right: a superseded row cannot receive a
  live obligation.** Corrected to **SR-073…SR-078 + SR-122**.

**SN-024** · form (i) PRESERVING

- **NOW:** "Subjective/perceptual acceptance — a realistic-looking render, an
  artifact comparison with no crisp measurable interface — is adjudicated by an
  **independent critical eye against a written rubric**, never by the session
  that authored the artifact."
- **PROPOSED:** "A reviewer can trust subjective/perceptual acceptance — a
  realistic-looking render, an artifact comparison with no crisp measurable
  interface — because it is adjudicated by an **independent critical eye against
  a written rubric**, never by the session that authored the artifact."
- **RESTORED (three separate drops):** revision 1 broadened the scoped cases to
  every *"judgement call"*; weakened *"independent critical eye"* / *"never by
  the session that authored the artifact"* to "someone other than the author";
  and **added** a new requirement that the rubric be written *"in advance"*.
  All three reverted; the scope clause and both qualifiers are verbatim.

**SN-025** · form (i) PRESERVING · form (ii) not recommended

- **NOW:** "A **single command from the repo root** (`agent-resume`) lets a
  configured LLM agent implement toward the vision — fully autonomously where
  enabled — with no human curating what comes next."
- **(i) PROPOSED:** unchanged — already end-user-facing and within the word bar.
- **(ii)** would drop `agent-resume`. **Not recommended**, and the reason is now
  a recommendation the sitting can rule once: **launcher names are end-user
  interface vocabulary, not implementation** — which is exactly what §8.3 item 1
  asks needs to be written *around*, and what items 2–4 ask for *more* of.
  Ruling this once resolves §D items 2, 3 and 4 at the same time.

**SN-026** · form (i) PRESERVING

- **NOW:** "**Several LLM families are configurable** — selected per job and per
  capability level — and work that benefits from an independent second opinion is
  automatically routed to a *different* family wherever that is configured."
- **PROPOSED:** "The repo owner can configure **several LLM families** —
  selected per job and per capability level — so that work benefiting from an
  independent second opinion is automatically routed to a *different* family
  wherever that is configured."
- **RESTORED:** revision 1 dropped *"per capability level"* and *"wherever that
  is configured"*. The second is load-bearing — it is the clause that makes the
  routing conditional on configuration rather than unconditional. Both restored.

**SN-027** · form (i) PRESERVING

- **NOW:** "Ready work **fans out across bounded parallel lanes**, while mutation
  of the integration branch stays **serialized and gated**."
- **PROPOSED:** "A team gets more than one piece of ready work moving at once:
  ready work **fans out across bounded parallel lanes**, while mutation of the
  integration branch stays **serialized and gated**."
- **RESTORED:** revision 1 dropped **bounded**, **parallel lanes**, and
  **serialized and gated** — the three constraints that are the entire content
  of the need. All restored verbatim.
- **Separate recommendation (unchanged):** the acceptance cell's trailing
  *"Spec of record: `docs/archive/specs/…` + `docs/concurrency-restructure.md`"*
  is design provenance in an acceptance cell; move to **SR-132**'s rationale.

**SN-028** · form (i) PRESERVING · **rewritten from scratch after correction 2**

- **NOW (Need):** "**Every policy dial has one home** — a single hand-edited,
  machine-read file — and a repo that declares the same dial twice is REFUSED
  rather than resolved by precedence."
- **(i) PROPOSED (Need):** "The repo owner can find and change every policy dial
  in **one home** — a **single hand-edited, machine-read file** — and a repo that
  declares the same dial twice is REFUSED rather than resolved by precedence."
- **RESTORED:** revision 1 reduced *"a single hand-edited, machine-read file"* to
  *"one place"*, dropping all three qualifiers. **Restored verbatim.**
- **(i) PROPOSED (acceptance, 109 → 92 words, every named interface kept):**
  > "`docs/process.toml` holds every process dial under **bare `[section]`
  > headers**, one `key = value` per line. The SHAPE is checked rather than
  > conventional, because two grammars read the file (`tomllib` and the hooks'
  > sh) and every shape only one of them understands is a silent flip of a
  > security gate; the two readings are pinned equal over a table of adversarial
  > files. A legacy one-word file still present alongside its key is a REFUSAL
  > naming both, and `bootstrap.py --migrate-config` — run by bootstrap and by
  > the documented re-sync — converts and deletes the legacy files so an adopter
  > never meets that refusal un-aided. A wrong-typed or out-of-range dial is
  > refused, never defaulted."
- **What changed:** sentence boundaries only. `docs/process.toml`, `bare
  [section]`, `tomllib`, the hooks' sh, the adversarial-file pinning,
  `bootstrap.py --migrate-config`, and the refusal semantics are all **verbatim**.
  Revision 1 generalised every one of them and then claimed form (ii) would
  remove names form (i) had already removed — **the reviewer caught the
  inconsistency and it is fixed.**
- **(ii)** would move the named interfaces to **SR-137 + SR-138** (§B.0: both
  PASS).

### Draft needs

**SN-029** · PRESERVING · **Draft — free to edit at zero cost**

- **PROPOSED (Need, 54 w):** "**An autonomous run gets as far as it honestly
  can.** Once triggered, the coordinator stops for a human judgement only when
  the declared ratification level reserves that tier for a human, when a round
  cannot converge on its own, or when requirement/test documentation is
  introduced or amended such that the gate drops below what automation is
  permitted to attest."
- This is the **current text with no change** except paragraph placement. On
  reflection the row does not need a rewrite: the owner reframed it on
  2026-08-10, and its three corrections ("a human judgement"; "a round that
  cannot converge"; "introduced **or amended**") are precisely the qualifiers a
  legibility pass would erode. **Recommend: leave the Need cell alone.**
- **Acceptance (148 w):** split into four numbered clauses **with no wording
  change**, mapping to **SR-139** (ordinal, stage, fail-direction) and
  **SR-140** (on-row anchor, amendment detection).

### Edge-case expectations

All ten are form (i) PRESERVING **after restoration**. Four rows had dropped
qualifiers in revision 1; all four are restored verbatim.

| SN | proposed `Expected` (form (i)) | revision-1 drop, restored |
|---|---|---|
| SN-013 | "The git hooks / coordinator **probe by running** a candidate and **skip-or-report clearly**; they never crash cryptically." | ✅ *"skip-or-report"* — revision 1 made reporting unconditional, **changing the allowed outcome** |
| SN-014 | "`check.py` reports **`SKIP(missing)`** and **fails the gate** — a missing tool is never a silent pass." | ✅ the measurable **`SKIP(missing)`** token |
| SN-015 | "The coordinator preflight reports 'not a git repo' and exits nonzero; it never hangs." | — |
| SN-016 | "`agent_loop.py` runs headless (**stdin closed**); a rate limit backs off, a stall aborts to protect the budget — the loop is never wedged by a prompt." | ✅ **stdin closed**, the headless *mechanism* |
| SN-017 | "The per-worktree lock is a kernel advisory lock the OS releases on death, so the next run is **not wedged** (no stale-pid file)." | — |
| SN-018 | "A second coordinator is **refused** rather than risking a two-writer race." | — |
| SN-019 | "The coordinator's rev-parse guard does not crash the loop." | — |
| SN-020 | "The session is logged **`ERROR`** and an **all-`ERROR`** stall is reported as an **unavailable agent**, not a work stall." | ✅ both the *logged `ERROR`* and the **all-`ERROR`** qualifier |
| SN-021 | "Its `--check` fails at the gate — a stale generated doc is a red, not a silent rot." | — |
| SN-022 | "`--no-placeholders` flags a leftover **`-000`** row from G2 on; a fresh scaffold stays green until it claims a gate." | ✅ the **`-000`** class token and **"from G2 on"** |

**Form (ii) for this tier** deletes the four `tests/test_agent_loop.py::test_…`
citations (SN-017, SN-018, SN-019, SN-020). Those are already the `Evidence`
selectors of the corresponding TCs, so the re-homing **PASSES** §B.0 — but note
the tier-level recommendation: **rule §C first**, since seven of these rows are
demotion candidates and rewriting a demoted row is wasted work.

---

## C · Edge-case tier — mis-levelling analysis

**Independently confirmed by the reviewer**, who re-ran the joins: exactly-one
rows are SN-013→SR-021, SN-014→SR-006, SN-015→SR-027, SN-018→SR-030,
SN-019→SR-028, SN-020→SR-028, SN-022→SR-003 — **7 of 10, not 8**; SN-016=12,
SN-017=5, SN-021=15; edge mean 3.9, core mean 12.56. **SN-019 and SN-020 do
share the same sole child, SR-028.**

> **⚠ Caveat added at the reviewer's suggestion, and it matters.** *"One SR means
> demote"* is a **sitting precedent, not a semantic proof.** A need can be
> genuinely stakeholder-level and thinly decomposed — because the decomposition
> is immature, not because the need is mis-levelled. The fan-out count is
> **evidence that should prompt the question**, not an answer to it. Each row
> below is recommended on the *content* argument, with the count as support.

| edge SN | SRs | recommendation | re-parent to | content argument |
|---|---|---|---|---|
| **SN-013** | 1 (SR-021) | **DEMOTE** | SN-011 | states a mechanism (probe by running), not a want |
| **SN-014** | 1 (SR-006) | **DEMOTE + MERGE** | SN-008 | its own text ends "(SN-008)", conceding it restates *gates are honest* |
| **SN-015** | 1 (SR-027) | **DEMOTE** | SN-006 | a precondition of SN-006's "fails clearly", not a separate want |
| **SN-016** | 12 | **KEEP; consider promoting to core** | — | 4 unique SRs; decomposes like a core need |
| **SN-017** | 5 | **KEEP** | — | above the line, 1 unique SR; a genuine failure-mode want |
| **SN-018** | 1 (SR-030) | **DEMOTE** | SN-006 | SR-030 already cites SN-006 |
| **SN-019** | 1 (SR-028) | **DEMOTE + MERGE with SN-020** | SN-006 | — |
| **SN-020** | 1 (SR-028, *same row*) | **DEMOTE + MERGE with SN-019** | SN-006 | two "needs", one requirement |
| **SN-021** | 15 | **MERGE into SN-010** | SN-010 | SN-010's acceptance already promises the freshness contract; 13 of 15 SRs cite both |
| **SN-022** | 1 (SR-003) | **DEMOTE** | SN-002 | SR-003 already cites SN-002 |

**Net if ruled as recommended:** 29 live SNs → 21. Ids **never re-minted** (D-4).

**Kit-level consequence:** this table ships to every adopter. **Recommended
shape:** keep the lifecycle framing (Provision / Startup / Runtime) in the
template as an **authoring checklist for SRs**, not as a second table of needs —
preserving what the tier taught while removing the level error.

---

## D · The six §8.3 intake items

Each drafted with the D-7 evidence test applied at birth (§8.3 challenge 7).

### ⚠ OWNER-RESOLUTION-REQUIRED — two textual artifacts

1. **The agent-resume item repeats dev-setup's "install all dependencies"
   text.** `repo-lock` records it as *"likely copy-paste"*. Item 3 is drafted
   **without** the clause, and the omission is flagged: **does the owner want
   agent-resume to also perform setup, or is the clause an artifact?** Not
   guessed.
2. **One item ends in an unfinished `"(Note this )"`.** The record does not say
   which item. **The owner must supply the completion.** Not reconstructed.

### Launcher facts (correcting §8.3 challenge 3) — reviewer-confirmed

| fact | evidence |
|---|---|
| Double-clickable dev-setup launchers **exist and ship** | `project-trajectory/scripts/dev-setup.template.{sh,ps1,command,cmd}`; the Windows `.cmd` rung was built as **WI-166 under SR-032** |
| They **scaffold**, and this repo **self-applies them** | `bootstrap.py` maps all four to `scripts/dev-setup.*`; those files exist here today |
| The real gap is **placement** | they land in `scripts/`, not at the root beside `agent-resume.*` |
| `agent-resume.{cmd,sh,command}` | at this repo's root, self-applied — item 3 mostly **ratifies existing capability** |
| `run.{cmd,sh,command}` | ship and are **Verified as SR-046**; deliberately **un-self-applied here**. Item 4 **reverses** that stance |

> **⚠ CANNOT VERIFY — the Linux double-click surface.** Revision 1 asserted a
> Linux "double-click" gap. **No desktop-environment contract in this repo
> establishes that an executable `.sh` is double-clickable**, and behaviour
> differs across GNOME/KDE/XFCE and by file-manager policy. Windows (`.cmd`) and
> macOS (`.command`) are verified double-click surfaces; **Linux is undefined and
> must be defined by the owner before it can appear in measurable text.** Items
> 2 and 3 below are scoped to Windows and macOS only.

**Item 1 — plain-language, end-user-perspective needs.** Drafted as: *"A reader
who has never seen this repository can understand what each stakeholder need
asks for on the first read, from the need's own words."* Failure prevented: a
need naming a tool goes false when the tool is renamed. 3 SRs sketched (no
implementation token in a Need cell; every need has ≥1 mechanically executable
child; a readability floor). **Level verdict: recommend folding into SN-010**
rather than minting an id — SN-010 already owns documentation honesty, and a new
SN would be the same want twice, the defect §C demotes eight rows for.
**⚠ BLOCKED ON §E.4 — this item contradicts SR-126 as ruled.**

**Item 2 — double-clickable `dev-setup` per platform.** Drafted as: *"A new
contributor on Windows or macOS can get a working development environment by
opening the repository and double-clicking one file."* **1 SR** ("the setup
launcher sits at the repository root for every supported platform"). **⚑
PROBABLY SR-TIER** per the demotion precedent — recommend amending **SR-032**
under SN-001, not a new need. Linux: **CANNOT VERIFY**, excluded.

**Item 3 — double-clickable `agent-resume` per platform.** Drafted as: *"The repo
owner can start an unattended agent session by double-clicking one file at the
top of the repository."* **1 SR**, and the capability already exists on both
verified surfaces. **⚑ PROBABLY SR-TIER**, under SN-025. **⚠ Blocked on owner
artifact 1** — if the install clause is meant, this is no longer one SR and no
longer SR-tier.

**Item 4 — `run` launcher menu.** The capability is **already Verified as
SR-046**. Item 4 adds no requirement; it makes a **self-application decision**.
**Level verdict: NOT AN SN — a dogfooding reversal**, for the log's Decisions
section plus a `[run]` declaration. Recommend recording the reason so the next
reader does not re-derive the old stance.

**Item 5 — decomposition prose carries the "hat" perspectives.** Drafted as: *"A
person asked to ratify a decomposition can see which role's judgement each part
of it needs, so no role's concern is silently skipped."* **2 SRs** (declared
roster home; brief injects it per tier). **BORDERLINE** — recommend folding
under SN-024 + SN-005. Machinery note (challenge 4): a WI, not a prose edit.

**Item 6 — component-boundary SRs.** **⚑ RULE WITH THE COMPONENTS MODEL (F-11).
Deliberately not drafted as adoptable text**, per §8.3 challenge 5: it reorders
the process spine and lands on the unruled partition that decides what "a
component-boundary interface" denotes. *(Reviewer confirmed this section complies
with the lock.)*

### The draft SR from §8.3 — ⚠ NOT ADOPTABLE UNTIL ONE RULING

- **Drafted (Draft status, intake only):** *"An unattended run shall consume
  outstanding handback documents **first** — minting a follow-up work item for
  each — and shall then advance the requirement spine tier by tier, halting at
  whichever tier the declared ratification level reserves for a human, before
  implementing the resulting work items autonomously."*
- **🚫 CONFLICT REQUIRING AN EXPLICIT OWNER RULING (reviewer correction 11,
  confirmed).** The owner's supplied text says **"SN (always human-attested)"**.
  The drafted text halts only where the *configurable* level reserves a tier —
  and this repo runs `human_ratification_through = 0`, under which **SN is not
  human-attested at all**. The two are incompatible. Revision 1 silently
  normalised the owner's words into the D-3 model. **That normalisation is
  withdrawn.** The owner must rule: *is SN attestation an absolute floor, or the
  bottom rung of a configurable ordinal?* The draft SR cannot be intaken either
  way until it is answered — and the answer also constrains SN-029 and SR-139.
- **Second conflict:** "handbacks first" collides with **SR-141** (*The loop's
  priority order is stated and pinned*, Draft), which gives `adjudication` rows
  top priority. Must be ruled together.

---

## E · SR-tier legibility pass, triaged

**The measurement.** On the `Requirement` cell: `score = words + 4 × clause_marks`
(`;`, `,`, `—`, ` - `). Clause marks are weighted because reader cost is per
*turn*, not per word. The 16 boilerplate `"SR-### is superseded by …"` stubs are
excluded as a class. Corpus: **mean 34 words, median 24**.

> **Revision-2 scope change (correction 3).** Revision 1 gave 26 rows as
> "lead + clauses" outlines with an unverifiable "zero words dropped" claim.
> **An outline is not a ratifiable proposal.** Revision 2 gives **exact
> replacement cells for 17 rows** with a word-delta ledger, and **drops 13 rows
> from the batch** rather than dressing an outline as a rewrite. The dropped
> rows are listed in §E.2 with the reason.

### E.1 · Exact replacement cells

Every proposal below is the **complete new `requirement` cell**. `Δ` states the
exact word delta. **No row claims preservation without the delta.**

> **The deltas are mechanically verified, not asserted.** Each was computed by
> token-multiset comparison of the current cell against the proposed cell
> (`collections.Counter` over whitespace tokens, then again over
> punctuation-stripped lowercase tokens to separate real word changes from
> punctuation and sentence-initial capitalisation). Three of revision 2's own
> first-draft claims were **wrong** and are corrected below — SR-046, SR-060 and
> SR-026 each claimed "zero word change" and only two of them were entitled to.
> This is the check the reviewer's correction 3 exists to force, and it caught
> me.

---

**SR-050** · Verified · score 201 / 145 w · **PRESERVING · Δ +4 / −0**

*CURRENT:* "gen_trajectory.py shall render a Process reference tab in
PROJECT_STATE.html beside the existing views, presenting how the project is built
as three linked panels: (1) artifact lifecycle x gates - Vision -> SN (G1) -> SR
(G1->G2) -> LLR + architecture (G2) -> TC (G2->G3) -> code+tests (G3), each stage
linked to its process-doc section and annotated with this repo live tier counts;
(2) the resume loop - the managed agent_loop flow (read status -> PLAN -> BUILD
-> REVIEW -> INTEGRATE -> commit -> hook/gate -> repeat) with its escalation
edges; (3) slices -> phase -> gates - a per-WI slice ends at the commit bar, a
phase closes at the gate bar, CI runs the same bar every push. Data-derived where
a canonical source exists (docs/gate, the spine registries, the WI registry
(docs/work/)); self-contained and byte-deterministic; a data-less repo renders
byte-identically; --check freshness unchanged."

*PROPOSED (exact):*
> gen_trajectory.py shall render a Process reference tab in PROJECT_STATE.html
> beside the existing views, presenting how the project is built as three linked
> panels:
> (1) artifact lifecycle x gates - Vision -> SN (G1) -> SR (G1->G2) -> LLR +
> architecture (G2) -> TC (G2->G3) -> code+tests (G3), each stage linked to its
> process-doc section and annotated with this repo live tier counts;
> (2) the resume loop - the managed agent_loop flow (read status -> PLAN -> BUILD
> -> REVIEW -> INTEGRATE -> commit -> hook/gate -> repeat) with its escalation
> edges;
> (3) slices -> phase -> gates - a per-WI slice ends at the commit bar, a phase
> closes at the gate bar, CI runs the same bar every push.
> The tab shall be data-derived where a canonical source exists (docs/gate, the
> spine registries, the WI registry (docs/work/)); self-contained and
> byte-deterministic; a data-less repo renders byte-identically; --check
> freshness unchanged.

*Δ:* **+4 words** — "The tab shall be", replacing the sentence-initial
"Data-derived" with "data-derived". **0 words removed.** Every other character
byte-identical; only line breaks inserted before `(1)`, `(2)`, `(3)` and the
final sentence. Free in TOML multi-line strings.

---

**SR-055** · Verified · score 165 / 117 w · **PRESERVING · Δ +0 / −0**

*PROPOSED (exact):*
> The Process tab shall additionally render the project's two circular working
> loops as linked flow panels:
> (A) the intake loop - owner/agent intake -> triage into work items with spec
> detail -> the scheduler-derived ready frontier in the WI registry (docs/work/)
> -> build/review -> merge; and
> (B) the human-decision loop - open-items population (including the
> gate-ratification table) -> human review and ruling -> the log's Decisions
> record -> merge
> - with the LLM_Agent entry point rendered once and shared by both loops;
> each stage links to its canonical home (status.md, the WI registry
> (docs/work/), open-items.html, log.md);
> the panels stay data-derived where a canonical source exists, self-contained,
> byte-deterministic; a data-less repo renders byte-identically and --check
> freshness is unchanged.

*Δ:* **0 words added, 0 removed** (verified — line breaks only; a true
zero-delta reformat, and the largest row in the corpus to achieve one).

---

**SR-046** · Verified · score 121 / 97 w · **PRESERVING · Δ +0 / −0**

*PROPOSED (exact):*
> The root run.cmd/run.sh/run.command launchers shall present every major
> capability an evaluator runs from a single declaration - one name = command line
> (plus an optional name.desc line) per capability in docs/stack.ini's [run]
> section - via a stdlib scripts/run_menu.py that reads it:
> no args gives a numbered interactive menu;
> run_menu.py <name> launches one directly with exit-code passthrough;
> and --list emits a stable name<TAB>desc machine listing (the agent surface).
> An absent or empty [run] section prints the no-launch-command-wired-yet guidance
> and exits 1.
> The launch command is declared once (the duplicated RUN_CMD is retired) and
> works on Windows and POSIX.

*Δ:* **0 words added, 0 removed** (verified). Three commas/semicolons became
sentence breaks, which changes six tokens' trailing punctuation and capitalises
two sentence openings — no lexical change. `stdlib` and `scripts/run_menu.py`
retained (the reviewer's SR-057 lesson applied pre-emptively).

---

**SR-132** · Modified · score 122 / 90 w · **PRESERVING · Δ +0 / −0**

*PROPOSED (exact):*
> The local integrator shall:
> (1) claim work via a serial trunk commit (queued spec to
> docs/work/active/<branch>/, branch cut from that commit, refused while
> docs/work/pause is present);
> (2) merge each finished claimed branch --no-ff onto a candidate worktree with
> the trunk step folded into the merge commit;
> (3) run the declared bar on the composed tree - refusing on a missing or empty
> check declaration and on any SKIP in the bar's own report;
> (4) require the policy-dialed verdict artifacts with git-derived freshness;
> (5) fast-forward the trunk only on green; and
> (6) stop loudly on red.

*Δ:* **0 words added, 0 removed** (verified — a true zero-delta reformat; six
numerals added as list markers). Already `Modified`, so it owes a re-blessing
regardless — the cheapest row in the batch.

---

**SR-060** · Modified · score 126 / 78 w · **PRESERVING · Δ +0 / −1**

*PROPOSED (exact):*
> The session engine shall run explicit per-worker claimed assignments (--wi, on
> the branch integrate.py claim cut; the session tag defaults to the branch name).
> A worker prompt is assembled from AGENTS.md, the WI row, its SpecRef,
> predecessor context, the current branch diff, and any rework finding (never
> docs/status.md or docs/next-wi).
> Worker branches never edit root status, other branches' claims, the root log,
> or generated artifacts.
> The result channel is committed trailer evidence (WI: / Blocked-WI: +
> BlockRef:).

*Δ:* **0 words added, 1 removed** (verified). The removed word is the
conjunction **"and"** joining the worker-branch prohibition to the result-channel
clause, which became a sentence break. No noun, verb, qualifier or named
artifact changed. If the sitting prefers a strict zero-delta, keep the `and` and
split at the comma instead.
**Note:** the `never docs/next-wi` clause names a file SR-059 deletes. It stays
meaningful as a prohibition, but the sitting may prefer to strike it once SR-059
lands. **Flagged, not changed.**

---

**SR-049** · Verified · score 111 / 87 w · **PRESERVING · Δ +2 / −0**

*PROPOSED (exact):*
> derive_gate.py shall compute the active gate from the spine artifact states (SN
> section-state + SR/LLR/TC Status maturity) and cache it to docs/gate rather than
> accept a hand-set value, so a gate advances only when the mechanical states do.
> Three Status values are recognized case-insensitively:
> (1) Draft (G0 + decomposition exemptions);
> (2) Verified (G3); and
> (3) Modified — a post-attestation amendment owing a re-attest, deriving G2
> through the existing decomposed-unverified rung with no arithmetic of its own.
> The cached basis line carries modified=N beside drafts=N so the pending state
> never hides.

*Δ:* **+2 words** ("and", "The") replacing two semicolons.

---

**SR-042** · Verified · score 105 / 81 w · **PRESERVING · Δ +2 / −0**

*PROPOSED (exact):*
> gen_okf.py shall export the spine registries AND the key process docs as a
> generated Open Knowledge Format bundle under docs/okf:
> one typed markdown concept per real row (graph as resolvable markdown links,
> per-tier indexes);
> plus a Process Guide concept per present process doc (a summary derived from
> that doc and a resource pointer to the unmodified source).
> The bundle shall be deterministic (no clocks), with --check failing on any
> stale, missing or extra bundle file; docs/okf-export off silences and
> placeholder-only registries are vacuous.

*Δ:* **+2 words** ("The bundle shall be" replacing "— deterministic"; net +2
after the em-dash pair is dropped).

---

**SR-057** · Modified · score 73 / 45 w · **PRESERVING · Δ +4 / −2**

*CURRENT:* "A stdlib schedule.py library/CLI shall derive the dependency-ready
frontier from the tracked WI registry plus the active claims - never from prose -
excluding blocked (queued + blockref), deferred, claimed, protected-conflicting
and exclusive-conflicting WIs, and exposing ready --explain, ready --format json
and simulate --jobs N."

*PROPOSED (exact):*
> A stdlib schedule.py library/CLI shall derive the dependency-ready frontier from
> the tracked WI registry plus the active claims - never from prose.
> It shall exclude blocked (queued + blockref), deferred, claimed,
> protected-conflicting and exclusive-conflicting WIs.
> It shall expose ready --explain, ready --format json and simulate --jobs N.

*Δ:* **+4 / −2** — "excluding"/"exposing" → "It shall exclude"/"It shall expose".
**`stdlib` and `library/CLI` retained** — the reviewer's specific catch on this
row; revision 1's outline had dropped both.

---

**SR-110** · Verified · score 63 / 51 w · **PRESERVING · Δ +3 / −0**

*PROPOSED (exact):*
> check_coverage.py shall fail when a module listed in the coverage-floor census
> is below its declared per-module line-coverage percentage in the pytest-cov JSON
> report, or is absent from that report — so the global --cov-fail-under floor
> cannot hide a thin high-risk module.
> An absent report skips, and an empty census is a no-op.

*Δ:* **+3 words** ("An", "and", "is"). The rationale clause *"so the global
--cov-fail-under floor cannot hide a thin high-risk module"* is **kept in the
requirement**, not moved — revision 1 proposed moving it to the rationale, which
would have been a cell-boundary change dressed as formatting.

---

**SR-130** · Modified · score 61 / 45 w · **PRESERVING · Δ +3 / −0**

*PROPOSED (exact):*
> A serial trunk step shall compile docs/log.d/ work-branch log fragments into
> docs/log.md in merge order derived from git history.
> It shall validate every fragment before any write, rebase relative links to the
> log's home, delete compiled fragments, fail loudly at the first error, and never
> commit.

*Δ:* **+3 words** ("It shall" + "and"), replacing the participial chain.

---

**SR-131** · Modified · score 58 / 42 w · **PRESERVING · Δ +2 / −0**

*PROPOSED (exact):*
> A tracked docs/work/pause file (TOML: reason, since) shall pause claiming —
> everything in flight finishes and integrates.
> It shall be read via pause_reason as the ONE pause home (the legacy untracked
> docs/pause half retired with the dispatcher at Phase 5), failing closed on
> malformation.

*Δ:* **+2 words** ("It shall"). The historical parenthetical is **kept in place**
— revision 1 proposed relocating it to the rationale; that is a cell-boundary
change requiring its own ruling, so it is now proposed separately in §E.5 rather
than smuggled into a formatting pass.

---

**SR-026** · Verified · score 81 / 61 w · **PRESERVING · Δ +0 / −0**

*PROPOSED (exact):*
> agent_loop.py shall resume headless with stdin closed, never blocking on a
> prompt.
> Resume authority (one path - the serial resume loop is retired): a worker
> resumes from its explicit claimed assignment plus the committed trailer evidence
> on its branch, and the integrator (SR-132) derives claim/queue state from trunk
> history alone.
> docs/status.md is a generated reference surface (SR-059), never a session input.

*Δ:* **0 words added, 0 removed** (verified). One semicolon became a sentence
break.

---

**SR-059** · Modified · score 69 / 57 w · **PRESERVING · Δ +1 / −0**

*PROPOSED (exact):*
> The migration shall delete docs/next-wi and docs/run-phase outright (fresh
> scaffold and migrated repo) and remove every live dependency on them.
> docs/status.md's derived snapshot is GENERATED (gen_trajectory --status) and
> freshness-gated, never hand-copied.
> (The generated docs/run-state surface this row once paired with retired with the
> dispatcher at Phase 5 - the stop banner and exit codes carry the outcome.)

*Δ:* **+1 word** ("The"). The trailing parenthetical is **ungrammatical as
written** ("this row once paired with retired with the dispatcher") and duplicates
SR-116. **Flagged for the owner, not silently repaired** — repairing it means
deciding what it meant, which is a ruling.

---

**SR-082** · Modified · score 56 / 48 w · **PRESERVING-CONDITIONAL · Δ +6 / −13**

*CURRENT:* "The coordinator shall apply fixed win-stay/lose-shift escalation and
page for shared failure, contradictions and tripwires per the declared
ratification level, keyed on whether the tier in process is still the human's to
ratify and on the separate drain dial the retired three-value enum bundled into
the same word."

*PROPOSED (exact):*
> The coordinator shall apply fixed win-stay/lose-shift escalation and page for
> shared failure, contradictions and tripwires per the declared ratification
> level, keyed on two separate dials: whether the tier in process is still the
> human's to ratify (human_ratification_through), and whether non-dependent work
> keeps running while a ratification is queued (keep_nondependent).

*Δ:* **+6 / −13.** The removed words are the periphrasis *"the separate drain
dial the retired three-value enum bundled into the same word"*; the added words
name what it denotes.
**CONDITIONAL on one owner confirmation:** that "the separate drain dial" is
`keep_nondependent`. Evidence: `docs/process.toml`'s own comment on that key —
*"This is an ORTHOGONAL policy an ordinal cannot express (it was the old
`single-ratify` level's distinguishing behaviour)"*. That is strong, but it is an
inference about intent, so it is marked conditional rather than asserted.

---

**SR-040** · Modified · **the one confirmed stale-text defect** · **CHANGING
(factual correction)**

*CURRENT (fragment):* "…surface the declared reviewer dial (docs/review-policy,
default 1) at run start without enforcing it;…"

*PROPOSED (exact, full cell):*
> The unattended coordinator shall select the agent command template per
> in-process session phase (PLAN/BUILD/REVIEW-A/REVIEW-B/DESIGN-CHECK/CRITIQUE -
> the coordinator's own activity; the retired docs/run-phase file, deleted by
> SR-059, is not an input) via AGENT_CMD_MAP/--cmd-map, falling back to the single
> AGENT_CMD.
> It shall surface the declared reviewer dial (docs/process.toml [policies]
> review_rounds, default 1; the legacy docs/review-policy is still read through
> the migration window) at run start without enforcing it.
> It shall warn (never block) when a lane resume surface exceeds the declared size
> threshold.

*Why this is the right correction, and why it is now stronger than revision 1's.*
The defect is real and the reviewer confirmed it: the `Requirement` names
`docs/review-policy` while the row's **own `AcceptanceCriteria`** already names
`docs/process.toml [policies] review_rounds`. But the reviewer's SR-018 evidence
— that the legacy files are still deliberately read through the migration window
— applies here too. So the fix is **not** to delete the legacy name; it is to
name the canonical home **and** keep the legacy read, in the exact phrasing
SR-017 already uses and that was already blessed. Revision 1 would have deleted
a true clause.

---

**SR-140** · Draft — free to edit · **PRESERVING · Δ +4 / −0**

*PROPOSED (exact):*
> The kit shall record each acceptance on the accepted artifact's own row - the
> commit whose tree carries the text that was accepted, and a digest of that row's
> NORMATIVE cells - never in a second registry keyed on the same artifact.
> It shall report text that has moved away from its recorded anchor regardless of
> any Status movement.
> It shall treat an anchor written in the same commit as the text it anchors as an
> error.

*Δ:* **+4 words** ("It shall" ×2). The shouting caps on "ON THE ACCEPTED
ARTIFACT'S OWN ROW" are lowercased; **"NORMATIVE" is kept capitalised** because
D-1 makes that scoping load-bearing.

---

**SR-137** · Draft — free to edit · **PRESERVING · Δ +0 / −0**

*PROPOSED (exact):*
> The kit shall read every process policy dial from a single `docs/process.toml`,
> and shall REFUSE — never resolve by precedence — a repo in which any dial is
> declared both there and in its legacy one-word file.
> The file's line shape shall be a checked contract: one `key = value` per line
> under a bare `[section]` header, no dotted keys, no inline tables, no multi-line
> strings.

*Δ:* **zero** — already two clean sentences; presented for completeness because
it is the receiving row for SN-028's form (ii).

### E.2 · Rows DROPPED from the batch

Per correction 3, these are removed rather than presented as outlines. **Reason
for all thirteen: exact replacement text was not produced in this pass, and an
outline is not ratifiable.** They remain on the measured list for a future pass.

`SR-129` · `SR-031` · `SR-136` · `SR-147`¹ · `SR-053` · `SR-054` · `SR-052` ·
`SR-056` · `SR-043`² · `SR-144` · `SR-139` · `SR-142` · `SR-145`

¹ SR-147 leaves the *legibility* batch but stays in §E.3 as a **carrier
correction**. ² SR-043 is additionally unresolved on fact — see §G.

### E.3 · Stale text — one confirmed, two carrier corrections, four CANNOT VERIFY

| SR | status | claim | verdict |
|---|---|---|---|
| **SR-040** | Modified | `Requirement` names retired `docs/review-policy` while its own acceptance names `docs/process.toml [policies] review_rounds` | **✅ CONFIRMED DEFECT** (reviewer concurs). Exact fix in §E.1 |
| **SR-018** | Verified | *revision 1 claimed:* `docs/privacy-check` is retired | **❌ WITHDRAWN — revision 1 was wrong.** Verified the reviewer's refutation myself: `check_privacy.py` falls back to `_first_declared_line(root/"docs"/"privacy-check")` "(migration window)", and **all three shipped hooks** (`pre-commit`, `pre-push`, `commit-msg`) read it. SR-031 and SR-138 preserve legacy reads by design. The text is **not false**; at most it names the non-canonical home. **Offered as an optional clarification only** — calling a `Verified` row defective would have spent a re-attestation on nothing |
| **SR-085** | Verified | "page through gate policy" = retired enum | **⚠ CANNOT VERIFY.** `agent_loop.py:2748` derives a **live** runtime label `gate_policy = "human-held" if human_held else "loop-held"`. The phrase may denote the live label, not the retired config enum. **Reviewer correct; revision 1 overclaimed** |
| **SR-108** | Verified | same | **⚠ CANNOT VERIFY** — same reasoning |
| **SR-125** | Modified | title says "gate policy" | **⚠ CANNOT VERIFY** — same reasoning; title-only in any case |
| **SR-082** | Modified | same | **⚠ CANNOT VERIFY (accepted at round 2).** Its *Requirement* cell says *"the **retired** three-value enum"* explicitly — unambiguous, and merely unreadable, not stale. But its *acceptance* cell separately says "page according to gate policy", the same ambiguous phrase as SR-085/108/125, so the row as a whole cannot be classified stale-vs-current without a ruling on which referent that phrase carries. The §E.1 rewrite of the Requirement cell stands, conditional on the sitting confirming the drain-dial reading |

> **The finding underneath all four CANNOT VERIFYs is worth more than the
> defects would have been.** `gate_policy` names **two different things**: a
> retired configuration enum (`attended`/`single-ratify`/`autonomous`) and a live
> runtime label (`human-held`/`loop-held`). `agent_loop.py:2865` even falls back
> to the string `"attested"`/`"attended"` for the live label. **One token, two
> meanings, one of them retired** — that is a naming defect that will keep
> generating false stale-text reports (it generated two in revision 1). Recommend
> the sitting **rename the live runtime label**.

**Carrier corrections — owed WITH the cutover commit** (correction 9, with the
precision fix). `git status` shows the TOML **staged** (`A`) and the CSV
**deleted** (`D`) in the index, with `interfaces.csv` still in conflict (`UU`);
`HEAD` still carries CSV. So these are not "already stale" and not
"forward-looking" — they are **false the moment that index is committed**, which
is imminent:

- **SR-002** — Title *"Integrity floor for ids and **CSV structure**"*;
  requirement *"a data row whose **column count** differs from its header"*. A
  TOML carrier has no column count. **The obligation survives; the wording does
  not.** Must ride the cutover commit.
- **SR-147** — describes the current spine as *"stakeholder needs as markdown
  prose tables, the other three tiers as CSV"*. True at `HEAD`, false at the next
  commit. Its converter obligation is unaffected; only the tense is.

### E.4 · ⚠ The rule §8.3 item 1 collides with — SR-126

**SR-126 (`Verified`):** *"trace.py shall fail under --strict when any spine row's
normative text cites a work item or a process doc."* Its acceptance criteria
close with: *"…a **script name**, artifact path, rubric or sibling spine id **does
not**."*

**The kit has already ruled, mechanically and at `Verified`, that script names in
spine normative text are permitted** — and built a check whose *explicit carve-out*
is the very thing §8.3 item 1 wants forbidden.

This is not a wording clash; it is two rules pointing opposite ways, one of them
enforced. Three coherent resolutions, for the owner:

1. **Scope item 1 to the SN tier only.** SR-126 governs "any spine row"; SNs are
   arguably outside its enforcement today (it names SR/LLR/TC cells). Cheapest,
   and consistent with this proposal's form-(i)/form-(ii) split.
2. **Amend SR-126** to move `script name` from the allowed list to the flagged
   list *for the SN tier*. A `Verified` row amendment — a real re-attest.
3. **Rule item 1 as prose guidance, not a mechanical check.** Then §D item 1's
   *SR-a* should not be minted at all.

**Do not adopt §8.3 item 1 as a mechanical rule until this is ruled.** It would
put two enforced rules in contradiction.

### E.5 · One pattern, offered as a separate ruling

Six rows carry **migration history inside the `Requirement` cell** ("the retired
X, deleted by SR-Y, is not an input"; "the legacy Z half retired with the
dispatcher at Phase 5"). A requirement cell states an obligation; *why it used to
be different* is rationale.

**Offered as its own ruling, not folded into the formatting pass** — because
moving text between cells changes which cell a re-attest reads, which is not a
formatting change. Revision 1 smuggled this into three "preserving" rewrites;
that was wrong and is undone above.

---

## F · Sequencing

**Land the batch inside the P0 sitting's part 2 re-blessing window, and after the
carrier cutover is committed.** Challenge 1 governs: rewriting ratified SN prose
opens re-attest windows, and part 2 *is* already a re-blessing window for the 25
rows it holds — doing both at once collapses two windows into one. The carrier
helps independently: every §E.1 reformat is a multi-line TOML string and a CSV
escaping exercise, so each is strictly cheaper after the cutover, and doing them
before means the converter must carry rewritten text through — braiding two
migrations the way §8.1 warns against. Within the window: **(1)** rule §C's level
question first, since seven of ten edge rows are demotion candidates and
rewriting a demoted row is wasted work; **(2)** rule §E.4 (the SR-126 collision)
next, because it decides whether §8.3 item 1 is a check, a scoped check, or
guidance — and therefore whether form (ii) exists at all; **(3)** rule the
challenge-2 re-homing as one policy yes/no, constrained by §B.0's three blocked
rows; **(4)** execute SR-040 and the two carrier corrections **regardless of the
prose ruling** — SR-040 is a confirmed defect and SR-002/SR-147 must ride the
cutover commit; **(5)** everything `Draft` — SN-029, SR-137, SR-139, SR-140,
SR-142, SR-144, SR-145, SR-147 — is editable **at any time at zero attestation
cost** and can go ahead of the sitting to shrink the window's load. Q11 still
binds: this batch preserves today's `Status` vocabulary and touches no `Modified`
row's obligation, so the 38 rows owing a re-blessing keep owing it — **nothing
here may be executed in a way that lets a prose edit look like a ratification.**

---

## G · Recorded as too low-confidence to propose

1. **The `"(Note this )"` completion** — the record does not say which item or
   what it meant. Owner input required.
2. **Whether `agent-resume` should also install dependencies** — the repeated
   dev-setup text is either artifact or requirement; the two produce materially
   different rows and different tiers.
3. **Whether `docs/subagent-gate` (SR-043) is stale** — no reader found in
   `project-trajectory/scripts/`; the gate is hook-side and was not traced to a
   reader. SR-043 is dropped from the batch on this ground.
4. **What SR-059's trailing parenthetical was meant to say** — it is
   ungrammatical as committed. Repairing it means deciding its meaning.
5. **Whether "gate policy" in SR-085/SR-108/SR-125 denotes the retired enum or
   the live runtime label** — see §E.3. Unresolvable from the text alone.
6. **Whether SN-016 should be promoted to core and SN-017 retained** — both are
   above the demotion line, so the precedent does not decide them.
7. **SR-025's title/requirement mismatch** — the title reads *"Skills index +
   checked per-agent fan-out"* while the requirement covers only index
   regeneration. Resolving it means deciding whether an obligation exists.
8. **Splitting SR-050 and SR-055 into separate requirements** — worth
   considering, deliberately not drafted: it mints ids, changes the
   decomposition, and may be pre-empted by §D item 6.
9. **Whether item 1 should mint a new SN or fold into SN-010** — argument both
   ways; now additionally blocked on §E.4.
10. **The Linux double-click surface** — no desktop contract exists in this repo;
    marked CANNOT VERIFY rather than asserted as a gap.
11. **Whether SN is always human-attested** — the owner's §8.3 text and the D-3
    ordinal model disagree. §D flags it; revision 1 silently normalised it and
    that normalisation is withdrawn.
