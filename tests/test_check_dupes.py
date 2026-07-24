"""check_dupes.py — the opt-in duplicate-code lint (Thread 53).

The detector flags a window of >= --min-tokens consecutive significant source
tokens appearing at more than one location (copy-paste), and nothing shorter —
so a lifted helper fails while idiomatic boilerplate passes. Legitimate
repetition is recorded in docs/dupes-allow, not fought. Adapted from the proven
gilbert implementation; these tests pin the kit-facing contract: red on a seeded
copy-paste (both locations named), green on clean source, threshold tunable,
allowlist honored.

WI-276 adds fingerprinted, count-aware census entries: an exemption keys a block
by its token fingerprint plus file pair, so NEW copy-paste inside an already
listed pair is no longer waved through; --emit-census regenerates the lines.
"""

import re

from conftest import SCRIPTS, load_script, run_py

# A helper long enough (~40 significant tokens) that copy-pasting it across two
# files trips the default 30-token window.
HELPER = """def load_rows(path, sep):
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            cells = line.rstrip("\\n").split(sep)
            if cells and cells[0]:
                rows.append(tuple(cells))
    return rows
"""

UNIQUE_A = """def alpha_only(items):
    return [i for i in items if str(i).isalpha()]
"""

UNIQUE_B = """def digits_only(items):
    return [i for i in items if str(i).isdigit()]
"""

# A SECOND lifted helper, distinct from HELPER (different first window → different
# fingerprint), used to seed genuinely new copy-paste between an already-listed
# pair.
HELPER2 = """def merge_maps(base, extra):
    out = dict(base)
    for key, value in extra.items():
        if key not in out:
            out[key] = value
    return out
"""

# A helper long enough (~70 significant tokens) that its distinctive FINAL token
# lands well PAST the 30-token window. HELPER_LONG_EDITED changes only that final
# token, keeping the block's first window AND total token extent identical — the
# exact shape a first-window-plus-length fingerprint waves through (WI-276 rework).
HELPER_LONG = """def summarize(rows, label):
    total = 0
    count = 0
    for row in rows:
        total = total + row.value
        count = count + 1
    average = total / count
    return {"label": label, "sum": total, "n": count, "avg": average, "tag": "orig"}
"""

HELPER_LONG_EDITED = HELPER_LONG.replace('"orig"', '"diff"')

_FP_LINE = re.compile(r"^[0-9a-f]{12}  src/a\.py == src/b\.py$")


def write_src(root, files):
    src = root / "src"
    src.mkdir(exist_ok=True)
    for name, body in files.items():
        (src / name).write_text(body, encoding="utf-8")
    return root


def dupes(root, *args):
    return run_py([SCRIPTS / "check_dupes.py", *args], cwd=root)


def emit(root, *args):
    """`--emit-census` stdout lines (each '<fp>  a == b'), sanctionable verbatim."""
    proc = dupes(root, "--emit-census", *args)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip().splitlines()


def write_census(root, text):
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "dupes-allow").write_text(text, encoding="utf-8")


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


