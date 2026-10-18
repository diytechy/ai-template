# WI-943 plan: the merge authorizes a MEANING re-attestation only for a blessed row, through the one reader the act derivation also reads

Spec: `docs/work/active/wi-943/WI-943-merge-floor-meaning-bless.md` (specref
`docs/decisions/wi-912.toml`, D-008, with D-011's follow-up note and D-012's
convergence map; the owner's calls `coordinator-2026-10-17` D-009 and D-010,
quoted in the spec). Delivers SR-232 and SR-178. Read in the lane worktree at
`396ff9f44`.

## The architectural-delta answer

DELTA: within

The work item does two of the four, inside its own scope (spec S5):

- **A domain narrows.** The merge's authorizing domain for an amendment
  part goes from `{MEANING, CLARITY}` to `{CLARITY, MEANING carrying the
  bless mark}`. No value is added to any enum or cell vocabulary: the mark
  `- [MEANING+BLESS]` already exists (WI-912).
- **An output depends on an input it did not read.** The merge's backing
  checks (`uncovered_refusal`, `unaccepted_refusal`) now read the mark,
  which is already in the accepted verdict part's body (`part[2]`) that
  `accepted` hands them. No new file, process or boundary is read.
- **No new state, no new boundary.** Both readers keep crossing the seams
  they cross today: the merge reads `kitlib/sitting` through IF-287 (via
  `acceptance_record`, IF-091), and the act derivation reads IF-287 and
  serves IF-296. `adjudicate_act` already imports `kitlib.sitting`
  (IF-287's requestor list already names it), so moving its bless read from
  `kitlib.verdict.blessed_rows` to `kitlib.sitting.judged_rows` removes an
  edge rather than adding one.

The rows that carry the change: P1 (the reader's narrowed domain and the
derivation's switch to it, one commit), P2 (IF-287's contract sentence and the
regenerated reference), P4 (the spine rows stating the narrowed domain). No
component, interface row or sub-component split changes, and no refactor is
owed. The spec's found-not-fixed item (the held-rung policy's two homes,
`intake.adjudication_action` vs `acceptance_record.held_reattest_refusal`)
stays the coordinator's to file; this plan does not touch it.

## What the code reads today (the facts the plan rests on)

- `kitlib/sitting.py` (711 lines): `_AUTHORIZING = {"first-approval":
  ("APPROVE",), "amendment": ("MEANING", "CLARITY")}`; `judged_rows(parsed)`
  returns `{(kind, rid)}` over `part[3]` (the rulings) only. It is NOT in
  `__all__`. Its callers: `_named_line` (→ `unaccepted_refusal`) and
  `uncovered_refusal`. `sitting.py` imports `row_rulings` from `.verdict`.
- `kitlib/verdict.py`: `ROW_RULINGS["amendment"]` maps `- [MEANING]`,
  `- [CLARITY]` and `BLESS_TAG = "- [MEANING+BLESS]"`, the last to `MEANING`;
  a row tagged two ways reads the fail-toward `MEANING`. `blessed_rows(text)`
  returns the rows marked `[MEANING+BLESS]` minus every row also tagged
  another way. Its one caller is `adjudicate_act._authorized` (line 215).
- `adjudicate_act.py` (481 lines): `_authorized(parts, dial)` calls
  `kverdict.blessed_rows(parts[kind][2])` per kind and passes `rid in blessed`
  to `_arm(ruling, held, blessed)`, which returns None for a MEANING row
  without the mark. The module docstring (line 17, "WHAT THE VERDICT
  AUTHORIZES") and `_arm`'s docstring state the mark as "the one condition
  this module adds".
- `acceptance_record.merge_approval_refusal` runs, in order:
  `held_reattest_refusal` → `kitlib.sitting.unaccepted_refusal` (acts naming a
  verdict) → `backed_act_refusal` (→ `uncovered_refusal` over every acted row;
  its reason is appended to `lane_approval_refusal`'s text, so the row lines
  and remedy reach the caller). `backed_act_refusal`'s docstring says "each
  row it re-attests ruled MEANING or CLARITY". With `metas=[]` (an unscoped
  lane) no scope check runs and the backing check still does.
- The probe (`review-tmp/2026-10-17e/drafts/probe/probe_floor.out`): a plain
  `[MEANING]` hand re-attestation on a released rung is admitted (`None`)
  both with `[("WI-301.md", {"brief": "amendment", "adjudicates":
  ["SR-001"]})]` and with `[]`; with the reader patched it is refused and the
  `[MEANING+BLESS]` act is admitted.
