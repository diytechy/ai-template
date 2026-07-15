# 093-REVIEW-A — WI-152 (knowledge home — `docs/knowledge/README.md` + bootstrap scaffold wiring + tests)

Independent review of commit `7016736` (WI-152: scaffold the knowledge home),
built session 092. Reviewed the diff against the spec-of-record
(`docs/specs/research-knowledge.md` §3a/§4.1/§8.1), the WI-152 registry row
(`WI-145`, `research-knowledge` campaign, phase-default tier), the bootstrap
`MAPPING` + `test_bootstrap` contract, and the `check_docs` doc-graph rules the
scaffolded index must satisfy. No SN/SR/LLR/TC rows were added or changed (the
diff touches only a WI Status/Notes flip, a WI-153 `BuildTier` pin, and the
knowledge-home surface), so no registry sweep applies; derived gate is **G3**,
run-phase **BUILD**, not a `[phase]-[g*]` Status-change ratification, so no
`--ratify` hierarchy applies.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check.py --gate all` → **RESULT: PASS** —
  all 16 steps PASS incl. `tests+coverage` (191.6s), `format`, `lint`, `dupes`,
  `registry-integrity`, `derived-gate`, `traceability`, `privacy`,
  `doc-navigability`, `arch-map`, `trajectory-map` (`gen_trajectory --check` →
  "project-state dashboard up to date"), `okf` (`--check` up to date, 257
  files), `skills-sync` (10 per-agent copies match), `trajectory`.
- `python project-trajectory/scripts/trace.py --root .` → `SN=24 SR=56 LLR=57
  TC=57 orphans=0 integrity=0 components=5 component-findings=0 interfaces=52
  interface-findings=0`.
- `python project-trajectory/scripts/check_trajectory.py --root .` → `clean (170
  work item(s), 150 done (88%), graph acyclic)` — matches the regenerated
  `PROJECT_STATE.html` (150/170).
- `python project-trajectory/scripts/check_docs.py --root . --stale` → `OK - 98
  doc(s), 418 intra-repo link(s), 0 broken (40 orphan warning(s))`; all 40
  orphans are pre-existing (reviews, `docs/specs/*`, `report.md`), none from this
  diff — the new template lives under `project-trajectory/` and is outside the
  scanned root+`docs/` doc graph.
- `python -m pytest tests/test_bootstrap.py -q` → `39 passed`.
- **Real scaffold** (`bootstrap.py --dest <tmp> --stack python`): produces
  `docs/knowledge/README.md` verbatim from the template; its `../process.md` /
  `../process-options.md` links resolve to the scaffolded files;
  `check_docs --root <scaffold>` → `0 broken`, the knowledge README is **not**
  an orphan (reachable from the project-README entry-root link on line 68), only
  the pre-existing `docs/test/report.md` orphan remains.

## Assessment

The deliverable matches §8.1 exactly and is correctly scoped to the home only —
the warn-first `Knowledge`-ref resolution and knowledge⇒component coupling are
WI-153, and the meta-repo dogfood is WI-155, both correctly left out. The pack
contract is faithful to §3a on every point: one-topic-per-file/filename-is-label,
the "records only what no registry can" list (evidence, rationale, vendor/tool
quirks, failed approaches, external refs **with retrieval dates**), the
link-ids-don't-restate rule, the advisory/never-gates + change-intake promotion
rule, and "a durable module spec = the CMP row + its refs, not a parallel spec
tree". The `MAPPING` entry, `test_bootstrap` file-list, the load-bearing-contract
assertions, and the project-README entry-root link all land, and the whole G3
suite is green. The WI-153 `BuildTier=medium` pin folded into this commit is the
mechanism by which `next-wi=WI-153` hands off a medium starting tier (WI-126
reads the row's `BuildTier`), is disclosed in log.md, and is documented with
rationale in status.md — integral to the handoff, not an unrelated-WI triage, so
it does not draw a finding. Bookkeeping is forward-only and coherent (WI-152
dropped from the status queue and Next-action, `next-wi` → WI-153, WI-164 prose
de-referenced from the now-done WI-152); declared policies match the prose
(`push-policy: human` → "Not pushed"; run-state RUNNING).

One MINOR remains. The spec assigns the scaffolded index the job of keeping packs
out of the orphan set (§3a: "a scaffolded `docs/knowledge/README.md` indexes
them, so packs aren't orphans"; §4.1 a "pack index table"), and the template's
own line 28 says "Add every pack here so documentation checks can discover it."
But `check_docs` reachability follows markdown doc→doc links, and the example row
(line 32) demonstrates a **code-span** label `` `example` ``, not a link. I
confirmed empirically: adding a pack and an index row in the exact example format
leaves the pack an orphan (`WARN - orphan doc: docs/knowledge/foo.md`); switching
the label to a link (`` [`foo`](foo.md) ``) clears it. So an adopter copying the
example format gets exactly the orphan the index is meant to prevent. Warn-first
(orphan is a warning, not a gate failure) and the WI's tests pass because they
never add a real pack, so this is MINOR, but it undercuts the copy-ready intent
of the index and the property §3a assigns to it.

## Findings

- [MINOR] project-trajectory/knowledge/README.template.md:32 -> the pack-index example row uses a code-span label `` `example` `` rather than a markdown link, but `check_docs` discovers packs only via doc→doc links, so a pack added in the example's own format stays an orphan (confirmed: adding `docs/knowledge/foo.md` + an example-format row yields `WARN - orphan doc: docs/knowledge/foo.md`; a linked label clears it) — defeating line 28's "so documentation checks can discover it" and spec §3a's "indexes them, so packs aren't orphans" -> render the example Label as a link to its pack file, e.g. `` [`example`](example.md) ``, so a copied row makes the pack reachable -> @owner

VERDICT: APPROVE findings=1
