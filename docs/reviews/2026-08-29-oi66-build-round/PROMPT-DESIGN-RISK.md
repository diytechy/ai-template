You are reviewing four design decisions taken while building a feature in the repo at c:\Projects\ai-template. I need an adversarial read on RISK, especially risk to DOWNSTREAM ADOPTERS of this kit. Be blunt; say which decisions are wrong.

BACKGROUND. This repo ships a reusable process kit. Downstream repos copy it in. A Python module can declare the interface seams it provides with a docstring line:

    Contracts: IF-001, IF-021 — the seams this module declares.

`gen_arch_map.module_contracts()` harvests those ids. We are building a feature (ruled as OI-66 option (a)) where each module ALSO states the contract BODY for each seam it declares, harvested into a new committed, freshness-gated `docs/interface-reference.md`, so a registry cell can point at the module instead of restating it.

Read these to ground yourself:
- `project-trajectory/scripts/gen_arch_map.py` — `_is_contracts_marker`, `module_contracts`, `module_contract_bodies`, `build_contract_reference`, `_contracts_doc_exit`, `_refuse_ambiguous_continuation`
- `tests/test_gen_arch_map.py` — the new tests at the end, and `test_contracts_and_if_edges`
- `docs/requirements/open-items.toml` — `[open_item.OI-66]`
- `project-trajectory/PROCESS.md` section 8

THE FOUR DECISIONS:

**D1 — the harvester now requires the marker at LINE START.** It was "the line contains the word Contracts". That harvested `IF-080` out of `handback.py`'s sentence *"No `Contracts:` line, deliberately: the integrator seam this extends is IF-080"* — a negated declaration read as a declaration. Fixing that was a binding precondition of the ruling. The new rule: strip a leading `#`, then the line must start with `Contracts:`. All 57 real anchors in this repo satisfy it. BUT the existing test `test_contracts_and_if_edges` uses a MID-LINE form (`"""Module A. Contracts: IF-003, IF-004"""`) and now fails. An adopter using the mid-line form would SILENTLY lose their declarations on upgrade.
My proposed resolution: keep line-start strict, and ADD a loud named warning when a line contains `Contracts:` with IF ids but does not open with it — so the regression is named, never silent. Then update the test fixture.
QUESTIONS: Is line-start the right grammar at all, or should the fix instead target the negation specifically? Is a warning sufficient mitigation for an adopter-visible silent behaviour change, or does this need a RESYNC_PACK migration entry / a version bump / a deprecation window? Is there a form of the negation bug that line-start does NOT fix (e.g. a line that opens with `Contracts:` inside a longer denial)?

**D2 — the body grammar.** After the marker line, a block opens on a line whose first token is `IF-###:` and runs to the next such line, a blank line, or the end of the docstring; wrapped lines join into one paragraph. A body whose id is NOT on the marker line raises `ContractsGrammarError`. QUESTIONS: is this parseable unambiguously against real docstring prose? What legitimate docstring content would this misparse as a body block? Is hard-failing the right severity, given the rest of this harness warns first and gates only under `--strict`?

**D3 — the reference lists a declared seam that states no body**, printing "_no contract stated in this module._" rather than omitting it. QUESTION: does surfacing 135 unstated seams make the generated document useless noise on day one, and would omitting them hide a real gap?

**D4 — "deliberately no contracts" needs no syntax.** A module that does not open a line with `Contracts:` declares nothing; `handback.py`'s prose denial is just prose. OI-66 flagged that fixing the harvester "raises the question whether a module may declare 'no contracts, deliberately' as a first-class state". I decided it does not need one. QUESTION: is that right, or does the absence of an explicit "none, deliberately" marker mean a module that SHOULD declare a seam is indistinguishable from one that deliberately declares none — and does any check depend on telling those apart?

Also answer: **what did I miss?** Anything in this build that is likely to break an adopter, or that contradicts something already in PROCESS.md or the interfaces template.

Do not edit any file. Return a written review, ranked by risk, with a clear verdict per decision: KEEP / CHANGE (say to what) / REVERT.
