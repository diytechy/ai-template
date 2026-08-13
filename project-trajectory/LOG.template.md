# Project Log — Append-only history

The durable record for the gated process (see [process.md](process.md) §5):
sitting sign-offs, review verdicts, ratified decisions, and session notes append
here, **newest last**, and are never rewritten. The working surface — what to
do *next* — lives in [status.md](status.md), which points here; this file is
**evidence, never normative**: a rule or requirement belongs in the process
doc or a registry, not in a log entry. Entries here and in status.md cite
**stable ids** (OI-n, stage/bar names, dates), never iteration-branch commit
SHAs — sync scrub/collation may rewrite those (process-options.md "Agent
iteration branch & sync").

**Entries already written are never re-worded, including their vocabulary.** A
sign-off that recorded a named human certifying `G1` recorded exactly that; a  <!-- check_vocab: allow -->
later vocabulary change (the stage ladder retired the `G*` tags) does not reach
backwards, because rewriting an attestation makes the record claim something was
signed that was not. Read historical rows through the translation in
process.md §4.

---

## Sittings

**A sitting is an occasion, not a rung.** The stage ladder has eight rungs
(`DevStg-Needs` … `DevStg-Release`, process.md §4) and a project holds far fewer
sittings than that — so sittings stay their **own axis** and each row names the
**rung range it certifies**. Add a row when you actually sit; do not pre-create
one per rung. Add columns for any active domain hats, and drop a row your
deliverable does not need.

Keep the role columns and the `Human` column distinct: the roles record which
hat signed, `Human` records that a **person** looked. Collapsing them loses the
ability to answer "which sittings did a human actually attend?".

| Sitting | Rungs certified | Stakeholder | UX/Docs | System Eng | Test Eng | Human |
|---|---|---|---|---|---|---|
| Requirements/UX/Constraints | `DevStg-Needs` → `DevStg-Reqs` | PENDING | PENDING | PENDING | n/a | PENDING |
| Decomposition & Test Coverage | `DevStg-Arch` → `DevStg-Tests` | n/a | n/a | PENDING | PENDING | PENDING |
| Implementation | `DevStg-Impl` | n/a | n/a | PENDING | PENDING | PENDING |
| Release readiness | `DevStg-Release` | n/a | n/a | n/a | PENDING | PENDING |
| Acceptance | `DevStg-Release` (the owner's final read) | PENDING | n/a | n/a | (evidence) | PENDING |

## Decisions log

_Ratified or executed decisions only — the call, the alternatives passed over,
why (one bullet each; cite ids). A decision still **awaiting** a human is an
Open item in [status.md](status.md), not a log entry._

## Audit log

<!-- Append verdict blocks here per process.md §5. Newest at the bottom. -->

### DRIVER — DevBar-Reqs — Round 1 — <YYYY-MM-DD>
Scaffolding created. Starting DevBar-Reqs.
