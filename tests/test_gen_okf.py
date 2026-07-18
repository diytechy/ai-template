"""gen_okf.py — the OKF knowledge-bundle export (Thread 48).

The bundle is a generated view, never a parallel source of truth: what matters
is that it is deterministic (byte-stable --check), complete (one concept per
real registry row, frontmatter typed, graph links resolving), self-pruning
(a deleted row's file goes away; a stray hand-added file reads as stale), and
free for non-adopters (placeholder-only registries are vacuous; docs/okf-export
`off` silences). Exercised over the conftest minimal project.
"""

from conftest import SCRIPTS, make_minimal_project, run_py


def okf(root, *args):
    return run_py([SCRIPTS / "gen_okf.py", *args], cwd=root)


def bundle(root):
    return root / "docs" / "okf"


def test_bundle_generates_typed_linked_concepts(scaffold):
    make_minimal_project(scaffold)
    proc = okf(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    sr = (bundle(scaffold) / "system-requirements" / "SR-001.md").read_text(
        encoding="utf-8"
    )
    assert sr.startswith("---\n")
    assert 'type: "System Requirement"' in sr
    assert 'resource: "docs/requirements/system-requirements.csv (SR-001)"' in sr
    # The graph as markdown links: up to the SN, down to LLR and TC.
    assert "[SN-001](../stakeholder-needs/SN-001.md)" in sr
    assert "[LLR-001](../low-level-requirements/LLR-001.md)" in sr
    assert "[TC-001](../test-cases/TC-001.md)" in sr
    # Progressive disclosure + the spec pin.
    index = (bundle(scaffold) / "index.md").read_text(encoding="utf-8")
    assert "[system-requirements](system-requirements/index.md)" in index
    assert (bundle(scaffold) / "UPSTREAM.md").exists()
    # No wall-clock anywhere: determinism is the freshness gate's foundation.
    assert "timestamp" not in sr


def test_generation_is_deterministic_and_check_gates_staleness(scaffold):
    make_minimal_project(scaffold)
    assert okf(scaffold).returncode == 0
    sr_file = bundle(scaffold) / "system-requirements" / "SR-001.md"
    first = sr_file.read_bytes()
    again = okf(scaffold)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert sr_file.read_bytes() == first
    assert okf(scaffold, "--check").returncode == 0
    # Edit a registry without regenerating -> stale, named actionably.
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace("Addition", "Summation"),
        encoding="utf-8",
    )
    stale = okf(scaffold, "--check")
    assert stale.returncode == 1 and "STALE" in stale.stderr
    assert okf(scaffold).returncode == 0
    assert okf(scaffold, "--check").returncode == 0


def test_write_mode_prunes_and_check_flags_extras(scaffold):
    # A hand-added file inside the generated bundle is drift: --check flags it,
    # the write mode prunes it (the bundle is never hand-maintained).
    make_minimal_project(scaffold)
    assert okf(scaffold).returncode == 0
    stray = bundle(scaffold) / "hand-edited.md"
    stray.write_text("not generated\n", encoding="utf-8")
    assert okf(scaffold, "--check").returncode == 1
    assert okf(scaffold).returncode == 0
    assert not stray.exists()


def test_placeholder_only_scaffold_is_vacuous(scaffold):
    # The fresh scaffold carries only -000 rows: nothing is emitted and --check
    # passes out of the box (the ruled fresh-scaffold-green requirement).
    proc = okf(scaffold, "--check")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "vacuously clean" in proc.stdout
    assert not bundle(scaffold).exists()


def test_opt_out_silences(scaffold):
    # `off` short-circuits before any generation or comparison — even a stale
    # (here: registry-edited) bundle no longer gates, and nothing is written.
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace("Addition", "Summation"),
        encoding="utf-8",
    )
    (scaffold / "docs" / "okf-export").write_text("off\n", encoding="utf-8")
    proc = okf(scaffold, "--check")
    assert proc.returncode == 0 and "off" in proc.stdout


