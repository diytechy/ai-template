## 2026-09-01 — WI-572: the approval act is the adjudicator's, on trunk

**Spec of record:** `../plans/2026-09-01-approval-act-adjudicator-only.md`
(the owner's ruling, 2026-09-01, recorded in
`../log.md` from `2026-09-01-owner-ruling-approval-act.md`). Serialized behind
WI-571 (the copy-scope row); both touch `intake.py` / `baseline_snapshot.py`.

**In one line:** a worker lane may author `Drafted` spine rows and amend cell
text, but the approval act — the `Status` flip into `Approved`/`Founded` and
the `docs/archive/last_approved/` copy that anchors it — is the adjudicator's,
performed on the serial trunk side.

### The baseline this row is measured against

Every commit that moved an `"Approved"` string in a spine registry before the
ruling, classified by where it happened:

- **1 worker-lane flip** — `580df781` (WI-508 slice 6), whose next review round
  returned CHANGES-REQUESTED against exactly those flips.
- **4 lanes minted rows born `Approved`**, skipping the brief entirely —
  `8848f6fb` (WI-483), `ad2222df` (WI-500), `69e4a854` (WI-501), `0cfb2e6f`
  (WI-507).
- The rest were trunk sittings or the pre-ladder rename.

fig: 17 commits, classified by subject; `git log --format='%h|%s'
-S'"Approved"' fd86e47f -- docs/requirements/system-requirements.toml
docs/requirements/low-level-requirements.toml docs/test/test-cases.toml
docs/requirements/system-requirements.csv
docs/requirements/low-level-requirements.csv docs/test/test-cases.csv`
at `fd86e47f`.

### Deliverables

**1. A lane's merge is refused when its delta performs an approval act.**
`acceptance_record.staged_approval_acts` reports a `Status` crossing INTO
`Approved`/`Founded` and a row that arrives already claiming one;
`lane_approval_refusal` words the refusal, naming each row, its registry, the
shape of act, and every `docs/archive/last_approved/` file the branch touched —
each worded by what the branch DID to it (round 4; see below).
`integrate._approval_act_refusal` is the rung, beside `_minted_id_refusal`
whose shape it copies exactly — the merge base, and the ladder placement.

Construction-first, as the plan required: `staged_spine_amendments` already
diffs the merged commit and EXEMPTS a row whose Status moved; the new reader
reports that exempted set MINUS the de-approvals (round 4). All three readers (plus
`staged_drafted_rows`) now share ONE two-tree walk, `_spine_row_sides`,
extracted rather than copied. Verified against the record itself: the reader
reproduces the census above exactly — four flips at `580df781`, and the
born-`Approved` rows of all four lanes.

The judgement lives in `acceptance_record`, not in the merge slot, on LLR-178's
separation: the coordinator that merges is not the reader that decides what a
spine delta did. That also kept `integrate.py`'s size bump to a new rung's
irreducible core.

**2. The first-approval adjudication arm.** If a lane may not approve what it
authored, something must. `intake._first_approval_drafts` (trigger a2) mints ONE
`brief = "first-approval"` adjudication per merge over the `Drafted` rows the
delta added or amended — the exact mirror of trigger (a), one section below it.
`agent_common.SPINE_APPROVAL_RUNGS` names the DevStg rung each spine tier is
approved into so the dial can answer whether that tier is loop-held; a rung the
dial HOLDS is not minted (the owner approves those, through the approval brief,
as today), and an unmapped tier is held. (That table was `intake.APPROVAL_RUNG`
until REVIEW-A; see "The dial filter the brief did not have" below.)

`prompts/adjudicate-first-approval.template.md` is the fifth adjudicator brief,
with `adjudicate_brief.first_approval_values` behind it and its own verdict
grammar (`OUTCOME: APPROVE|RETURN rows=N`). The brief renders each row's WHOLE
CHAIN, which is the owner's stated reason the act is the adjudicator's — so
`trace.reattest_model`'s `chain_of` closure became the public
`trace.spine_chain` + `chain_buckets`. The model's own `rows` list carries only
what changed or is `Drafted`: the right answer to the re-attest brief's question
and exactly the wrong one here, where the settled parent and the passing sibling
test ARE the evidence.

