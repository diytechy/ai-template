## 2026-08-22 — WI-504: terminal WI history relocates to docs/archive/work/

Executed OI-55's ruled (a) shape in full: the registry readers were taught
BOTH roots before the move, the ~495 terminal files moved whole in one `git
mv` per status directory, the link sweep ran, tombstone READMEs went into the
vacated directories, and the scaffold surface (bootstrap, templates,
RESYNC_PACK.md) was updated so a fresh adopter gets the new shape directly.

**Files moved**: **495** (472 `complete/`, 21 `cancelled/`, 1 `partial/`, plus `partial/.gitkeep`) — fig: cmd="git diff --name-status d6818b0b0e2bfcd2568c9547483976f3836b0752 -- docs/archive/work | grep -c '^[AR]'" rev=d6818b0b0e2bfcd2568c9547483976f3836b0752

**Readers taught** (both roots valid — `docs/work/` and its `docs/archive/work/`
sibling read as ONE registry):

- `scripts/kitlib/registry.py` — `read_spec_rows` now unions `work_dir` and
  its new `spec_archive_dir`/`spec_roots` sibling; `spec_files` stays
  single-root (the narrower primitive some callers still want undiluted).
  Every consumer that already funnels through `read_spec_rows` — `schedule.py`'s
  done-set, `check_trajectory.py`'s registry, `agent_common.py`, `intake.py`'s
  dedup and mint — inherited the fix with no call-site change.
- `scripts/check_trajectory.py` — `_head_spec_status_map`'s HEAD `ls-tree`
  read and `_staged_spec_registry`'s staged-diff gate both scan `WI_WORK` AND
  the new `WI_ARCHIVE_WORK`, so a close that lands in the archive is still
  visible to the staged-registry (no-validation-delta) ratchets.
- `scripts/integrate.py` — `branch_outcomes` reads both `WORK` and the new
  `ARCHIVE_WORK` prefix (the outcome-dir index differs per prefix — stated
  per-prefix, not assumed constant); `docs/archive/work/` joined
  `_ADJUDICATION_SURFACES` so a disposition lane's own terminal move does not
  fall off the no-bar path.
- `scripts/intake.py` — new `_terminal_hits` helper (unions `WORK`/`ARCHIVE_WORK`
  for one status dir) now backs `_closed_spec` (disposition-mint arm),
  `_disposition_drafts` (the clean-close spot-check arm), and `_cmd_sweep`
  (the by-hand recovery sweep); `next_wi_id`'s filename sweep for id-taken
  also scans both roots (the watermark stays the primary floor).
- `scripts/check.py` — `docs/archive/work/*` joined the doc-navigability
  `--ignore` list beside `docs/work/*` (a closed spec's body is DATA, not
  navigable prose, wherever it lives).
- `scripts/bootstrap.py` + `orphans-allow.template` +
  `work/README.template.md` + `work/WI-000.template.md` — a **fresh** scaffold
  now ships the new shape directly: `docs/work/{draft,active,deferred}/` plus
  `docs/archive/work/{partial,cancelled,complete}/`, no migration step needed.
- `project-trajectory/RESYNC_PACK.md` — one new §3 entry (`[since d6818b0b]`)
  with the one-command `git mv` migration recipe for an already-adopted repo.
- `scripts/traj_panels.py` — the dashboard's outcome cards now link into
  `docs/archive/work/<outcome>/`, not the tombstoned old path.
- `scripts/check_vocab.py` — the generic `docs/archive/*` exemption already
  covers the new home; the three pre-migration `docs/work/{partial,complete,
  cancelled}/*` rows STAY (never-rewrite-history: a citation of the old path,
  in this repo's own record or a downstream repo mid-migration, must keep
  reading as history).
- `docs/orphans-allow` (this repo's own instance) — `docs/archive/work/*`
  joins `docs/work/*` as a declared expected-live-orphan class.

**station.py / spec_move.py — deliberately UNTOUCHED, and why.**
`kitlib.station.REPORTS` ("docs/handbacks") never nested under `docs/work/` —
SR-144's own reasoning (a report there would be walked by `spec_files`, raise
on its undeclared directory, and be silently skipped while its id counted as
taken) — so it did not move, and "the report IS the close event" stands
unchanged. Re-reading OI-55's exact text: "`partial/` handback reports move
WITH their specs and the disposition keys update in the same commit" means
temporal togetherness (one commit) and updating any disposition row's
`specref` that cited the pre-move path — checked (`grep specref =
"docs/work/\(partial\|cancelled\)/"` over every open spec) and found **zero**
live citations to update, so this half of the ruling is a no-op for THIS
migration but the reader (`intake._closed_spec`) is taught for the next one.
`spec_move.py` needed no change at all: it is a generic `(src, dest)` mover
with no hardcoded terminal destinations — the move itself was driven by
directory-level `git mv` for speed (three `git mv`s instead of ~495 single-file
moves), then `spec_move._rebase_moved_spec_links` / `_relink_inbound_links`
ran once over the precomputed `(old, new)` pairs for the link sweep.

