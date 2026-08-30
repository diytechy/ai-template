"""trace.py's IF-### interface-seam tier — WI-521 slice 3 split this from
tests/test_trace.py by behavior boundary (M-06).

The interface catalog trace.py reads at process.md §8: IF id integrity and the
owner-shape --strict findings, the warn-first IF+CMP schema tier (WI-443 / OI-14
part B), the endpoint reachability advisory, the OI-67 owner/consumers reshape
and IF carriage, and the one ruled home for a seam citation — the TC's `Verifies`
cell joined against interfaces.toml (WI-065). Every test here rides a
scaffold-driven trace.py subprocess run, the same heavy class as the module it
came out of, so tests/conftest.py lists it beside test_trace in SLOW_MODULES.

What stays in tests/test_trace.py is the SN->SR->LLR->TC spine: the orphan /
strict gates, the verification-category buckets, the schema-safe extra columns,
the SN status vocabulary, the Drafted exemptions and the approved-phase
completeness rule.
"""

from conftest import make_minimal_project, record_ids, run_py


# --- WI-056: the IF-### interface-seam tier (process.md §8) ---------------------
# trace.py now reads the interface catalog (the SR-002-era gap): IF id integrity,
# the owner-SHAPE findings (a --strict finding, like PB's), and a warn-only
# reachability advisory. The full architecture-connectivity coverage lives in
# check_trajectory.

IF_HEADER = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


def _ifs_toml(body):
    """The CSV bodies below as the TOML carrier the tier moved to at WI-443.

    Translated rather than rewritten at every call site for the reason
    test_trajectory_arch states: these tests are about back-links, endpoints and
    seam citations, and burying their subject under a schema migration would
    cost more than it proves. `Status` is DROPPED — the column retired with the
    ruling. The CSV carrier itself keeps a test of its own
    (`test_legacy_interfaces_csv_still_reads_through_the_carrier`)."""
    import csv as _csv
    import io as _io

    # The fixture bodies keep the legacy CSV's column shape because that is what
    # the legacy carrier holds; the translation applies the renames the registry
    # took. OI-67 (ruled (a), 2026-08-29) is the latest: the row is ONE OWNER,
    # ITS CONSUMERS AND A TYPED STATEMENT, so `ThisProject` is now the `owner`
    # (the providing THING, in the one spelling `consumers` uses) and `Contract`
    # is the `data` summary. `Direction` and `Req-Refs` translate to NOTHING —
    # flow is the shape of the row, and the spine link is reached THROUGH the
    # owner rather than stated on it.
    keys = [
        ("ThisProject", "owner"),
        ("Contract", "data"),
        ("Version", "version"),
        ("Stability", "status"),
        ("Component", "component"),
        ("Notes", "notes"),
    ]
    out = []
    for r in _csv.DictReader(_io.StringIO(IF_HEADER + body)):
        rid = (r.get("IF-ID") or "").strip()
        if not rid:
            continue
        out.append("[interface.{}]".format(rid))
        # `channel` is REQUIRED and closed. The bodies below are module-to-module
        # seams, so `call` is the honest seed; a test about the vocabulary itself
        # writes TOML directly.
        out.append('channel = "call"')
        consumers = [
            c.strip() for c in (r.get("Counterpart") or "").split(";") if c.strip()
        ]
        out.append(
            "consumers = [{}]".format(
                ", ".join('"{}"'.format(c.replace('"', '\\"')) for c in consumers)
            )
        )
        for col, key in keys:
            value = (r.get(col) or "").strip()
            if value:
                out.append('{} = """{}"""'.format(key, value))
        out.append("")
    return "\n".join(out) + "\n"


def _write_ifs(scaffold, body):
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        _ifs_toml(body), encoding="utf-8"
    )
    record_ids(scaffold)


