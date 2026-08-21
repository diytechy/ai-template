# The LLM re-sync pack (bringing an adopted repo forward to a newer kit)

**Who reads this:** an LLM agent (or a human) carrying a repo that adopted this
kit at some earlier commit forward to a newer one. It is the single home for the
re-sync *rules* — the file classes, the per-change migration entries, the
concept renames. `ADOPTING.md` §6 frames the job and points here; the
`downstream-resync` skill sequences it and points here. **If a rule is wrong,
fix it here** — there is no second copy to keep in step.

<!-- check_vocab: allow-file — this pack is the DECLARED home of every concept
rename the kit has shipped, so it necessarily spells out retired vocabulary on
both sides of each arrow (§4 is literally the translation table). Exempting the
whole file is correct here and correct nowhere else: an entry that could not name
what it replaces would be useless to the reader it exists for. -->


**Where this lives, and which copy to read.** This is a kit reference doc
(`project-trajectory/RESYNC_PACK.md`), like `ADOPTING.md` and `EXAMPLE.md` — it
is **not** scaffolded into an adopting repo, deliberately. A copy frozen in your
repo at adoption time would be missing exactly the entries you need (the ones
added since), and a re-sync doc that is stale on the day it matters is worse than
no doc. So read the pack **from the kit checkout you are syncing TO** — the same
checkout you are diffing against, which this procedure already requires you to
have.

**The one anchor you have** is `docs/kit-version` in the adopting repo: the kit's
short SHA + date that bootstrap stamped there. Every entry in §3 and §4 below
carries `[since <sha>]` — the kit commit at which the change landed. That is what
makes range selection mechanical rather than a 40-entry read: your stamp's SHA to
your target SHA is a range, and an entry applies when its `since` SHA is **in**
that range. See §5 for what happens when the entries stop being prose.

---

## 1. The procedure

Bounded on purpose: this is what to read, in what order, and where the judgement
sits. Do not improvise a wider sweep — the deviation review in §2 is the sweep.

### 1.1 Establish the range

1. Read `docs/kit-version` — the kit short-SHA + date this repo was last
   scaffolded or re-synced from — and `docs/kit-profile`, the structural choices
   (stack + omitted sections) its process docs were *generated* with.
2. **If the stamp reads `unknown (kit not a git checkout)`**, the repo was
   scaffolded from a tarball and has **no anchor**. Do not guess a range.
   Reconstruct one from artifacts: which scripts and docs the repo actually has,
   which registry carriers are live, which columns its registries carry. Each §3
   entry names the artifacts its change creates or moves, so the entries
   themselves are the probe list. Treat the whole of §3 as potentially applicable
   and re-stamp honestly at the end.
3. Choose the target kit commit. **Sync only from a committed kit state**, never
   a dirty kit tree: bootstrap stamps `<sha>-dirty` and warns, and a dirty stamp
   is unreproducible and cannot be diffed later.
4. Diff the recorded SHA against the target *before touching anything*, so the
   moves below are driven by what actually changed rather than by this document's
   full length.
5. While the diff is open, recheck the **new capability surface** across the
   range — new or updated skills (`skills/INDEX.csv`), opt-in layers added to
   `process-options.md`, new vendorable packs (guardrails / efficiency /
   knowledge). An upgrade that only takes script fixes leaves accelerators on the
   table (`ADOPTING.md` §6).

### 1.2 The judgement this pack does NOT make for you

`SR-036` declares the overwrite-vs-preserve call **`verification = "Inspection"`**
— one of a handful of non-Test requirements in the kit's own spine — because it
rests on a fact no tool holds: *did the adopter edit this file, and does their
edit still mean something under the new kit?* This pack bounds what you look at
and states the default class for every kit-owned path. **It does not decide a
file you have edited.** Where §2's class and your local edit disagree, that is a
decision for the operator, recorded in the re-sync commit — not something to
resolve by taking the kit's copy because it is newer.

### 1.3 The order of moves

1. **Legacy one-word policy files first.** If the repo still carries them under
   `docs/`, fold them into `docs/process.toml` **before running anything else** —
   running with both homes live is *refused*, not resolved by precedence. §3
   entry *One policy home* has the command.
2. **Then a plain `bootstrap.py --dest .` re-run.** This is **ADD-ONLY**: it
   creates the files the repo lacks, updates **nothing** it already has, and
   never deletes a script the kit has since retired. It is the safe first move,
   not the whole move.
3. **Then the deviation review** (§2) over the changed files: overwrite,
   regenerate, re-apply dials, or preserve — per file, per its class.
4. **Then the applicable §3 entries**, oldest first. They cover what a file copy
   cannot: registry conversions, renamed or deleted scripts you must remove by
   hand, config folds, and state you must reconcile before a derived value is
   trustworthy. Where two entries touch the same artifact, the later one may
   *supersede* the earlier — each such pair says so in its text.
5. **Then the translation helper** (§4) for any concept your own prose, scripts,
   CI or registry cells still spell the old way.
6. **Re-stamp last.** Re-run bootstrap to refresh generated pieces (it re-stamps
   `docs/kit-version` + `docs/kit-profile`), refresh materialized per-agent
   skills with `bootstrap.py --dest . --sync` (scope guarantee: `--sync`
   force-overwrites ONLY the `<agent>/skills/…` subtrees, nothing else — the
   `skills-sync` gate flags a drifted copy), and commit the stamps as the
   **last** step so the record reflects the state you actually landed on.

### 1.4 Verify — and why a green can lie

Run the harness (`scripts/check.py` / `check.{sh,ps1}`) and `scripts/check_docs.py`.
A re-sync that leaves the harness red is not done.

**A green is only as new as your checkers.** If step 3 left any kit-owned script
un-updated, the repo is being judged by the OLD one — which cannot see what the
new kit refuses. This is measured, not hypothetical: on a three-week range, an
add-only re-sync leaves the spine registries under **both** carriers, a state the
current kit hard-refuses, and the surviving old `trace.py` passes it
(`tests/test_old_kit_resync.py` pins exactly this). Before believing the green,
run the **target** kit's checkers against your tree —
`python <kit>/scripts/trace.py --strict` from your repo root — and treat any
disagreement between the two as the list of moves step 3 still owes.

---

## 2. The file-by-file deviation review

### 2.1 The inventory

`bootstrap.py`'s `MAPPING` list is the authoritative inventory of every file the
kit places in an adopting repo: each row is `(source in the kit, destination in
your repo)`. Read it from the **target** kit — it is the file list for this
review, and it is generated-by-being-executable rather than a hand-kept table
that can rot. The kit checkout you are diffing against carries the reference copy
of every source in it, so "what should this file look like?" is always answerable
by reading, never by inference.

Walk the destinations, not your whole tree: a path that is not a MAPPING
destination is yours, and no re-sync rule applies to it.

### 2.2 The four classes

- **Overwrite freely (kit-owned; you don't hand-edit these).** The process
  scripts under `scripts/` (`trace.py`, `derive_gate.py`, `check_docs.py`,
  `check_flows.py`, `check_perf.py`, `check_privacy.py`, `gen_arch_map.py`,
  `gen_*`, `agent_loop.py`), the git hooks (`.githooks/pre-commit`,
  `.githooks/commit-msg`, `.githooks/pre-push`), `pytest.ini` markers, and
  **`scripts/check.py`**. `check.py` is safe to take wholesale because your whole
  toolchain lives in `docs/stack.ini` — the format/lint/test commands **and any
  project-specific gates, as `[step:<name>]` sections** — not in `check.py`. (If
  you still have a hand-added step inside a pre-`[step:]` `check.py`, move it into
  a `[step:<name>]` section once and it survives every re-sync after.) Diff before
  committing anyway, so a kit change you disagree with doesn't land unread.
- **Regenerate, never raw-copy (kit-owned but generated).** `docs/process.md` +
  `docs/process-options.md` are *generated* from the kit masters per the recorded
  `docs/kit-profile`. Raw-copying `PROCESS.md`/`PROCESS_OPTIONS.md` over them
  would ship the masters' `kit-only`/`profile` marker comments, the copy-me
  meta-prose, and any sections your repo opted out of. To take the new versions:
  **delete the two files, then re-run `bootstrap.py --dest .`** — it re-reads
  `docs/kit-profile` (explicit `--stack`/`--omit` flags override it), regenerates
  them with the same structural choices, and re-stamps `kit-version` +
  `kit-profile`.
- **Overwrite, then re-apply your dials (kit-owned, but hand-edited).**
  `docs/process.toml` — the one home for every process dial (gate authority, the
  human-ratification level, push authority, the reviewer count, the privacy and
  secrets gates, guardrails, the blackout window). Unlike `docs/stack.ini` it is
  **kit-owned**: its explanatory header and its key set come from
  `process.toml.template`, so take the kit's version on re-sync and re-apply your
  non-default values in the same commit — by hand, or by re-running the scaffold
  pass with `--gate-policy` / `--push-policy` / `--privacy-check`, which rewrite
  one key in place instead of replacing the file. `--force` **rewrites the whole
  file and resets every dial to the kit defaults**; never aim it at a live repo
  without a diff pass.
- **Preserve always (yours; the kit only seeds them).** `docs/stack.ini` (your
  declared toolchain — the kit seeds the Python reference once and never
  re-touches it; its `[generated]` section, the integrator's auto-resolution
  allowlist, is likewise project-owned), every registry — the four spine TOMLs
  (`docs/requirements/stakeholder-needs.toml`, `system-requirements.toml`,
  `low-level-requirements.toml`, `docs/test/test-cases.toml`) plus the off-spine
  registries that did not move carrier, and their legacy `.md`/`.csv` forms in a
  repo that has not run `migrate_carrier` yet — the `docs/work/` WI spec folder,
  `docs/status.md`, `docs/log.md`, `docs/plan.md` (your work plan — the kit seeds
  the block-list skeleton once), `docs/iteration/` + `docs/iteration_index.md`
  (session history), `docs/runtime-flows.md`'s authored flows (the architecture
  itself derives — there is no committed copy to preserve, see the
  `docs/architecture.md` RETIRES entry), `AGENTS.md` project content, the root launchers' EDIT
  slots, `docs/gate`, and `.gitignore`/`.gitattributes` (merge new kit lines in by
  hand). `bootstrap.py` **skips existing files**, so a plain re-run won't clobber
  these — but don't run it with `--force` against a live repo without a diff pass.

Two classes have **exceptions that an entry states**, and the entry wins: a §3
entry may invert a standing rule for one file (the clearest case is a migration
that requires `docs/gate` to be **regenerated** rather than preserved). Read the
applicable entries before applying the classes, not after.

### 2.3 Set-together files

Some kit-owned files only work as a **set** — take a newer hook with an older
`check.py` and every commit fails on a step that doesn't exist
(`check: no step named '<x>'`). Never re-sync one half of a set:

- `.githooks/pre-commit` + `scripts/check.py` — every entry that adds a harness
  step (`skills-sync`, `okf`, `trajectory-map`, `derived-gate`) names this.
- `scripts/trace.py` + `scripts/trace_text.py` — an `ImportError` on first check
  otherwise, not a quiet degradation.
- `scripts/spine_carrier.py` with `trace.py`, `check_trajectory.py`,
  `check_docs.py`, `trunk_step.py` and `agent_route.py`.
- `scripts/gen_trajectory.py` + the six `traj_*` renderers.
- The work-item vocabulary set: `check_trajectory.py`, `schedule.py`,
  `agent_common.py`, `wi_convert.py`, `gen_trajectory.py` + `traj_*`,
  `bootstrap.py` — the loaders, scheduler, converter and dashboard must share one
  status vocabulary.

`bootstrap.py` copies each set together; a hand-managed re-sync must too.

### 2.4 The per-file walk

For each MAPPING destination that the range changed:

1. Does the file exist in your repo? If not, the add-only re-run already created
   it — read it and move on.
2. Which class (§2.2) is it in, and does an applicable §3 entry override that
   class for this file?
3. Does your copy differ from the kit's copy at your **recorded** SHA? If it does
   **not**, you never edited it — take the kit's new version outright.
4. If it does differ, that difference is your edit. Re-apply it on top of the new
   version, or record why you are dropping it. This is the SR-036 judgement
   (§1.2); it is the only step of this review that is not mechanical.
5. Is it in a set (§2.3)? Then move the whole set in the same commit.

---

## 3. What changed over time

Every entry is anchored: `[since <sha>]` is the kit commit at which the change
landed, so an entry applies when that SHA falls inside your stamp-to-target
range. Entries are ordered **oldest first** — apply them in that order.

*(Writing an entry for a change that has not committed yet? You cannot know your
own commit's SHA, so anchor at the **preceding** commit and say so in a
parenthetical — the convention several entries below already use. Never leave an
entry unanchored: an entry with no SHA falls in no range and every re-sync skips
it silently.)*

### The TC `Tier` column [since af852db7]

Adoptions created `docs/test/test-cases.csv` before the `Tier` column existed.
`trace.py --strict-schema` requires `Tier` as a non-empty field (it validates the
full TC schema at DevStg-Impl). Migration is mechanical: add a `Tier` column and set a
default of `Full`; mark hardware/network/interactive cases `Release` so they
don't run on unattended CI. Once the column is present, `--strict-schema` also
validates that values are in `{Smoke, Full, Release}`, so tighten any free-text
entries at the same time.

### UN → SN id-tier rename (User Need → Stakeholder Need) [since 3ea00aa5]

The top tier was renamed. **Keep the id *numbers* — only the prefix changes**
(`UN-014` → `SN-014`); renumbering would break every back-link. Recipe: rename
the file reference and the prefix in the stakeholder-needs registry and every
`SN-Refs`/`UN-Refs` cell across the SR registry, then rerun `trace.py --strict`
(it validates the SN↔SR join and will flag any missed `UN-###`). **Do *not*
rewrite audit-log / status.md evidence quotes** that say "UN-014" — those are a
historical record of what was decided at the time; rewriting history to match a
later rename is dishonest. Leave them, optionally with a one-line
"(UN-### = today's SN-### after the rename)" note where confusion is likely.

- *Tooling latitude:* `trace.py` intentionally does **not** accept legacy
  `UN-Refs` — a lingering `UN-` after you claim the rename is done is a real
  orphan you want surfaced, not silently bridged, and the migration is a one-time
  find-replace, not an ongoing compatibility burden. If your repo is mid-rename
  and wants a transitional deprecation warning, that's a *local* patch to your
  copy of `trace.py`, not something the kit ships.
- *Downstream test import:* overwriting `scripts/gen_release_checklist.py` from
  the kit renames its public function `read_user_needs` →
  `read_stakeholder_needs`. Any downstream test or script that imports
  `gen_release_checklist.read_user_needs` by the old name will break (a real
  adopter was bitten by this). Grep for `read_user_needs` in your tests and
  scripts as part of this recipe.

### `process.md` splits into `process.md` + `process-options.md` [since cdb64dc2]

The opt-in layers (phased delivery, lifecycle tags, the §8/§9 boundary notes, the
multi-repo rung) moved out of `process.md` into a companion
`process-options.md`, keeping `§`-numbering stable. To migrate: drop in **both**
new files; anything your repo added *inside* the old monolith (rare — it's
kit-owned) moves to whichever file now owns that section. Fix references: a link
to `process.md#section-9` may now point into `process-options.md`. Run
`check_docs.py` — it fails on exactly these broken intra-repo links.

### `Attest` verification kind + the binary-asset registry [since 31f43343]

