"""`kitlib.station` — the lane-close terminal-outcome read model (TC-177).

The half of `SR-144` that is a DECISION rather than an effect. `integrate`
reads the branch tree; what the read MEANS is this module, and the point of
extracting it is that the meaning is now assertable without building a git
repository, a branch and a claim first.
"""

from kitlib import station


def test_outcome_of_names_one_outcome_or_none():
    """One declared directory names its outcome; both failure shapes answer
    None, because the caller refuses on either.

    The two-directory case is the one with history: a spec left in TWO declared
    folders names two outcomes, and a dict keyed on the basename once let the
    last `ls-tree` line win — plain alphabetical precedence, which put a
    handback ahead of a merge. `None` is the fail-closed answer, not a pick.
    """
    for status_dir, outcome in station.OUTCOME_DIRS.items():
        assert station.outcome_of({status_dir}) == outcome
        # a repeat of the same directory is still ONE outcome
        assert station.outcome_of([status_dir, status_dir]) == outcome

    assert station.outcome_of(set()) is None
    assert station.outcome_of({"queued"}) is None, (
        "an OPEN folder declares no terminal outcome — that is the whole of "
        "SR-144's amendment and it must not resolve to one"
    )
    assert station.outcome_of({"complete", "queued"}) == station.Outcome.MERGED, (
        "an undeclared directory asserts nothing and must not spoil a declared one"
    )
    assert station.outcome_of({"complete", "partial"}) is None
    assert station.outcome_of({"complete", "cancelled", "partial"}) is None


def test_the_outcomes_are_strings_so_no_caller_had_to_move():
    """`Outcome` subclasses `str` on purpose.

    The outcome is written into handback records, merge audit lines and the
    dashboard, and every reader in and outside this repo compares it against a
    literal. Being an enum adds the closed set; being a `str` is what let the
    vocabulary move modules without a single caller changing.
    """
    assert station.Outcome.MERGED == "merged"
    assert "{}".format(station.Outcome.PARTIAL) == "partial"
    assert sorted(set(station.OUTCOME_DIRS.values())) == [
        "cancelled",
        "merged",
        "partial",
    ]


def test_the_table_is_immutable_and_holds_only_terminal_states():
    """No OPEN folder may appear, and no caller may add one at runtime.

    Before `SR-144` a close into `queued`/`draft`/`deferred` read as a handback
    and put the row straight back on the frontier. Their absence is the
    contract, so pin the absence rather than only the presence.
    """
    assert set(station.OUTCOME_DIRS) == {"complete", "cancelled", "partial"}
    try:
        station.OUTCOME_DIRS["queued"] = station.Outcome.MERGED
    except TypeError:
        pass
    else:  # pragma: no cover - only reached if the table stops being a proxy
        raise AssertionError("OUTCOME_DIRS must not be mutable")


def test_the_merge_coordinator_still_exports_the_former_names():
    """The re-export is a shipped compatibility promise, so it is pinned.

    An adopter's own tooling may read `integrate.OUTCOME_DIRS`; the re-sync
    entry tells them it still resolves, and this is what makes that true.
    """
    import integrate

    assert integrate.OUTCOME_DIRS is station.OUTCOME_DIRS
    assert integrate.BAR_GREEN == station.BAR_GREEN
