# WI-916 implementation plan: the RESYNC entry presence check

Spec: `docs/work/active/wi-916/WI-916-resync-entry-presence-check.md`
(specref: `docs/plans/2026-10-11-review-churn/README.md` §6, proposals 2
and 3, under owner ruling 6). Planned against lane base `6533a2331`.

## What the build reads, and what it found

- **SR-036** (`docs/requirements/system-requirements.toml`), "Deliberate
  re-sync integration": a re-sync follows the documented procedure against the
  recorded kit-version diff. The pack's `[since <sha>]` entries are what select
  the right changes for a stamp-to-target range, so an entry missing for a
  shipped change is a hole in that procedure. That is the link to this item.
  SR-036's only verifier is **TC-036** (`docs/test/test-cases.toml`): an
  Inspection of `ADOPTING.md` and the `downstream-resync` skill, triggered by
  those two files. This item changes neither.
- **The check is this repo's tooling, untraced** (spec deliverable 1), like
  `scripts/check_smoke_budget.py` and `scripts/check_changed.py`. Neither of
  those appears in `docs/requirements/interfaces.toml` or
  `docs/requirements/components.toml`, which register the traced product
  (`project-trajectory/scripts`). So this item adds no IF, CMP, LLR or TC
  row. SR-036 sits in `[unplaced]` in `components.derived.toml`, and no
  component changes. `docs/runtime-flows.md` Flow 2 (scaffold and re-sync,
  SR-036) describes the adopter-side procedure, which this item leaves
  unchanged. No flow edit.
- **Existing seams the check crosses:**
  - `agent_common.default_base` (IF-189). It returns the lane's merge base
    with trunk, and HEAD on trunk: on trunk, `claim_base` finds no
    `-> active/<trunk> (bookkeeping)` claim subject and falls through to
    `merge-base trunk HEAD`, which is HEAD.
  - `bootstrap.delivery_inventory()`. No IF row owns it. The nearest is
    IF-262, the `MAPPING` inventory.
  - the `[run] smoke` line of `docs/stack.ini` (IF-049).
  - `RESYNC_PACK.md`'s heading grammar, which today lives only in
    `tests/test_resync_pack.py`.
- **Reuse, so nothing is duplicated:**
  - `scripts/check_changed.changed_paths(root, base)` already returns exactly
    "base to working tree, index and untracked files included, renames off so
    both old and new paths appear". On a failed read it returns `None`, never
    an empty list. The check imports it rather than writing a second change
    reader.
  - `delivery_inventory()` is the only list of what ships.
