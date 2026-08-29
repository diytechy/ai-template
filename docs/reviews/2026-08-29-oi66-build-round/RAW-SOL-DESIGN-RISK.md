## Verdicts

| Decision | Verdict | Bottom line |
|---|---|---|
| D1 — line-start marker | **CHANGE** | Keep line-start grammar, but a warning alone is inadequate. Add a migration entry and make legacy-looking mid-line declarations a blocking, named diagnostic during upgrade. |
| D2 — body grammar | **CHANGE** | The current parser is unsafe and does not implement its documented grammar. Use an explicit `Contract IF-###:` opener and validate structure. |
| D3 — render every missing body inline | **CHANGE** | Do not omit gaps, but do not bury the reference under 135 repeated placeholders. Summarize them in a compact debt section and enforce coverage separately. |
| D4 — no explicit “none” syntax | **KEEP** | “None” is derivable from the interface registry. Another declaration would duplicate state and could lie. Fix the registry-to-module join instead. |

Overall: D2 and the adopter migration are release blockers. This is presently a mechanism prototype, not a complete implementation of OI-66(a).

## Ranked findings

### 1. Critical — the build has not moved the contract’s source of truth

PROCESS.md still says the registry `Contract` cell states the typed crossing and is fed verbatim into planning briefs (`PROCESS.md`). The shipped interface template still requires and explains that cell (`interfaces.template.toml`). `plan_briefs` still consumes it as authority.

Meanwhile, the new generator says the module states what the provider promises (`gen_arch_map.py`). Those are competing authorities. Until the registry schema, PROCESS.md, planner input, checks, and template all agree that the registry points to the module body, downstream adopters will maintain two contracts and assume both are authoritative.

This directly contradicts the one-home purpose of OI-66.

Required change:

- Define precisely what remains in the registry cell—probably the crossing/link, not the contract body.
- Make planning briefs follow the generated/module body.
- Update PROCESS.md and the interface template before shipping.
- Add a check that the registry’s provider resolves to the exact module declaring and stating that IF body.

The present reverse check only asks whether an IF id appears in *some* module (`check_trajectory.py`). Putting `IF-021` on the wrong module can pass.

### 2. Critical — D2’s parser is structurally wrong

The documentation says bodies occur “after the marker,” but the implementation scans the entire docstring (`gen_arch_map.py`). I confirmed:

- `IF-001: prose` before the marker is harvested as the body.
- Two `IF-001:` bodies silently keep the second.
- A comment-form declaration can never carry a body because bodies are read only from the docstring.
- Any ordinary docstring line beginning `IF-###:` is treated as contract syntax.

Legitimate collisions include examples, protocol descriptions, changelogs, mapping documentation, or prose such as `IF-001: legacy identifier retained for compatibility.` Because `line.strip()` discards indentation, putting it in an indented example does not protect it.

**D2: CHANGE.** Use syntax that does not resemble ordinary prose, for example:

```text
Contracts: IF-001, IF-021

Contract IF-001:
    ...

Contract IF-021:
    ...
```

Then:

- Recognize exactly one canonical declaration marker.
- Recognize only `Contract IF-###:` as a body opener.
- Reject duplicate bodies, empty bodies, and undeclared body ids.
- Define whether comment-form declarations are legacy declaration-only or support equivalent comment bodies.
- Return a concise named diagnostic, not an uncaught traceback.

A hard failure is appropriate for malformed *explicit contract syntax*. It is not appropriate for an ordinary `IF-###:` prose line that the parser merely guessed was syntax. Missing bodies should be warn-first during migration and promotable later.

### 3. High — D1 is the right grammar but the proposed compatibility posture is insufficient

Targeting the particular word “No” would be wrong. Negation is unbounded: “not,” “does not declare,” quoted examples, historical statements, and other phrasings would recreate the defect. Declaration syntax should be structural, so line-start is correct.

But the old mid-line form is demonstrably supported behavior: the existing test encodes it (`test_gen_arch_map.py`), and the targeted run currently fails. A warning does not compensate if the declaration is immediately dropped and downstream checks remain warn-first.

**D1: CHANGE** to:

