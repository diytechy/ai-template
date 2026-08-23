+++
id = "WI-422"
title = "Measured dead-symbol sweep across project-trajectory/scripts: nothing in the kit catches an ORPHANED symbol. The module-size ratchet catches GROWTH (a module that gets bigger must argue for it), test_complexity_ratchet catches a function getting harder, and check_dupes catches a block getting copied - but a helper whose last caller left is invisible to all three, because deleting the caller made the module SMALLER, which every ratchet reads as an improvement. The 2026-08-08 mechanized-loop program retired several call paths (the gate-policy enum's four re-interpretation tables, the handback-into-queued shape, the three prompt string constants), so this sweep runs at a moment there is likely real residue. METHOD, and it must be MEASURED rather than eyeballed: take gen_arch_map.py's symbol inventory as the candidate set, grep every candidate across scripts/ + tests/ + the templates, and classify each zero-hit symbol as (a) genuinely dead - delete it, (b) a PUBLIC seam a downstream repo may call, in which case it is not dead and its docstring should say who calls it, or (c) reached dynamically (a getattr, a CLI subcommand table, a re-export). Class (b) is the reason this is a judgement and not a script: the kit's scripts are copied INTO other repos, so an unused-here symbol may be someone else's entry point. Deliver the classified inventory in the spec's Deliverable, not just the deletions. EXPLICITLY NOT a broad refactor: WI-390 forbids being built as a dead-code sweep and this row does not license one either - delete what is provably unreachable, record what is not, and stop."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**19 symbols deleted, 222 lines out of `project-trajectory/scripts`; 21 kept
with the reason recorded.** The classification below IS the deliverable — the
next sweep reads it instead of re-deriving the same judgements.

### The method, exactly as run (reproducible)

- **Candidate set:** `gen_arch_map.py`'s inventory rule — every module-level
  `FunctionDef` / `ClassDef` / `Assign`-to-`Name` in `project-trajectory/scripts/*.py`
  — widened once, deliberately, to include the `_`-prefixed symbols the arch
  map hides. A private helper is the *strongest* case the row describes: it can
  only be called from its own module, so zero intra-module hits is a proof, not
  an inference. **1,904 candidates.**
- **Corpus:** every text file in the repo except `.git`, `__pycache__`,
  `.venv` and `OWNER_SCRATCHPAD.md` — 1,984 files: `scripts/` + `tests/` + the
  templates + `docs/` + hooks + prompts + skills + the shell launchers.
- **Three passes, because the first two lie in opposite directions.**
  1. *Raw token grep* over the whole corpus. Zero-hit count: **0** — worthless,
     because `docs/architecture.md` is the GENERATED symbol index and names
     every public symbol, and `docs/spine-restructure-2026-08-08.md` §8 names
     the dead ones in a prose table. A grep that counts its own index as a
     consumer can never find anything.
  2. *`tokenize` NAME tokens only* (strings, comments and docstrings dropped),
     `.py` files only. Removes the prose false-negatives.
  3. *Same, with sibling DEFINITION lines discounted.* This is the pass that
     matters: three modules each defining `SPEC_EXAMPLE`, and three each
     defining `_sn_fields`, made every copy look "used by the other two". Pass 2
     missed all six for exactly that reason.
- **Consumer classes recorded per symbol:** own-module · other kit script ·
  `tests/` · other corpus file. Re-run to fixpoint after each deletion — which
  caught one real cascade (below).

The script is throwaway (it lives in the session scratchpad, not the kit): this
row bought a **judgement**, and mechanizing it needs `ruff F401`/vulture, which
`docs/dependencies.md` has no row for.

### Class (a) — genuinely dead, DELETED (19 symbols, −222 lines)

Two of these are F5 triplets, so the count of *distinct* dead ideas is 13.