`integrate._adjudication_lane` exempts the actor the ruling names. The
concurrency half the owner asked for was **already built** and is not
re-implemented: an adjudication row is not `ordinary`, so
`dispatch._branch_exclusive` already runs its lane alone. The ruling is what
points the act at that guarantee.

**3. The amendment arm's aftermath is stated and true.** The template's closing
"the flip, if one is owed, is the mechanical tool's act, not yours" went false
when OI-45 (b) retired that tool, so a MEANING verdict on a loop-held rung ended
at a brief nobody was owed. Replaced by a DERIVED `{aftermath}` slot
(`adjudicate_brief._aftermath`), which reads the declared gate authority for the
tiers actually shown and tells the session whether the re-attestation is its own
act or the owner's — rather than leaving it to read and interpret a dial
mid-verdict. `prompts/CATALOG.md` regenerated.

**4. The doctrine says it once.** PROCESS.md §4 gains one clause in its fixed
points and links to PROCESS_OPTIONS.md "Who performs the approval act" (the
ruling, its two reasons, the division-of-labour table the owner asked for in
§2a, and the three holding mechanisms). OI-45 (b) gains the narrowing sentence.
`gate-advance` names the acceptor its procedure was already addressed to;
`spine-authoring` opens with "authoring is not approving"; `worker.template.md`
gains the NEVER clause and its close ritual now says "minted or amended". The
two reference surfaces follow the mechanism they describe:
`docs/enforcement-audit.md` gains the rule's row (with its three-fold honest
residue), and `docs/registry-machinery-reference.md` records the other half of
the amendment walk, plus the narrowing on the `Founded` row's OI-45 citation.

**5. Tests**, all in the modules' existing style: five at the merge slot, four
at the reader, four at the trigger, and — counting the terminal-sequence
regression of round 3 and the three scope regressions of round 4 — nine at the
brief, plus the widened schema pin and the loader triplet's third member.

**6. The two registry rows this lane's own code moved.** New code under an
existing row's Module leaves that row's cells stale, and the rule from the
WI-553 reading is that a lane re-points its own staleness IN-LANE rather than
deferring it:

- `LLR-158` (`Approved`) — its `code_symbol` named four symbols; the module now
  carries the shared two-tree walk and three more readers off it, and the row's
  `Detail` gained the sentence that explains them. Amended, **not flipped**:
  there is no status for a post-approval amendment, the row stays `Approved`,
  and the DRIFT against `docs/archive/last_approved/` is the signal.
- `IF-091` (`Drafted`) — `integrate` is now a second requestor of the seam, so
  it is named as one. Without it the new import is a cross-component crossing
  that no interface row declares.

Both warns were **introduced by this branch** and both are gone;
`check_trajectory` exits 0 with only the pre-existing `schedule -> trace`
crossing standing. The amendment was checked against this row's OWN mechanism
rather than assumed safe: `staged_approval_acts` returns `[]` and
`lane_approval_refusal` returns `None` over `4d0b972d..<staged tree>` — amending
is not approving — while `staged_spine_amendments` reports `LLR-158`, so the
amendment adjudication trigger (a) raises a row for it at merge. This lane's own
edit is the first customer of the arm the same lane shipped, which is the
intended shape and not a special case.

RE-CHECKED AT THE FINAL TIP, because the reading above was taken at a staged
tree BEFORE the close, and the close changes an input this rung reads: draining
`docs/work/active/` empties `_claimed_specs`, so `_adjudication_lane` answers
False and this branch is judged as the work lane it is, with no exemption. Over
`4d0b972d..78e20e4e` the answers are unchanged — `staged_approval_acts` `[]`,
`lane_approval_refusal` `None`, `staged_spine_amendments` still reporting
`LLR-158`. The branch that added the refusal is merge-clean under it at the tree
the integrator sees, which is the only tree the claim is worth anything at.

The amend-without-flip guard then fired on `LLR-158`, both arms, and both are
answered rather than absorbed:

- **The drift arm** — "re-attest in this commit, or the change rides as SNAPSHOT
  DRIFT until the next sitting". Riding as drift is not a miss here, it is the
  ruling: the lane may not re-attest its own amendment, and `intake.py snapshot`
  on this branch is precisely what deliverable 1 refuses. The drift IS the
  handover.