- Tests: `tests/test_snapshot_readers.py` drives `merge_approval_refusal` on
  real scaffolds. `_bind_branch(root, rows, ...)` writes every amendment row
  `[CLARITY]` and every first-approval row `[APPROVE]` (no tag override);
  `_amendment_act(root, reattests, held, verdict, binding, judged)` names a
  verdict when `verdict` text is given; `_mixed_act(root, approve_scope,
  amend_scope, metas)` binds via `_bind_branch`. The held pins are
  `test_a_held_rung_*` (lines 420-532). `tests/test_adjudicate_act.py` holds
  the bless reader tests (lines 175-198), the derivation tests (285-360) and
  `test_each_rows_act_arm_follows_the_adjudication_action_policy_on_every_rung`
  (678), which loops `_arm(ruling, held, blessed)` over `blessed in (True,
  False)`.
- No module-size ratchet `BASELINE` entry exists for `kitlib/sitting.py`,
  `adjudicate_act.py` or `acceptance_record.py` relevant here (all under
  `THRESHOLD = 1000` or unchanged in size class); the change is a few lines
  net.
- Lane order: WI-929 has landed (`e45ed5a75`), so LLR-310 is read as it left
  it. WI-942 is in flight in its own lane and amends LLR-278, TC-278 and the
  same recipes paragraph; the spec (S1, S6) has it land first. This plan's
  code step (P1) does not touch WI-942's surface and can build now; P3's
  recipes edit, P4's LLR-278/TC-278 edits and P5's RESYNC entry are written
  after this lane rebases onto WI-942's landing (recipes §3: rebase a lane
  with committed spine rows, never merge-refresh). If WI-942 has not landed
  when P1 is done, the builder stops and reports rather than editing those
  three shared surfaces cross-lane.

## Design decisions the builder follows

1. **`judged_rows` holds the condition** (`kitlib/sitting.py`).
   - Import `blessed_rows` beside `row_rulings` from `.verdict`.
   - `judged_rows(parsed)`: for each `(kind, part)`, compute
     `blessed = blessed_rows(part[2]) if kind == "amendment" else frozenset()`
     and admit `(kind, rid)` when `ruling in _AUTHORIZING[kind]` and (ruling
     is not `MEANING` or `rid in blessed`). `_AUTHORIZING` keeps its shape;
     its comment says the amendment's MEANING authorizes only with the mark,
     and the held-rung CLARITY-only rule stays `acceptance_record`'s.
   - `judged_rows` joins `__all__` (deliverable 1).
   - Docstrings and lines: `judged_rows` says it is the one reader of what an
     accepted verdict authorizes an act on; `_named_line`'s line reads
     `"  {} (does not authorize {})"`; `unaccepted_refusal`'s headline says
     "one that does not authorize the rows it re-attests"; each
     `uncovered_refusal` row line reads `"  {} ({}) is authorized by no
     accepted verdict"`. Both remedies gain the one sentence: "An amendment's
     MEANING row authorizes a re-attestation only when its verdict marks it
     `[MEANING+BLESS]`: re-sit that row." The headlines keep the words
     `ACCEPTED`, so the existing assertions (`"ACCEPTED" in refusal`) hold.
   - **Check before editing the row lines:** the existing assertion
     `"SR-001 (amendment)" in refusal`
     (`test_an_accepted_sitting_over_other_rows_does_not_authorize_this_act`,
     `test_a_single_kind_verdict_over_other_rows_does_not_authorize`) still
     matches, since the `"<row> (<kind>)"` prefix is kept. The builder greps
     `tests/` for "is judged by no accepted verdict" and "does not judge" and
     keeps every existing assertion's expectation unchanged (the spec's pins);
     if one asserts the old wording verbatim, the old phrase is kept and the
     new sentence is only added.
   - `acceptance_record.held_reattest_refusal` and `_held_act_lines` are not
     touched.
