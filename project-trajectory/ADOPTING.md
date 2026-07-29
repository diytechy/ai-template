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
  `command =` (required), `gates =` (space/comma `G1|G2|G3`, default G3),
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
python scripts/derive_gate.py      # compute docs/gate from the artifact states
python scripts/check.py            # gate from docs/gate (G1 to start)
python scripts/trace.py            # writes docs/test/report.md
```

The G1 bar is deliberately small (doc navigability). **The gate is derived, not
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

**Re-weigh the opt-in layers while you're here.** A re-sync is the natural moment
to reconsider vendoring or extending a guardrails / efficiency package
(process-options.md "Tier-conditional guardrails") as the kit and the agent
ecosystem move — the same decision adoption raised (§5). And recheck what's
**new** in the range you're syncing across, not just what changed in files you
already have: diff `skills/INDEX.csv` for new or updated **skills** (materialize
for your agent with `bootstrap.py --dest . --agents <agent>`; refresh existing
per-agent copies with `--sync`), scan process-options.md's layer list for
**opt-in layers added** since your pinned commit, and revisit the **vendorable
packs** those layers name (guardrails cores, efficiency packages, knowledge
bundles). An upgrade that only takes script fixes leaves accelerators on the
table.

### What to overwrite vs preserve

- **Overwrite freely (kit-owned, you don't hand-edit these):** the process
  scripts under `scripts/` (`trace.py`, `derive_gate.py`, `check_docs.py`,
  `check_flows.py`, `check_perf.py`, `check_privacy.py`, `gen_arch_map.py`,
  `gen_*`, `agent_loop.py`), the git hooks (`.githooks/pre-commit`,
  `.githooks/pre-push`), `pytest.ini` markers, **`scripts/check.py`**. These are
  now safe to take wholesale: your whole toolchain lives in `docs/stack.ini`
  (below) — the format/lint/test commands **and any project-specific gates, as
  `[step:<name>]` sections** — not in `check.py`, so a re-sync no longer needs
  you to re-apply an EDIT block or re-add a custom step. (If you still have a
  hand-added step inside a pre-`[step:]` `check.py`, move it into a
  `[step:<name>]` section once, and it survives every re-sync after.) Diff
  before committing anyway, so a kit change you disagree with doesn't land
  unread. **Cross-agent skill sync (2026-07, S7):** the hook gains a
  `check.py --run-step skills-sync` step, so **re-sync `check.py` together with
  the hook** (an older `check.py` with no `skills-sync` step fails every commit
  with `check: no step named 'skills-sync'` — the same kit-owned-set-together
  caveat as `okf`/`trajectory-map`). The step is vacuous unless the repo hosts
  the neutral `skills/` source and per-agent skill dirs; if you keep per-agent
  copies (`.claude`/`.gemini`/`.agents` `skills/`), refresh them from source with
  `bootstrap.py --dest . --sync` and commit — a drifted copy is a gate finding.
  **Derived gate (2026-07, WI-089…096):** the re-sync ships `derive_gate.py` and a
  `check.py --run-step derived-gate` step (so re-sync `check.py` + the hook
  together, the same set-together caveat). `docs/gate` is now **generated** from
  the artifact states — run `python scripts/derive_gate.py` **once** to migrate
  your legacy hand-set `docs/gate` to the derived form (until you do, the
  `derived-gate --check` step accepts the old one-line value **value-only**, so an
  un-migrated repo is never broken). After migrating, you stop bumping the line —
  you ratify artifacts (`Status` `Draft`→`Planned`, or an SN section move) in a
  reviewed commit and regenerate (process-options.md "Derived gate model").
  **Reconcile states against your ratification history before trusting the
  migrated value.** The derived gate believes your recorded `Status` values and
  SN sections — but a legacy repo's registries usually contain artifacts added
  *after* the commit that last set `docs/gate`, states no reviewer ever
  ratified. Find that commit (`git log --oneline -- docs/gate`), diff the
  requirement surfaces since (`git diff <sha>..HEAD -- docs/requirements
  docs/test`), and stage everything added or materially changed since per the
  new model — new stakeholder needs into a `## Draft needs (unratified)`
  section, not-yet-re-reviewed SRs to `Status=Draft` — so `derive_gate.py`
  reproduces the gate your history actually attests instead of laundering
  post-attestation additions into it. If the derived value still disagrees with
  your old hand-set line after that, the *disagreement is the finding*: ratify
  (or demote) deliberately before relying on the derived gate.
  **Phase model + the retired grouping column (2026-07, WI-188):** the delivery
  `Phase` is now a column on `low-level-requirements.csv` and `test-cases.csv` too
  (it was SR-only), and `work-items.csv` **drops** its old per-WI grouping column
  (the one the dashboard used to bin the roadmap by — it now tiers `phase ⊃
  workstream ⊃ work-item`). Both changes are **vacuous-until-armed**, so a re-sync
  is diffable and never breaks: a registry with no phased row keeps `trace.py`'s
  ratified-Phase schema rule dormant (blank = in scope for every phase), and any
  leftover grouping column is simply ignored (read by name, no vocabulary rule).
  Recommended convention is **bare integers** (`1`, `2`, …), but a `vN` label still
  digit-parses everywhere (`--phase`, the derived current phase, the schema rule),
  so a downstream that kept `vN` arms the rule and passes it. Once you phase any
  row, phase every *ratified* SR/LLR/TC — a ratified blank/unparseable `Phase` is
  then a `--strict-schema` finding — and the foundation (minimum) phase stays in
  scope under `--phase`.
