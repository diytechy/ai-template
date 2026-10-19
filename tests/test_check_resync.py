"""The commit bar's RESYNC entry check (scripts/check_resync.py).

A change to a shipped kit file passes only when it adds a `RESYNC_PACK.md`
entry heading anchored at its own trunk base. Most cases drive the pure
verdict with no git; a few build a small temp repo whose stub `bootstrap.py`
carries the inventory, because the check classifies each side with that
side's own inventory code.
"""

import importlib.util
import os
import subprocess
import sys

from conftest import KIT, ROOT, declare_trunk

SCRIPT = ROOT / "scripts" / "check_resync.py"
_spec = importlib.util.spec_from_file_location("check_resync", SCRIPT)
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)

BASE = "a" * 40
OTHER = "b" * 40
SHIPPED = "project-trajectory/scripts/trace.py"
OLD = "### An older change [since 1234567]"


def _resolver(mapping):
    return lambda sha: mapping.get(sha)


def _judge(changed, *, shipped=(), base_only=(), head_only=(), added=(), **kw):
    """Drive `judge` with both sides holding `shipped` unless told otherwise."""
    present = set(shipped) | {"project-trajectory/RESYNC_PACK.md"}
    args = {
        "changed": changed,
        "shipped_base": set(shipped) | set(base_only),
        "shipped_head": set(shipped) | set(head_only),
        "present_base": present | set(base_only),
        "present_head": present | set(head_only),
        "base_headings": [OLD],
        "head_headings": [OLD, *added],
        "base_sha": BASE,
        "resolve": _resolver({"aaaaaaa": BASE, "bbbbbbb": OTHER}),
    }
    args.update(kw)
    return check.judge(**args)


def test_a_shipped_change_with_no_entry_is_refused():
    refusals = _judge([SHIPPED], shipped=[SHIPPED])
    assert refusals == [(SHIPPED, check.NO_ENTRY)]


def test_an_entry_anchored_at_the_base_passes():
    refusals = _judge([SHIPPED], shipped=[SHIPPED], added=["### New [since aaaaaaa]"])
    assert refusals == []


def test_an_entry_anchored_at_another_commit_is_refused():
    heading = "### New [since bbbbbbb]"
    refusals = _judge([SHIPPED], shipped=[SHIPPED], added=[heading])
    subjects = [subject for subject, _ in refusals]
    assert subjects == [heading, SHIPPED]
    assert BASE in refusals[0][1]


def test_an_unresolvable_anchor_is_refused():
    heading = "### New [since ccccccc]"
    refusals = _judge([SHIPPED], shipped=[SHIPPED], added=[heading])
    assert [subject for subject, _ in refusals] == [heading, SHIPPED]


def test_an_edited_only_entry_does_not_count():
    # The body under an existing heading changed; the heading set did not.
    refusals = _judge([SHIPPED, "project-trajectory/RESYNC_PACK.md"], shipped=[SHIPPED])
    assert refusals == [(SHIPPED, check.NO_ENTRY)]


RE_ANCHORED = "### An older change [since aaaaaaa]"
NEW = "### New [since aaaaaaa]"


def test_a_re_anchored_existing_entry_does_not_count():
    refusals = _judge([SHIPPED], shipped=[SHIPPED], head_headings=[RE_ANCHORED])
    assert refusals == [(SHIPPED, check.NO_ENTRY)]


def test_a_retitled_and_re_anchored_entry_does_not_count():
    heading = "### A renamed change [since aaaaaaa]"
    refusals = _judge([SHIPPED], shipped=[SHIPPED], head_headings=[heading])
    assert refusals == [(SHIPPED, check.NO_ENTRY)]


def test_a_new_entry_beside_a_removed_one_does_not_count():
    # Removing a landed entry is not refused, but it cancels one new entry.
    refusals = _judge([SHIPPED], shipped=[SHIPPED], head_headings=[NEW])
    assert refusals == [(SHIPPED, check.NO_ENTRY)]
    assert _judge([], head_headings=[RE_ANCHORED]) == []


def test_a_moved_entry_with_a_new_one_passes():
    refusals = _judge([SHIPPED], shipped=[SHIPPED], head_headings=[NEW, OLD])
    assert refusals == []


