"""check_doc_refs.py — dangling path/symbol references in prose (Thread 49).

False-positive control is the design center: only path-shaped backticked
tokens and the explicit `sym:` convention are validated — never every
backticked word. Warn-first (exit 0) unless --strict; the sym: tier skips
cleanly without a module-map inventory. Exercised over temp repos.
"""

from conftest import SCRIPTS, load_script, run_py

ARCH = """# Architecture

<!-- BEGIN GENERATED MODULE MAP -->
### `src/demo`
_Demo module._

| Public item | Summary | Implements |
|---|---|---|
| `add(a, b)` | Adds. |  |
| `sub(a, b)` | Subtracts. |  |
<!-- END GENERATED MODULE MAP -->
"""


def make_repo(root, body, with_arch=True):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(body, encoding="utf-8")
    if with_arch:
        (root / "docs" / "architecture.md").write_text(ARCH, encoding="utf-8")
    (root / "scripts").mkdir(exist_ok=True)
    # `load`/`save` are the names the spine fixtures' LLR CodeSymbol cites, and
    # they are DEFINED here so those rows are FOUNDED under the WI-429 anchor
    # rule: a fixture whose LLR names code that does not exist would make every
    # registry-tier test convict for the wrong reason.
    (root / "scripts" / "real.py").write_text(
        "x = 1\n\n\ndef load():\n    pass\n\n\ndef save():\n    pass\n",
        encoding="utf-8",
    )
    return root


def refs(root, *args):
    return run_py([SCRIPTS / "check_doc_refs.py", *args], cwd=root)


