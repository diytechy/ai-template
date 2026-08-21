## 2026-08-20 — The program grind, in series (owner directive, second batch): per-WI record

The owner's directive for this batch: grind the open PROGRAM frontier in
series with opus/sonnet workers routed by BuildTier (strong→opus,
medium→sonnet), one large adversarial review (internal Opus + cross-family
Sol via codex, medium effort) at the end, consolidated and iterated in one
action. One entry per WI as its session ends; adjacent findings accumulate
at the bottom for the closing review. Program rows that cannot honestly
complete in one session land their largest coherent slice and record the
remainder — no false completes.

Deferred open items: OI-48, OI-49, OI-50 — the running union of the per-section
declarations below, re-derived as each session closes (the WI-485
fragment-scope lesson applied from the start). OI-49 and OI-50 joined at the
WI-455 close.

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

- **full unfiltered suite, on the LANDED commit**: `2685 passed, 14 skipped in
  571.42s (0:09:31)`
  <!-- fig: cmd="python -m pytest -q -n auto" rev=46de9442 -->
  The pre-fix run of the same command was `7 failed, 2677 passed, 14 skipped in
  498.73s` — all seven were the predicted guard classes (the two package-blind
  scans, the isolated-copy fixture, the size ratchet, the uncontained-module
  view), and every one was FIXED rather than waived.
- smoke: `1244 passed, 5 skipped in 66.21s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b94bf58c-dirty -->
  Re-run on the landed commit: `1244 passed, 5 skipped in 134.16s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=46de9442 -->
  **Read the 134s as contended, not as a budget measurement** — the full suite
  above was still finishing on the same box when it started. The uncontended
  figures this session are 66.21 s and 71.97 s, both already past the 60 s
  ceiling `docs/stack.ini` declares. That is consistent with CLAUDE.md's own
  2026-08-20 record for this box (54.9 / 64.0 / 55.7, one over), so nothing
  here is new evidence and the budget is NOT moved to fit it. One box is one
  data point.
- `check_docs.py --root . --stale`: `OK - 960 doc(s), 1325 intra-repo link(s), 0 broken (1 orphan warning(s))`
- `check_trajectory.py --root . --strict`: exit 0. The baseline at `b94bf58c`
  was also exit 0 (50 warn lines); the kitlib work transiently made it exit 1
  (4 modules in no CMP component) and the `LLR-181` row cleared it. The red was
  closed with a real spine row, never by touching `[checks] components_check`.

### WI-455 — the architecture.md retirement program, crossing half (opus worker) — SLICE landed, lane stays active

**Slice 2 of a program row.** `docs/architecture.md` was already retired by
slice 1; what the lane still owed was the interface/boundary remainder. The
CROSSING half of that is now done and the SCHEMA half is not — and it is
BLOCKED, not merely unstarted, so closing here would have been a false
complete. Spec Context now carries the three owed items with their blockers
named.

Deferred open items: OI-49, OI-50 — both minted this slice (see below).

**B-01 and B-04's hook half now have a FACING, and the choice between the two
shapes is the substance.** WI-459 handed this lane two options: tie-backs on
IF-040/IF-042/IF-043, or new external-facing hook rows. Took the second. Those
three rows state which SCRIPT the hook runs — an internal call between two
in-tree endpoints — while the crossing is the contract git holds the hook to,
and the registry's own rule is that a row ties back only when it REALIZES a
crossing. A tie-back on them would have claimed a realization their contracts
do not state; WI-459's own analysis had already named the gap as a missing
FACING rather than a missing surface, which is exactly the distinction a
tie-back cannot supply. So `IF-134` (pre-commit) / `IF-135` (pre-push) minted
Drafted, `owner = LLR-019 / LLR-020`.

**The owner cells went to the DESIGN tier although WI-459 named SRs**, and the
divergence is deliberate: the schema header prefers the design tier wherever a
design row exists for the owner-side endpoint, and here that row IS the hook
module, so the derivability advisory agrees by construction rather than by
luck. `SR-019`/`SR-020` keep the crossing's ownership through `req_refs`,
which is the cell that means "the requirements this seam realizes".

