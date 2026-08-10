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

## 0. Start here — the four things awaiting a decision

Everything below is context for these. Nothing in this document is blocked on
more analysis; it is blocked on rulings.

| # | question | where to read it | recommendation |
|---|---|---|---|
| **C** | Does one machine-parseable **carrier** hold all four requirement tiers? The `.md` + `.csv` split has **no recorded rationale anywhere**. | card on [`open-items.html`](open-items.html) · §6 F-7 | **TOML** as the destination; sequencing is the real question, see below |
| **OI-13** | What does **`Status`** mean across the six registries that carry one — including [`interfaces.csv`](requirements/interfaces.csv)'s undeclared `Status` overlapping `Stability`? | card · §3 Q2 · §6 F-1, F-9 | reserve the word for ratifiable-artifact maturity, rename the rest, **execute with OI-12** |
| **OI-14** | What is an IF row's **`Contract` cell for**? Measured: design narrative and history, 1% requirement voice, and the registry has **no schema tier at all**. | card · §6 F-10 | **declare now, split gradually** — never a 95-row sweep |
| *(unfiled)* | The **component model**. `LLR.Component` is a *traced* cell, so the partition moves with no re-attest window — and it **decides how many IF rows must exist**. | §6 F-11 | not filed on purpose; filing it would be me setting the sitting's agenda |

**Read them in this order: components → IF → `Status` → carrier.** OI-14
assumes today's 95 IF rows are the right 95, and that rests on the unruled
component model; OI-13 and OI-12 both rewrite registry definitions, so ruling
them apart pays the migration cost twice.

**Separately, and not blocked by any of the above: the P0 sitting can be held.**
Ratification is a `Status` flip; the anchor that records *what* was ratified is
the only part waiting on OI-12 (§5 step 3).

**Four rulings already made** are not pending: **D-1** (the attestation anchor
moves onto the artifact's own row; `attestations.csv` retired — the removal
half shipped), **D-2** (stakeholder needs gain fields rather than a new carrier
— the *shape* of those fields folded into OI-12), **D-3** (a column name means
one thing repo-wide; shared semantics ruled for `Status`, `Title`, `Phase`,
`SR-Refs`, `Rationale` and `Priority`, with `Status` a four-rung ladder
`Drafted → Attested → Ready → Verified`), and **D-4** (supersession is
deletion, not a forwarding pointer — and ids must therefore never be reused).
All four in §2.

**Two things in that set need the owner's eye before they are built**, both
recorded with recommendations: `Status`'s new `Verified` **re-points a word 370
live rows already use with the old meaning** (§2 D-3 Q9 — recommend spending a
fresh word instead, so a half-migration cannot hide), and D-4 **must not ship
before an id watermark exists**, because every mint in the repo derives its
high-water mark from the live set and a deletion frees the id (§2 D-4).

**D-3 changes OI-13's status**: it answers the vocabulary question in the
general case, so what remains on that card is the *migration* — which registries
rename, and what happens to the IF `Status`/`Stability` pair. It also has a
dependency the reading order above does not yet show: D-3 gives IF a shared
`Rationale` column, which is the mechanical destination OI-14's split needs
(§2 D-3, Q8). **D-3's own five open sub-questions** (Q5–Q9 there) are build-time
consequences with recommendations, not new sittings — except Q6, which is a
correction the owner should see: `Phase` is *not* the non-functional grouping
attribute the ruling assumes.

---

## 1. Where the repo stands

Measured 2026-08-09 on `infra/mechanized-loop` at `b2507c8c`, from the files
themselves — not restated from the handoff.

| fact | value | source |
|---|---|---|
| derived gate | **G1** (`computed=G0 ex-draft=G2 phase=4 stage=0`) | [`gate`](gate) |
| SR | 111 `Verified` · **25 `Modified`** · **10 `Draft`** | [`requirements/system-requirements.csv`](requirements/system-requirements.csv) |
| LLR | 131 `Verified` · 6 `Modified` · 10 `Draft` | [`requirements/low-level-requirements.csv`](requirements/low-level-requirements.csv) |
| TC | 128 `Verified` · 7 `Modified` · 8 `Draft` | [`test/test-cases.csv`](test/test-cases.csv) |
| SN | 32 ids; **SN-028…032 sit in a `Draft needs (unratified)` section** | [`requirements/stakeholder-needs.md`](requirements/stakeholder-needs.md) |
| owner surface | **3 pending decisions** + **35 attestation cards** (25 `Modified` + 10 `Draft` SRs) | [`open-items.html`](open-items.html) |
| attestation ledger | **gone** — it held 1 row, the `ATT-000` example, for its whole life (D-1) | — |

The gate is G1 *because* a `Draft` SN reads G0. That is the machinery reporting
the truth: the code is built and tested, the requirements behind it are proposed.
**Nothing this program has done moves the gate**, and that is correct — no
artifact has been ratified.

**What this program has landed**, all on `infra/mechanized-loop`:

| commit | what |
|---|---|
| `9b6c7fc0` | this document, and **OI-12** on the carrier |
| `0156e0fe` | **OI-13** on `Status` across six registries |
| `91831f4d` | **D-1's removal half** — the ledger retired, the digest kept |
| `b2507c8c` | **OI-14** on the IF `Contract` cell, plus the registry audit (F-9…F-11) |

Full detail on the program *before* this one — its commits, the measured bar,
the warn-only residue and this machine's environment gotchas — is in
[`handoff-2026-08-08-mechanized-loop.md`](handoff-2026-08-08-mechanized-loop.md);
that document stays the record and is **not** superseded by this one.

---

## 2. Decisions ruled

### D-1 — the attestation anchor moves ONTO the spine row; `attestations.csv` is retired

**Ruled by the owner, 2026-08-09**, on the handoff's §2 question. The third
option: keep the digest, drop the separate registry. `HashedOn` and
`TextHash` become **fields on the artifact's own row** — *which* cells that
means is the carrier's business, ruled separately (OI-12), which is why
SR-140's amended text says "row" and never "column".

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
| `TextHash` | **new column** |
| `HashedOn` | **new column** |
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
a row's `TextHash` must write the digest of that row's text *as it stands in
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

- **ALT-1 · `HashedOn` alone; recompute the historical text from git.**
  Not hypothetical — this is *already how the word-diff works*:
  `trace._attested_baseline` returns a commit and `_rows_at` reads the row at
  that revision through `git show`. ALT-1 is therefore "drop `TextHash`, keep
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
`HashedOn` is the **reviewable** anchor and the input to the diff a human
actually reads; `TextHash` is the **git-independent tripwire** that survives
squash, rebase and shallow clone. The owner's objection is answered by making
the commit the primary record — and by dropping the digest to a **short form
(`sha256:` + 16 hex, 23 characters)**, since §6 F-5's analysis shows the
full-width justification does not hold for a pairwise comparison. That
overturns the `digest()` docstring's stated reason and needs to be recorded as
such when implemented.

**Field names — ruled 2026-08-09.** The working names are **`TextHash`** and
**`HashedOn`**; the earlier `TextDigest` / `AcceptedCommit` are retired
before either cell exists, which is the cheapest moment to rename — nothing
outside this document and two historical records uses them.

- `TextDigest` → **`TextHash`**: owner preference; *hash* is the plainer word
  for what the cell holds, and `digest()` the function keeps its name.
- `AcceptedCommit` → **`HashedOn`**: the old name **overclaimed**. A commit is
  a repo-wide snapshot, not an act of accepting this row's text — reading
  `AcceptedCommit` as "this text was accepted here" invites exactly the
  inference the adjudicator procedure below has to walk back when the commit is
  unresolvable. `HashedOn` claims only what is true: **the commit at which
  `TextHash` was last produced or re-verified**. It is deliberately silent
  about acceptance, which `Status` records, and about correctness, which
  nothing records.

  The two cells now read as one statement — *this hash, taken at this commit* —
  and that pairing is what makes the co-mutation guard expressible: a commit
  that writes `TextHash` must write the digest of that row's text **as it
  stands in that same commit**, and must set `HashedOn` to itself. The cell
  therefore moves **only when the hash is written**, never on an unrelated
  edit. `BaselineCommit` was the intermediate name and is rejected for being a
  *consequence* rather than the fact: the commit happens to be where a diff
  starts (`trace._attested_baseline` returns it, `_rows_at` reads the row at
  that revision), but that is what the machinery *does with* the value, not
  what the value *is*. Under TOML the key can carry the rest of the sentence in
  a comment, as the owner notes — `hashed_on = "…"  # commit the hash was last
  produced or verified at`.