def test_existing_path_and_symbol_pass(tmp_path):
    make_repo(tmp_path, "See `scripts/real.py` and sym:demo.add for the core.\n")
    proc = refs(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_dangling_path_warns_then_gates_under_strict(tmp_path):
    make_repo(tmp_path, "The old `scripts/deleted.py` did this.\n")
    proc = refs(tmp_path)
    assert proc.returncode == 0, "warn-first: findings must not gate by default"
    assert "scripts/deleted.py" in proc.stderr
    strict = refs(tmp_path, "--strict")
    assert strict.returncode == 1


def test_non_path_backticks_urls_and_globs_are_ignored(tmp_path):
    make_repo(
        tmp_path,
        "Use `off` or `type`; see `https://example.com/a.py` and "
        "`scripts/*.py` and `docs/{name}.md` shapes.\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_path_ok_line_is_exempt(tmp_path):
    make_repo(
        tmp_path,
        "A downstream repo gets `scripts/not-here.py` <!-- path-ok -->\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_dangling_symbol_is_flagged_against_the_inventory(tmp_path):
    make_repo(tmp_path, "Call sym:demo.multiply to combine.\n")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "multiply" in proc.stderr and "public inventory" in proc.stderr


def test_unknown_module_is_flagged(tmp_path):
    make_repo(tmp_path, "See sym:ghost.add.\n")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "not in the module map" in proc.stderr


def test_node_id_file_half_is_judged_and_joined_lists_stay_out_of_scope(tmp_path):
    # WI-394 (owner ruling R2 2026-08-01, option (c)) RE-SCOPED the A2-era `::`
    # guard this test used to pin: a pytest node id — the kit's sanctioned
    # Evidence form — is a real FILE plus a selector, so the FILE half is now
    # judged like any path. `;`/`,`-joined lists keep their exclusion
    # (false-positive control, unchanged), even when one half is dead.
    make_repo(
        tmp_path,
        "Evidence `tests/real.py::test_it` and `tests/nowhere.py;scripts/real.py`.\n",
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "real.py").write_text("x = 1\n", encoding="utf-8")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_an_invented_node_id_citation_gates_on_its_file_half(tmp_path):
    # The invented-citation case WI-394 was filed on: warn-first by default
    # (the WI-062 precedent), red under --strict, and the finding quotes the
    # token AS WRITTEN so a reader can find it in the doc.
    make_repo(tmp_path, "Evidence `tests/never_written.py::test_invented`.\n")
    proc = refs(tmp_path)
    assert proc.returncode == 0, "warn-first: findings must not gate by default"
    assert "`tests/never_written.py::test_invented` does not exist" in proc.stderr
    assert refs(tmp_path, "--strict").returncode == 1


def test_the_node_selector_half_is_ruled_prose_never_validated(tmp_path):
    # The other half of ruling (c), pinned so nobody reads coverage into it: a
    # selector naming a test the LIVE file does not define stays clean. A
    # renamed-but-present node is an ACCEPTED gap, recorded in
    # docs/enforcement-audit.md — not a promise waiting on a better oracle.
    make_repo(tmp_path, "Evidence `scripts/real.py::test_no_such_node`.\n")
    assert refs(tmp_path, "--strict").returncode == 0


def test_a_path_ok_marked_node_id_quotation_is_exempt(tmp_path):
    # The plan/spec quote invented citations AS EVIDENCE, marked `path-ok`; the
    # re-scoped guard must not convict the marked quotations (the same per-line
    # exemption the path tier has always honored).
    make_repo(
        tmp_path,
        "Quoted: `tests/never.py::test_x` <!-- path-ok: driven evidence -->\n",
    )
    assert refs(tmp_path, "--strict").returncode == 0


def test_generated_linguist_tree_is_not_linted(tmp_path):
    # A2: a dir marked linguist-generated in .gitattributes (e.g. docs/okf/) is
    # the generator's output — never hand-authored prose — so it is skipped,
    # even when it names a path that doesn't exist here.
    make_repo(tmp_path, "clean root doc\n")
    (tmp_path / ".gitattributes").write_text(
        "docs/okf/** linguist-generated=true -diff\n", encoding="utf-8"
    )
    gen = tmp_path / "docs" / "okf"
    gen.mkdir(parents=True)
    (gen / "SR-001.md").write_text(
        "**Evidence.** `tests/gone.py::test_x`\nalso `scripts/gone.py`\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- WI-062: UNTRACED vs DANGLING ---------------------------------------------
# A path that isn't on disk is not automatically rot. Before the split this repo
# reported 561 findings, 534 of them explainable — and noise is how a real broken
# link hides. Each tier below classifies by a REASON, never by a suppression
# list, so the untraced count stays a number you can watch.


def test_kit_relative_path_is_untraced_not_dangling(tmp_path):
    # A kit's prose addresses its portable unit by the paths an ADOPTING repo
    # will have after copy-in, so `scripts/check.py` is right for its reader even
    # though this repo keeps it under project-trajectory/.
    make_repo(tmp_path, "Wire `scripts/check.py` into CI.\n")
    kit = tmp_path / "project-trajectory" / "scripts"
    kit.mkdir(parents=True)
    (kit / "check.py").write_text("x = 1\n", encoding="utf-8")

    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, "a kit-relative path must not gate"
    assert "scripts/check.py does not exist" not in proc.stderr
    assert "1 untraced" in proc.stdout
    listed = refs(tmp_path, "--show-untraced")
    assert "UNTRACED" in listed.stderr and "kit-relative" in listed.stderr

    # ...and the classification is a REASON, not a blanket pass: the same token
    # with no such file anywhere is still dangling.
    (kit / "check.py").unlink()
    assert refs(tmp_path, "--strict").returncode == 1


def test_record_surface_path_is_untraced_not_dangling(tmp_path):
    # A session log naming a since-retired file is accurate history. "Fixing" it
    # would falsify the record, so it can never be a gating finding.
    make_repo(tmp_path, "Nothing here.\n")
    (tmp_path / "docs" / "log.md").write_text(
        "2026-01-01 — retired `docs/next-wi` in favour of the scheduler.\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 untraced" in proc.stdout
    listed = refs(tmp_path, "--show-untraced")
    assert "record surface" in listed.stderr

    # The SAME token in a LIVE doc still gates — the tier keys on the surface,
    # not on the token, so retired-file rot in live prose stays visible.
    (tmp_path / "README.md").write_text("Set `docs/next-wi`.\n", encoding="utf-8")
    assert refs(tmp_path, "--strict").returncode == 1


def test_untraced_count_is_always_reported_even_when_silent(tmp_path):
    # A classification whose size you cannot see is a suppression list. The count
    # prints on stdout whether or not the list is shown.
    make_repo(tmp_path, "Nothing here.\n")
    (tmp_path / "docs" / "log.md").write_text(
        "`docs/gone-a` and `docs/gone-b` were retired.\n", encoding="utf-8"
    )
    proc = refs(tmp_path)
    assert "2 untraced" in proc.stdout
    assert "UNTRACED" not in proc.stderr, "silent by default"


def test_placeholder_and_anchored_shapes_are_not_paths(tmp_path):
    # `WI-###`/`NNN` are FORMS ("your id here") and `…` is "and the rest"; an
    # anchored doc reference is a LINK, which is check_docs.py's job.
    make_repo(
        tmp_path,
        "Name it `docs/specs/WI-###.md`, file `docs/reviews/NNN-AUDIT.md`, "
        "see `docs/…` and `docs/specs/my-effort.md#s1--first-slice`.\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "untraced" not in proc.stdout, "these are not paths at all, not excuses"


def test_symbol_tier_skips_without_inventory(tmp_path):
    # A files-mode / non-Python stack has no symbol inventory: the sym: tier
    # skips with a note, and the path tier still runs.
    make_repo(tmp_path, "Call sym:demo.add; also `scripts/real.py`.\n", with_arch=False)
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipped" in proc.stdout


def test_declared_absence_is_untraced_with_its_own_reason(tmp_path):
    # WI-308's third untraced reason: a repo may DECLARE, with a reason, the
    # paths it deliberately does not carry — an opt-in registry it never
    # enabled, a policy file whose absence IS the documented default. Prose
    # naming one is correct for its reader, exactly like a kit-relative path.
    make_repo(tmp_path, "Set `docs/review-cadence` to change it; see `docs/nope.md`.\n")
    (tmp_path / "docs" / "declared-absences").write_text(
        "# why each is missing\n"
        "docs/review-cadence — absent = `slice`, the default cadence\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict", "--show-untraced")
    # the declared one is reclassified, WITH the declared reason quoted back...
    assert "docs/review-cadence" in proc.stderr
    assert "absent = `slice`, the default cadence" in proc.stderr
    assert "UNTRACED" in proc.stderr
    # ...and the undeclared one on the SAME line still gates: this is a
    # classification, not a blanket exemption for the file or the line.
    assert proc.returncode == 1
    assert "docs/nope.md` does not exist" in proc.stderr


def test_absences_file_absent_or_malformed_never_silences(tmp_path):
    # Degrade in the safe direction. No file at all, and a file whose line
    # carries no separator, must both leave the path DANGLING — a reader that
    # guessed at a malformed entry would silence real rot.
    make_repo(tmp_path, "See `docs/review-cadence`.\n")
    assert refs(tmp_path, "--strict").returncode == 1, "no file: still rot"
    (tmp_path / "docs" / "declared-absences").write_text(
        "docs/review-cadence\n", encoding="utf-8"
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1, "a line with no reason declares nothing"
    assert "docs/review-cadence` does not exist" in proc.stderr


# --- WI-396: a LINE-SUFFIXED citation is the path it names --------------------
# `docs/x.md:40-41` defeated the extension test, so every suffixed token fell to
# PATH_PREFIXES — the DOWNSTREAM layout — and a suffixed reference into the kit's
# own `project-trajectory/` tree reached NO bucket: not dangling, not untraced,
# never classified. The suffix is now stripped before the shape test AND before
# the stat, so the two byte-identical halves of a dogfooded pair reach the same
# NAMED verdict: BOTH CLEAN.

KIT_HALF = "project-trajectory/work/WI-000.template.md"
DOCS_HALF = "docs/work/queued/WI-000-example.md"
SUFFIX = ":40-41"


def pair_repo(root, suffix=SUFFIX):
    """The dogfooded pair: byte-identical files under the kit tree and under
    docs/, cited in one sentence of live prose with the same line suffix."""
    make_repo(
        root,
        "Two halves: `{}{}` and `{}{}`.\n".format(KIT_HALF, suffix, DOCS_HALF, suffix),
    )
    for half in (KIT_HALF, DOCS_HALF):
        p = root / half
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("same bytes\n", encoding="utf-8")
    return root


def verdict(proc, token):
    """The token's NAMED outcome — the row's DONE-WHEN is about which bucket it
    lands in, not merely about whether the two agree."""
    if "`{}` does not exist".format(token) in proc.stderr:
        return "DANGLING"
    if "UNTRACED - " in proc.stderr and "`{}` —".format(token) in proc.stderr:
        return "UNTRACED"
    return "CLEAN"


def test_a_suffixed_pair_reaches_the_same_named_verdict_both_clean(tmp_path):
    proc = refs(pair_repo(tmp_path), "--strict", "--show-untraced")
    assert verdict(proc, KIT_HALF + SUFFIX) == "CLEAN"
    assert verdict(proc, DOCS_HALF + SUFFIX) == "CLEAN"
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # CLEAN because both RESOLVE, not because either was excused: an untraced
    # count here would mean the kit half passed as "kit-relative" instead.
    assert "untraced" not in proc.stdout, proc.stdout


def test_the_suffixed_pair_diverges_when_either_half_is_broken(tmp_path):
    # The mutation twin (WI-353 discipline). Equality alone cannot FAIL if the
    # tool stops examining a half — which is precisely the defect — so break each
    # half in turn and assert the pair DIVERGES. Both directions, because a rule
    # that looked at only one side would still pass a single-sided mutation.
    for i, (broken, intact) in enumerate(
        ((KIT_HALF, DOCS_HALF), (DOCS_HALF, KIT_HALF))
    ):
        root = pair_repo(tmp_path / "case{}".format(i))
        (root / broken).unlink()
        proc = refs(root, "--strict", "--show-untraced")
        assert verdict(proc, broken + SUFFIX) == "DANGLING", proc.stderr
        assert verdict(proc, intact + SUFFIX) == "CLEAN", proc.stderr
        assert proc.returncode == 1


def test_a_suffixed_citation_to_a_missing_file_still_gates(tmp_path):
    # Stripping the suffix is not a free pass for suffixed tokens (the shape the
    # "suffixed is never a path" alternative would have taken), and the finding
    # quotes the token AS WRITTEN so it can be found in the doc.
    make_repo(tmp_path, "The old `scripts/deleted.py:40` did this.\n")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "`scripts/deleted.py:40` does not exist" in proc.stderr


def test_only_an_all_digit_trailing_suffix_is_stripped(tmp_path):
    # `:40`/`:40-41` are line citations; anything else is part of the path, and
    # a real file whose name contains a colon must still resolve.
    make_repo(tmp_path, "See `scripts/real.py:40` and `scripts/real.py:40-41`.\n")
    assert refs(tmp_path, "--strict").returncode == 0
    make_repo(tmp_path, "See `scripts/real.py:head`.\n")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1, "`:head` is not a line suffix — the token stands"
    assert "`scripts/real.py:head` does not exist" in proc.stderr


def test_declared_absences_is_a_declaration_not_a_suppression_list(tmp_path):
    # The count is still reported, so the size of the class stays visible — the
    # same honesty rule WI-062 applied to the kit-relative and record reasons.
    make_repo(tmp_path, "See `docs/a-thing.md` and `docs/other-thing.md`.\n")
    (tmp_path / "docs" / "declared-absences").write_text(
        "docs/a-thing.md — opt-in layer this repo never enabled\n"
        "docs/other-thing.md — likewise\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0
    assert "2 untraced" in proc.stdout
    assert "declared absent" in proc.stdout


# --- WI-394 ruling (c): the REGISTRY tier -------------------------------------
# The markdown tiers never see the CSVs, yet the spine's Evidence-class cells
# (TC `Evidence`; LLR `Module`/`CodeSymbol`/`TestRefs`) are exactly the pointers
# that carry the spine's claim to be grounded in the code. The FILE half of each
# citation must exist; the `::node` selector is ruled PROSE (accepted gap). The
# tier's absence-skip needs no test of its own: every fixture above runs the tool
# without the registries and stays green.

TC_HEADER = "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status,Phase\n"
LLR_HEADER = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,Rationale,TestRefs,Status,Component,Phase\n"


def spine_repo(root, evidence, module="scripts/real.py", symbol="load/save"):
    """A repo whose spine has one TC row (Evidence as given) and one LLR row."""
    make_repo(root, "clean doc\n")
    (root / "docs" / "test").mkdir(parents=True)
    (root / "docs" / "requirements").mkdir(parents=True)
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TC_HEADER
        + "TC-001,SR-001,Unit,run it,Full,,ok,Yes,{},Verified,1\n".format(evidence),
        encoding="utf-8",
    )
    (root / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLR_HEADER
        + "LLR-001,SR-001,T,{},{},detail,,(see TC-001),Verified,,1\n".format(
            module, symbol
        ),
        encoding="utf-8",
    )
    return root


def test_registry_citations_whose_files_exist_pass(tmp_path):
    # Both node ids cite selectors the file does not define — clean, because the
    # selector half is prose under ruling (c); only the FILE half is judged.
    spine_repo(tmp_path, "tests/real.py::test_a;tests/real.py::test_b")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "real.py").write_text("x = 1\n", encoding="utf-8")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_an_invented_registry_evidence_citation_reds_under_strict(tmp_path):
    # The WI-394 finding itself: an Automated=Yes / Status=Verified row citing
    # a file that has never existed. Warn-first names the row and the column.
    spine_repo(tmp_path, "tests/never_existed.py::test_invented")
    proc = refs(tmp_path)
    assert proc.returncode == 0, "warn-first, the WI-062 precedent"
    assert "TC-001 Evidence" in proc.stderr
    assert "`tests/never_existed.py::test_invented` does not exist" in proc.stderr
    assert refs(tmp_path, "--strict").returncode == 1


def test_registry_joined_module_list_is_split_and_judged_per_half(tmp_path):
    # A registry cell is a KNOWN joined list — unlike a prose token, the joiner
    # is a separator, not an out-of-scope marker. Only the dead half convicts.
    spine_repo(tmp_path, "scripts/real.py", module="scripts/real.py;scripts/gone.py")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "LLR-001 Module" in proc.stderr
    assert "`scripts/gone.py` does not exist" in proc.stderr
    assert "`scripts/real.py`" not in proc.stderr


def test_registry_placeholder_rows_and_symbol_joins_stay_out_of_scope(tmp_path):
    # `*-000` example rows keep the scaffolded templates copy-ready, and a
    # CodeSymbol's `/`-joined symbol names are not paths — neither may convict.
    # `load/save` is the `/`-joined shape under test: two symbol names, not a
    # path — the joiner must keep it out of the PATH tier entirely.
    spine_repo(tmp_path, "scripts/real.py", symbol="load/save")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        TC_HEADER
        + "TC-000,SR-000,Unit,example,Full,,ok,Yes,tests/nope.py::test_x,Planned,1\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- the LLR CodeSymbol ANCHOR rule (WI-429) ---------------------------------
# The discharge test D-9 leaves open for the LLR tier: `Status = Founded` means
# the artifacts a row calls for EXIST, and an LLR has no children here, so its
# discharge is resolving code. The rule is an ANCHOR — at least one
# identifier-shaped CodeSymbol token must bind in a named `.py` Module — for
# the reason the census established: the cell has no stated grammar and really
# does carry locals, attributes, CSS tokens and prose, so a per-token rule
# would red 31 of this repo's 149 live rows on arrival.


def test_llr_symbol_anchor_reds_on_a_planted_defect(tmp_path):
    # NON-VACUITY, planted: a real module and a real LLR naming a real symbol
    # is silent; the same fixture plus one row naming a symbol nothing defines
    # is a DANGLING finding that gates under --strict.
    spine_repo(tmp_path, "scripts/real.py")
    assert refs(tmp_path, "--strict").returncode == 0, "the founded row is silent"
    llr = tmp_path / "docs" / "requirements" / "low-level-requirements.csv"
    llr.write_text(
        llr.read_text(encoding="utf-8")
        + "LLR-901,SR-001,Planted,scripts/real.py,no_such_symbol_anywhere,"
        "detail,,(see TC-001),Verified,,1\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path)
    assert proc.returncode == 0, "warn-first, the WI-062 precedent"
    assert "LLR-901 CodeSymbol" in proc.stderr
    assert "no_such_symbol_anywhere" in proc.stderr
    assert "LLR-001" not in proc.stderr, "the founded row must not be swept in"
    assert refs(tmp_path, "--strict").returncode == 1


def test_llr_symbol_anchor_needs_only_one_resolving_token(tmp_path):
    # The anchor, stated as a test: a cell whose OTHER members are a local, a
    # CSS custom property and free prose is still founded on its one real
    # symbol — and the misses are COUNTED as untraced, never silently dropped.
    spine_repo(tmp_path, "scripts/real.py", symbol="load/a_local_name/--nhead")
    proc = refs(tmp_path, "--strict", "--show-untraced")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "a_local_name" in proc.stderr, "the miss is reported"
    assert "UNTRACED" in proc.stderr, "...as untraced, not as a gate"


def _nonpy_repo(root, module="hooks/pre-commit"):
    """A spine whose one LLR names only a non-Python module, on disk."""
    spine_repo(root, "scripts/real.py", module=module, symbol="pre-commit")
    (root / "hooks").mkdir(exist_ok=True)
    (root / "hooks" / "pre-commit").write_text("#!/bin/sh\n", encoding="utf-8")
    return root


def test_llr_symbol_anchor_skips_a_non_python_module(tmp_path):
    # A hook or a shell template has no Python name to bind, so the rule has
    # nothing to say — it must skip, not convict.
    _nonpy_repo(tmp_path)
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_llr_symbol_anchor_reports_the_non_python_skip_as_an_advisory(tmp_path):
    # WI-449 / OI-20's OI-28 guard: the skip is CORRECT and unchanged, but it
    # used to be SILENT, which is a fail-open now that template paths are ruled
    # admissible in Module as realization artifacts. The row must be named,
    # with its module and the reason discharge is not computed for it.
    _nonpy_repo(tmp_path)
    proc = refs(tmp_path)
    assert "ADVISORY" in proc.stderr, proc.stdout + proc.stderr
    assert "LLR-001" in proc.stderr
    assert "hooks/pre-commit" in proc.stderr
    assert "NOT computed" in proc.stderr
    # ...and it is NEVER the exit code, not even under --strict, and never a
    # WARN (which in this module is exactly the ink that gates under --strict).
    strict = refs(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert "ADVISORY" in strict.stderr
    assert "LLR-001 CodeSymbol" not in strict.stderr, "an advisory is not a finding"


def test_llr_symbol_anchor_binds_through_the_py_half_of_a_mixed_module_cell(tmp_path):
    # A row naming BOTH a hook and a `.py` module is checkable through its `.py`
    # half, so the rule runs normally: it founds on the binding token and stays
    # silent. The advisory is for rows with NO Python module at all.
    spine_repo(
        tmp_path,
        "scripts/real.py",
        module="scripts/real.py;hooks/pre-commit",
        symbol="load",
    )
    (tmp_path / "hooks").mkdir()
    (tmp_path / "hooks" / "pre-commit").write_text("#!/bin/sh\n", encoding="utf-8")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ADVISORY" not in proc.stderr, "a checkable row must not be advised"


def test_the_non_python_advisory_folds_to_one_line_when_the_list_is_long():
    # Legibility is the point of making the skip visible, so past the threshold
    # the per-row report folds to ONE line — which still names every row id, so
    # nothing is dropped, only the repetition.
    check_doc_refs = load_script("check_doc_refs")
    n = check_doc_refs.ADVISORY_FOLD_ABOVE
    rel = check_doc_refs.LLR_REL
    rows = [
        "{}: LLR-{:03d} Module names only ...".format(rel, i) for i in range(1, n + 1)
    ]
    assert check_doc_refs.fold_advisories(rows) == rows, "at the threshold, per row"
    folded = check_doc_refs.fold_advisories(rows + [rows[0].replace("001", "900")])
    assert len(folded) == 1
    assert "{} row(s)".format(n + 1) in folded[0]
    assert "LLR-001" in folded[0] and "LLR-900" in folded[0], "no row id is dropped"


def test_the_codesymbol_grammar_is_stated_where_the_rule_binds():
    # OI-20 ruled WHAT THE CELL MAY NAME, and a ruling nobody can find at the
    # point of enforcement is a ruling that gets re-litigated. A light presence
    # pin: the admissible list and the floor live in the rule's own docstring.
    doc = load_script("check_doc_refs").symbol_findings.__doc__
    for phrase in ("RESOLVABLE CODE SYMBOL", "MODULE PATH", "PART SOURCE"):
        assert phrase in doc, "admissible: " + phrase
    for phrase in ("NOT ADMISSIBLE", "GENERATED ARTIFACT", "PROSE CONTRACT"):
        assert phrase in doc, "inadmissible: " + phrase
    assert "DECOMPOSITION FLOOR" in doc, "the ruling's weight (OI-21 rung 4)"


def test_llr_symbol_anchor_sees_private_names_and_constants(tmp_path):
    # The reason the oracle is gen_arch_map.module_bindings and NOT the rendered
    # module map: the map is a public-API view that drops `_`-names and every
    # constant, and 41 of this repo's 149 live LLR rows name exactly those.
    for i, symbol in enumerate(("_helper", "CONST", "Klass", "method")):
        root = tmp_path / "r{}".format(i)
        root.mkdir()
        spine_repo(root, "scripts/real.py", symbol=symbol)
        (root / "scripts" / "real.py").write_text(
            "CONST = 1\n\n\ndef _helper():\n    pass\n\n\n"
            "class Klass:\n    def method(self):\n        pass\n",
            encoding="utf-8",
        )
        proc = refs(root, "--strict")
        assert proc.returncode == 0, symbol + ": " + proc.stdout + proc.stderr


def test_llr_symbol_anchor_does_not_double_report_a_missing_module(tmp_path):
    # A Module that is not on disk is the PATH tier's finding. Reporting it here
    # too would count one rot twice and make the anchor's number unreadable.
    spine_repo(tmp_path, "scripts/real.py", module="scripts/gone.py", symbol="load")
    proc = refs(tmp_path)
    assert "LLR-001 Module" in proc.stderr, "the path tier still convicts"
    assert "LLR-001 CodeSymbol" not in proc.stderr


def test_llr_symbol_anchor_skips_placeholder_rows(tmp_path):
    # `*-000` example rows keep a scaffolded template copy-ready.
    spine_repo(tmp_path, "scripts/real.py")
    llr = tmp_path / "docs" / "requirements" / "low-level-requirements.csv"
    llr.write_text(
        llr.read_text(encoding="utf-8")
        + "LLR-000,SR-000,Example,scripts/real.py,your_symbol_here,"
        "detail,,(see TC-000),Draft,,1\n",
        encoding="utf-8",
    )
    assert refs(tmp_path, "--strict").returncode == 0
