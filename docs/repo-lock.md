# The lock program — living scope and decisions

**What this file is.** The one place scope and rulings accumulate until the
repository is **locked** — every requirement ratified or rejected, every window
closed, the derived gate back at its honest ceiling, and nothing owed to a
sitting. It is *living*: entries are appended and amended in place as decisions
land, and it is deleted (or archived) when §5's checklist is empty.

**What it is not.** Not a working surface and not a second source of truth. The
working surfaces stay [`status.md`](status.md), the registries, and
[`log.md`](log.md); the narrative record of *what happened* stays the log. When
a ruling here is executed, its home becomes the registry row and the log's
Decisions section — this file then keeps only the pointer.

**How a decision enters.** Owner rules it → recorded here with its rationale and
its consequence inventory → executed → the row/log carries it → the entry here
collapses to a one-line pointer with the commit.

---

## 1. Where the repo stands

Measured 2026-08-09 on `infra/mechanized-loop` at `a6ebc957`, from the files
themselves — not restated from the handoff.

| fact | value | source |
|---|---|---|
| derived gate | **G1** (`computed=G0 ex-draft=G2 phase=4`) | [`gate`](gate) |
| SR | 111 `Verified` · **25 `Modified`** · **10 `Draft`** | [`requirements/system-requirements.csv`](requirements/system-requirements.csv) |
| LLR | 131 `Verified` · 6 `Modified` · 10 `Draft` | [`requirements/low-level-requirements.csv`](requirements/low-level-requirements.csv) |
| TC | 128 `Verified` · 7 `Modified` · 8 `Draft` | [`test/test-cases.csv`](test/test-cases.csv) |
| SN | 32 ids; **SN-028…032 sit in a `Draft needs (unratified)` section** | [`requirements/stakeholder-needs.md`](requirements/stakeholder-needs.md) |
| owner surface | **35 attestation cards** = 25 `Modified` + 10 `Draft` SRs | [`open-items.html`](open-items.html) |
| attestation ledger | **1 row, the `ATT-000` example** — zero real data | [`requirements/attestations.csv`](requirements/attestations.csv) |

The gate is G1 *because* a `Draft` SN reads G0. That is the machinery reporting
the truth: the code is built and tested, the requirements behind it are proposed.
Full detail — the program's commits, the measured bar, the warn-only residue and
this machine's environment gotchas — is in
[`handoff-2026-08-08-mechanized-loop.md`](handoff-2026-08-08-mechanized-loop.md);
that document stays the record and is **not** superseded by this one.

---

## 2. Decisions ruled

### D-1 — the attestation anchor moves ONTO the spine row; `attestations.csv` is retired

**Ruled by the owner, 2026-08-09**, on the handoff's §2 question. The third
option: keep the digest, drop the separate registry. `TextDigest` and
`AcceptedCommit` become **columns on the SR / LLR / TC rows themselves**.

**Why this and not the ledger.** The kit preaches one-row-one-home and then
shipped a second registry holding a fact about a row that already exists. The
ledger's cost was not theoretical: it drove the largest single module bump in
the program (`check_trajectory.py` +272 lines) and owned three of the eight
BLOCKERs the reviews found — including the one where *deleting the ledger
silenced all three of its own checks at once*. A mechanism whose failure mode is
"delete it and every guard goes quiet" is carrying its own weight badly.

**Why this and not the narrowed detector** (the alternative the handoff records
as not taken): narrowing `staged_spine_amendments` re-opens the question that
exit was written to close, and leaves stakeholder needs with no anchor by any
path. D-1 keeps the anchor; it only moves its home.

**What survives, unchanged in substance.** The obligation SN-029 and SR-140
state does not weaken:

- a digest of the row's **normative** cells, recorded **at acceptance time**;
- drift reported **regardless of any `Status` movement** — the gap the ledger
  was introduced to close, which the on-row anchor closes identically;
- a corrupt or absent anchor treated as an **error**, not an advisory;
- the ghost-anchor rung (an anchor naming an artifact that is not a current
  row) — it survives as "a row carries a digest that does not match any
  recomputation", plus the `SupersededBy` case below.

**What the ledger's own columns become.** Three of its seven columns were
already duplicated by the row and can be dropped rather than migrated — which is
itself an argument for D-1:

| ledger column | on-row home |
|---|---|
| `ATT-ID` | gone — the row's own id is the key |
| `Artifact` | gone — the row *is* the artifact |
| `TextDigest` | **new column** |
| `AcceptedCommit` | **new column** |
| `Decision` `ratified` / `meaning` | already `Status` — `Verified` vs `Modified` |
| `Decision` `superseded` | already `SupersededBy` (SR) |
| `Decision` `clarity` / `override`, `Date`, `Ref` | the log's Decisions section — evidence, never normative |

**What this costs, stated honestly.** The ledger's one genuinely unique property
was an **immutable sequence of past acceptances**, guarded by
`staged_attestation_rewrite_findings`. On-row, the *current* anchor is explicit
and read (not re-derived), but the *history* of anchors lives only in git
history of the CSV. Two things are worth being exact about:

- This is a smaller loss than it first reads. Append-only never prevented
  "amend the text and record a fresh acceptance in the same commit" — appending
  is the sanctioned act, so that tamper shape silenced the drift check under the
  ledger too. What is lost is the *audit trail*, not a detection.
- What SN-029 argued against was **re-deriving the baseline by inferring from
  `Status` across git history**, which is fragile. Reading past anchors from git
  history as *evidence* is not that, and is sound. Reading the *live* anchor
  from an explicit cell is strictly better than either.

The replacement guard is **co-mutation**, not equivalence: a commit that changes
a row's `TextDigest` must write the digest of that row's text *as it stands in
that same commit*, and a commit that changes normative cells must not also
re-stamp the digest. That is checkable with the two-tree read
(`check_trajectory._spine_revs`) the amendment scan already uses. It is weaker
than append-only and must be described that way in the SR — no ledger-equivalent
claim.

The handoff's §5 residue item — *"the append-only guard's rev-range arm is wired
only for `--staged`"* — **does not disappear with the ledger**. It reappears as
the same question for the co-mutation guard, and is now Q3 below.

**Two alternatives to the digest, examined 2026-08-09 at the owner's
proposal.** Both attack the same objection: *a sha256 is derived data living in
a document meant to define project information, and no human can verify it by
eye.* The objection is correct.

