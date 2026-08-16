# Re-tier v2 — the one-decision tiering model (rulings recorded; execution NOT started)

**For the owner and the executing sessions.** Branch: `infra/mechanized-loop`.
Ruled in session 2026-08-15 (log `2026-08-15p`), grown out of the owner's
grounding question on 2.7(a) (log `2026-08-15o`). Program row: `WI-464`.
Nothing in this plan has executed; every slice below is overturnable at its
own review.

---

## 1. The rulings (owner, in session, 2026-08-15)

1. **R1 — one decision per row, one home per method (the owner's wording).**
   A single interface/method is fully defined by exactly one requirement, and
   a requirement calls out at most one method/action. Exceptions are
   extraordinarily rare and ride the existing 13v valve (a stated per-row
   reason); the corpus's two standing waivers (SR-140, SR-147) are the
   expected census.
2. **R2 — no artifact-establishing rows; requirement cells never name a
   concrete artifact.** SUPERSEDES sitting-1 ruling 2.7(a)'s license. SRs
   speak in delivered-capability or artifact-CLASS voice ("the delivered
   harness", "launchers at the repository root", "the shipped reference CI
   workflow"); a concrete filename appears only in the ACCEPTANCE cell as
   current-carrier evidence ("read off the current carrier / declaration
   sites, as the current set: …" — the SR-157/SR-158 pattern, rewritable
   without moving the shall). The three binding homes that make this lossless:
   the shipped-file inventory (SR-163/SN-038 — why a file ships), the LLR
   `module` cell (who implements), the IF registry (what seam it stands on).
3. **R3 — a fan-out advisory on SR→LLR children.** Warn-first, declared bound
   (default **7** direct LLR children per SR), re-stampable per row with a
   stated reason — the TOP_VIEW_MAX / smoke-budget family, never a hard cap
   (a hard cap invites merging LLRs to slip under it). The warn is a DETECTOR
   for R1 violations: today's seven offenders are precisely the merged
   "one delivered contract" rows.
4. **R4 — the IF registry's end-state schema (ruled direction; wi455
   executes the removals).** `owner` stays id-typed and points at design tier
   wherever a design row exists (the owner's stated expectation; F6's
   IF-004/IF-031 precedent). A **consumers/endpoints list** carries the
   coverage declarations, with value grammar module-or-path-or-`external:`.
   Then: `direction` DIES (flow derives from owner-side vs consumer-side;
   Q2 already ruled Consumes rows are coverage, not ownership);
   `this_project` DIES once derivable as owner→LLR→`module` (advisory on
   disagreement first, cell dropped at wi455 per the schema's existing HELD
   note); `counterpart` TRANSFORMS into the consumers/endpoint list — it
   cannot be deleted, because 45 of 122 counterparts are non-module facts
   (B2, now measured). One artifact binding, stated once, at the LLR module
   cell.
5. **Sequencing — v2 runs BEFORE the sitting signs and seeds** (owner ruling
   at this plan's mint). The amendment window stays open, rows v2 touches
   re-enter the regenerated brief, and ONE sitting blesses everything — the
   2026-08-14e one-sequence precedent. The seed (birth of drift detection)
   deliberately waits.
6. **Attestation.** v2 may amend rows that are not `Modified` — the owner's
   explicit sanction at this plan's mint ("it might touch rows that aren't in
   a modified state — and that's okay"), extending the 2026-08-15 ruling that
   overriding a historical attest is fine where it improves the design. Every
   such touch is NAMED in the log entry of the slice that makes it, never
   ridden in quietly.

## 2. The measured basis

Fan-out (SR→direct LLR children): 48 of 60 SRs have children; 39 of 48 carry
≤5; seven exceed 7 — SR-070 (16), SR-157 (15), SR-156 (13), SR-155 (11),
SR-148 (10), SR-054 (9), SR-053 (8).
<!-- fig: cmd="python - # tomllib over docs/requirements/low-level-requirements.toml + system-requirements.toml: count sr_refs per SR" rev=7fd5b940 -->

IF registry (122 rows): `owner` = SR on 114, LLR on 8; `this_project`
derivable from the owner-LLR's module on ~4 of the 8 today (the derivability
case REQUIRES the owner re-point pass first); `counterpart` kinds: 77 module,
31 registry/file path, 13 `external:`, 1 other → **45 non-module facts**, the
B2 blocker quantified; `direction`: 42 Provides / 80 Consumes.
<!-- fig: cmd="python - # tomllib over docs/requirements/interfaces.toml + low-level-requirements.toml: owner tier, endpoint derivability, counterpart kinds" rev=7fd5b940 -->

Voice precedents already in the corpus: behavior voice (SR-157/158/159/162),
artifact-class voice (SR-160 launchers, SR-151 shipped workflow), the
current-carrier acceptance pattern (SR-157's "as the current set", SR-167
post-`2026-08-15o`).

## 3. Execution slices (each ends at the commit bar; full suite at slice close)

- **S1 — the rules land in prose, once.** The tiering rules join the process
  master at their one home (PROCESS.md §-stable; overflow to
  PROCESS_OPTIONS.md), 2.7(a)'s supersession recorded; byte budgets checked
  before/after (`byte-budget-guard`). The enforcement-audit gains the rows.
- **S2 — the two advisories, warn-first.** (a) The artifact-naming census:
  a `*.py` token in an SR requirement cell is a finding unless the rationale
  carries a stated 13v reason; >1 SR naming one artifact is a finding naming
  the rows. (b) The fan-out bound: declared value (default 7), per-row
  re-stamp with reason. Both in trace_text (the advisory pipe, never the
  exit code), both tested, both listed in the enforcement audit. This closes
  the recorded "2.7(a) has no executable form" gap.
- **S3 — the HOLDS-bundle reword.** The census's 34 HOLDS rows
  (docs/plans/2026-08-14-wi451-slice1-sr-census.md §1) re-read under R2;
  rows whose requirement cells name concrete artifacts re-word to
  capability/artifact-class voice, concrete names moving to acceptance as
  current carriers; clauses that are method contracts (the SR-006/SR-007
  shape) shed to LLRs under the surviving row. Every touched non-Modified
  row named in the log per ruling 6.
- **S4 — the offender splits.** The seven >7 fan-out rows re-read under R1;
  each either splits by observable class or takes a recorded per-row
  re-stamp with its reason. No filler tiers, no pseudo-SRs.
- **S5 — the folded sitting-desk items** (one window, one brief): the L1
  pair call executed as ruled (SR-151+SR-152 together or not at all — the
  owner rules which at the sitting if not before), TC-123's retired-vocabulary
  method cell, LLR-014.sr_refs + TC-014.verifies gaining SR-167, and the
  IF owner re-point pass toward design-tier rows (R4's precondition; the
  `this_project` disagreement advisory lands with it).
- **S6 — settle and hand to the sitting.** Regenerate everything (brief, OKF,
  dashboards, gate), run the second top-down read on the settled layer, take
  the cross-family adversarial round AFTER the settle (the WI-451 lesson: a
  round is spent by the next commit), then the ONE sitting: read the brief
  (including any ex-`Planned` rows v2 did not touch — the `2026-08-15m` list
  still owes the deliberate read), sign, seed, step 7 arms.

## 4. Deliberately NOT in scope

- Executing the IF field removals — `direction`/`this_project` deletion and
  the counterpart→consumers transform are **wi455's** (the schema's HELD note
  already names it as evidence-and-removal owner). v2 delivers the ruling,
  the owner re-point, and the disagreement advisory; wi455 executes.
- WI-448 (common-module inversion) — code consolidation, disjoint from
  registry tiering; no shared rows.
- Any `Status`, `approval` or attestation flip as an act of its own — flips
  happen only as the mechanical consequence of amending a row's text, and
  the sitting signs them.
- The schema inversion (dead, `2026-08-15` interface plan §2) stays dead;
  R4 is not it — no column moves to the SR tier.

## 5. Preconditions (clear before S3 opens)

1. **WI-463** — strict-clean `check_trajectory` (quick). **CLEARED
   2026-08-16 (`b5c4d22d`, log `2026-08-16a`).**
2. **WI-462** — the MAX_PATH xdist deaths (quick). **CLEARED 2026-08-16
   (`525357f8`).**
3. **WI-461** — the CRLF-relay conviction red (P2, medium). **CLEARED
   2026-08-16 (`01018dcc`): the oracle was right, the fixture was blind
   (system `core.autocrlf`), and the full suite is honestly green on this
   box — 2541/13/0, log `2026-08-16a`.**
4. S1+S2 land before S3 so the rewording sessions run WITH the advisories
   that police them. **OPEN — this is now v2's first act.**