- Keep strict line-start recognition.
- Detect mid-line `Contracts:` plus IF ids as a named legacy/ambiguous grammar finding.
- Make that finding blocking in the upgrade/freshness path, or temporarily continue harvesting an explicitly defined legacy form while warning. Silent dropping is unacceptable.
- Add a `RESYNC_PACK.md` migration entry with a command/search recipe and the required rewrite.
- Let `docs/kit-version` identify the kit upgrade; do not bump every IF row’s `version`, because marker syntax did not change the interface semantics.

A separate semantic version bump is warranted only if this kit has a release-version scheme beyond its existing commit stamp.

Line-start does not eliminate false declarations. I confirmed this still harvests `IF-080`:

```text
Contracts: not IF-080; this is an example, not a declaration.
```

The marker line needs an anchored positive grammar, not “starts correctly, then harvest every IF token anywhere on the line.” Parse a canonical comma-separated id list and reject other marker-like forms. A line-start marker with zero valid declarations should be an error.

### 4. High — there is no downstream migration or scaffold delivery

OI-66 explicitly says adopters take this feature, but:

- `project-trajectory/stack.ini.template` does not declare `docs/interface-reference.md` (`stack.ini.template`).
- Bootstrap does not scaffold an interface-reference document.
- `RESYNC_PACK.md` has no migration entry.
- Existing adopters own their `docs/stack.ini`; overwriting kit scripts will not add the generated-artifact declaration for them.
- The normative process and interface template have not been updated.

Therefore fresh adopters do not receive the committed reference, and existing adopters have no instructions for creating, declaring, populating, or migrating to it.

This needs a `RESYNC_PACK` entry regardless of the D1 compatibility choice. The repo’s own contributor guide explicitly says adopter-forcing changes must be surfaced.

### 5. High — deleting or failing to scan the document can produce a false green

`_contracts_doc_exit` exits successfully when the target is absent (`gen_arch_map.py`). The comment claims `[generated]` and links will detect deletion, but the generated census validates enforcer wiring, not artifact existence, and the necessary normative links have not been added.

Also, `scan_contracts` silently skips unreadable, syntactically invalid, and non-UTF-8 Python modules (`gen_arch_map.py`). A freshness gate must not report success after silently omitting source.

Required:

- If the reference is declared in `[generated]`, absence must fail.
- Parse/read failures must fail the reference build or be governed by the existing `--strict-parse` contract.
- Opt-in should be determined once from configuration, not independently by “file happens to exist.”

### 6. Medium — D3 confuses presentation with enforcement

Repeating `_no contract stated..._` 135 times will dominate the document and make the useful contract bodies hard to find. Omitting them entirely would be worse because it would hide real debt.

**D3: CHANGE** to:

- Render stated contracts as the primary reference.
- Add a compact “Unstated declarations” section grouped by module, e.g. `scripts/foo — IF-001, IF-021`.
- Keep headline counts.
- Add a separate coverage finding: declared seam lacks a non-empty body.
- Baseline/allowlist existing debt if necessary, then promote new missing bodies immediately.

The generated prose is not a substitute for a detector. Right now a reference containing zero bodies can be perfectly fresh and green.

### 7. Medium — D4 is correct, but the existing check must become module-specific

No explicit `Contracts: none` is needed. The registry already knows which modules provide and consume seams, and the connectivity checker already uses `source`/`sink` honesty valves (`check_trajectory.py`).

An explicit “none” would be redundant state:

- Registry says module provides IF-021.
- Module says “none deliberately.”
- Now another rule must decide which declaration wins.

Instead, derive the obligation:

- If the registry says module X provides IF-021, X must declare IF-021 and state its body.
- If the registry assigns X no provided seam, absence is legitimate.
- A module need not restate “none.”

Thus **D4: KEEP**, but only after replacing the current global-id reverse check with an exact provider-module join.

## Additional omissions

Before release, add tests for:

- Mid-line legacy declaration diagnostics.
- A line-start denial such as `Contracts: not IF-080`.
- Body text before the marker.
- Duplicate and empty bodies.
- Comment-form declarations.
- Syntax/read failures during reference generation.
- Missing declared generated document.
- IF body stated by the wrong module.
- Fresh-scaffold delivery and an adopter re-sync fixture.
- Generated-marker text appearing inside a contract body; bodies are currently inserted as raw Markdown and could inject the reference’s own end marker.

No files were edited. The targeted test run produced **1 failed, 2 passed**; the failure is the existing mid-line declaration fixture.