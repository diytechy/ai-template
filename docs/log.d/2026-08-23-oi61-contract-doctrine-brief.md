## 2026-08-23 — OI-61 filed: what the interfaces registry's `contract` cell is FOR

Deferred open items: OI-61 — the whole session IS the deferral. The owner asked
two questions about the `contract` cell in session; this sitting measured the
evidence and filed the brief, and every option in it is the owner's to rule.
Nothing was changed in the schema, in any contract cell, or in any checker.

**One-line summary.** The owner questioned whether an interface row needs a
detailed `contract` at all when 27 of them are hand-written restatements of a
CLI, and then whether `contract` is necessary at all where the fact is not
mechanically checkable; `OI-61` puts the four-option space in front of him —
generalize the CLI family, retire the prose registry-wide, add an LLM
three-way-agreement lens, or keep the prose and add rot tripwires — grounded in
a census taken over the live registry, with a staged recommendation and the
seam-test sub-question carried alongside.

### The owner's words

First message, verbatim: *"These interfaces are just methods that we provide to
downstream users. They will naturally terminate. Since they are methods, I would
think the consumer would just be the boundary interface that defines the main
connection to the template. … How is rot prevented between interfaces.toml and
the actual module providing the behavior? … Aren't there methods of generating
documentation for python files? … I would question if this is really an
interface that needs such a detailed contract if it's just restatement …
wondering if it should be generalized to just stating that this method of the SR
is provided as a behavior to the downstream users, where-upon the user would
reference the owner itself to know the details."*

Second message, verbatim: *"I would wonder if 'contract' is necessary at all.
Unless it is something that is easy to identify and test without an LLM (like
type: float … length-max: 6540), there is not a trivial way to design around it,
at which point the consumer might as well go back to the owner module and verify
what it actually provides instead of referring to a potentially rotting
document. … the source of what a module provides actually lives with the module
and is validated with the tests … ideally there would be some comment generated
at the source, validated by its own tests, and some method to kick off an LLM
based interface validation layer to ensure what the owner does, what it says it
does, and what the test checks around that interface are all agreed upon. …
there might be times an interface doesn't need a test, if these are lower level
interfaces to build up to bigger functionality, maybe the parent functionality
is all that needs to be tested."*

### The census the brief is built on

Measured over the live registry before anything was edited; the full set is in
the row's `decision` field.

<!-- fig: cmd="python - # tomllib over docs/requirements/interfaces.toml + external.toml: CLI-contract population, owner tier, boundary ties, contract lengths, signal typing, Contracts: docstring coverage" rev=d16ddbb2 -->

- **135 live IF rows, 46 `Provides` / 89 `Consumes`. 27 contracts contain
  `CLI:`, and all 27 are `Provides` — 59% of that tier.** 26 of the 27 literally
  open `<module>.py CLI:` (`IF-053` the exception). Owner tier 9 `SR` / 18 `LLR`.
- **Seven of the 27 tie to `B-05`** (`IF-013`/`014`/`015`/`016`/`017`/`018`/`048`)
  — exactly the seven whose counterpart is `external:`; the other 20 name an
  internal counterpart, 15 of them `scripts/check`. Registry-wide: 28 boundary
  ties, 25 of them B-05.
- **Contract length on the CLI rows: min 128, median 180, mean 273.5, max 800.**
  Thirteen over 200, seven over 300, and **four breach the ruled 500-character
  ceiling** (`IF-121` 587, `IF-015` 722, `IF-044` 788, `IF-103` 800), drawing
  `trace.if_contract_advisories`' fourth rule (warn-first by the WI-443 ruling).
  Whole registry: median 374, mean 380.7, 34 rows over the ceiling.