- **The `Hat-Refs` arm** — it says an unchanged cell cannot distinguish "re-read
  and unchanged" from "never re-read", so the answer belongs in the record.
  DELIBERATE: the cell stays inherited (`LLR-158` declares none and takes
  SR-178's `TEST-ENGINEER`). The amendment documents more of the SAME mechanism
  — one walk, four readers — and does not move the row's question, which is
  still how an amendment is DETECTED. Who may act on what is detected is a
  governance concern; it lives on the PROCESS surfaces and in `integrate`'s
  rung, not in this row's cells. Re-read, unchanged, and said so.

### REVIEW-A rework: the dial filter the brief did not have

Round 1 returned CHANGES-REQUESTED with one MAJOR finding, and it was right.

**What was wrong.** `intake._released_drafted_rows` filters the minted
population by the dial — a rung the owner still holds is not handed to an
adjudicator. `adjudicate_brief.first_approval_values` then RE-RESOLVES that
population live at composition time, deliberately (a row minted at a merge is
claimed later, and `red_tc_values`' rule says brief the world the judge is
actually in). But it re-resolved it from `trace.reattest_model`, which is
dial-blind by design, and never put the filter back. Re-computing live had
quietly become re-computing a WIDER question than the mint asked.

The consequence is not cosmetic. Under a mixed dial — `human_approval_through =
"DevStg-Reqs"` holds the SR tier and releases the LLR tier below it — the brief
rendered a held `Drafted` SR beside a released `Drafted` LLR, marked BOTH
`[AWAITING FIRST APPROVAL]`, and derived a `--approves` argument naming both
registries. That is a generated prompt instructing an adjudicator to perform a
signature the owner owes, with the act's own recorded scope carrying it. At the
kit's shipped default dial (`DevStg-Release`, which holds every rung) every row
in the brief was the owner's.

**Why the test suite did not catch it.** `_first_approval_repo` declared no
`docs/process.toml` at all, so its dial fell back to `DevStg-Release` — the
fixture was not this arm's scenario, it was the owner's, and it went green. The
fixture now declares `DevStg-Needs` explicitly, which is the honest statement of
what the arm requires to exist.

**The fix is a deletion, not a guard.** The rung table existed TWICE for one
commit: `intake.APPROVAL_RUNG` keyed by registry (the mint) and
`adjudicate_brief._APPROVAL_RUNG_OF` keyed by tier (the amendment aftermath) —
and the first-approval brief, the third consumer, was wired to neither. Both
copies are deleted. `agent_common.SPINE_APPROVAL_RUNGS` +
`human_approves_spine` is the one home, sitting beside the off-spine
`APPROVAL_RUNGS`/`human_approves` pair it mirrors arm for arm, unmapped-is-HELD
included. The mint, the amendment aftermath and the first-approval brief now all
read it; `intake.py` and `adjudicate_brief.py` both shrank. The predicate's
docstring carries the reader-side contract the off-spine one states for writers:
*a filter applied only at the mint is a filter the brief does not have.*

Three things follow from putting it in the derivation rather than the prose:

- A held `Drafted` row is still SHOWN — it is part of the chain, and holding the
  chain is the owner's whole reason this act is the adjudicator's — but labelled
  `HELD FOR THE OWNER, NOT YOURS TO FLIP`, and it contributes no registry, so a
  session that ignored every word of the prose still cannot record it in scope.
- An SR whose chain holds no released `Drafted` row is dropped whole, and if
  nothing survives the assembler REFUSES, naming the dial. A brief whose every
  row is the owner's is not this arm's question.
- The template's opening claim ("the rung they sit at is one the gate authority
  has released, so no human signature is pending behind you") was TRUE of the
  mint and false of the brief. It now scopes itself to the `[AWAITING FIRST
  APPROVAL]` label and says which mechanism makes it true. `{registries}`' empty
  fallback string went with the refusal that made it unreachable.

**Not taken, and why.** The finding's suggested remedy was to carry the minted
row identities as typed scope on the adjudication row and re-resolve only those.
That is not available at the size the fix warrants: `intake._draft_row`
serializes only `wi_convert.COLUMNS`, and `parse_spec` drops any frontmatter key
that is not a column — the trap `Supersedes`' own comment records — so a typed
scope carrier means a NEW REGISTRY COLUMN, which every adopting repo migrates
to. Against that, the module's stated rule (`red_tc_values`, restated in this
assembler's docstring) is that a brief re-derives its population rather than
remembering the mint's, and the adjudication lane is exclusive on trunk, so the
live population at claim time is the authoritative one. What the finding's
failure scenario actually turns on is the dial, and that is now filtered from
one home at both ends. The identity-scoping half is named here rather than done
silently; if the owner wants it, it is a schema row of its own.

### REVIEW-A rework: a withdrawal still owes re-approval

Round 4 found the shared reader's last asymmetric edge: `Approved` → `Drafted`
was correctly absent from the lane refusal, but a status-only withdrawal was
also absent from `staged_drafted_rows`. That silently stranded the row even
though the live re-attestation model correctly said it awaited `approve`.

The shared two-tree reader now classifies every transition into `Drafted` as an
`amended` Drafted row, with an empty content delta when Status alone moved.
That record feeds the existing first-approval trigger; the approval-act reader
is unchanged and still refuses no de-approval. A reader regression pins both
sides of that split, and a trigger regression pins the resulting
`brief = "first-approval"` mint.

### The harness, and the two reds it leaves

Full unfiltered suite, re-measured after the status-only-withdrawal rework:
**3261 passed, 2 failed, 24 skipped in 576.13 s**. Both failures are the two
reds analysed below, and neither is this row's. The smoke tier on the same tree:
1455 passed, 1 failed, 8 skipped in 21.15 s; the independent budget run measured
20.9 s against the 60 s ceiling — within.

fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=9cc58b2d
fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=9cc58b2d
fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=9cc58b2d

The first failure is
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`, and
it is the DERIVED-ARTIFACT SPLIT, not a defect in the change:

- It passed at `7021e4e1` and fails at `a68cc52a` — i.e. it is the registry
  amendment above, verified by running that single test in a worktree at each
  commit, not inferred.
- `docs/stage` is derived over the SETTLED spine rows, so amending an
  `Approved` row moves its input digest. Regenerating it in a scratch worktree
  at `a68cc52a` changes **only** the `fingerprint` and the `# computed … as-of`
  stamp: `stage`, `stage-ord`, `settled-stage`, `live-stage`, `per-phase`,
  `per-phase-live` and `drafted` all come back byte-identical. No rung moved.
  Re-confirmed at the final tip by `derive_stage.py --print`: every derived
  value above, `phase = 5` included, matches the committed `docs/stage` line for
  line, and `fingerprint` is the single field that differs.
- Regenerating it is not this lane's act. `docs/stage` is a declared generated
  artifact, and every commit that has ever written it is a trunk-side
  bookkeeping commit (`claim:`, `refresh:`, `log:`, `mint:`). The commit bar
  agrees and says so out loud: the `derived-stage --check` step SKIPS on a work
  branch with "generated freshness is the trunk lane's". The trunk lane
  regenerates after the merge and the red clears with it.

**A second red appears only AFTER the close, and it is not this row's either.**
The smoke tier run after the terminal move reds
`test_wi_convert.py::test_the_live_registry_round_trips_in_whichever_home_is_authoritative`
on `docs/work/cancelled/README.md: does not start with a +++ frontmatter fence`.
The test takes one of two branches: with a claim in flight the converter must
refuse BY NAME (`drained-stop`, `active/`) and that refusal IS the test's claim;
with `active/` empty it runs the real folder round-trip. Closing WI-572 drained
the last claim on this branch and moved it onto the second branch, where the
folder walker does not skip the `README.md` files that sit in the work
subfolders.

Not introduced here, and checked rather than argued: the identical failure
reproduces at `9eaeac93` — the trunk commit BEFORE WI-572 was claimed, whose
`docs/work/active/` does not exist at all. It is a latent defect masked by any
in-flight claim, so trunk meets it whenever the queue drains. Named here because
this close is what unmasks it on this branch, and the next session should know
it inherited the red rather than caused it. Like the `docs/stage` red, it is a
harness-bar repair on its own row, not a fix to smuggle into this one.

**A finding this row sharpened but does not fix.** That test asserts a
trunk-side invariant with no work-branch exemption, while its commit-bar twin
has one. Until now the mismatch was nearly unreachable, because a lane amending
a settled spine row was rare. This row makes lane-side amendment the NORMAL
path — a lane amends, an adjudicator approves — so the same red will now greet
routine lanes. Teaching the test the exemption its `--check` twin already has is
a real follow-on; it is a change to the harness's own bar and belongs on its own
row, not smuggled into this one.

### Deviations from the plan

- **The refusal points at PROCESS.md §4, not at the plan.** The plan's
  done-when 1 says the refusal "points at this plan". It is shipped kit code:
  a downstream repo has no `docs/plans/2026-09-01-...`, and CLAUDE.md's
  copy-ready rule refuses a token that cites a record the adopter can never
  read. PROCESS.md §4 ships, and now carries the ruling.
- **The adjudication runs as an exclusive claimed lane, not as a bare
  trunk-side session.** The plan says "on the serial trunk side as an exclusive
  lane". Read literally as "commits directly on trunk", that would be a new
  execution mode; read against this repo's vocabulary, an adjudication row is
  already claimed, already runs alone (`dispatch._branch_exclusive`), and
  already merges through the serial fail-closed queue. So the ruling's
  substance — a work lane never approves, only an adjudication does, and two
  acts cannot overlap — is delivered by exempting the adjudication lane rather
  than by building a second path.
- **One correction outside the row's own scope.** PROCESS.md §4's snapshot
  sentence still said the copy is "replaced wholesale at each approval", which
  WI-571 made false. It is the sentence this row was editing, so leaving a
  known-false clause in place was worse than the one-clause fix.

### Ratchets re-stamped (each with its reason, in the commit that earned it)

`integrate.py` 1,270 -> 1,298 (two stamps: the rung, then its exemption);
`intake.py` 1,179 -> 1,255 (trigger a2), then RE-STAMPED DOWN to 1,247 at the
REVIEW-A rework as the rung table left it; `agent_common.py` 1,262 -> 1,272 at
that rework, where the table landed; `bootstrap.py` 1,652 -> 1,657 (the
MAPPING row); `trace.py:reattest_model` complexity DOWN 19 -> 13, recorded in
the same commit as the extraction that earned it. Byte-watched:
`PROCESS.md` 87,871 -> 88,355, `PROCESS_OPTIONS.md` 181,369 -> 185,060, and
byte-budget-guard's own row to 4,906 (cap 5,000).

### Not done here

The plan's §2a table row "Surfaces to the owner" says rows above the threshold
do NOT surface to the owner. That is the *consequence* of this row, not a
separate surface change: `trace.py --approve modified` still renders every
`Drafted` chain, held or released. Narrowing the owner's brief to the held rungs
alone is a real follow-on and is deliberately not taken here — it would change
what the owner sees at a sitting, which is the owner's call, not a side effect
of moving who acts.

The plan's §2a consequence — that the six MEANING rows of the WI-566 amendment
adjudication are this arm's first re-attestation case — is a trunk-side act on a
future adjudication, not something this lane may perform.

Deferred open items: none — the ruling this row executes is already recorded.
Two candidate follow-ons are NAMED above rather than owed back as decisions:
narrowing the owner's approval brief to the held rungs, and giving
`test_this_repo_s_committed_stage_is_current` the work-branch exemption its
`derive_stage --check` twin already has. (The third named here through round 3 —
`wi_convert`'s folder-home walk — was TAKEN in lane at round 4 below, because
this close is what unmasks it and a red bar fails where it surfaces.)

### REVIEW-A rework: the terminal sequence performs the ruled act

Round 3 found that the first-approval brief's last sentence still carried the
generic adjudication protocol — commit the verdict and stop — after the body had
assigned an approving session a second commit containing the flip and scoped
snapshot. A session could therefore conform to the terminal instruction while
leaving an `APPROVE` verdict unapplied. The terminal sequence now branches on
the per-row rulings: any approved row, including the approved portion of a mixed
`OUTCOME: RETURN` batch, requires the separate approval commit before stopping;
only an all-RETURN result stops without a registry or snapshot change. The
rendered-prompt regression pins all four parts of that sequence.

Rework verification at the implementation commit:

- The complete prompt-brief module is green: **42 passed in 5.02 s**.
  <!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_adjudicate_brief.py" rev=99aedcda -->
- The full suite reads **3260 passed, 2 failed, 24 skipped in 580.39 s**. The
  failures are exactly the inherited `docs/stage` fingerprint and
  folder-registry `README.md` reds analysed above; the added regression is the
  one-test increase over the preceding tip's reading.
  <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=99aedcda -->
- The smoke tier reads **1455 passed, 1 failed, 8 skipped in 22.78 s**, with
  only the same folder-registry red. Its budget enforcer exits 0: **35.3 s
  against the 60 s ceiling**, explicitly classifying that pytest failure as
  non-budget.
  <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=99aedcda -->
  <!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=99aedcda -->
- The docs check reports **0 broken links** (one pre-existing orphan warning),
  and the generated prompt catalogue is fresh at eight prompts.
  <!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=99aedcda -->
  <!-- fig: cmd=".venv/bin/python project-trajectory/scripts/gen_prompt_catalog.py --check" rev=99aedcda -->

### REVIEW-A rework, round 4: four findings answered, one still in flight

Round 4 returned five findings. The four settled below are landed; the MAJOR on
the brief's population is the section after this one.

**The folder-home walk, taken in lane rather than deferred (MAJOR 2).** Round 3
named this a follow-on; round 4 correctly refused the deferral, because the red
is unmasked BY THIS CLOSE and the per-commit bar fails where it surfaces.
`wi_convert.read_specs` walked `rglob("*.md")` and then demanded every hit under
a status directory parse as a spec — a strictness the folder home does not
define. It now reads through `spec_paths`, the `kitlib.registry.spec_files`
re-export this module ALREADY carried twenty lines above it: the write side and
the read side derive their population from one function, so a file the reader
treats as residue cannot be a file the writer treats as a broken row. That is a
deletion of a second walk, not an exclusion of one filename.

**And the repair uncovered why nobody had seen it.** With the walk fixed, four
of `test_wi_convert.py`'s guards went from SKIPPED to failing on stale premises.
The `live_csv` fixture caught EVERY `ConvertError` and reported it as "live
registry has in-flight claims" — so the `cancelled/README.md` parse error read
as a drained-stop refusal, and four guards had been dark since WI-504 split the
folder home into two roots. Both halves are fixed:

- the skip now fires only on the refusal it names (`"drained-stop" in str(exc)`);
  anything else RAISES. A skip whose reason is a guess hides the thing it names.
- the guards measure the registry, which since WI-504 is the UNION of
  `docs/work/` and `docs/archive/work/` — the same union
  `kitlib.registry.read_spec_rows` gives every other consumer. `docs/work/` alone
  is 24 rows, so the "not truncated" guard was reading 546 archived rows as
  truncation, the cancellation guard was vacuous (21 cancelled rows are all in
  the archive), and the not-id-sorted premise was unprovable. `_merged_folder_home`
  copies both roots into one tree — a copy because `to_csv`/`to_specs` are
  single-root by contract and both trees use identical status directory names,
  so the union IS a folder home of the same shape.

Mutation-proven both ways at this tip, not assumed: restoring the `*.md` walk
reds `test_the_live_registry_round_trips_...` and ERRORS the other four (the
fixture raising instead of skipping is the second half of the repair, driven).
With the fix: **21 passed, 0 skipped**.

**The refusal names the act it observed, not the act it assumed (MINOR 3).**
`lane_approval_refusal`'s snapshot arm read `git diff --name-only`, which lists
DELETIONS beside writes, and rendered every name as `wrote {}`. A branch removing
a stale `docs/archive/last_approved/` file was refused with a record stating it
wrote a file it deleted — a false sentence in the one artifact a human opens to
learn why the merge stopped. It now reads `--name-status` and words each line
from the letter (`_SNAPSHOT_ACT`: wrote / rewrote / deleted, `changed` for an
unrecognised letter, because the file did change and which way is the part this
does not know). A wording correction, so no unrepresentable-form clause is owed.

**Two statements about the mirror, made one (MINOR 5).** `staged_approval_acts`'
docstring claimed to report "exactly the set `staged_spine_amendments` exempts"
and then carved out the de-approval four paragraphs later. An `Approved` →
`Drafted` withdrawal moves `Status`, so the amendment reader exempts it, but it
blesses nothing, so this reader does not report it. The mirror is now stated as
the exempted set MINUS the de-approvals, with where the withdrawal DOES surface
(`staged_drafted_rows`, as the re-approval it owes) named in the same breath —
in the docstring, in `LLR-158`'s `Detail`, and in
`docs/registry-machinery-reference.md`, the three places that quoted it.

**A seam that declared a record never crossing it (MINOR 4).** `IF-091`'s `data`
named "staged_approval_acts records ... (integrate)". Verified rather than
assumed: `grep` over `project-trajectory/scripts` and `scripts` finds
`staged_approval_acts` called nowhere outside `acceptance_record` itself — the
one mention in `integrate.py` is prose in a docstring. The clause is dropped and
the seam names `lane_approval_refusal` alone. The same false claim was in the
reader's own docstring, in BOTH halves ("`intake` reads it off a landed trunk
commit" is false too — intake never calls it), so that sentence is corrected to
what is true: its one consumer is `lane_approval_refusal` directly below it, and
this reader does not itself cross the seam.

### REVIEW-A rework, round 4: the act's scope is a fact the row carries

Round 4's MAJOR was the one round 1 raised and this row's author DEFERRED, with
the deferral written into this fragment as a named follow-on. The reviewer was
right to refuse the deferral twice, and the deferral's own argument was the
tell: it conceded the widening was real and priced the fix at a schema column.
The column is the price.

**The defect, measured rather than argued.** `first_approval_values` re-derives
its population LIVE from `trace.reattest_model` — deliberately, because the row
is claimed long after the merge that minted it and `red_tc_values`' rule is that
a brief describes the world the judge is actually in. But `reattest_model` walks
EVERY SR in the repo, and nothing bounded the re-derivation. Driven here against
this repo with a synthetic row and no merge context at all, it returned 4 SR
chains, 11 `[AWAITING FIRST APPROVAL]` rows, ~40k characters, and a `registries`
slot naming ALL THREE spine registries. The mint that produced the row named ONE
row in its title and `## Context`.

Two harms, and neither is cosmetic:

- The template tells the session "You hold the approval authority for every row
  below marked `[AWAITING FIRST APPROVAL]`". So a merge staging one `Drafted`
  LLR authorised a flip of eleven rows across unrelated workstreams, and moved
  the approval snapshot for all three registries under one WI. That contradicts
  the doctrine this same change wrote into PROCESS_OPTIONS.md — the merge mints
  an adjudication "over the `Drafted` rows the lane handed over" — and the
  owner's own concurrency reason for moving the act to trunk, which is that the
  approval snapshot must not move across a workstream.
- It manufactured owner interrupts. A second merge's adjudication, minted while
  the first was still queued, found nothing left and composed to `(None,
  reason)`, which rule 3 turns into a HELD-for-a-human stop. This repo is live
  for it: `human_approval_through = "DevStg-Needs"` releases all three rungs.

**The fix, and why it costs a schema column.** The scope has to be a fact the
ROW CARRIES. It cannot be re-derived (the derivation is the thing that widened),
it cannot ride the title or `## Context` (prose carrying control flow is the
WI-417 fold this module's own header cites), and it cannot be a frontmatter key
outside the schema (`parse_spec` drops those — the trap `Supersedes`' comment
records). So `Adjudicates` joins `wi_convert.COLUMNS` as a `;`-joined list
column, exactly as `Supersedes` and `Brief` did before it, and for the same
stated reason. `intake._first_approval_drafts` writes the ids it minted over —
NOT truncated the way the advisory `sr_refs` cell is, because a boundary with a
`[:8]` on it silently authorises the ninth row or silently strands it.
`adjudicate_brief.adjudicates(row)` reads it, and the intersection is taken at
the CHAIN ROW in one expression:

    yours = drafted and rid in scope and _loop_approves(root, kind)

Three filters, one label — the live model's answer, the mint's question, the
dial's permission — and `yours` is what mints both the chain label and the
`--approves` registry. The wider population is not filtered out downstream; no
code path turns a repo-wide `Drafted` row into a `yours`, so it is never
constructible. The dial check stays BESIDE the scope check rather than being
replaced by it: the mint filtered by the dial it saw, and a dial the owner
tightens afterwards must bind an act it has not yet authorised.

**Three consequences, each of which needed saying somewhere.**

- `_CHAIN_LABEL`'s two-key table became `_chain_label`, three states. A
  `Drafted` row can fail to be yours because the OWNER holds its rung or because
  it is ANOTHER act's row, and those take opposite actions — wait for a
  signature, versus a sibling adjudication will rule on it. One
  "HELD FOR THE OWNER" line for both would be a true label for the wrong reason,
  which is still rule 2's failure. The template gained the paragraph for the new
  label beside the one it already had.
- The "nothing survives" refusal now names WHICH filter emptied it: ruled on
  already, held by the dial, or a scope naming rows this spine no longer has.
  The repo-wide `if not model` early return was DELETED rather than kept beside
  it — it answered the same question less precisely, and two refusals for one
  state is two answers to one question.
- A row declaring NO scope REFUSES. An empty cell is an unstated boundary, and
  reading it as "everything" is the widening itself, so it fails toward the
  human.

**The column's real cost, paid rather than hidden — and WRITTEN DOWN.** It is a 19th column, so an
adopter carrying the legacy CSV home adds a header cell — `load_csv` refuses a
header that is not the declared schema, by design. `test_dogfood_sync`'s
schema-widening proof covers it automatically (it derives the optional set from
the template), so behaviour-neutrality is measured, not asserted. Five
hand-maintained copies of the header exist; four were pinned to each other and
the fifth, `kitlib.registry.WI_COLUMNS`, was pinned to NOTHING — which is how far
the new cell got before anything noticed it was written by the mint and dropped
by every reader. That pin now exists, and covers the field maps as well as the
column list: a column in both tables but in neither `LIST_FIELDS`/`SPEC_LISTS`
round-trips as an empty cell. `test_wi_loader_sync` gained the third member of
its `bar`/`brief` triplet — and `Adjudicates` is the only `;`-joined cell outside
the two ref columns, so it is what proves a LIST column survives both homes.

`RESYNC_PACK.md` carries the adopter-facing entry, which is a one-cell CSV header
edit and a no-op for the folder home. Writing it surfaced a SEPARATE, older gap,
named there rather than fixed here: `Supersedes` and `Brief` added columns to the
same schema and neither got an entry, so an adopter still on the legacy CSV has
been three cells behind rather than one. The new entry says so and tells them to
add all three.

**Tests**: three at the brief (the widening regression, the no-scope refusal, the
settled-scope refusal naming its rows), one at the mint, one at the loader
triplet, and the widened schema pin. The widening regression is mutation-proven
— dropping `rid in scope` reds it and the settled-scope refusal both.

**Driven at this tip against this repo, not only against a fixture.** The
review's own probe — a `first-approval` row with no merge context — now REFUSES
by naming the missing cell. Given a scope of one real row (`LLR-206`, one of the
eleven `Drafted` rows this repo currently carries across four SR chains), the
brief renders **1 chain, 1 `[AWAITING FIRST APPROVAL]` row, 3 siblings labelled
OUTSIDE THIS ACT'S SCOPE, 9,541 chars, and one registry** — against the
pre-fix reading of 4 chains, 11 rows, 40,658 chars and all three registries.
The act reaches what the merge handed it and nothing else.

`intake.py` 1247 -> 1249, re-stamped with its reason: two lines, the `_draft_row`
assignment and the mint's `adjudicates` key.

Registry rows this round moved, re-pointed in lane: `IF-092`'s `data` (18 -> 19
columns), and `LLR-136` (`Approved`, amended not flipped, like `LLR-158`) which
now records that `read_specs` takes its population from the read side's
`spec_paths` and that `COLUMNS` is pinned to its read-side twin.

### The harness at the round-4 tip

- Smoke tier: **1461 passed, 4 skipped in 20.99 s** — GREEN, where the tip this
  round inherited was `1 failed, 1455 passed`. The budget enforcer reads
  **23.3 s against the 60 s ceiling**.
  <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=HEAD -->
  <!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=HEAD -->
- The four previously-dark `test_wi_convert.py` guards run and pass: **21
  passed, 0 skipped**.
- Byte-watched: `PROCESS_OPTIONS.md` 185,060 -> 185,555 (+495, mechanism 2's
  scope sentence), and byte-budget-guard's own row re-stamped and re-trimmed to
  **4,982 against its 5,000 cap** — the first draft of that row put the file at
  5,142, over cap, which is exactly what the guard exists to catch.
