## 2026-08-18 — OI-39's research round lands: two directions, one knowledge pack, and a second open item

A three-agent research round produced a decision-grade briefing for **OI-39**.
This fragment records what was preserved, what was re-measured, and the one
finding that turned out to be independent of how OI-39 rules.

Filed as a **log fragment with no WI row**, following this month's precedent for
in-session owner-directed rounds (`2026-08-18-doc-diet`, `-okf-off`,
`-scripts-sweep`, `-spine-hardening`, `-budget-guard`). Nothing here rules
anything: both open items stay `pending`, no `status` cell moved, and no spine
row was minted.

---

### 1. The finding that reorganized the question

**"Traceability between code and requirements" names two obligations, and the
evidence points opposite ways on them.**

- **registry → code** — a design row names a realization symbol, a checker
  verifies it binds. *Assert-and-verify.* This is what
  `check_doc_refs.symbol_findings` does, hard under `--strict`, and it is what
  **OI-39's own text has always been about**.
- **code → registry** — a source comment cites a requirement id
  (`Implements: SR-007, LLR-014`). *An annotation convention.* Mandated
  unconditionally in two **shipped** documents, enforced by nothing.

The phrasing that sent the question to research named the **second**. OI-39 is
the **first**. Ruling them together would have taken the evidence for one and
applied it to the other — so the second direction was **split out as OI-42**
rather than folded in, and OI-39 gained an `(e)` option recording *why* the
widened mint is refused rather than merely not chosen.

### 2. What was preserved

`docs/knowledge/traceability-enforcement.md` (new; index row added,
`CMP-006`, reviewed 2026-08-18). It holds the durable half: why recovered links
are not gate-grade (best classical IR ≈ F 48.7 across the eleven CoEST
benchmarks; LiSSA's best req→code F1 .322 against VSM's .282; EasyLink showing
SOTA P@1 falling 32.5 → 14.4 under a realistic candidate distribution); what
DO-178C §11.21 and IEC 62304 actually require (the **association**, never its
representation — and Trace Data is enumerated *alongside* Source Code, not
inside it); the proxies for annotation decay, each labelled as a proxy because
**no measured decay rate for trace links exists anywhere**; that the benefit
studies hand subjects pre-built correct links and so measure consumption only;
that the per-LOC cost figures are vendor and consultancy folklore with circular
sourcing; and the ranked language-agnostic oracles, with **universal-ctags**
first and OpenFastTrace's **revision suffix** recorded as the best single idea
in the space.

Two things are recorded as **not** verified rather than quietly dropped: ISO
26262 and IEC 61508 could not be checked against primary text, and LLM
benchmark contamination is largely unmeasured.

### 3. What was re-measured here before it was written down

Per the standing rule that measured claims get re-derived by an independent
route. **Method:** AST walk over the 59 modules of
`project-trajectory/scripts/*.py`, counting module-level `def`/`class` whose
name does not start with `_` — `gen_arch_map.scan_module`'s own public-API
rule; back-links counted as lines literally matching
`Implements:\s*(SN|SR|LLR|TC)-\d+`; ids resolved against the four spine
registries with `tomllib`.

**Independent cross-check:** `grep -hE '^(def|class) [A-Za-z]'` over the same
files returns **782**, and the single excess reconciles exactly —
`check_figures.py:10` is a docstring line beginning `"class cheap instead:"`.
That the cross-check's one error was a regex matching prose is the same failure
the harvester makes below, at smaller scale.

| measurement | value |
|---|---|
| public symbols in `project-trajectory/scripts/*.py` | **781** |
| carrying a literal `Implements:` back-link | **2** — `subagent_gate.decide` (:130), `subagent_gate.main` (:187), both `SR-043, LLR-040` |
| ratio | **0.26 %** |
| reverse coverage against live LLR rows | **1 of 161 (0.6 %)** — LLR-040 |
| three-digit spine-id citations in the scripts | **300** occurrences, **83** distinct ids |
| distinct cited ids naming **no live row** | **8** (21 occurrences) — SN-000, SN-013, SN-016, SN-030, SN-031, SN-032, SR-001, SR-141 |
| symbols given a non-empty `Implements` column by `gen_arch_map.implements()` | **50** |
| harvested (symbol, id) back-links | **62** — of which **60 (97 %) were never declared** and **13 (21 %) name no live row** |

