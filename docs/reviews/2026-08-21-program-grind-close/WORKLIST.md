# Consolidated worklist — 2026-08-21 program-grind close

Sources: ROUND-OPUS.md (2 CRITICAL / 13 MAJOR / 18 MINOR, mutation-proven) and
ROUND-SOL-RAW.md (1 CRITICAL / 8 MAJOR / 2 MINOR + full banked-findings
disposition). Deduplicated below; each item names its sources. Findings are
CLAIMS: the iterate worker confirms each against the tree before fixing (both
reviewers supplied repro steps — use them). Group-1 fixes must be PROVEN
against the review's own executed attacks, not just unit-tested.

## Group 1 — CRITICAL, fix first

- **W-1 (Opus C-1 = Sol 1). The recorded-correction verb's authority is a
  comment inside the file it guards.** Proven attacks: hand-typed record
  accepted; chained second correction accepted; nonexistent ruling (OI-999)
  accepted; second record silently erases the first from the parsed map.
  Fix all four arms: (a) the cited ruling must resolve to a `ruled` row in
  docs/requirements/open-items.toml whose text names the space; (b) the
  one-shot rule moves into `_mark_history_findings` (a space with a committed
  correction refuses another); (c) `read_corrections` appends rather than
  overwrites so a duplicate-space record is itself a finding; (d) each attack
  from the review table becomes a regression test that REDS on the pre-fix
  code.
- **W-2 (Opus C-2). WI-491 converted an explicit legacy `deny` into `ask`
  under a "fail-closed" subject.** On UNPARSEABLE, consult the legacy file
  and take the MORE RESTRICTIVE of (ask, legacy decision); correct the module
  docstring + RESYNC entry to say precisely what the arm does; rewrite the
  flipped test to pin deny-stays-deny and add the corrupt+no-legacy → ask
  case beside it. Re-verify with the real hook on a scaffold (both fixtures).

## Group 2 — MAJOR, mechanical fixes this iterate

- **W-3 (Opus M-3). Prose lines parse as Implements declarations.** Tighten
  `gen_arch_map.backlink_ids` to require the token to OPEN the line (only
  whitespace/comment markers/quote chars before it); reword the two
  check_trajectory.py docstring lines; regression test: a mid-line mention is
  not harvested, the 83 genuine tags still all parse (count unchanged).
- **W-4 (Sol 2 + Opus m-16). The seam-TC allowlist can grow silently.** Pin
  the seeded 120-id set in a test (exact set, not count); require
  ` — <reason>` on any entry beyond the seed (reader + hygiene enforce);
  hygiene reports growth vs the seed. Do NOT relitigate the seed itself
  (NR-1: honest).
- **W-5 (Sol 4 + Opus M-12). The SCC ratchet is blind to intra-SCC density.**
  Add an intra-SCC edge-count ratchet beside CYCLES (assert <=, re-stamp
  downward only), counting deferred/function-body edges. Mutation-verify: the
  review's planted `lane→dispatch` deferred edge must red it.
- **W-6 (Sol 6 + Opus m-27). The module-size census cannot see packages.**
  Make the census recursive, key baselines by path relative to scripts/,
  seed reviewed baselines for the five kitlib files, correct the docstring.
- **W-7 (Opus M-4/M-5/M-6 + Sol 7, factual half only). Smoke-tier honesty.**
  (a) Re-stamp `max-tests` at HEAD naming the WI-484..492 delta; fix the
  1282/1283 inconsistency and the false "+8/0.6% headroom" sentence.
  (b) Replace check_smoke_budget.py's (and test.yml's) stale "~7.5 s / ~5x
  headroom" justification with a dated 2026-08-21 multi-run re-measurement
  and re-argued wording — the budget VALUE does not move.
  (c) Annotate stack.ini's 46.97 s stamp as a single unreproduced outlier.
  (d) The policy question (60 s vs this box's 55–117 s spread; Sol's
  "enforce locally or redefine") is the OWNER's — record it as a queued
  ruling in the fragment/status, do not decide it.
- **W-8 (Opus M-7). byte-budget-guard SKILL.md's own baseline row is stale
  and its headroom claim false.** Re-stamp Baseline to measured bytes (all
  three tracked copies), correct "2–18%", add a test pinning each Capped-
  table Baseline cell to the file's real size.
- **W-9 (Opus M-8/M-9). Two product-floor tests are vacuous (mutation-
  proven).** Give the dedup test a fixture where a product step is tagged
  {DevStg-Reqs, DevStg-Tests} (appears once); give the two-axes test a
  non-empty `held` via the CANARY_PRODUCT profile shape. Both must red under
  the review's two mutations (dedup guard deleted; floor_plan → []).