2. **`_authorized` reads the same reader** (`adjudicate_act.py`, same commit
   as 1).
   - `judged = ksitting.judged_rows(parts)`; for each kind in
     `("amendment", "first-approval")` and each `(rid, ruling)` of
     `parts[kind][3]` in its existing order, skip a row whose `(kind, rid)` is
     not in `judged`, then `act = _arm(ruling, held)`. The set is only a
     filter, so the derived order (amendment first, verdict order within) is
     unchanged.
   - `_arm(ruling, held)`: the `blessed` parameter and its clause go; it keeps
     `ruling not in (APPROVE, CLARITY, MEANING) → None` and
     `intake.adjudication_action(held, ruling) == "recommend" → None`.
   - The `kverdict` import stays only if another use remains (the builder
     checks; `ROW_RULINGS` is used by tests through `kverdict`, not by the
     module). The module docstring's "Q2 makes a MEANING row's blessing a
     typed mark on the verdict (`kitlib.verdict.blessed_rows`)" and "WHAT THE
     VERDICT AUTHORIZES" say the authorized rows are `kitlib.sitting.judged_rows`'s,
     the reader the merge also reads; `_arm`'s docstring drops "The bless mark
     is the one condition this module adds".
3. **Stale docstring outside the spec's file list.**
   `acceptance_record.backed_act_refusal`'s docstring ("each row it
   re-attests ruled MEANING or CLARITY in an amendment part") becomes "ruled
   CLARITY, or MEANING with the bless mark, in an amendment part (the one
   reader, `kitlib.sitting.judged_rows`)". It is a docstring only, but it
   makes `scripts/acceptance_record.py` a changed kit-owned file, so P5's
   RESYNC overwrite list names it beside the spec's three. Flagged for the
   critic: the spec lists three kit-owned files; this is the fourth, for a
   comment the change makes false.
4. **IF-287.** The contract paragraph in `kitlib/sitting.py`'s docstring gains
   one clause after `accepted`/`accepted_at`: "`judged_rows(parsed)` is the
   ONE reader of the rows an accepted verdict authorizes an act on - an
   APPROVE row, a CLARITY row, and a MEANING row only with its bless mark -
   which the merge's backing checks and the act assembler both read". The
   `interfaces.toml` row's `data` cell ("verdict binding/path and
   accepted-verdict grammar; ...") is left as it is: the clause sits under
   "accepted-verdict grammar", and the spec asks for the docstring sentence
   only. `docs/interface-reference.md` is regenerated with the generator
   `check.py` names for it (`gen_arch_map.py`, the repository's invocation;
   the builder confirms the exact flags from `check.py`'s freshness step and
   uses `--src` as the coordinator recipes do).