- **Regenerate, never raw-copy (kit-owned but generated):** `docs/process.md` +
  `docs/process-options.md` are *generated* from the kit masters per the
  recorded `docs/kit-profile` (§1). Raw-copying `PROCESS.md`/
  `PROCESS_OPTIONS.md` over them would ship the masters' `kit-only`/`profile`
  marker comments, the copy-me meta-prose, and any sections this repo opted
  out of. To take the new versions: **delete the two files, then re-run
  `bootstrap.py --dest .`** — it re-reads `docs/kit-profile` (explicit
  `--stack`/`--omit` flags override it), regenerates them with the same
  structural choices, and re-stamps `kit-version` + `kit-profile`.
- **Preserve always (yours, kit only seeds them):** `docs/stack.ini` (your
  declared toolchain — the kit seeds the Python reference once and never
  re-touches it; its `[generated]` section — the integrator's auto-resolution
  allowlist, WI-235 — is likewise project-owned: keep your own artifact rows on
  re-sync), every registry CSV, the `docs/work/` WI spec folder, and
  `stakeholder-needs.md`, `docs/status.md`, `docs/log.md`, `docs/plan.md`
  (**migrating a pre-flip repo:** a `docs/requirements/work-items.csv` keeps
  working via dual-read; when ready, run `scripts/wi_convert.py --verify` then
  `--to-specs` and delete the CSV — the folder wins the moment it holds a real
  spec, and both-present is an integrity error by design),
  (your work plan — the kit seeds the block-list skeleton once),
  `docs/iteration/` + `docs/iteration_index.md` (session history),
  `docs/architecture.md`'s hand-written overview (regenerate only the marker
  blocks), `AGENTS.md` project content, the root launchers' EDIT slots,
  `docs/gate`, `.gitignore`/`.gitattributes` (merge new kit lines in by hand).
  `bootstrap.py` **skips existing files**, so a plain re-run won't clobber these —
  but don't run it with `--force` against a live repo without a diff pass.
- **Re-stamp `docs/kit-version`** and commit it as the last step, so the record
  reflects the state you actually landed on.

### Migration recipes for specific kit changes

