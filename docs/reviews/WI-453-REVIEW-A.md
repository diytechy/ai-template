# WI-453 — REVIEW-A (2026-08-14)

**Reviewer:** OPENAI-TERRA (`gpt-5.6-terra`, medium effort) via the `codex`
CLI — cross-family, fresh context each round, independent of the lane builder.
Charter: [code-review-adversarial](../rubrics/code-review-adversarial.md).
Given the branch diff (`infra/mechanized-loop...wi453-hats-roster`, 9 files,
+374/−48 at round 1's tip 5459640d) and the requirement surface: the owner
ruling of record — Decision 11 in
[the sitting-2 plan](../plans/2026-08-13-sitting-2-boundary-and-context.md)
(rulings 2026-08-13q/r/s, accepted 13u; the seven new hats' row text is OWNER
TEXT, verbatim-landing REQUIRED) — and the WI-453 row's frontmatter clause
list (`docs/work/complete/WI-453-hats-roster-boundary-execution.md`). The
spec's `## Deliverable` prose is the implementer's own account and was
supplied only as claims-to-verify, never as evidence; no other self-assessment
was shown. Run under `--sandbox workspace-write` with an out-of-repo
scratchpad; every round's drives left the tree clean. Machine-local absolute
paths in the reviewer's output are rewritten repo-relative (`<scratch>` = the
session scratchpad); nothing else in the verdicts is edited. Findings were
re-verified by the session author against the real tree before any fix (the
author-re-verifies convention); the one consumed finding below reproduced,
and both refuted findings are recorded with their driven counter-evidence,
not dropped.

**Final verdict: APPROVE at ca69f7ba** — round 1 CHANGES-REQUESTED (1 MINOR:
the live roster header's stale six-hat owner instruction; consumed at
ca69f7ba), round 2 CHANGES-REQUESTED (2 MINOR prose claims, both REFUTED with
driven evidence, no code change), round 3 the adjudication + verdict round on
the same tip: both refutations upheld, APPROVE. The machine line that governs
is the last one in this file.

**The predicate-scope question, adjudicated (both reviewer and author,
independently, same numbers).** Decision 11's fix language for
FIRST-RUN-ADOPTER is *"Re-point it at the deliverable (a
`tags contains "templates"`-style predicate that actually fires)"* — a style
example with a stated intent, not verbatim row text (unlike the seven new
hats' rows, which 13u ruled verbatim and which land byte-identical). The
landed predicate
`'tags contains "scripts" or tags contains "templates" or tags contains "process"'`
adds two clauses beyond the literal example. Measured over the real census
(453 work-item contexts from `docs/work/**/*.md` front matter through
`hats.context_from_work_item`): `templates` fires on exactly 1 historical row
(WI-131, a workstream label no later row uses), `scripts` on 208, `process`
on 15, the union on 224. The ruling's literal example alone would therefore
leave the hat still effectively voiceless — defeating the ruling's own stated
purpose, *"a predicate that actually fires"* — while the three clauses are
precisely the kit's deliverable classes (its product is its shipped scripts,
templates and process docs), the same vocabulary CROSS-PLATFORM already keys
on. Judged a **faithful execution of the ruling's intent, not unauthorized
scope**; the roster file remains MARKED FOR THE OWNER'S EDIT AT RETURN, so
the owner sees and may re-cut the clause set on the standing surface built
for exactly that. One honest residual for that owner pass: the `dashboard`
workstream (47 rows) also edits shipped scripts, and the hat does not fire
there — under-coverage the owner may choose to close by adding a clause.

---

## Round 1 — at 5459640d (CHANGES-REQUESTED, 1 MINOR)

