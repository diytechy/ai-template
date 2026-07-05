# ai-template — Downstream Adoption Field Report

**From:** Finance-Auditor boot (kit `605252d`), 2026-07-04
**Scope:** limitations that surfaced scaffolding a **Node/TypeScript** product with a
**modified gate policy**, and the changes that would reduce that friction.
**Lens:** the kit's own constraint — *"flag anything that forces downstream repos to
migrate"* (IMPROVEMENT_PLAN.md). This complements, not duplicates, TEMPLATE_REVIEW.md
(which found green-before-ready issues on the Python reference itself); everything
here is about the **non-Python / policy-override** adoption path.

---

## Executive summary

The kit's core bet — a **stdlib-Python "process" layer that is genuinely
stack-agnostic, bolted to a swappable "product" layer** — held up well and is the
single reason a Node product was tractable at all. The friction was concentrated in
two seams:

1. **"Stack-agnostic" overstates the product layer.** It is really *Python-reference
   with a stack-agnostic process layer*. Adopting a non-Python stack meant editing
   ~6 files, and **one whole capability (the generated architecture map) has no
   non-Python/PowerShell path**, so this repo had to drop it. More seriously, the
   kit's flagship anti-false-green guarantee ("missing tool != pass") is **silently
   Python-only** and had to be re-implemented to cover the product toolchain.

2. **Gate-authority is hard-coded prose, not configuration.** A legitimate policy
   change (this repo runs one human gate instead of five) required scattering
   `MODIFIED-FROM-KIT` edits across 5 files — and the "pause for human approval"
   assertion is **duplicated *within* files** beyond what our enumeration
   anticipated, so the independent review had to catch the copies we missed. That
   is the kit violating its own single-source-of-truth rule.

Nothing here is a defect in the *process* — it caught real bugs and the gates worked.
These are **adoption-cost** issues: every one of them is a place where a downstream
repo pays to bend a Python/one-policy default into its actual shape.

---

## Limitations, ranked

| # | Limitation | Severity | Migration cost it imposes |
|---|---|---|---|
| A2 | `check.py`'s "missing tool != pass" guard checks Python module importability only (`importlib.find_spec`); it cannot see a missing Node/other toolchain | **High** | The kit's central honesty guarantee silently doesn't hold for product steps on any non-Python stack — a missing linter fails with a confusing crash or, worse, is skippable |
| A1 | Architecture-map generator is Python-AST-only (PowerShell reference port exists; **no JS/TS**) | **High** | A TS/JS/Go/… repo loses the generated-map freshness check entirely — must "drop-and-record" and hand-maintain the map, which is exactly the drift the generator existed to prevent |
| B1/B2 | Gate-authority policy is restated as prose in 5+ files, and duplicated *within* files, with no config to override | **High** | Any non-default gate policy is a scattered manual patch; duplication makes enumeration miss copies (ours did — reviews caught 3 un-enumerated assertions in AGENTS.md alone) |
| A3 | Test tiering is pytest-marker-based (`pytest.ini`, `-m`); no tier model for other runners | Med | Non-pytest stacks must invent a tier mechanism (we used test-directory tiers for vitest) and delete the dead `pytest.ini` |
| A4 | `setup.{sh,ps1}`, `ci/check.yml`, and the pre-commit format step all default to a Python venv + ruff/pytest install | Med | For a stdlib-process + Node-product repo the venv/pip install is pure waste; all three must be rewired |
| C1 | `TEMPLATE_REWRITES` (strip "copy-me" meta-prose on scaffold) covers only `process.md` | Med | Other scaffolded docs read as templates, not as the project's docs — `interfaces.md` shipped literally saying "Copy to docs/interfaces.md" |
| D2 | bootstrap `--stack` vocabulary is `python\|go\|rust\|powershell\|any` — **omits JS/TS/Node** | Med | The mechanism meant to tailor the scaffold to a stack can't name the most common web stack; we passed `--stack any` |
| C2 | Fresh scaffold is not fully green: `interfaces.md` scaffolds as an orphan doc (doc-navigability warn) | Low | Undercuts the "scaffold starts green" promise; every adopter either links it or learns to ignore the warning |
| C3 | Python-only artifacts (`pytest.ini`, the ruff/pytest toolchain assumptions) are copied unconditionally even when `--stack` says non-Python | Low | Dead files the adopter must recognize and remove |
| D1 | SR registry schema has no first-class `Area`/owner-hat column, though the process assigns domain-hat ownership of SRs | Low | Each project invents its own (we added `Area` as an ad-hoc 12th column); cross-project tooling and `trace.py` can't report hat ownership |

---

## What worked (do not "fix" these)

- **The `requires=()` process/product split is the hero.** Because trace / flows /
  docs / perf / arch-map-contract are declared stdlib-only, they stayed byte-for-byte
  untouched through a full stack swap. This is the kit's best portability decision.
- **Gate-scoped `docs/gate`** gave a genuinely green G1 scaffold and a CI bar that
  matches the project's real stage (modulo C2).