- **`trace.py` splits into two files (2026-07).** `scripts/trace_text.py` joins
  `scripts/trace.py`, and **a re-sync must copy both** — `trace.py` imports its
  spine-row text layer from the sibling, so a repo that picks up one and not the
  other gets an `ImportError` on its first check rather than a quiet
  degradation. `bootstrap.py` copies them together; a hand-managed re-sync must
  too. No behaviour changes: the split is pure decomposition, and the kit's three
  golden report files stay byte-identical across it. *Why:* the four text
  predicates (`provenance_findings`, `form_findings`, `paraphrase_advisories`,
  `ac_advisories`) and the row primitives they share are one concern — *is this
  row readable and decidable on its own?* — and pure (rows in, findings out), so
  they separate cleanly from the join that owns I/O and reporting.
- **The LLR `Rationale` column (2026-07).** `low-level-requirements.csv` gains an
  optional **`Rationale`** column after `Detail`. Non-breaking and header-driven:
  a registry without it reads as blank and stays valid, so migration is adding
  one header cell whenever convenient. *Why it exists:* `Detail` was the LLR's
  only prose cell, so the *what*, the *why*, the ruled-out alternatives and the
  authoring history were structurally forced into one field — and a cell asked to
  hold four things holds none of them legibly. `Rationale` is a requirement
  attribute at **every** level (ISO/IEC/IEEE 29148); the SR had one and the LLR
  did not, and that asymmetry was the bug. It stays **optional** on purpose: a
  short mechanical decomposition row's why *is* its parent SR's, and requiring one
  everywhere would manufacture exactly the restatement §3 forbids. Fill it where
  the decomposition was itself a decision. It is normative text, so the
  stand-alone rule applies — no work-item ids, no process-doc citations
  (`trace.py` gates it under `--strict`).
- **The component/workstream schema bundle (2026-07).** Four coupled, **never
  breaking** registry changes land together: **(a)** the work-items `Track`
  column is renamed **`Workstream`** (a mutable grouping category — "track" now
  means only the parallel-execution lane); the legacy header is still read, so
  migration is renaming one header cell whenever convenient. **(b)**
  `Predecessors` gains an edge kind: a bare id is a **hard** (blocking) edge, a
  `~`-prefixed id (`~WI-013`) a **soft** advisory-ordering edge — audit your DAG
  and demote narrative "reads-well-after" edges to `~`. **(c)** A new optional
  **`components.csv`** (`CMP-###`, process-options.md "Component layer") is
  scaffolded, and the LLR/IF/ASSET/PART templates gain an optional `Component`
  tag column; existing files without the column stay valid (header-driven) —
  adopt by adding the column where you name components. **(d)** The multi-repo
  registry is renamed **`repos.csv` / `REPO-###`** (formerly
  `modules.csv`/`MOD-###`); the legacy file + ids are still read, and both may
  coexist mid-migration.
- **`docs/trajectory.html` → root `PROJECT_STATE.html` (2026-07, WI-039).**
  The trajectory dashboard evolved into the unified project-state artifact at
  the repo **root** (adds the How-SW module-map view, the optional CMP table,
  and a git-derived as-of stamp that `--check` ignores). Migration: after the
  re-sync, delete your committed `docs/trajectory.html`, run
  `python scripts/gen_trajectory.py`, and commit the new root file — the
  `trajectory-map` gate/hook step name is unchanged and now checks the new
  path automatically.
- **The OKF knowledge bundle (2026-07, Thread 48).** Newer kits export the
  spine registries as a generated `docs/okf/` bundle, **on by default** with a
  pre-commit + G3 freshness gate. After a re-sync, either run
  `python scripts/gen_okf.py` once and commit the bundle (it stays fresh via
  the hook from then on), or opt out with the one word `off` in
  `docs/okf-export` — a repo with placeholder-only registries needs neither
  (vacuous). **Re-sync `check.py` together with the hook:** the hook's
  step 1b runs `check.py --run-step okf`, so an older `check.py` with no `okf`
  step fails every commit with `check: no step named 'okf'` — the same
  re-sync-the-kit-owned-set-together caveat the `trajectory-map` step carries.
  The okf step runs **before** the dashboard step on purpose: the dashboard now
  consumes the bundle (its Knowledge tab), so the regen order is
  arch-map → okf → trajectory.
