# WI-388 — REVIEW-A (2026-08-02)

Verdict: CHANGES-REQUESTED — the mint's id discipline, all-or-nothing shape,
idempotency, the no-recursion invariant, the `bar` key, the context block and
both gate-policy arms all reproduce under my own scratch attack drives, and
the two cell rulings are judged sound. Two MAJOR findings block: (1) the
no-bar arm has no diff-scope guard, and I drove a product-code change with a
RED declared bar through an adjudication-only lane onto trunk with the check
harness never invoked — an un-run green, the exact fixed point §A8 says
survives every level; (2) the branch as shipped cannot pass its own merge
refresh — the moment `trunk_step --regen` folds `scripts/intake` into the
arch map, `check_trajectory --strict` exits 1 on an undeclared cross-component
import (intake CMP-004 → wi_convert CMP-005), and the bar runs `--strict` at
the live G3 gate. Three MINOR findings follow. The adjudication judgements
this charter delegates are recorded below; since this verdict is not an
APPROVE, they are prepared briefs for the re-review round — the ratification
rides the eventual APPROVE.

Reviewed: branch `wi-388-adjudication-mechanical-scope-judgement` at
`76c3d704` (six commits walked in order: `900dac6a` kind+schema+rulings,
`b4e7cd0b` intake.py, `d0131ce6` context block, `082dc25a` policy arms,
`d5805460` registration, `76c3d704` close); merge-base/claim `aabff213`;
trunk `ConcurrencyTrainRewrite`. All commands under the worktree's
`.venv/bin/python`. Per the brief: `docs/log.d/` was not read, and the full
unfiltered suite was not re-driven (the Deliverable's watched 1959 passed /
5 skipped is taken as the builder's claim). My tier: module suites, smoke,
strict checks, and the scratch drives below
(`test_wi388_review_drive.py`, 13 drives, all passing as written).

## Hunt 1 — the mint's id discipline, driven

**max+1 over everything.** The shipped
`test_the_id_is_max_plus_one_over_every_status_directory` covers
draft/queued/deferred/cancelled/complete/active-branch; my drive extends it
to an UNDECLARED residue folder (`docs/work/residue-not-a-status/WI-020-…` →
`next_wi_id` answers `WI-021`), which `next_wi_id`'s `rglob` makes true by
construction ("for a MINT, an id held anywhere is an id taken",
intake.py:127-140). Two triggers firing in one intake (an SR amendment + a
handback) mint sequential ids in ONE bookkeeping commit — my drive asserts
`["WI-006", "WI-007"]` and exactly one commit past the pre-mint head. No
collision, no skip.

**All-or-nothing.** Injected a `ConvertError` on the SECOND spec write of a
two-draft mint: refusal returned, `HEAD` unchanged (no half-minted commit),
`git status --porcelain` empty (trunk restored clean). The
regen/write-tree/commit-tree failure arms all route through the same
`restore()` (intake.py:768-774). A hard kill mid-mint leaves an uncommitted
dirty tree that the queue's clean-trunk rung refuses loudly on the next run —
recoverable, never silent.

**Idempotency.** Exact-title dedup reproduces (shipped rerun tests + my
drives). A NEAR-duplicate title (one char differs) is NOT wrongly deduped —
it mints, as it must. Probe result worth recording: two DISTINCT census lines
sharing a ≥139-char prefix clip to the SAME derived title (`_LINE_CLIP` 140)
and both still mint on the first pass (no intra-batch dedup), so nothing is
lost; on a rerun both dedupe against the identical titles. Edge-of-edge, not
filed. The amendment title carries its sha pair, so distinct merges never
collide. But see finding 3: the DISPOSITION title carries no such
event-distinguishing token.

## Hunt 2 — no recursion, both ends and a third path

Both ends refuse, structurally: `handback._no_recursion_refusal`
(handback.py:220-240, read off the TRUNK claim; shipped
`test_a_disposition_rows_own_handback_is_refused_structurally` asserts
"never hands back" + "R3" and the claim not moved), and the intake end
(intake.py:498-508 mints NOTHING for a handed-back adjudication row; shipped
`test_a_handed_back_adjudication_row_mints_no_second_disposition`). Third
path hunted and closed: a `## Dispositions` draft declaring
`safety_class = "adjudication"` is a REFUSAL with nothing minted
(intake.py:586-591, shipped test), and the deeper-review route
`planmode = "dual"` derives the `high-risk` kind — my drive pins
`schedule.kind_of({"safetyclass": "", "planmode": "dual"}) == "high-risk"`,
exclusive, never a second adjudication row and never handback-capable-free.
A dual draft beside a contradicting declared class also refuses
(intake.py:596-601).

## Hunt 3 — the no-bar arm (finding 1, MAJOR)

The stated behaviour reproduces: an adjudication-only lane's refresh runs
`trunk_step` only, commits a verified `Bar-Green` whose summary reads
`no-bar (adjudication, §A5.2)` (shipped `test_an_adjudication_lane_runs_no_bar`
asserts `_order(wt) == ["trunk_step"]`), and a mixed batch fails TOWARD the
bar (`test_a_mixed_claim_still_runs_the_bar`), as does unreadable frontmatter
(integrate.py:1427 returns `False, None, None`).

**But the ruled premise — "its outputs are Status cells and the work
registry, nothing a product bar can speak to" — is enforced nowhere.** My
drive `test_MAJOR_probe_product_code_red_bar_merges_unbarred_on_adjudication_lane`:
`station_repo(check_src=STUB_CHECK_RED, safety="adjudication")` — the lane
carries a product file (`wi-401.txt`) and a check harness that FAILS if
invoked. The refresh reports green (`no-bar`), `integrate_one` merges, and
`git ls-tree HEAD` shows the product file on trunk with the check stub never
having run. That is an un-run green reaching trunk, against §A8's fixed
points ("**no un-run greens**; the harness is still the bar" — fixed points
that "survive every level and the dispatcher must not paper over them"). The
only remaining guard is the RULING-7 verdict gate — one LLM APPROVE at the
kit's scaffolded `review-policy` 1, dialable to 0 — the weaker enforcer by
this repo's own enforcement-audit hierarchy, guarding the one lane class that
runs with no harness at all.

## Hunt 4 — the `bar` key

`schedule.load_wis` (schedule.py:449-481) structurally never reads `Bar` —
no key touches it; my mutation drive builds the same row with and without
`bar = "G3"` and asserts the scheduler dict AND `classify()` output are
identical (the loader row itself carries `Bar: "G3"`, so the column is not
silently dropped either). The key reaches `check.py --gate` off the
recording stub's OWN argv (shipped `test_the_bar_key_reaches_check_gate`:
`--gate` immediately followed by `G2`); an undeclared key passes no `--gate`;
a malformed value refuses the refresh naming it (`bar` + `G9` in the
refusal), and refuses at the disposition MINT too (my drive: `bar = "G9"` in
a draft → refusal carrying `G9`, nothing minted). The schema note is
verbatim in all five loader homes plus the shipped template header, pinned
by `test_wi_loader_sync` (my suite run: green).

