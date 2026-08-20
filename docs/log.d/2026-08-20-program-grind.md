## 2026-08-20 — The program grind, in series (owner directive, second batch): per-WI record

The owner's directive for this batch: grind the open PROGRAM frontier in
series with opus/sonnet workers routed by BuildTier (strong→opus,
medium→sonnet), one large adversarial review (internal Opus + cross-family
Sol via codex, medium effort) at the end, consolidated and iterated in one
action. One entry per WI as its session ends; adjacent findings accumulate
at the bottom for the closing review. Program rows that cannot honestly
complete in one session land their largest coherent slice and record the
remainder — no false completes.

Deferred open items: none — declarations accumulate per section as the
grind runs; this top-matter line is re-derived to the union at the batch
close (the WI-485 fragment-scope lesson applied from the start).

### WI-448 — the common-module inversion (opus worker) — SLICE landed, row stays active

**Slice 1 of a program row.** Landed to `docs/work/active/wi448-common-module/`,
not `complete/`: the row is honestly unfinished and its spec's Context now
carries the five numbered items still owed. The largest of them — 33 remaining
`_utf8_console` copies — is 264 of the 477 redundant lines that survive, so
closing here would have been a false complete by more than half the residue.

Deferred open items: OI-48 — which component owns the shared kernel.

**What shipped.** `project-trajectory/scripts/kitlib/`, the kit's first shipped
package: `config` (the declared-policy line reader plus its two adapters),
`git` (the best-effort-off-git pattern), `registry` (the `docs/work/`
spec-folder reader). THEMED, never one generic `common.py` — the 2026-08-19
review's H-09 shape, adopted. `station` and `views` are named by that shape and
deliberately NOT created empty: an empty module is a worse statement than an
absent one.

**The inversion, which is the load-bearing half.** D-8's literal step 2 (import
FROM `bootstrap.py`) is unbuildable — `bootstrap.py` is deliberately absent from
its own `MAPPING`, so a shipped script importing it ImportErrors on a fresh
scaffold while passing here, where the kit folder holds every file. That is the
exact failure this repo shipped once with `schedule.py`. So the package ships
and the scaffolder imports it. **The replacing rule stopped being a comment**:
`test_bootstrap_imports_only_the_common_package` asserts bootstrap's sibling
imports are exactly `{kitlib}`, and that no `kitlib` module imports a
non-`kitlib` sibling — the second half matters, or the one sanctioned edge
smuggles the whole graph into the installer.

**Verified by BOOTSTRAPPING A REAL SCAFFOLD**, per the standing lesson, not by
unit tests alone: the package landed whole and `check_trajectory`, `trace`,
`derive_gate`, `check_privacy`, `schedule` and `subagent_gate` all ran there.

**The guard that could not have caught it, and the one built because of that.**
`test_every_sibling_imported_module_is_shipped_by_mapping` compares TOP-LEVEL
import names, so once ANY `kitlib` row is in MAPPING the name reads as mapped
and a missing module INSIDE the package is invisible to it. Probed, not
assumed: deleting the `config.py` row leaves that guard GREEN. Per-file
completeness is a manifest question, so `test_the_common_package_ships_complete`
asks it of a real scaffold — and the same probe reds it, naming the missing
file.

**Duplication figures — the deferred P5 ratification's basis.** One command,
run at both revisions:

| | groups | redundant copies | redundant lines |
|---|---|---|---|
| before (`b94bf58c`) | 24 | 67 | 757 |
| after | 17 | 48 | 477 |

What it does, in readable form — hash each function's body with its docstring
stripped, keep bodies of 4+ lines, and count the groups with more than one
member, the members beyond the first, and their lines:

```python
# equivalent of the declared command below, which is quote-free only because
# the marker grammar reserves the double quote for its own attribute delimiter
groups = defaultdict(list)
for p in sorted(Path("project-trajectory/scripts").rglob("*.py")):
    if "__pycache__" in p.parts:
        continue
    for n in ast.walk(ast.parse(p.read_bytes())):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = strip_docstring(n.body)
            lines = n.end_lineno - n.lineno + 1
            if body and lines >= 4:
                groups[sha1_of(body)].append(lines)
dups = [v for v in groups.values() if len(v) > 1]
# len(dups), sum(len(v) - 1 for v in dups), sum(sum(v[1:]) for v in dups)
```

