# Owner-feedback batch — gate cadence · campaign language · owner scratchpad · archive scan-scope · How-SW containment — PLAN

**Status:** 🟢 **RULED BY DIRECTION (owner, 2026-07-11)** — five feedback
items; FB3/FB5 are explicit directives, FB1/FB2/FB4 are answered questions
whose adopted mechanism is recorded here (working defaults flagged where the
coordinator chose the cut). Ingested as **WI-071…WI-073**. Spine-touchers
ride the one pending G3 re-attestation (the campaign ruling).

---

## FB1 — Gate cadence: stop running the full gate per slice

**Owner question.** The full G3 gate appears to run after every change during
iteration — expected? Is there a better mechanism to defer gate checks until
all changes land, or run only relevant tests?

**Diagnosis (honest).** The kit mandates per commit only the **commit bar**:
the pre-commit hook floor (trace integrity, secrets, freshness steps —
seconds) plus `pytest -q` + `check_docs --stale`. The full 13-step
`check.py --gate G3` — which re-runs the whole suite *under coverage* — is
the **gate bar**: required when a gate advances or its evidence is
re-verified, and run by CI's `gate` job. Running it at the end of every WI
session was orchestration convention, not a kit rule; every adopting repo
inherited the same convention.

**Adopted mechanism (the campaign cadence).**
- **Mid-campaign WI sessions end at the commit bar.** The full gate is NOT
  required per slice.
- **The full gate runs once at campaign close** (the coordinating close),
  and CI runs it on every push regardless — a mid-campaign regression is
  caught by the per-commit suite run; the coverage/format/gate tiers are
  verified at close.
- **Test-impact selection is rejected**: running "only relevant tests"
  invites the false green the harness contract exists to prevent (a missed
  transitive dependency passes silently; the coverage floor breaks). The
  sanctioned cheap layer for repos with slow suites is the existing
  `stack.ini [tiers]` **smoke** tier (`pytest -m smoke` per commit, full
  tier at gates) — declared, visible, already supported; no new code.

**Steps.** State the cadence once in PROCESS_OPTIONS (inside the campaign
paragraph); update the `session-protocol` skill (source + fan-out copies stay
byte-identical — the skills-sync gate) so sessions know which bar applies.
Docs only.

## FB2 — "campaign" adoption in the documentation

**Owner question.** Is the language "campaign" adopted into the
documentation / README?

**Answer.** Partially: the campaign ruling paragraph lives in PROCESS_OPTIONS
("Trajectory / work-items layer") and the kit README mentions it once; the
**root README does not**. **Adopted:** one sentence in the root README's
process material naming the campaign convention (batch spine-touching work so
one owner sitting re-attests it all), pointing at PROCESS_OPTIONS — the term
is load-bearing vocabulary now and readers start at the README. Docs only.

## FB3 — `OWNER_SCRATCHPAD.md` (owner directive)

A root **`OWNER_SCRATCHPAD.md`** in this repo AND scaffolded to templated
repos (an `OWNER_SCRATCHPAD.template.md` in bootstrap's MAPPING), with
specific instructions for LLM agents to **IGNORE / not utilize** the content:
it is for a human to keep notes in; those notes may be old, augmented, or yet
to be formed.

**Shape.**
- The file opens with a loud, unambiguous header block: *for the human owner
  only; LLM agents must not read, index, summarize, cite, or act on anything
  in this file; nothing here is a requirement, ruling, or working surface —
  the working surfaces are `docs/status.md`, the registries, and `docs/log.md`;
  notes may be stale, contradictory, or half-formed.* Below the header, an
  empty notes area.
- **check_docs exempts it entirely** (links, orphans, stale hints) — free-form
  human notes must never gate a commit.
- The **secrets floor still applies** (check_privacy scans staged diffs
  regardless of file) — state that in the header so the owner knows notes are
  not a secrets-safe zone.
- Agent-side enforcement home: the file's own header is primary. If a
  one-line mention fits `AGENTS.template.md`'s byte budget by tightening
  elsewhere (the working-agreement precedent), add it; otherwise the header +
  a PROCESS_OPTIONS line suffice — record the decision either way. The meta
  repo's `CLAUDE.md` (not budgeted) gets the one-liner.

## FB4 — check_docs and the archive (answered question)

**Owner question.** Should check_docs ignore the archive?

**Answer + adopted scope (working default — flagged for veto).** Half-ignore:
- **Keep broken-link validation** for `docs/archive/` — a link in the design
  history that resolves nowhere misleads future readers, and the archival
  flow already re-bases links once at archive time (cheap, mechanical, done
  twice this week without pain).
- **Drop archive files from orphan warnings and stale-mtime hints** — an
  archived doc is frozen context; "possibly stale vs a live file" and
  "nothing links to it" are noise there by definition.
- `OWNER_SCRATCHPAD.md` is fully exempt (FB3).

## FB5 — How-SW top view: ≤10 items, containerized by component (owner directive)

**Owner directive.** In the software-architecture diagram on
`PROJECT_STATE.html`, the **first view must show at most 10 items**. To
contain this, software items that belong to a component are **containerized**
into that component (and a component may contain components). Exceeding the
bound is a **failure**, to drive right-sizing of component designations.

**Model.**
- **Membership** = the AXES-ratified mechanism: `Component` list-tags on LLR
  rows join `LLR.Module` → `CMP-###` (authored, machine-suggestable by
  path-prefix); CMP nesting via the CMP registry's `PartOf`.
- **The top view** of the How-SW panel shows top-level components (a CMP with
  no `PartOf`) plus any **uncontained modules**; expanding a component
  reveals its members (members render inside/beneath their container —
  progressive disclosure, deterministic layout, the existing interaction
  idiom; IF edges aggregate to the container boundary at the top level).
- **The right-sizing rule:** top-view item count (top-level CMPs +
  uncontained modules) **> 10 is a finding** — warn at the hook floor, **fail
  under `--strict` (G2+)**, the views-checker idiom. Opt-out via the one-word
  `off` in **`docs/components-check`** (the `trajectory-check`/
  `interfaces-check` idiom); a repo with ≤10 modules and no CMP rows passes
  trivially (the bound, not the registry, is the rule). Never-breaking for
  small repos; a 20-module repo is *supposed* to feel this — that is the
  directive's point.
- **Meta dogfood:** the kit's 21 modules currently have zero CMP rows → the
  meta repo fails its own new rule until it authors
  `docs/requirements/components.csv` (a handful of right-sized components —
  e.g. the traceability core, the generators, the doc/quality checkers, the
  unattended loop, the scaffold/onboarding surface) and the `Component` tags
  on its LLR rows. Author them; regenerate; the top view drops to the
  component level.

**Spine (working default — flagged for veto):** one new **SR-048** under
SN-023 (the single-dashboard SN): *the architecture view stays legible — the
top view is bounded and composition is declared* (render + the right-sizing
check), with its LLR/TC. SR-038 text gains only the minimal containerized-
top-view clause if coherence demands. Rides the pending re-attestation.

---

## WI mapping

- **WI-071** — FB1 + FB2 (docs: the campaign cadence + campaign language in
  the root README).
- **WI-072** — FB3 + FB4 (the owner scratchpad + check_docs scan-scope).
- **WI-073** — FB5 (How-SW containment + right-sizing rule + the meta CMP
  dogfood).

Per FB1's own ruling, WI sessions in this batch end at the **commit bar**;
the coordinating close runs the full gate once.