- **The TC `Evidence` column (2026-07, Thread 51).** `test-cases.csv` gains an
  **`Evidence`** column (between `Automated` and `Status`) naming the concrete
  test — a pytest node, a script path, or a procedure-doc link
  (inspection-only text, never mechanically resolved). Optional in general,
  but from G3 `--strict-schema` **requires it non-empty on `Automated=Yes`
  rows** — a claimed-automated test with no cited location is a soft
  false-green; a legacy CSV without the column reads as empty and is flagged
  the same way, so migration is: add the header cell, then move any test
  pointers you had squeezed into `Parameters` (the old `node=…` workaround)
  into `Evidence`, restoring `Parameters` to dimensional inputs only. Below
  G3 a legacy file keeps passing untouched.
- **Architecture-connectivity coverage (2026-07, WI-056).** `trace.py` now reads
  the `IF-###` interface tier (id/SR-Refs integrity, closing the SR-002-era gap),
  `interfaces.template.csv` gains a `Notes` column (legacy rows read it empty),
  and `check_trajectory.py` runs a warn-first **connectivity coverage** over the
  arch-map inventory. It is **opt-out, default-on** (the `docs/trajectory-check`
  posture — no file is scaffolded; absence reads on), so after a re-sync a
  **multi-module** repo with no declared seams starts warning "connectivity
  undeclared" at the hook and G3. That never fails a gate — the warns only nudge.
  To act on them, declare `IF-###` rows (process.md §8; use a `source`/`sink`
  first-word `Notes` marker for a deliberate pure source/sink) and regenerate the
  arch-map + `PROJECT_STATE.html`; to silence the whole layer, put the one word
  `off` in `docs/interfaces-check`. A single-module repo is vacuous and needs
  nothing.
- **Conditional scaffold generation (`docs/kit-profile`).** Newer kits
  *generate* `docs/process.md` + `docs/process-options.md` from marker-carrying
  masters per a recorded profile (`docs/kit-profile`: `stack=` +
  `omit=nfr,multi-module` axes; omitted sections keep their § heading plus a
  one-line stub, so labels never renumber and links never dangle). An older
  adoption has no profile record; its first re-sync is a **one-time
  regeneration**: delete the two process docs, re-run
  `bootstrap.py --dest . [--stack …] [--omit …]`, and commit the two
  regenerated docs plus the new `docs/kit-profile`. With no `--omit` the
  regenerated docs match the old full copies (minus the copy-me meta-prose the
  markers now strip); declaring omissions is opt-in and can happen at any
  later re-sync.
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
- **`Area` column on the SR registry (owner-hat coverage).** Newer kit
  templates end the SR header with an optional `Area` column (owner-hat/domain
  tag, process.md §1); `trace.py` reports per-Area SR counts when it carries
  values. Adding it to an existing CSV is **optional, not a migration** — the
  column is outside the required schema, so a legacy registry without it stays
  green even under `--strict-schema`.
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
- **status/log split (`docs/status.md` → `status.md` + `docs/log.md`).** Newer
  kits split the blackboard: `status.md` is the **working surface** — only what
  the agent or human must perform next — and `docs/log.md` is the
  **append-only history** it points at (the Gate Sign-offs table, verdict
  blocks, ratified decisions, session notes; process.md §5). Migration is
  **optional and proportionate — never forced**: an adopted repo may keep its
  merged file. To adopt: copy `LOG.template.md` → `docs/log.md`, cut the
  accreted history sections over **with their headings preserved verbatim**
  (downstream greps and the §5 wording rely on them), and leave the
  `History: docs/log.md` pointer in status.md's header. Don't rewrite the moved
  entries — they are the historical record.
