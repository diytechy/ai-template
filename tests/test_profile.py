"""Conditional scaffold generation (Thread 34, the Q8 ruling).

The kit masters carry ALL permutations; bootstrap generates each repo's docs by
omitting what the declared profile turns off. The properties pinned here are
the ruling's own constraints: § labels never renumber, omissions leave
resolvable stubs, every permutation scaffolds fully green, the default profile
changes nothing, and a re-sync regenerates from the recorded docs/kit-profile.
"""

import itertools

import pytest
from conftest import KIT, SCRIPTS, load_script, run_py

boot = load_script("bootstrap")

# The copy-me meta-prose that must never survive into a scaffold (it lives in
# kit-only regions of the masters), plus the marker vocabulary itself.
LEFTOVER_PHRASES = (
    "<!-- kit-only -->",
    "<!-- /kit-only -->",
    "<!-- profile:",
    "<!-- /profile -->",
    "Copy this into a new repo",
    "Copied into a new repo",
    "Scaffolds to `AGENTS.md`",
    "Copy to `docs/",
)

# Every §-numbered heading the profile axes gate; these labels must be literal,
# stable text in EVERY permutation (the owner's §N-constancy constraint).
GATED_HEADINGS = {
    "docs/process.md": (
        "## 9. Non-functional requirements & performance budgets",
        "## 10. Project scale — one module, several modules, several repos",
    ),
    "docs/process-options.md": (
        "## §9 NFR checklist",
        "## §9 perf comparator",
        "## §10 several modules, one repo",
    ),
}

# Which stub markers each omitted axis must leave, per generated doc.
AXIS_STUBS = {
    "nfr": {"docs/process.md": 1, "docs/process-options.md": 2},
    "multi-module": {"docs/process.md": 1, "docs/process-options.md": 1},
}


def _bootstrap(tmp_path, *extra):
    dest = tmp_path / "repo"
    tmp_path.mkdir(parents=True, exist_ok=True)  # sub-dirs like tmp_path/"a"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest, *extra], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return dest


def _zero_findings(dest):
    """check_docs with the harness's own invocation must report zero findings
    of ANY class — not just zero failures (R8/C2)."""
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=dest
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" not in proc.stdout, proc.stdout
    assert "FAIL" not in proc.stdout, proc.stdout


# --- The marker grammar (unit) ------------------------------------------------


def test_strip_markers_drops_kit_only_and_keeps_selected_profiles():
    text = "a\n<!-- kit-only -->\ncopy me\n<!-- /kit-only -->\nb\n<!-- profile: nfr -->\nbody\n<!-- /profile -->\nc\n"
    kept = boot.strip_markers(text, frozenset())
    assert kept == "a\nb\nbody\nc\n"
    omitted = boot.strip_markers(text, frozenset(["nfr"]))
    assert "copy me" not in omitted
    assert "body" not in omitted
    assert boot.profile_stub("nfr") in omitted
    assert omitted.splitlines()[-1] == "c"


def test_strip_markers_rejects_malformed_regions():
    for bad in (
        "<!-- kit-only -->\nnever closed\n",
        "<!-- /profile -->\nclose without open\n",
        "<!-- profile: nfr -->\n<!-- kit-only -->\nnested\n<!-- /kit-only -->\n<!-- /profile -->\n",
    ):
        with pytest.raises(ValueError):
            boot.strip_markers(bad, frozenset())


def test_kit_masters_markers_balanced_with_known_axes():
    # Lint every shipped Markdown template: markers must balance (strip_markers
    # raises otherwise) and every profile axis must be a declared one — an
    # unknown axis would silently never be omittable.
    every = frozenset(boot.PROFILE_AXES)
    for src_rel, dst_rel in boot.MAPPING:
        if not dst_rel.endswith(".md"):
            continue
        text = (KIT / src_rel).read_text(encoding="utf-8")
        boot.strip_markers(text, every, src_rel)  # raises on malformed markers
        for line in text.splitlines():
            m = boot.PROFILE_OPEN_RE.match(line.strip())
            if m:
                assert m.group(1) in boot.PROFILE_AXES, (
                    src_rel + ": unknown profile axis " + m.group(1)
                )


# --- The generated scaffold ---------------------------------------------------


