+++
id = "WI-511"
title = "hats.py grows an OPTIONAL_KEYS mechanism, unblocking WI-484 phase 4's `knowledge` field"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 1
+++

## Deliverable

Landed an `OPTIONAL_KEYS` concept in `project-trajectory/scripts/hats.py`,
unblocking WI-484 phase 4's `knowledge` field on the hats roster down to the
owner's own value-filling pass.

**The mechanism.** `OPTIONAL_KEYS = ("knowledge",)`: a key in this set is no
longer refused as unknown; its presence is validated by
`OPTIONAL_KEY_VALIDATORS["knowledge"]` (`_validate_knowledge`) — a non-empty
list of non-empty strings, refusing a bare string, a present-and-empty list,
or a non-string/blank entry, each naming `` `knowledge` `` by name; its
ABSENCE stays fine on every row, never defaulted to `""`/`[]`. A key in
neither set still refuses loudly — the strict unknown-key posture is
unchanged; a *declared* optional set is the whole mechanism, not a loosened
check. `hats.py list` and `_cmd_applicable` (via `brief_block`) print the
field where a row carries it and stay silent where it does not.

**The value shape**, decided from phase 4's brief in `open-items.toml`
`OI-32` ("knowledge packs derived from concerns"): a non-empty list of
non-empty strings — repo-relative paths or pack names, e.g.
`knowledge = ["docs/knowledge/security-review.md"]`. Kept minimal: nothing
downstream reads more than "which packs does this hat cite" today; a richer
shape is grown later against a real consumer.

**The shipped template** (`project-trajectory/registries/hats.template.toml`)
gained a commented explanation of the key — no row fills it in. **This repo's
own `docs/requirements/hats.toml` is untouched**: no `knowledge` values were
added, per the owner's explicit instruction — the mechanism ships EMPTY here;
the value-filling pass is the owner's act, not this WI's.

**WI-484's spec (item 5) and `docs/status.md`'s wi484 bullet** were updated in
the same commit: the blocker's mechanism half is DONE; what phase 4 still
awaits is the owner's own `hats.toml` value pass.

**Adopter surface:** `project-trajectory/RESYNC_PACK.md` gained an entry
(`[since 46dcac8a]`) describing the change and what an adopter must do
(nothing mechanical; add `knowledge` only if wanted).

