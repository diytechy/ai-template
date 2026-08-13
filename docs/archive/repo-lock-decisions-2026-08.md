# The lock program — archived decision record, August 2026

**What this is.** The full reasoning behind the lock program's **executed**
decisions, plus the reference findings and the running log that produced them.
It was moved here from [`../repo-lock.md`](../repo-lock.md) on **2026-08-11**
so that file could go back to being what it claims to be: a statement of what
is still owed, not an archive of what was already settled.

**What it is not.** Not a working surface, and not a place decisions are made.
Every ruling below is DONE. The live ones — and the checklist of what remains —
stay in `repo-lock.md`, which keeps a one-line pointer at each heading here.
Where source code cites a decision by id (`repo-lock D-5`, `D-7`, …), the id
still resolves in `repo-lock.md`; the reasoning is here.

**Why keep it at all.** Two reasons this repo has learned the hard way. The
overturned claims are where the reasoning is still worth having — every one of
them cost real work (§7). And a decision whose *why* is lost gets re-litigated
by the next reader, which is the cost the D-7 evidence ledger was built to
measure.

---

## Executed decisions, in the order they were ruled

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

**The removal half is DONE** (the full per-file inventory is in git). What a
future reader needs from it is one warning: `check_trajectory` KEPT
`normative_text`, `sn_normative_text`, `digest`, `current_digests`,
`_DIGEST_SEP` and `_DIGEST_EXCLUDED` — the anchor's engine, currently with **no
writer**, so a dead-symbol sweep must not read them as unused. `intake.py` fell
back under the 1500-line monolith threshold and its ratchet entry was deleted
rather than left standing as headroom.

**Still owed with the anchor half:** the two cells, `_DIGEST_EXCLUDED`, the
third cell class, the co-mutation guard, the template columns, and
`test_dogfood_sync`'s header rule. All carrier-exposed, so all waiting on OI-12.

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

> **Correction, 2026-08-10.** That pass was **half-applied, and this paragraph
> overstated it.** It amended SN-029's *acceptance-intent* cell and **missed the
> Need cell**, which went on saying what was ratified is "recorded in an
> append-only ledger" — leaving the row contradicting itself, since its own
> acceptance intent already read "never in a second registry keyed on the same
> artifact." `git log -S"append-only ledger"` shows the string entered at
> `cb9c36ac` and no commit removed it. Closed at the P0 sitting, where the owner
> reframed the row around impact rather than mechanism; see the Decisions entry
> in [`log.md`](../log.md). The lesson generalizes and is the reason this is
> recorded rather than quietly fixed: **an amendment that edits one cell of a
> multi-cell row has not amended the row**, and nothing mechanical was checking
> the other cells for the retired name.

### D-2 — stakeholder needs gain FIELDS rather than a new carrier

