## 2026-08-23 — WI-448 slice 3: the spine_rules/trace POLICY pair gets one home

Deferred open items: none — this slice took no owner decision. The two questions
it could have raised are both settled inside it: the kernel declaration is
correctly ABSENT (no cross-component edge exists yet, so there is nothing to
declare and nothing silenced), and the home choice is a shape decision the WI's
own adopted constraint already ruled.

**Summary.** Item 3 of WI-448's STILL OWED list. The ten duplicated groups the
`trace.py`/`spine_rules.py` pair carried — the row vocabulary `tests/test_rule_sync.py`
pinned most carefully, because it is POLICY and a disagreement between the module
that ENFORCES the spine and the module that DERIVES its stage is a false green or
a false red AT A GATE — consolidate into a new themed module,
`project-trajectory/scripts/kitlib/spine.py`. Nine equality pins retire with the
copies. CLI behaviour is byte-identical: every former name is re-exported from
its original module, so no call site in either 5,000-line consumer moved.

### The home, and why it is a new module

`kitlib/registry.py` was the obvious candidate and is the wrong one: it is the
`docs/work/` SPEC-FOLDER reader — a different registry, a different carrier, a
different consumer set. Folding the spine's row rules in would have grown the
package's largest module into exactly the generic bucket the adopted 2026-08-19
review shape constraint (H-09) forbids this package. `kitlib/spine.py` is the
`ladder.py` shape one tier over: a closed vocabulary as near-pure data, below
every axis that reads it, importing only `csv` and `re`.

The module joins `bootstrap.MAPPING`, `tests/test_bootstrap.py`'s file list, the
kit README's contents row, the package roster in `kitlib/__init__.py`, and
`RESYNC_PACK.md` §3 as an entry `[since d00a8506]`. It takes `LLR-197` /
`TC-193`, `Component = CMP-006`.

**Both new rows land `Drafted`, not `Approved`, and the reason is a real
one rather than caution.** Approving them in this commit would have made
`trace.py --strict-integrity` demand a `docs/archive/last_approved` refresh
in the same act ("adding a row and approving it must be one act") — and that
refresh would ALSO have absorbed this slice's amendment to LLR-147's Detail,
which is approved text no Status flip authorises. Absorbing it is exactly the
laundering `baseline_snapshot.refresh_refusal` and `--approves` exist to
prevent. So the amendment stays legibly OWING re-attestation in
`docs/ratify/CURRENT.md`, where the owner meets it at a sitting, and the two
new rows wait for the same act. `drafted` rises 9 -> 11; `docs/stage` is
unmoved (phase 5 already reads DevStg-LLReqs).

### Per-group disposition

| group | copies | home chosen | copies' diff | pin |
|---|---|---|---|---|
| `load_csv` | `trace`, `spine_rules` | `kitlib.spine` | byte-identical | never had one (plumbing) |
| `is_drafted` | `trace_text`, `spine_rules` | `kitlib.spine` | bodies identical; docstrings differ | `test_is_drafted_agrees` RETIRED |
| `is_approved` | `trace`, `spine_rules` | `kitlib.spine` | bodies identical | `test_is_approved_agrees` RETIRED |
| `is_founded` | `trace`, `spine_rules` | `kitlib.spine` | bodies identical | `test_is_founded_agrees` RETIRED |
| `LLR_EXEMPT` + `llr_exempt` | `trace`, `spine_rules` | `kitlib.spine` | **DISAGREED — see below** | `test_llr_exempt_sets_agree` + `test_llr_exempt_agrees` RETIRED |
| `phase_num` | `trace`, `spine_rules` | `kitlib.spine` | byte-identical | never had one |
| `sn_all_ids` | `trace`, `spine_rules` | `kitlib.spine` | bodies identical | `test_sn_all_ids_agrees` RETIRED |
| `sn_cited_ids` | `trace`, `spine_rules` | `kitlib.spine` | bodies identical | `test_sn_cited_ids_agrees` RETIRED |
| `sn_draft_ids` | `trace`, `spine_rules` | **stays out** — bound direct to `spine_carrier.draft_ids_from_text` | one-line delegation, identical | `test_sn_draft_ids_agrees` RETIRED |
| `refs`, `is_example` | `trace_text`, `spine_rules` | `kitlib.spine` | identical (the `None` crash was already fixed) | `test_is_example_agrees…` KEPT — see below |

