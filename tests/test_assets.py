"""trace.py's optional binary/large-asset provenance registry (WI-1.7,
process-options.md "Binary assets"): ASSET-### rows live off the SN->SR->LLR->TC
spine and record the facts *about* an unavoidably-binary asset (art, music,
voice, video) that can't be diffed — provenance (human/AI, for Steam-style
AI-content disclosure), license, attribution, contract/release link, and a
pointer + hash. Like PART, trace.py integrity-checks the ASSET- id only. The
registry is optional: an absent file is a no-op and the bootstrapped ASSET-000
placeholder never blocks a gate.
"""

from conftest import make_minimal_project, run_py

ASSET_HEADER = (
    "ASSET-ID,Name,Refs,Kind,Provenance,License,Attribution,"
    "ContractRef,Location,Hash,Version,Notes\n"
)
ROW = (
    "{aid},Hero art,SR-001,image,ai-generated,proprietary,"
    "credit studio,contracts/x.pdf,lfs:art/hero.png,sha256:abc,v1,note\n"
)


def asset_path(root):
    return root / "docs" / "requirements" / "assets.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_assets(root, *rows):
    asset_path(root).write_text(ASSET_HEADER + "".join(rows), encoding="utf-8")


def test_clean_asset_row_passes(scaffold):
    make_minimal_project(scaffold)
    write_assets(scaffold, ROW.format(aid="ASSET-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "assets=1" in proc.stdout
    assert "Binary assets (process-options.md)" in report_of(scaffold)


def test_malformed_asset_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_assets(scaffold, ROW.format(aid="ASSET-XX"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ASSET id 'ASSET-XX' is malformed" in report_of(scaffold)


def test_duplicate_asset_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_assets(
        scaffold,
        ROW.format(aid="ASSET-001"),
        ROW.format(aid="ASSET-001"),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ASSET id ASSET-001 is duplicated" in report_of(scaffold)


def test_placeholder_asset_registry_is_inert(scaffold):
    # The bootstrapped ASSET-000 placeholder must never block a gate for a project
    # with no binary assets (same stance as procurement/PB): it survives even
    # --no-placeholders, which the spine does not.
    make_minimal_project(scaffold)
    assert asset_path(scaffold).exists()  # bootstrap laid down the registry
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "assets=" not in proc.stdout
