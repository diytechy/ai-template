"""gen_arch_map.py: map content, flow entry resolution, and splice safety."""

import pytest

from conftest import load_script

gen_arch_map = load_script("gen_arch_map")

MOD_A = '''"""Module A — demo."""


def helper_a():
    """Helper in A."""


def run():
    """Run A. Implements: SR-001"""
    helper_a()
'''

MOD_B = '''"""Module B — demo."""


def helper_b():
    """Helper in B."""


def run():
    """Run B."""
    helper_b()
'''


@pytest.fixture
def two_module_src(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text(MOD_A, encoding="utf-8")
    (src / "b.py").write_text(MOD_B, encoding="utf-8")
    return str(src)


def test_map_harvests_summaries_and_implements(two_module_src):
    out = gen_arch_map.build_map([two_module_src])
    assert "Module A — demo." in out
    assert "SR-001" in out  # Implements back-link from the docstring
    assert "`helper_b()`" in out


def test_flow_module_qualifier_selects_the_right_run(two_module_src):
    # Regression: the `module:entry` form used to be accepted but ignored.
    flow_b = gen_arch_map.build_flow([two_module_src], "b:run")
    assert "Run B." in flow_b
    assert "helper_b" in flow_b
    assert "helper_a" not in flow_b


def test_flow_ambiguous_bare_name_errors(two_module_src):
    with pytest.raises(SystemExit, match="ambiguous"):
        gen_arch_map.build_flow([two_module_src], "run")


def test_flow_unknown_entry_errors(two_module_src):
    with pytest.raises(SystemExit, match="not found"):
        gen_arch_map.build_flow([two_module_src], "nope")


def test_splice_refuses_duplicated_markers():
    b, e = gen_arch_map.BEGIN, gen_arch_map.END
    doc = "x\n{b}\nold\n{e}\ny\n{b}\nagain\n{e}\n".format(b=b, e=e)
    with pytest.raises(SystemExit, match="duplicated marker"):
        gen_arch_map.splice_region(doc, b, e, "new", "doc.md", required=True)


def test_splice_replaces_between_markers():
    b, e = gen_arch_map.BEGIN, gen_arch_map.END
    doc = "intro\n{}\nold\n{}\noutro\n".format(b, e)
    out = gen_arch_map.splice_region(doc, b, e, "new", "doc.md", required=True)
    assert "old" not in out
    assert "new" in out
    assert out.startswith("intro\n") and out.endswith("outro\n")