**A real commit-bar blocker found and fixed in the same commit, not deferred**
(the antidote reflex applied to the session's own gate, not just the hats
mechanism): moving this WI's own spec straight to
`docs/archive/work/complete/` and bumping the id watermark to WI-511 in ONE
commit hit `trace.py --strict-integrity`'s watermark-raise rule — it refused
the raise as unjustified, because `_wi_ids` (feeding `live_max_ids`) only
ever scanned `docs/work`, never its archive sibling `docs/archive/work`
(WI-504 relocated terminal history one directory deeper, and
`kitlib.registry.spec_roots` already exists as the one home for "both are one
registry" — `_wi_ids` was simply never updated to use it). The prior
same-session mint-and-close precedents (WI-509, WI-510) never hit this: their
watermark bump landed in the MINT commit, while the spec still sat under
`docs/work/queued/` (which the old scan did see), and the archive move
happened in a LATER commit where the mark did not need to rise again. A
direct mint-to-archive in one commit is exactly the pattern this WI's own
task asked for, so the gap was live, not hypothetical. Fixed by routing
`_wi_ids` through `kitlib.registry.spec_roots(docs / "work")` instead of a
hardcoded `docs / "work"`; `tests/test_module_size_ratchet.py`'s `trace.py`
baseline re-stamped +6 (5316 -> 5322) for the six added lines, reason
recorded there. Regression pinned: `tests/test_id_watermark.py
::test_live_wi_ids_are_counted_under_the_archive_sibling_too`.

**Tests** (`tests/test_hats.py`, in-process, smoke-tier): a declared optional
key absent loads clean and carries no such dict key; present and well-formed
is parsed and surfaces on `brief_block`/`list`; five malformed shapes (bare
string, empty list, non-string entry, empty string entry, whitespace-only
entry) each refuse naming `` `knowledge` ``; an unrelated unknown key
(`notes`) still refuses by name; the CLI `list` command prints the
`knowledge:` line only on the row that carries it.

**Scaffold verification:** bootstrapped a fresh scaffold, confirmed the
template's roster (with its new documentation comment, no filled row) parses
under `hats.py`, that `hats.py list` surfaces an appended test row's
`knowledge` field, and that an empty-list `knowledge` value refuses by name —
verified against the real scaffolded artifact, not by reading the generator.

Gates (final, on the tree including the `trace.py` fix): `pytest -q -n auto
-m smoke` 1311 passed / 5 skipped in 26.4s; `check_smoke_budget.py --mode
enforce` 18.7s vs 60s budget; `check_docs.py --stale` 0 broken;
`check_trajectory.py --strict` clean (all WARNs pre-existing); full
unfiltered `pytest -q -n auto` 2987 passed / 14 skipped in 1283.55s
(0:21:23). Full record: `docs/log.d/2026-08-23-wi511-hats-optional-keys.md`.

Deviations from spec: one, found and fixed rather than deferred — the
`trace.py _wi_ids` archive-scan gap above. Everything else landed as scoped.

## Context

Owner-directed 2026-08-23, in-session: WI-484's spec (item 5) records that
phase 4 — deriving knowledge packs from concerns via a `knowledge` field on
`hats.toml` — is blocked on a mechanism the brief did not anticipate.
`scripts/hats.py` enforces a STRICT unknown-key refusal (`REQUIRED_KEYS`, and
`_hat_from_row` raises on any extra key) with no notion of an *optional* key:
adding `knowledge` today would either make it MANDATORY on all 16 live rows
and all 16 shipped-template rows, or require an `OPTIONAL_KEYS` concept minted
first. `docs/requirements/hats.toml` is also declared OWNER TEXT in its own
header, so filling the values is not an agent's act.

This WI lands the mechanism NOW, mined from the watermark and executed in the
same sitting, so phase 4 waits only on the owner's `hats.toml` value-filling
pass — not on a second worker session to build the plumbing first.

**The value shape**, decided from phase 4's brief in `open-items.toml`
`OI-32` ("knowledge packs derived from concerns"): a non-empty list of
non-empty strings — repo-relative paths or pack names, e.g.
`knowledge = ["docs/knowledge/security-review.md"]`. Kept deliberately
minimal: nothing downstream reads more than "which packs does this hat cite"
today, and a richer shape (typed pack references, ordering, per-pack
metadata) can be grown later against a real consumer rather than guessed
ahead of one.

**The mechanism**, in `project-trajectory/scripts/hats.py`:

- `OPTIONAL_KEYS = ("knowledge",)` — a key in this set is no longer an
  "unknown key" refusal (unlike `REQUIRED_KEYS`, its ABSENCE is always fine);
  a key in neither set still refuses loudly, so the strict posture survives —
  that is the entire point of a *declared* optional set rather than a
  loosened check.
- `OPTIONAL_KEY_VALIDATORS` maps each optional key to a validator; `knowledge`'s
  refuses a bare string, an empty list, and a non-string/blank entry, each
  naming `` `knowledge` `` in the message.
- `_hat_from_row` parses a present optional key into the hat dict; an absent
  one is never defaulted to `""`/`[]` — the same "declared vs not" honesty
  `REQUIRED_KEYS` already gives, one tier down, so existing structural pins
  (`set(hat) == {...}`) are untouched on every row that does not use it.
- `hats.py list` and `_cmd_applicable` (via `brief_block`) print the field
  where a row carries it and say nothing where it does not.

**The shipped template** (`project-trajectory/registries/hats.template.toml`)
gains a commented explanation of the new key, with NO row filling it in —
values stay the owner's editing act. **This repo's own**
`docs/requirements/hats.toml` is untouched: no `knowledge` values are added
here, per the owner's explicit instruction that the field is owner text and
the mechanism ships empty in this repo.

**Adopter surface:** a `RESYNC_PACK.md` §3/§4-region entry (anchored
`[since 46dcac8a]`, the commit preceding this WI's own) records the change and
what an adopter must do (nothing mechanical; add `knowledge` to a row only if
they want it).