def test_scaffold_carries_no_marker_or_copyme_leftovers(scaffold):
    # The spec's own acceptance grep: no scaffolded doc reads as a template.
    for md in list(scaffold.glob("*.md")) + list((scaffold / "docs").rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for phrase in LEFTOVER_PHRASES:
            assert phrase not in text, "{}: leftover {!r}".format(md.name, phrase)


def test_default_scaffold_is_fully_green_including_warnings(scaffold):
    # R8/C2: zero findings of any class on a fresh scaffold — the README links
    # docs/interfaces.md and the stakeholder-needs registry so no doc is an
    # orphan, and the generated trace report is --ignore'd as check.py does.
    _zero_findings(scaffold)


def test_default_scaffold_keeps_all_gated_sections(scaffold):
    # No --omit: every gated section ships with its body, no stubs anywhere.
    for rel, headings in GATED_HEADINGS.items():
        text = (scaffold / rel).read_text(encoding="utf-8")
        for heading in headings:
            assert heading in text, rel + " must keep " + heading
        assert "Omitted by this repo's profile" not in text
    profile = (scaffold / "docs" / "kit-profile").read_text(encoding="utf-8")
    assert "stack=any" in profile
    assert "omit=\n" in profile


@pytest.mark.parametrize(
    "omit,stack",
    list(
        itertools.product(
            [(), ("nfr",), ("multi-module",), ("nfr", "multi-module")],
            ["any", "node"],
        )
    ),
    ids=lambda v: (",".join(v) or "none") if isinstance(v, tuple) else v,
)
def test_every_profile_permutation_scaffolds_green(tmp_path, omit, stack):
    # The permutation matrix that holds the Q8 line: every profile must
    # scaffold green (docs + trace), keep every § label, and leave a stub
    # exactly where a section was omitted.
    args = ["--stack", stack]
    if omit:
        args += ["--omit", ",".join(omit)]
    dest = _bootstrap(tmp_path, *args)
    for rel, headings in GATED_HEADINGS.items():
        text = (dest / rel).read_text(encoding="utf-8")
        for heading in headings:
            assert heading in text, "§ label lost in {} ({})".format(rel, omit)
        for axis in boot.PROFILE_AXES:
            expected = AXIS_STUBS[axis].get(rel, 0) if axis in omit else 0
            assert text.count(boot.profile_stub(axis)) == expected, (
                "{}: wrong stub count for {} under omit={}".format(rel, axis, omit)
            )
    _zero_findings(dest)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=dest)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # THE OWNER DECISION SURFACE IS ALWAYS ON (OI-41, ruled 2026-08-20): the
    # registry AND its generated view land in every permutation, so `check_docs`
    # S-3 means the same thing in every adopting repo instead of standing down
    # wherever the layer was declined. Both halves, because a missing view reads
    # as STALE to its own freshness gate — asserted right here with the profile
    # matrix, since "for every profile" is a claim only this test can make.
    assert (dest / "docs" / "requirements" / "open-items.toml").is_file()
    assert (dest / "docs" / "open-items.html").is_file()
    fresh = run_py(["scripts/gen_open_items.py", "--check"], cwd=dest)
    assert fresh.returncode == 0, fresh.stdout + fresh.stderr
    assert "VACUITY" not in fresh.stdout


# --- Stack-gated artifacts (R7/C3) --------------------------------------------


def test_node_scaffold_gates_python_artifacts_and_appends_checklist(tmp_path):
    dest = _bootstrap(tmp_path, "--stack", "node")
    assert not (dest / "pytest.ini").exists(), "node scaffold must skip pytest.ini"
    status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
    for oi in ("OI-3", "OI-4", "OI-5", "OI-6"):
        assert oi in status, "rewiring checklist bullet missing: " + oi
    assert "node toolchain commands" in status
    # The checklist bullets' links must resolve (zero findings covers them).
    _zero_findings(dest)
    profile = (dest / "docs" / "kit-profile").read_text(encoding="utf-8")
    assert "stack=node" in profile


def test_stack_any_matches_default_byte_for_byte(tmp_path):
    # The CI-safe property, extended: blank/any --stack is byte-for-byte
    # today's scaffold — same files, same bytes (kit-version/profile included;
    # both runs come from the same kit state).
    a = _bootstrap(tmp_path / "a")
    b = _bootstrap(tmp_path / "b", "--stack", "any")
    files_a = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
    files_b = sorted(p.relative_to(b) for p in b.rglob("*") if p.is_file())
    assert files_a == files_b
    for rel in files_a:
        assert (a / rel).read_bytes() == (b / rel).read_bytes(), str(rel)


