# WI-393 — REVIEW-A (2026-08-01)

Verdict: APPROVE — I drove the ritual myself, forged claim commits against the
oracle, and re-ran every registered bar. The deliverable's central claims all
reproduced; what I broke is confined to the whitespace/EOL margin of the
oracle's conviction property and to link-grammar corners the restored originals
carried byte-identically. Findings below, severity-ordered; none blocks.

Reviewed: branch `wi-393-rehome-the-link-aware-archival-ritual` at `3497fada`
(work `9b91e04f` + close), trunk `ConcurrencyTrainRewrite`. All commands run
under `/Users/diytechy/Documents/ai-template/.venv/bin/python` from the
worktree. Per the brief, `docs/log.d/` fragments were not read.

## What I verified before hunting

Drove the archival in a scratch git repo carrying every documented class —
inbound links from three depths with `#fragment`s, outbound relative links, a
CRLF file, an external URL, a protocol-relative URL, a root-relative link, a
bare anchor:

```
spec_move: docs/specs/WI-777.md -> docs/archive/specs/WI-777.2026-08-01.md
spec_move: relinked README.md
spec_move: relinked docs/archive/specs/WI-777.2026-08-01.md
spec_move: relinked docs/crlf.md
spec_move: relinked docs/log.md
spec_move: relinked docs/reviews/R.md
```

Every class behaved as documented: outbound targets re-relativised one deeper
(`[log](../../log.md)`), fragments carried (`[anchor](../../log.md#anchor)`,
inbound `[its bar](archive/specs/WI-777.2026-08-01.md#done-when)`), link text
untouched, external/protocol-relative/bare-anchor untouched, root-relative
untouched in the rebase half, CRLF preserved byte-for-byte (`od -c`:
`... 1 . m d ) \r \n`), and everything staged as one changeset
(`git status --porcelain`: `R docs/specs/WI-777.md -> docs/archive/...` plus
four `M` relinks, nothing dirty).

## Findings

**1. MODERATE — the oracle's "byte-for-byte" conviction has a whitespace/EOL
blind spot; a whitespace-only or EOL-relay hand edit in a claim-shaped commit
is excused and destroyed with the branch.** `_relinked_exactly` reads both
sides through `ac.git(root, "show", ...)`, and `ac.git` (agent_common.py:1113)
does `out = (proc.stdout or "").strip()` on a `text=True` subprocess —
leading/trailing whitespace is stripped and universal-newlines decode maps
`\r\n`/`\r` to `\n` on both sides before the compare. I forged four
claim-shaped commits (exact `_claim_subject`, real `spec_move.move_spec` move
pair, one commit past trunk) and ran `integrate._abandoned_claim` on each:

```
genuine-relinked-claim       _abandoned_claim -> True
one-extra-md-byte            _abandoned_claim -> False
trailing-newline-only        _abandoned_claim -> True
crlf-relay-hand-edit         _abandoned_claim -> True
```