- **`MODIFIED-FROM-KIT` markers + the downstream-resync skill** are a sound
  deviation-tracking design; the problem (B) is only that the *targets* are
  duplicated, not that the marker convention is wrong.
- **The independent-reviewer / verdict protocol** caught four genuine requirement
  contradictions at G1 (an unpinned run-outcome vocabulary, a shall/AC conflict, an
  unrealized failure path, an inverted privacy adjective) — the review layer earns
  its cost.
- **bootstrap.py hygiene:** idempotence, the kit-version stamp, and the dirty-tree
  refusal all behaved exactly as documented.

---

## Recommendations (change → why), prioritized

### High

**R1 — Generalize "missing tool != pass" from modules to commands.**
In `check.py`'s `run_step`, before executing, also verify `cmd[0]` resolves
(`Path(cmd[0]).exists() or shutil.which(cmd[0])`) and emit the same
`SKIP(missing)`/`FAIL` as the Python-module guard.
*Why:* it is stdlib, cross-platform, harmless for Python steps, and restores the
kit's flagship anti-false-green guarantee for **every** stack. This is the single
highest value-to-effort change; it forces no downstream migration.
*(This repo already carries the patch — it could be promoted upstream verbatim.)*

**R2 — Make the product toolchain a declared profile read in one place.**
Today the product commands live inline in `check.py` **and** are re-encoded in
`setup.*`, `ci/check.yml`, `pre-commit`, and `pytest.ini`. Let a project declare
`format` / `lint` / `test+coverage` / tier-map **once** (a small `stack` block that
`check.py`, the launchers, and CI all read).
*Why:* collapses the ~6-file "EDIT FOR YOUR STACK" surface to one, and removes the
class of bug where the CI/pre-commit copy drifts from the check.py copy. Phase it —
even just having CI and pre-commit *call `check.py`* for the product steps (instead
of re-installing tools themselves) removes most of the duplication.

**R3 — Give the architecture map a non-Python path.**
The marker-block contract is already language-agnostic ("any generator that fills the
block works"); only the *fillers* are Python+PowerShell. Ship a JS/TS generator port,
**or** a tiny stack-neutral fallback that fills the block from a declared module
manifest, so a non-Python repo keeps *a* freshness check instead of dropping the step.
*Why:* Finance-Auditor lost the map-drift guardrail entirely — the exact anti-drift
lever the kit prizes — because "drop-and-record" was the only option offered.

**R4 — Make gate authority a declared policy, and de-duplicate the assertion.**
Introduce a single canonical statement of gate authority (a `docs/gate-policy` file
or one block in `status.md`) that the other docs **reference** rather than restate;
at minimum, collapse the "pause for human approval" claim to **one** sentence per
file.
*Why:* this repo's override legitimately touched 5 files, and because the claim was
duplicated *within* AGENTS.md (harness bullet, "Comment for humans" subsection,
entry-point parenthetical), our enumeration missed copies and only the review caught
them. A one-place policy makes an override a one-line change and makes it
mechanically checkable that no stale copy remains — enforcing the kit's own
single-source-of-truth rule on the kit itself.

### Medium

**R5 — Complete the `TEMPLATE_REWRITES` sweep (or move copy-me prose out of band).**
Every template that says "Copy this into…" should be rewritten on scaffold, or carry
that guidance in an HTML comment the rewrite strips.
*Why:* several scaffolded docs read as templates, not as the project's own docs;
`interfaces.md` was the concrete miss (shipped saying "Copy to docs/interfaces.md").

**R6 — Add JS/TS to the `--stack` vocabulary** (and, with R2, a matching profile).
*Why:* the scaffold-tailoring mechanism can't currently name the most common
downstream stack; `--stack any` is a workaround that also disables stack-aware skill
matching.

**R7 — Gate the Python-only product artifacts behind the declared stack.**
bootstrap already knows `--stack`; don't copy `pytest.ini` (and don't default the
venv/pip scaffolding) when the product stack is non-Python.
*Why:* removes dead files the adopter must recognize and delete, and stops
setup.* from doing a pointless Python install for a Node product.

### Low

**R8 — Fix the fresh-scaffold orphan-doc warning** (link `interfaces.md` from the
README skeleton, or exempt the inert `IF-000`-only file from the orphan check).
*Why:* "scaffold starts green" should be literally true, warnings included.

**R9 — Add a first-class `Area` / owner-hat column to the SR schema.**
*Why:* the process assigns SR ownership to domain hats but the registry can't record
it; a kit-level column lets `trace.py` report hat coverage instead of each project
inventing an ad-hoc column.

---

## One-line takeaway

The process layer is portable; the **product layer and the gate-policy prose are
not, and both pretend to be** — R1 and R4 are the two changes that would most reduce
the adoption tax, because each closes a place where the kit silently stops honoring
its own guarantee (no-false-green; single-source-of-truth) the moment a downstream
repo differs from the Python/one-policy reference.