def _report(scaffold):
    return (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def test_if_tier_integrity(scaffold):
    make_minimal_project(scaffold)
    # A clean seam: the owner is a module path LLR-001's `Module` names.
    _write_ifs(
        scaffold,
        'IF-001,Provides,src/demo,downstream adopter,"cli --help exits 0",'
        "SR-001,v1,Stable,Active,,\n",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=1 interface-findings=0" in proc.stdout

    # An ID-SHAPED owner -> a --strict finding. This was the `Req-Refs` back-link
    # rule until OI-67 (ruled (a), 2026-08-29): the spine link is REACHED through
    # the owner now, so stating a requirement id in the cell that must hold the
    # providing THING is the wrong shape rather than a missing link.
    _write_ifs(scaffold, 'IF-001,Provides,SR-001,git,"pushes",,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "IF IF-001 Owner='SR-001' names a requirement or design id" in _report(
        scaffold
    )

    # And it is the SHAPE that is wrong, not the resolution: an id nothing
    # resolves reports the same finding, in the same words.
    _write_ifs(scaffold, 'IF-001,Provides,LLR-999,git,"pushes",,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "IF IF-001 Owner='LLR-999' names a requirement or design id" in _report(
        scaffold
    )

    # A malformed IF id joins the always-on integrity floor (--strict-integrity).
    _write_ifs(
        scaffold, 'IF-1x,Provides,src/demo,git,"pushes",SR-001,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    assert "malformed" in _report(scaffold)


def test_if_endpoint_advisory_is_warn_only(scaffold):
    # A module-shaped owner that no design row's `Module` names and whose header
    # declares no `Implements:` line traces to no requirement — warn-only since
    # OI-67, because a file-owned or external-owned seam legitimately reaches no
    # design row and the class that does is a debt list, not a gate.
    make_minimal_project(scaffold)
    _write_ifs(
        scaffold, 'IF-001,Provides,src/nowhere,git,"x",SR-001,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "this seam traces to no requirement" in proc.stdout
    assert "endpoint advisories" in _report(scaffold).lower()
    # The other half: the SAME body owned by the module LLR-001 names is silent,
    # so the advisory is the reachability judgement and not a rule that fires on
    # every row.
    _write_ifs(scaffold, 'IF-001,Provides,src/demo,git,"x",SR-001,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "traces to no requirement" not in proc.stdout


def test_a_row_with_no_in_tree_endpoint_is_a_strict_finding(scaffold):
    # Adversarial review 2026-08-29, F2. An `external:` owner is exempt from
    # the reachability advisory (an external party has no design row) — and
    # that exemption used to be the row's LAST rule, so a row whose far side
    # was `external:` too owed nothing to anybody: not a design row, not a
    # `Contract IF-###:` body (the armed gate states our reading of an external
    # surface in the header of the kit module that FACES it, and here there is
    # none). A crossing between two external parties is `external.toml`'s row,
    # not this tier's.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    all_external = (
        "[interface.IF-001]\n"
        'owner = "external:git"\n'
        'consumers = ["external:downstream adopter"]\n'
        'channel = "git"\n'
        'data = "the ref state"\n'
        'status = "Drafted"\n'
    )
    (req / "interfaces.toml").write_text(all_external, encoding="utf-8")
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "IF IF-001 has no in-tree endpoint" in _report(scaffold)

    # The other half: ONE kit module on the far side and the row is a seam of
    # this system again — the rule is "no endpoint in the tree", not "the owner
    # is external".
    (req / "interfaces.toml").write_text(
        all_external.replace(
            'consumers = ["external:downstream adopter"]', 'consumers = ["src/demo"]'
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no in-tree endpoint" not in _report(scaffold)


# --- WI-443 / OI-14 part B: the IF+CMP schema tier, WARN-FIRST -----------------
# The ruled sequencing is advisory-until-the-corpus-converges, so EVERY test in
# this section asserts the WARN TEXT and `returncode == 0` under `--strict`. A
# rule that reddens a gate here would be this slice overreaching its ruling; a
# rule that says nothing would be the state OI-14 spent three days measuring the
# drift of. Both halves are pinned, per rule.

CLEAN_IF = (
    'IF-001,Provides,src/demo,external:git,"reads the ref state",'
    "SR-001,v1,Approved,Active,,\n"
)


def _warn_run(scaffold, body):
    """`--strict` over one IF row; returns stdout and asserts the exit is
    UNTOUCHED — the warn-first contract, checked at every call site rather than
    once, because 'advisory' is the property most easily lost by accident."""
    _write_ifs(scaffold, body)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def test_clean_if_row_trips_none_of_the_new_rules(scaffold):
    # The other half of every test below: a clean row must be SILENT, or a rule
    # that fires on everything would pass each fires-on-a-defect assertion.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF)
    for noise in (
        "Data names WI-",
        "cites decision",
        "Data argues",
        "ceiling 160",
        "has empty required field",
        "closed vocabulary",
        "resolves to no module, file or directory",
        "carries the retired",
    ):
        assert noise not in out, noise


def test_a_retired_cell_is_a_strict_finding(scaffold):
    # OI-67 slice 6, the armed gate's registry half: the five cells the ruling
    # took off the row are the wrong SHAPE wherever they still appear — a
    # `contract` (the definition has one home, the owner's header), a
    # `provider`/`req_refs`/`signal`/`signal_note` (derived or subsumed). Each
    # is named by key; the legacy summarizing warning is gone. ONE finding per
    # retired KEY, naming the rows that carry it (adversarial review
    # 2026-08-29, F7) — the registry is what carries a retired column, and a
    # per-row copy of one column's finding says the same thing N times.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "call"\n'
        'contract = "the definition, in the wrong home"\n'
        'req_refs = ["SR-001"]\n'
        'version = "v1"\n'
        'status = "Drafted"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = _report(scaffold)
    assert "carries the retired `contract` cell (set on IF-001)" in report
    assert "carries the retired `req_refs` cell (set on IF-001)" in report
    assert "legacy `contract` cell" not in proc.stdout
    # Delete them and the row is clean: the finding is the cell, not the row.
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "call"\n'
        'version = "v1"\n'
        'status = "Drafted"\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "carries the retired" not in _report(scaffold)


def test_a_retired_column_in_a_legacy_csv_header_is_a_strict_finding(scaffold):
    # THE HOLE THE PRESENCE RULE CLOSES (adversarial review 2026-08-29, F7).
    # The retired SHAPE is the key, not its value: under the legacy CSV carrier
    # a header column is present on EVERY row whether or not anyone filled it
    # in, so a value test read a retired column with empty cells as absent and
    # a registry could carry it indefinitely by keeping it blank. Reported ONCE
    # per column, naming the header — not once per row, which would say the
    # same thing as many times as the registry has rows.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "interfaces.toml").unlink()  # the CSV is the ONLY home, not a second
    (req / "interfaces.csv").write_text(
        "IF-ID,Owner,Consumers,Channel,Data,Contract,Version,Status\n"
        "IF-001,src/demo,external:git,call,the ref state,,v1,Drafted\n"
        "IF-002,src/demo,external:git,call,the commit range,,v1,Drafted\n",
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = _report(scaffold)
    assert (
        "carries the retired `contract` cell (the header column `Contract`)" in report
    )
    assert report.count("carries the retired") == 1, report
    # Drop the column and the registry is clean — the finding is the column.
    (req / "interfaces.csv").write_text(
        "IF-ID,Owner,Consumers,Channel,Data,Version,Status\n"
        "IF-001,src/demo,external:git,call,the ref state,v1,Drafted\n"
        "IF-002,src/demo,external:git,call,the commit range,v1,Drafted\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "carries the retired" not in _report(scaffold)


def test_an_empty_retired_cell_and_a_nested_sub_table_are_refused_by_the_carrier(
    scaffold,
):
    # The other two shapes the 2026-08-29 review named, PINNED HERE rather than
    # re-implemented in `interface_findings`: `spine_carrier.load` already
    # refuses both over every TOML registry it reads, this tier included, and a
    # second copy of a rule that already fires is exactly what the 0→A→B rule
    # forbids. `provider = ""` is the explicit-empty refusal (under this
    # carrier an unset cell is an ABSENT key); `[interface.IF-002.legacy]` is
    # the nested-table refusal (a cell that is itself a table is not a cell).
    # Both land as a REFUSAL rather than a report — the fail-closed half of the
    # carrier fork — so `--strict` reds either way.
    make_minimal_project(scaffold)
    ifs = scaffold / "docs" / "requirements" / "interfaces.toml"
    clean = (
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "call"\n'
        'data = "the ref state"\n'
        'status = "Drafted"\n'
    )
    ifs.write_text(clean, encoding="utf-8")
    record_ids(scaffold)
    assert run_py(["scripts/trace.py", "--strict"], cwd=scaffold).returncode == 0

    ifs.write_text(clean + 'provider = ""\n', encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "IF-001 sets `provider` to an EMPTY STRING" in proc.stdout + proc.stderr

    ifs.write_text(
        clean + '\n[interface.IF-001.legacy]\ncontract = "an old body"\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "IF-001.legacy is a TABLE, not a cell" in proc.stdout + proc.stderr


def test_channel_refuses_an_unknown_value_as_a_warn(scaffold):
    # The owner's ruled typing is a CLOSED vocabulary — `Channel` since OI-67,
    # which subsumed `Signal`'s discrete/variable pair (`exit-code` and `env` are
    # the discrete kinds; the rest are unbounded). Written straight to TOML:
    # `_write_ifs` supplies `channel = "call"`, and the point here is a value the
    # vocabulary does not contain.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "analog"\n'
        'data = "reads the ref state"\n'
        'version = "v1"\n'
        'status = "Approved"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn-first
    assert "IF IF-001 has Channel='analog'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    assert "bytes, call, cli, env, exit-code, file, git, stdout" in proc.stdout


def test_approval_refuses_an_unknown_value_as_a_warn(scaffold):
    # The successor of the `Stability=Provisional` case (WI-442). `Provisional`
    # was the real value four live rows carried while `Stability` was declared by
    # process.md §8 and validated by nothing; the vocabulary is closed now, and
    # the check has to bite on the SUCCESSOR column or the lesson was migrated
    # away rather than kept.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace(",v1,Approved,", ",v1,Provisional,"))
    assert "IF IF-001 has Status='Provisional'" in out
    assert "Approved, Drafted" in out


def test_cmp_state_refuses_an_unknown_value_as_a_warn(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "components.toml").write_text(
        '[component.CMP-001]\nname = "Core"\ncategory = "software"\n'
        'status = "in-flight"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "CMP CMP-001 has Status='in-flight'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout


# --- the SN tier's Status vocabulary (the enum floor's fourth tier) -----------
# `ENUM_FIELDS["SN"]["Status"]` was DECLARED while analyze()'s enum fold ran over
# `{"SR", "LLR", "TC"}` only, so a need could carry any word at all and no bar
# said so. These two are the always-on floor's fires-on-a-defect / silent-on-a-
# clean-row pair, run through the CLI like every other vocabulary case above.
NEEDS_TOML = """[need.SN-001]
status = "{status}"
priority = "M"
need = "Add two numbers."
why = "Demo."
acceptance = "add(1,2) gives 3."
"""


def _needs_on_toml(scaffold, status):
    """Re-home the scaffold's need tier on the TOML carrier at one status.

    The markdown file is REMOVED, not left beside it: `spine_carrier.resolve`
    refuses both homes at once (and that refusal is the rule working), which is
    the same reason `use_legacy_spine_carrier` drops the home it is not using."""
    req = scaffold / "docs" / "requirements"
    (req / "stakeholder-needs.md").unlink(missing_ok=True)
    (req / "stakeholder-needs.toml").write_text(
        NEEDS_TOML.format(status=status), encoding="utf-8"
    )


def test_sn_status_outside_the_closed_vocabulary_is_an_integrity_finding(scaffold):
    make_minimal_project(scaffold)
    _needs_on_toml(scaffold, "Bananas")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert "SN SN-001 has Status='Bananas'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    # INTEGRITY-class, so it gates at the always-on floor rather than waiting for
    # --strict-schema at DevStg-Impl (the D-9 correction C1 routing).
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_every_declared_sn_status_leaves_the_enum_floor_silent(scaffold):
    # The other half: a rule that fired on everything would pass the assertions
    # above. All three live vocabulary words, each on its own scaffold run.
    make_minimal_project(scaffold)
    for status in ("Drafted", "Approved", "Founded"):
        _needs_on_toml(scaffold, status)
        proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
        assert "closed vocabulary" not in proc.stdout, status
        assert proc.returncode == 0, status + proc.stdout + proc.stderr


def test_missing_required_if_field_is_a_warn(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'data = "reads the ref state"\n'
        'version = "v1"\n'
        'status = "Approved"\n',  # no `channel`
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF IF-001 has empty required field Channel" in proc.stdout


def test_work_item_id_in_data_is_a_refuse_class_warn(scaffold):
    # ~24% of live rows carried one when the rule was written. A work-item id
    # AGES, and a cancelled row's id sitting in the cell still reads as
    # authority. The four form rules moved from `Contract` to `Data` unchanged
    # at OI-67 — the cell they police is the row's typed statement now.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        CLEAN_IF.replace("reads the ref state", "reads the ref state (WI-374)"),
    )
    assert "IF IF-001 Data names WI-374" in out
    assert "belongs in the log" in out


def test_decision_citation_in_data_is_a_refuse_class_warn(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        CLEAN_IF.replace("reads the ref state", "reads the ref state per D-9"),
    )
    assert "IF IF-001 Data cites decision D-9" in out


def test_a_crossing_id_is_not_read_as_a_decision(scaffold):
    # The narrowing that a broader `<LETTER>-<n>` pattern got wrong: it read the
    # part-A data pack's own crossing ids (M-10) as rulings, which is a check
    # inventing a rule nobody wrote.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold, CLEAN_IF.replace("reads the ref state", "the M-10 crossing")
    )
    assert "cites decision" not in out


def test_rationale_connective_in_data_warns(scaffold):
    make_minimal_project(scaffold)
    for word in ("because", "rather than", "so that", "since"):
        out = _warn_run(
            scaffold,
            CLEAN_IF.replace("reads the ref state", "reads it " + word + " it must"),
        )
        assert "Data argues ('{}')".format(word) in out, word
        assert "move the ARGUMENT to the Rationale column" in out
        # The CITATION half now points at the log, not at Rationale: the owner
        # ruling forbids a citation frame in any living registry cell, so the
        # advice that used to send it next door would send it somewhere it is
        # equally forbidden.
        assert "any citation inside it to the log" in out


def test_data_over_the_length_ceiling_warns(scaffold):
    # The ceiling came DOWN from 500 to 160 with the cell (OI-67): `Data` is the
    # alphabet or a one-clause schema pointer, and the definition it used to hold
    # lives in the owner's `Contract IF-###:` body.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace("reads the ref state", "x" * 161))
    assert "IF IF-001 Data is 161 characters (ceiling 160)" in out
    # ...and 160 exactly is inside the ceiling (a boundary, not an off-by-one).
    out = _warn_run(scaffold, CLEAN_IF.replace("reads the ref state", "y" * 160))
    assert "ceiling 160" not in out


def test_untagged_endpoint_advisory_classifies_instead_of_staying_silent(scaffold):
    """The coverage fix the part-A data pack demands.

    45 of 113 live rows have an endpoint carrying no component tag, which makes
    `cross_component_findings` VACUOUS for them — and the containment rule that
    was assumed to cover them CANNOT, because it ranges over arch-map modules
    while these endpoints are data files, directories and external actors. Both
    checks were green and neither was saying anything. This advisory does not
    make them findings; it makes them VISIBLE, and it names individually only
    the endpoints that resolve to nothing, which are the only actionable ones."""
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,docs/status.md,"writes",SR-001,v1,Stable,Active,,\n'
        'IF-002,Provides,src/demo,external:downstream adopter,"cli",'
        "SR-001,v1,Stable,Active,,\n"
        'IF-003,Provides,src/demo,docs/gone/nowhere.md,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF endpoint coverage:" in out
    assert "1 resolve to a file or directory in the tree" in out
    assert "1 are marked `external:`" in out
    assert "1 resolve to nothing" in out
    # Only the unresolved one is named individually.
    assert "IF IF-003 Consumers='docs/gone/nowhere.md' resolves to no module" in out
    assert "IF IF-001 Consumers" not in out
    assert "IF IF-002 Consumers" not in out


def test_semicolon_joined_endpoint_is_several_endpoints(scaffold):
    # A `;`-joined cell names SEVERAL endpoints; reading it as one reported a
    # real three-module seam (IF-097) as a dangling path. IF-097 KEPT this shape
    # at the 2026-08-15 rework rather than splitting into three rows: the three
    # consumers share ONE contract, and three rows would be three copies of it.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,"docs/status.md;docs/log.md","x",'
        "SR-001,v1,Stable,Active,,\n",
    )
    assert "2 resolve to a file or directory in the tree" in out
    assert "resolve to nothing" in out and "0 resolve to nothing" in out


# --- 2026-08-15 interface rework, step 2: endpoint validation ------------------
# The rule the plan asks for: an endpoint that resolves to NOTHING and carries no
# external marker is a named warn — in EITHER endpoint column, path-shaped or
# not. Before this, the classifier guessed from spelling, so a name-shaped rot
# was silently "an external actor" and a real actor could never be distinguished
# from one.


def test_actor_shaped_endpoint_without_the_marker_is_now_named(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,agent CLI,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF IF-001 Consumers='agent CLI' resolves to no module" in out
    assert "mark it `external:<actor>`" in out
    assert "0 are marked `external:`" in out


def test_the_external_marker_silences_it_and_is_counted(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,external:agent CLI,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "resolves to no module" not in out
    assert "1 are marked `external:`" in out


def test_a_bare_external_marker_names_nobody_and_still_warns(scaffold):
    # The one way the marker could be worse than the guess it replaced: a cell
    # that claims externality without saying what is on the far side.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold, 'IF-001,Provides,src/demo,external:,"x",SR-001,v1,Stable,Active,,\n'
    )
    assert "IF IF-001 Consumers='external:' resolves to no module" in out


def test_the_owner_endpoint_is_validated_too_not_just_consumers(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/gone,docs/status.md,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF IF-001 Owner='src/gone' resolves to no module" in out


# --- OI-67 ruled (a): the Owner cell is the providing THING, plus carriage -----
# The owner is one endpoint in the one spelling `consumers` uses — a module path,
# a file or directory path, or an `external:` party — and the SHAPE is a --strict
# finding, because an id-typed owner and a path-typed provider were the same fact
# in two spellings and only one of them survived. Q3's carriage rules (an IF may
# name another IF as the bundle carrying it, and that graph must be acyclic and
# bounded) stay warn-first beside it: the bound is provisional.


def _if_row(**kw):
    base = {
        "owner": "src/demo",
        "consumers": '["external:git"]',
        "channel": "call",
        "data": "reads the ref state",
        "version": '"v1"',
        "status": '"Drafted"',
    }
    base.update(kw)
    lines = ["[interface.IF-001]"]
    for k, v in base.items():
        lines.append("{} = {}".format(k, v if v.startswith(("[", '"')) else '"%s"' % v))
    return "\n".join(lines) + "\n"


def _toml_write(scaffold, text):
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        text, encoding="utf-8"
    )
    record_ids(scaffold)


def _toml_warn_run(scaffold, text):
    _toml_write(scaffold, text)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn-first, always
    return proc.stdout


def _toml_finding_run(scaffold, text):
    """`--strict` over one IF row that is expected to FAIL, returning stdout.

    The owner-shape rules are the one arm of this tier that GATES, so their call
    sites assert the nonzero exit as loudly as the warn-first sites assert the
    zero one — a finding that stopped joining the failure set would otherwise
    read as a passing test."""
    _toml_write(scaffold, text)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    return proc.stdout


def test_an_owner_that_names_a_requirement_or_design_row_is_a_finding(scaffold):
    # The shape OI-67 retired, and BOTH tiers are wrong for the same reason: a
    # design row's module IS the providing thing, so naming the row instead of
    # the thing states a derivable fact in a second spelling.
    make_minimal_project(scaffold)
    for oid in ('"SR-001"', '"LLR-001"'):
        out = _toml_finding_run(scaffold, _if_row(owner=oid))
        assert "names a requirement or design id" in out, oid
        assert "the owner is the providing THING" in out, oid


def test_an_owner_that_is_a_path_is_the_clean_shape(scaffold):
    # The other half, and the one that keeps the rule from firing on everything:
    # a module path, a file path and a marked external party are the three
    # legitimate spellings, and none of them reports.
    make_minimal_project(scaffold)
    for owner, extra in (
        ("src/demo", {}),
        ("docs/status.md", {}),
        # An `external:` owner needs a kit module on its FAR SIDE to be a seam
        # of this system at all — the default `consumers` cell is itself
        # `external:git`, which is
        # `test_a_row_with_no_in_tree_endpoint_is_a_strict_finding`'s subject
        # and not this test's. The owner spelling is what is under test here.
        ("external:git", {"consumers": '["src/demo"]'}),
    ):
        out = _toml_warn_run(scaffold, _if_row(owner='"%s"' % owner, **extra))
        assert "Owner=" not in out, owner
        assert "no in-tree endpoint" not in out, owner


def test_an_owner_naming_several_endpoints_is_a_finding(scaffold):
    # One row has ONE owner: a `;`-joined cell is a bundle wearing one row's
    # clothes, and the ruling splits it or declares a carrier on `carried_by`.
    make_minimal_project(scaffold)
    out = _toml_finding_run(scaffold, _if_row(owner='"src/demo;src/helper"'))
    assert "names 2 endpoints" in out
    assert "one row has ONE owner" in out


def test_the_far_side_names_the_direction_and_both_or_neither_is_a_warn(scaffold):
    # THE FAR SIDE IS EXACTLY ONE OF `requestors` / `consumers` (OI-67, the
    # owner's own addition): the key name is the direction. Both or neither is
    # reported WARN-FIRST — the same tier as an empty required cell, because a
    # row with no far side is incomplete (an adopter mid-migration), where an
    # id-shaped owner is wrong (the retired meaning, stated) and gates.
    make_minimal_project(scaffold)
    consumers_line = 'consumers = ["external:git"]\n'
    neither = _if_row().replace(consumers_line, "")
    out = _toml_warn_run(scaffold, neither)
    assert "IF IF-001 names neither Requestors and Consumers" in out
    both = _if_row(requestors='["src/helper"]')
    out = _toml_warn_run(scaffold, both)
    assert "IF IF-001 names both Requestors and Consumers" in out
    # ...and a requestors-only row is the clean shape, exactly as consumers-only is.
    only = _if_row(requestors='["src/helper"]').replace(consumers_line, "")
    assert "Requestors and Consumers" not in _toml_warn_run(scaffold, only)


def test_a_missing_owner_is_the_required_field_rule_not_a_second_one(scaffold):
    # One defect, one sentence: an empty cell is already "has empty required
    # field Owner", and saying it twice teaches the reader there are two rules.
    make_minimal_project(scaffold)
    text = _if_row()
    out = _toml_warn_run(scaffold, text.replace('owner = "src/demo"\n', ""))
    assert "IF IF-001 has empty required field Owner" in out
    assert "Owner=" not in out


def test_carried_by_resolves_and_a_self_carrier_is_named_as_such(scaffold):
    make_minimal_project(scaffold)
    out = _toml_warn_run(scaffold, _if_row(carried_by='"IF-404"'))
    assert "IF IF-001 CarriedBy references unknown IF-404" in out
    out = _toml_warn_run(scaffold, _if_row(carried_by='"IF-001"'))
    assert "CarriedBy names itself — leave the cell empty" in out


def test_a_carriage_cycle_is_reported_once_per_row_on_it(scaffold):
    # The obligation Q3 created: `IF-A carried by IF-B carried by IF-A` is
    # representable the moment a link may point at its own tier.
    make_minimal_project(scaffold)
    text = _if_row(carried_by='"IF-002"') + _if_row().replace(
        "IF-001", "IF-002"
    ).replace('status = "Drafted"\n', 'status = "Drafted"\ncarried_by = "IF-001"\n')
    out = _toml_warn_run(scaffold, text)
    assert out.count("sits on a CarriedBy CYCLE") == 2


def test_carriage_deeper_than_the_bound_warns_and_two_is_clean(scaffold):
    make_minimal_project(scaffold)

    def chain(n):
        # IF-001 -> IF-002 -> ... -> IF-00n, the last carrying nothing.
        out = []
        for i in range(1, n + 1):
            row = _if_row().replace("IF-001", "IF-00%d" % i)
            if i < n:
                row = row.replace(
                    'status = "Drafted"\n',
                    'status = "Drafted"\ncarried_by = "IF-00%d"\n' % (i + 1),
                )
            out.append(row)
        return "".join(out)

    assert "carriers deep" not in _toml_warn_run(scaffold, chain(3))  # depth 2
    out = _toml_warn_run(scaffold, chain(4))  # depth 3
    assert "IF IF-001 is 3 carriers deep (bound 2)" in out
    assert "the bound is provisional" in out


def test_a_declared_absence_is_not_a_dangling_endpoint(scaffold):
    """`docs/declared-absences` gets its third reader.

    An endpoint naming a path the repo has DECLARED it does not carry is neither
    rot nor external — the layer is opt-in and switched off, and the row is
    honest about what the module would read if it were on. This repo's worked
    case is `docs/requirements/assets.csv`: the off-spine asset registry, absent
    because a meta-repo ships no binary assets, with the reason already written
    down one directory up. Naming it would have been the checker demanding the
    repo delete a true statement.

    RE-POINTED 2026-08-20 (the batch review's MINOR-19): the example was
    `performance-budgets.csv` until WI-481 seeded that registry and deleted its
    declared-absence line, which left this docstring teaching a worked case that
    had become live. The scenario below uses a synthetic path, so only the
    example named in words moved."""
    make_minimal_project(scaffold)
    body = (
        'IF-001,Provides,src/demo,docs/off/budgets.csv,"x",SR-001,v1,Stable,Active,,\n'
    )
    out = _warn_run(scaffold, body)
    assert "IF IF-001 Consumers='docs/off/budgets.csv' resolves to no module" in out
    (scaffold / "docs" / "declared-absences").write_text(
        "# declared\ndocs/off/budgets.csv — the perf layer is not enabled\n",
        encoding="utf-8",
    )
    out = _warn_run(scaffold, body)
    assert "resolves to no module" not in out
    # A line with no reason declares nothing — the file requires one.
    (scaffold / "docs" / "declared-absences").write_text(
        "docs/off/budgets.csv\n", encoding="utf-8"
    )
    assert "resolves to no module" in _warn_run(scaffold, body)


def test_the_retired_direction_column_closes_no_vocabulary_here(scaffold):
    # Step 1 closed `Direction`'s vocabulary — the one IF column process.md §8
    # stated and nothing checked. WI-455 then retired the column itself (OI-60
    # ruled (a)): flow is the SHAPE of the row, owner -> consumers. The
    # vocabulary must go WITH it, or the tier keeps refusing values for a cell
    # no row is allowed to carry — and the enum survives, correctly, on the
    # BOUNDARY tier, which is the collision the shed closed.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace("IF-001,Provides,", "IF-001,Serves,"))
    assert "Direction" not in out
    assert "Consumes, Provides" not in out


def test_if_placeholder_and_absent_are_free(scaffold):
    # The scaffold ships an inert IF-000 placeholder: no interface section, green.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=" not in proc.stdout  # only the -000 placeholder
    # A truly absent registry is equally free.
    (scaffold / "docs" / "requirements" / "interfaces.toml").unlink()
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_legacy_interfaces_csv_still_reads_through_the_carrier(scaffold):
    # NEVER-BREAKING, WI-443: the tier's home is `interfaces.toml` now, but an
    # adopter who has not migrated still has `interfaces.csv` — and it must keep
    # loading, including a pre-WI-056 file with no Notes column (the missing cell
    # reads as empty) and the retired `Status` column (an unknown column is
    # simply carried, not a crash).
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "interfaces.toml").unlink()  # the CSV is the ONLY home, not a second
    legacy = (
        "IF-ID,Direction,ThisProject,Counterpart,Version,Stability,Status,Component\n"
    )
    # The RETIRED columns are gone from the header, and that is the rule rather
    # than tidiness: since the presence fix (2026-08-29) a retired column is a
    # strict finding wherever it is DECLARED, and a CSV header declares it on
    # every row (test_a_retired_column_in_a_legacy_csv_header_is_a_strict_finding).
    # What this test is about survives unchanged — the columns the tier retired
    # but never banned (`Direction`, `ThisProject`, `Counterpart`, `Stability`)
    # are simply carried, a pre-WI-056 file with no Notes column still reads,
    # and nothing crashes.
    (req / "interfaces.csv").write_text(
        legacy + "IF-001,Provides,src/demo,git,v1,Stable,Active,\n",
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=1 interface-findings=0" in proc.stdout


def test_both_interface_carriers_at_once_is_refused(scaffold):
    # THE HOUSE RULE (spine_carrier.resolve): two homes for one fact is the state
    # a migration exists to LEAVE, so it is refused rather than resolved by
    # precedence — a precedence rule lets a half-finished migration keep working
    # while quietly reading the stale half, and nobody finds out.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    assert (req / "interfaces.toml").exists()
    (req / "interfaces.csv").write_text(
        "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
        "Stability,Component,Notes\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0
    assert "REFUSED" in (proc.stdout + proc.stderr)
    assert "BOTH carriers" in (proc.stdout + proc.stderr)


# --- WI-065: one ruled home for a seam citation — the TC's `Verifies` cell ------
# check_trajectory's seam-TC warn reads IF-### ids out of `Verifies`, but trace's
# orphan rule used to reject any token that was not an SR/LLR id — so citing a
# seam the documented way passed one check and ORPHANED under the other, and the
# rule could not be satisfied honestly. Ruled: `Verifies` is the one citation
# cell, and trace joins IF tokens against interfaces.csv. Both halves of that
# ruling are exercised HERE, on one scaffold, because a test that ran only one
# checker is exactly what let the two disagree for as long as they did.

TWO_MODULE_IFS = (
    'IF-001,Provides,src/demo,src/helper,"add() is called by the helper",'
    "SR-001,v1,Stable,Active,,sink\n"
    'IF-002,Consumes,src/helper,src/demo,"helper reads add()",'
    "SR-001,v1,Stable,Active,,source\n"
)

HELPER_SRC = '''"""A second module, so the connectivity checks are not vacuous."""

from demo import add


def twice(n):
    """Double a number via the seam. Implements: SR-001, LLR-001"""
    return add(n, n)
'''


def _seam_scaffold(scaffold, verifies):
    """A two-module project whose single TC cites `verifies` (no arch-map
    refresh since WI-455 — trace joins IF endpoints to LLR Module cells, and
    the derived inventory reads the source tree directly)."""
    make_minimal_project(scaffold)
    (scaffold / "src" / "helper.py").write_text(HELPER_SRC, encoding="utf-8")
    _write_ifs(scaffold, TWO_MODULE_IFS)
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        'TC-001,{},Unit,call add and assert the sum,Smoke,"a=1; b=2",'
        '"Satisfies SR-001 AcceptanceCriteria",Yes,'
        "tests/test_demo.py::test_add_sr001,Approved\n".format(verifies),
        encoding="utf-8",
    )
    return scaffold


def test_seam_citation_satisfies_trace_and_check_trajectory_together(scaffold):
    _seam_scaffold(scaffold, "SR-001;LLR-001;IF-001")

    # Half one: trace no longer orphans the seam token.
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout
    assert "references unknown IF-001" not in _report(scaffold)

    # Half two: the SAME cell satisfies the seam-TC warn — the cited seam is
    # quiet while its uncited sibling still warns, so this is not vacuous.
    proc = run_py(["scripts/check_trajectory.py"], cwd=scaffold)
    seam = [ln for ln in proc.stderr.splitlines() if "cited by no TC" in ln]
    assert len(seam) == 1 and "IF-002" in seam[0] and "IF-001" not in seam[0]


def test_unknown_seam_id_in_verifies_is_still_an_orphan(scaffold):
    # Accepting the IF vocabulary is not accepting anything IF-shaped: an id that
    # resolves to no interfaces.csv row is as wrong as an unknown SR.
    _seam_scaffold(scaffold, "SR-001;LLR-001;IF-999")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "TC TC-001 references unknown IF-999" in _report(scaffold)


def test_tc_citing_only_seam_ids_is_an_orphan(scaffold):
    # A seam citation SUPPLEMENTS the spine citation. Without this rule the new
    # vocabulary would let `Verifies=IF-001` alone pass, and a test would no
    # longer have to say which requirement it discharges.
    _seam_scaffold(scaffold, "IF-001")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "TC TC-001 cites only seam id(s)" in _report(scaffold)
