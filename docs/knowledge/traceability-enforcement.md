# Traceability enforcement: registry→code versus code→registry

This pack preserves what published evidence (retrieved 2026-08-18) supports
about enforcing traceability links, and what this repo's own source tree
measures. It exists because OI-39 and OI-42 are about two *different*
obligations that read as one sentence. Rulings stay in `open-items.toml`; this
pack holds the evidence they rest on.

## Findings retained

**The two directions are not the same problem, and the evidence differs
sharply.** REGISTRY→CODE — a design row names a realization symbol and a
checker verifies it binds — is *assert-and-verify*: the human writes the claim,
the machine falsifies it. CODE→REGISTRY — a source comment cites a requirement
id — is an *annotation convention*: the machine can check the id exists but not
that it is the right one. Every finding below sorts into one of these two, and
almost nothing transfers between them.

**Assert-and-verify beats discover-and-link, measured.** Automated trace
recovery is not gate-grade. On the same project and tooling, text→text recovery
scores MAP 86.5 while design→Java scores 51.6
([arXiv:2306.10972](https://arxiv.org/abs/2306.10972)) — the artifact gap, not
the algorithm, is the ceiling. Across the eleven standard CoEST benchmarks the
best classical IR method averages F≈48.7, and plain VSM beats LDA and LM-JM
(ICSME 2018). LLMs have not changed it: LiSSA (ICSE 2025) reaches req→code best
F1 .322 against VSM's .282 and is *worse* than the baseline on some projects;
EasyLink (ICSE 2026) showed the standard 99-false-link sampling is unrealistic
(true average 1,530 candidates) and that under a realistic distribution SOTA
P@1 falls 32.5 → 14.4 while plain VSM beats it. Contamination of LLM results by
benchmark leakage is largely unmeasured. So a checker that *verifies a claimed
link* is a categorically better instrument than one that *proposes links*.

**Standards require the association, not the representation.** DO-178C §11.21
makes Trace Data a lifecycle data item requiring bidirectional LLR↔source
associations, whose stated purpose is that no code is orphan or dead — and it
specifies no representation. Trace Data is enumerated ALONGSIDE Source Code,
not inside it. IEC 62304's normative traceability chain omits source code
entirely; code-implements-requirements appears only as a review-criteria NOTE.
No surveyed commercial tool (DOORS, Jama, codebeamer, IBM EWM, Helix, LDRA)
requires the link to live in code; Polarion offers optional in-source tags for
three languages. **ISO 26262 and IEC 61508 could NOT be verified from primary
text** and are recorded here as unchecked rather than as support.

**Code-side annotation conventions are not maintained.** No measured decay RATE
for trace links exists anywhere — Mäder & Gotel (JSS 2012) say so themselves —
so everything here is a PROXY and is labelled as one. Cross-sectionally: ~48% of
commits carry no issue tag in six Apache projects *chosen for good discipline*
(ICSE 2018); bug→commit linkage runs 8–55% and is severity-biased, so the
missing links are not random (FSE 2009); only 13–20% of code changes trigger a
comment update, and renames are among the LEAST likely changes to (ICPC 2019,
1,500 systems); of seven audited safety-critical projects, NONE was fully
conformant, with 0–80% of required links missing (ICSE 2014).

**Benefit studies measure only consumption.** The headline results — 24% faster
and 50% more correct (n=71), 21%/60% (n=52) — hand subjects PRE-BUILT CORRECT
links. They measure the value of *having* traceability, not the cost of
producing or maintaining it. Production and upkeep cost is essentially
unmeasured in the field.

**The per-LOC cost figures are vendor folklore.** "$100/line" traces back to a
vendor quote in a trade magazine; "25–40% overhead" to a consultancy's own
marketing, whose apparently-independent IEEE citation is by the same author.
The FAA's own study says the cost "is generally high" and gives no figure. Do
not cite any of these three as evidence in either direction.

**The structural reason code-side ids cannot be mechanically checked for
meaning.** Under ruling D-4 (`docs/repo-lock.md` §D-4) supersession is deletion
and an id is never re-minted. So a retired id sitting in a comment is
LEGITIMATE HISTORY — `intake.py`'s "`SN-031` retired X" is a true sentence
about a completed removal. A checker over code-side ids therefore either gates
on accurate history (wrong) or needs a per-site human ruling (unscalable).
EXISTENCE-checking is still possible and cheap; MEANING-checking is not. This
asymmetry, not effort, is why the two directions get different instruments.

### This repo's own measurement (2026-08-18)

The kit mandates the code→registry direction unconditionally in two SHIPPED
documents: `PROCESS.md:161` ("Code carries back-links (`Implements: SR-007,
LLR-014`)") and `AGENTS.template.md:83`/`:102` ("`Implements: SR-007, LLR-014`
on implementing symbols"; "**Every public symbol** … include `Implements:
SR-/LLR-`"). Measured against the kit's own scripts:

METHOD — an AST walk over the 59 modules in `project-trajectory/scripts/*.py`,
counting module-level `def`/`class` whose name does not start with `_`, which is
`gen_arch_map.scan_module`'s own public-API rule; back-links counted as lines
literally matching `Implements:\s*(SN|SR|LLR|TC)-\d+`; ids resolved against the
four spine registries loaded with `tomllib`. Cross-checked by an independent
route: `grep -hE '^(def|class) [A-Za-z]'` over the same files returns 782, and
the single excess reconciles exactly — `check_figures.py:10` is a docstring line
beginning "class cheap instead:". (That the cross-check's one error was a regex
matching prose is the same failure the harvester makes below, at smaller scale.)

- **781 public symbols. 2 carry a literal `Implements:` back-link — 0.26%.**
  Both are in `subagent_gate.py` (`decide` at :130, `main` at :187) and both
  read `Implements: SR-043, LLR-040`.
- **Reverse coverage: 1 of 161 live LLR rows (0.6%)** is named by any
  `Implements:` back-link in the scripts — LLR-040.
- **300 three-digit spine-id citations** (`\b(SN|SR|LLR|TC)-\d{3}\b`) appear
  across the scripts, spanning **83 distinct ids, of which 8 name no live
  registry row** (21 occurrences): SN-000, SN-013, SN-016, SN-030, SN-031,
  SN-032, SR-001, SR-141. Most are D-4-legitimate history; SR-141 is not (below).
- **The harvester fabricates links from prose.** `gen_arch_map.implements()`
  regexes any spine id out of a symbol's docstring OR the ~4 comment lines above
  its `def`. Result: **50 of 781 symbols get a non-empty `Implements` column,
  62 (symbol, id) back-links in total — so 60 of the 62 (97%) were never
  declared**, and **13 of the 62 (21%) name no live row**. Five are pure prose
  examples: `trace.id_sort_key`'s docstring "so SR-9 orders before SR-10" is
  harvested as back-links to SR-9 and SR-10, and `trace.triangle_findings`'
  hypothetical "a TC citing LLR-1 next to SR-2 when LLR-1 decomposes SR-1"
  becomes three more. The column does not report the convention's adherence; it
  reports a regex's reading of nearby English.
- This repo commits no rendered map today (the scaffolded `docs/architecture.md`
  target retired at WI-455), so the fabricated column is LATENT here and SHIPS
  to every adopter who splices the map into `AGENTS.md`.
- **`docs/enforcement-audit.md:90` is itself now stale on this point.** It
  records the convention as unenforced Prose — correct — but adds "the
  meta-repo's own scripts carry none and the column is empty". Two carry it, and
  the column is non-empty for 50 symbols, nearly all of it fabricated. The audit
  under-describes its own gap.

**The WI-425 decay instance, verified.** `docs/log.md` (2026-08-11) records the
repoint campaign after the 2026-08-10 sitting retired SN-030/031/032: **69
explanatory comments and docstrings** across kit scripts and tests cited the
deleted ids, and nothing mechanized catches that. The campaign could not be
mechanized — its own heading is "**Read every site, no sedding**" — because
under D-4 the token alone does not decide: 56 sites were repointed *by what they
name* (rung, shape), **11 were kept as accurate history**, 2 were deferred, and
one (`agent_route.py:143`) was flagged as a lower-confidence call rather than
silently resolved. One site turned out not to be a citation at all but synthetic
fixture text, where repointing would have MANUFACTURED a link.

Two things measured today make the decay concrete rather than theoretical:

- **`dispatch.py:310` still cites SR-141**, in `_judgement_first`'s docstring,
  and SR-141 is not a live row — it merged into SR-148 on 2026-08-14
  (`docs/log.md:32342`). `git log -L 310,310:…/dispatch.py` shows that line was
  **written by WI-425 itself** (`08eb70fd`, 2026-08-11, "repoint retired
  SN-030/031/032 citations"). The hand-audited repair decayed in **three days**,
  and nothing noticed for four more.
- **`adjudicate_brief.py` was born citing retired ids.** Its SN-031 and SN-030
  section headers (:213, :289) and its SN-032 module docstring landed in
  `6a1293c2` (WI-424) on 2026-08-11 — the day AFTER the sitting retired those
  ids and the same day as the sweep that was cleaning them up. A one-off audit
  cannot outrun concurrent authoring.

### Language-agnostic symbol oracles, ranked

For the registry→code direction, ranked by fitness against this kit's
constraints (stdlib-preferred, hermetic, Windows + POSIX, zero adopter burden):

1. **universal-ctags** — ~150 parsers, JSON Lines output parseable by the
   stdlib, prebuilt Windows binaries, GPL-2.0, and **zero annotation required of
   the adopter**. Sharp edge: BSD ctags also answers to `ctags`, so a probe must
   match the literal string "Universal Ctags" in `--version`.
2. **Doxygen ≥ 1.16.0** (Jan 2026) — now has NATIVE `\requirement` /
   `\satisfies` / `\verifies` commands emitting `<satisfies>` XML plus a
   bidirectional `requirements.xml`, and dangling-reference warnings that can
   FAIL THE BUILD. The most complete off-the-shelf answer, but only ~12
   languages.
3. **SCIP** — a stdlib-readable protobuf index, but producing one needs a
   per-language indexer and the CLI ships no Windows binary.
4. **tree-sitter** — 371+ languages, but a compiled dependency with no stdlib
   route, and since v1.0.0 the language pack downloads grammars at runtime: a
   hermeticity hazard, not just a dependency row.
5. **LSIF** — dead. Its own community index is archived and points at SCIP.
6. **LSP direct** — needs a language server and its toolchain per language, with
   a CI-hostile cold start.

**The best single idea in the space is OpenFastTrace's REVISION SUFFIX**
(`artifact~name~revision`): a covering tag names the requirement *and the
revision it covered*, so bumping a requirement's revision turns every stale
covering tag into a REPORTED DEFECT. It converts silent decay into loud failure
— the one mechanism found that addresses the meaning problem without a per-site
human ruling, by making the human ruling *demanded at the right moment* instead.

## Application here

- **Enforce the direction the evidence supports.** registry→code is
  assert-and-verify and already hard-gates here (`check_doc_refs.symbol_findings`
  under `--strict`). Keep it hard, and state its obligation in terms an adopter
  whose implementation units are not `.py` files can satisfy.
- **Do not mint a code→requirement back-link obligation.** No standard requires
  the representation, no surveyed tool requires it, the proxies say conventions
  like it are not maintained, and this repo adheres at 0.26% while shipping the
  rule unconditionally.
- **If code-side ids are touched at all, check EXISTENCE, never meaning.** A
  stdlib regex asking only "does this id name a live row, or is it explicitly
  marked history" is language-agnostic by construction and would have caught the
  SR-141 site. Meaning-checking is refused by D-4, not by cost.
- **Fix the harvester before trusting its column.** A column populated 97% from
  undeclared prose is not evidence of adherence, and it is shipped machinery.
- **Cite this pack, not its numbers, when arguing.** The in-repo figures are
  reproducible by the method above; re-derive rather than re-quote.

## Failed or bounded approaches

- **Automated link recovery as a gate** — best classical F≈48.7, LLMs no better
  and worse under a realistic candidate distribution. Fine as a suggester, never
  as a bar.
- **Mechanizing a repoint campaign** — refuted in this repo at WI-425: 69 sites,
  11 of them accurate history, one a fixture that would have gained a fabricated
  link. The token does not decide.
- **A one-off hand audit as the fix** — measured to decay in three days
  (`dispatch.py:310`) and to be outrun by concurrent authoring the same day
  (`adjudicate_brief.py`).
- **Regex-over-prose as a link harvester** — `gen_arch_map.implements()` reports
  SR-9, SR-10, SR-1, SR-2 and LLR-1 as requirement back-links because a
  docstring used them as *sorting and counter-example illustrations*.
- **Citing per-LOC traceability cost figures** — "$100/line" and "25–40%
  overhead" are vendor and consultancy folklore with circular sourcing.
- **Citing ISO 26262 / IEC 61508** for what they require of source code — not
  verified from primary text here, so not available as support.
