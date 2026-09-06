# P0 inventory — refreshed baseline

**Prepared:** 2026-09-05, from revision `5645798c9f689c4ff6b98bf96fa7c4e8a1c717d4`
on `contract_split`. This is the read-only P0a census needed to start supervised
work. It is not a completed P0a proof, a runtime change, a WI, or an approval
of the redesign. `OWNER_SCRATCHPAD.md` was excluded.

## Reproducible census

The following commands were run from the repository root. The registry counts
are section-key counts, and the queued count excludes the inert `WI-000`
example.

```text
$ git rev-parse HEAD
5645798c9f689c4ff6b98bf96fa7c4e8a1c717d4
$ git rev-list --left-right --count HEAD...@{upstream}
0	0
$ python3 - <<'PY'
> from pathlib import Path
> import re
> specs = [
>  ('SN','docs/requirements/stakeholder-needs.toml',r'^\[need\.(SN-\d+)\]'),
>  ('SR','docs/requirements/system-requirements.toml',r'^\[requirement\.(SR-\d+)\]'),
>  ('LLR','docs/requirements/low-level-requirements.toml',r'^\[design\.(LLR-\d+)\]'),
>  ('TC','docs/test/test-cases.toml',r'^\[test\.(TC-\d+)\]'),
>  ('IF','docs/requirements/interfaces.toml',r'^\[interface\.(IF-\d+)\]'),
>  ('CMP','docs/requirements/components.toml',r'^\[component\.(CMP-\d+)\]'),
> ]
> for label, rel, pat in specs:
>     print(label, len(re.findall(pat, Path(rel).read_text(), re.M)))
> queued = sorted(p for p in Path('docs/work/queued').glob('WI-*.md') if not p.name.startswith('WI-000'))
> print('queued_non_example', len(queued))
> print('queued_ids', ' '.join(re.search(r'WI-\d+', p.name).group() for p in queued))
> PY
SN 27
SR 76
LLR 192
TC 191
IF 167
CMP 4
queued_non_example 18
queued_ids WI-536 WI-539 WI-541 WI-545 WI-551 WI-556 WI-557 WI-570 WI-577 WI-581 WI-582 WI-596 WI-597 WI-598 WI-601 WI-602 WI-603 WI-604
```

The registry probe above counts section headers. The queued identities also
match [`BACKLOG-MIGRATION.md`](BACKLOG-MIGRATION.md) §5. Source-line references
below describe the committed baseline, before this sitting's implementation
edits. The upstream result describes only that baseline commit; it does not
claim the in-progress worktree is clean or that later commits were pushed.

Spine status is 27 approved SNs; 75 approved and 1 drafted SR; 189 approved and
3 drafted LLRs; and 184 approved and 7 drafted TCs. The 11 drafted rows are an
existing stage fact, not a P0a permission to alter the spine.

## Queue and preserved work

The loop is paused under tracked `docs/work/pause`; there is no active lane in
the working tree. `docs/work/active/` is absent, `docs/work/deferred/` contains
only `.gitkeep`, and `git worktree list --porcelain` shows the primary checkout
plus the documentation-only redesign worktree. The local
`wi416-parked-handback-contract` branch and remote
`origin/wi508-architectural-remap-HELD-for-owner-verdict` are preserved parked
refs, not active lanes. The five partial handbacks (WI-451, WI-484, WI-508,
WI-521, WI-540), their terminal specs, and the two preserved patches under
`docs/work/handback/` remain evidence. Do not delete, rebase, or apply them as
part of P0a.

The 18 queued rows remain the obligation records; their proposed slice mappings
are in [`BACKLOG-MIGRATION.md`](BACKLOG-MIGRATION.md) §2. The overlap points that can
affect initial work are: WI-551/WI-541 retention; WI-581 close hygiene;
WI-582 parsed dependency/seam behavior; WI-557 delegated reports; WI-570 typed
briefs; WI-577 held approval population; WI-596 snapshot authority; WI-597
scoping wording; and WI-601/603/604 pending amendment/approval judgments.
Those obligations must be read from each complete spec before a successor or
replacement slice is proposed.

## Initial obligation map

The redesign's package-to-obligation map is retained in
[`IMPLEMENTATION.md`](IMPLEMENTATION.md) §3 and the executable details in
[`EXECUTION-DETAILS.md`](EXECUTION-DETAILS.md) §7; this file records only the
items that constrain the first supervised fixes:

| Obligation | Initial slice | Current evidence and boundary |
|---|---|---|
| OI-83: coordinator executes stale imported modules | P0b | `project-trajectory/scripts/agent_loop.py:165-181` imports the runtime graph once; `docs/status.md` and `decisions-for-review-2026-09-05.md` §6 retain the owner decision. A launch digest/exit route needs a reviewed implementation and tests. |
| OI-84: resumed worker can infer an empty evidence range | P0b | `project-trajectory/scripts/agent_common.py:2253-2268` still derives `default_base`; `train_evidence` reads `base..HEAD` at `:1878-1891`. Existing lane topology coverage is `tests/test_agent_loop_review.py:1137-1167`; the single-checkout resumed case remains the gap. |
| Invocation attribution minimum | P0b | `agent_common.write_session_log` is the existing carrier (`:2407-2483`), and `agent_loop.session_meta` is its producer (`:3257-3336`, called at `:3934-3950`). Add the minimum identity/role/provider/tier/raw-counter fields there without a metrics database or second transcript store. |
| Honest smoke baseline | P0b/P0c | `docs/stack.ini` declares the smoke tier and 60-second budget; `tests/conftest.py:SLOW_MODULES` partitions heavy modules. The proposed `[step:smoke]` at `from-stage = DevStg-Tests` is additive and does not discharge SN-007's full-suite promise. No current run is claimed by this census. |
| H1: need/WI hat context is lost in real decomposition | P0a/P1 disposition, then P2a/P7a repair | `plan_runner._hat_slots` (`:206-232`) calls only `hat_context_for_work_item`; the documented SN-026 probe omits LEGAL, DATA-PROTECTION and UNATTENDED-OPS. `HATS-AND-DECOMPOSITION-REVIEW.md` §2 gives the bounded reproduction. |
| Adopter meaning and upgrade preservation | P0a fixture, P10 acceptance | Existing old-kit resync fixture is `tests/test_old_kit_resync.py:172-245`; it exercises one pinned tarball-adopter range and explicitly exposes add-only/old-checker limitations. Node profile tests (`tests/test_profile.py:188-241`, `tests/test_stack_profile.py:449-464`) are fresh scaffolds, not populated upgrades. |

## What this does and does not establish

This refresh establishes the current revision, queue identities, directory
state, preserved evidence locations, spine counts, and source seams for P0b.
It does not complete the full P0a clause map across every LLR/TC/test family,
run the scripted crash/recovery scenarios, prove the adopter upgrade workflow,
settle OI-82/OI-83/OI-84, or choose retain/targeted-repair/replace at P0c.
No tests, paid providers, authority changes, queue edits, or preserved-patch
applications were performed for this inventory.
