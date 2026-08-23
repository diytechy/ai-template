> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# Wrap-up plan — closing out the template

**Purpose.** A resumption guide for finishing this repo's open work in a later
session. Written 2026-07-25; revised 2026-07-26 after the WI-316 session — the
`Modified` re-attest marker landed, the first re-attest window is OPEN, and the
old §3/§4/§7 content (OI-4/OI-8 unruled; WI-300/272/273/278/065/062 open) is
all superseded: those are done, ruled, or retired. This revision replaces them
with the live wrap-up sequence.

**This file is a POINTER, not a source of truth.** [status.md](../../status.md) is the
forward-only working surface, [work-items.csv](../../work/) is the
authoritative registry, and [log.md](../../log.md) holds what shipped. Read those first;
this file only adds what they don't carry — a **sequencing recommendation** and a
**deferred-backlog review**. Where it disagrees with them, they win.

---

## 1. Where the repo actually stands

Read the generated block at the top of [status.md](../../status.md) for live numbers.
As of 2026-07-26 (branch `dualplan-routing-fix` @ `d09b8d0`, NOT pushed):
spine SN=25 SR=110 LLR=112 TC=115, `drafts=0`, **`modified=4`**.

**The derived gate reads DevBar-Tests DELIBERATELY — do not "fix" it.** This is the
WI-316 `Modified` re-attest window (canonical semantics: process.md §7), not a
regression: SR-049/052/053/054 carry `Status=Modified` (post-attestation
amendments awaiting the owner sitting), per-phase `1=DevBar-Tests;3=DevBar-Tests`. The sitting
flips each row `Modified`→`Verified` (bless) or →`Planned` (evidence
invalidated) in a reviewed commit and **DevBar-Release re-derives on its own** — no checker
edits. Sitting inputs, both committed: the generated pending block in
[open-items.html](../../open-items.html) (one line per Modified SR) and the before/after
brief [ratify/2026-07-26-reattest.md](../../ratify/2026-07-26-reattest.md)
(regenerate: `trace.py --ratify modified`; a pre-regime streak needs
`--since <rev>`). While the window is open the harness bar is the **DevBar-Tests bar**
(the DevBar-Release-only steps drop out) — don't let it sprawl.

The last full-suite run: **1557 passed, 7 skipped**; `check.py` at the derived
gate 5/6 PASS, the sole red the owner-parked `perceptual-stale` on SR-054
(§2). The `RE-ATTESTATION PENDING` commit-message convention is **retired** —
the marker is registry state now, the `--staged` hook warn polices the write
side, and `derive_gate`'s basis line counts it (`modified=N`).

**Environment note (still true):** until 2026-07-25 the DevBar-Release harness had never
been runnable on the owner's machine. Treat any pre-2026-07-25 "all passing"
claim as a partial run.

## 2. The perceptual gate: how it actually works (read this before touching gen_trajectory.py)

`check_trajectory --strict` has a fail-closed `perceptual-stale` finding: when
`gen_trajectory.py` (or `shoot.mjs`) changes **after** the latest
`docs/reviews/*-CRITIQUE.md`, any `Verification=Critique` SR (currently SR-052,
SR-053, SR-054) is judged stale and the gate reds at DevBar-Tests/DevBar-Release. This is **git-time-based
and mechanical** — it does not care who wrote the critique, only when.

**On "family-heterogeneous."** SR-084/SR-085's own text says a CRITIQUE session
should be "family-heterogeneous," and earlier notes in this file (and WI-273's old
`BlockRef`) hardened that into an absolute "Claude/Opus can never satisfy this."
**That was wrong.** `agent_route.py:50-53,608-653` states the actual contract:
family-heterogeneity is *preferred, not required* — "degraded availability is
legal... fresh context is the invariant." Nothing in `check_trajectory.py` or
`agent_dispatch.py` inspects which model produced a verdict file. So:

1. **A genuinely different (non-Anthropic) provider is still the stronger-
   corroboration path** per SR-084/SR-085 and worth reaching for when access
   allows — it earns real independence, not just fresh context.
