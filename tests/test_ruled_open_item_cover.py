"""A ruled open item has its action planned, done or handed on (WI-1006).

Ruling an open item takes it off the operator's page, so what the ruling asked
for lives on only where something names the item. A `ruled` item is covered
when a work item in an open or complete directory names it, when another open
item names it and is `pending` (or `ruled` and itself covered), or when its
`follow_up` cell is set. `gen_open_items.py --ruled-cover` reports every other
ruled item, warn-only, and `run.cmd audit` runs it ahead of the smoke budget.

Every case here builds a temporary repository and reads it in-process.

Implements: TC-430, TC-431
"""

import configparser
import json
import shlex
import tomllib

import pytest

from conftest import KIT, ROOT, load_script

gen = load_script("gen_open_items")
pending = load_script("pending")


def _registry(root, items):
    """Write the open-items registry: one `(id, status, extra cells)` per row."""
    lines = []
    for oid, state, cells in items:
        lines += ["[open_item.{}]".format(oid), 'title = "{} title"'.format(oid)]
        lines.append("status = {}".format(json.dumps(state)))
        for key, value in cells.items():
            lines.append("{} = {}".format(key, json.dumps(value)))
        lines.append("")
    path = root / "docs/requirements/open-items.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _work(root, wid, text, where="queued", base="docs/work"):
    """Write one work item whose body says `text`, under `base/where/`."""
    path = root / base / where / "{}-row.md".format(wid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '+++\nid = "{0}"\ntitle = "{0} row"\n+++\n\n## Context\n\n{1}\n'.format(
            wid, text
        ),
        encoding="utf-8",
    )


def _reported(root):
    """The ids the report names, in order."""
    return [oid for oid, _row in pending.ruled_cover(root)]


# --- TC-430: the rule ---------------------------------------------------------


@pytest.mark.parametrize(
    "base, where",
    [
        ("docs/work", "draft"),
        ("docs/work", "queued"),
        ("docs/work", "active"),
        ("docs/work", "deferred"),
        ("docs/archive/work", "complete"),
        ("docs/work", "complete"),
    ],
)
def test_a_row_in_an_open_or_complete_directory_covers_the_item(
    tmp_path, base, where
):
    _registry(tmp_path, [("OI-5", "ruled", {}), ("OI-6", "ruled", {})])
    _work(tmp_path, "WI-1", "OI-5 ruled 2026-01-02: done.", where, base)
    assert _reported(tmp_path) == ["OI-6"]


@pytest.mark.parametrize(
    "base, where",
    [
        ("docs/archive/work", "cancelled"),
        ("docs/archive/work", "partial"),
        ("docs/archive/work", "restructured"),
        ("docs/work", "handback"),
    ],
)
def test_a_cancelled_partial_or_restructured_row_covers_nothing(
    tmp_path, base, where
):
    # `handback` is not a status directory, so a file there is no work item.
    _registry(tmp_path, [("OI-5", "ruled", {})])
    _work(tmp_path, "WI-1", "OI-5 ruled 2026-01-02: done.", where, base)
    assert _reported(tmp_path) == ["OI-5"]


def test_an_item_handed_to_a_pending_item_is_covered(tmp_path):
    _registry(
        tmp_path,
        [
            ("OI-5", "ruled", {}),
            ("OI-6", "pending", {"decision": "Continues OI-5's ruling."}),
        ],
    )
    assert _reported(tmp_path) == []


def test_an_item_handed_through_a_covered_ruled_item_is_covered(tmp_path):
    _registry(
        tmp_path,
        [
            ("OI-5", "ruled", {}),
            ("OI-6", "ruled", {"options": "- (a) carry OI-5 forward."}),
            ("OI-7", "ruled", {"recommendation": "Builds on OI-6."}),
        ],
    )
    _work(tmp_path, "WI-1", "OI-7 ruled 2026-01-02: built.")
    assert _reported(tmp_path) == []


def test_a_ruled_citer_that_is_not_covered_hands_nothing_on(tmp_path):
    _registry(
        tmp_path,
        [("OI-5", "ruled", {}), ("OI-6", "ruled", {"decision": "After OI-5."})],
    )
    assert _reported(tmp_path) == ["OI-5", "OI-6"]


def test_a_cycle_of_ruled_items_with_no_row_is_reported(tmp_path):
    _registry(
        tmp_path,
        [
            ("OI-5", "ruled", {"decision": "See OI-6."}),
            ("OI-6", "ruled", {"decision": "See OI-5."}),
        ],
    )
    assert _reported(tmp_path) == ["OI-5", "OI-6"]
    # One covered member covers the whole cycle.
    _work(tmp_path, "WI-1", "OI-6 ruled 2026-01-02: done.")
    assert _reported(tmp_path) == []


def test_a_follow_up_cell_covers_the_item_and_a_blank_one_does_not(tmp_path):
    _registry(
        tmp_path,
        [
            ("OI-5", "ruled", {"follow_up": "none — the ruling kept things as is"}),
            ("OI-6", "ruled", {"follow_up": "   "}),
        ],
    )
    assert _reported(tmp_path) == ["OI-6"]