- **ALT-1 · `AcceptedCommit` alone; recompute the historical text from git.**
  Not hypothetical — this is *already how the word-diff works*:
  `trace._attested_baseline` returns a commit and `_rows_at` reads the row at
  that revision through `git show`. ALT-1 is therefore "drop `TextDigest`, keep
  the commit, derive the comparison". **Wins:** no derived data in a reviewed
  artifact; a commit id is meaningful to a human and a digest is not; and it
  yields the whole historical row rather than a changed/unchanged bit.
  **What kills it as the sole anchor: history rewriting.** A squash-merge — the
  default many adopting teams use — destroys every recorded sha at once, and
  `_resolvable` then reports no anchor **repo-wide, silently**. Shallow CI
  clones (`fetch-depth: 1`) do the same. The code already names this hazard in
  `_attested_baseline` ("a rebase or squash rewrote the sha, a shallow clone
  never fetched it"). A content-derived digest survives all three; a
  history-derived pointer cannot.
- **ALT-2 · a per-requirement `-snapshot` copy of the accepted text.** **Win:**
  the only option that gives a human a directly readable *"this is what was
  last blessed"* document, with no git and no hashing. **Costs:** ~150
  machine-written files, each owing a freshness guard; N writes per sitting;
  cleanup on every rename or retirement; and it duplicates what git already
  stores content-addressed — the duplication doctrine the kit preaches against.
  It also buys **no** integrity: a snapshot is as rewritable as the row it
  copies, so amend-both-in-one-commit is silent exactly as it is everywhere
  else. The tempting variant — one whole-registry snapshot instead of N files —
  **breaks on partial ratification**: bless 12 of 25 rows and the snapshot is a
  mixture that cannot be written honestly. Per-row is forced, which lands back
  on N files or a per-row cell.

**Ruling recorded: keep both cells, and reframe which is primary.** They fail in
*different directions*, which is why this is not redundancy:
`AcceptedCommit` is the **reviewable** anchor and the input to the diff a human
actually reads; `TextDigest` is the **git-independent tripwire** that survives
squash, rebase and shallow clone. The owner's objection is answered by making
the commit the primary record — and by dropping the digest to a **short form
(`sha256:` + 16 hex, 23 characters)**, since §6 F-5's analysis shows the
full-width justification does not hold for a pairwise comparison. That
overturns the `digest()` docstring's stated reason and needs to be recorded as
such when implemented.

**Mechanical consequences found while scoping this — none of them optional.**

1. **The digest becomes self-referential unless the new columns are excluded.**
   `check_trajectory.normative_text` folds in *every* column that is not in
   `_DIGEST_EXCLUDED` and not classified `traced`, and the residual in
   `spine_cell_class` deliberately fails safe — an unclassified new column reads
   as **ratified**, i.e. normative. So `TextDigest` would be hashed into its own
   digest. This is not a corner case: it makes every stamped row read as drifted,
   permanently, from the first stamp. Both new columns must join
   `_DIGEST_EXCLUDED` beside `SR-ID`/`LLR-ID`/`TC-ID`/`Status`, for the same
   reason those are excluded — the anchor is not content.
2. **The §A5.1 two-way split needs a third class.** `tests/test_trajectory_staged.py`
   asserts every column of the live registry *and* its template is classified
   `ratified` or `traced` (plus the id and `Status`). Neither is right: an anchor
   cell is not normative prose and not a traceability pointer. So the split grows
   an explicit **anchor** bucket. This is good news — the test forces the ruling
   instead of letting the fail-safe residual silently break hazard 1.
3. **Templates must move with the live registries.**
   `tests/test_dogfood_sync.py` requires each live header to be an *ordered
   superset* of its template header. Appending the same two columns, in the same
   order, to both `project-trajectory/registries/*.template.csv` and the live
   files satisfies it. The template must carry them regardless: a fresh scaffold
   without the columns has a vacuous check, which is the exact "green hides a
   skipped check" failure SN-008 forbids.

**Removal / rework inventory** (measured, not estimated):

| where | what happens |
|---|---|
| [`requirements/attestations.csv`](requirements/attestations.csv) | delete |
| `project-trajectory/registries/attestations.template.csv` | delete |
| [`check_trajectory.py`](../project-trajectory/scripts/check_trajectory.py) | delete `ATTESTATIONS_CSV`, `ATTESTATION_DECISIONS`, `read_attestations`, `newest_attestations`, `attestation_findings`, `attestation_integrity_findings`, `staged_attestation_rewrite_findings`, `_report_attestations` + its `main` wiring (≈250 lines). **Keep and re-point** `normative_text`, `sn_normative_text`, `digest`, `current_digests`, `_DIGEST_SEP`, `_DIGEST_EXCLUDED` — these are the on-row model. |
| [`trace.py`](../project-trajectory/scripts/trace.py) | delete `_ledger_baseline`; `_attested_baseline` reads the row's `AcceptedCommit` cell (no file read at all, and the unresolvable-ref degrade stays) |
| [`intake.py`](../project-trajectory/scripts/intake.py) | `next_att_id` + `record_attestations` → a re-stamp that writes the two cells inside `_apply_flips`, so the flip and the anchor stay **one act**; the `attest` subcommand keeps its name and its `--rows`/`--decision` contract where it still means something |
| [`bootstrap.py`](../project-trajectory/scripts/bootstrap.py) | drop the ledger from the scaffold mapping |
| [`../tests/test_attestation_ledger.py`](../tests/test_attestation_ledger.py) | **rewritten, not deleted** (523 lines). The behaviours it drives — drift regardless of `Status`, the ghost anchor, malformation as an error — all survive; the append-only cases become co-mutation cases. |
| `tests/test_trajectory_staged.py`, `tests/test_dogfood_sync.py`, `tests/test_module_size_ratchet.py` | column classification, header superset, module size |
| [`registry-machinery-reference.md`](registry-machinery-reference.md), `project-trajectory/EXAMPLE.md`, `PROCESS.md` §7 | field docs + the worked chain |
| `docs/okf/system-requirements/SR-140.md` | regenerated, not hand-edited |

**SR-140 is AMENDED, not rejected.** Its obligation stands; only the home
changes. It stays `Draft` and is ratified in its amended form at the sitting —
which means the sitting rules on the text D-1 produces, not on the text that
exists today. Its chain moves with it: **LLR-158** (the three rungs, currently
naming `attestation_findings` / `attestation_integrity_findings` /
`staged_attestation_rewrite_findings` as its `CodeSymbol`) and **TC-153**.
SN-029's own acceptance-intent clause naming `docs/requirements/attestations.csv`
is amended in the same pass — an SN whose text names a retired file is exactly
the "`Verified` row whose text is false" the program spent the 2026-08-08 session
eliminating.

### D-2 — stakeholder needs gain FIELDS rather than a new carrier

**Owner direction, 2026-08-09**, given with D-1 and answering its one unsolved
weakness (the third option "still leaves SNs — no row, no columns — unsolved"):
extend [`stakeholder-needs.md`](requirements/stakeholder-needs.md) with
additional fields so the same anchor mechanism reaches SNs, rather than changing
what an SN *is*. The file stays markdown prose tables; it gains capacity to
encode information instead of a new format.

The direction is ruled. **Two sub-decisions inside it are not, and they change
the work** — they are Q1 and Q2 below.

What is already settled by the direction, and is worth stating because it is the
part that has bitten before: `check_trajectory.sn_normative_text` hashes the
**raw table line**, deliberately — the three SN tables have different shapes and
a parsed projection would hash the garbling. Adding trailing columns to a line
puts the anchor inside its own digest, which is hazard 1 again in a worse form.
The fix is a column-count truncation (drop the trailing anchor fields before
hashing), not a semantic parse — the "raw line" property survives, slightly
qualified, and the qualification must be written into the docstring.

---

## 3. Open questions — what this document is waiting on

### Q1 · Where do the SN anchor fields live inside the file? — **WITHDRAWN 2026-08-09, folded into OI-12**

**The owner refuted this as an independent question:** *"Won't this be impacted
by TOML? If stakeholder needs convert to TOML, then the sha lives in the same
row (stakeholder need element)."* Correct, and it dissolves the question. Under
a TOML carrier an SN is an element with keys; `text_digest` is simply another
key, and the (a)-versus-(b) distinction — *on the row* versus *in a separate
anchor table* — **has no referent**, because there is no table. Every hour spent
ruling and implementing Q1 is discarded if OI-12 rules (b). Q1 is therefore a
*sub-question of the carrier*, not a peer of it, and it is answered by whatever
OI-12 answers. The analysis below is retained as the record of what was
examined, not as a live decision.

**This question has been asked before, and the answer was ruled.** Owner
ruling at G1, **2026-07-12**, recorded in
[`archive/specs/derived-gate-model.2026-07-20.md`](archive/specs/derived-gate-model.2026-07-20.md)
§4 and the WI-090 entry in [`log.md`](log.md). Three options were on the table
for where SN maturity lives:

- **(a) section-as-state** — *chosen*, for "least schema churn, git-derived date";
- **(b) a `Status` cell appended to the SN table** — considered and not taken,
  with the explicit note that this is *"a table column, not a spine CSV — the
  owner's 'no new column' was scoped to SR/LLR/TC"*, i.e. widening the SN
  markdown table was already understood to be permitted and cheap;
- **(c) a ratification ledger `docs/requirements/ratifications.csv`
  (`id,gate,state,who,date`)** covering SN *and* the whole spine — deferred,
  *"revisitable only if per-artifact human attribution beyond git-author is
  later wanted."*

Two things follow, and both should be said plainly. **`attestations.csv` is
option (c)**, rebuilt four weeks later without reference to the ruling that
deferred it — and the trigger the ruling named (human attribution beyond
git-author) is *not* the reason it was built. D-1 therefore returns the repo to
the 2026-07-12 position rather than departing from it. And **D-2 is option
(b)**, which that ruling had already priced as cheap. So Q1/Q2 are not a new
design question: they are a **deliberate re-open** of a G1 ruling on new
information — the amend+flip blind spot, which did not exist in July. Recording
it as a re-open is what keeps the ruling honest.

Three shapes, all consistent with D-2.

- **(a) Widen the need rows.** Append the fields to the `Core needs` and
  `Draft needs` tables, one cell each. Most direct reading of the direction;
  every fact about a need sits on its line. Costs: a 71-character `sha256:`
  cell on rows already carrying 1,500-character prose; and the `Edge-case
  expectations` table (SN-013…022) has a *different* four-column shape, so
  either it widens too or `sn_normative_text` truncates per-table.
- **(b) One anchor table at the foot of the file**, `| SN-ID | … |`, with the
  prose tables untouched. Keeps the reading surface exactly as it is today,
  hashes the prose line unchanged, and handles all three table shapes with one
  rule. Costs: two places in one file mention an SN, which reads as the
  two-homes smell — though only one of them is prose and the other is derived
  state.

- **(c) The WI treatment — one file per need.** Not what D-2 asked for, recorded
  because it is the honest answer to *"isn't there tooling to break a markdown
  file into row elements?"*: **this repo already runs that pattern at scale.**
  [`docs/work/`](work/) is a markdown registry whose rows are *files* —
  `+++`-fenced TOML frontmatter for the typed fields, prose body beneath,
  **directory-as-state** for status — 400+ live specs, three F5-synced loaders,
  and the only *closed* status vocabulary in the repo (an unknown directory is a
  loader refusal, §6 F-1). `SN-028-....md` under `docs/requirements/needs/` would
  give every field D-1 and D-2 want, typed, with no digest-truncation trick at
  all. **Cost: it is a carrier change, not a field addition** — so it
  contradicts the direction — and it moves the ground under **ten** modules that
  read `stakeholder-needs.md` today (`trace`, `derive_gate`, `check_trajectory`,
  `check_docs`, `check_flows`, `gen_okf`, `gen_release_checklist`, `traj_parse`,
  `intake`, `bootstrap`), plus the shipped template and every adopter.

  **Five risks, examined 2026-08-09 (owner question: "WIs are a single item,
  SNs are multiple rows").** They are recorded because the option is recorded;
  together they are why (c) stays not-recommended.

  1. **A WI has ONE axis; an SN has TWO.** Directory-as-state works for
     `docs/work/` because a WI's directory carries its whole state. An SN
     carries *kind* (core need vs edge-case expectation — different columns,
     different tables) **and** *maturity* (draft vs ratified). One of the two
     must fall back to frontmatter, so the "same as WI" claim is already only
     half true, and the closed-vocabulary loader refusal — the property that
     makes the WI home strong — only guards the axis that got the directory.
  2. **SNs are read as a SET; WIs are read as a QUEUE.** Nobody reads 400 WIs
     together; they read a frontier of five. The G1 consistency review reads
     *every* need against the vision in one pass, and the non-goals are read as
     a boundary around the whole set. A generated index restores the view but
     the authoring surface becomes 32 files, and the review is a human act over
     prose.
  3. **The edge-case table is a FORM, not a list.** The shipped template seeds
     13 lifecycle rows with blank `Expected behavior` cells and says "fill in
     every phase below or mark it an explicit n/a". **The blanks are the
     teaching.** One file per row cannot show a gap, and the scaffold loses the
     pedagogy that makes an author write the Provision/Startup rows they
     otherwise skip.
  4. **A carrier change fails OPEN across those ten readers — verified, not
     assumed.** `derive_gate.py` guards its read with `if sn_md.exists()` and
     falls to empty sets; `check_docs._registry_needs` returns `[], []` with the
     comment *"no needs to hold the README to (vacuous)"*. Re-point eight
     readers and miss two and the repo gets **quieter**, not redder — the exact
     permissive-direction failure the handoff's §7 names as the pattern to hunt
     for in anything built on this machinery.
  5. **It does not remove the digest problem; it swaps it.** (An earlier
     revision of this section said "no digest-truncation trick at all" — that
     was too generous.) A table line is trivially canonical, which is why
     `sn_normative_text` can hash it raw. A free-form markdown body is not:
     whitespace, heading depth and list markers all move the digest without
     moving the meaning, so the anchor needs a canonicalization rule instead of
     a truncation rule. Nothing digests a WI spec today, so there is no
     precedent in the WI home to borrow.

  **What survives the five.** (c)'s one real win is *typed fields, no
  truncation trick* — and that is also what **(b)** buys, at a fraction of the
  blast radius. The examination therefore strengthens (b) rather than (c).

**I do not have a confident answer between (a) and (b).** (b) is mechanically
cheaper and leaves the document a human reads alone; (a) is the more literal
reading of the direction and keeps one line per need. The deciding question is
whether the anchor is *content about the need* (→ a) or *bookkeeping about its
acceptance* (→ b), and that is the owner's call, not a derivable fact. **(c) is
what I would choose if the SN tier were being designed today** — and is the
wrong size for a lock program, so it is recorded, not recommended.

**On the tooling assumption behind (c):** a markdown *AST parser* would be a
**dependency**, and [`dependencies.md`](dependencies.md) currently holds two
rows, both `system` (git, gh) — **zero Python packages ever admitted**. A parser
inside a shipped check forces every adopter to install it, the one tier the kit
holds stdlib-*preferred* ("rare, ideally never"). It is admissible through a
reviewed ledger row, but "hand-rolling is worse" is hard to argue here: the
current SN readers are ten-line heading scanners, and `docs/work/` proves the
pattern needs no parser at all.

### Q2 · Do SNs get a `Status` cell — **WIDENED 2026-08-09 to every registry**

**Owner:** *"Yes but we need to align on all the registry definitions. I'm
afraid this will impact the interface definitions as well."* Verified — it does,
and [`interfaces.csv`](requirements/interfaces.csv) is in worse shape than the
spine:

- **`Status` is an UNDECLARED column on the IF registry.** `PROCESS.md` §8 names
  the IF row's fields as *"direction, counterpart, contract, the `SR-Refs` that
  realize/rely on it, version, and stability"*. **`Status` is not among them** —
  yet it ships in the template (`Draft`) and carries a value on all 95 live rows
  (Stable 87 · Active 4 · Draft 4).
- **It overlaps its own neighbour.** `Stability` is {Stable, Experimental};
  `Status` is {Stable, Active, Draft}. *Stable* appears in both, meaning
  different things, in adjacent columns of the same row.
- **Their enforcement is inverted from what a reader would assume.**
  `Stability` — the declared field — is read by exactly one consumer
  (`gen_release_checklist`). `Status` — the undeclared one — is read by
  **nothing mechanical at all**; its only consumer is
  `plan_briefs.IF_SURFACE_COLUMNS`, which hands it verbatim to the dual-plan
  **LLM briefs**. An undeclared, unvalidated, self-overlapping column is being
  presented to a model as fact.

So the real question is not *"does an SN get a `Status` cell"* but **"what does
`Status` mean across all six registries, which of them should carry one, and
what happens to the IF pair"** — §6 F-1's six carriers and F-2's undeclared
contract, turned into a decision. That is a cross-registry design act, not a
sub-question of D-2, and it wants **its own OI row** rather than a Q in a living
document. The SN half stays as recommended below; it is now the *smallest* part
of the question.

#### The SN half, unchanged

The handoff's gap 2 is "an SN has no `Status` cell at all". D-1 + D-2 close the
*anchor* half. The *state* half is separate and is what determines the answer to
§4 below (whether SNs reach the owner surface at all).

Today SN draft-ness is **section-as-state (§4a)**: an SN is `Draft` because it
sits under a heading containing the word "draft". Both `derive_gate.py` and
`trace.py` implement that rule independently. If SNs gain a `Status` cell, that
is **two homes for one dial** — precisely what SN-028 just shipped a REFUSAL
for. So the two moves are coupled:

- **Q2 = yes** → the `Status` cell is authoritative, section-as-state is
  **retired** in both readers, the `Draft needs (unratified)` heading becomes
  prose organisation only, and SNs become renderable in
  [`open-items.html`](open-items.html) as first-class ratification cards.
- **Q2 = no** → SNs keep section-as-state, gain only the anchor fields, and stay
  invisible to the owner surface (§4's finding stands, mitigated only by pointing
  at the file).

**Recommendation: yes, with the retirement in the same commit** — never both. The
kit's own doctrine says a repo declaring one dial twice is refused, and shipping
that shape in its own registry after refusing it downstream is the shadowing
defect [`process.toml`](process.toml) already names in its `[attestation]` note.

### Q3 · How far back does the co-mutation guard compare?

Inherited unchanged from the handoff's §5 (it was folded into the ledger
question and survives it). The `--staged` arm is straightforward; the rev-range
arm needs a declared base, and "how far back" has no obviously correct answer.
Until it is ruled, the guard is honest but partial — and must say so in its
docstring rather than reading as complete.

### Q4 · Does the sitting rule on today's SR-140 text or on D-1's amended text?

Recommended: **D-1's amended text**. Ratifying the current wording and
immediately amending it burns a ratification on prose already known to be
retired, and manufactures a `Modified` row on the day it is created.
Consequence: D-1 is implemented **before** the sitting, not after it.

---

## 4. Answers to questions already asked

### "Are you indicating SN-028…SN-032 have changed?"

**No.** They are **new and never ratified**, not amended. The whole 2026-08-08
program touched [`stakeholder-needs.md`](requirements/stakeholder-needs.md) by
`+20 −1` lines — the new `Draft needs (unratified)` section and its heading. No
existing need's prose moved.

The word "changed" belongs to a different set: the **25 `Modified` SRs**. Those
are `Verified` rows whose text was amended because the machinery underneath them
was retired (`hand_back`, `## Handback`, `docs/gate-policy`,
`attended`/`single-ratify`, two TCs citing renamed tests). They were flipped to
`Modified` deliberately — a `Verified` row whose text is false is the worst thing
this registry can carry. Both sets are owed at the same sitting, which is why the
handoff bundles them; they are owed for opposite reasons.

### "Are these getting pulled properly into open-items.html for straightforward review?"

**Partly — and the missing part is precisely the SNs.** Measured against the
generated file:

| what an owner needs to rule | on the surface? | detail |
|---|---|---|
| the 25 `Modified` SRs, per-cell before/after | **yes** | with the baseline revision printed on every section |
| the 10 new SRs (SR-137…146) | **yes** | rendered as *"ratification owed / no baseline — awaiting its FIRST ratification"*, whole current content |
| their LLR / TC chain (LLR-155…164, TC-150…157) | **yes** | they ride the owning SR's card — all ten LLRs and all eight TCs emit a chain row (counted from the rendered row heads: 35 SR cards, 34 LLR and 39 TC chain rows in total) |
| **SN-028…032 themselves** | **no** | they appear only as the literal token `SN-028` inside an SR's `SN-Refs` cell |

The mechanism, not a guess: `gen_open_items.render` builds its model from
`trace.reattest_model(root, reg.srs, reg.llrs, reg.tcs, statuses=("modified","draft"))`.
**The attestation unit is the SR.** SNs are not passed in and structurally
cannot be — `reattest_model` selects rows by `Status`, and an SN has no `Status`
cell. The section's own empty-state text says so out loud: *"No `Draft` or
`Modified` **SR**"*.

So the concrete gap: an owner ratifying SR-137 reads the requirement in full and
sees, as the need it serves, the bare string `SN-028`. The ~1,200 characters of
need / why-it-matters / acceptance-intent they are actually being asked to
ratify are in another file, and nothing on the surface says to go there. Five
needs — the top of the chain, the tier the whole program hangs from — are the
one thing the decision surface does not show.

**Q2 is what closes this.** With a `Status` cell, SNs become selectable by
`reattest_model` and render as their own cards; without one, no amount of work
in the renderer can reach them. Note also that the surface is
freshness-gated (`--check` byte-compares) and carries a stamped baseline that
regeneration must reuse, so this change lands **with** a regeneration, never
after it.

---

## 5. What "locked" means — the close-out checklist

Ordered by dependency, and split by **who owes what** — the distinction that
matters, because the first block is not work and the second cannot start
without it.

**Revised 2026-08-09** after the owner refuted the previous ordering on three
counts (Q1 collapses into the carrier; `Status` alignment reaches the IF
registry; deferring the carrier buys a second round of test rewrites). The
revision turns on a **seam inside D-1** that the objections exposed:

| half of D-1 | carrier exposure | can it ship now? |
|---|---|---|
| **the removal** — delete `attestations.csv` + template, ~250 lines in `check_trajectory`, `trace._ledger_baseline`, `intake.record_attestations`, the scaffold rows; rewrite `test_attestation_ledger.py` | **none** — adds no column, touches no schema | **yes**, and it costs nothing: the ledger holds **zero real rows** (only `ATT-000`), so deleting it loses no detection that exists |
| **the anchor** — the two cells, `_DIGEST_EXCLUDED`, the third cell class, the co-mutation guard, template columns, `test_dogfood_sync` | **total** | **no** — this is the half that gets built twice |

And one more thing the objections make available: **SR-140 can be written
carrier-neutrally and ratified at the sitting.** *"The anchor is recorded on the
artifact's own row/element"* names no format. The carrier appears only in the
LLR's `Module` / `CodeSymbol` — which are **traced** cells, so re-pointing them
at a TOML reader later opens **no re-attest window** (§6 F-3). That is
mechanically supported, not wishful.

### Ship now — carrier-independent, blocked on nothing

1. **The removal half of D-1.** Pure deletion; no data lost.
2. **SR-140 / SN-029 amended to carrier-neutral prose**, so the sitting can
   ratify the obligation without ratifying a format. LLR-158 / TC-153 follow.

### Owed by the owner — two rulings, both now gating

- **OI-12 · the carrier.** Promoted from *rulable later* to **the gating
  decision**: Q1 folds into it and the anchor half waits on it. Card is live on
  [`open-items.html`](open-items.html); recommendation unchanged in substance —
  TOML is the right destination — but the *sequencing* recommendation is
  withdrawn, because "defer it, nothing is foreclosed" was wrong about cost.
- **`Status` across all six registries** (Q2 widened) — including
  [`interfaces.csv`](requirements/interfaces.csv)'s undeclared `Status` and its
  overlap with `Stability`. **Wants its own OI row**; not yet filed.

Q3 (how far back the co-mutation guard compares) and Q4 (which SR-140 text the
sitting rules on) are answered inline in §3 and need no separate act.

### Then, in order

3. **Hold the P0 sitting** — ratify / amend / reject SN-028…032 and their
   decomposition, and work the 25-row re-attest brief
   ([`ratify/2026-08-08-mechanized-loop.md`](ratify/2026-08-08-mechanized-loop.md)).
   Every ruling appends to [`log.md`](log.md)'s Decisions. **Not blocked by the
   anchor:** ratification is a `Status` flip, and the anchor records what was
   ratified. Stamping afterwards leaves the sitting-to-stamp window
   unprotected, which is **no worse than today** — the ledger has never held a
   row.
4. **Build the anchor half of D-1, plus D-2, ONCE** — on the carrier OI-12
   rules — and stamp what the sitting accepted.
5. **Regenerate the derived artifacts** — `docs/gate`, `open-items.html`,
   `PROJECT_STATE.html`, the OKF export — and confirm the gate rises to its
   honest ceiling. A gate that does *not* rise is a finding, not a nuisance.
6. **Drain or dispose the open frontier** — WI-390, WI-415, WI-422, WI-423,
   WI-424. WI-424 (route the adjudicator briefs) carries its own two decisions;
   see the handoff's §4.
7. **Dispose the warn-only residue** — the handoff's §5 list, each either fixed
   or recorded as accepted. "Known and accepted" is a disposition; "still there"
   is not.
8. **Full bar green, stated with real output**: `pytest -q -n auto` unfiltered,
   `check.py` at the derived gate, `check_trajectory.py --strict` unfiltered.
9. **Merge to `main`** — an owner act (`push = "human"`), and the standing
   deliberate item [`status.md`](status.md) already carries.

Locked = both rulings made, 1–9 done, `drafts=0 modified=0`, and this file
archived.

### Loose ends this discussion surfaced, owed to no step above

- **The unpinned SN reader twin.** `traj_parse._sn_rows` ↔ `gen_okf.sn_rows` are
  held equal by a docstring and nothing else, and have already drifted once
  (a phantom `SN-000` root in the dashboard icicle). Real under every carrier
  answer, so it should not wait on OI-12.
- **`status.md`'s ratification-level prose is stale** — it still says the level
  is `autonomous`, a value [`process.toml`](process.toml) *deleted* in favour of
  `human_ratification_through = 0`. Hand-authored owner prose; flagged, not
  edited.
- **`status.md` is 445 lines against a 120-line warn budget** — pre-existing;
  this file is meant to absorb some of that depth, and has not yet.

---

## 6. Reference findings that bear on D-1 / D-2

Compiled 2026-08-09 by reading source, in answer to "what are the `Status`
options, is that an interface, and which columns are mechanical vs prose". The
per-field mechanical detail already has a home —
[`registry-machinery-reference.md`](registry-machinery-reference.md) §2–§5, §10,
§12 — and is **not** restated here. Only what changes a decision is.

**F-1 · There is no single `Status` vocabulary — there are six carriers, and
only one is closed.** SR/LLR/TC `Status` is *open* with three magic values
(`Draft`, `Verified`, `Modified`, exact match, case-insensitive); SN state is a
*heading substring* ("draft"); WI state is a *directory* and is the only closed
one (unknown dir = loader refusal); IF `Status`, OI `Status` and CMP `State` are
open and unvalidated. Consequence for **Q2**: giving SNs a `Status` cell moves
them from the substring rule to the equality rule — which is a *stricter*
mechanism, and the migration must not leave a heading saying one thing and a
cell another.

**F-2 · The vocabulary is not declared as an interface, and the IF registry has
no shape for it.** Of 95 IF rows, five name `Status` in their `Contract`
(IF-021 trace, IF-051 derive_gate, IF-059 plan_briefs, IF-054 schedule,
IF-073 gen_open_items) — **all on the `Consumes` side**. No row *provides* the
vocabulary, because IF models module↔module and module↔file seams, not data
vocabularies. Its actual homes are `PROCESS.md` §7 prose, the F5-duplicated
`is_draft` / `is_verified` / `is_modified` predicates (`trace_text.py`,
`trace.py`, `derive_gate.py`), and the reference doc — held together by
`tests/test_rule_sync.py`. That is a contract between six readers enforced by a
sync test rather than declared anywhere. Not a defect to fix inside this
program; worth naming because **D-1 and Q2 both add readers to it**.

**F-3 · Spine columns fall into four classes, not two — and the fourth is the
one D-1 creates.**

| class | what it means | examples |
|---|---|---|
| **mechanical** | parsed, joined, or gated | ids, `SN-Refs`, `SR-Refs`, `Verifies`, `Status`, `Verification`, `Tier`, `Automated`+`Evidence`, `Phase`, `Module`, `SupersededBy` |
| **prose an LLM is handed** | lifted verbatim into an assembled brief | SR `Title`/`Requirement`/`Rationale`/`AcceptanceCriteria` (critique brief + dual-plan surface), TC `Parameters`/`Method` (artifact recipe + rubric-path scan), and everything in the generated OKF bundle |
| **inert** | shipped and often *required*, but no code reads the value | `LLR.TestRefs` (nothing reads it at all), `LLR.CodeSymbol` (required, never resolved), `SR.Area`, `SR.Lifecycle`, the *values* of `SR.Priority` / `TC.Level` / `TC.Method`, every SN column, and `SR.Permutations` — a machine grammar that `gen_cases.py` only ever receives by hand via `--spec` |
| **anchor** *(new, D-1)* | machine-written, machine-read, never human-authored | `TextDigest`, `AcceptedCommit` |

The fourth class is why the §A5.1 traced/ratified split needs a third bucket
(§2, hazard 2): an anchor cell is not ratified prose and not a traceability
pointer, and the fail-safe residual would classify it as normative and break its
own digest. **The class distinction is the ruling**, not a code detail.

**F-4 · The inert class is a live risk for an agent-run repo**, and it is the
class most likely to grow. An agent filling `LLR.TestRefs` or `LLR.CodeSymbol`
believes it is feeding a mechanism; nothing checks the claim, and a reader
downstream trusts a cell nothing maintains. No action inside this program —
recorded so that "add a column" is never treated as free.

**F-5 · The digest's full width is not justified by its stated reason.**
`digest()` says *"Full width — this is an ANCHOR, and a truncated one is a
collision waiting to be the reason an amendment went unnoticed."* Every check is
a **pairwise** comparison on one named row — never a search across a set — so
the birthday bound does not apply: at 16 hex characters an accidental collision
is ~1 in 1.8×10¹⁹ per comparison. The width is also unpinned — the only shape
check is `.startswith("sha256:")`, and the test fixtures use `sha256:a`. The
reasons that *do* hold are duller (free in a CSV cell, self-describing,
no new rule to justify), and they stop holding the moment the cell lands in a
markdown table a human reads.

**F-6 · There is no reusable markdown-table reader in this repo, and CSV→
markdown would not be a like-for-like swap.** Two separate facts, often
conflated:

- The `docs/work/` loader **parses no tables at all** — it is `tomllib` over
  `+++`-fenced frontmatter (~15 lines, `parse_spec_frontmatter`) plus
  directory-as-state. It is small *because* the typed fields are TOML, not
  because markdown is easy to read.
- The SN tables are read by **six bespoke scanners**, several F5-duplicated:
  `sn_all_ids` + `sn_draft_ids` (trace/derive_gate twins), `sn_normative_text`
  (raw-line match), `check_docs._registry_needs` (heading scan + Priority-column
  discovery), and `traj_parse.sn_rows` + `gen_okf.sn_rows` — the last pair split
  on `|` and index cells **positionally** (`cells[0]`, `cells[1]`, `cells[3]`),
  are required to stay byte-identical, and **have already drifted once** (one
  kept `-000`, one did not, rendering a phantom root in the icicle).

**Measured, 2026-08-09.** Reading **32 SN rows** costs **~239 lines / ~166 code
lines across 14 functions in 8 modules**. Reading **436 spine rows** (146 SR +
147 LLR + 143 TC) *and every off-spine registry* costs **`trace.load_csv`, five
lines**, because `csv.DictReader` does the rest. Splitting the SN figure
honestly: ~139 code lines are pure **carrier parsing** and would vanish under a
structured carrier (`sn_all_ids` ×2, `sn_draft_ids` ×2, `sn_normative_text`,
`_registry_needs`, `gen_okf.sn_rows`, `read_stakeholder_needs`,
`traj_parse._sn_rows`, `scan_sn_placeholders`, `check_flows`'s inline regex);
~28 are **semantics that survive any carrier** (`sn_gate`, `sn_cited_ids`,
`sn_integrity_findings`). So the SN tier costs roughly **28× the parsing code
for 7% of the rows** — and it is also the tier with **no schema tier at all**
(no required-field, no enum checks; reference doc §12.5). Most parsing code,
least enforcement.

Two F5 pairs carry that duplication, and they are **not equally guarded**:
`sn_all_ids` / `sn_draft_ids` (trace ↔ derive_gate) *are* pinned equal by
`tests/test_rule_sync.py`; `traj_parse._sn_rows` ↔ `gen_okf.sn_rows` are pinned
by **nothing but a docstring** ("Change both together") — and they have already
drifted once, rendering a phantom `SN-000` root in the dashboard's icicle. That
unpinned twin is a live hazard today, independent of any carrier decision.

Measured against the live registries, converting SR/LLR/TC to markdown tables
would hit: **five cells that already contain a literal `|`** (SR-024, SR-043,
LLR-024, LLR-040, LLR-152) — which `traj_parse`'s naive `.split("|")` shape
cannot survive; **552 cells containing commas**, which CSV handles by RFC-4180
quoting and markdown has no equivalent for; a **1,553-character** longest cell;
and no representation at all for an embedded newline (none today, but the CSV
form permits one and `gen_open_items.normalize` exists because a Windows-authored
multi-line cell was observed). `trace.structure_findings` — the column-count
integrity guard — has no markdown analogue, and positional indexing is exactly
the failure it exists to catch.

**F-7 · TOML as ONE carrier for all four tiers is the strongest technical
option raised, and the right answer for a successor program — not this one.**
Owner question, 2026-08-09: could a `.toml` file replace the `.md` + `.csv`
combination?

*Why it is strong.* `tomllib` is **stdlib at the kit's 3.11 floor** — no
dependency, unlike a markdown parser (F-6). The kit already sanctions TOML in
two homes: [`process.toml`](process.toml) and the `+++` frontmatter of every
`docs/work/` spec. Multi-line basic strings dissolve every carrier defect F-6
measured — the five cells holding a literal `|`, the 552 comma-bearing cells,
the 1,553-character cell, and the unrepresentable embedded newline. Typed
arrays (`SN-Refs = ["SN-028"]`) retire `refs()`'s split-on-whitespace rule and
with it reference §12.8's `SN-001 and SN-002` → `and`-is-an-orphan bug. And TOML
carries **comments**, which CSV cannot — today the SR template fakes them by
stuffing a ~700-character explanation of the `Phase` rule *inside an example
row's cell value*.

*The blocker that isn't.* `tomllib` is read-only (PEP 680 omitted a writer
deliberately), and the kit writes registries programmatically — `intake`
rewrites `Status` today and must write the anchor cells under D-1. But this
repo has already solved that **twice, two different ways**:
`wi_convert.toml_string` + `_TOML_ESCAPES` is a hand-rolled emitter
("*the TOML emitter (tomllib is read-only)* … *Verified by re-parsing every
emitted file with tomllib*"), and `bootstrap.set_process_key` takes the other
route — **a line rewrite, never a re-serialization**, so the file's explanatory
header survives. They are not interchangeable: the line rewrite works only
because `process.toml` owes the git hooks a one-`key = value`-per-line
contract, which a registry holding multi-line prose cannot honour. A spine
carrier would need the emitter form — a third copy, or the first genuinely
shared one.

*The cost is knowable, because this migration has already been run once here.*
The WI registry **was** `work-items.csv`; it is now `docs/work/**/WI-*.md` with
`+++` TOML frontmatter. That conversion ran as a multi-phase program
(2b → the 2c authority flip → Phase 5's "the CSV home died"), spanned weeks,
forced a re-attestation sitting (LLR-051/056 re-grounded, SR-129/LLR-136
`Modified`), and surfaced real defects — `build_scope_srs` and
`critique_control` had been reading **silently EMPTY since the 2c flip**, the
fail-open shape again. A spine migration is *larger*: the WI registry carries no
upward/downward joins into three sibling registries, and the spine does.
`trace.structure_findings` (column-count integrity) has no analogue — though a
parse error is arguably a stronger check — and `test_dogfood_sync`'s
"live header is an ordered superset of the template header" rule has no meaning
over TOML keys and would need redesigning. Every F5-duplicated loader changes,
and every adopting repo migrates.

*Sequencing — CORRECTED 2026-08-09.* This section first said deferring "costs
nothing" because "D-1 and D-2 are carrier-neutral". **That was overstated and
the owner caught it:** *"isn't this going to result in some test rewrites after
the fact if everything is not clubbed together?"* Yes. The **fields** are
carrier-neutral; the **code and tests are not**. Building the anchor on CSV and
then converting rewrites the column-classification machinery (columns become
keys), `test_dogfood_sync`'s ordered-superset header rule (no meaning over TOML
keys), `structure_findings` (column count becomes a parse error), `intake`'s
writer (`csv.writer` becomes a TOML emitter), the two-tree `git show` parse in
`_rows_at` / `_spine_revs`, and `test_attestation_ledger.py` **for a second
time**. "Forecloses nothing" is true of the design and false of the labour.

What survives the correction is a **seam inside D-1**, and it is what the
revised §5 is built on: the *removal* half has zero carrier exposure and the
*anchor* half is entirely carrier-exposed. See §5.

**F-8 · A design constraint has NO declared home in this method** — found while
placing F-7 (owner, 2026-08-09: *"it's not necessarily a stakeholder need … it
is perhaps a design constraint"*). The observation is correct and the gap is the
kit's, not this program's:

- `PROCESS.md`'s **G1 bar literally requires** "usability/doc needs +
  **constraints** + non-goals captured". Non-goals have a declared home (the
  `## Non-goals` section, `NG-#`). **Constraints have none** — no ADR concept,
  no constraints registry, no `DC-` id space anywhere in the kit.
- In practice they are recorded as **SNs**, and several already are: SN-003
  (stack-agnostic), SN-011 (stdlib + argued dependencies), SN-012 (right-sized
  process). None is a desire; each is a constraint whose "stakeholder" is the
  adopting team and the agents working in the repo. The SN file already carries
  non-need content, so the tier is in practice *top-level obligations, whoever
  they serve*.

**Placement for F-7, recommended.** It is not a constraint yet — it is an
**unruled decision**, and the kit has a registry for exactly that.
[`open-items.csv`](requirements/open-items.csv) carries `OneLine` / `Decision` /
`BlastRadius` / `Options` / `Recommendation` / `WI-Refs` and renders as a card
in [`open-items.html`](open-items.html), the surface the sitting reads anyway.
The owner queue is **currently empty** (OI-7/10/11 all ruled; only the `-000`
example remains), so this would be its only card; the next id is **OI-12**.
Sequence: *OI-12 now → if ruled "one carrier", it becomes an SN + SR on the
SN-011 shape.* The rejected alternative is a new `## Design constraints` /
`DC-#` section: `sn_all_ids` scrapes `SN-\d+` only, `trace.ID_PATTERNS` knows no
`DC`, and no orphan or gate rung would see it — **inert until built**, which is
the worst of the three outcomes. `architecture.md` is likewise wrong here: a G2,
partly-generated artifact with no G1 rung and no anchor.

**Candidate follow-up, not filed:** the *prose-an-LLM-is-handed* view above
exists nowhere as a consolidated surface —
[`registry-machinery-reference.md`](registry-machinery-reference.md) documents
mechanical effect per field and mentions LLM consumption only in passing. Folding
F-3 into it as a new section would give the question one home. Deliberately not
done mid-program: it is a reference-doc edit with no bearing on the lock.

---

## 7. This document's own log

- **2026-08-09** — created. Records D-1 (owner ruling: the attestation anchor
  moves onto the spine row; `attestations.csv` retired) and D-2 (owner
  direction: stakeholder needs gain fields, not a new carrier), the four open
  questions those raise, and the measured answer to *"are SN-028…032 on the
  owner surface?"* — they are not, and Q2 is what would put them there.
- **2026-08-09** — §6 added: the four reference findings from reading the
  `Status` carriers and the column classes (F-1 six vocabularies, F-2 not an
  interface, F-3 the four column classes including the new *anchor* class,
  F-4 the inert-column risk).
- **2026-08-09** — Q1 reframed as a **re-open** of the 2026-07-12 G1 ruling on
  SN maturity (section-as-state chosen over a `Status` cell and over a
  ratifications ledger): D-1 returns to that ruling's position, D-2 is its
  option (b). Q1 gained option (c), the `docs/work/` one-file-per-row pattern,
  with the dependency argument against a markdown parser. **No recorded
  rationale exists for storing SN as markdown while SR/LLR/TC are CSV** — the
  form is inherited from `user-needs.template.md`, described everywhere and
  justified nowhere.
- **2026-08-09** — Q1 option (c) examined against the owner's objection ("WIs
  are a single item, SNs are multiple rows"). Five risks recorded; the
  one-axis-vs-two-axes point is the deepest, and the fail-open degrade in
  `derive_gate` / `check_docs` was verified in source rather than assumed. A
  claim in the previous entry — that (c) removes the digest problem — is
  corrected there: it swaps a truncation rule for a canonicalization rule. Net
  effect: the examination strengthens **(b)**, not (c).
- **2026-08-09** — D-1 gained the two owner-proposed alternatives to the digest
  (ALT-1 commit-only + git recompute; ALT-2 per-requirement snapshot files) and
  the ruling that follows: **keep both cells, make the commit primary, shorten
  the digest to 16 hex**. The decisive finding is that ALT-1 dies silently
  repo-wide under squash-merge or a shallow clone, which a content-derived
  digest survives. §6 gained F-5 (the full-width justification does not hold)
  and F-6 (no reusable markdown-table reader exists; five live cells already
  contain a literal `|`).
- **2026-08-09** — **three owner objections, all upheld, plan revised.**
  (1) Q1 **withdrawn** as an independent ruling — under a TOML carrier an SN is
  an element with keys and the on-row-vs-anchor-table distinction has no
  referent, so it folds into OI-12. (2) Q2 **widened** from "does an SN get a
  `Status` cell" to `Status` across all six registries, after verifying that
  [`interfaces.csv`](requirements/interfaces.csv) carries an **undeclared**
  `Status` column (absent from `PROCESS.md` §8's field list) that overlaps
  `Stability`, is read by nothing mechanical, and is fed verbatim to the
  dual-plan LLM briefs. (3) **"Carrier-neutral / forecloses nothing" corrected**
  — true of the design, false of the labour; deferring the carrier buys a second
  round of test rewrites. §5 rebuilt on the **seam inside D-1**: the *removal*
  half ships now (zero carrier exposure, zero real ledger rows), the *anchor*
  half waits for OI-12, and SR-140 is written carrier-neutrally so the sitting
  is not blocked by either.
- **2026-08-09** — §6 gained **F-7**: TOML as one carrier for all four tiers.
  Strongest technical option raised; `tomllib` is stdlib, the repo already
  writes TOML two ways, and it has run this exact migration once (work-items.csv
  → the `docs/work/` spec folder). **Deferred to a successor program, not
  refused** — D-1/D-2 are carrier-neutral fields, so shipping them forecloses
  nothing. F-6 also gained the measurement: 32 SN rows cost ~166 code lines to
  read, 436 CSV rows cost five.