## Hunt 5 — the context block

Joins verified against real registries: the shipped ordering test pins all
six sections in failure-cost order (cancelled precedent WITH REASONS <
pending OIs < LLR/TC code map < knowledge packs < IF seams < precedent
reviews). Poison drive: `open-items.csv`/`components.csv`/`interfaces.csv`
overwritten with NUL bytes, a lone `"` and truncated headers — the block
answers a string, never raises (`context_block`'s `except Exception → ""`,
intake.py:206-209), and the MINT never half-commits: on a genuinely broken
registry the regen step is honestly RED, the refusal says "trunk restored",
`HEAD` is unchanged and the porcelain is clean (driven). The
`worker_prompt` line is present ("read the Context refs below before
starting", agent_loop.py:470-474; shipped test also proves the bare-repo arm
renders NO dangling header). `knowledge_pack_findings` is warn-only outside
the exit code even under `--strict` (check_trajectory.py:3444-3455) and the
live registry carries ZERO pack warns (grep of the strict stderr: 0).

## Hunt 6 — the policy arms

Attended: recommend, registries byte-untouched (shipped test compares
`read_bytes` before/after). Flip: cell-exact — shipped test proves every
non-Status cell of every row unchanged; my drive goes further on the LIVE
registries: copied this repo's real SR/LLR/TC CSVs into a scratch repo,
flagged one row `Modified`, flipped under `autonomous`, and the flipped file
is **byte-identical to the original live registry** (and the untouched
registries byte-identical to pre-flip) — the "quoting is all by necessity"
claim measured true. Unknown id refuses whole; unknown level answers
`recommend` (`adjudication_action` defaults away from machine ratification,
intake.py:886). The policy is read from `docs/gate-policy`'s one home, never
passed by hand.

