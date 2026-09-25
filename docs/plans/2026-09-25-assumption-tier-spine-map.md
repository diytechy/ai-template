# The assumption tier's spine — derivation map and decision record

**Status: WORKING RECORD of an attended grind, begun 2026-09-25.** The owner
ruled the [C1 sitting package](2026-09-25-c1-sitting-package.md) and asked for
the spine to be derived down to test cases for
[the assumption-tier plan](2026-09-20-validation-gap-and-the-assumption-tier.md)
("AT") and the work in its scope. The owner is absent. A Fable reviewer stands
in for the owner's approvals, and a codex Sol review (medium effort) runs on
each iteration. This file is the decomposition record those reviews read: which
row realizes which part of the plan, why each row sits at its tier, where
decomposition stops, and every assumption or decision made on the way (§6).

The rows themselves are the spec of record; this file restates none of their
text.

---

## 1. Scope

| in scope | source |
|---|---|
| The assumption tier's core, C1–C5 | AT §6–§8, §10.2a–l, §11 |
| The interface-allocation extension, E | AT §9, §10.3 |
| Hats per piece | AT §6.5 |
| S3: the needs' pointer column and the vision's two headline needs | sister plan §1.3; package §3 |
| S6: re-judging observation tests at checkpoints, designed with C3 | sister plan §2.3, S6 ruling |

**Out of scope** (decision D1, §6): the other queued sister-plan items
(WI-613 to WI-624, WI-626), the terminology prose pass (T, WI-615), and the
frame's own content (its rows are the sitting commit's, after the build).

## 2. The needs

| need | stakeholder (package §3.2) | source (package §3.4) | chains answering it |
|---|---|---|---|
| SN-041 readable, maintainable code | Owner | the vision's O1 anchor | SR-216 |
| SN-042 test-first | Owner | the vision's O3 anchor | SR-217 |
| SN-043 premises beyond the system's own behavior are recorded and checked | Reviewer | — | SR-187, SR-188, SR-191–SR-206, SR-210–SR-212, SR-214, SR-215, SR-218 |
| SN-044 each need names its stakeholders and its source | Owner | — | SR-189, SR-190, SR-195 |

SN-043 and SN-044 are new: no existing need demands the assumption tier or the
stakeholder list (D2). All four stay Drafted until a complete chain answers
each (package §0.2(a)). Their `stakeholder_refs` and `source` cells cannot be
written until the build ships those keys (D3).

## 3. Plan coverage

| plan item | row(s) |
|---|---|
| §10.2a frame cells: `system` on crossings | SR-187 |
| §5.1 an SR's system derived from its crossings; one spanning both reported | SR-219 |
| §6.2 check: a need met in operation with no operation crossing | SR-188 |
| §10.2f stakeholder list, SN `stakeholder_refs` | SR-189 |
| S3 the needs' `source` column | SR-190 |
| §10.2b assumption registry and its applies-when | SR-191 |
| §5.3 / §8.3 surrogates | SR-192 |
| §10.2d SR `da_refs` or a `coincident` waiver; unclassified | SR-193 |
| §9 / §10.2k SR `form` | SR-194 |
| §6.2 `effect_at` reach, `mediates` | SR-195 |
| §6.2 checks: an uncited assumption, no falsifier | SR-196 |
| §10.2e TC `assumption_refs`, conditional `Verifies`, phase inheritance, attribution | SR-197 |
| §10.2e TC `sampling` and `max_age`, the seven-day floor; S6's declared inputs; the sampling model §7 needs | SR-198 |
| §10.2l observation result records, judged-state digest (shared with S6) | SR-199 |
| §7 evidence level, one freshness model | SR-200 |
| §12.6 item 1 blast radius; §11 falsified-assumption finding | SR-201 |
| §7 `accepted_risk` triggers | SR-202 |
| §10.2g assumption approval brief | SR-203 |
| §10.2c stage arms, off until the first approval; tier-specific status | SR-204 |
| SN-043's "a reviewer can see, for each outcome": the per-need view | SR-218 |
| §11 C5 gate at DevStg-Boundary (maturity) | SR-205 |
| §11 C5 gate at DevStg-Release (evidence) | SR-206 |
| §10.2j row-level refusal | SR-207 |
| §10.2h dial enforcement for off-spine registries | SR-208 |
| §10.2i loop provenance trailer | SR-209 |
| §11 finding: a loop commit changing a human-held status | SR-210 |
| §9 IF `bridged_by` / `coincident` | SR-211 |
| §9 the extension's gate | SR-212 |
| §6.5 `speaks_for` | SR-213 |
| §6.5 obstacle provenance | SR-214 |
| S6 checkpoint re-judging | SR-215 |
| SN-041's second acceptance sentence | SR-216 |
| SN-042 | SR-217 |