| symbol | site | why it is dead |
|---|---|---|
| `_sn_fields` ×3 | `trace.py`, `traj_parse.py`, `gen_okf.py` | **The largest find (−108).** `df840a3b` (D-5 step 2d) collapsed the drifting SN-prose triplet onto `spine_carrier.folded` and left all three copies standing with no caller. Exactly the residue this row predicted from the carrier cutover. |
| `SPEC_EXAMPLE` ×3 | `check_trajectory.py`, `schedule.py`, `agent_common.py` | `"WI-000-"` copied into three modules and read by none. |
| `EXAMPLE_PREFIX` | `wi_convert.py` | **The cascade.** The fourth copy of the same literal; its only reader was `folder_is_authoritative`, so deleting that orphaned this. Found by re-running the sweep, not by eye. All four copies of the `-000` filename rule were inert — the live rule is the id-suffix test (`endswith("-000")`). |
| `folder_is_authoritative` | `wi_convert.py` | Answered "is the folder home authoritative yet?" — a question Phase 5 / RULING-4 closed by making the folder the only home. Its caller was rewritten out at `059a9705`. **Flagged below** as the one downstream-visible removal. |
| `prompt_text` | `bootstrap.py` | Free-text sibling of `prompt_choice` (10 callers). Born with no caller and never given one. |
| `_rev7` | `intake.py` | WI-416 took title-token authority off the disposition mint; the short-sha resolver stayed behind. The two surviving sites inline `str(rev)[:7]`. |
| `_by_id` | `schedule.py` | Born unused at WI-179; its twin `_status` two lines below is live. |
| `_norm_anchor` | `score_reviews.py` | `corroboration` inlines the same tuple. |
| `_field_value`, `_ONELINE_LABEL_RE`, `_RECO_LABEL_RE` | `traj_status.py` | Orphaned by WI-322. `_OI_ID_RE`, sitting between them, is live — the asymmetry is the whole tell. |
| `SEVERITIES` | `score_reviews.py` | `("BLOCKER","MAJOR","MINOR")`, never compared against: severity comes straight from `FINDING_RE`'s group, uppercased, unvalidated. **Finding, not fixed:** the vocabulary is documented and unenforced. |
| `SR_SURFACE_COLUMNS` | `plan_briefs.py` | The SR brief surface is a bullet list, not a table, so it never read the tuple; the IF twin `IF_SURFACE_COLUMNS` *is* read, which is why the asymmetry survived unnoticed. The redaction contract the tuple carried was **moved into `_sr_surface`'s docstring**, not dropped. |
| `KNOWN_STATUSES` | `check_trajectory.py` | Zero readers. `OPEN_STATUSES` and `TERMINAL_STATUSES`, immediately above it, are the live vocabulary and reconstruct it exactly. |
| `_NUL` | `check_vendored.py` | The **refuted** heuristic's constant: `looks_text`'s docstring records 130-REVIEW-A proving a NUL test wrong (a PPM with no NUL collided two byte-distinct images) and replaces it with positive UTF-8 identification. The refutation landed; the constant did not leave with it. |

Nothing else changed: no behaviour edit, no signature change, no test deleted.
**Test delta: 0** — full suite `2206 passed, 5 skipped` before and after, so no
deletion was paid for by removing its own guard.

### Class (b) — NOT dead: public seams, and reserved-by-ruling

| symbol(s) | why it stays |
|---|---|
| `check_trajectory.normative_text`, `sn_normative_text`, `digest`, `current_digests`, `_DIGEST_SEP`, `_DIGEST_EXCLUDED` | **RESERVED BY RULING**, not unused: the attestation anchor's ENGINE with deliberately **no writer yet** — D-1 landed the removal half (`attestations.csv` gone) and the on-row `TextHash`/`HashedOn` writer is built after the sitting (repo-lock §2 D-1, §5 step 1). `current_digests` measures as test-only; the others as own-module + test. **The pointer is now IN THE CODE** (`current_digests`'s docstring), so the next sweep does not have to reach repo-lock to be safe. |
| `lane.run_worker` | **Zero callers anywhere — and kept.** LLR-150's `code_symbol` names it (`Status = Verified`), so deleting it is a spine amendment, i.e. sitting territory. Its docstring now says who calls it — see the finding below, because what it *used* to say was false. |
| `spine_carrier.rows_from_csv` + the carrier-aware baseline reads | Deliberate dead weight with a **declared expiry** (repo-lock D-5). Reachable via `rows_from_text`; recorded here so a future sweep does not mistake "deliberate" for "forgotten". |
| `migrate_carrier.py`'s surface | Provisional scaffolding (IF-103) shipped to adopters — every symbol is a public seam by construction. Its one comment naming `traj_parse._sn_fields` was repointed to `spine_carrier.folded`. |
| `bootstrap.py` entry points; hook-invoked checkers | `bootstrap.py` runs *before* the kit is copied and the hook checkers run standalone, so "no in-tree caller" is their normal state, not a signal. |

