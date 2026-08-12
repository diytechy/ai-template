# The lock program — what is still owed

**What this file is.** The one place scope and rulings accumulate until the
repository is **locked** — every requirement ratified or rejected, every window
closed, the derived gate back at its honest ceiling, and nothing owed to a
sitting. It is *living*: entries are appended and amended in place as decisions
land, and it is deleted (or archived) when §5's checklist is empty.

**What it is not.** Not a working surface and not a second source of truth. The
working surfaces stay [`status.md`](status.md), the registries, and
[`log.md`](log.md); the narrative record of *what happened* stays the log.

**How a decision enters.** Owner rules it → recorded here with its rationale and
its consequence inventory → executed → the row/log carries it → **the entry here
collapses to a one-line pointer with the commit.**

> **Compacted 2026-08-11.** That last step had never been performed, and the
> file had grown to 2,343 lines — most of it reasoning behind decisions already
> executed, which is precisely what drowns a "what's next" surface. The full
> record of every **executed** decision, the F-1…F-12 reference findings, and
> this document's own log now live in
> [`archive/repo-lock-decisions-2026-08.md`](archive/repo-lock-decisions-2026-08.md).
> **Every `D-n` heading and every `§N` number survives here as a resolvable
> pointer** — **33 live source and test files** cite them in prose
> (`repo-lock D-5`, `repo-lock §5's`) where nothing link-checks them, so the
> ids must keep resolving. What remains below is what is still owed.

---

## WHAT IS LEFT — the whole list

Listed in the order they unblock each other, top to bottom. **Deliberately
un-numbered:** this file already carries two numbering systems — the `§N`
sections, and §5's checklist steps 6–12 — and a third would invite reading
"item 7" as "§7". The arrow on each line is the only pointer that means
anything.

**Owner acts — everything below them waits on one of these:**

- **Rule the component model's PARTITION** — the *direction* landed 2026-08-12
  (§8.6): components define the boundaries SRs are written against; interfaces
  carry interfaces only (each signal typed discrete vs variable). Still owed:
  the actual partition and the IF schema rewrite, ruled *with* OI-14. → **§0**,
  **§8.6**
