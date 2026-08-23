## 2026-08-23 — WI-511: an OPTIONAL_KEYS mechanism in hats.py, unblocking WI-484 phase 4

Owner-directed 2026-08-23, in-session: *"file AND execute a new work item
minting the optional-key mechanism in `hats.py`, so that WI-484's phase 4
(`knowledge` on the hats roster) is unblocked down to the owner's own
value-filling pass."* Minted and executed in one sitting — the WI's spec:
`docs/archive/work/complete/WI-511-hats-optional-keys.md`.

**The blocker (WI-484's spec, item 5).** `scripts/hats.py` refused any hat-row
key beyond the three `REQUIRED_KEYS` with no notion of an optional one, so
adding `knowledge` (phase 4, OI-32 (d): knowledge packs derived from concerns)
could only be done by making it mandatory on all 16 live rows and all 16
shipped-template rows — and `docs/requirements/hats.toml` is declared owner
text, so filling those values is not an agent's act.

**The value-shape decision**, from OI-32's phase-4 brief ("knowledge packs
derived from concerns"): a non-empty list of non-empty strings — repo-relative
paths or pack names, e.g. `knowledge = ["docs/knowledge/security-review.md"]`.
Kept deliberately minimal, on the same reasoning the roster's own three
required keys use: nothing downstream reads more than "which packs does this
hat cite" today, so a richer shape (typed references, per-pack metadata,
ordering) is grown later against a real consumer rather than guessed ahead of
one.

**The mechanism, `project-trajectory/scripts/hats.py`.**

- `OPTIONAL_KEYS = ("knowledge",)` — a key in this set is no longer an
  "unknown key" refusal; its ABSENCE stays fine on every row, and a key in
  neither set still refuses loudly (the strict posture is unchanged — that is
  the entire point of a *declared* optional set over a loosened check).
- `OPTIONAL_KEY_VALIDATORS["knowledge"]` (`_validate_knowledge`) refuses a bare
  string, a present-and-empty list, and a non-string/blank entry, each naming
  `` `knowledge` `` by name in the message — never a generic "malformed row".
- `_hat_from_row` parses a present optional key into the hat dict; an absent
  one is never defaulted to `""`/`[]`, so `set(hat) == {...}` pins elsewhere in
  the suite (the template/instance STRUCTURE test) are untouched by a
  mechanism no live row uses yet.
- `hats.py list` and `_cmd_applicable` (via `brief_block`) print the field
  where a row carries it and stay silent where it does not.

**The shipped template**, `project-trajectory/registries/hats.template.toml`,
gained a commented explanation of the key — no row fills it in. **This repo's
own `docs/requirements/hats.toml` is untouched**: no `knowledge` values were
added, per the owner's explicit instruction — the mechanism ships EMPTY here,
and the value-filling pass is the owner's, not this session's.

**WI-484's spec (item 5) and `docs/status.md`'s wi484 bullet** are both
updated in the same commit: the blocker's mechanism half is DONE, and what
phase 4 still awaits is the owner's own `hats.toml` value pass, not a next
worker slice.

**Adopter surface**: `project-trajectory/RESYNC_PACK.md` gained an entry
(`[since 46dcac8a]`, the commit preceding this one) describing the change and
what an adopter must do (nothing mechanical; add `knowledge` only if wanted).

**A real commit-bar blocker found and fixed, not deferred.** Moving this WI's
own spec straight to `docs/archive/work/complete/` while bumping the id
watermark to WI-511 IN THE SAME COMMIT hit `trace.py --strict-integrity`'s
watermark-raise rule: it refused the raise as unjustified. Root cause —
`_wi_ids` (feeding `live_max_ids`) only ever scanned `docs/work`, never its
archive sibling `docs/archive/work` (WI-504 relocated terminal WI history one
directory deeper months before this session; `kitlib.registry.spec_roots`
already exists as the one home for "both are one registry", but `_wi_ids` was
never repointed at it). The prior same-session mint-and-close precedents
(WI-509, WI-510) never hit this: their watermark bump landed in the MINT
commit while the spec still sat under `docs/work/queued/` (which the old scan
did see), and the archive move happened in a LATER commit where the mark did
not need to rise again — a direct mint-to-archive in one commit, which is
exactly the pattern this WI's own task asked for, was the first thing to
exercise the gap. Fixed by routing `_wi_ids` through
`kitlib.registry.spec_roots(docs / "work")` instead of a hardcoded
`docs / "work"`. `tests/test_module_size_ratchet.py`'s `trace.py` baseline
re-stamped +6 (5316 -> 5322), reason recorded at the entry. Regression
pinned: `tests/test_id_watermark.py
::test_live_wi_ids_are_counted_under_the_archive_sibling_too`.

**Tests** (`tests/test_hats.py`, in-process, smoke-tier): a declared optional
key absent loads clean and carries no such dict key; present and well-formed
is parsed, order-preserved-and-stripped, and surfaces on `brief_block`/`list`;
five malformed shapes (bare string, empty list, non-string entry, empty
string entry, whitespace-only entry) each refuse naming `` `knowledge` ``; an
unrelated unknown key (`notes`) still refuses by name, proving the optional
set does not loosen the general check; the CLI `list` command prints the
`knowledge:` line only on the row that carries it.

Deviations from spec: one, found and fixed rather than deferred — the
`trace.py _wi_ids` archive-scan gap above, hit by this WI's own close.
Everything else landed exactly as scoped: `knowledge` values were
deliberately not filled into this repo's live roster, per the owner's
directive that the field is owner text.

Gates, real output on this box (final run, tree includes the `trace.py` fix):

- `python -m pytest -q -n auto -m smoke` -> **1311 passed, 5 skipped in
  26.38s** (+1 over the mechanism-only run: the new watermark regression
  test).
- `python scripts/check_smoke_budget.py --mode enforce` -> **smoke wall-clock
  budget: 18.7s vs 60s budget -> within**.
- `python project-trajectory/scripts/check_docs.py --root . --stale` -> **OK -
  1044 doc(s), 1356 intra-repo link(s), 0 broken** (staleness hints are
  pre-existing, none naming a file this session touched).
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` ->
  **clean (508 work item(s), 482 done (95%), 21 cancelled, graph acyclic)** —
  all WARN lines pre-existing (arch-map connectivity, IF/TC coverage gaps,
  WI-508's own staleness against SR-163, title-length hints); none newly
  introduced by this WI.
- `python -m pytest -q -n auto -k "test_id_watermark or test_trace"` (the
  watermark/trace suites, standalone) -> **200 passed, 1 skipped, 22
  deselected in 244.04s** — confirms the `_wi_ids` fix against its own
  siblings before the full run below.
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp-hats` (full,
  unfiltered, mechanism-only tree, before the `trace.py` fix) -> **2986
  passed, 14 skipped in 1170.36s (0:19:30)**.
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp-hats2` (full,
  unfiltered, FINAL tree including the `trace.py` fix) -> **2987 passed, 14
  skipped in 1283.55s (0:21:23)** — clean; the +1 over the mechanism-only
  run's 2986 is exactly the new watermark regression test.

Deferred open items: none — the mechanism is complete as scoped, the
watermark gap found along the way was fixed rather than deferred, and the one
thing left (filling `knowledge` values into `docs/requirements/hats.toml`) is
an owner act stated explicitly in WI-484's own spec, not an open question this
session leaves unrecorded.