2. **Absent that, a fresh, non-authoring-session Claude/Opus critique is a legal
   `DEGRADED` substitute.** SN-024's real invariant is "never the authoring
   session," not "never the same family." Dispatch it via a fresh subagent with
   NO access to the build session (isolated sandbox: rubric + SN/SR intent +
   rendered PNGs only — see the `render-dashboard-critique` skill and
   `docs/reviews/119-CRITIQUE.md`/`120-CRITIQUE.md` for the worked pattern), and
   **record it as `DEGRADED`** in the critique file — don't claim full
   heterogeneity, and don't refuse to dispatch just because no non-Anthropic
   model is available.

**The other way it clears for good:** WI-300's option (f) — decompose each
mechanizable rubric anchor into a child LLR+TC, so an SR drops `Verification=Critique`
entirely once its perceptual residue is empty. See §4.

⚠️ **Never revert a real fix, or sanction a check, to make either of these green.**

## 3. Open owner decisions (nobody else can make these)

Revised 2026-07-26. OI-4 (Apache-2.0) and OI-8 (hosted CI on every branch
push) are **ruled** — rulings in [log.md](../../log.md)'s Decisions. WI-273 is
**attested and integrated**. What remains:

| | Subject | State / recommendation |
|---|---|---|
| **Sitting** | Re-attest the `Modified` rows (§1) | **Recommended: hold ONE sitting at the END of the wrap-up sequence (§7)** — the render WIs in §4 will re-flip SR-054, and the phase-cadence rule batches spine work into a single sitting. SR-054's flip should FOLLOW the fresh critique (its `Verified` rests on critique evidence; blessing it while `perceptual-stale` is red is blessing stale evidence). SR-049/052/053 rest on green tests and could flip any time — but one sitting covers all. |
| **Queue scope** | The six queued WIs (§4) | Build (launch `agent-resume`), or defer/retire to shrink the wrap-up. Note the incentive: WI-305/306/307 fix exactly the anchors (T1/T2/T7) that failed 119-CRITIQUE — landing them is what makes the final critique's APPROVE plausible. |
| **OI-7** | WI-123 — review cadence | **RULED 2026-07-27** (Decisions log): keep per-slice review, **WI-123 `retired`**, spec archived. The owner ruled on the evidence this row recommended waiting for — per-slice adversarial review caught real defects on WI-297, WI-313, WI-316 and again across 124/125/126-REVIEW-A. No decision brief is pending now. |
| **WI-061/063** | Archive-anchored deferred rows | Re-specify against live homes or `retired`; low stakes, but a wrapped registry shouldn't carry specs pointing into the archive. |
| **Publish** | Push → CI → merge-to-`main` | `push-policy: human`. Safe order per the OI-8 ruling: push the branch FIRST, let hosted CI (Linux+Windows+macOS) run the first genuinely independent-environment validation this branch has ever had, then merge and push `main`. Separately: the unpushed `guardrails-fable-method` branch (WI-213/214) still awaits integrate-or-drop. |

## 4. The active queue

Six rows, generated order in status.md's **Ready frontier**:

- **WI-308** (quick, non-render) — triage the 22 dangling doc refs WI-062
  exposed, then wire `[step:doc-refs]` into `docs/stack.ini`. Independent of
  everything below; can land any time without re-redding the perceptual gate.
- **WI-305 / WI-306 / WI-307** (render) — the 119-CRITIQUE defects: no
  next-work surface in one tab switch (T1), the landing tab not
  start-collapsed (T2), SVG emitters not reflowing at declared widths (T7 —
  one mobile case, one desktop case). All touch `gen_trajectory.py`.
- **WI-314** (render) — bind SR-054's T6 theme-lock (mechanizable, residue
  none) per the option-(f) pattern.
- **WI-315** (render, gated behind WI-305) — bind T1's reworded operational
  bar; its spec demands the guard be proven against the rendered artifact with
  real registry data (the zero-active-rows fixture that fooled a structural
  check).