**Nine pins retired**, each with the reasoning recorded in its place in
`tests/test_rule_sync.py` (the slice-1 precedent). Three more were TRIMMED where
the consolidation made half of them a call to the same object twice —
`test_the_three_recognized_status_values_are_mutually_exclusive`,
`test_the_need_reader_agrees_with_both_heading_scrapers` and
`test_draft_ness_reads_by_the_rule_the_file_was_written_under` each lost a
`TRACE.x == GATE.x` limb and kept its real claim. Two replacements landed:
`test_the_spine_row_vocabulary_is_one_home` (IDENTITY, `is` not `==`, which is
the deletion's warrant) and three by-VALUE batteries holding the half of the
retired pins that was never about sameness — the four retired Status spellings
answering False, review 017's whitespace-padded exempt method, the whole-text SN
scrape.

**Pins deliberately KEPT** because they still guard genuinely-duplicated policy
elsewhere: `test_is_example_agrees_across_all_three_copies_including_none`
(`gen_release_checklist` is still a third home — item 4's business, not this
slice's), the `[checks]` enablement trio, the carrier reader/writer inverse, the
ref splitters, `test_is_drifted_has_exactly_ONE_home`, and the
retired-Status-word grep and vocabulary assertions (all three now also assert
against `kitlib.spine`, which is where a resurrected predicate would have to
appear).

### The copy disagreement found

`trace.LLR_EXEMPT` was a `tuple`; `spine_rules.LLR_EXEMPT` was a `set`. The pin
that existed to catch exactly this class read
`set(TRACE.LLR_EXEMPT) == set(GATE.LLR_EXEMPT)`, so the TYPE never entered the
assertion — structurally blind, the same shape as the comment-only drift slice 1
found in the spec-folder copies. Both answer `in` identically, so nothing was
observably broken; the surviving behaviour is a **`frozenset`**, chosen over
either original because a mutable closed vocabulary handed out by a shared kernel
can be moved by any one caller for every other reader in the process. The type is
now part of the pin (`test_the_llr_exemption_answers_by_value`).

`sn_draft_ids` is the one member of the pair that could not move: its body
delegates to `spine_carrier`, and this package's single asserted rule is that it
imports no sibling of `scripts/` — a `kitlib` module reaching for a sibling would
smuggle the whole script graph into the scaffolder. So the duplicate is retired
the OTHER way: both modules now bind the carrier's function directly under the
same local name, and two wrapper bodies plus their duplicated docstrings
disappear without a home here. That is a better outcome than relocation would
have been and it is recorded as the design, not as a shortfall.

### Cross-component / kernel handling

No new cross-component edge, so **no `docs/kernel-modules-allow` entry**, and
that is the sanctioned answer rather than a silenced finding. Every consumer of
the new module — `trace.py`, `trace_text.py`, `spine_rules.py` — is `CMP-006`,
the same component `LLR-197` tags the module itself. `cross_component_findings`
reports nothing on these edges (verified: `check_trajectory.py --root . --strict`
is error-free and names none of them), and that file's own header criteria are
not met: a module whose real consumers do NOT span components is not kernel, and
declaring it would silence edges before they exist. `station.py`'s absence from
that file is the precedent. The WI-440 multi-membership advisory keeps surfacing
the module if a consumer outside CMP-006 ever appears.

### Census

Both readings taken with the SAME command — the named script WI-507 made
standing, not a re-typed `python -c` one-liner — in one sitting:

- before: **15 / 15 / 202**
  <!-- fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev=d00a8506 -->
- after: **6 / 6 / 76**
  <!-- fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev=d00a8506-dirty -->

**15 -> 6 groups, 15 -> 6 copies, 202 -> 76 redundant lines.** The
`docs/stack.ini` `[dupes-census]` baseline is re-stamped DOWNWARD to 6/6/76 in
this commit, per its own downward-only rule, with the reason in the file. The six
residuals are exactly items 4 and 5 of the WI-448 owed list plus the two intra-
`kitlib` pairs: `_process_check` x2, `_norm_module` x2, `sn_rows`/`_sn_rows`,
`field_block` (evidence/stage), `spec_work_dir`/`work_dir_for`, and
`_split_tokens`/`split_refs`.

### Ratchets re-stamped

- `tests/test_module_size_ratchet.py` `"trace.py"`: **5460 -> 5373 (-87)**,
  re-stamped DOWN in the same commit rather than left as headroom, per that
  file's rule.
- `docs/stack.ini` `[dupes-census]`: **15/15/202 -> 6/6/76**, as above.

### Deviations from the brief

1. **A new `kitlib` module rather than `kitlib/registry.py`.** The brief named
   `registry.py` as the natural home for registry-policy predicates and asked the
   choice be recorded; it is recorded above and it went the other way, for the
   themed-modules constraint and because it would have grown the package's
   largest file.
2. **`refs` and `is_example` rode along** although item 4 names `is_example`.
   They are not optional: `sn_all_ids` and `sn_cited_ids` are written on them, so
   moving those two without them would have left the shared functions calling
   module-local copies. Only the `trace_text`/`spine_rules` pair moved —
   `gen_release_checklist`'s third `is_example` copy is untouched and its pin
   still has real content, so item 4 keeps its population.
3. **Item 2 (`STACK_OI3_ROW`) did NOT ride along.** The open-items key vocabulary
   did not appear anywhere in this movement — `bootstrap.py`'s duplicate is a
   TOML row emitter against `spine_carrier.REGISTRY_KEYS`, an unrelated surface —
   so it stays owed, and its stale pin comment stays for that slice to correct.

### Gates (Windows, `-n auto`) — real output, none sanctioned

- `python -m pytest -q -n auto -m smoke`: **1266 passed, 5 skipped in 25.43s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d00a8506-dirty -->
- `python scripts/check_smoke_budget.py --mode enforce`: **22.2s vs 60s budget
  -> within** (the WI-496 re-tier's reading holds; the tier gained no member)
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=d00a8506-dirty -->
- `python project-trajectory/scripts/check_docs.py --root . --stale`:
  **OK — 1031 doc(s), 1355 intra-repo link(s), 0 broken (1 orphan warning)**
- `python project-trajectory/scripts/check_trajectory.py --root . --strict`:
  **exit 0** — and specifically no `cross_component_findings` on the new module's
  edges, and no unresolved-CodeSymbol warning (the `Implements: SR-049, LLR-147`
  tag was removed from `sn_cited_ids` on arrival, with the reason in its place:
  `spine_stage`, the rung that reads the set, did NOT move, so LLR-147 stays
  whole on `spine_rules.py` and `LLR-197` claims the module).
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w448` (full, unfiltered —
  required here because this is a broad script change): **2904 passed, 14
  skipped in 992.38s (0:16:32)**
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w448" rev=d00a8506-dirty -->
- **Scaffold sanity, the standing lesson**: a real scaffold bootstrapped to the
  scratchpad (`bootstrap.py --dest … --stack python`) receives all NINE
  `scripts/kitlib/*.py` modules; in it, `trace.py --strict-integrity` exits 0,
  `derive_stage.py` writes `DevStg-Reqs`, and an in-scaffold import asserts
  `trace.is_approved is kitlib.spine.is_approved is spine_rules.is_approved`
  and `trace.is_drafted is trace_text.is_drafted`. The MAPPING row is therefore
  verified where it can actually be wrong, not only in this repo.

Two ratchets moved, both DOWN except the manifest: `trace.py` 5460 -> 5373,
`bootstrap.py` 3109 -> 3116 (one MAPPING row + its reason comment — a manifest
growing, which is what a manifest does; the axis complaint OI-16 records applies
unchanged). `docs/id-watermark` bumped LLR 196 -> 197 and TC 192 -> 193 via
`trace.py --bump-ids`, never by hand.
