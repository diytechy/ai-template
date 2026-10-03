"""The tree helpers the baseline-snapshot suites share.

Moved verbatim out of `tests/test_baseline_snapshot.py` when its in-process drift
corners split out to `tests/test_baseline_drift.py`: both modules build the same
tmp tree from this repository's real registries. No `test_` prefix, so it is
never collected.
"""

import re
import shutil

from conftest import ROOT, load_script

SNAP = load_script("baseline_snapshot")
SR_REL = "docs/requirements/system-requirements.toml"


def _tree(tmp_path):
    """A tmp repo carrying this repo's seven real registries at their real
    paths. SR, LLR and TC statuses start Approved so tests plant their own
    maturity moves instead of depending on the live spine's approval progress.
    Everything resolves off `root`, so nothing else needs to come along."""
    root = tmp_path / "repo"
    for rel in SNAP.SNAPSHOTTED:
        src = ROOT / rel
        if not src.is_file():
            continue
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        if rel in (
            SR_REL,
            "docs/requirements/low-level-requirements.toml",
            "docs/test/test-cases.toml",
        ):
            dest.write_bytes(
                re.sub(
                    rb'(?m)^status = "[^"]+"',
                    b'status = "Approved"',
                    dest.read_bytes(),
                )
            )
    return root


def _seeded(tmp_path):
    """`_tree` plus its first snapshot — the post-signing steady state every
    reader test starts from."""
    root = _tree(tmp_path)
    SNAP.copy_live(root, seed=True)
    return root


def _rewrite(root, rel, old, new):
    """One substring edit to a live registry, asserted to have actually
    changed something — a fixture that silently matched nothing would make
    every assertion below vacuously true.

    ON BYTES, NOT TEXT (2026-08-20). `Path.write_text` translates `\\n` to
    `os.linesep`, so on Windows this "one substring edit" rewrote every line
    ending in the file and git saw the WHOLE registry change — which is the same
    fixture-CRLF class WI-465 swept, and it silently defeats any assertion about
    WHAT a commit touched (it fooled the status-cell pickaxe into reporting a
    traced-only commit as an approval). Bytes in, bytes out, endings untouched."""
    path = root / rel
    data = path.read_bytes()
    assert old.encode("utf-8") in data, "fixture substring not found: " + old
    path.write_bytes(data.replace(old.encode("utf-8"), new.encode("utf-8"), 1))


def _first_row_at(root, status, exclude=()):
    """`(id, row)` of the first SR carrying `status`, from the LIVE tree."""
    spine_carrier = load_script("spine_carrier")
    for row in spine_carrier.load(root / SR_REL, "SR-ID", keep_examples=False):
        if (row.get("Status") or "").strip().lower() == status and row[
            "SR-ID"
        ] not in exclude:
            return row["SR-ID"], row
    raise AssertionError("no SR at status " + status + " in the fixture")
