# 075-REVIEW-A — WI-161 (per-phase within-tier model preference)

Independent review of commit `75cb46c` (WI-161: add per-phase model preference),
built session 074. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-14b.md#phase-preference`), the WI-161 registry
row, the PROCESS_OPTIONS "Unattended operation" routing contract, and the
launcher/agents-enabled surfaces. No SN/SR/LLR/TC rows were added or changed
(off-spine `unattended` work), so no registry sweep applies; this is not a
G1/G2 ratification, so no `--ratify` hierarchy applies.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check.py` (derived gate **G3**, tier all) →
  `RESULT: PASS` — all 15 steps PASS incl. `tests+coverage` (192.6s), `format`,
  `lint`, `dupes`, `derived-gate`, `traceability`, `doc-navigability`,
  `arch-map`, `trajectory-map`, `okf`, `skills-sync`.
- `python -m pytest -q tests/test_agent_route.py tests/test_agent_loop_review.py`
  → `55 passed in 31.32s`.
- `python project-trajectory/scripts/trace.py` → `SN=24 SR=56 LLR=57 TC=57
  orphans=0 integrity=0 components=5 interfaces=52`.
- `wc -c project-trajectory/PROCESS_OPTIONS.md` → `137877` — matches the
  re-stamped byte-budget baseline in all three tracked `byte-budget-guard`
  SKILL copies.

## Assessment

The change is correct and matches every Done-when in the spec. `select()` adds
`preferred_ids`, reordering `avail` (`preferred + rest`) *inside each tier's
availability list* before the family-heterogeneity branch — so a preference can
never pull the resolved tier down (wrong-tier/quick preferred ids are absent
from the strong `avail` and fall through), cooling/disabled/unknown ids fall
through to enable-list order, and `prefer_different` still filters by family so
reviewer/critic heterogeneity wins over the preference. I traced all three
branches (plain, prefer_different, degraded) and the selection is still LOGGED
before launch — no silent swap. `select()` is reached only under `if managed:`,
and the `--prefer-map`/`AGENT_PREFER_MAP` preflight (id-syntax `ID_RE` +
non-empty phase/id) sits in the same `managed` block, so an invalid map fails
preflight with `EXIT_PREFLIGHT` before iteration 1.

The unit tests directly exercise within-tier selection, cooldown fall-through,
wrong-tier containment, and heterogeneity-beats-preference; the managed-loop
test is non-vacuous (default BUILD would draw `builda`; the preference flips it
to `revb`, then the reviewer differs). The self-applied launchers set
`AGENT_PREFER_MAP=BUILD=OPENAI-SOL` while `docs/agents-enabled` returns to
Fable-first — restoring Fable-led PLAN/DESIGN-CHECK while BUILD keeps Sol,
exactly the WI's stated outcome. `.cmd` slots need no `export` (batch env is
inherited); the `.sh` export line was correctly extended. PROCESS_OPTIONS,
architecture code-map, status.md, next-wi, log.md, and the WI row are all
coherent, and the declared policies (`gate-policy: autonomous`,
`push-policy: human`, `run-phase: BUILD`) match the prose. Generated artifacts
(`PROJECT_STATE.html`, `docs/architecture.md`) are in sync (`--check` steps
pass). No defects found.

## Findings

(none)

VERDICT: APPROVE findings=0