**One tie-back deliberately NOT made, recorded on the row rather than
smoothed.** `IF-135` carries `B-04` only. `SR-020` names both crossings, but
what pre-push gates is content LEAVING while `B-01` is *"the one write path
from the session into the system's governed state"*. Claiming it would have
widened a LOCKED crossing by assertion. The row says so, and says what would
change the answer: if the frame means B-01 to cover the whole hook floor in
both directions, the crossing's text is what needs widening, not this row's
attribution. Same shape SR-137 already uses for its own recorded strain.

**The five untied `external:` rows, adjudicated one at a time — and they did
not take one answer.** `IF-080`/`IF-081` were plain omissions (integrate.py and
trunk_step.py are both in `bootstrap.MAPPING`, so they are delivered package
content) and now tie to `B-05`. The other three keep NO tie-back, each with a
DIFFERENT reason written into the row, because the absences are not the same
fact: `git` is dissolved into the entity that holds the checkout, so `IF-032`
reads this system's own working copy rather than exchanging with a fourth
party; `IF-041`'s far side is already ruled an external-to-external
relationship touching the session and not the system — and the contrast that
makes it precise is `IF-020`, which faces the SAME CLI and DOES tie back,
because a guardrail verdict this system emits is a system output whoever
consumes it; `IF-036`'s far side is a party the locked frame names no entity
for AT ALL, which is a gap in the FRAME and is queued rather than papered over.

**`B-02` stays unrealized on purpose, and the reason MOVED to where a reader
meets it.** The ruling existed but lived in a closed WI's `## Close`, where
nobody reading tie-backs would ever find it — so the header now states it with
the `SR-140` condition that would change the answer. External.toml was NOT
touched: it is Approved and LOCKED, and the reason belongs on the Drafted
surface that carries tie-backs, not on the frame.

**The one live derivability fire is CLOSED — by measurement, and the check
that it is a real clear and not a skip is the whole point.** `IF-128` cleared
at the 2026-08-17 owner re-point, before this lane ran. Verified rather than
assumed: the row is `Consumes`, so its owner-side column is `counterpart`
(`scripts/spine_carrier`), and `LLR-166`'s `module` is that module — they agree
inside the predicate, not by falling out of one of its skip branches (a row
whose owner is an SR, or whose owner LLR has no module, would exit early and
LOOK identical in the totals). `docs/test/report.md`: *"None. Every LLR-owned
row's owner-side endpoint agrees with its owner's Module."*

**22 notes cells swept of retired CMP ids, and three of them were FALSE rather
than stale.** `CMP-001..005` retired when the narrow-waist partition minted
`CMP-006..009`; the WI-441 pass re-pointed the `component` CELLS and left the
PROSE. These do not merely dangle, they silently re-point — and `IF-099`,
`IF-100` and `IF-113` each read "the cross-component edge …" about an edge the
partition had made INTRA-component, since the coordinator and the prompt loader
landed in one unit. Those three were re-authored, not renumbered. Each row's
own `component` cell was the mechanical cross-check; `IF-118`'s notes had been
contradicting its own component cell, which is the cheapest tell. Per-pattern
count assertions in the sweep script, so a miscount failed loudly rather than
silently skipping a row.

**Two retired ids deliberately LEFT** (`IF-056`, `IF-077`): both sit inside the
held `Contract`-cell clause the WI-469 pass deletes whole, and correcting a
number inside a sentence already scheduled for removal is two passes for one
fix. Recorded, not forgotten.

**The migrate_carrier framing fixed on all three surfaces** (banked by the
WI-452 worker): `IF-103`'s Contract said "the ONE-SHOT converter", its notes
said "migration scaffolding with a defined end … RETIRABLE once", and the kit
README said the same. The ruling made it a live downstream-resync helper with
NO terminus. Two of those surfaces also still cited `Provisional` — a
`Stability` value whose whole column was retired — so the same edit dropped a
dead vocabulary word from a SHIPPED doc. `RESYNC_PACK.md` got the narrowest
possible correction: the fallback's expiry claim is still TRUE and was left
alone; only the trailing clause that made the converter share that expiry moved.

