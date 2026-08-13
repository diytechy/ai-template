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
On a non-Python repo, declare it: `--stack node|go|rust|powershell` skips the
dead `pytest.ini` and appends the §2 rewiring checklist to `docs/status.md` as
Open-items bullets, so the remaining hand-edits are visible work items.
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
- **`docs/kit-profile`** — always (re)written beside it: the structural choices
  (`stack=`, `omit=`) the process docs were *generated* with. `docs/process.md`
  and `docs/process-options.md` are not raw copies of the kit masters —
  bootstrap strips the masters' `kit-only` regions and keeps or stubs
  `profile:` regions per this record (an omitted section keeps its § heading
  plus a one-line stub; § labels never renumber). Commit it: a re-sync
  regenerates from it (see "Re-syncing" below).
- **`docs/kit-license`** — always (re)written beside those two: the kit's own
  **Apache-2.0** text, so your repo redistributes the copied kit files legally
  without anyone fetching it (§4(a)). Commit it. It covers **the kit files
  only** — your code, and every artifact this scaffold produces (your filled
  registries, requirements, architecture, log), are yours under whatever license
  you choose. Put that one in your repo's own `LICENSE`; the two don't compete.
  If you modify a kit file, §4(b) asks you to say so in that file — the delta
  from `docs/kit-version` is what makes that visible.
- **`.github/workflows/check.yml`** — if you have CI already, add the
  `check.py` invocation to it instead of adopting the reference workflow
  wholesale. Keep one definition of "passing": CI runs the same command you run
  locally.
- **`pytest.ini`** — Python repos with an existing pytest config: merge the
  tier markers (`smoke`/`full`/`release`) rather than replacing the file.
- **`src/`, `tests/`** — bootstrap only adds `.gitkeep`s; your layout stays.
  Point the harness at the real roots (`[paths]` `src`/`tests` in
  `docs/stack.ini`).
- **`README.md`** — skipped if present (the common case). Retrofit the
  *evaluator's rungs* into your existing README instead: a "Run it" section
  pointing at the root `run.{cmd,sh,command}` launchers (declare your
  capabilities in `docs/stack.ini`'s `[run]` section — one `<name> = <command>`
  line each — and the launchers present them; see §6)
  and a getting-started pointer at the `scripts/onboard.* → dev-setup → setup
  → check` ladder. A pure library deletes the launchers and describes usage.
- **Pre-commit hook** — `setup.{sh,ps1}` set `git config core.hooksPath
  .githooks`, which **overrides** any existing `.git/hooks` or hook manager
  (husky, pre-commit-framework). If you already have hooks, either call
  `.githooks/pre-commit` from your existing hook chain or skip the wiring —
  CI remains the enforcement of record.
- **`scripts/dev-setup.*` roles** — the workstation script declares one
  **role** per contributor kind over a shared baseline; the default provisions
  every role, `--profile <role>` narrows to one. Fill the `ROLES` list (sh) /
  `$Roles` table (ps1) and each role's detect/install slots for your stack.
  *Upgrading from an earlier kit* (`--profile code|domain`, a single
  `DOMAIN_VIEWER_*` slot): move that slot's commands into a role entry (e.g.
  `design`); the default now installs all roles rather than just `code`.
- Delete what genuinely doesn't apply (e.g. `docs/interfaces.md` for a
  standalone project) — but prefer leaving the inert optional registries in
  place; they cost nothing empty.

## 2. Wire the harness to your stack

Edit **`docs/stack.ini`** — the single declared home for the product toolchain.
`check.py` reads it; CI, the pre-commit hook, and `setup.*` delegate to it, so a
stack swap is one file, not six copies. (Delete it to fall back to `check.py`'s
built-in Python-reference defaults — identical values.)

- **`[product]`** (format / lint / test) — swap the `ruff`/`pytest` commands for
  your toolchain (`gradle check`, `npm test`, `cargo clippy`, …). `{py}` is the
  interpreter running `check.py`; `{src}`/`{tests}` are `[paths]`. A command
  that runs `{py} -m <mod>` auto-fails on a missing module; any other
  executable's absence on PATH is the same designed failure. Drop a step you
  don't have by leaving its command blank.
- **`[tiers]`** — map smoke/full/release/all onto your runner's selectors (the
  A3 gap: non-pytest stacks declare their tiers here, e.g. a path or
  `--project`, instead of inventing an out-of-band scheme). **`[coverage]`** —
  the threshold and the extra args appended at the covered tiers.
