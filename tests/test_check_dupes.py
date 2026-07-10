"""check_dupes.py — the opt-in duplicate-code lint (Thread 53).

The detector flags a window of >= --min-tokens consecutive significant source
tokens appearing at more than one location (copy-paste), and nothing shorter —
so a lifted helper fails while idiomatic boilerplate passes. Legitimate
repetition is recorded in docs/dupes-allow, not fought. Adapted from the proven
gilbert implementation; these tests pin the kit-facing contract: red on a seeded
copy-paste (both locations named), green on clean source, threshold tunable,
allowlist honored.
"""

from conftest import SCRIPTS, run_py

# A helper long enough (~40 significant tokens) that copy-pasting it across two
# files trips the default 30-token window.
HELPER = '''def load_rows(path, sep):
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            cells = line.rstrip("\\n").split(sep)
            if cells and cells[0]:
                rows.append(tuple(cells))
    return rows
'''

UNIQUE_A = '''def alpha_only(items):
    return [i for i in items if str(i).isalpha()]
'''

UNIQUE_B = '''def digits_only(items):
    return [i for i in items if str(i).isdigit()]
'''


def write_src(root, files):
    src = root / "src"
    src.mkdir(exist_ok=True)
    for name, body in files.items():
        (src / name).write_text(body, encoding="utf-8")
    return root


def dupes(root, *args):
    return run_py([SCRIPTS / "check_dupes.py", *args], cwd=root)


def test_clean_source_passes(tmp_path):
    write_src(tmp_path, {"a.py": UNIQUE_A, "b.py": UNIQUE_B})
    proc = dupes(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_copy_pasted_helper_fails_naming_both_locations(tmp_path):
    write_src(
        tmp_path,
        {"a.py": UNIQUE_A + HELPER, "b.py": UNIQUE_B + HELPER},
    )
    proc = dupes(tmp_path)
    assert proc.returncode == 1
    assert "duplicate block" in proc.stderr
    # One merged finding naming both file:line locations, not one per window.
    assert proc.stderr.count("duplicate block") == 1
    assert "a.py" in proc.stderr and "b.py" in proc.stderr


def test_threshold_is_tunable(tmp_path):
    # The same duplicate passes when --min-tokens is raised above its length —
    # the per-repo tuning knob (the shipped default stays 30).
    write_src(
        tmp_path,
        {"a.py": UNIQUE_A + HELPER, "b.py": UNIQUE_B + HELPER},
    )
    assert dupes(tmp_path).returncode == 1
    proc = dupes(tmp_path, "--min-tokens", "100")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_allowlist_suppresses_recorded_pair(tmp_path):
    # docs/dupes-allow records legitimate repetition by the line-number-free
    # pair form, so the allow survives the files growing/shifting.
    write_src(
        tmp_path,
        {"a.py": UNIQUE_A + HELPER, "b.py": UNIQUE_B + HELPER},
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "dupes-allow").write_text(
        "# the loader is deliberately duplicated (standalone-scripts rule)\n"
        "src/a.py == src/b.py\n",
        encoding="utf-8",
    )
    proc = dupes(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_repetition_inside_one_block_does_not_self_report(tmp_path):
    # A window repeated only *within* one physical block (same file, same
    # location) must not report against itself.
    write_src(tmp_path, {"a.py": UNIQUE_A + HELPER})
    proc = dupes(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