- **The presence link is 27/27 complete and caught neither rot exhibit.** Every
  one of the 27 modules declares its own id on a `Contracts:` docstring line;
  `check_trajectory.interface_findings`' two arms are pure set differences over
  ids, warn-first forever, and compare no cell content. `IF-055` still names
  `SCHED_*` constants with zero grep hits in `schedule.py`; `IF-080` still says
  `--no-ff onto a candidate worktree`, the phrase `WI-390` slice 1 had already
  corrected in `PROCESS_OPTIONS.md` — both banked by that program close as
  "banked here, not fixed".
- **`signal` is 100% populated (127 `variable` / 8 `discrete`) but 25 rows —
  14 of them CLI rows — carry the `DERIVED, NOT HAND-TYPED … re-type it by hand`
  note.** The typed embryo the owner's "type: float, length-max: 6540" points at
  exists at one bit of resolution, and on half the family it was inferred rather
  than authored.
- **Nine of the 27 are also in the twelve-row report** — `IF-001`, `IF-005`,
  `IF-009`, `IF-011`, `IF-013`, `IF-014`, `IF-015`, `IF-044`, `IF-053` — so the
  ownership judgement and the contract-doctrine question land on the same rows.

### The brief

`OI-61`, `status = "pending"`, in the house form: the owner's two messages
quoted whole, the ten-point census, the counterweights carried honestly
(`WI-495`'s dossier adjudicated five owner picks by *reading the contracts*;
source comments rot too; an LLM lens is a cost and a new judgement surface), the
interactions named (the twelve-seam report, the pending `counterpart` →
`consumers` rename, B-05 as the natural consumer for the adopter-facing rows),
and four lettered options each with FOR/AGAINST plus a sub-question on the
seam-test posture. The sub-question's honest finding: there is **no** existing
"verified by the parent's tests" idiom — the `Verification` vocabulary's only
exemption is LLR-exemption for `Analysis`/`Inspection`/`Attest`, `PROCESS.md`
holds "Every SR needs ≥1 TC row regardless of method", and IF rows carry no
`Verification` cell at all, so the position cannot currently be stated.

**Recommended:** (a) now as a measured first step *declared as staged toward*
(b), with a scoped dose of (d)'s named-symbol check on surviving prose, (c)
deferred on a stated condition, and the sub-question sanctioned now as a
warn-first `verified_by` pointer. The argument is that (a) and (b) are the same
answer at two confidence levels and only one is measured — (a) runs the
hypothesis as a controlled trial on the third of the registry where the
restatement is provable, and its outcome is the number that makes (b) either
obvious or refutable.

### Deliverables

- **`OI-61` appended** to `docs/requirements/open-items.toml`, `pending`.
- **`docs/id-watermark` bumped** `OI 60 → 61` by `trace.py --bump-ids` (never by
  hand); one space raised, seventeen written.
- **`docs/open-items.html` regenerated** — the surface reads **1 pending
  decision(s)** again, and the Pending-decisions band carries the card.
- **`docs/status.md` re-pointed, forward-only** — the top block's "no pending
  row" sentence, correct since `OI-60`'s ruling this morning, now names `OI-61`
  and says what it blocks (nothing).

### Deviations from the brief-for-this-session

- **`wi_refs` is absent rather than empty.** The carrier refuses an explicit
  empty string (`an unset cell is an ABSENT KEY … a third state the readers
  disagree about`), so the key is omitted — the correct spelling of "no
  execution row yet", which is the truth here: every option is unruled.
- **Nothing else moved.** No schema field, no `contract` cell, no checker, and
  no shipped template — the session's instruction was to file the brief only,
  and the two rot exhibits (`IF-055`, `IF-080`) are deliberately left standing
  as the brief's own evidence rather than fixed underneath it.

### Gates

- `python -m pytest -q -n auto -m smoke`
- `python scripts/check_smoke_budget.py --mode enforce`
- `python project-trajectory/scripts/check_docs.py --root . --stale`
- `python project-trajectory/scripts/check_trajectory.py --strict`
- `python project-trajectory/scripts/gen_open_items.py --root . --check`
- Registry-append only, no script or test touched: **no full suite owed**, and
  no byte-budgeted file was modified.
