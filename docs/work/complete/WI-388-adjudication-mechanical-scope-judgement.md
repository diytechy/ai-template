+++
id = "WI-388"
title = "RULED 2026-07-31 (docs/concurrency-v2.md §A5.2) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. Add the ADJUDICATION kind: the step that makes WI-380's narrowed detector SAFE. Narrowing the amendment detector without this would only move the mis-fires from spurious window to MISSED window, so the two are a pair. MINTING IS DETERMINISTIC AND NEEDS NO MODEL (owner, 2026-07-31: a detected scope change is mechanical, and the WI can be created with a derived description so it does not require an LLM at all to create the initial structure and force in a WI that must be attended to). A trunk commit changing a RATIFIED cell of a Verified spine row causes the dispatcher to write docs/work/queued/WI-NNN-adjudicate-<rows>.md in a bookkeeping commit (docs/work/ is already an allowed RULING-6 prefix), carrying safety_class = adjudication (exclusive, rank 1 per WI-383), an empty blockref because it is WORK and not a decision brief, and a Deliverable body listing each changed row, cell and before/after - all derived from the diff staged_spine_findings already computes. ADJUDICATION RUNS NO BAR: its only outputs are (a) flipping Modified rows back to Verified when the change was grammar, clarity, or a re-point that did not move scope, or (b) filing real WIs - a spine WI for the actual scope change, plus cancellations or re-scopes of queued WIs whose premise moved. It touches Status cells and the work registry, nothing a product bar can speak to, which is why the kind needs its own no-bar arm. SN-Refs and Verifies changes route HERE rather than arming a window (the WI-380 ruling), because whether a re-point moved scope is exactly the judgement this kind exists to make. ABSORBS WI-385 ENTIRELY (that row is retired): re-evaluating the backlog after a re-attest - verify whether current work items in queue need adjustment or cancellation - is the same judgement, made by the same agent, with the diff already in front of it; a separate git-derived warn would be a second and strictly weaker reader of one fact, able only to say re-read this where the adjudicator can cancel the row, re-scope it, or file its replacement. One behaviour, one home. ID ALLOCATION MATTERS HERE and is why WI-384 must land: WI-NNN must be max(existing)+1 over EVERY spec in docs/work/, which only holds if every folder holding a spec is a declared status directory - and this is a mint that runs with nobody watching. GATE-POLICY BEHAVIOUR IS RULED (owner decision 2, 2026-07-31): RECOMMEND-ONLY UNDER `attended`, FLIP UNDER `single-ratify` AND `autonomous`. Flipping Modified->Verified is a Status change that RECOVERS THE GATE, and under attended a ratification is the human's act - so at that level adjudication writes its judgement into the WI and the open-items card and stops, and the owner still sits but with a PREPARED BRIEF (these 19 cells are traced-only, no scope moved, recommend re-verify) instead of a bare Modified count, which is most of the win this row exists for. At the other two levels it flips directly, since at those levels an LLM verdict already carries ratification authority. This matters for ADOPTERS even though it cannot bite here: attended is the kit default while this repo runs autonomous, so a flip-always build would ship a path never exercised at the default level - build and test BOTH arms. Last in the sequence: the only row needing both the narrowed detector (WI-380) and the dispatcher (WI-381). RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written. INTAKE FROM WI-380 (2026-08-01, its REVIEW-A finding 3): TWO CELLS ARE LEFT UNCLASSIFIED AND ARE THIS ROW'S TO RULE - LLR `SR-Refs` and SR `SupersededBy`. Both are live columns that the §A5.1 table does not name. WI-380 left them RATIFIED, which is the fail-safe reading (its residual rule is that an unclassified column arms the warn, so a new column can only ever be too loud, never silently un-ratified) and deliberately NOT a narrowing past what the owner ruled. But the §A5 principle - traceability is TRACED - arguably reaches LLR `SR-Refs`, which is the same shape of pointer as the ruled-traced `SN-Refs` and `Verifies`, and re-pointing an LLR at a different owning SR is exactly the moved-scope-or-not judgement this row exists to make. Rule both cells here: either confirm ratified (and say why the pointer differs from `SN-Refs`), or move `SR-Refs` to traced and route it to adjudication like its two siblings. `SupersededBy` is likely to stay ratified - a supersession IS a scope statement - but it should be ruled rather than left to the residual. WI-380 delivered the seam: `check_trajectory.staged_spine_amendments(root, base, head)` returns per-row `{ratified, traced}` cell dicts with before/after, and takes the rev pair, so this row's post-commit trunk trigger (§A5.2) is expressible as `staged_spine_amendments(root, '<before>', '<after>')` without re-opening that scan; only the `SN-Refs`/`Verifies` subset of `traced` is a WI-388 case today, the rest being silent by ruling. AMENDED 2026-08-01 (owner session - R3 ruled + the context sweep; log.md Decisions this date). (1) THE MINT GENERALIZES to ONE helper with THREE triggers, all trunk-side at intake, serial by construction: a ratified-cell diff on the merged commit (the original trigger, via staged_spine_amendments(root, before, after)); a merged spec carrying a `## Handback` section, which mints the DISPOSITION row - same adjudication kind, rank 1, outcomes cancel / defer / re-queue with drafted follow-up / surface an open item, and it may NEVER itself hand back (the no-recursion invariant); and the empty-frontier gap census handed over by the dispatcher (WI-381's ladder rung 1: unverified in-scope SRs, orphan rows, draft SNs - what trace.py already names - become concrete gap-closure rows with derived descriptions). THE INVARIANT THIS SEALS: a WI id is created ONLY by a human trunk commit or this helper - lanes never mint, R1 absolute, no carve-outs. Consequently the phrase 'filing real WIs' above EXECUTES AS DRAFTS: the adjudication row writes follow-ups into its own spec body (a Dispositions section) and intake mints them at its merge - an in-lane mint would trip WI-397's rung at this row's own merge slot. (2) TIER SIGNALS: the mint sets buildtier from measurable inputs (rows touched, gate delta, handback reason class); deeper review is reached by a drafted follow-up carrying planmode = dual - never by a second kind, and 'arbiter' is not used as a kind name (taken by the dual-plan arbiter). (3) THE `bar` KEY: an optional frontmatter key bar = G1|G2|G3 the lane's refresh passes to check.py --gate, so a row claimed to deliver evidence at a level still bars at that level if docs/gate moves mid-flight. Schema note verbatim: bar declares verification strictness for this row's lane; it never affects scheduling. The three F5-mirrored loader tables (wi_convert.py / check_trajectory.py / schedule.py) gain the column together, pinned by test_wi_loader_sync. (4) THE CONTEXT BLOCK: one function context_block(wi_row) built from pure registry joins, clipped like pred_block, advisory-never-gating, three consumers - written into every minted row's body at mint (minted rows have no spec author); computed fresh in worker_prompt at claim for every WI, with one new prompt line (read your Context refs before starting); and warn-first on hand-authored specs whose rows' components declare knowledge packs the spec never cites. Content order by failure cost: cancelled/ precedent sharing sr_refs WITH ITS REASONS first (prevents re-proposing the refuted - the measured WI-391 failure mode), then pending OIs whose WI-Refs intersect self/predecessors/siblings (premise risk), then the LLR/TC decomposition rows with their Module/CodeSymbol/TestRefs code map, then LLR.Component -> CMP.Knowledge packs, IF seams via LLR.Module, and docs/reviews/ entries of precedent rows. Excluded BY DESIGN: docs/status.md (not a resume surface, WI-210), the OKF bundle (generated copy - workers read its sources), implementer self-assessments (review independence)."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
needs = ["WI-380", "WI-381"]
+++