### Class (c) — reached dynamically or re-exported

| mechanism | symbols |
|---|---|
| **Re-export block** (`agent_loop.py:175-243`, whose header declares it "agent_loop's public surface (tests, downstream imports, monkeypatch targets)") | 43 names rebound from `agent_common` / `agent_session` / `plan_runner`. Three measure as unconsumed *through the re-export*: `head_sha_full` (zero either side), `pause_reason`, `regenerate_index` (test-only). Deleting a member of a declared compatibility surface because this repo does not use it is the class-(b) mistake in re-export clothing. |
| **Re-export, F5-pinned** | `check_trajectory._spine_stem` and `trace._spine_stem`, both `= spine_carrier.stem`; `tests/test_rule_sync.py` pins them equal. |
| **Dispatch table** | `adjudicate_brief._ASSEMBLERS` / `ROUTED` (brief kind → assembler); `prompts.py`'s `{"list": _cmd_list, "check": _cmd_check}[args.cmd]` — both reached by string key, invisible to a call-graph grep. |

### Class (d) — the shape the row did not name: consumer is its OWN TEST

Not zero-hit, so **not deleted** — a symbol with a passing test is reachable.
But it is the exact silhouette the row's argument describes (the production
caller left, the test stayed), so it is recorded rather than dropped. 18 rows;
the ones whose reason is *not* already class (b)/(c):

- `check_trajectory.cell_integrity_errors` — **already documented as
  deliberate**: `tests/test_trajectory_specs.py:98-118` records that `main()`
  stopped calling it when the CSV WI home retired at Phase 5, and that it
  "survives for the spine CSVs, whose rows ARE lines". **Finding:** D-5 moved
  the spine to TOML, so that stated reason now rests on the CSV fallback's
  declared-expiry window. When the window closes, this function's justification
  closes with it — re-examine it there, not here.
- `plan_artifacts.WI_HEADER`, `schedule.load_rows` — the retired CSV registry's
  schema and reader, surviving as legacy interchange (`wi_convert`'s stated
  role) and as F5 sync anchors.
- `derive_gate.stage_to_gate` — declares itself "a reader's reconciliation, not
  a second source of truth"; nothing deriving from it is the *point*.
- `gen_open_items.theme_tokens` — a drift guard's parser; its only legitimate
  consumer IS a test (122-REVIEW-A: a fixture-fed value would prove nothing).
- `spine_carrier.SPINE_TIER_KEYS` — the schema of record both the template and
  the live registry are checked against; `test_dogfood_sync` is its consumer by
  design.
- `spine_carrier.need_ids`, `score_reviews.latest_phase_verdicts`,
  `trace._toml_rows_text`, `check_trajectory.SPINE_RATIFIED_CELLS`,
  `adjudicate_brief.ROUTED`, `agent_common.pause_reason` /
  `regenerate_index` (+ their `agent_loop` re-exports),
  `check_trajectory.current_digests`, `check_trajectory._spine_stem`,
  `trace._spine_stem` — covered by (b)/(c) above.

### Findings, filed rather than fixed

1. **`lane.run_worker`'s docstring was FALSE, and so is LLR-150's `detail`.**
   Both said it is "the dispatcher's default when no test injects a worker
   callable". `dispatch._launch`'s `worker is None` branch calls
   `lane.spawn_worker` (non-blocking, so N lanes overlap — §A4.3's whole
   point); `run_worker` is called by nothing. The **docstring is corrected**
   (a comment edit, safe); **LLR-150's `detail` cell is NOT** — amending a
   `Verified` spine row is the sitting's act, and this row has no licence for
   it. The row still names the symbol correctly, so the seam is real; only its
   stated caller is wrong.