**The 49-citation hold: re-measured, UNCHANGED, and still held.** Exactly 49
(46 `Contract names WI-###` + 3 `Contract cites decision`). Not swept, because
the recorded hold is bounded by WI-469 and that WI runs after this one — one
pass instead of two is the entire argument, and it still holds.

**Two owner rows minted rather than decided here.** `OI-49` — what the sitting
is actually being asked to ratify from the 2026-08-15 interface rework. The
finding that made the row worth writing: **it cannot ratify "the 21 judgement
picks" as a list, because that list no longer describes the registry.** Ten of
the 21 now hold an `LLR-###` where the log records an `SR-###`, re-picked
legitimately by a later design-tier pass — so a ratification quoting the
2026-08-15 entry would be signing a superseded list. Also surfaced: 2 of the 21
were recorded as BARE PAIRS with no reason (`IF-013`, `IF-044`), and the
`carried_by` prototype has been generalised to three carriers past its own
stated precondition (*"prove it on IF-102 before generalising"*) — `IF-102` now
carries 16 constituents where 14 are recorded, and `IF-131` is a bundle with
exactly ONE constituent, which is a pointer wearing composition's field.
`OI-50` — the locked frame names no party for a vendored upstream source.

**`IF-097` and `IF-080` recorded as CLOSED so they are not re-derived.** Both
were plan-predicted defects that execution refuted; the refutations stand.
Verified in code rather than inherited: `_declared_seam_pairs` genuinely does
not split on `;`, so `IF-097` contributes NO coverage pair — and it is the only
`;`-joined endpoint cell in the registry, a population of one. Harmless today
ONLY because all three consumers sit in CMP-008 with `scripts/prompts`; the
safety is co-location, not design, so moving any one of them silently stops a
seam covering an edge it appears to cover. Stated in OI-49; not fixed, because
the charge-through forbade touching that function's semantics.

**Line endings.** `pathlib.write_text` on Windows translated LF to CRLF on all
three scripted edits — caught by running `git ls-files --eol` BEFORE trusting
any count, exactly as the standing rule says, and normalized back to LF before
staging. The WI-477 worker's lesson, hit again in the same week: a scripted
edit on this box introduces CRLF unless it writes bytes.

**Gates.**

- smoke: `1244 passed, 5 skipped in 65.46s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=3bc20bc8-dirty -->
  Past the 60 s ceiling `docs/stack.ini` declares, consistent with this box's
  own 2026-08-20 record (54.9 / 64.0 / 55.7, one over). Nothing new; the budget
  is NOT moved to fit it.
- full unfiltered suite, on the slice-2 tree: `2685 passed, 14 skipped in
  587.32s (0:09:47)`
  <!-- fig: cmd="python -m pytest -q -n auto" rev=6aff590f-dirty -->
  Same totals as the WI-448 close earlier today, which is the expected
  reading: this slice added registry rows and prose, no test and no script
  behaviour.
  **Read the scope of that run honestly rather than as a blanket green:** it
  was taken with the registry rows, the spec Context and the regenerated
  surfaces all in place, but BEFORE this fragment's own text was written, so
  it does not cover the records commit. Re-run on the landed tree rather than
  argued away — smoke `1244 passed, 5 skipped in 74.78s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=31e00bf5 -->
  and `check_trajectory.py --root . --strict` exit 0, clean (490 work items,
  graph acyclic).
- `check_trajectory.py --root . --strict`: exit 0, clean (490 work items, graph
  acyclic; the pre-existing shared-specref WARNs).
- `check_docs.py --root . --stale`: `OK - 960 doc(s), 1325 intra-repo link(s), 0 broken (1 orphan warning(s))`
- `trace.py --strict-integrity`: exit 0, integrity=0, interface-findings=0,
  interfaces **126 → 128**, and the unrealized-crossing advisory reads **B-02**
  where it read **B-01, B-02**. The regenerated status block was diffed line by
  line: `126 → 128 seams` and nothing else, so no gate or phase moved (the
  WI-448 lesson applied).