<!-- fig: cmd="python -c 'import ast,hashlib,pathlib,collections;P=bytes([112,114,111,106,101,99,116,45,116,114,97,106,101,99,116,111,114,121,47,115,99,114,105,112,116,115]).decode();G=bytes([42,46,112,121]).decode();C=bytes([95,95,112,121,99,97,99,104,101,95,95]).decode();B=lambda n:(n.body[1:] if n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str) else n.body);g=collections.defaultdict(list);[g[hashlib.sha1(chr(10).join(map(ast.dump,B(n))).encode()).hexdigest()].append(n.end_lineno-n.lineno+1) for p in sorted(pathlib.Path(P).rglob(G)) if C not in p.parts for n in ast.walk(ast.parse(p.read_bytes())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and B(n) and n.end_lineno-n.lineno+1>=4];d=[v for v in g.values() if len(v)>1];print(len(d),sum(len(v)-1 for v in d),sum(sum(v[1:]) for v in d))'" rev=b94bf58c -->

Run from the repo root at each revision; both figures above were produced by
that exact command. Read the numbers honestly: the population is
identical-after-docstring-stripping function BODIES of 4+ lines under
`project-trajectory/scripts/`, so it counts EXACT clones and is blind to a
DIVERGED copy — which is the dangerous kind, and the reason the retired
`check_dupes` census was torn down (D-7). **33 of the 48 surviving copies are
the one `_utf8_console` body**, so the residue is one pending slice plus a long
tail, not 48 distinct problems.

**Two findings the extraction produced rather than assumed.**

- The three spec-reader copies were **not** "copied VERBATIM" as their own
  shared header claimed. `agent_common`'s carried `a DevStg-* value` where the
  other two carried the literal `DevStg-Reqs|DevStg-Tests|DevStg-Impl` enum — a
  comment-only drift from the 2026-08-18 one-vocabulary rename reaching two
  homes of three. Behaviour-equal, so the behavioural pin was structurally
  blind to it: exactly the class D-7 accepted when it chose pins over
  extraction. The more informative spelling is the one kept.
- The subagent gate's two divergences (lowercased result, `""` sentinel) did
  not need harmonizing away. They survive as a stated ADAPTER over the shared
  rule, so a contract that used to be re-argued inside a duplicate body is now
  written once.

**Pins deleted, with the reasoning in their place.** The two `test_rule_sync`
equality tests over the declared-line copies are gone: with one function behind
five names, "the copies agree" cannot fail, and a test asserting a function
equals itself is not a weaker pin but a VACUOUS one — this file's own
`_sn_fields` lesson. An identity test replaces them; the subagent divergence
stays pinned BY VALUE because it is still a real choice. Drift is now
unrepresentable rather than detected, which is the stated preference.

**Three guards had to learn what a package is**, or they would have gone blind
or false-red on the kit's own code: the MAPPING sibling walk (blind), the
dependency-ledger scan (`kitlib` is not a "dependency" — it demanded a
`docs/dependencies.md` row for a file in this very repo) and the shipped-tier
bar (same false red, and its walk would never have opened the package's own
modules, so a real dependency hidden inside `kitlib/` would have been invisible
to the bar it is most subject to).

**Ratchet re-stamped deliberately, in BOTH directions.** `agent_common` −233
and `check_trajectory` −227 re-stamped downward, as that file's rule requires;
`bootstrap` +40, `check` +3, `trace` +3 bumped with reasons in each entry. The
bump on `bootstrap` is the owner's own correction showing up in practice: its
DECLARATION grew by a MAPPING block stating the ruling's whole downstream risk
surface while its IMPLEMENTATION shed two duplicated bodies — a line ratchet
asking for a reviewed bump on a file that got simpler. Banked below as the
ratchet-axis finding; not redesigned here.

