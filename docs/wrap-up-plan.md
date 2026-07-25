# Wrap-up plan — closing out the template

**Purpose.** A resumption guide for finishing this repo's open work in a later
session. Written 2026-07-25.

**This file is a POINTER, not a source of truth.** [status.md](status.md) is the
forward-only working surface, [work-items.csv](requirements/work-items.csv) is the
authoritative registry, and [log.md](log.md) holds what shipped. Read those first;
this file only adds what they don't carry — a **sequencing recommendation** and a
**deferred-backlog review**. Where it disagrees with them, they win.

---

## 1. Where the repo actually stands

Read the generated block at the top of [status.md](status.md) for live numbers. As
of writing: derived gate **G3**, spine SN=25 SR=110 LLR=101 TC=104, `drafts=0`,
full suite **green** on Python 3.13.14.

The one thing you cannot learn from status.md: **until 2026-07-25 the G3 harness had
never been runnable on the owner's machine.** The `.venv` was Python 3.9.6, below the
kit's own 3.11 floor, so ~104 tests silently skipped and `check.py --gate G3` could
not execute at all. That is fixed. Everything green before that date was green on a
*partial* run — treat pre-2026-07-25 "all passing" claims with that caveat.

## 2. The one thing blocking a green G3

`check.py --gate G3` is **16 PASS / 1 FAIL**. The sole failure:

> `trajectory --strict` → `perceptual-stale`: SR-052/053/054 are
> `Verification=Critique`, and `gen_trajectory.py` changed after `118-CRITIQUE`, so
> those verdicts judge an older render.