**Every render row will re-flip SR-054 `Modified` when it lands** (the
amend+flip same-commit rule) — expected, and why the sitting comes last (§7).

**The batching constraint (learned the hard way 2026-07-24 — do not replay
it):** if these run through the PARALLEL dispatcher, each render train
separately needs a CRITIQUE APPROVE at its reviewed head to integrate
(WI-243/WI-260, fail-closed), and APPROVE requires EVERY anchor — but
T1/T2/T7 only pass once ALL THREE defect fixes have landed. Three separate
trains therefore deadlock exactly the way WI-272/273 did (each held by
anchors it never touched). **Batch the render WIs into ONE train or one
attended session, and dispatch ONE critique after the last render commit.**

## 5. Deferred backlog — review, and actions taken 2026-07-25

> **Delta 2026-07-26:** everything below stands as the historical record; the
> live deltas since: WI-278/WI-062/WI-065 are **done** (no longer queued),
> OI-4/OI-8 are **ruled**, WI-097 is **done** (Apache-2.0 landed), and the
> WI-123 evidence now includes a third adversarial round (WI-316: 8 confirmed
> findings, 1 HIGH). The keep-deferred table is unchanged except WI-097 (done)
> and WI-123 (rule it — §3).
>
> **Delta 2026-07-27:** **OI-7 is ruled and WI-123 is `retired`** — keep
> per-slice review (Decisions log). The keep-deferred table's WI-123 row is
> spent: it is no longer deferred work awaiting a ruling, it is a closed
> question.

