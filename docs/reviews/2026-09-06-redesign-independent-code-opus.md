# redesign-independent-code — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `5c4d981d52dcab170ea1b0804a2cdf0eb2520fe913ff6712a1d17f5926c92b38`

Tracked invocation: [session log](../iteration/call_41c8df5ee5da45eeb70b1b9887868e3c-20260906-095940.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

# Adversarial review — H1 / `--status` / prompt-catalog slices

**Verdict: CHANGES_REQUESTED** (3 findings; none require redesign, all are ≤5-line fixes)

---

## B1 — `_canonical_need_ref` silently drops the `.md` alias on Windows

`plan_briefs.py`:

```python
canonical = {NEEDS_REL, str(Path(NEEDS_REL).with_suffix(".md"))}
```

`str(Path(...))` yields the **native** separator. On Windows this set is
`{"docs/requirements/stakeholder-needs.toml", "docs\\requirements\\stakeholder-needs.md"}`.

Counterexample: a WI row carrying `SpecRef = "docs/requirements/stakeholder-needs.md#SN-1"` (the spelling every registry cell uses, and the exact carrier a mid-migration adopter still has live) matches nothing on Windows → `_canonical_need_ref` returns `None` → the declared parent is dropped **silently**, no refusal, fewer hats in the brief. Same row on macOS/Linux resolves. That is a platform-dependent decomposition brief, which this kit CI-tests both ways.

Smallest fix:

```python
canonical = {NEEDS_REL, Path(NEEDS_REL).with_suffix(".md").as_posix()}
```

(`NEEDS_REL` is also already defined in `hats.py` with the same value — importing `hats_roster.NEEDS_REL` removes the second home and the whole hazard.)

## B2 — the alias test cannot fail; it green-lights the dropped path

`test_plan_runner_scope_resolves_toml_spec_ref_as_markdown_need_alias` asserts `== ["SECURITY"]`. The `.md` fixture needs carry **no** `scope`/`tags`, so resolving SN-1 selects exactly the same set as not resolving it. Replace the whole body of `_canonical_need_ref` with `return None` and this test still passes — it is byte-identical in outcome to `test_plan_runner_scope_ignores_unrelated_goal_specref` two tests above. It is therefore reading silence, and it is the only coverage of the alias branch B1 breaks.

Smallest fix: drive the alias through a **refusal** it cannot reach otherwise — e.g. a second arm asserting `HatsError` `unknown SN id(s) SN-404` for `stakeholder-needs.md#SN-404` under `need_carrier="md"`. That proves the fragment was parsed and the carrier resolved, and it fails on Windows today, which is the point.

## B3 — the re-sync path ships the generator but not its mandatory artifact

`initialize_generated_docs` returns early unless `docs/status.md` was **created** — true only for a fresh scaffold. So an existing adopter who re-syncs now receives `scripts/gen_prompt_catalog.py` (new MAPPING row) with **no** `prompts/CATALOG.md`, and the shipped `prompt-catalog` harness step runs `--check` against a missing target → red harness after a documented re-sync, with nothing telling the operator what to run.

This is demonstrated by the diff's own evidence: `test_node_adopter_upgrade_preserves_populated_owner_content` hand-runs `run_py(["scripts/gen_prompt_catalog.py"], cwd=supported)` in the supported path. That call is the fix, performed by the fixture, and it is not in `RESYNC_PACK.md` §3. Consequently the test's later `assert "PASS  prompt-catalog" in harness_output` is attributable to the manual line, **not** to this diff — only `test_fresh_node_scaffold_generates_its_required_prompt_catalog` demonstrates the initialize half.

Smallest fix: one `RESYNC_PACK.md` §3 per-change entry ("kits after `<sha>` ship `scripts/gen_prompt_catalog.py`; run it once — a re-sync never generates another generator's artifact"). Do **not** relax the `created` gate; that rule is load-bearing and stated in the function's own docstring.

---

## Cleared on inspection

- **Cross-parent AND / non-composition.** `_hat_parent_context` unions WI tags into each parent separately and `hat_surface_for_work_item` projects the selected *names* back through roster order — deterministic, no sibling bleed. Correct.
- **Malformed / unknown / absent carriers.** `HatsError` for unknown SR/SN ids and absent declared carriers; `SystemExit` (parse/dual-home) now inside the intake boundary, converted to `PAGE` with the reader's own reason. Moving `build_surface` into the `try` is the right repair.
- **Roster absent = opt-out** returns before any parent read (`test_..._does_not_read_parent_refs_when_roster_is_absent` is non-vacuous: it pairs absence with an unresolvable `SR-MISSING`).
- **Legacy no-slot override** unchanged, warn-only, and proven not to read parents (`malformed_sr=True` + `{}`).
- **LLR-176 / SR-175.** `build_surface` untouched; the hat read is a separately named function over declared inputs. No consent/egress claim is made or implied. Correct as written.
- **`--status` import independence.** The `runpy` + `meta_path` deny-finder is a genuine execution proof, not a source-text grep; `_STATUS_ONLY` is `False` for in-process imports so the facade stays whole. `--root=--status` is exact-membership-safe; `--root --status` fails in argparse before any name is touched. No `NameError` path found.
- **Ratchet arithmetic.** +2 SLOC (one MAPPING tuple, one list entry) → 1663. Correct.

## Freeze-run risk (not blockers, name them in the full run)

Only two focused tests exercised P0a. The MAPPING/exclusion move changes `delivery_inventory()` classification, and the new scaffold now emits a catalog file not listed in `generated`. Re-run **`test_bootstrap*` scaffold-manifest / byte-comparison and the SR-163 delivery-inventory tests** before claiming P0a; the new bare MAPPING pair also adds one unmapped-entry warning to the SR-163 burn-down (consider carrying the reference cell).

Minor: the ratchet's new note sits *above* the entry while the inline comment still reads `+1 (1660 -> 1661)`, so the line contradicts its value; fold it into the inline chain and cite a concrete path, not "the execution record".
