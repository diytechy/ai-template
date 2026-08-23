+++
id = "WI-505"
title = "Staleness headers on generated and archive artifacts - option (a) only, no forward pointers, no enforcement check (OI-56 ruled, 2026-08-22)"
specref = ""
workstream = "docs"
sr_refs = []
needs = ["WI-504"]
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed OI-56 as RULED — (a) only, with the owner's two narrowings honoured
(no live-surface pointer in an archive header; no enforcement check). Full
per-path/per-file record: `docs/log.d/2026-08-23-wi505-staleness-headers.md`.

**Generated headers**, stamped BY THE GENERATORS, over the staged-divergence
step's 9 declared paths (`docs/stack.ini` `[generated]`): `docs/stage`
(`derive_stage.py`), the `docs/status.md` block (`gen_trajectory.py --status`
/ `traj_status.py`), `docs/open-items.html` (`gen_open_items.py`),
`PROJECT_STATE.html` (`gen_trajectory.py`, the fuller REPORT form),
`docs/ratify/` (`trace.py --approve`), `project-trajectory/skills/INDEX.csv`
(`gen_skills_index.py`), `project-trajectory/prompts/CATALOG.md`
(`gen_prompt_catalog.py`), and `docs/okf/` (`gen_okf.py`, currently opted
out in this repo — its banner was already compliant and is armed for when it
is turned on). Most already carried a compliant or near-compliant header from
earlier work and were normalized in wording only; `skills/INDEX.csv` was
genuinely unstamped and gained a new leading `#`-comment banner.
`tests/test_module_size_ratchet.py` (the linecounts baseline) is EXCLUDED
from the generator-stamp population — it is hand-maintained census data
re-stamped by reviewed edit, not a mechanical generator's output, so there is
no `<script>`/`regenerate:` command to name.

**Archive banner sweep**, one-time, over `docs/archive/**` (after WI-504's
relocation): 181 files gained the leading
`> **ARCHIVE** — design history as of <date>; not current guidance.` banner
(date = the file's own `git log -1 --format=%as`, else the sweep date).
Excluded, with reasons checked against the actual readers: the 503
registry-parsed specs under `docs/archive/work/**` (`kitlib.registry`
requires the `+++` fence as line 0 and the body to start with
`## Deliverable`), the 8 files under `docs/archive/last_approved/**` (the
byte-compared approval snapshot), one `.patch` file (a literal diff) and one
`.rtf` file (a binary-ish container). `docs/archive/README.md` gained the
one-line statement of the convention plus the same banner every other archive
file carries.

**Downstream.** Bootstrapped a real scaffold and confirmed the shipped
generators (`gen_trajectory.py`, `traj_status.py`, `trace.py`, `gen_okf.py`,
`derive_stage.py`) are byte-identical to this repo's edited sources, so every
adopter's next regeneration carries the same header wording; added a
`[since a8b40abd]` `RESYNC_PACK.md` entry recording the change and that the
archive sweep is one-time and not mechanized (nothing for a resync to pull).

Done-when: every declared-generated path carries its ruled header (stamped by
the generator, verified by regenerating and diffing); the archive sweep ran
once over `docs/archive/**` with documented exclusions; the archive README
states the convention; the smoke + smoke-budget + `check_docs --stale` +
`check_trajectory --strict` commit bar is green; the full suite is green.
