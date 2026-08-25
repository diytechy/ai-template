## 2026-08-25 — WI-516: the 108 non-CLI contracts, measured and not touched — the CLI number does not generalize

Deferred open items: **OI-63** — the relocation question, filed pending at this
close as `OI-62`'s ruling sequenced it, with the measured per-family numbers in
its brief. It is the only thing this row owes the owner.

**Summary.** `OI-62`'s option (e) executed in full: every one of the 108 non-CLI
`contract` cells read per row in `WI-512`'s discipline, never regexed, **no
registry cell edited**. Both ruled obligations discharged — the durable per-row
verdict record at
[../plans/2026-08-25-if-contract-verdicts.md](../plans/2026-08-25-if-contract-verdicts.md)
and `OI-63` filed. The five ambiguous (d) tripwire findings triaged inside
tranche 1. The headline: **the CLI family's 87.7% does not generalize**, and it
misses in the direction option (d) predicted.

### THE NUMBERS, per family, separately

The ruling set the tranche grain so a heterogeneous population could not hide
behind one average. It could not.

| | CLI (WI-512) | tranche 1 `Provides` | tranche 2 `Consumes` | combined |
|---|---|---|---|---|
| rows | 27 | **19** | **89** | **108** |
| characters | 7,385 | 10,278 | 33,717 | **43,995** |
| RESTATEMENT | **87.7%** | **75.9%** | **60.8%** | **64.3%** |
| irreducible REMAINDER | 12.3% | 21.2% | 20.2% | **20.4%** |
| NON-CROSSING | not a category | 2.9% | 19.0% | **15.3%** |
| rows carrying a remainder | **40.7%** | **84.2%** | **61.8%** | **65.7%** |

Read as the owner's own question — how much would be missed once it is gone —
**35.7%**, against the CLI family's 12.3%. Only 21 of 108 rows are pure
restatement end to end, where `WI-512` found 16 of 27.

**The family split is recovered from git, not invented.** `WI-455` shed the
`direction` column, so "non-CLI `Provides` first, then `Consumes`" no longer
names anything in the live registry; the assignment is read off `d16ddbb2`, the
commit before the shed. It also turned up a fact neither brief had: **all 27
rows `WI-512` thinned were `Provides`**, so tranche 1 is only the 19 that pass
left behind.

<!-- fig: cmd="python -c \"rs=[l.split('|') for l in open('docs/plans/2026-08-25-if-contract-verdicts.md',encoding='utf-8') if l.startswith('| `IF-')];c=[[int(x) for x in r[2:6]] for r in rs if all(x.strip().isdigit() for x in r[2:6])];print(len(c),[sum(k) for k in zip(*c)])\"" rev=14759fc8 -->

### A hypothesis this pass held, and refuted

Going in, the expectation was that requirement-owned rows — no `detail` cell to
recover from — would carry markedly more remainder, which would have made the
relocation case nearly automatic. Measured: SR-owned 36 rows at 19.1%
remainder, LLR-owned 72 rows at 20.8%. Within noise. What the tiers DO differ
on is non-crossing prose, 8.6% against **17.4%**. Recorded as a refutation
rather than dropped, because the recommendation in `OI-63` would have been
different if it had held.

### The taxonomy, extended — and the extension that reshapes the question

`WI-512` named three remainder kinds; the ruling invited extension where the
population demands it. It demands seven more — typed shape, closed vocabulary,
**consumer-side obligation**, posture, compatibility guarantee, counterparty
calling convention, and a NON-CROSSING class. Honesty first: **four of the
seven were already latent in `WI-512`'s own kept clauses** (`IF-014`'s
idempotence, `IF-016`'s posture, `IF-044`/`IF-053`'s purity, `IF-010`'s library
seam), so its stated three did not cover all eleven of its own rows. This is
the taxonomy catching up.

Two of the additions bear directly on `OI-63`, which is why the brief is filed
wider than the ruling's one sentence:

- **Consumer-side obligations have no provider-side home by construction.**
  `IF-115` — *"a row that DECLARES a brief this seam cannot compose must be
  held for a human"* — binds the READER; the row's own `notes` say the
  obligation *"would otherwise be recorded nowhere"*. `IF-050`, `IF-116` and
  `IF-124` carry the same shape. A contract header on the provider's side
  cannot state it.
