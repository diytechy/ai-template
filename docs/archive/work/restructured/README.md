# `restructured/` — terminal work-item history (rows absorbed by a successor)

The FOURTH terminal state (the 2026-09-02 backlog-restructure plan §1.6),
living beside its three siblings under the archive for the reason WI-504
established (OI-55 ruled (a)): the active workspace lists only rows in flight.
Status is still the DIRECTORY — a spec in this folder reads as `restructured`.

A row lands here when a **consolidation** absorbs it into a successor: several
queued rows whose scopes overlap are replaced by one row that carries all of
them. The absorbed row's scope text stays **byte-identical** (a scope
definition never changes to mean something else) and its `## Deliverable` is
exactly one line, `Restructured into WI-<successor>.` — the successor is the
whole record, because the successor's Context quotes the absorbed Done-when
blocks under their old ids.

It is not `cancelled`: nothing here was refuted, and reading it as refutation
would be actively wrong — `intake.context_block` briefs every later row on the
same SRs with the cancelled precedent "do not re-propose the refuted", so an
absorbed row filed as cancelled would tell its own successor not to build it.
It is not `partial` either: no lane stopped early, so there is no per-close
report and no disposition to mint.

TERMINAL means terminal — nothing re-claims a row here, no lane may close into
it (`kitlib.station.CLAIMED_OUTCOMES` and `integrate.Outcome` deliberately do
not name it; only the consolidation close and a hand trunk commit file a row
here), and its inbound hard edges are RE-POINTED to the successor at the close.
An edge still naming a row in this folder is a missed re-point, and both the
scheduler (`waiting:hard-pred-restructured:`) and the validator
(`check_trajectory.dead_dependency_findings`) report it rather than letting the
successor strand. `kitlib.registry.read_spec_rows` reads `docs/work/` and
`docs/archive/work/` as one registry, so every row here keeps its full standing
as a trace link and a dashboard count.
