+++
id = "WI-485"
title = "Every announced deferral resolves to an open item: the allow-file OI-### grammar, the session-log deferral declaration, the re-aimed vacuity check, and the open-items layer always-on (OI-41 ruled (e), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-41"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

OI-41 ruled (e) executed in full. ARM 1: `docs/provenance-allow`'s entry
grammar gains a required `OI-###` as the first token of the reason — a
position, not a mention — parsed by the single `trace.parse_provenance_allow`
that `load_provenance_allow` now views, checked as an INTEGRITY error on
the always-on `--strict-integrity` floor (present + resolves; the row's
STATE deliberately belongs to ARM 3, not a second copy — every live row is
`ruled` today and ruled-but-unexecuted is a legitimate transient), with all
17 live entries migrated in one pass (16 → OI-34, 1 → OI-37; the ruling's
19 had lost two to their rulings). ARM 2: a `docs/log.d/` fragment declares
its deferred OI ids under `Deferred open items:` — ids or an explicit
none — checked at the commit bar warn-only, the declared weakness pinned by
a test; the live 2026-08-20 rulings fragment parses as a none-declaration
from its own prose. ARM 3: the vacuity check re-aimed — zero pending rows
while the exception surface still defers is a contradiction NAMING the
entries — and it fired truthfully on its first day: 16 OI-34 entries + 1
OI-37 entry whose ruled executions never landed, now queued as WI-489.
ALWAYS-ON: the layer moved into PROCESS.md §5 (+987 bytes, flagged and
re-stamped; the options doc keeps the depth), S-3 is non-vacuous (an
ABSENT registry is the finding), every profile scaffolds the registry +
html — verified by bootstrapping real scaffolds and pinned in the profile
permutation matrix. RESYNC entries for both downstream-visible changes;
the enforcement audit carries the three arms with the ruling's caveat:
always-on is the substrate, never the mechanism. Full suite 2635/13 green.

## Context

Executes OI-41's ruling — (e), three arms that are each a FIELD or a COUNT,
plus the folded-in always-on direction. The row's options/recommendation
cells carry the full design; the build obligations:

- **ARM 1 (hard immediately):** `docs/provenance-allow`'s entry grammar gains
  a required `OI-###`; an entry naming a nonexistent or non-pending row is a
  finding; the 19 entries that promise a row in prose migrate in one pass.
  The file's grammar is already parsed and tested — extend, don't rebuild.
- **ARM 2 (the declared-weak arm — keep it labelled):** a session's
  `docs/log.d/` fragment declares the `OI` ids it deferred, checked at the
  commit bar; a session that defers silently passes clean, and the ruling
  accepts that on record.
- **ARM 3:** the vacuity check re-aimed — a pending count of zero while ARM 1
  entries or ARM 2 declarations exist is a contradiction, and the finding
  NAMES the entry. Counts, not phrases; no phrase-vocabulary arm ships.
- **ALWAYS-ON:** the open-items layer moves from `PROCESS_OPTIONS.md` into
  always-shipped process (every scaffold gets `open-items.toml` +
  `open-items.html`), making `check_docs` S-3 non-vacuous — with the ruling's
  own caveat standing: ALWAYS-ON IS NOT POPULATED, the substrate never the
  mechanism.

Costs the ruling priced, owed at execution: `PROCESS.md` is byte-budgeted, so
the always-on clause lands net-zero or displaces something
(byte-budget-guard before/after); the grammar change and the layer move are
downstream-visible — RESYNC entries owed; new checks arrive warn-first except
ARM 1, which is a field with no false positives and may be hard at birth.