**On a denser encoding than hex — examined 2026-08-09 at the owner's question,
recommendation: keep lowercase hex.** The question is fair; the measurement
does not support the change. Re-encoding the same 64 bits saves almost nothing:
base32 is 13 characters, base64url 11, Ascii85 10, against hex's 16 — a
best case of **6 characters**. The `sha256:` prefix is **7 characters on its
own**, so if width is the goal, shortening the prefix beats every alphabet
change and costs no new rule. Against that, non-hex buys three real problems:
it is **case-sensitive** (hex compares case-insensitively today, and a
spreadsheet round-trip or a lowercasing cleanup would silently corrupt base64 —
this repo already carries `gen_open_items.normalize` because a Windows-authored
cell was mangled once); it is not **greppable by eye** against a `git show`
output, where the whole point is that a human can spot two anchors differing;
and it needs a **new encoding rule argued into existence**, which the kit's own
bar makes expensive for a six-character win. Git itself is the precedent
against packing: shas are hex, and git's answer to width is **abbreviation**,
not re-encoding.

Packing into non-ASCII Unicode is the version to refuse outright. It would be
denser per character, but the cell would then be subject to **normalization**
(NFC/NFD can rewrite codepoints and thus the anchor), homoglyphs make visual
comparison worthless, and it breaks the one property a tripwire needs — that
it survives every transport between the author and the reviewer unchanged.

**And the owner's closing observation is the real resolution:** under a TOML
carrier (OI-12) this stops mattering. `text_hash = "…"` is a key/value on its
own line, the key name already says what the value is, and the width competes
with nothing. Width only ever hurt in the **SN markdown table**, where a
23-character cell sits beside 1,500-character prose — and even there the ruled
fix is the column-count truncation (§2, D-2), not a denser alphabet.

**Adjudicator recovery procedure — the degraded mode, owner-added 2026-08-09.**
When the digest trips but `HashedOn` is unresolvable (squash-merge,
rebase, shallow clone), no local mechanism can produce the before-text — the
digest answers only *changed*, never *what changed*. The procedure then is:

1. **Treat the row as a first ratification.** The machinery already renders
   this honestly — `open-items.html`'s *"no baseline — awaiting its FIRST
   ratification"* card shows the whole current content; the adjudicator
   re-reads and re-blesses the text as it stands.
2. **Use the children as semantic evidence, not as a mechanical check.**
   Before re-blessing an SN whose baseline is lost, read its SR / LLR / TC
   chain: if the decomposition still fulfills what the current prose asks —
   as if it were a newly proposed need — the *meaning* is judged unchanged
   even though the wording cannot be diffed. This inverts the trace direction
   (children vouching for the parent), which is why it is an adjudicator
   procedure recorded here and never a check a script runs.
3. **Look for the before-text off-repo before giving up on a diff.** A squash
   destroys the sha in the target branch, not necessarily everywhere: the PR's
   own history on the forge, an unpruned remote branch, or a teammate's clone
   may still hold the pre-squash commit. Worth one look; not worth a mechanism.

**Mechanical consequences found while scoping this — none of them optional.**

1. **The digest becomes self-referential unless the new columns are excluded.**
   `check_trajectory.normative_text` folds in *every* column that is not in
   `_DIGEST_EXCLUDED` and not classified `traced`, and the residual in
   `spine_cell_class` deliberately fails safe — an unclassified new column reads
   as **ratified**, i.e. normative. So `TextHash` would be hashed into its own
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

**Removal / rework inventory** (measured, not estimated). §5 splits this table
along one line: everything that **deletes** is the carrier-independent *removal
half* and ships now; the **two new columns and everything that classifies,
guards or templates them** is the carrier-exposed *anchor half* and waits for
OI-12.

| where | what happens |
|---|---|
| `docs/requirements/attestations.csv` | delete — **done** |
| `project-trajectory/registries/attestations.template.csv` | delete — **done** |
| [`check_trajectory.py`](../project-trajectory/scripts/check_trajectory.py) | **done, −193** (3991 → 3798): `ATTESTATIONS_CSV`, `ATTESTATION_DECISIONS`, `read_attestations`, `newest_attestations`, `attestation_findings`, `attestation_integrity_findings`, `staged_attestation_rewrite_findings`, `_report_attestations` and both `main` wirings. **KEPT** — `normative_text`, `sn_normative_text`, `digest`, `current_digests`, `_DIGEST_SEP`, `_DIGEST_EXCLUDED`: the anchor's engine, currently with **no writer**, so a dead-symbol sweep must not read them as unused. |
| [`trace.py`](../project-trajectory/scripts/trace.py) | **done, −51**: `_ledger_baseline` and the `_resolvable` guard that existed only to protect it. `_attested_baseline` is the git derivation alone again — which is what every caller was actually getting, the ledger having never held a row. It reads the row's own `HashedOn` when the anchor half lands. |
| [`intake.py`](../project-trajectory/scripts/intake.py) | **done, −85**: `next_att_id`, `record_attestations`, `_cmd_attest` and the `attest` subparser. The module drops **back under the 1500-line monolith threshold**. The flip path keeps a comment saying the anchor is still owed there; the re-stamp that writes it — and `attest` under its own name — return with the anchor half. |
| [`bootstrap.py`](../project-trajectory/scripts/bootstrap.py) | **done, −2**: the MAPPING row goes, so an adopter scaffolds no second attestation home. |
| `tests/test_attestation_ledger.py` (523 lines) | **rewritten, not deleted** — landed as [`../tests/test_attestation_digest.py`](../tests/test_attestation_digest.py), 4 tests. The digest-composition cases and the seam-blindness premise survive; the ledger-shape and append-only cases go, and the co-mutation cases arrive with the anchor half. |
| `tests/test_module_size_ratchet.py` | **done**: three baselines re-stamped **downward** and `intake.py`'s entry **deleted** (under threshold). `test_trajectory_staged.py` (cell classification) and `test_dogfood_sync.py` (header superset) are untouched — they belong to the **anchor** half, which is what adds columns. |
| [`registry-machinery-reference.md`](registry-machinery-reference.md), `project-trajectory/EXAMPLE.md`, `PROCESS.md` §7 | **not owed by the removal half** — verified: none of the three ever documented the ledger. They gain the anchor's fields with the anchor half. |
| `docs/okf/…`, `docs/architecture.md`, `docs/gate`, `open-items.html`, `PROJECT_STATE.html` | **done** — all regenerated, none hand-edited. |

**SR-140 is AMENDED, not rejected.** Its obligation stands; only the home
changes. It stays `Draft` and is ratified in its amended form at the sitting —
which means the sitting rules on the text D-1 produces, not on the text that
existed before it. **Amended 2026-08-09**, carrier-neutral: *"on the accepted
artifact's own row … never in a second registry keyed on the same artifact"*.
Its chain moved with it — **LLR-158** now names the four surviving digest
symbols and says plainly that the writer and the co-mutation guard are not
there yet, and **TC-153** points at the rewritten test module.
SN-029's own acceptance-intent clause naming the retired ledger file
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

### D-3 — a column name means ONE thing repo-wide; the shared semantics, ruled

**Owner ruling, 2026-08-09**, answering OI-13 in the general case rather than
the `Status` case: *"all registries should use common semantics."* A column
name is now a **repo-wide term**, not a per-registry label. Where two
registries carry the same name they carry the same meaning; where they need
different meanings they need different names. This subsumes OI-13's
recommendation (reserve `Status`, rename the rest) and extends it to every
colliding column in §6 F-9's matrix.