def test_untokenizable_file_warns_and_skips_not_crash(tmp_path):
    # A1: a lint surfaces bad input, never crashes on it — an unterminated
    # string/bracket file is warned and skipped, and the clean file still passes.
    write_src(tmp_path, {"good.py": UNIQUE_A})
    (tmp_path / "src" / "broken.py").write_text('x = (1, 2\ns = "', encoding="utf-8")
    proc = dupes(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "could not tokenize" in proc.stderr and "broken.py" in proc.stderr


def test_distinct_same_offset_blocks_report_separately(tmp_path):
    # A6: two separate duplicated regions that share a line offset (identical
    # blocks at the same position in both files, with a gap between them) must
    # report as two findings, not one merged/inflated block.
    gap = "\n".join("z{} = {}".format(i, i) for i in range(6)) + "\n"
    body = UNIQUE_A + HELPER + gap + HELPER
    write_src(tmp_path, {"a.py": body, "b.py": body.replace("alpha_only", "beta_only")})
    proc = dupes(tmp_path)
    assert proc.returncode == 1
    assert proc.stderr.count("duplicate block") >= 2


def test_repetition_inside_one_block_does_not_self_report(tmp_path):
    # A window repeated only *within* one physical block (same file, same
    # location) must not report against itself.
    write_src(tmp_path, {"a.py": UNIQUE_A + HELPER})
    proc = dupes(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_emit_census_prints_fingerprint_lines_that_round_trip(tmp_path):
    # WI-276: --emit-census prints one '<fp>  a == b' line per block, and pasting
    # them into the census turns the gate green — the regeneration workflow.
    write_src(tmp_path, {"a.py": UNIQUE_A + HELPER, "b.py": UNIQUE_B + HELPER})
    lines = emit(tmp_path)
    assert lines and all(_FP_LINE.match(ln) for ln in lines), lines
    write_census(tmp_path, "\n".join(lines) + "\n")
    proc = dupes(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_fingerprint_scoped_allow_suppresses_that_block(tmp_path):
    # A fingerprinted census line suppresses exactly its block. It also names
    # the pair, so the finding's error prints a paste-ready sanction line.
    write_src(tmp_path, {"a.py": UNIQUE_A + HELPER, "b.py": UNIQUE_B + HELPER})
    unallowed = dupes(tmp_path)
    assert unallowed.returncode == 1
    assert "sanction with census line:" in unallowed.stderr
    write_census(tmp_path, emit(tmp_path)[0] + "\n")
    assert dupes(tmp_path).returncode == 0


def test_new_copypaste_in_listed_pair_now_fails(tmp_path):
    # The core WI-276 behavior: with one block recorded by fingerprint, a NEW,
    # distinct copy-paste between the SAME already-listed pair must fail — it is
    # no longer waved through, while the recorded block stays suppressed.
    write_src(tmp_path, {"a.py": UNIQUE_A + HELPER, "b.py": UNIQUE_B + HELPER})
    write_census(tmp_path, emit(tmp_path)[0] + "\n")
    assert dupes(tmp_path).returncode == 0

    write_src(
        tmp_path,
        {
            "a.py": UNIQUE_A + HELPER + HELPER2,
            "b.py": UNIQUE_B + HELPER + HELPER2,
        },
    )
    proc = dupes(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    # Only the NEW block is reported; the recorded one is not re-flagged.
    assert proc.stderr.count("duplicate block") == 1
    assert "merge_maps" not in proc.stderr  # location, not source, is printed
    assert "sanction with census line:" in proc.stderr


def test_post_window_token_change_defeats_stale_fingerprint(tmp_path):
    # WI-276 rework: the block fingerprint hashes the COMPLETE merged token
    # sequence, not just its first --min-tokens window plus extent. Census a long
    # block, then change ONE token AFTER that first window in both files while
    # keeping the extent (token count) identical. A first-window+length hash
    # would reuse the recorded fingerprint and stay exempt (exit 0); hashing the
    # whole block must instead re-flag the edited copy (exit 1).
    write_src(
        tmp_path, {"a.py": UNIQUE_A + HELPER_LONG, "b.py": UNIQUE_B + HELPER_LONG}
    )
    write_census(tmp_path, emit(tmp_path)[0] + "\n")
    assert dupes(tmp_path).returncode == 0  # the recorded block is exempt

    write_src(
        tmp_path,
        {"a.py": UNIQUE_A + HELPER_LONG_EDITED, "b.py": UNIQUE_B + HELPER_LONG_EDITED},
    )
    proc = dupes(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "duplicate block" in proc.stderr
    # The edited block now needs its own deliberate census line.
    assert "sanction with census line:" in proc.stderr


def test_same_line_separate_blocks_do_not_share_stale_census_fingerprint(tmp_path):
    # Review regression (WI-276): two distinct 30+-token expressions can live
    # on one line and therefore share a line offset. Their sliding windows are
    # not adjacent in token space, so they must remain two blocks. Census both,
    # then edit an early interior token of only the second expression in both
    # files. A line-adjacent merge loses that token from its reconstructed
    # signature and incorrectly lets the stale census pass.
    first = " + ".join("first{}".format(i) for i in range(36))
    second = " + ".join("second{}".format(i) for i in range(36))
    body_a = "left = {}; divider_a = 1; right = {}\n".format(first, second)
    body_b = "left = {}; divider_b = 1; right = {}\n".format(first, second)
    write_src(tmp_path, {"a.py": body_a, "b.py": body_b})
    lines = emit(tmp_path)
    assert len(lines) == 2, lines
    write_census(tmp_path, "\n".join(lines) + "\n")
    assert dupes(tmp_path).returncode == 0

    # This is inside the second block's first 30-token window, where the old
    # cross-expression merge never placed it in the reconstructed signature.
    write_src(
        tmp_path,
        {
            "a.py": body_a.replace("second10", "edited10"),
            "b.py": body_b.replace("second10", "edited10"),
        },
    )
    proc = dupes(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert proc.stderr.count("duplicate block") == 1
    assert "sanction with census line:" in proc.stderr


def test_bare_pair_line_still_coarsely_allows_the_whole_pair(tmp_path):
    # Backward compatibility: a legacy bare 'a == b' line (no fingerprint) keeps
    # exempting every block in the pair, so a repo that adopted the old census
    # form does not break on upgrade.
    write_src(
        tmp_path,
        {
            "a.py": UNIQUE_A + HELPER + HELPER2,
            "b.py": UNIQUE_B + HELPER + HELPER2,
        },
    )
    assert dupes(tmp_path).returncode == 1
    write_census(tmp_path, "src/a.py == src/b.py\n")
    assert dupes(tmp_path).returncode == 0


def test_signature_keys_on_stable_token_names_not_version_ids(tmp_path):
    # Regression (WI-276): token-type INTEGERS shift across Python releases (OP
    # is 54 on 3.11, 55 on 3.12), so a fingerprint hashing them would make a
    # census generated on one interpreter fail on another — the gate job may run
    # a newer Python than a developer. The signature keys on the stable tok_name
    # string instead; guard that significant_tokens yields names, not ints.
    cd = load_script("check_dupes")
    src = tmp_path / "m.py"
    src.write_text("x = 1 + 2\n", encoding="utf-8")
    kinds = [kind for kind, _text, _line in cd.significant_tokens(str(src))]
    assert kinds and all(isinstance(k, str) for k in kinds), kinds
    assert "OP" in kinds and "NAME" in kinds  # stable names, not 54/1


def test_unallowed_is_count_aware_and_fingerprint_scoped():
    # Unit-level: two blocks that collide on one fingerprint+pair (the real
    # census carries such repeats) must each be sanctioned. One census line
    # covers one copy, so the second still fails; two lines cover both. A block
    # of a different fingerprint in the same pair is never covered by the entry.
    cd = load_script("check_dupes")
    f1 = (("src/a.py", 10), ("src/b.py", 20), 40, "abc123abc123")
    f2 = (("src/a.py", 10), ("src/b.py", 90), 40, "abc123abc123")  # same fp+pair
    one = [("abc123abc123", "src/a.py == src/b.py")]
    assert len(cd.unallowed([f1, f2], one)) == 1  # only one copy sanctioned
    assert cd.unallowed([f1, f2], one * 2) == []  # both copies sanctioned
    other = (("src/a.py", 10), ("src/b.py", 30), 40, "ffffffffffff")
    assert len(cd.unallowed([other], one)) == 1  # different fp: not covered
    # A legacy bare-pair entry covers any block in the pair and is not consumed.
    assert cd.unallowed([f1, f2, other], [(None, "src/a.py == src/b.py")]) == []