def test_a_new_entry_beside_a_re_anchored_one_passes():
    head = [RE_ANCHORED, NEW]
    assert _judge([SHIPPED], shipped=[SHIPPED], head_headings=head) == []


def test_a_reserved_placeholder_does_not_count():
    heading = "### Reserved: a later change"
    assert [s for s, _ in _judge([SHIPPED], shipped=[SHIPPED], added=[heading])] == [
        heading,
        SHIPPED,
    ]
    assert [s for s, _ in _judge([], added=[heading])] == [heading]


def test_a_pre_anchor_does_not_count():
    heading = "### Old news [since pre-aaaaaaa]"
    assert [s for s, _ in _judge([SHIPPED], shipped=[SHIPPED], added=[heading])] == [
        heading,
        SHIPPED,
    ]
    assert [s for s, _ in _judge([], added=[heading])] == [heading]


def test_a_heading_outside_the_grammar_is_refused():
    heading = "### A change (2026-10)"
    assert [s for s, _ in _judge([], added=[heading])] == [heading]


def test_a_change_only_to_a_this_repo_skill_owes_no_entry():
    skill = "project-trajectory/skills/render-dashboard-critique/SKILL.md"
    refusals = _judge([skill], present_base={skill}, present_head={skill})
    assert refusals == []


def test_a_deleted_shipped_file_owes_an_entry():
    gone = "project-trajectory/scripts/retired.py"
    refusals = _judge([gone], base_only=[gone])
    assert refusals == [(gone, check.NO_ENTRY)]


def test_a_change_outside_the_kit_owes_no_entry():
    refusals = _judge(["tests/x.py", ".claude/skills/a/SKILL.md", "scripts/y.py"])
    assert refusals == []


def test_a_file_that_stops_shipping_owes_an_entry():
    # Same bytes on both sides; only the exclusion registry changed, and that
    # registry does not ship itself.
    moved = "project-trajectory/EXAMPLE.md"
    registry = "project-trajectory/mapping-source-exclusions"
    refusals = _judge(
        [registry],
        present_base={moved, registry},
        present_head={moved, registry},
        shipped_base={moved},
        shipped_head=set(),
    )
    assert refusals == [(moved, check.NO_ENTRY)]


def test_a_changed_kit_path_no_inventory_saw_counts_as_shipped():
    stray = "project-trajectory/scripts/__pycache__/x.pyc"
    assert _judge([stray]) == [(stray, check.NO_ENTRY)]


def test_a_generator_source_and_an_unclassified_kit_path_count_as_shipped():
    kit = check.Kit(
        present=frozenset(),
        excluded=frozenset({"scripts/bootstrap.py", "LICENSE", "README.md"}),
        generators=frozenset({"scripts/bootstrap.py", "LICENSE"}),
    )
    assert kit.ships("project-trajectory/scripts/bootstrap.py")
    assert kit.ships("project-trajectory/LICENSE")
    assert kit.ships("project-trajectory/zz-unclassified.txt")
    assert not kit.ships("project-trajectory/README.md")
    assert not kit.ships("scripts/check_changed.py")


def test_the_real_inventory_classifies_the_kit():
    kit = check.kit_classes(KIT)
    skill = "project-trajectory/skills/render-dashboard-critique/SKILL.md"
    assert skill in kit.present and not kit.ships(skill)
    for path in ("scripts/bootstrap.py", "LICENSE", "scripts/trace.py"):
        assert kit.ships("project-trajectory/" + path), path
    assert not kit.ships("project-trajectory/RESYNC_PACK.md")
    assert kit.ships("project-trajectory/zz-unclassified.txt")


# --- git-backed: a small repo whose kit carries a stub inventory -------------

STUB = """from pathlib import Path

KIT = Path(__file__).resolve().parent.parent


def delivery_inventory():
    if (KIT / "broken").exists():
        raise RuntimeError("inventory broken")
    sources = {p.relative_to(KIT).as_posix() for p in KIT.rglob("*") if p.is_file()}
    excluded = {"RESYNC_PACK.md": "kit-side", "notes.md": "kit-side"}
    return sources, excluded, (), (("scripts/bootstrap.py", "docs/kit-version"),)
"""

PACK_TEXT = """# Pack

## 3. What changed over time

{entries}
## 4. Translation helper

## 5. Promotion
"""


