## 2026-08-20 — The program grind, in series (owner directive, second batch): per-WI record

The owner's directive for this batch: grind the open PROGRAM frontier in
series with opus/sonnet workers routed by BuildTier (strong→opus,
medium→sonnet), one large adversarial review (internal Opus + cross-family
Sol via codex, medium effort) at the end, consolidated and iterated in one
action. One entry per WI as its session ends; adjacent findings accumulate
at the bottom for the closing review. Program rows that cannot honestly
complete in one session land their largest coherent slice and record the
remainder — no false completes.

Deferred open items: OI-48, OI-49, OI-50, OI-51 — the running union of the
per-section declarations below, re-derived as each session closes (the WI-485
fragment-scope lesson applied from the start). OI-49 and OI-50 joined at the
WI-455 close; OI-51 at WI-473.

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

### WI-469 — Consumes rows that name the medium (sonnet worker) — CLOSED

**Full row, not a slice.** All 27 SR-owned file-as-endpoint `Consumes` rows
in `docs/requirements/interfaces.toml` re-authored, each landing in one of
the ruling's two shapes; spec moved to `docs/work/complete/`. No `status`,
`direction`, `owner`, or `contract` cell touched anywhere — only
`counterpart`, `interface_to_external` (where earned), and `notes`.

**The discriminator, made concrete rather than trusted from the 2026-08-17
counts.** A dedicated research pass re-measured genuine (content-reading, not
docstring/MAPPING-mention) readers for each of the 18 distinct counterpart
targets across the 27 rows. Two populations fell out cleanly:

- **10 LOW fan-out rows** — a closed, small, nameable reader set — now carry
  that set as `counterpart` (semicolon-joined module paths): IF-025, IF-026
  (each an independent AST walker of the source tree with fan-out=1, so the
  named module is the row's own — matching the worked coverage.json example's
  shape exactly), IF-029, IF-035, IF-037, IF-045 (fan-out=1, agent_route is
  the sole direct file-reader; agent_loop/plan_runner consume its API, a
  separate seam), IF-047, IF-070 (check_coverage parses the JSON; check.py
  only clears a stale copy — named per the WI's own worked example), IF-072.
  **IF-052 is the interesting one**: its counterpart was `docs/gate`, but
  `gen_trajectory` does not read that file directly — WI-280 moved the read
  into `traj_parse._gate_value`, which the facade calls. Re-pointed at the
  actual module boundary (`scripts/traj_parse`) rather than the file it
  wraps — a genuine staleness catch, not just a reframing.
- **16 PUBLISHED-CONTRACT / HIGH fan-out rows** — an open, growing consumer
  class where naming one reader would misstate the file's role — now carry
  `counterpart = "external:downstream adopter"` + `interface_to_external =
  "B-05"`, the IF-013…IF-018/IF-048 shape: IF-021, IF-022, IF-023, IF-024,
  IF-030, IF-033, IF-034, IF-038, IF-049, IF-051, IF-054, IF-057, IF-059,
  IF-068, IF-073, IF-079. Every one of these targets a spine or declared-
  policy registry (SR/SN/IF/OI, `docs/work`, `docs/stack.ini`,
  `docs/process.toml`, the whole `docs` tree) that ships blank as a template
  an adopter fills in — B-05's own `carries` text ("content of the package")
  covers the registry FORMAT, not just a script's CLI contract, which is why
  the tie applies even though these rows are `Consumes`, not `Provides`.
  **`IF-028` needed no change**: the concurrent WI-455 crossing-half slice had
  already re-pointed its counterpart from the retired `docs/architecture.md`
  to `scripts/gen_arch_map` — already module-shaped, already this WI's goal —
  before this session started.

Each touched row's `notes` cell records the pick and its verified evidence
(the measured reader set), e.g. IF-072's declared-absences readers verified
as three real content-readers (`check_doc_refs`, `trace`, `check_vocab`) plus
`tests/test_dogfood_sync.py` — the WI's own "five checkers" framing had
over-counted a comment-only mention (`check_need_form.py`) as a read.

**Self-correcting catch: the citation-frame rule applies to a row's own
argument, not just its history.** First-draft notes cited `(WI-469):
re-measured 2026-08-20` inline — `trace.py`'s provenance rule (no citation
frame in any living cell) flagged all 25 of them as advisory findings on the
first `--strict-integrity` run. Fixed by stripping the WI id/date stamp and
keeping the argument as prose that stands alone; the account (what was
measured, when, by what WI) lives here in the log instead. Zero citation-
frame findings on the touched rows after the fix.

**Unblocks the wi455 lane, precisely — one item cleanly, one only halfway.**
The lane's item 2 (the 49 held `Contract`-cell provenance citations,
`docs/provenance-allow`'s header) named WI-469 as its SOLE blocker and is now
UNBLOCKED — the interface lane can sweep those 46 `Contract names WI-###` +
3 `Contract cites decision` findings in one pass without re-touching rows
this WI just edited. The lane's item 1 (the `direction`/`this_project` shed
and the counterpart→consumers transform) has this WI's precondition
satisfied too, but stays blocked on a SEPARATE, still-unruled owner
question — which reading of `owner` governs a `Consumes` row, the-module-
that-holds-the-code or the provider — that the wi455 spec flags but does not
settle and that this WI deliberately left untouched (no `owner` cell was
edited anywhere in this pass). Recorded, not decided: that question has no
open-items row yet and is the owner's/wi455 lane's to file, not minted here.

**Adjacent (banked below):** the specref-clearing rule at close, and a
registry-editing footgun hit twice during the pass.

**Gates.**

