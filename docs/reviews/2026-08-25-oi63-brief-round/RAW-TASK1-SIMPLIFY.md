# RAW - TASK 1, the simplification draft

Unedited final message from `OPENAI-SOL` (`gpt-5.6-sol`, `codex exec`),
2026-08-25, executing TASK 1 of [BRIEF.md](BRIEF.md). 84,115 tokens.
Adjudication: [RESUME.md](RESUME.md).

---

## one_line

OI-63 discharges obligation 2 of OI-62's option (e), MEASURE, DO NOT REWRITE: decide whether irreducible `contract` content moves to an owning-component header or stays in-cell. Across 108 non-CLI rows, WI-516 found 64.3% restatement (CLI: 87.7%) and remainder on 65.7% of rows (CLI: 40.7%). It also found that 15.3% is non-crossing registry bookkeeping, provenance, or argument belonging in neither home.

## decision

ORIGIN

OI-62 ruled (e): classify 108 non-CLI rows without editing, preserve durable verdicts, then file relocation with per-family numbers. OI-63 discharges obligation 2:

"at the pass's close, the relocation question - does the irreducible remainder move to a contract header / output-interface declaration on the owning component's side, or stay in the cell - is FILED as its own open item with the measured per-family numbers in its brief."

The owner's question:

"if enough appear to be restatement, my next question would be if the unique content that does exist in the contract today should instead be absorbed as some sort of contract header / output interface definition on the owning component side rather than something sitting in the contract row."

NUMBERS

| metric | CLI | Provides | Consumes | non-CLI |
|---|---:|---:|---:|---:|
| rows | 27 | 19 | 89 | 108 |
| characters | 7,385 | 10,278 | 33,717 | 43,995 |
| restatement | 87.7% | 75.9% | 60.8% | 64.3% |
| remainder | 12.3% | 21.2% | 20.2% | 20.4% |
| non-crossing | not a category | 2.9% | 19.0% | 15.3% |
| rows with remainder | 40.7% | 84.2% | 61.8% | 65.7% |

Every row was read, never regexed; `docs/plans/2026-08-25-if-contract-verdicts.md` is the derivation.

CATEGORIES

RESTATEMENT  
: Recoverable from the owner row, harvested module surface, committed generated reference/declared policy, the row's other cells, or the consumed medium's header.

IRREDUCIBLE REMAINDER  
: A typed crossing fact in none of those homes, recoverable only from implementation. Classes: A—written artifact/named medium; B—fail-loud guarantee; C—exclusion/negative claim; D—typed shape/wire format; E—closed vocabulary; F—consumer-side obligation binding the reader; G—purity/idempotence/determinism/network-gating posture; H—compatibility guarantee; I—counterparty calling convention.

NON-CROSSING  
: Neither recoverable nor about the crossing. M—module internals; X—registry bookkeeping, provenance, or argument.

FINDINGS

1. Pilot outlier: 19/108 non-CLI rows are pure restatement versus 16/27 CLI rows. Relocation still covers 8,975 characters over 71 rows, but remainder occurs on most rows.
2. Family split: Provides is longer/denser in remainder with 2.9% non-crossing; Consumes has 19.0% non-crossing. A common ruling rests on an average.
3. Third class: `IF-082/083/084/085/138` name another row's contract, then spend 110–250 characters explaining existence; `IF-112` spends 330/468 on a defect. Shipped `rationale` is used only by `IF-141`, once in 135 rows. `trace.py` independently flags 27 Contract-argues and 30 over-ceiling rows.
4. Consumer duties: `IF-115`, `IF-124`, `IF-050`, and `IF-116` bind the reader; a provider header cannot carry F without another rule.
5. Missing target: CLI content points to committed, freshness-gated `docs/cli-reference.md`. The committed module map retired at WI-455. Symbols can be harvested on demand, but no successor artifact exists; relocation needs a generated reference and freshness gate, not only a docstring convention.

## blast_radius

SCOPE

The current row calls (a) zero-radius and registry-unchanged, and says every other option crosses the kit/instance line; its case for (d) instead says no kit change. See Findings.

Header options (b)/(c)/(e) affect shipped `PROCESS.md` §8, `interfaces.template.toml`, `INTERFACES.template.md`, `gen_arch_map.py`, `check_trajectory.py`, a new generated reference plus `check.py` freshness step and `docs/stack.ini [generated]` row, `tests/test_dogfood_sync.py`, and `RESYNC_PACK.md`. Every adopter inherits the OI-12/OI-13-precedent kit version bump.

MEASURED AUTHORING

- Up to 8,975 remainder characters/71 rows move. The anchor exists on 57 of 76 modules; the other 19 need `Contracts:`.
- 28,305 restatement characters are deleted wherever editing runs.
- 6,715 non-crossing characters need `rationale`, log, or deletion under every option, including (a).

OI-62 measured first to avoid authoring remainder twice. Remainder is 20.4%, not 12.3%: exposure is two-thirds larger, strengthening placement-first and enlarging the deferred edit.

NO RULING