**Link sweep**: **8** inbound files re-pointed (`docs/log.md`, 3
`docs/archive/plans/*`, `docs/archive/history/handback-contract.md`, 2
`docs/plans/*`, `docs/runtime-flows.md`) + **22** moved specs' own outbound
links re-relativised (their bodies are DATA, not link-checked, but
correctness costs nothing here), via `spec_move._relink_inbound_links` /
`_rebase_moved_spec_links` run once over the precomputed 495-pair remap — fig: cmd="python -c \"import sys; sys.path.insert(0,'project-trajectory/scripts'); import spec_move; from pathlib import Path; root=Path('.').resolve(); moves=[(f'docs/work/{s}/{p.name}', f'docs/archive/work/{s}/{p.name}') for s in ('complete','cancelled','partial') for p in sorted((root/'docs/archive/work'/s).glob('*.md'))]; print(len(spec_move._relink_inbound_links(root, moves)))\"" rev=d6818b0b0e2bfcd2568c9547483976f3836b0752. `check_docs.py --ignore docs/test/report.md --ignore "docs/work/*" --ignore "docs/archive/work/*" --ignore "docs/handbacks/*" --stale` — the exact invocation `check.py`'s doc-navigability step runs — reports **0 broken** across 504 docs / 1315 links — fig: cmd="python project-trajectory/scripts/check.py --run-step doc-navigability" rev=d6818b0b0e2bfcd2568c9547483976f3836b0752

Hand-swept live prose (not link-checked, so not caught by the sweep above, but
inaccurate if left): the three `.claude`/`.agents`/`project-trajectory` copies
of `skills/session-protocol/SKILL.md` (kept byte-identical to each other),
`docs/handbacks/README.md`, `docs/registry-machinery-reference.md`,
`docs/archive/README.md` (new `docs/archive/work/` row), `docs/status.md`'s
top-block homes line. Left alone, deliberately, as historical citations of
where a thing lived when the record was written: `docs/concurrency-v2.md`'s
OI-11 (2026-08-01) measurement paragraph, every `docs/log.d/*` / `docs/log.md`
/ `docs/reviews/*` / `docs/archive/history/*` / `docs/archive/specs/*` mention,
and the moved specs' own body prose.

**Tombstones**: `docs/work/{complete,cancelled,partial}/README.md`, one apiece,
pointing at the new `docs/archive/work/<status>/` home — so a link authored
against the old path (this migration missed none, per the sweep above, but a
future one might) resolves to an explanation instead of a 404.

**Reader tests added** (drive the archive-union behaviour directly, not just
backward-compatibility with the old fixtures, all of which still pass
unchanged): `test_wi_folder_loaders.py::test_terminal_history_reads_from_its_archive_home`,
`test_integrate.py::test_the_outcome_is_read_off_the_archive_home_too`,
`test_intake.py::test_a_merged_handback_mints_from_the_archive_home_too`,
`test_hats.py::_real_work_item_contexts` widened to scan both roots (its own
census test was silently reading 14 rows instead of >100 the moment the real
population moved — caught live, fixed in the same commit).

**Module-size ratchet** — five files crossed their committed baseline on real
behaviour, re-stamped with reasons in the same commit:
`bootstrap.py` 3042→3054, `check.py` 2326→2332, `check_trajectory.py`
4624→4637, `intake.py` 1937→1960, `integrate.py` 2578→2597 (see
`tests/test_module_size_ratchet.py` BASELINE comments for the per-file why).

**Scaffold verification**: `bootstrap.py --dest <scratch>` produced a fresh
scaffold shipping `docs/work/{draft,active,deferred}/` +
`docs/archive/work/{partial,cancelled,complete}/` directly (confirmed by
directory listing — no migration step needed on a fresh checkout); a
hand-filed `WI-901` was then driven filed → claimed (`integrate.py claim`) →
closed by hand into `docs/archive/work/complete/` on its branch →
`kitlib.registry.read_spec_rows` read it back as `("WI-901", "done")`,
`integrate.branch_outcomes` read `{"WI-901": Outcome.MERGED}` with no
unresolved names, and `integrate.finished_branches` listed the branch as
drained — all three readers agreed with the tree at the new archive location
without further changes. (A malformed hand-edit to the scratch fixture — `##
Deliverable` placed after `## Context`, the exact ordering rule this
session's own close obeys — correctly reproduced check_trajectory's R-A
error, further confirmation the validator is reading the moved file's
content, not just its path.) fig: derived="hand-driven session transcript, this fragment's own record; not a re-runnable single command"