Reviewed 2026-07-25 (see the reasoning that drove each call below); **owner
acted on all four recommendations the same day** — WI-278/WI-062/WI-065 are now
`queued` (they appear in status.md's Ready frontier above) and WI-060 is
`retired`. The rest of the fourteen deferred rows are correctly parked as-is.

### Now queued

**WI-278 — branch integration & CI-on-branch.** *Why:* this session produced
decisive evidence. The local gate had a **total blind spot** — the entire
`agent_loop_*` layer (~104 tests) could not execute on this machine, and the DevBar-Release
harness had never run, concealing two failing steps including four
pre-existing duplicate blocks. Hosted CI on Linux + Windows would have caught
both immediately. The branch is also ~845 commits ahead of `main` with **no CI
on push** (`test.yml` fires only on `push: main` and `pull_request`). Highest
value-per-effort item in the repo — closes a class of blindness, not one
defect. **OI-8 (the underlying CI-strategy decision) is still NOT ruled** —
queuing the WI makes it buildable, but the owner should still bless the
approach (open a PR vs. add `on.push.branches` vs. merge in slices) before or
while it lands; see §3.

**WI-062 — `check_doc_refs` warn-first untraced-path tier.** *Why:* **562
dangling references** repo-wide today — pure noise, and noise is how a real
broken link hides. Tiering separates "illustrative placeholder path" from
"actually broken." Largest active noise source in the doc checks.

**WI-065 — active-seam TC citation, reconcile `trace`'s `Verifies` vocabulary.**
*Why:* it touches the **exact vocabulary WI-300's option (f) leans on** —
binding work (`Verifies: SR-xxx;LLR-xxx`) is actively being built on this
vocabulary right now (LLR-102..105/TC-105..108 landed just this session), so an
unreconciled vocabulary risks rework the more binding lands. Spec (archived at
close): [WI-065](../specs/WI-065.2026-07-25.md). **Landed 2026-07-25**,
ahead of the remaining U2/U4/A1/A3/A4 binding exactly as this recommended —
`Verifies` is the one ruled citation cell and `trace.py` now joins `IF-###`
tokens against `interfaces.csv`.

### Now retired

**WI-060 — coordinator working-tree stash/rollback between sessions.** *Why:*
it contradicted a settled design decision — the `session-protocol` skill states
the loop surfaces residue into the session prompt but "never auto-stashes —
the judgment is yours." WI-060 proposed automating exactly that. Retired
(not deleted) with the reason recorded in its `Deliverable` field, per the
repo's retire-don't-delete habit — if cross-session residue becomes a real
recurring pain, a successor WI should re-scope around surfacing +
human-directed cleanup, not automated rollback.

### Keep deferred (correctly parked)

| WI | Why it stays |
|---|---|
| **WI-097** | Owner ruling (OI-4), not queueable work. Blocks public release. |
| **WI-123** | Owner ruling (OI-7). |
| **WI-108** | Flaky test: **1 failure in 8 runs**, never reproduced, unforce-able even oversubscribed. Its spec correctly parks it until it recurs often enough to verify a fix against. Windows CI (WI-278) is the likeliest way to surface it. |
| **WI-271** | Warn-tier, non-gating, and its own spec says the warn still earns its keep. |
| **WI-277** | Genuinely hard-gated behind WI-280's seams stabilising. |
| **WI-280** | A deliberate design program, not a cleanup. See the note below. |
| **WI-061** | Mutating source-doc frontmatter is invasive for the value; flag-gated at best. |
| **WI-063** | No pain signal — no composite artifact has gone stale. |
| **WI-158** | Nice-to-have export; no demand. |
| **WI-187** | Large and design-heavy; overlaps WI-280's territory. |

**Evidence for OI-7 (WI-123) against relaxing review cadence.** An adversarial
review of WI-297 earlier this session's timeline refuted its headline claim and
found a **severe** defect (a children-presentational `role="img"` still sitting
over 9 focusable links — the exact bug the WI existed to fix), plus a
mis-measurement that made the reported numbers wrong. `trace.py` could confirm the
TC existed and named tests; **nothing mechanical could tell that its `Evidence`
described the artifact incorrectly.** Under option (f), a binding is only as
honest as the review that lands it. This session's own critique dispatches
(119/120) independently reconfirmed known findings and caught nothing spurious —
consistent evidence, not new evidence either way. Weigh both before reducing
review cadence.

**Note on WI-280.** The module-size ratchet fired again this session
(`gen_trajectory.py` 4632 → 4729, a reviewed bump for the new `_ring_ink`/
`_ring_style` helpers — see `tests/test_module_size_ratchet.py`'s comment trail for
the exact convention: state *why* right above the new baseline number, then bump
it). Not itself evidence for or against WI-280, but the ratchet's discipline
(reviewed bump vs. decompose) is working as designed.

## 6. Standing hazards for a new session

- **Always invoke `./.venv/bin/python`** — bare `python` is not on PATH.
- **Diagnose environment before code.** `./.venv/bin/python -m pytest -q
  tests/test_prereq_toolchain.py` — two failures plus a `!! TOOLCHAIN PREREQ` banner
  means the interpreter, not the branch.
- **`status.md` is forward-only and it is enforced.** A `done` WI id anywhere in
  its hand-authored prose (not just the obvious spots) WARNs at the commit bar,
  ERRORs under `--strict` at DevBar-Release. This bit twice this session — once for a `done`
  id in a sentence explaining *why* a row was still queued, once for a WI that had
  actually been closed in an *earlier* session and was still referenced as if
  open. Before writing status.md prose, check the WI's actual `Status` in the
  registry, don't assume from memory.
- **Closing a WI has a ritual:** `Status=done`, fill `Deliverable`, **clear
  `SpecRef`** (R-E), scrub the id from status.md's hand-authored prose (the
  generated block scrubs itself).
- **Editing `gen_trajectory.py` re-reds `perceptual-stale`** — it is path-triggered,
  independent of what you changed. Budget a critique with every render fix (see
  §2 for how to dispatch one without non-Anthropic access).
- **When adding a new per-node attribute to a shared SVG emitter** (`_drill_layer_svg`,
  `arch_icicle`, `dag_svg`, the knowledge-graph node loop), **append it last** in
  the attribute string. Existing tests assert adjacency between specific
  attributes (`data-tier="…" data-descend="…"`); inserting a new one in the middle
  breaks them even though the new attribute itself is unrelated.