2. **One downstream-visible removal: `wi_convert.folder_is_authoritative`.**
   It is a *public* function of a script the kit ships. Nothing in the kit,
   the docs, `interfaces.csv` or any LLR names it, and the question it answers
   was closed by ruling — so it fails the class-(b) test on its own terms
   (a seam whose docstring cannot say who calls it is not a seam). Recorded
   here because an adopter who imported it would need a one-line migration.
3. **Two vocabularies were documented-but-unenforced**, and deleting the
   constant removed the *appearance* of enforcement without changing behaviour:
   `score_reviews` severities, and `plan_briefs`' SR redaction columns. The
   second's contract was preserved as prose on `_sr_surface`. Mechanizing
   either is its own row, not this one.
4. **The census the row's title named as a non-catcher is gone** (D-7, WI-426)
   — and this sweep confirms the row's premise held: **13 distinct dead ideas
   survived every live ratchet**, because every one of them made its module
   *smaller*, which the module-size ratchet reads as an improvement. Five
   baselines were re-stamped DOWN in the same commit as the deletions.

### Same-commit obligations, discharged

`tests/test_module_size_ratchet.py` re-stamped **down** for `trace.py`
(3439→3401), `check_trajectory.py` (3907→3901, the −14 plus the +8 D-1
pointer), `bootstrap.py` (2735→2723), `agent_common.py` (2450→2446),
`intake.py` (1669→1661), each with its reason inline. Arch map, OKF export,
derived gate, dashboard, status block and open-items regenerated by
`trunk_step.py` in the same commit.

Measured on the working tree at `897c171a` + this change:

- `2206 passed, 5 skipped in 351.40s` — unchanged from baseline, so the
  deletions cost no test.
  <!-- fig: cmd="python -m pytest -q -n auto" rev=897c171a -->
- `orphans=0 integrity=0`
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev=897c171a -->
- `0 broken` of 1,100 intra-repo links
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root . --stale" rev=897c171a -->
- `17 dangling` — **identical before and after**, measured by stashing the
  change and re-running, so the sweep added no doc rot.
  <!-- fig: cmd="python project-trajectory/scripts/check_doc_refs.py --root . --strict" rev=897c171a -->
- `1904` candidates over `1984` corpus files; `19` deleted, `21` kept with a
  recorded reason.
  <!-- fig: derived="gen_arch_map inventory rule over project-trajectory/scripts/*.py, widened to private module-level symbols; consumer counts from tokenize NAME tokens with sibling definition lines discounted" -->


## Context

Plan §9's first cleanup finding, verified when the plan was written: there is no
existing WI for unused functions. The queued set at that time was WI-000
(exemplar), 390, 413, 415, 416, 417, 418, and WI-390 *explicitly forbids* being
built as a dead-code sweep.

Why it is worth doing NOW rather than whenever: the SN-028..032 program
deliberately retired several call paths in one pass. A sweep is cheapest right
after a retirement and least useful long after one, because that is when the
residue is both largest and still explicable — the person reading a zero-hit
symbol can still tell whether it died last week or was always a public seam.

The classification is the deliverable. A list of deletions with no record of
what was KEPT and why leaves the next sweep to re-derive the same judgements
from scratch.

**2026-08-11 (WI-426, repo-lock D-7).** This row's title lists three ratchets
that catch adjacent failures and argues a dead symbol slips past all of them.
One of the three is gone: the duplication census (`check_dupes.py`) was torn
down by owner ruling, along with its census file and the spine chain
`SR-039 → LLR-036 → TC-039`. **The row's argument is unaffected and arguably
stronger** — the premise was that no existing check sees an orphaned symbol, and
the census was named only as one of the three that does not. Read the title's
third clause as history. The two live ratchets (the module-size ratchet,
`test_complexity_ratchet`) still bound growth and complexity, and
`gen_arch_map.py`'s symbol inventory — the candidate set this row's METHOD
starts from — is untouched by the teardown.