**The checker is right and this is fail-closed by owner ruling (2026-07-20) — but that
ruling is about staleness, not about who may run the critique.** SR-084's own text and
its router (`project-trajectory/scripts/agent_route.py:50-53,608-653`) make
family-heterogeneity a **preference, not a mandate**: a reviewer/critic *prefers* a
different family from the implementer, but "degraded availability is legal — fresh
context is the invariant," and same-family runs are accepted with a `DEGRADED` banner
and a weaker corroboration weight, never a hard refusal. Nothing in
`check_trajectory.py`/`agent_dispatch.py` inspects which model or family produced a
`docs/reviews/*-CRITIQUE.md` verdict — the staleness check is purely git-time-based.
**Earlier wording in this file (and in WI-273's `BlockRef`) hardened that preference
into an absolute "Claude/Opus can never satisfy SR-084," which overstates the actual
design** — corroboration is why a genuinely different family is worth reaching for
first, but it is not the fail-closed thing here; staleness is. It clears two ways:

1. **Run a fresh CRITIQUE.** A genuinely different (non-Anthropic) provider is still
   the preferred, stronger-corroboration path per SR-084/SR-085 and worth reaching for
   when access allows. Absent that, a **fresh, non-authoring-session Claude/Opus
   critique is a legal degraded substitute** — SN-024's actual invariant is "never the
   authoring session," not "never the same family" — so record it as `DEGRADED` (per
   the router's own convention) rather than either refusing it or silently claiming
   full heterogeneity.
2. **Finish WI-300's option (f) mechanization** until SR-052 and SR-053 carry no
   perceptual residue and flip to `Verification=Test`. They then leave
   `_load_critique_srs` and stop demanding a critique at all.

**Route 2 retires the perceptual residue instead of leaning on a corroboration
workaround, so it is still the sturdier long-term fix** and the practical case for
prioritising WI-300 — but route 1 is not actually closed the way earlier notes here
claimed; don't treat "no non-Claude access" as a dead end without at least trying a
fresh same-family critique and recording it honestly as degraded.

⚠️ **Never revert a real fix, or sanction a check, to make this green.**

## 3. Open owner decisions (nobody else can make these)

| | Subject | State |
|---|---|---|
| **OI-4** | WI-097 — LICENSE + public/private intent | No recommendation possible; needs your intent first. **Blocks any public release** (review finding H-3). |
| **OI-7** | WI-123 — review cadence | Recommendation: wait for evidence. **New evidence below — it now points at keeping per-slice review.** |
| **OI-8** | WI-278 — branch integration & CI-on-branch | Ruled: open a PR. **Not yet implemented.** See §5 — this session made the case much stronger. |

Full briefs: [open-items.md](open-items.md). OI-9 was **ruled** 2026-07-25 (option
(f)); its brief is deleted per the pending-only rule and the ruling is in log.md's
Decisions.

## 4. The active queue

Generated order lives in status.md's **Ready frontier**. The shape:

- **WI-300** (`P1`, strong, spine) — the (f) decomposition. Its spec
  ([specs/WI-300.md](specs/WI-300.md)) carries the full per-anchor pass.
  **Key finding: the anchors are already largely TESTED** — owning tests exist,
  several already named after their anchor. What was missing is the **registry
  binding**. So the remaining work is mostly registry decomposition, and it is gated
  not by test-authoring but by the **open defects** on the render rows below.
- **WI-292 / WI-294 / WI-295 / WI-299** — the render fixes. Each now closes by
  **binding**: fix + the test that owns its anchor + the child LLR/TC naming that test
  in `Evidence`, **in one commit**.
- **WI-272** — dashboard status fidelity (not a critique finding; independent).
- **WI-273** — `blocked`, needs an attest/ratify of the heterogeneous CRITIQUE
  dispatch.

**Hard constraint, harness-enforced:** a child LLR/TC **cannot** land ahead of its
test behind `Status: Draft`. `Draft` escapes `--require-verified`, but
`derive_gate.py` returns **G0** for a draft row — one draft drops the gate off G3.
Tests first, flip second, never the reverse.

**Sequencing note:** SR-052/SR-053 flip only when their *last* anchor binds, so the
payoff — seven rows released from the CRITIQUE gate, WI-273 included — arrives at the
end of the render set, not incrementally.

## 5. Deferred backlog — review and recommendations

Fourteen deferred rows, reviewed 2026-07-25. **Three should be queued; one should
probably be retired; the rest are correctly parked.**

### Queue these

**WI-278 — branch integration & CI-on-branch. Strongest recommendation here.**
*Pro:* this session produced decisive evidence. The local gate had a **total blind
spot** — the entire `agent_loop_*` layer (~104 tests) could not execute on this
machine, and the G3 harness had never run, concealing two failing steps including
four pre-existing duplicate blocks. Hosted CI on Linux + Windows would have caught
both immediately. The branch is also ~845 commits ahead of `main` with **no CI on
push** (`test.yml` fires only on `push: main` and `pull_request`). OI-8 is already
ruled; the cheapest option (open a PR) is `quick` tier.
*Con:* opening a PR invites review pressure on a large delta; merging in slices is
real work.
*Verdict:* **queue now.** It is the highest value-per-effort item in the repo, and it
closes a class of blindness rather than one defect.

**WI-062 — `check_doc_refs` warn-first untraced-path tier.**
*Pro:* **562 dangling references** repo-wide today. That volume is pure noise, and
noise is how a real broken link hides — the check's signal is currently near zero.
Tiering separates "illustrative placeholder path" from "actually broken".
*Con:* needs a design decision on what the tiers are; `--strict` already gates, so
nothing is currently *unsafe*.
*Verdict:* **queue.** Largest active noise source in the doc checks.

**WI-065 — active-seam TC citation, reconcile `trace` `Verifies` vocabulary.**
*Pro:* it touches the **exact vocabulary option (f) leans on**. WI-300 is binding
anchors via `Verifies: SR-xxx;LLR-xxx`, so building that out on an unreconciled
vocabulary risks rework. Has a real spec ([specs/WI-065.md](specs/WI-065.md)).
*Con:* spine-adjacent, so it wants care; not blocking today.
*Verdict:* **queue, ideally before the bulk of WI-300's binding work.**

### Consider retiring

**WI-060 — coordinator working-tree stash/rollback between sessions.**
*Pro:* residue between sessions is a genuine unattended hazard.
*Con:* it appears to **contradict a settled design decision**. The `session-protocol`
skill states the loop surfaces residue into the session prompt but "never
auto-stashes — the judgment is yours." WI-060 proposes automating exactly that.
*Verdict:* **don't queue.** Rule it: either retire with that reason recorded (the
repo's retire-don't-delete habit keeps the reasoning traceable), or re-scope it to
something that doesn't fight the existing contract.

### Keep deferred (correctly parked)