def test_the_token_reads_a_whole_number(tmp_path):
    _registry(tmp_path, [("OI-35", "ruled", {}), ("OI-36", "ruled", {})])
    _work(tmp_path, "WI-1", "OI-350, XOI-35 and oi-35 are not it; OI-036 is OI-36.")
    assert _reported(tmp_path) == ["OI-35"]


def test_the_historical_cell_and_a_self_mention_cover_nothing(tmp_path):
    _registry(
        tmp_path,
        [
            ("OI-5", "ruled", {"decision": "OI-5 is ruled."}),
            ("OI-6", "pending", {"wi_refs": ["WI-1", "OI-7"]}),
            ("OI-7", "ruled", {}),
        ],
    )
    assert _reported(tmp_path) == ["OI-5", "OI-7"]


def test_an_example_row_is_never_judged_and_its_work_item_covers_nothing(tmp_path):
    _registry(tmp_path, [("OI-000", "ruled", {}), ("OI-5", "ruled", {})])
    _work(tmp_path, "WI-000", "OI-5 is the example's.")
    assert _reported(tmp_path) == ["OI-5"]


def test_an_example_row_hands_nothing_on(tmp_path):
    _registry(
        tmp_path,
        [("OI-000", "pending", {"decision": "OI-5 follows."}), ("OI-5", "ruled", {})],
    )
    assert _reported(tmp_path) == ["OI-5"]


def test_a_citer_outside_pending_and_ruled_covers_nothing(tmp_path):
    # A light-spine `implemented` item is not judged itself, and covers nothing.
    _registry(
        tmp_path,
        [
            ("OI-5", "ruled", {}),
            ("OI-6", "implemented", {"decision": "Did OI-5's work."}),
        ],
    )
    assert _reported(tmp_path) == ["OI-5"]


def test_a_status_is_read_trimmed_and_in_lower_case(tmp_path):
    _registry(
        tmp_path,
        [
            ("OI-5", " Ruled ", {}),
            ("OI-6", "PENDING", {"decision": "Continues OI-7."}),
            ("OI-7", "ruled", {}),
        ],
    )
    assert _reported(tmp_path) == ["OI-5"]


# --- TC-431: the report and the audit -------------------------------------------


def test_no_registry_is_vacuous(tmp_path, capsys):
    assert pending.ruled_cover(tmp_path) is None
    assert gen.main(["--root", str(tmp_path), "--ruled-cover"]) == 0
    assert "vacuous" in capsys.readouterr().out


def test_a_registry_that_does_not_parse_stops_the_report(tmp_path):
    path = tmp_path / "docs/requirements/open-items.toml"
    path.parent.mkdir(parents=True)
    path.write_text('[open_item.OI-1]\ntitle = "unterminated\n', encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        gen.main(["--root", str(tmp_path), "--ruled-cover"])
    assert "does not parse" in str(exc.value.code)


def test_a_finding_names_the_item_and_its_title_and_exits_zero(tmp_path, capsys):
    _registry(tmp_path, [("OI-5", "ruled", {}), ("OI-6", "ruled", {})])
    _work(tmp_path, "WI-1", "OI-6 ruled 2026-01-02: done.")
    assert gen.main(["--root", str(tmp_path), "--ruled-cover"]) == 0
    out = capsys.readouterr().out
    warn = [line for line in out.splitlines() if "WARN" in line]
    assert len(warn) == 1 and "OI-5" in warn[0] and "OI-5 title" in warn[0], out
    assert "follow_up" in warn[0], out
    assert "1 finding" in out, out


def test_a_covered_registry_reports_no_finding(tmp_path, capsys):
    _registry(tmp_path, [("OI-5", "ruled", {"follow_up": "commit abc1234"})])
    assert gen.main(["--root", str(tmp_path), "--ruled-cover"]) == 0
    out = capsys.readouterr().out
    assert "WARN" not in out and "0 finding" in out, out


def _audit_steps():
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(ROOT / "docs" / "stack.ini", encoding="utf-8-sig")
    return [step.strip() for step in cp["run"]["audit"].split("&&")]


def test_the_audit_runs_the_report_before_the_budget_step():
    steps = _audit_steps()
    report = "python project-trajectory/scripts/gen_open_items.py --ruled-cover"
    assert steps[0] == report, steps
    assert "python scripts/check_smoke_budget.py --mode enforce" in steps[1:], steps
    # The report's own line runs it with no other mode, so it exits 0 on a finding.
    assert shlex.split(steps[0])[2:] == ["--ruled-cover"]


def _example_row(path):
    return tomllib.loads(path.read_text(encoding="utf-8"))["open_item"]["OI-000"]


def test_the_template_and_this_registry_show_follow_up_on_their_example_row():
    template = KIT / "registries" / "open-items.template.toml"
    live = ROOT / "docs" / "requirements" / "open-items.toml"
    assert _example_row(template).get("follow_up")
    assert _example_row(live).get("follow_up")
    header = [
        line
        for line in template.read_text(encoding="utf-8").splitlines()
        if line.startswith("#")
    ]
    assert any("`follow_up`" in line for line in header)
    assert any("--ruled-cover" in line for line in header)
