## 2026-08-24 — OI-62 ruled (e), and the nineteen are approved from the corrected brief

Deferred open items: none — the item this sitting ruled is RULED; its
execution row and the follow-on rows it commissions are queued WORK, and the
relocation question the ruling names is deliberately NOT filed today (the
ruling itself sequences that filing to the measuring pass's close, with the
numbers in its brief).

Two owner acts in one directive, in session 2026-08-24. The owner's words,
verbatim, because the second half is the warrant for both halves of this
sitting: *"please spin up opus / sonnet agents as appropriate, and you can
commit, and then I will approve of the spine changes and lock in on option e
of OI-62."* Recorded honestly as issued — a directive in advance of the
record, executed as directed, on the `2026-08-23` sitting's precedent: a
ruling and the acts it authorizes are one event, one commit. The widened
`OI-62` brief the ruling answers landed one commit earlier (`3da625e2`), so
what was ruled is exactly what the owner read.

### Act 1 — `OI-62` ruled: option (e), MEASURE, DON'T REWRITE

`status = "ruled"`, `ruled_date = "2026-08-24"`, `ruling_ref` = this fragment,
`wi_refs = ["WI-516"]`. The ruling is written into the row's `recommendation`
cell above the pre-ruling text, kept verbatim — the `OI-60`/`OI-61` form.
What is ruled, restated once: a read-only classification pass over the 108
non-CLI `contract` rows at (b)'s tranche grain (non-CLI `Provides`, then
`Consumes`), per-row in `WI-512`'s discipline, no cell edited; the per-row
verdicts recorded DURABLY as the follow-on's input; and at the close, the
relocation question — remainder to a component-side contract-header
declaration (the `Contracts: IF-###` docstring line, 57 of 76 modules,
harvested by `gen_arch_map.py`, policed both ways by `check_trajectory.py`),
or stays in the cell — FILED as its own open item carrying the measured
per-family numbers. The 5 ambiguous (d) findings triage inside tranche 1.

**Execution row minted: `WI-516`**, queued, `buildtier = "strong"`,
`safety_class = "ordinary"` (deliberate, argued in the spec: the pass writes
no registry cell — the care lives in the tier, not the class), workstream
`requirements`, `needs = []`, priority 2 —
[../work/queued/WI-516-if-contract-e-measure.md](../work/queued/WI-516-if-contract-e-measure.md).
Watermark `WI 515 -> 516` via `trace.py --bump-ids`.

### Act 2 — the spine approval, executed against the corrected brief

The three preceding fixes (the `owes()` widening, the SR text rendering, the
wording round) existed so this act could happen from an honest surface; the
2026-08-23 sitting stopped rather than approve from the under-counted one.

**The dated brief was minted FIRST**, before a single cell moved:
[../ratify/2026-08-24-spine-approval.md](../ratify/2026-08-24-spine-approval.md)
(`trace.py --mint-approval-brief spine-approval`, immutable under
`approval-immutable`). A byte copy of the `CURRENT.md` the owner read —
verified against a fresh render before minting: the ONE differing line was
the git-derived approval-provenance footer, same staleness shape the
2026-08-23 brief recorded; the brief keeps what was on screen.

**The approved set — 19 `Drafted` rows, INDEPENDENTLY RE-DERIVED before the
flip.** A read-only subagent enumerated, from the registries and the snapshot
alone (no status surface, no log), every `Drafted` spine row and every
live-vs-snapshot drift: **9 LLR** (`LLR-187/193/194/196/198/199/200/201/202`)
+ **10 TC** (`TC-182/188/189/191/192/194/195/196/197/198`), 0 SR, and exactly
ONE non-Drafted **spine** drift — `LLR-041`'s `detail` cell, under `SR-159`.
Identical to the `WI-513` census and to the rendered brief: three routes, one
answer. **SCOPED HONESTLY after the adversarial round caught the sentence
claiming more than it measured (its MAJOR-2):** the re-seed also absorbs the
OFF-SPINE tiers, and there the delta is large — a 135-row, 797-line
`interfaces.toml` reshape (the WI-455 rename + the WI-512 `contract`
thinning, each landed under its own ruling, so no content is unblessed) that
the approval brief STRUCTURALLY cannot render: `--approve modified` is one
section per SR, and the IF tier never reaches it. Bounded today (every IF row
reads `Drafted`; nothing mechanical treats the absorbed copy as blessed), but
the signer's surface has a disclosure hole — **`WI-518`** filed for the
off-spine census line the brief owes its reader; watermark `WI 517 -> 518`.
<!-- fig: cmd="python -c \"import sys; sys.path.insert(0,'project-trajectory/scripts'); import trace as tr, spine_rules; from pathlib import Path; reg=tr.load_registries(Path('docs')); print(sum(1 for rows in (reg.srs,reg.llrs,reg.tcs) for r in rows if spine_rules.is_drafted(r)))\"" rev=3da625e2 -->

**The flip is `Status` cells only**: the whole registry diff is exactly
`19 -status = "Drafted"` / `19 +status = "Approved"` (verified by grep over
the diff — zero non-status lines). No row's text was edited, which is what
keeps this an approval rather than an amendment; the wording-round text the
owner read IS the text that got approved.

**The authority.** `docs/process.toml` `human_approval_through` reads
`DevStg-Needs`, so the LLR/TC tier is agent-performable at this dial — and
here additionally owner-directed in writing, quoted above. All 27 SN rows
read `Approved`; nothing on the human-held tier was touched.

**The baseline re-seed.** `intake.py snapshot --approves "<the owner's words
verbatim> — recorded at this fragment"` — 7 registry files copied, the
warrant in the snapshot's own stamp. The re-seed absorbs `LLR-041`'s ratified
`detail` (the `SR-159` re-attest — no Status cell exists to move on a drift,
per §7; the copy is the signature).