## Hunt 7 — the cell rulings, adjudicated (prepared briefs; the act rides the eventual APPROVE)

**LLR `SR-Refs` → TRACED, routed: JUDGED SOUND.** The owner's §A5 principle
("traceability — the Module pointer and its kin — is traced, not ratified")
reaches it: it is the same shape of pointer as the ruled-traced
`SN-Refs`/`Verifies` (chain edges, re-pointing changes no attested prose on
either side), and question C's confirmed routing — a re-point is exactly the
moved-scope-or-not judgement adjudication exists to make, with the same
asymmetric cost — transfers whole. The spec's amended title named this exact
arm as one of the two permitted outcomes. Recorded at the cell-split table's
home (check_trajectory.py:2697-2711, `SR-Refs` moved out of
`SPINE_RATIFIED_CELLS`), pinned by
`test_the_two_wi388_cell_rulings_are_recorded_in_the_split`, and the
behaviour actually changed: an SR-Refs re-point is SILENT at
`staged_spine_findings` (driven by the shipped
`test_staged_llr_sr_refs_repoint_is_traced_not_a_reattest_warn`) while the
adjudication trigger FIRES on it
(`test_a_routed_traced_repoint_mints_and_a_silent_traced_edit_does_not`,
which also proves a Module-only move stays silent).

**SR `SupersededBy` → RATIFIED, confirmed: JUDGED SOUND.** A supersession
terminates a requirement's lifecycle in favour of another — a scope
statement under the owner's own definition, unlike the three pointers it
ends a chain rather than re-pointing one, and a silent supersession would be
a missed window nobody sees. Confirming the residual changes no behaviour —
the fail-safe direction.

**The TC-144 no-flip amendment, adjudicated.** `staged_spine_amendments`
over the branch range (`aabff213..HEAD`) returns EXACTLY one record:

    id=TC-144 registry=docs/test/test-cases.csv
      RATIFIED Method: 'Run the dispatch loop suite…' -> 'Run the dispatch loop suite…'

— precisely the disclosed record, nothing else (the three new LLR + three
new TC rows are silent at the seam by design). Judgement: NO SCOPE MOVED — a
test-method description caught up with ruled behaviour (the empty-frontier
ladder now HANDS the census to the intake mint rather than reporting it
inert), Level/Tier/Expected untouched. **Dogfood expectation verified by
dry-run**: `intake._routed_amendments(root, aabff213, HEAD)` returns 1 and
`_amendment_drafts` yields the adjudication draft
(`adjudicate: TC-144 - ratified/routed cell(s) amended on merged trunk
aabff21..HEAD (§A5.2)…`, buildtier medium, kind adjudication) — the intake
trigger WILL fire at this branch's own merge, exactly as the registration
commit predicted.

## Hunt 8 — mechanical

- Module suites, my run: `243 passed in 8.70s` (intake/schedule/loader-sync/
  wi_convert/staged/agent_loop_worker/trajectory_arch/plan_artifacts) and
  `228 passed in 49.38s` (integrate/handback/dispatch/dupes-census/
  size-ratchet/bootstrap).
- Smoke, my run: `666 passed, 2 skipped in 12.15s` — byte-matches the close
  commit's claim.