WI-453 executes the Decision 11 boundary roster: FIRST-RUN-ADOPTER's
by-defect-silent predicate re-pointed, seven ruled hats added (the UX pair +
five tag-keyed aspect hats) to BOTH roster copies —
`docs/requirements/hats.toml` (this repo's live instance) and the shipped
`project-trajectory/registries/hats.template.toml` — with the two kinds of
silence stated in both headers, the UX pair `always` here and
`render`/`ui`-gated in the template (the 13u-accepted VALUES split), and the
census/structure tests updated. `hats.py` itself is UNCHANGED in the range
(verified by git, then treated as testable). The worst failure class is a
paraphrased owner ruling: silently wrong roster text in the one file whose
whole job is to be owner-read.

### Failure classes hunted, worst-first

1. Ruled rows not byte-verbatim to Decision 11 in either copy; pre-existing
   hat text disturbed.
2. Unauthorized scope in the predicate fix (the `scripts`/`process`
   clauses) — judged from the ruling text against the measured census.
3. "Off by default" aspect hats actually firing on real rows.
4. The dogfood split done wrong (STRUCTURE drift between copies; census/
   structure tests asserting the wrong thing).
5. hats.py refusal paths regressed by the grown roster.
6. Prose-count drift (six vs thirteen) across README/bootstrap/tests and the
   scaffold surface.
7. Done-when coverage: every Deliverable claim reproduced or UNCOVERED.

### Exact commands and driven output (reviewer, re-verified by the author)

1. Byte-level script diff of all seven new hats' `asks`/`listens_for`/
   `applies_when` in BOTH copies against Decision 11's ruled text: verbatim,
   zero text failures; FIRST-RUN-ADOPTER's `asks`/`listens_for` and the five
   other original hats untouched by the diff (author twin drive:
   `<scratch>/verbatim_check.py`, same result — the only `applies_when`
   deltas are the predicate fix and the instance UX pair's `always`, i.e.
   the ruled fix and the 13u-accepted divergence).
2. Census derived fresh (453 contexts): no context declares `scope`; the old
   predicate's scope clauses fire on 0 rows, the whole old predicate on
   exactly {WI-131}; the new predicate on 224 ⊃ {WI-131} — the spec's three
   figures reproduce exactly. Predicate-scope judgment: PASS (the header
   verdict above).
3. All five aspect hats driven over all 453 real contexts through
   `hats.applicable`: 0 fire; each fires with its own tag
   (`safety`/`legal`/`personal-data`/`a11y`/`perf`). Template UX pair: silent
   on `{}`, fires on `render` and on `ui`; question text identical across
   copies.
4. Refusal paths driven: unknown key, missing key, mixed `or`/`and`,
   malformed TOML, falsey `hat` table all raise `HatsError`; absent file
   → `[]`; both shipped roster files load through `hats.load`.
5. `tests/test_hats.py` + `tests/test_dogfood_sync.py` → 71 passed,
   1 skipped; targeted scaffold + refusal tests passed; `bootstrap.py`
   scaffolds the thirteen-hat template to `docs/requirements/hats.toml`.
6. R4 map: every numbered Deliverable claim covered by a driven observation
   or a named test; none UNCOVERED. (Author baseline at this tip:
   `tests/test_hats.py tests/test_dogfood_sync.py tests/test_bootstrap.py`
   → 125 passed, 1 skipped.)

### Findings

- [MINOR] docs/requirements/hats.toml:3 -> live roster header still calls itself a "six-hat starting roster" and tells the owner to "review the six", contradicting the thirteen-hat roster and updated shipped prose -> update the active header references to thirteen/current wording while preserving intended historical attribution -> @owner

VERDICT: CHANGES-REQUESTED findings=1

**Author re-verification and consume (fix commit ca69f7ba).** Reproduced:
`grep` shows the instance header's lines 3 and 6 were the only live stale
"six" references repo-wide (every other hit is historical record — archived
WI specs, ruled OI rows, logs — or unrelated; the template header already
counts thirteen). Fixed with a comment-only edit: the OI-19 citation now
records the growth ("grown to thirteen by Decision 11, rulings 2026-08-13q/s
— WI-453") and the active owner instruction reads "review the thirteen",
stating which rows are ruled owner text (13u). Ruled rows untouched. Commit
bar green: smoke `1134 passed, 7 skipped` (30.1s), `check_docs` OK
(404 docs, 1185 links, 0 broken).

---

## Round 2 — at ca69f7ba (CHANGES-REQUESTED, 2 MINOR — both REFUTED)

REWORK re-verdict per charter R5, fresh context: re-drive round 1's break
scenarios on the fixed tip, probe the fix's own seams, confirm the finding is
consumed.

### Exact commands and driven output

1. The fix's seams held: `git show ca69f7ba` touches only the header comment
   block; both files parse and load; exactly thirteen `[hat.*]` tables
   counted, not trusted from prose; the seven ruled rows re-verified
   byte-verbatim in both copies.
2. Round-1 scenarios re-drove clean on this tip: aspects silent on all real
   contexts and tag-live (`ASPECTS_SILENT_ALL_AND_TAG_LIVE_OK`), census
   `old == {WI-131} ⊂ new`, UX split + identical question text
   (`UX_SPLIT_AND_IDENTICAL_TEXT_OK`), refusal paths refuse.
3. Suites re-run: `test_dogfood_sync.py` 36 passed 1 skipped;
   `test_bootstrap.py` 54 passed; hats census/structure pins green.

### Findings

- [MINOR] docs/requirements/hats.toml:3 -> live header still says "six-hat starting roster" -> describe it as the historical six-hat launch with the current roster thirteen -> @owner — **REFUTED with driven evidence**: the phrase sits inside the citation of the OI-19 ruling and the SAME sentence continues "grown to thirteen by Decision 11, rulings 2026-08-13q/s — WI-453"; the header's active instruction (round 1's actual defect) now reads "review the thirteen" and states thirteen twice. A historical attribution whose sentence states the current truth is not stale active text; round 3 upheld this.
- [MINOR] docs/requirements/open-items.toml:424 -> live recommendation still instructs "review the six" -> update or supersede -> @owner — **REFUTED with driven evidence**: `open-items.toml` is not in the WI-453 diff at all (`git diff 160a0c1d..ca69f7ba --name-only` matches 0), the text predates the WI (landed 2026-08-12, commit db34b072), and it sits in the ruled OI-19 row's `recommendation` field — the decision-time record of what was put to the owner, whose `decision` field records "RULED (owner, 2026-08-13)". Rewriting a ruled row's recommendation falsifies the record; round 3 upheld this.

VERDICT: CHANGES-REQUESTED findings=2

**Author adjudication.** Both findings refuted as above — no code change, tip
unchanged at ca69f7ba — and both refutations handed to a fresh round 3
context to break.

---

## Round 3 — at ca69f7ba (APPROVE)

The adjudication + verdict round on the final tip, fresh context: break the
two refutations if they are wrong, and sweep the diff surface for anything
both prior rounds missed.

### Exact commands and driven output

1. Refutation A adjudicated: **HOLDS** — the current active header text says
   "review the thirteen"; the six-hat phrase is historical attribution
   completed with the current truth in the same sentence.
2. Refutation B adjudicated: **HOLDS** — `open-items.toml` is absent from the
   diff, OI-19 is ruled, and its recommendation field is historical decision
   input, not active instruction.
3. Fresh sweep of the diff surface produced no new finding.
4. **Author supplement, driven on the final tip ca69f7ba from the main
   venv:** full unfiltered suite `python -m pytest -q -n auto` →
   `2495 passed, 11 skipped in 401.80s (0:06:41)`; smoke
   `1134 passed, 7 skipped in 30.09s`; `check_docs.py --ignore
   docs/test/report.md --ignore "docs/work/*" --stale` → OK, 0 broken.

### Findings

(none)

**Author re-verification.** Every reviewer claim across the three rounds was
independently re-driven against the real tree before recording (the verbatim
byte-diff, the 453-row census and all three predicate counts, the
aspect-silence and tag-activation drives, the UX split, the refusal paths,
the suites). The review's cumulative record: 3 findings across two rounds —
1 consumed at ca69f7ba with the commit bar green, 2 refuted with driven
counter-evidence. The predicate's `scripts`/`process` clauses are judged a
faithful execution of Decision 11's stated intent (the header verdict), with
the `dashboard`-workstream under-coverage noted for the owner's standing
roster-edit pass.

VERDICT: APPROVE findings=0