**Not rows, by design:** the frame's content (the sitting commit); the reversal
sweep of the nine stale rows (package §2.2, a work item); the terminology pass
(T); enabling C5 in this repository (a setting, not a requirement); the DA and
surrogate rows themselves (C2 content, after the build); moving the approval
dial (Q14, a setting, in the sitting commit).

## 4. Tiering and stopping boundaries

- **Every SR is `Test`.** Each obligation is a harness behavior with a
  mechanical outcome (a strict failure, an advisory line, a refusal, a derived
  value). No row's floor is a human judgment.
- **One decision per SR.** A crossing's system (SR-187) and a requirement's
  derived system (SR-219) are separate rows, because either can pass while the
  other fails. Where one SR still names two outcomes, its rationale says why
  they are one contract (SR-198's declaration, SR-204's start of reading).
- **Registration plumbing is design, not requirement.** The id space, the carrier
  maps, the template, the scaffold mapping and the snapshot tier of each new
  registry are LLRs under the SR that introduces the registry.
- **Cell classification (Q23) sits with the SR that introduces the cell.** Each
  SR's acceptance states whether its cell is traced or approved content; one
  design row carries the classifier table for all of them.
- **Decomposition stops at the LLR** that names the symbol realizing the SR.
  Test cases verify the SR and its LLRs together (the triangle rule).

## 5. Iterations