### Adjacent findings accumulating for the closing review

_(per-WI sections are inserted ABOVE this section, in close order; banked
findings accumulate below as list items)_

- (WI-455 worker — a CLASS, not a one-off) **a mechanical re-pointing pass
  that rewrites CELLS and not PROSE leaves each row contradicting itself, and
  nothing catches it.** WI-441 retired CMP-001..005 and re-pointed 149 LLR +
  54 IF `component` cells; the `notes` prose naming those same ids was left,
  so **22 IF rows** sat with a notes cell naming a dead component while their
  own `component` cell named the live one — `IF-118` literally disagreed with
  itself. Worse than dangling: the retired ids SILENTLY RE-POINT (old CMP-002
  was "Generators"; today CMP-002 is nothing, so a reader assuming a shift
  lands on the wrong unit), and three rows had become FALSE rather than stale,
  reading "cross-component edge" about an edge the new partition had made
  intra-component. This is mechanizable and cheap: a retired id is derivable
  (at or below the watermark, absent from `components.toml`), so a warn-only
  "a living cell names a retired CMP id" rule would have caught all 22 at the
  renumbering. Swept by hand this session; the DETECTOR is not built, and the
  same gap exists for every other id space a future renumbering touches.
- (WI-455 worker) **`pathlib.write_text` introduced CRLF into three
  LF-indexed files, and this is the second time in one week** (the WI-477
  worker hit it too). On Windows the default newline translation turns every
  LF into CRLF, so any scripted edit that is not byte-mode plants working-tree
  CRLF. Caught here only because the standing rule says to run
  `git ls-files --eol` BEFORE trusting a count. Two workers finding the same
  trap by discipline rather than by machinery is the argument for a check: the
  hook floor already reads staged content and could refuse a file whose index
  is LF and whose working tree is CRLF. Relatedly, this is a third data point
  for the banked ~47-file CRLF-residue finding — some of that residue is very
  likely prior sessions' scripted edits rather than autocrlf alone.
- (WI-455 worker) **`IF-131` is a carrier with exactly ONE constituent.** The
  `carried_by` field exists so several seams can ride one bundle; a bundle of
  one is a pointer wearing composition's field, and it is the tell that a
  concept has been applied past its evidence — step 7 said to prove carriage
  on `IF-102` BEFORE generalising, and there are now three carriers (16 / 3 /
  1). Queued inside `OI-49` rather than fixed, because withdrawing or keeping
  it is the owner's ratification call and not an execution one.
- (WI-455 worker) **the id watermark's next mint for two spaces lands on SPENT
  ids, and the only thing preventing it is a prose block.** `docs/id-watermark`
  reads `B = 7` and `EXT = 5` while `B-06`, `B-07` and `EXT-004` were allocated
  and then CUT, and are cited by id in ruled documents — so a mint from the
  mark re-points that history onto different things. `external.toml`'s header
  says so, and also says that correcting a mis-computed seed needs a mechanism
  the kit does not have. Pre-existing and known; surfaced again because `OI-50`
  could require a `B` mint, and if that row is ruled (b) the seed problem must
  be solved FIRST. A watermark correctable only by hand — which `trace.py`'s
  integrity rule refuses — is a gap with no current answer.
- (WI-455 worker — for the orchestrator, not the closing review)
  `gen_open_items` emits three warnings against OTHER workers' fragments:
  `docs/log.d/2026-08-20-frontier-grind.md:9` declares `OI-45` and `OI-46`
  deferred, and `docs/log.d/2026-08-20-owner-rulings-oi45-46.md:3` declares
  `OI-47` deferred, while all three rows now read `ruled`. Warn-only today,
  but it is exactly the fragment-scope staleness the deferral field exists to
  prevent, and it will read as noise at the batch close.
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
