## 2026-08-18 — Review-round residue: the claims that did not survive re-measurement

Two adversarial reviews over the 2026-08-18 commit run (`3b8d306d` okf-off →
`4e9a5c8a` the provenance ruling) filed eight findings against this lane's
files. Every one was re-verified from the artifacts before it was fixed; the
verdicts and evidence are below, including where a finding overstated itself.
Nothing here changes a requirement, a gate or a dial — it corrects records and
repairs two pieces of tooling the same commit run broke.

### M6 — a log fragment claimed a green it did not produce · **UPHELD, fixed**

`docs/log.d/2026-08-18-okf-off.md` said the pre-commit batch was green end to
end *and* that the regenerated dashboard carried four tabs at 1.92 MB with
`gen_trajectory.py --check` clean. Measured:

- `git show 3b8d306d --name-only` names no `PROJECT_STATE.html`. The blob at
  `3b8d306d` and at `3b8d306d~1` is the same object — `5f63248d`, 2,635,523
  bytes, five `data-tab` panels including `know`. The four-tab, 1,916,019-byte
  dashboard is blob `214fe97c`, which first appears one commit later in
  `712ff788`.
- Against `git archive 3b8d306d`, the hook's own 12-step floor batch
  (`check.py --run-steps arch-map,okf,trajectory-map,…`) is **11 PASS / 1 FAIL,
  exit 1**: `trajectory-map` prints `project-state dashboard STALE in
  PROJECT_STATE.html`.

The green was real against the author's *working tree*; the regenerated file was
simply never staged. The fragment now states only what the commit's tree
supports and carries a struck-through CORRECTION block with this evidence,
rather than a quiet deletion.

### N14 — the "60-day evidence" behind the byte caps · **UPHELD, re-derived**

`docs/knowledge/instruction-file-adherence.md` cited a common 60-day window with
"hard-capped file −14%; watched files +263% to +1,092%". Sixty days before
2026-08-18 is 2026-06-19, and two of the three files did not exist yet
(`AGENTS.template.md` created 2026-06-28 at `53eac479`; `PROCESS_OPTIONS.md`
2026-07-01 at `cdb64dc2`), so there was no common window at all. Route-by-route,
`PROCESS.md` measures +281% from the nearest commit to the 60-day mark
(`6d98b212`, 21,572 bytes), +1,388% from creation (5,522) and +91% from the
`PROCESS_OPTIONS.md` split (42,932) — **+263% matches none of them**. The −14%
is a creation-to-now figure whose whole content is the one-off trim that
*introduced* the cap.

Re-derived over one window in which all three exist at both ends —
**2026-07-01 `cdb64dc2` → 2026-08-18 `4e9a5c8a`, 48 days**, `git cat-file -s`
per blob:

| File | Regime | Start | End | Δ |
|---|---|---|---|---|
| `project-trajectory/AGENTS.template.md` | capped 10,000 | 9,702 | 9,953 | **+2.6%** |
| `project-trajectory/PROCESS.md` | watched | 42,932 | 82,190 | **+91%** |
| `project-trajectory/PROCESS_OPTIONS.md` | watched | 14,434 | 173,374 | **+1,101%** |

`cdb64dc2` is the honest anchor twice over: it is the commit that created
`PROCESS_OPTIONS.md`, and it is downstream of `6ade9daa` (2026-07-01), where the
AGENTS cap first became test-enforced — so at both ends all three files exist
and the capped one is actually under a cap. The claim the caps rest on survives
in a stronger form (a capped file held to +2.6% while its unwatched neighbours
ran to +91% and +1,101%); only the unreproducible numbers are withdrawn, and the
pack says so in place. It remains one repo and one author: consistent-with, not
proof-of.

### N4 — a deferred provenance exception on SN-027 · **PARTLY UPHELD**

`docs/requirements/stakeholder-needs.toml` SN-027's `acceptance` still ends
`Spec of record: docs/archive/specs/parallel-wi-dispatch.2026-07-20.md +
docs/concurrency-restructure.md`, and it is **not** in `docs/provenance-allow`
while `4e9a5c8a`'s message says the SN tier was taken to zero. But "recorded
nowhere" overstates it: `docs/log.d/2026-08-18-provenance-rule.md` §4 tables the
deferral explicitly, names the `docs/cmp/` ruling it is blocked on, and says in
its own words that "the detector does not flag a path, so they are invisible to
the worklist and this entry is their only record."