- **Privacy-check toggle (`docs/privacy-check`) — replaces the old
  `docs/commit-identity` glob.** Newer kits split *identity* from *privacy*
  (process-options.md "Commit identity & privacy"): which account authors is
  the user's own git config (no longer pinned by a repo file), and a one-value
  toggle `docs/privacy-check` (`true`/`false`) runs the privacy gate — the
  commit author email and committed content/messages are scanned for PII, with
  the exempt-email allowlist (`EXEMPT_EMAILS`, default `*noreply*`) in
  `check_privacy.py`. To adopt: overwrite the hooks (`pre-commit`, the new
  `commit-msg`, `pre-push`) + `check_privacy.py` + `setup.*` from the kit, and
  replace `docs/commit-identity` with `privacy-check.template` → `docs/privacy-check`
  (set `true` if you had a non-`inherit` glob, else `false`). Migrating from an
  older kit: delete `docs/commit-identity`; the pre-commit author check is now a
  Python `--author` step, so a Python-less machine no longer enforces identity
  (deliberate — that pin moved to git config). The guard covers **future commits
  in clones that ran setup** only — history already committed with a private
  identity needs a git history rewrite, out of the kit's scope; decide that
  deliberately before publishing.
- **Secrets floor (`check_privacy.py`, every repo) — a behavior change to
  expect.** Newer kits run the deterministic secrets floor (private-key headers
  + GitHub/Slack/AWS/`sk-…` shapes) in **all** repos, not just privacy-checked
  ones (process-options.md "Secrets floor (every repo)"). Overwriting the hooks +
  `check_privacy.py` on re-sync therefore starts scanning a privacy-off repo that
  previously had none: the pre-commit hook blocks a staged commit carrying a
  credential shape, `check.py` flags a tracked one at every gate, and the
  pre-push hook scans the outgoing range. **That is the point** — but if the
  repo legitimately holds secret-shaped content (test fixtures, sample keys),
  mark those lines with the inline `privacy-ok` marker, and only as a last
  resort track the one word `off` in `docs/secrets-scan` to disable the floor
  repo-wide (a reviewed, recorded decision). No new scaffolded file is required;
  absent `docs/secrets-scan` reads *on*.
- **Push policy + agent iteration branch (`docs/push-policy`).** Newer kits
  declare who may publish (process-options.md "Agent iteration branch &
  sync"): a one-word file — `human` (default: an agent never pushes, even if
  asked mid-session; it prepares the branch and requests), `agent-iteration`
  (only the scrubbed `llm/<branch>` iteration branch), or `agent`. To adopt:
  copy `push-policy.template` → `docs/push-policy` and pick the value in a
  reviewed commit. The full iteration-branch discipline (agent work on
  `llm/<branch>`, history scrubbed and collated into categorical commits
  before landing on the dev branch) is an **opt-in layer** for agent-driven
  repos — a repo without agent-driven work keeps the default file and pays
  nothing. If you adopt the layer, add `"llm/**"` to your CI push triggers
  (the newer shipped `check.yml` already carries it) so the floor runs on
  agent legs too.
- **Unattended coordinator (`scripts/agent_loop.py` + root `agent-resume.*`).**
  Newer kits ship a walk-away entry (process-options.md "Unattended
  operation"): the launchers boot the dispatcher (or one hands-on session at
  the right tier) and ship **inert** until their `AGENT_CMD` slot is wired. To adopt: copy the engine
  (kit-owned, overwrite freely on later re-syncs) + the three launchers
  (yours after seeding — like `run.*`), and merge the `out/run-logs/` line
  into `.gitignore`. The tracked `docs/iteration/` logs + `iteration_index.md`
  appear on first run; preserve them like `docs/log.md` — they are history. A
  repo without agent-driven work skips all of it.