- **Facts the classifier must honour** (measured on this tree):
  - `RESYNC_PACK.md`, `ADOPTING.md`, `README.md`, `scripts/bootstrap.py` and
    `LICENSE` are in `project-trajectory/mapping-source-exclusions`.
  - The inventory's generated list names
    `{LICENSE, scripts/bootstrap.py, scripts/gen_open_items.py, scripts/trace.py}`
    as generator sources. So the spec's "generator sources count as shipped"
    overrides the exclusion for `bootstrap.py` and `LICENSE`.
  - Every file of a `scope: this-repo` skill is excluded, for example
    `skills/render-dashboard-critique/` (WI-823's dismissed K4 finding).
  - An edit to `RESYNC_PACK.md` alone is therefore not a shipped change.
- **Ordering preconditions (D4), verified read-only:**
  - WI-913's landing `b803dd019` is an ancestor of the lane base.
  - WI-914's landing `4fe9114a1` is an ancestor of the lane base.
  - `[run] smoke` already carries WI-914's chain: `trace.py --strict`,
    `check_trajectory.py --strict`, `check_docs.py --root . --stale`, then
    `check_smoke_budget.py --mode enforce`.
- **Smoke-tier headroom:** 2664 smoke tests are collected against
  `max-tests = 2715`. The new tests below add about 16, which fits. WI-914's
  landing measured the budget at 44.9 s of 60 s.

## Design of `scripts/check_resync.py`

The check is split into one pure verdict and thin readers, so that most cases
are tested in process with no git.

- **`ENTRY_RE`, `RESERVED_PREFIX`:** these move here verbatim from
  `tests/test_resync_pack.py`, and the test imports them (one home).
- **`entry_headings(text)`:** the `### ` lines between `## 3. What changed
  over time` and `## 5. Promotion`, which covers §3 and §4. It raises
  `ValueError` when a section marker is missing, so a pack that cannot be read
  counts as unreadable, never as having no headings.
- **`kit_classes(kit_dir)`:** runs
  `[sys.executable, "-I", "-c", SNIPPET, <kit_dir>/scripts]`. The snippet
  imports *that tree's* `bootstrap` and prints JSON holding the exclusion keys
  and the generator sources (the first element of each `generated` pair). So
  the base is classified by the base's own code over the base's own files: one
  inventory, no second list. Any non-zero exit or unparseable output raises
  "inventory cannot be computed". A file is shipped when it lies under
  `project-trajectory/` and is either a generator source or not excluded. An
  unclassified path is therefore shipped (deny by default).
- **`base_kit(root, base)`:** `git archive <base> project-trajectory`,
  extracted with `tarfile` (`filter="data"`) into a `TemporaryDirectory`.
  Measured at about 1.1 s for the archive and 0.4 s for the classifier
  subprocess. Both are paid only when some changed path is under
  `project-trajectory/`.
- **`judge(changed, shipped_base, shipped_head, present_base, present_head,
  base_headings, head_headings, base_sha, resolve)`:** pure. It returns a list
  of `(subject, reason)` refusals.
  - The judged kit set is:
    - every changed path that ships at the base or in the working tree, so a
      deleted shipped file counts;
    - plus every path present on both sides whose class differs, so a file
      that a new exclusion line stops shipping still owes an entry. This is the
      spec's "a file that stops shipping still owes an entry". The changed path
      itself, `mapping-source-exclusions`, is excluded and would otherwise hide
      it.
  - The added headings are `head_headings - base_headings`. Each must match
    `ENTRY_RE`, must not be `### Reserved:`, must not carry a `pre-` anchor,
    and must satisfy `resolve(sha) == base_sha`. Otherwise it is refused,
    whether or not anything shipped (Trust: the rules bind every added
    heading).
  - If the judged kit set is non-empty and no added heading passes, every
    path in it is refused with "no RESYNC_PACK.md entry added for this
    change".
- **`run(root, base)`:** the readers plus `judge`.
  - It refuses with a stated reason for any of these:
    - `base is None` (an unreadable claim history);
    - a base `rev-parse` failure;
    - a `changed_paths` result of `None`;
    - a pack that is absent or unreadable at the base (`git show
      <base>:project-trajectory/RESYNC_PACK.md`) or in the working tree;
    - an inventory failure.
  - `resolve` is `git rev-parse --verify <sha>^{commit}`, compared with the
    full base sha. An ambiguous short sha fails and is refused.
  - It prints one line per refusal, then exits 1. When it passes it prints one
    summary line ("N shipped path(s) changed; entry ... anchored at <base>",
    or "no shipped path changed") and exits 0.
- **`main(argv)`:** takes `--root` (default: this repo), resolves the base with
  `agent_common.default_base(root)`, and calls `run`.
- **Path setup:** it puts `project-trajectory/scripts` on `sys.path`, as
  `check_changed.py` does.
- **Dependencies:** stdlib only.

A consequence to name, not a scope change: retitling an *existing* entry reads
as an added heading anchored at another commit, and is refused. That is the
spec's rule. A retitle of a landed entry goes through as a new entry or a
reviewed edit of the check. No live recipe retitles landed entries.
(`recipes.md` folds a fix round's entry into its parent *before* landing,
where its anchor is still the base.)

## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | `scripts/check_resync.py`: the entry grammar's new home, the pure verdict, the base/working-tree readers, the CLI; plus `tests/test_check_resync.py` | D1; SR-036 | IF-189 (`default_base`, the base it judges from); IF-262 nearest for `delivery_inventory`, which no row owns; no row is added, because the caller is untraced repo tooling like `check_changed.py` |  |
| P2 | `tests/test_resync_pack.py` imports `ENTRY_RE` and `RESERVED_PREFIX` from the check instead of defining them | D1; SR-036 | intra-module: test-only import of P1's constants, no interface | P1 |
| P3 | Wire the check into the bar: `docs/stack.ini` `[run] smoke` gains `python scripts/check_resync.py` after `check_docs.py --root . --stale` and before `check_smoke_budget.py --mode enforce`; `smoke.desc` names it; the bar-order test pins it; the hook, `check.py` and every `[step:]` stay untouched | D2; SR-036 | IF-049 (the `[run]` line's value changes; its format does not) | P1 |
| P4 | Records: K4 leaves `docs/rubrics/kit-change-review.md`; `RESYNC_PACK.md` §5's "nothing enforces" sentence states what the check holds and what stays with review; `docs/enforcement-audit.md` gains the rule's row | D3; SR-036 | no interface: prose records only | P1; P3 |
| P5 | Verify and land: confirm the ordering preconditions, run the bar on the lane tip, rebase onto the trunk tip, and at landing run the bar and the check on the staged squash | D4; D5; SR-036 | IF-049 (the declared bar run on the tip and on the squash) | P1; P2; P3; P4 |

Excludes: TC-036 — it inspects the adopter-side re-sync procedure (`ADOPTING.md` and the `downstream-resync` skill, which are its trigger files), and this item changes neither the procedure nor SR-036's text. The check is untraced repo tooling, so it adds no TC. Its evidence is the pytest module P1 adds, run in the smoke tier.

### P1: the check and its tests

**Builds:** `scripts/check_resync.py`, as designed above.

**Adds `tests/test_check_resync.py`.** It stays in the smoke tier: it is not
in `SLOW_MODULES`.

- **Before the change, every test in it fails at collection:** the module it
  imports does not exist (`ImportError` / `FileNotFoundError`).
- **In-process tests of `judge`** (no git), one per spec case or rule:
  1. `test_a_shipped_change_with_no_entry_is_refused`: names the path and the
     "no entry" reason.
  2. `test_an_entry_anchored_at_the_base_passes`: the positive control, so the
     refusals are not vacuous.
  3. `test_an_entry_anchored_at_another_commit_is_refused`: the resolver
     returns a different sha.
  4. `test_an_edited_only_entry_does_not_count`: an existing heading kept,
     body changed, so no added heading means a refusal.
  5. `test_a_reserved_placeholder_does_not_count` and
     `test_a_pre_anchor_does_not_count`: both refused, including when no
     shipped path changed.
  6. `test_a_change_only_to_a_this_repo_skill_owes_no_entry`: the path is
     classified excluded on both sides, so the check passes.
  7. `test_a_deleted_shipped_file_owes_an_entry`: present and shipped at the
     base, absent in the working tree.
  8. `test_a_change_outside_the_kit_owes_no_entry`: for example `tests/x.py`
     and `.claude/skills/...`.
  9. `test_a_file_that_stops_shipping_owes_an_entry`: same bytes,
     reclassified by the base and head inventories.
  10. `test_a_generator_source_and_an_unclassified_kit_path_count_as_shipped`.
- **Tests against this repo's real inventory:**
  `test_the_real_inventory_classifies_the_kit` calls `kit_classes` on this
  repo's `project-trajectory/`. It asserts four things:
  - `skills/render-dashboard-critique/SKILL.md` is not shipped;
  - `scripts/bootstrap.py`, `LICENSE` and `scripts/trace.py` are shipped;
  - `RESYNC_PACK.md` is not shipped;
  - an invented `project-trajectory/zz-unclassified.txt` is shipped.
- **Git-backed tests**, each on a small temp repo whose
  `project-trajectory/scripts/bootstrap.py` is a ten-line stub
  `delivery_inventory`. The check runs whatever inventory the tree carries.
  - `test_an_unreadable_base_is_refused`: `run(root, None)` and
    `run(root, "<unknown sha>")` both exit 1 with the reason.
  - `test_an_absent_pack_is_refused`: the pack is missing in the working tree,
    and in a second case missing at the base.
  - `test_an_uncomputable_inventory_is_refused`: the stub raises.
  - `test_an_untracked_shipped_file_counts`: a new, unstaged kit file with no
    entry is refused.
  - `test_the_cli_on_trunk_judges_against_head`: a subprocess run of
    `scripts/check_resync.py --root <tmp>` on the temp repo's only branch. A
    staged shipped change with an entry anchored at HEAD exits 0. The same
    change anchored at HEAD's parent exits 1. This proves the
    `default_base` wiring and the "staged squash judged against its parent"
    landing case.
- **Budget:** about 16 tests. At most 5 build git fixtures, and the pure cases
  cost milliseconds. After P1, `run.cmd smoke` must stay at or under 60 s; the
  measured wall time is pasted with the commit.

### P2: one home for the grammar

`tests/test_resync_pack.py` drops its own `ENTRY_RE` and `RESERVED_PREFIX`
definitions. It imports them from `scripts/check_resync.py`, through
`importlib`, as `test_check_smoke_budget.py` loads its script.

- **Its existing tests run unchanged against the imported names.** These are
  `test_every_entry_carries_a_sha_anchor`,
  `test_no_reserved_placeholder_survives_a_commit`,
  `test_bite_the_grammar_rejects_a_planted_unanchored_entry` and the anchor
  resolution test.
- **Adds `test_the_entry_grammar_has_one_home`.** It asserts that the test
  module defines no regex literal of its own for the grammar: its `ENTRY_RE`
  *is* the check's object. Before the change this fails, because the module
  defines its own `ENTRY_RE` and the check does not exist.

### P3: wiring

**`docs/stack.ini` `[run] smoke`** becomes:

```
… && python project-trajectory/scripts/check_docs.py --root . --stale && python scripts/check_resync.py && python scripts/check_smoke_budget.py --mode enforce
```

`smoke.desc` gains "the RESYNC entry check". The budget check stays last, so
the tier still runs once.

**`tests/test_smoke_budget.py::test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget`**
gains the new step in its expected list, in that position.

- Before the change, it fails because the step is absent from the chain.
- `tier_steps == [steps[-1]]` still holds.

**Unchanged, verified by
`git diff <base> -- project-trajectory/hooks/ project-trajectory/scripts/check.py`
being empty, and by no new `[step:` section in `docs/stack.ini`:**

- the pre-commit hook;
- `check.py`'s built-in steps (they ship to adopters, who have no pack);
- every `[step:]` (its `paths` would run it in the hook through
  `--path-triggered`).

**`session-protocol` §3** describes the bar's order ("lints first, budget
last") and stays true. It is left as is. The steps have one home,
`[run] smoke`.

### P4: retirements and records

**`docs/rubrics/kit-change-review.md`:** the K4 paragraph is deleted. A live
grep finds no other live surface naming K4, only historical review, decision
and log records, which stay.

**`project-trajectory/RESYNC_PACK.md` §5:** "The honest cost is that nothing
enforces 'a kit change that needed an entry got one': the obligation holds by
attention." becomes a sentence of this shape: since WI-916 this repo's commit
bar refuses a change to a shipped kit file unless the change adds a §3/§4 entry
anchored at its trunk base. Presence and anchor are held; whether the entry
says enough is review's.

- The pack itself is excluded from the inventory, so this edit is not a
  shipped change.
- Its shape tests (`test_resync_pack.py`) stay green.

**`docs/enforcement-audit.md`:** a "Process disciplines" row with:

- **Rule:** a change to a shipped kit file adds a `RESYNC_PACK.md` entry
  anchored at its trunk base.
- **Primary:** Harness (commit bar) + Reviewer.
- **Enforcer:** `scripts/check_resync.py` in `[run] smoke`. Shipped is closed
  by `delivery_inventory`, with deny by default. It fails closed on any
  unreadable input.
- **Honest residue:**
  - it runs in the bar, not in the hook, so a commit made without the bar is
    caught at the next build round's bar or at landing;
  - the entry's content is review's.

**Tests:** none added. D3's clauses are prose, verified by reading the diff.
The existing pack-shape tests guard §5's presence.

### P5: verification and landing

**Ordering (D4):** before the first build commit, confirm with
`git merge-base --is-ancestor b803dd019 HEAD` (WI-913) and the same for
`4fe9114a1` (WI-914). Both pass at the lane base today. The row lands only
after WI-914, which has already landed.

**Lane bar:** `run.cmd smoke` on the lane tip is green, with the check's own
line in the output. Paste the real output, the smoke wall time against 60 s
included.

**Landing (D5):**

1. Rebase onto the trunk tip (`recipes.md` §4).
2. Stage the squash.
3. Run the bar on it. Its check line judges the squash against its parent,
   HEAD.

**This item changes no shipped path.** Its paths are:

- `scripts/`;
- `tests/`;
- `docs/stack.ini`;
- `docs/rubrics/`;
- `docs/enforcement-audit.md`;
- `project-trajectory/RESYNC_PACK.md`, which is excluded.

So the check prints "no shipped path changed" and exits 0, and no entry is
invented for adopters, who receive nothing new.

**If a fix round does touch a shipped file**, the landing carries an entry
anchored at the landing's parent (`recipes.md`, "RESYNC"), and the same check
line must pass over it. Either way, the landing record pastes the check's
output line.

**Phase close:** the full unfiltered suite runs per CLAUDE.md. Not every WI
runs it.

## Risks

- **Smoke wall time.** The git-backed fixtures are the cost. They are capped
  at five, and every other case is pure. If the bar breaches 60 s, this is
  found at P1's commit, not deferred. The budget is not moved.
- **A mid-build lane that changes a shipped file goes red** at every bar
  until its entry exists. That is the intended effect of ruling 6 ("every
  build round's bar"). Builders add the entry with the first shipped change
  and re-anchor it on rebase, which the recipes already require.
- **The base tree is classified by the base's own `bootstrap.py`.** A base
  without `delivery_inventory` (one predating WI-543) refuses as "inventory
  cannot be computed". No live lane has such a base.

## Architectural delta

The item adds no state and no domain value, and it crosses no new boundary.
The check reads git and the delivery inventory, both existing, and its one
seam into the kit is `default_base` (IF-189). It does make an output depend on
a new input: the commit bar's verdict, the `[run] smoke` value of IF-049, now
depends on the change's shipped paths against the pack's added headings. The
plan's rows carry that change: P1 is the input's reader and verdict, and P3
wires it into the bar. No interface row or domain edit is owed. The `[run]`
format is unchanged, and the reader is untraced repo tooling, which the
registries do not model.

DELTA: within
