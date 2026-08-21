"""The station's TERMINAL-OUTCOME vocabulary — the lane-close read model.

`SR-144`: every lane close is a terminal state with an immutable record. A lane
declares its outcome by the DIRECTORY it moved its claimed specs into —
`complete/` asserts the work is done, `cancelled/` asserts it never will be,
`partial/` asserts it stopped early. There is no fourth answer and no state file
that could hold one, which is what makes "every lane ends in a merge, branches
never hang" a property of the tree rather than a rule someone has to remember.

EVERY OUTCOME IS TERMINAL. Before `SR-144` a close into any OPEN folder
(`queued`/`draft`/`deferred`) read as a handback, so the returned row went
straight back on the frontier and needed a `blockref` to stop the driver
claiming, closing and re-claiming it forever. Those three are absent from
`OUTCOME_DIRS` on purpose: a lane that closes into an open folder names NO
outcome, and the merge refuses "exactly ONE declared state directory" — the
correct fail-closed posture, because under this contract stopping early is a
state with a name and a report, not a return to the queue.

WHY THIS IS A MODULE AND NOT A CONSTANT IN THE MERGE COORDINATOR (WI-483).
Until this module the table lived in `integrate.py`, and every reader of the
vocabulary imported the 2,500-line merge coordinator to reach it. The dashboard
was one of those readers: `traj_panels` — a render leaf that writes nothing and
must not be able to — imported the module that claims lanes, merges branches and
moves specs, for two constants. That import was an edge of the seven-module
cycle the 2026-08-19 repository review recorded (H-02), and the direction it ran
is the one a layered system forbids outright: a VIEW reaching into a MUTATION
service. The vocabulary itself depends on nothing, so it belongs below both.

The POLICY lives here too, not just the table. `outcome_of` answers "which
single terminal outcome do these status directories name?" — including the two
ways the answer is *none*: a spec that landed in no declared folder names none of
the three, and a spec left in TWO declared folders names two. Resolving the
second silently is worse than either (a dict keyed on basename once let the last
`ls-tree` line win, which is plain alphabetical precedence and put `queued` ahead
of `complete`). Reading the git tree stays with the coordinator, where the effect
belongs; deciding what the tree MEANS is a pure function over a set of strings,
and it is testable without a repository.

Stdlib only, and import-clean of the rest of `scripts/`, like every `kitlib`
module.
"""

from __future__ import annotations

import enum
from types import MappingProxyType

__all__ = [
    "Outcome",
    "OUTCOME_DIRS",
    "BAR_GREEN",
    "outcome_of",
]


class Outcome(enum.StrEnum):
    """The three terminal states a lane can close into.

    A `str` subclass on purpose: the outcome is written into handback records,
    merge audit lines and the dashboard, and every existing reader compares it
    against a literal. Being an enum adds the closed set and the name; being a
    `str` means no caller had to change to gain it.
    """

    MERGED = "merged"
    CANCELLED = "cancelled"
    PARTIAL = "partial"


#: The declaring `docs/work/` status directory -> the outcome it asserts. Read
#: off the branch's own tree, so the outcome is derived from the same move that
#: made the branch FINISHED — one fact, read twice, never two facts to keep in
#: agreement. Immutable: a mutation here would be a bug in every consumer at
#: once, and there has never been a caller that wanted one.
OUTCOME_DIRS = MappingProxyType(
    {
        "complete": Outcome.MERGED,
        "cancelled": Outcome.CANCELLED,
        "partial": Outcome.PARTIAL,
    }
)

#: The bar's attestation, carried as a git trailer in the refresh commit, NAMING
#: the tree and the work commit it attests so both can be checked against git.
#: (`integrate.refresh_attestation` is why the names are the whole point: a
#: message alone rides through amend, rebase and cherry-pick onto trees nobody
#: barred.) It lives here because the station render draws the label and must
#: not import the coordinator to learn it.
BAR_GREEN = "Bar-Green:"


def outcome_of(status_dirs):
    """The ONE `Outcome` the given status directories name, or `None`.

    `None` covers both failures on purpose, because the caller refuses on
    either: a set naming no declared directory, and a set naming two. Unknown
    directory names are ignored rather than raising — the caller passes whatever
    the tree held, and an undeclared folder simply asserts nothing.
    """
    seen = {OUTCOME_DIRS[d] for d in status_dirs if d in OUTCOME_DIRS}
    return next(iter(seen)) if len(seen) == 1 else None