- **Parallel dispatch (`agent-resume --jobs`, v4).** Newer kits let one
  `agent-resume` launch drive **every dependency-ready WI in parallel** — a
  dispatcher/integrator over the WI DAG with durable Git reservations and
  serialized atomic integration (process-options.md "Worker assignment" /
  "The parallel dispatcher" / "The atomic integrator"). Since WI-210 a **plain
  launch is the dispatcher** (the legacy serial resume driver and `--track`
  lanes are retired — one engine, one selection path): absent
  `--jobs`/`AGENT_JOBS` resolves to the two-worker default, and the dispatcher
  **holds at `--jobs 1` until two audits pass** — a SafetyClass audit (every
  open WI classified) and a soft-edge audit (signed via `docs/parallel-ready`).
  A fresh scaffold passes both by construction. **The upgrade recipe** (the
  **downstream-resync skill** walks it): re-sync the kit, run your own
  migration audits (the SafetyClass + soft-edge audits above), flip
  (`AGENT_JOBS=2` in the launchers), then drop any local reliance
  on the retired legacy surfaces — the resume-from-`status.md` prompt, a
  hand-set `docs/run-state`, `docs/rework-wi`, `--track`/`docs/tracks/*`
  lanes, and `docs/next-wi`/`docs/run-phase` (the WI DAG + `Priority` are the
  whole ordering contract — no former content translates to scheduling state).
  `docs/status.md`/`docs/run-state` are **generated** dispatcher surfaces (a
  hand-authored `status.md` is left untouched until you adopt the generated
  one). Legacy `active` rows reconcile to `queued` as a logged finding, and a
  leftover `docs/tracks/*` is your own note directory now — the dispatcher
  never reads it.
- **Run launchers become a capability menu (`scripts/run_menu.py` + `[run]`).**
  Newer kits retire the hard-wired, duplicated `RUN_CMD` in `run.cmd`/`run.sh`:
  the launchers are now thin delegates to `scripts/run_menu.py`, which reads a
  **`[run]` section** in `docs/stack.ini` (one `<name> = <command>` line per
  capability + optional `<name>.desc`) and presents a menu / launches by name /
  `--list`s for an agent (process-options.md §7 "the evaluator's rungs").
  **Never forced — your edited launchers keep working:** a re-sync never
  clobbers a `run.cmd`/`run.sh` you filled with a `RUN_CMD` (bootstrap skips
  existing files; only *new* scaffolds get the delegates). To adopt: copy
  `scripts/run_menu.py` from the kit, overwrite the three `run.*` launchers with
  the delegate versions, and move your old `RUN_CMD` value into a `[run]` line
  (e.g. `serve = <your old command>`). A pure library still just deletes them.
- **Skills layer (newer kits ship `skills/`).** To bring an agent's skills into an
  already-adopted repo, re-run `bootstrap.py --agents claude|gemini|codex|both`
  against it: it materializes the matched `kit`-scope skills into the agent dir
  (`.claude/skills/…` / `.gemini/skills/…` / `.agents/skills/…` for Codex) and
  copies the inert hook example, **skipping any skill file that already exists**
  (your edits are safe; use `--force` only after a diff pass). The `skills/SKILL.md`
  sources are kit-owned — overwrite freely on re-sync; a skill you customized
  locally, treat like `check.py` (take the new version, re-apply your delta). To
  refresh the per-agent copies from source after a kit skill changes, run
  `bootstrap.py --dest . --sync` (force-overwrites only the `<agent>/skills/…`
  subtrees; the `skills-sync` gate flags a drifted copy — S7). Skills are opt-in
  accelerators, never a gate (process-options.md "Skills layer").
