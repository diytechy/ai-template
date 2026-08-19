# Provenance ruling + the diet — external adversarial round (Sol)

**Date:** 2026-08-18 · **Round:** external adversarial, over today's six
commits `ff03d323..HEAD` — `3b8d306d` (OKF export turned off for this repo,
`docs/okf/` removed, kit layer unchanged), `712ff788` (SN joins the always-on
Status enum floor; `is_draft_need` case-insensitive; the stale `CSV`→`TOML`
token sweep; `docs/work/README.md`), `903b7bcc` (the always-loaded-surface
diet: `CLAUDE.md` 9,891→6,677 B, `docs/status.md` 230→144 lines,
`byte-budget-guard` SKILL.md 24,336→4,101 B with test-enforced caps),
`a5b558d5` (the WI-455 architecture retirement — `docs/architecture.md` and its
template deleted, flows to `docs/runtime-flows.md`, architecture derived into
`PROJECT_STATE.html`), `3dd665fc` (the artifact-voice rule reaches the SN tier,
warn-only `sn_artifact_advisories`), `4e9a5c8a` (the owner ruling: no
provenance citation in any living registry cell).
**Model:** `gpt-5.6-sol` — the session banner reports
`model: gpt-5.6-sol · provider: openai · reasoning effort: medium ·
sandbox: read-only · approval: never`, codex-cli 0.145.0 (cross-family per the
routing policy). Read-only — no writes, no commits. One launch, ran to
completion in ~6 min wall (19:38:24 → 19:44:17 local).
**Command:**

    codex exec -m gpt-5.6-sol -c model_reasoning_effort=medium \
      --sandbox read-only -C /Users/diytechy/Documents/ai-template \
      --skip-git-repo-check -o <last-message-file> - < <hostile-brief>

the house command plus an explicit `-m` (the user config defaults to
`model_reasoning_effort = "xhigh"`, so `medium` is set on the invocation) and
an output file so the final message is captured byte-exact rather than scraped
from the transcript.
**Brief:** hostile — "find defects, not praise"; every finding to carry a
`file:line`, a quoted string, and a concrete failure scenario, ranked
MAJOR/MINOR; eight named hunting grounds (contradictions the kit still ships,
vacuous or false-firing detectors, sweeps that deleted meaning rather than
provenance, the diet's dropped instructions, the architecture retirement's
dangling references and un-derivable intent, the OKF dogfooding asymmetry,
missing `RESYNC_PACK.md` entries, and anything else actually wrong). The
reviewer was told to read the live files at HEAD, not only the diff, and to
take the diff itself with `PROJECT_STATE.html` and `docs/okf/**` excluded (the
raw `git show` is multi-megabyte almost entirely from those two). It was told
not to read `OWNER_SCRATCHPAD.md`.
**Scope reviewed:** `project-trajectory/PROCESS.md` §3,
`project-trajectory/RESYNC_PACK.md`,
`project-trajectory/scripts/{trace,trace_text,plan_coverage,gen_okf}.py`,
`project-trajectory/skills/{spine-authoring,registry-hygiene,byte-budget-guard}/SKILL.md`
(and the `.claude/` + `.agents/` mirrors),
`project-trajectory/RUNTIME_FLOWS.template.md`, `docs/requirements/*.toml`,
`docs/provenance-allow`, `docs/process.toml`, `docs/runtime-flows.md`,
`CLAUDE.md`, `tests/{test_trace_rules,test_trace,test_bootstrap,conftest}.py`.
**Verdict:** REJECT · 5 MAJOR + 2 MINOR — **nothing adjudicated or applied
here**; per the standing pattern the author re-verifies every finding and the
owner rules on it.

---

## The verdict, verbatim

Fenced as text so it is byte-exact and so the reviewer's paths and quoted
fragments are not read as repo links by `check_docs.py`.

~~~text
VERDICT: REJECT — 5 MAJOR, 2 MINOR

## Findings

1. **MAJOR — The shipped kit still explicitly licenses Markdown provenance citations that the new absolute rule forbids.**  
   `project-trajectory/PROCESS.md:107-111` quotes: “No provenance in a living registry cell … no … citation … no ruling, sitting, review-round or open-item reference.”  
   `project-trajectory/RESYNC_PACK.md:1809-1812` contradicts it: “`.md` is **excluded**: a document named in a spine cell is usually a *citation*, which §3's provenance clause already sanctions.”  
   `tests/test_trace_rules.py:957-969` then pins the contradiction as desired behavior: “`Spec of record: docs/concurrency-restructure.md`” must produce no advisory. The live `docs/requirements/stakeholder-needs.toml:241` contains exactly this forbidden form: “Spec of record: `docs/archive/specs/parallel-wi-dispatch.2026-07-20.md` + `docs/concurrency-restructure.md`.”  
   Why it is wrong: the repealed permission survives simultaneously in shipped migration guidance, executable comments, tests, and a living need.  
   Failure scenario: an adopter follows RESYNC_PACK, retains a design-document citation in an SN acceptance cell, runs every strict check, and receives a clean result despite violating the new §3 rule.  
   Suggested fix: remove the “sanctions” language, route Markdown citations to the log like every other provenance frame, detect them separately from artifact naming, and reverse the negative regression test.

