"""`kitlib.registry`'s one work-spec listing, in process (TC-313, TC-383).

The ruling sync and the adoption record both list the work specs of a tree
(or of the index): every path under the work root and its archive whose file
name begins `WI-` and ends `.md`, in git's order. One kernel function owns that
listing, and each caller keeps its own view over it: the ruling sync's
`{id: path}` (a `-000` example dropped, the last path winning), the adoption
record's `{id: [path, ...]}` (every path kept, so several specs carrying one id
still refuse), and the registry loader's work-root relpaths.

No repository is built: `kitlib.git.git_paths` is replaced by a fake answering
the argv the listing sends, and for the views the listing itself is replaced
by a recording fake. The same tree read through real git is characterized in
test_adoption_record.py.

Implements: TC-313, TC-383
"""

import pytest
from conftest import load_script

from kitlib import git as kgit
from kitlib import registry as kregistry

ar = load_script("adoption_record")
acceptance = load_script("acceptance_record")

ROOTS = ["docs/work", "docs/archive/work"]

#: A fixed listing in git's order: WI-005 twice (archived complete, then
#: queued), a `-000` example, and WI-007 under its lane's `active/` folder.
ARCHIVED_005 = "docs/archive/work/complete/WI-005-five.md"
ACTIVE_007 = "docs/work/active/wi-007/WI-007-seven.md"
EXAMPLE_000 = "docs/work/queued/WI-000-example.md"
QUEUED_005 = "docs/work/queued/WI-005-five.md"
LISTING = [ARCHIVED_005, ACTIVE_007, EXAMPLE_000, QUEUED_005]


def _fake_git_paths(monkeypatch, answer):
    """Replace `kitlib.git.git_paths` with a fake answering `answer` (a list,
    or None for a tree git cannot list); every argv is recorded in order."""
    seen = []

    def fake(_root, args):
        seen.append(list(args))
        return None if answer is None else list(answer)

    monkeypatch.setattr(kgit, "git_paths", fake)
    return seen


def test_the_listing_reads_both_spec_roots_at_a_tree_or_the_index(monkeypatch):
    assert hasattr(kregistry, "tree_spec_paths")
    assert getattr(kregistry, "WORK_SPEC_ROOTS", None) == tuple(ROOTS)
    raw = [
        "docs/archive/work/complete/WI-003-three.md",
        "docs/archive/work/complete/notes.md",
        "docs/work/README.md",
        "docs/work/queued/WI-000-example.md",
        "docs/work/queued/WI-011-eleven.txt",
        "docs/work/queued/XWI-012-twelve.md",
        "docs/work/active/wi-010/WI-010-ten.md",
    ]
    kept = [
        "docs/archive/work/complete/WI-003-three.md",
        "docs/work/queued/WI-000-example.md",
        "docs/work/active/wi-010/WI-010-ten.md",
    ]
    seen = _fake_git_paths(monkeypatch, raw)
    assert kregistry.tree_spec_paths("root", None) == kept
    assert kregistry.tree_spec_paths("root", "HEAD") == kept
    assert seen == [
        ["ls-files", "--", *ROOTS],
        ["ls-tree", "-r", "--name-only", "HEAD", "--", *ROOTS],
    ]
    _fake_git_paths(monkeypatch, None)
    assert kregistry.tree_spec_paths("root", "HEAD") is None
    assert kregistry.tree_spec_paths("root", None) is None


def _fake_listing(monkeypatch, answer):
    """Replace `kitlib.registry.tree_spec_paths` with a recording fake
    answering `answer`; git itself answers nothing, so a view that still
    lists for itself reads no tree."""
    calls = []

    def fake(root, rev):
        calls.append((root, rev))
        return None if answer is None else list(answer)

    monkeypatch.setattr(kregistry, "tree_spec_paths", fake, raising=False)
    monkeypatch.setattr(kgit, "git_bytes", lambda *_a, **_k: None)
    return calls


def test_one_listing_serves_both_views(monkeypatch):
    calls = _fake_listing(monkeypatch, LISTING)
    assert acceptance._tree_specs("root", "HEAD") == {
        "WI-005": QUEUED_005,
        "WI-007": ACTIVE_007,
    }
    assert ar._spec_paths("root", "HEAD") == {
        "WI-005": [ARCHIVED_005, QUEUED_005],
        "WI-007": [ACTIVE_007],
        "WI-000": [EXAMPLE_000],
    }
    assert [rel for rel, _read in ar.tree_specs("root", "HEAD")] == [
        "active/wi-007/WI-007-seven.md",
        "queued/WI-000-example.md",
        "queued/WI-005-five.md",
    ]
    assert calls == [("root", "HEAD")] * 3

    _fake_listing(monkeypatch, None)
    assert acceptance._tree_specs("root", "HEAD") is None
    with pytest.raises(OSError, match="HEAD"):
        ar._spec_paths("root", "HEAD")
    with pytest.raises(OSError, match="docs/work"):
        ar.tree_specs("root", "HEAD")
