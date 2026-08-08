# Mechanized-loop decisions and glossary (P0 of the 2026-08-08 build plan)

**Status:** RATIFIED 2026-08-08 by owner direction ("fully implement the plan
… outside of this repo's standard workflow"). This file is the **single home**
for the program's ratified terminology and decisions; the build plan
[stakeholder-needs-build-plan-2026-08-08.md](stakeholder-needs-build-plan-2026-08-08.md)
stays the *plan of record* (what to build, in what order) and does not restate
what is settled here.

**Its companion is
[mechanized-loop-contracts.md](mechanized-loop-contracts.md)** — the *seams*
the slices share (the `docs/config.toml` schema, the `docs/events/` envelope,
the module/symbol map, the canonicalisation rule, the refusal form). Decisions
here, interfaces there: a builder reads this file to learn what was ruled and
that one to learn what to call.

**Execution exception (plan §preamble, re-ratified here).** This program
replaces the machinery that would normally drive it, so it is built on the
single controlled branch `mechanized-loop` with explicit reviews and manual
integration checkpoints. The live `agent-resume` loop is **frozen for the
duration** by a tracked [`docs/work/pause`](work/pause) — deleting that file is
the owner's act, not a builder's.

---

## 1. Glossary

The words below are used with exactly these meanings across the config schema,
the ledgers, the prompts, the code and the tests. Where a word already had a
different meaning in this repo, the divergence is stated.

| Term | Meaning |
|---|---|
| **spine stage** (`spine_stage`) | 0–4. Which artifact tier of the SN→SR→LLR→TC spine is *in process*. The **workflow/admission** input. Table in §3. |
| **verification gate** (`verification_gate`) | `G1`\|`G2`\|`G3`. Which `check.py` step tier applies. The **harness** input. Unchanged in meaning from today's `docs/gate`. |
| **human ratification boundary** (`human_ratification_through`) | Integer 0–3, **cumulative and inclusive**: `0`=SN only; `1`=SN+SR; `2`=SN+SR+LLR; `3`=SN+SR+LLR+TC. A ratification at or below the boundary requires a human decision; above it an adjudicator may enact. Replaces `docs/gate-policy`'s enum. |
| **final full-spine review** (`final_full_spine_review`) | `never`\|`always`. Persistent policy for a whole-spine human review at stage 4. A *more frequent* one-shot ask is a **review-request event**, not a config edit. |
| **normative cells** | The subset of an artifact's cells whose change alters its **meaning**. Per-kind lists in §4. The digest input. |
| **attestation event** | One append-only record that an artifact's normative digest was accepted (`ratified`), re-accepted without meaning change (`clarity`), invalidated (`meaning`), or overridden by a human (`override`). |
| **accepted anchor** | The newest valid attestation event in an artifact's chain whose decision is `ratified`, `clarity`, or `override`-to-accepted. What "the current attested text" means. |
| **clarity** verdict | The normative digest changed but the meaning did not. Advances the accepted anchor to the new digest; does **not** lower `spine_stage`. |
| **meaning** verdict | The change alters obligation. Writes a *pending* event and pulls `spine_stage` back to that artifact's tier. |
| **worker outcome** | One of `complete` \| `cancelled` \| `partial`, chosen by the branch's worker and recorded in an immutable **outcome event**. |
| **outcome event** | The immutable per-attempt record written outside `docs/work/`. One per terminal branch. Carries facts, never instructions. |
| **disposition event** | The adjudicator's record confirming or overriding a worker outcome. Append-only; never edits the outcome event. |
| **successor** | A newly minted WI carrying the *remaining* scope of a Partial attempt, with explicit `supersedes` lineage. Never the original WI revived. |
| **admission verdict** | The recorded conflict ruling that permits a `draft/` candidate to enter `queued/`: `no-conflict` \| `compatible-overlap` \| `conflict`. |
| **job** | A named role a model is drawn for: `planner`, `critic`, `arbiter`, `implementer`, `reviewer`, `adjudicator`. Config declares a weighted **pool** per job. |
| **route** | One (provider × model × invocation) triple with strength and capabilities. The config successor of an `docs/agents.csv` row. |
| **prompt template** | A reviewed Markdown asset with a declared slot contract and output schema. The config successor of an embedded Python prompt constant. |
| **NEEDS-JUDGEMENT** | The renamed `NEEDS-HUMAN` signal (WI-417 judgement 4, absorbed here). Names the owed *act*; who supplies it follows from the ratification boundary. Exit code **7 does not move**. |

**Divergences to note.**

- `Attest` remains a *requirement verification method* in the SR `Verification`
  column. It is **not** the name of the human-boundary dial — that is
  `human_ratification_through` (plan §1.4).
- `exclusive` keeps its two existing senses (`schedule.py`'s mutex-key column
  vs. the concurrency axis). This program adds no third sense.
- `blocked` remains a *derived* disposition (queued + `blockref`). The general
  `blockref` mechanism survives; only its **handback** use is retired (§7).

---

## 2. Ratified decisions

Numbering follows the build plan §1 so a reader can move between the two.

1. **Python 3.11+ core, three thin starters, kept.** No launcher rewrite.
2. **One adopter-owned `docs/config.toml`** is the only editable source for
   behavior, validated by a strict loader. A kit re-sync never clobbers it; the
   kit ships `config.toml.template` plus a converter, and bootstrap/re-sync runs
   the converter automatically.
3. **`spine_stage` and `verification_gate` are separate derived facts.** No
   caller infers one from the other; a declared mapping function joins them.
4. **The numeric dial is `human_ratification_through`.**
5. **The branch's judgment is real:** the worker moves the byte-identical spec
   to `complete/`, `cancelled/` or `partial/` and writes a separate immutable
   outcome event. Partial and Cancelled always adjudicate; Complete adjudicates
   on risk triggers or sampling. Every path keeps an override channel. **Scope
   text never changes on the branch.**
6. **An attempted WI is never revived.** Remaining scope is a newly minted
   successor with lineage and a fresh queue-conflict verdict.
7. **Attestation history is an append-only ledger** keyed by artifact id and
   normative-text digest. No Git hashes are added to requirements rows.
8. **Every operational LLM prompt is an externalized, reviewed Markdown
   template** with validated slot and output contracts; template and
   rendered-prompt hashes are recorded per session.

### 2.1 Decisions this program additionally settles

These were open when the plan was written; they are settled here so the build
does not re-litigate them.

- **D-1 — the config-query entry point wins over the greppable convention.**
  Shell hooks call `python project-trajectory/scripts/config_query.py` for
  `privacy-check` and `review-policy`. A missing or below-floor interpreter
  **refuses loudly and fails closed**, which preserves (and strengthens) the
  M-42 requirement that a Python-less box still fails closed. The recorded
  fallback (a keyed-greppable one-`key = value`-per-line convention) is *not*
  built; it stays a documented contingency in §5 of the plan.
- **D-2 — terminal folder name is `partial/`**, not `returned/`.
  `docs/handback-contract.md` §5's `returned/` proposal is superseded; that
  document is amended to point here rather than deleted (it remains the
  diagnosis of record).
- **D-3 — outcome/disposition/attestation/failure events live outside
  `docs/work/`** in `docs/events/` (one JSONL ledger per kind). This avoids
  `agent_common.spec_files`' `rglob("WI-*.md")` trap (handback-contract §8) and
  keeps `docs/work/` exactly the WI registry.
- **D-4 — `handback.py`'s mutating return is retired**, together with the
  self-`blockref` convention and the mutable `## Handback` section. The
  `quarantine` arm survives and is generalized into the Partial
  keep/discard/quarantine classification.

  > **STATUS 2026-08-08: RULED, NOT LANDED — and the gap is deliberate.** P14
  > applied the rule it was given (*every caller moves to the outcome-event path
  > first, or the deletion does not happen*) and stopped, because **the ruling
  > this decision depends on does not exist**: `hand_back`'s only caller is
  > `dispatch._lane_close`, which is precisely the case where a worker exited
  > non-zero having decided **nothing**. D-5 gives the path where the *worker*
  > writes its own outcome event and moves its own spec; it says nothing about
  > who authors a `partial` outcome event **on behalf of** a worker that
  > crashed, nor what `parent` and rationale that event carries.
  >
  > Everything downstream waits on that one answer: `intake._returned_spec` /
  > `_handback_drafts` detect a return by reading the `## Handback` *section* off
  > the merged spec, and `integrate.OUTCOME_DIRS` still maps
  > `queued|draft|deferred -> handback` as a fourth answer the tree can give.
  >
  > Inventing the missing ruling inside a deletion slice would have been the
  > "policy change dressed as a cutover" the cutover slice had already refused
  > once. **What is owed is one owner ruling, not more code.** What DID land from
  > this decision's dependency set: `intake.tier_signal` no longer keys the build
  > tier off a prose substring (D-6 judgement 1), which was one of the couplings
  > that made the deletion expensive.
- **D-5 — `docs/agents.csv` and `docs/agents-enabled` are converted, not
  kept.** Routes move into `config.toml`; the **consent** property of
  `agents-enabled` (presence-as-consent) moves to an explicit
  `[routing] enabled = true` plus the per-job pools, and the file is retired at
  P14 only after the converter has run.
- **D-6 — the `NEEDS-HUMAN` label is renamed `NEEDS-JUDGEMENT`** (WI-417
  judgement 4) and the tier decision keys off the **worker exit-code class**,
  never off a substring of prose (judgement 1). A handback reason string is
  retired outright with `handback.py` (judgement 2 answered by deletion).
- **D-7 — a Partial attempt's branch commits must carry an explicit
  keep/discard/quarantine classification** before the integrator will accept the
  branch. This is the direct answer to the 2026-08-03 incident (`08e6c08a`),
  where a green-merged handback landed rejected code as-is.

---

## 3. The two axes

`spine_stage` — the workflow/admission input:

| `spine_stage` | Meaning | Entry condition |
|---:|---|---|
| 0 | Stakeholder needs in process | at least one current SN has no accepted normative-text anchor |
| 1 | System requirements in process | all current SNs are ratified; at least one current SR is not |
| 2 | Low-level requirements in process | all current SRs are ratified; at least one required LLR is not |
| 3 | Test cases in process | all required LLRs are ratified; at least one required TC is not validated |
| 4 | Full breakdown implemented and validated | all required TCs are validated *(attestation half — see below)* |

**Stage 4 is two facts owned by two components, ruled 2026-08-08.** The row
originally read "all required TCs are validated **and the full declared harness
is green**", which mixes an attestation fact with a harness fact.
`derive_gate.spine_stage` reads registries and the ledger; it cannot observe
harness greenness without running the harness, and a *cached* stage asserting a
green it never watched is exactly the dishonest green SN-008 forbids. So:

- **`spine_stage` derives the attestation half only** — every required TC has an
  accepted anchor. Stage 4 means "the breakdown is complete and attested."
- **`check.py` owns the harness half**, as it always has.
- **The resume planner joins them** (`§9`'s red-bar rung): stage 4 *plus* a red
  declared bar is what produces a failure event and a remediation draft. Neither
  component claims the other's fact.

`verification_gate` — the harness input, preserving today's `check.py`
contract:

| `spine_stage` | `verification_gate` |
|---:|---|
| 0 | `G1` |
| 1 | `G1` |
| 2 | `G2` |
| 3 | `G2` |
| 4 | `G3` |

A **meaning** verdict at tier *T* derives `spine_stage = T` (SN→0, SR→1,
LLR→2, TC→3). A **clarity** verdict advances the accepted anchor without
lowering the stage.

`docs/gate` remains the cached, generated home of `verification_gate` and keeps
its existing first-non-comment-line contract. The stage is published on the
same `# basis:` line as an additive `spine-stage=N` field, exactly as
`ex-draft=` and `uncovered=` were added before it.

---

## 4. Normative cells per artifact kind

The digest input. Cells outside these lists (evidence pointers, phase labels,
areas, status words) may change without invalidating an anchor.

| Kind | Normative cells |
|---|---|
| SN | the need statement, the rationale, the priority, the acceptance intent |
| SR | `Title`, `SN-Refs`, `Requirement`, `AcceptanceCriteria`, `Permutations`, `Priority`, `Verification` |
| LLR | `SR-Refs`, `Title`, `Detail` |
| TC | `Verifies`, `Level`, `Method`, `Parameters`, `Expected` |

Cells are canonicalized before digesting (NFC, CRLF→LF, collapse runs of
inline whitespace, strip leading/trailing whitespace) so a re-wrap is never a
false meaning change. The canonical form carries a schema version so the rule
can evolve without invalidating history.

---

## 5. What this program does NOT change

- `check.py`'s gate vocabulary and step table semantics (`G1`/`G2`/`G3`/`all`).
- The `SN→SR→LLR→TC` registry schemas and `trace.py`'s join/orphan rules.
- The station protocol: a branch may not enter the merge queue unless trunk is
  already its ancestor (`concurrency-v2.md` §A2).
- The R1 invariant: **a work branch never mints a WI id.**
- The F5 independently-copyable-script convention (duplication closed by
  sync tests, not by extraction).
- The 50%-of-machine test-run cap and the byte budgets.

---

## 6. Combined sitting declaration

Per plan §4, the following are declared **one combined drafting-plus-
re-attestation sitting**, executed on this branch:

- draft `SN-028`…`SN-032` under a `## Draft needs` heading and amend `SN-026`;
- re-attest the 21 already-`Modified` spine rows (20 SRs + `TC-034`);
- absorb `WI-390`'s still-needed spine/prose/connectivity close.

The temporary derived-gate drop while the sitting is open is the model
honestly exposing in-process scope, not a regression.