def test_python_and_default_scaffolds_keep_pytest_ini(tmp_path):
    for extra in ((), ("--stack", "python")):
        dest = _bootstrap(tmp_path / ("d" + str(len(extra))), *extra)
        assert (dest / "pytest.ini").exists()
        status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
        assert "OI-3" not in status, "checklist must not appear for " + str(extra)


# --- The recorded profile & re-sync regeneration ------------------------------


def test_resync_regenerates_from_recorded_profile(tmp_path):
    # ADOPTING.md §6: delete the generated process docs, re-run bootstrap with
    # NO flags — it re-reads docs/kit-profile and regenerates the same
    # structural choices instead of silently reverting them.
    dest = _bootstrap(tmp_path, "--stack", "node", "--omit", "nfr")
    (dest / "docs" / "process.md").unlink()
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    regen = (dest / "docs" / "process.md").read_text(encoding="utf-8")
    assert boot.profile_stub("nfr") in regen, "omission must survive the re-sync"
    assert boot.profile_stub("multi-module") not in regen
    assert not (dest / "pytest.ini").exists(), "stack choice must survive too"
    # The checklist must not be appended twice on the re-run.
    status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
    assert status.count("OI-3") == 1
    profile = (dest / "docs" / "kit-profile").read_text(encoding="utf-8")
    assert "stack=node" in profile and "omit=nfr" in profile


def test_explicit_flags_override_recorded_profile(tmp_path):
    dest = _bootstrap(tmp_path, "--omit", "nfr")
    (dest / "docs" / "process.md").unlink()
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--omit", ""], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    regen = (dest / "docs" / "process.md").read_text(encoding="utf-8")
    assert "Omitted by this repo's profile" not in regen
    profile = (dest / "docs" / "kit-profile").read_text(encoding="utf-8")
    assert "omit=\n" in profile, "the explicit empty --omit must be re-recorded"


def test_unknown_omit_axis_is_rejected(tmp_path):
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", tmp_path / "r", "--omit", "bogus"],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    assert "unknown profile axis" in proc.stderr


# --- The node vocabulary (D2/R6) ----------------------------------------------


def test_node_is_a_first_class_stack_choice():
    assert "node" in boot.STACK_CHOICES
    assert "node" in boot.NON_PYTHON_STACKS
    # The all-stack kit skills must match a node scope, or a node scaffold
    # with --agents would materialize nothing.
    chosen = {n for n, _ in boot.select_skills("node", "any", False)}
    assert {"registry-hygiene", "downstream-resync", "gate-advance"} <= chosen


# --- the scaffolded OI-3 brief on the TOML carrier (repo-lock §8.1) -----------


def test_the_scaffolded_oi3_brief_is_an_append_not_a_reserialization(tmp_path):
    """`bootstrap.py` runs BEFORE the kit is copied and can import no sibling,
    so it carries its own two-line TOML emitter. Three properties, each of which
    has its own way of going silently wrong:

      * every byte the template shipped survives — an APPEND, so the registry's
        header comment and its example row are untouched (the discipline
        `set_process_key` states for `process.toml`);
      * the appended row PARSES and comes back through the real reader, so the
        keys it invents are the keys the reader maps (a brief written under an
        unmapped key renders as a brief with no text, and `check_docs` S-3 then
        reports the owner ask as briefed);
      * the file stays LF. The CSV writer this replaced defaulted to CRLF, which
        is the exact defect this migration was warned about.
    """
    carrier = load_script("spine_carrier")
    template = (KIT / "registries" / "open-items.template.toml").read_bytes()
    dest = _bootstrap(tmp_path, "--stack", "node")
    registry = dest / "docs" / "requirements" / "open-items.toml"
    raw = registry.read_bytes()

    assert raw.startswith(template), "the append rewrote what the template shipped"
    assert b"\r" not in raw, "the registry must stay LF"

    rows = {r["OI-ID"]: r for r in carrier.load(registry, "OI-ID")}
    assert "OI-3" in rows
    assert "node toolchain commands" in rows["OI-3"]["Title"]
    assert rows["OI-3"]["Status"] == "pending"
    assert rows["OI-3"]["BlastRadius"]  # the cell a reader would find empty

    # Idempotent: a re-sync must not file OI-3 twice, and must not append a
    # second table (a duplicate id is a TOML decode error, so this would show up
    # as an unreadable registry rather than a duplicate row).
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert registry.read_bytes() == raw