The **`Attest`** `Verification` method (a named human's recorded judgment —
playtest, creative review, physical action — for what can't be mechanized) and an
optional **`assets`** registry (`ASSET-###`) for unavoidably-binary deliverables.
To adopt: overwrite `scripts/trace.py` (it now accepts `Attest` in the vocabulary
and reports the "attested vs mechanized" split) and drop in the assets registry
template. Retag any SR you were faking as `Test`/`Manual` but that really rests on
human judgment to `Verification=Attest`, and record **who/when** in its TC cell.
For binary deliverables (art, music, voice, video): manage them as **git-LFS or
out-of-repo pointers** and record provenance (human/AI — for Steam-style
AI-content disclosure), license, attribution, and the contract/release link as
`ASSET-###` rows — track *about* the asset in text even though the asset itself
can't be diffed. Both are opt-in; a scope with no subjective or binary work
ignores them (process-options.md "Proportionality doctrine" + "Binary assets").

### The skills layer [since 1bafeb11]

Newer kits ship `skills/`. To bring an agent's skills into an already-adopted
repo, re-run `bootstrap.py --agents claude|gemini|codex|both` against it: it
materializes the matched `kit`-scope skills into the agent dir
(`.claude/skills/…` / `.gemini/skills/…` / `.agents/skills/…` for Codex) and
copies the inert hook example, **skipping any skill file that already exists**
(your edits are safe; use `--force` only after a diff pass). The `SKILL.md`
sources are kit-owned — overwrite freely on re-sync; a skill you customized
locally, treat like `check.py` (take the new version, re-apply your delta). To
refresh the per-agent copies from source after a kit skill changes, run
`bootstrap.py --dest . --sync`. Skills are opt-in accelerators, never a gate
(process-options.md "Skills layer").

### The unattended coordinator (`scripts/agent_loop.py` + root `agent-resume.*`) [since 0386838a]

A walk-away entry point (process-options.md "Unattended operation"): a plain
launch drives the claim→build→integrate loop, and the launchers ship **inert**
until their `AGENT_CMD` slot is wired. To adopt: copy the engine (kit-owned,
overwrite freely on later re-syncs) + the three launchers (yours after seeding —
like `run.*`), and merge the `out/run-logs/` line into `.gitignore`. The tracked
`docs/iteration/` logs + `iteration_index.md` appear on first run; preserve them
like `docs/log.md` — they are history. A repo without agent-driven work skips all
of it.

### Conditional scaffold generation (`docs/kit-profile`) [since c0bd5207]

Newer kits *generate* `docs/process.md` + `docs/process-options.md` from
marker-carrying masters per a recorded profile (`docs/kit-profile`: `stack=` +
`omit=nfr,multi-module` axes; omitted sections keep their § heading plus a
one-line stub, so labels never renumber and links never dangle). An older
adoption has no profile record; its first re-sync is a **one-time regeneration**:
delete the two process docs, re-run `bootstrap.py --dest . [--stack …] [--omit …]`,
and commit the two regenerated docs plus the new `docs/kit-profile`. With no
`--omit` the regenerated docs match the old full copies (minus the copy-me
meta-prose the markers now strip); declaring omissions is opt-in and can happen
at any later re-sync.

### Push policy + the agent iteration branch [since 5aae786e]

Newer kits declare who may publish (process-options.md "Agent iteration branch &
sync"): one word — `human` (default: an agent never pushes, even if asked
mid-session; it prepares the branch and requests), `agent-iteration` (only the
scrubbed `llm/<branch>` iteration branch), or `agent`. To adopt: set the push
dial in a reviewed commit (it lives in `docs/process.toml` since the one-policy-home
entry below; it was its own one-word file before). The full iteration-branch
discipline (agent work on `llm/<branch>`, history scrubbed and collated into
categorical commits before landing on the dev branch) is an **opt-in layer** for
agent-driven repos — a repo without agent-driven work keeps the default and pays
nothing. If you adopt the layer, add `"llm/**"` to your CI push triggers (the
newer shipped `check.yml` already carries it) so the floor runs on agent legs too.

### The `Area` column on the SR registry (owner-hat coverage) [since 5e743dda]

Newer kit templates end the SR schema with an optional `Area` field (owner-hat /
domain tag, process.md §1); `trace.py` reports per-Area SR counts when it carries
values. Adding it to an existing registry is **optional, not a migration** — the
field is outside the required schema, so a legacy registry without it stays green
even under `--strict-schema`.

### status/log split (`docs/status.md` → `status.md` + `docs/log.md`) [since 6a74684c]

The blackboard splits: `status.md` is the **working surface** — only what the
agent or human must perform next — and `docs/log.md` is the **append-only
history** it points at (the Sittings table, verdict blocks, ratified
decisions, session notes; process.md §5). Migration is **optional and
proportionate — never forced**: an adopted repo may keep its merged file. To
adopt: copy `LOG.template.md` → `docs/log.md`, cut the accreted history sections
over **with their headings preserved verbatim** (downstream greps and the §5
wording rely on them), and leave the `History: docs/log.md` pointer in
status.md's header. Don't rewrite the moved entries — they are the historical
record.

### The secrets floor runs in every repo [since 24a8bab1]

The deterministic secrets floor (private-key headers + GitHub/Slack/AWS/`sk-…`
shapes) runs in **all** repos, not just privacy-checked ones (process-options.md
"Secrets floor (every repo)"). Overwriting the hooks + `check_privacy.py` on
re-sync therefore starts scanning a privacy-off repo that previously had none:
the pre-commit hook blocks a staged commit carrying a credential shape,
`check.py` flags a tracked one at every gate, and the pre-push hook scans the
outgoing range. **That is the point** — but if the repo legitimately holds
secret-shaped content (test fixtures, sample keys), mark those lines with the
inline `privacy-ok` marker, and only as a last resort disable the floor repo-wide
(`secrets_scan = false` in `docs/process.toml` today; a reviewed, recorded
decision). No new scaffolded file is required; the default is on, and a repo
migrating from the one-word file's *absent = on* convention lands on the same
value.

### Privacy-check toggle — replaces the old `docs/commit-identity` glob [since 914f9b10]

Newer kits split *identity* from *privacy* (process-options.md "Commit identity &
privacy"): which account authors is the user's own git config (no longer pinned
by a repo file), and a boolean dial runs the privacy gate — the commit author
email and committed content/messages are scanned for PII, with the exempt-email
allowlist (`EXEMPT_EMAILS`, default `*noreply*`) in `check_privacy.py`. To adopt:
overwrite the hooks (`pre-commit`, the new `commit-msg`, `pre-push`) +
`check_privacy.py` + `setup.*` from the kit, delete `docs/commit-identity`, and
set the privacy dial (`true` if you had a non-`inherit` glob, else `false`; the
dial lives in `docs/process.toml` since the one-policy-home entry below). Note
that the pre-commit author check is now a Python `--author` step, so a
Python-less machine no longer enforces identity — deliberate, that pin moved to
git config. The guard covers **future commits in clones that ran setup** only —
history already committed with a private identity needs a git history rewrite,
out of the kit's scope; decide that deliberately before publishing.

### The TC `Evidence` column [since 328f141e]

The test-case registry gains an **`Evidence`** field (between `Automated` and
`Status`) naming the concrete test — a pytest node, a script path, or a
procedure-doc link (inspection-only text, never mechanically resolved). Optional
in general, but from DevStg-Impl `--strict-schema` **requires it non-empty on
`Automated=Yes` rows** — a claimed-automated test with no cited location is a soft
false-green; a legacy registry without the column reads as empty and is flagged
the same way. Migration: add the field, then move any test pointers you had
squeezed into `Parameters` (the old `node=…` workaround) into `Evidence`,
restoring `Parameters` to dimensional inputs only. Below DevStg-Impl a legacy file keeps
passing untouched.

### The component / workstream schema bundle [since 73313e69]

Four coupled, **never breaking** registry changes land together (the bundle spans
`73313e69`…`7f8cdc56`):

**(a)** the work-items `Track` column is renamed **`Workstream`** (a mutable
grouping category — "track" now means only the parallel-execution lane); the
legacy header is still read, so migration is renaming one header cell whenever
convenient. **(b)** `Predecessors` gains an edge kind: a bare id is a **hard**
(blocking) edge, a `~`-prefixed id (`~WI-013`) a **soft** advisory-ordering edge —
audit your DAG and demote narrative "reads-well-after" edges to `~`. **(c)** A new
optional **`components`** registry (`CMP-###`, process-options.md "Component
layer") is scaffolded, and the LLR/IF/ASSET/PART templates gain an optional
`Component` tag column; existing files without it stay valid (header-driven) —
adopt by adding it where you name components. **(d)** The multi-repo registry is
renamed **`repos.csv` / `REPO-###`** (formerly `modules.csv`/`MOD-###`); the
legacy file + ids are still read, and both may coexist mid-migration.

### The OKF knowledge bundle [since 27ebc29d]

Newer kits export the spine registries as a generated `docs/okf/` bundle, **on by
default** with a pre-commit + DevStg-Impl freshness gate. After a re-sync, either run
`python scripts/gen_okf.py` once and commit the bundle (it stays fresh via the
hook from then on), or opt out with `okf_export = false` under `[checks]` in
`docs/process.toml` — a repo with placeholder-only registries needs neither
(vacuous). **Re-sync `check.py` together with the hook:** the hook's step 1b runs
`check.py --run-step okf`, so an older `check.py` with no `okf` step fails every
commit with `check: no step named 'okf'`. The okf step runs **before** the
dashboard step on purpose: the dashboard consumes the bundle (its Knowledge tab),
so the regen order is arch-map → okf → trajectory.

### `docs/trajectory.html` → root `PROJECT_STATE.html` [since 3e56f7ce]

The trajectory dashboard evolved into the unified project-state artifact at the
repo **root** (adds the How-SW module-map view, the optional CMP table, and a
git-derived as-of stamp that `--check` ignores). Migration: after the re-sync,
delete your committed `docs/trajectory.html`, run
`python scripts/gen_trajectory.py`, and commit the new root file — the
`trajectory-map` gate/hook step name is unchanged and now checks the new path
automatically.

### Architecture-connectivity coverage (the `IF-###` tier) [since 05b1b73b]

`trace.py` now reads the `IF-###` interface tier (id/SR-Refs integrity, closing
the SR-002-era gap), the interfaces template gains a `Notes` column (legacy rows
read it empty), and `check_trajectory.py` runs a warn-first **connectivity
coverage** over the arch-map inventory. It is **opt-out, default-on**, so after a
re-sync a **multi-module** repo with no declared seams starts warning
"connectivity undeclared" at the hook and DevStg-Impl. That never fails a gate — the warns
only nudge. To act on them, declare `IF-###` rows (process.md §8; use a
`source`/`sink` first-word `Notes` marker for a deliberate pure source/sink) and
regenerate the arch-map + `PROJECT_STATE.html`; to silence the whole layer, set
`interfaces_check = false` under `[checks]` in `docs/process.toml`. A
single-module repo is vacuous and needs nothing.

### Cross-agent skill sync (the `skills-sync` harness step) [since 2b0c013f]

The hook gains a `check.py --run-step skills-sync` step, so **re-sync `check.py`
together with the hook** — an older `check.py` with no `skills-sync` step fails
every commit with `check: no step named 'skills-sync'`. The step is vacuous
unless the repo hosts the neutral `skills/` source and per-agent skill dirs; if
you keep per-agent copies (`.claude`/`.gemini`/`.agents` `skills/`), refresh them
from source with `bootstrap.py --dest . --sync` and commit — a drifted copy is a
gate finding.

### Run launchers become a capability menu (`scripts/run_menu.py` + `[run]`) [since 3ca5e42b]

Newer kits retire the hard-wired, duplicated `RUN_CMD` in `run.cmd`/`run.sh`: the
launchers are thin delegates to `scripts/run_menu.py`, which reads a **`[run]`
section** in `docs/stack.ini` (one `<name> = <command>` line per capability +
optional `<name>.desc`) and presents a menu / launches by name / `--list`s for an
agent. **Never forced — your edited launchers keep working:** a re-sync never
clobbers a `run.cmd`/`run.sh` you filled with a `RUN_CMD` (bootstrap skips
existing files; only *new* scaffolds get the delegates). To adopt: copy
`scripts/run_menu.py` from the kit, overwrite the three `run.*` launchers with
the delegate versions, and move your old `RUN_CMD` value into a `[run]` line
(e.g. `serve = <your old command>`). A pure library still just deletes them.

### The derived gate (`docs/gate` becomes generated) [since 03b27c44]

The re-sync ships `derive_gate.py` and a `check.py --run-step derived-gate` step
(so re-sync `check.py` + the hook together). `docs/gate` is now **generated** from
the artifact states — run `python scripts/derive_gate.py` **once** to migrate your
legacy hand-set `docs/gate` to the derived form (until you do, the
`derived-gate --check` step accepts the old one-line value **value-only**, so an
un-migrated repo is never broken). After migrating you stop bumping the line — you
ratify artifacts (`Status` `Draft`→`Planned`, or an SN section move) in a reviewed
commit and regenerate (process-options.md "Derived gate model").

**Reconcile states against your ratification history before trusting the migrated
value.** The derived gate believes your recorded `Status` values and SN sections —
but a legacy repo's registries usually contain artifacts added *after* the commit
that last set `docs/gate`, states no reviewer ever ratified. Find that commit
(`git log --oneline -- docs/gate`), diff the requirement surfaces since
(`git diff <sha>..HEAD -- docs/requirements docs/test`), and stage everything
added or materially changed since per the new model — new stakeholder needs into a
`## Draft needs (unratified)` section, not-yet-re-reviewed SRs to `Status=Draft` —
so `derive_gate.py` reproduces the gate your history actually attests instead of
laundering post-attestation additions into it. If the derived value still
disagrees with your old hand-set line after that, **the disagreement is the
finding**: ratify (or demote) deliberately before relying on the derived gate.

### The phase model, and the retired grouping column [since 6daee92f]

The delivery `Phase` is now a field on the LLR and TC registries too (it was
SR-only), and the work-item registry **drops** its old per-WI grouping column (the
one the dashboard used to bin the roadmap by — it now tiers
`phase ⊃ workstream ⊃ work-item`). Both changes are **vacuous-until-armed**, so a
re-sync is diffable and never breaks: a registry with no phased row keeps
`trace.py`'s ratified-Phase schema rule dormant (blank = in scope for every
phase), and any leftover grouping column is simply ignored (read by name, no
vocabulary rule).

### `--require-verified` widened to method-blind [since a686bcc8]

The DevStg-Impl traceability floor `trace.py --require-verified` now demands
`Status=Verified` for **every** ratified, in-phase SR regardless of its
`Verification` method (was `Verification=Test` only), matching
`derive_gate.sr_gate` — which already blocked DevStg-Impl for any unverified decomposed SR.
**Downstream impact:** a repo passing `--require-verified` today with a non-Test SR
(Demonstration / Manual / Analysis / Inspection / Attest / Critique) still below
`Verified` will now fail — it was never actually at the derived gate, only
reporting so. To re-sync: set those SRs to `Verified` once acceptance is met
(attach the TC evidence / recorded attestation), or mark them `Draft` if not yet
ratified. The verification-basis report is now three-way (mechanized /
demonstrated-observed / attested); no registry schema change.

### Integrator verdict-gate unanimity + reviewer-dial redefinition [since 15015bd9]

The integrator no longer clears on a *count* of approving phases: **every
scheduled verdict phase's latest verdict at the reviewed head must be APPROVE**
(REVIEW-A, REVIEW-B, and CRITIQUE on a render-surface train). The reviewer dial
(`review_rounds`) now counts **reviewer** phases scheduled (0/1/2); CRITIQUE is
orthogonal — required on every render-surface train regardless of dial. A
same-head CHANGES-REQUESTED→APPROVE flip escalates NEEDS-HUMAN rather than
silently winning; a never-filed required phase pages instead of stalling.
**Downstream impact** *(historical — the v4 dispatcher retired at the Phase 5
restructure below; `integrate.py`'s serial verdict gate keeps the same
every-scheduled-phase-APPROVE rule)*: a train that previously integrated on an
extra approval covering a missing phase will now block — ensure each scheduled
phase actually files its verdict. No registry schema change.

### Status-map freshness gate made machine-pure [since 1282f52c]

*(Superseded by the open-items registry entry below, which retires
`docs/open-items.md` entirely — if you are syncing past that commit, do that
migration instead of this one.)* The `docs/open-items.md` PENDING block is split
into a committed-tree-pure gated region (blocked WI rows + the run-state ask) and
a **machine-local advisory** region (the `refs/llm/*`-derived source conflicts,
reservations, quarantines and stranded-train notes that don't transport with
clone/push), separated by a labeled boundary; only the pure region is
byte-compared by `--status --check`. **Downstream impact:** an adopter who seeded
`docs/open-items.md` from the old template gets one STALE nudge on the next
`status-map` gate — run `gen_trajectory.py --status` to regenerate the labeled
block (your hand-authored `## OI-N` briefs above the markers stay byte-untouched).
Overwrite the kit-owned open-items template on re-sync.

### The terminal `retired` work-item status [since baed9159]

*(Superseded by the six-state entry below, which respells this `cancelled` and
gives it its own directory; an adopter re-syncing past both applies them in
order.)* The work-item lifecycle gains a sixth `Status`, **`retired`** — a
terminal WON'T-BUILD row that stays in the registry forever with its reason in the
`Deliverable` column (never a `done` overload). Never breaking, vacuous until
used: no schema/header change, and a registry with no retired rows behaves exactly
as before. After re-sync, `check_trajectory.py` accepts `retired` (the
unknown-status lint no longer fires) and validates it as terminal — **R-A**
requires a non-empty `Deliverable` (the reason) and **R-F** requires an **empty**
`SpecRef`; the scheduler never schedules it or counts it as open;
`gen_trajectory.py` renders it in its own dashboard bucket (a separate count,
never folded into `done`). One behavior to know: **a retired predecessor does NOT
satisfy a successor's hard dependency** the way `done` does — a live WI hard-blocked
on a retired one stays `waiting` and is surfaced (a `dead-dep` finding; warn plain,
ERROR under `--strict`), so re-home that edge or retire the successor too.

### Python floor 3.8 → 3.11 [since 8cd569ae]

The kit's stdlib-only scripts declare a **Python 3.11+** floor (was 3.8). Why 3.11
and not 3.9/3.10: those are EOL or nearly so (3.10's security EOL is Oct 2026),
while 3.11 is supported to Oct 2027 and enables the queued `trace.py` refactor —
`dataclass` `slots=True`, finer "did-you-mean" tracebacks, and the interpreter
speedup. The `pytest-cov` Python-gated split dissolves with it: the old
`5.x`-on-3.8 / `7.x`-on-3.9+ marker in `requirements-dev.txt` collapses to a single
`pytest-cov~=7.0`, and `conftest.py` keeps only the 7.x coverage-wiring path.
**Downstream impact:** on a re-sync onto a repo whose contributors or CI still run
3.8–3.10, provision 3.11+ first, then overwrite `requirements-dev.txt`, bump the
`check.yml` / `test.yml` matrix cells from 3.8 to 3.11 (the macOS-arm64 3.8
exclusion was a runner-availability workaround — 3.11 has arm64 builds, so drop it
or keep it as a deliberate coverage call), and update the `dev-setup.*` "install
Python 3.x+" hints. The scripts stay de-facto runnable on 3.9 for now, so the bump
is a promise you enforce in CI immediately, not a same-day code break.

### The owner decision surface becomes a registry + a generated view [since 41b228a5]

`docs/open-items.md` is **retired**. Decision briefs are now ROWS in
`docs/requirements/open-items.toml`, and `scripts/gen_open_items.py` renders them —
together with every `Draft`/`Modified` spine row's per-cell before/after — into
`docs/open-items.html`, the surface the owner reads. The driver was a real sitting:
the old pending block was a POINTER ("run `trace.py --ratify modified`"), and the
depth that makes a re-attest readable is a word-level diff, which markdown cannot
mark.

**Downstream impact — a one-time migration, and it is manual by design because
only you can classify your briefs:**

1. copy the open-items registry template to `docs/requirements/open-items.toml`;
2. move each **pending** `## OI-N` section of your `docs/open-items.md` into a row
   (the section's fields map 1:1 onto the columns: one-line, decision, blast
   radius, options, recommendation). **Do not backfill ruled items** — their
   record is the log's Decisions, and OI ids have historically been reused after a
   section was deleted, so a backfill can collide;
3. delete `docs/open-items.md`;
4. run `python scripts/gen_open_items.py` and commit `docs/open-items.html`.

The `open-items` harness step gates its freshness (machine-local advisory region
masked, like the block it replaces). If you skip the migration entirely, the step
is **vacuous** — no registry and no view means nothing to render — so an adopter
who never used the surface pays nothing.

### The `Modified` re-attest marker + the basis-line format [since 4cc61fa3]

Spine `Status` gains a third recognized value, **`Modified`** — a
post-attestation amendment owing a re-attest (canonical semantics: process.md
§7): the derived gate reads DevStg-Tests for its phase until the sitting flips it back
(`Modified`→`Verified`, or →`Planned` when the amendment invalidated the
evidence), the pending-owner-actions projection carries one line per
Draft/Modified SR, a warn-first `--staged` check flags an amendment without the
flip, and `trace.py --ratify modified` emits a per-cell before/after brief against
the git-derived attested baseline. Never breaking for a registry that never writes
the value — with one **flagged migration**: the `docs/gate` `# basis:` line now
carries `modified=N` beside `drafts=N`, so the first `check.py`/pre-commit run
after re-sync reds the `derived-gate` freshness step once. Fix:
`python scripts/derive_gate.py` and commit the regenerated `docs/gate` (the
first-non-comment-line gate value and its consumers are unchanged).

### The LLR `Rationale` column [since c1bcc389]

The LLR registry gains an optional **`Rationale`** field after `Detail`.
Non-breaking and header-driven: a registry without it reads as blank and stays
valid, so migration is adding one field whenever convenient. *Why it exists:*
`Detail` was the LLR's only prose cell, so the *what*, the *why*, the ruled-out
alternatives and the authoring history were structurally forced into one field —
and a cell asked to hold four things holds none of them legibly. `Rationale` is a
requirement attribute at **every** level (ISO/IEC/IEEE 29148); the SR had one and
the LLR did not, and that asymmetry was the bug. It stays **optional** on purpose:
a short mechanical decomposition row's why *is* its parent SR's, and requiring one
everywhere would manufacture exactly the restatement the process forbids. Fill it
where the decomposition was itself a decision. It is normative text, so the
stand-alone rule applies — no work-item ids, no process-doc citations (`trace.py`
gates it under `--strict`).

### `trace.py` splits into two files [since f18672e5]

`scripts/trace_text.py` joins `scripts/trace.py`, and **a re-sync must copy both**
— `trace.py` imports its spine-row text layer from the sibling, so a repo that
picks up one and not the other gets an `ImportError` on its first check rather
than a quiet degradation. `bootstrap.py` copies them together; a hand-managed
re-sync must too. No behaviour changes: the split is pure decomposition, and the
kit's three golden report files stay byte-identical across it. *Why:* the four
text predicates (`provenance_findings`, `form_findings`, `paraphrase_advisories`,
`ac_advisories`) and the row primitives they share are one concern — *is this row
readable and decidable on its own?* — and pure (rows in, findings out), so they
separate cleanly from the join that owns I/O and reporting.

### Parallel dispatch (v4) is deleted; the integration seam replaces it [since 31ad569d]

The v4 dispatcher/integrator — durable Git reservations, `--jobs`/`AGENT_JOBS`,
worktree pools, `docs/run-state`, train branches — is **deleted**: its lifetime
record (19 reservations → 8 integrations → 0 gate-verified, 11 hand-rescues) did
not justify its 4,042 lines. What replaces it is composition (process-options.md
"Unattended operation" / "Parallel work — the integration seam"): claims are
`integrate.py claim` (queued spec → `docs/work/active/<branch>/`, branch cut from
the claim commit), merging is `integrate.py integrate` (the serial fail-closed
queue — full bar on the composed tree, verdict gate), and a plain `agent-resume`
launch **drives** the loop: frontier → claim → worker session → merge, the
frontier re-derived every cycle so mid-run-filed WIs are picked up in the same
run.

**The upgrade recipe:** re-sync the kit, convert the WI registry CSV to the spec
folder (`wi_convert.py --verify` → `--to-specs` → delete the CSV — and DELETE
it, not keep it beside the folder: the dual-read grace window is over, the
folder wins when it holds real specs, and a repo carrying BOTH homes is an
integrity ERROR on the current kit, not a fallback), drain or
hand-finish any live train worktrees/branches from the old scheme, seed
`docs/stack.ini [generated]`, then delete local reliance on the retired surfaces —
`AGENT_JOBS`, `docs/run-state`, `docs/rework-wi`, `--track`/`docs/tracks/*`,
`docs/next-wi`/`docs/run-phase`, `refs/llm/*`, `docs/parallel-ready`. The WI DAG +
`Priority` are the whole ordering contract; no former content translates to
scheduling state.

### An LLR grounding on a superseded SR is an integrity ERROR [since 871625ec]

*(Superseded by the SR-tier `SupersededBy` retirement below — the validator this
entry describes no longer ships.)*

If your SR registry uses the optional `SupersededBy` field, an LLR whose `SR-Refs`
cites a superseded SR reds `trace.py` at every gate after this re-sync (`--strict`
and `--strict-integrity`) — re-ground each such LLR on the successor SR, or delete
it, before re-syncing `trace.py`. TC citations of superseded SRs stay legal (they
are the retained evidence record). A registry without the field is unaffected.

### The six-state work-item model; `docs/work/archive/` splits and `disposition` is deleted [since 88db58af]

*A flagged migration — the one kit change so far that MOVES files in your
registry.* The status vocabulary becomes
`draft | queued | active | deferred | cancelled | complete`, and status stays what
it always was, the directory — only now the directory is the **whole** statement.
`archive/` held both terminal states, so it needed a `disposition = "retired"`
frontmatter key plus a validator to keep folder and attribute honest; splitting it
into `complete/` and `cancelled/` deletes the key, the validator and both of its
raise paths, because the inconsistent state it checked for is no longer
representable. Two words change with it: `retired` becomes `cancelled` (it could
be read as *finished and put out to pasture*; `cancelled` cannot), and `draft/` is
new — thinking-in-progress, which previously had to sit in `deferred/` and so read
as *a decision* rather than *the absence of one*.

Migrate in one commit:

1. `git mv` each `docs/work/archive/WI-*.md` carrying `disposition = "retired"` to
   `docs/work/cancelled/`, and every other `docs/work/archive/WI-*.md` to
   `docs/work/complete/`;
2. delete the `disposition = "retired"` line from the moved cancelled specs — the
   folder is now the whole statement;
3. `mkdir docs/work/draft` (add a `.gitkeep`; a fresh scaffold ships it), and
   remove the emptied `docs/work/archive/`;
4. rerun `check_trajectory.py --strict`: the loaders REFUSE an undeclared status
   directory, so a spec left behind in `archive/` is a loud, named error, never a
   silent skip.

Use `git mv` rather than delete+add: the backlog-staleness clock reads
`git log --follow --diff-filter=AM`, and it needs BOTH flags — driven on this
kit's own migration, `--follow` alone and `--diff-filter=AM` alone each answer the
rename commit (today), while the pair answers the row's true pre-migration date. A
rewritten history re-dates every row.

*Why `draft/` had to be a DECLARED directory rather than a scratch folder:*
because there is nowhere else safe to put a draft, and the two wrong places fail
differently. Both were driven on a fresh scaffold with the same spec. **An
undeclared directory UNDER `docs/work/`** (say `docs/work/thinking/`): the readers
walk `<status>/WI-*.md` and skip anything under a directory they do not know, so
the spec never enters the registry at all — the duplicate-id guard and the
dashboard go blind, `schedule ready` prints nothing and `gen_trajectory` renders
no document. The id mint alone survives, because it reads FILENAMES through an
unfiltered walk, so the id is held by accident rather than by design; and
`check_trajectory --strict` exits 1 naming the directory, so at least the state is
LOUD. **A folder outside `docs/work/`** (say `docs/drafts/`) is worse in the way
that matters: the mint does not see it either — so the next mint really would
reissue the held id — and **nothing reds**; `check_trajectory --strict` reads
`clean (no work items …)` and exits 0.

### The dispatcher split: `drive.py` → `dispatch.py` + `lane.py` [since 81cac0e1]

`scripts/drive.py` is renamed `scripts/dispatch.py` with `scripts/lane.py`
extracted (one lane's mechanics: worktree, worker subprocess, the refresh). On
re-sync, copy both new scripts and **delete your old `scripts/drive.py`** — a
stale copy would shadow nothing (`agent_loop` imports `dispatch`) but would drift
silently. The dispatcher now admits by the session-hold table: spine-class WIs
wait for the lanes to drain and then admit **together as one batch**, and a
pending ratification drains the lanes and exits 0 naming the cards in
`open-items.html` instead of refusing nonzero. The worker-lane count is a new
declared dial — `lanes` in `docs/stack.ini [agent-loop]` (CLI `--lanes` >
`AGENT_LANES` > stack.ini > default). **An absent key means 1**: your repo stays
exactly as serial as it was until you add the line (fresh scaffolds seed
`lanes = 2`); no re-sync ever changes your lane count, because `docs/stack.ini` is
yours.

### `Phase` is numeric-only once armed [since e0623526]

Once any row is phased, a *ratified* SR/LLR/TC `Phase` must be a **full-cell bare
integer** (`1`, `2`, …) — a prefixed label (`v2`, `P1`) is now a `--strict-schema`
finding, because the `--phase`/`--ratify` filters and the phase-drop detector match
the cell literally and a prefixed cell disarms them silently. A `vN` label still
digit-parses in those filters and the derived current phase (grandfathering), so a
`vN` registry **arms the rule and now fails it**: strip prefixes (`v2` → `2`)
across ratified rows when you take this kit version — a mechanical, diffable edit
(`Phase` is a *traced* cell, so no re-attest window opens). Once you phase any row,
phase every *ratified* SR/LLR/TC — blank stays legal on `Draft` rows only — and the
foundation (minimum) phase stays in scope under `--phase`.
`derive_gate.py --next-phase` prints the number a newly confirmed phase takes.

### One policy home (`docs/process.toml`) [since c560f928]

The ~10 one-word policy files under `docs/` — the gate-authority word, the push
policy, the reviewer count, the privacy toggle, the secrets floor, the
privacy-review posture, guardrails, the blackout window — collapse into a single
hand-edited, machine-read TOML. The old idiom was never a ruling: it accreted
around the git hooks' pure-sh parse (a Python-less box must still fail closed on a
declared privacy policy), and a `head -n 1` read is the only thing that format
buys. The hooks now do a **keyed** match instead, so the file's shape is
load-bearing: one `key = value` per line under a bare `[section]` header, no dotted
keys, no inline tables, no multi-line strings — checked, not merely conventional.

To adopt: re-sync the three hooks + the scripts, take `process.toml.template` →
`docs/process.toml`, then run
**`python scripts/bootstrap.py --migrate-config --dest .`**. It folds every legacy
file it finds into the matching key, **deletes that file**, and is idempotent — and
a full `bootstrap.py --dest .` scaffold pass runs it for you. Two dials change
*type*, not meaning: the reviewer count becomes an integer (`review_rounds = 1`)
and the toggles become booleans (`privacy_check = false`, `secrets_scan = true` —
the legacy `off` word reads as `false`). **Running with both homes live is REFUSED,
not resolved by precedence**, so land the conversion in one commit rather than
half-way.

What deliberately stays a file, each for its own reason: `docs/stack.ini`
(adopter-owned product toolchain, never under a kit-owned template), the
presence-as-semantics markers `docs/work/pause` and `docs/agents-enabled` (a key
cannot express deletion-as-an-act), and the generated cache `docs/gate`.

### `docs/id-watermark` becomes REQUIRED [since e36f5661]

A new one-line-per-space file records the highest id ever allocated in each space,
so that a deleted row's number is never handed out again — the live tree cannot
answer that, because `max(live) + 1` re-issues whatever was removed. `trace.py`'s
always-on integrity pass now refuses an **absent** mark rather than reading it as
"no id is taken", so a re-sync that copies the file but not your history goes red
on the first commit, naming every live id above the scaffold's marks.

**Do this once, immediately after the re-sync:**

```
python scripts/trace.py --bump-ids     # records your existing ids
git add docs/id-watermark && git commit -m "record the id watermark"
```

That is the whole migration: the marks rise to your live maxima and the check goes
quiet. Two cautions. **Never `--force` this file** — `bootstrap.py` exempts it
deliberately, because every other scaffold target is a template to fill or is
regenerable from the tree, while this one is the only record of ids that have been
*deleted*, and overwriting it frees them for silent re-use. And **commit it before
the second commit**: until the file is in git the "a mark only ever rises" rule has
no baseline and reports itself as skipped (it says so out loud rather than passing
quietly). Thereafter a new hand-authored id — the spine tiers have no minter — is a
finding until you re-run `--bump-ids`, which is the intended rhythm: allocate, then
record.

### The spine gains a sibling: `scripts/spine_carrier.py` [since 82d5b818]

The same rule as `trace_text.py` above, and a re-sync must copy it: `trace.py`,
`check_trajectory.py`, `check_docs.py`, `trunk_step.py` and (since the batch-2
entry below) `agent_route.py` import it, so a repo that picks up one and not the
other gets an `ImportError` on its first check. `scripts/migrate_carrier.py` ships
beside it. `bootstrap.py` copies all of them together; a hand-managed re-sync must
too.

*Why a shared module at all,* given the kit's own rule that each script stays an
independently-copyable drop-in: this one holds a **vocabulary** (the carrier key →
column-name map), not plumbing, and a divergence between copies of a vocabulary
does not fail loudly — the copy that has not learned a column returns a row with
that cell **missing**, which every consumer reads as "the cell is empty". Owner
ruling: "independently copyable" means **copyable with its declared siblings**,
which is what the kit already practised (`trace.py` + `trace_text.py`,
`gen_trajectory.py` + six `traj_*` modules) and had not written down.

### The spine's four registries become ONE TOML CARRIER [since bb69a622]

The biggest change the kit has shipped to an existing adoption, and it has a
converter (`scripts/migrate_carrier.py`, which arrived at `a9b6ced3`):
`stakeholder-needs.md` (prose tables) and the SR/LLR/TC CSVs become
`stakeholder-needs.toml` · `system-requirements.toml` ·
`low-level-requirements.toml` · `test-cases.toml`, id-keyed with the prefix
retained and the key bare — `[requirement.SR-137]` under the tier tables `need` ·
`requirement` · `design` · `test`.

**Run it, check it, then stage BOTH sides in the SAME commit:**

```
python scripts/migrate_carrier.py --root . --check   # converts in memory, writes nothing
python scripts/migrate_carrier.py --root .           # writes each .toml beside its source

# STAGE THE NEW FILES FIRST. They are untracked until you do, and the `git rm`
# below stages four deletions: commit without this line and you have deleted
# your registries. (If your scaffold left the shipped `-000` templates staged
# at these paths, this is also what replaces them with your converted rows.)
git add docs/requirements/stakeholder-needs.toml \
        docs/requirements/system-requirements.toml \
        docs/requirements/low-level-requirements.toml \
        docs/test/test-cases.toml

git rm docs/requirements/stakeholder-needs.md \
       docs/requirements/system-requirements.csv \
       docs/requirements/low-level-requirements.csv \
       docs/test/test-cases.csv

git status --short          # expect four A/M and four D — nothing else
```

`--check` converts and re-reads what it emitted, cell for cell, and exits 1 naming
the registry, row id and field for anything that did not survive; the write path
refuses a lossy conversion too. **Both homes at once is REFUSED, not resolved by
precedence** — the readers raise rather than pick — so the delete belongs in the
conversion commit, not a follow-up.

*What you gain, and it is not tidiness.* Three integrity rules stop being code and
become properties of the parse: a **duplicate id** is a decode error (the id is the
table key, and TOML forbids declaring one twice); a **ref list** is a typed array,
retiring the split-on-whitespace rule that read `SN-001 and SN-002` as citing an
orphan called `and`; an **empty cell** is an *absent key*, so "unset" and "set to
empty" stop being the same value. On the need tier, draft-ness becomes a field
(`kind = "draft"`) instead of "appears under a heading containing the word draft" —
a rule a passing prose mention of an id could trip, silently un-ratifying a need.

*Three things to know before you run it.*

1. **The template's `-000` row is now your schema.** TOML has no header line, so
   the shipped example row is the only place the column vocabulary is written
   down. Keep it until you have real rows to read the key names off.
2. **Prose around the tables is not a row, and the converter does not carry it.**
   If your `stakeholder-needs.md` holds guidance, a vision link, or a non-goals
   section, move it into `#` comments yourself — comments survive every tool that
   edits these files, because the one writer that does (`intake`'s `Modified` →
   `Verified` flip) rewrites a single line rather than re-serializing.
3. **Your own scripts may read these paths.** Anything of yours that opens
   `system-requirements.csv` by name gets a `FileNotFoundError` (loud, fine) — but
   anything that CSV-parses the new file gets zero rows, silently. Read through
   `spine_carrier.load(path, id_col)`, which resolves whichever carrier is live and
   hands rows back under today's column names.

The legacy carriers stay readable for now: every kit reader resolves TOML first and
falls back, so a repo that has not migrated keeps working. That fallback is
**deliberate dead weight with an expiry** and will be dropped once no supported
baseline predates the migration — `migrate_carrier.py` does NOT share that
expiry: it is the standing conversion path a repo re-syncing onto a newer kit
still needs, so it stays live after the fallback goes.

### Carrier batch 2: `open-items` and `agents` move too [since 955cddec]

`migrate_carrier.py` converts `docs/requirements/open-items.csv` and
`docs/agents.csv` alongside the spine, so there is nothing extra to run — but there
are two things to delete and one to check:

```
git rm docs/requirements/open-items.csv docs/agents.csv
python scripts/agent_route.py --list      # the pool must still resolve
python scripts/gen_open_items.py          # regenerate the owner surface
```

- **Comments survive, and one of them is executable.** TOML's comment is the same
  `#` line the CSV convention used, so the converter carries every one across
  byte-for-byte and *in place*. That matters most for the
  `# tag-rank: ga>preview>beta>exp` line in `agents.csv`, which
  `agent_route.load_tag_rank` **parses** — dropped, it would silently reset the
  maturity vocabulary that resolves a version-less enable-list token.
- **A model id containing a `.` must be QUOTED** — `[agent."OPENAI-GPT-5.2"]`.
  Written bare it is still valid TOML, declaring a table called `5` under a row
  called `OPENAI-GPT-`, so the file parses and the model row is simply gone. The
  converter quotes what needs it; a HAND edit is where this bites, and
  `spine_carrier` refuses such a row at load rather than reading it.
- **Your `docs/open-items.html` must be regenerated**, and any prose linking the
  old paths retargeted — `check_docs` reports those as broken links.

`interfaces.csv` and `components.csv` are deliberately NOT in this batch: they move
with the schema rulings that change what their rows *are*, so converting them first
would mean converting them twice.

### The six check-enablement toggles fold into `[checks]` [since 6562239f]

`docs/trajectory-check`, `docs/interfaces-check`, `docs/components-check`,
`docs/subagent-gate`, `docs/live-status` and `docs/okf-export` become the
`[checks]` section of `docs/process.toml`. `bootstrap.py --migrate-config` converts
and deletes each one, and every checker keeps reading its old file for the same
migration window — so an un-converted adoption is not broken, only un-migrated. The
independently copyable checkers each pay for it with their own small local TOML
reader, which is the cost the ruling weighed and accepted.

### `scripts/check_dupes.py` is REMOVED from the kit [since 704ffd0d]

The duplicate-code lint and the fingerprinted census file it read
(`docs/dupes-allow`) were torn down by owner ruling: over its life it caught
duplication once, at the one-time triage, and never again; it is structurally blind
to a *diverged* copy, which is the case that actually hurts (an edited copy is no
longer an identical token block, so the tool goes quiet exactly when the
duplication becomes dangerous); and 93% of its census lines were registering
deliberate, accepted idioms rather than restraining anything.

**A re-sync will delete the script**, because the re-sync overwrites kit-owned
files and `check_dupes.py` is no longer among them. **Your census file is YOURS** —
it lives under `docs/`, was never kit-owned, and the re-sync will not touch it.
Keeping the check is a legitimate choice: nothing about the ruling says the tool
cannot pay for itself in a repo with different duplication pressure. If you keep
it, pin the last shipped copy in your own tree
(`git show <recorded-kit-commit>:project-trajectory/scripts/check_dupes.py`) and
keep your `[step:dupes]` section pointing at it. If you drop it, delete three
things together or the harness reds: the `[step:dupes]` section in
`docs/stack.ini`, its `docs/dupes-allow = dupes` row in that file's `[generated]`
section, and any spine chain you traced the check with — under the kit's
supersession rule those rows are **deleted**, not marked, with the act recorded in
your log (the ids stay spent).

**What the kit offers instead**, and it is deliberately narrower: duplicated
*policy* — two modules each deciding what "Draft" means, or which methods are
exempt — needs a behavioural test that imports both and asserts they agree by
VALUE. Duplicated *plumbing* is accepted without a bound.

### Carrier batch 3 — `interfaces.csv` + `components.csv` to TOML; the IF tier changes SHAPE [since 2eb1c0c8]

The last two registries join the TOML carrier (`[interface.IF-###]` and
`[component.CMP-###]` tables), held back deliberately until the rulings that
change what their rows *are* landed, so each converts once. Same command
family as the earlier batches (`python scripts/migrate_carrier.py --check`,
then without `--check`, then `git rm` the CSV — a repo carrying BOTH carriers
is a hard refusal). **The IF tier also changes shape — read before running:**

- **`Status` RETIRES.** It was never one of the fields process.md §8 declared,
  nothing validated it, and it overlapped `Stability` — `Stable` appeared in
  both columns of one row meaning different things. `Stability`
  (`Experimental` · `Stable` · `Deprecated`) is now the row's one maturity
  field. Map your values onto it before converting; a surviving
  `status = ...` key is a column nothing reads.
- **`Signal` is NEW and required**: `discrete` (a finite enumerable alphabet)
  or `variable` (unbounded content). If both cross, the row is `variable`.
- **`Rationale` is NEW and optional** — the home for the *why* that used to
  have nowhere in the row to go except `Contract`.
- **A warn-first schema tier arrives with them** (`trace.py`): required
  fields, those closed vocabularies, `CMP.State`, four negative rules on
  `Contract` (no work-item id, no decision citation, no rationale connective,
  a 500-character ceiling), and an advisory classifying every endpoint that
  is not an arch-map module. All ADVISORY — none of it changes an exit code
  at any gate — so an unmigrated repo goes noisy, never red.

### The `G*` gate tags retire for the eight-rung stage ladder [since 08c985cb]

**The biggest vocabulary change the kit has shipped, and it reaches your own
files.** `G0`/`G1`/`G2`/`G3`/`G-Release`/`G-Final` are gone as tags. In their
place:

- **Eight stage rungs** — `DevStg-Needs` · `Boundary` · `Reqs` · `Arch` ·
  `LLReqs` · `Tests` · `Impl` · `Release`. A repo is **IN** a stage. The label is
  the identifier; the position is DERIVED (`stage-ord=`/`stage-of=` on the basis
  line), so an inserted rung re-numbers everything and moves no citation.
- **Three bars** — `DevStg-Reqs` · `DevStg-Tests` · `DevStg-Impl`, each named
  for the top rung it certifies (Needs…Reqs, Arch…Tests, Impl…Release). You
  **CLEAR** a bar. `DevStg-Below` is an internal sentinel, not a bar.

**The word "gate" survives** wherever it means a check that can fail — the
`docs/gate` path, `derive_gate.py`, `check.py --gate`, "the freshness gate". Only
the TAGS retired. Do **not** run a blanket find-replace on the word; the
conversion is tag-scoped, and `scripts/check_vocab.py` (new, shipped) tells you
which of your own lines still carry a tag.

**Nothing breaks on day one.** Every reader that could receive a retired tag
translates it: `check.py --gate G2` runs `DevStg-Tests` and warns once;
`docs/stack.ini` `gates = G2 G3` translates silently; a WI's `bar: G3`
translates silently. So your pipeline stays green through the re-sync and you
convert at your own pace.

**The recipe — six moves, in this order:**

1. **REGENERATE `docs/gate`. This OVERRIDES §1's preserve-classes rule and
   ADOPTING §6's "preserve always" classification for that one file.** The cache
   is *field*-compatible but not *value*-compatible: your committed file carries
   `G1` on its value line and `computed=G0 … stage=4` in its basis, and `stage=4`
   means something DIFFERENT under the eight-rung ladder than it did under the
   six-integer one. Run `python scripts/derive_gate.py` once and commit the
   result. There is **no compat shim** — `--check` reports the old cache STALE on
   the first recompute, deliberately, because a reader that accepted both
   vocabularies is how the retired tags grow back. The failure direction is safe:
   a stale cache makes the stage unreadable, and an unreadable stage is treated
   as **human-held**, so the one state it can produce is *more* human
   involvement.
2. **Re-apply your `docs/process.toml` dials.** `human_ratification_through`
   keeps its 0–4 meaning — it was **mapped** onto the ladder, not re-keyed — so
   your declared value still means what it meant. Confirm it survived the
   re-sync; every pre-existing answer for the four spine tiers is unchanged.
3. **Hand-check anything of yours that passes `--gate` LITERALLY** — your own
   git hooks, CI workflow steps, Makefile targets, editor tasks. They keep
   working via the alias, but each will print a deprecation line every run until
   you update it. This is the one class the re-sync cannot fix for you.
4. **Convert your own WI rows' `Bar` values** and your `docs/stack.ini`
   `[step:*] gates =` keys to the new spelling. Both translate on read, so this
   is cleanup, not a break — but `check_vocab.py` will name each line.
5. **Your own log sign-offs stay VERBATIM.** The attestation carve-out applies to
   adopters too: a row recording a named human certifying `G1` recorded exactly
   that, and re-wording it makes the record claim something was signed that was
   not. Add a one-line header note naming the retired vocabulary instead —
   `check_vocab.py` already exempts `docs/log.md`, `docs/ratify/`,
   `docs/archive/` and the closed-WI specs. **Do rename the heading**
   `## Gate Sign-offs` → `## Sittings` (it is code-pinned in
   `trunk_step.RESERVED_HEADINGS`); the rows underneath do not change, and each
   new row names the **rung range** it certifies.
6. **`--sync` any materialized per-agent skills** — `gate-advance` is a full
   rewrite onto the ladder, and `registry-hygiene` / `session-protocol` took
   passes. `python scripts/bootstrap.py --dest . --sync`.

**Then run `python scripts/check_vocab.py --root .`** and work the list. It is
**warn-first** at the requirements bar and promotes to ERROR from `DevStg-Tests`
on, so a repo mid-conversion sees every site without being blocked.

**Also converted, for reference:** the `[phase]-[g1|g2]` WI-title archetype
becomes `[phase]-[reqs|tests]` for NEW titles — your committed anchors keep their
spelling and still parse forever (a title is a citation).

### The hats layer — a declared-perspectives roster the planner briefs read [since e0112f8f]

A new shipped registry plus its reader: `registries/hats.template.toml`
scaffolds to `docs/requirements/hats.toml` — one `[hat.NAME]` per expert
perspective, three required keys (`applies_when`, a closed evaluable
condition; `asks`, the question that lands in the brief; `listens_for`, the
failure class it catches), and it ships with **content**, because an empty
roster is a form with nothing behind it. `scripts/hats.py` reads and audits
it; `scripts/plan_briefs.py` injects each applicable hat's question into the
dual-plan **planner** brief, which is what replaced the standing edge-case
checklist tier (the SN-template entry further down). To adopt: copy
`hats.template.toml` in, take `scripts/hats.py` + the current
`plan_briefs.py` as one set, then **edit the roster** — cut the hats that do
not earn their place and rewrite every `applies_when` against your
vocabulary; a roster inherited unread is ceremony. The file is seeded once
and then **preserved** (owner text, the §2.2 "Preserve always" class), so
your edits survive later re-syncs. Opt-out: delete the file — composers
proceed without hats; a file that exists and does not parse refuses loudly.
The SN registry later gains an optional **`tags`** key feeding the same
`applies_when` grammar (`tags contains "…"`): `hats.context_from_need` reads
it, so a hat whose charter subject is a need's own subject can see that
need. Untagged needs stay normal, and nothing gates on a hat.

### The depth-0 FRAME registry; IF `Stability` → `Approval`; rung 1 re-keys [since 0ff33a95]

Four migrations in one commit, and the third one **changes what your reported
stage means** — read that item before re-syncing scripts.

- **NEW: `docs/requirements/external.toml`**, scaffolded by `bootstrap.py` from
  `registries/external.template.toml`. It holds your **depth-0 frame** in three
  tiers on one path: `[entity.EXT-###]` (who is outside), `[boundary.B-##]`
  (what crosses your system boundary), `[relationship.REL-###]` (external-to-
  external flows you are not a party to). This is the tier your **system
  requirements form around**. An `IF-###` row is a concrete interface
  definition and ties BACK to a crossing only when it realizes one.
- **RUNG 1's APPLIES-WHEN MOVED, and your stage may RISE silently.**
  `derive_gate.boundary_incomplete` used to read `interfaces.toml` and cap you
  at `DevStg-Boundary` while any IF row read `Stability = Experimental`. It now
  reads `external.toml`'s crossing `Approval`. **A repo that carries
  `interfaces.toml` and no `external.toml` therefore SKIPS rung 1 entirely**
  where it was previously held. That is the correction — internal seam
  definitions never typed a boundary — but it is not a no-op: if you want the
  rung, scaffold `external.toml` and declare your crossings. If you never
  declared a boundary, the rung is now correctly free.
- **IF `Stability` RETIRES for `Approval`** (`draft` · `approved`), the tier's
  one maturity field, shared with the new boundary tier. Map your values before
  or during the re-sync — `Experimental` → `draft` is the direct reading;
  `Stable`/`Deprecated` → `approved` **only if you mean it**, because `Stable`
  was a MATURITY claim (the contract has settled) and `approved` is a
  RATIFICATION one. The kit's own registry mapped all 113 rows to `draft`
  rather than manufacture approvals nobody signed. A surviving `stability = ...`
  key is a column nothing reads.
- **NEW optional IF keys:** `interface_from_external` / `interface_to_external`,
  the directional tie-back naming a `B-##` crossing. Present ONLY on a row that
  realizes one; a row with neither is an internal seam.
- **NEW optional SR key: `boundary_refs`** (`Boundary-Refs`), the crossing(s) a
  requirement states an observable AT. An id that does not resolve is a HARD
  finding under `--strict`; leaving the cell blank is a warn-first coverage
  count, so an unmigrated spine goes noisy, never red.
- **Two checks changed arming, both warn-first, neither newly red.** The
  seam-TC citation rule now arms on every IF row instead of on a maturity
  value, so your uncited-seam count may RISE. WI-191's "a cited `Experimental`
  seam needs a rationale" arm is GONE — its input no longer exists, and
  re-keying it onto `draft` would have armed it on every row.

### The SR tier's `SupersededBy` column RETIRES; supersession is deletion [since fd26a966]

The optional SR `superseded_by` key, its ~110-line `trace.py` validator
(semicolon-list shape, unknown target, self-link, cycle, the LLR re-grounding
error above) and its ratified-cell classification are all GONE, on the ruling
that a supersession row is history wearing a row id: **a registry states what
IS; git and the log are the history.** A retired row is *deleted*, its id spent
forever (the id watermark's committed mark keeps the headroom), and one log
entry is the forwarding home naming the replacement rows.

- **If your SR registry carries `superseded_by` keys:** the carrier now REFUSES
  the key on an SR row (it is no longer in the tier's declared key set). Before
  re-syncing scripts, delete each tombstone row, re-point any citing IF rows at
  the replacement rows, re-check `sn_refs` coverage against the replacements,
  and record one forwarding log entry for the batch.
- **TC rows whose `verifies` cite only superseded SRs** must retire with them —
  a test case verifying nothing is not evidence.
- The **CMP registry's own `PartOf`/`SupersededBy`** is a different rule and is
  unchanged.

### `SR.Area` retires for a closed `Aspect` vocabulary [since 9861e957]

The free-text `Area` column is GONE from the SR tier, replaced by `Aspect` —
a **closed** six-value vocabulary: `process`, `trajectory`, `unattended-loop`,
`connectivity`, `perf`, `portability`.

**Why it is not a rename, and what that costs you.** The measurement behind
the ruling: of the kit's own 31 `Area` values, **25 were a component by
another name** — derivable from your decomposition and therefore redundant —
while only **6 spanned components**, which is what an aspect IS: a
cross-cutting concern no partition can express. So the conversion **DROPS**
the derivable values rather than remapping them. In the kit's own registry
that took 63 tagged rows down to 21; the other 42 now carry no aspect at all,
and that is the intended end state, not data loss.

- **Migrating:** for each SR, keep the value only if it names a cross-cutting
  concern that maps to one of the six; otherwise delete the cell. Do not
  invent a seventh value to preserve a tag — if your value names a component,
  your component registry already says it.
- **A blank cell is NORMAL and never a finding.** A requirement that is not
  cross-cutting carries no aspect. (In the kit's own spine, `portability`'s
  three rows have no owning module at all, and that was ruled *not* a defect.)
- **A non-empty out-of-vocabulary value IS a `--strict-schema` finding**
  naming the row and the allowed set — reported at the schema tier, gating
  under `--strict`, exactly like the `Verification`/`Tier` vocabularies.
- **A surviving `area = ...` key is a column nothing reads.** The carrier's
  SR-tier key set declares `aspect`; `Area` is absent from the traced-cell
  table, the OKF fact row, and `trace.py`'s per-tag count (now "SRs by
  aspect").
- Nothing else moves: `Aspect` stays REPORT-ONLY for counts, and no gate reads
  the distribution.

### `docs/architecture.md` RETIRES — the architecture derives into the dashboard [since c7adf7dc]

The markdown way-station between the registries and the dashboard is gone:
the module map, import graph and seams are now read STRAIGHT from your source
tree and registries, and `PROJECT_STATE.html`'s "How (SW architecture)" tab is
the one rendered home. The authored narrative — the **Runtime flows** the
DevStg-Tests bar requires — moves to its own doc and the dashboard embeds it.

- **NEW: `docs/runtime-flows.md`** (scaffolded from `RUNTIME_FLOWS.template.md`).
  **MOVE your authored "Runtime flows" section there** (heading included) —
  `check_flows.py`'s default `--doc` now points at it, and the obligation is
  unchanged: required from DevStg-Tests, every diagram citing real SR/LLR ids.
  A repo that skips this move fails the `design-flows` step with "doc missing".
- **`ARCHITECTURE.template.md` RETIRES; `docs/architecture.md` leaves `bootstrap.py`'s
  MAPPING** — a fresh scaffold no longer receives it. Your existing copy is
  YOURS: after moving the flows out, keep whatever hand-written overview you
  value (it is no longer checked) or delete the file.
- **The `arch-map` harness step RETIRES** (`check.py`, the pre-commit hook's
  batched floor, `trunk_step.py --regen`): there is no committed block left to
  drift. Remove the `docs/architecture.md = archmap | ...` row from your
  `docs/stack.ini` `[generated]` section. `[arch-map] mode` KEEPS its meaning
  — `files` now tells the AST-inventory readers (check_trajectory's coverage
  rules, the dashboard, `check_doc_refs`'s `sym:` tier) there is no Python
  source, keeping those layers dormant rather than vacuously green.
- **`check_doc_refs.py --arch` RETIRES**: the `sym:` oracle scans the source
  AST under `[paths] src` directly. If you passed `--arch`, drop the flag.
- **`gen_arch_map.py` stays shipped** as the AST walk the readers import
  (`scan_inventory`) and as the opt-in CLI for splicing the map into
  `AGENTS.md`/`CLAUDE.md` marker blocks (`--doc`); a files-mode committed map,
  if you relied on one, is yours to keep wiring manually.
- **Behavior sharpened by the live inventory:** the knowledge⇒component
  containment finding now fires on a module the moment it exists on disk
  (the old committed-map staleness window is gone) and names the uncontained
  modules; `gen_okf`'s process-guide for `docs/architecture.md` is replaced by
  a `runtime-flows` guide, so your `docs/okf/` bundle regenerates once.

### `docs/handbacks/*` in `orphans-allow` [since bd0e739a]

**Applies to every adoption that scaffolded `docs/orphans-allow` before this
commit — which is all of them.** The partial-close contract shipped without its
navigability entry, and the defect is invisible until the first lane closes
early: `handback.close_partial` writes an immutable per-close report under
`docs/handbacks/`, nothing links to it *by design* (its path is the close
event's identity, and the disposition row intake mints is what makes it
reachable as work), so `check_docs` reports `orphan doc (no path from an entry
root)` and the full suite goes red on a repo that did nothing wrong.

Found by dogfooding: the kit's own first partial close, 2026-08-15.

Migration is one line appended to `docs/orphans-allow`:

```
docs/handbacks/*
```

Do it **before** your first early close, not after — the failure arrives
attached to an unrelated merge, which is the worst moment to diagnose it. If
your `orphans-allow` is unmodified from the template you can simply overwrite it
with the kit's copy.

### The interface tier gains an owner, and `sr_refs` becomes `req_refs` [since a61de32d]

**One entry for the whole 2026-08-15 interface rework**, because the pieces only
make sense together: the tier now says who is answerable for a seam, and stops
making `Direction` pretend to. Owner rulings of 2026-08-15 (Q1–Q3). The anchor is
the commit the LAST schema piece landed in; the change spans `f4343653..a61de32d`,
and taking only part of that range leaves the registry and the checkers disagreeing. Applies to
every adoption carrying a populated `docs/requirements/interfaces.toml`; a repo
whose registry is still the `-000` placeholder can skip to step 4 and just
overwrite the template.

Everything below is **warn-first at every gate** — no exit code changes, so you
can land it in pieces. Nothing was deleted: `direction`, `this_project` and
`counterpart` all stay, and so do your `Consumes` rows.

1. **Rename `sr_refs` → `req_refs`** in every interface row (`Req-Refs` if you
   are still on the CSV carrier). Mechanical, one find-replace *scoped to the
   interfaces registry* — the design tier's `sr_refs` is a different column and
   must not move. The two meant different things under one name: an LLR's names
   its **parent** requirement, an interface's names the requirements that
   **realize or rely on** the seam.

2. **Add `owner` to every row**, one `SR-###` **or** one design-tier `LLR-###`
   (both are legitimate; exactly one). Seed it mechanically: where `req_refs`
   holds a single id, that id is the owner. Where it holds several, someone has
   to choose the row whose obligation answers for the seam's **contract** — that
   is a judgement, so make the picks in one pass and write down why, or the
   cells are unauditable. The kit's own 115 rows went 94 mechanical, 21 by
   judgement.

3. **Mark external endpoints.** `this_project` / `counterpart` are now validated
   against your tree, and one that resolves to no module, file or directory is
   named individually. Prefix the ones that are deliberately outside it:
   `counterpart = "external:downstream adopter"`. Run
   `python scripts/trace.py` and fix what it names — expect some of them to be
   genuine rot (spine files that migrated carrier and left the seam row behind
   was the kit's own case, 8 rows). A path already listed in
   `docs/declared-absences` counts as resolved and needs no marker.

4. **Overwrite `registries/interfaces.template.toml` and
   `docs/interfaces.md`** from the kit, and take the new `trace.py`,
   `spine_carrier.py`, `migrate_carrier.py`, `plan_briefs.py` and
   `gen_release_checklist.py` as one set — `spine_carrier` and `migrate_carrier`
   are pinned as inverses by a test, so a partial take fails loudly rather than
   silently dropping a cell.

**Optional, and only if you want it:** `carried_by = "IF-###"` lets a
constituent seam name the bundle that carries it, so one contract can be
declared at both grains. Leave the cell absent and nothing changes. If you use
it, the graph must resolve and be acyclic, and depth past 2 warns.

**One reading change to expect:** `Direction` no longer claims ownership. The
shipped rule was *"only the `Provides` side may close the owner's final read"*;
it is now the `Owner` cell's side. `Provides`/`Consumes` still mean what your
`Consumes` rows have always been doing — declaring that a cross-component edge
is intended and that this row discharges it — and the cross-component seam check
still reads them, unchanged.

### The `Status` vocabulary closes, and the attestation baseline moves out of git and onto disk [since 1d45730e]

*(Anchored at the first commit of the D-9 mechanical prefix; the mechanism lands across the three commits that follow it. Take them as one set.)*

**`Status` is now a CLOSED vocabulary on the spine — `{Draft, Planned, Modified, Verified}` for SR, LLR and TC — and an out-of-vocabulary value is an INTEGRITY finding**, which means it reds `trace.py --strict-integrity` and the pre-commit hook at every gate, not just at DevStg-Impl. This is the one entry here that can break a repo on the re-sync itself. If your LLR or TC rows carry maturity words of your own (`Implemented`, `In-Review`, …) — which the kit's own prose invited until now — map them onto the four before you take this. `Planned` is the closest fit for "ratified, not yet Verified"; the derived gate reads LLR/TC status only for `Draft`, so the mapping does not move your bar. Why the closure: the `Status` ladder D-9 is heading for renames these values, and a retired word that no predicate recognizes vanishes SILENTLY from the re-attest brief — an open vocabulary has no way to say "this row was left behind".

**What an approval records changed, and one CLI surface was deleted.** Until
now, "has this attested row changed since a human blessed it?" was answered by
walking git for the newest commit at which the row read `Verified`. That walk is
correct only while every amendment flips its row's `Status` in the same commit —
and the `Status` ladder D-9 is heading for deletes the flip, at which point the
newest-approved revision is HEAD and the diff is empty **by construction**: the
brief returns a clean bill forever, at exit 0, on exactly the rows a sitting
exists to judge.

So the baseline is now a **copy on disk**. What you receive:

- **`scripts/baseline_snapshot.py`** (new, and a sibling import of both
  `intake.py` and `trace.py` — take it with them or neither runs). It mirrors
  the four spine registries plus `interfaces.toml`, `external.toml` and
  `components.toml` into `docs/archive/last_approved/`, byte for byte, with
  repo-relative paths preserved.
- **`intake.py snapshot [--seed]`** — the human path. At a ratification sitting:
  edit the `Status` cells, run it, commit both together. The mechanical
  adjudication flip copies in the same act.
- **`docs/archive/last_approved/README.md`** in the scaffold (`bootstrap.py`
  MAPPING). That is the ONLY thing a fresh scaffold receives: an empty snapshot
  is the honest state for a repo that has approved nothing yet.
- **A new warn** — `check_trajectory`'s staged pass reports any commit that
  leaves a snapshot file differing from its live counterpart.

**Nothing happens to your repo until you seed it.** Every reader is vacuous
while `docs/archive/last_approved/` does not exist, so a re-sync alone changes no
output and fails no gate. When you are ready, run `intake.py snapshot --seed`
**in the reviewed commit that blesses your spine, after every pending row has
been ruled** — seeding earlier records a blessing of text nobody read. That is
the only moment the directory is created; the flag is unreachable from every
loop module, hook and `check.py`, and a test pins it so.

**DELETED, and you must stop passing it:** `trace.py --ratify modified --since
<rev>` and `gen_open_items.py --since <rev>`, plus the
`<!-- attestation-baseline: … -->` stamp the generated view carried. They
existed to override or reproduce a git-derived baseline that a regeneration
could move. A snapshot cannot sit after the amendment it precedes and is
identical on every machine and in CI, so there is nothing to override and
nothing to reproduce. A script or CI job passing `--since` now fails on an
unrecognized argument — which is the loud direction.

**One behaviour change worth expecting.** `trace.py --ratify <scope>` now
REFUSES a scope that matches no SR instead of emitting an empty brief at exit 0.
If you have a job that ratifies a phase tag which no longer exists, it will
start failing; that is the point, because the empty brief it used to produce
read as *"there is nothing to ratify"* to the human about to sign it.

### The `Status` ladder RENAME: `Draft`→`Drafted`, `Planned`/`Verified`→`Approved` [since 3771c003]

The successor to the entry above, and the one that moves **cells**, not just
machinery. The enum narrows from four values to three — `{Drafted, Approved,
Modified}` — and it is enforced on the always-on `--strict-integrity` floor, so
an unmigrated cell is a hard finding on your very next commit, not a silent
inertness. **Order matters; each step below is a separate failure if skipped.**

1. **The value map, applied to every SR/LLR/TC `status` cell.** `Draft` →
   `Drafted`; `Verified` → `Approved`; **`Planned` → `Approved`**. The third is
   a FOLD, not a rename: `Planned` (text ratified, evidence pending) and
   `Verified` (text ratified, evidence established) named one rung once the
   vocabulary stopped making a pass claim, so they collapse. Matching stays
   case-insensitive, so casing in your cells is not the issue — spelling is.
2. **The off-spine approval cells:** `approval = "draft"` → `"drafted"` in
   `docs/requirements/interfaces.toml` and `external.toml` (the `approved`
   spelling is unchanged). One word, one meaning, across every registry.
3. **The predicate renames, if you patched or imported them:** `is_draft` →
   `is_drafted` (in `trace_text.py`, re-exported by `trace.py`), `is_verified` →
   `is_approved` (in `trace.py` AND `derive_gate.py` — they are F5 duplicates
   and both move). **`is_planned` is DELETED, not re-keyed**; every site that
   read it now reads one of the three live predicates.
4. **The templates.** Overwrite `registries/*.template.toml`: the SR and TC
   examples now ship `status = "Drafted"` and the LLR example `status =
   "Approved"`. A scaffold created before this change still ships the retired
   words in its `-000` rows; those rows are placeholder-exempt from the
   integrity rule, so nothing fails — but leaving them means your template
   teaches a vocabulary the checker refuses.
5. **THE ONE THAT BITES SILENTLY — the `# basis:` line format.**
   `derive_gate.py` now emits `drafted=N` where it emitted `drafts=N`, and it no
   longer emits `planned=N` at all. Any consumer that parses that line by regex
   must move in the same commit or it goes BLIND rather than red — the kit's own
   `check._BASIS_RE` did exactly this once and twelve gate steps stopped running
   for twelve commits before anyone noticed. If you have local tooling reading
   `docs/gate`'s basis line, grep it for `drafts=` and `planned=` first.
   Regenerating `docs/gate` (`python scripts/derive_gate.py`) is required
   regardless: `--check` compares the line whole.

**If you carry a WIDER LLR/TC vocabulary** (`Implemented`, `In-Review`, …), this
is the change that ends it. The kit used to document `Status` as open with three
magic values and everything else "legal, unvalidated, and mechanically inert";
that promise is retired, and prose in `process.md` §4,
`process-options.md` and `docs/registry-machinery-reference.md` now says so. Map
your extra values onto the three before re-syncing — anything below approval is
`Drafted`, anything blessed is `Approved` — or every such row becomes an
integrity finding.

**A behaviour change to expect on the derived gate.** `sr_bar` now ceilings at
`DevStg-Tests`: `DevStg-Impl` is unreachable from a Status cell, and the
rendered bar says so — `DevStg-Tests (Release: pending harness driver)`. This is
deliberate and it is what keeps the `Planned`→`Approved` fold from RAISING your
derived gate for rows that never passed anything. `check.py --gate
DevStg-Impl` stays explicitly invocable at any time.

### SN template: the `edge` row kind retires; `tags` documented [since 166b406d]

*(Anchored at the shipped-docs audit commit; the change lands in the
commit(s) that follow it.)* The SN template's `kind` vocabulary narrows to
`core` | `draft`: the `edge` row kind — its `lifecycle`/`scenario`/`expected`
fields and the standing edge-case checklist — leaves the template,
`EXAMPLE.md` and `ADOPTING.md`. Edge-case coverage is the hats mechanism's
job now (the entry above): write a failure-mode expectation as an ordinary
need, and each applicable hat's question is put to every decomposition —
regenerated per need rather than maintained as a checklist tier. Nothing
breaks on the re-sync itself: no reader enforces a closed `kind` vocabulary,
so existing `edge` rows keep parsing — fold them into ordinary needs at your
own pace. The template's example row also now documents the optional `tags`
key (the hats entry above).

### The frame tiers join the id watermark: `B`/`EXT`/`REL` [since d28e1ccb]

*(Anchored at the preceding desk commit; the change lands in the commit(s)
that follow it.)* The three id spaces of `docs/requirements/external.toml` —
`[boundary.B-##]`, `[entity.EXT-###]`, `[relationship.REL-###]` — become
watermark spaces: `trace.py` now sweeps the frame for live ids and requires a
mark per space, so a deleted crossing's number can no longer be silently
re-minted (the frame is the one tier that had no guard, and this kit's own
history spent three ids that way). **What you will see on re-sync:** your
committed `docs/id-watermark` predates the three spaces, so the always-on
integrity pass goes red with `id watermark declares no mark for B` (and
`EXT`, `REL`). **The fix is one command** — the same one the file's header
names:

```
python scripts/trace.py --bump-ids    # adds the missing spaces; existing marks are kept, never lowered
```

One caution, and it is the mechanism's whole point: `--bump-ids` derives from
**live** rows, so if your repo ever deleted a `B`/`EXT`/`REL` row *before*
this change guarded those spaces, raise the fresh mark by hand to the highest
id you ever allocated before committing — a space's **first** committed mark
is a seed and may legally stand above `max(live)`; from the next commit on it
is held monotone like every other mark. (This kit seeded `B = 7` over a live
max of 5 for exactly that reason: `B-06`/`B-07` were cut before the guard
existed.)

---

### The SN row: one `status` field replaces `kind` + `attestation` + `amended` [since 810f1c01]

*(Anchored at the ruling commit that dispatched the migration; the change lands
in the commits that follow it.)* The need tier now encodes maturity in **one**
field, spelled and valued exactly as the other three spine tiers already spell
it — `status ∈ Drafted | Approved | Modified`. It encoded the same thing in
three fields before, one of which carried history.

1. **`kind` is DELETED, not renamed.** It conflated two unrelated questions:
   `core`/`draft` was maturity, `edge` was a row TYPE. The `edge` half retired
   separately (the entry above); the maturity half becomes `status`. Map
   `kind = "core"` → `status = "Approved"` and `kind = "draft"` →
   `status = "Drafted"` on every row, then drop the key.
2. **`attestation` and `amended` are DELETED with no successor field.**
   `attestation = "pending"` meant amended-and-unsigned, which is what the
   spine's `Modified` already says — so those rows become
   `status = "Modified"`. `amended = "<date>"` was PROVENANCE in a registry
   whose job is living truth: git and `docs/archive/` already hold when a row
   changed, hold it for *every* row rather than the ones somebody remembered to
   mark, and cannot drift from it. If you added either field by copying the
   kit's own registry, delete both. **Nothing ever read them**, so nothing
   breaks when they go.
3. **The selector, if you patched or imported it.** Drafted-ness is
   `spine_carrier.is_draft_need` now — one home, reading `status` — where
   `draft_need_ids` and `check_docs`' Must/Should floor each tested
   `kind == "draft"` separately. A LEGACY markdown needs registry keeps working:
   the reader translates section-as-state into `status` at the parse boundary,
   so a draft-heading row still reads as drafted. **If you have local tooling
   selecting on `kind`, it goes silently wrong rather than red** — it will find
   no drafts, and the derived gate RISES. Grep for `kind` before you re-sync.
4. **The schema census is now enforced on this tier.** `SPINE_TIER_KEYS` gained
   an `SN-ID` entry (`status · tags · need · why · priority · acceptance`) and
   `test_dogfood_sync` compares template ↔ live ↔ schema for it. `tags` is
   OPTIONAL but DECLARED. If your needs template omits a key your live rows use,
   that now fails — which is the point: the kit's own template shipped without
   `tags` for exactly as long as nothing was comparing them.
5. **Overwrite `registries/stakeholder-needs.template.toml`.** Its maturity
   header block is rewritten around the one enum, and it now says outright not
   to add a second field for this axis.

### Off-spine registries: `approval`/`state` → `status`, and the components SPLIT [since 810f1c01]

*(Same anchor as the entry above; the two land in sequence.)* The three
off-spine registries stop spelling one axis three ways. **Field name and value
casing both move, so an unmigrated cell is a required-field finding AND an
out-of-vocabulary one.**

1. **`interfaces.toml`, `external.toml`: `approval` → `status`**, and the values
   go Title-case — `drafted` → `Drafted`, `approved` → `Approved`. Same words as
   the spine, same field name, so "what is un-approved right now?" stops needing
   a per-registry special case. `Founded` is **not applicable** to these tiers
   and never will be: it means settled AND demonstrated, and an approval says
   the crossing is agreed, not that it was demonstrated.
2. **`components.toml`: `state` → `status` PLUS a new optional `standing`.**
   This one is a split, not a rename, because `state` carried two axes:

   | `state` was | `status` | `standing` |
   |---|---|---|
   | `planned` | `Drafted` | *(omit)* |
   | `built` | `Approved` | *(omit)* |
   | `verified` | `Founded` | *(omit)* |
   | `has-gap` | `Drafted` | `has-gap` |
   | `deprecated` | `Approved` | `deprecated` |

   `standing ∈ active | has-gap | deprecated`, and **omitting it means
   `active`** — so a registry with no lifecycle facts writes no `standing` cells
   at all. `planned` and `verified` LEAVE the vocabulary rather than being
   renamed: they were the retired spine words `Planned`/`Verified` regenerated
   in lowercase, in another field, in another registry, meaning something else.
   CMP is the one off-spine tier that reaches `Founded`, because a demonstrated
   partition is a claim something actually computes (`arch_incomplete`, rung 3).
3. **The predicate and table renames, if you patched or imported them.**
   `derive_gate.CMP_MATURITY` is now the identity over the one enum
   (`drafted`/`approved`/`founded`, lower-cased keys — `_maturity` lower-cases
   before the lookup, so your Title-case cells resolve). `has-gap` and
   `deprecated` are **gone from it**: they are `standing` values now, and
   `standing` maps to no maturity because it is not one.
4. **THE ONE THAT BITES SILENTLY — a guard keyed on the old spelling.** If you
   copied the kit's `test_no_shipped_loop_module_WRITES_an_approval_cell`, its
   regex hunts `approval = "approved"`. After this rename that pattern matches
   nothing any registry writes, so the guard passes VACUOUSLY forever while the
   thing it forbids becomes possible. Re-key it to the live spelling **and** the
   retired ones in the same commit. The same applies to any local check keyed on
   `Approval` or `State` as a column name.
5. **Overwrite the three templates** (`interfaces`, `external`, `components`):
   each declares the new field, the Title-case vocabulary, and — for the two
   that cannot reach it — that `Founded` does not apply.

**What does NOT change: any row's meaning.** Every off-spine row in the kit sat
in its vocabulary's first state when this ran, so the migration re-spelled cells
without moving any of them. The kit verified that by asserting its `derive_gate`
basis line was **byte-identical** before and after. If your registries carry
approved or verified rows, you do not get that check for free — apply the value
map above deliberately, and re-run `derive_gate.py` to compare.

### `docs/work/README.md` — the registry's own location→status contract [since 712ff788]

**A new scaffolded file, and one corrected table.** `bootstrap.py` now maps
`work/README.template.md` → `docs/work/README.md`: the seven status directories
with their status words, and the rule an adopter otherwise has to reconstruct
from the loaders — **a terminal row STAYS in the registry**. `complete/`,
`cancelled/` and `partial/` rows are never moved out and never deleted, because
every reader rglobs the whole of `docs/work/` and a closed row is still a `needs`
predecessor, a `sr_refs` trace link and a dashboard count. So
**`docs/work/archive/` must never exist** — the folder retired at the six-state
flip (see "The six-state work-item model" above) and the README now says so where
the question gets asked. The archiving lifecycle belongs to the *other* artifact:
the spec-of-record under `docs/specs/`, which moves to `docs/archive/specs/` at
close under rule R-F.

**The corrected table.** `work/WI-000.template.md` shipped a six-row status table
that omitted `partial/` — the third terminal that arrived with SR-144's
partial-close contract and has been in `SPEC_STATUS_DIRS` and
`TERMINAL_STATUSES` since. An adopter reading only the shipped docs could not
learn the state exists. The row is added in both the template and its scaffolded
copy.

**Migration, for a repo that already scaffolded:** copy
`work/README.template.md` in as `docs/work/README.md`, and re-copy
`work/WI-000.template.md` over `docs/work/queued/WI-000-example.md` if yours is
unmodified. Both are pure documentation — no reader parses either — so there is
nothing to do beyond the copy, and skipping it costs you only the answer to a
question you will otherwise ask twice. Also confirm `docs/work/partial/` exists
(`.gitkeep`, like its sibling terminals); a repo scaffolded before the folder
joined `GITKEEP_DIRS` may be missing it, and `handback.close_partial` needs it.
`docs/work/*` is already an expected-live-orphan glob in `docs/orphans-allow`, so
the README needs no navigation link.

### The artifact-voice rule reaches the NEED tier — and you owe your own rows a sweep [since 3dd665fc]

**The rule changed shape, not just scope.** `docs/process.md` §3 used to say a
*requirement* cell names no concrete artifact without a recorded reason; it now
says a **need or requirement** cell does. At SN that lands squarely on the
`acceptance` cell: a need states the observable **condition**, never the
instrument that observes it. "`trace.py --strict` reports zero orphans" is a
stakeholder outcome welded to one script — it cannot survive the script being
re-carried, and the stakeholder the tier exists for cannot validate a claim about
a file they have never opened. "The strict traceability check reports zero
orphans" says the same thing and outlives every carrier.

**The detector now warns on both tiers.** `trace.py`'s "Artifact-naming
advisories" section is joined by "**Need artifact-naming advisories**", fed by
`trace_text.sn_artifact_advisories`. Both are **warn-only and stay warn-only** —
neither joins the exit code under any flag, so nothing you have gates today
starts failing. Three differences from the SR arm, all deliberate:

- It reads a **wider artifact vocabulary** (`.py .toml .ini .csv .html .yml
  .yaml .sh .cmd .ps1 .bat .json`), because a need's instruments are mostly not
  scripts — they are config files and generated pages. `.md` is **excluded**: a
  markdown name in a spine cell is rarely the instrument that observes the
  condition — it is a document under specification or a pointer to a home — so
  charging a waiver for it would train authors to ignore the warning. (A
  markdown name that IS a citation has a different problem: the next entry
  forbids it outright, waiver or none.)
- It reads **`acceptance` only**. Your `need` cells belong to
  `check_need_form.py`, which already reports internal paths and
  implementation-only identifiers there — one token, one reporting check.
- There is **no shared-artifact census** at SN. Two needs may honestly describe
  outcomes one file happens to serve without either of them deciding anything
  about it; only the SR tier's "one home per method" makes that a defect.

**What YOU do — run the same conformance sweep over your own rows.** Nothing
migrates this for you, and a repo that adopted the kit before this change almost
certainly has needs written in instrument voice (the kit's own registry had 13 of
27 acceptance cells naming a carrier when the rule landed). Take it row by row:

1. Run `python scripts/trace.py` and read the two artifact-naming sections as a
   worklist — the SN one and the SR one, since the SR arm has been warning since
   the re-tier campaign and older repos never cleared it. It is a worklist and
   **not a definition of done**: the detector reads a fixed extension list, so a
   cell that names its instrument in words that list cannot see reads clean —
   read your cells, and stop when *they* are right, not when the section goes
   quiet.
2. For each flagged cell ask the one question: **is the artifact the SUBJECT of
   this row, or the INSTRUMENT that happens to carry it?** An instrument gets
   rewritten to the condition it produces ("the documentation check fails on a
   broken link", not "`check_docs.py` fails on a broken link"). A subject stays.
3. **Where the name stays, record the reason as a waiver** — the same
   `recorded waiver: <reason>` marker the one-`shall` and SR artifact valves
   already use, written in the
   tier's **reason cell**: `Rationale` at SR, and **`why` at SN**, because the
   need schema carries no `Rationale` and `why` is the field that already answers
   "why is this row the way it is". The reason must be one a later reader can
   argue with; "accepted" is not a reason.
4. One thing needs **no** waiver and should not get one, or the token stops
   meaning anything: a **declared vocabulary** token (a dial name, a status
   word, a `--flag`), which is not a carrier. A **provenance** citation is not a
   carrier either, but do not waive it — **delete it**: the next entry
   ([since 4e9a5c8a]) bans a citation frame from every living spine cell,
   including the reason cell you would have written the waiver in.

**This is a wording sweep, not a re-decomposition.** Do not change what a row
means, do not touch `status`, and expect your amendment detectors to fire on
every cell you rewrite — that is correct, and those rows are what your next
review sitting reads. If your process holds the need tier for human
ratification, the sweep is a provisional act your sitting countersigns.

### NO provenance citation in a living registry cell — all four spine tiers, reason cells included [since 4e9a5c8a]

**What changed.** `process.md` §3's stand-alone rule used to say a spine row must
not carry a work-item id or a citation of the process doc, in the normative text
of `SR`/`LLR`/`TC`. It now covers **all four spine tiers** (`SN` joins) and, on
every one of them, the **reason cell** as loudly as the normative ones —
`Rationale`, and `why` at `SN`. The forbidden vocabulary is the whole citation
frame: work-item id, process-doc citation, ruling, sitting, review-round or
open-item reference, decision id, edit-history verb, date stamp.

**One permission is REPEALED, and it is the load-bearing half.** The rationale
bullet used to say a review, ruling or design-thread reference was *optional
context on top of a sentence that already stands alone*. It is not optional
context any more; it does not belong in the cell. The substance of the reasoning
stays — what breaks without the row, which alternative lost — and only the
citation frame goes. The detailed history belongs in `docs/log.md` and the
archive, which can hold it in full and cannot rot into the specification.

**Why, measured.** The permission read as a licence. On the kit's own registries
it produced `Rationale` cells that are mostly changelog — `REWORDED <date>
(<round code>, <hat>; <sitting> item 8 ruling): …` — ~300 tokens across ~150 live
rows, with the durable half buried in the middle of a frame no outside reader can
resolve. Every one of those cells is read by an adopter, an agent and a reviewer
with none of the history that would make the frame mean anything.

**Two new checks, both WARN-FIRST and never gating.** `trace.py` grows a
**Provenance-citation advisories** section (`provenance_advisories` over
`SN`/`SR`/`LLR`/`TC`, plus `if_note_advisories` over the IF tier's
`Notes`/`SignalNote`). The pre-existing gating rule — a work-item id or a
process-doc citation in an `SR`/`LLR`/`TC` normative cell under `--strict` —
**keeps its severity exactly**. Nothing that passed before fails now.

**What YOU do — read the findings as a worklist and rewrite each row.**

1. Run `python scripts/trace.py` and read the **Provenance-citation advisories**
   section. Every line names the tier, the row, the cell and the tokens. It is a
   worklist and **not a definition of done**: the detector matches a fixed token
   vocabulary, so a citation frame worded outside it reads clean — read your
   cells, and stop when *they* are right, not when the section goes quiet. (The
   kit's own sweep stopped at the quiet detector and left 33 framed cells behind;
   the next review round found them.)
2. For each one: **drop the citation frame, KEEP the reason.** Where the frame
   wrapped a real argument, restate the durable half as standing prose ("this
   states a structural property, not a throughput claim: no instrument here
   measures speedup"). Where the block has no forward-looking half at all, it was
   a changelog — delete it; git and the log already hold it.
3. **The failure to watch for is deleting the frame and the argument together**,
   leaving a bare assertion. That is the exact failure the rationale rule exists
   to prevent, and it gets likelier now that the frame is forbidden.
4. Move the account to `docs/log.md`. A row that names a *dead* id is worse than
   one that names none: it reads as authority and resolves to nothing.

**The open-question carve-out, and the allow file.** One class of cell must NOT
be swept: the frame that is the **only record of an unresolved tension** — a
contradiction between two rows, an obligation whose carrier is gone, a
provisional label nothing mechanical signs. Stripping those deletes the repo's
only note that the question is open. Declare each one in **`docs/provenance-allow`**,
in the same idiom `docs/need-form-allow` established: one entry per line,
`<ROW-ID> — <reason>` or `<ROW-ID> <Cell> — <reason>`; `#` comments and blank
lines ignored; a line with no ` — ` separator declares nothing (fail-soft in the
loud direction — a malformed entry can only fail to silence a finding). The file
is **not scaffolded** and an absent file declares nothing, so a clean repo carries
none. Each entry should say the row **owes an open-item row at your next review
sitting**; when the ruling lands, the marker and the entry go together. The
allow list is not a second home for provenance — an entry that is only "we like
this citation" is the rule being routed around.

**A licence attribution is not provenance** and stays regardless of any of this.

**This is a wording sweep, not a re-decomposition.** Do not change what a row
means and do not touch `status`. Expect your amendment detectors to fire on every
cell you rewrite — that is correct, and those rows are what your next sitting
reads.

### The flows gate stops matching your document TITLE [since 4e9a5c8a]

*(Anchored at the preceding commit of the same review round; the change lands in
the commit that follows it.)* `check_flows.py` used to select the first heading
whose title *started with* "Runtime flows", at any level. In a doc **named** for
the section — which is how `RUNTIME_FLOWS.template.md` shipped, and what the
architecture-retirement entry above told you to build — the H1 title shadowed the
real section and ran to end-of-file. The gate could not fail: delete your entire
Runtime-flows section and the step stayed green so long as one id-citing mermaid
block survived anywhere in the doc.

**The document title no longer counts as the section.** The first heading in
`docs/runtime-flows.md` is skipped; the section is a matching heading *inside*
the doc (an exact "Runtime flows" wins over a longer "Runtime flows …").

- **Check your `docs/runtime-flows.md` shape.** If its only "Runtime flows"
  heading is line 1, the step now fails with `no "Runtime flows" section
  heading`. Fix: keep line 1 as the document title (name your project in it) and
  add a `## Runtime flows` heading above your first diagram — the shape
  `RUNTIME_FLOWS.template.md` now ships. No diagram content changes.
- **Content outside the section is no longer scanned.** Ids cited in an intro or
  a neighboring section are neither counted nor validated now (they never should
  have been). If a diagram relied on the doc-wide sweep to look green, move it
  under the section, where it belongs.
- This is a **hard fail at the DevStg-Tests bar** — unchanged severity, only the
  selection rule moved. A repo below that bar pays nothing.

### Your pre-commit hook gains a `staged-divergence` step [since 4b8f9ab4]

*(Anchored at the preceding commit; the change lands in the commit that follows
it.)* Every freshness step your hook runs — `okf`, `trajectory-map`,
`status-map`, `open-items`, `derived-gate`, `ratify-fresh`, `skills-sync`,
`skills-index`, `prompt-catalog` — regenerates in memory and byte-compares
against the **working tree**. None of them has any concept of the index. So an
author who regenerates a stale artifact and forgets to `git add` it gets an
honest green over a commit that still carries the stale bytes. That is not
hypothetical: it happened in the kit's own history and was found only by an
adversarial re-measurement.

**The floor batch is one step longer.** `check.py --run-steps …` now ends in
`,staged-divergence`, and the step reports every declared `[generated]` artifact
that is modified in the worktree but absent from the index.

- **Take the new hook line.** `project-trajectory/hooks/pre-commit` is a
  take-wholesale kit file; if you hand-edited your copy's `--run-steps` list,
  append `staged-divergence` to it. A named-but-unknown step fails every commit,
  so take `check.py` in the same re-sync — the step is built-in there, never a
  `docs/stack.ini` `[step:]` section.
- **It reads YOUR census, so there is nothing to configure.** The artifact list
  comes from your `docs/stack.ini` `[generated]` section (a prefix row ends in
  `/`; a marker-pair row matches the file). A repo that declares no `[generated]`
  artifacts gets a clean SKIP.
- **It cannot block a commit.** Warn-first by ruling — findings print, the exit
  code stays 0. `check.py --staged-divergence --strict` is the promotion path if
  you want the error today; the shipped step does not pass it.
- **It skips cleanly off git** — no git binary, not a checkout, or a root that
  is not the checkout's top level each SKIP with the reason named.
- **What it does NOT catch:** an artifact that was **staged while stale**. The
  freshness gates read the worktree, so a stale blob added to the index passes
  them and passes this. Closing that needs the gates themselves to read the
  staged tree, which is deliberately not this change.
- **The remediation prose changed with it**: the hook's own "then re-commit"
  advice now says to **stage** the regenerated files first. If you carry a local
  variant of that comment, take the correction — it is the half of this gap that
  no mechanism closes.

### The ladder's END STATE: `Modified` RETIRES, `Founded` ARMS [since 2d51f140]

*(Anchored at the signing commit that seeded `docs/archive/last_approved/`; the
change lands in the commit(s) that follow it.)* The spine enum reaches the shape
repo-lock D-9 ruled — **`{Drafted, Approved, Founded}`** — and both halves move in
ONE commit, because the enum must equal the set of values at least one live
predicate recognizes at every commit. It is enforced on the always-on
`--strict-integrity` floor, so an unmigrated `Modified` cell is a hard finding on
your very next commit.

1. **`Modified` is DELETED, and there is no successor VALUE.** It marked
   "approved text that has since been amended". Under the snapshot mechanism an
   amended row STAYS `Approved` and the amendment is caught by DIFFING it against
   its copy in `docs/archive/last_approved/` — for every row, rather than the
   ones somebody remembered to mark. **Migrate your cells before re-syncing:** a
   `Modified` row is one that owes a human read, so rule each one and write
   `Approved` (with `intake.py snapshot` in the same commit), or write `Drafted`
   if you are re-opening it. Do NOT bulk-rewrite them to `Approved` unread —
   that laundering is the exact thing the marker existed to prevent.
2. **`Founded` is LEGAL and COMPUTED.** It means settled AND demonstrated: the
   artifacts the row calls for exist (SRs under an SN, LLR+TC under an SR,
   resolving code under an LLR, a written test under a TC). The four discharge
   computations already shipped; what this step adds is that the word is
   recognized — `is_founded` in `trace.py` and `derive_gate.py` (F5 duplicates,
   both move), a `SPINE_MATURITY` row mapping it ABOVE `Approved`, and every
   blessed-text reader accepting it (`--require-verified`, `spine_stage`'s
   Impl→Release discriminator, the LLR-status advisory's exemption). **No cell
   moves to it in this step**, exactly as it armed for `components.toml`. Nothing
   WRITES it: whether a tool ever should, and whether a hand-authored `Founded`
   is itself an error, is still open (D-9 consequence 2).
3. **THE ONE THAT BITES SILENTLY — the `# basis:` line loses `modified=N`.**
   `derive_gate.py` no longer emits the field. The kit's own `check._BASIS_RE`
   was made to treat it as OPTIONAL in the same commit, so a gate file that still
   carries one keeps the window detector's conclusive arm; **local tooling that
   REQUIRES the field goes blind rather than red.** Grep any consumer of
   `docs/gate`'s basis line for `modified=` first. Regenerating `docs/gate`
   (`python scripts/derive_gate.py`) is required regardless — `--check` compares
   the line whole.
4. **Two snapshot rules ARM as integrity ERRORS**, on the always-on
   `--strict-integrity` floor plus the pre-commit hook. **UNANCHORED:** a row
   whose live `Status` claims approval-or-above with no copy in the snapshot, or
   a copy that reads below it. **THE MIRROR INVARIANT:** a snapshot file that is
   not byte-identical to its live counterpart in the same commit. Both were
   warn-only before. They stay **vacuous by absence** — a repo that has approved
   nothing pays nothing — so this only bites once you have seeded a snapshot, and
   the fix for both is the same: write text into the live registry and copy it
   with `intake.py snapshot`, never edit the snapshot.
5. **Predicates and sets, if you patched or imported them.** `is_modified` is
   DELETED, not re-keyed, in BOTH `trace.py` and `derive_gate.py`.
   `SPINE_MATURITY` loses its `modified` row and gains `founded`.
   `dispatch._TC_NOT_RED` swaps `modified` for `founded`. `intake._apply_flips`
   REFUSES a located row it cannot move instead of skipping it silently — under
   this ladder its one source state is gone, so the mechanical adjudication flip
   writes nothing pending a ruling on what should replace it.
6. **Overwrite `registries/stakeholder-needs.template.toml`** (its maturity
   header block drops the third value) and re-read `process.md` §4, whose closed
   vocabulary sentence is the one home for this enum.

### Launchers select an interpreter: prefer `.venv`, require 3.11+ [since 27a65c19]

*(Anchored at the preceding commit; the change lands in the commit that follows
it.)* Your `agent-resume.{cmd,sh}` and `scripts/check.{sh,ps1}` used to accept
**any runnable** `python` — the launchers asked "does it run?" and never "is it
the version this harness needs?", and `agent-resume.*` did not look at `.venv`
at all. On a multi-Python workstation that is a broken front door: the kit's
scripts import `tomllib` (3.11+), so an ambient 3.8 first on PATH dies at import
with a valid `./.venv` sitting unused two directories away. Found in the kit's
own repo, where the text-inspecting launcher tests all passed while it happened.

**The policy, identical in all four files.** Candidates in order — `.venv`
(both layouts: `bin/python`, `Scripts/python.exe`), then `python`/`python3`,
then `py -3` on Windows — each probed by RUNNING it twice: `-c "pass"` (does it
run at all? the Microsoft-Store alias stub does not) and then
`sys.version_info >= (3, 11)`. First one that answers both wins; if none does,
the launcher refuses and prints **every rejected candidate with its reason**
rather than a bare "not found" about a python that is plainly there.

- **Take the two `check` launchers wholesale** — `scripts/check.sh` and
  `scripts/check.ps1` are kit-owned thin launchers with nothing of yours in them.
- **The root `agent-resume.*` launchers are the "preserve always" class** (§2.2):
  their EDIT slots are yours. So do NOT overwrite them — port the block instead.
  It is self-contained and sits between the `AGENT_CMD` guard and the engine
  line: copy it from `scripts/agent-resume.template.{cmd,sh}`, keeping your own
  slot values above it untouched. `agent-resume.command` needs no change at all;
  it `exec`s the `.sh` twin and inherits the selection (the template's comment
  now says so).
- **Windows: the `call` in front of the probe and the engine line is load-bearing,
  not style.** Without it `cmd.exe` hands control to a `.cmd`/`.bat` shim python
  (pyenv-win ships exactly that shape) and never returns — the launcher then exits
  silently having done nothing. If you hand-port only part of this entry, port
  that.
- **PowerShell: the probe is `-c "pass"`, never `-c ""`.** PowerShell drops an
  empty string when it builds a native command line, so the empty form arrives as
  a bare `-c` and *every* candidate reads as broken.
- **If your project deliberately targets an older Python**, this floor is the same
  `(3, 11)` your `scripts/setup.{sh,ps1}` and the kit's `agent_common.MIN_PYTHON`
  already assert — lower it in all of them together or not at all.
- **A stale `.venv` no longer wins by merely existing**, which is the half of
  "prefer the venv" that is easy to get wrong: a venv built on an old interpreter
  is rejected with its reason and the launcher falls through to a good PATH
  python, instead of pinning you to the broken one.

### `docs/provenance-allow` entries must NAME an `OI-###` [since 45c65263]

*(Anchored at the preceding commit; the change lands in the commit that follows
it.)* If you carry a `docs/provenance-allow` — the reviewed exception list for
`trace.py`'s citation-frame advisory — its entry grammar gains a **required
field**. An entry now reads `<ROW-ID> <Cell> <token> — OI-###: <reason>`, and the
id is the **first token of the reason** (a position, not a mention: an id further
into the sentence is prose).

- **It is HARD from the first commit**, not warn-first, and it is
  **integrity-class**: an entry with no id, or one naming a row your
  `docs/requirements/open-items.toml` does not have, fails
  `trace.py --strict-integrity` — the always-on floor your pre-commit hook runs.
  A missing field has no false positives, which is the only reason a new rule
  ships hard here.
- **Why:** an allow entry is a DEFERRED DECISION — it says a rule you mechanize
  is knowingly not satisfied. In the kit's own file, 19 entries promised an
  open-item row **in prose** ("owes an open-item row at the sitting") and not one
  of them had one, because the announcement and the queue were two unconnected
  artifacts. The field makes the unrecorded deferral unrepresentable.
- **Migrate in one pass:** for each entry, add the id of the row that carries its
  question, right after the ` — `. If the question has no row yet, file one
  (`Status = "pending"`) — that IS the change.
- **Vacuous if you have no open-items registry**, and it stays that way until you
  scaffold one; the always-on entry below is what tells you to.

### The open-items layer is ALWAYS ON [since 45c65263]

*(Same commit as the entry above.)* The owner decision surface moved out of
`process-options.md` and into always-shipped process (`process.md` §5). Nothing
about the artifacts changed — what changed is that they are no longer optional.

- **Scaffold the registry if you do not carry one:** copy
  `registries/open-items.template.toml` to `docs/requirements/open-items.toml`
  and run `python scripts/gen_open_items.py` once, which writes
  `docs/open-items.html`. A missing view reads as STALE to its own freshness
  gate, so generate it in the same commit.
- **`check_docs.py` S-3 is no longer vacuous without the registry.** Its escape
  used to read "the surface is optional; omit it to opt out"; an absent registry
  is now the finding itself. **Warn-only** — it is never `check_docs`'s exit
  code — so this cannot block you mid-migration.
- **Your session log fragments gain an optional declaration.** A
  `docs/log.d/` fragment may state `Deferred open items: OI-45, OI-46` (or
  `… none — <why>`); `gen_open_items.py --check` verifies each declared id names
  a **pending** row, and reports a **VACUITY** finding when your queue holds zero
  pending rows while allow entries still defer, naming the entries. Both are
  warn-only: the step's exit code stays the freshness verdict.
- **Take `process.md` §5 and the `process-options.md` trajectory section**
  together — the layer's *depth* (why registry-plus-view, the lifecycle, the
  S-1..S-3 lint) stays in the options doc; only the *always-shipped* statement
  moved.
- **What it does NOT buy, stated so the change does not overclaim:** always-on is
  the substrate, never the mechanism. A fresh registry renders "the owner queue
  is empty" perfectly truthfully — which is the failure the three arms above
  exist to catch.
### The `Implements:` harvester tightens — expect the map's third column to EMPTY [since 1bf4e9ef]

*(Anchored at the preceding commit; the change lands in the commit that follows
it.)* `gen_arch_map.py` used to harvest ANY `SN|SR|LLR|TC-###` token out of a
public symbol's docstring or the four comment lines above its `def`. It now
requires the literal `Implements:` token on the same line
(`gen_arch_map.backlink_ids`). **This will look like a regression and is not.**

- **What you will see:** the `Implements` column of your generated MODULE MAP
  goes mostly or entirely blank on the next regeneration. In the kit's own repo
  it dropped from 50 populated symbols to 2 — because 60 of the 62 links it had
  been reporting were never declared by anyone, and 13 named no live registry
  row. A sorting example in a docstring ("SR-9 orders before SR-10") was being
  reported as two requirements that function implements.
- **What to do:** regenerate, look at what is left, and treat the empty column
  as your real starting point. If a symbol genuinely implements a row, write the
  declaration — a line carrying `Implements:` followed by the ids, in the
  docstring or in the four lines above the `def`.
- **The grammar is MARKER-LINE ONLY and does NOT refuse a wrapped list**,
  unlike the `Contracts:` grammar it sits beside. An id pushed onto its own
  continuation line is simply not declared; nothing raises. That asymmetry is
  deliberate (the module docstring states it) — a hard failure over a reflowed
  docstring would break map generation for everyone.
- **If your map is spliced into `AGENTS.md`/`CLAUDE.md`**, this changes a file
  agents read on every session. Regenerate in the same commit so the doc and the
  code agree.

### Reverse back-link coverage: a new `[checks]` dial and a new harness step [since 1bf4e9ef]

*(Same commit as the entry above.)* The other half of the same ruling. The
kit now MEASURES the convention instead of only asserting it, and the shipped
guide states it as a dial rather than an unconditional rule.

- **Add the dial.** `docs/process.toml` gains a seventh `[checks]` key —
  `backlink_coverage_min = 0`. It is the minimum PERCENTAGE of your live LLR
  rows that a literal `Implements:` declaration must name, and `0` is its off
  position. Copy the key and its header comment from
  `process.toml.template`; born there, it has no legacy one-word file, so
  nothing needs migrating and it cannot be double-declared.
- **A new harness step runs it.** `check.py` gains `backlink-coverage`
  (`gen_arch_map.py --backlink-coverage`) at `DevStg-Tests` and `DevStg-Impl`.
  It reports the percentage on every run; below the dial it WARNS, and
  `--strict-backlinks` (which the step passes from `DevStg-Tests` on) turns that
  into a failure. **At `0` it can never fail** — so a straight re-sync changes
  no exit code anywhere.
- **Scope, so the number means what you think:** the surface is
  `docs/stack.ini` `[paths] src` and deliberately NOT `[paths] tests` (an LLR
  that is verified but never built must not score as implemented). The file
  types are `gen_arch_map.BACKLINK_EXTS`, overridable with `--backlink-ext`.
  Widen that list only with care: the denominator is your LLR count, so a wider
  list can only RAISE the score — over-inclusion produces false PASSES.
- **It measures PRESENCE, never correctness.** A back-link naming the wrong
  requirement counts clean. Do not read the percentage as a verification result.
- **Raising the dial is a decision, and only one direction is legitimate:**
  write the declarations, then raise the number to a bar your tree already
  clears. The kit records 50% as the target; it ships at 0 because a bar its own
  author misses by 80x trains readers to silence warnings.
- **Vacuous with no LLR registry**, so a repo that has not scaffolded the design
  tier pays nothing.


### The shared helper package `scripts/kitlib/` [since b94bf58c]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**A new DIRECTORY under `scripts/`, and the first one the kit has ever
shipped.** Owner ruling D-8 ended the rule that every kit script duplicates its
small helpers to stay independently copy-able; the shared behaviours now live
once in `scripts/kitlib/` (`config.py`, `git.py`, `registry.py`, plus
`__init__.py`), and eleven shipped scripts — `bootstrap.py` among them — import
from it.

**What you must do: copy the whole directory.** `kitlib/` is kit-owned, like
every other `scripts/*.py`, so the overwrite rule for kit files applies to it
unchanged. The one thing that differs from every previous script addition is
that a PARTIAL copy is silently broken: the scripts import `kitlib.config` /
`kitlib.git` / `kitlib.registry` by name, so a directory missing one module
ImportErrors on your first check rather than degrading. Copy it whole, then run
`scripts/check.py` — the import resolves through `sys.path[0]`, which is the
script's own directory, so no `PYTHONPATH` or install step is involved.

**If you had edited a kit script's copy of one of these helpers** — a locally
patched `_first_declared_line`, `_utf8_console`, `_git_out`, or the
`docs/work/` spec-folder reader — that edit is on a kit-owned file and the
deviation review in §2 is where it surfaces. Re-apply it to
`scripts/kitlib/<module>.py` rather than to the consumer: the consumer now
holds a one-line re-export, so a patch re-applied there is silently overwritten
at the next re-sync.

**Nothing in your `docs/` changes**, and no registry cell moves. This is a
scripts-only change.


### `kitlib/station.py` — the terminal-outcome vocabulary leaves `integrate.py` [since b9538b26]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**A fifth module in `scripts/kitlib/`, and the same copy-it-whole rule.** The
three terminal lane outcomes (`OUTCOME_DIRS`), the `Bar-Green:` attestation
label, and the "exactly one declared status directory, or none" decision
(`outcome_of`) now live in `scripts/kitlib/station.py`. They used to be defined
in `scripts/integrate.py`, which meant any reader of the vocabulary imported the
merge coordinator to reach it — including the dashboard, a render leaf that
writes nothing.

**If you only overwrite kit files, you need do nothing but include the new
module in the copy.** `integrate.OUTCOME_DIRS` and `integrate.BAR_GREEN` are
still there and still resolve to the same values; they are re-exports now. No
call signature changed and no output changed.

**If you import those names yourself**, prefer `from kitlib.station import
OUTCOME_DIRS` going forward. The re-exports are kept, not deprecated — but a
tool of yours that reaches for the vocabulary should not have to load a merge
coordinator to get it.

**One value-shape note, and it is deliberately compatible.** The outcomes are
now members of a `str` enum (`kitlib.station.Outcome`) rather than bare strings.
Every `==` against `"merged"` / `"cancelled"` / `"partial"`, every f-string,
every `json.dumps` and every sort behaves exactly as before, because the enum
subclasses `str`. Only an identity check (`is "merged"`) or a `type(x) is str`
test would notice, and neither was ever a supported read.

**Nothing in your `docs/` changes**, and no registry cell moves.

## 4. Translation helper — concept renames

A rename reads to a diff as an unrelated deletion plus an unrelated addition, which
is exactly the class that bit a real adopter (a silently renamed public function
broke their imports). These are the renames the kit has shipped, each anchored the
same way. Grep your **own** prose, scripts, CI, hooks and registry cells for the
left-hand spelling.

### `UN-###` → `SN-###`; `read_user_needs` → `read_stakeholder_needs` [since 3ea00aa5]

User Need → Stakeholder Need, prefix only (numbers preserved). The function rename
is the import-breaking half — see the UN → SN entry in §3.

### `Track` → `Workstream` (work-item grouping) [since 73313e69]

"Track" now means only the parallel-execution lane. The legacy header is still
read, so this is a rename-when-convenient, not a break.

### `modules.csv` / `MOD-###` → `repos.csv` / `REPO-###` [since 7f8cdc56]

The multi-repo delegation registry names repos, not components. Legacy file + ids
still read; both may coexist mid-migration.

### `Campaign` (the per-WI grouping column) → deleted [since 1cc8d636]

The roadmap is binned `phase ⊃ workstream ⊃ work-item`. A leftover column is
ignored (read by name, no vocabulary rule), so nothing breaks — but your prose and
dashboards should stop saying it.

### `docs/trajectory.html` → `PROJECT_STATE.html` (repo root) [since 3e56f7ce]

Step name (`trajectory-map`) unchanged; the path it checks moved.

### `docs/open-items.md` → `docs/requirements/open-items.toml` + `docs/open-items.html` [since 41b228a5]

Source and view split: one is the registry you edit, the other is generated.

### `agent_dispatch.py` → `integrate.py` (+ the drive loop) [since 31ad569d]

The v4 dispatcher's job splits into claim/integrate on one side and the drive loop
on the other; the module name does not survive.

### `retired` → `cancelled`; `disposition = "retired"` → the directory [since 88db58af]

The work-item terminal state is respelled and moves into its own directory; the
frontmatter key is deleted, not renamed.

### `scripts/drive.py` → `scripts/dispatch.py` (+ `scripts/lane.py`) [since 81cac0e1]

Delete your old `drive.py`: `agent_loop` imports `dispatch`, so the stale file
shadows nothing and drifts silently.

### `G0|G1|G2|G3|G-Release|G-Final` → the stage ladder [since 08c985cb]

The tags retire; the traceability survives. Grep your own prose, scripts, CI,
hooks and registry cells for the left-hand spelling — **as a whole-word TAG, not
as the word "gate"**, which survives wherever it means a check that can fail
(`docs/gate`, `derive_gate.py`, `--gate`, "the freshness gate" all stay).

| retired tag | now | what it names |
|---|---|---|
| `G1` | `DevStg-Reqs` | the bar certifying `DevStg-Needs` … `DevStg-Reqs` |
| `G2` | `DevStg-Tests` | the bar certifying `DevStg-Arch` … `DevStg-Tests` |
| `G3` | `DevStg-Impl` | the bar certifying `DevStg-Impl` |
| `G0` | `DevStg-Below` | the internal below-the-floor sentinel — never a bar |
| `G-Release` | `DevStg-Release` | the release-readiness **rung** (never a mechanized bar) |
| `G-Final` | the owner's final read | the `final_review` dial, which is its own axis |
| `[phase]-[g1]` / `-[g2]` | `[phase]-[reqs]` / `-[tests]` | the phase-anchor archetype for NEW titles only |
| `## Gate Sign-offs` | `## Sittings` | code-pinned; each row now names a rung RANGE |

Every reader accepts the left-hand column as an alias, so this is a
convert-at-your-pace rename — with two exceptions that are **not** aliased:
`docs/gate`'s own contents (regenerate it) and a stage value in a basis line
(same regenerate). Full recipe: the §3 entry above.

### Requirement quality: the eight characteristics + the EARS pattern [since ed1d4863]

`docs/process.md` §3 now states the quality bar it previously only gated: the
eight characteristics (necessary, singular, unambiguous, complete, verifiable,
feasible, conforming, traceable) and the five **EARS** statement patterns, with
the condition fronted (`When` / `While` / `If … then` / `Where`, or a bare
subject for the ubiquitous case).

**Nothing in your registry breaks.** The new `trace.py` rule
(`ears_advisories`) is **warn-only under every flag** and reads only the OPENING
of an SR `requirement` cell, reporting a condition dressed in some other keyword
("Before …", "During …", "For …"). Take the file, run `trace.py`, and treat the
new report section as a worklist rather than a gate. The gating form rules are
unchanged.

If you keep a customized `registries/system-requirements.template.toml`, its
`-000` example row's `requirement` value is now the EARS grammar itself — a
kit-owned teaching cell worth taking, but a no-op if you deleted the example row
on your first real entry, as intended.

### The `DevBar-*` prefix retires — ONE vocabulary, the verb carries the axis [since 7ccbd3a6]

**The `DevBar-` prefix is gone.** A repo is **IN** a stage and **CLEARS** a
stage, and the same `DevStg-` token names both readings — what tells them apart
is the sentence around the token, never a second spelling. The three clearable
rungs are a strict subset of the eight.

**The mapping is NOT a prefix swap. Read the third row twice:**

| retired | now | why |
|---|---|---|
| `DevBar-Reqs` | `DevStg-Reqs` | 1:1 |
| `DevBar-Tests` | `DevStg-Tests` | 1:1 |
| `DevBar-Release` | **`DevStg-Impl`** | **not 1:1.** That bar always certified the **Impl** rung — `DevStg-Release` sits outside the derived range entirely (no value runs it). The old pair sat three letters apart meaning a strictness level and a per-release milestone; that trap is what the rename removes. |
| `DevBar-Below` | `DevStg-Below` | 1:1 (still the internal sentinel, still not a stage anyone is in) |

**Nothing breaks at the re-sync.** All four retired spellings are accepted as
read-side aliases wherever a value arrives — `check.py`'s flag, `docs/stack.ini`
`gates=`, a WI's `bar:` frontmatter — exactly as the `G1`/`G2`/`G3` tags have
been. `DevBar-Release` resolves to `DevStg-Impl` through that table, so an
un-migrated hook keeps selecting the same steps it always did.

**The flag renamed too: `--gate` → `--stage-cleared`.** The value is now a stage
token, so the flag has to say which reading it means — the stage being *cleared*,
not the stage in work. **`--gate` is still accepted, silently and indefinitely**:
it is a string your hooks, CI and launchers pass literally, and the word "gate"
was never retired where it means a check that can fail. `docs/gate` and
`derive_gate.py` **keep their names** for the same reason.

**What to do:** take the kit-owned scripts wholesale, then `grep -rn 'DevBar-'`
your own prose, `docs/stack.ini` and CI. Convert at your pace — and if you keep
a hand-written `docs/gate`, note that it regenerates: `python
scripts/derive_gate.py`. `scripts/check_vocab.py` now refuses the prefix in
authored files (warn-first, `--strict` gates), with your history, archives and
attestation quotes carved out as always — a record of what happened is not
rewritten.

### The `13v` waiver token → `recorded waiver: <reason>` [since 4e9a5c8a]

**If any of your rows carry `13v`, rewrite them.** The waiver marker that
clears the one-`shall` valve and the artifact-naming valve used to be the bare
token `13v`. That token was a **decision id** — it named this kit's own log
decision `2026-08-13v` — so the marker mandated into your reason cell was
exactly the kind of citation the provenance rule bans from that cell, and it
pointed at a ruling no adopter can read.

| retired | now |
|---|---|
| `13v` | `recorded waiver: <reason>` |

**This is a breaking change for your rows, not just for the kit's prose.** The
artifact-naming advisory recognizes only the new marker, so a row still
carrying `13v` loses its waiver and the advisory returns. Rewrite each one as
`recorded waiver: <reason>` in the tier's reason cell — `Rationale` at SR,
`why` at SN — keeping the reason itself, which is the part that was always
load-bearing. The colon is part of the marker: it is what separates a declared
valve from prose *about* a waiver, and in this repo two of the only two live
`13v` hits turned out to be prose saying the waiver was already spent.

---

### The shipped docs catch up to the enforced maturity field [since c5e19720]

**No row of yours changes; the DOCS that taught you how to author them do.**
The IF and frame tiers' one maturity field has been `Status`, valued
`Drafted` | `Approved`, since the 2026-08-17 registry status unification — but
`INTERFACES.template.md`, `PROCESS.md` §8, `MULTI_REPO.md`, `EXAMPLE.md`,
`KICKOFF_PROMPT.md` and the release checklist still documented the transitional
`Approval` column with lower-case `draft`/`approved`, and `INTERFACES.template.md`
documented a column its own worked example did not use.

| retired in the prose | now |
|---|---|
| `Approval` column | `Status` |
| `draft` · `approved` | `Drafted` · `Approved` |
| `Stable` interface (release checklist) | `Approved` interface |

**What to do.** If you copied `INTERFACES.template.md` or `EXAMPLE.md` into your
own docs and edited them, re-read the `Status` row against your registry: the
checker has always enforced `Drafted`/`Approved` here, so a row you authored
from the old prose is already failing `--strict-integrity` and the doc was the
only thing telling you otherwise. `Founded` is **not applicable** to these
tiers and never will be — it means settled *and demonstrated*, while an
approval says only that the seam is agreed.

**The kit now pins this rather than re-sweeping it.** `tests/` carries one
cross-document contract test that reads `trace.ENUM_FIELDS` — the same dict the
integrity floor reads — and fails when an instructing surface teaches a value
the enum no longer carries. Ten hand-maintained copies of one vocabulary is what
produced this entry; a rename now breaks a test instead of rotting a doc.

### The spec-of-record's new-seam row and its retired checker arm [since c5e19720]

**If your specs cite `Status=Proposed` seams, the value was never legal.**
`specs/README.template.md` and `specs/WI-000.template.md` instructed you to file
a new seam as a `Status=Proposed` row; no version of the IF schema has carried
`Proposed`. File it `Status=Drafted`. The `IF-045 (Proposed)` notation *on the
citation line* is unaffected — that is the spec's own shorthand for "this row is
being minted by this filing", not a registry value, and `plan_coverage.py` still
reads it.

**And the rationale check is gone, which those templates still promised.**
`check_trajectory.spec_interface_findings` verifies that your `## Interfaces`
citations **resolve** — nothing more. The forced nearest-existing-IF rationale
arm retired with its arming input (`Stability = Experimental`) at WI-442 and was
deliberately not re-keyed: on this repo's registry the obvious re-key would have
armed 113 rows instead of 5, at ERROR severity under `--strict`. Rationale
presence is now reviewer-tier alongside rationale honesty
(`docs/rubrics/spec-interface-hygiene.md`). If you relied on that check, the
rubric is where the obligation lives.

### Skill-copy wording: commit subjects and the standing rules [since c5e19720]

**Kit-owned files — overwrite them and move on.** The `session-protocol` skill
now states both live commit-subject forms (`WI-<n>:` for a session executing one
work item, `<category>:` for sittings, sweeps, merges and reviews) instead of
only the first, and carries a **Standing rules** subsection relocated out of the
forward-only `status.md`. The `registry-hygiene` skill's DevStg-Impl line names
the `--require-verified` flag instead of a bare "+ Verified", which folded into
`Approved` at the status unification. Nothing enforces the commit form; it is
stated once so a log carrying both stops reading as two conventions.

### The `last_approved` snapshot gains an AUTHORITY GATE (`--approves`) [since 46616726]

**Kit-owned files — overwrite them and move on:** `scripts/baseline_snapshot.py`,
`scripts/intake.py`. **What changes for you:** `intake.py snapshot` used to copy
whatever was in the tree, every time. It now REFUSES a refresh that would absorb
RATIFIED text into `docs/archive/last_approved/` unless one of three things is
true — the copy absorbs nothing ratified (a `Module`/`CodeSymbol`/`TestRefs` or
ref-pointer refresh, the common case, unchanged and free); a `Status` cell moved
in the same registry (amend-plus-flip IS ratification); or you pass
`--approves <ref>` naming the sitting, log fragment or commit that ruled the
cells, which is recorded into the snapshot's prose stamp
(`docs/archive/last_approved/README.md`, created if you have none).

**Why:** an adversarial round executed the hole end to end. Creating the record
was guarded (`--seed`) and REWRITING it was not, so a two-commit path — amend an
Approved requirement, then refresh — re-blessed the amendment with every check
green and the drift absorbed into the baseline. **What you must do:** nothing,
unless your sitting ritual amends approved text without moving its `Status`. If
it does, add `--approves` to that one command; the refusal names the rows and
the cells, so you will not have to guess which case you are in.

### The mirror invariant reaches COMMITTED state [since 46616726]

**Kit-owned files — overwrite them and move on:** `scripts/check_trajectory.py`,
`scripts/trace.py`. **What changes for you:** `trace.py --strict-integrity` — the
always-on floor your pre-commit hook runs — now also compares every file under
`docs/archive/last_approved/` against its live counterpart **at the commit that
last wrote it**, not just at the staged commit. A forged or stale snapshot that
LANDED (hooks bypassed, or a commit made outside them) now reds every subsequent
run instead of being invisible after the fact.

**It cannot fire on a pending amendment**, and that is deliberate: the comparison
is pinned to the snapshot's own writing commit, so live moving ahead — the lag
that IS the signal — stays silent. Two `git` invocations per run; silent off git
and for an untracked snapshot. **What you must do:** run
`trace.py --strict-integrity` once after syncing. If it reds with a LANDED
divergence, your record and your registries disagreed at some past commit — the
finding names the file and the commit; re-copy in a reviewed commit
(`intake.py snapshot --approves <ref>`) or restore the copy that was blessed.

### `backlink_coverage_min`: where the step actually runs [since 46616726]

**Kit-owned file — overwrite it and move on:** `process.toml.template`. **What
changes for you:** prose only, and it corrects a false statement. The `[checks]
backlink_coverage_min` header claimed the check "WARNS at a plain run and FAILS
from DevStg-Tests on". The first half was never true: `check.py`'s
`backlink-coverage` step exists from DevStg-Tests on and **not below**, so a
plain run does not warn — it does not run the step. The same block now also
carries the measurement's one caveat (the scan applies no position restriction,
so a spine id in a string literal counts as a carrier — an error that can only
RAISE your score, never lower it). Your `docs/process.toml` VALUE is yours; only
the kit's commentary moved.

### Product checks no longer fall when you draft a requirement [since aa46953e]

*(Anchored at the PRECEDING commit — this entry ships with the change itself.)*

**Kit-owned file — overwrite it and move on:** `scripts/check.py`. **What
changes for you:** a repo whose spine is mature can no longer lose its
**product-layer** checks by adding one `Drafted` row.

The derived bar is a MIN over every in-scope spine row, so one ordinary draft
requirement drops it to what a fresh scaffold shows — and `ci/check.yml` runs
`check.py` at exactly that value on every push and pull request. Product checks
were riding that same number, so *planning work suspended regression detection
for already-built code*. Now `check.py` selects product-layer steps at
`max(derived bar, ex-draft)`, where `ex-draft` is the same arithmetic with the
pending rows removed — already on your `docs/gate` `# basis:` line. Maturity
checks are untouched: they still fall with the bar, because that fall is the
new-phase signal.

**Which steps this covers:** everything at `layer = product` — `[product]`
format/lint/test plus each `[step:*]` you declared as product. Process-layer
steps are unaffected.

**In practice today that is your declared steps only, and the honest form of
the sentence above says so** (corrected 2026-08-21). The floor engages at one
bar, `DevStg-Tests` — `ex-draft` can never exceed it while `derive_gate`'s
release ceiling stands — and it selects by MEMBERSHIP, while `[product]`
format/lint/test are tagged `{DevStg-Impl}` only. So the floor cannot reach
those three, and it holds nothing at all unless you have written both
`gates = DevStg-Tests` and `layer = product` into a `[step:*]`. Whether the
three built-ins should be reachable is a live owner question (`OI-51` in the
kit's own registry); until it is ruled, do not read this entry as covering
them, and do not expect the red the next paragraph describes unless you have
declared such a step.

**What you may notice:** if you have a `[step:*] layer = product` declared at or
below the bar your ratified rows have earned, it now **gates** during a draft
window where it previously ran advisory (warn-only) or not at all. If that step
has been failing quietly, your first push after this re-sync reds. That is the
change working: the failure was already there, and the exit code was not
reporting it. There is deliberately no dial to switch the floor off.

**Nothing in your `docs/` changes.** No registry cell moves, no regeneration is
needed, and a `docs/gate` written before the `ex-draft=` field existed simply
gets no floor (the floor abstains rather than guessing) until you next run
`scripts/derive_gate.py`.

### The derived-requirement LABEL becomes a cell: `Hat-Refs` on SR and LLR [since 046843eb]

*(Anchored at the PRECEDING commit — this entry ships with the change itself.)*

**Kit-owned files — overwrite them and move on:** `scripts/spine_carrier.py`,
`scripts/migrate_carrier.py`, `scripts/trace.py`, `scripts/check_trajectory.py`,
`PROCESS.md`, `skills/spine-authoring/SKILL.md`, and the two `-000` example rows
in `registries/system-requirements.template.toml` +
`registries/low-level-requirements.template.toml`.

**What changes for you:** the SR and LLR tiers gain one **optional** key,
`hat_refs` (column `Hat-Refs`) — a typed array of **hat roster NAMES**
(`["SECURITY", "MAINTAINER"]`) naming the declared perspectives in
`docs/requirements/hats.toml` that a row's content is attributable to. `PROCESS.md`
and the `spine-authoring` skill used to tell you to record a derived
requirement's deriving hat as a **prose label in `Rationale`**. That instruction
is retired: a prose label resolves against nothing, so no check could tell a live
hat from one you deleted last month. The cell replaces it.

**Nothing you have already written breaks.** The key is optional at every tier
that declares it, and an **absent cell means NOT RECORDED — never "no
perspective applied"**, so nothing reads a blank as a claim. Concretely:

- **A `Hat-Refs` naming a hat your roster does not declare is a hard finding**
  under `trace.py --strict` (class `hat`), in the same class as an SR citing a
  deleted SN. This is the arm that stops the cell rotting when you retire a hat.
- **Coverage is warn-only, permanently.** `trace.py` reports ONE advisory line
  counting the rows with no `Hat-Refs`, plus one naming hats no row is
  attributable to. Neither ever gates. A repo that adopts the key and fills
  nothing stays green.
- **Deleted your `docs/requirements/hats.toml`?** The whole check is vacuous —
  absence is opt-out for the hats layer, so there is no name a row could fail to
  cite. Nothing to do.

**The one rule worth reading before you fill any LLR cell:** an LLR's `hat_refs`
carries **only what its own design decomposition raised — never a copy of its
parent SR's**. A row's EFFECTIVE set is DERIVED (`trace.effective_hats`: own refs
unioned with its `SR-Refs` parents'). Copy the parent's hats down instead and
re-ruling one requirement becomes a sweep over every child it has; derive them
and the same re-ruling propagates on the next read, correcting no LLR cell at all.

**Backfilling is optional and is its own piece of work — do not let a tool do
it.** If your rationale cells carry prose hat attributions today, they can be
lifted mechanically ONLY where the row states its own derivation in a fixed
label form. In this kit's own repo a regex over `hat.` matched 19 rows and TWO of
them were wrong: one names a hat in order to REFUSE it as a basis, and one
carries a struck attribution. Read every row you migrate.

**Cell classification, if you run the ratification ladder:** `Hat-Refs` is
declared **traced**, not ratified (`check_trajectory.SPINE_TRACED_CELLS`), so
adding it to an already-approved row does not arm a re-attest window or trip the
`last_approved` drift comparison — the drift basis reads the ratified half only.
It is deliberately NOT in `intake.ROUTED_TRACED_CELLS`: a hat re-point restates
which lens a row is attributable to and moves no obligation.

### Seam-TC coverage promotes at DevStg-Tests+ (OI-43 ruled (a)) [since d9a0a61f]

*(Anchored at the PRECEDING commit — this entry ships with the change itself.)*

**Kit-owned file — overwrite it and move on:** `scripts/check_trajectory.py`.
**What changes for you:** an IF seam cited by no TC — until now warn-only at
every gate — becomes an **ERROR under `--strict`**, wired the same way
`component_findings`/`spec_interface_findings` already are (`check.py` passes
`--strict` to this step from `DevStg-Tests` on; a plain commit and a
`DevStg-Reqs` gate stay warn-only). `interface_findings`' own total-uncited
line is unchanged and still never gates — a new function,
`if_tc_coverage_findings`, carries the promotable half.

**What you may notice:** if your spine has crossed `DevStg-Tests` and any
declared seam has no TC citing it, your first run after this re-sync reds —
same shape as the WI-473 product-floor entry above, and for the same reason:
the gap was already there, and the exit code is what changed. There is
deliberately no dial to switch the promotion off; it shares
`[checks] interfaces_check`, the same opt-out `interface_findings` already
uses.

**The migration allowlist is YOURS to seed, not the kit's to ship.** Create
`docs/if-tc-coverage-allow` (absent = empty = every uncited seam errors) with
one `IF-###` id per line, seeded from your own measurement:
`python scripts/check_trajectory.py --root .` and read its "IF seam(s) are
cited by no TC" line. State the basis (command, count, revision) in the file's
own header — `docs/if-tc-coverage-allow` in this repo, if you want a worked
example — and treat the list as a burn-down, not a permanent exemption: the
standing never-green-by-list-edit rule applies to every entry. A stale entry
(its seam gained a TC, or its id no longer resolves) is reported by
`if_tc_allow_hygiene_findings` — never blocking, so pruning it is
housekeeping, not a fix owed under pressure.

### `subagent_gate.py`'s parse-failure arm turns fail-closed (OI-46 ruled (1a)+(2a)) [since f3cb9801]

*(Anchored at the PRECEDING commit — this entry ships with the change itself.)*

**Kit-owned files — overwrite and move on:** `scripts/subagent_gate.py`,
`scripts/agent_loop.py`.

**What changes for you:** if your `docs/process.toml` is **present but does
not parse** (a syntax error, a bad encoding, an unreadable file) while
`[checks] subagent_gate` is opted in, an unattended run's subagent-spawn
`PreToolUse` hook used to read that as *undeclared* and fall through to the
legacy `docs/subagent-gate` file or, absent that too, a quiet `allow` —
diverging from `check_trajectory.py`/`gen_okf.py`, which have always read the
same state as ON. It now reads `ask` instead, and the legacy file stops being
the POLICY on that arm: a broken `docs/process.toml` is a place this gate
cannot proceed, not a place to keep moving. A genuinely **absent**
`docs/process.toml` is unaffected — that still allows (the opt-in posture).

**Said precisely, and corrected 2026-08-21:** the arm resolves to the **more
restrictive of `ask` and whatever the legacy `docs/subagent-gate` declares**.
The first cut of this change short-circuited to `ask` outright, which for a
repo carrying **both** surfaces mid-migration (the state `--migrate-config`
exists to serve) turned an explicit legacy `deny` — exit 2, the run halts —
into `ask` at exit 0. "Fail-closed" means never loosening a decision the human
already wrote down, so a legacy `deny` survives a broken `process.toml`; a
legacy `off` does not re-open the gate.

**What you may notice:** if you run with `subagent_gate` enabled AND your
`docs/process.toml` is currently malformed, your next unattended run defers
every subagent spawn to approval instead of silently allowing them — or keeps
refusing them outright if your legacy `docs/subagent-gate` says `deny`. There
is no dial to keep the old (fail-open) reading — fix the TOML, which you would
want to do anyway.

**The fail-open log is now surfaced, not just written.** Every gate decision
(including every fail-open-on-error allow) has always appended to
`out/subagent-gate.log`, and nothing read it. `agent_loop.py`'s launch banner
now prints its line count when the file is non-empty (silent otherwise), via
a new `_subagent_gate_log_count()` helper — no config, nothing to migrate.

---

### The id-watermark gains a RULED-correction arm (OI-47 ruled (e)) [since da4d3bcd]

*(Anchored at the PRECEDING commit — this entry ships with the change itself.)*

**Kit-owned files — overwrite and move on:** `scripts/trace.py`.

**What changes for you:** `docs/id-watermark` could previously only rise by
ALLOCATION (`--bump-ids`, raising every mark to the live maximum) — the one
other way a mark could ever move was a hand-edit, which `trace.py`'s
integrity floor has always refused outright ("a mark rises by allocating an
id, never by hand"). If your own `docs/id-watermark` was ever mis-seeded
below a space's true history (an id allocated, cited in ruled documents, then
cut — before that space had a mark to protect it, or from a bug in the
seeding computation itself), you had no sanctioned way to correct it short of
re-allocating a live row you may not want.

`trace.py` now ships a second, narrower path: `--correct-mark SPACE NEW
RULING` raises exactly one named space to a named value, citing the id of
the decision that authorized it. The ruling id is recorded as a `#
correction: SPACE old -> new (RULING)` comment line in the watermark's own
header — invisible to `read_watermark` (comments are skipped there) and
readable by `read_corrections`, the new function `_mark_history_findings`
consults so a correction's exact `(was, now)` transition — and only that
transition — clears the "nothing justifies this raise" finding an
unrecorded hand-raise still trips. **One-shot, deliberately:** a space that
already carries a recorded correction refuses a second one, even citing the
same ruling — the verb corrects a mis-seed once, it does not hand a ruling a
standing licence to keep raising the mark.

**The record is bound to your open-items registry (hardened 2026-08-21).** The
first cut kept the record's whole authority INSIDE the file it guards, so two
hand-typed lines forged a raise that passed `--strict-integrity` clean. Now
every recorded correction is checked whether or not a mark moved: the cited id
must resolve to a row of `docs/requirements/open-items.toml` whose status is
`ruled`, that row's text must name the space **at the corrected value** (`B =
8`, `B=8` or `B-008`), a space may carry only ONE record, and a record already
in git may not be edited or deleted. **What this means for you:** if you use
`--correct-mark`, write the ruling first and let it state the number it
authorizes — a ruling that only mentions the space in passing is refused, by
the verb at write time and by the integrity floor thereafter. If your repo has
no open-items registry, the verb refuses rather than proceeding on an
unverifiable citation.

**What you may notice:** nothing, unless you actually run `--correct-mark` —
`--bump-ids` and every existing watermark rule are unchanged, and a
regeneration now carries forward any correction record your file already
has (it only ever ADDS a record, via the new verb; an ordinary bump never
drops one). This repo used the verb on itself the same commit it shipped:
`B` 7 -> 8 and `REL` 3 -> 4, both citing `OI-47` — the two prior-cut,
mis-seeded ids `docs/requirements/external.toml`'s "SPENT IDS" prose used to
warn about by hand. That block is now a pointer at the ruling; the mark
carries the protection.

---

### Four checker corrections from the 2026-08-21 close review [since bd8fce68]

*(Anchored at the PRECEDING commit — this entry ships with the changes.)*

**Kit-owned files — overwrite and move on:** `scripts/gen_arch_map.py`,
`scripts/check_trajectory.py`, `scripts/spec_move.py`.

**1. A back-link declaration must now OPEN its line.** `Implements:` is read as
a declaration only when nothing precedes it on the line but whitespace, a
comment marker (`#`, `//`, `--`, `*`, `;`, `%`, `<!--`) or a quote. Two
docstring lines in the kit explaining that an id was *deliberately unclaimed*
were being harvested as declarations OF that id — a false link in a derived
artifact, sourced from the sentence denying it. **What you may notice:** a
declaration written after a summary sentence on the same line
(`"""Do the thing. Implements: LLR-001"""`) no longer counts, so
`--backlink-coverage` can report a lower percentage than before. The fix is to
put the token at the start of its own line; nothing else changes. Re-run
`python scripts/gen_arch_map.py --backlink-coverage --src <your src>` after the
re-sync and compare — this repo's own figure was unchanged (83/165).

**2. `docs/if-tc-coverage-allow` grows only with a reason.** The file gains one
machine-readable header key, `# seed-count: <int>`, naming how many entries are
the seeded baseline; every entry past that count must carry ` — <reason>` or it
declares nothing (the seam still errors), and allowlist hygiene reports the
growth either way. **What you may notice:** nothing until you add an entry — a
file with no `seed-count:` line has no baseline to grow past and behaves exactly
as before. When you seed yours, put the key in the header so future additions
cost a sentence, which is the whole burn-down discipline.

**3. A `;`-joined endpoint cell now declares every pair it names.**
`check_trajectory` read `scripts/a; scripts/b` as one module name where
`trace.py` split it, so a real cross-component seam could be reported as
undeclared while the row plainly named both modules. Strictly fewer false
findings; no action.

**4. `spec_move.py` recognizes directory intent.** A destination ending in `/`,
or naming an existing directory, now takes the source's filename rather than
writing a FILE named like the lane (which made the moved spec invisible to
registry discovery). A rooted or empty destination is refused loudly instead of
being guessed at. No action; if you scripted around the old behaviour by always
passing a full filename, that keeps working unchanged.

---

## 5. Promotion: when this pack stops being prose

This pack is deliberately **not** mechanized. Re-syncs are rare, every adopter is
inside the owner's own development sphere, and the LLM does the judgement work
under every design — so investing in what it reads beats investing in selectors
(the proportionality doctrine, SN-012). The honest cost is that nothing enforces
"a kit change that needed an entry got one": the obligation holds by attention.

**The promotion trigger, named so it is a decision rather than a drift:**

- the **first out-of-sphere adopter**, OR
- the **second observed drift incident** in this pack (the first, in the prose
  regime, was the `downstream-resync` skill's hand-maintained recipe copy going
  stale within weeks at zero re-sync traffic — caught by an audit, not by use).

Either event is evidence that attention has stopped being a sufficient enforcer.

**What promotion means.** Each entry lifts into a row of a shipped **migration
registry**: `since` SHA, a **detect probe** where one exists, the action, and a
pointer to the prose. Detection selects where it can; the SHA range selects the
rest. That lift is mechanical *precisely because* every entry here already carries
its `[since <sha>]` — the anchor is the column, so promotion is a transcription
rather than a re-derivation. The registry is only better than this document if its
**enforcer lands with it**; a registry no check enforces rots exactly like the
prose it replaced.

**If a detector ships early**, on its own, because some migration warrants one
anyway: record it in that migration's entry here. The kit already ships thirteen
detector-style migrations under a settled four-way taxonomy (auto-migrate,
degrade-gracefully, warn-only, hard-refuse), and none of them consults
`docs/kit-version` — each infers the repo's actual state from its artifacts, which
is why version-blind re-syncs have mostly survived. The two mechanisms compose
rather than compete.
