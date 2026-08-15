# The `last_approved` snapshot — spine change detection without hashes

**Provenance:** commissioned by the owner 2026-08-15 and produced the same day
by a read-only Opus design pass. The directive, verbatim: *"approved spine
changes just have their respective documents copied to `archive/last_approved`,
and then comparisons (Adjudicator or human, as well as html generator) just use
… the differences between the two."* This supersedes repo-lock D-1's anchor
half (`TextHash`/`HashedOn`) — see log `2026-08-15d` and
[2026-08-15-d9-migration-plan.md](2026-08-15-d9-migration-plan.md) §D.

**Status: design, ruled in direction (the owner's directive IS the direction),
execution details provisional.** `file:line` citations were resolved while
other lanes were landing; re-resolve at execution — the function names and
semantics are stable.

---

## A. The mechanism

### A1. Layout

```
docs/archive/last_approved/
  README.md                              # prose stamp — rendered, never parsed
  docs/requirements/stakeholder-needs.toml
  docs/requirements/system-requirements.toml
  docs/requirements/low-level-requirements.toml
  docs/test/test-cases.toml
  docs/requirements/interfaces.toml
  docs/requirements/external.toml
  docs/requirements/components.toml
```

**Repo-relative paths preserved under the snapshot root** — `spine_carrier.resolve`
/ `carriers` / `stem` all take a registry path, so `snapshot_root / rel` reuses
every existing resolver verbatim, carrier fallback included. Flattening would
need a second path vocabulary.

**Whole files, not extracted rows.** Three reasons in order of force:

1. **The mirror invariant only exists for whole files.** The copy is
   byte-for-byte, so "snapshot file == live file at the copy commit" is a
   decidable property — the mechanical guard against a hand-edited or partial
   snapshot (§F3). Extracted rows destroy it.
2. `intake._flip_status_lines` exists precisely because re-serialising a TOML
   registry normalises away comments and authored ordering. A row-extracting
   snapshot writer would be that re-serialiser.
3. The prose *outside* the rows is normative (`stakeholder-needs.toml`'s
   NON-GOALS block is "a DevBar-Reqs deliverable with no other home"). Row
   extraction silently drops it.

**All seven files.** The four spine registries, plus the three off-spine
registries that carry human-only approval cells (`interfaces.toml` `approval`,
`external.toml` `approval`, `components.toml` `state`) — the proposed
`human_approval_registries` set. If a human-only approval cell has no baseline,
the "approved text moved and nobody saw" hole reopens one tier down. Cost
≈ 475 KiB per generation (§F6 — a non-issue).

**Location: keep the owner's `docs/archive/last_approved/`.** The apparent
conflict with "archive is design history, not working surfaces" does not hold:
`check_trajectory.ARCHIVE_SPECS_DIR` already reads archive as live machinery
input, and archive placement is *actively load-bearing* —
`check_vocab.EXEMPT_GLOBS` exempts `docs/archive/*` (the snapshot legitimately
holds the *previous* vocabulary, so anywhere else would red the vocabulary
enforcer on every signing), `check_docs._in_archive` exempts it from
orphan/stale findings, and `check_doc_refs.RECORD_PREFIXES` keeps its inherited
citations from dangling. Amend `docs/archive/README.md` with one row: this
subtree is *frozen evidence read by live checks*, the same class as
`archive/specs/`.

### A2. Who copies, when

One function, in a new module `project-trajectory/scripts/baseline_snapshot.py`:

```python
def copy_live(root, *, seed=False) -> list[str]:
    """Mirror every SNAPSHOTTED registry into docs/archive/last_approved/.
    Byte-for-byte (shutil.copyfile), the LIVE carrier only, and any
    other-carrier file for the same stem is DELETED in the same act —
    otherwise spine_carrier.resolve raises 'exists under BOTH carriers'
    on the next read. Refuses when the snapshot dir does not exist
    unless seed=True."""
```

Exactly three callers:

1. **`intake._apply_flips` — the mechanical path.** Called after the TOML
   line-rewrite and CSV re-emit loops, before the return, only `if flipped:`.
   Ordering is load-bearing: the copy captures the file **with the flip already
   written**, so the snapshot row itself reads `Approved` — which is what makes
   the unanchored rule (§B4) decidable. This satisfies, literally, the standing
   comment "the flip and the record of WHAT TEXT was blessed have to be one
   act."
2. **`intake.py snapshot` — the human path.** The subcommand slot is already
   reserved ("the `attest` subcommand … returns with the anchor half — same
   name, different destination"; the destination changed, so the name changes
   to `snapshot`). No `--rows` — a whole-file mirror has no row scope. The
   owner's hand path: edit Status cells in the reviewed sitting commit → run
   `intake.py snapshot` → commit both. The `gate-advance` skill gains that
   line.
3. **Nothing else.** Not `agent_loop`, not `dispatch`, not the hooks, not
   `check.py`. A freshness step that *regenerates* the snapshot would defeat
   the mechanism — the snapshot is deliberately behind live whenever an
   amendment is pending. Stated in `copy_live`'s docstring so nobody wires it
   into `check.py`.

### A3. The bootstrap

**The first copy rides the signing act and nothing else.** `copy_live` refuses
to *create* the directory unless `seed=True`; `seed` is reachable only from
`intake.py snapshot --seed`; a grep test pins that no loop module, hook or
`check.py` contains the flag. Until the directory exists, every reader is
**vacuous by absence** (the `ratify-fresh` "doubly self-arming" pattern) — a
fresh adopter pays nothing, and the only vacuous state is the true
pre-attestation state. Once it exists, a missing file *inside* it is an ERROR.

The first snapshot contains the tree **after** the owner has ruled every
`Modified` row — repo-lock D-10's sequencing rule binds unchanged with
"stamping hashes" swapped for "copying files": copying before the sitting
launders the re-blessing those rows owe.

---

## B. Per-row semantics over file snapshots

### B1. Comparison basis — `split_changed_cells`, not `normative_text`

The migration plan named `normative_text` as the reuse; **the better function
is three lines away**: `check_trajectory._split_changed_cells(rel, id_col,
head, row)` already takes two row dicts from arbitrary trees and returns
`{"ratified": {cell: (before, after)}, "traced": {...}}` — `normative_text`'s
semantics *plus* the §A5.1 severity split *plus* the before/after pairs the
brief renders anyway. (`normative_text` returns a `\x1f`-joined string whose
only job was to be hashed; with the hash gone it has no job.) Promote it to
`split_changed_cells` (public).

Severity follows the existing ruling verbatim:

| what moved between snapshot and live | consequence |
|---|---|
| a **ratified** cell | **drifted** — re-attest owed, a section in the brief |
| a **traced** cell only | routes to adjudication, never arms a re-attest window (the WI-388 ruling, unchanged) |
| `Status` | invisible, by the function's own exclusion |
| the id | invisible (join key) |

`spine_cell_class` needs no change: its residual reads unclassified columns as
*ratified* (fails loud), and it keys off `spine_carrier.stem`, so it answers
for a snapshot file under either carrier.

### B2. Drift, defined

```python
def is_drifted(rel, id_col, live_row, snapshot_rows) -> bool:
    """True when this row claims Approved-or-above and its RATIFIED cells
    differ from its copy in the last_approved snapshot.

    A row not at Approved-or-above is never drifted — it has made no claim
    to fall from. An Approved row ABSENT from the snapshot is not 'drifted';
    it is UNANCHORED, a harder finding (unanchored_findings owns it)."""
```

### B3. What a `Drafted` row in the snapshot means

**For drift: nothing** — no attestation, nothing to fall from. **For the
unanchored rule: everything** — it is the *positive evidence* that the row was
NOT approved at the last signing. A live row reading `Approved` whose snapshot
copy reads `Drafted` is an approval that never rode a copy — the exact
laundering the mechanism exists to catch. Whole-file copying is what makes
this case decidable, and **this is the strongest single argument for the
owner's design**.

### B4. The successor to "Approved-with-no-hash is an ERROR"

> A row whose live `Status` is `Approved` or above is **UNANCHORED — an
> ERROR — when the snapshot does not contain that id, or contains it at a
> status below `Approved`.** Vacuous only while the snapshot directory does
> not exist at all; once it exists, a missing registry file inside it is
> itself the error.

Finding class: **integrity** (the always-on `--strict-integrity` floor + the
pre-commit hook), not schema (`--strict-schema` runs only at DevBar-Release).
**Armed only at migration step 7** — before the seed, or against a pre-rename
snapshot, it would red every row (§B6, §E2).

### B5. The four structural cases

| case | rule |
|---|---|
| row added since snapshot | live `Drafted` ⇒ ratification owed (`kind="ratify"`, reason "not in the last_approved snapshot — awaiting its FIRST approval"). Live `Approved` ⇒ **UNANCHORED ERROR** (cannot legitimately arise: adding + approving must ride a copy). |
| row deleted from live, `Approved` in snapshot | **warn-class in the brief, never an ERROR** — D-4 rules supersession IS deletion, so an error would block every legitimate deletion until the next signing. The `state == "removed"` rendering already exists. Clears at the next copy. |
| id renamed | reads as delete + add — correct, D-4 forbids id reuse. |
| carrier changes under a registry | the snapshot keeps whichever carrier was live at the copy; the reader resolves it independently via `spine_carrier.resolve(snap_root/rel)`; `rows_from_toml` maps a CSV-era snapshot onto today's column names. |

### B6. Version skew, three axes, three guards

1. **Carrier skew** — resolver handles it; `copy_live` must delete the
   other-carrier file per stem or `spine_carrier.resolve` hard-fails on the
   next read.
2. **Column-name skew** — `REGISTRY_COLUMN` maps old keys; a rename without a
   mapping entry surfaces as "every row drifted" — loud in the right
   direction.
3. **Vocabulary skew — the one that bites the migration.** A pre-rename
   snapshot reads `Verified`; `is_approved` returns False for it; every
   Approved row reads UNANCHORED. Guards: the snapshot is **one generation,
   replaced wholesale at each signing, never migrated in place** (git holds
   history); and the arming order — reader advisory at step 3–4, seed at step
   6 *in the post-rename vocabulary*, ERROR only at step 7.

**Parse failure is a refusal, not an empty read.** `rows_from_text` returning
`None` vs `{}` are opposite claims; the snapshot reader raises rather than
degrading — unlike git history, a snapshot file is on disk and fixable. (The
advisory-print degrade in `_rows_at` is correct for history and wrong here.)

### B7. The SN tier

`stakeholder-needs.toml` carries no `status` keys today, so SN drift cannot be
status-gated until D-9 gives SN a Status. `sn_normative_text` already parses
the wrong carrier (markdown) and dies with the rest. `spine_cell_class`'s
default answers for SN with every column ratified — loud-by-default; adding an
SN entry to `SPINE_TRACED_CELLS` is a narrowing decision that can wait for
evidence. **The one open sub-decision; the default is safe.**

---

## C. The rewiring table

### C1. The migration plan's drift/re-attest touchpoints, re-homed

| site | under snapshots |
|---|---|
| `reattest_model(..., statuses=("modified",))` | `reattest_model(root, srs, llrs, tcs, snapshot=None)`; selector `is_drafted(sr) or sr_chain_drifts(sr)`; **`statuses=` deleted, and with it the plan's "hard coupling"** |
| `reattest_lines` same kwarg | drops it |
| "No Modified SR — nothing owes a re-attest" | "No spine row differs from its `docs/archive/last_approved/` copy, and no row awaits a first approval." — checkable against a file, not a vocabulary |
| the `state == "draft"` arms | `kind = "ratify" if is_drafted(sr) else "reattest"`; the baseline question becomes a dict lookup; the "no git history" degrade arm dies |
| `_changed_cells`' Verified→Modified suppression | **deleted whole, never re-keyed** — `split_changed_cells` excludes Status structurally, and the brief gains the ratified/traced two-group rendering (a capability gain: the reader sees which changes owe attestation vs adjudication) |
| `_attested_baseline` (the git walk) | **DELETED (~45 lines)** — its docstring is an apology for a derivation D-9 breaks by construction |
| `gen_open_items` `statuses=("modified","draft")` | drops the kwarg; the model already unions drafted + drifted |

### C2. Four more that must move together

- `trace._DECLARED_BASELINE_RE` + `declared_since` — **deleted**; the WI-325
  "a gate that re-derives its own expectation" blocker dissolves; `ratify_check`
  becomes a plain regenerate-and-compare.
- The whole `--since` CLI surface (`trace.py`, `gen_open_items.py`
  `BASELINE_MARK`) — **deleted**; a snapshot cannot sit after the amendment.
- The "check the baseline … re-run with `--since <rev>`" empty-section prose —
  **deleted** (advice about a failure mode that no longer exists).
- `--ratify modified` reserved scope → renamed `drifted` at the rename step;
  closed `_RESERVED_RATIFY_SCOPES`; `_scope_srs` **raises** on empty
  resolution (an empty brief is a refusal, not an output); `check.py`'s
  `ratify-fresh` literal moves in the same commit.

### C3. The capability unlock: the `amendment` adjudicator becomes routable

`adjudicate_brief` records why the amendment brief is unroutable today: for a
row that never flipped, `_attested_baseline` resolves to the amendment commit
itself — presenting the text under judgement as its own accepted anchor. The
snapshot **is** an accepted anchor that is provably not the text under
judgement (the mirror invariant proves it was copied in a reviewed approval
commit). So `_ASSEMBLERS` gains `amendment` ("one entry away once the anchor
question has an answer" — its own docstring); `{baseline}` = the snapshot
stamp; `{rows}` = the drift model's ratified cells. The
`staged_spine_amendments` population and the drifted population become the
same population instead of disjoint ones. **The single largest capability win
in the change** — the adjudicator that pages a human on every amendment row
today becomes routable.

### C4. What dies entirely

`normative_text`, `sn_normative_text`, `digest`, `current_digests`
(docstring-reserved for the on-row writer, now ruled never built),
`_DIGEST_SEP`/`_DIGEST_EXCLUDED`/`_SN_ROW_RE`, the SN-029 comment block
(~107 lines in `check_trajectory.py`); `_attested_baseline`, `_changed_cells`,
`declared_since` + regex, the `--since` plumbing (~130 lines in `trace.py`);
`BASELINE_MARK` (`gen_open_items.py`); repo-lock **D-1 anchor items 1–6 all
die** (the two cells, the `_DIGEST_EXCLUDED` additions, the third cell class,
the co-mutation guard, the template columns, and Q3 — answered structurally:
exactly one generation back); D-2's owed half dies with them. Verified by
grep: the only non-test consumers are the four functions' mutual calls plus
documentation rows (LLR-158, TC-153 — those rows need re-pointing at
execution).

### C5. Tests

`test_attestation_digest.py` deletes (177 lines) — but its
`test_the_amendment_seam_is_BLIND_to_an_amend_plus_flip` is preserved
*reworded* in the new suite: it drives the reason a baseline outside the live
file is forced, which is unchanged. New `test_baseline_snapshot.py` (~250
lines): drift over a real copied tree; UNANCHORED both directions; the mirror
invariant catching a hand edit; the seed refusal; the both-carriers refusal; a
partial copy caught; an unparseable snapshot refusing. `test_trace_briefs`
loses the six `--since`/`declared_since` tests and the off-git degrade;
`test_gen_open_items` selectors rename; `test_rule_sync` asserts `is_drifted`
has ONE home (it is deliberately not an F5-duplicated predicate); module-size
ratchets re-stamp (three of four move DOWN); `test_complexity_ratchet`'s
`_split_changed_cells` mention renames; `test_dogfood_sync` applies if
`bootstrap.MAPPING` gains the README.

---

## D. The HTML surfacing

**No new tab, no new page.** Both owner-named surfaces already render the
shape:

1. **`open-items.html` §2 is the primary surface** — `_attestation_cards`
   already renders per-SR cards with per-cell before/after. Three edits: the
   baseline line becomes one hoisted header line ("Baseline:
   `docs/archive/last_approved/` — copied <date> (<sha>), the reviewed commit
   that last moved an approval"); `_chain_row` gains the ratified/traced two
   groups (~10 lines); the footer prose reinstructs (set Status to `Approved`
   **and run `intake.py snapshot` in the same commit**). Plus one counter: "N
   row(s) drifted from the approved snapshot".
2. **`PROJECT_STATE.html` inherits for free** — it renders
   `traj_status.pending_block`, which needs only the selector + two line
   templates changed.

A rendered raw `git diff` view was considered and rejected: no cell
classification, no ratified/traced split, no chain grouping, no
drifted-vs-unanchored distinction — and the owner already has `git diff` for
the raw view, which is itself an argument for the design: the snapshot is
inspectable with tools the owner already has.

---

## E. Sizing and the migration-step rewrite

Net: **≈ +108 lines of scripts** (one new ~170-line module;
`check_trajectory.py` −70, `trace.py` −55, `gen_open_items.py` −8; `intake.py`
+25; small edits in `traj_status`/`adjudicate_brief`/`derive_gate`/`check`/
`bootstrap`), tests −177/+250, ~40 lines of prose (repo-lock strike-and-restate,
archive README row, PROCESS §7, gate-advance skill, RESYNC entry). One new
import edge worth declaring: `trace` → (transitively) `check_trajectory` via
the new module.

The migration plan's steps 3/4/6/7 are rewritten accordingly (and a step 4b
inserted for the amendment adjudicator) — the plan document carries the
replacement text; the essentials:

- **Step 3** — build the mechanism READER-FIRST, advisory; nothing writes a
  snapshot; everything vacuous by absence.
- **Step 4** — `is_drifted` overlay alongside `is_modified`; the dead git-walk
  machinery deletes; drift stays WARN; UNANCHORED not armed.
- **Step 4b** — route the amendment adjudicator.
- **Step 6 (signing)** — the owner rules each Modified row;
  `_apply_flips` writes Approved then `copy_live`; **the first snapshot is
  seeded here and only here**, post-rename, after every row is ruled.
- **Step 7** — arm UNANCHORED as ERROR on the integrity floor.

---

## F. Risks, ranked, each with its mechanical guard

1. **The bootstrap seeding falsely blesses unreviewed text.** Guards, layered:
   `copy_live` refuses to create the dir without `seed=True`; `--seed`
   reachable only from `intake.py snapshot`, pinned by a grep test over every
   loop module/hook/check.py; the seed follows the owner ruling every Modified
   row (repo-lock D-10's own sequencing rule).
2. **An approval that never rode a copy.** Guard: the UNANCHORED rule — the
   snapshot's own Status cell still reads below Approved, an ERROR on the
   always-on floor. *This is why whole-file copying is load-bearing*: row
   extraction would delete the very evidence this check reads.
3. **The snapshot is hand-edited (it is just files).** Guard — **the mirror
   invariant, exact:** in any commit that touches a snapshot file, that file
   must be byte-identical to its live counterpart in that same commit.
   Legitimate copies satisfy it always; a hand edit, a partial copy, and a
   copy-then-amend-live all fail it. Implement as
   `check_trajectory.staged_snapshot_findings` (~15 lines reusing
   `_spine_revs`), warn at the staged hook, ERROR on the integrity floor. The
   only way to write text into the snapshot is to write it into the live
   registry first — an approval, in a reviewed commit, exactly as ruled.
4. **The snapshot goes stale silently.** Guard: the drift count joins the
   derived gate (`drifted=N` in the basis counters → `docs/gate`), with the
   producer-consumer round-trip pin on `check.py`'s `_BASIS_RE` (the
   twelve-commit precedent).
5. **Vocabulary/schema skew during the migration.** Guard: the arming order;
   one-generation-replaced-wholesale; the per-stem stale-carrier unlink.
6. **Git bytes: measured non-issue.** ≈ 475 KiB per generation against a
   195 MiB `.git`, delta-compressed against near-identical live blobs.
7. **Downstream vacuity.** A missing snapshot is *honest* ("this repo has
   approved nothing yet") — unlike the anchor's silent schema hole. Ship the
   README in `bootstrap.MAPPING`; a dir-exists-but-file-missing state is an
   ERROR, so the vacuum has exactly one state and it is the true one.
8. **The stamp becomes a ledger.** D-10's tripwire. Guard: the README stamp is
   prose, rendered and never parsed; every machine fact comes from the files
   or from git; its first line says so.

---

## What this buys, for the review sitting

- Kills `TextHash`/`HashedOn`, the co-mutation guard, the third cell class,
  the `--since` escape hatch, `declared_since`, the self-stamping baseline
  contract, `_attested_baseline`'s git walk and `_changed_cells`' suppression:
  **~160 lines of machinery that existed only because the baseline was a
  moving git derivation.** Three modules get smaller.
- **Unblocks the `amendment` adjudicator** — a live hold on every amendment
  row today.
- The baseline becomes inspectable with `git diff` and a text editor — no
  generator, no hash column.