5. **Runtime flows.** Flow 4 (the merge slot) and flow 6 (the act turn) keep
   their sequences: no message, participant or branch changes; only which
   rows a check admits. No flow edit. The sitting may ask for one.

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | One commit: `judged_rows` admits an amendment MEANING row only with its bless mark and joins `__all__`; its two callers' lines and remedies; `_authorized` filters by it and `_arm` loses `blessed`; the docstrings that state the old rule; the new tests and the arm test's moved half | D1; D2; D3; D4; D5; D6; D7; SR-232; SR-178; TC-278; TC-368; TC-331; TC-327 | IF-287; IF-296; IF-091 | |
| P2 | IF-287's contract sentence in `kitlib/sitting.py`; `docs/interface-reference.md` regenerated | D8; SR-232 | IF-287 | P1 |
| P3 | `PROCESS_OPTIONS.md` "How it is held" item 1 clause with `byte-budget-guard`'s delta; the recipes §3 "The act turn" item 5 sentence in the kit source and both skill copies, byte-identical (after the rebase onto WI-942's landing) | D8; SR-178; SR-232 | IF-091; IF-296 | P1 |
| P4 | Spine rows for the checkpoint sitting (Terra authors, after the rebase onto WI-942's landing): LLR-310, LLR-278, LLR-338, TC-278 amended; TC-278's evidence names the new merge tests; TC-368's evidence gains the new act-side tests as traced upkeep | D9; SR-232; SR-178; TC-278; TC-368 | IF-287; IF-296; IF-091 | P1; P2 |
| P5 | `RESYNC_PACK.md` entry anchored at the landing's parent; the commit bar, `check_trajectory.py --strict` and `trace.py --strict` on the landing tip | D10; D11; SR-232; SR-178; TC-278; TC-368; TC-331; TC-327 | IF-287; IF-296; IF-091 | P2; P3; P4 |

Excludes: TC-153; TC-269; TC-271 — they verify SR-178 through the drift comparison basis (LLR-158), the needs file's two tiers (LLR-271) and each registry's copy named on the owner's surfaces (LLR-273); this item changes none of those, their rows stay unchanged (spec deliverable 4, "Unchanged"), and their evidence runs untouched in the lane's full suite at P5.

## Step detail: what each changes, the tests it adds, and what each fails on before the change

### P1 — the reader and the derivation, one commit (D1-D7)

Edits per decisions 1-3. Tests added (all new names; "before" = the lane at
`396ff9f44`):

In `tests/test_snapshot_readers.py` (merge floor, real scaffolds, released
rung via `_release`). Fixture change: `_bind_branch` gains a keyword
`tags=None`, a `{row id: [tag, ...]}` override, so a row can be written
`[MEANING]`, `[MEANING+BLESS]` or two lines tagged two ways; the default
output is byte-identical to today's, so every existing caller is unchanged.
`_amendment_act` gains `tags=None` passed through to `_bind_branch`, and
`_mixed_act` gains `amend_tag="CLARITY"` passed through the same way. The
machine line stays from `_KIND_LINES` (`VERDICT: CLARITY rows=1`), which
`parse` accepts whatever the row tags say (the verdict's machine line and its
row lines are read separately; the builder confirms by running the existing
`[MEANING]` held test's shape, which already pairs a MEANING row with a
machine line).

1. `test_a_released_plain_MEANING_reattestation_is_refused_naming_the_row_and_the_mark`
   (parametrized over `metas` = `_AMENDMENT` and `[]`, ids `scoped`,
   `unscoped`) — D2. `_amendment_act(scaffold, {"SR-001"}, tags={"SR-001":
   ["MEANING"]})`; asserts the refusal is not None, contains
   `"SR-001 (amendment)"` and `"[MEANING+BLESS]"`. **Fails before:** the
   floor returns None for both (the probe).
2. `test_a_released_row_tagged_two_ways_is_refused` (parametrized over
   `["MEANING+BLESS", "CLARITY"]` and `["MEANING+BLESS", "MEANING"]`) — D3.
   Same shape, scoped. Asserts a refusal naming `SR-001 (amendment)`.
   **Fails before:** `row_rulings` reads MEANING, which `_AUTHORIZING`
   admits, so the floor returns None.
3. `test_a_combined_act_carrying_a_plain_MEANING_reattestation_is_refused_whole`
   — D4. `_mixed_act(scaffold, ["SR-002"], ["SR-001"], amend_tag="MEANING")`;
   asserts the refusal names `SR-001 (amendment)` and does not name
   `SR-002 (first-approval)` as unauthorized (the first approval is backed),
   and that the return is a refusal (the merge takes nothing of the act).
   **Fails before:** returns None (`test_a_mixed_approval_and_reattestation_act_merges`
   is the same act with CLARITY and merges).
4. `test_a_named_verdict_ruling_the_row_plain_MEANING_is_refused_naming_the_verdict`
   — D5. `_amendment_act(scaffold, {"SR-001"}, verdict="- [MEANING] SR-001
   title -> moved\n\nVERDICT: MEANING rows=1\n")` on the released rung;
   asserts `_VERDICT in refusal`, `"does not authorize SR-001" in refusal`
   (the named-verdict check, which `merge_approval_refusal` runs before the
   backing check, so its text is the one returned). **Fails before:** the
   named verdict "judges" SR-001 and the branch binding is the same file, so
   both checks pass and the floor returns None.
5. Pins (D6), each passing before and after:
   `test_a_released_MEANING_BLESS_reattestation_merges` (parametrized
   `scoped`/`unscoped`, `tags={"SR-001": ["MEANING+BLESS"]}`, asserts None);
   `test_a_named_verdict_blessing_the_row_merges` (the D5 shape with
   `- [MEANING+BLESS]`, asserts None);
   `test_a_combined_act_with_a_blessed_reattestation_merges`
   (`amend_tag="MEANING+BLESS"`, asserts None). The existing
   `test_a_held_rung_*` tests run unchanged (not edited).

In `tests/test_adjudicate_act.py`:

6. `test_judged_rows_admits_an_amendment_MEANING_row_only_with_its_bless_mark`
   — D2/D3 at the reader. Pure: builds `parsed` with
   `ksitting.accepted(text, ksitting.render_requested("amendment",
   ("amendment",), "accepted"))` for `[MEANING]`, `[MEANING+BLESS]`,
   `[CLARITY]`, and the two two-way pairings; asserts the set
   `judged_rows` returns (only the blessed and the CLARITY rows), and that a
   first-approval `[APPROVE]` row is still admitted and `[RETURN]` is not.
   **Fails before:** `[MEANING]` and both two-way rows are admitted.
7. `test_the_bless_mark_has_one_reader_shared_by_the_merge_and_the_act` — D7.
   Scans every `*.py` under `project-trajectory/scripts` (excluding
   `__pycache__`) for the token `blessed_rows` and asserts the set of files
   holding it is exactly `{kitlib/verdict.py, kitlib/sitting.py}`; asserts
   `"blessed" not in inspect.signature(act._arm).parameters`; asserts
   `"judged_rows" in ksitting.__all__`. **Fails before:** `adjudicate_act.py`
   holds `blessed_rows`, `_arm` takes `blessed`, `judged_rows` is not in
   `__all__`.
8. The arm test's moved half — D7. In
   `test_each_rows_act_arm_follows_the_adjudication_action_policy_on_every_rung`
   the `for blessed in (True, False)` loop goes: it asserts `_arm(ruling,
   held)` against `intake.adjudication_action` for every `(held, ruling)`
   (MEANING on a released rung now reads `"reattest"`, the policy's `flip`).
   The bless half becomes a verdict-text case in the same test function (so
   TC-368's evidence names the same test id): for held in `(True, False)`,
   `act._authorized(parsed, dial)` over one amendment part ruling
   `SR-001 [MEANING]`, `LLR-001 [MEANING+BLESS]`, `TC-001 [CLARITY]`, with
   `dial` the value the derivation tests use for each rung (`_repo`'s
   released default and `"DevStg-Release"`), via
   `kauthority.dial_at` on the two fixture repos if a bare value is not what
   `_held` takes. Released: `[("reattest", "LLR-001", False), ("reattest",
   "TC-001", False)]`; held: `[("reattest", "TC-001", True)]`. **This half is
   a pin, not a new failing test:** the derivation's output is unchanged by
   design (spec deliverable 2), so it passes before (through `blessed_rows`
   in `_authorized`) and after (through `judged_rows`). The first half fails
   before only by signature (`_arm` takes three arguments), which is the
   change itself.

Pins that must pass unchanged in expectation (D6, D7): the three bless-reader
tests (lines 178-198), `test_a_MEANING_row_without_the_bless_mark_is_left_unacted`,
`test_a_blessed_MEANING_row_on_a_released_rung_is_reattested`,
`test_a_blessed_MEANING_row_on_a_held_rung_is_left_unacted`, every other
derivation test in the file, the whole of `tests/test_snapshot_readers.py`'s
existing set (TC-278's evidence), and `tests/test_integrate_admission.py`
(TC-331's evidence; its `_bind`-style fixtures write CLARITY/APPROVE, so no
existing case relies on a plain MEANING authorizing). TC-327's
`tests/test_adjudicate_brief.py` set is run too (it reads `kitlib/sitting`).

The D1 proof: the builder runs the new tests on `396ff9f44` (stash the source
edits, keep the tests and fixture changes) and pastes the failures (items
1-4, 6, 7, and the first half of 8), then runs them and the pins green on the
P1 commit. Items 5 and the second half of 8 pass on both, as pins should.

Lane bar after P1: `run.cmd smoke` from the lane (60 s budget), plus
`python -m pytest -q tests/test_snapshot_readers.py tests/test_adjudicate_act.py
tests/test_integrate_admission.py tests/test_adjudicate_brief.py` (not all in
the smoke tier).

### P2 — IF-287 and the interface reference (D8)

Decision 4's sentence; regenerate `docs/interface-reference.md`; the
freshness step of `check.py` (interface-reference) passes. No test added: the
regenerated file is enforced by `check.py`'s existing freshness step, which
fails if the docstring changes without regeneration.

### P3 — PROCESS_OPTIONS.md and the recipes item (D8)

- `project-trajectory/PROCESS_OPTIONS.md`, "Who performs the approval act",
  "How it is held" item 1: after "bindings that judged that act's own rows"
  insert "(a meaning row's re-attestation only by a verdict that blesses
  it)". Invoke `byte-budget-guard` before and after; report its delta in the
  lane report. (The table row above it already says the act re-attests a
  meaning row "only when the verdict blesses it"; no second edit.)
- `project-trajectory/skills/coordinator-cycle/references/recipes.md` §3 "The
  act turn" item 5 (as WI-942 leaves it) gains: "An act a lane already took
  from such a verdict on a MEANING row is not authorized either: the merge
  slot refuses it, so re-sit the row before the landing." Then
  `bootstrap.py --dest . --sync`; `.claude/skills/coordinator-cycle/` and
  `.agents/skills/coordinator-cycle/` are byte-identical to the source
  (`tests/test_skills_sync.py` enforces; the builder runs it).

### P4 — the spine rows (D9)

Terra authors, the lane's checkpoint sitting judges. Text exactly as spec
deliverable 4 quotes it, applied to the rows as WI-942 leaves LLR-278 and
TC-278 (rebase first):

- LLR-310 (Approved): its three edits (the re-attestation clause, the named
  verdict "authorize ... in the same way", and the closing "One reader ...
  serves both the merge and the act assembler"). `code_symbol` already lists
  `judged_rows` and `blessed_rows`; no change.
- LLR-278 (Approved): its two edits.
- LLR-338 (Approved): the last sentence replaced.
- TC-278 (Approved): method, expected and evidence. Evidence gains the
  `tests/test_snapshot_readers.py::` ids of P1 items 1-5.
- TC-368 (Approved): text unchanged; its evidence cell gains P1 items 6 and 7
  (`tests/test_adjudicate_act.py::test_judged_rows_admits_an_amendment_MEANING_row_only_with_its_bless_mark`,
  `::test_the_bless_mark_has_one_reader_shared_by_the_merge_and_the_act`) as
  traced upkeep; the arm test keeps its id. Flagged for the sitting: the spec
  names TC-368's evidence as upkeep only "if the arm test is renamed"; these
  two tests verify LLR-310's and LLR-338's amended sentences, and TC-368 is
  the case that verifies both rows. If the sitting rules they belong on
  TC-278 instead, they move there.
- Unchanged: SR-232, SR-178, SR-228, SR-231, LLR-158, TC-331, TC-153, IF-287's
  and IF-296's registry rows.

After authoring: `check_trajectory.py --strict` and `trace.py --strict` clean
in the lane (every evidence id resolves to a collected test).

### P5 — RESYNC entry and the landing bar (D10, D11)

- `project-trajectory/RESYNC_PACK.md`: a new `### ... [since <landing
  parent>]` entry after WI-942's, in the pack's shape (What changed; Kit-owned
  files — overwrite: `scripts/kitlib/sitting.py`, `scripts/adjudicate_act.py`,
  `scripts/acceptance_record.py` (decision 3), `PROCESS_OPTIONS.md`, and the
  `coordinator-cycle` skill's `references/recipes.md` if the pack lists skill
  files for this-repo-scope skills, else not; what the adopter does: nothing
  migrates, no setting changes; a loop lane in flight whose sitting
  re-attested an unmarked MEANING row in-turn before the adopter's WI-912
  resync is refused at the slot until those rows are re-sat). The anchor is
  re-stamped at the landing (the coordinator's landing recipe);
  `tests/test_resync_pack.py` runs.
- On the landing tip: `run.cmd smoke` green within its 60 s budget, pasted;
  `python project-trajectory/scripts/check_trajectory.py --strict` and
  `python project-trajectory/scripts/trace.py --strict` clean, pasted. The
  regenerated surfaces the landing recipe lists (interface reference,
  components, cli-reference as applicable) are current.

## Risks and open points for the critic and the sitting

- **Wording of the refusal lines.** Decision 1 changes two refusal lines'
  verbs ("judge" → "authorize"). Existing tests assert prefixes that survive,
  but the builder must grep before editing; if an existing assertion pins the
  old verb, the old verb stays and only the remedy sentence is added (the
  spec's "pins pass before and after").
- **The fourth kit-owned file** (`acceptance_record.py`, docstring only) is a
  deviation from the spec's RESYNC list, argued in decision 3.
- **TC-368's evidence gains two ids** (P4), argued there.
- **D1 and the moved arm half.** The verdict-text half of the arm test cannot
  fail before: the spec makes the derivation's output unchanged. It is stated
  as a pin, not claimed as a red test.
- **WI-942 ordering.** P3's recipes edit, P4's LLR-278/TC-278 edits and P5's
  entry wait for WI-942's landing and this lane's rebase onto it; P1 and P2
  do not. If WI-942 stalls, the lane holds at P2 and reports.
- **The hand landing** stays outside the floor until WI-808 (spec Trust,
  residue; owner D-009). This plan adds no hook step.