2. **MAJOR — The provenance detectors knowingly pass forbidden prose and do not cover all living reason-cell registries.**  
   `project-trajectory/scripts/trace_text.py:485-490` limits the general detector to SN/SR/LLR/TC. The only off-spine extension is IF `Notes`/`SignalNote`; CMP and EXT reason cells are absent.  
   `tests/test_trace_rules.py:137-148` explicitly requires silence for “Names the ruling that retired the id” and a dated design-document pointer. Yet §3 forbids “ruling” and “date stamp” without requiring a structured ID.  
   The missed cases are not hypothetical. `docs/requirements/external.toml:124` says: “A model CLI is just a model CLI … (owner merge, 2026-08-13o).” Lines 101, 109, and 148 likewise retain decision, confirmation, ruling, and edit-history prose. `docs/requirements/stakeholder-needs.toml:148` still says “OPEN QUESTION for the sitting” and “the sitting rules…”.  
   Why it is wrong: the regex recognizes only enumerated structured shapes such as `sitting-3`, `RULING-3`, or an edit verb close to an ISO date. Plain-English citation frames—precisely what the rule bans—pass. All these checks are permanently warn-only, so even detected violations never affect a gate.  
   Failure scenario: a downstream author writes “kept by the owner’s second review” or “the ruling retired this alternative” in a rationale. No token matches, strict checking exits successfully, and the forbidden historical frame becomes permanent registry text.  
   Suggested fix: either narrow the stated rule to the patterns actually enforceable or broaden coverage using cell-aware checks across every governed reason-cell registry. Add mutation tests for plain-English review/ruling prose and current EXT/CMP rows; establish a zero-residue promotion criterion instead of “warn-first, always.”

3. **MAJOR — Three landed downstream migrations remain unselectable `Reserved` entries with no commit anchor.**  
   `project-trajectory/RESYNC_PACK.md:1741-1746` says detector migrations must be recorded and that commit-range selection composes with artifact inference. But the landed work-item README change remains `### Reserved` at line 1546, the SN artifact rule remains `### Reserved` at line 1789, and the provenance ruling remains `### Reserved` at line 1851. Lines 1849 and 1920 still say they are “awaiting [their] `[since <sha>]`”.  
   Why it is wrong: these changes already landed in `712ff788`, `3dd665fc`, and `4e9a5c8a`. The pack’s defining selection mechanism cannot associate them with any recorded-kit-version range.  
   Failure scenario: a repo stamped before these commits resyncs by selecting only entries whose `[since SHA]` falls in its range. It misses the new `docs/work/README.md`, leaves its need rows unswept, and retains prohibited provenance even though it copied the new scripts.  
   Suggested fix: replace every `Reserved` heading with the actual landing SHA, and add a test that rejects unanchored migration entries once their referenced file or detector exists at HEAD.

4. **MAJOR — Fresh adopters are still required to keep an authored architecture overview, but the scaffold no longer provides any place or form for it.**  
   `project-trajectory/PROCESS.md:162-165` still requires: “keep a hand-written one-page overview above” the generated architecture and calls for “one-page-readable architecture.”  
   `project-trajectory/RUNTIME_FLOWS.template.md:3-18`, however, defines the authored half solely as “hand-written Mermaid sequence diagrams” covering runtime behavior. The architecture migration tells existing adopters that their old overview is unchecked and optional: `project-trajectory/RESYNC_PACK.md:1764-1767` says to “keep whatever hand-written overview you value … or delete the file.” Fresh scaffolds receive no equivalent high-level-flow or module-responsibility section.  
   Why it is wrong: source-tree derivation can recover modules, symbols, and imports; it cannot derive intended layering, responsibility boundaries, rejected alternatives, or a conceptual data flow. The deleted template explicitly carried high-level flow and module-responsibility authoring slots; the replacement does not.  
   Failure scenario: a new adopter has two modules that are intentionally separated by a policy boundary but happen not to import each other. The dashboard derives no boundary, the runtime sequence need not mention it, and there is no scaffolded overview where the design intent is required to be written. A reviewer sees structure but cannot distinguish intentional separation from accidental absence.  
   Suggested fix: either add a compact static-architecture overview section to `RUNTIME_FLOWS.template.md` and check its presence, or repeal the surviving PROCESS requirement and explicitly relocate design intent and responsibility boundaries to named registry fields.

5. **MAJOR — The default-on OKF product has no real canonical-TOML end-to-end test after dogfooding was disabled.**  
   `docs/process.toml:144-150` turns the live export off while stating the kit still ships it. `tests/conftest.py:907-920` says TOML is covered by this repo’s own registries, but `make_minimal_project` immediately deletes the TOML spine and writes legacy Markdown/CSV at lines 943-954. The positive OKF tests all use that helper; the fresh TOML scaffold test is placeholder-only and therefore vacuous.  
   Why it is wrong: once `okf_export=false`, the meta-repo’s real TOML registries no longer exercise `gen_okf` or its dashboard consumer. The claimed dogfood coverage therefore does not exist for a populated canonical carrier.  
   Failure scenario: a change breaks TOML field mapping or TOML resource links while legacy CSV remains correct. Every OKF test passes, the meta-repo skips generation, and a new adopter—whose scaffold uses TOML and ships OKF on—gets a stale, empty, or malformed bundle.  
   Suggested fix: add a populated TOML-spine OKF integration fixture, including generation, `--check`, self-pruning, links, and dashboard consumption. Keep legacy-carrier coverage as a separate compatibility test.