- **Python floor 3.8 → 3.11 (2026-07, WI-262).** The kit's stdlib-only scripts
  now declare a **Python 3.11+** floor (was 3.8). Why 3.11 and not 3.9/3.10:
  those are EOL or nearly so (3.10's security EOL is Oct 2026), while 3.11 is
  supported to Oct 2027 and enables the queued `trace.py` refactor — `dataclass`
  `slots=True`, finer "did-you-mean" tracebacks, and the interpreter speedup. The
  `pytest-cov` Python-gated split dissolves with it: the old
  `5.x`-on-3.8 / `7.x`-on-3.9+ marker in `requirements-dev.txt` collapses to a
  single `pytest-cov~=7.0`, and `conftest.py` keeps only the 7.x coverage-wiring
  path (the pre-7 `COV_CORE_DATAFILE` fallback is gone). **Downstream impact:** on
  a re-sync onto a repo whose contributors or CI still run 3.8–3.10, provision
  3.11+ first, then overwrite `requirements-dev.txt`, bump the `check.yml` /
  `test.yml` matrix cells from 3.8 to 3.11 (the macOS-arm64 3.8 exclusion was a
  runner-availability workaround — 3.11 has arm64 builds, so drop it or keep it
  as a deliberate coverage call), and update the `dev-setup.*` "install Python
  3.x+" hints. The scripts stay de-facto runnable on 3.9 for now (no 3.11-only
  syntax has landed yet), so the bump is a promise you enforce in CI immediately,
  not a same-day code break.
- **`--require-verified` widened to method-blind (2026-07, WI-259).** The G3
  traceability floor `trace.py --require-verified` now demands `Status=Verified`
  for **every** ratified, in-phase SR regardless of its `Verification` method
  (was `Verification=Test` only), matching `derive_gate.sr_gate` — which already
  blocked G3 for any unverified decomposed SR. **Downstream impact:** a repo
  passing `--require-verified` today with a non-Test SR (Demonstration / Manual /
  Analysis / Inspection / Attest / Critique) still below `Verified` will now
  fail — it was never actually at the derived gate, only reporting so. To resync:
  set those SRs to `Verified` once acceptance is met (attach the TC evidence /
  recorded attestation), or mark them `Draft` if not yet ratified. The
  verification-basis report is now three-way (mechanized / demonstrated-observed /
  attested); no registry schema change.
- **Integrator verdict-gate unanimity + review-policy dial redefinition (2026-07,
  WI-260).** The parallel-dispatch integrator no longer clears on a *count* of
  approving phases: **every scheduled verdict phase's latest verdict at the
  reviewed head must be APPROVE** (REVIEW-A, REVIEW-B, and CRITIQUE on a
  render-surface train). The `review-policy` dial now counts **reviewer** phases
  scheduled (0/1/2); CRITIQUE is orthogonal — required on every render-surface
  train regardless of dial. A same-head CHANGES-REQUESTED→APPROVE flip escalates
  NEEDS-HUMAN rather than silently winning; a never-filed required phase pages
  instead of stalling. **Downstream impact:** if your repo runs the unattended
  parallel dispatcher, a train that previously integrated on an extra approval
  covering a missing phase will now block — ensure each scheduled phase actually
  files its verdict. No registry schema change.