- smoke: `1244 passed, 5 skipped in 142.92s (0:02:22)`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b94bf58c-dirty -->
- `check_docs.py --root . --stale`: `OK - 960 doc(s), 1325 intra-repo link(s), 0 broken (1 orphan warning(s))`
- `check_trajectory.py --root . --strict`: `clean (490 work item(s), 455 done (93%), 21 cancelled, graph acyclic)` — two R-A/R-F errors surfaced at close (a hand-authored `docs/status.md` bullet still naming the now-`done` id; the closed spec's `SpecRef` still set) and were fixed rather than waived: the status bullet reworded to drop the id token and state the unblock without it, `specref` cleared to `""`. R-F's archive half is scoped to `docs/specs/`; this row's spec-of-record lives at `docs/plans/2026-08-13-sitting-3-spine-verification.md` (a sitting doc, not a per-WI spec file), cited by no other open WI, so clearing the field was the whole fix — no archive move needed.
- full unfiltered suite, run in the foreground after the first attempt's
  background process was reaped by an idle turn boundary (re-run rather than
  trusted from a truncated log): `2685 passed, 14 skipped in 581.24s
  (0:09:41)`
  <!-- fig: cmd="python -m pytest -q -n auto" rev=55689752 -->

Deferred open items: none — this WI's own scope carried no open ruling
question; the owner-reading question for `Consumes` rows that its close
surfaced is wi455's to file (it is not yet a numbered `OI-###` row), and this
session deliberately did not decide it.

### WI-473 — the monotonic product-regression floor (opus worker) — SLICE landed, row stays QUEUED

**Slice 1 of a design+build row.** The mechanism is built, proven and documented;
the row does NOT close, because building it surfaced that the finding it
executes names the wrong binding constraint, and the constraint that IS binding
is an owner ruling. Spec Context now carries the four owed items with their
blockers named. Design record:
[../plans/2026-08-20-product-regression-floor.md](../plans/2026-08-20-product-regression-floor.md).

Deferred open items: OI-51 — which bar the three built-in product checks belong
at, now that DevStg-Impl is unreachable from the derived selector.

**THE FINDING THAT CHANGED THE ROW, measured rather than inherited.** C-01 says
one draft row "removes all product-code checks" from CI. Probed against the
tree, that is half right and the missing half matters twice over.

- What a draft actually does: `format`/`lint` degrade from GATING to **advisory**
  (WI-336's warn-only tier already re-runs them), and `tests+coverage` stops
  running altogether (`ADVISORY_EXCLUDE`). So the fix is *promote what already
  runs*, not *schedule what does not*.
- What is actually binding: **`DevStg-Impl` is unreachable from the derived
  selector at all.** OI-30 D2 ceilings `derive_gate.sr_bar` at `DevStg-Tests`
  ("unreachable from a status cell until a harness driver computes the release
  bar from test evidence"), and `ex-draft` is a MIN that includes `sr_bar`. The
  three built-in product steps are tagged `{DevStg-Impl}` only. **So they gate on
  no adopter's push or pull request, draft or no draft** — only the tag path
  forces `--gate all` (`ci/check.yml:89`). The draft mechanism C-01 describes is
  real; it is simply not what is stopping the three checks the finding is about.

That is a refutation of the finding's FRAMING, not of the finding — the silent
green is worse than reported. It is also why no built-in got re-tagged here: a
builder quietly moving three gate tags would be overturning an owner ruling's own
enumeration by side effect. `OI-51` carries it with a recommendation.

**What shipped.** `check.py` gains `product_floor()` (reads `ex-draft=` off the
`# basis:` line it already parses for `window_open`), `floor_plan()`,
`floor_notice()` and `resolve_plan()`. Product-LAYER steps are now selected at
`max(derived bar, ex-draft)`; maturity checks stay on the derived bar untouched.
Plus `PROCESS_OPTIONS.md`'s statement of the rule, a `RESYNC_PACK.md` §3 adopter
entry, and the corrected root workflow claim.

**The design decision, and why it is not a stored high-water mark.** The floor is
DERIVED — the same MIN arithmetic with the pending rows removed. Three reasons,
and the first is the strongest: **`PROCESS.md` §4 already pre-authorized exactly
this shape** — *"if a monotonic reading is wanted it is a second, derived
high-water number shown BESIDE the honest one, never instead"* — and
`derive_gate.compute` already ruled the axis against new state (excluding the
drafts recovers a mature spine's maturity *"WITHOUT history or a stored
high-water"*, WI-341). A derived value also cannot be gamed by deleting the file
that holds it, and `derive_gate --check` already guards the cache at every bar.

**Monotonicity stated precisely rather than claimed loosely**, because the
overclaim was available and this repo keeps catching it: the floor is monotonic
against **drafting**, the act C-01 names, and nothing wider. Demoting a ratified
row or approving one below the spine's min still lowers it — both REVIEWED
human-held spine acts, visible as a changed `ex-draft=` in a tracked derived
file. That visibility IS the sanction for a deliberate lowering; no new
re-stamp file and, deliberately, no dial that turns the floor off (a switch that
suspends real checks is a sanctioned check by another name).

**The review's other suggestion was rejected on a measurement.** "Infer the
floor from configured product commands" cannot ship default-on: `BUILTIN_PRODUCT`
gives EVERY scaffold configured commands from minute one, so it would fire on a
fresh repo with no source — `pytest` on an empty tree exits 5 and every new
adopter's first CI run reds. A configured command is intent, not a cleared bar.

**The fixture the review asked for, built on the PRODUCER.**
`test_one_drafted_row_does_not_lose_an_established_product_check` makes a mature
scaffold, runs the real `derive_gate`, adds ONE Drafted SR, re-derives, and
asserts the bar dropped (`DevStg-Tests` -> `DevStg-Reqs`) while `ex-draft` held
and the established product check stayed in the GATING plan. Hand-writing a
basis line would have asserted nothing about a field rename disarming the floor —
the D-9 precedent.

**Its control assertion was WRONG on the first run, and the correction is the
better claim.** The draft was expected to LOSE `traceability`; it does not — the
advisory tier demotes it to warn-only, and `--list` prints both tiers, so the
naive combined-text assertion failed. The two axes are therefore not "kept versus
dropped" but **kept AT THE BAR versus demoted to advisory**, and the test now
splits the output to say so. Read only as combined text, it would have passed a
floor that promoted everything.

**The dormancy is PINNED, not just noted.**
`test_the_floor_is_dormant_for_the_BUILT_IN_product_steps_and_says_so` asserts
both halves — the ceiling is still `BAR_TESTS`, the three built-ins are still
`{DevStg-Impl}`-only — and fails the day either moves. `derive_gate`'s own
ceiling comment says its removal must be *"an act rather than a drift"*; arming
this floor is now part of that act. Without this the next reader would take
C-01 as closed by a mechanism that cannot reach it.

**Two decompositions instead of a complexity re-stamp, both measured.** A nested
`steps_at` def took `main` 16 -> 17 (ruff's C901 counts a nested function into
its enclosing one). Rather than bump a pinned digit, `resolve_plan` lifts the
whole three-tier construction out of `main` — where the ORDER is the load-bearing
part (floor folded in BEFORE the advisory tier is built, or a promoted step runs
twice) — and `floor_notice` returns a newline-terminated string so its caller
needs no branch. Measured after: `main` is EXACTLY 16 again, so
`test_complexity_ratchet` is untouched.

**No spine row was minted or amended, deliberately.** `SR-006` is the requirement
home ("shall run the required steps of *the gate that must next be passed*") and
`LLR-060` its design row; both are **Approved**, and the floor makes `SR-006`'s
shall incomplete rather than wrong. Amending an Approved cell overrides
attestation — the sitting's act, on the `SR-158` precedent that left
`LLR-014`/`TC-014` re-points owed for this same reason. So the built behaviour is
ahead of its requirement and no TC claims it; both are on the owed list rather
than quietly absent. Minting a Drafted LLR under `SR-006` was considered and
declined: it would state what its Approved parent does not authorize, and
`SR-006` is phase 1 — the WI-448 lesson (a Drafted child drags its parent's whole
phase down) would have moved an unrelated gate to dodge an amendment.

**This repo cannot rehearse its own fix, and that is worth saying plainly.** Its
`ex-draft` reads `DevStg-Reqs` (nine Approved SRs undecomposed — the declared
orphans debt), so no floor engages here and nothing in this change is observable
from the meta-repo's own CI. The gap has never bitten here only because the
`test` matrix job runs the full pytest suite independently — which is exactly
what a downstream adopter does not have, and exactly why the root workflow's
enforcement comment (claiming all nine checks unconditionally) read as
enforcement the matrix was actually providing. Corrected.

**Line endings, and this time the standing rule EARNED its keep on a number
rather than on a diff.** Checked before trusting any byte count
(`git ls-files --eol`): the three `byte-budget-guard/SKILL.md` copies were
already CRLF in the working tree (the banked ~47-file residue). The scripted
re-stamps re-planted CRLF twice — `pathlib.write_text` on Windows, the exact trap
the WI-455 and WI-477 workers hit, now with a third witness — and all three were
normalized to LF before staging. The consequence is not cosmetic here: the same
file measures **4,963 bytes as CRLF and 4,873 as LF**, so 90 bytes of a 5,000
cap (1.8%) are line-ending residue. Banked below, because it means this file's
own stamped baselines may not all share a measurement basis.

**Byte deltas, one line per touched budgeted file:**
`project-trajectory/PROCESS_OPTIONS.md` 174,309 -> 175,330 (**+1,021**, watched,
FLAGGED and re-stamped in all three skill copies) — the derived-gate section
gains the floor's selection rule, what monotonicity is not being claimed, and
why no off-dial ships; the argument and the rejected alternatives stayed out, in
the design record. `byte-budget-guard/SKILL.md` 4,925 -> 4,963 CRLF / 4,873 LF
(capped at 5,000), all three copies.

**And the re-stamp itself blew the cap — caught by the FULL suite, which is the
argument for running it.** Writing a proportionate reason for a +1,021 flag took
that SKILL.md from 4,925 to 5,244 against its 5,000 cap. `test_bootstrap` is a
`SLOW_MODULES` member, so the smoke tier that had just gone green could not see
it; `pytest -q -n auto` failed on the first run and passed on the second. The
guard's own rule applied rather than the cap moved (pay for an addition by
tightening): the row was cut to a single clause, and the ARGUMENT for the growth
lives here in the log, which is where a stamp's reasoning belongs anyway.

**Gates.**

- smoke: `1249 passed, 5 skipped in 58.16s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=aa46953e-dirty -->
  Five new tests (1244 -> 1249), all in the commit bar by default; the tier's
  declared `max-tests = 1258` is not reached and NOT re-stamped. Under this box's
  60 s ceiling this once, which is one reading and not evidence the budget is
  comfortable — the same box logged 54.9 / 64.0 / 55.7 earlier today.
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1326 intra-repo link(s), 0 broken (1 orphan warning(s))`
  (960 -> 961: the design record, linked from the spec.)
- `trace.py --strict-integrity`: exit 0, integrity=0, interface-findings=0 —
  run before and after minting `OI-51`, and the watermark raised through the
  GENERATOR (`trace.py --bump-ids`, `OI 50 -> 51`) rather than by hand, since
  `docs/id-watermark` says do-not-hand-edit and its basis line would otherwise
  have gone stale.
- `check_trajectory.py --root . --strict`: exit 0,
  `clean (490 work item(s), 455 done (93%), 21 cancelled, graph acyclic)` — the
  pre-existing shared-specref WARNs only.
- **full unfiltered suite: `2690 passed, 14 skipped in 495.19s (0:08:15)`**
  <!-- fig: cmd="python -m pytest -q -n auto" rev=c23eb907-dirty -->
  2685 -> 2690 is exactly this session's five new tests; nothing else moved. The
  FIRST run of the same command on the same tree was `1 failed, 2689 passed, 14
  skipped in 572.29s` — the byte-cap failure above, FIXED rather than waived.
  **Read the scope honestly:** taken with the code, tests, registries and
  regenerated surfaces all in place, but before this fragment's own text was
  finished, so it does not cover the records commit — the WI-455 framing, and the
  same remedy: smoke re-run on the landed tree rather than argued away.
- The regenerated status block was diffed line by line before staging: **one
  added line (the `OI-51` bullet) and nothing else**; `PROJECT_STATE.html` moved
  only its as-of commit, and `docs/gate` did not move at all (no spine row was
  minted, so no bar, phase or count could).

### WI-483 — the successor decomposition program (opus worker) — SLICE landed, row goes ACTIVE

**Slice 1 of a program row.** Landed to
`docs/work/active/wi483-core-decomposition/`, not `complete/`: three of the
program's six shape items are untouched and the hard half of the cycle is
intact. Spec Context now carries the four owed items and the topology decision.

Deferred open items: none — this slice deliberately minted no owner question,
and was built so that the one it touches (`OI-48`) stays free to be ruled either
way. See the topology decision below; that freedom cost one extra spine row and
is the main design choice of the session.

**The census reproduces the review's exactly, and is now an instrument rather
than a paragraph.** 7 modules, 12 intra-cycle edges, **4 of them existing only
inside function bodies** — which is the whole reason the cycle was invisible.
`tests/test_import_layers.py` builds the AST import graph including
function-body imports, censuses the strongly connected components against a
baseline that may only tighten, and separately asserts the layer rule. It ships
with its own self-test, and that is the part worth defending: a walker that
quietly stopped descending into function bodies would make every cycle vanish
and turn the whole file green — the exact failure mode the review describes,
reproduced inside the instrument built to catch it. A known deferred edge
(`integrate -> handback`) is pinned present so that regression fails loudly.

**The edge broken, chosen on evidence rather than on the list order.**
`traj_panels` — a render leaf that writes nothing and must not be able to —
imported the 2,541-line merge coordinator for **exactly two constants**. That is
H-02's "the dashboard can drag mutation coordinators into read-only rendering",
literally, in one import line. So the lane-close terminal-outcome vocabulary
moved DOWN to `project-trajectory/scripts/kitlib/station.py`: `Outcome` (a `str`
enum — the review's named "terminal-state enum"), `OUTCOME_DIRS` (immutable),
`BAR_GREEN`, and `outcome_of`, which is the "exactly ONE declared status
directory, or none" DECISION lifted out of `integrate.branch_outcomes`. The
git-tree READ stayed in the coordinator, which is the policy/effect split the
program asks for, and the consequence is concrete rather than aesthetic: that
rule is now assertable without building a repo, a branch and a claim first.

**Cutting ONE edge dropped TWO modules: the SCC is 7 -> 5.** Not a coincidence
worth glossing — `traj_panels`' only route into the component was that constants
import, and `gen_trajectory`'s only route in was through `traj_panels`. The
remaining SCC is the lifecycle core proper (`dispatch`, `handback`, `intake`,
`integrate`, `lane`) and its three back edges are all deferred function-body
imports carrying real behaviour, not constants. That is the hard half and none
of it was attempted.

**THE TOPOLOGY DECISION, and it cost a spine row on purpose.** `kitlib/` was the
right home — `station` is a slot WI-448 NAMED and deliberately left uncreated,
handing it to this row by name. The live question was the design row. Appending
`station.py` to `LLR-181`'s `module` cell was one line and was REJECTED:
`LLR-181` carries the four-way usage tag `OI-48` is open about, and a four-way
tag SUPPRESSES the cross-component seam rule on every edge of the module. So
that spelling would have stopped policing the view-to-service seam **at the exact
moment it was fixed**, and would have spent an unruled owner question to tidy its
own diff. Instead `LLR-182` was minted Drafted with a SINGLE `CMP-008` tag — a
claim that is true here in a way it is not for the shared kernel, since every
module that ships the station flow is CMP-008 — and `IF-093` re-points
(`counterpart = scripts/kitlib/station`, `owner = LLR-182`), staying a policed
CMP-009 -> CMP-008 seam. Net effect for the owner: `OI-48` gets a worked data
point (per-theme ownership is available where a theme has an owner) and is
**not** pre-empted or widened.

**The parent SR was picked to move no gate, and the WI-448 lesson is why.**
`SR-144` ("every lane close is a terminal state with an immutable record") is the
requirement this vocabulary IS — the coordinator's own comment cites it — and it
is phase 5, where the drafts already sit. `SR-168` was the tempting parent
(`IF-093`'s own `req_refs`) and is phase 1: a Drafted child under it would have
dragged phase 1 down, exactly as `LLR-181` did before it was re-grounded.
Verified, not assumed — `docs/gate`'s regenerated basis line is byte-identical
on `per-phase`, `stage`, `computed` and `ex-draft`; only `LLR`, `TC` and
`drafted` moved.

**Verified by BOOTSTRAPPING A REAL SCAFFOLD**, per the standing lesson, because
MAPPING changed: the package arrived whole (five modules), `kitlib.station`
imported and answered from the scaffold's own `scripts/`, `integrate`'s
re-export was the SAME object there, `traj_panels` no longer holds `integrate`
in its namespace at all, and `check_trajectory` / `trace` / `derive_gate` /
`gen_trajectory` all ran clean. Read one result honestly: the scaffold's
dashboard is *vacuously* clean (a fresh scaffold has no work items), so the
station RENDER is proven by this repo's own regenerated dashboard and by
`test_traj_panels`, not by the scaffold.

**The mandated first act: the size ratchet has a live debt owner again.** It
directed active debt to `WI-280` for months after that item closed, and WI-280's
scope was the dashboard plus `bootstrap.main`, not the baseline. Re-pointed at
this row in the three NORMATIVE places — the module docstring, the census
comment, the assertion message. The **51 dated per-entry notes still reading
"re-stamp down with WI-280" were deliberately left**, and the file now says why:
each names the log entry that reviewed it, so it is a RECORD, and rewriting a
dated record to cite an item that did not exist on its date falsifies it. The
owner is stated once, at the top — which is this repo's own rule about not
restating a fact in fifty-one places.

**Ratchets re-stamped in both directions, with reasons.** `integrate.py`
2541 -> 2530 downward (the rule requires it; the last two of the eleven are a
`ruff format` unwrap of this session's own edit, caught by running the
formatter over the touched files rather than by the ratchet). `bootstrap.py` 2899 -> 2904 as a
reviewed bump: one MAPPING row plus four comment lines — a manifest growing,
which is what a manifest does, and the same axis complaint WI-448 banked, hit
again unchanged. The smoke MEMBERSHIP budget 1258 -> 1269 over a measured 1261,
the file's own ~0.6% convention.

**And the wall clock went DOWN while the tier grew, which is reported rather
than pocketed.** 1261 collected / **46.97 s**, against the previous stamp's
54.9 / 64.0 / 55.7 on this same box. Eleven pure in-process tests cannot make a
tier 8 s faster; that spread is load. The seconds budget was NOT touched **in
either direction** — a run that came in comfortably is no more a reason to
tighten it than the 64.0 s run was a reason to raise it. (The very next smoke
run, on the landed tree, read 62.69 s. Same tier, same box, 16 s apart: which is
the point.)

**One citation-frame cell cleaned as a by-product, and it is one row of another
lane's sweep.** `IF-093`'s contract carried `WI-389`; the cell was being
re-authored anyway, and the rule is that a living cell states the system, not its
history. That leaves the wi455 lane's held 49-citation sweep one row smaller
rather than colliding with it. No other held row was touched.

**Gates.** Line endings checked BEFORE trusting any count
(`git ls-files --eol`): every file this session edited with a script was written
in BYTE mode with the file's existing newline preserved, and `git diff --numstat`
confirms content-only diffs (`docs/stack.ini` 28/1, not a whole-file rewrite).
`tests/test_module_size_ratchet.py` and `docs/stack.ini` were already in the
banked ~47-file CRLF residue; the index stays LF.

- smoke: `1256 passed, 5 skipped in 62.69s (0:01:02)`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b9538b26-dirty -->
  Past the 60 s ceiling `docs/stack.ini` declares, consistent with this box's own
  2026-08-20 record. Not new evidence; the budget is not moved to fit it.
  Re-run on the LANDED tree, after the records edit: `1256 passed, 5 skipped in
  43.51s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b9538b26-dirty -->
  Three readings of the SAME tier on the SAME box this session — 46.97, 62.69,
  43.51 — a 19 s spread with the composition unchanged between the last two.
  That is the strongest one-box evidence this session produced, and it argues
  neither for raising the ceiling nor for tightening it; it argues that a
  wall-clock number from this box is a load measurement.
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1327 intra-repo link(s), 0 broken (1 orphan warning(s))`
- `trace.py --strict-integrity`: exit 0, integrity=0, interface-findings=0,
  component-findings=0; `LLR 163 -> 164`, `TC 159 -> 160`, `drafts 5 -> 7`,
  seams unchanged at 128. Watermark raised through the GENERATOR
  (`trace.py --bump-ids`, LLR 181 -> 182, TC 176 -> 177), never by hand.
- `check_trajectory.py --root . --strict`: exit 0. It went RED first, exactly as
  predicted — `1 arch-map module(s) are in no CMP-### component
  (scripts/kitlib/station)` — and was closed with a real spine row, never by
  touching `[checks] components_check`.
- The regenerated status block was diffed line by line before staging: **one
  changed line** (the spine counts) and nothing else. `docs/gate` moved only its
  counts and as-of commit; `per-phase`, `stage`, `computed` and `ex-draft` are
  byte-identical, so no gate, bar or phase moved.
- **full unfiltered suite, run to completion in the FOREGROUND**:
  `2697 passed, 14 skipped in 602.45s (0:10:02)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=b9538b26-dirty -->
  2690 -> 2697 is exactly this session's seven new tests and nothing else moved.
  **Two earlier attempts were DISCARDED rather than reported, and the second
  reason is the useful one.** The first was killed by a harness timeout at 98%
  with no failure on screen — a run that did not finish is not a green, however
  it looked. The second was abandoned deliberately: `ruff format` unwrapped one
  line of this session's own edit AFTER that run started, so its tree was two
  lines stale, and a suite result is only a claim about the tree it ran on. The
  figure above is the third run, on the tree that is committed.
  **Read its scope honestly**, the same caveat the WI-455 and WI-473 sections
  record: it was taken with the code, tests, registries, spine rows and
  regenerated surfaces all in place, but before this line itself was written, so
  it does not cover the records edit. Re-run rather than argued away — smoke on
  the landed tree below.

### WI-484 — concern/hat references on SR and LLR rows (opus worker) — SLICE landed, row goes ACTIVE

**Slice 1 of a six-phase program row.** Landed to
`docs/work/active/wi484-concern-refs-component-view/`, not `complete/`: phases 0
and 1 shipped whole, phase 2 is partial, and phases 3/4/5 are untouched. The
spec Context now carries the six owed items in the order they should be taken.

Deferred open items: none — phase 0's field-name ruling was DELEGATED to this
execution by the row's own spec ("one name, ruled here"), so ruling it is
executing the item, not deferring a new one. Phase 4's newly measured blocker is
recorded as a lane item rather than minted: it is a mechanism gap in `hats.py`,
not a question needing the owner's judgement, and the roster edit it gates on is
owner text either way.

**Phase 0, RULED: `hat_refs` / column `Hat-Refs`, values are roster NAMES.** Not
a coin-flip between the owner's `hats_ref` and the brief's `concern_refs` — both
were declined on precedent already written into the file the cell lands in.
`hats_ref` is the one form no sibling takes (`sn_refs`, `boundary_refs`,
`sr_refs`, `req_refs` are all singular-noun + `_refs`), so it keeps the owner's
VOCABULARY — hats, not concerns — in the house idiom. `concern_refs` fell to
`boundary_refs`' own minting rule three lines above it in `SPINE_COLUMN`: a refs
column is named for the tier it resolves INTO, which is why that cell is not
`bif_refs`. A `concern` cell resolving against `[hat.NAME]` rows is exactly the
vocabulary hop that rule refuses. The `C-SEC-2`-style clause numbering living in
eight rationale cells is NOT promoted to a second id space — it resolves nowhere
and stays prose.

**Phase 1, the cell and its three rules.** `hat_refs` is OPTIONAL on the SR and
LLR tiers; `trace.load_hat_names` reads the roster's table keys;
`trace.hat_findings` splits severity the way `sr_boundary_findings` does —
resolution is a `--strict` finding under its own `hat` class, coverage is one
advisory line — and `trace.effective_hats` derives a design row's set as its own
refs unioned with its SR parents' — and it is WIRED, not reserved: the coverage
arm counts EFFECTIVE sets, which is the difference between 220/237 and **178/238**
on this repo's own spine (42 design rows inherit attribution from a parent). A
derivation defined and called by nothing is the exact defect this module's own
size-baseline records against `unanchored_findings`. `LLR-183`/`TC-178` minted Drafted under
**`SR-161`**, which is not a convenience: SR-161 is *"Decompositions carry a
perspective record"*, the row `LLR-168` says the record half of SN-036 was
DELIBERATELY not built for. It was an ORPHAN (no LLR, no TC) until this slice — trace's orphan count drops
**17 → 15** as a side effect, and that is the honest test of the choice: if the
cell had needed a new SR, the perspective record would have had two homes.
The row states what it does NOT discharge in the `LLR-172` debt-stating pattern:
SR-161 wants not-applicable distinguished from considered-with-no-finding, and
this cell expresses neither — both are facts about a DECOMPOSITION, this cell is
a fact about a ROW, and applicability is separately derivable from the roster's
own predicates, so storing it would store a derived fact and let it go stale.

**The anti-staleness decision, which is the whole design.** An LLR's cell holds
only what its own decomposition raised. Copying parents down would turn
re-ruling ONE requirement into a sweep over every child it has — the
hand-maintenance the generated view exists to escape, moved one tier down and
multiplied by the fan-out. `test_a_parent_re_ruling_moves_the_child_with_no_child_cell_edited`
pins it on the same child dict.

**The second reader of `hats.toml` is deliberate, and the alternative was
worse.** `trace.py` is CMP-006, `hats.py` is CMP-008, and the declared crossing
between them (`IF-133`) already runs CMP-008 → CMP-006. Importing `hats` here to
save a `tomllib.load` would mint a component-level CYCLE — against the direction
the live WI-483 lane is pulling. So trace reads the roster's KEYS only;
`hats.py` stays the sole validator of roster CONTENT, the two answer different
questions, and `test_the_roster_path_matches_the_hats_module` pins the paths
equal (a TEST may import both where the shipped code may not).

**The backfill, and the measurement that says a tool must not finish it.** 17 SR
rows migrated — exactly the population stating its own derivation in the ruled
`Hat-derived (hat.X)` label form, extracted from that parenthetical only. A
naive `hat.` regex over `rationale` matches **19**, and both extras are wrong in
opposite directions: `SR-015` names `hat.PERFORMANCE` in order to REFUSE it as a
basis, and `SR-040` carries an attribution left struck under OI-38. Cross-check
that the migration is faithful: it leaves exactly **5** hats attributed to no
row, matching OI-32's own independent census ("eleven distinct hats appear
across the 18", 16 − 11 = 5). Coverage moved 237/237 → 220/237 by cells, and to 178/238 once the effective-set
reading landed. The prose was
NOT deleted — `Rationale` is a ratified cell on Approved rows, so the
de-duplication is owner-adjacent and recorded as owed.

**No re-attest window opened, and that is a classification, not luck.**
`spine_cell_class`'s residual reads an unclassified column as RATIFIED, so
shipping the cell without classifying it would have armed a window on all 17
Approved rows and tripped the `last_approved` drift comparison. `Hat-Refs` joins
`SPINE_TRACED_CELLS` at both tiers — which is what makes the owner's own
sequencing note ("NOT anticipated to be an attested cell, so it can be tacked on
AFTER the sitting") true rather than hoped. Deliberately NOT added to
`intake.ROUTED_TRACED_CELLS`: a hat re-point restates which lens a row is
attributable to and moves no obligation.

**The first-run-adopter defect, caught by regenerating a golden.** The first
build emitted the coverage line and "16 hats attributed to NO row" on every run
— and a freshly bootstrapped scaffold ships all 16 hats with zero `Hat-Refs`, so
every new adopter would have been greeted by sixteen declared perspectives
called "unrecorded or ceremony" about a layer they had not opted into. That is
this kit's own FIRST-RUN-ADOPTER failure class, and it is how an advisory pipe
stops being read. Both advisories are now gated on the cell being IN USE; the
regenerated goldens show the scaffold report gaining two quiet metric rows and
one factual section, and nothing else.

**VERIFIED BY BOOTSTRAPPING A REAL SCAFFOLD**, per the standing lesson, not by
the golden fixtures alone. A fresh scaffold receives `hat_refs` with its guidance
in both `-000` rows and the 16-hat roster, and `trace --strict` there is SILENT —
no coverage line, no unattributed-hats line, which is the first-run-adopter
property the gate exists for. Adding one row with `hat_refs = ["SECURITY"]`
reports no coverage line (the row is covered) and correctly names the other 15
hats as unattributed; typo it to `SEKURITY` and the run gives
`FINDING (hat): SR SR-001 Hat-Refs references unknown hat SEKURITY`, exit 1. The
rule is demonstrated able to bite in an adopter's tree, not only in a fixture.

**The vocabulary retirement the WI-489 worker banked, discharged.** `PROCESS.md`
and the `spine-authoring` skill no longer teach "a labelled derived SR"; both
now name the cell, and the skill says why a prose label is not a record (it
resolves against nothing, so nothing can tell a retired hat from a live one).
Shipped as a `RESYNC_PACK.md` entry `[since 046843eb]` carrying the four things
an adopter needs: nothing existing breaks, coverage never gates, the roster is
opt-out, and DO NOT let a tool do the backfill — with this repo's own 19-vs-17
measurement as the argument.

**Two ratchets re-stamped, one REFUSED and fixed instead.** `trace.py`
4761 → 4961 (measured POST-`ruff format`, which reflowed one call in this
session's own edit after the first stamp — the WI-483 trap, re-encountered) and `check_trajectory.py` 4018 → 4042 (declaration only), reasons in
the baseline entries. The complexity ratchet fired on `render_report` 17 → 18
and was NOT bumped: the section moved into a `_hat_report_section` helper
following `_frame_report_section`, which is the idiom that file already agreed
on for a conditionally-rendered section — the C901 census is unchanged by this
WI. `max-tests` 1269 → 1291 for 22 new tests, 21 of them pure.

**The full suite earned its place in the bar, concretely.** The first full run
came back `2 failed` on `tests/test_trace_rules.py`, a module the commit tier
does not carry: `_findings_stub` is a HAND-MAINTAINED mirror of the attributes
`exit_code` reads, and it drifted silently the moment `exit_code` gained the
`hat_dangling` arm. Smoke was green across that defect twice. Fixed in the stub
with the rule recorded in place.

Byte deltas, one line per touched file:
`project-trajectory/PROCESS.md` 84,080 → 84,383 (**+303**, FLAGGED — watched
file). The growth is one sentence-pair replacing one clause, and it is
load-bearing rather than expansion: the retired clause told an author to write a
prose label, so re-pointing it at the cell is the minimum, and the two rules a
reader cannot derive from the column name — that a BLANK means *not recorded*
rather than *none applied*, and that an LLR's effective set is own + parents'
rather than a copy — are exactly the two an adopter gets wrong by default. Both
are stated once here and nowhere else in the core. Tightened once before landing
(a first draft measured +354). No other capped or watched file was touched:
`AGENTS.template.md` 9,948 and `CLAUDE.md` 7,147 unchanged.

Gate figures, this tree:
- `trace.py --root . --strict`: **zero hat findings** on the live spine, and the
  run's exit 1 is the pre-existing `trajectory` orphan red status.md already
  names (SRs with no LLR) — unchanged by this WI except that it SHRANK, 17 → 15.
- `check_trajectory.py --strict`: **clean** (490 work items, 455 done, 21
  cancelled, graph acyclic); warnings only, all pre-existing shared-specref
  pairs.
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1327 intra-repo link(s), 0
  broken`.
- **full unfiltered suite, run to completion in the FOREGROUND**:
  `2719 passed, 14 skipped in 625.68s (0:10:25)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=046843eb-dirty -->
  2697 -> 2719 is exactly this session's 22 new tests and nothing else moved.
  **An earlier run was DISCARDED rather than reported, and it is the reason the
  full suite is the bar for a slice.** That run came back `2 failed` on
  `tests/test_trace_rules.py` — a module the commit tier does not carry — where
  `_findings_stub` is a hand-maintained mirror of the attributes `exit_code`
  reads and drifted the moment `exit_code` gained the `hat_dangling` arm. Smoke
  was green across that defect twice. A second run was abandoned deliberately:
  the effective-set wiring landed after it started, so its tree was stale, and a
  suite result is only a claim about the tree it ran on. The figure above is the
  third, on the tree being committed. **Read its scope honestly:** it was taken
  with the code, tests, registries, spine rows and regenerated surfaces all in
  place, but before this fragment and the `registry-machinery-reference.md` row
  were written — docs-only edits, and the one test that READS that file
  (`tests/test_status_vocabulary_contract.py`, 8 passed) was re-run on the final
  tree.
- smoke, final reading on the same tree: `1278 passed, 5 skipped in 68.11s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=046843eb-dirty -->
  (earlier readings this session, before the last two edits: 69.04 s and
  64.90 s).
  **EVERY READING IS OVER THE DECLARED 60 s CEILING AND THE BUDGET IS NOT MOVED.** This
  box's prior readings on a smaller tier were 54.9 / 64.0 / 55.7 s and then
  46.97 s at the WI-483 stamp, so it already straddled the ceiling before this
  WI added ~3.5 s of mostly-pure tests. Three readings here, all 64-69 s. Reported as a machine condition and as
  more evidence for the already-banked seconds-budget question (the WI-477 and
  WI-475 workers each recorded it); a run brushing a budget is not a reason to
  raise the budget.
- The regenerated surfaces were diffed before staging: `docs/status.md`'s
  generated block moved **one line** (the spine counts), and `docs/gate` moved
  only its counts, `drafted` and as-of commit — `computed`, `ex-draft`,
  `per-phase`, `stage` byte-identical, so no gate, bar or phase moved.

### WI-390 — concurrency-v2 program close (sonnet worker) — SLICE landed, row stays ACTIVE

**Slice 1 of the program's closing row.** Landed to
`docs/work/active/wi390-concurrency-v2-program-close/`, not `complete/`: of
the four surfaces `docs/concurrency-v2.md` §A9.1 names as owed to this row,
three closed and one is a window question for the owner. Spec Context carries
the full account.

Deferred open items: **the LLR-056/TC-056 spine amendment** (below) — a
recommendation is written into the row's Context, execution is not, because
both cells are `Approved` and amending an Approved cell overrides
attestation, this repo's own precedent for the sitting's act, not a
builder's.

**(2) Connectivity — the drift this program itself caused, closed.**
`scripts/lane` and `scripts/handback` were arch-map modules naming no
`IF-###` row at all — both modules' own docstrings said so, explicitly
naming this row as the owner ("part of the drift docs/concurrency-v2.md
§A9.1 hands to the program-close row rather than to any single builder").
Minted `IF-136` (dispatch consumes lane) and `IF-137` (dispatch consumes
handback), owners `LLR-150`/`LLR-144` (the rows that already describe these
two modules), declared via a `Contracts:` line in `dispatch.py`. `IF-055`
and `IF-080` (`this_project = scripts/integrate`) and `IF-081`
(`this_project = scripts/trunk_step`) sat in the registry with no script
declaring them — the design doc's own named list; declared in `integrate.py`
and `trunk_step.py` respectively. `drive.py` itself no longer exists (already
renamed away by an earlier build in this same program) and was not live-flagged
at all — the design doc's list was stale on that one entry, recorded rather
than acted on.

**A checker false-quiet found along the way, banked rather than fixed.**
`check_trajectory` never actually warned about `IF-080` even before this
session, and the reason is a real defect in `gen_arch_map.module_contracts`:
its per-line harvester matches any line containing the substring
`"Contracts"`, and `handback.py`'s own docstring line 63 — *"No `Contracts:`
line, deliberately: the integrator seam this extends is IF-080, whose row
already sits..."* — contains both the trigger word and the id on the SAME
line, so a sentence explicitly saying there is no declaration was read as
one. A false quiet, not a false red, so nothing this session depended on it
being wrong (`IF-080` was fixed for real regardless); flagged for whoever
next touches the Contracts grammar.

**(3) Process prose — the one live contradiction, found by reading rather
than by grep.** A literal-term grep of `PROCESS_OPTIONS.md` and
`AGENTS.template.md` for the retired vocabulary (`SCHED_`, `single-WI`,
`packing`, `EXIT_NEEDS_HUMAN`, `parked-branch`, `merge-conflict`/`conflict
arm`) came back clean — already scrubbed by Phase 5. But
`PROCESS_OPTIONS.md`'s "serial merge queue" paragraph still read *"a
`--no-ff` merge onto a candidate worktree"*, which directly contradicts
`integrate.py`'s own docstring: there is no candidate worktree any more
(§A2 deleted it — trunk-is-ancestor makes the merge trivially clean and the
composed tree byte-identical to the branch tip, so the bar runs ONCE, on the
branch, at refresh, not again on a merge-time candidate). Corrected onto the
live model; byte delta `PROCESS_OPTIONS.md` 175,330 -> 175,531 (**+201**,
watched, FLAGGED, re-stamped in all three tracked skill copies).

**(4) Stamps — verified mechanically, nothing owed.** `check_stubs.py` scans
a `src/` directory this repo does not have (it is a downstream-adopter tool)
and runs clean by construction: `check_stubs: OK - no source directory at
src`. The size ratchet (`tests/test_module_size_ratchet.py`) carries no
`drive.py` baseline entry to retire — the module was never tracked there.
The duplication-census stamp this row's own title still names is already
confirmed gone (D-7/WI-426, recorded in this file's own earlier section); no
substitute `test_rule_sync.py` pin is owed, since this slice left no
duplicated POLICY behind.

**(1) The spine amendment — re-measured, and it splits into a closed half and
an open window question.** Two facts, neither trusted from this file's own
stale citations:

- `SR-093`/`SR-124`/`SR-131`/`SR-132`/`SR-050` are **gone** from
  `docs/requirements/system-requirements.toml` (zero grep hits) — deleted
  outright, not marked `Superseded`, by the unrelated WI-451 SR re-tier
  campaign's tombstone class (2026-08-14b); `SR-133`'s clause folded into
  `SR-006` verbatim. This file's own 2026-08-18b note already calls this "a
  re-scope of a spine-class row… not a builder's call — raise it at the
  sitting rather than inventing a mapping." Raised here, not re-mapped: the
  six original amendment targets are closed by a different program's ruling,
  and nothing further is owed from this row on them.
- `LLR-051`/`LLR-056`/`TC-051`/`TC-056` (the WI-414 re-scope's four surviving
  targets) are **not** `Modified`, as the 2026-08-13w note assumed —
  re-measured today, all four are **`Approved`**. `LLR-056.detail` and
  `TC-056.method`/`.expected` still describe the retired two-intersecting-hoops
  render ("6 for the 5-stage intake loop + 5 for the 4-stage decision loop =
  11", the shared `LLM_Agent` hub), while `TC-056.evidence` already cites only
  the live station-cycle tests and the shipped render
  (`traj_panels._station_panel`) draws one station cycle — confirmed by
  reading the render and `test_process_tab_renders_the_station_cycle`, not
  assumed. **Recommendation, written into the row's Context rather than
  executed:** re-word `LLR-056.detail` off the two-loop framing onto the
  seven-stage station-cycle description its own Evidence already tests
  (Dispatcher tick -> Claim -> Lane build -> Station refresh -> Merge slot ->
  Trunk advance -> Intake mint), and re-word `TC-056.method`/`.expected` to
  match — `.evidence` needs no change. **Not executed**, because both cells
  are `Approved`: amending an Approved cell overrides attestation, and this
  repo's own precedent today (`SR-006`/`LLR-014`/`TC-014`, the WI-473
  session) treats that as the sitting's act — which is also why this row
  carries `safety_class = spine` in the first place, so its amendments land
  in one owner-reviewed window rather than by a session's unilateral edit.

**A second advisory found and accepted as expected, not fixed.**
`check_trajectory` now reports `scripts/lane` and `scripts/handback`
"declares no Consumes seam" — the provide-only-leaf advisory, same class
already carried unmarked by `scripts/kitlib/station` since WI-483. Both
modules' own docstrings describe a deliberate no-back-channel,
no-state-file design, so this is the honest shape, not a defect; left
unmarked for the same reason the precedent was.

**Gates.** Line endings checked before trusting any count
(`git ls-files --eol | grep 'w/crlf'`): none of this session's touched files
appear in the pre-existing ~47-file residue list.

- `trace.py --root . --bump-ids`: `IF 135 -> 137` (the two new rows), written
  through the generator, never by hand.
- `trace.py --strict-integrity`: exit 0 both before and after fixing two
  transient findings the new rows themselves produced on the first pass — a
  citation-frame hit (`WI-381`/`WI-387`/`WI-390` named inside live `Contract`/
  `Notes` cells) and a 545-char `IF-137` contract past the 500 ceiling; both
  fixed by dropping the id/date frame and tightening the prose, never by
  editing the rule that caught them.
- `check_trajectory.py --root . --strict`: exit 0. Diffed the WARN list
  before/after: the five targeted connectivity WARNs (`lane`, `handback`,
  `IF-055`, `IF-080`, `IF-081`) are gone; no new ones appeared beyond the
  expected `lane`/`handback` "no Consumes seam" advisories addressed above.
- smoke: first run caught a real ratchet fire (`integrate.py` baseline 2530 ->
  2542, the new `Contracts:` paragraph) — re-stamped deliberately with the
  reason in `tests/test_module_size_ratchet.py`, never reverted. Clean re-run:
  `1278 passed, 5 skipped in 75.73s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b9538b26-dirty -->
  Past the declared 60 s ceiling, consistent with this box's own 2026-08-20
  record; not new evidence, budget not moved.
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1327 intra-repo
  link(s), 0 broken (1 orphan warning(s))`.
- The regenerated surfaces were diffed line by line before staging
  (`trunk_step.py --regen`): `docs/status.md`'s generated block moved only
  the seam count (128 -> 130) and `docs/gate` moved only its as-of commit —
  `basis`, `computed`'s DevStg value, `per-phase`, `stage` byte-identical, so
  no gate, bar or phase moved. `PROJECT_STATE.html` moved the as-of sha and
  the active-work-item count/listing (4 -> 5, `WI-390` now shown active) and
  nothing else.
- **The byte-budget-guard skill hit its own trap, live, a second witness for
  the WI-473 finding.** The first FOREGROUND full-suite attempt was reaped
  when the turn ended before it finished (frozen at 65%, no output growth on
  re-check) — re-run per protocol rather than trusted from a truncated log,
  and the re-run caught a real defect the first attempt would have too: the
  `PROCESS_OPTIONS.md` re-stamp row, written to satisfy this session's own
  guard, pushed all three tracked `byte-budget-guard/SKILL.md` copies to
  5,072 bytes against their 5,000 cap. `test_always_loaded_docs_stay_within_
  byte_caps` (outside the smoke tier) caught it; smoke had gone green across
  it. Fixed by tightening the new row's prose (99 bytes shorter), never by
  moving the cap — all three copies now 4,973 bytes.
- **full unfiltered suite, run to completion in the FOREGROUND after the
  reaped attempt was discarded and re-run**: `2719 passed, 14 skipped in
  506.64s (0:08:26)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=c2c72757-dirty -->
  2697 -> 2719 (WI-483/484's own additions landed on trunk since the last
  recorded full-suite total this fragment shows); nothing from this session
  added or removed a test. Final smoke re-check on the landed tree:
  `1278 passed, 5 skipped in 56.78s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=c2c72757-dirty -->
  and `check_trajectory.py --root . --strict`: exit 0, clean (490 work items,
  455 done, 21 cancelled, graph acyclic).

### WI-467 — the blind re-derivation validation row (sonnet worker) — CLOSED

**Not a re-run — a housekeeping close.** Before touching anything, `git log
--all` for the spec's own path turned up two commits already claiming this
WI's title: `cda29c42` ("83% convergence, zero contradictions") and `dea8364e`
(the hat-aware extension), both dated 2026-08-16. `git merge-base
--is-ancestor` against `HEAD` confirmed both are already in THIS branch's own
history. The exercise the spec asks for — two blind, axis-diverse capability
breakdowns, a mechanical alignment map, orphans as findings never silent
merges — had already run in full, weeks before this grind session, and its
findings had already been ruled on: `docs/work/complete/WI-468-hat-exposed-obligation-intake.md`
and `docs/work/complete/WI-470-open-items-a3-coverage.md` are both terminal,
closing the loop the alignment map opened. The one thing that had NOT
happened was closing the WI-467 row itself — it sat in `queued/` describing
work that was done, diffed, and acted on.

**Headline result, read off the artifacts rather than trusted from commit
prose.** Two independent blind breakdowns —
[`plans/2026-08-16-blind-derivation-a.md`](../plans/2026-08-16-blind-derivation-a.md)
(actor/crossing axis, 77 rows) and
[`-b.md`](../plans/2026-08-16-blind-derivation-b.md) (lifecycle/value-flow
axis, 73 rows), each reading only the README vision + `stakeholder-needs.toml`
+ `external.toml`, each covering 27/27 SNs — plus a hat-aware third variant,
[`-c-hats.md`](../plans/2026-08-16-blind-derivation-c-hats.md) (80 rows, 13
hats), owner-approved as an extension. The alignment pass,
[`plans/2026-08-16-derivation-alignment.md`](../plans/2026-08-16-derivation-alignment.md):
**71 obligation clusters, 59 convergent (83%), 0 flat contradictions** (5
divergences of placement/strength), 7 tensions hit by both teams
independently; **63 legacy SRs — 47 MATCHED, 16 ORPHANED-IN-LEGACY** (8
implementation-born/derived-requirement class, 7 needs-understatement, 1
accretion), **11 ORPHANED-IN-FRESH** (7 real/partial holes, 4 over-read or
already covered). §4's hat-aware delta: 14 of the 16 legacy orphans gain a
naming lens (derived-requirement, DO-178C class, now reviewable); `SR-053`
alone stays underivable from every input tried (needs-only, frame-only, and
hat-aware all three failed to produce it) — the sharpest single finding of
the whole exercise, since it converts "maybe accretion" into "no current
input demands this, by three independent tries."

**The notable divergence worth restating for anyone reading only this
fragment.** D1 in the alignment map: team A read the frame as FORBIDDING a
delivered-surface obligation for SN-023 (the dashboard's rendered view sits
outside the boundary, only the generator capability is claimable at B-05);
team B stated the surface obligation flatly, no caveat. Not resolved by
either team — flagged as the sharpest divergence in the whole comparison, and
still unruled as far as this closing session can tell (not something WI-468
or WI-470 addressed).

**Why this session did not spawn a fresh blind pair.** The task brief asked
for two independently blind agents on divergent axes; running that again
against a spine the earlier pass already diffed, with the sitting already
having ruled on the findings, is not a second N-version instance — it is
implementation-mirroring against the exercise's OWN prior output, the exact
failure class the blind-derivation guard exists to prevent. The honest act
available was verifying the existing result held up under real downstream
use (it did — twice, via WI-468 and WI-470), and closing the row that never
got closed.

**R-F caught a real omission on the first commit, fixed on the second.**
`check_trajectory --strict` reds immediately after the close commit: a
terminal WI must clear `SpecRef` (the row still pointed at
`docs/plans/2026-08-16-tiering-research-memo.md`). Same disposition as the
WI-469 close precedent — the archive-to-`docs/archive/specs/` half of R-F is
scoped to `docs/specs/`, this row's spec-of-record is a plan doc, and a grep
confirmed no other open WI cites it, so clearing the field was the whole fix.

Deferred open items: none — this close mints no new question; D1's
unresolved divergence is restated above for visibility but was already
banked, not newly surfaced, and disposing it is the sitting's call, not a
new OI.

**Gates.**

- smoke (first commit): `1278 passed, 5 skipped in 116.37s` (contended;
  earlier same-tier readings this session ran 65–75s)
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=484e9f28-dirty -->
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1331 intra-repo link(s), 0 broken (1 orphan warning(s))`
- full unfiltered suite, on the landed tree (both commits in place):
  `2719 passed, 14 skipped in 496.17s (0:08:16)`
  <!-- fig: cmd="python -m pytest -q -n auto" rev=0adf0868 -->
  2719 is byte-identical to the WI-484 close's own total earlier today —
  nothing this session added or removed a test, which is the expected
  reading for a spec-close-only slice.
- `check_trajectory.py --root . --strict`, on the landed tree: `clean (490
  work item(s), 456 done (93%), 21 cancelled, graph acyclic)` — 455 → 456 is
  exactly this row.
- Line endings checked before trusting any count
  (`git ls-files --eol | grep 'w/crlf'`): none of this session's touched
  files (the spec, `docs/status.md`, `docs/gate`, `PROJECT_STATE.html`)
  appear in the pre-existing residue list.

### WI-487 — the back-link campaign (sonnet worker, 7 parallel review batches) — CLOSED complete

Executed the campaign half of OI-42's ruling. Reverse coverage rose from
1/165 (0.6%) at WI-486's close to **83/165 (50.3%)**, clearing the recorded
50% target — `python project-trajectory/scripts/gen_arch_map.py
--backlink-coverage --src project-trajectory/scripts --root .`
<!-- fig: cmd="python project-trajectory/scripts/gen_arch_map.py --backlink-coverage --src project-trajectory/scripts --root ." rev=5d0dc4f6 -->
Seven parallel batches (by module group) each read an LLR row's `detail`
text and the actual code before tagging — 79 tags placed across 17 modules,
14 candidates SKIPPED on real registry-staleness findings rather than
forced (banked below). One tag that WAS placed did not survive this
worker's own verification pass and was removed: **LLR-005**, whose registry
`code_symbol` (`module_findings`) names a function-local inside
`trace.analyze`, never a real module-scope binding — no placement honestly
carried the claim. A replacement, independently code-reviewed, closed the
gap to hold the target: **LLR-038** on `check_doc_refs.findings_for`
(confirmed against the function body — it runs exactly the path/`sym:`
scan the row describes).

**Verification method, since this worker did not originate the seven
batches' own numbers first-hand.** An automated cross-check (AST-parsed
every `Implements:` line's enclosing top-level symbol against each row's
registry `code_symbol`) flagged 9 of 83 candidates; 8 were the checker's
own false positives (comments correctly placed 1-4 lines above a module
constant or inside a class docstring, which a naive span heuristic
misattributes to a neighboring method/assignment) verified by direct
reading; the 9th was LLR-005, above.

**`docs/process.toml` `[checks] backlink_coverage_min` rises 0 → 50** (this
repo's own instance value; the shipped `process.toml.template` stays 0 for
a fresh adopter — VALUE divergence, not STRUCTURE). `test_rule_sync.py`'s
`OWNER_DIALS` allowlist gained the entry with its reason, caught by the
full suite (see gate totals) after the smoke tier passed clean — that test
is not in the smoke tier's module set. `dispatch.py:310`'s dangling SR-141
citation (merged into SR-148 2026-08-14) is repointed, closing the row's
"rides along" item. The module-size ratchet's 8 legitimate growers
(agent_common.py, agent_loop.py, bootstrap.py, check.py,
check_trajectory.py, derive_gate.py, integrate.py, trace.py — all
prose/docstring lines, zero executable change) are re-stamped in
`tests/test_module_size_ratchet.py` with reasons.

**The decay answer, owed at close per the ruling.** RE-CONSIDERED option
(c) (the OFT-style revisioned marker) and recommend NOT building it now —
it mints a revision field on every spine row plus a marker-grammar
migration, a large human-held decision, to guard a convention this same
session just hand-wrote. The campaign's own code-review pass found sharper
evidence than OI-42's original WI-425 citation: three LLR rows'
`code_symbol` cells were ALREADY stale before any tag was written
(`LLR-147` names `sn_gate`, live function is `sn_bar`; `LLR-077` names
`spec_ref_findings`, live function is `specref_findings`; `LLR-005`, above)
— pre-existing registry drift the mandatory read-the-code step surfaced,
not decay from this campaign's own tags. Recommended instead: a cheaper
report-only companion check in `gen_arch_map` confirming each declared
`Implements:` line's adjacent symbol still parses as a real definition
(existence, not meaning; no spine field) — sized as its own small WI if the
owner wants it. Full recommendation on the WI's own spec
(`docs/work/complete/WI-487-implements-backlink-campaign.md`, "Decay
answer, recorded at close").

**Gate totals, all foreground/unfiltered, this session:**
- Commit-bar smoke (final, post-fix): `1278 passed, 5 skipped in 62.74s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=5d0dc4f6 -->
- `check_docs.py --stale`: `OK - 961 doc(s), 1335 intra-repo link(s), 0
  broken (1 orphan warning(s))`.
- Full unfiltered suite (first pass, foreground, caught the real
  `test_rule_sync.py` OWNER_DIALS gap): `1 failed, 2718 passed, 14 skipped
  in 542.76s`. After the fix, re-run: `2719 passed, 14 skipped in 472.24s`
  <!-- fig: cmd="python -m pytest -q -n auto" rev=5d0dc4f6 -->
  — the +1 over WI-484's 2718/2719-ish baseline is this WI's own new
  OWNER_DIALS assertion coverage, not a new test file.
- `check_trajectory.py --strict`: exits 0, `clean (490 work item(s), 457
  done (93%), 21 cancelled, graph acyclic)` — warn-only pre-existing noise
  (open-WI title lengths, shared-specref pairs, IF connectivity/TC-coverage
  gaps) untouched by this row.

**Deviations from the orchestrator's relayed batch totals.** The
orchestrator's mid-session relay of the seven batches' self-reported
tag/skip counts (A1 11/2 … A7 9/4, summing to 78 tagged) did not match the
tree: 83 distinct LLR ids carried a tag before this worker's own fix pass,
and specific ids the relay described as "skipped" (LLR-005) were in fact
present in the working tree, tagged — the relay's provenance was each
batch's own final-message summary, not a re-read of the diff. This worker
verified against the actual files rather than the relayed arithmetic before
acting, per instructions.

**Banked findings** (registry staleness the code-review pass surfaced;
Approved rows, not touched — spine tiers are human-held):
- LLR-143's `detail` is contradicted by the code/a test (batch A5 finding;
  not independently re-verified by this worker beyond confirming no tag
  was forced).
- LLR-089's registered `code_symbol` never existed in `schedule.py` (batch
  A5 finding).
- LLR-050, LLR-142, and a third `derive_gate.py`/`check.py` row describe
  D-9-retired behavior (predicates deleted at the D-9 migration steps
  recorded in `tests/test_module_size_ratchet.py`'s own baseline
  comments) — batch A6/A7 findings.
- LLR-057, LLR-104, LLR-108's `module` cells are stale after a file split
  (batch A6/A7 findings; same class as the WI-472/WI-477 `LLR-172`
  banked item already on this fragment).
- LLR-147's `code_symbol` names `sn_gate`; the live function is `sn_bar`
  (this worker's own verification pass, above — tag placed on `sn_bar`
  since the code genuinely matches, but the registry cell itself is stale
  and worth a future WI-482-class repair).
- LLR-077's `code_symbol` names `spec_ref_findings`; the live function is
  `specref_findings` (same class, same disposition: tagged the real
  function, registry spelling is what drifted).

Deferred open items: none — the decay recommendation (don't build (c) now;
consider a lighter existence-check WI later) is recorded on WI-487's own
spec rather than a new OI, since OI-42 already covers this ground and
stays `ruled`; the banked registry-staleness findings above are candidates
for a future small WI-482-class repair, not an owner decision.

### WI-488 — the interface contract-test coverage promotion (sonnet worker) — CLOSED complete

**Full row, not a slice.** Executes OI-43's ruling (a) in full: the
promotion, the migration allowlist, and the declared burn-down expectation,
sequenced behind WI-469 (closed) and the wi455 lane's landed crossing-half.
Spec moved to `docs/work/complete/`.

Deferred open items: none — see below for the one item recorded as an owed
recommendation on the WI's own spec rather than minted as an OI (the shape
this session's own WI-473 precedent uses for the same class of question).

**The promotion.** `check_trajectory.py` gains `if_tc_coverage_findings` — an
IF seam cited by no TC and NOT on the migration allowlist is WARN plain,
ERROR under `--strict`, wired through `main()` exactly like
`component_findings`/`spec_interface_findings` (so `check.py`'s existing
gate-conditional `--strict` — passed from `DevStg-Tests` on, its own
unmodified logic — carries the promotion for free; `check.py` itself needed
no change). `interface_findings`' own "cited by no TC" line is UNCHANGED,
stays warn-first forever, and still reports the TOTAL (allowlisted seams
included), so the whole debt stays visible once the actionable subset goes
quiet. A companion `if_tc_allow_hygiene_findings` reports — never blocks, not
even under `--strict` — a listed seam that has since gained a TC, or an id
that no longer resolves, so the burn-down is visible rather than silently
absorbed.

**A scope-widening bug caught before landing, not after.** The first draft
of the two new functions checked only `[checks] interfaces_check`, not
`interface_findings`' OWN ≤1-module arch-map vacuity gate. Measured against a
single-module fixture: the old warn stayed silent (as designed) while the new
promotable function fired anyway — a real behavior divergence, since the
ruling promotes an EXISTING warn's severity, not its scope. A `files`-mode or
single-module adopter who never saw the warn would otherwise start seeing the
error. Both new functions now share the same vacuity check
(`test_seam_tc_promotion_shares_the_one_module_vacuity` pins it); caught by
building a scaffold fixture rather than only testing on this repo's own
multi-module tree, where the bug was invisible.

**The allowlist, re-measured rather than trusted from the ruling's own
citation.** `docs/if-tc-coverage-allow`, seeded with **120** ids (was 115 at
the 2026-08-19 ruling) — the tree moved between the ruling and this row's
execution: WI-455 minted IF-134/135, WI-390 minted IF-136/137 and declared
IF-055/080/081 (existed but declared no script), WI-483 re-pointed IF-093 —
none of the five new/re-declared seams carry a TC. 130 live IF rows today
(was 125), 120 uncited. The ruling's own text anticipated exactly this ("the
seed problem" is not one — its INTENT, seed at the measured uncovered
population, governs over the stale number, and its text explicitly says so).
Not a kit-shipped template — like `docs/provenance-allow`, the file is
absent-tolerant and each adopting repo seeds its own once the promotion
starts to bite (`read_if_tc_allow` returns `{}` for a missing file, so a
fresh scaffold is unaffected until it needs one).

**Verified by BOOTSTRAPPING A REAL SCAFFOLD**, per the standing lesson, not
just on this repo: a fresh two-module scaffold with one uncited seam, run
through `check.py` itself (not `check_trajectory.py` called directly) —
`--stage-cleared DevStg-Reqs --run-step trajectory` runs with NO `--strict`
(WARN only, PASS, exit 0); `--stage-cleared DevStg-Tests --run-step
trajectory` runs WITH `--strict` (the seam ERRORs, FAIL, exit 1); seeding the
scaffold's own `docs/if-tc-coverage-allow` with that one id turns the same
DevStg-Tests run green again. The ruling's own framing — "this repo is at
DevStg-Reqs today, so the promotion bites nobody here until the bar rises" —
demonstrated end to end, not assumed. Reproduced on this repo's own tree too:
`check_trajectory.py --root . --strict` is clean with the seeded allowlist;
removing one entry reproduces the ERROR.

**Deliberately deferred, recorded rather than executed: no spine row claims
the new mechanism.** `LLR-042` (`SR-159`) — the design row
`interface_findings` cites — is `Approved`, and its `detail` says the
connectivity layer emits its findings "without changing exit status": still
TRUE of `interface_findings` (untouched), and would be FALSE if cited from
`if_tc_coverage_findings`. Amending an Approved cell overrides attestation
(the SR-006/LLR-060 precedent, WI-473, same session, same day). Minting a
fresh Drafted LLR under `SR-159` was considered and declined for the same
reason WI-448 hit first: `SR-159` is phase 1 (currently `DevStg-Tests`), and
a Drafted child would drag that phase's derived bar down as a side effect of
unrelated work. Recorded as an owed recommendation on the WI's own spec
(Deliverable) rather than executed or minted as a new OI — the built
behaviour is ahead of its requirement, honestly unclaimed rather than falsely
claimed. No `Implements:` line names `LLR-042` from either new function.

**Docs.** `PROCESS_OPTIONS.md`'s "Intra-repo interfaces & the architecture
graph" section splits the now-inaccurate "all warn-first" claim into the two
halves that stay true (endpoint/docstring warns) and the one that promotes,
and states the allowlist + burn-down. `RESYNC_PACK.md` §3 gains an entry (the
WI-473 product-floor entry's shape: what changes, what an adopter may notice
on their first post-re-sync DevStg-Tests run, and that seeding their own
allowlist is theirs to do). `PROCESS.md`'s and `README.md`'s "every interface
is backed by a contract/fixture test" claim is UNCHANGED, per the spec — the
promotion is what makes it true, not a rewording.

**Two ratchets re-stamped, both reviewed bumps.** `check_trajectory.py`
module size 4,096 → 4,295 (+199: the two new functions, the allowlist
parser, and the doc comments recording the deliberately-unclaimed
`Implements:` decision); `check_trajectory.py:main` complexity 22 → 24 (+2:
one more WARN-plain/ERROR-under-`--strict` loop beside `comp_errors`' — the
same shape `component_findings` already costs main() two branches for — not
decomposed, since the file already carries two near-identical bare promotion
loops rather than one shared helper, and a third follows the established
idiom instead of inventing a fourth shape for one caller).

**Line endings.** `tests/test_complexity_ratchet.py` was already
whole-file CRLF in the working tree (pre-existing residue, the banked
~47-file finding — confirmed by the uniform 341/341 CRLF count, not a
partial edit of mine) and was normalized to LF before staging, since this
session touched it. No other file this session edited appears in
`git ls-files --eol | grep 'w/crlf'` beyond the pre-existing residue list
(down to 42 files afterward).

**Byte deltas, one line per touched budgeted file:**
`project-trajectory/PROCESS_OPTIONS.md` 175,531 → 176,601 (**+1,070**,
watched, FLAGGED and re-stamped in all three tracked skill copies) — the
seam-TC coverage paragraph split off the promotable half, the allowlist and
its burn-down expectation; the argument and the rejected framings stayed out,
recorded here instead. `byte-budget-guard/SKILL.md`'s own re-stamp row first
blew its 5,000-byte cap (5,028, the WI-473/WI-390 trap, a third witness) and
was tightened to 4,982 in the same commit — caught by
`test_always_loaded_docs_stay_within_byte_caps`, never by moving the cap.

**Gates.**

- smoke (final, landed tree): `1278 passed, 5 skipped in 65.57s (0:01:05)`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d9a0a61f-dirty -->
  Unchanged count from the WI-484/WI-487 baseline — `test_trajectory_arch` is
  a `SLOW_MODULES` member (subprocess-heavy, `run_traj`), so this WI's four
  new tests land in the full tier, not smoke.
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1335 intra-repo
  link(s), 0 broken (1 orphan warning(s))` — unchanged from the WI-487
  baseline (no doc added or removed).
- `check_trajectory.py --root . --strict`: exit 0, `clean (490 work item(s),
  458 done (93%), 21 cancelled, graph acyclic)` — 457 → 458 is exactly this
  row; no new WARN or ERROR class beyond the pre-existing shared-specref
  pairs.
- **full unfiltered suite, run to completion in the FOREGROUND**:
  `2723 passed, 14 skipped in 507.30s (0:08:27)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=d9a0a61f-dirty -->
  2719 → 2723 is exactly this session's four new tests. **Two earlier full
  runs on the pre-fix tree were real reds, fixed rather than waived**: the
  first caught the two ratchets above; a second, taken before the scope-
  widening bug fix, caught three UNRELATED cross-component/overlap-advisory
  tests failing under `--strict` for the first time
  (`test_cross_cmp_import_with_declared_seam_is_silent`,
  `test_cross_cmp_seam_covers_either_direction`,
  `test_overlap_advisory_yields_to_a_declared_seam`) — each fixture declares
  a real IF seam with no TC, which the NEW promotion correctly flagged; fixed
  by adding a TC citation to each fixture (`_write_tc_citing`), the honest
  fix, since the promotion working as designed is not itself a defect.
- The regenerated surfaces were diffed line by line before staging:
  `docs/status.md`'s generated block moved **one line** (WI-488 dropped from
  the Ready frontier) and nothing else; `docs/gate` did not move at all (no
  spine row was minted, so `derive_gate.py --check` reports up to date
  without a re-derive); `PROJECT_STATE.html` moved only the as-of sha/date
  and the done-count (457 → 458) plus the Next-work listing.

### WI-490 — retire the mechanical-ratification arm (sonnet worker) — CLOSED complete

**Full row, not a slice — and a record-only one.** Executes OI-45's ruling
(b) RETIRE THE ARM. The code deletion itself (the write loops and
`copy_live`) had already landed at the 2026-08-20 batch review's iterate
pass (MINOR-12); what this WI owed was the RECORD catching up to the
ruling — every touched docstring/comment stopped presenting (a)/(b) as an
open question and started stating the ruled shape, with OI-45 cited as the
record. Spec moved to `docs/work/complete/`.

Deferred open items: none — OI-45 is fully executed by this row; no new
question surfaced.

**What moved, all docstring/comment-only, zero executable lines.**
`intake.flip_verified`'s "what the `flip` arm still has to move" paragraph
now states mechanical ratification is retired permanently, not pending;
`intake._apply_flips`'s docstring drops the "the ruling could restore a
writer here" hedge and states OI-45 as the record, keeping the two
D-9-step-7 candidate shapes as history rather than live options; the
trailing comment after its refusal loop updated the same way.
`intake.adjudication_action` gained a paragraph noting that even where it
returns `"flip"`, `_apply_flips` writes nothing — the name only routes
which brief the caller owes. `intake._cmd_adjudicate` and the `adjudicate`
subcommand's `--help` text now say RECOMMEND, never enact, per the WI's own
instruction that a subcommand whose only act is refusal must say so where
its help text speaks. `intake._cmd_snapshot` gained the paragraph the WI
asked for verbatim in substance: ratification authority was deliberately
NOT mechanized (OI-45 is the record), and this refresh is the ONE
mechanical toucher of the approval record. `trace.is_founded`'s docstring
splits D-9 consequence 2 into its two halves — whether a tool ever WRITES
the cell stays open, whether an AGENT-authored `Founded` is itself an error
is now answered (sanctioned, under the declared human-ratification level)
— citing OI-45 instead of claiming the whole question open.

**One live reference doc carried the same stale claim, found by grep rather
than assumed absent.** `docs/registry-machinery-reference.md`'s `Founded`
table row repeated "whether an authored `Founded` is itself an error is
still open (D-9 consequence 2)" — the exact defect class this WI exists to
close, just outside the three named touchpoints. Corrected to match the
code, since a reference doc is a live surface an adopter reads, not an
archived record.

**The scope-note rule, checked rather than assumed satisfied.** Every
touched surface states "ratification was deliberately not MECHANIZED,"
never "no agent may ever move a Status cell" — an LLM session or
adjudicator remains expected to flip a row's Status to `Approved`/`Founded`
for spine content past the declared human-ratification level
(`agent_common.human_holds` says which). A repo-wide grep for `100% human`,
`only a human` and `never mechanically` found no other live occurrence of
the overstatement class: the hits outside `tests/`/archived plans/reviews
are unrelated judgments (spec-correctness, a PlanMode/SafetyClass
conflict), and the archived/dated ones (RESYNC_PACK.md's D-9 migration
entry, `docs/reviews/`, `docs/plans/`) are records of a past state, left
alone on the same principle the log itself is append-only under.

**No test pinned the retired framing, and none needed changing.** Searched
for a source-grep test on the deleted write-and-copy block or on the
docstring wording before editing: none exists (`tests/test_intake.py`'s
`flip_verified`/`_apply_flips` coverage is behavioral only — refusal
messages, idempotence, the missing-status raise). The full suite below is
the confirmation the MINOR-12 deletion did not regrow and nothing else
moved.

**Ratchets re-stamped deliberately, both directions accounted for.**
`trace.py` 4989 → 4993 (+4, `is_founded`'s split docstring) and `intake.py`
1864 → 1901 (+37, the five touched functions plus the CLI help text) —
docstring-only, no executable line moved, reasons in
`tests/test_module_size_ratchet.py`'s own entries per the standing rule
(re-stamp deliberately, never revert a real edit to dodge the ratchet).

**Gates.** Line endings checked before trusting any count
(`git ls-files --eol | grep 'w/crlf'`): none of this session's touched
files appear among the (now 51-file, up from the banked ~47) pre-existing
CRLF residue list.

- smoke: `1278 passed, 5 skipped in 65.13s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=366a8131-dirty -->
  First run caught the predicted ratchet fire (`intake.py`/`trace.py` past
  baseline); re-stamped deliberately per above, clean re-run shown.
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1335 intra-repo
  link(s), 0 broken (1 orphan warning(s))` — unchanged from the WI-488
  baseline (no doc added or removed).
- `check_trajectory.py --root . --strict`: first run caught a real R-F
  (terminal WI still carrying its `SpecRef`) — fixed by clearing the field
  rather than waived, same disposition as the WI-469/WI-467 close precedent
  (the archive-to-`docs/archive/specs/` half of R-F is scoped to
  `docs/specs/`; this row's spec-of-record is `docs/requirements/
  open-items.toml#OI-45`, cited by no other open WI). Clean re-run: `clean
  (490 work item(s), 459 done (94%), 21 cancelled, graph acyclic)` —
  458 → 459 is exactly this row; no new WARN class.
- The regenerated surfaces were diffed line by line before staging:
  `docs/status.md`'s generated block moved **one line** (WI-490 dropped
  from the Ready frontier) and nothing else; `derive_gate.py --check`
  reported `docs/gate` already up to date (no spine row was minted, so
  nothing to re-derive); `PROJECT_STATE.html` moved only the as-of
  sha/date and the done-count (458 → 459).
- **full unfiltered suite, run to completion in the FOREGROUND**: `2723
  passed, 14 skipped in 477.10s (0:07:57)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=366a8131-dirty -->
  Byte-identical to the WI-488 close's own total — nothing this session
  added or removed a test, the expected reading for a docstring/comment-only
  slice. (An earlier run auto-backgrounded past the shell tool's 120s
  default and was reaped at the turn boundary before it could finish; this
  is the re-run, taken as one foreground call with an explicit 600s
  timeout.)

### WI-491 — the subagent-gate parse asymmetry + fail-open log (sonnet worker) — CLOSED complete

**Executes OI-46's ruling, (1a)+(2a) both, one row.** `subagent_gate.py`'s
`read_process_policy` gains an `UNPARSEABLE` sentinel (a plain `object()`)
returned when `docs/process.toml` is PRESENT but does not parse/read;
`decide()` resolves it to `ask` (fail-closed) via its own branch, and
`main()` treats it as terminal rather than a `None`, so a broken
`process.toml` no longer falls through to the legacy `docs/subagent-gate`
file or a quiet `allow`. Genuine absence is untouched — still `allow`, the
ruled opt-in posture. Aligned against the concrete, tested precedent —
`tests/test_rule_sync.py`'s D-7 pin of `check_trajectory.py`/`gen_okf.py`,
which have always read the same state as ON — rather than OI-46's own looser
prose naming "the hook's grep reader, the loop's tomllib reader" (banked
below: those two actually read different `[checks]` keys and reach a
stricter posture by a different mechanism — a hard preflight refusal via
`config_conflicts`, not a per-call `ask`).

`agent_loop.py` gains `_subagent_gate_log_count(root)` and `print_run_banner`
now prints `subagent-gate: N decision(s) recorded in out/subagent-gate.log …`
whenever the count is non-zero, silent otherwise. **Deviation from a first
pass:** the helper first imported `subagent_gate` for its `LOG_NAME`
constant; `check_trajectory.py --strict` caught that as a real ERROR (a new
`CMP-008 -> CMP-007` cross-component seam with no declared `IF-###` row, not
merely advisory). Declaring a seam for one shared string would have widened
this row past OI-46's ruled scope, so the fix reads a pinned literal instead
— `tests/test_agent_loop.py::test_subagent_gate_log_filename_matches_the_writer`
guards the two sides from drifting apart silently.

**Verified against a real scaffold** (`bootstrap.py --dest <tmp> --agents
claude`), not just the unit suite: a syntactically-broken `docs/process.toml`
made the real `PreToolUse` hook print `permissionDecision: "ask"` (exit 0);
adding a legacy `docs/subagent-gate` file set to `deny` alongside it left the
decision `ask` (corruption does not fall through); removing both files
returned `allow`. `out/subagent-gate.log` accumulated the three decisions,
and a direct call to `agent_loop._subagent_gate_log_count` against that real
log file read back `3`.

RESYNC entry added (`project-trajectory/RESYNC_PACK.md` §4, `[since
f3cb9801]`): a present-but-broken `docs/process.toml` now defers subagent
spawns instead of silently allowing them when `[checks] subagent_gate` is
opted in.

Deferred open items: none — OI-46 is fully executed by this row; no new open
item surfaced.

**Ratchet.** `agent_loop.py` module-size baseline re-stamped 3202 → 3231
(+29), reason inline in `tests/test_module_size_ratchet.py`.

**Gates.** Code commit `f3cb9801`. Line endings checked
(`git ls-files --eol | grep 'w/crlf'`): none of this session's files are new
CRLF entries.

- smoke (final): `1278 passed, 5 skipped in 57.60s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=f3cb9801-dirty -->
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1335 intra-repo
  link(s), 0 broken (1 orphan warning(s))` — unchanged from the WI-490
  baseline.
- `check_trajectory.py --root . --strict`: first run caught the real
  cross-component ERROR described above (fixed, not waived); clean re-run:
  `clean (490 work item(s), 460 done (94%), 21 cancelled, graph acyclic)` —
  459 → 460 is exactly this row's own close.
- **full unfiltered suite, run to completion in the FOREGROUND**: `2726
  passed, 14 skipped in 500.96s (0:08:20)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=f3cb9801-dirty -->
  2723 (the WI-490 close's own total) → 2726 is exactly this session's three
  net-new tests (two banner tests + the filename drift guard); the four
  renamed M-13/D-7 tests each replaced an existing one.

### Adjacent findings accumulating for the closing review

_(per-WI sections are inserted ABOVE this section, in close order; banked
findings accumulate below as list items)_

- (WI-491 worker) **OI-46's ruling prose names the wrong twin pair for
  subagent_gate.py, though its operative recommendation is unaffected.** The
  ruling text says the two readers this module should align with are "the
  hook's grep reader" and "the loop's tomllib reader." Measured: the git
  hooks' grep reader (`GREPPABLE_KEYS` in `agent_common.py`) matches only
  `privacy_check`/`privacy_review`, never `subagent_gate`; and "the loop's
  tomllib reader" (`agent_common.declared_policy`/`process_config`) reaches
  its stricter posture by a DIFFERENT mechanism — `config_conflicts` refuses
  the whole coordinator launch at preflight on a malformed `process.toml`,
  it does not resolve one dial to a stricter per-call value the way
  `decide()` now does. The concrete, TESTED twin pair — cited by
  `subagent_gate.py`'s own pre-existing docstring and pinned by
  `tests/test_rule_sync.py`'s D-7 test — is `check_trajectory.py` and
  `gen_okf.py`, which really do read the same `[checks]`-section parse
  failure as a terminal, non-falling-through ON. WI-491 aligned against that
  pair; the ruling's own prose reads as a paraphrase that drifted from the
  code it was describing. No action needed — the executed behavior matches
  the ruling's operative recommendation ("present-but-unparseable = ask,
  absence = allow") either way — flagged only so a future reader of OI-46
  does not go looking for a grep-based subagent_gate twin that does not
  exist.
- (WI-491 worker) **`agent-hooks/README.md`'s subagent-gate paragraph still
  says "deny-by-default fan-out."** Pre-existing staleness, not introduced by
  this row: `subagent_gate.py`'s own module docstring has stated since the
  2026-08-19 review (M-13) that this description is exactly backwards (the
  gate is fail-OPEN by design, `off`/absent/unparseable-formerly/error all
  allow), and OI-46/WI-491 only narrows the unparseable arm — the module
  stays fail-open by design everywhere else. `agent-hooks/README.md` line 30
  was not in this WI's scope (a different file, no ruling named it) and is
  banked here as a one-line fix for a future doc sweep: replace
  "deny-by-default fan-out" with language matching the module's own header
  ("OPT-IN, FAIL-OPEN … deny only once a human writes `deny`").
- (WI-484 worker — **settles two banked items, both by measurement**) The
  `LLR-172` / `budget_findings` anchor pair banked by the WI-477 and WI-472
  workers is **already resolved and needs no WI**. `LLR-172` names
  `check_trajectory.py` today and `component_findings` IS a module-level def at
  `check_trajectory.py:1318`; `check_doc_refs --strict` reports ZERO hits for
  `LLR-172`, `LLR-015`, `component_findings` or `budget_findings`; and no LLR
  row names `budget_findings` at all. The WI-482 close ("the three stale
  anchors") appears to have taken it. The banked note said WI-484's execution
  would settle which module was the intended landing — it settles it by
  measuring that the question closed already.
- (WI-484 worker) The `spine-authoring` skill's FRONTMATTER `description` still
  reads "a labelled derived requirement" — the one live occurrence of the
  retired vocabulary left in the tree. Deliberately not fixed here: the
  description is copied into `project-trajectory/skills/INDEX.csv`, a
  trunk-owned generated artifact `[generated]` says a work branch must never
  commit. It is a one-line trunk step.
- (WI-484 worker — a real checker hole, same class as the WI-474 worker's
  `Contracts:` finding) `tests/test_trace_rules.py::_findings_stub` is a
  hand-maintained list mirroring what `trace.exit_code` reads, with NOTHING
  pinning the two together. Adding an `exit_code` arm without it raises
  `AttributeError` — found only by the full suite, since the module is outside
  the commit tier. A one-line assertion comparing the stub's attribute set to
  the names `exit_code` reads would close it; worth the same defensive treatment
  the WI-465 worker asked for on `.gitattributes`.
- (WI-484 worker) `docs/registry-machinery-reference.md`'s traced/ratified table
  listed LLR `SR-Refs` as RATIFIED while `SPINE_TRACED_CELLS` has had it TRACED
  since WI-388. Corrected in this slice rather than banked, because leaving a
  known-false row beside the true `Hat-Refs` row I was adding is worse than the
  scope cost — but it is evidence the table is a second hand-maintained mirror
  of a constant, the same shape as the `_findings_stub` finding above.
- (WI-484 worker) Phase 4 of this program is blocked on a MECHANISM, not a
  ruling: `hats.py` refuses any unknown roster key and has no optional-key
  concept, so a `knowledge` field cannot be added to `hats.toml` without minting
  one — and it would otherwise become mandatory on all 16 live rows and all 16
  shipped-template rows. `hats.toml` is also declared owner text. Whoever takes
  phase 4 should expect to build `OPTIONAL_KEYS` first.

- (WI-483 worker — the one the closing review should weigh) **the shared
  kernel's four-way component tag is no longer just an open question, it is a
  DESIGN PRESSURE pulling toward the wrong answer.** `OI-48` records that
  `LLR-181`'s four-way tag suppresses the cross-component seam rule on every
  edge of `kitlib`. What this slice found is the second-order effect: for any
  future module that belongs in the shared package, the CHEAPEST correct-looking
  move — append it to `LLR-181`'s `module` cell, one line, no new spine row — is
  the move that silently disarms a check. Here it would have un-policed the
  exact view-to-service seam the slice existed to fix, and nothing would have
  reported it, because a suppressed rule produces no finding by construction.
  This slice paid a whole extra design row to avoid it, and a worker with less
  time or less context would not. The class: **an unruled tag whose lazy
  spelling is also its silencing spelling gets more expensive every week it
  stays unruled**, and the cost is invisible in exactly the runs that would
  otherwise surface it. Ruling `OI-48` is worth more than its blast radius
  suggests.
- (WI-483 worker) **the interface derivability check agrees on MODULE and is
  blind to RELEVANCE, so a seam row can name a design row that has nothing to do
  with what crosses and still pass.** `IF-093` — the dashboard's read of the
  terminal-outcome vocabulary — carried `owner = LLR-154`, "the merge slot's
  post-merge intake arm". The predicate compares the owner LLR's `module`
  against the row's owner-side endpoint; `LLR-154`'s module is `integrate.py`
  and the counterpart was `scripts/integrate`, so they agreed and the row read
  clean. But `LLR-154` says nothing about `OUTCOME_DIRS`; it is simply *a* design
  row that happens to live in the same 2,541-line file. That is the mechanism by
  which a monolith launders provenance: while N design rows share one module
  cell, any of them satisfies the check for any seam into that file, and the
  check cannot tell which. It is also self-limiting in a useful direction —
  decomposition FIXES it, because a smaller module has fewer rows to be confused
  with — but until then the derivability report's "every LLR-owned row agrees
  with its owner's Module" reads stronger than it is. Cheap partial mechanization
  exists: compare the row's named symbols against the owner's `code_symbol`
  where both are present, warn-only.
- (WI-483 worker — a second witness for a finding already banked above)
  **`spec_move.py`'s destination handling is asymmetric in the unsafe
  direction**, and it costs a round trip every time. It REFUSES a destination
  directory that EXISTS ("REFUSED - the destination ... already exists"), and it
  CREATES A FILE for a trailing-slash destination that does not. So the two
  obvious ways to move a spec into a new lane both fail, in opposite ways, and
  only one of them fails loudly: `mkdir` first then pass the directory is
  refused, and passing the directory without `mkdir` silently produces a file
  where a lane was meant, which is how WI-448 briefly vanished from the registry
  earlier today. The working spelling is the full destination FILE path, which
  neither the refusal message nor the help text points at. One sentence in the
  refusal ("name the destination file, or let this tool create the lane
  directory") would close it.
- (WI-483 worker, small) **`tests/test_bootstrap.py` hand-maintains a spot-check
  copy of the `kitlib` MAPPING rows**, so adding one module to the package means
  editing the manifest in two places. The comment there already concedes the
  duplication ("these rows are the spot-check that keeps the expectation
  readable") and `test_the_common_package_ships_complete` is the real guard, so
  the list buys readability at the cost of a second edit site that a future
  slice will forget. Deriving the spot-check from `bootstrap.MAPPING` would keep
  the readability and drop the drift surface.
- (WI-473 worker — the biggest one, and it is NOT scoped to WI-473) **an owner
  ruling's "this relaxes nothing" enumeration missed the harness's own step
  SELECTION, and nothing in the repo would have reported it.** OI-30 D2
  ceilinged `sr_bar` at DevStg-Tests and reasoned it through explicitly:
  "every consumer of DevStg-Impl was enumerated before the ruling — harness
  strictness selection, the rung-6/7 stage record, the release checklist — and
  every one is monotone-stricter in the bar. Withholding the top bar therefore
  withholds ESCALATION and relaxes no check that was running." The counterexample
  is the first item in its own list: withholding DevStg-Impl from the SELECTOR
  does not decline to escalate, it withdraws the three product steps that were
  only ever scheduled there. Invisible from this repo (nothing here had reached
  DevStg-Impl, and the CI matrix runs the whole suite regardless), live for any
  adopter with a decomposed spine. The class, which is what makes it worth
  banking: **a "no consumer is affected" enumeration is a claim about a
  dependency graph that nothing checks**, and this one was written by the same
  session that made the change. A cheap mechanization exists for exactly this
  case — the step table already declares its bars, so "which steps become
  unreachable if bar X is never derived?" is a query, not an audit.
- (WI-473 worker) **ruff's C901 counts a NESTED FUNCTION into its enclosing
  one, so extracting a helper INTO a function raises the number that extraction
  is supposed to lower.** Hit live: adding a three-line `def steps_at(g)` inside
  `main()` took it 16 -> 17 and reddened the complexity ratchet, while moving
  the same code to module level took it back to exactly 16. The trap is that the
  instinctive fix for "this expression is repeated" is a local def, and here that
  is the one shape the ratchet punishes. Worth a sentence wherever the ratchet's
  rule is stated ("decompose rather than re-stamp" — decompose OUTWARD, not
  inward), because the next author will reach for the same local def.
- (WI-473 worker) **the byte-budget guard's own numbers are LINE-ENDING
  DEPENDENT, and its baselines may not share a measurement basis.** Measured
  this session on one file: `byte-budget-guard/SKILL.md` is **4,963 bytes with
  CRLF and 4,873 with LF** — 90 bytes, 1.8% of its 5,000 cap, decided entirely by
  a worktree artifact the repo's own standing rule says to check before trusting
  any count. `test_always_loaded_docs_stay_within_byte_caps` reads the file from
  DISK, so on a CRLF worktree it grades a number that is not the committed one;
  the same edit can pass on one machine and fail on another. Both directions are
  live: a stamp recorded from a CRLF tree overstates its baseline, and the cap
  test can red on residue rather than on content. Cheap fix either way — measure
  the INDEX form (`git show :<path> | wc -c`) or normalize before measuring — and
  the skill already tells its reader to check `git ls-files --eol` first, so this
  is its own rule not applied to itself.
- (WI-473 worker) **`--list` prints the gating and advisory tiers into one
  stream, and a test that greps the combined text cannot tell "at the bar" from
  "warn-only".** This session's first fixture asserted a process step was LOST to
  a draft; it is not lost, it is demoted, and the naive assertion failed for the
  right reason only by luck — the reverse mistake (asserting a step IS present)
  would have passed while the step was merely advisory, which is precisely the
  false green the advisory tier's own marker exists to prevent. The output does
  mark advisory rows in the SUMMARY (`[advisory — not gating]`); `--list`'s
  section header is the only separator, so any programmatic reader must split on
  it. A machine-readable `--list` (or a marker per line, as the summary has)
  would remove a whole class of test that passes for the wrong reason.
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
- (WI-469 worker) **the citation-frame rule reaches a row's own live prose,
  not just quoted history — hit twice in one edit pass.** Writing "(WI-469):
  re-measured 2026-08-20" into 25 `notes` cells as honest per-row evidence
  tripped `trace.py`'s provenance advisory on every one of them: the rule
  bans a citation frame in ANY living cell, and a cell's own supporting
  argument for ITS OWN CURRENT SESSION's edit is not exempt just because it
  is fresh rather than inherited. The fix is mechanical once seen (drop the
  id/date, keep the argument, put the account in the log) but the trap is
  easy to walk into precisely when doing the RIGHT thing (recording evidence
  per-row, as this WI's own spec asked for) — a worked example of "state the
  reason, not its history" in `AGENTS.template.md`/the spine-authoring skill
  would have caught this before the first `--strict-integrity` run rather
  than after.
- (WI-469 worker) **a bulk registry edit that appends a new cell after
  `status = "Drafted"` without checking for an EXISTING later cell of the
  same key produces unparseable TOML, and `tomllib` reports only the byte
  offset of the LAST duplicate, not which edit caused it.** Three of 26
  per-row edits in this session added a `notes` line right after `status`
  without noticing the row already carried its own `notes` (or, in one case,
  a second edit's `notes` collided with the first's) two-plus lines further
  down — `Cannot overwrite a value` fired at parse time with no row id in the
  message, and each of the three took a separate read-diagnose-fix round
  trip. A cheap guard for the NEXT bulk registry edit: grep the target rows
  for the key being added BEFORE editing, not after the parser complains —
  `grep -c "^notes = "` inside each `[interface.IF-###]`..next-header span
  would have caught all three up front.