**The harvester fabricates links from prose.** `implements()` (:178–189) regexes
any spine id out of a docstring *or* the four comment lines above a `def`, and
never requires the word `Implements`. So `trace.id_sort_key`'s docstring —
which explains sorting, "so `SR-9` orders before `SR-10`" — publishes SR-9 and
SR-10 as requirements that function implements, and
`trace.triangle_findings`' hypothetical "a TC citing `LLR-1` next to `SR-2` when
`LLR-1` decomposes `SR-1`" publishes three more. This repo commits no rendered
map today (the scaffolded `docs/architecture.md` target retired at WI-455), so
the fabrication is **latent here and ships to every adopter** who splices the
map into `AGENTS.md`.

**One correction to an existing surface.** `docs/enforcement-audit.md:90` is
right that the convention is unenforced Prose, but adds "the meta-repo's own
scripts carry none and the column is empty". **Two carry it, and the column is
populated for 50 symbols, nearly all of it fabricated.** Not corrected in this
change — it is named in OI-42's recommendation as owed in the same change as
whatever is ruled, so the correction rides the ruling rather than pre-empting it.

### 4. The WI-425 decay instance, verified — and it is worse than the brief said

`docs/log.md` (2026-08-11) records that retiring SN-030/031/032 left **69**
explanatory comments and docstrings citing deleted ids, "a dangling pointer
nothing mechanized catches". The campaign heading is **"Read every site, no
sedding"**: 56 repointed by *what they name*, **11 kept as accurate history**, 2
deferred, one flagged low-confidence, and one that turned out to be synthetic
fixture text where repointing would have *manufactured* a citation. The reason
it could not be mechanized is ruling **D-4** — supersession is deletion and ids
are never re-minted, so a retired id in prose is legitimate history.

Two things measured today:

- **`dispatch.py:310` still cites `SR-141`**, in `_judgement_first`'s docstring,
  and SR-141 is not a live row — it merged into SR-148 on 2026-08-14
  (`docs/log.md:32342`). `git log -L 310,310:…/dispatch.py` shows **that line
  was written by WI-425 itself** (`08eb70fd`, 2026-08-11, *"repoint retired
  SN-030/031/032 citations"*). The hand-audited repair went stale in **three
  days**, and nothing noticed for four more.
- **`adjudicate_brief.py` was born citing retired ids** — its SN-031/SN-030
  section headers (:213, :289) and SN-032 module docstring landed in `6a1293c2`
  (WI-424) on 2026-08-11, the day *after* the sitting retired those ids and the
  same day as the sweep cleaning them up. A one-off audit cannot outrun
  concurrent authoring.

Both go to the same conclusion, and it is a bound rather than a complaint:
**existence-checking is decidable, meaning-checking is not.** A checker over
code-side ids either gates on accurate history (wrong) or needs a per-site human
ruling (unscalable).

### 5. What changed on the surfaces

- **`docs/knowledge/traceability-enforcement.md`** — new pack; index row in
  `docs/knowledge/README.md` (`CMP-006`, 2026-08-18).
- **OI-39** — disambiguation prepended to `decision`; the oracle and standards
  evidence added to `blast_radius`; a new option `(e)` recording the refused
  widened mint; `recommendation` rewritten to three separate answers — **mint
  the SR for the enforced direction, written against the obligation** (not
  against Python, not against `check_doc_refs`), **do not mint a
  code→requirement back-link obligation**, and **the LLR is owed either way**.
  Still `pending`; the owner rules.
- **OI-42** — minted for the code→registry direction, with the measurements
  above and four options: (a) cheap existence scan, (b) soften the guide + tighten
  the harvester, (c) an OFT-style revisioned marker, (d) do nothing.
  Recommendation is **(b) with (a) as a second arm**, on the ground that one
  half of this is not a gap but a **defect** — shipped machinery producing false
  statements — while the other half is a rule the repo has already declined by
  revealed preference, 779 times. **"Do neither" is the current state**, and it
  is exactly what `docs/enforcement-audit.md` exists to catch — which is why
  that file's own drift is the sharpest argument against (d).
- **`docs/id-watermark`** — `OI` **41 → 42** via `trace.py --bump-ids`.
- **`docs/open-items.html`**, **`docs/status.md`** — regenerated.