- **Status-map freshness gate made machine-pure (2026-07, WI-266).** The
  `docs/open-items.md` PENDING block is split into a committed-tree-pure gated
  region (blocked WI rows + the run-state ask) and a **machine-local advisory**
  region (the `refs/llm/*`-derived source conflicts, reservations, quarantines,
  and stranded-train notes that don't transport with clone/push), separated by a
  labeled boundary; only the pure region is byte-compared by `--status --check`.
  **Downstream impact:** an adopter who seeded `docs/open-items.md` from the old
  template gets one STALE nudge on the next `status-map` gate — run
  `gen_trajectory.py --status` to regenerate the labeled block (your hand-authored
  `## OI-N` briefs above the markers stay byte-untouched). Overwrite the kit-owned
  `OPEN_ITEMS.template.md` on resync. *(Superseded by WI-322 below, which retires
  that file entirely — if you are adopting past that version, do its migration
  instead of this one.)*
- **The owner decision surface became a registry + a generated view (2026-07,
  WI-322).** `docs/open-items.md` is **retired**. Decision briefs are now ROWS in
  `docs/requirements/open-items.csv` (scaffolded from
  `registries/open-items.template.csv`), and `scripts/gen_open_items.py` renders
  them — together with every `Draft`/`Modified` spine row's per-cell
  before/after — into `docs/open-items.html`, the surface the owner reads. The
  driver was a real sitting: the old pending block was a POINTER ("run
  `trace.py --ratify modified`"), and the depth that makes a re-attest readable
  is a word-level diff, which markdown cannot mark.
  **Downstream impact — a one-time migration, and it is manual by design because
  only you can classify your briefs:**
  1. copy `registries/open-items.template.csv` to
     `docs/requirements/open-items.csv`;
  2. move each **pending** `## OI-N` section of your `docs/open-items.md` into a
     row (the section's fields map 1:1 onto the columns: one-line, decision,
     blast radius, options, recommendation). **Do not backfill ruled items** —
     their record is the log's Decisions, and OI ids have historically been
     reused after a section was deleted, so a backfill can collide;
  3. delete `docs/open-items.md`;
  4. run `python scripts/gen_open_items.py` and commit `docs/open-items.html`.
  The new `open-items` harness step gates its freshness (machine-local advisory
  region masked, like the block it replaces). If you skip the migration
  entirely, the step is **vacuous** — no registry and no view means nothing to
  render — so an adopter who never used the surface pays nothing.
- **The terminal `retired` work-item Status (2026-07, WI-267).** The work-item
  lifecycle gains a sixth `Status`, **`retired`** — a terminal WON'T-BUILD row
  that stays in the registry forever with its reason in the `Deliverable` column
  (never a `done` overload). Never breaking, vacuous until used: no schema/header
  change, and a registry with no retired rows behaves exactly as before. After
  resync, `check_trajectory.py` accepts `retired` (the unknown-status lint no
  longer fires) and validates it as terminal — **R-A** requires a non-empty
  `Deliverable` (the reason) and **R-F** requires an **empty** `SpecRef`;
  `schedule.py`/`agent_dispatch.py` never schedule it or count it as open;
  `gen_trajectory.py` renders it in its own dashboard bucket (a separate count,
  never folded into `done`). One behavior to know: **a retired predecessor does
  NOT satisfy a successor's hard dependency** the way `done` does — a live WI
  hard-blocked on a retired one stays `waiting` and is surfaced (a `dead-dep`
  finding; warn plain, ERROR under `--strict`), so re-home that edge or retire the
  successor too. Resync the kit-owned set together (`check_trajectory.py`,
  `schedule.py`, `agent_dispatch.py`, `gen_trajectory.py`) so the validator,
  scheduler, and dashboard agree.
- **The `Modified` re-attest marker + the basis-line format (2026-07, WI-316).**
  Spine `Status` gains a third recognized value, **`Modified`** — a
  post-attestation amendment owing a re-attest (canonical semantics:
  `process.md` §7): the derived gate reads G2 for its phase until the sitting
  flips it back (`Modified`→`Verified`, or →`Planned` when the amendment
  invalidated the evidence), the pending-owner-actions projection carries one
  line per Draft/Modified SR, a warn-first `--staged` check flags an amendment
  without the flip, and `trace.py --ratify modified` emits a per-cell
  before/after brief against the git-derived attested baseline. Never breaking
  for a registry that never writes the value — with one **flagged migration**:
  the `docs/gate` `# basis:` line now carries `modified=N` beside `drafts=N`,
  so the first `check.py`/pre-commit run after resync reds the `derived-gate`
  freshness step once. Fix: `python scripts/derive_gate.py` and commit the
  regenerated `docs/gate` (the first-non-comment-line gate value and its
  consumers are unchanged).

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
