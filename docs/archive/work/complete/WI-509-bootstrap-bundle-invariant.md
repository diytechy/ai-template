+++
id = "WI-509"
title = "Pin the kit-path invariant and document where the machinery lives (OI-59 ruled (a)+(c), 2026-08-22)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

`tests/test_kit_path_invariant.py` (new, in-process, smoke-tier by default):
four tests deriving their swept population from `bootstrap.py`'s own `MAPPING`
list (never a hand-kept list) — every `MAPPING` source plus `RESYNC_PACK.md`
must never spell a bare `python scripts/bootstrap.py` invocation (must instead
address `project-trajectory/scripts/bootstrap.py`); `ADOPTING.md`, the kit's
own root `README.md` and `KICKOFF_PROMPT.md` may use the bare form only beside
explicit kit-folder framing; `bootstrap.py` is confirmed absent from its own
`MAPPING`; and the `--migrate-config`/`--sync` flags OI-59 names are confirmed
present in `bootstrap.py`'s own `argparse` surface. The sweep found and fixed
8 live offenders in the same commit (the pin arming on a clean baseline):
`scripts/agent_common.py` (3 remediation messages), the three git hooks
(`hooks/pre-commit`, `hooks/commit-msg`, `hooks/pre-push`),
`process.toml.template` (2 comment sites), `PROCESS_OPTIONS.md` (1 site), and
`RESYNC_PACK.md` (2 sites) — all bare `scripts/bootstrap.py` invocations an
adopter's own repo, or an already-adopted repo, never has. This repo's own
dogfooded `docs/process.toml` carried the same pre-fix text (out of the pin's
swept surface, since it is not a kit-shipped instructing surface) and was
fixed alongside for consistency.

`ADOPTING.md` §1 gained a "Where the machinery lives" paragraph, immediately
after the scaffold command it explains: the kit folder is the tool, the
scaffold is the product; keep the tool (conventionally `project-trajectory/`)
or forfeit resync/migration by design; a second installer copy (option (b))
was considered and declined by the ruling. `RESYNC_PACK.md` gained a §3/§4
boundary entry recording the change for re-syncing adopters.

Full detail, gate output and byte deltas:
[../../../log.d/2026-08-23-wi509-kit-path-invariant.md](../../../log.md#2026-08-23--wi-509-pin-the-kit-path-invariant-and-document-where-the-machinery-lives).

## Context

Executes OI-59 (a)+(c): bootstrap.py stays out of MAPPING (the bundle IS
the kit folder; the scaffold is the product), and the recurring defect
class — instructions addressing bootstrap/migration machinery at a
SCAFFOLD path the adopter does not have (the WI-498 slice-5 recovery hit
it live) — is made unrepresentable:

1. **The pin**: a test sweeps every shipped instructing surface
   (RESYNC_PACK, ADOPTING, KICKOFF, templates, docstrings the scaffold
   receives) for invocations of bootstrap/migration machinery and asserts
   each addresses the KIT path form, never a bare scaffold-relative one.
2. **The paragraph**: ADOPTING.md's "where the machinery lives" — the kit
   folder is the tool, the scaffold is the product, keep the tool; deleting
   the kit folder after init forfeits resync/migration, by design.
(b) — shipping a second installer copy into the scaffold — is DECLINED by
the ruling: version skew between two installers is the drift class the kit
exists to prevent.