- **Editing a declared list to clear a finding IS accepting what it measures.**
  Never reach for a coverage floor, an orphan glob or a ratchet baseline to green
  a step. (This entry used to name the duplication census as the worked example;
  the census was torn down 2026-08-11 — D-7/WI-426 — and the rule survives it.)
- **The runtime pin in `scripts/dev-setup.command` must be re-stamped** when the kit
  moves Python (currently 3.13.14). Nothing reminds you; the re-stamp command is in
  the file.
- **CSV registry edits: use Python's `csv` module, not sed/awk/text substitution.**
  These files have embedded commas and quoted multi-paragraph fields; a
  line-oriented edit risks corrupting an unrelated row. Read the target row's
  `Status` field before writing status.md prose about it (see the forward-only
  hazard above).
- **A `DEGRADED` same-family critique is legal — dispatch it rather than stalling**
  on "no non-Anthropic access." See §2. Still reach for a genuinely different
  provider first when one is available; record which you used.
- **Amend a spine row → flip it `Modified` in the SAME commit** (process.md §7;
  the `--staged` hook warn polices it, suppressed when the owning SR flips in
  the same staged set). The brief's default baseline walk DEPENDS on this rule
  — a streak that amended while `Verified` needs `--ratify modified --since
  <rev>`, and an unresolvable rev now hard-fails rather than fabricating.
- **A scripted CSV cell edit that introduces a comma into an UNQUOTED cell
  silently shifts every later column** — this bit SR-049 during WI-316
  (`Status` read `Test`). Re-parse the row with the `csv` module immediately
  after every scripted edit; grep is not a parse.
- **Judge the backlog-staleness warns POST-commit** — pre-commit, blame times
  come from the working tree at wall-clock now, and sub-second jitter re-fires
  warns that same-commit landings actually clear.
- **An open `Modified` window suppresses later chain-amendment warns for its
  SR** (review judgement J2) — the brief's baseline still captures them, but
  the write-time discipline is off for the duration. One more reason the
  window should be short.

## 7. Suggested order (revised 2026-07-26 — the wrap-up sequence)

The hard sequencing constraint: **the final critique must post-date the LAST
render-touching commit** (`perceptual-stale` is git-time-based — any later
`gen_trajectory.py`/`shoot.mjs` commit re-reds it, wasting the dispatch), and
**the sitting comes after the critique** (SR-054's flip blesses critique
evidence). WI-308 is the only queue row exempt — non-render, land it any time.

1. **Launch `agent-resume`** → WI-308, then the render set
   (WI-305 → WI-315, WI-306, WI-307, WI-314) **batched per §4's constraint**
   — one train or one attended session, no per-train critiques.
2. **Dispatch ONE render critique** against the last render commit (the
   `render-dashboard-critique` skill; §2's provider rules). This clears
   `perceptual-stale` — and with T1/T2/T7 fixed by step 1, APPROVE is the
   expected verdict for the first time.
3. **Hold the ONE owner sitting**: read the regenerated brief
   (`trace.py --ratify modified`; `--since` for the pre-regime streak), flip
   every `Modified` row →`Verified`/`Planned` in a reviewed commit. DevBar-Release
   re-derives all phases on its own.
4. **Run `check.py --gate DevBar-Release --jobs 0`** — the target is all-17 green with no
   parked red, for the first time with nothing waived.
5. ~~**Rule OI-7**~~ **done 2026-07-27** (WI-123 `retired`; no pending brief
   remains) — still owed: disposition **WI-061/063**, so the archive-anchored
   deferred rows go to zero too.
6. **Push the branch** → hosted CI validates on three OSes → **merge to
   `main`** and push. Decide `guardrails-fable-method` in the same sitting.

After step 6: 0 queued, 0 blocked, 0 `Modified`, open-items empty, gate DevBar-Release,
CI green on an independent machine — wrapped, in this repo's own terms.