- **15.3% of characters belong in NEITHER home.** `IF-082`/`083`/`084`/`085`
  and `IF-138` state in their own text that their contract is another row's,
  then spend 110–250 characters on why the row exists; `IF-112` spends 330 of
  468 on the defect narrative of the carrier it replaced. Relocation would
  inherit that unchanged. The kit already ships the home — `rationale`, used
  ONCE in 135 rows (`IF-141`) — and `trace.py`'s own "Contract argues"
  advisory independently names **27** of these rows, its over-ceiling advisory
  **30**.

### The (d) tripwire triage — five ambiguous findings, all false positives

Re-run live: 7 findings over 5 rows, unchanged. `IF-055` left standing as
ruled. Each of the other five is a false positive with a concrete, mechanical
narrowing: `IF-038` `SUBAGENT_GATE` is an env-var key the module reads (teach
the ALL-CAPS arm about env keys); `IF-072` `SCAFFOLD_OMISSIONS` is a real
symbol in a module this row's own `consumers` cell NAMES (widen the resolution
surface to the row's declared endpoints); `IF-061` `docs/plans/DP-NNN-` is an
id template (decline placeholder segments); `IF-132` `registries/source` is an
English gloss that survived only because `registries` looks directory-shaped —
no such directory exists at the root (require the first segment to resolve at
the ROOT); `IF-143`'s `scripts/x` is a metavariable, and the honest fix there
is authoring, not a rule change. One true positive in seven is a precision that
would train a reader to ignore the rule.

### Banked findings — measured, not fixed, and none of them this row's to fix

- **`IF-117` is a second demonstrated rot exhibit and no token grammar reaches
  it.** Three false claims in one cell: *"the committed module map is a
  PUBLIC-API view"*, present tense for `docs/architecture.md` **retired at
  `WI-455`**; *"the `sym:` tier keeps reading the artifact"*, false —
  `load_symbol_oracle` reads `scan_inventory` and says so in its own docstring;
  and *"149 live LLR rows"* against a live **184**. The path arm is silent
  because that path is a legitimate declared absence; a stale COUNT is
  invisible to every arm. **`OI-61`'s (c) is NOT re-raised** — out of this
  row's scope by its spec, and this is the evidence a future raiser would use,
  not the raise.
- **Two further stale claims.** `IF-057` names `system-requirements.csv` as a
  live source; the carrier is TOML. `IF-061` describes a `work-items.csv`
  dual-write home this repo no longer carries — live-but-dormant compatibility
  code, so flagged stale rather than dead.
- **One contradiction.** `IF-115` says such a row is *"never dispatched with
  the worker assignment"*; its owner `LLR-167` says *"A refusal falls back to
  the worker assignment and PRINTS why."* One is wrong. Not adjudicated — this
  pass writes no cell.
- **One duplicated fact** (the Windows prompt-in-argv refusal, in both
  `IF-041` and `IF-064`) and **two opaque citations** (`IF-090`'s *"ruled
  decision 2"*, `IF-094`'s *"the ruled A1/A8 tables"*) — `IF-080`'s class.
- **The relocation target is less built than `OI-62`'s brief assumed.** The CLI
  relocation worked because `--cli-doc` produces a COMMITTED, freshness-gated
  `docs/cli-reference.md`. The module symbol inventory has no equivalent: the
  committed module map retired at `WI-455` and `docs/stack.ini`'s `[generated]`
  section declares no successor. Adopting a contract-header convention means
  building that artifact and its gate, not only agreeing a docstring line. It
  is in `OI-63`'s blast radius.

### Deviations from spec

- **The verdict document lives in `docs/plans/`**, the executor's call the
  ruling left open — on the `2026-08-22-interface-exception-dossier` precedent,
  since this is a dossier feeding a follow-on ruling rather than a review round.
- **The NON-CROSSING class is not in `WI-512`'s vocabulary and is not a
  remainder kind.** It is reported as its own third verdict because a two-way
  restatement/remainder split would have scored 6,715 characters of changelog
  as "irreducible", which is true and misleading at once.
- **Remainder and non-crossing character counts are clause SPANS, not post-edit
  lengths.** `WI-512` measured its `KEPT` figure by subtraction because it
  rewrote the cell; a pass forbidden to write cannot. Stated in the document
  and again in `OI-63`: the ROW counts are exact, the percentages are accurate
  to the clause.
- **`wi_refs = []` on the new OI row was REFUSED** by `spine_carrier` — under
  this carrier an explicit empty is a third state — and the key was deleted
  rather than the refusal worked around. The execution row is minted at the
  ruling, as `OI-62`'s was.

### Byte deltas on budgeted files

`AGENTS.template.md`, `CLAUDE.md`, `PROCESS.md`, `PROCESS_OPTIONS.md`: all
unchanged. This row edits no kit file.
