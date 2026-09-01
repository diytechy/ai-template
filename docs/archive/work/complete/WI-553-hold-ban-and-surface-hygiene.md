+++
id = "WI-553"
title = "The hold ban mechanized: claim-ref check, blocked_pending retired, fragment declaration cross-checked (OI-70)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

OI-70's hold-by-rename ban mechanized, all four Done-when arms shipped:

1. **Claim-ref check** — `check_trajectory.holdbyrename_findings` reports every
   `docs/work/active/<branch>/` claim directory with no matching
   `refs/heads/<branch>` (the rename-hold / phantom-head signature). Warn at the
   commit bar, ERROR under `--strict` (the DevStg-Impl gate), silent off-git —
   the R-E/R-F promotable tier, no new `main()` branch. `tests/test_trajectory_holdban.py`
   drives it both ways on a git scaffold plus the empty-dir and off-git edges;
   tiered into `conftest.SLOW_MODULES`.
2. **`blockref` vocabulary retired** — `pending.blocked_pending` (the owner
   surface with zero producers) and the `blockref` FIELD are gone: both loaders,
   the canonical `kitlib.registry.WI_COLUMNS`, `wi_convert`, `plan_artifacts`,
   the shipped template header, and the three derivations (`schedule._disposition`'s
   blocked arm, `traj_views._wi_status`, `blocked_pending`). The `-000` example
   twin, README twins, authored docs, and a RESYNC_PACK.md entry follow. The
   `blocked` WI-384 status WORD stays as defensive vocabulary (OI-70 retires the
   mechanism, not the status model); the `Blocked-WI:`/`BlockRef:` COMMIT
   TRAILERS (a worker's block signal) are a distinct, live instrument, untouched.
3. **Fragment `none` cross-checked** — `gen_open_items` ARM 4
   (`_none_declaration_findings` + `_scope_span`): a fragment declaring
   `Deferred open items: none` while its own scope cites a PENDING open item is
   contradicted, the TRUTH check beside ARM 2's presence check. Position-is-scope,
   warn-first, fail-soft. Four tests.
4. **Ban stated where supervisors read** — the session-protocol skill (a
   Standing rule), `docs/handbacks/README.md`, and the ADJUDICATE
   `adjudicate-disposition` prompt name the partial close as the ONLY sanctioned
   stop and cite OI-70.

Ratchets re-stamped for the change (`check_trajectory` SLOC 2245→2273,
`stack.ini` smoke `max-tests` →1467, the `gen_open_items` newline-site pin);
`PROCESS_OPTIONS.md` +43 flagged in the byte-budget-guard skill; skill copies +
`prompts/CATALOG.md` regenerated. Full unfiltered suite: 3219 passed; the only
failures are a pre-existing ruff-0.16.5 skew (I001 in the bootstrap-generated
demo) confirmed identical on the integration base, unrelated to this WI.
FOLLOW-UP surfaced, not fixed (out of lane, `sr_refs = []`): five Approved spine
cells (LLR-158/161/198, two TC Methods) still *describe* the retired blockref
mechanism — semantic prose drift only (no snapshot drift, no re-attest triggered,
no new crosscheck finding), left for a spine-hygiene pass / owner re-attest.

## Context

`OI-70`'s ruling bans the hold-by-rename outright — a lane must close or it
gets lost, as the wi508 lane nearly was — and the owner endorsed the
mechanization: a claim directory must have a matching branch ref. That
mismatch (spec in `active/`, no ref) is the rename-hold's exact signature and
the same scheduler/dispatcher disagreement `docs/handoff-2026-08-31.md` §2
names as the phantom head. Two dead surfaces ride with the ruling:
`pending.blocked_pending` reads `queued/` rows carrying a `blockref` and
NOTHING produces one any more (`LLR-161` removed the producers), and
`gen_open_items.py --check` verifies a fragment DECLARES its deferred open
items without checking the declaration is true.

## Done-when

1. A check (harness-run, warn-or-gate per the declared policy) reports every
   `docs/work/active/<branch>/` claim directory with no matching branch ref —
   driven on a scaffold both ways (matching ref: silent; renamed ref: named).
2. `pending.blocked_pending` and the `blockref` vocabulary are retired or
   re-pointed — the owner surface keeps no source with zero producers; the
   `-000` example row and any doc teaching `blockref` follow in the same
   slice.
3. The fragment deferred-open-items declaration is cross-checked against the
   registry (a fragment claiming `none` while it should have deferred a row
   is contradicted), not merely presence-checked.
4. The ban is stated where supervisors read: the session-protocol skill and
   the handback/ADJUDICATE docs name the sanctioned stop (the partial close;
   nothing else) and cite `OI-70` as the ruling of record.