**Owner direction, 2026-08-09**, given with D-1 and answering its one unsolved
weakness (the third option "still leaves SNs — no row, no columns — unsolved"):
extend [`stakeholder-needs.md`](../requirements/stakeholder-needs.toml) with
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
| **`Status`** | ~~a **four-rung ladder** — `Drafted` / `Attested` / `Ready` / `Verified` (TC only)~~ **SUPERSEDED 2026-08-11 by D-9: THREE rungs, `Drafted` → `Approved` → `Founded`, uniform across all four tiers.** The reasoning below stands and is why D-9 went the way it did; the *words* and the fourth rung did not survive. `Attested`→`Approved` (collision with the `Attest` verification method), `Ready`→`Founded` (ambiguity, and it never fit a TC), and the pass rung is **deleted** rather than renamed — pass/fail is run, never recorded. **SN carries the ladder on the same terms as every other tier.** | replaces `Draft`/`Verified`/`Modified` entirely. `Modified` leaves the authored set (Q5); `Verified` **leaves the vocabulary altogether**, which is what dissolves Q9's word-reuse hazard |
| **`Title`** | unchanged | none |
| **`Phase`** | an integer orienting a row to a campaign/programme; a **grouping attribute**. **Added to SN.** | new on SN; but see Q6 — it is *not* non-functional today |
| **`SR-Refs`** | unchanged — the same pointer shape it already has on LLR · IF · WI | none |
| **`Rationale`** | unchanged | but see Q8 — extending it to IF is what fixes OI-14 |
| **`Priority`** | a **float**, higher = work me first, negatives and decimals allowed. Ordering is **relative within a group only** — an SN's `1` is not comparable to an SR's `0`. | SR's `M`/`S`/`C` becomes a number (146 rows); WI's integer widens. See Q7 |
| **`Evidence`** | **where the proof lives** — a pointer. A test file, a node id, a procedure doc. | unchanged, and see below: it must stay a *traced* cell |
| **`Method`** | **how you obtain the proof** — normative prose. Drive the cited test, or perform the procedure. | unchanged; it must stay a *ratified* cell, and must NOT hold the pointer |

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
[`trace.py:1052`](../../project-trajectory/scripts/trace.py#L1052) **filters the
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

**The one conclusion from the pre-ladder analysis that survives:** pass/fail
must never be AUTHORED. Whichever column it lands in, it is read from the
harness — a hand-maintained duplicate of something already measured is stale the
moment it is written, and would mean a human edits a registry cell when CI goes
red.

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

**Q12 · `Method` vs `Evidence` — ruled 2026-08-09, and the reason is mechanical
rather than aesthetic.** The owner's framing: *"the method indicates how to get
the evidence (whether driving the evidence pointer test file, or performing a
procedure)"*, with the follow-up — if a test is automated, should `Method` hold
the pointer and `Evidence` go blank?

**Ruled: no. The pointer stays in `Evidence`.** The two columns sit on opposite
sides of the attestation split, and that is what decides it:

- `Evidence` is a **traced** cell — a pointer, not in the digest. Changing it
  opens **no re-attest window**.
- `Method` is a **ratified** cell (TC's ratified set is `Method` · `Expected` ·
  `Parameters` · `Level` · `Tier`) — normative text, hashed into the row's
  attestation.

So today, renaming a test file or splitting a test module is free. Move the
pointer into `Method` and every such rename becomes a ratified-cell amendment.
Not hypothetical: WI-277's test-module splits moved **110** cited tests, which
under that arrangement would have been 110 re-attestations for work that changed
no requirement. The current split is the right one and is a cleaner statement of
the owner's own model than the columns currently manage: **`Evidence` = where the
proof lives (cheap to change); `Method` = how you obtain it (expensive to
change).**

**What is actually wrong is that `Method` is unvalidated.** It is a required
non-empty field (`trace.py:267`) whose value *is never checked* — the reference
doc says so outright. It is then rendered to humans and models in five surfaces:
the traceability graph node label (`trace.py:946`), the `--ratify` sitting brief
(`trace.py:1571`), the OKF export, the release checklist and the dashboard — and
`agent_loop.py:725` scans it for `docs/rubrics/*.md` paths and **inlines those
files into critique briefs**, so a path written there has a real side effect.
Required, normative, LLM-facing, and unvalidated is how pointers leaked into it
and into `Parameters` (§6 F-12: 24 of 143 `Parameters` cells filled, 24 holding a
repo path, **1** matching that column's declared shape).

**And it settles the selector question by making it unnecessary.** `Ready` means
the test exists; `Evidence` naming a file answers that. So D-3 does **not** make
the `::node` selector load-bearing, ruling **R2 stands**, and what remains is not
a missing check but **stale data**: 111 of 212 selectors name a test that has
moved. Since `Evidence` is traced, repointing them costs no re-attestation.

**Accepted knowingly:** file granularity means a TC can reach `Ready` on a file
that exists for another TC's sake — 32 rows cite `tests/test_gen_trajectory.py`.
`Ready` is a staging signal, not per-test assurance.

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
git, and [`log.md`](../log.md)'s Decisions section — which is the same argument
D-1 made for retiring the attestation ledger: a registry states what **is**,
never what **was**.

**What this deletes.** `SupersededBy` is live-only on SR and also present on
CMP (§6 F-9), and it is not a passive cell — [`trace.py`](../../project-trajectory/scripts/trace.py)
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

### D-5 — ONE TOML CARRIER for all four tiers, and it runs FIRST

**Owner ruling, 2026-08-10**, answering OI-12 with option (b) and overriding
that row's own *"sequence it as its own program once the repo is locked"*: the
owner wants to work in the new format while the remaining schema decisions are
still open, so the anchor (D-1), the ladder (D-3) and the `SupersededBy`
deletion (D-4) land on the destination carrier **once** instead of being built
on CSV and ported. That is exactly what §6 F-7's corrected sequencing note
argues — *"the fields are carrier-neutral; the code and tests are not."*

#### The shape, ruled with the owner

```toml
[requirement.SR-137]        # id-keyed, prefix RETAINED, and BARE
title = "One policy home, with a checked shape"
sn_refs = ["SN-028"]        # refs are typed arrays
phase = 5                   # ints are ints
requirement = """…"""       # multi-line strings hold the prose cells
```

Table names by tier: `need` · `requirement` · `design` · `test`.

**Three integrity rules stop being code and become properties of the parse.** A
**duplicate id** is a `TOMLDecodeError` (the id is the table key, and TOML
forbids declaring one twice); a **ref list** is an array, retiring `refs()`'s
split-on-whitespace and with it the `SN-001 and SN-002` → *"`and` is an orphan"*
defect §12.8 records; an **empty cell** is an *absent key*, so "unset" and "set
to empty" stop being the same value.

**The id prefix stays in the key**, against the owner's own proposal of a bare
`[stakeholder-need.137]` — decided on measurement, not taste:

- TOML keys are **always strings**. `[r.137]` yields `'137'`, so a numeric key
  buys no type change at all.
- `001` and `1` parse as **different keys**, both legal. Our ids are
  zero-padded, so any normalisation creates a second row instead of erroring.
  The prefixed form has no such near-miss.
- **~6,400 hand-authored citations** (SR 3,270 · LLR 1,163 · TC 973 · SN 967)
  use the prefixed token, in commit messages, log entries, docstrings and
  archived docs. Dropping it from the definition means `grep SR-137` no longer
  finds the row that defines it.
- `is_example(rid)` is literally `rid.endswith("-000")`.

The quotes, however, are unnecessary: **TOML bare keys allow `-`**, so
`[requirement.SR-137]` is valid unquoted.

#### CARRIER ONLY — and this is the guardrail the reordering rests on

`Status` keeps `Draft` / `Verified` / `Modified`. **No** ladder, **no** anchor
cells, **no** `Priority` float, **no** `SupersededBy` deletion, **no** `Status`
on SN. Retiring `Modified` is the ladder's job; doing it inside the carrier
change would stamp 38 rows clean and launder the re-blessing they owe (Q11).
Keep these apart or the sitting is compromised.

#### The SN tier keeps its edge-case fields

Edge-case rows carry `lifecycle` / `scenario` / `expected` as themselves, not
folded onto the core four. `traj_parse._sn_fields`' fold — an edge row's
Scenario read as the need — is a **presentation** rule the markdown table
forced; baking it into the carrier would make the exporter's reading the only
reading there is. The fold stays in the exporters, reading from TOML.

Converting also **retires section-as-state**: draft-ness becomes
`kind = "draft"` instead of *"appears under a heading containing the word
draft"*. That is Q2's *"never both"*, and it kills a live sharp edge — during
the 2026-08-10 sitting a prose mention of an id under the draft heading
silently re-drafted an attested need, because `sn_all_ids` scrapes the whole
file and `sn_draft_ids` scans by heading.

#### THE ONE THING THAT MUST NOT BE FORGOTTEN

**`trace._rows_at` reads the baseline through `git show <rev>:<path>` and
CSV-parses it.** After the cutover, that path does not exist at pre-migration
revisions, so it returns `{}` — which the code reads as *"nothing existed = an
empty baseline"*. Every one of the 25 `Modified` rows would then render as
*"no baseline — awaiting its FIRST ratification"* and the owner would re-bless
full text with **no diff of what changed**, silently. It is the same fail-open
shape as the squash-merge hazard D-1 rejected in ALT-1.

So the cutover **must** carry a carrier-aware baseline read: try the TOML path
at that revision, fall back to the CSV path. The file *was* CSV then, so
reading it that way is honest history, not a shim. `check_trajectory`'s
`_spine_revs` two-tree read needs the same treatment.

#### Why the 16 consumer modules do not change

The loader presents TOML rows using **today's column names** (`SR-ID`,
`Title`, `SN-Refs`, …), so the carrier change is data + one loader + the
writers, rather than a 16-module rename braided into a carrier migration.
D-3 is the pass that renames things, and it can do so on TOML afterwards.

#### State, 2026-08-10

**Shipped:** `scripts/migrate_carrier.py` + `tests/test_migrate_carrier.py`
(commit `a9b6ced3`). Round-trip clean over all **466** of this repo's own rows
(29 SN · 146 SR · 147 LLR · 144 TC), cell for cell, with the loss detector
driven against five corruption classes — a round-trip check that cannot fail
would be the false green SN-008 forbids. **Nothing has moved yet**: no registry
changed carrier, so the tree is still single-home.

> **Correction, 2026-08-10 — `a9b6ced3` did not ship green, and step 11's
> "MET" claim below did not survive it.** The converter landed with **no spine
> row of its own**, so `migrate_carrier.py` entered the arch-map inventory as
> an *uncontained* module and `test_meta_component_top_view_smoke` went red:
> `assert ['scripts/migrate_carrier'] == []`. Measured on a clean checkout of
> `fe09dcd6`: **1 failed, 2179 passed, 5 skipped** (6:30). Closed by minting
> the chain the module always owed — **SR-147** (one machine-parseable carrier
> for the spine, tracing SN-002 · SN-012, the same pair SR-129 traces for the
> work-item registry's converter) → **LLR-165** (`migrate_carrier.py`, tagged
> `CMP-005` beside `wi_convert.py`, its exact analogue) → **TC-159**
> (`tests/test_migrate_carrier.py`), all `Draft`, watermark raised
> SR 146→147 · LLR 164→165 · TC 158→159. Suite back to **2180 passed,
> 5 skipped, 0 failed** (5:58).
>
> The lesson is narrow and worth keeping: **the containment rule fires on the
> arch map, not on the registry**, so a new module is uncontained the moment it
> exists and stays green only until the next full run — the module-level twin
> of the "an amendment that edits one cell has not amended the row" lesson
> under D-1. A per-commit smoke tier does not catch it; the full tier does.

**Owed, in order — the next session's list, authoritative:**

1. ~~the carrier-aware baseline read~~ **DONE** (`a35f12f6`)
2. ~~the loader, every spine reader including the SN tier~~ **DONE**
   (`82d5b818` · `d97f2634` · `9a5d7267` · `df840a3b`)
3. ~~**the cutover**~~ **DONE** (`bb69a622`) — applied from the patch by 3-way
   merge, ~64 red driven to zero, ten fail-open readers fixed in the landing.
   See "LANDED, 2026-08-11" below.
4. ~~`intake`'s writer becomes a TOML emitter~~ **DONE** (`bb69a622`) — the
   line rewrite, as ruled: `status = "Modified"` is one `key = value` line,
   comments and ordering preserved.
5. ~~`test_dogfood_sync`'s header rule~~ **DONE** (`bb69a622`) — redesigned
   with **inverted direction** ("live keys ⊆ template keys, template keys ⊆
   carrier vocabulary"; the old direction is unmeasurable over TOML). Driven
   against planted defects both ways; caught two pre-existing drifts on
   arrival. Recorded as builder decision (3) in the LANDED note.
6. ~~templates + ADOPTING~~ **DONE** (`bb69a622` + `f7be75af`).

**Step 1 — the carrier-aware baseline read — is DONE.** `trace._rows_at` and
`check_trajectory._spine_rows_at` each resolve the carrier a revision actually
used: TOML first, CSV as the fallback, rows presented under today's column
names either way so nothing downstream learns which answered. Two properties
came out of it that were not in the plan and are worth keeping:

- **The cutover commit is now CHECKED by the amendment guard rather than
  invisible to it.** Because each side resolves independently, a diff across
  the cutover reads CSV on the old side and TOML on the new one and compares
  cells — so a lossless cutover is *silent*, and text smuggled into it is
  named. That is a second proof of the conversion, independent of the
  converter's own round-trip check, and the mutation test that makes the
  silence non-vacuous is `test_text_smuggled_into_the_cutover_commit_is_caught`.
  It also forced the `touches` applicability test to name **both** carrier
  paths: the cutover deletes the `.csv` and adds the `.toml`, so a single-name
  test would match neither and skip the one commit that rewrites every row.
- **A carrier that does not parse is reported ABSENT, never EMPTY.** The two
  are opposite claims — `{}` says "this registry had no rows", which for a
  baseline read means "re-bless everything with no diff". `_toml_rows_text`
  returns `None` on a decode error so the caller can tell them apart.

**Step 2 — the live loader — is DONE for the SR/LLR/TC tiers.** Nine readers
now go through `spine_carrier`, so each answers whichever carrier is live:
`trace` · `check_trajectory` · `derive_gate` · `gen_okf` ·
`gen_release_checklist` · `check_doc_refs` · `check_flows` · `plan_coverage` ·
`plan_briefs`. **Still on `csv`/markdown and owed before the cutover:**
`intake` (which also **writes** — step 4), `agent_loop`, `agent_common`,
`check_docs`, and every reader of the **SN tier**, whose shape is different and
which the cutover converts (`traj_parse._sn_rows` · `gen_okf.sn_rows` ·
`sn_all_ids` / `sn_draft_ids` · `sn_normative_text` ·
`check_docs._registry_needs` · `check_flows`'s inline SN regex).

Three things the wiring cost, all of them the architecture layer charging for
the ruling rather than resisting it — and worth knowing before the next step:

- **Five cross-component seams had to be declared** (IF-104…IF-108): a shared
  module imported from CMP-002/003/004 into CMP-001 needs one `Consumes` row
  per crossing, the same convention `schedule.py` already follows. This is the
  visible price of D-6 and it is the right price — the seam is now in the
  registry rather than implied by an import line.
- **The duplicate census had to be reclassified by READING each block**, not by
  its path pair. A first pass filed all twelve new blocks under
  `import-fallback` by inference; opening them showed three were the `cli`
  preamble and one the `spine-loader` id reader. That is precisely the
  bucketing failure `test_dupes_census_audit` exists to catch, caught by it.
- **A dedent left a loop body nested under a `continue`** in
  `check_doc_refs.registry_findings` — syntactically valid, silently scanning
  nothing, and `ruff` has no unreachable-code rule to catch it. Found by two
  tests that assert the check REDS on a planted defect. Recorded because it is
  the same lesson in a new place: what saves you is the test that proves a
  guard can still fail, not the one that proves it passes.

**Step 3 — THE CUTOVER — was RUN and is NOT LANDED.** It is preserved as
`git stash@{0}` and as [`plans/2026-08-10-carrier-cutover.patch`](../plans/2026-08-10-carrier-cutover.patch);
the branch stayed at the green commit rather than taking a red one. Run it, do
not re-derive it — what it proved and what it exposed is the whole value:

**Proved working, on the real registries:** all four tiers converted
round-trip-clean and the `.csv`/`.md` sources deleted in the same tree;
`trace --strict` reads TOML at `SN=29 SR=147 LLR=149 TC=146 orphans=0
integrity=0`; `check_docs` at **0 broken links**; `derive_gate`, `okf`,
`open-items` and `arch-map` all green; and the gating harness **PASSED** with
the advisory set back at the session baseline.

**And the hazard D-5 flagged hardest did not fire.** The 25-row re-attest brief
regenerated across the carrier change with **zero "no baseline" cards** — real
before/after diffs, CSV on the old side and TOML on the new. That is step 1
doing exactly the job it was built for, verified on the real thing rather than
on a fixture.

**What it exposed — three readers that were never wired, two of them
FAIL-OPEN:**

1. `trace.load_registries` still parsed CSV, so `trace --strict` reported
   **`SN=0 SR=0 LLR=0 TC=0 orphans=0`** — a *vacuous green*, the exact shape
   this repo exists to prevent, and it would have passed a gate. Fixed in the
   patch.
2. `check_trajectory.read_rows` likewise, which emptied the AXES join and
   reported **55 uncontained modules**. Loud rather than silent, and fixed.
3. `traj_parse._spine` called `ct.read_rows` on TOML paths and got nothing, so
   the dashboard would have rendered an **empty spine** — and `--check` would
   have byte-compared two empty renders and called it fresh. Fixed.

**What is still owed on the patch: ~76 test failures, not diagnosed to root.**
One cause is known (fixtures write `.csv`, which `resolve` still finds, so
those are *not* the failures — look past them); the rest are readers not yet
traced and renders that changed. Do not assume the count is the work: one fix
to `traj_parse._spine` cleared a large block of them.

**The generalizable lesson, and the reason this is recorded rather than
retried quietly:** the cutover is what found the unwired readers, because a
carrier change turns "this reader was never converted" from invisible into
either an empty result or a crash. Wiring readers against the OLD carrier can
never surface them — every reader looks fine while the file it expects still
exists. So the cutover is not the last step of the migration; it is the
*detector*, and it should be run early and often against a throwaway tree.

The carrier vocabulary is now shared by three modules (both readers plus
`migrate_carrier`'s writer) and **pinned three ways** in
`tests/test_rule_sync.py`: the readers' constants equal, both the exact inverse
of the writer's `KEY`, and every column of every *live* header driven through
the pair so the agreement cannot be vacuous. Censused in `docs/dupes-allow`
with that reason. **The CSV fallback is deliberate dead weight with an expiry**:
it should be dropped once no supported baseline predates the cutover, and both
ratchet entries say so.

#### LANDED, 2026-08-11 — the cutover is COMMITTED and the full bar is green

`bb69a622` (the cutover: four tiers to TOML, sources deleted, plus steps 4, 5
and 6's templates — each step's tests only became runnable once the carrier
moved, so they landed together) and `f7be75af` (ADOPTING's migration recipe).
Full unfiltered suite: **2197 passed, 5 skipped, 6:07**. `trace --strict`
`SN=29 SR=147 LLR=149 TC=146 orphans=0 integrity=0`; the **38 `Modified` rows
survived exactly** (25 SR · 6 LLR · 7 TC), no `Status` on SN, vocabulary
unchanged — the reordering guardrail held. The re-attest brief regenerates
**byte-identical** across the carrier change. Applied from the patch file via
3-way merge (HEAD had moved; one `interfaces.csv` EOF conflict, resolved to
the patch's side); `stash@{0}` verified redundant and dropped.

> **Correction: step 1 was recorded as DONE above and was not done enough.**
> `trace._rows_at` was carrier-aware; `trace._attested_baseline`'s `git log`
> **pathspec** was not — after the cutover the `.toml` path's history contains
> only the cutover commit, where every amended row reads `Modified`, so no
> Verified revision is found and **all 25 rows reported "No attested
> baseline"**. The exact fail-open D-5 flagged hardest, one function away from
> where it was fixed. Caught at the builder's guardrail check, fixed in
> `bb69a622` by naming both carrier paths. Two lessons: a "DONE" that means
> "the function I looked at is done" is not a property of the *path*; and the
> grep that "confirms" a hazard didn't fire must quote the real string — the
> first check passed by searching this file's paraphrase of the message.

**Six decisions the builder made that this file had not ruled** (recorded, not
re-litigated — all are live in `bb69a622`): **(1)** `TestRefs` stays a plain
string, not a ref array — its conventional `(see TC-017)` value would split
and re-join as text damage across 140 LLR rows. **(2)** Ref arrays re-join on
`;` bare, matching all 271 multi-ref cells as measured; the prettier `"; "`
would have pushed ~40 spurious cell-changed entries into the sitting's brief.
**(3)** `test_dogfood_sync`'s replacement rule **inverted direction**: "live
keys ⊆ template keys, template keys ⊆ carrier vocabulary" — the old direction
is unmeasurable over TOML (an all-empty column like `Permutations` legitimately
vanishes from the live carrier). Non-vacuous by construction and by planted
defect: it immediately caught two drifts the old rule permitted (`SupersededBy`
never templated; the LLR template's blank `Component` silently dropping the
key). **(4)** Fixtures stay on the legacy CSV carrier so the un-migrated
adopter's fallback path keeps its coverage; the TOML arm rides this repo's own
registries + fresh-scaffold tests. **(5)** `gen_cases` gained a `toml` paste
format beside `csv`. **(6)** The needs registry's markdown guidance —
including `## Non-goals`, a G1 deliverable with no other home — survives as
TOML comments rather than being dropped by the row-reading converter.

**Ten fail-open readers were found and fixed in the landing** — the patch's
known three plus seven more, including three inside `spine_carrier` itself.
The worst: `derive_gate`'s needs-registry existence probe read the markdown
file as absent → empty draft set → **the derived gate would have RISEN**;
`spine_carrier.load`'s `{id: row}` shape silently collapsed duplicate CSV ids,
destroying the first thing `--strict-integrity` exists to fail on; and
`_blame_row_times` looked rows up by the CSV shape and passed staleness having
checked nothing. The step-3 lesson stands confirmed: the cutover is the
detector.

**Rows whose text the cutover falsifies — TABLED for the sitting, not
amended** (the builder was instructed to stop, not amend): `SR-002` (title
"…CSV structure", column-count clause) is the clear one; also worth a
read-through: SR-025 · SR-129 · SR-147 · LLR-002 · LLR-025 · LLR-034 ·
LLR-041 · LLR-118 · LLR-136 · LLR-165 · TC-025 · TC-129 · TC-160 · SN-026 —
some may still be true (the off-spine registries and WI carrier are still
CSV). §8.4 carries the full sitting-input list this joins.

### D-6 — the spine carrier gets ONE home; F5 is AMENDED, not ignored

**Owner ruling, 2026-08-10**, taken on measurement during D-5 step 2. The
question was where the TOML reader lives, and it was a genuine fork because two
of the kit's own rules pointed opposite ways: D-5 says "data plus **one**
loader", and the F5 ruling (WI-078) rejected a shared `_kitcommon.py` so every
script stays an independently-copyable drop-in.

**Ruled: one sibling module** — `project-trajectory/scripts/spine_carrier.py`,
imported by the spine readers. This **amends F5** rather than quietly stepping
around it, and the amendment is narrow enough to state exactly:

> F5 buys cross-script copy-ability, and it was written for small stable
> **plumbing** — a five-line CSV loader, the argparse preamble — where a
> divergence between copies is visible and cheap. It does not cover a shared
> **vocabulary**, whose divergence is neither.

**The measurement that decided it**, taken before the ruling: two readers need
all 28 columns, **three need none**, and the rest need between 1 and 20 — so
the duplicated form is **~300 lines of vocabulary across eleven modules**, plus
eleven reviewed ratchet bumps and eleven census entries. Against that, the
failure mode is the one this program keeps finding: a copy that has not learned
a column **does not fail loudly**. It returns a row with that cell missing,
which every consumer downstream reads as *"the cell is empty"* — silent content
loss on the registries the kit exists to make trustworthy. The third option
considered and rejected — a per-script map sized to what that script reads —
is the same hazard made routine.

**What it costs, stated plainly:** "independently copyable" becomes "copyable
with its **declared siblings**". That is what the kit already practised and had
not said — `trace.py` has shipped with `trace_text.py` since WI-329, and
`gen_trajectory.py` with six `traj_*` modules — so the amendment writes down an
existing exception rather than creating a new one. `ADOPTING.md` §6 and
`bootstrap.py`'s MAPPING carry the file, on the same rule the other siblings
use: a scaffold missing it `ImportError`s on the first check.

**Measured effect on the ratchets, both directions:** `trace.py` −84 and
`check_trajectory.py` −57 against their step-1 bumps (the vocabulary and both
readers left), `bootstrap.py` +11 (two MAPPING rows and the reason each is
copied). The census lost the five `spine-carrier` blocks step 1 added and kept
three — the constants each module still names for its own use.

**Its own chain, minted with it:** `LLR-166` + `TC-160` under SR-147, and
**IF-102** declaring the seam. `migrate_carrier.py` got **IF-103** in the same
pass, closing a connectivity warn this program had created — and marked
`Provisional`, because it is migration scaffolding with a defined end and
should be retired once no supported repo is still on the legacy carriers.

### D-7 — the duplication census is TORN DOWN; test_rule_sync is the anti-drift tool of record

**Owner ruling, 2026-08-10**, on the evidence ledger above: *"unless there is a
better alternative it seems to be creating more maintenance structure than it
really solves, so it should probably just be torn down."* The member-list
improvement was on the table and was judged not worth keeping the apparatus
for. The hedge is recorded as an instruction: if the teardown's builder finds a
genuinely cheaper form **mid-execution**, bring it back to the owner rather
than building it.

**Why (the ledger, §"Is the census earning its keep"):** one real catch at the
one-time triage, zero recorded since; structurally blind to both real drift
incidents this repo suffered (a diverged copy is no longer an identical token
block, so the tool goes silent exactly when duplication becomes dangerous);
93% of its 253 lines register accepted idioms; and it carried its own defect
chain, a 12-test meta-audit over its prose, and three churn cycles in one
session.

**Consequence inventory — none optional:**

1. `check_dupes.py` retires from the kit: the `bootstrap.py` MAPPING row, the
   README kit-contents row, `docs/stack.ini` `[step:dupes]`, and `check.py`'s
   advisory step all go with it.
2. `docs/dupes-allow` is **deleted, not archived** — a registry states what
   *is*; git is the history (the D-1/D-4 doctrine).
3. `tests/test_check_dupes.py` (18 tests) and `tests/test_dupes_census_audit.py`
   (12) are deleted with their subject.
4. **The spine chain `SR-039 → LLR-036 → TC-039` is superseded — which under
   D-4 means DELETED**, ids retired against the watermark, the act recorded in
   the log's Decisions. This is the first real supersession D-4 will execute,
   so it doubles as D-4's proving case.
5. **F5 becomes unbounded again — the WI-078 concern re-opens, and the
   mitigation is named rather than implied:** `test_rule_sync` is the
   anti-drift tool of record, and new F5 duplication of **policy** requires a
   behavioral pin there; plumbing duplication is accepted unbounded, which the
   ledger shows was its de-facto state anyway.
6. ADOPTING notes the removal; an adopter's copy is their file after copy-in —
   keeping it is their call.

**Sequencing:** *not* braided into the carrier cutover — the cutover's ~76 red
must land against a stable baseline first. Executes as its own WI in the step-7
area, where the D-4 supersession machinery it exercises already lands.

**EXECUTED 2026-08-11 as WI-426** (`ada89294` → `704ffd0d` → `bc829516`), all
six inventory items, nothing deferred; the hedge found no cheaper census.
**D-4's proving case succeeded**: SR-039 → LLR-036 → TC-039 deleted, ids
retired, marks unchanged and both watermark rules verified could-not-break
(interior ids, never a maximum); the log's Decisions entry is the forwarding
pointer. Two consequences the inventory had not priced, both forced by the
orphan check and taken: **IF-007 and IF-027 deleted** (an IF citing an
unknown SR is a `--strict` finding, so keeping them traded one dangling
pointer for two), and **WI-037/WI-078's machine-read `sr_refs` cleared**
(prose keeps the history, joins cannot point at nothing). The retired paths
joined `docs/declared-absences`; the F5 ruling re-homed from the census
header to `test_rule_sync`'s docstring (policy owes a by-VALUE pin there,
plumbing unbounded); `enforcement-audit.md` records the Harness→Test+Reviewer
downgrade. Full bar on a detached worktree: **2188 passed, 6 skipped**, the
−30 delta measured by collect-only counts (2224 → 2194 = exactly the 18 + 12
deleted). `trace --strict` `SR=146 LLR=148 TC=145 orphans=0 integrity=0`.


---

## 3. The questions, and where each one went

Every Q1–Q4 is closed. Kept as a map, because the *reasoning* is what a ruler
needs and the full text is in git (`git log -p docs/repo-lock.md`).

| # | asked | outcome |
|---|---|---|
| **Q1** | where the SN anchor fields live inside the file | **withdrawn** — under a TOML carrier an SN is an element with keys, so the on-row-vs-anchor-table distinction has no referent. Folded into **OI-12**. Its examined option (c), one file per need on the `docs/work/` pattern, is recorded as *not recommended*: an SN has two axes where a WI has one, SNs are read as a set rather than a queue, and the edge-case table is a **form** whose blanks are the teaching. |
| **Q2** | does an SN get a `Status` cell | **widened** into **OI-13** once `interfaces.csv` turned out to carry an undeclared `Status` overlapping `Stability`, read by nothing mechanical yet fed verbatim to LLM briefs. Answer for SN itself: **yes**, with section-as-state retired in the same commit — never both, or the repo declares one dial twice. |
| **Q3** | how far back the co-mutation guard compares | **still open**, but a *build-time* decision for the anchor half. Needs a declared base for the rev-range arm; until then the guard must say in its docstring that it is partial. |
| **Q4** | which SR-140 text the sitting rules on | **answered and shipped**: D-1's amended, carrier-neutral text. Ratifying prose already known to be retired would manufacture a `Modified` row on the day it is created. |
| **Q5–Q12** | the consequences inside D-3 | in §2 under D-3. Q9 (the TC gray area) and Q12 (`Method` vs `Evidence`) are the two that changed the build. |

## 4. Answers to questions already asked

Both closed; kept as one line each.

- **"Are SN-028…032 changed?"** No — **new and never ratified**, not amended.
  The word "changed" belongs to the **25 `Modified` SRs**, whose text was
  amended because machinery under them was retired. Both sets are owed at the
  same sitting, for opposite reasons.
- **"Are they pulled into `open-items.html`?"** The SRs and their chains, yes;
  **the SNs themselves, no** — `reattest_model` selects by `Status`, and an SN
  has no `Status` cell. **OI-13/D-3 is what closes it**: with the ladder an SN
  becomes selectable and renders as its own card.

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
[`registry-machinery-reference.md`](../registry-machinery-reference.md) §2–§5, §10,
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
option raised.** Owner question, 2026-08-09: could a `.toml` file replace the
`.md` + `.csv` combination?

> **VERDICT OVERTAKEN, 2026-08-10.** This finding closed with *"the right
> answer for a successor program — not this one"*, and the owner has since
> ruled the opposite: the migration runs **inside** this program and **ahead
> of** the sitting (**§2 D-5**). The *measurements* below all stand and are why
> the ruling went the way it did — what changed is the sequencing judgement,
> and it changed on this section's own corrected argument that the code and
> tests are not carrier-neutral. Read the paragraphs below as evidence, not as
> a live recommendation to defer.

*Why it is strong.* `tomllib` is **stdlib at the kit's 3.11 floor** — no
dependency, unlike a markdown parser (F-6). The kit already sanctions TOML in
two homes: [`process.toml`](../process.toml) and the `+++` frontmatter of every
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
`open-items.csv` carries `OneLine` / `Decision` /
`BlastRadius` / `Options` / `Recommendation` / `WI-Refs` and renders as a card
in [`open-items.html`](../open-items.html), the surface the sitting reads anyway.
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
  [`docs/requirements/components.csv`](../requirements/components.toml): `CMP-ID`,
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

**F-12 · A TC's claim to have a test is checked at FILE granularity — and the
data behind it had rotted. FIXED, except the check itself.** Two checks touch
the claim: `trace.py` requires `Automated=Yes` to cite a non-empty `Evidence`,
and `check_doc_refs` checks the cited path exists — but only the FILE half, since
resolving a node id means running the project's test runner. Measured over 143
live rows: 0 cited files missing, but **111 of 212 selectors did not resolve**,
across 42 rows, almost all from the WI-277 test-module splits. One file was cited
by 32 TCs, so the file-half check could never have caught it.

**All 212 now resolve** (`b9d41833`), repointed deterministically from a
name→file map — 102 of 103 stale citations had exactly one home, the last was a
rename `git log -S` proved, and 21 bare `::selector` continuations (invisible to
tooling, since `is_path_shaped('::x')` is False) are fully qualified. `Evidence`
is traced, so it cost no re-attestation.

**The check stays declined** under ruling R2, and Q12 explains why that is right
rather than merely deferred: `Ready` means the test EXISTS, and `Evidence`
naming a file answers that. Accepted knowingly: a TC can reach `Ready` on a file
that exists for another TC's sake.

**The finding underneath it survives and is not fixed:** the missing granularity
had been hand-written into `Parameters` — declared as an input recipe
(`param=a; other=x`), filled on 24 of 143 rows, of which **24 carry a repo path
and exactly ONE matches the declared shape**. `Method` is required, normative,
rendered in five surfaces, scanned by `agent_loop` for rubric paths it INLINES
into briefs — and never validated. That is how pointers leak into columns that
were never meant to hold them.

**Candidate follow-up, not filed:** the *prose-an-LLM-is-handed* view above
exists nowhere as a consolidated surface —
[`registry-machinery-reference.md`](../registry-machinery-reference.md) documents
mechanical effect per field and mentions LLM consumption only in passing. Folding
F-3 into it as a new section would give the question one home. Deliberately not
done mid-program: it is a reference-doc edit with no bearing on the lock.

---

## 7. This document's own log

Compressed 2026-08-09 — the blow-by-blow is in `git log docs/repo-lock.md`.
What a reader needs is which rulings landed and which claims were **overturned**,
because the overturned ones are where the reasoning is still worth having.

**Rulings, in order:** D-1 (the anchor moves onto the artifact's own row;
`attestations.csv` retired) → D-2 (SNs gain fields, not a new carrier) → D-3 (a
column name means one thing repo-wide; `Status` becomes the four-rung ladder) →
D-4 (supersession is deletion; ids are never reused).

**Claims this document made and then had to withdraw** — each one cost real work,
which is the argument for writing them down:

- *"Deferring the carrier forecloses nothing."* True of the design, **false of
  the labour** (F-7). Building the anchor on CSV and converting rewrites the
  column-classification machinery, the header-superset rule, `structure_findings`,
  `intake`'s writer and the attestation tests a second time. OI-12's own card
  carried the false version until it was corrected.
- *"The `::node` selector check is a ship-now item."* It **overturns owner ruling
  R2 of 2026-08-01**, which weighed exactly that question and shipped the file
  half. Recommended without checking; withdrawn. Q12 then made it unnecessary.
- *"An equality test pins the SN reader twin."* The three readers were
  byte-identical **and all three wrong the same way**, so equality was already
  true while every edge-case row rendered its Lifecycle word as the need.
- *"The `intake → trace` import owes no IF row."* It did. The component rule
  joins on the **generated** arch-map, and I read the check before regenerating.
- *"Counting extra ids can only raise the floor."* An adversarial review showed
  the scan **under-counted** — it read the first id-*shaped* cell rather than the
  id *column* — plus two blockers where the guard defeated itself through its own
  documented remediation. All fixed at `d97cdc75`.

**Two rulings that came from the owner refusing a framing**, both load-bearing:
`Ready` means decomposed-and-handed-on while `Verified` means proven-by-execution
(so an SN/SR/LLR never claims `Verified`); and the `Evidence` pointer stays in a
**traced** cell rather than moving to the **ratified** `Method`, because moving it
would turn every test-file rename into a re-attestation — 110 of them for WI-277
alone.

---

