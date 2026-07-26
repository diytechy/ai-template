# Wrap-up plan — closing out the template

**Purpose.** A resumption guide for finishing this repo's open work in a later
session. Written 2026-07-25; revised same day after a session that dispatched
two fresh critiques and closed WI-292/294/295/299.

**This file is a POINTER, not a source of truth.** [status.md](status.md) is the
forward-only working surface, [work-items.csv](requirements/work-items.csv) is the
authoritative registry, and [log.md](log.md) holds what shipped. Read those first;
this file only adds what they don't carry — a **sequencing recommendation** and a
**deferred-backlog review**. Where it disagrees with them, they win.

---

## 1. Where the repo actually stands

Read the generated block at the top of [status.md](status.md) for live numbers. As
of writing: derived gate **G3**, spine SN=25 SR=110 LLR=105 TC=108, `drafts=0`.

**`check.py --gate G3 --jobs 0` is currently green — RESULT: PASS, all 17 steps** —
full suite 1502 passed / 6 skipped, 92.15% coverage. This is a fresh green, not a
standing one: it will **re-red the moment `gen_trajectory.py` changes again** (see
§2) — which WI-300, WI-272, WI-305, WI-306, and WI-307 all do. Don't be surprised
by it; budget a re-critique with the next render-touching commit.

**Environment note (still true):** until 2026-07-25 the G3 harness had never been
runnable on the owner's machine (`.venv` was Python 3.9.6, below the kit's own 3.11
floor). That is fixed. Treat any pre-2026-07-25 "all passing" claim with that
caveat — it was a *partial* run.

## 2. The perceptual gate: how it actually works (read this before touching gen_trajectory.py)

`check_trajectory --strict` has a fail-closed `perceptual-stale` finding: when
`gen_trajectory.py` (or `shoot.mjs`) changes **after** the latest
`docs/reviews/*-CRITIQUE.md`, any `Verification=Critique` SR (currently SR-052,
SR-053, SR-054) is judged stale and the gate reds at G2/G3. This is **git-time-based
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

Unchanged this session — still open, still need the owner:

| | Subject | State |
|---|---|---|
| **OI-4** | WI-097 — LICENSE + public/private intent | No recommendation possible; needs your intent first. **Blocks any public release** (review finding H-3). |
| **OI-7** | WI-123 — review cadence | Recommendation: wait for evidence. Per-slice review just caught a real defect this session (see §5) — that's evidence *against* relaxing, if anything. |
| **OI-8** | WI-278 — branch integration & CI-on-branch | **Not yet ruled** — recommendation is open a PR. WI-278 is now `queued` (2026-07-25) so the build is ready to go, but the owner should still bless the approach before/while it lands. |

Full briefs: [open-items.md](open-items.md).

## 4. The active queue

Generated order lives in status.md's **Ready frontier**. Current shape:

- **WI-300** (`P1`, strong, spine) — the (f) decomposition, **partially done this
  session**. What landed: U5 (WI-292), U3 (WI-294), U1 (WI-295), and T5 (WI-299)
  are each fixed + tested + bound to a new child LLR/TC
  (LLR-102..105/TC-105..108). **What's still open, and who owns it:**
  - **SR-053 → `Verification=Test`** needs **U2** (one colour vocabulary) and
    **U4** (one interaction idiom) bound too. Both anchors **already pass** —
    they're structurally guaranteed by the shared `STATUS_FILL`/`TIER_FILL`/etc.
    dicts and the shared `_drill_layer_svg` emitter — but neither has a
    dedicated test or child LLR/TC. **No defect WI owns this**; it's net-new
    test-authoring that only WI-300 itself can close. Once bound, retire the
    coarse `LLR-054`/`TC-054` and flip `SR-053`.
  - **SR-052 → `Verification=Test`** needs **A1** (blocked — WI-273 needs your
    attest/ratify, see below), **A3** (no info by colour alone — likely already
    true, needs a test), and **A4's broader arithmetic core** (every text/fill
    pair, not just the ring WI-299 bound) — none of these three have a child
    LLR/TC yet. A2 is done (`LLR-101`/`TC-104`, delivered by WI-297 earlier).
  - Spec of record: [specs/WI-300.md](specs/WI-300.md) (its per-anchor pass
    predates this session's builds — read status.md/log.md for what's actually
    landed, not the spec's original estimate table).
- **WI-305 / WI-306 / WI-307** — new, filed from `119-CRITIQUE.md` findings no
  existing WI covered: no next-work surface reachable in one tab switch (T1), the
  What/landing tab doesn't start-collapsed like the other three tabs (T2), and two
  SVG emitters clip/force sideways-scroll at their declared widths (T7, both a
  mobile How-SW case and a **desktop-width** What-icicle case). None are gated on
  anything; all three touch `gen_trajectory.py` so budget a re-critique.
- **WI-272** — dashboard work-item status fidelity (preserve `deferred`/`blocked`
  instead of rewriting both as `queued` in the UI). Independent of the critique
  chain; not gated on WI-300.
- **WI-273** — `blocked`. Its code is proven sound (composed, green, both a
  non-Anthropic REVIEW-A and CRITIQUE already ran against it) — it's blocked
  purely on your **attest/ratify** of that dispatch (see
  [open-items.md](open-items.md)'s generated Pending section). Once ratified it
  unblocks on its own; nothing to build.

**Hard constraint, harness-enforced:** a child LLR/TC **cannot** land ahead of its
test behind `Status: Draft`. `Draft` escapes `--require-verified`, but
`derive_gate.py` returns **G0** for a draft row — one draft drops the gate off G3.
Tests first, flip second, never the reverse. (This bit a first attempt this
session in a different way: inserting a new per-node attribute *in the middle* of
an existing attribute string broke three unrelated tests that asserted attribute
*adjacency* — e.g. `data-tier="phase" data-descend="..."` had to stay literally
adjacent. If you add a new inline attribute to a shared emitter, append it
**last**, after everything existing tests might assert about the tag's shape.)

## 5. Deferred backlog — review, and actions taken 2026-07-25

Reviewed 2026-07-25 (see the reasoning that drove each call below); **owner
acted on all four recommendations the same day** — WI-278/WI-062/WI-065 are now
`queued` (they appear in status.md's Ready frontier above) and WI-060 is
`retired`. The rest of the fourteen deferred rows are correctly parked as-is.

### Now queued

**WI-278 — branch integration & CI-on-branch.** *Why:* this session produced
decisive evidence. The local gate had a **total blind spot** — the entire
`agent_loop_*` layer (~104 tests) could not execute on this machine, and the G3
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
close): [WI-065](archive/specs/WI-065.2026-07-25.md). **Landed 2026-07-25**,
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
  ERRORs under `--strict` at G3. This bit twice this session — once for a `done`
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
- **A census sanction (`docs/dupes-allow`) IS accepting the duplication.** Never reach
  for one to green a step.
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

## 7. Suggested order

1. **WI-278** — get CI running on the branch. Everything else is safer once an
   independent environment is checking it.
2. **WI-065** — reconcile the `Verifies` vocabulary before adding more child
   LLR/TC bindings on top of it.
3. **WI-300's remaining binding** — U2 + U4 (SR-053, no defect, pure test-authoring)
   and A3 + A4-core (SR-052). This is the critical path to both SRs flipping to
   `Test` and the seven render rows leaving the critique chain for good.
4. **Ratify WI-273** (owner attest/ratify only — the code and both non-Anthropic
   verdicts are already in) — unblocks on its own once SR-052 flips or on your say-so.
5. **WI-305 / WI-306 / WI-307** — the three new render-usability fixes from
   119-CRITIQUE, each closing by binding like the WI-292/294/295/299 set did.
6. **WI-272** — dashboard status fidelity.
7. **WI-062** — de-noise the doc-ref check.
8. Rule **OI-4** (LICENSE) whenever your public/private intent settles, and
   **OI-8** (CI strategy) whenever you're ready to bless WI-278's approach.