def _git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def _write(root, path, text):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _pack(root, *headings):
    body = "".join(h + "\n\nBody.\n\n" for h in headings)
    _write(root, "project-trajectory/RESYNC_PACK.md", PACK_TEXT.format(entries=body))


def _repo(tmp_path):
    _git(tmp_path, "init", "-q", "-b", "trunk")
    _git(tmp_path, "config", "user.email", "test@example.invalid")
    _git(tmp_path, "config", "user.name", "Resync test")
    _git(tmp_path, "config", "core.autocrlf", "false")
    _write(tmp_path, "project-trajectory/scripts/bootstrap.py", STUB)
    _write(tmp_path, "project-trajectory/tool.py", "VALUE = 1\n")
    _pack(tmp_path, OLD)
    declare_trunk(tmp_path, "trunk")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-qm", "base")
    return tmp_path, _git(tmp_path, "rev-parse", "HEAD")


def test_an_unreadable_base_is_refused(tmp_path):
    root, _ = _repo(tmp_path)
    for base in (None, "f" * 40):
        refusals, _summary = check.run(root, base)
        assert refusals and refusals[0][0] == "base", refusals


def test_an_absent_pack_is_refused(tmp_path):
    root, base = _repo(tmp_path)
    pack = root / "project-trajectory/RESYNC_PACK.md"
    pack.unlink()
    refusals, _ = check.run(root, base)
    assert [s for s, _ in refusals] == ["RESYNC_PACK.md"]
    _git(root, "rm", "-q", "project-trajectory/RESYNC_PACK.md")
    _git(root, "commit", "-qm", "pack gone")
    _pack(root, OLD)
    refusals, _ = check.run(root, _git(root, "rev-parse", "HEAD"))
    assert [s for s, _ in refusals] == ["RESYNC_PACK.md"]


def test_an_uncomputable_inventory_is_refused(tmp_path):
    root, base = _repo(tmp_path)
    _write(root, "project-trajectory/broken", "x\n")
    refusals, _ = check.run(root, base)
    assert [s for s, _ in refusals] == ["inventory"]
    assert "inventory broken" in refusals[0][1]


def test_an_untracked_shipped_file_counts(tmp_path):
    root, base = _repo(tmp_path)
    _write(root, "project-trajectory/new_tool.py", "NEW = 1\n")
    refusals, _ = check.run(root, base)
    assert refusals == [("project-trajectory/new_tool.py", check.NO_ENTRY)]
    _write(root, "project-trajectory/notes.md", "kit-side only\n")
    _git(root, "rm", "-q", "project-trajectory/tool.py")
    refusals, _ = check.run(root, base)
    assert [s for s, _ in refusals] == [
        "project-trajectory/new_tool.py",
        "project-trajectory/tool.py",
    ]


def test_the_cli_on_trunk_judges_against_head(tmp_path):
    root, base = _repo(tmp_path)
    _write(root, "project-trajectory/tool.py", "VALUE = 2\n")
    _git(root, "commit", "-qam", "a second commit")
    head = _git(root, "rev-parse", "HEAD")
    _write(root, "project-trajectory/tool.py", "VALUE = 3\n")

    def cli(anchor):
        _pack(root, OLD, "### Tool value [since {}]".format(anchor[:9]))
        _git(root, "add", ".")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root)],
            capture_output=True,
            text=True,
        )

    passed = cli(head)
    assert passed.returncode == 0, passed.stdout + passed.stderr
    assert head in passed.stdout
    refused = cli(base)
    assert refused.returncode == 1, refused.stdout + refused.stderr
    assert "project-trajectory/tool.py" in refused.stdout


def test_a_refused_heading_a_legacy_console_cannot_encode_is_still_named(tmp_path):
    root, _base = _repo(tmp_path)
    _write(root, "project-trajectory/tool.py", "VALUE = 2\n")
    heading = "### Tool \u2192 value [since 1234567]"
    _pack(root, OLD, heading)
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    env.pop("PYTHONUTF8", None)
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        env=env,
    )
    out = proc.stdout.decode("utf-8")
    assert proc.returncode == 1, out + proc.stderr.decode("utf-8", "replace")
    assert "REFUSED " + heading + ": anchored at 1234567" in out
    assert "REFUSED project-trajectory/tool.py: " + check.NO_ENTRY in out