**Done-count invariant**: **472 done / 21 cancelled / 507 total, unchanged by
the relocation itself** — fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=d6818b0b0e2bfcd2568c9547483976f3836b0752 (exit 0 both before the move and after; WARN-only findings, all pre-existing and unrelated — SpecRef-staleness on open-items.toml-referencing rows, connectivity-undeclared kitlib modules, IF/TC coverage gaps). This row's OWN close then advances the count once more, from 472 to **473 done**, in the ordinary way any WI close does — that increment is the row closing, not a symptom of the relocation.

**Gates**:

```
python -m pytest -q -n auto -m smoke
1399 passed, 5 skipped in 66.06s
```

```
python project-trajectory/scripts/check_docs.py --root . --stale
(with the check.py doc-navigability step's own --ignore flags)
check_docs: OK - 504 doc(s), 1315 intra-repo link(s), 0 broken.
```

Full unfiltered suite, per the broad-script-change bar — the confirming run
was taken by the coordinator session after the worker's runs were lost to a
basetemp collision, on a shell with the environment gates satisfied
(`sh.exe` on PATH; an ungated first attempt failed
`test_every_required_environment_gate_is_satisfied` exactly as that check
is designed to):

```
python -m pytest -q -n auto --basetemp=D:\pytest-tmp-main
2894 passed, 14 skipped in 1435.39s (0:23:55)
```

The coordinator also closed the last link gap before the run: the three
tombstone READMEs pointed at `docs/archive/work/*/README.md` targets that
did not yet exist; the three archive-side READMEs were written and staged,
taking `check_docs` from 3 broken back to 0.

**The full suite EARNED its keep twice** — this is exactly the case the bar
exists for (smoke drops the subprocess/scaffold-heavy modules, so a defect
only a real scaffold or the meta-repo's own tree can show survives smoke
clean). Two rounds, both fixed in this commit:

Round 1 (4 failures, first full run): `tests/test_check_docs.py::
test_harness_wires_stale_into_doc_navigability`'s fixed 1000-char search window
for `--stale` no longer reached it past the new `docs/archive/work/*` ignore
row — widened to 1300 per the test's own stated convention ("widen it when a
reason is added, never drop it"). Three `tests/test_integrate.py` end-to-end
fixtures (`scaffolded_closed_branch` and its one inline assertion) hardcoded
the pre-migration close destination `docs/work/complete/` — a real defect
class this WI's own change created: a fixture that goes through
`bootstrap.py` now gets the NEW shape, where `docs/work/complete/` does not
exist to write into. Re-pointed to `docs/archive/work/complete/`.

Round 2 (1 failure, second full run — after fixing round 1 and re-running
clean): `tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_
orphans` reported a genuine broken link inside the just-moved
`docs/archive/work/complete/WI-504-wi-history-to-archive.md` — this row's own
Deliverable, authored (wrongly) with THREE `../` for a link that needed only
TWO while the file still lived at `docs/work/queued/`, then correctly
rebalanced by `spec_move`'s automatic outbound-link rebase when the file
moved one directory DEEPER than intended-for, landing at FOUR `../` instead
of the THREE its final location needs. Fixed the link directly; also widened
this test's own `--ignore` list to include `docs/archive/work/*` alongside
`docs/work/*` — it had drifted from the harness invocation it claims to
mirror, which already carries both rows after this WI's `check.py` change,
so the same drift would have hidden a REAL broken link into the archive on
every future run.

**Deviations from spec**: none in shape. Three clarifications made explicit
above rather than left implicit: (1) `docs/handbacks/` does not move — it was
never nested under `docs/work/` and OI-55's "reports move WITH their specs"
reads as one-commit togetherness plus disposition-key currency, both
satisfied; (2) the mass move used three directory-level `git mv`s plus one
whole-repo link-sweep pass rather than ~495 individual `spec_move.move_spec`
calls, for the same result at a fraction of the git operations (`spec_move`'s
own primitives — `_rebase_moved_spec_links` / `_relink_inbound_links` — were
reused directly on the precomputed remap, so the ritual's logic is not
reimplemented, only its per-file driving loop); (3) the full suite's real
job — catching what smoke cannot — is recorded above rather than smoothed
over: two commits' worth of fixture drift only the meta-repo's own tree and a
real scaffold could show, both closed in this same commit rather than
deferred.

Deferred open items: none.

(For context, not a deferral: the open item this WI executes reads fully
RULED and EXECUTED by this close; its sibling ruling about a staleness-header
stamp is sequenced next as its own already-queued work item, not deferred
from this one.)
