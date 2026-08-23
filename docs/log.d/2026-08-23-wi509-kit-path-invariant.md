## 2026-08-23 — WI-509: pin the kit-path invariant and document where the machinery lives

Executed OI-59 ruled (a)+(c) (docs/log.d/2026-08-22-oi55-59-rule.md): `bootstrap.py`
stays out of its own `MAPPING` (verified, and now asserted by the pin — the
bundle IS the kit folder), and the recurring defect class WI-498's slice-5
recovery hit live — an instructing surface addressing bootstrap/migration
machinery at a SCAFFOLD path the adopter does not have — is made unrepresentable
by a swept, mechanically-armed test. (b), a second installer copy shipped into
the scaffold, was DECLINED per the ruling; no such prose was found to remove.

**The pin — `tests/test_kit_path_invariant.py` (new, in-process, smoke-tier by
default; not filed into `conftest.SLOW_MODULES`).** Two tiers, because the kit
ships bootstrap instructions from two different assumed working directories:
**STRICT surfaces** — every file `bootstrap.py`'s own `MAPPING` (read live from
`bootstrap.py`, not hand-listed) copies or generates into an adopter's
scaffolded repo, plus `RESYNC_PACK.md` (its recipes run standing in an
ALREADY-ADOPTED repo) — must never use a bare `scripts/bootstrap.py`; every
invocation must spell `project-trajectory/scripts/bootstrap.py`. **FRAMED
surfaces** — `ADOPTING.md`, the kit's own root `README.md`, `KICKOFF_PROMPT.md`
— are read with the kit itself as the CWD, so a bare invocation is legal there
only when the same sentence names the CWD explicitly ("kit folder", "kit
checkout", "from this kit", "from inside it"). `bootstrap.py`'s own docstring
is exempt by construction (it is not a MAPPING destination and not a FRAMED
surface — the machinery describing its own invocation, not an instruction
pointing at it from elsewhere). A third test asserts `bootstrap.py` stays out
of its own `MAPPING`, and a fourth confirms the two flags OI-59's ruling names
(`--migrate-config`, `--sync`) are still present in `bootstrap.py`'s own
`argparse` surface, so the pin's flag references cannot silently drift from
the one home for the inventory they describe.

**fig:** swept population = every `bootstrap.py` `MAPPING` source (129 pairs,
`python project-trajectory/scripts/bootstrap.py -c "..."` reads the live list)
+ `RESYNC_PACK.md` (STRICT) + `ADOPTING.md`/root `README.md`/`KICKOFF_PROMPT.md`
(FRAMED) — `python -m pytest tests/test_kit_path_invariant.py -v` (this commit).
**Offenders found and fixed in the same commit: 8**, all bare
`python scripts/bootstrap.py` invocations with no kit-folder framing, the
armed-on-a-clean-baseline case the WI asked for:

- `project-trajectory/scripts/agent_common.py` — 3 runtime remediation
  messages (`--migrate-config` printed on a legacy-key/legacy-ordinal read and
  on a mixed-config finding).
- `project-trajectory/hooks/pre-commit`, `hooks/commit-msg`, `hooks/pre-push`
  — the `mixed_config_refusal` remediation `echo` line, identical in all three.
- `project-trajectory/process.toml.template` — 2 comment sites (the `[MIGRATION]`
  header note and the 0-4-ordinal translation note).
- `project-trajectory/PROCESS_OPTIONS.md` — the "one policy home" paragraph's
  `--migrate-config` command.
- `project-trajectory/RESYNC_PACK.md` — 2 sites ("One policy home" §3 step,
  and the gate-tag-retirement recipe's `--sync` step); both now carry the same
  explicit "from your kept kit checkout" framing the pack's *own* later entries
  (the `docs/gate` re-key steps) already used, closing the inconsistency within
  the pack itself.

Also fixed, out of the pin's swept surface but the same live defect: this
repo's own dogfooded `docs/process.toml` (2 comment sites, generated from
`process.toml.template` before this fix). `ADOPTING.md`, the kit's own root
`README.md`, and `KICKOFF_PROMPT.md` were inspected and found already correctly
framed ("From the kit folder:", "from this kit, run", "from inside it") — no
change needed there; the FRAMED-tier test passes them as-is.

**The paragraph — ADOPTING.md §1, "Where the machinery lives"** (placed
immediately after the §1 scaffold command it explains): the kit folder is the
tool, the scaffolded repo is the product; keep the tool (conventionally at
`project-trajectory/`) so later resync/migrate keeps working; deleting it after
init forfeits resync/migration by design; a second installer copy was
considered and declined (OI-59 option (b)) because two installers drift.
`ADOPTING.md` is not byte-capped, only kept tight (byte-budget-guard skill).

Deviations from spec: none — both named deliverables (the pin, the paragraph)
landed as scoped; (b) was already absent from the kit's prose, so there was
nothing to remove.

Byte deltas on watched/capped files: `project-trajectory/PROCESS_OPTIONS.md`
177,704 -> 177,715 bytes (**+11**, watched not capped) — the two bare
`scripts/bootstrap.py` migration commands in its config-migration paragraphs
now spell the kit-relative path. `PROCESS.md` untouched by this WI (85,862
bytes on this tree, pre-existing drift from its own stamped 85,889 baseline —
not this WI's change, not re-stamped here). `AGENTS.template.md` and `CLAUDE.md`
untouched. `byte-budget-guard/SKILL.md` itself (capped at 5,000): 4,825 ->
4,835 bytes (**+10**, converged after re-stamping its own baseline row
alongside the `PROCESS_OPTIONS.md` row it tracks — a self-referential fixed
point, resolved by measuring after the edit rather than before), re-stamped in
`project-trajectory/skills/byte-budget-guard/SKILL.md` +
`.agents/skills/byte-budget-guard/SKILL.md` +
`.claude/skills/byte-budget-guard/SKILL.md`, all three byte-identical.

Ratchet re-stamped deliberately: `tests/test_module_size_ratchet.py`
`agent_common.py` baseline 2,631 -> 2,634 (+3; the three remediation messages'
wording grew by the kit-relative path text — comment/string-literal only, zero
behavioural change).

**A second, pre-existing test-fixture bug found by the full-suite run and
fixed in the same commit** (`tests/test_traj_views.py::test_when_and_how_...`):
its `_real_repo_snapshot` helper copies `docs/work` into an isolated tmp_path
to read this repo's own live WI registry without a torn-read race, but never
picked up `docs/archive/work` — the terminal sibling `read_registry_rows`
has unioned in via `kitlib.registry.spec_roots` since the WI-504/OI-55 archive
split. The gap was invisible while this repo's OPEN WI population stayed
diverse enough (>3 distinct phases or workstreams) to clear the test's own
drill-vs-flat threshold on its own; closing WI-509 thinned the open set to 4
WIs whose workstreams collapsed to 3, which is an ordinary, expected
consequence of closing a WI, not a defect in this WI's own change. Fixed by
adding `"docs/archive/work"` to `_REAL_ROOT_INPUTS`, restoring what the
snapshot was always supposed to mirror.

Gates, real output on this box:

- `python -m pytest -q -n auto -m smoke` -> **1270 passed, 5 skipped in 24.51s**
  (re-confirmed after both fixes above; smoke does not carry either affected
  test — `test_bootstrap`/`test_traj_views` heavy siblings are in
  `conftest.SLOW_MODULES`, and the byte-cap pin is in-process and fast, so this
  reading predates and postdates the two fixes identically).
- `python scripts/check_smoke_budget.py --mode enforce` -> **smoke wall-clock
  budget: 24.9s vs 60s budget -> within**.
- `python project-trajectory/scripts/check_docs.py --root . --stale` -> **OK -
  512 doc(s), 1315 intra-repo link(s), 0 broken** (the "possibly stale" hints
  are pre-existing links into files this WI did not touch; none name a file
  this session edited).
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` ->
  **clean (507 work item(s), 480 done (95%), 21 cancelled, graph acyclic)**.
- `python project-trajectory/scripts/check.py --jobs 0` -> **RESULT: PASS**
  (11 steps).
- `python -m pytest -q -n auto` (full, unfiltered), first run on the tree
  before the two fixes below landed -> **2906 passed, 14 skipped, 2 failed in
  1077.67s (0:17:57)** — `test_capped_doc_baselines_match_the_real_sizes`
  (this session's own byte-budget-guard re-stamp was one edit short: the
  `PROCESS_OPTIONS.md` row was corrected but the file's own capped row was
  not, so its declared baseline no longer matched its real size) and
  `test_when_and_how_drills_use_bounded_orthogonal_wires_and_explicit_ports`
  (the pre-existing `_real_repo_snapshot` gap above, exposed — not caused —
  by closing WI-509). Both fixed in this commit.
- `python -m pytest -q -n auto` (full, unfiltered), re-run on the landed tree
  -> **2908 passed, 14 skipped in 1047.15s (0:17:27)** — clean, and the +2
  over the first run's 2906 is exactly the two tests above flipping to pass.

Deferred open items: none — the ruling this WI executes was already made in
full, (b) was declined with nothing left to remove, and no new decision was
surfaced.
