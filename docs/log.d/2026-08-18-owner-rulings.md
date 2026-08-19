## 2026-08-18 — The owner rules on the ten briefs: four ruled, two re-pointed, three answered, one minted

The ten briefs minted earlier the same day (`docs/log.d/2026-08-18-open-items-minted.md`)
went to the owner. This is the disposition of all ten, plus one new row for the
owner's meta-question about the surface itself.

`open-items.toml` is **exempt from the provenance rule** (its subject IS
provenance — `docs/log.d/2026-08-18-provenance-rule.md` §4, "excluded
wholesale"), so dates, ruling references and work-item ids in those cells are
correct and expected.

| id | disposition |
|---|---|
| OI-31 | **RULED** — adopt the recommendation, (b) warn-first divergence step |
| OI-32 | **re-pointed**, still pending — owner direction: a generated component view |
| OI-33 | **re-pointed**, still pending — the same direction, which deletes most of the question |
| OI-34 | **RULED** — kill the derived-requirement label; hats replace it |
| OI-35 | **RULED** — the rule reaches headers; executed the same date |
| OI-36 | pending — owner question answered on the row |
| OI-37 | **RULED** — relax SN-006; executed the same date |
| OI-38 | pending — owner question answered on the row |
| OI-39 | pending — owner leans mint, research in flight |
| OI-40 | pending, unchanged |
| OI-41 | **minted** — why deferred decisions do not reach the surface |

---

### OI-31 — RULED: the divergence step, warn-first

Adopt the recommendation, option **(b)**: one new check step asking whether a
generated artifact is *modified in the worktree but absent from the index*,
warn-first, its artifact list **derived from the `[generated]` census** rather
than copied. The nine existing freshness gates are unchanged.

**(a) is recorded as the destination** — a gate that reads the tree being
committed is strictly more honest — and is refused today on cost, not
correctness: it would turn nine "pure function of a directory" scripts into
git-object readers, and that contract is what lets the freshness tier be tested
against a temp scaffold.

**(b)'s honest gap is stated in the ruling**: it does not catch an artifact
*staged while stale*. That needs (a). It is the rarer shape — staging a file you
never regenerated, versus forgetting one `git add`.

`3b8d306d` stays as it is: still an ancestor, still failing
`gen_trajectory --check`, recorded so a future bisect does not read it as a
later regression. **Execution is another lane's**; this session recorded only.

### OI-34 — RULED: kill the label, and give the rows their hats

The owner's leaning, taken as the ruling: **kill** the derived-requirement label
(option (c)) and instead give SRs and LLRs **the hat(s) they were derived from**
— a row may carry several. That hat data generates the component view, and the
component is what a work item strongly references, so the work carries context
on why the component exists, what it does, and which knowledge to weigh more
heavily in that space.

So the label is not deleted into nothing: the deriving **lens** is what it was
really pointing at, and a hat field names the lens as data. What is deliberately
given up is the **signature** state — there is no ratification ceremony for a
hat attribution.

**Same thread as OI-32/OI-33, marked as a dependency on the row.** The
population to migrate is **18**, not 17: seventeen unsigned parentheticals
(SR-024, 033, 040, 043, 052, 054, 111, 112, 129, 144, 146, 147, 149, 167, 175,
176, 177) plus **SR-053's signed form**. All 18 already name their hat in prose
in the same cell, covering 11 of the 16 hats. **Migration not executed** — it is
its own WI, and must land as one change because the parentheticals are also 17
`docs/provenance-allow` entries that retire with the marker they mark.

### OI-35 — RULED: headers are light field guides. Executed.

The owner: headers should be *"pretty light. They don't need to carry any
history reference at all here, just what field and a very short why / how it's
used."*

Executed the same date. The brief measured 45 tokens over three headers;
re-running the detector over **every** registry header found a fourth the brief
had not counted — `hats.toml` — so the true population was **59**.

| file | header lines before → after | tokens before → after |
|---|---|---|
| `docs/requirements/stakeholder-needs.toml` | 103 → 90 | 13 → 0 |
| `docs/requirements/interfaces.toml` | 105 → 105 | 17 → 0 |
| `docs/requirements/external.toml` | 94 → 95 | 15 → 0 |
| `docs/requirements/hats.toml` | 108 → 67 | 14 → 0 |
| `system-requirements` · `low-level-requirements` · `test-cases` · `components` · `open-items` | no header block | 0 → 0 |

Each rewritten header is now a per-field guide: what the field is, its
vocabulary where it has one, and a short why/how it is used. **No row cell was
touched**, no `status` moved, no re-attest window opened.

**Kept, each checked before it was kept:**

- `external.toml`'s **SPENT IDS** statement — history in form, a live re-mint
  guard in function (`B-08`/`REL-004` are cited by id in ruled documents and
  `docs/id-watermark` does not protect them). Restated as a rule about the
  file's id space rather than as the story of how the ids were spent.
- `stakeholder-needs.toml`'s `## Non-goals` section including **NG-1** — a
  DevStg-Reqs deliverable with no other home in the repo. Its citation of the
  review that first recorded it was dropped; the non-goal stayed.
- Every field statement, in all four files.
- `hats.toml`'s standing instruction that the file is **owner text marked for
  the owner's edit at return**, and the still-open call on whether SAFETY
  belongs in this repo's roster — a live instruction and a live open question,
  not a record of one.

**Dropped:** the OI-18 dissolution paragraph opening the needs registry, the
interfaces header's two-reason hold narrative and its retirement ledger,
`external.toml`'s decision-by-decision status and flip-authority history, the
`§1R.x` section-reference suffixes on its three divider comments, and
`hats.toml`'s growth record — together with every work-item id, open-item
reference, decision id, sitting reference and dated stamp in all four.

**Nothing mechanical read any of it.** Checked before deleting: no test or
script asserts on live registry header text; the `## Core needs` / `## Draft
needs` headings are inert under the TOML carrier
(`spine_carrier.draft_ids_from_text` takes the field path when
`needs_from_toml` parses, and the heading scan is the legacy-markdown branch);
no document anchors into any of these headers.

### OI-37 — RULED: relax SN-006. Executed.

The owner: *"SN-006 needs to be relaxed. Note this is not the first time I've
seen absolutes in a place it wasn't warranted. SN-006 really just means the
unattended layer will move forward as much as possible, only surfacing to the
human if it is unable to move forward."*

The general note is **recorded as part of the ruling**, because it generalizes:
an absolute in a need is a promise every child must keep under every condition,
including the conditions where the child's own machinery is broken. Here SR-043's
clause did not change — the parent's promise did — and the child was put in the
wrong by a word.

**`need`, before:**

> …It also stays **safe**: declared limits bound the workers it may set running
> and the actions it takes that cannot be undone, and only an override a human
> provides — never one the model can set — may relax those limits.

**`need`, after** — the same sentence, plus:

> That safety is **supervision rather than an absolute**: the layer's first
> obligation is to move forward as far as it can, and it surfaces to a human when
> it cannot proceed — so a fault in the machinery that carries a limit degrades
> to a recorded condition, not to a stopped run.

**`acceptance`, before:**

> …During unattended operation, configured limits bound every spawned worker and
> irreversible action; only an explicit human-provided override may exceed those
> limits; **a gate error preserves the configured bound**. (That last clause is
> the OPEN QUESTION for the sitting… the sitting rules fail-closed, a narrower
> independently-enforced ceiling, or a narrowed need.)

**`acceptance`, after:**

> …During unattended operation, configured limits bound every spawned worker and
> irreversible action, and only an explicit human-provided override may exceed
> those limits. **A fault in a limit's own enforcement is recorded and lets the
> run continue rather than halting it** — the run surfaces to a human when it
> cannot proceed, never when its own supervision errs.

**Preserved:** the resume/typed-code/preflight half of the acceptance verbatim;
the bound itself (declared limits bound spawned workers and irreversible
actions); and the human-held override that the model cannot set. **Removed:** the
absolute (`a gate error preserves the configured bound`) and the open-question
parenthetical it carried.

**Is the SR-043 contradiction dissolved? Yes.** SR-043's shall — *"fail open on
any error so a broken gate never wedges the tools"* — now **realizes** the
amended acceptance instead of contradicting it: a fault in the gate's own
enforcement lets the run continue, and SR-043's acceptance already requires that
the fail-open be **logged** (`a malformed payload fails open (allow) and is
logged`), which is the "recorded" half. No wording in the new cells asks for
anything `subagent_gate.py` does not do.

**One residual honesty point, not a contradiction:** "recorded" is satisfied by
`out/subagent-gate.log`, and **nothing reads that log**. A fail-open nobody
counts leaves a degraded run indistinguishable from a clean one. That is a gap
worth its own row, not a defect in the amendment — noted on OI-37's ruling.

**Owed and deliberately not done here:** SR-043's `rationale` still carries its
`OPEN QUESTION FOR THE SITTING` paragraph and the matching
`docs/provenance-allow:28` entry. Both are now correct to retire, and they
retire **together** (the allow file's own rule). That is a separate amendment on
an SR row.

**Provisional, as a spine amendment must be.** SN-006 was already `Modified`; no
`status` cell was flipped, nothing was attested, and the amendment machinery is
expected to flag it. The sitting countersigns.

### OI-32 + OI-33 — re-pointed on the owner's direction, still pending

**Not a ruling.** The owner is *considering a generated approach*: one living
source of "this is what this component does", but rather than meticulously
maintaining it, **a generated list of all requirements inside a component** —
the SRs and LLRs tied to it. The acknowledged gap is that it **does not show
internals**, and the owner argues that may be a **benefit**: it is not trying to
show implementation.

On knowledge packs the owner wonders whether those could be derived too, though
it might take more attributes — **if SRs were tagged with the hat that derived
them, knowledge packs could be tied to HATS rather than components**, which
would *"dissolve knowledge packs as something to infer, and instead set it as
something derived from the SR or LLR based on how the need surfaced in the first
place."* Net: **both** pieces of information a component was meant to carry
become derived.

Both rows gained the generated approach as a first-class option with its FOR and
AGAINST (OI-32 option (d), OI-33 option (e)) and a **feasibility** paragraph
grounded in what the repo already has — measured, not sketched:

- `docs/requirements/hats.toml` **exists**, with **16** ratified hats.
- **18 SR rows already record their deriving hat — in PROSE**
  (`Hat-derived (hat.MAINTAINER)`, …), covering 11 of the 16. Nothing mechanical
  reads any of it. **Zero LLR rows record a hat at all.**
- Component membership today is a **`component` tag on the PRIMITIVE rows**
  (LLR/IF/ASSET/PART), exactly as the shipped components template prescribes:
  **161 of 161** LLR rows carry one (CMP-008 53, CMP-009 52, CMP-006 35,
  CMP-007 21), **57 of 125** IF rows do — and **SR rows carry none (0 of 72)**.

So, plainly: an **LLR-tier component view is buildable today with no new
attribute**. The **SR half needs a derivation path** — SR→LLR→`component` is the
only one available, and on it **60 of 72** SRs have at least one LLR child, **12
have none** and would appear in no view, and **6** have children in more than one
component so the derived value is a **set**. The **knowledge half needs a new
SR-tier hat attribute**, whose first 18 values are already written in prose.

Neither brief designs the thing; both say plainly that **execution is its own
WI**. OI-33's dependency on OI-32 is now **existential rather than locational**:
if the generated view is ruled, most of OI-33's question ceases to exist — (b),
(c), (d) and (e) of its five obligations are answered by the generator — and
what survives is the narrower "leave the requirement rows correct at close".

### OI-36 / OI-38 / OI-39 — pending, with the owner's questions and the answers on the row

**OI-36.** The owner asks whether the 49 can ride WI-455 so it happens at once.
Answer, in two parts. **It can, and that supports (b):** WI-455's lane IS still
open (`docs/work/active/wi455-architecture-retirement/`), and that lane already
owns the `Contract` cell's other rules, so the 46 rows are rewritten once.
**Caveat:** that lane's remainder is itself **blocked behind WI-469**, whose own
title says it "unblocks wi455's column-drop: re-author first, then drop what has
become derivable". So the 49 do not merely ride WI-455 — they **inherit its
blocker**. The hold must therefore go on a live surface with the chain named.

**OI-38.** The owner asked what "size" refers to. It is the size of the **lane
resume surface** — the document an agent reads to resume a lane. Nothing else.
The tripwire **warned and never blocked** (`status_size_warning` printed and
returned `None` when `limit <= 0`; it could not fail a run, a gate or a step),
which matches both hat lenses reaching a smell rather than a defect. And the
surface it watched is now a **generated integrator artifact whose size the
generator owns** — which is why a rebuild is a new requirement against a new
subject, not a restore.

**OI-39.** The owner asks for **research** and **leans toward minting**, while
noting the answer must be **language-agnostic, not Python-specific**. A research
briefing is in flight; the row waits on it. Language-agnosticism is recorded as a
**binding constraint on any answer**: the rule as implemented is Python-shaped
twice over (`symbol_findings` searches `.py`; "identifier-shaped" is a Python
identifier), so a minted SR must state that a design row's named symbol
**resolves in its named implementation unit** and leave the mechanism to the
declared stack profile.

### OI-40 — pending, unchanged.

### OI-41 — minted: a generated view can be fresh and carry nothing

The owner's meta-question: *"Why did these only show up on open-items when I
prompted? Is there some other mechanism / reference that could help reinforce
that ideally all items surface in open-items.toml for single point review?"*

**The failure is not staleness.** Before today `gen_open_items --check` reported
*up to date* — truthfully: the HTML matched its regeneration. The registry held
22 rows, 21 `ruled` and one `pending` which was the inert `OI-000` placeholder,
so the owner surface rendered *"No pending decision — the owner queue is empty"*
while ~10 genuine decisions lived in log fragments, `docs/provenance-allow`
entries and session reports. **Every freshness gate here asks whether the
artifact matches its regeneration; none asks whether the source was populated.**

**The strongest lead: the surfaces already announce the deferral in a detectable
phrase.** Measured at `77f6edd1`:

- `docs/provenance-allow` — **19 of its 34 entry lines** literally end *"Owes an
  open-item row at the sitting"*, and its header states the rule for the whole
  file. Nineteen written promises; until today, zero rows.
- Registry cells carry the same tell in three other spellings:
  `OPEN QUESTION FOR THE SITTING` (SR-043 `rationale`, SN-006 `acceptance` —
  both now resolved), `FLAGGED FOR THE OWNER` (IF-117 `notes`), `OPEN RULING`
  (`external.toml` header).
- **The sharpest instance is still live**: the mis-seeded `B-08`/`REL-004`
  watermark correction is named an OPEN RULING in `external.toml` **and** listed
  as item 1 of "What the sitting still has to RULE" in `docs/status.md` — and it
  has **no `OI-###` row**.

Options recorded: (a) a defer-phrase checker over live surfaces requiring a
resolving `OI-###`; (b) an `OI-###` field required by the allow-file entry
grammar; (c) a vacuity check on the generated view — report "0 pending" as a
finding when other surfaces defer; (d) prose only.

**Recommendation: (a), warn-first, with (b) as its hardest arm.** (b) is the
stronger mechanism where it applies — a required field is a constraint, a phrase
match is a detector — but it sees one file, and the one live miss remaining
(`B`/`REL`) is not in it. So: where a surface has a grammar, encode the
requirement as a **field**; where it has only prose, match a **declared**
vocabulary and warn. (c) folds in as presentation of (a)'s result, not as an
alternative. **(d) is refused on its own evidence**: 19 entries state the prose
rule in their authors' own words and produced zero rows.

**Stated limit:** none of this catches a decision deferred with no words at all.
What it buys is that a deferral *announced anywhere* resolves to a row — which is
exactly what failed, since all ten were announced somewhere and none was queued.

---

**Watermark.** `OI` 40 → 41, written by `trace.py --bump-ids` (the `# basis:`
line regenerates with it — the file is generated, not hand-edited).

**Live pending after this session: seven** — OI-32, OI-33, OI-36, OI-38, OI-39,
OI-40, OI-41. `docs/status.md`'s hand-authored rule-list line was corrected to
match.