- Strict at the committed tree: `trace --strict rc=0`,
  `check_trajectory --strict rc=0`, `check_doc_refs --strict rc=0`,
  `check_figures --strict rc=0` ("68 declared figure(s), every one carrying
  its command and revision"), `derive_gate --check rc=0`. Figure spot-check:
  the close's smoke figure (666/2) reproduced exactly. BUT see finding 2 —
  strict does NOT survive the arch-map regen the merge will perform — and
  finding 5 on the smoke-budget figure.
- Arch-map regen on a scratch copy: the harvester DOES read intake's
  docstring line — the regenerated section carries
  `Contracts (interfaces): IF-090, IF-091` — and the two
  no-docstring-declaration WARNs clear; the cross-CMP ERROR and the two
  no-TC-citation WARNs appear (findings 2 and 4). Trunk-copy baseline after
  the same regen: `strict rc=0` — the red is this WI's alone.
- `ruff check`: "All checks passed!"; `ruff format --check`: 156 files
  already formatted.
- `docs/work` delta over the branch: exactly one entry — `R068` of the
  WI-388 spec `active/… → complete/`. WI-388-only.
- R-A/R-F: strict rc=0 covers R-A; the completed spec carries zero `specref`
  lines (R-F). The `docs/gate` basis moved LLR 134→137 / TC 131→134 with
  value G3 unchanged, as-of `d5805460` — coherent with the three new rows.
- Registration/ratchet/dupes/bootstrap coherent via their suites (size
  stamps each carry a reason at the entry; the IF-087 requote the
  registration commit made is CELL-exact — parsed before/after fields
  identical). Smoke-budget raise 660→700 argued at the entry (headroom
  rationale) — but see finding 5.

## Findings

1. **MAJOR — a product-code diff merges unbarred under `kind=adjudication`;
   the no-bar arm needs a diff-scope guard.** Driven live (Hunt 3): a
   product file plus a check harness that fails if invoked rode an
   adjudication-only lane to trunk — refresh green
   (`no-bar (adjudication, §A5.2)`), `integrate_one` merged, the check stub
   never executed. §A5.2's premise ("it touches Status cells and the work
   registry, nothing a product bar can speak to") is asserted by prose only;
   §A8's fixed points ("no un-run greens; the harness is still the bar")
   hold at every level and this arm breaks them for arbitrary lane content.
   The remaining guard is one LLM verdict (review-policy, scaffolded 1,
   dialable 0) — the weaker enforcer guarding the only lane class with no
   harness at all. Fix shape: `_lane_bar_directives` honours `skip` only
   when the branch's merge-base..tip delta touches nothing outside the
   registry/bookkeeping surfaces (`docs/work/`, the spine CSVs, `docs/gate`,
   the declared generated set, `docs/reviews/`, `docs/log.d/`); any other
   path fails TOWARD the bar — the same branch-delta read
   `_minted_id_refusal` already makes at the same slot.

2. **MAJOR — undeclared cross-component seam `scripts/intake` (CMP-004) →
   `scripts/wi_convert` (CMP-005); the branch reds its own merge refresh.**
   Invisible at the committed (pre-intake) arch map — which is what every
   green above was measured against — but the refresh's `trunk_step --regen`
   regenerates `docs/architecture.md`, and on that tree
   `check_trajectory --strict` exits 1: "cross-component import
   scripts/intake (CMP-004) -> scripts/wi_convert (CMP-005) has no declared
   IF-### seam". `check.py` appends `--strict` to the trajectory step at
   G2/G3 (check.py:479-481) and `docs/gate` is G3, so the branch's own
   refresh bar is RED at merge time; trunk-copy baseline after the same
   regen is rc=0. One-row fix: a Consumes IF row for the
   `write_spec_file`/`COLUMNS` seam (IF-078, plan_artifacts → wi_convert, is
   the exact precedent shape) — or a membership retag.

3. **MINOR — a repeat handback of the same WI silently mints no second
   disposition row.** The disposition title (intake.py:511-515) derives from
   `wi_id` + relpath only — no event-distinguishing token (the amendment
   title carries its sha pair) — and the dedup surface is every row
   including terminal ones. So after dispose → re-queue → second handback,
   the exact-title dedup eats the second disposition: the R3 flow ("the
   dispatcher completes the disposition") degrades to an open-items blocked
   card with nobody owed the judgement. Salt the title with the handback
   merge's sha (or count prior dispositions) so each RETURN event mints.

4. **MINOR — IF-090/IF-091 ship two new permanent strict WARNs.** Declared
   `Status=Active` but no TC `Verifies` cell cites either id, so
   "IF IF-090/091 is Active but cited by no TC" joins the live output (17 vs
   trunk's 13 warns today; these two persist after the arch-map regen).
   TC-147/TC-148 genuinely drive both seams — cite the ids in their
   Verifies cells (or align Status with the IF-086..089 siblings).

5. **MINOR — the smoke-budget figure disagrees with its own rev pin.**
   `docs/stack.ini` argues "700 keeps ~6% headroom over the measured 661"
   above `fig: cmd="python -m pytest -q -n auto -m smoke --collect-only"
   rev=d5805460`, but the collect at that tree is 668 (666 passed + 2
   skipped; reproduced). The budget holds (~4.8% headroom); the prose number
   is stale against the rev the close commit pinned it to.

VERDICT: CHANGES-REQUESTED findings=5

---

# Round 2 — the remedy (2026-08-02, same reviewer)

Judging ONLY the two rework commits (`81147e33` scope rung + disposition
event token; `fcf8b2be` IF-092 seam + Verifies citations + honest figure).
All five round-1 findings verify closed under my own re-drives; one new
MINOR finding (6) is recorded against the finding-3 remedy's recovery-CLI
edge — bounded, visible, non-blocking. The APPROVE below carries the three
adjudication acts round 1 prepared.

## Finding 1 (MAJOR) — CLOSED, and the rung survives attack

**My round-1 fixture, re-driven against the shipped rung**: the SAME
product-file + red-harness adjudication lane now RUNS the bar
(`check-red` recorded in the stub order) and the refresh refuses —
"the bar is RED on the refreshed tree"; `_merge_ready` answers not-ready,
`integrate_one` refuses (the in-slot pessimistic refresh reds the same way),
trunk never moves and the product file never reaches it (driven:
`test_ROUND2_product_code_red_bar_now_refuses_on_adjudication_lane`). The
complement holds: a pure registry-shape lane (spec move + a spine Status
edit, no product path) keeps the no-bar path with the honest
`no-bar (adjudication, §A5.2)` attestation (driven). The builder also kept
my fixture as the shipped regression
(`test_a_product_touching_adjudication_lane_fails_toward_the_bar`).

**The rung itself, attacked.** The matcher
(`_adjudication_scope_ok`, integrate.py) is exact-match for file entries and
prefix-match ONLY for `/`-terminated entries, over `git diff --name-only
--no-renames` output (which is always root-canonical — a `docs/work/../…`
traversal is unrepresentable in that listing; git stores canonical paths).
Hostile shapes driven, all failing TOWARD the bar: a file literally named
`docs/gate2` and a `docs/reviewsx.md` sibling both red the refresh with the
harness having RUN; the unit matrix pins `docs/gate` ok / `docs/gate2` no,
`docs/work/queued/x.md` ok / `docs/workx/…` no, `docs/reviews/…` ok /
`docs/reviewsx.md` no, `scripts/evil.py` no, and the declared [generated]
key `PROJECT_STATE.html` ok. `_generated_paths` reads the TRUNK's stack.ini
(root, not the branch), so a lane cannot widen its own allowance without
touching `docs/stack.ini` — which is not on the list and forces the bar.
Unreadable git answers False (toward the bar).

*Observation, not a finding*: this repo's `[generated]` set includes
`tests/test_module_size_ratchet.py` and `docs/dupes-allow` (stamp files), so
an adjudication lane could re-stamp a ratchet baseline un-barred. This is
the same trust class RULING-6 already grants those keys on non-merge trunk
commits (the mint's own bookkeeping commit included), stamp honesty was
never the bar's rule (a raised baseline passes its own bar in any lane —
the reviewer owns stamp honesty), and the edit is visible in the merge
diff. Recorded so the next reader knows the bound was seen, not missed.

## Finding 2 (MAJOR) — CLOSED, verified by regen parity

IF-092 declares the seam (Consumes, scripts/intake → scripts/wi_convert,
the IF-078 precedent shape; `Stable,Stable`, so it arms no Active-seam
warn), and intake.py's one Contracts line now carries all three ids. My
re-run of the round-1 experiment: scratch copy of THIS tree, arch-map
regenerated (`### \`scripts/intake\`` present with
`Contracts (interfaces): IF-090, IF-091, IF-092`), then
`check_trajectory --strict` **rc=0** with **11 WARNs**; the trunk baseline
regenerated the same way is rc=0 with 11 WARNs and the two warn lists are
**byte-identical** (diff empty) — which is simultaneously finding 4's
proof: TC-147 cites IF-091 and TC-148 cites IF-090 in their `Verifies`
cells (both suites genuinely drive those seams), and the two
Active-but-uncited warns are gone. The TC-147/148 `Verifies` edits are new
rows on this branch, so they are silent at the amendment seam by
construction — verified: the dogfood dry-run below still returns exactly
one record.

## Finding 3 (MINOR) — CLOSED as specified; one new edge (finding 6)

Driven: two handbacks of the same WI at two merge shas mint TWO
dispositions with distinct ids, each title carrying its event sha
(`…handed-back-at-a84a5cf…` / `…handed-back-at-6907032…`), and a re-run of
the SAME second event dedupes to nothing
(`test_ROUND2_two_handbacks_two_dispositions_then_dedupe`; the builder's
`test_a_second_handback_of_the_same_row_mints_a_second_disposition` pins
the same red-then-green).

## Finding 4 (MINOR) — CLOSED (see finding 2: warn parity byte-identical).

## Finding 5 (MINOR) — CLOSED

`docs/stack.ini` now reads "700 keeps ~4.6% headroom over the measured 669"
with `fig: … rev=81147e33`; my collect at the tip (docs-only commits since)
answers exactly `669/1966 tests collected`. The integrate.py ratchet
re-stamp (2353 → 2417) carries its reason at the entry, naming the scope
rung.

## Finding 6 (MINOR, NEW — the remedy's recovery-CLI edge; non-blocking)

The event token defeats the dedupe for the BARE sweep: `_cmd_sweep`
defaults before/after to symbolic `HEAD`, and `_rev7` resolves the CURRENT
head — which differs from the original handback merge's sha as soon as
anything lands (the mint's own bookkeeping commit already moves it). Driven
(`test_ROUND2_finding6_probe_bare_sweep_re_mints_a_disposed_handback`): the
slot mints the disposition at sha1; a bare re-sweep while the returned spec
still carries `## Handback` (it keeps the section through a defer or
re-queue outcome) mints a DUPLICATE disposition under the new head token.
Bounded: only the by-hand recovery CLI reaches it (the slot path is scoped
by the merged branch's own outcomes; a sweep re-run with the SAME
`--before/--after` is idempotent — shipped test), and the failure shape is
a visible extra queued row, cancellable, never a silent loss. Fix
direction: derive the handback token from the RETURN event itself (e.g.
`git log -1 --format=%h -- <returned spec relpath>`) rather than from
`after`, so the slot and any sweep name one event one way — or dedupe the
handback arm on an OPEN disposition for `(wi_id, relpath)`.

## Round-2 measurements

- Module suites: `244 passed in 9.33s` (intake/schedule/loader-sync/
  wi_convert/staged/agent_loop_worker/trajectory_arch/plan_artifacts) and
  `229 passed in 50.03s` (integrate/handback/dispatch/dupes-census/
  size-ratchet/bootstrap).
- Smoke: `667 passed, 2 skipped in 14.98s`; collect `669/1966`.
- Strict at the tip: trace rc=0, check_trajectory rc=0, check_doc_refs
  rc=0, check_figures rc=0 ("69 declared figure(s), every one carrying its
  command and revision"), derive_gate --check rc=0. `ruff check`: "All
  checks passed!"; `ruff format --check`: 156 files already formatted.
- Scratch regen parity: branch copy strict rc=0 / 11 WARNs; trunk copy
  strict rc=0 / 11 WARNs; warn lists byte-identical.
- `docs/work` delta across the rework: the WI-388 spec's own Deliverable
  rework record only.
- My drive suite: 18 tests, all passing as written (the round-1 MAJOR probe
  inverted to the remedy expectation, plus the rung attacks, the
  two-handback sequence, and the finding-6 probe).

## The adjudication acts, taken

This APPROVE carries the three acts the round-1 briefs prepared:

1. **LLR `SR-Refs` → TRACED, routed to adjudication — RATIFIED.** The §A5
   principle and the question-C precedent transfer whole; the behaviour is
   driven both ways (warn silent, mint fires; Module-only silent) and the
   ruling is recorded at the cell-split table's home, test-pinned.
2. **SR `SupersededBy` → RATIFIED, confirmed — RATIFIED.** A supersession
   is a scope statement (terminates a lifecycle); confirming the residual
   is the fail-safe direction and changes no behaviour.
3. **TC-144's Method amendment — adjudicated NO SCOPE MOVED.**
   `staged_spine_amendments` over `aabff213..HEAD` at the rework tip still
   returns exactly one record (TC-144, ratified `Method`, nothing else —
   the TC-147/148 Verifies edits are new-row-silent as disclosed), and the
   intake trigger verified live to fire at this branch's merge
   (`_amendment_drafts` yields the `adjudicate: TC-144 …` adjudication
   draft). The Method text caught up with ruled behaviour (the census now
   handed to the mint); Level/Tier/Expected unmoved; the row's Status
   rightly never flipped. The adjudication row this merge mints should
   close as no-scope-moved, per this act.

VERDICT: APPROVE findings=6
