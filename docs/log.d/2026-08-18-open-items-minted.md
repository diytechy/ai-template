## 2026-08-18 — Ten decision briefs minted: the day's owner decisions reach the decision surface

**The problem.** `docs/requirements/open-items.toml` held 22 rows — 21 `ruled`
and one `pending`, which was the `OI-000` example placeholder. So
`docs/open-items.html` regenerated "up to date" while its pending band read
`No pending decision — the owner queue is empty`, and the day's ~10 genuine
owner decisions lived only in log fragments, `docs/provenance-allow` entries
and session reports. Ten of the eleven allow-file entries state in their own
words that the row "owes an open-item row at the sitting"; none had one.

**What was minted.** `OI-31` … `OI-40`, all `status = "pending"`,
`raised = "2026-08-18"`. Watermark `OI` 30 → 40, written by
`trace.py --bump-ids` (the `# basis:` line regenerates with it — the file is
generated, not hand-edited).

`open-items.toml` is **exempt from the provenance rule** (it is a decision log
whose subject IS provenance — `docs/log.d/2026-08-18-provenance-rule.md` §4,
"excluded wholesale"), so dates, ruling references and WI ids in these cells are
correct and expected.

| id | one-line |
|---|---|
| OI-31 | The freshness gates read the WORKING TREE, not the staged tree |
| OI-32 | `docs/cmp/` is a designed home that was never built |
| OI-33 | The component-spec maintenance protocol — components are the living spec |
| OI-34 | The derived-requirement label has no schema cell |
| OI-35 | Does the provenance rule reach a registry file's HEADER COMMENTS? |
| OI-36 | Scope of the provenance sweep at the IF tier |
| OI-37 | SR-043's fail-open vs SN-006's normative bound |
| OI-38 | SR-040's resume-surface tripwire — rebuild or strike |
| OI-39 | No SR states the CodeSymbol-anchor obligation |
| OI-40 | LLR-037 + TC-040 — the tripwire pair |

---

### 1. What each row rests on, and the corrections research produced

Each brief was researched against the tree rather than written from the raise.
Four claims in the raise were **corrected by measurement** and the corrections
are carried inside the rows:

- **OI-32.** SR-043 does **not** cite `docs/archive/specs/`. It cites
  `docs/archive/INTEGRATION_PLAN.md` Phase 4 (`system-requirements.toml:277`) —
  one level above `specs/`. The living rows citing archived material are SN-027
  (`stakeholder-needs.toml:241`), SR-049 (`system-requirements.toml:301`) and
  SR-043, and SN-027 and SR-049 cite **different** specs. The strongest evidence
  is not the empty directory: `derived-gate-model.2026-07-20.md` is read by six
  live scripts (`derive_gate.py:11,32`, `check.py:599,1221`,
  `check_trajectory.py:1656`, `trace.py:49`) from inside the archive.
- **OI-34.** The label population is **18**, not 15 or 17. Seventeen carry
  `(Derived-requirement label, added <date> — PROVISIONAL, unsigned.)`; the
  eighteenth, **SR-053** (`system-requirements.toml:326`), carries the *signed*
  form `(Derived-requirement label; charter ruled, row retained.)` and appears in
  no tally anywhere. That no artifact in the repo counts 18 is itself the
  finding — both sides of the ratification question are carried by wording.
- **OI-35.** The header population is **45 tokens across three registries**
  (stakeholder-needs 13, interfaces 17, external 15), not 5. Four of the needs
  registry's are of the shape that **gates** under `--strict` in a cell
  (`WI-454`, `WI-467`, two `PROCESS.md` citations). The exclusion is structural,
  not a policy: `spine_carrier.load` parses via `tomllib`, which discards `#`
  comments before any detector runs, and `cite_advisories`
  (`trace_text.py:678-716`) iterates rows keyed by id.
- **OI-36.** The 49 is a **sentence in a log fragment**
  (`2026-08-18-provenance-rule.md:213`) pinned by nothing —
  `if_contract_advisories` takes no `allow` parameter at all
  (`trace.py:1525`), unlike `if_note_advisories`. Re-measured live: 46 WI-id +
  3 decision = 49. The 8-frame worklist re-measured live at exactly 8.