| # | tier | rows | Sol review | stand-in verdict |
|---|---|---|---|---|
| 1 | SN + SR | SN-041–SN-044, SR-187–SR-219 | NOT YET SOUND: 1 blocker, 6 major, 1 minor; all applied | APPROVE-WITH-CHANGES: 1 blocker, 7 major, 6 minor, all applied; fixes CONFIRMED with one residual major (SR-217's quantifier) and three minor, all applied. The later SR-207/SR-208 scoping is confirmed with iteration 2. |

## 6. Assumptions and critical decisions

Each entry: what was decided, why, and what the owner would change to reverse
it. Numbered so the owner can answer by number.

- **D1 — Scope.** "The full plan and work items in scope" is read as the
  assumption-tier plan in full, plus the sister-plan items it pulls in (S3 at
  C1, S6 designed with C3). The other queued sister-plan items are separate work
  with their own specs of record.
- **D2 — Two new needs.** SN-043 (the assumption tier) and SN-044 (stakeholders
  and sources) are written because no existing need demands those rows. Tracing
  them to SN-002 or SN-037 would attach them to needs whose text does not ask
  for them. Both are new text at the owner's held rung, so the stand-in's
  approval of them is the one most in need of the owner's re-attestation.
- **D3 — Needs without their new cells.** SN-041 to SN-044 are written without
  `stakeholder_refs` and `source`, because the dogfood key rule refuses a key
  the template does not ship. The build adds them, and the sitting commit
  writes every need's stakeholder.
- **D4 — Phase 6.** Every new row is phase 6 (`derive_stage.py --next-phase`).
  Complete chains approved together read DevStg-Impl in phase 6, and the
  repository's headline stage stays DevStg-Tests (phase 5 is the minimum).
- **D5 — SN-041's first acceptance sentence is an assumption, not an SR.** The
  sentence about a reader new to the code is a claim about people, the W the
  assumption tier exists to record. It becomes an assumption row with a sampled
  test in C2, after the registry exists. Until then SR-216 alone answers the
  need, which the coverage rung accepts.
- **D6 — SN-042's acceptance amended to a prospective scope.** It said "for
  every requirement", which this repository cannot meet: its existing
  requirements were largely written after their code. Both reviewers found SR-217
  silently narrowing it. On the stand-in's recommendation the acceptance now
  reads "for every requirement approved after the project adopts this rule", and
  SR-217 defines the implementation event as the first commit that adds code
  declaring it implements the requirement or one of its design rows. A project
  declaring no starting point is judged whole. OWNER-RESERVED: this changes text
  the owner accepted verbatim, so it is the first thing to re-attest.
- **D7 — Bundles.** New SRs cite `B-05`, the delivered package, except the
  authority rows (SR-207, SR-208, SR-210 on `B-02`) and the commit floor
  (SR-209 on `B-01`, `B-04`). After the redraw, C2 re-points them by subject.
- **D8 — The gate's rungs.** The extension's gate (SR-212) sits at
  DevStg-Arch, where interfaces are approved; AT §11 says the Boundary half
  "also runs per reached boundary IF". Interfaces exist only from the Arch rung,
  so the check waits for them. OWNER-RESERVED: confirm the deviation.
- **D9 — Observation tests declare their inputs.** S6's digest needs each
  observation test case to declare what it reads. The stand-in ruled the
  declaration approved content at the SR tier, so SR-198 now carries every
  observation test case's declaration: its inputs, a result lifetime of at least
  seven days, a sampling policy where it evidences an assumption, and an optional
  sampling model, which SR-206 needs for a sampled result to count. Omissions are
  reported rather than refused, so existing inspection tests keep passing.
- **D10 — The smoke budget.** Commits in this grind record the smoke budget's
  failure on this 8-core machine (about 400 s against 60 s) rather than
  re-stamping it, as the handoff records. Results pass every time.
- **D11 — "Down to test cases" means TC rows, not test code.** Each TC names
  the test it will be (its `Evidence` cell points at the planned test file),
  and the implementation work item writes that test red, then the code that
  turns it green. Failing tests committed now would red every commit's bar.
- **D12 — No new interface rows yet.** A new seam's IF row needs its contract
  body in the owning module's header, and those modules do not exist. Each
  implementation work item adds the IF rows its seams imply, as the Tests-bar
  practice asks.
- **D13 — Activation is derived, not declared.** SR-204 first said "one
  declared setting". The stage research found no legal home for one:
  `docs/process.toml` is kept out of the stage's inputs by an existing ruling,
  and no registry carries a file-level key. A tier is now read once one of its
  rows is approved, which puts the switch in the commit that approves the first
  batch — the single commit Q20 asks for — with nothing to disagree with the
  rows.
- **D14 — SR-187 is derived from SN-043.** No need asks for two systems of
  interest; SN-037 speaks of one system. The split exists so an assumption has
  an operation crossing to land on, which SN-043's "where its outcome lands"
  needs, and the rationale argues that. OWNER-RESERVED: whether the two-frame
  orientation deserves an owner need of its own, as a design constraint.
- **D15 — SR-213 kept, derived through the maintainer's lens.** The stand-in
  preferred folding `speaks_for` into SR-189; Sol found SN-044 does not demand
  it. It stays its own row under SN-036 only, attributed to MAINTAINER, because
  recording whose voice a perspective is answers "why does this perspective
  exist" for a later reader.
- **D16 — Gates are check steps, not stage conjuncts.** SR-205, SR-206 and
  SR-212 "fail the gate" as harness steps at the Boundary, Release and Arch
  thresholds, enabled by a `[checks]` setting. Putting them in the stage
  derivation would break the single evidence-driven Release producer and read a
  file the stage may not read. This is an LLR choice, recorded here because it
  fixes what "gate" means in three SRs.
- **D17 — Firing review perspectives per assumption is design.** AT §6.5 notes
  that hats fire per assumption only with assumption tags or a composer per
  bundle. That mechanism is an LLR under SR-214, not a row of its own.
- **D18 — SR-207 stops at the tiers the kit compares.** Need-text drift is
  not detected anywhere, and the owner kept that detector deferred (OI-85).
  Row-level refusal therefore covers every tier compared with a recorded copy,
  including tiers sharing a file, and says outright that stakeholder needs stay
  outside it until their drift is compared. Funding the need-drift detector
  would close the gap; it is not part of this grind.
- **D19 — SR-208 promises that a refused change never lands.** An AI session's
  own staging cannot be intercepted, and several loop writers bypass the commit
  hook, so the refusal comes where the loop's code commits and again at the merge.
- **D20 — The stand-in authorized SN-042's amendment** (D6) as the owner's
  stand-in. It is recorded as the stand-in's act, not the owner's signature.
