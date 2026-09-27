"""What is generated has one home: the regeneration's declared writes.

`trunk_step.REGEN_STEPS` names every path each regeneration step writes, and
the stack profile's `[generated]` section is what the lane-close readers
(`integrate._abandoned_claim`, `integrate.audit`) treat as generated. The
shipped template declared three of the ten, so an adopter's claim commit
touched paths its own audit then flagged. The template's list is now held
EQUAL to the regeneration's writes, both ways, and this repo's own profile
must cover every write (it declares more: hand-stamped data and artifacts with
their own regenerators, which is ownership the regeneration does not write).
In memory: no scaffold, no subprocess, no git. The two readers themselves are
driven over real git fixtures in the slow integrator modules.
"""

import configparser

from conftest import KIT, ROOT, load_script

TEMPLATE = KIT / "stack.ini.template"
LIVE = ROOT / "docs" / "stack.ini"


def _declared(path):
    cp = configparser.ConfigParser(interpolation=None)
    cp.optionxform = str  # keys are paths; the default lowercases them
    cp.read_string(path.read_text(encoding="utf-8"))
    return {k.strip() for k in cp.options("generated") if k.strip()}


def _covers(entry, path):
    return path.startswith(entry) if entry.endswith("/") else path == entry


def generated_drift(declared, writes):
    """`(omitted, unwritten)`: each regeneration write no declared row covers,
    and each declared row no regeneration step writes."""
    omitted = sorted(w for w in writes if not any(_covers(d, w) for d in declared))
    unwritten = sorted(d for d in declared if d not in writes)
    return omitted, unwritten


def _writes():
    return set(load_script("trunk_step").regen_writes())


def test_the_template_declares_exactly_what_the_regeneration_writes():
    omitted, unwritten = generated_drift(_declared(TEMPLATE), _writes())
    assert omitted == [], "a regeneration write the template does not declare"
    assert unwritten == [], "a template row no regeneration step writes"


def test_the_drift_reads_both_directions():
    # Non-vacuity: a new regeneration step's write, and a stale template row,
    # each fail the equality above on their own.
    writes = _writes()
    declared = _declared(TEMPLATE)
    assert generated_drift(declared, writes | {"docs/new-view.html"}) == (
        ["docs/new-view.html"],
        [],
    )
    assert generated_drift(declared | {"docs/retired.html"}, writes) == (
        [],
        ["docs/retired.html"],
    )


def test_this_repo_declares_every_regeneration_write():
    omitted, _ownership = generated_drift(_declared(LIVE), _writes())
    assert omitted == [], "docs/stack.ini [generated] omits a regeneration write"


def test_the_declared_set_reader_returns_the_template_rows(tmp_path):
    # The shared read, in memory. The two readers are driven behaviourally
    # against the shipped list in the slow integrator modules: a claim-shaped
    # commit carrying every regeneration output (tests/test_integrate.py) and an
    # audit window of one (tests/test_integrate_admission.py), each accepted
    # under the template and refused under a stale list.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_bytes(TEMPLATE.read_bytes())
    integrate = load_script("integrate")
    assert set(integrate._generated_paths(tmp_path)) == _writes()
