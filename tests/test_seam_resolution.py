"""The IF tier's two-cell shape and the derivations it rests on (WI-455).

`OI-60` ruled (a) on 2026-08-23 and ordered its two clauses: rename
`counterpart` into a consumers list FIRST, shed `direction` (and the derivable
provider cell) immediately behind it. The shed is only lossless while three
things hold, so they are asserted here over the LIVE registry rather than
argued in a log:

* **flow is recoverable** — every row resolves to a provider and a consumer
  set, so the producer -> consumer orientation the three seam readers need is
  read off the row instead of a retired flag;
* **the provider is recoverable** — absent from a row exactly when
  `owner` -> LLR -> `Module` derives it UNIQUELY, and stated otherwise;
* **the rows that cannot derive it still carry it** — the twelve
  requirement-owned provider-side seams the SR-owned-`Provides` report is
  about, whose `owner` is a requirement and therefore names no module.

The 21 rows that state NO provider are declared here by id, because "a row with
one known side" is a real shape (a published medium whose readers are the fact
the row records) and an UNDECLARED one would be indistinguishable from a cell
the transform dropped by accident.
"""

import tomllib

from conftest import ROOT, load_script

CARRIER = load_script("spine_carrier")

# `kitlib` is a package beside the scripts, so it imports directly once
# loading a script has put scripts/ on sys.path.
from kitlib import spine as KIT  # noqa: E402

LIVE_IFS = ROOT / "docs" / "requirements" / "interfaces.toml"
LIVE_LLRS = ROOT / "docs" / "requirements" / "low-level-requirements.toml"

# The report's twelve: `owner` is a requirement, which carries no `Module`, so
# `provider` is the ONLY record anywhere of which module serves the seam.
REQUIREMENT_OWNED_PROVIDERS = frozenset(
    {
        "IF-001",
        "IF-005",
        "IF-009",
        "IF-011",
        "IF-013",
        "IF-014",
        "IF-015",
        "IF-044",
        "IF-053",
        "IF-065",
        "IF-076",
        "IF-081",
    }
)

# The published-medium rows: what crosses is a file the `contract` names, and
# what the row RECORDS is the measured reader set — the 16 facing the adopter
# class plus the five `WI-469` reader-set rows. No endpoint cell ever claimed
# the medium, so none states a provider.
NO_PROVIDER = frozenset(
    {
        "IF-021",
        "IF-022",
        "IF-023",
        "IF-024",
        "IF-029",
        "IF-030",
        "IF-033",
        "IF-034",
        "IF-035",
        "IF-037",
        "IF-038",
        "IF-047",
        "IF-049",
        "IF-051",
        "IF-054",
        "IF-057",
        "IF-059",
        "IF-068",
        "IF-072",
        "IF-073",
        "IF-079",
    }
)


def _live_rows():
    return [
        r
        for r in CARRIER.load(LIVE_IFS, "IF-ID", keep_examples=False)
        if (r.get("IF-ID") or "").startswith("IF-")
    ]


def _live_modules():
    return CARRIER.llr_modules(ROOT)


def test_no_live_row_carries_a_retired_endpoint_cell():
    # The rename is COMPLETE or it is a second vocabulary: a row still carrying
    # `direction`/`this_project`/`counterpart` would read as empty to every
    # updated reader while looking authored to a human.
    raw = tomllib.loads(LIVE_IFS.read_text(encoding="utf-8"))["interface"]
    retired = {
        rid: sorted(set(cells) & {"direction", "this_project", "counterpart"})
        for rid, cells in raw.items()
        if set(cells) & {"direction", "this_project", "counterpart"}
    }
    assert retired == {}
    # And every row carries the cell that replaced them, as a LIST.
    assert [rid for rid, cells in raw.items() if not cells.get("consumers")] == []
    assert [
        rid for rid, cells in raw.items() if not isinstance(cells["consumers"], list)
    ] == []


def test_flow_is_recoverable_on_every_row():
    # What the three orienting readers (`check_trajectory.interface_findings`,
    # `traj_views`' two seam graphs, `gen_arch_map`'s dotted edges) need is the
    # producer -> consumer pair, not the retired flag. Every row answers it.
    modules = _live_modules()
    for row in _live_rows():
        rid = row["IF-ID"]
        consumers = KIT.seam_consumers(row)
        assert consumers, rid
        provider = KIT.seam_provider(row, modules)
        assert bool(provider) is (rid not in NO_PROVIDER), rid
        # An endpoint is never on both sides of its own seam: that reads as a
        # module talking to itself, which is no seam at all.
        if provider:
            assert KIT.norm_module(provider) not in {
                KIT.norm_module(c) for c in consumers
            }, rid


def test_the_provider_cell_is_present_exactly_where_it_is_underivable():
    # The shed's rule, stated executably: the cell dies where `owner` -> LLR ->
    # `Module` derives it UNIQUELY, and survives everywhere else. A multi-module
    # owner derives a SET, which is not the fact, so those rows keep it.
    modules = _live_modules()
    for row in _live_rows():
        rid = row["IF-ID"]
        owners = KIT.refs(row.get("Owner"))
        derivable = (
            len(owners) == 1
            and owners[0].startswith("LLR-")
            and len(KIT.seam_endpoints(modules.get(owners[0], ""))) == 1
        )
        stated = bool((row.get("Provider") or "").strip())
        if derivable:
            assert not stated, rid  # a derivable cell is a second spelling
        else:
            assert stated or rid in NO_PROVIDER, rid


def test_the_report_s_twelve_still_carry_their_provider_fact():
    # `OI-60` (a) keeps the provider-side endpoint on these rows until their
    # owners are re-pointed at the design tier. Losing the cell here deletes the
    # providing module outright — with it the module's producer credit in the
    # connectivity advisory and the source end of its declared seam pair.
    rows = {r["IF-ID"]: r for r in _live_rows()}
    for rid in sorted(REQUIREMENT_OWNED_PROVIDERS):
        row = rows[rid]
        assert KIT.refs(row["Owner"])[0].startswith("SR-"), rid
        assert (row.get("Provider") or "").strip(), rid


def test_seam_provider_prefers_the_stated_cell_over_the_derivation():
    # Precedence, pinned: a row that states a provider is answered from its own
    # cell. The derivation is the FALLBACK, so a re-pointed owner can never
    # silently overrule an endpoint an author wrote down — `if_provider_advisories`
    # reports that disagreement instead of resolving it.
    modules = {"LLR-001": "project-trajectory/scripts/a.py"}
    row = {"IF-ID": "IF-001", "Owner": "LLR-001", "Provider": "scripts/b"}
    assert KIT.seam_provider(row, modules) == "scripts/b"
    assert KIT.seam_provider({"IF-ID": "IF-001", "Owner": "LLR-001"}, modules) == (
        "project-trajectory/scripts/a.py"
    )
    # Neither a stated cell nor a derivable owner: '' — the published-medium
    # shape, never a crash and never a guess.
    assert KIT.seam_provider({"IF-ID": "IF-001", "Owner": "SR-001"}, modules) == ""
    assert (
        KIT.seam_provider(
            {"IF-ID": "IF-001", "Owner": "LLR-002"},
            {"LLR-002": "a.py;b.py"},
        )
        == ""
    )
