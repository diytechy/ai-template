# Adopting the kit in an existing repo (retrofit guide)

> `bootstrap.py` and the README quick-start assume a **new, empty** repo. This
> guide covers the harder, more common case: dropping the kit into a repo that
> already has code, history, CI — and possibly a non-Python stack. It is a
> reference doc (like `EXAMPLE.md`), not scaffolded into projects.

The short version: the **process layer ports everywhere as-is**; the **product
layer you rewire**; the two Python-reference generators (`gen_arch_map.py`,
`check_stubs.py`) you **port or explicitly drop — never leave passing
vacuously**. Requirements are **backfilled from the boundary outward**, not
retro-documented wholesale.

## 1. Scaffold into the existing repo

From the kit folder: `python scripts/bootstrap.py --dest /path/to/repo`.
Bootstrap never overwrites an existing file (no `--force`), so collisions are
reported as `skipped (exists)` — resolve each by hand:

- **`.gitignore`** — skipped if present; merge `gitignore.template`'s entries in
  (the generated composites under `docs/test/` must be ignored, or they churn
  every diff — `report.md`/`report.html`, `perf-report.md`, `perf-metrics.json`,
  `stub-report.md`). If you'd rather *keep* a composite tracked, drop its ignore
  line and tell `check_docs.py` to skip it as a scanned doc with
  `--ignore docs/test/report.md` (repeatable) so it isn't flagged as an orphan.
- **`.gitattributes`** — skipped if present; merge in the one load-bearing rule
  `.githooks/pre-commit text eol=lf`. Without it a Windows clone with
  `core.autocrlf=true` rewrites the extensionless sh hook to CRLF and its
  `#!/bin/sh` shebang breaks (the pilot hit this). `gitattributes.template` also
  pins `*.sh`/`*.command` to LF and `*.ps1`/`*.cmd`/`*.bat` to CRLF.
- **`docs/kit-version`** — always (re)written, not skipped: it stamps the kit
  commit this scaffold/re-sync came from (see "Re-syncing" below). Commit it, so
  the next re-sync is a diff, not a guess.
- **`.github/workflows/check.yml`** — if you have CI already, add the
  `check.py` invocation to it instead of adopting the reference workflow
  wholesale. Keep one definition of "passing": CI runs the same command you run
  locally.
- **`pytest.ini`** — Python repos with an existing pytest config: merge the
  tier markers (`smoke`/`full`/`release`) rather than replacing the file.
- **`src/`, `tests/`** — bootstrap only adds `.gitkeep`s; your layout stays.
  Point the harness at the real roots (`SRC`/`TESTS` in `check.py`).
- **`README.md`** — skipped if present (the common case). Retrofit the
  *evaluator's rungs* into your existing README instead: a "Run it" section
  pointing at the root `run.{cmd,sh,command}` launchers (fill their `RUN_CMD`
  with your start command — `run.cmd` and `run.sh`; `run.command` delegates)
  and a getting-started pointer at the `scripts/onboard.* → dev-setup → setup
  → check` ladder. A pure library deletes the launchers and describes usage.
- **Pre-commit hook** — `setup.{sh,ps1}` set `git config core.hooksPath
  .githooks`, which **overrides** any existing `.git/hooks` or hook manager
  (husky, pre-commit-framework). If you already have hooks, either call
  `.githooks/pre-commit` from your existing hook chain or skip the wiring —
  CI remains the enforcement of record.
- Delete what genuinely doesn't apply (e.g. `docs/interfaces.md` for a
  standalone project) — but prefer leaving the inert optional registries in
  place; they cost nothing empty.

## 2. Wire the harness to your stack

Edit `scripts/check.py` (`SRC`/`TESTS` + the "EDIT FOR YOUR STACK" block in
`steps()`):

- **Product steps** (format / lint / tests+coverage) — swap the `ruff`/`pytest`
  commands for your toolchain (`gradle check`, `npm test`, `cargo clippy`, …)
  or drop a step you don't have. Keep each step's gate tags.