6. **MINOR — `provenance-allow` is an indefinitely renewable, over-broad suppression mechanism.**  
   `project-trajectory/scripts/trace.py:1587-1593` parses only the text before ` — ` and stores it as a key; it validates neither the reason, an owner, an open-item reference, nor an expiry. A row-only key suppresses every governed cell, as pinned by `tests/test_trace_rules.py:152-160`. `docs/provenance-allow:14-43` contains 23 standing entries that merely say they are owed “at the sitting,” with no dated deadline or mechanically joined open item.  
   Why it is wrong: future citation frames added to an allow-listed row can be silently suppressed, and nothing proves the promised open item exists or that the list shrinks.  
   Failure scenario: an author adds a new dated changelog sentence to another cell of an allow-listed row. A row-wide exception hides it forever; subsequent sittings have no failing check or stale-exception report.  
   Suggested fix: permit cell-scoped entries only, require a resolvable OI identifier and owner/deadline, report stale or unmatched entries, and fail when an exception survives past its declared review boundary.

7. **MINOR — The claimed CSV→TOML prose sweep left shipped instructions that prescribe the wrong repair.**  
   `project-trajectory/skills/registry-hygiene/SKILL.md:20-21,44-50` still defines integrity as CSV column-count checking and tells an adopter to fix an unquoted comma by quoting the CSV cell. Canonical spine registries are TOML. `project-trajectory/scripts/plan_coverage.py:369-372` still reports “no system-requirements.csv” when the canonical registry is absent, and `project-trajectory/scripts/gen_okf.py:7-9` still says “the reviewed truth stays the CSV registries.”  
   Why it is wrong: these are current downstream-facing instructions and diagnostics, not historical migration prose.  
   Failure scenario: an adopter gets a TOML parsing or missing-registry failure, invokes the shipped registry-hygiene skill, and is told to inspect a CSV header and quote a CSV cell that does not exist.  
   Suggested fix: describe carrier-neutral integrity first, give separate TOML and legacy-CSV remedies, and make diagnostics name the resolved canonical stem or both supported carriers.

## What I checked and found clean

- The 15 SN condition-voice rewrites did not reveal a defensible obligation loss; the strongest changes were carrier-to-condition rewrites.
- The provenance sweep generally retained the durable reasoning; I found no supportable before/after semantic-deletion finding.
- The three `spine-authoring` mirrors and three `byte-budget-guard` mirrors are byte-identical.
- Current capped sizes are below their limits; the new caps test kit source files, not adopter-modified copies.
- The architecture retirement removed the executable scaffold/harness dependency on `docs/architecture.md`; the defect is the missing authored-intent replacement, not a surviving runtime read.
- `is_draft_need` is case-insensitive at HEAD.
- I found no evidence that turning OKF off directly breaks the disabled meta-repo harness; the defect is loss of canonical live coverage.

## Confidence and gaps

High confidence from live-file inspection, commit-specific diffs, detector code, and regression-test assertions. I did not execute pytest because the sandbox is read-only and the suite creates scaffolds, generated reports, caches, and temporary repositories. I did not inspect `OWNER_SCRATCHPAD.md`. I excluded the regenerated `PROJECT_STATE.html` body and the 551 deleted OKF files except for targeted references, and did not perform a visual dashboard review.
~~~

## Author's note — provenance of this document, not adjudication

Recorded so the round's provenance is exact. **None of this is a ruling on the
findings**, and nothing above was corrected, softened or re-ordered: the fenced
block is the reviewer's final message byte-for-byte, including its trailing
two-space line breaks.

- One launch, no retries; exit code 0. The reviewer's own transcript shows it
  read the live files, ran `git`, and grepped the shipped kit; the earlier
  round's harness-kill failure mode did not recur.
- The reviewer states it did **not** run `pytest` (read-only sandbox), so every
  claim about a test — vacuous, pinning the wrong behavior, or absent — is a
  code-reading claim and is the author's to re-verify by execution.
- It also excluded the regenerated `PROJECT_STATE.html` body and the 551
  deleted `docs/okf/` files except where it cited them, and did no visual
  dashboard review. Those exclusions were instructed by the brief.
- It did not read `OWNER_SCRATCHPAD.md`, as instructed.

## Not done here (stated so its absence is not read as coverage)

- No finding was applied. This document is this round's only write; the
  registries, scripts, tests and process docs are byte-identical to `4e9a5c8a`.
- No finding was confirmed or refuted. The CONFIRMED / CONFIRMED-IN-PART /
  REFUTED disposition table that the earlier rounds carry is deliberately
  absent — it is the author's next step, not the collector's.
- Only one reviewer ran this round (Sol). No second-family cross-check.