Two further facts were verified rather than assumed:

- **OI-31.** `git archive 3b8d306d` into a scratch tree and
  `gen_trajectory.py --check --root <tree>` prints
  `project-state dashboard STALE in PROJECT_STATE.html` and exits 1, while the
  same binary on today's worktree exits 0. `3b8d306d:PROJECT_STATE.html` and
  `ff03d323:PROJECT_STATE.html` are the same blob (`5f63248d`), and that commit
  deleted 551 `docs/okf/` files — a direct input to the dashboard's Knowledge
  tab. Nine `check.py` steps are regenerate-and-compare; **none** reads the
  index, while the hook reads it in three other places
  (`hooks/pre-commit:260,277,290`).
- **OI-40.** TC-040's three function-granular evidence tests pass
  (`3 passed, 62 deselected`), and the row is still `Modified` because its
  `expected` cell says the tripwire clause is "unverified BY CONSTRUCTION".

### 2. What was deliberately NOT minted as an open item

An open item is an **owner decision**. Work that is already ruled, or that a
lane owns, is not one. Held out, with where each is tracked instead:

- **The `SN-027` allow-file line.** The residue review drafted the exact text
  and handed it to another lane (`2026-08-18-review-round-residue.md`,
  "Handoffs"); no lane has applied it. That is a task, not a decision — recorded
  inside OI-32's recommendation as owed either way.
- **Sweeping the seven non-`IF-117` frames of the 8-frame worklist.** Execution
  under whatever OI-36 rules; the worklist itself lives in
  `2026-08-18-review-round-detector.md` §7.
- **The `byte-budget-guard` 60-day-evidence rewording** and the other residue
  handoffs. Already dispositioned in the residue fragment.
- **The mis-seeded `B`/`REL` watermark mechanism.** Already the sitting's item 1
  in `docs/status.md`; it needs no brief because the question is stated there and
  the interim protection (the SPENT IDS block in `external.toml`'s header) is in
  place. Note it is *also* the one thing OI-35's extension must carve out.
- **The `LLR` for `check_doc_refs.symbol_findings`.** Owed under either of
  OI-39's answers, so it is a task; recorded inside OI-39's recommendation
  rather than given its own row.
- **A TC evidence-granularity census.** The file-granular-evidence finding
  discovered on TC-040 generalizes, but the response (a census, or a warn-first
  rule that a TC's evidence names functions) is work, not a decision — recorded
  inside OI-40's recommendation.

`OI-33` is the one row that is a decision **because** the owner framed it as
one: its five constraints (scope own work / correct level of detail / right
location / remove mutated decisions / do not restate the WI's scope) are stated
in the owner's terms and the row's job is to make them rulable, not to answer
them.

### 3. Couplings recorded inside the rows

- **OI-33 is downstream of OI-32** — there is no location to write into until
  `docs/cmp/` exists; if OI-32 rules RETIRE, OI-33 is struck rather than left
  pending.
- **OI-40 tracks OI-38** — the pair is the design and test half of the clause
  OI-38 rules on; it cannot resolve first and cannot resolve differently.
- **OI-38 feeds OI-34** — if SR-040's clause is struck, that row's derived
  label loses its subject and OI-34's population drops by one.
- **OI-36 carves `IF-117` out of its sweep** — its remaining tokens are the only
  live record of the gap OI-39 rules on.

### 4. Discipline

- `trace.py --strict-integrity`: `orphans=0 integrity=0`, unchanged from the
  pre-edit baseline. OI ids are integrity-checked and the watermark rose 30 → 40
  via `--bump-ids`, never by hand.
- `docs/open-items.html` regenerated: **0 → 10 pending decision(s)**, ten cards
  rendered `OI-31`…`OI-40`, and the
  `No pending decision — the owner queue is empty` empty-state is gone.
- `docs/status.md`: one net line. Its "exactly two items" claim was false the
  moment these rows landed, so the heading now names the ten briefs and points at
  `open-items.html`, with item 2 re-labelled as `OI-38`. S-3 (OI coherence)
  stands down under the `<!-- BEGIN GENERATED STATUS -->` block, so no
  orphan-brief warning is owed; the S-1 line-budget warning is pre-existing.
- `gen_okf` NOT run — dial off.