- **`[paths]`** — point `src`/`tests` at your real roots.
- **`[step:<name>]`** — add a gate your **domain** needs (duplicate-code,
  license-lint, capability/dataflow integrity, …) as its own section:
  `command =` (required), `gates =` (space/comma `DevBar-Reqs|DevBar-Tests|DevBar-Release`, default DevBar-Release),
  `layer =` (`process|product`, default product). `check.py` runs it alongside
  the built-in plan, so CI and the local harness pick it up with no code change
  — and, crucially, your custom gates live **here**, not hand-edited into
  `check.py`, so the script stays take-wholesale on a re-sync (§6). The name may
  not shadow a built-in step.

(`scripts/check.py`'s "EDIT FOR YOUR STACK" constants are the same values, used
only as the fallback when no `docs/stack.ini` exists — prefer the profile.)
- **Process steps** (traceability, design-flows, doc-navigability,
  perf-budgets) — keep as-is. They are stdlib Python and read only the
  registries and docs, so they work identically for a Java, Kotlin, or Rust
  repo. The kit needs a Python 3.11+ interpreter on the machine for these even
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
  2. **Run the stack-neutral fallback** (`gen_arch_map.py --mode files`): the
     same script fills the same marker block with **one row per source file**
     (path + first comment line) instead of symbol-level rows. No new runtime,
     works for any language, and `--check` still trips on a file
     added/removed/renamed or a summary edit — a real freshness gate, just
     coarser. Wire it by declaring `[arch-map] mode = files` in
     `docs/stack.ini` (plus `comment-prefixes = <tokens>` if your comment
     token isn't `#`/`//`/`--`) — the take-wholesale `check.py` reads it, no
     hand-edit needed; a fresh `bootstrap.py --stack node|go|rust|powershell`
     seeds it for you. Prefer this over a vacuous pass whenever you haven't
     ported a symbol-level generator yet.
  3. **Remove the `arch-map` step** from `check.py` and delete the generated
     markers from `architecture.md`, keeping the hand-written overview. Honest,
     just weaker: record the loss in `docs/status.md` constraints.
- **`check_stubs.py`** is Python-only and already optional/product-layer: swap
  it for your language's equivalent or ignore it.
- **`check_flows.py`** (the authored "Runtime flows" section, required from DevBar-Tests)
  reads only the doc and the registries, so it ports as-is — but the diagrams it
  checks are hand-written. Retrofit it the same three ways you handle any
  generated block you can't yet fill (mirror the `gen_arch_map` choice above):
  **author** the section (write the sequence diagrams for the key scenarios and
  cite their SR/LLR ids), **retitle-and-cite** an equivalent section you already
  have, or **drop** the flows step from `check.py` and record that in
  `docs/status.md` constraints. Don't leave the template's `-000` placeholder
  flow citing example ids — `--no-placeholders` (wired from DevBar-Tests) will flag it.

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

- **Set `docs/gate` to `DevBar-Reqs` honestly**, whatever the code's maturity — gates
  describe the *registry's* coverage of the product, and that coverage starts
  near zero. Claim DevBar-Tests/DevBar-Release only when their criteria genuinely hold for the scope
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
python scripts/derive_gate.py      # compute docs/gate from the artifact states
python scripts/check.py            # gate from docs/gate (DevBar-Reqs to start)
python scripts/trace.py            # writes docs/test/report.md
```

The DevBar-Reqs bar is deliberately small (doc navigability). **The gate is derived, not
bumped** (process.md §7; process-options.md "Derived gate model"): `docs/gate` is
generated by `scripts/derive_gate.py` from the artifact states, and it rises as you
**ratify artifacts in a reviewed commit** (`Status` `Draft`→`Planned`, or an SN out
of its draft section) and regenerate — CI reads the cached value and raises the bar
with you. A fresh scaffold ships a legacy one-line `docs/gate`; the first
`derive_gate.py` run above migrates it to the generated form (until then the
`derived-gate --check` step accepts it value-only, so you upgrade without a red
day).

**Weigh the opt-in layers now** — they cost nothing until enabled, and adoption
is the cheapest moment to decide: the unattended coordinator, the reviewer dial,
and the **vendored guardrails / efficiency packages** (process-options.md
"Tier-conditional guardrails" names worked examples — a behavior package and a
token-efficiency package). Re-check the same list at every re-sync (§6).

## 6. Re-syncing an existing adoption (picking up kit updates)

A repo that adopted the kit months ago will drift behind it: new scripts, renamed
tiers, split docs, retired files. Re-syncing is *not* a fresh bootstrap — you
merge kit changes into files you have filled in, and that merge call is
deliberately a person's (or an LLM's): `SR-036` carries
`verification = "Inspection"` precisely because *did the adopter edit this, and
does their edit still mean something under the new kit?* is not a fact a tool
holds.

**The procedure and every rule live in [`RESYNC_PACK.md`](RESYNC_PACK.md)** — the
kit's LLM re-sync pack. It is ONE HOME on purpose: these recipes used to sit here
*and* in the `downstream-resync` skill, and the two drifted apart within weeks at
zero re-sync traffic (OI-27). This section frames the job and points; the pack
does it. Read the pack from the kit checkout you are syncing **to** — the same
one you are diffing against.

| What you need | Where |
| --- | --- |
| the procedure: what to read, in what order, and the judgement SR-036 leaves to you | pack §1 |
| the file-by-file deviation review over the `MAPPING` inventory — overwrite / regenerate / re-apply-dials / preserve, and the sets that only move together | pack §2 |
| the per-change migration entries, each anchored `[since <kit sha>]` so your stamp-to-target range selects the ones that apply | pack §3 |
| the translation helper for concept renames (`drive.py` → `dispatch.py`, `UN-###` → `SN-###`, `retired` → `cancelled`, the `G*` tags → the stage ladder, …) | pack §4 |
| when the pack stops being prose: the named promotion trigger and what it promotes to | pack §5 |

**One standing rule in that table is overridden by exactly one migration.** The
deviation review classes `docs/gate` as *preserve* — it is a committed file whose
value is the repo's own. The **`G*` → stage-ladder** conversion (pack §3) inverts
that for `docs/gate` alone: the cache is field-compatible but not
value-compatible, so it must be **regenerated**, once, with
`python scripts/derive_gate.py`. Take the pack entry's word over the class here;
it is the more specific rule and it says so in place.

The anchor the whole procedure turns on is `docs/kit-version` — the kit short-SHA
+ date `bootstrap.py` stamps at scaffold time (§1), which is what makes a re-sync
a **diff** instead of a guess. Pack §1.1 says what to do with it, including the
tarball case where it reads `unknown (kit not a git checkout)` and there is no
range to diff.

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
| Gates `DevBar-Reqs`–`DevBar-Release` | Technical review gates SRR / PDR / CDR / TRR (IEEE 15288.2) | Rough altitude match, not a 1:1 mapping: `DevBar-Reqs`≈requirements agreed (SRR), `DevBar-Tests`≈design/impl reviewed (PDR/CDR), `DevBar-Release`≈verified (TRR). The kit's gates are lightweight self-reviews, not staffed milestone reviews. |
| `DevStg-Release` | Functional / Physical Configuration Audit (FCA / PCA, IEEE 15288.2) | Confirms the built product matches its requirements and its declared configuration before release. |
| `IF-###` interface catalog | Interface Control Document (ICD) | One row per interface of record; the kit's is a CSV catalog, not a standalone controlled document. |
| `PB-###` performance budgets (§9) | Technical Performance Measures (TPMs) / resource budgets | Same intent — track measurable performance/resource targets against thresholds. |
| `ASSET-###` + manifest/hash | Configuration items + baselines (IEEE 828 / ISO 10007) | A configuration item with a recorded, hashable baseline; the kit tracks provenance/license/hash in text where the asset itself can't be diffed. |
| `status.md` risks & assumptions | Risk register (ISO 31000 family) | Same purpose — a living record of identified risks and assumptions; the kit keeps it lightweight and inline, not a separate managed register. |
| `Verification` column | TDIA methods — Test, Demonstration, Inspection, Analysis (MIL-STD-961E / ISO/IEC/IEEE 29148 / INCOSE SE Handbook) | Direct adoption. Plus the kit's `Manual` and `Attest`; `Attest`'s nearest analog is a witnessed test / QA sign-off, with the attested-vs-mechanized reporting deliberately beyond the standards (process.md §4). |
| Overall needs → requirements → outputs → verification shape | FDA design controls (21 CFR 820.30) / ISO 13485 Design History File (DHF) | A structural cousin, not a claim of compliance: the same design-input → design-output → verification loop, right-sized for software. |
