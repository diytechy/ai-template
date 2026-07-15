# 082-REVIEW-A — WI-162 (parallel WI dispatch across coordinator lanes — design spec)

Independent review of commit `d8c496d` (WI-162: specify parallel WI dispatch),
built session 081. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-14b.md#parallel-dispatch`), the WI-162 registry
row (`WI-025;~WI-149`, `BuildTier=strong`), the existing `--track` machinery it
designs over (`project-trajectory/scripts/agent_loop.py`), and the
PROCESS_OPTIONS "Parallel tracks (multi-lane operation)" layer it extends. No
SN/SR/LLR/TC rows were added or changed (off-spine `unattended` design-spec work;
`docs/specs/parallel-wi-dispatch.md` is a new proposed doc, spine untouched), so
no registry sweep applies; this is a BUILD commit, not a G1/G2 Status-change
ratification, so no `--ratify` hierarchy applies.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/trace.py` → `SN=24 SR=56 LLR=57 TC=57
  orphans=0 integrity=0 components=5 component-findings=0 interfaces=52
  interface-findings=0`.
- `python project-trajectory/scripts/check_trajectory.py` → `clean (167 work
  item(s), 144 done (86%), graph acyclic)`.
- `python project-trajectory/scripts/check_docs.py --stale` → `OK - 93 doc(s),
  398 intra-repo link(s), 0 broken (40 orphan warning(s))`; the new
  `docs/specs/parallel-wi-dispatch.md` is one of the 40 orphan warnings, which is
  the established pattern for `docs/specs/*` (WI-107.md, WI-110.md are also
  orphan docs — reachable via the `work-items.csv` SpecRef and log prose, which
  the link graph does not traverse), not a regression.
- `python -m pytest -q -n auto -m smoke` → `622 passed, 2 skipped in 53.80s`
  (matches the log's green claim; no script or test changed in this diff).
- `python project-trajectory/scripts/derive_gate.py --check` → `docs/gate up to
  date (G3)`; `python project-trajectory/scripts/gen_trajectory.py --check` →
  `project-state dashboard up to date`.
- Declared policies vs status.md prose: `gate-policy=autonomous`,
  `push-policy=human`, `run-state=RUNNING`, `run-phase=BUILD`, `next-wi=WI-165` —
  all match the status/log prose; no contradiction.

## Assessment

The spec satisfies the intake's named surface completely: an actionability scan
(all hard predecessors `done`, soft `~` as ordering/overlap signal only, §3), an
overlap guard carrying every heuristic the intake named — shared `Campaign`,
same `Workstream`, shared `SpecRef` surface, spine-touching-stays-serial — plus
dependency and declared-path keys with an explicit unknown-means-serial default
(§4), a lane lifecycle over `docs/parallel` N lanes with per-lane `next-wi` and a
telemetry projection (§5, §7), and per-lane review-round semantics (§6). The
five implementation slices (§10) and campaign done-when (§11) are specified for
filing on ratification, as the WI contract requires (no implementation shipped).

I verified the spec's claims about existing machinery against the code rather
than trusting them: `agent_loop.py --track x` does run on `llm/x` in its own
worktree with coordination files under `docs/tracks/x/` guarded by
`out/agent-loop.lock` (docstring L71-82, resolution L1879-1901), and `next-wi`
**is** lane-resolved (`lane / "next-wi"`, L2201/2248/2255) — so §2's
"lane's tracked `docs/tracks/<lane>/next-wi`" and §5.2's lane-local `next-wi` are
accurate, not invented. The registry columns the overlap guard reads
(`Status`, `SR-Refs`, `Predecessors`, `SpecRef`, `Campaign`, `Workstream`,
`BuildTier`) all exist in `work-items.csv`. The design is consistent with
PROCESS_OPTIONS "Parallel tracks": dispatcher/integrator is the sole root writer,
integration is serialized, the `SN→SR→LLR→TC` spine and single `docs/gate` stay
repo-singular. Byte-budgeted files (AGENTS.template.md, PROCESS.md,
PROCESS_OPTIONS.md) are untouched — the canonical PROCESS_OPTIONS text is
correctly deferred to slice 5. Bookkeeping is forward-only and coherent: WI-162
dropped from the status queue and next-action, `next-wi` → WI-165, the WI row
closed with a faithful summary.

Two MINOR items remain, neither blocking. The commit bundles an out-of-scope
BuildTier upgrade to a *different* WI (disclosed, defensible), and the spec
states the one-WI-per-lane property without naming the mechanism that enforces it
against `agent_loop`'s documented close-and-advance behavior.

## Findings

- [MINOR] docs/requirements/work-items.csv:166 -> the WI-162 commit also flips WI-165's BuildTier from empty (phase default) to `strong` — an out-of-scope triage of a different WI folded into the design-spec commit; it is disclosed in log.md and defensible (WI-165 may harden TC-056 via change-intake, so it is spine-touching), and it is an upgrade not a downgrade, but per the working agreement ("don't change unrelated code; surface it separately") it belongs in WI-165's own dispatch or an owner triage note, not here -> either split it out or record it as an explicit one-line triage decision in status/log so the tier bump is not an invisible rider on WI-162 -> @owner
- [MINOR] docs/specs/parallel-wi-dispatch.md:100 -> §5.5/§8 assert "at most one owner per WI" and each lane completes "without occupying another WI", but §5.3 launches `agent_loop.py --track <lane>` "with the normal policy" and names no bound confining that lane loop to its single assignment — `agent_loop` on WI close rewrites the lane's `next-wi` to the next actionable and continues (agent_loop.py L2197-2201), so the property depends on an unspecified stop-after-assignment mechanism; a ratifiable design should state it -> name how the lane is confined to one WI (e.g. a single-WI/stop-at-close mode the dispatcher runs the lane under, or that the lane's self-advance yields control to the dispatcher rather than self-selecting a new WI) in §5 -> @owner

VERDICT: APPROVE findings=2