The owner's framing of the mechanism is worth keeping verbatim, because it is
the sharpest thing said about the registries this program: **these columns
should probably be interface definitions themselves.** They are contracts
between many readers, versioned, breakable — exactly what an IF row is for.
See "the irony, and the obstacle" below; the interfaces themselves are
**explicitly deferred** by the same ruling (*"we'll have to come back on the
interfaces"*).

#### Ruled semantics

| column | ruled meaning | change from today |
|---|---|---|
| **`Status`** | discrete, with per-tier overload — a **four-rung ladder**, revised 2026-08-09. **`Drafted`** = the id is allocated and **nothing else about the row may be validated against it**. **`Attested`** = the text has been attested valid. **`Ready`** = the row's discharge is in place — children for a decomposable tier, an existing test for a TC. **`Verified`** = the test passes; **TC only**. **SN carries the ladder on the same terms as every other tier.** | replaces `Draft`/`Verified`/`Modified` entirely. `Modified` leaves the authored set (Q5); `Verified` is **re-pointed to a new meaning** — see the word-reuse hazard in Q9 |
| **`Title`** | unchanged | none |
| **`Phase`** | an integer orienting a row to a campaign/programme; a **grouping attribute**. **Added to SN.** | new on SN; but see Q6 — it is *not* non-functional today |
| **`SR-Refs`** | unchanged — the same pointer shape it already has on LLR · IF · WI | none |
| **`Rationale`** | unchanged | but see Q8 — extending it to IF is what fixes OI-14 |
| **`Priority`** | a **float**, higher = work me first, negatives and decimals allowed. Ordering is **relative within a group only** — an SN's `1` is not comparable to an SR's `0`. | SR's `M`/`S`/`C` becomes a number (146 rows); WI's integer widens. See Q7 |

#### What the ruling leaves open, with recommendations

**Q5 · `Modified` has no place in the ruled ladder — recommend deriving it, not
authoring it.** Today's vocabulary is `Draft`/`Verified`/`Modified`; the ladder
names `Drafted`/`Attested`/`Ready`/`Verified` and has no rung for *"was blessed,
then the text moved."* The clean reading is that **`Modified` stops being a
value anyone writes**: with `TextHash` + `HashedOn` on the row, drift is
*computable* — recompute the hash, compare. That is strictly better than the
authored cell, which is a hand-maintained claim that can be false, and it is
the reason the anchor is being built at all.

Mechanically it is not a fifth rung but a **flag on `Attested` and above**: a
row is `Attested` (drifted) or `Ready` (drifted), and the drift is what sends
it back to the sitting. Rendering it as a status *value* would lose which rung
it fell from. Consequence to accept knowingly: a row at `Attested` or beyond
carrying **no hash** must be an *error*, not a silent pass — otherwise drift
detection is vacuous exactly where it matters.

**Q6 · `Phase` is NOT a grouping attribute today — this is a correction, not a
quibble.** The ruling says *"doesn't have a functional impact."* Measured, it
does: `derive_gate.py:145` and `trace.py:181` parse an integer out of it,
[`trace.py:1052`](../project-trajectory/scripts/trace.py#L1052) **filters the
SR set by phase**, `gen_release_checklist` groups the checklist by it, and
`check_trajectory` lists it among the required-field sets for all three spine
tiers. §6 F-3 classes it **mechanical**. So there are two different rulings
available and they should not be conflated: *(a)* add `Phase` to SN as the same
mechanical integer the spine already uses — cheap, consistent, recommended; or
*(b)* demote `Phase` repo-wide to advisory grouping — which is a real
migration touching gate derivation and phase-scoped selection, and needs ruling
on its own evidence. **Recommend (a)**; the ruling's *intent* (another grouping
axis, now available on SN) is satisfied by it without disturbing the gate.

**Q7 · `Priority` as a float is fine for SR and load-bearing for WI.** On SR
today it is `M`/`S`/`C` and F-3 classes its *value* **inert** — nothing reads
it — so a float is a free improvement there, costing one value migration over
146 rows. On WI it is **not** advisory: `schedule.py:495` parses it with
`_int(..., 0)` and `schedule.py:702` sorts the dispatch frontier on
`-wi["priority"]`, so it decides **what an agent picks up next**. A float still
works as a sort key, but `_int` must become a float parse or `1.5` silently
truncates to `1` — the quiet-wrong-answer failure this program keeps finding.
The "relative within a group" rule also needs its **group declared**: within a
registry is the natural reading and matches the owner's own SN-vs-SR example.

**Q8 · The shared-`Rationale` clause quietly fixes OI-14's root cause.**
Measured just now, the IF header is
`IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,Stability,Status,Component,Notes`
— **there is no `Rationale` column**, which is precisely why F-10 found design
narrative and defect history stuffed into `Contract` (27% of rows name a
`WI-###`). D-3's "same definition holds everywhere" makes `Rationale` available
to IF, and OI-14's recommended split — normative contract in `Contract`,
history and why elsewhere — stops being a judgment call and becomes a
**mechanical destination**. This is the strongest argument yet for ruling D-3
*before* OI-14 rather than after.

**Q9 · The test-case gray area — RESOLVED by the four-rung ladder, with one
overlap to fix and one hazard to avoid.** The owner's question was: a TC whose
text is attested but which cannot pass yet, because the implementation is owed
by an open WI. The revised ladder answers it *inside* `Status` rather than
beside it, and that works — the three axes this session identified map onto
three rungs exactly:

| axis | question | rung |
|---|---|---|
| 1 | is the **text** blessed? | `Attested` |
| 2 | does the **thing** exist — children, or a written test? | `Ready` |
| 3 | does it **pass**? | `Verified` (TC only) |

So the owner's case is `Attested`: text blessed, test not yet written, and the
WI DAG says who owes it. It advances to `Ready` when the test exists and to
`Verified` when it runs green. Nothing is stale and nothing lies.

**The ladder also dissolves an ordering trap**, which is the strongest argument
for it. `Attested` must be reachable **without** a discharge, or the process
deadlocks: an SN cannot have SR children before it is blessed, because SRs are
written *from* a ratified need at G1 — so a vocabulary where blessing implies
children makes the very first blessing illegal. Splitting "text blessed" from
"discharge in place" into two rungs is exactly what makes the first rung
legal, and it means the discharge is checked as a **transition into `Ready`**
rather than as a precondition of `Attested`.

**The overlap to fix — CONFIRMED by the owner 2026-08-09.** As given, `Ready`
said *"it should either have children or if it's a test case it should be
passing"*, and `Verified` said *"the test case passes"* — so for a TC the two
rungs said the same thing and one was empty. The reading that makes the ladder
monotone is that **`Ready` is the existence rung, not the passing rung**: for a
decomposable tier the discharge is *children exist*, and for a TC it is *the
test exists*. Passing is `Verified` alone.

The owner confirmed this and supplied the semantic argument for it: *"`Verified`
can imply the functionality is verified, when the column is just trying to say
the requirement has been fully decomposed and ready for the next stage."*
Exactly — which is why an SN/SR/LLR tops out at `Ready` and never reaches
`Verified`. **`Ready` means decomposed and handed on; `Verified` means proven by
execution, and only a test case can make that claim.**

**The hazard: `Verified` is being re-pointed to a new meaning on a column that
already holds 370 rows using the old one.** Today `Verified` means *ratified* —
111 SRs, 131 LLRs and 128 TCs carry it right now. Under the ladder it means
*the test passes*, and is illegal on SR and LLR entirely. A migration that is
interrupted, partial, or merged from a stale branch therefore leaves rows whose
`Verified` means the **opposite tier of claim** from its neighbours, and — this
is the sharp part — **nothing can tell them apart by inspection**, because the
cell is byte-identical either way. Every other value in the ladder is a new
word (`Drafted`, `Attested`, `Ready`) and is self-announcing on a half-migration;
`Verified` alone is silent. Two ways out, and the second is safer:

- migrate atomically, all 370 rows in one commit, with a check that refuses any
  `Verified` on an SR/LLR row; or
- **spend a different word for the new rung** — `Passing` or `Proven` — so that
  no value in the repo ever changes meaning, and a stray `Verified` anywhere is
  unambiguously an un-migrated row. **Recommended.** It costs one word and buys
  a migration that cannot silently half-apply, which is the failure mode this
  program has found in the machinery four times already.

Recorded because the ladder is otherwise clean, and because the objection is
about the *word*, not the design. With the owner's confirmation above, the
semantics are settled and **only the migration-safety question remains open**:
`Verified` is the right word for what a TC claims, and the sole argument
against keeping it is that reusing a word 370 rows already carry makes a
half-applied migration invisible.

**Q11 · Migrating the existing 370 rows onto the ladder — mostly derivable, with
one FAIL-OPEN that fixes the sequencing.** The mapping needs no re-judgment:
today's `Draft` → `Drafted`; today's `Verified` → `Attested`, then promoted to
`Ready` wherever the discharge check passes, which is a registry join the
scripts already compute. That is what keeps the P0 sitting **unblocked by
D-3** — the sitting is a human judgment and the vocabulary change is a
mechanical re-spelling of what it records.

The exception is **`Modified`, and it fails in the permissive direction.** 38
live rows carry it (25 SR · 6 LLR · 7 TC), meaning *was blessed, text has since
moved*. Under Q5 that state stops being authored and becomes derived from
`TextHash` — but **the hashes do not exist yet**. So a migration that retires
the word before the anchor is stamped has nothing to derive from, and a
migration that stamps the hash over each row's *current* text records those 38
rows as clean `Attested`. Their drift is not detected as resolved; it is
**laundered**, silently, in exactly the direction this program keeps finding.
Two exits:

- **Resolve the 38 at the sitting first**, then migrate — they are re-blessed,
  their text is current, and stamping the hash over current text is *correct*
  rather than concealing. This is already §5 step 3, so it costs nothing new.
  **Recommended.**
- Or seed each hash from the row's **baseline** revision rather than its
  current text, so the drift survives the migration and re-derives.

**This is a hard sequencing constraint, not a preference: the sitting must
complete before the ladder migration**, or 38 rows lose the only record that
they owe a re-blessing. §5 carries it.

#### Superseded reasoning, retained (the two-axis analysis, before the ladder)

The analysis below produced the axes the ladder now encodes, and is kept
because the reasoning is what a ruler needs. It argued the axes should live in
*different columns*; the owner's ladder puts them in *different rungs of one
column*, which achieves the same separation with less schema. The one
conclusion that survives intact is that **pass/fail must never be authored**:
whichever column it lands in, it is read from the harness.

The tension comes from the clause *"if it's a test case it should be passing"*,
which puts a **runtime fact** inside a **maturity cell**. Those want opposite
things: the text's maturity changes at a ratification sitting and should be
stable between them, while pass/fail changes on every commit and is owned by
the harness. Encoding pass/fail in `Status` would mean a human edits a
registry cell when CI goes red, and the cell is stale the moment it is written
— a hand-maintained duplicate of something already measured, which is the one
shape this kit refuses everywhere else.

The second axis **already exists and is already mechanical**: TC carries
`Automated` + `Evidence`, which §6 F-3 classes mechanical. So the recommended
reading is:

- **`Status` = is the test case's *text* blessed?** `Asserted` means "this is a
  correct statement of what must be proven" — a judgment a human makes once,
  and one that is *worth* making before the code exists, since a reviewed test
  case is a specification.
- **Passing = derived from evidence, never authored.** Whether it is green is
  read from the harness, at the moment it is asked.

Then the owner's case is **fully representable and entirely ordinary**:
`Status = Asserted`, evidence not yet green, and the WI DAG says which work
item owes the implementation. Nothing is lying, nothing is stale, and the gate
can still refuse to advance — because the gate reads the *evidence* axis, which
is exactly what it should be refusing on.

**The general form, which also answers the ordering trap.** `Asserted` is a
statement about the **text**; the discharge it demands — children, or a green
run — is an **obligation the row now carries**, checked at the **gate**, not a
precondition of asserting. It has to work that way or the process deadlocks:
an SN cannot have SRs before it is blessed (SRs are written *from* a ratified
need at G1), so "asserted ⇒ has children" would make the first assertion
illegal. So the honest state machine is `Draft` → `Asserted` (undischarged) →
`Asserted` (discharged), where **only the middle-to-last transition is
mechanical** and the TC gray area is simply the middle state having a name.

**Q10 · `Evidence` keeps its name — the rename is withdrawn by the owner, and
the definition is ruled.** *"A path to evidence, or a script that produces
evidence."* The withdrawn objection was that the cell holds a **location**
while the word promises **proof of execution** — the repo's own code agrees
with the objection three times over (`trace.py`'s finding calls it "a cited
**location**"; the reference doc calls it "pytest node / path / procedure
link"; `trace_text.PROVENANCE_COLS` groups it with `Module`/`CodeSymbol`/
`TestRefs` as "pointers by design"). The owner's rescission — *"if the test
case passes, the file path is providing the evidence"* — answers it, and the
ruled definition is what makes it coherent: the cell names **either the
evidence itself or the thing that produces it**, which covers a procedure doc
(`Automated=No`, evidence *is* the document) and a test node (`Automated=Yes`,
evidence is what running it emits). Under the ladder the word also stops
competing with anything, because axis 3 now has `Verified` and does not need
the noun.

**What survives the rescission, unchanged: the granularity gap.** It was never
really a naming problem. `check_doc_refs.registry_findings` validates only the
**file half** of the citation and rules the `::node` selector prose, so a TC
citing `tests/test_gen_trajectory.py` is satisfied by a file **54 other TCs
already guarantee exists**. That does not block `Attested` — but it makes the
`Attested → Ready` transition **unenforceable**, which is the one transition
the ladder just made load-bearing. So the selector check is now owed by D-3
itself rather than being an optional tightening: resolving the `::node`
selector (or, stdlib and stack-agnostically, confirming the selector token
appears in the cited file) is *how a row earns `Ready`*. Measured: 66 of 143
live TCs carry a selector today, so the majority of the work is already done in
the data and unenforced in the code. §6 F-12 records the measurement.

#### The irony, and the obstacle

The observation that these columns *are* interfaces is correct, and §6 F-2
already measured why it cannot be acted on today: **the IF registry has no
shape for a data vocabulary.** It models module↔module and module↔file seams —
of 95 rows, the five that mention `Status` all name it on the `Consumes` side,
and **no row provides it**, because there is nothing in the schema for "a term
that six readers agree on." Declaring D-3's semantics as IF rows would need a
second IF row *kind* (a vocabulary/contract row with no `Direction` and no
`Counterpart` in the module sense) — which is a change to what an interface
*is*, and lands squarely inside OI-14's "the IF registry has never had a
declared content contract." Correctly deferred by the ruling. Until then D-3's
table above is the declaration, and its enforcement home is a schema tier, not
an IF row.

### D-4 — supersession is DELETION, and ids are never reused

**Owner ruling, 2026-08-09.** *"For superseded: these need not live in the
registry. If something is superseded, it should just get removed."* A
superseded row is deleted rather than retained with a forwarding pointer. The
history of what it said and why it went lives where history already lives —
git, and [`log.md`](log.md)'s Decisions section — which is the same argument
D-1 made for retiring the attestation ledger: a registry states what **is**,
never what **was**.

**What this deletes.** `SupersededBy` is live-only on SR and also present on
CMP (§6 F-9), and it is not a passive cell — [`trace.py`](../project-trajectory/scripts/trace.py)
carries a whole validator for it across lines 470–553 (semicolon-list shape, no
repeats, target must exist, no self-link, **no cycles**), plus the
`PartOf`/`SupersededBy` rule at 2018–2027, and `check_trajectory` classifies it
**ratified** at 2932–2948. All of that goes. It also **closes §5's loose end**
about an adopting repo inheriting the superseded-SR integrity rules without the
column or its documentation — under D-4 there is no column to inherit, and the
rule "an LLR citing a superseded SR must re-ground" collapses into the orphan
check `trace.py` already runs, because a deleted SR is simply not there.

**The repo's doctrine already blesses the one cost.** Archived and historical
documents cite ids by design, and after a deletion those citations dangle.
`check_doc_refs` has ruled this exact case for *files* already — its docstring
says a historical document "naming a file that has since been retired is
accurate history, not a broken pointer; 'fixing' it would falsify the record."
D-4 extends that doctrine from files to ids, which is consistent rather than
new. Where a live document needs a forwarding pointer, the log entry that
recorded the supersession is it.

#### The id-reuse hazard — the owner's own objection, confirmed in code

*"The only remaining problem is if IDs get reused… perhaps there should be a
counter ticking up the unique IDs for the repo."* The concern is correct, and
it is **worse than it looks**, because every mint in this repo derives its
high-water mark from **what currently exists**:

- `intake.next_wi_id` is `max(existing) + 1` over spec **filenames**. Its
  docstring already shows the right instinct — *"a broader read than the
  loaders on purpose: for a MINT, an id held anywhere is an id taken"* — but
  "held anywhere" still means *held by a live file*. Delete the file and the id
  is free.
- `plan_artifacts` mints `DP-###` the same way, from directory names.
- **The spine has no mint at all.** Grepped for an `SR-`/`LLR-`/`TC-` id
  formatter across every script: there is none. Spine ids are allocated by a
  human or an agent reading the registry and adding one — so under D-4 the
  reuse guard is *a convention*, with no code to fix and nothing to fail.

An id is the join key of the entire traceability graph and the token every
commit message, log entry and archived document cites. A reused id does not
break a check; it silently **re-points history at a different meaning** — the
worst failure available in this repo, and undetectable by inspection.

**Recommended: a persisted high-water mark per id space, and mint from it —
never from the live set.** A single repo-wide counter would satisfy the rule
but costs readability (`SR-147` followed by `LLR-148`), so per-space marks give
the same guarantee while keeping ids readable. Two properties make it cheap and
safe: it is **machine-written, machine-read, never human-authored** — §6 F-3's
**anchor** class, the same one `TextHash`/`HashedOn` created, so it needs no
ratification and belongs in `_DIGEST_EXCLUDED` by the same argument — and it is
checkable with two rules that need no history: *the mark never decreases*, and
*no live id exceeds it*. Note this is worth doing **whether or not D-4 lands**:
today's mints are already reuse-prone the moment any row is removed for any
reason, and D-4 only makes removal routine.

**Sequencing:** D-4 must not ship before the watermark exists, or the first
supersession frees an id with nothing watching. The watermark is
carrier-independent and could ship with the removal-half class of work; the
`SupersededBy` deletion is a registry-schema change and belongs with OI-12's
migration.

---

## 3. The questions, and where each one went

**None of Q1–Q4 is still open as written** — §0 is the live list. This
section is the record of how each resolved, kept because the *reasoning* is
what a ruler needs and it does not survive compression:

- **Q1** (where the SN anchor fields live) — **withdrawn**, folded into
  **OI-12**: under a TOML carrier the distinction it asked about has no
  referent.
- **Q2** (does an SN get a `Status` cell) — **widened** into **OI-13**, once
  the IF registry turned out to carry the same disease worse.
- **Q3** (how far back the co-mutation guard compares) — **still genuinely
  open**, but it is a *build-time* decision for the anchor half, not a
  sitting decision; it needs no card.
- **Q4** (which SR-140 text the sitting rules on) — **answered and acted on**:
  D-1's amended, carrier-neutral text, which is why the removal half shipped
  before the sitting.

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
sub-question of D-2. **Filed 2026-08-09 as OI-13**, live on
[`open-items.html`](open-items.html), with three options — declare-don't-unify ·
reserve the word `Status` for ratifiable-artifact maturity and rename the rest
*(recommended, executed WITH OI-12 because both rewrite registry definitions)* ·
SN-half-only. Two things in that brief do **not** wait for the ruling: the IF
column is a *defect* (undeclared, overlapping, unread, yet handed to LLM
briefs), and taking SN-half-only must be a **knowing interim** rather than a
default. The SN half stays as recommended below; it is now the *smallest* part
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

1. ~~**The removal half of D-1.**~~ **DONE 2026-08-09.** Pure deletion, no data
   lost: `attestations.csv` + its template + its `bootstrap` MAPPING row gone;
   `check_trajectory` −195 (the three rungs, their two readers,
   `_report_attestations`, both constants, both `main` wirings); `trace` −51
   (`_ledger_baseline` and the `_resolvable` guard that existed only for it);
   `intake` −85 (`next_att_id`, `record_attestations`, `_cmd_attest`, the
   `attest` subparser) — which drops it **back under the 1500-line monolith
   threshold**, so its ratchet entry is deleted rather than re-stamped.
   `test_attestation_ledger.py` (523 lines) → `test_attestation_digest.py`
   (4 tests): the digest-composition cases survive, the ledger-shape cases go,
   and the **premise test survives and matters more** — it drives the
   amendment seam's blindness to a sanctioned amend+flip, which is why an
   anchor is owed at all.
2. ~~**SR-140 / SN-029 amended to carrier-neutral prose.**~~ **DONE
   2026-08-09**, with LLR-158 / TC-153. SR-140 now reads *"on the accepted
   artifact's own row … never in a second registry keyed on the same
   artifact"* and states the two-cell rationale (the commit is reviewable and
   diffable; the digest is what survives a squash, rebase or shallow clone) —
   no format named, so the sitting can ratify it before OI-12 is ruled.

