# The monotonic product-regression floor (WI-473, repo review 2026-08-19 C-01)

**Status:** design taken and built for the derived half; the SPINE amendment it
implies is owed to the owner (`OI-51`). **Branch:**
`requirements/ears-and-quality-characteristics`. **Row:** `WI-473`
(`buildtier = strong`, `safety_class = spine`).

This is the written design the WI's Context asks for — what the floor holds, how
it ratchets, and how a deliberate lowering is sanctioned — recorded before the
build so the reasoning outlives the diff.

---

## 1. The defect, re-measured rather than inherited

C-01 as written says a draft row "removes all product-code checks from both push
and PR plans". Measured against this tree, that is **half right, and the half it
misses changes the fix**:

| what the review said | what the code does |
|---|---|
| one draft drops the derived bar | true — `docs/gate`'s value is a MIN over every in-scope row, and a `Drafted` row reads below the lowest bar |
| product checks stop gating | **true** — `format`/`lint`/`tests+coverage` are tagged `{BAR_RELEASE}` only (`check.py`), and `plan = [s for s in all_for_gate if gate in s[3]]` drops them |
| product checks stop running | **only for `tests+coverage`** — `advisory_plan` already re-runs higher-bar steps WARN-ONLY while `window_open()` is true, and `ADVISORY_EXCLUDE` holds `tests+coverage` and `module-coverage` out of that tier |

Probed, not assumed: with a synthetic mature basis line
(`drafted=1 computed=DevStg-Below ex-draft=DevStg-Impl`) `window_open()` is
`True`, and the `DevStg-Reqs` plan contains **zero product-layer steps** while
`DevStg-Impl`'s contains `format`, `lint`, `tests+coverage`.

So the honest statement of the defect is: **`format` and `lint` degrade from
gating to advisory, and `tests+coverage` stops running altogether** — in a
downstream repo whose CI runs `check.py` at the derived bar. Either way the exit
code stops reflecting the product's health, which is the silent green SN-008
exists to forbid; but the fix is "promote what already runs", not "schedule
something that does not".

### 1a. And the binding constraint is not the one C-01 names

Measured while building the floor, and it changes what this row can honestly
claim. **`DevStg-Impl` is unreachable from the derived selector at all.**
`derive_gate.sr_bar` is ceilinged at `BAR_TESTS` by owner ruling OI-30 D2 —
"`DevStg-Impl` is UNREACHABLE FROM A STATUS CELL until a harness driver computes
the release bar from test evidence" — and `ex-draft` is a MIN that includes
`sr_bar`, so neither the bar nor the floor can ever exceed `DevStg-Tests` while
any real SR exists. The three built-in product steps are tagged `{DevStg-Impl}`
only.

Therefore, for `format`/`lint`/`tests+coverage`: **a draft row is not what stops
them. They already never run on any adopter's push or pull request**, draft or no
draft — only the tag path forces `--gate all` (`ci/check.yml:89`). C-01's stated
mechanism is real but it is not the binding one for the three checks the finding
is actually about.

That is a refutation of the finding's framing, not of the finding. The silent
green is worse than reported, and the floor is a necessary but *insufficient*
part of the remedy: it is the mechanism that makes the product checks survive a
draft, and something still has to make them reachable in the first place. Which
bar they belong at is `OI-51`, deferred with a recommendation rather than
guessed — a builder re-tagging three steps would be overturning an owner ruling's
own enumeration by side effect.

That distinction matters for a second reason. The advisory tier is the 2026-07-27
owner ruling's answer to *this same shape of problem* — a window must be a lower
bar, not a blind spot. The floor is not a rival mechanism; it is that ruling
carried the last step for the checks whose failure is a REGRESSION rather than an
immaturity.

## 2. What the floor holds — the two axes, made concrete

The review's framing, adopted: **artifact maturity and product regression are two
different questions wearing one number.**

- **Artifact-maturity checks** (`traceability`, `trajectory`, `need-form`,
  `design-flows`, the freshness gates …) answer *"is the spine mature enough for
  this bar?"*. A new draft genuinely lowers that answer, and lowering it is the
  signal a new phase is due. These stay selected by the derived bar, unchanged.
- **Product-regression checks** answer *"does the code that already exists still
  build, lint, and pass its tests?"*. Drafting a requirement says nothing about
  that. These get a floor.

**The floor's membership rule is the `product` LAYER — the whole selector, and
nothing else.** `check.py` already tags every step `process` or `product`, and
the tag already carries exactly the right meaning: a product step's command is
the one **the repo wrote down in `docs/stack.ini`** (`[product] format/lint/test`
plus each `[step:*]` declaring `layer = product`). Declaring it IS the repo
saying it wants that tool run — the `missing_tool_banner` selector rests on the
same reading, so the floor inherits a distinction the kit has already argued and
adds no second vocabulary. An adopter who adds `[step:secrets]` or
`[step:build]` at `layer = product` gets it in the floor for free, which is the
review's "secrets and build" ask satisfied by the existing extension point rather
than by a hard-coded name list.

## 3. How it ratchets — `ex-draft`, not a stored high-water mark

The floor is `max(derived bar, ex-draft)`, where `ex-draft` is the value already
on `docs/gate`'s `# basis:` line: **the same MIN arithmetic run over the spine
with the pending rows removed** — "what would the bar be if nothing were
pending?".