- **Process steps** (traceability, design-flows, doc-navigability,
  perf-budgets) — keep as-is. They are stdlib Python and read only the
  registries and docs, so they work identically for a Java, Kotlin, or Rust
  repo. The kit needs a Python 3.8+ interpreter on the machine for these even
  when the product isn't Python; that is the only requirement.

## 3. Non-Python stacks: the two generators (don't fake the guarantee)

Two shipped scripts parse **Python source specifically**:

- **`gen_arch_map.py`** (the code map + dependency diagram + `--check`
  freshness gate). On a repo with no `.py` under `SRC` it generates an empty
  map once, and `--check` then passes **vacuously forever** — the
  "architecture can't drift" guarantee silently lapses while the docs still
  claim it (the script now warns on stderr when it scans nothing). Pick one,
  explicitly:
  1. **Port it** (recommended for a repo you'll live in): any tool that can
     enumerate modules/symbols in your language (ts-morph, `go doc`, a Gradle
     task over the AST) writing into the **same marker block**
     (`<!-- BEGIN/END GENERATED MODULE MAP -->` etc.) — the marker block is
     the whole contract; `--check`-style freshness is a string comparison.
     **PowerShell repos start from the shipped port:** copy
     `scripts/gen_arch_map.reference.ps1` to `scripts/gen_arch_map.ps1`, edit
     its `$ModuleGlob` / `$EntryScripts` / `-Flow` default, and drive it with
     `-Check`. It fills the same three marker blocks from the PowerShell AST, so
     the pre-commit hook and CI treat it exactly like the Python one. (The
     kit's `hooks/pre-commit` carries the `gen_arch_map.py --check` line as an
     **EDIT marker** naming the `pwsh … gen_arch_map.ps1 -Check` swap.)
  2. **Remove the `arch-map` step** from `check.py` and delete the generated
     markers from `architecture.md`, keeping the hand-written overview. Honest,
     just weaker: record the loss in `docs/status.md` constraints.
- **`check_stubs.py`** is Python-only and already optional/product-layer: swap
  it for your language's equivalent or ignore it.
- **`check_flows.py`** (the authored "Runtime flows" section, required from G2)
  reads only the doc and the registries, so it ports as-is — but the diagrams it
  checks are hand-written. Retrofit it the same three ways you handle any
  generated block you can't yet fill (mirror the `gen_arch_map` choice above):
  **author** the section (write the sequence diagrams for the key scenarios and
  cite their SR/LLR ids), **retitle-and-cite** an equivalent section you already
  have, or **drop** the flows step from `check.py` and record that in
  `docs/status.md` constraints. Don't leave the template's `-000` placeholder
  flow citing example ids — `--no-placeholders` (wired from G2) will flag it.

### Which command is "passing" on a non-Python repo

There is **one** definition of passing, and CI must run it too. On a PowerShell
repo that is **`scripts/check.ps1`** (the launcher that runs lint + tests +
`trace.py` + the PowerShell arch-map freshness) — *not* `check.py`, which drives
the Python toolchain. Wire `.github/workflows/` to invoke the same `check.ps1`
so local and CI agree (the FileBackup pilot's canonical gate is `check.ps1`; its
`check.py` is a thin optional shim, not the source of truth). Whatever you pick,
state it in `AGENTS.md`/`CLAUDE.md` so an agent runs the real gate, not a
half-gate.

## 4. Backfill requirements from the boundary, not wholesale

Retro-documenting an entire existing codebase into SN→SR→LLR→TC rows is
make-work that produces paraphrase, not traceability. Instead:

- **Set `docs/gate` to `G1` honestly**, whatever the code's maturity — gates
  describe the *registry's* coverage of the product, and that coverage starts
  near zero. Claim G2/G3 only when their criteria genuinely hold for the scope
  the registries actually cover.
- **Write SNs/SRs for the load-bearing behavior first**: what the project must
  keep doing (the things a regression would page you for), plus the edge-case
  table. These are cheap rows with high protective value.
- **New work gets the full spine from day one**; existing code earns rows when
  you next touch it (the same change that edits the code adds its SR/LLR/TC).
  Coverage grows along the paths that actually change — which is where the
  risk is.
- Existing tests can be adopted as TCs: give each meaningful test a `TC-###`
  row and put the id in the test name — no rewrite needed.

## 5. First green run

```
python scripts/check.py            # gate from docs/gate (G1 to start)
python scripts/trace.py            # writes docs/test/report.md
```

The G1 bar is deliberately small (doc navigability). Bump `docs/gate` in a
reviewed commit as each gate's criteria are genuinely met — CI reads it and
raises the bar with you (process.md §7 "The active gate").

## 6. Re-syncing an existing adoption (picking up kit updates)

A repo that adopted the kit months ago will drift behind it: new scripts, renamed
tiers, split docs. Re-syncing is *not* a fresh bootstrap — you must merge kit
changes into files you've filled in. Do it deliberately.

**Sync only from a committed kit state — never a dirty kit working tree.** Pin
the re-sync to a specific kit commit and let the tooling stamp it: `bootstrap.py`
writes `docs/kit-version` (the kit's short SHA + date) and **warns + marks the
stamp `-dirty`** if the kit tree has uncommitted changes. A dirty stamp is
unreproducible and can't be diffed later, so commit the kit first. (The pilot's
kit HEAD moved twice mid-adoption; the stamp is what makes "which kit is this
repo on?" answerable at all.) With it, a re-sync is a **diff**: compare the SHA
in your `docs/kit-version` against the kit commit you're moving to, and read that
range to see exactly which templates/scripts changed before you touch anything.

### What to overwrite vs preserve

- **Overwrite freely (kit-owned, you don't hand-edit these):** the process
  scripts under `scripts/` (`trace.py`, `check_docs.py`, `check_flows.py`,
  `check_perf.py`, `gen_arch_map.py`, `gen_*`), `docs/process.md` +
  `docs/process-options.md`, the pre-commit hook, `pytest.ini` markers. Take the
  new versions wholesale, then re-apply your local edits — for `check.py` that's
  only the marked **"EDIT FOR YOUR STACK"** block (`SRC`/`TESTS`, the product
  step commands). Diff before committing so a kit change to a step you dropped
  doesn't silently reappear.
- **Preserve always (yours, kit only seeds them):** every registry CSV and
  `stakeholder-needs.md`, `docs/status.md`, `docs/architecture.md`'s hand-written
  overview (regenerate only the marker blocks), `AGENTS.md` project content,
  `docs/gate`, `.gitignore`/`.gitattributes` (merge new kit lines in by hand).
  `bootstrap.py` **skips existing files**, so a plain re-run won't clobber these —
  but don't run it with `--force` against a live repo without a diff pass.
- **Re-stamp `docs/kit-version`** and commit it as the last step, so the record
  reflects the state you actually landed on.

### Migration recipes for specific kit changes

- **`process.md` → `process.md` + `process-options.md` split.** Newer kits moved
  the opt-in layers (phased delivery, lifecycle tags, §8/§9 boundary notes, the
  multi-repo rung) out of `process.md` into a companion `process-options.md`,
  keeping `§`-numbering stable. To migrate: drop in **both** new files; anything
  your repo added *inside* the old monolith (rare — it's kit-owned) moves to
  whichever file now owns that section. Fix references: a link to
  `process.md#section-9` may now point into `process-options.md`. Run
  `check_docs.py` — it fails on exactly these broken intra-repo links.
- **UN → SN id-tier rename (User Need → Stakeholder Need).** The top tier was
  renamed. **Keep the id *numbers* — only the prefix changes** (`UN-014` →
  `SN-014`); renumbering would break every back-link. Recipe: rename the file
  reference and the prefix in `stakeholder-needs.md` and every `SN-Refs`/`UN-Refs`
  cell across the SR registry, then rerun `trace.py --strict` (it validates the
  SN↔SR join and will flag any missed `UN-###`). **Do *not* rewrite audit-log /
  status.md evidence quotes** that say "UN-014" — those are a historical record
  of what was decided at the time; rewriting history to match a later rename is
  dishonest. Leave them, optionally with a one-line "(UN-### = today's SN-###
  after the Session-K rename)" note where confusion is likely.
  - *Tooling latitude:* `trace.py` intentionally does **not** accept legacy
    `UN-Refs` — a lingering `UN-` after you claim the rename is done is a real
    orphan you want surfaced, not silently bridged, and the migration is a
    one-time find-replace, not an ongoing compatibility burden. If your repo is
    mid-rename and wants a transitional deprecation warning, that's a *local*
    patch to your copy of `trace.py`, not something the kit ships. (Docs-only
    call, deliberate: a permanent alias would let the old prefix live forever.)
  - *Downstream test import:* overwriting `scripts/gen_release_checklist.py`
    from the kit renames its public function `read_user_needs` →
    `read_stakeholder_needs`. Any downstream test or script that imports
    `gen_release_checklist.read_user_needs` by the old name will break (the
    PictureSorter re-sync was bitten by this). Update callers as part of the
    UN→SN recipe — grep for `read_user_needs` in your tests and scripts.
- **Legacy TC CSVs missing the `Tier` column.** Older adoptions created
  `docs/test/test-cases.csv` before the `Tier` column was added to the
  template. `trace.py --strict-schema` requires `Tier` as a non-empty field
  (it validates the full TC schema at G3). Migration is mechanical: add a
  `Tier` column and set a default of `Full`; mark hardware/network/interactive
  cases `Release` so they don't run on unattended CI. Once the column is
  present, `trace.py --strict-schema` will also validate that values are in
  `{Smoke, Full, Release}`, so tighten any free-text entries at the same time.
- **`Attest` verification kind + binary-asset registry (creative / subjective
  scopes).** Newer kits add the **`Attest`** `Verification` method (a named
  human's recorded judgment — playtest, creative review, physical action — for
  what can't be mechanized) and an optional **`assets.csv`** registry
  (`ASSET-###`) for unavoidably-binary deliverables. To adopt: overwrite
  `scripts/trace.py` (it now accepts `Attest` in the vocabulary and reports the
  "attested vs mechanized" split) and drop in `registries/assets.template.csv →
  docs/requirements/assets.csv`. Retag any SR you were faking as `Test`/`Manual`
  but that really rests on human judgment to `Verification=Attest`, and record
  **who/when** in its TC cell. For binary deliverables (art, music, voice, video):
  manage them as **git-LFS or out-of-repo pointers** and record provenance
  (human/AI — for Steam-style AI-content disclosure), license, attribution, and
  the contract/release link as `ASSET-###` rows — track *about* the asset in text
  even though the asset itself can't be diffed. Both are opt-in; a scope with no
  subjective/binary work ignores them (process-options.md "Proportionality
  doctrine" + "Binary assets").
- **Skills layer (newer kits ship `skills/`).** To bring an agent's skills into an
  already-adopted repo, re-run `bootstrap.py --agents claude|gemini|both` against
  it: it materializes the matched `kit`-scope skills into the agent dir
  (`.claude/skills/…` / `.gemini/skills/…`) and copies the inert hook example,
  **skipping any skill file that already exists** (your edits are safe; use
  `--force` only after a diff pass). The `skills/SKILL.md` sources are kit-owned —
  overwrite freely on re-sync; a skill you customized locally, treat like
  `check.py` (take the new version, re-apply your delta). Skills are opt-in
  accelerators, never a gate (process-options.md "Skills layer").

### Repos whose `AGENTS.md` already means something else

The kit's model is **`AGENTS.md` = the agent guide** (with thin `CLAUDE.md`/
`GEMINI.md` stubs pointing at it). Some repos already use `AGENTS.md` as their
**project encyclopedia** — the single source for architecture, invariants, and
history — with `CLAUDE.md` as the thin agent guide. That's the **inverse** of the
kit layout (the FileBackup pilot is exactly this case), and it's fine: the kit
cares that *one* file is the durable source of truth and the others point at it,
not which filename plays which role. When re-syncing such a repo:

- **Don't let bootstrap overwrite your `AGENTS.md`** with the kit's guide
  template — it's skipped as an existing file, but never `--force` it here.
- Put the kit's **agent-guide content** (the working agreement, the "how we work"
  rules, the generated code-map routing) wherever your agent guide actually lives
  — for the inverse layout that's `CLAUDE.md`. Route `gen_arch_map`'s `--doc`
  there (and/or into `architecture.md`), not blindly into `AGENTS.md`.
- Keep the pointer discipline: whichever file is the encyclopedia, the others say
  "defer to it, don't duplicate." State the mapping once at the top of each file
  so an agent isn't guessing which `AGENTS.md` convention this repo follows.

## 7. Standards crosswalk (for people and tools from standards-world)

Most of the kit's vocabulary is a **right-sized application of established
systems-engineering ideas**, not a new invention. This table maps kit terms to
their standard equivalents so an adopter (or an LLM) fluent in those standards can
onboard instantly and settle definition disputes by citation. It is for
**communication and citation only** — the kit deliberately borrows the *ideas*,
not any standard's full mandated process (that ceremony is exactly the weight the
Proportionality doctrine warns against; see `process-options.md`). Where the kit
honestly deviates, the row says so.

| Kit concept | Standard equivalent | Notes / honest deviation |
| --- | --- | --- |
| `SN`→`SR`→`LLR`→`TC` spine | ISO/IEC/IEEE 29148 StRS → SyRS/SRS requirement levels; DO-178C HLR/LLR + trace-to-test | `SN`≈StRS (stakeholder), `SR`≈SyRS/SRS (system/software), `LLR`≈DO-178C low-level requirement/design. The kit collapses the ceremony into four CSV tiers. |
| `trace.py` output (`report.md` / graph) | Requirements Traceability Matrix (RTM) | Same job — every requirement linked to its verification — generated from the registries, never hand-maintained. |
| Gates `G1`–`G3` | Technical review gates SRR / PDR / CDR / TRR (IEEE 15288.2) | Rough altitude match, not a 1:1 mapping: `G1`≈requirements agreed (SRR), `G2`≈design/impl reviewed (PDR/CDR), `G3`≈verified (TRR). The kit's gates are lightweight self-reviews, not staffed milestone reviews. |
| `G-Release` | Functional / Physical Configuration Audit (FCA / PCA, IEEE 15288.2) | Confirms the built product matches its requirements and its declared configuration before release. |
| `IF-###` interface catalog | Interface Control Document (ICD) | One row per interface of record; the kit's is a CSV catalog, not a standalone controlled document. |
| `PB-###` performance budgets (§9) | Technical Performance Measures (TPMs) / resource budgets | Same intent — track measurable performance/resource targets against thresholds. |
| `ASSET-###` + manifest/hash | Configuration items + baselines (IEEE 828 / ISO 10007) | A configuration item with a recorded, hashable baseline; the kit tracks provenance/license/hash in text where the asset itself can't be diffed. |
| `status.md` risks & assumptions | Risk register (ISO 31000 family) | Same purpose — a living record of identified risks and assumptions; the kit keeps it lightweight and inline, not a separate managed register. |
| `Verification` column | TDIA methods — Test, Demonstration, Inspection, Analysis (MIL-STD-961E / ISO/IEC/IEEE 29148 / INCOSE SE Handbook) | Direct adoption. Plus the kit's `Manual` and `Attest`; `Attest`'s nearest analog is a witnessed test / QA sign-off, with the attested-vs-mechanized reporting deliberately beyond the standards (process.md §4). |
| Overall needs → requirements → outputs → verification shape | FDA design controls (21 CFR 820.30) / ISO 13485 Design History File (DHF) | A structural cousin, not a claim of compliance: the same design-input → design-output → verification loop, right-sized for software. |