| WI | Why it stays |
|---|---|
| **WI-097** | Owner ruling (OI-4), not queueable work. Blocks public release. |
| **WI-123** | Owner ruling (OI-7). **New evidence — see below.** |
| **WI-108** | Flaky test: **1 failure in 8 runs**, never reproduced, unforce-able even oversubscribed. Its spec correctly parks it until it recurs often enough to verify a fix against. Passed again 2026-07-25 under `-n auto` + coverage. Windows CI (WI-278) is the likeliest way to surface it. |
| **WI-271** | Warn-tier, non-gating, and its own spec says the warn still earns its keep. |
| **WI-277** | Genuinely hard-gated behind WI-280's seams stabilising. |
| **WI-280** | A deliberate design program, not a cleanup. See the note below. |
| **WI-061** | Mutating source-doc frontmatter is invasive for the value; flag-gated at best. |
| **WI-063** | No pain signal — no composite artifact has gone stale. |
| **WI-158** | Nice-to-have export; no demand. |
| **WI-187** | Large and design-heavy; overlaps WI-280's territory. |

**New evidence for OI-7 (WI-123).** The recommendation was to wait for ≥2 phases of
medium-BUILD evidence before relaxing per-slice review. This session supplies a data
point **against relaxing**: an adversarial review of WI-297 refuted its headline claim
and found a **severe** defect (a children-presentational `role="img"` still sitting
over 9 focusable links — the exact bug the WI existed to fix), plus a mis-measurement
that made the reported numbers wrong. `trace.py` could confirm the TC existed and
named tests; **nothing mechanical could tell that its `Evidence` described the
artifact incorrectly.** Under option (f), a binding is only as honest as the review
that lands it. Weigh that before reducing review cadence.

**Note on WI-280.** Evidence accumulated this session: the module-size ratchet fired
three times, and WI-304 found that `agent_dispatch.py` contained extractable
boilerplate **plus a latent error-hiding defect** (five raw tail-slices that could
truncate away the reason a dispatch failed). Targeted extraction proved tractable and
valuable. Consider carving a **first slice** rather than keeping the whole program
parked.

## 6. Standing hazards for a new session

- **Always invoke `./.venv/bin/python`** — bare `python` is not on PATH.
- **Diagnose environment before code.** `./.venv/bin/python -m pytest -q
  tests/test_prereq_toolchain.py` — two failures plus a `!! TOOLCHAIN PREREQ` banner
  means the interpreter, not the branch.
- **`status.md` is forward-only and it is enforced.** A `done` WI id in that file
  WARNs at the commit bar, ERRORs under `--strict` at G3, and has a hard test
  (`test_forward_only_unit_over_the_real_meta_repo`). Scrub ids on close.
- **Closing a WI has a ritual:** `Status=done`, fill `Deliverable`, **clear
  `SpecRef`** (R-E), scrub the id from status.md.
- **Editing `gen_trajectory.py` re-reds `perceptual-stale`** — it is path-triggered,
  independent of what you changed. Budget a critique with every render fix.
- **A census sanction (`docs/dupes-allow`) IS accepting the duplication.** Never reach
  for one to green a step — WI-304 showed the duplication was masking a real defect.
- **The runtime pin in `scripts/dev-setup.command` must be re-stamped** when the kit
  moves Python (currently 3.13.14). Nothing reminds you; the re-stamp command is in
  the file.
- **Opus/Claude CAN satisfy CRITIQUE as a degraded, same-family substitute** — a
  fresh, non-authoring session, recorded `DEGRADED` per the router's convention.
  A genuinely different (non-Anthropic) family is still *preferred* (SR-084/SR-085)
  for its stronger corroboration weight; don't skip reaching for one when available,
  and don't record a degraded run as if it were full heterogeneity.

## 7. Suggested order

1. **WI-278** — get CI running on the branch. Everything else is safer once an
   independent environment is checking it.
2. **WI-065** — reconcile the `Verifies` vocabulary before building more bindings on
   it.
3. **WI-292 / 294 / 295 / 299** — the render set, each closing by binding. This is
   also the critical path to SR-052/053 flipping to `Test`.
4. **WI-300** completion — the flip, once the residue is empty. G3 goes green here.
5. **WI-272**, then **WI-273** (needs your attest).
6. **WI-062** — de-noise the doc-ref check.
7. Rule **OI-4** (LICENSE) whenever your public/private intent settles; rule
   **WI-060** retire-or-rescope.