So the gap is narrower than filed and still real: the *live* exception surface
does not carry it, and the log is history rather than a working surface. The row
itself is honest — both cited paths exist on disk — and the pointer is left
standing exactly as the ruling left it; dropping it would lose the design
pointer, which is the reason it was deferred. The allow-file line another lane
must add is in "Handoffs" below. Adding it is safe by construction:
`trace.py.load_provenance_allow` is a plain key set with no unmatched-entry
check, so an entry for a row the detector never flags declares without
suppressing anything.

### N5 — two SN rewrites deleted the reasoning with the citation · **UPHELD, restored**

`git show 3dd665fc` is the wrong commit for this; the edits are in `4e9a5c8a`.
There, SN-034 lost "the reframe makes this a multi-requirement need, so the
demotion test no longer applies" and SN-035 lost "kept at need tier — the row's
subject is the self-application boundary, a stakeholder-level scope decision no
requirement cell can carry", each deleted whole with its `(Ruled 2026-08-13,
OI-17 …)` frame. That is the failure the same commit's own rule names: *drop the
frame, KEEP the reason.* Five sibling rows in that diff (SN-005, SN-006, SN-008,
SN-011, SN-027) were handled correctly, which is what makes these two the
exception rather than the reading.

Both reasons are load-bearing — they are the answer to "why is this a need and
not a requirement", the first question a re-tier review asks of a launcher row —
so both are restored as standing prose in their original cells: no ruling, no
date, no open-item id. `trace.py` after: `orphans=0 integrity=0`, no advisory on
either row, and the citation-frame advisory count is unmoved.

### N8 — `docs/orphans-allow` lost `docs/specs/WI-*.md` · **UPHELD, restored**

`git show 712ff788 -- docs/orphans-allow` removes the glob in the same hunk that
adds `docs/work/*`; the commit message describes the sweep as "docs/orphans-allow
refreshed (454 warnings -> 1)" and never mentions the deletion. `docs/specs/` is
live — `check_trajectory.SPECS_DIR`, the name-resolved home of an open WI's
spec-of-record — and today holds `README.md` plus `WI-000.md`, which is
reachable only because the folder README hand-links it.

Measured on `git archive HEAD` with a synthetic `docs/specs/WI-999.md` dropped
in: **before** the restore, 603 expected-matched and `WARN - orphan doc (no path
from an entry root): docs/specs/WI-999.md`; **after**, 604 expected-matched and
`0 orphan warning(s)`. So the deletion had no effect today and would have
produced a fresh warning on the next spec filed. The glob is back with a reason
that does not repeat the old one's mistake: the old text pointed at
`docs/requirements/work-items.csv`, which is genuinely retired — the citation was
the stale part, not the declaration.

Live-tree counts moved 604 → 605 expected across the same edit, but that +1 is a
concurrent lane's new `docs/log.d/` fragment, not this change; the genuine
orphan warning (`docs/test/report.md`) is unchanged at 1 throughout.

### N10 — the render-critique tooling could not run here · **UPHELD, fixed**

`scripts/dashboard-shots/shoot.mjs` clicked `nav.tabs button[data-tab="know"]`
unconditionally. With the OKF dial off that button does not exist — the rendered
dashboard carries exactly `arch`, `dag`, `sw`, `process` — so `page.click` waits
out Playwright's 30s default and the run exits 1 partway through the first
theme/width cell. The declared matrix is now a **superset**: `resolveTabs()`
reads the page's actual `data-tab` buttons once, intersects, and reports in both
directions — a declared tab that is absent is `SKIPPED` by name, and a rendered
tab missing from `TABS` is reported as `NOT shot`, which is the case that would
otherwise let a new tab go uncritiqued forever. An empty intersection still
exits 1, loudly.

Playwright is **not installed in this checkout** (`node_modules/` absent), so the
browser path was not executed. Verified instead by `node --check` plus a
simulation that feeds `resolveTabs`' body the `data-tab` list parsed out of the
real `PROJECT_STATE.html`: it prints `declared tab(s) not in this dashboard,
SKIPPED: know (Knowledge (OKF))` and `shooting 4 tab(s): arch, dag, sw,
process`. The README's "all five" and 36-shot matrix are corrected to the
general form (3 × 2 × *T* full + 6 folds) with today's value stated: **T = 4, 30
shots**. The `render-dashboard-critique` skill carries neither number, so no
skill copy needs aligning.

### N11 — the okf reversal recipe · **UPHELD, rewritten**

"Reversible in one key" was executed literally on a `git archive HEAD` copy:
flip `okf_export`, run `gen_okf.py` (which wrote 553 files, not the 551
deleted), delete the `docs/declared-absences` row. Result over the three
affected modules: **3 failed, 100 passed**, and over the full suite **4 failed,
2565 passed, 19 skipped** — the fourth,
`test_check_lane.py::test_the_primary_checkout_is_not_a_work_branch`, fails
identically on an *unmodified* archive copy (no `.git`), so it is a scratch-copy
artifact and not a cost of the reversal. The three real failures are one-way
ratchets written against the dial's current value:
`test_rule_sync`'s `OWNER_DIALS` map, and the `assert gt.know_graph(ROOT) is
None` opener in both `test_traj_panels::test_meta_spine_renders_the_knowledge_graph_at_real_scale`
and `test_traj_graph::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes`.
The recipe in the okf-off fragment is now a seven-step worklist naming each,
plus the two steps nobody had written down: regenerate `PROJECT_STATE.html`
(stale the moment the bundle exists) and put the `README.md` dial row back.

### N13 — the PowerShell port still defaulted to the retired doc · **UPHELD, fixed**

`gen_arch_map.reference.ps1` defaulted `$Doc` to `docs/architecture.md` +
`AGENTS.md` and then threw `Target doc not found` at the write loop. The Python
side was swept at WI-455 — `--doc` is now REQUIRED with an explanatory
`SystemExit` — and the port was not, so a PowerShell adopter following
ADOPTING.md §3 met a failure naming a path they never typed. `-Doc` is now
required with the same message and reason, and the comment-based help says so.

**Not executed: `pwsh` is not installed on this machine** (`which pwsh` →
nothing), so the change is deliberately minimal and syntactically local — a
`throw` replacing a default assignment, plus help text. No path-normalization or
other behaviour was folded in. No test in `tests/` reads this file.

### Handoffs — exact text for the lanes that own these files

**`docs/provenance-allow`** — append under the first block (not this lane):

```
SN-027 acceptance — the BLOCKED design pointer: the "Spec of record" paths are held by the docs/cmp/ ruling, and with docs/cmp/ unmaterialized they can only be dropped, which loses the pointer. The detector does not flag a path, so this entry is the live record that the frame is deliberate rather than missed. Owes an open-item row at the sitting.
```

**`project-trajectory/skills/byte-budget-guard/SKILL.md`** (and its `.claude/` +
`.agents/` mirrors) — replace the "60-day evidence" sentence with:

> The doc-size evidence (2026-08-18, re-derived over one 48-day window with all
> three files present; the derivation and the withdrawn earlier figures are in
> `docs/knowledge/instruction-file-adherence.md`) is that **hard caps hold and
> watch-only does not**: capped `AGENTS.template.md` +2.6% and still under cap;
> watched `PROCESS.md` +91% and `PROCESS_OPTIONS.md` +1,101%. Check before you
> edit and again before you commit.

That is **+156 bytes** on the source copy, which is 4,636 at the time of writing
(another lane holds it open) — 4,792 against the 5,000 cap. The derivation lives
once, in the knowledge pack; the skill points at it rather than restating it.

**`project-trajectory/ADOPTING.md` §3** — the PowerShell retrofit step says to
edit `$ModuleGlob` / `$EntryScripts` / `-Flow` and "drive it with `-Check`". With
`-Doc` now required it must also name `-Doc`.

**`PROJECT_STATE.html`** — this lane's SN-034/SN-035 edits stale the dashboard
(`gen_trajectory.py --check` exits 1; verified against a clean `git archive HEAD`
that the same tree plus only this file is what flips it). Regenerating it is
outside this lane; whoever composes the trunk must run
`python project-trajectory/scripts/gen_trajectory.py` before the commit lands.