- **Rule OI-14** (what an IF row's `Contract` cell is for) — it inherits an
  11-row citation sweep and decides when `interfaces.csv` may convert. The
  2026-08-12 direction (interfaces-only) narrows it but does not close it.
  → **§0**
- **Hold the P0 sitting, part 2** — the 25-row re-attest brief, worked
  *together with* the prose batch so two re-blessing windows collapse into one.
  Gates the entire schema batch via Q11. → **§5 step 6**, **§8.4**
- **Ratify ONE remaining agent decision** — WI-429's LLR discharge rule
  (`CodeSymbol` must resolve), taken under a "proceed" and now gating hard
  under `--strict`. The other three are settled: WI-423 **overturned** and
  re-executed, the `key = ""` refusal **ratified**, the blackout dial
  **ruled**. → **§8.5**
- **Review the agent decisions taken executing the 2026-08-12 rulings** —
  recorded as they were made. → **§8.7**

**Ruled 2026-08-12 (this sitting), now mechanical:**

- ~~**Rule the stage/gate semantics**~~ — **RULED: gate-as-state is retired
  for stage semantics** per the
  [proposal](plans/2026-08-11-stage-gate-semantics.md); the heavy rework is
  accepted. Execution is underway this session. → **§0**, **§8.6**
- ~~**Rule the six SN-tier intake items**~~ — **RULED: all six hold**, with
  item 2 (and its launcher siblings) relaxed to double-clickable *where the
  platform allows* (Linux needs the execute bit). They enter as Draft rows
  together with the 2026-08-12 additions; attestation stays the sitting's.
  → **§8.3**, **§8.6**

**Mechanical work:**

- **Build the schema batch ONCE** — D-1's anchor half, D-2's SN fields, D-3's
  remaining columns, D-4's `SupersededBy` deletion, **D-9's ladder migration**
  (closing the `Status` enum *first*), and **D-10's approval-log writer**.
  **Includes the one hole D-9 left: nothing drives G2→G3 once `Verified` is
  gone** — the fix is to read the harness rather than a cell, see D-9's
  correction note. Blocked on the sitting. → **§5 step 7**
- **Repoint the `derived-gate-model.md` citations** — 23 across 18 files, of
  which **14 are live** (8 kit source, 5 tests, 1 shipped doc). Unblocked
  today; `SR-049` is fenced out of it as a spine amendment.
  → **§5 loose ends**
- **Finish batch-2** — `interfaces.csv` (after OI-14) and `components.csv`
  (after the component model). `open-items` and `agents` are done. → **§8.1**
- **Close WI-390** — the concurrency-v2 program close; it carries spine
  amendments, so it belongs with the sitting. The last open work item.
  → **§5 step 9**
- **Regenerate, and confirm the gate rises** to its honest ceiling. A gate that
  does *not* rise is a finding. → **§5 step 8**
- **Dispose the warn-only residue**, then re-run the full bar and merge.
  → **§5 steps 10–12**

**Not blocking, but owed to nobody and therefore easy to lose:** the loose ends
in **§5** — `intake.py`'s monolith, the traced/ratified split `trace.py` cannot
see (this one bites *at* the sitting), the un-reusable policy-scaffold census,
and the four unfounded LLRs.

---

## 0. Start here — TWO rulings owed

| # | question | where | recommendation |
|---|---|---|---|
| **components** | The **component model**. `LLR.Component` is *traced*, so the partition moves with no re-attest window — and it **decides how many IF rows must exist**. **Direction received 2026-08-12** (§8.6): boundaries define SR I/O; the partition itself is still owed. | §6 F-11 (archived) · §8.6 | work the partition as an *optimization over system I/O* (§8.6 item 1), present it; the ruling stays the owner's |
| **OI-14** | What an IF row's **`Contract` cell is for**. Measured: design narrative and history, 1% requirement voice, and the registry has **no schema tier at all**. **It inherits a sweep** — see below. **Narrowed 2026-08-12**: interfaces carry *interfaces only*, signals typed discrete vs variable. | §6 F-10 (archived) · §8.6 | **declare now, split gradually** — never a 95-row sweep |

> **OI-14 has grown a second half, and it is the same finding twice.** F-10
> measured `Contract` cells carrying design narrative and defect history rather
> than contract, and noted the cost is not cosmetic: `plan_briefs`'
> `IF_SURFACE_COLUMNS` feeds `Contract` **verbatim into LLM planning briefs**,
> so history spends brief budget without constraining behaviour. **That pattern
> then grew back** — 11 of 110 IF rows now cite `repo-lock D-n` in
> `Contract`/`Notes`, most of it added by this program. The owner ruled the
> general case on 2026-08-11: *"if someone wants to know the history and the
> rationale, they should look in the archive"* — state the constraint, cite a
> decision only where a reader could plausibly undo it, at most once per
> module. The kit-source sweep executes now under its own WI; **the 11 IF rows
> are deliberately NOT swept**, because OI-14 is going to rewrite what a
> `Contract` cell may contain and sweeping first means sweeping twice.

**Read them in that order:** OI-14 assumes today's IF rows are the right ones,
and that rests on the unruled component model. §8.3 item 6 (SRs written against
component-boundary interfaces) lands on the same question and should be ruled
with it.

**Ruled and closed since:** ~~OI-12~~ (one TOML carrier — **D-5**, executed),
~~OI-13~~ (what `Status` means — **D-9**, ruled 2026-08-11; migration owed).

**The stage/gate semantics are RULED — 2026-08-12, this file's third §0
question closed.** The owner: *"gate semantics should be retired / archived
for stage semantics even though it will result in some relatively heavy
rework."* That adopts
[`plans/2026-08-11-stage-gate-semantics.md`](plans/2026-08-11-stage-gate-semantics.md):
**stages are the tiers of the decomposition; gates are the subset of
boundaries that require a human to certify** — stage is the *state*, a gate is
an *event you pass*, `G0` is retired (it was "stage 0" in the wrong units),
the missing **implementation rung** is added, and the phrase "the active gate"
leaves the vocabulary. Execution started 2026-08-12 (§8.7 records the
judgment calls the rework forced). **The two questions the ruling needed
settled with it, both measured 2026-08-11 — resolved as follows, recorded for
review (§8.7):**

- **WHERE the semantics live — the evidence says `PROCESS.md`, not
  `PROCESS_OPTIONS.md`.** The options file's own header states *"Nothing here
  is required for the minimum profile"*, yet its table lists **`Derived gate
  model | always, once you use gates`** — an always-on layer in a file of
  opt-in layers. (`Proportionality doctrine` is marked "always" too, so this is
  a pattern.) The stage axis is the stronger case: there is no applies-when
  under which a project has a spine but no stage, and it drives the human-stop
  decision. Sizes for the trade: `PROCESS.md` 64,466 bytes ·
  `PROCESS_OPTIONS.md` 170,459; the guard enforces a hard 10,000 only on
  `AGENTS.template.md` and *watches* these two, so moving the summary between
  them is roughly budget-neutral across the pair.
- **The authority is reachable — my earlier "restore it" was WRONG.**
  `docs/specs/derived-gate-model.md` was a **design spec** (spec-of-record for
  WI-089…096, WI-116, WI-117), archived **correctly** by the WI-251
  spec-lifecycle sweep under rule R-F to
  [`archive/specs/derived-gate-model.2026-07-20.md`](archive/specs/derived-gate-model.2026-07-20.md).
  Nothing is lost. What was never done is repointing the citations — see §5's
  loose ends. Note `PROCESS_OPTIONS.md` calls its own section *"the working
  summary"* and defers to the spec for *"full design + rationale"*, so ruling
  into the options file would mean **promoting the summary to the authority**
  and dropping that deference clause, not just editing a paragraph.

> **Resolutions taken with the 2026-08-12 ruling (agent judgment, owed
> review — §8.7):** the semantics' home is **`PROCESS.md`** (the owner adopted
> the proposal without naming a home; the evidence above all points one way,
> and the stage axis is always-on, which is disqualifying for a file of opt-in
> layers). The 13 live source/test citations repoint to the **archived spec**
> (its §-numbers are what they cite; `PROCESS.md` carries the ruled semantics,
> not the gate-arithmetic detail). `PROCESS_OPTIONS.md`'s summary keeps only
> the opt-in material and defers to `PROCESS.md`.

**Also owed by the owner, and larger than a ruling:** the **P0 sitting's part
2** — the 25-row re-attest brief (§5 step 6). It gates the ladder migration
(Q11), the anchor half, and the schema batch. Everything mechanizable is now
done; the sitting is the critical path.

**Two things need the owner's eye that are not on the ruling list:** the
**edge-case SN tier may be mis-levelled** (measured: **seven** of ten rows
decompose into exactly one SR against 12.6 for a core need, and SN-019/SN-020
share the *same* single SR-028) — a **kit-level** finding, since that table
ships to every adopter, and one the 2026-08-10 sitting already set precedent
for by demoting three needs on this exact test. And the tabled items in
**§8.4** and **§8.5**.

---

## 1. Where the repo stands

Measured 2026-08-12 at `982109b3` on `infra/mechanized-loop`, after 70 commits.

| fact | value |
|---|---|
| derived gate | **G1** — `computed=G0` floored to G1, because drafts exist. Correct: everything that moves it now waits on the owner. |
| spine | SN 29 · SR 146 · LLR 149 · TC 146 · **37 drafts** · **38 `Modified`** |
| integrity | `orphans=0 integrity=0 component-findings=0 interface-findings=0`; interfaces 113 |
| strict modes | `trace --strict` **rc 0** · `check_trajectory --strict` **rc 0** |
| full bar | **2291 passed, 5 skipped** |
| owner surface | **4 rulings** (components · OI-14 · stage/gate · the SN batch) + **1 ratification** (WI-429) + the sitting's 25-row re-attest brief |

**Predecessor records**, kept reachable because they are the account of the
program *before* this one and are not superseded by it:
[`handoff-2026-08-08-mechanized-loop.md`](handoff-2026-08-08-mechanized-loop.md)
and its build-out plan
[`spine-restructure-2026-08-08.md`](spine-restructure-2026-08-08.md) — how the
five needs the sitting has now ruled on were decomposed in the first place.
Both are **history**: they keep their `SN-030`/`SN-031`/`SN-032` citations after
those ids were retired, on the doctrine `check_doc_refs` applies to retired
files (naming one is accurate history; "fixing" it falsifies the record).

**The gate has not moved and should not have.** One SN was attested and three
demoted at the sitting's part 1, but every SR/LLR/TC under them is still
`Draft`, and a `Draft` row reads G0. Worth knowing: a `[phase]-[g*]` detector
fires on phase 4 — per the derived-gate model that **is** the signal a new
phase is due, not a regression.

---

## 2. Decisions — pointers, and the ones still owed

Full reasoning for every executed decision:
[`archive/repo-lock-decisions-2026-08.md`](archive/repo-lock-decisions-2026-08.md).

### D-1 — the attestation anchor moves ONTO the spine row; `attestations.csv` is retired

**Ruled 2026-08-09.** `HashedOn` and `TextHash` become fields on the artifact's
own row; the separate ledger is retired. `HashedOn` is the **reviewable**
anchor, `TextHash` the **git-independent tripwire** that survives squash,
rebase and shallow clone. Replacement guard is **co-mutation**, not
equivalence — weaker than append-only and must be described that way.

**Removal half: DONE.** Warning for a dead-symbol sweep: `normative_text`,
`sn_normative_text`, `digest`, `current_digests`, `_DIGEST_SEP` and
`_DIGEST_EXCLUDED` survive as the anchor's engine **with no writer yet** — they
are not unused. (WI-429's sweep already honoured this.)

**ANCHOR HALF — STILL OWED, and it is §5 step 7's core:**

1. the two cells on the spine rows, and on SNs (D-2);
2. both cells into **`_DIGEST_EXCLUDED`** — otherwise the digest is
   **self-referential** and every stamped row reads as drifted, permanently,
   from the first stamp;
3. a **third cell class** — an anchor cell is neither `ratified` prose nor a
   `traced` pointer, and `spine_cell_class`'s residual fails safe by reading an
   unclassified column as *ratified*, which would arm hazard 2;
4. the **co-mutation guard** (a commit writing `TextHash` writes the digest of
   that row's text as it stands in that same commit, and sets `HashedOn` to
   itself);
5. the template columns — a fresh scaffold without them has a **vacuous
   check**, the exact "green hides a skipped check" SN-008 forbids;
6. **Q3, still open and build-time:** how far back the co-mutation guard
   compares. Until decided, its docstring must say it is partial.

### D-2 — stakeholder needs gain FIELDS rather than a new carrier

**Ruled 2026-08-09**, and **largely dissolved by D-5**: under TOML an SN is an
element with keys, so "where do the fields go" has no referent. **Owed with the
anchor half:** the SN anchor fields, and the column-count truncation in
`sn_normative_text` so the anchor is not hashed into its own digest.

### D-3 — a column name means ONE thing repo-wide

**Ruled 2026-08-09.** Where two registries carry the same name they carry the
same meaning; where they need different meanings they need different names.

**Its `Status` half is SUPERSEDED by D-9.** What remains unmigrated:

- **`Phase`** — add to SN as the same mechanical integer the spine uses
  (option (a); the ruling's *intent* is satisfied without disturbing the gate).
  It is **not** advisory today: `derive_gate` and `trace` parse it, `trace`
  filters the SR set by it, and the release checklist groups on it.
- **`Priority`** — a float, higher = first, relative **within a registry**.
  Free on SR (146 rows, value inert); **load-bearing on WI**, where
  `schedule.py` sorts the dispatch frontier on it — so `_int` must become a
  float parse or `1.5` silently truncates to `1`.
- **`Evidence` keeps its name** (rescinded rename) = *where the proof lives*, a
  **traced** cell. **`Method`** = *how you obtain it*, a **ratified** cell. The
  split stays: moving the pointer into `Method` would turn every test-file
  rename into a re-attestation — 110 of them for WI-277 alone.
- **`Rationale` becomes available to IF**, which is the mechanical destination
  OI-14's split needs.
- **The vocabulary-as-interface question stays deferred** by the same ruling —
  the IF registry has no shape for a data vocabulary.

### D-4 — supersession is DELETION, and ids are never reused

**Ruled 2026-08-09.** A superseded row is deleted; history lives in git and the
log. The id-reuse hazard is real and was worse than it looked — every mint
derived its high-water mark from what currently exists.

**DONE:** the id watermark (14 spaces, three rules in the always-on integrity
floor) — and **repaired 2026-08-11**, when a cross-family review found
`live_max_ids` never learned the TOML carrier, leaving "no live id exceeds its
mark" **vacuous on three of four spine tiers** with LLR-167/TC-161 already
above their marks. `plan_artifacts`' two mints still derived from
`max(live)+1`; literal reuse was reproduced, then eliminated. **First real
supersession executed** (WI-426).

**STILL OWED — the `SupersededBy` column deletion**, with its ~80-line
validator in `trace.py` (semicolon-list shape, no repeats, target exists, no
self-link, no cycles), the `PartOf`/`SupersededBy` rule, and its `ratified`
classification in `check_trajectory`. A registry-schema change → §5 step 7.

### D-5 — ONE TOML CARRIER for all four tiers

**Ruled 2026-08-10, EXECUTED 2026-08-11** (`bb69a622` · `f7be75af`, plus
`49ab1c1c` closing an adversarial review's 3 BLOCKERs / 4 MAJORs on the forward
path). All four tiers on TOML, sources deleted, the 38 `Modified` rows intact,
the re-attest brief regenerating byte-identical across the carrier change. Ten
fail-open readers were found and fixed in the landing; the cutover is the
detector, which is why it is run rather than reasoned about.

**Live residue:** the **CSV fallback is deliberate dead weight with an
expiry** — drop it once no supported baseline predates the cutover; both
ratchet entries say so.

### D-6 — the spine carrier gets ONE home; F5 is AMENDED, not ignored

**Ruled 2026-08-10, EXECUTED.** `spine_carrier.py` is a declared sibling.
F5 buys cross-script copy-ability for small stable **plumbing**; it does not
cover a shared **vocabulary**, whose divergence is silent content loss.
"Independently copyable" becomes "copyable with its **declared siblings**" —
writing down an exception the kit already practised.

### D-7 — the duplication census is TORN DOWN; `test_rule_sync` is the anti-drift tool of record

**Ruled 2026-08-10, EXECUTED as WI-426.** One real catch at the one-time
triage, zero since, structurally blind to both real drift incidents this repo
suffered. **Live consequence:** F5 duplication is unbounded again, and new
duplication of **policy** requires a behavioral pin in `test_rule_sync`;
plumbing duplication is accepted unbounded.

### D-9 — the `Status` ladder is THREE rungs: `Drafted` → `Approved` → `Founded`

**Owner ruling, 2026-08-11**, closing **OI-13** and superseding D-3's four-rung
table. Settled over four candidate vocabularies; the owner's closing note is
part of the ruling: *"semantics can be modified moving forward."*

| value | means | set by |
|---|---|---|
| **`Drafted`** | the id is allocated, and **nothing else about the row may be validated against it** | authored |
| **`Approved`** | **a judgement was made** — the row's text is blessed | authored; the ladder's only human judgment |
| **`Founded`** | the artifacts this row calls for **exist**: SRs under an SN, LLR+TC under an SR, resolving code under an LLR, a written test under a TC | **computed** |

**Uniform across SN · SR · LLR · TC.** No per-tier overload — that uniformity
is what three rejected candidates failed to give.

**`Approved` is defined generally, not as a spine value:** *"it just means a
judgement was made, that can apply to other interfaces so long as the meaning
is coherent."* That makes the review verdict `APPROVE` and a row's `Approved`
the same concept at two scopes rather than a collision, and gives `IF`/`OI` a
legitimate target instead of a rename.

**THE PASS RUNG IS DELETED, not renamed.** D-3 had a fourth rung (`Verified` =
the test passes, TC only) and §0 carried a standing recommendation to spend a
fresh word on it. The owner asked the better question — *"Can't that be derived
from running the tests?"* — and it can: pass/fail is a live fact CI answers on
every push, so a cell is a stale duplicate. Deleting it makes the ladder
uniform, and **dissolves the word-reuse hazard rather than working around it** —
`Verified` is not re-pointed, it ceases to exist.

> **CORRECTION, 2026-08-11 — this paragraph originally said `derive_gate`'s G3
> rung ("decomposed AND `Status=Verified`") "becomes simply at `Founded`".
> That is WRONG, and the owner's question found it.** `Founded` **is** the old
> G2 condition (decomposed — its LLR and TC exist), so mapping G3 onto it
> collapses G2 into G3 and would declare implementation complete the moment the
> tests are *written*. **Under D-9, nothing currently drives G2→G3.**
>
> The deeper finding is that today's rung was never sound either. `sr_gate`
> reads `decomposed and is_verified(sr)` — a **hand-set cell asserting the
> tests pass**, which is precisely the authored pass/fail claim **Q11 forbids**.
> The tension predates D-9; deleting the pass rung exposed it rather than
> causing it.
>
> **The fix is where `PROCESS.md` already puts it: the HARNESS is the signal** —
> G3's bar is *"passes the full harness: format/lint, full test tier, coverage
> ≥ threshold … no stubs."* `derive_gate` never read it; it read a cell that
> claimed it. So the G2→G3 driver must become a harness result, not a status
> value — which also makes the proposed **stage 4 → 5** boundary
> (implementation → release candidate) harness-driven, consistently with the
> rest of the ladder. **Owed with the step-7 batch**; it is the one piece of
> D-9 whose consequence inventory was incomplete.

**The `GreenOn` idea — right shape, deferred with a trigger.** Recording the
commit a row was last green at is the anchor pattern and is sound; built
*today* it would copy one repo-wide fact onto 146 rows, because per-row
demonstration needs per-test granularity and **R2** declined that. Build it
when the suite is too expensive to run on every push, or when the `::node`
selector resolves.

**Words rejected**, so none is re-proposed: `Ready` (ambiguous) · `Verified`
(re-points a word 370 rows carry, and is the only value silent on a
half-migration) · `Attested` (collides with `Attest`, a live `Verification`
method) · `Granulated` (no home; does not fit a TC) · `Distilled` (points the
wrong way — distillation concentrates, this rung expands; and the repo already
spends the word six times meaning compress-to-essence) · `Grounded`
(**proposed by me twice and withdrawn** — "re-ground" points UP the chain) ·
`Decomposed` (the runner-up; passed over for the TC fit, and because naming the
*state* distinctly from the *motion* is cleaner).

#### Consequence inventory — none optional

1. **`Draft`, `Verified` and `Modified` all leave the vocabulary.** Drift
   becomes a **derived overlay**, not a value — `Approved (drifted)` preserves
   which rung a row fell from. Therefore **a row at `Approved` or above
   carrying no hash is an ERROR**, or drift detection is vacuous exactly where
   it matters.
2. **`Founded` is computed and must never be hand-authored.** Open: does a tool
   **write** it into the cell (anchor-cell precedent) or is it layered at read
   time? That decides what a human sees in the file — and whether an *authored*
   `Founded` should itself be an error.
3. **The SN tier's `kind` sheds `draft`** (18 core · 10 edge · 1 draft today),
   leaving `kind` holding only the tier distinction. One fact, one home.
4. **The three F5-duplicated predicates change together** — `is_draft` /
   `is_verified` / `is_modified` across `trace_text` · `trace` · `derive_gate`,
   pinned by `test_rule_sync`. That pin is the migration's safety rail; it must
   also assert that **no predicate still honours a retired word**.
5. **The other carriers:** `IF`'s `Status` overlaps its own `Stability` column
   (`Stable` live in both, meaning different things) — lands with **OI-14**.
   `OI`'s is a workflow state. `CMP`'s `State` is already distinct and
   compliant. **`WI` state is the directory** and a work item is not a
   requirement — the ladder does not apply.
6. **Migration mapping:** `Draft`→`Drafted`, `Verified`→`Approved`,
   `Modified`→resolved at the sitting→`Approved`, then promoted to `Founded`
   where the discharge computes. **470 rows.**
7. **THE SAFETY PROPERTY IS NOT FREE — `Status` is open-vocabulary, checked
   NOWHERE.** Measured: `ENUM_FIELDS` covers only `SR.Verification` and
   `TC.Tier`; a row with `Status = "Bananas"` yields **no finding** and all
   three predicates **False**. So "a stray `Verified` is unambiguously an
   un-migrated row" has no enforcer, and the failure directions are asymmetric:
   a half-migrated `Approved`/`Verified` reads loudly (gate drops, orphans
   appear), but an unmigrated **`Modified`** read by a new drift predicate
   returns False and **silently vanishes from the re-attest brief** — the exact
   laundering Q11 exists to prevent. **The migration's first act is to close
   the vocabulary.** Full checklist:
   [`plans/2026-08-11-status-ladder-migration.md`](plans/2026-08-11-status-ladder-migration.md)
   (measured blast radius: 8 literal sites in scripts, 96 in tests, 8 shipped
   docs).

#### `Founded`'s discharge test, per tier

Three already existed; the fourth was built.

- **SN** → `derive_gate`'s coverage rung, counted as `uncovered=N`.
- **SR** → `derive_gate`'s existing G2 decomposition test.
- **TC** → the file-existence half of the `Evidence` check (sufficient under R2).
- **LLR** → **BUILT as WI-429**, taken under the owner's *"proceed"*;
  **ratification owed with the ladder migration.** `CodeSymbol`/`Module`
  resolving is the discharge, giving `CodeSymbol` its first real job after a
  lifetime as F-3's "required, never resolved". The census found the predicted
  rot: of 149 rows **31 carried a non-binding token and 9 bound nothing**, the
  cell having no enforced grammar (function locals, instance attributes, CSS
  properties and prose alongside real symbols). 14 rows repaired where the
  symbol had exactly one home; **4 left unfounded with reasons rather than
  guessed** — under D-9 those are simply LLRs that are not `Founded`, which is
  the computation working. The rule is deliberately **coarse** (≥1 token binds)
  because per-token would red 31/149 on arrival; per-token misses are counted
  *untraced* so tightening stays available. **Hard under `--strict`**, argued
  from D-9: an advisory would make `Founded` vacuous for one of four tiers.

### D-10 — approval provenance is an APPEND-ONLY LOG RECORD, never a registry cell

**Owner ruling, 2026-08-11**, on the question D-9 left implicit: `Approved`
records *that* a judgement was made, never *who* made it.

**Why not a cell — the owner's two objections compose into a proof.** An
`ApprovedBy` column holds only the **last** actor, and under the ladder a row
goes `Drafted → Approved → Founded` where **`Founded` is computed** — so the
machinery that observes the children exist would **overwrite the record that a
human approved the text**. The only cell-based escape is one field per
transition (`ApprovedBy`, `FoundedBy`, …), which is column growth. So *any*
cell-based approach either destroys the fact or multiplies the schema.

**Why not git, measured** — "it is in the commit history" is true in principle
and false here, in the direction that fails silently:

- **The author field already says the human for LLM work.** Every agent-driven
  commit in this session reads `author=diytechy`, with the model only in a
  trailer. The kit never sets identity (`setup.sh` prompts, `check_privacy`
  reads), so loop commits inherit ambient config. Git's answer to "who approved
  this?" is currently *the owner*, for work the owner did not do.
- **The `Co-Authored-By` trailer is unenforced** — the two tests naming it only
  check it passes the privacy floor.
- **Squash misattributes rather than loses.** D-1 already rejected this class
  when it killed ALT-1 on history rewriting; for authorship it is worse, since
  a squash collapses N commits into one authored by the *merger*.

**Ruled shape.** The transition is recorded as an **append-only entry in the
log** — `row · from→to · actor · commit` — written by the machinery that
performs the flip. The actor is valued as an **`agents` registry id** or a
human marker, so "was this row blessed by a human or by a hat?" is answerable
by query rather than by reading prose. It survives squash (file content, not
git metadata), cannot be overwritten (append-only), and costs the registries
nothing. It is the row-level sibling of `log.md`'s existing **Gate Sign-offs**
table.

**THE GUARDRAIL, and it is the whole reason this is not the ledger D-1 tore
down: the row records the STATE, the log records the EVENT, and NOTHING JOINS
ON THE LOG.** The retired `attestations.csv` was a *registry* — keyed, joined,
and read by three checks, so deleting it silenced all three at once. This
record is narrative: nothing gates on it, and deleting it loses history without
breaking a check. **The day a check reads it to decide something, it has become
the ledger again** — that is the tripwire, not a style note.

**Sequencing: build it WITH D-9's migration (§5 step 7).** The status-flip
machinery is being rewritten there anyway, so the writer is a small addition to
scheduled work rather than a new mechanism. It also closes, at row granularity,
the gap that nothing durably records who certified what — the Gate Sign-offs
table being its gate-granularity twin, hand-maintained and last filled
2026-07-07.

**SEQUENCING — Q11 binds.** Fixing the vocabulary is safe; **migrating is
not.** The 38 `Modified` rows must be resolved at the sitting first, or
stamping hashes over their current text launders the re-blessing they owe — and
`Modified`-as-derived needs `TextHash`/`HashedOn` to exist at all (D-1's anchor
half). The ladder migration runs after the sitting, in one atomic act with the
predicates and the pin.

---

## 3. The questions, and where each one went

Q1–Q4 all closed; Q5–Q12 live inside D-3 and D-9. The map and the full
reasoning are archived —
[`archive/repo-lock-decisions-2026-08.md`](archive/repo-lock-decisions-2026-08.md).
**Q3 alone is still open** and is listed under D-1 above.

## 4. Answers to questions already asked

Both closed; archived with §3.

---

## 5. What "locked" means — the close-out checklist

Locked = the rulings made, everything below done, `drafts=0 modified=0`, and
this file archived.

### Owed by the owner

The **two rulings** in §0 (components → OI-14), and the **P0 sitting's part
2**. Nothing mechanizable is waiting on anything else.

### Then, in order

6. **Hold the P0 sitting.** Part 1 is done (2026-08-10: one need attested,
   three ruled mis-levelled and demoted, one reframed — see [`log.md`](log.md)'s
   Decisions). **What remains is the 25-row re-attest brief**
   ([`ratify/2026-08-08-mechanized-loop.md`](ratify/2026-08-08-mechanized-loop.md)),
   and it should be worked **together with the prose batch** in §8.4 — both are
   re-blessing windows, and doing them at once collapses two windows into one.
   **Must precede** the ladder migration (Q11).
7. **Build the schema batch ONCE**, on the D-5 carrier: D-1's anchor half,
   D-2's SN fields, D-3's unmigrated columns (`Phase` on SN, `Priority` float),
   D-4's `SupersededBy` deletion and its ~80-line validator, **D-9's ladder
   migration** (closing the enum first — consequence 7), **the SN `Scope`
   field** (template vs this-repo — §8.6 item 3), and every test asserting a
   column shape. This is the batch that gets built twice if it starts early.
8. **Regenerate the derived artifacts** and confirm the gate rises to its
   honest ceiling. A gate that does *not* rise is a finding, not a nuisance.
9. ~~**Drain or dispose the open frontier**~~ — **DONE 2026-08-11** except
   **WI-390**, which is deliberately last: it is the concurrency-v2 program
   close and carries **spine amendments**, so it belongs with the sitting.
   Closed this pass: WI-415 · WI-422 · WI-423 · WI-424 · WI-425 · WI-426 ·
   WI-427 · WI-428 · WI-429.
10. **Dispose the warn-only residue.** "Known and accepted" is a disposition;
    "still there" is not. The standing candidate is extending
    [`enforcement-audit.md`](enforcement-audit.md) with a per-check **catch
    ledger** — the D-7 method applied check-by-check.
11. **Full bar green, stated with real output.** The bar is a *state*, not a
    trophy — it has been claimed true and been false one commit later. Re-run
    it at the end. Last measured **2291 passed, 5 skipped** at `982109b3`.
12. **Merge to `main`** — an owner act (`push = "human"`).

### Loose ends, owed to no step above

- **`intake.py` is a monolith again** (1503 → higher since the carrier and
  brief work). Recorded rather than shaved, because trimming a comment to clear
  a threshold buys a green by editing the guard instead of the thing it
  measures. A WI-280 decomposition candidate.
- **`trace.py` does not know the traced/ratified split** (`spine_cell_class`
  lives in `check_trajectory`), so the re-attest brief diffs every cell equally
  and cannot tell a mechanical pointer fix from a requirement amendment. This
  one bites at the sitting.
- **No supported way to ask "which test scaffolds carry which declared
  policy."** WI-428's exposure census had to be improvised (instrument the
  waiting function, run the suite twice inside the window). It worked and is
  **not reusable**: `blackout` is only special in that it *waits*, so the day
  another dial grows blocking behavior the same false-green is available.
- **The four unfounded LLRs need a ruling on what `CodeSymbol` may claim** —
  belongs with the ladder migration, not a rewrite of authored cells (WI-429).
- ~~**`docs/declared-absences:92`'s stated reason is discharged**~~ —
  **WITHDRAWN 2026-08-12: this claim was a misreading.** The entry at that
  line (now ~98) is about the `drive.py`→`dispatch.py` rename and LLR-143's
  stale Module pointer, gated on **WI-390** — nothing to do with the
  derived-gate-model repoint. The checker declined to edit it; it stays until
  WI-390.
- **The `derived-gate-model.md` citations — REPOINTED 2026-08-12.** The 13
  live source/test citations (plus a 14th the inventory missed, in
  `hooks/pre-commit:229`) now cite the archived spec; touched-module tests ran
  green (163 passed, 1 skipped) and `check_docs` reports 0 broken links.
  `PROCESS_OPTIONS.md`'s citation moves with the stage-semantics rework;
  `docs/gate`'s header line self-corrects at next regeneration (generated
  file, not hand-edited). `SR-049` remains fenced out (sitting territory,
  §8.4 item 7). Original measurement, kept for the record:

  | class | citations | where |
  |---|---|---|
  | **live kit source** | **8** | `derive_gate.py` (4) · `check.py` (2) · `trace.py` · `check_trajectory.py` |
  | **live kit tests** | **5** | `test_trajectory_arch` · `test_trace` · `test_derive_gate` · `test_check_harness` · `conftest` |
  | **live shipped doc** | **1** | `PROCESS_OPTIONS.md` — the one an adopter reads, pointing at a path absent even from the kit |
  | live docs | 7 | `log.md` (2) · `spine-restructure` · `reviews/003-REVIEW-A` · `repo-review-2026-07-21` · this file · the stage/gate proposal |
  | generated | 1 | `okf/system-requirements/SR-049.md` |
  | history — keeps it | 1 | `work/complete/WI-088-…` |

  **Repoint the 14 live ones** at the archived spec, whose **§3 / §4a / §5 /
  §7 / §9.3** the citations name precisely — `PROCESS_OPTIONS.md`'s summary is
  unnumbered prose, so retargeting there would silently coarsen every one.
  Four of the seven "live docs" are historical records and keep their citations
  under the `check_doc_refs` doctrine.

  **`SR-049` is NOT a repoint — checked, and it is sitting territory.** The
  dead path sits in its **`rationale`** cell (*"SSOT applied to the gate itself
  (docs/specs/derived-gate-model.md)"*), `spine_cell_class` classes `Rationale`
  as **ratified**, and the row is **`Verified`**. So correcting it is a spine
  amendment that opens a re-attest window, not a mechanical fix. It joins the
  carrier-falsified list in §8.4 item 7 — the same batch, the same window, and
  it must not be swept in with the other 14.
- **A red test case cannot mint the work item that fixes it.** The
  `adjudicate-red-tc` brief is wired (WI-424) and re-runs the census live, but
  its typed verdict enum is **`DRAFTED | NEEDS-JUDGEMENT`** — neither of which
  is *"mint a WI to plug the gap"*, which is the outcome the owner expects a
  red TC to produce. Worth knowing that the repo **can** already tell the three
  failure kinds apart, on three separate mechanisms: **not implemented** (the
  symbol does not resolve → the LLR never reaches `Founded`, WI-429),
  **implemented as a stub** (`check_stubs.py`, a G3 bar item), and
  **implemented wrong** (substantive symbol, red test). So the discovery half
  works; it is the *disposition* half that has no verdict word.
- **`blackout.template` still ends `12:00-19:00`** — a value the kit no longer
  ships. Low risk (the kit README already labels it a *retired scaffold
  source*, and nothing scaffolds it), recorded rather than churned. Step 10.
- **`status.md` is ~450 lines against a 120-line warn budget** — pre-existing.
- **`Priority` names two incompatible vocabularies** — D-3 rules it a float;
  the migration is owed (step 7).

---

## 6. Reference findings

F-1 … F-12, compiled 2026-08-09, are **archived** —
[`archive/repo-lock-decisions-2026-08.md`](archive/repo-lock-decisions-2026-08.md).
They are the evidence behind rulings now made. Two are still load-bearing and
are cited from §0: **F-10** (what the IF `Contract` cell encodes → OI-14) and
**F-11** (components bind the other rulings). The per-field mechanical detail
has its own permanent home in
[`registry-machinery-reference.md`](registry-machinery-reference.md).

## 7. This document's own log

Archived with §6, including the **claims this document made and had to
withdraw** — which is the part still worth reading, because each cost real
work.

---

## 8. Owner intake, 2026-08-10 onward

### 8.1 · Should the OTHER registries move to TOML too? — measured, yes, as batch-2

The owner leans "all of them", and the shapes support it: `interfaces.csv`
(110 rows, 5 pipe cells, 968-char longest), `open-items.csv` (**3,126-char**
cells — the loudest case in the repo), `agents.csv`, `components.csv`. Every
argument that moved the spine applies.

> **HALF DONE, 2026-08-11 — WI-431** (`f458aea7` → `fd9e9fb7`).
> **`open-items` and `agents` are on TOML**, owner-approved; the converter and
> `spine_carrier` learned both, every reader is wired, and the sources are
> deleted. Bar: **2282 passed, 5 skipped**. **Remaining: `interfaces.csv`
> (waits for OI-14, which rewrites what a `Contract` cell may contain) and
> `components.csv` (waits for the components ruling, which is *about* CMP
> rows).**
>
> **This section's reader inventory below was WRONG, in two ways that mattered.**
> It named **3** open-items readers; there are **8** (`gen_open_items` ·
> `check_docs` · `traj_status` · `check_trajectory` · `trunk_step` ·
> `integrate` · `intake` · `bootstrap`). And it named **`intake` as a writer —
> it is not**; `intake` only reads, and the **writer is `bootstrap.py`**, which
> *appends* a whole row. That distinction changed the work: the spine's line
> rewrite exists because it *changes a cell of an existing row*, and an append
> touches nothing, so no rewrite machinery was owed. Treat the inventory for
> the remaining two registries as unverified until re-measured.
>
> **The cutover was again the detector, and again it found fail-opens** — three
> readers that looked fine against the old carrier: `gen_open_items` rendered
> **"0 pending decisions"**, `traj_status` spliced an empty block into
> `status.md`, and `check_trajectory`'s brief lint went vacuously clean. Only
> `agent_route` failed loudly. That is the exact silent-false-green shape a
> decision queue must never have.
>
> **A carrier hazard nobody had named: ids containing a dot.**
> `[agent.ANTHROPIC-OPUS-4.8]` written bare is **valid TOML declaring nested
> tables** — the file parses, and the row silently vanishes. Fixed at three
> levels (the emitter quotes, the converter detects, and
> `spine_carrier.nested_table_findings` refuses at load), so the remaining
> batch-2 registries inherit the guard. Worth knowing because it fails in the
> worst direction: no parse error, no finding, one fewer row.
>
> **`test_dogfood_sync`'s rule was extended rather than forked — and it bit on
> the way in**, catching the template conversion dropping `RuledDate` /
> `RulingRef` / `Env` (columns the CSV header declared with every shipped cell
> empty). Exactly the drift the redesigned rule exists to catch, on its first
> outing against a new registry.

Two design notes:

- **`interfaces.csv` converts WITH its schema change, not before** — OI-14 and
  the deferred vocabulary-IF question rewrite what an IF row *is*; converting
  first means converting twice.
- **The `test_dogfood_sync` rule was redesigned for the spine** during the
  cutover ("live keys ⊆ template keys ⊆ carrier vocabulary", plus
  `SPINE_TIER_KEYS` as a stated schema). Batch-2 should reuse that shape rather
  than invent a second one.
- `migrate_carrier.py` generalizes (a `KEY` map per registry); the converter is
  not the work, the readers are — and batch-2's are far fewer.

### 8.2 · The common-module question — candidate **D-8**, measured both ways

The owner: F5's single-file-copy advantage is *"basically moot given how things
have grown."* Measured: **25 of 55 kit scripts already import a kit sibling**,
and D-6 added twelve importers in one day. What still argues for standalone and
must survive any ruling: **`bootstrap.py` runs before the kit is copied**, the
git-hook checkers run in constrained contexts, and ADOPTING's re-sync copies
`scripts/` directory-wise.

**Recommended shape if ruled:** invert the default — kit scripts *may* import a
declared common sibling, with an explicit standalone-required list. **Execute
after the lock**, as its own program: ~30 files plus the scaffold surface.

> **RE-MEASURED 2026-08-12 (owner re-posed the question; AST census, not
> grep).** The figure above is stale: **32 of 55** scripts import a sibling;
> `spine_carrier` alone has **17 importers**. The "constrained context"
> argument is dead on inspection — `check_trajectory.py` is hook-invoked AND
> already imports `spine_carrier` with no failure mode, and ADOPTING's §6
> re-sync copies `scripts/` wholesale (the same mechanism that already ships
> the declared siblings). **The standalone-required list reduces to
> `bootstrap.py`** (its own source states why, twice; its two deliberate
> duplicates are pinned) — plus `subagent_gate.py` as a *recommended*
> exception on fail-open/latency grounds the owner ruled on 2026-08-11.
> **Live drift found by the census, worth fixing regardless of D-8:**
> `is_example` is 3-way duplicated and `trace_text`'s copy crashes on `None`
> (unpinned, untested); the declared-line reader is a **5-way**
> reimplementation (`read_declared` ×2 + `_first_declared_line` ×3) with a
> false prose equivalence claim and zero cross-pins; `value_to_cell` writer
> and reader claim mutual inversion with no round-trip test (a non-`str`
> list element breaks one direction only). **Cheapest immediate act:** the
> three `test_rule_sync` value-pin batteries — independent of any
> consolidation. **Recommended D-8 shape, updated:** extend the
> declared-sibling pattern by TOPIC (predicates → `spine_carrier`; the
> byte-identical 9-function `spec_*` family in 3 files → delegate to
> `agent_common`'s copies), **no monolithic `common.py`** — phase 1 is 9
> files, 3 new import edges, 0 new modules, ~650 duplicate lines deleted.
> Still: **execute after the lock.**

### 8.3 · The stakeholder-need batch — six items + one draft SR — **RULED 2026-08-12**

**The owner: all six hold**, with item 2 — and by the same reasoning items 3
and 4 — relaxed from "double-clickable" to **double-clickable *where the
platform allows*** (Linux desktops require the execute bit / a `.desktop`
entry, so a bare double-click contract is unpromisable there). The batch
enters as **Draft rows together with the §8.6 additions** ("sprinkled in
along with the other needs … both directly and implied"); attestation stays
the sitting's. The challenges below were part of the record the owner ruled
over and stay binding on the drafting — especially item 6, which still lands
with the component-model partition.

The owner's six SN-tier items: **(1)** SNs written from the end-user's
perspective, plain language, no implementation references; **(2)** a
double-clickable `dev-setup` launcher per platform; **(3)** same for
`agent-resume`; **(4)** a `run` launcher opening a menu of applicable actions;
**(5)** SN→SR decomposition prose must carry the repo's "hat" perspectives;
**(6)** SRs written against component-boundary interfaces, with architecture
and SR decomposition simultaneous. Plus a draft SR: the loop addresses handback
documents first, then works tier-by-tier, halting where attestation is
required.

**The challenges that survive, honestly:**

1. **Timing is favorable** — rewriting ratified SN prose opens re-attest
   windows, and the sitting's part 2 is already one. Q11 still binds: ladder
   migration after.
2. **"No implementation references" conflicts with today's acceptance-intent
   cells**, which cite scripts by name. A 29-row mass amendment. **And it
   conflicts with a live requirement** — see §8.4 finding 2.
3. **Launcher facts, corrected:** `agent-resume.*` exists self-applied.
   `run.*` ships but is **deliberately un-self-applied** here ("a meta-repo has
   no product to launch"), so item 4 is a **reversal**, not an addition.
   `dev-setup` launchers **do exist** (`.command`/`.cmd`/`.sh`/`.ps1`,
   scaffolded and self-applied) — in `scripts/`, not at root — so item 2 is a
   **placement** change, clearly SR-tier by the sitting's own demotion test.
   Linux double-click has no defined desktop contract on any profile.
4. **Item 5 changes machinery:** the "hat" roster needs a declared home and
   `trace.py --ratify` must inject it — a WI, not a prose edit.
5. **Item 6 is the big one** and lands on the **unruled components model**
   (§0). It reorders the process spine (SRs at G1, architecture at G2 today).
   It cannot be adopted as a sentence; rule it with components.
6. **The draft SR** presumes the D-9 ladder and the attestation dials — intake
   as Draft, decompose against what the loop already does.
7. **The owner's own guardrail applies:** every SN admitted here should pass
   the D-7 evidence test at birth — name the failure it prevents and the
   evidence it would leave, or it is ceremony.

### 8.4 · The prose legibility rewrite — PREPARED, adversarially reviewed twice

[`plans/2026-08-10-sn-sr-prose-rewrite.md`](plans/2026-08-10-sn-sr-prose-rewrite.md)
— exact replacement text for all 29 SNs (form (i), qualifiers retained
verbatim), a 17-SR exact-text batch (13 further rows *dropped* rather than
shipped as outlines), the §B.0 obligation-coverage matrix, and the edge-case
mis-levelling analysis. **Reviewed twice by OpenAI `gpt-5.6-sol` at medium
effort** — round 1 adversarial (12 corrections, including 12 laundered-qualifier
rows), round 2 verification (4 residuals). Dispositions are in the document.
**Work it with the sitting's part 2** (§5 step 6).

**What it surfaced beyond prose, each a sitting input:**

1. **Two decomposition GAPS.** No SR carries SN-005's *CI runs the same
   harness* obligation, nor SN-007's *a change to a script is covered by a
   test*. **SN-007: RULED 2026-08-11 — strike the clause** (the row's own
   acceptance already states the sustainable version, so the deletion makes it
   self-consistent). **SN-005: reform, don't delete** — the obligation is *true
   and shipped* (`ci/check.yml` runs `check.py`; this repo's `test.yml`
   dogfoods it) but **nothing pins it**: the tests read triggers, pinned
   actions and job names, never a `run:` line. The cheap half — one definition
   of passing — is a stdlib string search. Proving CI≡local on all inputs, and
   anything about an adopter's copy, is not worth mechanizing.
2. **SR-126 (`Verified`) already PERMITS script names in spine normative
   text** — its acceptance carves out "a script name, artifact path, rubric or
   sibling spine id does not [open a window]". §8.3 item 1 as a mechanical rule
   contradicts a live enforced requirement. Rule them together.
3. **`gate_policy` names two different things** — the retired config enum *and*
   a live runtime label (`human-held`/`loop-held`). It generated two false
   stale-text defects inside one analysis pass. Recommend renaming the runtime
   label.
4. **`PROCESS_OPTIONS.md` still instructs through the retired enum** at **10**
   distinct `gate_policy` token lines (the two hyphenated `--gate-policy` sites
   are live translated interface, not residue). `test_rule_sync`'s pin covers
   only the template, so nothing mechanical sees this — and adopters read it as
   operative process.
5. **Stale-text verdicts, settled:** SR-040 **CONFIRMED** (contradicts itself
   between adjacent cells); SR-018 **WITHDRAWN** (the legacy `docs/privacy-check`
   read is a deliberate shipped migration window); SR-082/085/108/125 **CANNOT
   VERIFY** until finding 3 is resolved.
6. **The draft SR collides with SR-141** (which gives adjudication rows top
   priority) and presumes "SN always human-attested", which
   `human_ratification_through = 0` contradicts.
7. **Rows the carrier cutover falsified — tabled, not amended:** `SR-002` is
   the clear one ("…CSV structure", a column-count clause). Also worth reading:
   SR-025 · SR-129 · SR-147 · LLR-002 · LLR-025 · LLR-034 · LLR-041 · LLR-118 ·
   LLR-136 · LLR-165 · TC-025 · TC-129 · TC-160 · SN-026. Some may still be
   true (the off-spine registries are still CSV). **Add the rows that still
   name the six toggle FILES as a dial's home** — WI-432 moved those dials into
   `process.toml [checks]`, and the spine cells naming `docs/trajectory-check`
   and its siblings are now imprecise; they were fenced out of that WI because
   they are ratified text. **Add `SR-049`**, whose
   ratified `rationale` cites the pre-archive `docs/specs/derived-gate-model.md`
   path (§5 loose ends). **Add `LLR-150`**, whose
   `detail` repeats a docstring claim WI-429 proved false.

### 8.5 · Agent rulings — three settled 2026-08-11, one still owed

**The list did its job.** Of the four entries below, the owner **overturned**
one (WI-423 — and the reversal was cheap precisely because the agent had
measured its own row's cost premise false), **ratified** one with a scope
correction (`key = ""`), and **ruled** the tabled question (the blackout dial).
**Only WI-429's LLR discharge rule is still owed a yes or no** — it was taken
under a "proceed" and is gating hard under `--strict` today.

- ~~**WI-423 — check-enablement toggles STAY FILES**~~ **OVERTURNED BY THE
  OWNER, 2026-08-11.** The agent ruling rested on **absence-as-declaration** —
  no file means the check is on, and you create a file to switch it off. The
  owner's ruling: *"creating files to toggle something off is also very
  confusing … far better to tie those into `process.toml` and key them all to
  on / true."* That answers the agent's objection rather than ignoring it:
  the objection was "a TOML key cannot be absent and still declare, so folding
  means shipping six visible keys" — and **shipping six visible `= true` keys
  is the point**, because explicit beats implicit. The agent's own measurement
  makes the reversal cheap: it found the row's stated cost premise **false**
  (the sh-parse hooks read only three keys, none of them these six), so
  option (a) is ~15-line `tomllib` reads in three stdlib checkers, not five
  copies of a shell contract. **EXECUTED as WI-432** (`6562239f`): the six now
  ship in `[checks]`, both headers rewritten, the overturned text gone, and
  WI-423's own closed spec carries a dated OVERTURNED banner so a reader cannot
  mistake it for live.

  > **My brief for that work was WRONG, and the builder caught it.** I said
  > five of the six were on-by-default. Measured, **four** are:
  > `agent_loop` read `read_declared(docs/live-status, "false")`, so an absent
  > file **disabled** the live console. Shipping it `= true` would have changed
  > every fresh scaffold's console behaviour **under cover of a re-homing** —
  > the exact class of silent change this program keeps finding. My figure came
  > from inferring the README dial table rather than reading the code. Shipped:
  > `trajectory_check` · `interfaces_check` · `components_check` ·
  > `okf_export` = `true`; `live_status` = `false`; `subagent_gate` = `"off"`
  > (kept a **string**, since `ask` and `deny` are different restrictions).
  > Measured F5 cost: three local readers (24/22/36 lines, 10/10/7 executable);
  > `agent_loop` and `bootstrap` needed none. The migration rides SN-028's
  > existing dual-read window rather than starting a second clock, so an
  > adopter's window is **one re-sync long**.
- **The `key = ""` refusal** (`49ab1c1c`) — **RATIFIED 2026-08-11**, with one
  correction the owner should see. Ruling: *"if it's restricted to the spine,
  draft state is the right approach"* — i.e. a half-written row is marked
  `Drafted`, not blanked. **It is no longer spine-only:** WI-431 routed
  `open-items` and `agents` through the same loader. That is still safe,
  because the finding's actual remedy is *"delete the line"*, which works
  everywhere — but the **`Drafted` remedy is spine-only**: `open-items` has a
  `status` with a different vocabulary, and **`agents` has no status field at
  all**. So off-spine, the answer to "not ready yet" is delete the key, not
  mark it draft.
- **WI-429's LLR discharge rule** — see D-9.
- ~~**TABLED: should the kit ship YOUR blackout window to every adopter?**~~
  **RULED 2026-08-11: ship it DISABLED, but keep the shape.** The template
  becomes `blackout = "12:00-12:00"` — verified mechanically to disable
  (`start == end`, probed across the day, runs at every hour) — with a comment
  naming the window an adopter might want. **One caveat on the comment's
  wording:** the reason offered was that Claude models see heavier usage
  12:00–19:00 UTC, and **I cannot validate that** — I have no source for
  Anthropic's aggregate load and will not manufacture one. What is checkable is
  the mapping (12:00–19:00 UTC = 08:00–15:00 US Eastern, 05:00–12:00 Pacific),
  which is plausibly peak for a US-centric service but is not a measurement.
  Since this ships to every adopter, the comment should read as the kit
  author's operating observation, not as an asserted fact about the vendor.
  **EXECUTED as WI-433** (`231eb1de`). Verified on a real fresh scaffold:
  `(720, 720)`, **0 waits across 504 probed clock times**, against **105** for
  the populated window. The pin was **re-aimed, not deleted** — split into
  four, with the non-vacuity moved to *"a populated window still blocks"*, and
  this repo's own dial asserted present-and-parseable but deliberately **not
  pinned to a value**, since it is the owner's. Red-proofed on four separate
  breaks. The wording constraint is **mechanized**: a test requires the
  observation framing and *refuses* the strings `Anthropic`, `Claude models
  see`, `usage peaks` — so the unvalidated vendor claim cannot creep back in.

  *(Original entry, kept for the reasoning — see the executed WI-433 record
  above it:)*
  **should the kit ship YOUR blackout window to every adopter?**
  `process.toml.template` ships `blackout = "12:00-19:00"` (UTC weekdays), and
  its comment records that as deliberate (*"a MOVE, not an occasion to
  re-decide it"*). **Nothing has changed the value.** But its cost is now
  visible: an adopting team in another timezone inherits a business-hours
  blackout they did not choose, and it silently disabled ten of the kit's own
  tests for seven hours of every weekday (fixed as WI-428, without touching the
  dial). **The asymmetry when ruling:** a shipped-empty dial an adopter forgets
  costs odd-hours activity; a shipped-populated dial an adopter does not notice
  costs seven hours a day of a loop that looks broken.

### 8.6 · Owner intake, 2026-08-12 — the sitting that ruled stage semantics and the SN batch

Everything below is owner direction from one sitting, recorded before
execution. Items 1–2 shape rulings still owed; 3–4 are new obligations; 5–8
are questions the owner asked this session (answers land here as the analyses
finish).

1. **The component model's direction.** Components are architectural
   breakdowns **and define the boundaries system requirements are written
   against** — an SR's inputs and outputs must correspond to
   component-boundary interfaces. Method: *"lay out the inputs/outputs of the
   system first, and then break that into components with internal signals"* —
   and the owner suspects the breakdown is an **optimization problem** with a
   mathematical expression behind it, rather than something an LLM should
   freestyle (which is what this repo has historically done). **Research
   DELIVERED 2026-08-12** →
   [`docs/knowledge/system-decomposition-methods.md`](knowledge/system-decomposition-methods.md).
   The short version: the owner's "lay out system I/O first" intuition **is**
   the N2/DSM method literally, not analogously; `interfaces.csv`'s `SR-Refs`
   column already forms the signals×requirements incidence matrix; the right
   objective is **hypergraph-cut minimization** (count the cross-boundary IF
   rows a partition forces — the exact thing wanted small), with raw Newman
   modularity rejected for its resolution-limit failure at this registry's
   size; a stdlib hill-climber can *rank and propose* partitions while the
   human names the clusters and judges volatility (Parnas). This is the
   worked input for the components-partition ruling in §0.
   **Interfaces must be INTERFACES only** — each signal typed **discrete vs
   variable** — and every component boundary must have *all* its crossings
   described by interface rows. Mechanical enforcement method: open, part of
   the OI-14/components ruling.
2. **The edge-case tier dissolves into per-need SRs via "hats."** Each SN is
   decomposed wearing every applicable expert perspective; a domain expert is
   not a stakeholder (no needs of their own) but their hat constrains the
   decomposition. The roster is a declared **TOML** file the decomposer prose
   injects — this is §8.3 item 5's roster, now with a carrier ruled. The hats
   include the perspectives accessible to downstream users (the examples).
3. **Every SN declares its scope** — template (downstream adopters + this
   repo) or this repo only. The mechanical field is a registry-schema change
   and **joins the §5 step-7 batch** (build the schema ONCE); until then new
   drafts state scope in their text.
4. **Everything the template provides chains back to a stakeholder need.**
   Each document/file the kit ships fulfills a requirement, tied in — a
   coverage obligation over the *shipped tree*, not just the code. Enters the
   SN batch; the enforcement candidate is a shipped-file → requirement
   mapping check.
5. **Should the prose templates that mechanically build CLI prompts also be
   TOML? — ANSWERED 2026-08-12: NO, and the repo's own precedent says why.**
   The D-5/WI-431 criterion that moved the registries is **rows with
   fields** — many records, stable columns, CSV quoting pain. The prompt
   templates (`worker` / `reviewer` / `critique` / `dual-plan` ×3 /
   `adjudicate-*` ×4) fail it on every axis: each is ONE document, all
   multi-line prose with markdown structure and literal braces, so TOML adds
   an escaping layer and buys nothing (TOML has no templating — the same
   `str.format`/strict-fill machinery would sit on top). Diff legibility
   *worsens* (prose wrapped in `body = """…"""` noise — re-creating the
   "reviewable only by reading source" problem `prompts.py` was built to
   escape). The kit already draws the right line itself: the WI spec is
   **TOML frontmatter for typed cells + markdown body for narrative**. Keep:
   registries/dials = TOML; templates/rubrics = markdown; typed control flow
   = frontmatter cells, never prose (the `prompts/README.md` rule).
6. **The common-module question (§8.2, candidate D-8), re-posed** — the owner:
   the single-file-copy advantage is *"basically moot given how things have
   grown."* **Census delivered 2026-08-12 — see the §8.2 re-measurement
   box** (32/55 import siblings; the standalone list reduces to
   `bootstrap.py`; three live drift hazards found; phase-1 shape is 9 files,
   0 new modules). D-8 is now decidable on measurement.
7. **How do guardrails reach a branch-scoped agent? — ANSWERED 2026-08-12,
   measured against the machinery.** Facts: **`AGENTS.md` is never replaced
   or rewritten per-branch** (claim = spec-move + regen + one commit + branch
   cut, nothing else); **`process.md` is never modified per-branch**; the
   worker prompt is `worker.template.md` filled with the WI row's typed
   cells plus small *computed, clipped* blocks (predecessors, registry
   joins, branch diff, rework findings) and it **points at** `AGENTS.md` and
   the spec as ambient reads rather than pasting them. Tier differences are
   routing-only (model/CLI/effort) except one model-keyed prepend:
   `docs/guardrails/core.md` under the `[policies] guardrails` matcher —
   dormant here (`off`). **The owner's hypothesis does not match the
   machinery:** `docs/agents.toml` is a pure routing registry (family ×
   model × tier × cmd_template × env × notes) carrying zero worker-facing
   prose, and giving it scope prose would conflate "which model" with "what
   this WI may touch." Where new guardrails go, by kind: universal → 
   `AGENTS.md` (ambient, budget-guarded); tier/model-conditional → the
   existing guardrails-core + policy matcher; per-WI → a **typed frontmatter
   cell** on the WI spec joined into the context block (the kit's stated
   rule: prose that carries control flow must be a typed field). One real
   gap found: nothing supports guardrails finer than per-WI (per-path /
   per-subsystem) — new machinery if ever wanted, not a re-homing.
8. **The loop-ordering draft SR, restated:** under `agent-resume`, an agent
   first addresses handback documents from executed work items (minting
   follow-ups if needed), then works tier-by-tier in batch — SN (always
   human-attested) → SR → LLR → TC — halting wherever the automation level
   requires human/external attestation; after all TCs are laid out,
   implementation proceeds autonomously through work-item construction.
   **§8.4 finding 6 still stands** (collides with SR-141's adjudication-first
   priority; "SN always human-attested" contradicts this repo's
   `human_ratification_through = 0`) — intake as Draft, decompose against
   what the loop already does, surface the collision at the sitting.

### 8.7 · Agent decisions taken 2026-08-12, owed owner review

The owner asked for every moderately-confident call to be recorded for later
review. The §8.5 pattern, continued. Entries accumulate as the rework runs.

- **Stage-semantics home = `PROCESS.md`.** The ruling adopted the proposal
  without naming the home. Taken on the §0 evidence (the axis is always-on;
  the options file's own header forbids always-on layers; sizes measured
  budget-neutral across the pair). Reversal cost if overruled: move one
  section and re-aim its links.
- **Gates KEEP their names and their sign-off role.** "Retire gate semantics"
  is executed as retiring gate-as-*state* (the "active gate", `G0`, "at G1"
  phrasing) — G1/G2/G3 survive as the human-certified boundaries between
  stages, because the proposal the owner adopted defines them that way and
  the sign-off record depends on them. If the owner meant retiring the gate
  *vocabulary entirely*, that is a different and larger rework — flagging the
  reading explicitly.
- **The 13 live source/test citations repoint to the archived spec**, not to
  the new `PROCESS.md` section — they cite the archived §-numbers precisely,
  and the new section carries ruled semantics, not gate arithmetic.
- **SN scope field deferred into the step-7 schema batch** (§8.6 item 3) —
  "build the schema ONCE" outweighs having the field now; drafts state scope
  in text meanwhile.
- **The launcher needs enter as Draft rows under the §8.3 challenge-3
  facts** — `dev-setup` is a *placement* change, `run` is a *reversal* of this
  repo's recorded non-goal ("no `run.*` product launchers"): the non-goal's
  boundary changes from "no launchers" to "no *product* launch; an
  actions-menu launcher is in scope". `status.md`'s Scope bullet and the SN
  registry's NG prose need the same amendment — made with the intake, flagged
  here because it edits a recorded non-goal.