**Three more items joined this block on 2026-08-09 with D-3/D-4.** Each is
needed under **every** carrier answer, touches no registry schema, and is
therefore not part of the work that gets built twice. This is the batch that
can start immediately — the answer to *"should implementation kick off from
here?"* is **yes, for these three and nothing else.**

3. **The id watermark — D-4's precondition, and worth doing regardless.** A
   persisted high-water mark per id space; mint from it, never from the live
   set. Today `intake.next_wi_id` and `plan_artifacts` both compute
   `max(existing) + 1`, and **the spine has no mint function at all**, so any
   removal — D-4's or otherwise — frees an id for silent reuse. Two checks
   carry it: the mark never decreases, and no live id exceeds it. F-3 *anchor*
   class (machine-written, machine-read), so it needs no ratification and joins
   `_DIGEST_EXCLUDED` for the same reason the other anchors do.
4. **The `::node` selector check — BLOCKED 2026-08-09, and it is an owner
   decision, not a build task.** It was recommended here before the ground was
   checked. Two findings, both verified in source, withdraw it from this block:

   - **It overturns a ruling.** Owner ruling **R2 of 2026-08-01** (WI-394)
     weighed exactly this: option (a) *build the resolver* against option (c)
     *the file half only*, and shipped (c). `_strip_node_selector`
     (`check_doc_refs.py:176-182`) discards the selector **by that ruling**, and
     **two named tests pin the behaviour** —
     `test_the_node_selector_half_is_ruled_prose_never_validated` and
     `test_registry_citations_whose_files_exist_pass`. The WI's own record says
     it in as many words: *"a builder must not pick this — the owner rules
     this."* [`enforcement-audit.md`](enforcement-audit.md):40 records the gap
     as **accepted**, *"recorded here so it is never implied as covered"*.
   - **The data is not ready for it.** Measured over the live registry: 302
     `Evidence` tokens, 212 carrying a selector, and **111 of those do not
     resolve in the file they cite** — 110 because the WI-277 test-module splits
     moved the tests out (`test_gen_trajectory.py` → `test_traj_*.py`,
     `test_trace.py` → `test_trace_rules.py`, `test_agent_loop.py` →
     `test_agent_loop_policy.py`) and one that exists nowhere
     (`test_a4_hub_fill_is_not_the_page_accent`, TC-119). **42 of 143 rows would
     turn red at once.** `docs/stack.ini`'s own comment on this step records the
     precedent against that: wiring at scale *"would have added a wall of warns
     to every gate run, which is exactly how a check earns the ignore."*

   **So the finding is real but the fix is not this.** What F-12 measured stands
   — `Attested → Ready` has no mechanism — but the ordering is now: **triage the
   111 stale selectors first** (that is data rot with no ruling attached, and it
   is what a reader of a `Ready` row is being misled by today), **then** ask the
   owner whether R2 is re-opened by D-3 having made that transition
   load-bearing. R2 was ruled before the ladder existed, which is a genuine
   change of premise — but it is the owner's to weigh.

   One measured fact for that decision: the cheap oracle is good enough. Over
   all 212 live selectors, *"the token appears as a word in the cited file"* and
   *"the token is defined as a `def` in the cited file"* **agree exactly, 0
   disagreements** — so no pytest dependency is needed, which was option (a)'s
   main cost. And the re-attest cost is zero: `Evidence` is a **traced** cell
   (TC's ratified set is `Method`/`Expected`/`Parameters`/`Level`/`Tier`).

   **Also found, and separately actionable: `check_doc_refs` is ALREADY RED and
   nobody sees it.** `--root . --strict` exits 1 today with 17 dangling and 1056
   untraced. It does not gate, for two compounding reasons: `[step:doc-refs]` is
   `gates = G3`, and this repo's derived gate is **G1** — where an open
   ratification window demotes every higher-gate step to *advisory, reported,
   exit code unaffected*. So a green harness proves nothing about this check,
   and anything built on it must be verified by running the script directly.
5. **The unpinned SN reader twin — and the two live defects under it.**
   `traj_parse._sn_rows` ↔ `gen_okf.sn_rows` are held equal by a docstring and
   nothing else. Scouted 2026-08-09, and the pin is the *smaller* half:

   - The two bodies are **byte-identical today**, and **both are wrong in the
     same two ways** — so `assert _sn_rows(r) == sn_rows(r)` is `True` right now
     over the real registry. A pure equality test would ship, go green forever,
     and change nothing. The precedent already knows this:
     `tests/test_rule_sync.py` pins behaviour equality **and** an absolute
     expected value on every rule.
   - **There is a THIRD copy.** `trace._sn_prose` carries the identical
     positional parse and feeds the `--ratify` sitting brief — the surface a
     human reads *before ratifying*. Its own docstring says all three change
     together.
   - **Defect A — FIXED 2026-08-09** (`3d8e3e3b`): SN-029's Why cell held
     `(`attended | single-ratify | autonomous`)`, two unescaped pipes, so the
     row was seven cells in a five-column table and its acceptance intent was
     read out of the middle of its Why column. Done now because SN-029 is still
     `Draft` and its raw line is its normative text — after the sitting the same
     edit is a ratified-cell amendment.
   - **Defect B — OPEN, and it needs a ruling rather than a patch.** The 10
     edge-case rows (SN-013…022) are a **four-column** table parsed with
     five-column indexing, so `need` reads the Lifecycle word
     (`docs/okf/stakeholder-needs/SN-013.md` is titled `"Provision"`) and
     `acceptance` is always empty. This is **known**, documented at
     `check_trajectory.py:3020-3025` — it is exactly why `sn_normative_text`
     hashes the raw line instead of a parsed projection. But routing the
     *digest* around it left the two surfaces an owner actually **reads** still
     rendering it. Fixing it means choosing what a four-column row maps to, in
     three copies at once, which is a rendering decision with more than one
     defensible answer — so it is surfaced, not picked. Promoted
   out of the loose-ends list because it is genuinely carrier-independent and
   has waited long enough.

### Owed by the owner — three filed rulings and one unfiled question

Indexed in §0; the sequencing argument is here.

- **OI-12 · the carrier.** Promoted from *rulable later* to **the gating
  decision**: Q1 folds into it and the anchor half waits on it. Recommendation
  unchanged in substance — TOML is the right destination — but the *sequencing*
  recommendation is withdrawn, because "defer it, nothing is foreclosed" was
  wrong about cost (§6 F-7).
- **OI-13 · `Status` across all six registries** (Q2 widened) — including
  [`interfaces.csv`](requirements/interfaces.csv)'s undeclared `Status` and its
  overlap with `Stability`. Recommendation is to reserve the word for
  ratifiable-artifact maturity and rename the rest, **executed together with
  OI-12**, since paying the registry-definition and downstream-migration cost
  twice is the same double-labour trap that reordered this plan.
- **OI-14 · the IF `Contract` cell**, and with it a schema tier for a registry
  that has none. Recommendation: **declare now, split gradually** — the
  declaration and the enum check cost nothing and fix the root defect (the cell
  has never had a stated purpose), while a 95-row prose sweep is where
  load-bearing maintainer knowledge gets quietly lost.
- **The component model — NOT FILED, deliberately.** §6 F-11 records it:
  membership is derived from the traced `LLR.Component` cell, so the partition
  moves with **no re-attest window**, and `cross_component_findings` makes that
  partition **decide how many IF rows must exist**. It is the loosest joint in
  the arrangement and it sits *upstream* of OI-14. Left unfiled because a fourth
  card would be an agent setting the sitting's agenda; **file it if the sitting
  agrees it is a decision rather than a consequence of OI-13/OI-14.**

**Ruling order: components → IF (OI-14) → `Status` (OI-13) → carrier (OI-12).**
Each earlier one bounds the next. OI-13 and OI-12 then *execute* together.

Q3 (how far back the co-mutation guard compares) and Q4 (which SR-140 text the
sitting rules on) are answered inline in §3 and need no separate act.

### Then, in order

6. **Hold the P0 sitting** — ratify / amend / reject SN-028…032 and their
   decomposition, and work the 25-row re-attest brief
   ([`ratify/2026-08-08-mechanized-loop.md`](ratify/2026-08-08-mechanized-loop.md)).
   Every ruling appends to [`log.md`](log.md)'s Decisions. **Not blocked by the
   anchor:** ratification is a `Status` flip, and the anchor records what was
   ratified. Stamping afterwards leaves the sitting-to-stamp window
   unprotected, which is **no worse than today** — the ledger has never held a
   row. **Not blocked by D-3 either** — the ladder is a mechanical re-spelling
   of what the sitting records (Q11). But it **must precede** the ladder
   migration: the 38 `Modified` rows have no hash to derive their drift from,
   so migrating first launders it (Q11).
7. **Build the anchor half of D-1, plus D-2, and the D-3/D-4 schema changes,
   ONCE** — on the carrier OI-12 rules — and stamp what the sitting accepted.
   This is the batch that gets built twice if it starts early: the ladder's
   values, the `Priority` float, `Phase` on SN, the `SupersededBy` deletion and
   its ~80-line validator, and every test that asserts a column shape.
8. **Regenerate the derived artifacts** — `docs/gate`, `open-items.html`,
   `PROJECT_STATE.html`, the OKF export — and confirm the gate rises to its
   honest ceiling. A gate that does *not* rise is a finding, not a nuisance.
9. **Drain or dispose the open frontier** — WI-390, WI-415, WI-422, WI-423,
   WI-424. WI-424 (route the adjudicator briefs) carries its own two decisions;
   see the handoff's §4.
10. **Dispose the warn-only residue** — the handoff's §5 list, each either fixed
   or recorded as accepted. "Known and accepted" is a disposition; "still there"
   is not.
11. **Full bar green, stated with real output**: `pytest -q -n auto` unfiltered,
   `check.py` at the derived gate, `check_trajectory.py --strict` unfiltered.
12. **Merge to `main`** — an owner act (`push = "human"`), and the standing
   deliberate item [`status.md`](status.md) already carries.

Locked = the rulings made, 1–12 done, `drafts=0 modified=0`, and this file
archived.

### Loose ends this program surfaced, owed to no step above

- ~~**The unpinned SN reader twin.**~~ — **promoted to §5 step 5**, the
  ship-now block, because it is carrier-independent and has waited long enough.
- **`status.md`'s ratification-level prose is stale** — it still says the level
  is `autonomous`, a value [`process.toml`](process.toml) *deleted* in favour of
  `human_ratification_through = 0`. Hand-authored owner prose; flagged, not
  edited.
- **`status.md` is ~449 lines against a 120-line warn budget** — pre-existing
  and warn-only; this file is meant to absorb some of that depth and has begun
  to (the sitting's owed-work bullet now points here rather than restating it).
- ~~**`SupersededBy` is live-only on the SR registry**~~ — **CLOSED by D-4**:
  the column is deleted rather than documented, and the integrity rule it
  carried collapses into the orphan check, because a superseded row is simply
  not there. What the loose end becomes is D-4's **precondition**: the id
  watermark must exist before any row is deleted.
- **OI-12's card carries two stale claims**, and it is the surface the sitting
  reads. Its `BlastRadius` cell still names `TextDigest` / `AcceptedCommit`
  (renamed in §2 D-1), and — the one that matters — it still asserts *"ruling
  this later forecloses nothing"*, which the owner **corrected on 2026-08-09**
  and §6 F-7 now records as true of the design and **false of the labour**.
  Left unedited on purpose: `open-items.csv` is freshness-gated against
  [`open-items.html`](open-items.html), so the fix lands **with** a
  regeneration, and rewriting a pending decision's own brief is a change the
  owner should see rather than find already made.
- **`Priority` names two incompatible vocabularies** — `M`/`S`/`C` on an SR, a
  scheduler integer on a WI, neither enum-checked (§6 F-9). Smaller than OI-13
  and the same shape of defect.

---

## 6. Reference findings

Compiled 2026-08-09 by reading source, in answer to the owner's questions
across this session: what the `Status` options are and whether they are an
interface (F-1, F-2); which registry columns drive machinery versus feed an LLM
versus do nothing (F-3, F-4); the digest's width (F-5); whether markdown or
TOML could carry the registries (F-6, F-7); where a design constraint lives
(F-8); whether template and live headers agree (F-9); what the IF `Contract`
cell encodes (F-10); and how components are defined, which turns out to bind
the other three (F-11).

The per-field mechanical detail already has a home —
[`registry-machinery-reference.md`](registry-machinery-reference.md) §2–§5, §10,
§12 — and is **not** restated here. Only what changes a decision is.

**Index:** F-1 six `Status` carriers · F-2 the vocabulary is not an interface ·
F-3 four column classes · F-4 the inert class · F-5 the digest's width ·
F-6 no markdown-table reader · F-7 TOML as one carrier · F-8 constraints have
no home · F-9 template↔live headers + the cross-registry matrix · F-10 what IF
`Contract` encodes · F-11 components bind all three · F-12 the TC existence
claim is checked at file granularity only.

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
| **anchor** *(new, D-1)* | machine-written, machine-read, never human-authored | `TextHash`, `HashedOn` |

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

**The width lever is the prefix, not the alphabet** (added 2026-08-09 with the
encoding question in §2). Encoding the same 64 bits denser saves at most six
characters — base32 13, base64url 11, Ascii85 10, against hex's 16 — while
`sha256:` costs seven on its own. So the two honest levers are dropping the
prefix (which today is the *only* shape check there is, `.startswith("sha256:")`
— so it cannot go without replacing that check) and dropping the carrier
constraint entirely by moving to TOML, where the key name carries what the
prefix was carrying. §2 records the ruling: **keep lowercase hex.**

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

**F-9 · Template↔live headers all match; the alignment questions are BETWEEN
registries, not between a registry and its template.** Audited 2026-08-09
before the owner's CSV review. Every shipped registry's live header is an
ordered superset of its template, as `tests/test_dogfood_sync.py` requires, and
`stakeholder-needs.md`'s three markdown tables match the template column for
column (its sections are ordered Core / Draft / Edge-case against the
template's Core / Edge-case / Draft, which is mechanically irrelevant —
section-as-state matches a heading *containing* "draft"):

| registry | template | live | verdict |
|---|---|---|---|
| **SN** | Core 5 · Edge-case 4 · Draft 5 | identical | match |
| **SR** | 12 | 13 | ordered superset — one live-only extra, `SupersededBy` |
| **LLR** | 11 | 11 | exact |
| **TC** | 11 | 11 | exact |
| IF | 11 | 11 | exact |
| CMP | 9 | 9 | exact |
| OI | 12 | 12 | exact |

Two asymmetries worth naming rather than filing. `SupersededBy` being
**live-only on SR** is legal under the superset rule, but an adopting repo
inherits the *rules* — including the integrity-class "an LLR citing a
superseded SR must re-ground" — **without the column or its documentation**
(reference doc §12.9). And `work-items.template.csv` still ships with **no live
counterpart**: the WI registry became the `docs/work/` spec folder at the Phase
2c flip, and the template survives only as the legacy format `wi_convert.py`
migrates *from* — deliberately excluded from the sync census, so do not read it
as a live schema.

**Where the columns actually collide** — the cut that matters for a
cross-registry review:

| column | appears in | note |
|---|---|---|
| **`Status`** | **SR · LLR · TC · IF · OI · WI** (6) | one word, six vocabularies — **OI-13** |
| `Title` | SR · LLR · OI · WI | |
| `Phase` | SR · LLR · TC | |
| `SR-Refs` | LLR · IF · WI | the same pointer shape in three registries |
| `Rationale` | SR · LLR | |
| **`Priority`** | SR · WI | **two incompatible vocabularies under one name** — `M`/`S`/`C` on an SR, a scheduler integer on a WI; neither is enum-checked |
| `SupersededBy` | SR · CMP | |
| `Component` | LLR · IF | |
| `Notes` | IF · CMP | |

And a seventh `Status` vocabulary hides from a grep: **CMP calls it `State`.**

**F-10 · What the IF registry's `Contract` cell actually encodes** — owner
question, 2026-08-09: *"the prose in IF appear to be requirements, when it is
intended to be interface definitions."* Measured over all 95 live rows:

| signal | rows | share |
|---|---|---|
| names a `WI-###` (history) | 26 | 27% |
| cites another IF/SR/LLR/TC id | 13 | 14% |
| names a callable signature | 12 | 13% |
| carries a rationale connective (*because*, *rather than*, *so that*) | 10 | 11% |
| narrates a past defect or incident | 9 | 9% |
| **uses `shall`/`must` (requirement voice)** | **1** | **1%** |

Length: median 260, mean 323, max 968 characters; 21 rows over 500. In the
five longest cells, **history/incident sentences outnumber everything else**.

**The reading is right, with one correction.** They are *not* requirements in
the shall-statement sense — 1% — and §8's backing rule holds mechanically:
**zero** rows have an empty `SR-Refs`, so every seam does hang off a real
requirement. What the cells actually carry is **design narrative**: what a
module does across a seam, which WI split it from what, and what defect the
shape was chosen to avoid. That is closer to `architecture.md` prose than to a
contract in the interface-specification sense (signature, types, error modes,
what a `Version` bump would mean).

Three reasons that matters, and one reason it is defensible:

- The `Provides` side is meant to hold *the authoritative spec*, and a consumer
  "pins the version" — but nothing in the cell says which part is the pinned
  obligation and which is background, so `Version` bumps against an unstated
  baseline.
- 27% naming a `WI-###` **duplicates `log.md`**, and a WI id ages: a cancelled
  row's id sitting in a `Contract` cell still reads as authority.
- It is fed **verbatim to LLM planning briefs**
  (`plan_briefs.IF_SURFACE_COLUMNS` carries `Contract`), so history sentences
  spend brief budget without constraining behaviour — and mix narrative with
  normative statement in a prompt.
- *Defensible, though:* the kit is stack-agnostic, so a signature cannot be
  demanded (a seam may be a file format, a CLI, or an external actor), and the
  IF row has **no `Rationale` or `Detail` column**, so the "why" has nowhere
  else in the row to go. The content is not misjudged so much as **unfiled**.

Nothing validates any of it — `--strict-schema` covers SR/LLR/TC only, so the
IF registry has **no schema tier at all**. Together with OI-13's finding (an
undeclared `Status` overlapping `Stability`), the honest summary is that **the
IF registry has never had a declared content contract of its own**. **Filed
2026-08-09 as OI-14** — its own row rather than more scope on OI-13, because
that is a cross-registry *vocabulary* question and this is a single-registry
*content* question, ruled by different reasoning. Recommendation: **declare
now, split gradually** — write the content contract and add IF a schema tier
(`Stability` enum-checked, `Contract` required) immediately, then let the
history/rationale migrate per row as rows are touched, never as a 95-row sweep
nobody can review carefully.

**F-11 · The three open items are coupled through the COMPONENT partition, and
that is the piece with no OI of its own.** `check_trajectory.cross_component_findings`
(WI-064) makes an import edge between two components a finding **unless a
covering `IF-###` row exists** — so the CMP partition *determines how many IF
rows must exist*. How components themselves are defined is a two-part answer,
and only the first part is authored:

- **Declared** — one hand-written row per component in
  [`requirements/components.csv`](requirements/components.csv): `CMP-ID`,
  `Name`, `Category`, `Knowledge` (skill / pack refs), `State`,
  `SupersededBy`, `PartOf` (nesting), `DetailDoc`, `Notes`. Five rows live,
  all `State=built`, none nested.
- **Derived, and deliberately never restated** (the shipped template says so in
  its own `Notes`: *"Structure is DERIVED, never restated here"*) —
  **membership** comes from the **`LLR.Component` tag joined on `LLR.Module`**
  (`module_components`), so the registry declares the *set* and the LLR rows
  declare *what is in it*; `PartOf` is inverted to `children_of` and resolved
  upward to `roots_of`; and the **top view** is `top_roots` (roots containing
  ≥1 module) plus `uncontained` (arch-map modules tagged into nothing),
  measured against the inventory scraped from the **generated**
  `docs/architecture.md` module map.

Live: **53 arch-map modules → 5 components → 0 uncontained**, top view 5
against a bound of 10. Note `LLR.Component` is a **traced** cell, so re-tagging
a module's component opens no re-attest window — the partition can move
without a sitting, and moving it changes which IF rows are owed.

So the reading order for the sitting is **components → IF → `Status`**:
OI-14 assumes today's 95 IF rows are the right 95, and that assumption rests on
a component model nobody has ruled.

**F-12 · A TC's claim to have a test is checked at FILE granularity, and the
finer pointer is already being hand-written into the wrong column.** Measured
2026-08-09 over the 143 live TC rows, answering the owner's *"nothing here
indicates if the test itself actually exists."*

Two checks touch the claim and neither reaches it. `trace.py:837` requires that
`Automated=Yes` cite a non-empty `Evidence`. `check_doc_refs.registry_findings`
(WI-394) then checks that the cited path exists — but **only the file half**;
its own comment rules the `::node` selector prose, because resolving a node id
means running the project's test runner, which is stack-specific. So:

| | |
|---|---|
| TCs citing `Evidence` | 143 of 143 — none blank |
| cited files that do not exist | **0** |
| TCs carrying a `::node` selector | **66 of 143** — unchecked even where present |
| distinct files cited | 76 |
| files cited by more than one TC | 27, carrying 208 citations |
| most-shared file | `tests/test_gen_trajectory.py`, cited by **54** TCs |

The concrete hole: cite `tests/test_gen_trajectory.py`, never write the test,
and every check stays green — 54 other TCs already guarantee the file exists.
This is the F-4 inert-cell family, but **half-enforced is worse than inert**: a
reviewer sees WI-394 wired up and reasonably concludes the claim is covered.

**And the missing granularity is already being written by hand, in
`Parameters`.** The template declares that column as an input recipe
(`param=a; other=x`) and the reference doc calls it "the artifact recipe in the
critique brief. Not validated." Its one mechanical consumer is
`agent_loop.py:718`, which lifts it into the critique brief and scans it for
`docs/rubrics/*.md` paths to inline (narrowly scoped — test `.py` paths are
**not** slurped; verified). Measured: filled on **24 of 143** rows; of those,
**1** uses the declared `key=value` shape and **24 contain a repo path** —
TC-103's reads `tests/test_gen_trajectory.py fixture tiered_repo(TIER_UNION_WIS)`.
Authors felt the gap and filled the nearest cell. Two costs follow: the value
is unvalidated free prose, and `Parameters` is classified **ratified**, so
correcting the drift is a re-attestation rather than a cleanup.

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
- **2026-08-09** — **brought current for a separate review session** (owner:
  *"I'll likely review them separately and chew through them in a separate
  session"*). Added **§0**, a start-here index of the four things awaiting a
  decision with the ruling order and the recommendation for each; refreshed §1
  onto `b2507c8c` with the four commits this program landed; widened §5's
  owner block to name OI-14 and the unfiled component question; and gave §6 an
  index plus a preamble mapping each finding to the question that produced it.
  Two loose ends promoted out of prose into §5's list — SR's live-only
  `SupersededBy` and `Priority`'s two vocabularies. **The document is now
  readable cold, top to bottom, with no reference to this session's chat.**
- **2026-08-09** — §6 gained **F-9** (template↔live headers all match; the
  real collisions are *between* registries — the cross-registry column matrix,
  `Priority` meaning two incompatible things, and CMP's `State` as a seventh
  `Status` vocabulary that hides from a grep) and **F-10** (what the IF
  `Contract` cell actually encodes, measured over all 95 rows: design narrative
  and history, 1% requirement voice, 13% callable signatures — the owner's read
  upheld with one correction, since every row does have a real `SR-Refs`).
  F-10's conclusion — the IF registry has never had a declared content contract
  — is **filed as OI-14** (declare now, split gradually, never a 95-row sweep).
  §6 also gained **F-11**: the three open items are coupled through the
  **component partition**, which decides how many IF rows must exist and has no
  OI of its own — so the reading order is components → IF → `Status`.
- **2026-08-09** — **D-1's removal half SHIPPED** (§5 step 1–2, struck through
  there). ~331 lines deleted across four modules, two registry files removed,
  the test module rewritten around what survives, and SR-140 / LLR-158 /
  TC-153 / SN-029 amended to carrier-neutral prose. Three ratchet baselines
  re-stamped **downward** and `intake.py`'s entry **deleted** — it fell back
  under the monolith threshold, which is what this repo's own rule requires
  rather than leaving the old number standing as headroom. One thing to know
  before touching `check_trajectory` next: `normative_text`,
  `sn_normative_text`, `digest` and `current_digests` now have **no writer** —
  they are the anchor's engine waiting on OI-12, and an unreferenced-symbol
  sweep (WI-422) must not read them as dead.
- **2026-08-09** — committed at `9b6c7fc0` (this file + OI-12 + the regenerated
  owner surface). **OI-13 filed**: what `Status` means across all six
  registries, recommended for execution *together with* OI-12. Q2 now points at
  it; §5's owner-rulings block names it.
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
- **2026-08-09** — **the ladder's rungs confirmed, and the plan re-cut around
  what can actually start.** The owner confirmed `Ready` as the terminal rung
  for SN/SR/LLR with the semantic argument for it — *"`Verified` can imply the
  functionality is verified, when the column is just trying to say the
  requirement has been fully decomposed and ready for the next stage"* — so
  `Ready` means decomposed-and-handed-on and `Verified` means proven-by-
  execution, which only a TC can claim. The semantics are now settled and the
  only open question about the word is **migration safety** (Q9). **Q11 added**:
  the 370-row migration is derivable (`Draft`→`Drafted`, `Verified`→`Attested`
  then promoted to `Ready` where the discharge check passes), which is what
  keeps the sitting unblocked by D-3 — **except `Modified`**, whose 38 rows have
  no hash to derive drift from, so migrating before the sitting **launders**
  their owed re-blessing. That makes "sitting before ladder migration" a hard
  sequencing constraint, now carried in §5. §5 also gained **three
  carrier-independent steps that can start now** (the id watermark, the
  `::node` selector check, the SN reader twin) and folded the D-3/D-4 schema
  work into the build-once step; the checklist renumbered to 1–12.
- **2026-08-09** — **`Status` revised to a four-rung ladder, and D-4 ruled.**
  The vocabulary is now `Drafted` (id allocated, nothing validated against it)
  → `Attested` (text attested valid) → `Ready` (discharge in place — children,
  or an existing test) → `Verified` (the test passes; **TC only**). This
  **resolves Q9's gray area inside `Status`** rather than beside it: the three
  axes this session separated — text blessed, thing exists, thing passes — are
  three rungs, and the owner's case (attested text, unwritten test) is simply
  `Attested`. It also dissolves the ordering trap, since `Attested` is
  reachable without a discharge and the discharge is checked as the transition
  into `Ready`. **Two corrections recorded:** as given, `Ready` and `Verified`
  said the same thing for a TC, so `Ready` is read as the *existence* rung;
  and **`Verified` re-points a word 370 live rows already carry with the old
  meaning**, which a half-applied migration cannot announce — recommend
  spending a fresh word (`Passing`/`Proven`) instead. **Q10** records the
  withdrawn `Evidence` rename (owner: *"if the test case passes, the file path
  is providing the evidence"*) and the ruled definition — a path to evidence,
  or a script that produces it — while noting the **granularity gap survives
  the rescission** and is now load-bearing, because it is what makes
  `Attested → Ready` enforceable. **D-4**: a superseded row is deleted, not
  retained — which deletes `SupersededBy`, its ~80-line validator in `trace.py`,
  and **closes §5's live-only-`SupersededBy` loose end**. Its hazard is the
  owner's own and confirmed in code: every mint here is `max(live) + 1`, and
  **the spine has no mint function at all**, so a deletion frees an id for
  silent reuse. Recommend a persisted per-space high-water mark — F-3 *anchor*
  class, machine-only — as a **precondition** of D-4, worth doing regardless.
  §6 gained **F-12**: the TC existence claim is checked at file granularity
  only (66 of 143 rows carry an unchecked `::node` selector; one file is cited
  by 54 TCs), and the missing granularity is already hand-written into
  `Parameters` — 24 of 143 filled, 24 carrying a repo path, **1** matching that
  column's declared `key=value` shape.
- **2026-08-09** — **D-3 ruled: a column name means ONE thing repo-wide.**
  Shared semantics fixed for `Status` (discrete with per-tier overload;
  `Draft` = id allocated and nothing else validated against it, `Asserted` =
  text asserted valid and a discharge now owed; **SN carries it like every
  other tier**), `Title`, `Phase` (integer campaign grouping, **added to SN**),
  `SR-Refs`, `Rationale`, and `Priority` (**float**, higher = first, negatives
  and decimals legal, comparable only within a group). Recorded with five
  consequences the ruling leaves open (Q5–Q9 in §2): `Modified` should become
  **derived from the hash rather than authored**; `Phase` is **already
  mechanical** and demoting it is a separate migration — flagged as a
  correction; `Priority` is inert on SR but **drives the WI dispatch frontier**,
  so the float needs a float parse in `schedule.py`; the shared `Rationale`
  gives IF the column it lacks and thereby **fixes OI-14's root cause**; and
  the **test-case gray area dissolves** once `Status` (text maturity) and
  `Automated`/`Evidence` (pass/fail) are read as the two axes they already are
  — `Asserted` but undischarged is an ordinary, fully representable state, and
  discharge is checked at the **gate**, never as a precondition of asserting,
  or the first assertion of an SN would be illegal. The owner's framing that
  **these columns are themselves interfaces** is recorded and correct;
  acting on it is blocked by F-2 (the IF registry has no shape for a data
  vocabulary — no row *provides* one) and is deferred with the interfaces.
- **2026-08-09** — **the anchor cells renamed before they exist**, owner
  direction: `TextDigest` → **`TextHash`**, `AcceptedCommit` →
  **`HashedOn`** (via an intermediate `BaselineCommit`, rejected for naming
  the machinery's *use* of the value rather than the value itself). The second
  is the substantive one — the old name
  overclaimed, since a commit is a repo-wide snapshot and not an act of
  accepting this row's text, while the cell's actual job (and the job
  `trace._attested_baseline` / `_rows_at` already give it) is to say *where the
  diff starts*. Free to do now: outside this document the names survive only in
  the handoff and one ratchet bump-comment, both historical records left as
  written. **Open follow-up:** OI-12's `BlastRadius` cell still names the old
  pair — see §5's loose ends. D-1 also gained the measured answer to *"can a
  denser encoding shrink the hash?"* — **no, keep lowercase hex**: the best
  alphabet change saves six characters while the `sha256:` prefix costs seven,
  and non-hex forfeits case-insensitive comparison and eye-grepping against a
  `git show`. §6 F-5 gained the same measurement.
- **2026-08-09** — D-1 gained the **adjudicator recovery procedure** for the
  degraded mode (digest trips, `HashedOn` unresolvable after a squash /
  rebase / shallow clone): treat the row as a first ratification, read the
  SR / LLR / TC chain as *semantic* evidence that the meaning survived — an
  adjudicator judgment, deliberately never a scripted check, since it inverts
  the trace direction — and check the forge / unpruned remotes for the
  pre-squash text before giving up on a diff. Owner-proposed; closes the
  "the hash only says *changed*, not *what changed*" objection honestly
  rather than pretending the digest can answer it.
- **2026-08-09** — §6 gained **F-7**: TOML as one carrier for all four tiers.
  Strongest technical option raised; `tomllib` is stdlib, the repo already
  writes TOML two ways, and it has run this exact migration once (work-items.csv
  → the `docs/work/` spec folder). **Deferred to a successor program, not
  refused** — D-1/D-2 are carrier-neutral fields, so shipping them forecloses
  nothing. F-6 also gained the measurement: 32 SN rows cost ~166 code lines to
  read, 436 CSV rows cost five.