**Spine.** `LLR-181` + `TC-176` minted Drafted, `OI-48` minted open. The LLR
first grounded on `SR-010`, and that dropped **phase 1 from DevStg-Tests to
DevStg-Below**: `derive_gate._per_phase` buckets an LLR by its PARENT SR's
phase, not by its own `phase` cell, so a Drafted row under a phase-1 SR drags
that phase down. Caught by diffing the regenerated status block, not by a gate.
Fixed by grounding on **`SR-166`** instead — the better parent on the merits
("whether what was promised ARRIVES WHERE IT WAS PROMISED … at its declared
destination in a fresh scaffold") and phase 5, where the drafts already sit.
Phase 1 is back at DevStg-Tests and no unrelated gate moved.

**OI-27's obligation is met** by a `RESYNC_PACK.md` §3 entry, SHA-anchored at
the preceding commit per the convention — the ruled home under OI-27's (e),
rather than a fourth prose recipe.

**Gates.** Line endings checked BEFORE trusting any count
(`git ls-files --eol | grep 'w/crlf'`): no file this session touched appears,
and the index is LF throughout.

- smoke: `1244 passed, 5 skipped in 66.21s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b94bf58c-dirty -->
- `check_docs.py --root . --stale`: `OK - 960 doc(s), 1323 intra-repo link(s), 0 broken (1 orphan warning(s))`
- `check_trajectory.py --root . --strict`: exit 0. The baseline at `b94bf58c`
  was also exit 0 (50 warn lines); the kitlib work transiently made it exit 1
  (4 modules in no CMP component) and the `LLR-181` row cleared it. The red was
  closed with a real spine row, never by touching `[checks] components_check`.

### Adjacent findings accumulating for the closing review

_(per-WI sections are inserted ABOVE this section, in close order; banked
findings accumulate below as list items)_

- **The module-size ratchet measures the wrong axis, and WI-448 is the second
  witness the owner's own correction predicted** (OI-16: "the monolith risk was
  always about FUNCTION size and complexity, not file length"). Concretely:
  `bootstrap.py` shed two duplicated helper BODIES and gained a MAPPING
  declaration block, and the line ratchet demanded a reviewed bump on a file
  that got structurally simpler; meanwhile `agent_common`/`check_trajectory`
  each lost 230-ish lines of pure duplication and the ratchet's only response
  was "re-stamp downward". Neither direction told anyone anything about
  complexity. Note the axis it wants ALREADY EXISTS unused-for-this-purpose:
  `tests/test_complexity_ratchet.py` runs ruff `C901` per function and, unlike
  the line ratchet, RECURSES into packages. NOT redesigned here, deliberately —
  filing it is the WI's instruction. The question for the owner is whether the
  line ratchet retires in favour of the complexity one, or the two keep
  different jobs with the line one demoted to advisory.
- **The line ratchet is blind to packages.** `test_module_size_ratchet._census`
  globs `scripts/*.py` (top-level only), so every module under
  `scripts/kitlib/` is uncensused — a 3,000-line module could land there and
  the ratchet would never see it. Not fixed in WI-448 because the fix forces a
  keying decision (`path.name` collides once two packages hold a `registry.py`;
  `test_complexity_ratchet` already keys on the relpath) and that is the same
  axis question above. Cheap to fix, but it should be fixed WITH the ruling,
  not before it.
- **~47 tracked files carry CRLF in the working tree while the index holds LF**
  (`git ls-files --eol | grep 'w/crlf'`): 33 `docs/iteration/*.log`, 8 `*.md`
  including two `byte-budget-guard/SKILL.md` copies, 3 `tests/*.py`,
  `docs/process.toml`, `docs/stack.ini`, `project-trajectory/process.toml.template`.
  A fresh worktree of the same commit has only the expected `*.cmd`/`*.ps1`, so
  this is local working-tree residue, not committed state — but the standing
  hygiene rule says only `ps1`/`cmd`/`bat` may appear, and anyone following it
  literally will now see a false alarm and learn to ignore the check. Either
  the tree gets renormalized or the rule's wording admits the `i/lf w/crlf`
  case explicitly.
- **`tests/test_rule_sync.py`'s `test_bootstraps_scaffolded_brief_uses_the_converters_own_keys`
  now rests on a premise WI-448 overturned.** Its comment says `bootstrap.py`
  "runs BEFORE the kit is copied and can import no sibling (repo-lock §8.2)" —
  bootstrap now imports `kitlib`, and D-8 measured that premise as weaker than
  its own comment claimed (the documented path runs it from INSIDE the kit).
  The pin itself is still correct and still needed; only its stated reason is
  stale. It gets corrected when the `STACK_OI3_ROW` duplicate is shed, which is
  item 2 on WI-448's remaining list — flagged here so the stale reason is not
  read as current doctrine in the meantime.
- **`spec_move.py` silently creates a FILE where a lane DIRECTORY was meant,
  and the work item disappears from the registry.** Hit live this session:
  `spec_move.py <spec> docs/work/active/wi448-common-module/` (trailing slash,
  destination absent) wrote the spec to a file literally named
  `docs/work/active/wi448-common-module`. `spec_files` only yields
  `WI-*.md` under a status directory, so the row vanished from the registry
  entirely — `trace.py` and the dashboard simply stopped seeing WI-448.
  Two things made it survivable and both were luck rather than design: the
  destination happened to be referenced by another row (`WI-483`'s
  `~WI-448` predecessor), so `check_trajectory --strict` reported
  "predecessor 'WI-448' is not a work item"; and the tool's own relink pass
  rewrote a live archive link to the bogus path in the same act. A row with no
  dependents would have gone missing with NO finding at all. The tool already
  REFUSES a destination directory that exists ("REFUSED - the destination
  ... already exists"), so it clearly reasons about directory-ness; it should
  equally refuse (or mkdir) a trailing-slash destination that does not, rather
  than falling back to treating it as a filename. Worth a row of its own.
