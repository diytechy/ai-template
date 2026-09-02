+++
id = "WI-571"
title = "The snapshot copies only what the act authorises: copy_live scoped to the flipped registry and the named --approves refs"
workstream = "process"
specref = ""
buildtier = "medium"
priority = 5
safety_class = "ordinary"
+++

## Deliverable

`baseline_snapshot.copy_live` is scoped to the act. A refresh of a populated
snapshot now copies ONLY the registries the act authorises — every registry a
`--approves` ref names, plus every registry an approving `Status` move happened
in (`_authorised_registries`: a flip on an existing row, or a new row that
arrives already `Approved`) — and leaves every other registry byte-identical to
what it was. The seed / first-signing (a `--seed`, a scaffold that still holds
no registry, or an unreadable record being repaired — decided by
`_refresh_targets`) still copies the whole tree. Both mirror rules stay green
untouched, because each is pinned to the file it judges:
`staged_snapshot_findings` only checks snapshot files IN the commit, and
`committed_snapshot_findings` compares each to live at its own writing commit —
an untouched file is not "written". This closes the whole-tree re-seal that
dragged live off-spine drift into the record on every spine-only approval.

`--approves` is a NAMED list: `parse_approves` turns a `;`-joined `REGISTRY=REF`
CLI value into `{registry rel: ref}` (`resolve_registry` accepts a rel,
filename, or carrier-less stem), and a ref mutes `refresh_refusal` for the ONE
registry it names — the secondary widening (`if approves: return ""` muted all
seven) is closed. `_record_approval` records the act's scope into the prose
stamp: the registries copied and, for each, whether a ref named it or a Status
move authorised it. `intake.py snapshot`'s `--approves` help/metavar move to
`REGISTRY=REF`; parsing lives in `baseline_snapshot`, so intake grows by the
two-line CLI edge only (reviewed baseline bump 1177→1179, recorded in the
ratchet with reason in the fragment).

Tests: `tests/test_baseline_snapshot.py` gains five scope tests (a spine flip
leaves off-spine snapshot bytes untouched and the census intact; a named ref
copies exactly its registry; a ref mutes only the registry it names; a
`Status`-move-only refresh is stamped as a `Status move`; the seed still copies
all) and a mirror-green-across-a-scoped-act test; the two existing
tests whose contract changed (a traced-only and a Drafted-only refresh now copy
NOTHING rather than the whole tree) and the approval-stamp test (exercised via a
named amendment, since a traced-only refresh now writes nothing) are re-pointed;
`tests/test_trace_briefs.py`'s two `--approves` callers move to the named form.
Full-suite result and the pre-existing-failure accounting are in the fragment
`docs/log.d/WI-571-snapshot-copy-scope.md`.

NOT done here (plan §2): `OI-78` is not ruled — rows already absorbed at
`580df781` stay absorbed until the owner rules; this row stops the NEXT act from
absorbing more. The queued reseal row `WI-569`'s `## Context` is updated (triage)
to record that, since that row's approval commit moves no `Status` (its
`LLR-203`/`LLR-204` are already `Approved` and merely confirmed), a bare
`intake.py snapshot` there now copies ZERO registries — the off-spine census
survives to its own review, and any registry it means to re-seal must be NAMED
with `--approves`. No spine rows were minted or re-statused, so
no approval brief regeneration was owed. Standing constraint honoured: no
`Status` flip, no `intake.py snapshot` run against this repo's own snapshot —
the scoped copy was driven on scratch scaffolds and tmp trees only.

## Context

Filed 2026-09-01 (evening supervised session) from the owner's question on OI-78 and an independent investigation: baseline_snapshot.copy_live mirrors all seven registries on every intake.py snapshot act, so a spine Status flip re-seals whatever off-spine drift is live at that moment (9 of 21 prior snapshot commits did; the wi508 handback merge was not causal). Scope copy_live to the flipped registry plus the registries named by --approves; make --approves a named list; stamp the act's scope; re-read the queued reseal row's stand branch. Read the plan's section 2 before widening - moving the write to the trunk lane is the recorded alternative, not this row.

**Standing constraint (owner ruling 2026-09-01, the approval act is the
adjudicator's):** if this row authors or amends spine rows (SR/LLR/TC), leave
them `Drafted`; do NOT flip any `Status`, and do NOT run `intake.py snapshot`
or write `docs/archive/last_approved/` on this lane — including while testing
the scoped copy, which must be driven on a scaffold, never on this repo's
snapshot. The flip and the snapshot are performed on trunk by the
adjudication arm once it ships.