- **W-10 (Opus M-10/M-11). The floor's live set is empty and two adopter
  docs overclaim it.** One corrective sentence in RESYNC_PACK.md §3 entry and
  PROCESS_OPTIONS.md naming the DevStg-Impl tagging + OI-51; correct OI-51's
  blast_radius sentence to "live only for a product step explicitly tagged
  DevStg-Tests; no shipped artifact produces one today".
- **W-11 (Opus M-13). The backlink dial docs still say 0.** Update
  README.md's dial cell and docs/enforcement-audit.md; add the README dial
  column to the existing dial-pin pattern in test_rule_sync.py if cheap.
- **W-12 (Opus M-14 + Sol's IF corroboration). Two seam readers disagree on
  `;`-joined endpoint cells (7 rows).** Split on `;` in
  `check_trajectory._declared_seam_pairs` to match trace.py; regression test
  with a multi-valued cell; verify the 14 unresolvable pairs become
  resolvable.
- **W-13 (Opus M-15 + m-17). Three self-referential Consumes rows
  (IF-025/026/045).** Re-author each to the real far side (for IF-045 the
  registry+enable-list readers measured today: agent_route AND dispatch.py's
  direct read — m-17's fan-out=1 claim is false; correct the note). Traced
  cells only; no status/owner changes.
- **W-14 (Sol 9 + Opus confirmation). `_findings_stub` is an unpinned mirror
  of `trace.exit_code`'s reads.** Build the stub from the real Findings
  type/defaults (or assert attribute-set parity with what exit_code reads).
- **W-15 (Sol 8). `spec_move.py` trailing-slash destination writes a FILE
  named like the lane dir.** Recognize directory intent (trailing slash or
  existing dir → append source filename); refuse ambiguous destinations
  loudly; regression test with the exact WI-448 invocation shape.

## Group 3 — MINOR sweep

- **W-16 (Opus m-19/m-20 = Sol 10). IF-070 and IF-072 counterpart
  corrections** (drop scripts/check; align IF-072 to its contract's real
  reader). **m-18**: add the one-sentence "measured over <surface>" note to
  IF-037.
- **W-17 (Opus m-22/m-23/m-25). Fragment factual repairs:** 27→26 wording;
  the duplication after-row gets its own rev (and note the HEAD value 484
  honestly); rewrite the banked watermark note to name B-08/REL-004 (the ids
  actually at risk) instead of B-06/B-07/EXT-004.
- **W-18 (Sol 11 + Opus m-24). Deferral-parse noise:** rephrase the three
  "none — OI-45/46/47 is fully executed" lines so no OI id sits on the
  declaration line; update the two older fragments' stale declarations
  (frontier-grind, owner-rulings) with a superseding note in the sanctioned
  grammar rather than deleting history.
- **W-19 (Opus m-28). Replace the source-text log-filename assertion with a
  behavioral test** (write a log, assert count + LOG_NAME parity).
- **W-20 (Opus m-29/m-30). Strengthen the dormancy pin** (assert
  `compute(docs)["ex_draft"] <= BAR_TESTS` on a fully-decomposed fixture;
  keep the constant pin) and either tighten `deferred >= 3` to a stamped
  count-window or comment why it stays loose.
- **W-21 (Opus m-31/m-32). `--gate` help documents the floor override;
  banner counts fail-open lines separately** (the ruling's actual target),
  keeping the total.
- **W-22 (Opus m-33). Regenerate docs/gate so the as-of stamp names the
  confirming commit.**

## Queued for the owner / future WIs — record, do not execute

- **Q-1 (Sol 3).** Collective-row backlink semantics (`Implements-part:` or
  facade-symbol convention) — shipped-grammar change, wants a design row.
  Opus NR-3 confirms current tags honest; this is about the claim's grain.
- **Q-2 (Sol 5).** B-05 conversions keep internal-consumer populations only
  in prose — a machine-readable consumer-set field is a registry-schema
  question for the wi455 lane / owner.
- **Q-3 (Sol 7 / Opus M-4).** The smoke budget policy question (see W-7d).
- **Q-4 (Opus m-26 + campaign skips).** Stale spine rows surfaced by the
  campaign (LLR-175/LLR-011 CodeSymbols; LLR-143/089/050/157/142/057/104/
  108/068/172-adjacent) — Approved rows, human-held; needs a batch amendment
  sitting or a WI-482-class repair row.
- **Q-5 (Opus m-21).** IF-056/IF-077's expired deferral rationale — give the
  49-citation-clause deletion pass a tracked home in the wi455 lane spec.
- **Q-6 (Opus suspicion).** The `external:git` endpoint convention vs
  EXT-001 dissolution — reader trap, wi455 lane's vocabulary to settle.

## Declined, with reasons

- Re-fixing the six B-05 conversions wholesale (Sol 5's suggested schema) —
  Q-2 owns the design; the rows are honest per their notes today.
- Moving the smoke budget or the 60 s value in any direction — owner's dial
  (both reviews agree the number itself was not to move).
- Editing OWNER-held Approved spine rows for m-26-class staleness — Q-4.