The both-ways claim holds for every semantic byte (one mid-file byte convicts,
the genuine relink is excused — the builder's tests
`test_a_crashed_claim_that_relinked_docs_is_still_re_cut` and
`test_an_md_edit_that_is_not_the_relink_still_convicts` are honest), but a
hand edit consisting only of appended blank lines, or a whole-file CRLF→LF
relay, rides through as "relink-identical" and the branch carrying it is
deleted and re-cut. No semantic content can slip (strip touches only the
string's ends; EOL translation is content-preserving on decode), and the harm
direction is deletion of a whitespace-only edit — never a false merge, never a
false green. But this repo's own discipline (WI-234/WI-337) treats line
endings as load-bearing, so an EOL relay is a real content change the oracle
cannot see; and the word "byte-for-byte" in the `_relinked_exactly` docstring,
the integrate.py size-stamp entry, LLR-145's Detail cell, and commit
`9b91e04f`'s message overstates what is actually compared
(stripped-and-EOL-normalised text). Remedy owed (follow-up, not this row):
read both sides raw (`git cat-file blob` bytes, or strip()-free capture) so
the stated property is the implemented one — the fix is confined to
`_relinked_exactly`'s two reads. -> follow-up WI or docstring narrowing ->
@owner.

**2. MINOR — the rewriter's link grammar diverges from `check_docs`'s in both
directions at four corners; all four are byte-faithful restorations of the
WI-288/WI-353 originals the spec demanded verbatim.** I drove reference-style
links, fenced examples, angle-bracket targets, and titled links through an
archival, then ran the real `check_docs`:

- *Angle-bracket target in the moved file is mangled, not missed*:
  `[ang](<../log.md>)` (valid under check_docs's own
  `LINK_RE = ...(<[^>]*>|[^)\s]*)...`) became
  `[ang](../../specs/<../log.md>)` — the rebase treated `<../log.md>` as a
  path and prepended the prefix outside the brackets. Caught late as
  `check_docs: FAIL - ... broken link -> ../../specs/<../log.md>`, so a
  bar-green link becomes a bar-red one after the move.
- *Inbound angle and titled targets are missed* (left pointing at the vacated
  path) — caught by check_docs as broken; the titled-link exclusion is
  documented at `_MD_LINK_TARGET_RE` (WI-288's own comment), the angle miss is
  not.
- *Reference-style definitions (`[x]: path`) are missed both ways and the miss
  is silent* — check_docs flagged neither the moved file's stale
  `[refstyle]: ../log.md` nor the inbound `[inboundref]: specs/WI-888.md`,
  i.e. the bar shares the blindness, so nothing detects the break.
- *Links inside code fences and inline code ARE rewritten* although check_docs
  strips fences/inline-code before checking: a fenced documentation example or
  a review quoting a link verbatim as evidence is silently altered by any move
  that remaps its target (I confirmed `[ex](../log.md)` inside a ```` ``` ````
  fence was rewritten to `[ex](../../log.md)`).

I diffed the restored primitives against the pre-Phase-5 dispatcher
(`git show 31ad569d^:...agent_dispatch.py`): `_MD_LINK_TARGET_RE`
(`(\]\()([^)\s]+)(\))`), `_URL_SCHEME_RE`, and the `_relink_archived_specs`
traversal (rglob, `.git`/`node_modules` exclusions) are byte-identical, so
these are inherited boundaries, not regressions — and the spec scoped the row
to "the discipline the originals carried ... verbatim". The breaking corners
land in the bar (late red, the pre-existing surface shape); the silent corners
sit outside the bar's grammar on both sides. Worth a comment in spec_move.py
naming the angle/reference-style boundary honestly. -> no remedy owed this
row -> @owner.

**3. MINOR (pre-existing) — the oracle never verifies the moved spec's own
content.** `_claim_delta` records the `A` under `active/<branch>/` as the move
destination but nothing compares its content: a claim-shaped commit whose
*spec file itself* carries a hand edit is excused and deleted exactly as
before WI-393 (the bare-`git mv` era checked no content either). WI-393 makes
dest content legitimately differ from src (the outbound rebase), so the old
implicit equality can never return — but the same module now provides the
closing tool: dest could be checked against `rewrite_text` over
`_rebased_link_target`, the mirror of what `expected_relink` does for the
inbound half. Unchanged width, harm direction is deletion (never a merge), so
advisory only. -> no remedy owed this row -> @owner.

**4. INFO — the indivisibility claim is API- and commit-level, not
crash-level, and the shipped wording stays honest about it.** Read honestly:
`_place_moved_file` runs `git mv` (stages the rename immediately), then the
two relink passes write and stage; a process kill in that window leaves the
two-thirds state — a staged move with stranded links — in the *working tree*.
Nothing committed can hold it: `claim()`'s regen/tree/commit failures all
`git reset --hard`, a kill leaves a dirty trunk the next claim's
`working_tree_dirty` rung refuses by name, and the branch/trunk writes happen
only after the whole ritual. The handback's `new_text` path writes the
destination before removing the source, so its crash residue is a duplicate
(fail-safe), not a loss. The load-bearing claims as written — "no caller can
perform two-thirds of it", "no two-thirds state can reach trunk"
(test_claim_runs_the_link_aware_move_ritual) — are accurate; only a stronger
reading ("crash-atomic") would be false, and nothing in the diff claims it.
-> no remedy owed -> @owner.

**5. INFO — the RULING-6 deviation (audit allowed-set not widened) is honestly
scoped and fail-closed; no claim can exploit it today.** The window audit
(`integrate.audit`) still allows only `BOOKKEEPING_PREFIXES`
(`docs/work/`, `docs/log.d/`, `docs/log.md`) plus the declared `[generated]`
set, and its docstring already reserves widening as an owner ruling. Not
widening means the new failure mode is a false *positive*: a claim whose
inbound relinks touch a non-bookkeeping, non-generated path (e.g. `README.md`
or `docs/reviews/`) will be flagged at the end of the merge drain
(`the RULING-6 window audit flagged this run's own history`) and stop the run
loudly — operational friction, not a hole; the allowed set excuses nothing it
did not before. The exposure is narrowed further by the repo's own convention
(the drain plan deliberately un-linked its row table for exactly this reason).
The deviation's record is stated to live in the WI's log fragment, which this
review did not read per its brief; judged on the code, the scoping is the
conservative one. -> owner ruling stands -> @owner.

## Mandatory bars (all run in the worktree at `3497fada`)

- Covering tests: `pytest -q tests/test_spec_move.py tests/test_handback.py`
  → `30 passed in 4.13s` (test_spec_move contributes 16 — all smoke:
  `pytest -q tests/test_spec_move.py -m smoke --collect-only` →
  `16 tests collected`); `pytest -q tests/test_integrate.py` →
  `107 passed in 36.63s` (`-k claim`: `33 passed, 74 deselected`).
- Smoke tier: `pytest -q -n auto -m smoke` → `598 passed, 2 skipped in 9.55s`
  (builder recorded 594/6; totals agree at 600 — the delta is env-gated
  skips).
- `check_trajectory.py --root . --strict` → rc=0,
  `clean (400 work item(s), 373 done (93%), 17 cancelled, graph acyclic)`
  (WARNs only, all pre-existing classes; `scripts/spec_move` joins the same
  undeclared-IF WARN family as `scripts/drive`/`scripts/handback`).
- `check_doc_refs.py --root . --strict` → rc=0,
  `no dangling path or sym: references · 856 untraced (explained...)`.
- `trace.py --root . --strict-integrity` → rc=0,
  `SN=25 SR=135 LLR=128 TC=125 orphans=0 integrity=0`.
- `ruff format --check` over the six touched py files →
  `6 files already formatted`.
- Spine rows: LLR-145's Module/CodeSymbol name real code
  (`move_spec`/`expected_relink`/`archive_dest` all exist in spec_move.py;
  arch map row + `handback -> spec_move`, `integrate -> spec_move` edges
  present in docs/architecture.md), TC-139's Evidence
  (`tests/test_spec_move.py`) exists and passes (16), cell shapes match the
  TC-137/TC-138 conventions (Tier=Full, Status=Verified, Phase=4). SR-132 is
  genuinely the owning SR (its Requirement owns the serial claim move and its
  AcceptanceCriteria's "A claim moves the spec..."; LLR-144/handback sits
  under it by the same reasoning). Filing NEW rows at build time follows the
  WI-387 precedent (`4b4f29d6` filed LLR-144 + TC-138 on a work branch) and
  the Class B registration argument; `staged_spine_amendments` skips NEW rows
  by construction (`head is None → continue`) and no existing row's cells were
  amended (system-requirements.csv untouched), so no un-ratified spine change
  occurred.
- Size stamps: `wc -l` → integrate.py 1946, bootstrap.py 2257 — both exact
  against the new BASELINE entries, both entries name the WI and reason per
  the ratchet's own escape-hatch rule; spec_move.py at 368 sits far under
  THRESHOLD=1500 (no stamp owed); `pytest -q tests/test_module_size_ratchet.py`
  → `1 passed`.
- Mechanical close: R-A Deliverable true to the diff (16 smoke tests, cli 86 +
  link-rebase census rows, README/bootstrap/arch-map/gate/dashboard all in the
  diff as claimed); R-F satisfied — the closed spec's frontmatter carries no
  `specref` and the close commit records why nothing archives; the docs/work
  delta is a single `R061` move of WI-393's own spec (no WI id minted; the
  only new ids are the two spine rows, which R1 does not govern).

VERDICT: APPROVE findings=5