**Closed, verified rather than assumed:** `baseline_snapshot.refresh_refusal`
returns `None`; `trace.py --approve modified --check` exits 0 — *"no row owes
an approval or a re-attest — the window is closed"*; regenerated `CURRENT.md`
renders the no-rows arm. `derive_stage.py`: **`drafted = 0`**, and **phase 4
climbs `DevStg-LLReqs` → `DevStg-Impl`** — the reopened-phase warning its
minted drafts held open clears with it. `stage` stays `DevStg-LLReqs` on
phase 5, honestly: approving text moves no test evidence.
<!-- fig: cmd="python project-trajectory/scripts/derive_stage.py && grep -E '^(drafted|per-phase) ' docs/stage" rev=3da625e2 -->

### Banked finding — `approval_stamp` is blind on BSD regex (WI-517 filed)

Found while verifying the brief's staleness, not fixed here (sitting scope):
`baseline_snapshot.approval_stamp`'s `git log -G'^\s*(status|Status)…'` uses
`\s`, a GNU-regex extension — honored by git's Windows build (glibc compat
regex), matched-as-nothing by macOS's BSD `regcomp`. Measured both ways on
this checkout: the shipped pattern returns empty; the same pattern with
`[[:space:]]` names `2b7be11a`. So every brief rendered on this Mac degrades
its provenance line to "git cannot say" while the owner's Windows box names
the commit — a cross-platform defect in a shipped script, one machine one
data point (Darwin measured; Linux unverified). **`WI-517`** filed, `quick`,
with the fix shape and the test-gap question; watermark `WI 516 -> 517`.

### Adversarial round — taken and iterated before the commit

Owner-directed ("spin up opus / sonnet agents as appropriate"): the flip set
was independently re-derived by a read-only Sonnet subagent BEFORE any edit
(the three-routes-one-answer above), and the full staged diff took a hostile
Opus review BEFORE the commit. **Verdict: no CRITICAL** — registry purity
(19/19 status pairs, zero text lines, re-verified semantically via tomllib),
snapshot/live blob-hash identity across all 7 files, the dated brief byte-
equal to the pre-flip `CURRENT.md` the owner read, the ruling text byte-
preserving its pre-ruling cell, and status.md's forward-only scrub all held
under independent re-derivation. Every finding dispositioned in this commit:

- **MAJOR-1** (a `fig:` marker stamping `rev=3da625e2` on a figure false at
  that revision — `drafted = 0` is true only of THIS commit's tree):
  conceded; the derive-stage and pytest markers are re-stamped onto this
  sitting's own hash in the follow-up stamp commit this fragment declares
  below, the `55d1cb77` precedent. The 19-census marker stays at `3da625e2`
  deliberately — that figure is a pre-flip fact.
- **MAJOR-2** (the drift sentence hid the off-spine absorption): the
  sentence is re-scoped above and **`WI-518`** carries the mechanism gap.
- **MINOR** (snapshot stamp quoted the warrant mid-sentence, no elision
  mark): the uncommitted ledger line re-authored to the house citation shape
  with the elision marked and explained.
- **MINOR** (`WI-516` title at 131 chars tripped the >120 advisory this
  commit would have introduced): shortened to 118.
- **MINOR** (dangling "surface gap above" pointer in `status.md`'s snapshot-
  block bullet, aimed at prose this same diff deletes): re-pointed at the
  closed state.
- **MINOR** (as-of stamps on `docs/stage` / `CURRENT.md` name the parent
  commit): the same `55d1cb77`-precedent follow-up owns them — DECLARED here
  so it is not dropped: **the next commit after this sitting re-derives the
  as-of stamps and the two fig revs onto the sitting commit's hash.**

Un-dispositioned, on purpose: the reviewer's note that the pre-mint
CURRENT.md freshness diff "rests on the author's word" — true, it does; it
is recorded as an in-session verification, and the BSD-regcomp finding it
led to is independently confirmed either way.

### Gates

- `python -m pytest -q -n auto -m smoke` → **1321 passed, 7 skipped in
  22.89s** (pre-sitting baseline run; re-run at commit); budget enforce →
  within.
- `check_trajectory.py --root . --strict` → clean, exit 0. WARN delta vs
  HEAD, disclosed line by line: the phase-4 reopened-anchor WARN **clears**
  (the approval is what closes it), and two advisories of a pre-existing
  class appear — `WI-516`'s specref names `open-items.toml#OI-62`, and the
  shared-spec-of-record advisory is anchor-blind, so it pair-warns against
  `WI-484` and `WI-508` exactly as those two already pair-warn against each
  other at HEAD. Left standing knowingly: the specref is the true
  spec-of-record, and re-pointing it to dodge an advisory would be
  sanctioning the check.
- `check_docs.py --root .` → 0 broken links.
- Full unfiltered suite, run TWICE — pre-sitting on the widened-brief tree
  (**3003 passed, 1 failed, 23 skipped in 547.07s**) and again on the final
  staged tree (**3003 passed, 1 failed, 23 skipped in 519.67s**), identical
  populations — the ONE red,
  `test_approval_stamp_names_the_commit_that_MOVED_A_STATUS_CELL`, is
  PRE-EXISTING at HEAD (verified by stash) and is the same defect `WI-517`
  now owns: the test drives `approval_stamp` on this Mac and the `-G`
  pattern returns empty. Not introduced, not worked around, now tracked.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=3da625e2 -->
<!-- fig: cmd="python -m pytest -q -n auto" rev=3da625e2 -->