def test_process_guides_emit_with_derived_summaries(scaffold):
    # Layer B2: a real-spine repo also gets Process Guide concepts for its
    # process docs — typed, resource-linked, the summary DERIVED from the doc
    # (not hand-authored), the source left untouched.
    make_minimal_project(scaffold)
    proc = okf(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    guide = bundle(scaffold) / "process-guides" / "architecture.md"
    assert guide.exists()
    text = guide.read_text(encoding="utf-8")
    assert 'type: "Process Guide"' in text
    assert 'resource: "docs/architecture.md"' in text
    assert (
        "[docs/architecture.md](../../../docs/architecture.md)" in text
    )  # source link
    # The summary is the doc's own first prose line, proving derivation.
    arch = scaffold / "docs" / "architecture.md"
    first_prose = next(
        ln.strip()
        for ln in arch.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith(("#", "|", "<!--", "-", ">", "`"))
    )
    assert first_prose[:40] in text
    # The root index lists the new tier; the source doc is unmodified (B1 not B2).
    assert "process-guides" in (bundle(scaffold) / "index.md").read_text(
        encoding="utf-8"
    )
    assert "type:" not in arch.read_text(encoding="utf-8").splitlines()[0]


def test_process_guides_skip_absent_docs(scaffold):
    # A doc a given repo doesn't carry is skipped (like the off-spine tiers), so
    # the shipped candidate list is generous without minting dangling concepts.
    make_minimal_project(scaffold)
    assert not (scaffold / "docs" / "plan.md").exists() or True
    assert okf(scaffold).returncode == 0
    # docs/interfaces.md is not a scaffolded doc -> no such guide.
    assert not (bundle(scaffold) / "process-guides" / "interfaces.md").exists()


def test_process_guides_absent_on_vacuous_scaffold(scaffold):
    # The vacuity gate: process docs exist in a fresh scaffold, but with only
    # placeholder registries nothing is emitted at all — so fresh-scaffold-green
    # and the zero-cost opt-out hold (guides ride the real-spine gate).
    proc = okf(scaffold, "--check")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not bundle(scaffold).exists()


def test_malformed_id_is_ignored_not_path_escape(scaffold):
    # A4: an id that isn't PREFIX-<digits> (a crafted traversal id) is not
    # turned into a path component — it's simply skipped, like trace.py's
    # integrity rule. The real rows still export.
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8")
        + 'SR-/../../evil,Bad,SN-001,"x",R,"y",,M,Test,Verified\n',
        encoding="utf-8",
    )
    proc = okf(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (bundle(scaffold) / "system-requirements" / "SR-001.md").exists()
    assert not (scaffold / "docs" / "evil.md").exists()


def test_prune_removes_emptied_tier_directory(scaffold):
    # A7: deleting the last row of a tier leaves no empty directory behind.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "interfaces.csv").write_text(
        "IF-ID,Name,Contract,Status\nIF-001,Seam,contract text,Verified\n",
        encoding="utf-8",
    )
    assert okf(scaffold).returncode == 0
    assert (bundle(scaffold) / "interfaces").is_dir()
    (req / "interfaces.csv").write_text(
        "IF-ID,Name,Contract,Status\n", encoding="utf-8"
    )
    assert okf(scaffold).returncode == 0
    assert not (bundle(scaffold) / "interfaces").exists()


def test_generated_banner_on_every_file_type(scaffold):
    # WI-066: every emitted file self-identifies as a generated reference copy
    # with a one-line, source-slotted GENERATED banner immediately after the
    # frontmatter (or first, in the frontmatter-less UPSTREAM.md).
    make_minimal_project(scaffold)
    assert okf(scaffold).returncode == 0
    b = bundle(scaffold)
    lead = "> **GENERATED — a reference copy, not the source of truth.**"

    # A concept file: banner right after the frontmatter, naming its exact source.
    sr = (b / "system-requirements" / "SR-001.md").read_text(encoding="utf-8")
    lines = sr.splitlines()
    close = lines.index("---", 1)  # the closing frontmatter fence
    assert lines[close + 1].startswith(lead)
    assert "docs/requirements/system-requirements.csv (SR-001)" in lines[close + 1]
    assert "docs/okf-export: off silences the layer" in lines[close + 1]
    assert lines[close + 2] == ""  # blank line before the heading
    assert lines[close + 3].startswith("# SR-001")

    # A tier index names its tier's registry.
    idx = (b / "system-requirements" / "index.md").read_text(encoding="utf-8")
    head = idx.split("\n# ")[0]
    assert lead in head
    assert "docs/requirements/system-requirements.csv" in head

    # The root index states it exactly once (the old routing prose is absorbed).
    root = (b / "index.md").read_text(encoding="utf-8")
    assert root.count(lead) == 1
    assert "the spine registries and the process docs" in root
    assert "Generated from the spine registries" not in root

    # A process guide names the summarized source doc.
    guide = (b / "process-guides" / "architecture.md").read_text(encoding="utf-8")
    assert "Derived from docs/architecture.md by scripts/gen_okf.py" in guide

    # UPSTREAM has no frontmatter: the banner is its first line, stated once.
    up = (b / "UPSTREAM.md").read_text(encoding="utf-8")
    assert up.splitlines()[0].startswith(lead)
    assert up.count(lead) == 1

    # The banner introduces no clock, and the bundle stays byte-stable under --check.
    assert "timestamp" not in sr
    assert okf(scaffold, "--check").returncode == 0


def test_okf_step_wired_at_g3(scaffold):
    # The harness carries the freshness gate like arch-map/trajectory-map.
    from conftest import load_script

    check = load_script("check")
    allg = check.steps(80, "full", "all")
    cmd = next(s[2] for s in allg if s[0] == "okf")
    assert any("gen_okf.py" in str(t) for t in cmd) and "--check" in cmd
    gates = next(s[3] for s in allg if s[0] == "okf")
    assert gates == {"G3"}
