+++
id = "WI-472"
title = "Mint the SR that states the CodeSymbol-anchor obligation, plus its LLR and TC, and re-point IF-117 (OI-39 ruled (a) MINT, 2026-08-19). The strongest checker in the repo has no requirement and no design row: check_doc_refs.symbol_findings decides when decomposition is FINISHED — under the D-9 ladder, LLR definition terminates where a token binds — and it is HARD under --strict, yet it is normative only in OI-20's ruling. THREE ROWS AND ONE RE-POINT: (1) an SR stating the obligation — a design row's named realization symbol RESOLVES within its named implementation unit, and a row naming no resolving symbol is not discharged; (2) an LLR naming check_doc_refs.symbol_findings (owed under EITHER ruling, since a hard --strict gate with no design row is a gap on the repo's own terms); (3) a TC. Then IF-117's req_refs/owner re-point onto the new rows, retiring the standing note that no design row is answerable for the owner-side endpoint. THE BINDING CONSTRAINT, owner 2026-08-18, is LANGUAGE-AGNOSTICISM and it is not a wording preference: the rule as implemented is Python-shaped in two places at once (symbol_findings searches .py modules; 'identifier-shaped' is a Python identifier), and the kit's doctrine is a stack-agnostic core with a Python-first REFERENCE. The shall must be satisfiable by an adopter whose implementation units are not Python files, with the resolution mechanism left to the declared stack profile exactly as the harness commands already are. A row that says '.py' ships a Python requirement to every adopter. THE GUARD: write the SR against the OBLIGATION, not against check_doc_refs — if the shall reads as a description of the checker, it was written wrong, and language-agnosticism is the testable form of that guard. EXPLICITLY OUT OF SCOPE: no code-to-registry back-link obligation is minted here. That is the opposite direction, its evidence points the other way, and it is OI-42's subject — state in the ruling record that it was considered and left there, or the next reader finds an SR about code-and-requirement traceability and reasonably infers the Implements: mandate was ratified alongside it."
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

Minted SR-180 ("a design row is discharged only by a realization symbol
that resolves"), LLR-180 (`check_doc_refs.symbol_findings` +
`gen_arch_map.module_bindings`, CMP-006) and TC-175 (12 existing test
nodes as evidence — the behavior already ships and is covered), all
Drafted at phase 5, and re-pointed IF-117's `req_refs` → SR-180 and
`owner` → LLR-180, rewriting its standing no-design-row note to record
what is now answerable. The shall is EARS unwanted-behaviour form, written
against the OBLIGATION and language-agnostic word by word: a realization
symbol, an implementation unit, and a resolution rule read from the
declared stack profile — no extension, no checker name, no Python-shaped
term; SN-003 cited as a parent so the altitude is traced. The row's own
rationale states no back-link obligation is minted or implied (the OI-42
boundary). LLR-180 names BOTH halves of the seam because IF-117 is a
Consumes row whose owner-side endpoint is gen_arch_map — exactly the
endpoint the retired note said nothing covered — and the CMP-006 tag was
chosen ON MEASUREMENT (zero-line strict diff; CMP-007 would have falsified
the components-note straddle claim). Text rules pre-run with statuses
forced Approved: all empty, so ratification cannot red them. Watermarks
SR/LLR/TC → 180/180/175; snapshot refreshed. The three Drafted rows drop
phase 5 to DevStg-Below and the stage to DevStg-Reqs with ex-draft holding
— the designed new-phase signal, awaiting ratification. Full suite
2661/13 green.

## Context

(2026-08-19, repo-review triage.) The 2026-08-19 repository review's M-08
(archived at `docs/archive/repo-review-2026-08-19.md`) supplies fresh evidence
for the obligation this row states: three live LLR anchors verified stale
(LLR-087, LLR-088, LLR-112 — their repair is WI-482's, not this row's), while
two of the review's five claims were REFUTED on verification (LLR-015's
symbol exists; LLR-172 is honestly Drafted/not-built). The refuted pair is
exactly the distinction the minted SR must survive: a planned symbol declared
as planned is not a stale anchor. The OI-42 boundary in the title stands —
the review's code-to-registry findings route there, not here.