Three reasons this beats persisting a high-water mark:

1. **The kit has already ruled this axis, in the opposite direction of new
   state.** `derive_gate.compute` says so where `ex_draft` is computed:
   excluding the drafts recovers a mature spine's maturity *"WITHOUT history or a
   stored high-water: the rows the draft did not touch are still standing right
   here"* (WI-341). A stored mark would be a second, weaker answer to a question
   the derivation already answers from evidence in the tree.
2. **It cannot be gamed by deletion.** A high-water file is a thing to delete; a
   derived value is recomputed from the rows every run, and `derive_gate --check`
   already guards the cache against rot at every bar.
3. **`check.py` can already read it.** `_EX_DRAFT_RE` and `window_open()` parse
   this exact field today. The floor is a few lines beside a mechanism that
   already exists, not a new subsystem — which is the conservative-edit bar this
   repo holds itself to.

**Monotonicity, stated precisely rather than claimed loosely.** The floor is
monotonic against the act C-01 names — **drafting can never lower it**, because
drafts are exactly what `ex-draft` removes. It is NOT a universal high-water
mark, and pretending otherwise would be the signed-claim failure this repo keeps
catching. Two acts can still lower it:

- **demoting or deleting a ratified row** (an approval reversal), and
- **approving a new, less mature row** — e.g. an SR approved before its LLR/TC
  exist lowers the MIN over the non-draft subset.

Both are **reviewed spine acts in a human-held tier**, visible as a changed
`ex-draft=` on the basis line and therefore in the diff of a tracked, derived
file. That is the sanction, and it is the same one every other gate movement
already has: *the floor falls only where a human approved the act that lowered
it, and the record of the lowering is the commit that did it.* No new
re-stamp file, no new escape hatch.

The second case is the residual, and it is real: a mature repo that approves
"SR for feature 2" ahead of its decomposition drops `ex-draft` and with it the
floor. Whether that is acceptable (it is a reviewed act, and arguably approving
an undecomposed SR SHOULD be visible) or whether the floor must be a true
watermark is the one genuine policy question here, and it is `OI-51`'s, with
option (b) recorded as the strict-monotonic alternative.

**Rejected: inferring the floor from "configured product commands".** The
review's other suggestion cannot ship default-on. The kit's `BUILTIN_PRODUCT`
defaults mean *every* scaffold has configured commands from minute one, so the
floor would fire on a fresh repo with no source and no tests — `pytest` on an
empty tree exits 5, and every new adopter's first CI run would red. Presence of a
command is a statement of intent, not evidence of a cleared bar.

## 4. What a downstream green MEANS after this — the migration, stated

Exactly one class of repository changes behaviour: **one whose ratified spine
stands at a product bar its derived bar has fallen below.** That is the C-01 case
and only the C-01 case.

- A repo that never reached the floor's bar: no product step joins the floor,
  **zero change**.
- A repo steadily AT its ratified bar: the derived bar already selects them,
  **zero change**.
- A mature repo with a draft open: its **declared** product steps
  (`[step:*] layer = product`) at or below `DevStg-Tests` stay gating instead of
  falling to advisory.
- The three BUILT-IN product steps: **no change today** — §1a, they are tagged
  at a bar nothing can derive. The floor covers them the moment `OI-51` is ruled
  and they become reachable, and `tests/test_product_floor.py` fails loudly on
  that day so the arming is an act rather than a drift.

So the migration an adopter feels is *"CI now fails on the lint and test
failures it was previously hiding"*. Per the standing rule — never sanction a
check to green a step — that is the correct direction and is not softened with an
opt-out dial. A `product_floor = off` knob would be a sanctioned check by
another name; it is deliberately not built. The change is recorded in
`RESYNC_PACK.md` §3 so an adopter meets it at re-sync rather than in a red build.

**The cost objection, answered where it was raised.** `ADVISORY_EXCLUDE`'s
comment argues `tests+coverage` is too expensive to run warn-only for the life of
a window. That argument holds for the ADVISORY tier and is left standing; it does
not reach the floor, because a repo over the floor was running the suite at every
gate run *before the draft landed*. The floor restores the pre-draft cost, it does
not add a new one — and the exclusion stays in place, so no step runs twice.

## 5. What this session built, and what it did not

**Built:** `check.py:product_floor()` + the selector change, the `--list` and
summary disclosure of the floor, the shipped CI regression fixture the review
specifies, and the correction to `.github/workflows/test.yml`'s
enforcement claim.

**Deliberately NOT done — the spine amendment, deferred to the owner (`OI-51`).**
`SR-006` is the requirement home ("shall run the required steps of **the gate
that must next be passed**") and `LLR-060` its design row; both are **Approved**,
and the floor makes `SR-006`'s shall incomplete rather than wrong. Amending an
Approved cell overrides attestation, which is the sitting's act, not a builder's
— the precedent is `SR-158`'s own rationale leaving `LLR-014`/`TC-014` re-points
owed for exactly this reason. `OI-51` carries the proposed clause text so the
ruling is a read-and-sign rather than a re-derivation. Until it is taken, the
built behaviour is ahead of its requirement, and that gap is stated here rather
than papered over.
