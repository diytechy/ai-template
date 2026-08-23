+++
id = "WI-503"
title = "The re-attestation brief splits: a regenerated CURRENT.md plus dated briefs that are immutable once minted"
specref = ""
workstream = "scripts"
sr_refs = ["SR-178"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Both Done-when surfaces built and driven; every Done-when bullet is a passing
test.

**The split.** `docs/ratify/CURRENT.md` is now the ONE file
`trace.py --ratify modified` ever regenerates — `current_ratify_brief`
(`project-trajectory/scripts/trace.py`) replaces the retired
`newest_ratify_brief` "pick the newest filename" rule with a fixed path, and
the `--check`/`--out`-less default resolves there. A dated
`docs/ratify/<date>-<slug>.md` is now MINTED, never hand-written:
`trace.py --mint-ratify-brief SLUG [--mint-date DATE]` copies `CURRENT.md`
to the dated name and refuses (i) with no `CURRENT.md` to mint from and
(ii) when the destination already exists — a dated brief cannot be minted
twice. The seam lives in `trace.py` itself (`mint_ratify_brief` +
`_cmd_mint_ratify_brief`), the smallest-total-code home: the mint is a plain
file copy over machinery (`current_ratify_brief`, the CURRENT.md path) this
module already owns, so a sibling script would duplicate that path
knowledge and `intake.py`'s writers are all registry-shaped, not a byte
copy of a rendered view.

**The immutability enforcer.** `check.py`'s new `ratify_immutability`
(`--ratify-immutable`, step `ratify-immutable` in `steps()` and
`BUILTIN_STEP_NAMES`) is `staged_divergence`'s sibling — same read (`git
diff --cached`, degrading cleanly off-git/outside-checkout/wrong-root) but
the opposite question: not "did you forget to stage a regeneration" but
"does this commit rewrite a dated brief that already exists". It reads
`--name-status --no-renames` on the staged tree and refuses any status other
than a plain `A` (add) on an existing `docs/ratify/<date>-*.md` (excluding
`CURRENT.md`/`README.md`) — fail-closed by default, no `--strict` switch,
because the property guarded has no honest warn-through state. Wired into
`hooks/pre-commit`'s batched floor beside `ratify-fresh`/`staged-divergence`
and the built-in `steps()` plan (both bars — never stood down on a work
branch, the same reasoning `staged-divergence` states: it reads the staged
tree, not a regenerated artifact's freshness).

**`ratify-fresh` still fails closed**, now comparing `CURRENT.md`:
`ratify_check`'s default out-path (no `--out`) is `current_ratify_brief(root)
or .../CURRENT.md`, so a stale `CURRENT.md` still reds the gate and an
absent one (or a closed re-attest window) is still the arming idiom's silent
no-op.

**`docs/stack.ini`'s `[generated]` row is UNCHANGED in value** —
`docs/ratify/ = ratify` was already a directory prefix, so it already
covered one regenerated file plus N immutable ones without an edit; its
comment now states that split explicitly, and so does the freshly reasoned
`staged-divergence` interaction (CURRENT.md is the only member ever
"regenerated but unstaged"; a dated file showing divergence is already the
`ratify-immutable` violation, caught by its own step).

**`gen_open_items.py`'s summary needed no change**: it computes the
pending/attested projection from `trace.reattest_model` directly (registry
state), never from a `docs/ratify/*.md` file path, so the split does not
touch it — confirmed by re-running its `--check` and reading the rendered
page.

**Scaffold surface: no change owed.** `bootstrap.py` MAPPING ships nothing
under `docs/ratify/` (grepped, confirmed), so `tests/test_bootstrap.py`'s
file lists are untouched. A `project-trajectory/RESYNC_PACK.md` entry is
added (`docs/ratify/` splits: a regenerated CURRENT.md plus immutable dated
briefs `[since d08b5bd2]`) matching the newest entries' `[since <sha>]` form.
The shipped `gate-advance` skill (neutral source
`project-trajectory/skills/gate-advance/SKILL.md`) is corrected — it used to
recommend `--out docs/ratify/<date>-reattest.md` directly, exactly the
anti-pattern this WI fixes — and the two fan-out copies
(`.claude/`, `.agents/`) are refreshed via `bootstrap.py --sync`
(`gen_skills_index.py --check-agents` confirmed fresh after).
`docs/ratify/README.md` and `docs/registry-machinery-reference.md`'s command
reference are updated to the new two-step workflow.

**Repo dogfooding.** `docs/ratify/CURRENT.md` is regenerated and committed
(the window is currently closed — "No spine row differs" — so this seeds the
live surface rather than recording a pending re-attest).

**Deviations from spec.** None load-bearing. One incidental fix bundled in
because it directly blocked driving the mint CLI's failure path as a test:
`trace.py main()`'s `_writer_mode` dispatch used a bare `return` where
`main()` is called bare (`main()`, not `sys.exit(main())`) at the bottom of
the module — so a WRITER's failure exit code (`--correct-mark`,
`--bump-ids`, now `--mint-ratify-brief`) was silently swallowed and the
process always exited 0. Changed the one line to `sys.exit(writer_code)`,
matching the `--ratify --check` path's own documented reasoning three lines
above it in the same function.

**Gates.** Commit-bar smoke: `1397 passed, 5 skipped in 61.56s` (`python -m
pytest -q -n auto -m smoke`, `.venv/Scripts/python.exe`); full suite pasted
at close. `check_docs.py --root . --stale`: the 4 broken links + 1 orphan
this run reports pre-date this branch (`git stash` confirms — all reference
the already-closed WI-390 program) and are outside this WI's scope.
`check_trajectory.py --strict`: clean, exit 0 (the filename-stem WARN this
WI's own spec carried is resolved by this same close's rename). Module-size
ratchet re-stamped: `check.py` 2176 -> 2326 (net +150 after a `ruff format`
tightening), `trace.py` 5361 -> 5457
(+96), reason recorded at each entry and in the log fragment. Smoke
membership untouched — every new test lives in `test_trace_briefs.py` /
`test_check_harness.py`, both already in `conftest.SLOW_MODULES`.

**Deferred open items: none** — every Done-when bullet is driven, the two
declared trunk-lane wiring points (`hooks/pre-commit`, `steps()`) are both
updated, and the scaffold-surface / RESYNC-pack items the spec flagged as
"if bootstrap ships anything" resolved to "nothing to do", confirmed rather
than assumed.

## Context

Minted at the WI-498 program close from ROUND-OPUS finding 13, assessed
there as too large to fold into the close (it moves a gate that
deliberately fails CLOSED because a human is about to attest) and recorded
as a row rather than a deferral.

**The defect.** `docs/ratify/*.md` briefs are DATED and NAMED for the
sitting that minted them, and are read as the record of what was owed at
that moment — but `trace.py --ratify modified` regenerates the NEWEST brief
IN PLACE (`newest_ratify_brief` picks the newest by filename, and
`ratify_check` regenerates and byte-compares it). So a dated file keeps
being rewritten until a newer date is minted.

Measured: `docs/ratify/2026-08-13-wi444.md` is dated 2026-08-13 and named
for WI-444, and its content at the WI-498 close was the WI-498 drift —
`SR-049`/`SR-140`/`SR-170`/`SR-173` sections, a baseline stamped
`2026-08-20 (a5471e0f)` and an approval provenance of `1a7984ea
(2026-08-21)` — with nothing about WI-444 in it. `git log` on that path
shows **ten** rewrites; `c170da9f` alone added 77 lines to it.

This is pre-existing machinery behaviour, NOT something WI-498 introduced.
It is filed here because the program wrote into that file and because an
attestation record that is mutable until superseded cannot answer the one
question it exists for: *what was the human shown when they signed?*

**The design (Opus's, adopted as the spec).**

- `--ratify modified` regenerates an UNDATED `docs/ratify/CURRENT.md` — the
  live surface, always the working tree's answer, and the artifact the
  `ratify-fresh` freshness gate compares. That gate keeps its fail-closed
  posture and its reason: a stale brief is read by a human about to attest.
- A DATED brief is MINTED from `CURRENT.md` at a sitting and is IMMUTABLE
  once written. Regeneration never touches a dated file again.
- The immutability needs an enforcer, or it is a convention that rots like
  the byte baselines did: a check that refuses a commit whose diff modifies
  an existing `docs/ratify/<date>-*.md`, with the mint itself the one
  permitted writer.

**Surfaces this moves, so the size is not rediscovered mid-flight:**
`trace.newest_ratify_brief` / `ratify_check` / `reattest_lines`;
`check.py`'s `ratify-fresh` step; the `[generated]` census row
`docs/ratify/ = ratify` in `docs/stack.ini` (it declares a PREFIX, which
would now cover one regenerated file and N immutable ones — the
staged-divergence detector reads that same row); `gen_open_items`, which
renders the baseline/attestation-depth summary; `bootstrap.py` MAPPING and
`tests/test_bootstrap.py` file lists if the scaffold ships a seed brief;
the existing dated briefs, which stay exactly as they are (they are
history, and rewriting them is the defect); and a RESYNC_PACK entry,
because an adopter's `docs/ratify/` layout changes.

## Done-when

- `--ratify modified` writes `CURRENT.md`; no dated brief is ever rewritten
  by a regeneration, driven as a test.
- A test asserts the immutability enforcer REFUSES a modification to an
  existing dated brief and PERMITS the mint.
- `ratify-fresh` still fails closed on a stale `CURRENT.md`.
- `docs/stack.ini`'s `[generated]` row and the staged-divergence detector
  agree with the new layout.
- RESYNC_PACK entry written; `check_docs --stale` 0 broken.