## Deliverable

Shipped 2026-08-02, five commits (900dac6a, b4e7cd0b, d0131ce6, 082dc25a,
d5805460), every clause of the amended title built:

- **The kind**: `adjudication` in `schedule.SAFETY_CLASSES` — exclusive,
  rank 1 (the reserved §A1 slot, no renumbering), NO product bar: the
  refresh's `_lane_bar_directives`/`_refresh_bar` no-bar arm still commits a
  verified `Bar-Green` attestation whose summary reads
  `no-bar (adjudication, §A5.2)`; mixed batches fail toward the bar.
- **The unified mint**: the new kit sibling
  `project-trajectory/scripts/intake.py` — R1/R3 sealed (a WI id is created
  only by a human trunk commit or this helper; id = max+1 over every spec
  filename under docs/work/). Trigger (a) ratified/ROUTED-cell diff via
  `staged_spine_amendments(root, before, after)` at `integrate_one`'s
  post-merge arm (in-slot, serial); trigger (b) the handback DISPOSITION row
  with the R3 outcome vocabulary verbatim in its title and the no-recursion
  invariant structural at both ends (`handback._no_recursion_refusal` + the
  intake's own refusal); trigger (c) the dispatcher's rung-1 census handed to
  `mint_gap_rows` — mint, keep driving, dedupe (loop-proof), honest
  exhausted banner. Drafts-not-mints: `## Dispositions` fenced-TOML drafts
  minted at the row's OWN merge, loudly validated. Tier signals measurable
  (rows touched, gate delta, handback reason class); recovery CLI
  `intake.py sweep|census|adjudicate`, idempotent by exact-title dedup.
- **The `bar` key**: G1|G2|G3 → `check.py --gate` at the refresh (strictest
  of the batch; malformed refuses); schema note verbatim in every loader
  table — bar declares verification strictness for this row's lane; it never
  affects scheduling — landed across wi_convert / the three F5 reader copies
  / plan_artifacts / the shipped template header together
  (test_wi_loader_sync + header pins).
- **The context block**: `context_block(root, wi_row)` — cancelled precedent
  WITH REASONS, pending OIs, the LLR/TC code map, CMP knowledge packs, IF
  seams, precedent reviews; advisory-never-gating, clipped like pred_block;
  consumers: minted bodies at mint, `worker_prompt` fresh at claim (one new
  instruction line), and the warn-only pack-citation check
  (`knowledge_pack_findings`; zero warns on the live registry, measured).
- **The gate-policy arms** (ruled decision 2): recommend-only under
  attended (prepared brief, registries untouched), flip under
  single-ratify/autonomous (`flip_verified` — only the named Status cells
  move, cell-exact elsewhere, idempotent); unknown levels fail toward
  recommend. Both arms tested.
- **The two unclassified cells, RULED**: LLR `SR-Refs` → traced, routed to
  adjudication like `SN-Refs`/`Verifies`; SR `SupersededBy` → ratified,
  confirmed — recorded at the cell-split table's home in
  check_trajectory.py, pinned by tests, disclosed in the log entry this
  date.
- **Registration**: LLR-152..154 + TC-146..148 (CMP-004, SR-093/SR-132),
  IF-090/091 with the Contracts ids on the one line the harvester reads,
  bootstrap MAPPING + kit-contents + test_bootstrap rows for intake.py, size
  stamps with reasons (integrate 2353, check_trajectory 3531, agent_common
  1839, agent_loop 3007, bootstrap 2278), dupes census re-stamped (+ the
  intake-mint class), smoke max-tests 660→700.

REVIEW-A rework (2026-08-02, CHANGES-REQUESTED findings=5, all closed;
docs/reviews/WI-388-REVIEW-A.md): (1) the no-bar arm gained its DIFF-SCOPE
RUNG — `_adjudication_scope_ok`: the branch's non-refresh delta must stay on
the §A5.2 surfaces (docs/work/, the three spine CSVs, open-items.csv,
docs/gate, docs/log.d/, docs/reviews/, + the declared [generated] set) or
the FULL bar runs; the reviewer's product-file + red-harness drive is now
the shipped regression, red-then-green both ways. (2) the intake→wi_convert
cross-CMP seam declared (IF-092, the IF-078 shape; Contracts line updated) —
post-regen `check_trajectory --strict` rc=0 on a scratch copy, warn list
byte-identical to the trunk baseline (11). (3) the disposition title carries
the handback merge's sha, so a re-queued row's second handback mints its own
disposition (two-handback sequence driven red-then-green). (4) TC-147/148
Verifies cite IF-091/IF-090. (5) the smoke-budget figure re-measured under
its own rev pin (669 collected at 81147e33).

Watched 2026-08-02 (pre-rework close): full suite 1959 passed / 5 skipped (0:05:14)
<!-- fig: cmd="python -m pytest -q -n auto" rev=d5805460 -->
post-rework: full suite 1961 passed / 5 skipped (0:05:18)
<!-- fig: cmd="python -m pytest -q -n auto" rev=81147e33 -->
smoke 667 passed / 2 skipped
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=81147e33 -->
trace/check_trajectory/check_doc_refs/check_figures all rc=0 under --strict;
derive_gate --check rc=0. Full detail, the deviations (including the
TC-144 Method amendment this row's own merge is expected to adjudicate), and
the cell-ruling disclosure: the log entry of this date.
