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
  scripts under `scripts/` (`trace.py`, `spine_rules.py`, `derive_stage.py`,
  `check_docs.py`,
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
  human-approval level, push authority, the reviewer count, the privacy and
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
  slots, and `.gitignore`/`.gitattributes` (merge new kit lines in by
  hand). (`docs/gate` was in this set until it RETIRED — see below.) `bootstrap.py` **skips existing files**, so a plain re-run won't clobber
  these — but don't run it with `--force` against a live repo without a diff pass.

Two classes have **exceptions that an entry states**, and the entry wins: a §3
entry may invert a standing rule for one file, and `docs/gate` is the case that
demonstrates both directions — an early migration required it to be
**regenerated** rather than preserved, and the final one **DELETES** it outright
(nothing derives or reads it any more; its successor is `docs/stage`, which is
generated and so is regenerated, never merged). Read the applicable entries
before applying the classes, not after.

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
history** it points at (the Sittings table, verdict blocks, approved
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

The re-sync ships the deriver and a `check.py --run-step derived-gate` step
(so re-sync `check.py` + the hook together). `docs/gate` is now **generated** from
the artifact states — it had to be regenerated once to migrate a legacy hand-set
value to the derived form (SUPERSEDED — see “`docs/gate` RETIRES” below: the file is DELETED at re-sync, not regenerated) (until you did, the
`derived-gate --check` step accepts the old one-line value **value-only**, so an
un-migrated repo is never broken). After migrating you stop bumping the line — you
approve artifacts (`Status` `Draft`→`Planned`, or an SN section move) in a reviewed
commit and regenerate (process-options.md "Derived gate model").

**Reconcile states against your approval history before trusting the migrated
value.** The derived gate believes your recorded `Status` values and SN sections —
but a legacy repo's registries usually contain artifacts added *after* the commit
that last set `docs/gate`, states no reviewer ever approved. Find that commit
(`git log --oneline -- docs/gate`), diff the requirement surfaces since
(`git diff <sha>..HEAD -- docs/requirements docs/test`), and stage everything
added or materially changed since per the new model — new stakeholder needs into a
`## Draft needs (unapproved)` section, not-yet-re-reviewed SRs to `Status=Draft` —
so `spine_rules.py` reproduces the gate your history actually attests instead of
laundering post-attestation additions into it. If the derived value still
disagrees with your old hand-set line after that, **the disagreement is the
finding**: approve (or demote) deliberately before relying on the derived gate.

### The phase model, and the retired grouping column [since 6daee92f]

The delivery `Phase` is now a field on the LLR and TC registries too (it was
SR-only), and the work-item registry **drops** its old per-WI grouping column (the
one the dashboard used to bin the roadmap by — it now tiers
`phase ⊃ workstream ⊃ work-item`). Both changes are **vacuous-until-armed**, so a
re-sync is diffable and never breaks: a registry with no phased row keeps
`trace.py`'s approved-Phase schema rule dormant (blank = in scope for every
phase), and any leftover grouping column is simply ignored (read by name, no
vocabulary rule).

### `--require-verified` widened to method-blind [since a686bcc8]

The DevStg-Impl traceability floor `trace.py --require-verified` now demands
`Status=Verified` for **every** approved, in-phase SR regardless of its
`Verification` method (was `Verification=Test` only), matching
`spine_rules.sr_gate` — which already blocked DevStg-Impl for any unverified decomposed SR.
**Downstream impact:** a repo passing `--require-verified` today with a non-Test SR
(Demonstration / Manual / Analysis / Inspection / Attest / Critique) still below
`Verified` will now fail — it was never actually at the derived gate, only
reporting so. To re-sync: set those SRs to `Verified` once acceptance is met
(attach the TC evidence / recorded attestation), or mark them `Draft` if not yet
approved. The verification-basis report is now three-way (mechanized /
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
the old pending block was a POINTER ("run `trace.py --approve modified`"), and the
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
flip, and `trace.py --approve modified` emits a per-cell before/after brief against
the git-derived attested baseline. Never breaking for a registry that never writes
the value — with one **flagged migration**: the `docs/gate` `# basis:` line now
carries `modified=N` beside `drafts=N`, so the first `check.py`/pre-commit run
after re-sync reds the `derived-gate` freshness step once. The fix was to
regenerate and commit `docs/gate` (SUPERSEDED — see “`docs/gate` RETIRES” below: the file is DELETED at re-sync, not regenerated).

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
pending approval drains the lanes and exits 0 naming the cards in
`open-items.html` instead of refusing nonzero. The worker-lane count is a new
declared dial — `lanes` in `docs/stack.ini [agent-loop]` (CLI `--lanes` >
`AGENT_LANES` > stack.ini > default). **An absent key means 1**: your repo stays
exactly as serial as it was until you add the line (fresh scaffolds seed
`lanes = 2`); no re-sync ever changes your lane count, because `docs/stack.ini` is
yours.

### `Phase` is numeric-only once armed [since e0623526]

Once any row is phased, a *approved* SR/LLR/TC `Phase` must be a **full-cell bare
integer** (`1`, `2`, …) — a prefixed label (`v2`, `P1`) is now a `--strict-schema`
finding, because the `--phase`/`--approve` filters and the phase-drop detector match
the cell literally and a prefixed cell disarms them silently. A `vN` label still
digit-parses in those filters and the derived current phase (grandfathering), so a
`vN` registry **arms the rule and now fails it**: strip prefixes (`v2` → `2`)
across approved rows when you take this kit version — a mechanical, diffable edit
(`Phase` is a *traced* cell, so no re-attest window opens). Once you phase any row,
phase every *approved* SR/LLR/TC — blank stays legal on `Draft` rows only — and the
foundation (minimum) phase stays in scope under `--phase`.
`derive_stage.py --next-phase` prints the number a newly confirmed phase takes.

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
`docs/process.toml`, then, **from your kept kit checkout** (not your own repo —
`bootstrap.py` is kit-side and is never scaffolded into an adopting repo, unlike
every other `scripts/…` command in this pack), run
**`python project-trajectory/scripts/bootstrap.py --migrate-config --dest .`**.
It folds every legacy
file it finds into the matching key, **deletes that file**, and is idempotent — and
a full `bootstrap.py --dest .` scaffold pass (also run from the kit checkout)
runs it for you. Two dials change
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
a rule a passing prose mention of an id could trip, silently un-approving a need.

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
`docs/gate` path, `spine_rules.py`, `check.py --gate`, "the freshness gate". Only
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
   six-integer one. That cache had to be regenerated once (SUPERSEDED — see “`docs/gate` RETIRES” below: the file is DELETED at re-sync, not regenerated). There is **no compat shim** — `--check` reported the old cache STALE on
   the first recompute, deliberately, because a reader that accepted both
   vocabularies is how the retired tags grow back. The failure direction is safe:
   a stale cache makes the stage unreadable, and an unreadable stage is treated
   as **human-held**, so the one state it can produce is *more* human
   involvement.
2. **Re-apply your `docs/process.toml` dials.** `human_approval_through`
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
   passes. From your kept kit checkout:
   `python project-trajectory/scripts/bootstrap.py --dest . --sync`.

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
  `spine_rules.boundary_incomplete` used to read `interfaces.toml` and cap you
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
  was a MATURITY claim (the contract has settled) and `approved` is an
  APPROVAL one. The kit's own registry mapped all 113 rows to `draft`
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
error above) and its approved-cell classification are all GONE, on the ruling
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
can land it in pieces. Nothing was deleted here: `direction`, `this_project` and
`counterpart` all stay, and so do your `Consumes` rows. **All three DID go
later** — see *The interface tier sheds `direction` and renames its endpoints*
below; if your range covers both, read them in order, because this entry is what
makes that one's derivation possible.

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

**`Status` is now a CLOSED vocabulary on the spine — `{Draft, Planned, Modified, Verified}` for SR, LLR and TC — and an out-of-vocabulary value is an INTEGRITY finding**, which means it reds `trace.py --strict-integrity` and the pre-commit hook at every gate, not just at DevStg-Impl. This is the one entry here that can break a repo on the re-sync itself. If your LLR or TC rows carry maturity words of your own (`Implemented`, `In-Review`, …) — which the kit's own prose invited until now — map them onto the four before you take this. `Planned` is the closest fit for "approved, not yet Verified"; the derived gate reads LLR/TC status only for `Draft`, so the mapping does not move your bar. Why the closure: the `Status` ladder D-9 is heading for renames these values, and a retired word that no predicate recognizes vanishes SILENTLY from the re-attest brief — an open vocabulary has no way to say "this row was left behind".

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
- **`intake.py snapshot [--seed]`** — the human path. At an approval sitting:
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

**DELETED, and you must stop passing it:** `trace.py --approve modified --since
<rev>` and `gen_open_items.py --since <rev>`, plus the
`<!-- attestation-baseline: … -->` stamp the generated view carried. They
existed to override or reproduce a git-derived baseline that a regeneration
could move. A snapshot cannot sit after the amendment it precedes and is
identical on every machine and in CI, so there is nothing to override and
nothing to reproduce. A script or CI job passing `--since` now fails on an
unrecognized argument — which is the loud direction.

**One behaviour change worth expecting.** `trace.py --approve <scope>` now
REFUSES a scope that matches no SR instead of emitting an empty brief at exit 0.
If you have a job that approves a phase tag which no longer exists, it will
start failing; that is the point, because the empty brief it used to produce
read as *"there is nothing to approve"* to the human about to sign it.

### The `Status` ladder RENAME: `Draft`→`Drafted`, `Planned`/`Verified`→`Approved` [since 3771c003]

The successor to the entry above, and the one that moves **cells**, not just
machinery. The enum narrows from four values to three — `{Drafted, Approved,
Modified}` — and it is enforced on the always-on `--strict-integrity` floor, so
an unmigrated cell is a hard finding on your very next commit, not a silent
inertness. **Order matters; each step below is a separate failure if skipped.**

1. **The value map, applied to every SR/LLR/TC `status` cell.** `Draft` →
   `Drafted`; `Verified` → `Approved`; **`Planned` → `Approved`**. The third is
   a FOLD, not a rename: `Planned` (text approved, evidence pending) and
   `Verified` (text approved, evidence established) named one rung once the
   vocabulary stopped making a pass claim, so they collapse. Matching stays
   case-insensitive, so casing in your cells is not the issue — spelling is.
2. **The off-spine approval cells:** `approval = "draft"` → `"drafted"` in
   `docs/requirements/interfaces.toml` and `external.toml` (the `approved`
   spelling is unchanged). One word, one meaning, across every registry.
3. **The predicate renames, if you patched or imported them:** `is_draft` →
   `is_drafted` (in `trace_text.py`, re-exported by `trace.py`), `is_verified` →
   `is_approved` (in `trace.py` AND `spine_rules.py` — they are F5 duplicates
   and both move). **`is_planned` is DELETED, not re-keyed**; every site that
   read it now reads one of the three live predicates.
4. **The templates.** Overwrite `registries/*.template.toml`: the SR and TC
   examples now ship `status = "Drafted"` and the LLR example `status =
   "Approved"`. A scaffold created before this change still ships the retired
   words in its `-000` rows; those rows are placeholder-exempt from the
   integrity rule, so nothing fails — but leaving them means your template
   teaches a vocabulary the checker refuses.
5. **THE ONE THAT BITES SILENTLY — the `# basis:` line format.**
   `spine_rules.py` now emits `drafted=N` where it emitted `drafts=N`, and it no
   longer emits `planned=N` at all. Any consumer that parses that line by regex
   must move in the same commit or it goes BLIND rather than red — the kit's own
   `check._BASIS_RE` did exactly this once and twelve gate steps stopped running
   for twelve commits before anyone noticed. If you have local tooling reading
   `docs/gate`'s basis line, grep it for `drafts=` and `planned=` first.
   Regenerating `docs/gate` was required regardless, because `--check`
   compared the line whole (SUPERSEDED — see “`docs/gate` RETIRES” below: the file is DELETED at re-sync, not regenerated).

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
   `spine_rules.CMP_MATURITY` is now the identity over the one enum
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
without moving any of them. The kit verified that by asserting its `spine_rules`
basis line was **byte-identical** before and after. If your registries carry
approved or verified rows, you do not get that check for free — apply the value
map above deliberately, and re-run `spine_rules.py` to compare.

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
approval, the sweep is a provisional act your sitting countersigns.

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
`status-map`, `open-items`, `derived-gate`, `approval-fresh`, `skills-sync`,
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
   recognized — `is_founded` in `trace.py` and `spine_rules.py` (F5 duplicates,
   both move), a `SPINE_MATURITY` row mapping it ABOVE `Approved`, and every
   blessed-text reader accepting it (`--require-verified`, `spine_stage`'s
   Impl→Release discriminator, the LLR-status advisory's exemption). **No cell
   moves to it in this step**, exactly as it armed for `components.toml`. Nothing
   WRITES it: whether a tool ever should, and whether a hand-authored `Founded`
   is itself an error, is still open (D-9 consequence 2).
3. **THE ONE THAT BITES SILENTLY — the `# basis:` line loses `modified=N`.**
   `spine_rules.py` no longer emits the field. The kit's own `check._BASIS_RE`
   was made to treat it as OPTIONAL in the same commit, so a gate file that still
   carries one keeps the window detector's conclusive arm; **local tooling that
   REQUIRES the field goes blind rather than red.** Grep any consumer of
   `docs/gate`'s basis line for `modified=` first. Regenerating `docs/gate`
   was required regardless, because `--check` compared the line whole (SUPERSEDED — see “`docs/gate` RETIRES” below: the file is DELETED at re-sync, not regenerated).
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
   DELETED, not re-keyed, in BOTH `trace.py` and `spine_rules.py`.
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

### `kitlib/ladder.py` — the eight-rung stage vocabulary gets one home [since f23e6002]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**A sixth module in `scripts/kitlib/`, and the same copy-it-whole rule.** The
`DevStg-*` rung labels, their ladder order, the derived rung count, the
per-rung descriptions and `stage_ord` (the only legal way to compare two
stages) now live in `scripts/kitlib/ladder.py`. They used to be defined in
`scripts/spine_rules.py` and RESTATED as literals in `scripts/agent_common.py`
(pinned equal by a test) and `scripts/traj_status.py` (pinned by nothing at
all), which is three places a reworded or inserted rung had to be edited in
step.

**If you only overwrite kit files, you need do nothing but include the new
module in the copy.** `spine_rules.STAGE_ORDER`, `spine_rules.STAGE_DESC`,
`spine_rules.STAGE_NEEDS` … `spine_rules.STAGE_RELEASE`, `spine_rules.STAGE_OF`
and `spine_rules.stage_ord` are all still there and still resolve to the same
values; they are re-exports now. No call signature changed, no derived value
changed, and `docs/gate`'s `# basis:` line is byte-identical for an unchanged
spine.

**If you import those names yourself**, prefer `from kitlib.ladder import
STAGE_ORDER` going forward. The re-exports are kept, not deprecated — but a
tool of yours that needs the rung vocabulary should not have to load the gate
derivation engine to get it.

**If you have your OWN copy of the rung strings** — a script, a renderer, a
template filter that spells out the eight labels or their descriptions — this
is the moment to delete it and import instead. That is exactly the drift this
change removes inside the kit, and the copy the kit had gone unpinned in a
renderer, where a stale sentence shows up as wrong output rather than as a
failing test.

**One error-message note.** `stage_ord` on an unknown label still raises
`ValueError`; the message now reads `kitlib.ladder: …` where it read
`spine_rules: …`. Only a test asserting on that prefix would notice.

**Nothing in your `docs/` changes**, and no registry cell moves. The bar
vocabulary (`BAR_*`, `docs/gate`'s value itself) is untouched by this entry.

### `docs/stage` + `derive_stage.py` — the effective stage gets its own derived file [since 87bd45dd]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**A new generated artifact, a new script, a new `kitlib` module, and a new
`check.py` step. `docs/gate` is UNCHANGED and still authoritative for everything
that reads it** — the two files run side by side deliberately while the readers
are cut over in a later change. Nothing you have breaks on this entry.

**Copy in, then run once.** Take `scripts/derive_stage.py`,
`scripts/kitlib/stage.py`, the updated `scripts/check.py`, `scripts/trunk_step.py`
and `hooks/pre-commit`, and — if you scaffolded before this entry and have no
`docs/stage` — `stage.template` copied to `docs/stage`. Then:

```
python scripts/derive_stage.py
git add docs/stage
```

**This overrides §1's preserve-classes rule for one path**: `docs/stage` is a
generated cache, so it is REGENERATED, never merged — the same directive
`docs/gate` already carries.

**If you skip the run:** the new `derived-stage` step passes with a note while
`docs/stage` is still the comment-only placeholder (there is nothing for it to be
stale against yet), and FAILS if the file is absent entirely. So a fresh scaffold
is green; a repo that deleted the file is loudly told which command to run. It is
never silently green over a stale record.

**What the file says, and why it is not just `docs/gate` again.** The headline
`stage =` is the EFFECTIVE stage — the rung your SETTLED spine has earned, folded
per phase and floored — where `docs/gate`'s `# basis:` line carried only the raw
live reading. The practical difference: one newly Drafted requirement no longer
drops the reported stage to what a fresh scaffold reads. The honest live value is
still there beside it (`live-stage =`), with the per-phase breakdown and the draft
count, so nothing is hidden — the derived reading is shown BESIDE the honest one,
which is the rule process.md §4 has always stated.

**`fingerprint =` is the part worth knowing about.** It is a SHA-256 over the
LF-normalized content of the declared derivation inputs — your spine registries
and `docs/process.toml`, a list stated once in `kitlib/stage.py`. Any reader
recomputes it and trusts the recorded record only on a match, deriving fresh in
memory otherwise. Consequences for you: the value is correct on a work branch even
though the freshness step stands down there, and it is correct mid-session after
you approve something and before anyone regenerates. Readers never WRITE the file —
regeneration stays `trunk_step.py --regen` and your own explicit run.

**If your registries live in CSV rather than TOML**, nothing changes: the input
list resolves by carrier exactly as the derivation does, and which carrier
answered is part of the fingerprint.

### `check.py` selects AT OR ABOVE the derived stage — the bar axis leaves selection [since 1a7984ea]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**THIS ONE CHANGES WHICH CHECKS RUN IN YOUR CI. Read it before you take the
files.** Everything else in this range was additive; this is not.

**The rule.** A step used to run because its `gates=` tag CONTAINED the derived
bar — set membership. It now runs because your repo's stage is **at or above**
the single rung the step declares. `check.py` reads `docs/stage`, not
`docs/gate`, and the three readers it had of the latter (`resolve_gate`,
`window_open`, `product_floor`) are gone.

**What you must expect to start running.** Under the old axis the derived bar
was a MIN over every in-scope row and was CEILINGED at `DevStg-Tests`, so the
steps tagged `{DevStg-Impl}` — **`format`, `lint`, `tests+coverage`, and any
`[step:*]` of your own that took the default** — could not be selected by a
derived value **at all**, on any repo. If your spine is fully decomposed and
settled, they select now. That is the defect this change exists to fix, and the
honest consequence is that a repo whose product checks have been quietly
skipped in CI will go red on the first run. **Run `check.py --list` before you
push** to see the plan you are about to get.

**What can no longer stop running.** Drafting a requirement used to drop the
derived bar to what a fresh scaffold reads, which removed steps; a
compensating "product floor" and a warn-only "advisory tier" existed for that.
The effective stage is derived over your SETTLED spine, so drafting cannot lower
selection at all — for any step, not just the product ones. Both compensating
mechanisms are therefore deleted, and their disappearance costs you nothing: what
they ran warn-only now gates.

**One step changes when it runs rather than whether:** `registry-integrity` was
tagged `{DevStg-Reqs}` alone and now runs at every rung. It is a cheap read-only
pass, and a structurally broken registry is unreadable at every rung.

**Your `[step:*]` sections: `gates =` becomes `from-stage =`.** The new key takes
ONE rung of the eight-stage ladder and means "from here up". Your existing
`gates =` lists keep working and are translated on read, with one notice per run
naming the section — but the translation is not the span floor you might expect:
`gates = DevStg-Tests` becomes `from-stage = DevStg-Impl`, because the
`DevStg-Tests` BAR was only ever reached by a fully decomposed spine, which is
the `DevStg-Impl` RUNG. Migrating by hand means opening that judgement, so prefer
the translation unless you know the step's real prerequisite.

**The flag.** `--stage` is the canonical spelling. `--gate` keeps working
**silently and indefinitely** — it is a flag name your hooks and CI pass
literally. `--stage-cleared` also keeps working but now prints one deprecation
line per run: unlike `--gate` it makes a claim about the axis ("a bar being
cleared") that this change retires. The VALUE spellings are unchanged and the
retired `G1`/`G2`/`G3` and `DevBar-*` aliases still translate with their warning;
what changed is the reading — `DevStg-Tests` now says "the repo is at that rung",
not "that bar must next be cleared".

**Take:** the updated `scripts/check.py`, `scripts/spine_rules.py`,
`scripts/integrate.py`, `ci/check.yml`, `stack.ini.template`, and the `setup.*` /
`check.*` launcher scripts. **`docs/gate` is still generated and still
freshness-gated** — the phase-drop and tier-signal detectors read its committed
history, and it retires in a later entry, not this one.

### Terminal WI history moves to `docs/archive/work/` (WI-504, OI-55 ruled (a)) [since d6818b0b]

`docs/work/{complete,cancelled,partial}/` relocate WHOLE to
`docs/archive/work/{complete,cancelled,partial}/`, one directory deeper — so
`docs/work/` holds only rows still in flight (`draft/`, `queued/`, `active/`,
`deferred/`) and an agent listing the registry meets the frontier, not hundreds
of closed rows. Status stays directory-encoded; nothing about a closed row's
STANDING changed, only its parent directory. `docs/handbacks/` (the per-close
report home) did **not** move — it was never nested under `docs/work/` to begin
with (SR-144's own reasoning: a report living there would be walked by
`spec_files`, raise on its undeclared directory, and be silently skipped by
every reader while its id counted as taken by the mint).

**Readers are taught first, so both roots are honest.**
`kitlib.registry.read_spec_rows` (and, through it, every consumer —
`schedule.py`'s done-set, `check_trajectory.py`'s registry, `agent_common.py`,
`intake.py`'s dedup) unions `docs/work/` and its `spec_roots` archive sibling
into ONE registry; a repo that has not yet moved its own terminal population
still reads correctly, because the union degrades to "whichever root actually
holds the file." Take the updated `scripts/kitlib/registry.py`,
`scripts/check_trajectory.py` (`_head_spec_status_map` now scans both prefixes
so a close INTO the archive is still visible to the staged-registry ratchets),
`scripts/integrate.py` (`branch_outcomes` reads both prefixes, and
`docs/archive/work/` joins `_ADJUDICATION_SURFACES`), and `scripts/intake.py`
(`_terminal_hits` — the by-hand recovery sweep, the disposition-mint arm, the
spot-check arm, and the id-mint's filename sweep all read both roots now).

**Migration recipe, one commit:**

```
mkdir -p docs/archive/work
git mv docs/work/complete   docs/archive/work/complete
git mv docs/work/cancelled  docs/archive/work/cancelled
git mv docs/work/partial    docs/archive/work/partial
```

Then, in the same commit: (1) run the link sweep — every committed doc that
links INTO a moved spec (a log fragment, a review, a README) needs its target
re-pointed one directory deeper; `scripts/spec_move.py`'s
`_rebase_moved_spec_links` / `_relink_inbound_links` primitives do this given
the `(old, new)` path pairs the `git mv`s above produce — and re-run
`check_docs.py --stale` until it is clean; (2) drop a short tombstone
`README.md` into each now-empty `docs/work/{complete,cancelled,partial}/`
pointing at the new home, so a link written against the old path resolves to an
explanation instead of a 404; (3) re-point `docs/orphans-allow`'s
`docs/work/*`-adjacent entry to also cover `docs/archive/work/*` (both stay
declared — the old glob still covers the four open-state directories); (4) if
your repo carries `check_vocab.py`'s `EXEMPT_GLOBS`, the generic
`docs/archive/*` row already covers the new home, so any repo-local
`docs/work/{complete,cancelled,partial}/*` rows are now dead and should be
deleted rather than left pointing at directories that hold only a tombstone.
**Do not rewrite old paths inside `docs/log.md` / `docs/log.d/*` / review
records** — those are historical citations of where a thing lived when the
record was written, not a live index.

**Take:** the updated `scripts/kitlib/registry.py`, `scripts/check_trajectory.py`,
`scripts/integrate.py`, `scripts/intake.py`, `scripts/check.py` (the
doc-navigability `--ignore` list gains `docs/archive/work/*`, mirroring the
existing `docs/work/*` row — a closed spec's body is DATA, not navigable
prose, wherever it lives), `scripts/bootstrap.py` (a **fresh** scaffold ships
the new shape directly — `docs/work/{draft,active,deferred}/` plus
`docs/archive/work/{partial,cancelled,complete}/`, no migration needed), and
`orphans-allow.template` / `work/README.template.md` / `work/WI-000.template.md`.

### The worker brief gains a standing-state clause [since 7507c569]

`prompts/worker.template.md` (kit-owned, no override) gains one Rules bullet:
before spending effort on heavy verification, the worker session starts its
`docs/log.d/<WI-id>-<slug>.md` fragment and lands the spec's own
`## Context`/`## Deliverable` edits in a commit, and keeps both current as the
session continues rather than writing them once at the end. This is prose
only — no new slot, no loop-side change — because the relaunch half already
works off committed branch state: `worker_prompt`'s `diff_block` recomputes
the branch's own accepted-not-yet-reviewed commits fresh at every launch, so a
session killed mid-verification already hands the next one its own diff; the
only gap was that nothing told the worker to make that diff resumable *before*
the long stretch of verification that might kill it. **Take:** the updated
`prompts/worker.template.md` (your repo's copy is kit-owned and gets
overwritten on re-sync the same way the reviewer/critique briefs are — a
locally forked worker brief must reapply this clause by hand) and the
regenerated `prompts/CATALOG.md` (`gen_prompt_catalog.py`, `--check` fails
until you do).

### `check_docs.py` blanks HTML comments before the inline-code strip [since 59f52549]

A lone backtick inside an HTML comment used to open an inline-code span that
swallowed headings for thousands of lines — 226 of one compiled log's 555
headings vanished from the anchor set, and every `#anchor` link into the range
read as broken. Comments are now blanked to a single space before the
inline-code strip (a comment QUOTED inside inline code keeps its backticks).
**Take:** the updated `scripts/check_docs.py` on re-sync; nothing else moves.
The change only widens what resolves — a repo that was green stays green.

### An opencode registry row needs `--dir .` [since 59ab2951]

An ADOPTER-SIDE check, not a file to take: the kit's own
`agents.template.toml` ships no opencode row, but if your `docs/agents.toml`
carries one, `opencode run` resolves its project root by walking UP from the
cwd — from a lane worktree it lands on the MAIN repo and the session reads
the wrong tree (a reviewer drawn on a lane reviewed trunk, live, 2026-08-30).
Add `--dir .` to the row's `cmd_template` (`opencode run --dir . -m {model}
--auto`); the session engine runs every child with `cwd=<worktree>`, so `.`
is always the lane.

### The stall-guard change set: exit 9, the idle deadline, the probe, the relaxed rung, the close rituals, the brief slots [since 959c5996]

A reviewer outage no longer closes finished work `partial` (the 2026-08-30
incident class). Six contract-visible pieces ship together; the scripts and
prompts are kit-owned copies, so a plain re-sync takes them — what needs YOUR
attention:

1. **Exit code 9 (`EXIT_REVIEW_OWED`)** joins the loop's alphabet (appended at
   the end; 10 stays retired). A wrapper of yours that switches on worker exit
   codes must treat 9 as *parked, resumable* — like a crash, never a decided
   outcome.
2. **The launchers gain `AGENT_SESSION_IDLE_TIMEOUT`** (default 900 s; blank =
   engine default, 0 disables) beside `AGENT_SESSION_TIMEOUT`, passed as
   `--session-idle-timeout`. The launchers are near-verbatim copies — re-take
   them, or add the slot + flag to your edited copy by hand (structural parity
   is what `test_dogfood_sync` pins in the kit repo). An unedited launcher
   still gets the engine default: silent hangs are killed ~15 min after their
   last output line instead of at the wall.
3. **The reviewer brief carries three slots now** — `{verdict}`, `{trunk}`,
   `{process_doc}` — rendered by the loop. A `--prompt-map` override file of
   yours keeps working (missing slots render unchanged), but consider adopting
   the new reading-scope text: three-dot diff against the current trunk with
   telemetry/generated exclusions, summary-only harness reads.
4. **The worker and adjudicate-disposition briefs state the close ritual**
   (Deliverable before Context, specref cleared, `spec_move.py`, the `WI:`
   trailer; the adjudicator closes its OWN row). Without it, a mechanized lane
   parks its finished spec in `active/` forever.
5. **`integrate` unload sheds the loop's own `out/run-logs/` streams and the
   `out/review-owed` marker** as declared residue (their clipped copies are
   tracked under `docs/iteration/`). If you relied on the unload refusing over
   a session stream, that refusal is gone — anything else in the worktree
   still refuses by name.
6. The same-family review fallback is legal AND recorded (`-relaxed` verdict
   filename, `heterogeneity: relaxed` telemetry); a single-family roster was
   always same-family — now it says so. The 30 s liveness probe runs only on
   routes that already failed this run.

### The `blockref` vocabulary retires; the hold-by-rename ban is mechanized [since a024e766]

(Anchored at the preceding kit commit — the WI-553 change lands just after it,
so there is no merge SHA to name yet.)

Two kit-owned changes, both taken by a plain re-sync of the scripts; what needs
YOUR attention is one schema column and one new check.

1. **The `BlockRef` column leaves the WI registry schema.** It fed
   `pending.blocked_pending` — a "blocked" owner-surface line derived from a
   `queued/` spec carrying a `blockref` — but nothing has PRODUCED one since a
   stopped lane began closing to the terminal `partial/` (LLR-161), so OI-70
   retired the field, the canonical column (`kitlib.registry.WI_COLUMNS`), and
   the derivations that read it. The loaders are TOLERANT: a registry still
   carrying a `BlockRef` column reads clean (the column is ignored), so this
   migration is optional — drop the column from
   `docs/requirements/work-items.csv` (and any folder-spec `blockref`
   frontmatter key) at your convenience. The `blocked` STATUS word survives in
   the lifecycle vocabulary; nothing mints it now. Distinct and UNCHANGED: the
   `Blocked-WI:` / `BlockRef:` git COMMIT TRAILERS a worker uses to signal a
   block are a different instrument and stay live.

2. **A new harness check reports a ref-less active claim.** `check_trajectory`
   now names any `docs/work/active/<branch>/` claim directory with no matching
   `refs/heads/<branch>` — the signature of a hold-by-rename, which OI-70 BANS
   (a lane must close PARTIAL, never park by renaming its ref). WARN at the
   commit bar, ERROR under `--strict` (the DevStg-Impl gate); silent off-git. If
   your repo carries a stranded active claim, close it partial or delete the
   directory.

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
(`docs/gate`, `spine_rules.py`, `--gate`, "the freshness gate" all stay).

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
`spine_rules.py` **keep their names** for the same reason.

**What to do:** take the kit-owned scripts wholesale, then `grep -rn 'DevBar-'`
your own prose, `docs/stack.ini` and CI. Convert at your pace — and if you keep
a hand-written `docs/gate`, note that it regenerates: `python
scripts/spine_rules.py`. `scripts/check_vocab.py` now refuses the prefix in
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
APPROVED text into `docs/archive/last_approved/` unless one of three things is
true — the copy absorbs nothing approved (a `Module`/`CodeSymbol`/`TestRefs` or
ref-pointer refresh, the common case, unchanged and free); a `Status` cell moved
in the same registry (amend-plus-flip IS approval); or you pass
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
bar, `DevStg-Tests` — `ex-draft` can never exceed it while `spine_rules`'s
release ceiling stands — and it selects by MEMBERSHIP, while `[product]`
format/lint/test are tagged `{DevStg-Impl}` only. So the floor cannot reach
those three, and it holds nothing at all unless you have written both
`gates = DevStg-Tests` and `layer = product` into a `[step:*]`. Whether the
three built-ins should be reachable is a live owner question (`OI-51` in the
kit's own registry); until it is ruled, do not read this entry as covering
them, and do not expect the red the next paragraph describes unless you have
declared such a step.

**What you may notice:** if you have a `[step:*] layer = product` declared at or
below the bar your approved rows have earned, it now **gates** during a draft
window where it previously ran advisory (warn-only) or not at all. If that step
has been failing quietly, your first push after this re-sync reds. That is the
change working: the failure was already there, and the exit code was not
reporting it. There is deliberately no dial to switch the floor off.

**Nothing in your `docs/` changes.** No registry cell moves and no regeneration
is needed; a `docs/gate` written before the `ex-draft=` field existed simply got
no floor (the floor abstained rather than guessing) until the next regeneration
(SUPERSEDED — see “`docs/gate` RETIRES” below: the file is DELETED at re-sync, not regenerated).

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

**Cell classification, if you run the approval ladder:** `Hat-Refs` is
declared **traced**, not approved (`check_trajectory.SPINE_TRACED_CELLS`), so
adding it to an already-approved row does not arm a re-attest window or trip the
`last_approved` drift comparison — the drift basis reads the approved half only.
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

### A settled spine now reads `DevStg-Impl`; `DevStg-Release` is evidence-gated [since d4a8d27a]

*(Anchored at the PRECEDING commit — this entry ships with the changes.)*

**Kit-owned files — overwrite and move on:** `scripts/spine_rules.py`,
`scripts/derive_stage.py`.

**YOUR DERIVED STAGE CAN CHANGE VALUE AT THIS RE-SYNC, with no edit to your
registries.** A repo whose requirements are all `Approved` or `Founded` through
the test tier used to derive `DevStg-Release` — rendered as *"nothing in work;
release checklist available"*. It now derives **`DevStg-Impl`**, *"implementation
in work"*. Nothing about your project changed; the ladder's top was
discriminating on the wrong side. The old reading said "finished" for the entire
stretch during which a team is actually building the thing.

Read the new rungs this way:

- **`DevStg-Impl`** — the requirements are broken down and the test cases are
  LAID. Making them pass is the work in progress. This is where a healthy
  project sits for most of its life.
- **`DevStg-Release`** — every declared test case PASSES. **Nothing derives this
  rung today.** It needs a machine reading of test outcomes, and the kit has
  none: a `Status` cell may never claim the evidence passed (that rule is
  unchanged and long-standing), and no results artifact is joined back to test
  ids yet. The rung is deliberately unreachable rather than quietly approximated.
  When the evidence carrier lands, it becomes reachable honestly.

**What you may notice.** Under at-or-above selection, `DevStg-Impl` is the
threshold for the product steps (`format`, `lint`, `tests+coverage`,
`perf-budgets`, `backlink-coverage`, the generated-view family), so a settled
spine still selects all of them — the value moved, the selection did not. Your
dashboard and `docs/status.md` will render the new sentence after the next
regeneration. If you had a repo genuinely reading `DevStg-Release`, it will now
read one rung lower and no check will stop running.

**New, and warn-first: the phase rule.**
`python scripts/derive_stage.py --phase-rule` checks one authoring-time rule
against `HEAD` — *a spine edit that LOWERS the effective stage must surface as a
phase change.* Every row the edit added or re-statused has to carry a `Phase`
tag that is not the phase the settled work was standing in: a new (higher)
phase, or an already-open lower one. Exactly one decrease is exempt —
`DevStg-LLReqs → DevStg-Arch`, the permitted decomposition cycle, since
architecture rework surfaced by breaking a requirement down is within-phase
churn. It **warns and exits 0**; `--strict` exits 1. It is not wired into
`check.py` and cannot block a commit, so **no action is required at re-sync** —
run it if you want the signal. Without git it degrades silently.

### A dead adjudication signal comes back to life; the phase-drop detector re-keys [since ae4f6bce]

*(Anchored at the PRECEDING commit — this entry ships with the changes.)*

**Kit-owned files — overwrite and move on:** `scripts/intake.py`,
`scripts/check_trajectory.py`, `scripts/kitlib/stage.py`,
`scripts/kitlib/config.py`, `scripts/agent_common.py`, `scripts/check.py`.

**A MECHANISM THAT HAS BEEN SILENTLY DEAD IN YOUR REPO STARTS FIRING.**
`intake.py` mints an adjudication row when a merged commit amends an approved
spine cell, and it grades that row `strong` (deeper review) when the amendment
moved the repo's derived stage. The stage half of that test has been broken
since the gate became a generated file: it compared the FIRST LINE of
`docs/gate`, which is the static "do not hand-edit" header and is identical at
every revision. So the answer was always "no move", and `strong` was reachable
only by touching more than three rows at once. It now reads the `stage` field of
`docs/stage` at the two commits.

**What you will see:** occasionally an adjudication row that used to arrive
`buildtier = "medium"` now arrives `strong`. That is the tier the amendment
always warranted. Nothing about the mint's trigger changed, so no NEW rows
appear — only some existing ones are graded higher. If you route `strong` rows
to a heavier review lane, expect a little more traffic there.

**The phase-drop detector now reads the stage axis.** `check_trajectory.py`'s
warn-first check — *a phase dropped below the level its own closed anchor
recorded* — used to read `docs/gate`'s `# basis: per-phase=` line and now reads
`docs/stage`'s `per-phase-live` through the common reader. Three consequences:

- **Your closed phase anchors keep working, untouched.** A phase anchor is a WI
  title (`[v2]-[g1]`, `[v2]-[reqs]`, …) and those are committed history. They
  are TRANSLATED on read, by meaning rather than by spelling: `[p]-[reqs]`/`[g1]`
  records that the phase reached **`DevStg-LLReqs`**, `[p]-[tests]`/`[g2]` that
  it reached **`DevStg-Impl`**. Note both are two rungs off the word — `reqs` is
  the rung the phase LEFT, not the one it landed on.
- **New anchors take the rung itself:** `[<phase>]-[DevStg-LLReqs]`,
  `[<phase>]-[DevStg-Impl]`, or any other rung. One vocabulary, and a title that
  says which rung it means. The old spellings are accepted forever.
- **It now ABSTAINS instead of blaming a phase for a repo-wide fact.** Three
  rungs — `DevStg-Needs`, `DevStg-Boundary`, `DevStg-Arch` — are decided by your
  need, external and component registries, which are read whole for every phase.
  While one of those holds, every phase reads that rung at once and no drop can
  be attributed to any one of them. You get ONE warn saying the detector stood
  down, naming the rung and the phases, instead of a false drop warn per phase.
  If your component registry has drafted rows, this is the state you are in, and
  the detector resumes when the frame settles.

**`docs/gate` is still generated and still freshness-gated.** Four readers
remain — three display surfaces and `agent_common.spine_stage_of`, which feeds
approval authority — and it retires with them in a later entry.

**One documentation correction with no behaviour attached:**
`kitlib.config.read_declared` was described in two places as the reader for
`docs/gate`. No call site has ever put it to that file. The function is
unchanged; only the false claim is gone.

### `docs/gate` RETIRES; the stage becomes the one axis; the dial re-keys [since 2a0a85a4]

*(Anchored at the PRECEDING commit — this entry ships with the changes. It is
the LAST entry of the WI-498 stage-unification program and is written so the
whole re-sync can be executed from this entry alone; the six entries above it
land the machinery in stages, this one lands the migration.)*

**Kit-owned files — overwrite and move on:** every `scripts/*.py`,
`project-trajectory/PROCESS.md`, `PROCESS_OPTIONS.md`, `ADOPTING.md`,
`README.md`, `skills/gate-advance/SKILL.md`, `process.toml.template`,
`gate-policy.template`, `stack.ini.template`, `ci/check.yml`, `hooks/pre-commit`.

**Two files change NAME, and a rename reads to a diff as an unrelated deletion
plus an unrelated addition (§4's warning, in force here):**

| was | is | note |
|---|---|---|
| `scripts/derive_gate.py` | `scripts/spine_rules.py` | it derives no gate and writes no file; what survives is the row predicates and the rung fall-through. **No `main()`** — anything that ran it as a command must move (see below) |
| `docs/gate` | `docs/stage` | already shipped by an earlier entry; this one DELETES the predecessor |

#### Do this, in order

1. **Delete `docs/gate`.** Nothing reads it. It is the one file in the kit whose
   re-sync rule INVERTS: `ADOPTING.md` used to class it *preserve always*
   (it was a derived file with your values in it), and it is now *delete*.
   `git rm docs/gate` — it is not migrated, and no value in it is needed.
2. **Delete `gate.template`** from your kit copy if you vendored the templates.
3. **Re-key the approval dial.** From your **KIT CHECKOUT** (not your own
   repo — `bootstrap.py` is kit-side and is never scaffolded into an adopting
   repo, unlike every other `scripts/…` command in this list), run
   `python project-trajectory/scripts/bootstrap.py --migrate-config --dest <your repo>`.
   It rewrites `[attestation] human_approval_through` from the retired 0–4
   ordinal to a `DevStg-*` rung in place and prints what it did
   (`… migrated the retired ordinal 2 -> `DevStg-Arch` … The rungs held are
   unchanged.`). An out-of-range value is left alone with a note. See "the dial"
   below for what happens if you skip this entirely (a warning per run, not a
   failure).
4. **Regenerate `docs/stage`:** `python scripts/derive_stage.py`. Commit it.
   **The order against step 3 does not matter**, and the reason is the part
   worth carrying away: `docs/process.toml` is **NOT** a declared derivation
   input (`kitlib/stage.py DECLARED_INPUTS`, owner ruling 2026-08-21). Dials
   govern **who may approve**, not **what stage is derived**, so re-keying the
   dial cannot move the fingerprint and cannot stale this file. The declared
   inputs are the six spine and frame registries, and nothing else. If you ever
   extend that list in your own repo, add the file in the same change that
   teaches the derivation to READ it — an input that is read but undeclared is
   the expensive direction: the fingerprint stops covering it, every consumer
   returns the recorded stage permanently, and `--check` stays green while it
   happens.
5. **Grep your own surfaces** for `derive_gate`, `docs/gate` and `--gate-policy`
   prose. Your history — logs, archives, closed work items, attestation records
   — is NOT swept: it is a record of what happened and rewriting it makes it a
   record of something else. Sweep only what is normative or teaching.
6. **Run the checks:** `python scripts/check.py --jobs 0`, then
   `python scripts/check_vocab.py --root . --strict`.

#### What changed, and why each thing moved

**THERE IS NOW ONE AXIS.** The kit derived two values over the same registry
rows: an eight-rung STAGE ladder (where the decomposition has got to) and a
three-value BAR (how strict the harness runs). The bar is deleted. It was a
`min` over every in-scope row, so a single drafted requirement collapsed it to
what a fresh scaffold reads and product checks silently stopped running — the
defect OI-51 names. The stage is derived over the SETTLED spine, so drafting
cannot lower what selects your checks, and the honest unfloored reading rides
beside it in the same file (`live-stage =`, `per-phase-live =`).

**Selection: at-or-above.** A step runs when your stage is AT OR ABOVE its
threshold. In `docs/stack.ini`, a `[step:*]` section's `gates = <list of bars>`
becomes `from-stage = <one rung>`. The legacy list is still read and translated,
with one notice per run naming the section; declaring both keys fails loudly.

**Flags:** `--stage` is canonical. `--gate` is accepted **silently and
indefinitely** — it is a flag name your hooks and CI pass literally, and the
word was never retired where it means a check that can fail. `--stage-cleared`
is accepted and WARNS: unlike `--gate` it makes a claim about the axis, and that
claim is the trap being retired. **Your VALUES do not change**: the three bar
spellings were always ladder rungs, so `--gate DevStg-Tests` still resolves.
What changed is the READING, which is why this is a note and not a translation
table.

**The `derived-gate` check step is gone**, with the file it guarded.
`derived-stage` (`derive_stage.py --check`) is its successor and was already
shipped. If your CI names steps explicitly, drop `derived-gate`.

**`--next-phase` moved house.** It was `derive_gate.py --next-phase`; it is now
`derive_stage.py --next-phase`, because that module already derives `phase` from
the same rows by the same rule. Same output — the next delivery phase number,
printed bare so a script can `int()` it.

**THE DIAL: `human_approval_through` is a rung, not a number.** It names the
HIGHEST rung a human still approves, and every rung AT OR BELOW it is
human-held — the mirror of the selection rule above. The shipped default is
`"DevStg-Release"` (everything human-held). `"DevStg-Below"` means nothing is.

| retired | now | holds |
|---|---|---|
| `0` | `"DevStg-Below"` | nothing |
| `1` | `"DevStg-Boundary"` | Needs, Boundary |
| `2` | `"DevStg-Arch"` | ...and Reqs, Arch |
| `3` | `"DevStg-LLReqs"` | ...and LLReqs |
| `4` | `"DevStg-Release"` | everything |

Each row holds **exactly** the rungs its number held — the equivalence was driven
before the old mapping table was deleted, so this is a re-spelling and not a
policy change. **A repo still carrying the number keeps working**: it is read,
translated, and warned about once per run, and step 4 above ends the warning. An
out-of-range number (`-1`, `9`) is refused as it always was, and reads as the
most conservative setting until you fix it. The re-key also makes three settings
reachable that the ordinal could not spell — `DevStg-Needs`, `DevStg-Reqs`,
`DevStg-Tests` and `DevStg-Impl` are now legal dial values.

**A settled spine reads `DevStg-Impl`, and `DevStg-Release` is derived by
nothing** (shipped by an earlier entry, restated here because it is the value
change an adopter notices): leaving Impl means the declared tests PASS, which no
`Status` cell may claim.

**PHASE ANCHORS: the canonical title is `[<phase>]-[DevStg-<Rung>]`.** The
retired `[<phase>]-[g1]`/`[reqs]` and `[<phase>]-[g2]`/`[tests]` spellings are
TRANSLATED on read and never rewritten — a WI title is a citation. **They
translate BY MEANING, not by spelling**, and this is the one trap in the change:
a closed `[reqs]`/`[g1]` anchor records **`DevStg-LLReqs`** (its SRs are
authored AND approved, so the phase has LEFT the Reqs rung) and a closed
`[tests]`/`[g2]` anchor records **`DevStg-Impl`**. Both are two rungs above the
word they share with the ladder. Taking the spelling would under-report every
phase's reach. `check_vocab.py` refuses the retired tokens in newly authored
text; mark a line that must quote one with `check_vocab: allow`.

**`check_vocab.py` scope correction:** `docs/stage` is now in scope as a
generated surface (its predecessor was named in the exemption list but not in
the text-file list, so that exemption never actually fired), and `docs/log.d/`,
`docs/work/partial/` and `docs/rubrics/` join the history/citation carve-outs.

**Where the depth went.** `PROCESS.md` §4 now teaches one vocabulary in fewer
words; the phase-anchor grammar and the batch cadence are taught in
`PROCESS_OPTIONS.md` under "Trajectory / work-items layer".

### A regenerated-but-unstaged artifact now REFUSES the commit [since 3c030ef7]

**What changes for you: a commit that used to warn now fails.** The
`staged-divergence` step — which asks which declared `[generated]` artifact is
modified in your working tree but absent from the INDEX, i.e. which one you
regenerated and did not `git add` — shipped warn-first under OI-31's ruling,
with the promotion named as its own later act "once it has run clean for a
program". This is that promotion. The step's plan entry now runs `--strict`, so
the pre-commit floor and CI both exit non-zero on a finding.

**Why it was promoted.** Because warn-first was still admitting the exact
false green it was built to report. Every freshness step (`derived-stage`,
`trajectory-map`, `status-map`, `open-items`, `okf`, `approval-fresh`, …)
resolves its artifact from the FILESYSTEM, so their honest claim is "the
artifact on disk matches its regeneration" — not "the artifact you are about to
commit does". Stage a registry edit, run `derive_stage.py`, forget the
`git add`, and the whole floor is green over a commit that carries the OLD
derived stage. What your bar vouches for is now the tree being COMMITTED.

**What you must do:** nothing, if you already stage what you regenerate. The
one workflow that changes is the DELIBERATELY partial commit: while any
declared generated artifact is dirty-and-unstaged, no commit will pass. Stage it
or revert it. `python scripts/check.py --staged-divergence` (without `--strict`)
is still the read-only detector to run mid-work.

**What this still does NOT catch**, stated so the promotion is not read as a
guarantee: an artifact that was STAGED WHILE STALE. The freshness gates read the
working tree, so a stale blob added to the index passes them and passes this.
That case needs the gates themselves to read the staged tree — OI-31 option (a),
recorded as the destination and still not taken.

### Placeholder-only frame registries read as NOT ADOPTED [since 3c030ef7]

**Read this one if your repo has never filled `external.toml` or
`components.toml`: your derived stage is about to go UP, correctly.**

`bootstrap.py` installs both frame registries carrying only the templates'
`-000` example rows. Both templates promise those rows are inert ("`trace.py`
ignores any id ending `-000`, so they are inert until deleted"; "this `-000` row
is inert and never blocks a gate"). They were not inert. The example rows filter
out, the row list comes back empty, and an empty-but-present registry CAPS its
rung — and because `DevStg-Boundary` and `DevStg-Arch` are repo-global and sit
below every spine rung, the untouched scaffold pinned every adopting repo at
`DevStg-Boundary` permanently. Measured on a real bootstrap: a spine with every
SN/SR/LLR/TC row `Founded` still derived `settled-stage = DevStg-Boundary`, so
`format`, `lint` and `tests+coverage` could never be selected from the derived
value.

**The rule now**, and the middle case is the whole change:

| your `external.toml` / `components.toml` | reading |
|---|---|
| absent | not adopted — rung skipped (unchanged) |
| present, **only `-000` example rows** | **not adopted — rung skipped (NEW)** |
| present with real rows, or emptied by hand | adopted — the rung applies (unchanged) |

Deleting the `-000` rows is an adopter ACT and keeps the tier, which is why an
emptied file still caps: the discriminator is "did anything but placeholders
ever get written here", not "is the row list empty".

**What you must do:** re-run `python scripts/derive_stage.py` and commit the
result. If your repo genuinely intends to declare a frame it has not typed yet,
nothing above disarms the rung — write one real row and the rung caps again.
**A repo that already filled either registry is unaffected**, and the kit's own
repo derived the identical rung before and after.

### `DevStg-Release` becomes REACHABLE — the test-evidence carrier [since c3c9b36a]

*(Anchored at the preceding commit: an entry cannot know its own SHA.)*

**Read this one if you want the top rung. Nothing here changes any repo that
does not: with no evidence record present, the derivation, the fingerprint and
the cost are all exactly what they were.**

The previous entry above left `DevStg-Release` **returned by nothing**,
deliberately — leaving `DevStg-Impl` means "every declared test case PASSES",
and no Status cell may ever claim that. The producer has now landed, so the rung
has exactly one input and it is a harness verdict.

**Two new kit files**, both copied by `bootstrap.py` and both needed as a set:

| file | what it is |
|---|---|
| `scripts/kitlib/evidence.py` | the `docs/test/evidence` record's format and the declared source surface its claim binds to |
| `scripts/record_test_evidence.py` | the **only** sanctioned producer of that record |

**How you earn the rung:**

```
python scripts/record_test_evidence.py --tier full   # runs check.py; writes only on exit 0
python scripts/derive_stage.py                       # the rung follows
git add docs/test/evidence docs/stage && git commit  # a reviewable approving act
```

**The record is bound BY VALUE to the tree it was measured on.** Its `binding`
field is a SHA-256 over your spine registries plus the declared `[paths] src`
and `tests` trees (and `docs/stack.ini` itself, which declares the bar). Move a
byte on either side and the record stops holding, the rung drops back to
`DevStg-Impl`, and `derive_stage --check` reds until you re-run the suite or
delete the record. **Never edit `binding` to clear a red** — that is the one
thing this mechanism exists to make visible. A `smoke` tier is refused by the
writer and by the reader: a declared subset cannot carry a whole-suite claim.

**What you must do if you do NOT want the rung:** nothing. The evidence file is a
declared stage input, so `docs/stage`'s `fingerprint` changes shape once — re-run
`python scripts/derive_stage.py` and commit the result at your next re-sync, as
usual. Your derived rung will not move.

**Two things this does not do**, stated so you do not expect them: it is not a
signature (a determined author can compute a valid binding by hand — it defeats a
green that outlived its tree, not forgery), and hosted CI does **not** write the
record. A runner committing back would need write credentials and a bot identity;
your CI needs no new step, because a stale record already reds the freshness
check wherever `derive_stage --check` runs.

---

### `docs/ratify/` splits: a regenerated `CURRENT.md` plus immutable dated briefs [since d08b5bd2]

*(Anchored at the preceding commit: an entry cannot know its own SHA.)*

**The defect this fixes.** `trace.py --approve modified --check` used to gate
whichever `docs/ratify/*.md` file was **newest by filename** — so a
regeneration rewrote a DATED file (named and read as the record of one
sitting) in place, sometimes many times, none of the rewrites about the WI the
file was named for (measured: one file, ten rewrites).

**What changed.**

- The live surface is now the fixed name **`docs/ratify/CURRENT.md`**.
  `trace.py --approve modified --out docs/ratify/CURRENT.md` is the one command
  that ever writes it; `--approve modified --check` (no `--out`) now compares
  against `CURRENT.md`, not "whatever is newest".
- A dated brief — `docs/ratify/<date>-<slug>.md` — is now **minted**, never
  hand-written with `--out`: `trace.py --mint-approval-brief SLUG` copies
  `CURRENT.md` to a dated name and refuses to overwrite one that already
  exists (`--mint-date` overrides the calendar date for backfill/testing).
- A new harness step, **`approval-immutable`** (`check.py --approval-immutable`,
  wired into `steps()`, `BUILTIN_STEP_NAMES`, and the shipped
  `hooks/pre-commit`'s batched floor), refuses any STAGED commit that modifies
  or deletes an already-committed `docs/ratify/<date>-*.md` — a plain ADD of a
  brand-new name (what the mint produces) is the only change it permits.
  Fail-closed, no warn mode, no `--strict` switch: unlike its sibling
  `staged-divergence`, there is no honest partial-compliance state for "a
  historical sign-off record just got rewritten".
- `docs/stack.ini`'s `[generated]` row (`docs/ratify/ = approve`) is unchanged —
  it was already a directory PREFIX, so it already covers both the one
  regenerated file and the N immutable ones without edit; its comment block
  now states the split explicitly.

**What you must do.** If you (or a job) ever passed `--out
docs/ratify/<date>-something.md` directly to `--approve modified`, stop:
write to `docs/ratify/CURRENT.md` and mint the dated copy as a second step.
Any EXISTING dated brief in your repo is untouched and stays exactly as
committed — the split changes nothing about history, only how the next one is
produced. `newest_approval_brief` (the "pick the newest filename" helper) is
RENAMED to `current_approval_brief` and now reads the fixed `CURRENT.md` path;
a script that imported the old name in-process needs the new one.

---

### The consolidation doctrine lands, plus a standing duplication census [since 1806f5c8]

*(Anchored at the preceding commit: an entry cannot know its own SHA.)*

**What changed.** `CLAUDE.md`, `AGENTS.template.md` and `PROCESS.md` gain a
consolidation clause beside (not replacing) edit-conservatively: conservative
WITHIN a task, consolidating ACROSS the codebase when the task itself is
consolidation — prefer the change that minimizes TOTAL behavior, extract the
shared stage a duplicated fix wants (the 0→A→B rule), restructure where
outputs overlap. The full text lives once, in `PROCESS.md` §3
("Consolidate, don't duplicate — the 0→A→B rule"); `CLAUDE.md` and
`AGENTS.template.md` each carry a one-line pointer, not a restatement.

A new standing check, `scripts/check_dupes_census.py`
(`[step:dupes-census]` in `docs/stack.ini`, `layer = product`,
`from-stage = DevStg-Impl`), measures duplicated function bodies across
your own `scripts/` tree — the WI-448 function-body-hash census, now a named
function instead of a `python -c` one-liner. It is **WARN-ONLY FOREVER**:
it never fails a gate, not even under `--strict`. The baseline lives in
`docs/stack.ini` `[dupes-census]` (`groups`/`copies`/`lines`), hand
re-stamped downward-only with a reason, the same convention the module-size
and smoke-budget ratchets already use.

**What you must do.** Merge the three doctrine edits (small, additive) and
either adopt `[step:dupes-census]` + `check_dupes_census.py` verbatim, or skip
it if your repo already ran and retired an equivalent (this kit's own history
did exactly that — see `docs/stack.ini`'s retired `[step:dupes]` note — before
OI-58 re-armed a deliberately narrower, never-gating version). If you adopt
it, stamp your own baseline: run `check_dupes_census.py --root .` once with no
baseline present, and write the printed reading into `[dupes-census]`.

### `antidote` joins the shipped skill set, vendored [since 1806f5c8]

*(Anchored at the preceding commit: an entry cannot know its own SHA.)*

**What changed.** `project-trajectory/skills/antidote/SKILL.md` is a new
**vendored** (not authored) `kit`-scope, `domains: [any]` skill — a
root-cause-vs-patch review discipline, the per-fix companion to the
consolidation doctrine above. Source: MIT-licensed
[Avtr99/antidote](https://github.com/Avtr99/antidote), commit
`8e0350e3d86df36852d56ad0a502376e24de870c`; the ledger row is in
`docs/dependencies.md` (a new `kit` tier there, for vendored content rather
than a Python import). `skills/INDEX.csv` is regenerated to include it.

**What you must do.** Re-run the skill fan-out for your chosen agent(s) —
`bootstrap.py --sync` (or your repo's equivalent materialization step) picks
up the new `scope: kit`, `domains: [any]` skill automatically, the same as any
other shipped skill; no repo-specific action beyond the normal sync. If your
repo hand-curates which kit skills it dogfoods into `.claude/skills/` (or
`.gemini`/`.agents`) rather than materializing the full set, decide whether to
add `antidote` explicitly — it is not force-selected by scope alone once a
repo has departed from full auto-selection.

### "Ratification" retires for "approval" across the live kit [since 7e898d15]

*(Anchored at the PRECEDING commit — this entry ships with the changes,
the same convention the `docs/gate` RETIRES entry above uses.)*

**What changed.** Owner ruling 2026-08-21 ("ratification holds a weight to it
that the semantics here don't need"): the kit's vocabulary unifies on
**approval** everywhere it is live prose, a code identifier, or a CLI flag.
`docs/process.toml [attestation] human_ratification_through` renames to
`human_approval_through`; `trace.py --ratify` and its `ratify-fresh` harness
step rename to `--approve` and `approval-fresh`; WI-503's `--mint-ratify-brief`
/ `--ratify-immutable` / `ratify-immutable` step rename to
`--mint-approval-brief` / `--approval-immutable` / `approval-immutable`;
`check_vocab.py`'s retired-tag enforcer gained the whole `ratif*` word family
(same mechanism as the `G*` tags). **The `docs/ratify/` DIRECTORY KEEPS ITS
NAME** — it is a record home for the immutable dated re-attestation briefs
that already lived there, and renaming a directory a record already cites
would misdate the record — so `docs/ratify/CURRENT.md` and the dated briefs
under it do not move, even though every script and doc that talks ABOUT that
directory now says "approval".

**What you must do.**

1. **Re-key the dial** from your **KIT CHECKOUT**:
   `python project-trajectory/scripts/bootstrap.py --migrate-config --dest <your repo>`.
   It rewrites `[attestation] human_ratification_through` to
   `human_approval_through` in place (the VALUE is untouched by this step —
   if it is still the retired 0-4 ordinal, the same command's existing
   ordinal migration fixes that too, in the same pass). Skipping this is not
   fatal: `agent_common.approval_through` reads the old key as a loud,
   per-call fallback and names the fix, the same shape WI-493 used for the
   ordinal.
2. **Kit-owned files — overwrite and move on:** every `scripts/*.py`,
   `PROCESS.md`, `PROCESS_OPTIONS.md`, `ADOPTING.md`, `README.md`,
   `AGENTS.template.md`, every shipped `skills/*/SKILL.md`,
   `process.toml.template`, `gate-policy.template`, `hooks/pre-commit`,
   `ci/check.yml`, `registries/*.template.*`.
3. **One test file renamed:** `tests/test_ratification_level.py` →
   `tests/test_approval_level.py` — a plain `git mv` if you vendored the
   kit's own tests rather than writing your own.
4. **Grep your own live surfaces** for `ratif` (case-insensitive) — your
   requirements/test-case registries, your own process docs, anything you
   authored rather than received from the kit. Leave `docs/ratify/` path
   references and anything inside your own history (logs, archives, closed
   work items, attestation records) alone; a record is not rewritten to
   agree with a later word choice (D-4).
5. **Run the checks:** `python scripts/check.py --jobs 0`, then
   `python scripts/check_vocab.py --root . --strict` — it now refuses a
   fresh `ratif*` site the same way it refuses a `G1`.

---

### Staleness headers land on generated and archive artifacts (OI-56 ruled (a)) [since a8b40abd]

**What changed.** WI-505 stamps every generated-but-live surface
(`docs/stage`, the `docs/status.md` generated block, `docs/open-items.html`,
`PROJECT_STATE.html`, `docs/ratify/CURRENT.md` + `trace.py --approve`,
`skills/INDEX.csv`, `prompts/CATALOG.md`) with a header its own generator
writes — "GENERATED by \<script\> — do not hand-edit; cite \<source\>, not
this rendering" for a live surface, the fuller "may be stale relative to the
tree — regenerate before trusting" form for a report/dashboard — so the
convention can never rot out of sync with the artifact. `docs/archive/**`
gets a one-time banner sweep ("ARCHIVE — design history as of \<date\>; not
current guidance.", no live-surface pointer — the owner declined that link as
backlink-rot risk) except the registry-parsed specs under `archive/work/**`
and the byte-compared snapshot under `archive/last_approved/**`, both of
which a banner line would break mechanically; the convention is recorded as
one line in `docs/archive/README.md` and enforced no further, by ruling.

**What you must do.**

1. **Kit-owned generators — overwrite and re-run:** `scripts/gen_trajectory.py`
   (+ its sibling `scripts/traj_status.py`), `scripts/trace.py`,
   `scripts/gen_skills_index.py` carry the new header text; regenerate your
   own tree's copies (`PROJECT_STATE.html`, `docs/status.md`,
   `docs/ratify/CURRENT.md`, `skills/INDEX.csv` if you maintain a kit-scope
   skills source) after overwriting the scripts.
2. **Archive sweep is one-time and yours to run, not the kit's:** the banner
   is additive prose, not a mechanized check, so there is nothing to pull —
   if you want the same convention over your own `docs/archive/**`, prepend
   `> **ARCHIVE** — design history as of <date>; not current guidance.` to
   each file (skip anything a script parses: your own archived spec/registry
   forms, any byte-compared snapshot, non-text formats like `.patch`/`.rtf`).
3. **No new check to wire.** OI-56 declined the enforcement half — nothing in
   `check.py`/`check_docs.py` gates the banner's presence, so there is no gate
   to add to your CI.

---

### The kit-path invariant: every `bootstrap.py` invocation in a shipped surface must be kit-relative (OI-59 ruled (a)+(c)) [since a296b4ff]

*(Anchored at the preceding commit; the change lands in the commit that
follows it.)* **What changed.** `bootstrap.py` stays out of its own `MAPPING` (unchanged —
the bundle IS the kit folder), but every place the kit tells a reader to *run*
it now spells the kit-relative path, `project-trajectory/scripts/bootstrap.py`,
rather than a bare `scripts/bootstrap.py` that resolves, from inside an
adopter's own repo, to a file that repo was never given. `tests/test_kit_path_invariant.py`
(kit-side, not scaffolded) pins this by sweeping every `bootstrap.py` `MAPPING`
source plus `RESYNC_PACK.md` for a bare invocation.

**What you must do.** Overwrite the corrected sources on re-sync as usual (the
three hooks, `scripts/agent_common.py`, `process.toml.template`) — no action
beyond the normal file-class rules in §2. If you kept a local edit to one of
their remediation messages, re-apply it over the corrected wording rather than
the bare form: your own copy of `docs/process.toml` (regenerated from
`process.toml.template`, a hand-edited-but-kit-owned file per §2.2) carries the
same bare-path text if it predates this re-sync and is worth fixing the same
way in the same commit.

### `kitlib/spine.py` — the spine ROW vocabulary gets one home [since d00a8506]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**An eighth module in `scripts/kitlib/`, and the same copy-it-whole rule.** The
row predicates `trace.py` and `spine_rules.py` each carried their own copy of —
`is_drafted`, `is_approved`, `is_founded`, `llr_exempt` with its `LLR_EXEMPT`
set, `phase_num`, `sn_all_ids`, `sn_cited_ids`, `refs`, `is_example` and the
registry CSV loader `load_csv` — now live in `scripts/kitlib/spine.py`. Nine
duplicated function bodies, held equal by nine `tests/test_rule_sync.py` pins,
because the retired F5 rule licensed the duplication and a test could only
CONTAIN the drift rather than remove it. Those pins are deleted with the copies.

**If you only overwrite kit files, you need do nothing but include the new
module in the copy.** `trace.is_approved`, `spine_rules.is_drafted`,
`trace_text.refs`, `spine_rules.LLR_EXEMPT` and every one of their siblings are
still there under the same names and still answer identically; they are
re-exports now. No call signature changed and no derived value changed.

**One type note, and it is the only observable difference.**
`trace.LLR_EXEMPT` was a `tuple` and `spine_rules.LLR_EXEMPT` a `set`; both are
now the same `frozenset`. `in` is unaffected — only code that indexed the tuple
(`LLR_EXEMPT[0]`) or mutated the set would notice, and neither existed in the
kit.

**`sn_draft_ids` is the one name that did NOT move here**, deliberately: it was
a one-line delegation to `spine_carrier.draft_ids_from_text`, and `kitlib` may
import no sibling of `scripts/`. Both modules now bind that function directly,
so `trace.sn_draft_ids` and `spine_rules.sn_draft_ids` still resolve and still
behave identically — they are simply the carrier's function under a local name.

**If you have your OWN copy of any of these predicates** — a report script that
spells out `Status.strip().lower() == "approved"`, a dashboard filter with its
own `-000` test — this is the moment to delete it and import instead. A second
opinion about what `Approved` means is a false green or a false red at a gate,
which is the whole reason this consolidation happened.

**Nothing in your `docs/` changes**, and no registry cell moves.

---

### The component view is GENERATED and `DetailDoc` retires (OI-32 ruled (d)) [since f1cc0b44]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**What changed.** A new shipped generator, `scripts/gen_components.py`, derives
`docs/requirements/components.derived.toml` from four registries you already
keep: `components.toml` declares WHICH components exist, the LLR tier's
`Component` cell carries membership, the SR tier is reached through it, and
`interfaces.toml` supplies the seams. Per component the view lists the design
rows that belong to it, the requirements those rows decompose (marking the ones
shared with another component), the perspectives that bear on it, its modules,
and its seams split internal from boundary; a repo-wide `[unplaced]` table names
every requirement and seam that reaches no component, so nothing is silently
dropped. It carries **no** approval or maturity cell, ever — the hand-authored
row still declares the component, and a generated file that flipped an approval
would route around your `human_approval_through` dial.

With it, the CMP **`DetailDoc` column retires**: it named a prose home the kit
never created and no script ever read, and the derived view is the home it was
pointing at. The column is gone from `registries/components.template.toml`, from
`spine_carrier.OFFSPINE_KEYS`/`OFFSPINE_COLUMN` and from `migrate_carrier.KEY`.

**What you must do.**

1. **Copy the new generator in** (`scripts/gen_components.py`) alongside the
   overwritten `scripts/check.py`, `scripts/trunk_step.py`,
   `scripts/spine_carrier.py`, `scripts/migrate_carrier.py`, `scripts/bootstrap.py`
   and `registries/components.template.toml`, and the shipped
   `hooks/pre-commit`.
2. **Declare the artifact**, in your own `docs/stack.ini` `[generated]` section
   — it is YOUR file, so the kit cannot write this row for you:
   `docs/requirements/components.derived.toml = components`. The `component-view`
   check.py step and the hook floor already name it once the scripts are
   overwritten; leaving the row out means the step still runs but
   `staged-divergence` and the trunk's regen ownership rule will not know the
   artifact is generated.
3. **Generate it once and commit it:** `python scripts/gen_components.py`.
   Vacuous — exit 0, nothing written — if your `components.toml` holds only the
   inert `CMP-000` row, so a repo that never adopted the component layer pays
   nothing and needs neither step 2 nor this one.
4. **If any CMP row of yours carries `detail_doc`,** the key now fails your
   schema check rather than being silently absorbed (the same retirement shape
   the IF tier's `Status` took). Move whatever that document held into the rows
   the view derives from — the design rows' `Detail`, the seam's `Contract`, a
   `docs/knowledge/` pack for durable findings — and delete the cell. If the
   document is genuinely mechanism prose that no row can hold, keep the file and
   link it from the component's `Notes`; the view deliberately shows no
   internals.

### The dashboard grows a System-context view, and a new `traj_*` sibling ships with it [since d6818b0b]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**What changed.** `PROJECT_STATE.html`'s architecture tab now opens on a
**System context** block derived from `docs/requirements/external.toml` — the
declared external parties, the boundary crossings, and the external-to-external
relationships the system is not a party to — with the realizing `IF-###` rows
joined from `interfaces.toml`, an unrealized crossing drawn dashed, and any
`external:`-endpoint interface row that ties back to no crossing listed with the
reason its own row records. It splices ABOVE the derived module map: the frame is
the architecture's context, and it is generated rather than hand-drawn (the
ruling that let `docs/architecture.md` be retired).

The renderer lives in a **new shipped module, `scripts/traj_context.py`**, which
joins the `gen_trajectory.py` sibling set that copies together.

**What you must do.**

1. **Copy the new module in** (`scripts/traj_context.py`) alongside the
   overwritten `scripts/gen_trajectory.py`, `scripts/traj_parse.py`,
   `scripts/traj_views.py` and `scripts/bootstrap.py`. A scaffold that takes the
   new `gen_trajectory.py` without it `ImportError`s on the first render — the
   standing rule for that set.
2. **Regenerate and commit the dashboard** (`python scripts/gen_trajectory.py`);
   otherwise the `trajectory-map` freshness step reds on the new block.
3. **Nothing else.** No registry column changed and no dial moved. A repo that
   declares no boundary — no `external.toml`, or one holding only the blank
   form's `-000` rows — renders **byte-identically** to before, so the view costs
   a non-adopter nothing.

---

### The residual shared helpers reach their themed homes; `kitlib` gains no module [since 77d67c38]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**No new file, and that is the whole shape of this one.** The last six duplicate
groups the kit's own census reported all joined a `scripts/kitlib/` module that
already existed, so the package is still the same nine files you already copy
whole. What moved:

- `kitlib.config.process_check(root, key)` is NEW — the `docs/process.toml`
  `[checks]` toggle reader that `check_trajectory.py` and `gen_okf.py` each
  carried privately. Both still expose `_process_check` under that name.
- `kitlib.spine` gains `norm_module(path)` and `MODULE_EXTS` — the
  naming-neutral key an LLR `Module` cell, an IF `Endpoint` and an arch-map node
  all reduce to. `check_trajectory._norm_module`, `gen_arch_map._norm_module`
  and `trace_text.norm_module` are re-exports now, as are
  `trace_text.MODULE_EXTS` and the two `_MODULE_EXTS` spellings.
- `kitlib.spine.refs` absorbs the multi-ref cell split from five more modules
  (`check_trajectory._split_refs`, `gen_okf.split_refs`,
  `plan_coverage.split_refs`, `plan_artifacts._split_tokens`,
  `schedule._split_refs`), and `kitlib.spine.is_example` absorbs
  `gen_release_checklist.is_example`.
- `kitlib.evidence.render_fields(record, fields, fmt)` is NEW — the `k = v`
  block renderer `kitlib.stage` shares with it.
- `wi_convert.work_dir_for` / `.spec_paths` now re-export
  `kitlib.registry.spec_work_dir` / `.spec_files`.
- `spine_carrier.needs_for_root(root)` is NEW — the root-relative need-row read
  `traj_parse._sn_rows` and `gen_okf.sn_rows` each wrapped. It lives on the
  carrier rather than in `kitlib` because `kitlib` may import no sibling of
  `scripts/`.

**If you only overwrite kit files, you need do nothing.** Every former name
still resolves, under the same spelling, and answers identically — these are
re-exports, not renames. No call signature, derived value, registry cell or dial
changed.

**If you have your OWN copy of any of these** — a report script with its own
`;`-or-whitespace ref split, a tool that strips `.py` off a `Module` cell by
hand, a checker that re-reads `[checks]` — this is the moment to import instead.
The ref splitter is the one this kit watched drift in the wild: a copy that
split on `[;,]` alone read a whitespace-separated pair as one garbage token and
matched nothing, silently.

**Two things worth knowing about the census that found these**
(`scripts/check_dupes_census.py`, warn-only, baseline in `docs/stack.ini`
`[dupes-census]`): it is stamped at `0 / 0 / 0` here, which is a READING and not
a floor — a new duplicate re-appears as a WARN — and it is blind to a copy that
renames the constant it reads, which is how one of the four `norm_module` homes
above stayed invisible until the others consolidated.

### The registry schema of record and the TOML emitter move into `kitlib.spine` [since 23890e5d]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**No new file again** — the package is the same nine modules, and the last two
things `bootstrap.py` restated instead of importing now live in one of them.
What moved, all as re-exports under their existing spellings:

- `spine_carrier.SPINE_TIER_KEYS` / `.OFFSPINE_KEYS` / `.REGISTRY_KEYS` — the
  per-tier **schema of record** — are now `kitlib.spine`'s, bound on the carrier.
  If you add a column to a registry tier, the reviewed edit is in
  `scripts/kitlib/spine.py` from here on; the carrier still answers with the
  same table object.
- `wi_convert.toml_string` / `.toml_value` / `.render_frontmatter` are now
  `kitlib.spine.toml_string` / `.toml_value` / `.toml_fields`, re-exported. The
  TOML emitter had three homes in the kit and one of them (`bootstrap`'s) escaped
  only the backslash and the quote, so a cell carrying a tab produced a file
  `tomllib` refuses to read back. Two of the three are now one; the third
  (`migrate_carrier.toml_scalar`, which promotes a long cell to a multi-line
  string) is a different rule with one caller and stays.

**If you only overwrite kit files, you need do nothing.** Every former name
resolves and answers identically. The one behaviour that changes is the
scaffolder's: it emits its non-Python `OI-3` brief in the schema's key order
(byte-identical to before for every shipped stack) and **raises** on a key the
open-items tier does not declare, rather than writing a brief that renders empty.

**If you have your OWN copy** of a TOML writer for these files, this is the
moment to import `kitlib.spine`'s instead.

### `Hat-Refs` gains its WRITE instruction, at the tier that mints the row [since 0069b6a6]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**Kit-owned file — overwrite it and move on:** `skills/spine-authoring/SKILL.md`
(then `python project-trajectory/scripts/bootstrap.py --dest . --sync` to
re-materialize your per-agent copies; `gen_skills_index.py --check-agents` is
the drift gate).

**What changes for you:** nothing mechanical — **no schema, checker, gate or
brief moves**. The `Hat-Refs` entry above shipped the cell and its detectors but
left the writing to judgement, and judgement with no stated rule fills the cell
by pattern. The skill now carries the rule, at SR (`§2(c2)`) and LLR (`§3`):

- **Attribute a hat only where THAT hat's own `listens_for` names a failure the
  row prevents** — not "which lens could be held up to this row". The second
  reading is the one that ruins the column: if your roster's hats are mostly
  `applies_when = "always"`, it puts every name in every cell.
- **An empty cell is an answer** (it reads *not recorded*, never *no perspective
  applied*), and two shapes earn it: a row naming a hat in order to **refuse**
  it as a basis, and a row whose attribution's subject is gone.
- **An LLR records only what its own decomposition raised** — a restatement of
  the derivation rule the previous entry already carries, now sited where the
  child row is written.

**Why the skill and not the planner brief.** The obvious other home was
`prompts/dual-plan-planner.template.md`, the one consumer of the
`{{HAT_QUESTIONS}}` block — but its output contract is a **plan table of
proposed work items**, and it mints no spine row at all, so a write instruction
there would be unfollowable by construction. If you have re-carried that brief
with an output contract that DOES mint SR/LLR rows, this is the entry to read
twice: the instruction belongs wherever your minting session actually reads.

### The hats roster gains an OPTIONAL-key concept: `knowledge` [since 46dcac8a]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**What changed.** `scripts/hats.py` refused any row key beyond the three
required ones (`applies_when`, `asks`, `listens_for`) with no notion of an
optional one — so a new field like `knowledge` (knowledge packs derived from a
hat's concern, WI-484 phase 4 / OI-32 (d)) could only be added by making it
MANDATORY on every row. It now declares `OPTIONAL_KEYS = ("knowledge",)`: a key
in that set is no longer an "unknown key" refusal, its presence is validated
(a non-empty list of non-empty strings; a bare string, an empty list, or a
non-string entry is refused BY NAME), and its ABSENCE stays fine on every row —
the strict posture is unchanged for every key not in either set. `hats.py
list`/`applicable` print the field where a row carries it and say nothing where
it does not.

**Take:** the overwritten `scripts/hats.py` and `registries/hats.template.toml`
(the template gained a commented explanation of the key, no row filling it in —
your `docs/requirements/hats.toml` is owner text and this pack does not touch
its values). Nothing else moves: no schema-breaking change, no new required
field, no checker or gate reads `knowledge` yet.

**What you must do.** Nothing mechanical unless you want the field: your live
roster keeps parsing exactly as before. If you want to cite knowledge packs
from a hat, add `knowledge = ["docs/knowledge/…"]` to that hat's row yourself —
this pack does not fill values into owner text.

### The interface tier sheds `direction` and renames its endpoints to `provider` / `consumers` [since 55d1cb77]

The last piece of the 2026-08-15 rework's ruled end state (owner ruling on
`OI-60`, option (a), 2026-08-23), and it is a **schema change to every IF row**.
Applies to any adoption carrying a populated `docs/requirements/interfaces.toml`;
a repo still on the `-000` placeholder just overwrites the template.

**What the row looks like now.** Three cells become two, and flow stops being a
column:

| was | now |
|---|---|
| `direction = "Provides"` / `"Consumes"` | *deleted* — flow is the SHAPE of the row, `provider` → `consumers` |
| `this_project` (this side) | `provider` on a Provides row; folded into `consumers` on a Consumes row |
| `counterpart` (the far side) | `consumers` (a LIST) on a Provides row; `provider` on a Consumes row whose far side is the provider or the medium |

**Then `provider` is dropped wherever it is DERIVABLE**: an `owner` that is a
design row naming exactly one `module` IS the provider. The cell survives only
where the derivation cannot run — a requirement owner (which names no module),
an owner naming several modules (a set, not the fact), or a provider that is a
file medium or an `external:` party. `trace.py` gains a warn-only advisory naming
any row that states a provider its owner already derives.

**The migration, in order — and measure before you edit.**

1. **Classify every `Consumes` row before you touch it.** The far side is one of
   three things and only you know which: the **provider** module, the **medium**
   consumed (a file or directory — that becomes `provider`, which is honest: it
   is the side the contract is served from), or a **consumer class / reader set**
   (`external:downstream adopter`, or the other measured readers of one file). On
   that third class both cells are consumers: they merge into `consumers`, and
   the row states NO provider, because none was ever recorded. The kit's own 135
   rows split 51 + 5 carrier, 12 medium, 16 consumer-class, 5 reader-set, 46
   `Provides`. Guessing here silently reverses seams; a row you cannot classify
   is a row to stop on.
2. **Rewrite the cells** per the table above, `consumers` always a LIST.
3. **Drop `provider`** on every row whose owner derives it. Run
   `python scripts/trace.py` and read the *Provider derivability advisories*
   section of `docs/test/report.md` — it names what is left to drop.
4. **Take the readers as one set**: `kitlib/spine.py` (the schema plus the new
   `seam_provider`/`seam_consumers`/`seam_endpoints` resolvers), `spine_carrier.py`
   (the column map plus `llr_modules`), `trace.py`, `trace_text.py`,
   `check_trajectory.py` (`load_ifs` now RESOLVES each row and `load_seams` is the
   one live-registry call), `traj_views.py`, `gen_arch_map.py`,
   `gen_components.py`, `traj_parse.py`, `intake.py`, `plan_briefs.py`. A partial
   take leaves a reader looking for a column that no longer exists.
5. **Overwrite `registries/interfaces.template.toml`, `INTERFACES.template.md`
   and `prompts/dual-plan-planner.template.md`**, and re-read `PROCESS.md` §8.

**Two behaviour changes worth expecting.** The `source`/`sink` honesty valve now
marks a ROLE rather than a cell — `source` the row's provider, `sink` its
consumers — which is what both words meant when both were read off
`this_project`. And the How-SW seam graph draws nothing for a row that states no
provider: those rows record readers of a medium the row names only in `contract`,
and the old arrow pointed the wrong way (from the adopter INTO the module).
Recording those media as providers is authoring, per row, and the kit has not
done it.

### An interface `contract` stops restating its owner; `VerifiedBy` and two new checks arrive [since 3cf43e2e]

Four coupled changes to the interface tier (owner ruling on `OI-61`, 2026-08-23).
**None of them breaks a legacy registry**: the new cell is optional, both new
checks are warn-first and never join a failure set, and the generated reference
is opt-in. Take them in this order.

**(a) Thin the contracts that only restate their owner.** Where a row's
`contract` paraphrases what the `owner` row and the module already say — the
whole `<module>.py CLI: --flag does X` family is the worked case — rewrite it as
the crossing and stop:

```
contract = """SR-006's obligation delivered as a CLI at check.py; crosses B-05."""
```

What crosses, who answers for it, which boundary. **Review it per row, never by
regex**: keep (or re-home) any clause carrying a typed fact the owner row does
*not* state — a written artifact, a fail-loud guarantee, an exclusion in a
comparison. The kit's own pass took 27 rows from 7,385 characters to 2,605 and
cleared all four of its over-ceiling breaches; expect roughly two thirds off a
comparable family, and expect a handful of rows to keep a clause.

**(b) Adopt the generated CLI reference, or don't.** `gen_arch_map.py` gains
`--cli-doc FILE` (repeatable, honours `--check`): it reads every scanned module's
`argparse` tree — by AST, never importing it — and splices a flag/help table plus
each module's declared `Contracts: IF-###` line into a
`<!-- BEGIN GENERATED CLI REFERENCE -->` marker pair. It is its own mode and
needs no `--doc`, so adopting it does **not** re-commit the module map that
retired at `WI-455`. To adopt: create the doc with the marker pair, add a
`[generated]` row of kind `cli` naming it (with its markers), and the shipped
`cli-reference` check step + `trunk_step.py --regen` pick it up. Skip all of it
and the step is vacuous — a missing target prints a notice and exits 0.

**(c) Expect new warn-first findings on your `contract` cells.** `trace.py` now
resolves the names a contract *claims*: a `SCHED_*` / `Foo.bar` / `CONSTANT_NAME`
token must exist in the declared source surface (`[paths] src`, symbol mode), and
a path whose first segment is a real directory must exist. A path your
`docs/declared-absences` already declares is resolved, not dangling. The rule is
vacuous — silent — where there is no surface to read (`[arch-map] mode = files`,
a missing source dir), because an empty surface would report every name as dead.
Read the findings; they are the class no form rule could ever see.

**(d) `VerifiedBy` is available and optional.** A new optional IF cell taking a
`TC-###` or an `LLR-###`. **Empty means "verified in its own right"** and is the
ordinary case, so there is nothing to backfill. Fill it only on a *low-level*
seam whose honest answer is that the parent functionality's tests are what cover
it — the position `Verification` cannot state, since its one exemption is
LLR-exemption on an SR and an IF row carries no `Verification` cell at all. Only
resolution is checked, warn-first. Take
`kitlib/spine.py` (the tier schema), `spine_carrier.py` (the column map),
`trace.py`, and overwrite `registries/interfaces.template.toml` +
`INTERFACES.template.md`; re-read `PROCESS.md` §8.

### `kitlib/secret_classes.py` — the credential class vocabulary gets one home [since 2f054aab]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**A new module in `scripts/kitlib/`, and the same copy-it-whole rule.** The
credential PATTERN table — which classes (PEM private key, GitHub token,
GitHub fine-grained token, Slack token, AWS access key id, API secret key,
generic bearer token) each of the commit-hook secrets floor
(`check_privacy.py`'s `KEY_RE`/`TOKEN_RES`) and the session-transcript
redactor (`agent_common.py`'s `redact_secrets`/`_SECRET_RES`) compile — used
to be two independent literals in those two modules. A WI-508 alignment pass
measured them disagreeing on four of five driven samples, **in both
directions**: the worst case, a PEM private-key block was refused at the
commit hook but passed unredacted into a committed transcript, so the durable
artifact was less protected than the ephemeral one. `kitlib.secret_classes`
is the one table both now read.

**If you only overwrite kit files, you need do nothing but include the new
module in the copy.** `check_privacy.KEY_RE` / `check_privacy.TOKEN_RES` and
`agent_common._SECRET_RES` are all still there and still resolve to the same
names; they are now derived from the shared table rather than hand-copied.
**One behavior change, and it is the fix this entry exists to describe:**
`agent_common.redact_secrets` now also redacts a PEM private-key header,
which it did not before. Every other class's matching behavior — on both
sides — is unchanged; the two modules' driving test
(`tests/test_kitlib_secret_classes.py`) pins that directly against the
pre-change literals.

**If you had a local patch to either module's pattern list** — an added
credential shape, a tightened or loosened threshold — that edit is on a
kit-owned file and the deviation review in §2 is where it surfaces. Re-apply
it to `scripts/kitlib/secret_classes.py`'s `SECRET_CLASSES` table (a
`SecretClass(name, scan_pattern, redact_pattern)` tuple; either pattern may be
`None`, a deliberate per-class decision), not to `check_privacy.py` or
`agent_common.py` directly — both now derive their working pattern lists from
that table by comprehension, so a hand-edit on either consumer is silently
shadowed at the next re-sync.

**Nothing in your `docs/` changes**, and no registry cell moves — `SR-017` /
`SR-018` / `SR-176` and their LLR rows are unchanged; this is an
implementation consolidation under the same obligations, not a new one.

### The allow-file parse-honesty arm reaches three more declared exception readers [since e1c01f2b]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**Kit-owned files — overwrite and move on:** `scripts/check_trajectory.py`,
`scripts/check_doc_refs.py`, `scripts/check_need_form.py`.

**Three more declared-exception readers now REPORT a declaring line their
grammar cannot read, instead of silently dropping it.** `docs/provenance-allow`
and `docs/kernel-modules-allow` already did this (a malformed line grants no
exemption either way — fail-safe, unchanged — but a drop that also removes the
entry from every COUNT was itself worth reporting, `trace.read_provenance_allow`'s
own docstring argues why). The same arm now reaches `docs/if-tc-coverage-allow`
(`check_trajectory.if_tc_allow_parse_findings`), `docs/declared-absences`
(`check_doc_refs.declared_absences_parse_findings`) and `docs/need-form-allow`
(`check_need_form.need_form_allow_parse_findings`). Nothing is merged: each of
the five files keeps its own grammar, its own required fields and its own
fail-safe direction — only the "a malformed line is worth naming" behavior is
now uniform.

**What you may notice:** nothing, unless one of your three files already
carries a line the grammar cannot read (no separator; for
`docs/if-tc-coverage-allow`, a first token that does not parse as `IF-###`) —
in which case the next run reports it where it did not before:

- `check_trajectory` — a malformed `docs/if-tc-coverage-allow` line rides
  `if_tc_coverage_findings`' own `[checks] interfaces_check` opt-out and its
  WARN-plain / ERROR-under-`--strict` severity (unlike that function, it does
  NOT share the ≤1-module arch-map vacuity — a malformed line is a fact about
  the file, not about whether the coverage rule currently has anything to say).
- `check_doc_refs` — a malformed `docs/declared-absences` line joins the same
  `findings` list a dangling reference does: WARN plain, `--strict` gates.
- `check_need_form` — a malformed `docs/need-form-allow` line shares that
  checker's own WARN-always / ERROR-only-under-its-own-`--strict` severity
  (still not wired into `check.py` at any bar).

Every well-formed file behaves exactly as before — this repo's own five allow
files were re-verified to parse to what they parsed to before this change; no
existing entry needs an edit.

**If you had a local patch to any of the five parsers** — `check_doc_refs.
load_declared_absences` and `check_need_form.load_allow` keep their exact
prior signatures and return shapes (a new sibling accessor,
`read_declared_absences`/`read_need_form_allow`, carries the malformed-line
half instead), and `check_trajectory.parse_if_tc_allow` keeps its pinned
2-tuple return for the same reason. Re-apply your patch to whichever function
you touched; nothing downstream of it needed to change shape.

### `scripts/acceptance_record.py` — the acceptance record leaves the checker [since c3bc6e07]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**Kit-owned files — overwrite and move on:** `scripts/check_trajectory.py`,
`scripts/acceptance_record.py` (NEW), `scripts/intake.py`,
`scripts/kitlib/git.py`, `scripts/bootstrap.py`.

**A NEW SHIPPED SCRIPT, and a scaffold without it cannot run the checker.**
`check_trajectory.py` imports `acceptance_record` UNGUARDED and joins its
findings to the failure set, so copy the new file across with the rest — it is a
`bootstrap.MAPPING` row, so a re-bootstrap or a `--repair` places it for you.

**What moved, and nothing else did.** 677 lines came out of
`check_trajectory.py` VERBATIM: the §A5.1 approved/traced cell split
(`SPINE_TRACED_CELLS`, `SPINE_APPROVED_CELLS`, `spine_cell_class`,
`traced_cells`), the two-tree comparison (`SPINE_CSVS`, `_spine_rows_at`,
`_spine_revs`, `split_changed_cells`, `staged_spine_amendments`), the two staged
warns (`staged_spine_findings`, `staged_hat_refs_findings`) and the mirror
invariant in both forms (`staged_snapshot_findings`,
`committed_snapshot_findings`). The boundary: **what compares two git trees is
in the new module; what reads the working tree stayed.**

**What you may notice: nothing.** `check_trajectory.py` re-exports every one of
those names under its former spelling, so `check_trajectory.staged_spine_
amendments(...)` and the rest still resolve. CLI console output and exit codes
are unchanged — measured, not asserted: nine driven CLI paths and 56 API probes
capture-diffed empty against the pre-change tree.

**If you call these from your own code**, prefer the new home
(`import acceptance_record`) — that is what this kit's own `intake.py` now does,
which removed its import of a ~5,000-line validator entirely. The re-exports are
not deprecated and nothing warns; they are how the move cost no caller anything.

**One shared helper widened:** `kitlib.git.git_out(root, args)` gained an
optional third parameter, `stdin=None`, and absorbed `check_trajectory._git` —
a fourth copy of the "git, or None" pattern that the D-8/`OI-16` consolidation
missed because the extra argument made it look like a different function.
Existing two-argument calls are byte-for-byte unaffected. **If you had a local
copy of that pattern**, this is the moment to alias it (`_git = kitgit.git_out`)
rather than carry a fifth.

**Registry side, if you traced these rows:** three LLR `Module` cells re-point
to the new module. `Module` is a TRACED cell, so this amends no attested prose
and arms no re-attest window; re-point yours the same way if your registry names
the old home for the amendment or mirror rules.

---

### The contract may live beside the code, and the `Contracts:` marker tightens [since 8cf9e23d]

*(Anchored at the preceding commit — an entry cannot know its own SHA.)*

**Kit-owned files — overwrite and move on:** `scripts/gen_arch_map.py`,
`scripts/check.py`, `scripts/trunk_step.py`, `registries/interfaces.template.toml`.

**(a) READ THIS ONE EVEN IF YOU ADOPT NOTHING BELOW — the `Contracts:` marker
now has to OPEN its line.** It used to be "the line contains the word
`Contracts`", which harvested ids out of prose that DENIED a declaration: the
kit's own `handback.py` says *"No `Contracts:` line, deliberately: the integrator
seam this extends is IF-080"* and the old rule read that as declaring `IF-080`.
The new rule strips a leading `#` and requires the line to PARSE:
`Contracts:` followed by a comma-separated `IF-###` list, optionally then prose
after an em dash, hyphen, colon or parenthesis. Line-start alone was not enough —
`Contracts: not IF-080; an example, not a declaration` opens correctly and would
still have leaked IF-080 under a "harvest every IF token on the line" rule.

*What this costs you:* a module whose marker sits MID-LINE — e.g.
`"""Module A. Contracts: IF-003, IF-004"""` — no longer declares anything.
All 57 anchors in the kit's own tree already open their line, so the kit saw no
loss; your repo may differ. **Find yours before upgrading:**

```
grep -rn "Contracts:" --include="*.py" . | grep -v ":Contracts:" | grep "IF-"
```

Anything that prints and is a real declaration must move the marker to the start
of its own line. A hit that is prose (a denial, a cross-reference) is now
correctly ignored — that is the fix, not a regression.

**You are not left to find them by grep alone.** `gen_arch_map` reports both
lossy forms by name — a marker-shaped line whose id list will not parse, and a
`Contracts:` carrying ids mid-line — so an upgrade tells you what stopped
declaring instead of dropping it in silence. Do not bump each IF row's
`version`: the marker syntax changed, the interface semantics did not.

**(b) Adopt the generated interface reference, or don't.** `gen_arch_map.py`
gains `--contracts-doc FILE` (repeatable, honours `--check`), the exact shape of
`--cli-doc`. After its marker line a module may state each contract as a block
opening `Contract IF-###:`, running to the next such line, a blank line, or the
end of the docstring; wrapped lines join into one paragraph. The opener is
`Contract IF-###:` and not a bare `IF-###:` on purpose — a bare id-colon is
ordinary docstring prose (`IF-001: legacy identifier retained`, a mapping table,
an example), and only a form nobody writes by accident is safe to hard-fail on.
Four things raise `ContractsGrammarError`: a body before the marker line, a body
for an id NOT on it, a second body for one id, and a body carrying an HTML
comment (the text is spliced into generated Markdown and must not be able to
close its own end marker). To adopt: create the doc with a
`<!-- BEGIN GENERATED INTERFACE REFERENCE -->` / `<!-- END ... -->` pair, add a
`[generated]` row of kind `interface-reference` naming it with its markers, and
the shipped `interface-reference` check step plus `trunk_step.py --regen` pick it
up. Skip all of it and the step is vacuous — a missing target prints a notice and
exits 0.

*What it buys:* the contract sits beside the code that must honour it, so a
rename moves the two together and the registry cell can state what crosses and
point rather than restate. *What it costs:* a declared seam with no body is
listed in the reference as unstated rather than dropped, so adopting the doc
before writing any bodies produces a document that is mostly gaps — which is the
honest picture, and the reason it is opt-in.

### The interface row becomes one owner, its far side and a typed statement [since 088a6cca]

**Kit-owned files — overwrite and move on:** `scripts/kitlib/spine.py`,
`scripts/spine_carrier.py`, `scripts/migrate_carrier.py`, `scripts/trace.py`,
`scripts/trace_text.py`, `scripts/check_trajectory.py`, `scripts/gen_arch_map.py`,
`scripts/gen_components.py`, `scripts/gen_okf.py`, `scripts/gen_release_checklist.py`,
`scripts/intake.py`, `scripts/plan_briefs.py`, `scripts/traj_parse.py`,
`scripts/traj_views.py`, `registries/interfaces.template.toml`,
`INTERFACES.template.md`, `PROCESS.md`, `PROCESS_OPTIONS.md`.

**Your registry changes SHAPE, and the converter does the mechanical half.**
An `IF-###` row is now `owner` (the providing THING — a module path, a file or
directory path, or `external:<party>`; **never** an `SR-###`/`LLR-###`),
exactly one of `requestors` / `consumers` (the key IS the direction: requestors
put information into the owner's surface, consumers take what it emits),
`channel` (closed: `cli` `exit-code` `stdout` `file` `call` `env` `git`
`bytes`), an optional `data` (≤160 characters, the alphabet or schema pointer)
and the unchanged `version` / `status` / `rationale` / `verified_by` /
`carried_by` / tie-backs / `component` / `notes`. **Four cells leave:**
`provider` (folded into `owner`), `req_refs` (the requirement is reached
through the owner — the design rows whose `module` names it, or the module's
`Implements:` line), `signal` and `signal_note` (subsumed by `channel`).
`contract` stays as a LEGACY cell, read and counted by one warning, until its
content has moved into the owner's `Contract IF-###:` body; the arming slice
retires it. Run, from your repo root, with the kit checkout you are syncing to:

```
python <kit>/scripts/migrate_carrier.py --if-shape --check   # report only
python <kit>/scripts/migrate_carrier.py --if-shape           # rewrite in place
```

It rewrites each old-shape row in place (comments and order kept): `owner` from
the stated `provider`, else from the owner design row's single `module`;
`channel` SEEDED from the owner's kind (`call` for a module, `file` for a file
or directory, `bytes` for an `external:` party) — a seed, and the report says
so per row; `consumers` kept as `consumers`; the four retired cells dropped.
**Nothing leaves unseen:** every dropped `req_refs` value is printed in the
report beside its row, and every row whose owner could not be derived (an
`SR-###` owner with no `provider` — a published medium no cell ever named) is
listed for you to name by hand; until you do, `trace.py --strict` names it.
Then read each row once: move `consumers` to `requestors` where the far side
puts information INTO the owner (callers, invokers, writers), and confirm the
seeded `channel`. **Find the rows the converter could not finish:**

```
grep -n "^owner = \"\(SR\|LLR\)-" docs/requirements/interfaces.toml
```

*What replaces the `req_refs` grep* ("which seams does SR-012 touch?"): join
the other way — the SR's design rows name modules, and those modules own
rows — or read the module's `Contracts:` marker. The planning briefs now hand
a planner `Owner`, the far side, `Channel` and `Data` instead of the prose
`Contract`. Do not bump each row's `version`: the row's shape changed, the
interface semantics did not.

**Mint header-first from now on** (PROCESS.md §8): a work item that creates a
module mints its seam rows and the module's stub header before any code, so
parallel workers read the same home the finished module will have.

### The definition gate is armed [since 816090cd]

**Kit-owned files — overwrite and move on:** `scripts/kitlib/spine.py`,
`scripts/trace.py`, `scripts/check_trajectory.py`, `scripts/migrate_carrier.py`,
`scripts/gen_okf.py`, every CSV-reading script, `registries/interfaces.template.toml`,
`INTERFACES.template.md`, `PROCESS.md`.

**What reds now, and where.** `check_trajectory --strict` fails an interface
row with no stated definition: its owner declares it on a `Contracts:` line but
states no `Contract IF-###:` body ("declared, not stated"), or its header is
refused by the contract grammar, or a source declares a row the registry owns
to another in-tree source; an owner that declares nothing only warns (the
migration list). `trace.py --strict` fails a registry still carrying any of the
five retired cells, by KEY PRESENCE — a TOML row that sets one, even empty, or
a legacy CSV header that still declares the column (delete it) — `contract`
included, which the previous entry left as a counted warning. Both share the `[checks] interfaces_check` opt-out. **Find
the rows that will red before you upgrade:**

```
python <kit>/scripts/migrate_carrier.py --if-shape --check   # every row still carrying `contract`
python <kit>/scripts/gen_arch_map.py --src <src> --contracts-doc docs/interface-reference.md   # the "Declared, not stated" list
```

Each `contract` cell's text moves into the owner's header as its `Contract
IF-###:` body, then the cell is deleted; the converter reports the rows and
never drops the cell, because its content has no mechanical home.

**Where an `external:`-owned row is stated:** by the kit module on its far
side — the consumer that reads the external surface, or the requestor that
drives it — since the external party's header is not yours to write. Add the
row's id to that module's `Contracts:` marker and write the body there as
"our reading of" the surface: what is read or sent, what is assumed, what a
failure does. A module that is not the far side may not state it.

**A CSV registry may now carry the `#` header** (a `Contracts:` marker and
bodies at the top of `performance-budgets.csv`, say): every kit reader strips
a leading comment block before the header row, through the one shared reader
`kitlib.spine.csv_body`. A CSV your OWN tooling reads must skip it the same
way, or add no header to that file.

### The armed gate's blind spots close: a refused header, a retired column, a row with no in-tree endpoint [since 7fc42a5a]

*(Two commits: a cross-family adversarial round over the arming slice, then the
follow-on that minted the arms it surfaced — the kit's own registry grew to 163
rows there, which is the kit's spine and changes nothing in yours.)*

**Kit-owned files — overwrite and move on:** `scripts/trace.py`,
`scripts/check_trajectory.py`, `scripts/gen_arch_map.py`,
`scripts/kitlib/spine.py`, `scripts/spine_carrier.py`, `scripts/agent_route.py`,
`scripts/intake.py`, `scripts/check_flows.py`, `scripts/gen_okf.py`,
`scripts/schedule.py`, `scripts/derive_stage.py`, `scripts/check_perf.py`,
`scripts/integrate.py`, `scripts/subagent_gate.py`,
`registries/interfaces.template.toml`, `INTERFACES.template.md`, `EXAMPLE.md`,
`PROCESS.md`, `gitignore.template`.

**(a) One refused header used to disarm the WHOLE gate.** A source whose
`Contracts:` header the contract grammar refuses — an empty `Contract IF-###:`
opener, a body before its marker, a duplicate body, an HTML comment in a body —
was caught for the whole scan and answered "no surface", so one malformed
docstring anywhere in your tree made `check_trajectory --strict` exit 0 with
output byte-identical to a clean tree. A refusal is now the gate's FOURTH
finding shape, naming the source, and the scan continues past it;
`gen_arch_map --contracts-doc` still raises on the same header. **And,
correcting the previous entry, which overclaimed it: an owner that declares
nothing only WARNS** — the migration list, visible in the reference's summary
line, not a finding.

**(b) The five retired cells are found by KEY PRESENCE, per registry.**
`contract`, `provider`, `req_refs`, `signal`, `signal_note`: a TOML row that
sets one — even to `""` — or a legacy `interfaces.csv` whose HEADER still
declares the column is one `trace.py --strict` finding per retired key, naming
the rows, or the header column once. The old rule read VALUES, so an empty
retired column in a CSV header passed forever. The remedy is a one-line edit
either way: delete the key, delete the column.

**(c) A row with no in-tree endpoint is refused**, as the template header now
states it: "A row whose owner AND far side are all `external:` parties has no
in-tree endpoint — no module whose header can hold our reading of the surface —
so it is not a seam of this repo, and `trace.py --strict` refuses it." Such a
row owed its definition nowhere. State a repo-to-repo seam in the OWNING repo
and link it from the consuming repo as an `external:`-owned row with an in-tree
far side; a true crossing of your system boundary is a row in `external.toml`.

**Find the rows that will red before you upgrade:**

```
python project-trajectory/scripts/trace.py --root . --strict            # the retired-key and no-in-tree-endpoint lines
python project-trajectory/scripts/check_trajectory.py --root . --strict # "refused by the contract grammar"
grep -rn '^Contract IF-[0-9]*:\s*$' --include="*.py" .                  # an opener whose body is empty
```

**Four smaller changes in the same range.** `kitlib.spine.csv_body` treats
BLANK lines before the header as preamble — a blank between a `#` header block
and the header row used to become the header itself, hiding every column — and
it finally reaches every kit reader, which the previous entry claimed before it
was true: `agent_route` (the agents CSV carrier), `intake`'s legacy carrier read
and `spine_carrier.columns` were still raw, so a `#`-headed CSV now reads
identically everywhere. **`gen_arch_map.py` changes behaviour for any script of
yours that combines its flags:** one invocation naming several of
`--backlink-coverage`, `--cli-doc`, `--contracts-doc` runs EVERY named mode, in
that order, and exits with the worst code — before, only the first ran, so
`--check` could report a green over a stale target. `schedule.py` refuses
`simulate --jobs` below 1 with exit 2 through argparse instead of a `ValueError`
traceback, and its Usage puts `--root` before the subcommand, where argparse
always required it. `gen_okf` reads the text after a comment's `-->` on the same
line when it derives a Process Guide summary from a doc; it used to drop it.

**One line to copy by hand:** `gitignore.template` gains `out/subagent-gate.log`,
the PreToolUse spawn gate's best-effort decision log, an untracked cache — and
`.gitignore` is merged by hand (ADOPTING.md).

**Shipped texts re-stated, worth re-reading if you teach from them.**
`EXAMPLE.md` §9 and §10 show the one-owner row shape: the header body beside the
code, and the coordinator rows as `external:`-owned rows with an in-tree far
side. `INTERFACES.template.md`, `registries/interfaces.template.toml` and
`PROCESS.md` §8 say the undeclared owner warns and name the refused-header
shape; the two template headers state the no-in-tree-endpoint rule.

### The work-item schema gains `Adjudicates` — the scope of an adjudication's act [since d54bae41]

**What changed.** The work-item row schema (`wi_convert.COLUMNS` and its read-side
twin `kitlib.registry.WI_COLUMNS`) gains a 19th column, `Adjudicates`: the
`;`-joined registry row ids an adjudication was minted OVER. `intake`'s
first-approval mint writes it, and `adjudicate_brief` intersects the brief's LIVE
re-derivation with it, so the approval act cannot reach a row no merge handed it.
Empty on every row that is not an adjudication.

**Migration: none, if you carry the FOLDER home** — which is the live home since
Phase 2c. The column is a frontmatter key (`adjudicates`), and a key a spec file
does not carry reads as an empty cell, which is what every pre-existing row means.
Nothing to add, nothing to re-scaffold.

**If you still carry the legacy `docs/requirements/work-items.csv`:** add
`Adjudicates` as the last header cell and a trailing comma on every row.
`wi_convert.load_csv` REFUSES a header that is not the declared schema, by design
— a converter that guessed at an unknown shape is how a column gets dropped — so
the refusal names the mismatch rather than silently losing a cell. This is the
same one-cell migration the `Supersedes` and `Brief` columns needed and, unlike
those two, it is written down: **that omission is the reason this entry exists**,
so if your header predates either of them, add all three at once.

### `supersedes` accepts a LIST of ids — and now refuses two shapes it used to mint [since 36395b54]

**What changed.** A successor's `supersedes` may name SEVERAL predecessors, as a
TOML list, because a consolidation absorbs several rows into one row that carries
all of them. A bare id string is unchanged in every respect — same cell, same
bytes in the spec file — and `intake.supersedes_ids` is the one reader of both
spellings, so the registry cell stays `;`-joined and every dependent of every
absorbed row is re-pointed in ONE pass.

**Migration: none for the value; TWO NEW REFUSALS to know about.** This entry
exists for the half that is not additive — the mint is all-or-nothing, so either
refusal stops the whole intake at a merge rather than minting a bad row:

1. `intake._draft_refusal` now checks the SHAPE of a hand-authored
   `## Dispositions` block's `supersedes`: every entry must match `WI-<digits>`.
   A block that carried prose there ("the row above", a title, a bare number)
   used to mint and simply re-point nothing; it now refuses by name.
2. `intake._mint_shape_refusal` gained a LIVENESS arm: a `supersedes` naming an
   id that is no row in the pre-mint registry refuses. A typo'd id used to leave
   the row it meant to absorb queued beside its own successor, silently.

If your loop stops at a merge with `every entry must be a WI-### id` or `no live
registry row`, the disposition block is the thing to fix — the refusal names the
offending token and nothing was minted.

**AMENDED by the round-2 review, same migration (none), two more refusals.**
(3) A hand-authored `supersedes` STRING must now be exactly one `WI-###` id;
several ids are a TOML list. The `;`-joined spelling is the WRITER's (it is how
the registry cell round-trips) and was never a documented authoring form —
`supersedes = "WI-1;WI-2"` in a `## Dispositions` block now refuses with `a
string names exactly ONE WI-### id`. (4) A draft may not supersede a row that is
already `restructured`: lineage does not chain, so name the row that absorbed it
instead (`naming a row that is ALREADY restructured`). Both refuse before
anything is written.

### A fourth terminal work-item status, `restructured` [since 891a5b24]

**What changed.** The work-item status vocabulary gains a fourth terminal word,
`restructured`, with the directory `docs/archive/work/restructured/`. A row lands
there when a **consolidation** absorbs it into a successor: several overlapping
queued rows are replaced by one row that carries all of them. Its scope text
stays byte-identical and its `## Deliverable` is exactly one line,
`Restructured into WI-<successor>.`

It exists because neither sibling can carry that meaning. `cancelled` says the
scope was REFUTED, and says it loudly — `intake.context_block` briefs every later
row on the same SRs with the cancelled precedent "do not re-propose the refuted",
so an absorbed row filed as cancelled would tell its own successor not to build
it. `partial` says a lane stopped early, and owes a per-close report under
`docs/handbacks/` plus a minted disposition, neither of which a consolidation
produces.

Its `## Deliverable` is PARSED, not merely required to be non-empty: R-A refuses
anything but the exact line above (several successors comma-separated, and
surrounding whitespace ignored), and every successor it names must be a DISTINCT
FORWARD CARRIER — a registry row, not this row itself, named once, not itself
`restructured`, and naming this row back in its own `Supersedes` cell. The last
two make a chain (A → B → C) and a cycle (A ↔ B) unrepresentable rather than
merely unlikely: a reader following the record lands on the absorbing row, never
on another redirect (that row may since have closed `done`, `cancelled` or
`partial` — liveness is "is a registry row", not "is still open"). A hard error, like the rest of R-A. Its `SpecRef`, on the other hand, is a
MAY: R-F carves out both terminals whose work CONTINUES in a successor
(`partial` and `restructured`), so the cell may stay or be cleared. If you carry
restructured rows written before this, check the two cells; nothing else changes.

Terminal means terminal: nothing re-claims a restructured row, and no LANE may
close into one — `kitlib.station.CLAIMED_OUTCOMES` and `integrate.Outcome` are
deliberately unchanged, so only a consolidation close or a hand trunk commit
files a row there. Its inbound hard edges are re-pointed to the successor at the
close; an edge still naming it is reported as a dead one by both the scheduler
(`waiting:hard-pred-restructured:`) and `check_trajectory.dead_dependency_findings`,
never silently satisfied.

**Migration: additive — you gain a folder, nothing you hold changes.** No
existing row, cell or file means anything different. Two optional steps:

1. `mkdir -p docs/archive/work/restructured` and put a `.gitkeep` (or a README)
   in it, so the folder is tracked — this is what `bootstrap.py` now scaffolds
   for a new repo. You can also skip it: the folder is created on demand the
   first time a spec moves there (`spec_move.py` makes the destination's
   parent).
2. If your `docs/work/README.md` predates this, its location→status table and
   its "three terminal states" prose are now one row and one word short. The kit
   copy (`project-trajectory/work/README.template.md`) carries the updated text;
   the file is yours to own, so re-copy or hand-edit as you prefer.

Nothing detects a missing folder, because nothing needs to: an absent status
directory reads as zero rows in that state, which is what it means.

### The merge gate reads the ROUND FILES, not a hand-authored rollup [since 6e19da1e]

**What changed.** `integrate._verdict_gate` no longer requires
`docs/reviews/WI-<n>-REVIEW-A.md`. It computes its predicate over the round
files your loop already writes — `docs/reviews/<train>/<NNN>-REVIEW-<X>-<sha7>.md`
— restricted to rounds a **logged reviewer session** produced (the coordinator's
own committed session log `docs/iteration/<train>-<NNN>-*.log`, whose `# phase:`
header names a REVIEW phase). An implementer-authored file in the review path is
therefore not a round, which it used to be able to become.

And the governing rule changed from an ORDERING to an IDENTITY. A verdict counts
only if it names the branch's current **non-record tree** — the tree with
`docs/reviews/`, `docs/log.d/` and `docs/iteration/` removed. There is no
timestamp comparison left: a commit that changed the work changed the tree, so
the verdict simply no longer names it, and a commit that only recorded the
process cannot invalidate anything. (`docs/work/` is IN the identity, exactly as
it was in the retired comparison.) The identity is read at the branch's WORK TIP,
so a station refresh still does not stale an honest APPROVE.

Two additions ride with it, both optional for you:

- **`Review-Verdict: APPROVE|CHANGES-REQUESTED rounds=<N> tree=<64 hex>`**, a
  commit trailer the coordinator writes on the commit that records a round — the
  `Bar-Green:` pattern applied to a verdict. It is ADDITIVE and costs you nothing
  until your loop writes one; the gate reads it as a cross-check (a trailer that
  names the tree under judgement and contradicts the rounds refuses) and never as
  an accept path. `N` is the number of completed review cycles represented at
  that governing tree (a dual REVIEW-A/REVIEW-B cycle still counts once); rework
  changes the tree and starts that count over.
- **`gen_verdict_rollup.py`**, which regenerates a human-readable per-review-scope
  rollup into `docs/reviews/rollup/<train>.md`. It is declared in
  `docs/stack.ini [generated]`, gated by `--check`, run by `trunk_step.py --regen`,
  and **never read by the gate**.

**Migration: a window, and you are inside it if you run `review-policy = 1`.**
For the length of the window the gate accepts EITHER the round-file evidence or
a legacy hand-authored `docs/reviews/WI-<n>-REVIEW-A.md`, and **warns on stderr**
whenever the legacy path is what cleared it. The legacy rollup is judged by the
same identity rule (it names this tree or it does not count), so a rollup that
used to clear the gate still does.

**At `review-policy = 2` there is no window**, deliberately: that dial declares
two INDEPENDENT reviewer phases, and one hand-authored document is one author's
word — honouring it would clear both phases on a single reviewer. If you run
policy 2 on legacy rollups today, your first merge after taking this kit refuses
with *"the governing round(s) at this tree are not an APPROVE (REVIEW-A,
REVIEW-B)"*: draw the rounds, or sit at policy 1 for the length of the window.

Three steps, in the order that costs least:

1. Do nothing and keep merging. Read your integrator's stderr: every WARN naming
   `LEGACY hand-authored rollup` is a lane that would stop once the window
   closes.
2. Add the two `[generated]` and `REGEN_STEPS` rows if you carry your own copies
   of `docs/stack.ini` and `trunk_step.py` — the kit ships both, and an adopter
   who takes `trunk_step.py` without the `docs/reviews/rollup/` declaration will
   have a lane commit a generated artifact.
3. Add `[attestation] adjudication_review` to `docs/process.toml` (see the entry
   below) if you run adjudication lanes.

The window closes when the kit says so, not on a date; nothing here is removed in
this change.

### `[attestation] adjudication_review` — whether a judgement gets its own round [since 6e19da1e]

**What changed.** A new dial over the closed alphabet
`"never" | "when-minting" | "always"`, shipped at `"when-minting"`. It decides
BOTH whether the loop schedules a review round after a committing `ADJUDICATE`
session and whether the merge gate demands that lane's verdict — one reader,
`agent_common.adjudication_review_owed`, so the two cannot come apart.

Before it, `ADJUDICATE` was in `agent_loop.NON_BUILD_PHASES` (no round was ever
scheduled) while the gate demanded a verdict from every merged WI. If you run
adjudication lanes on an older kit, every one of their merges is a stop that only
a human can clear. That is the defect this closes.

`when-minting` demands a round when the verdict drafts ANY successor at `spine`
or `high-risk`, or when its brief is `consolidate` — the cases where the
judgement creates exclusive work or moves scope. An amendment that only
recommends a flip, a red-tc drafting ordinary fix rows, and a clean-close spot
check get none.

**Migration: additive, with a default that changes behaviour.** An undeclared key
reads as `"when-minting"`, so taking this kit CHANGES what your adjudication
lanes are asked for: most stop owing a verdict they could not produce, and a
minting one starts having a round drawn for it. Declare `"always"` in
`docs/process.toml [attestation]` if you want the old intent (now actually
implemented rather than merely demanded). The value is refused at preflight if it
is not one of the three words — a typo is loud, not a silent fallback.

### A committing DESIGN-CHECK arms the review round itself [since 87421a12]

**What changed.** After a `CHANGES-REQUESTED` round under a loop-held tier the
escalation ladder re-arms a `DESIGN-CHECK` session, which runs the worker brief
with the findings attached — so its commit IS the rework. Until now only a
`BUILD`-phase commit armed the next review round, so every cycle ran a second
`BUILD` session whose only job was to produce a commit: it re-verified the
design-check's work and re-ran the full suite inside its turn. Measured on one
lane (WI-579, 2026-09-03, eleven rounds): 13 such sessions, 5.1 h, against 4.4 h
of actual rework and 1.2 h of review. `agent_loop.build_bookkeeping`'s
`DESIGN-CHECK` arm now records the session as the committing build (its family
is the one the reviewer must differ from) and schedules the round, exactly as
the `BUILD` arm does. A non-committing design-check still arms nothing and the
next phase still resets to `BUILD`.

**Migration: behavioural, no file changes.** A loop-held run whose lane took a
`CHANGES-REQUESTED` verdict now goes design-check → review instead of
design-check → build → review. If you relied on the extra build session as a
same-family second look at the design-check's rework, the reviewer round is
that look. Nothing to edit; re-sync the script.

### Four batch-lane defects: the walk, the two closes, and the mechanical-close peel [since f4ca1bd5]

**What changed.** Four independent fixes, all specific to a lane carrying a
MULTI-ROW `--wi 'A;B;C;D'` assignment (the §A4 spine batch). A one-row lane hits
none of them and observes none of the fixes. Measured 2026-09-03 on one
four-row lane plus the WI-586 adjudication merge.

1. **The walk asks the tree as well as the trailer.**
   `agent_loop.current_assignment_wi` counted a row done with once its `WI:`
   trailer was committed, while `integrate.finished_branches` asks whether the
   spec has left `active/<branch>/`. A row whose session committed the trailer
   and ran out before its close ritual satisfied one reader and not the other:
   the walk stepped past it for the rest of the lane and the branch never
   counted as finished. A row is now BUILT only when both halves hold, and the
   tree read is `integrate.claimed_ids_on_branch`, beside `finished_branches`.
2. **Neither close treats a row the lane already closed as its own.** Both
   `handback.close_partial` and `handback.close_adjudication` read the claimed
   set off the TRUNK, which lists every row of a batch. `close_adjudication`
   read an already-moved spec as "cannot read the claimed spec" — which
   `dispatch._close_done_adjudication` turns into `EXIT_PREFLIGHT`, ending the
   whole run over a lane that owed nothing — and `close_partial` would have
   moved such a row a second time, overwriting the outcome the lane itself
   declared. `handback.open_claimed_specs` is the one filter both now apply; an
   empty result is the documented NO-OP, never a refusal. The report-immutability
   rung moved ABOVE that filter, so a second close of a row already in
   `partial/` still refuses.
3. **A row this branch closed is not a stale assignment.** The worker preflight
   refused any assigned WI whose registry `Status` is terminal. On a
   partly-finished batch that is every row the lane closed itself, so a resumed
   worker refused its own work. `agent_common.stale_terminal_assignment` now
   asks whether the row is terminal for a reason OTHER than this branch's own
   `WI:` trailer over `merge-base(trunk, HEAD)..HEAD`. `trunk_name` and
   `default_base` moved from `agent_loop` to `agent_common` for it (re-exported
   there) rather than growing a second merge-base rule.
4. **`EXIT_PREFLIGHT` is no longer a lane outcome.** It left
   `dispatch._WORKER_OUTCOMES`. A preflight refusal is the worker saying it
   could not START, so it is evidence about the launch and never about the work;
   handing back on it committed the lane's uncommitted residue as-is and moved
   rows to the terminal `partial/` over a failure the lane could not have caused.
   Such a lane now parks exactly like a crashed one — the claim stays in
   `active/`, the next cycle resumes it, and the stall guard bounds it.
5. **The mechanical adjudication close is a DISPOSABLE commit.** An adjudication
   lane cannot obey "close before the final verdict round": the round is drawn
   while the row is still in `active/`, and `close_adjudication` moves the spec
   afterwards, at the worker's DONE. Since `docs/work/` is IN the non-record
   tree identity, that machine-authored move staled the APPROVE that had just
   judged the row and the merge slot refused. `kitlib.verdict.governing_rev` now
   peels it, on exactly the refresh commit's argument and with the same
   verify-against-git discipline: the subject must be the one
   `kitlib.station.mechanical_close_subject` composes, the commit must have
   exactly one parent, and every path it changed must be under `docs/work/`.
   Each check fails toward MORE review.

**Migration: behavioural, no file changes — but read (4) before you re-sync.**
Nothing in your tree needs editing; take the scripts. Two behaviours change for
an unattended run. A worker exiting `EXIT_PREFLIGHT` no longer produces a
`partial/` close and its `docs/handbacks/` report: if your wrappers or a
dashboard counted those to notice a broken launch, the signal is now the
dispatcher's `REFUSED ITS PREFLIGHT` line on stderr and, if it persists, the
stall guard's exit 4. And an adjudication lane that used to stop at the merge
gate for a hand-compiled legacy rollup after its mechanical close now merges on
the round it actually drew — if you hold such rollups, they stay valid through
the policy-1 migration window and nothing new needs writing.

### The trunk step regenerates the live approval brief [since dc395734]

**What changed.** `trunk_step.REGEN_STEPS` gains a leaf step,
`approval-brief` — `trace.py --approve modified --out docs/ratify/CURRENT.md`,
armed when the brief exists. Measured 2026-09-04 on an adjudication lane
whose approval act moved the `docs/archive/last_approved` snapshot: its tip
carried a stale brief, the station's refresh regenerated every other declared
artifact, and `check.py`'s `approval-fresh` step reddened the refresh bar on a
file nothing in the table named. Regenerating it on the lane AFTER the
round would have changed the tree identity the round named; the refresh
commit is the one commit the verdict gate peels, so the station is where it
has to happen.

**What to do.** Re-sync `scripts/trunk_step.py`. Nothing to edit: a repo
without `docs/ratify/CURRENT.md` skips the step, and one with it gets the
brief refreshed on every trunk step from now on. If your merge slot has ever
refused a lane on `approval-fresh` alone, that class is closed.

### The verdict rollup is written by the trunk step only [since 7ea3cce7]

**What changed.** `gen_verdict_rollup.py` refuses a direct write (exit 2,
reason on stderr) when the checkout is on any branch other than the trunk —
the primary checkout's branch per `agent_common.trunk_name`. `--check` never
writes and is never refused. `trunk_step.py` passes the new `--trunk-step`
flag, the one writer allowed off the trunk, because the station's refresh
runs the trunk step inside the lane worktree. This is LLR-208's
exclusive-writer clause ("a work branch never writes the rollup") enforced
rather than stated: measured 2026-09-04, the generator wrote
`docs/reviews/rollup/` in a claimed lane and returned 0, and the work-branch
freshness stand-down hid the write. A single-checkout repo is its own trunk,
so an attended run and every fixture keep writing as before.

**What to do.** Re-sync `scripts/gen_verdict_rollup.py` and
`scripts/trunk_step.py` together — the flag and its one caller ship as a
pair. Anything else that invoked the generator directly from a work branch
(a lane hook, a make target) now gets the refusal and should stop; the merge
regenerates the rollup.

### The CONSOLIDATION adjudicator — a fifth brief, a new column, and one retired template [since 1c258508]

**What changed.** The queue can now be judged for overlap, and the judgement can
absorb several rows into one. Five pieces, and the fifth is a deletion:

- **`prompts/adjudicate-conflict.template.md` is RETIRED**, with its
  `ADJUDICATE-CONFLICT` prompt key and its catalogue row. It shipped a template
  and a verdict grammar and never had any of the three things that make a brief
  real: nothing minted a queue-conflict row, no assembler filled its slots, and
  nothing read the `needs=` its own grammar demanded.
- **`prompts/adjudicate-consolidate.template.md` replaces it**, carrying its
  three questions (contradiction with the spine, scope overlap, already
  answered) plus a fourth outcome it lacked. `adjudicate_brief.VERDICT_GRAMMAR`
  gains `consolidate`: `OUTCOME: QUEUE|QUEUE-WITH-EDGE|RETURN-TO-DRAFT|
  CONSOLIDATE needs=<id or -> absorbs=<id;id;… or ->`, both counters required on
  every alternative.
- **`scripts/consolidate.py` is a new module** — the census that decides which
  queued rows are one work item wearing several ids, and the three guards that
  stop the question being asked twice. `intake.py` imports it UNGUARDED, so a
  scaffold missing it ImportErrors on the first mint.
- **A new registry column, `Digests`** (`<queue sha>|<spine sha>`), in
  `wi_convert.COLUMNS` + `SCALAR_FIELDS`, `kitlib.registry.WI_COLUMNS` +
  `SPEC_SCALARS`, `plan_artifacts.WI_HEADER` and
  `registries/work-items.template.csv`. Empty on every row that is not a
  consolidation.
- **`handback.close_adjudication` gains a consolidation arm**, reading a typed
  `## Consolidation` TOML block in the judging row's own spec:
  `queue-with-edge` writes the hard `needs` edge (the reader the conflict brief
  promised and never got), `return-to-draft` moves `queued/ -> draft/` with the
  verdict's finding quoted into Context, `consolidate` hands the absorbed set to
  the mint. `intake._mint` then moves every absorbed row into
  `docs/archive/work/restructured/` with `Restructured into WI-<successor>.` as
  its whole Deliverable — at the MINT and not at the close, because that line
  names an id `_mint` allocates and because `_supersedes_refusal` refuses a
  draft continuing an already-`restructured` row.

`check_trajectory.queue_conflict_findings` keeps its signature and its output;
it is now the rendering of a new pair-level producer, `queue_conflict_pairs`,
which the census reads for EDGES rather than parsing the warn sentences.

**What to do.**

1. **Re-sync the kit-owned files as a set** — `scripts/consolidate.py` (new),
   `scripts/intake.py`, `scripts/handback.py`, `scripts/adjudicate_brief.py`,
   `scripts/check_trajectory.py`, `scripts/wi_convert.py`,
   `scripts/kitlib/registry.py`, `scripts/plan_artifacts.py`,
   `scripts/prompts.py`, `scripts/bootstrap.py`, and the two prompt templates
   (add `adjudicate-consolidate.template.md`, delete
   `adjudicate-conflict.template.md`). They are one change: `intake` imports
   `consolidate` at module scope, and the column has to land in all four schema
   homes or the mint writes a cell every reader drops.
2. **Add the `Digests` column to your own work-item registry header**, if you
   carry the legacy CSV form. The spec-folder form needs no migration: an
   absent frontmatter key reads as an empty cell, and every existing row is
   correct with one.
3. **Delete any local reference to the `conflict` brief.** A row whose `Brief`
   cell says `conflict` now refuses at composition as an unknown brief and is
   HELD for a human — which is the intended failure, but re-point the cell to
   `consolidate` (or clear it) rather than leaving a row that pages someone.
4. **Wire the census into your dispatcher, or do not.** The mint arm is
   `intake.mint_consolidation(root, busy)`; a repo that never calls it is
   exactly as it was, because nothing else mints a `consolidate` row. Where the
   kit's own `dispatch._admit` calls it, the call site is four lines at the top
   of a tick, after the parked-branch arm and before the frontier is loaded:
   mint, print the refusal to stderr and exit non-zero if there is one.
5. **Expect nothing on an empty queue.** The census refuses on an idle station
   with no overlap, on a station holding any adjudication row, and on any queue
   state a `consolidate` row has already judged — including one whose row has
   since gone terminal. If it mints on your first tick, it found real overlap.
### `intake.py sweep --before/--after` is a RANGE sweep, not a repo scan [since 5bf9f28c]

**What changed.** `sweep` used to run the terminal-folder walk on top of
whatever range it was handed: it built its outcomes map by globbing
`docs/work/{partial,cancelled,complete}/` **and** their `docs/archive/work/`
siblings, then passed that map to `intake_after_merge` alongside `--before`
/`--after`. On a repo with any history that means every close ever archived is
reconsidered beside a two-commit range, so the subcommand was unusable for its
one stated job — re-running the intake for a landed merge — and a supervising
session had to call `intake.intake_after_merge(root, before, after,
outcomes=None, branch=...)` from a Python snippet instead (measured on this
kit's own trunk, 2026-09-04, for an out-of-band range that owed two rows).

Given `--before` or `--after`, the sweep now runs triggers (a)/(a2) over
exactly that range and nothing else — the same call `integrate.integrate_one`
makes inside the held merge slot, minus the outcomes map no out-of-band range
has. Two new flags: `--with-terminal` asks the terminal scan back on a range
sweep, and `--branch <label>` names the mint subject (a range sweep with no
`--branch` labels itself `sweep <before>..<after>`). A **bare** `sweep` with no
range is unchanged — `HEAD..HEAD` plus the terminal scan. The ending is a
count (`_mint` already announces each row it writes) or `nothing to mint.`
with exit 0; a refusal still prints and exits 1. Idempotence is unchanged and
unchanged in kind: the mint's exact-title dedup answers a re-run of either
shape, so a range sweep repeated mints nothing the second time.

**Migration: no file changes.** The kit script is the whole change; re-sync
`intake.py` and regenerate your CLI reference if you keep one
(`gen_arch_map.py --src <scripts> --cli-doc <doc>`). Behaviourally, a runbook
or operating note that reaches for `sweep --before X --after Y` now gets the
range alone — if you were **relying** on the incidental terminal scan riding
along with a range (an unlikely dependency, and one that scaled with your
archive rather than with the range), add `--with-terminal` to that invocation.
A bare `sweep` needs no edit.
### The station settles a `[generated]` refresh conflict, and an ignored `.venv/` no longer blocks the unload [since d11250de]

**What changed.** Two independent fixes in `integrate.py`, each measured
three times on 2026-09-04's queue drain.

*The refresh.* When merging the trunk into a lane CONFLICTS, `refresh` now
lists the conflicted paths and takes the TRUNK side of every one DECLARED in
`docs/stack.ini` `[generated]`, then continues into the trunk step exactly as
a clean merge does — that step regenerates those files from source seconds
later, so the conflict has no content question in it. Three refreshes that day
refused with `PROJECT_STATE.html` / `docs/ratify/CURRENT.md` as the only
conflicted paths, and a supervisor resolved each one by hand, identically. One
declared kind is held back BY NAME: `linecounts`
(`tests/test_module_size_ratchet.py`), whose rows are measured data
re-stamped by hand with a reason, so both sides of a conflict there carry a
reviewed reason and no command re-derives them. A conflict with anything else
in it — product code, a delete/modify git cannot take `--theirs` on — still
refuses with the message it always carried, plus the list of generated paths
settled first. The `[generated]` declaration is read, not restated:
`_generated_table` parses it into `{path: kind}` and the RULING-6 audit's
`_generated_paths` is two lines over it.

*The unload.* §5.6 stops counting ignored BUILD RESIDUE as dirt: `.venv/`,
`__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage*`. Three merged
lanes that day ended `UNLOAD INCOMPLETE … DIRTY (1 uncommitted or ignored
path(s))` over the lane's own `.venv/`, exiting 1 after every merge. A real
virtualenv is NOT shed file by file — `git worktree remove` takes it with the
lane — but a `.venv` that is a SYMLINK is unlinked under `os.path.islink` and
never followed, because the shared virtualenv it points at lives outside the
lane. Everything outside the allowlist keeps the existing caveat verbatim,
an ignored `out/run-logs/` stream included.

**What to do.** Re-sync `scripts/integrate.py`. Nothing to edit and nothing
to declare: the auto-resolve reads the `[generated]` section your repo already
has (a repo that declares none resolves nothing and refuses exactly as
before), and the residue allowlist is enumerated in the script. If your
`[generated]` table declares an artifact whose rows are hand-stamped rather
than regenerated, give it the `linecounts` kind — that kind, not the path, is
what holds it back.
### A MINOR-only refusal routes as an APPROVE [since 68bd9ebd]

**What changed.** `kitlib/verdict.py` gains `effective_verdict(word,
findings)`: a `CHANGES-REQUESTED` carrying at least one finding, all of them
`[MINOR]`, is READ as an `APPROVE`. The reviewer's round file is never
rewritten — its own `VERDICT:` line and its findings stand as written; what
changes is what the two readers do with them, and both apply the rule or it
buys nothing. The loop reads it through the new
`score_reviews.merged_routing_verdict` (which prints `review round:
CHANGES-REQUESTED with MINOR-only findings routed as APPROVE (N findings
carried)` when the reading changes the outcome) and the merge slot through
`kitlib.verdict.round_entries`, so a lane routed as approved is not then
refused at the slot. A `CHANGES-REQUESTED` naming NO finding stays a refusal:
a reviewer who blocks without naming anything is a different defect.
Measured 2026-09-03/04: four rounds refused a lane over a single `[MINOR]`
each (WI-586 rounds 006 and 010, WI-590 round 013), every refusal costing a
rework session AND another round.

**What to do.** Re-sync `scripts/kitlib/verdict.py`, `scripts/score_reviews.py`
and `scripts/agent_loop.py` together — the rule and its two readers ship as a
set. Nothing to edit and no dial: if you WANT a MINOR to block, raise it as a
MAJOR, which is what the severity scale already meant. Your existing
`prompts/reviewer.template.md` needs no change; the kit's own is unchanged
because nothing in it said a finding of any severity forces a refusal.

### No review round is drawn on a tree a verdict already named [since 68bd9ebd]

**What changed.** `kitlib/verdict.py` gains `tree_already_judged(root, branch,
base, parse)` — the merge slot's own question (does a logged round already name
this governing tree?) — and `agent_loop.schedule_review_round` asks it BEFORE
queueing a round. When the answer is yes it prints `dispatch: no review round
scheduled — rework changed no non-record path; a round on the same tree would
be refused as a reroll` and escalates through the existing page ladder instead
of drawing the round. Measured 2026-09-03: a rework that DECLINED a finding
committed only its answer under `docs/reviews/`, a record path the identity
ignores, so the redrawn round approved the very tree the first had refused and
`integrate._round_refusal` refused the pair as a reroll-until-green — two
reviewer sessions and a merge attempt for nothing, with no line saying why.
Unreadable git answers "not shown to be unchanged" and the round is still
drawn, so a repo the readers cannot see into never wedges its first build.

**What to do.** Re-sync `scripts/kitlib/verdict.py` and `scripts/agent_loop.py`.
Nothing to edit. `schedule_review_round`, `schedule_adjudication_round` and
`build_bookkeeping` now return an exit code (or `None`) so the page can end the
run — if you have forked any of the three, thread the return value through.
Your loop-held runs degrade to a DESIGN-CHECK exactly as a review escalation
does; human-held runs stop with a banner naming the cause.
### The coordinator resumes a finished lane that owes a round, and a pause stops only the claim [since 678801c1]

**What changed.** Two arms of `dispatch.py`, both about a lane the run had
decided was beyond a worker's help.

`_round_owed` + `_parked_branches`: before the merge slot sees a finished
branch, the coordinator asks whether that branch still owes a review ROUND at
its current tree, and resumes it as a worker if it does (the existing
parked-resume path — `dispatch: cycle N - resuming parked branch …` — whose
worker schedules the owed phases through `agent_loop.resume_owed_round`). Only
a branch that owes nothing goes to the slot. Measured 2026-09-04 on a lane that
was DONE and then had its tree moved by a rework of the spec's
`## Dispositions`: the merge slot refused "no logged review round names its
current tree" and the run exited with no worker ever resuming to draw it. The
predicate composes the two readers that already own the question —
`integrate._verdict_gate` (would the slot refuse at all: the reviewer dial, the
adjudication waiver, the legacy-rollup migration window) narrowed by
`kitlib.verdict.phases_owed` at the governing identity (was the phase ever
DRAWN here) — so a dissent, a reroll-until-green or a contradicted attestation
still stops the run for a human instead of earning another draw, and a lane
carrying a legacy rollup still merges on it.

The pause arm: `docs/work/pause` now stops the CLAIM and nothing else, which is
what §5.6 always said ("pause = stop claiming; everything in flight finishes,
integrates and archives"). A fresh launch under a pause resumes every parked
lane and integrates every finished branch exactly as an unpaused run does;
`EXIT_PAUSED` (8) comes when nothing is left in flight. Before this a fresh
`agent_loop.py --root .` under a tracked pause exited 8 immediately and
stranded the very lane the pause promises to finish and merge.

**What to do.** Re-sync `scripts/dispatch.py`. Nothing to edit and no
migration: both changes are read off state your repo already keeps (the claim
directories, the branch refs, the round files, the pause). Two behaviours to
expect. (1) If your repo runs at `review_rounds >= 1`, a finished-but-unmerged
branch whose tree no round names is now RESUMED rather than refused — budget
one more worker session for it, and note that a lane which draws no round at
all is bounded by the iteration budget and the trunk-unmoved stall guard, not
by a round cap. (2) If your operating notes carry the "delete the pause, launch,
re-create it" recipe for resuming a lane under a pause, drop it — the launch
does that itself now. One deliberate ordering change: a pause over a DIRTY
trunk with nothing in flight reports the dirty-trunk refusal (exit 2) rather
than the pause banner, because the drain a pause now performs needs a clean
trunk like every other merge.

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