All 108 rows retain 28,305 restatement characters and rot. `IF-055` has stale `SCHED_*`, caught by the tripwire; `IF-117` has three tripwire-invisible falsehoods: present tense for the module map retired at WI-455, the wrong `sym:` oracle, and 149 live LLR rows versus 184.

## options

(a) STAY IN-CELL; OI-62(b) LATER DELETES RESTATEMENT

FOR: Zero kit/adopter radius, artifact, or gate; 65.7% of rows have real content where readers look; one local pass.  
AGAINST: Settles the owner's question by default; content remains held to code by nobody (`IF-055`, `IF-117`); 12 requirement-owned Provides rows with remainder have no design row.

(b) RELOCATE REMAINDER; CELL KEEPS CROSSING + POINTER

Give `Contracts: IF-###` a structured body, generate/freshness-gate a committed reference.  
FOR: Beside-code declarations make rot self-correcting; WI-512 CLI is precedent; matches decompose-don't-paraphrase/generated-not-hand-maintained; 57/76 modules have the anchor.  
AGAINST: Largest every-adopter radius; OI-62 did not price the artifact/gate; no home for consumer duties or 15.3% non-crossing; the stated 21 pure-restatement rows move nothing, concentrating benefit on 71. See Findings for the count conflict.

(c) SPLIT BY FAMILY

Relocate Provides (21.2% remainder, 2.9% non-crossing; provider is module); retain Consumes when the far side is a file/external party.  
FOR: Fits the numbers, retains consumer duties with their row, and makes Provides a 19-row pass.  
AGAINST: Two rules; adopters must identify family; restores a Provides/Consumes convention WI-455 removed as a column.

(d) REMOVE NON-CROSSING; DEFER AND RE-ASK PLACEMENT

Move it to `rationale`/log.  
FOR: Removes 6,715 characters (15.3%) through an existing field used by `IF-141`, with no kit change; clarifies relocation; Contract-argues identifies 27 rows.  
AGAINST: Again defers the owner's question—OI-62 warned that "a measured number with no row to rule on is how a deferred question becomes a forgotten one"—and removes none of the 64.3% restatement.

(e) RELOCATE ONLY A (ARTIFACT) AND B (FAIL-LOUD)

Retain shapes, vocabularies, postures, and consumer duties in-cell.  
FOR: Modules can assert A/B about themselves; stale refusals are dangerous; smaller than (b), with no artifact if headers stay prose.  
AGAINST: Per-clause rules are hardest to teach/check, invite inconsistency, leave most content in-cell, and yield least benefit.

## recommendation

RECOMMEND (d), THEN RE-ASK; (c) IS THE STRONG SECOND.

The pilot did not generalize: 64.3% is not 87.7%; two in three rows carry real content. The pilot also had a uniform shape, one boundary, and an existing generated argparse home. Extending its answer to 108 rows is the extrapolation OI-62 warned against.

(d) first removes the unambiguous 15.3% about registry history/argument, not code or crossings. `rationale` already ships and is used once; no kit change, migration, or gate is needed, and the advisory enumerates much of it. Then placement is judged on relevant content. `IF-112` and `IF-107` are both about 470 characters, but one is a bug story and one a type-coercion fact; averaging them misleads.

Do not rule (b) yet: although it fits the owner's direction and doctrine, four rows carry consumer duties as their whole remainder with no provider destination, and WI-455 retired the module map without a generated, freshness-gated successor. It would choose a nonexistent mechanism where restatement is about a quarter below the pilot.

(a) is honest if adopter cost dominates, but preserves `IF-117`'s unowned-code rot; pair it with non-crossing cleanup. (c) best fits the numbers, but restores a family distinction WI-455 removed; WI-516 recovered it from git history, evidence it remains load-bearing. (e) is hardest to teach, easiest to vary, and buys least.

MEASUREMENT LIMIT

Remainder/non-crossing counts are judged clause spans, not post-edit lengths: accurate to the clause, not the character, because WI-516 could not edit. Exact rows: 108 read; 71 with remainder; 19 pure restatement; 18 zero-remainder at non-trivial length. The recommendation rests on row counts, not percentages.

## Findings

1. COUNT CONFLICT: option (b) in `docs/requirements/open-items.toml:2440` says 21 rows are pure restatement. The durable table, OI-63's measurement-limit paragraph, and a direct re-sum give 19 pure-restatement rows, plus 18 non-trivially long rows with zero remainder: 37 zero-remainder rows total. The draft preserves the current option's 21 and flags it; adjudication should choose the intended count before applying the draft.
2. RADIUS CONFLICT: `docs/requirements/open-items.toml:2431` says every option except (a) crosses the kit/instance line. Option (d) at line 2444 and the recommendation at line 2453 say (d) uses existing `rationale`/log machinery and needs no kit change. The draft preserves and exposes both claims rather than silently selecting one.

## Character counts

Counts include LF line breaks and exclude the labels above.

| cell | current | draft |
|---|---:|---:|
| `one_line` | 581 | 404 |
| `decision` | 4,451 | 3,034 |
| `blast_radius` | 2,313 | 1,334 |
| `options` | 4,383 | 2,116 |
| `recommendation` | 3,939 | 1,708 |
| **total** | **15,667** | **8,596 (54.9%)** |
