+++
id = "WI-452"
title = "Resurface LLR-165's carrier converter as the downstream-resync helper it now is (owner-ruled 2026-08-13, sitting decision 2.3): the 2.3 status lift treats SR-147/LLR-165/TC-160 as shipped one-shot migration machinery, but the owner's ruling adds a forward obligation — a downstream repo re-syncing onto this kit AFTER the carrier cutover still holds its registries on the old markdown/CSV carrier, and migrate_carrier.py's convert()/compare() (LLR-165) is exactly the proven, loss-refusing path for that conversion. Scope: (1) verify the resync surfaces (RESYNC_PACK.md's carrier entry, ADOPTING.md §6, the downstream-resync skill) actually NAME migrate_carrier.py as the adopter's conversion step with its refuse-on-loss contract, and wire the pointer where missing; (2) confirm the converter still runs against a pre-cutover scaffold (the throwaway-clone detector lesson: run it, don't read it) and that TC-159/TC-160 still exercise the path; (3) there is NO requirement that resync be mechanized end to end — helper functions are welcome, a one-command wrapper is optional and only if it stays stdlib and earns its place; do not build orchestration nobody asked for. LLR-165 stays a live row serving the resync effort, not spent history."
workstream = "docs"
sr_refs = ["SR-147"]
needs = ["~WI-455"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Verified the three named resync surfaces already name `migrate_carrier.py`
with its refuse-on-loss contract (RESYNC_PACK.md fully; ADOPTING.md §6 and
the downstream-resync skill correctly DEFER to the pack under the standing
OI-27 one-home rule — adding the name there would reintroduce the drift
that rule closed), so no wiring was missing and none was added. Ran the
converter LIVE against a scaffold rebuilt from the kit's actual
pre-cutover revision: round-trip clean, exit 0. TC-159's evidence checks
out; TC-160's Evidence cell named a test deleted 2026-08-15 and was
repaired to the four tests that now cover its Method clause verbatim
(Evidence is a traced pointer cell — no amendment; snapshot mirrored). No
orchestration built — the pack's tested copy-paste recipe is already the
one-command surface. Surface list scoped to what is live at this session's
start per the soft ~WI-455 edge (external.toml never had a CSV carrier).
Adjacent finding banked: IF-103 and the kit README still frame the
converter as one-shot/terminable, against the ruling this row executes.
174 targeted tests + smoke green; integrity 0.

**Provenance label (added 2026-08-20, closing review ROUND-OPUS MAJOR-9):**
"Ran the converter LIVE … round-trip clean, exit 0" is a WORKER SELF-REPORT.
Its provenance is that worker's session transcript; this repo retains no
artifact of the run — no scaffold, no log, no `fig:` marker — so it cannot
be re-read, only re-driven. Labelled rather than marked, deliberately:
attaching a provenance marker after the fact would manufacture evidence for
a run the closer did not witness. The claim is plausible and untested here;
TC-159 remains the standing mechanized cover for the same path.

## Context

**The TC-159 chain gap is CLOSED — this guard is spent (updated 2026-08-14f).**
Part (2) says *"confirm … that TC-159/TC-160 still exercise the path."* The
guard that used to stand here said *"confirm, do not lift"* because lifting was
a spine window owed to sitting 3 §2.2. **That window ran:** the owner ruled
(log `2026-08-14f`) that §2.3's lift had CROSSED the subject pairs — TC-159
drives the converter and verifies LLR-165, TC-160 drives the reader and
verifies LLR-166 — and both halves were aligned in the same act: TC-159 and
LLR-166 lifted `Draft` → `Planned`. **Re-measured `2026-08-18b`: all four
carrier rows (LLR-165/166, TC-159/160) are `Approved`** — the sentence here
read `Planned`, a word the D-9 rename retired by folding it into `Approved`
(log `2026-08-15m`), so this row was teaching a vocabulary the registry no
longer admits. The maturity is unchanged; only its spelling is. So part (2)
is a straight confirmation — **run the converter and check the two TCs still exercise the
path; there is no chain gap left to record, and this row still flips no
Status.**

**The surface list is fed by two other programs — run last or scope to today.**
Part (1)'s surface list grows if/when `external.toml` lands (a new registry
earns a resync entry) and again when `docs/architecture.md` retires (D8 — a
scaffold-surface change is a declared re-sync entry). Either sequence this row
**after** both, or state explicitly that it covers only the surfaces live at
its start and that those two programs each carry their own resync entry.
(The old IF-103 tension is DISSOLVED — 13u retires `Stability`, so the
converter's maturity is not the frame's business. No action here.)

(2026-08-19, repo-review triage: the paragraph above's "run last" choice is now
encoded as the `~WI-455` soft edge — `external.toml` landed, so the wi455 lane
is the one remaining feeder. The alternative — scope to surfaces live at start
— remains the claiming session's call; the edge is soft for exactly that
reason.)

