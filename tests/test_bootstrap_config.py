"""bootstrap.sync_config — an adopter-edited configuration survives a re-sync
(SR-141/LLR-161, TC-155).

TC-155 permutations: edited-config | absent-config | legacy-source-present.

The property is the one adopters actually depend on: upgrading the kit must
never cost a repo its behavioural setup. So the edited case is asserted
byte-for-byte, and asserted again under `--force` — the flag that DOES overwrite
every ordinary scaffolded file, and the reason docs/config.toml is not a MAPPING
row at all.

The ordering is tested too, because it is load-bearing rather than incidental:
bootstrap scaffolds the retired one-word files, so a converter run AFTER the copy
pass would convert this run's own freshly-written defaults and hand a brand-new
repo a mixed-source refusal on day one.
"""

import tomllib

import pytest
from conftest import KIT, SCRIPTS, load_script, run_py

BOOTSTRAP = load_script("bootstrap")
CONFIG = load_script("config")
MIGRATE = load_script("config_migrate")

TEMPLATE = (KIT / "config.toml.template").read_text(encoding="utf-8")
EDITED = 'schema = 1\n\n# my repo, my dials\n[policy]\npush = "agent"\n'


def legacy(root, rel, text):
    path = root.joinpath(*rel.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def config_of(root):
    return (root / "docs" / "config.toml").read_bytes()


# --- TC-155: absent-config ----------------------------------------------------
def test_absent_config_receives_the_blank_form(tmp_path):
    written, report = BOOTSTRAP.sync_config(tmp_path)
    assert written == ["docs/config.toml"]
    assert report == []
    assert (tmp_path / "docs" / "config.toml").read_text(encoding="utf-8") == TEMPLATE


def test_the_written_blank_form_has_lf_endings(tmp_path):
    BOOTSTRAP.sync_config(tmp_path)
    assert b"\r\n" not in config_of(tmp_path)


def test_a_dry_run_writes_nothing(tmp_path):
    written, report = BOOTSTRAP.sync_config(tmp_path, dry_run=True)
    assert written == ["docs/config.toml"]
    assert not (tmp_path / "docs" / "config.toml").exists()


# --- TC-155: edited-config ----------------------------------------------------
def test_an_edited_config_is_untouched(tmp_path):
    legacy(tmp_path, "docs/config.toml", EDITED)
    before = config_of(tmp_path)
    written, report = BOOTSTRAP.sync_config(tmp_path)
    assert written == [] and report == []
    assert config_of(tmp_path) == before


def test_an_edited_config_survives_a_legacy_source_reappearing(tmp_path):
    legacy(tmp_path, "docs/config.toml", EDITED)
    legacy(tmp_path, "docs/push-policy", "human\n")
    before = config_of(tmp_path)
    BOOTSTRAP.sync_config(tmp_path)
    assert config_of(tmp_path) == before


# --- TC-155: legacy-source-present -------------------------------------------
def test_a_surviving_retired_source_is_converted(tmp_path):
    legacy(tmp_path, "docs/push-policy", "# header\nagent\n")
    legacy(tmp_path, "docs/review-policy", "2\n")
    BOOTSTRAP.sync_config(tmp_path)
    cfg, findings = CONFIG.load_config(tmp_path)
    assert findings == [], CONFIG.refusal_lines(findings)
    assert cfg.policy.push == "agent"
    assert cfg.policy.review_rounds == 2
    assert config_of(tmp_path) != TEMPLATE.encode("utf-8")


def test_the_converters_open_questions_are_returned_not_swallowed(tmp_path):
    legacy(tmp_path, "docs/gate-policy", "autonomous\n")
    written, report = BOOTSTRAP.sync_config(tmp_path)
    assert written == ["docs/config.toml"]
    assert [item.source for item in report] == ["docs/gate-policy"]


def test_a_stack_ini_with_nothing_to_carry_still_gets_the_blank_form(tmp_path):
    # docs/stack.ini survives the migration, so its mere presence must not be
    # read as "there is something to convert".
    legacy(
        tmp_path, "docs/stack.ini", "[paths]\nsrc = src\n\n[agent-loop]\nmodel = opus\n"
    )
    BOOTSTRAP.sync_config(tmp_path)
    assert (tmp_path / "docs" / "config.toml").read_text(encoding="utf-8") == TEMPLATE


def test_a_stack_ini_lane_dial_is_carried_across(tmp_path):
    legacy(tmp_path, "docs/stack.ini", "[agent-loop]\nlanes = 4\n")
    BOOTSTRAP.sync_config(tmp_path)
    cfg, findings = CONFIG.load_config(tmp_path)
    assert findings == []
    assert cfg.automation.lanes == 4


# --- the real scaffolder, end to end -----------------------------------------
@pytest.fixture
def fresh(tmp_path):
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return tmp_path


def test_a_fresh_scaffold_gets_the_blank_form_not_a_conversion(fresh):
    """The ordering property, stated as an outcome.

    The copy pass lays down docs/gate-policy, docs/push-policy,
    docs/review-policy, docs/privacy-check, docs/blackout and docs/agents.csv.
    Converting THOSE would declare canonical keys beside the retired files this
    same run just wrote — mixed-source on day one, for a repo that has made no
    choices yet.
    """
    assert (fresh / "docs" / "config.toml").read_text(encoding="utf-8") == TEMPLATE
    assert CONFIG.mixed_source_findings(fresh) == []
    cfg, findings = CONFIG.load_config(fresh)
    assert findings == [], CONFIG.refusal_lines(findings)


def test_a_fresh_scaffold_can_answer_a_policy_query(fresh):
    # The hooks are only as good as the reader the scaffold ships them.
    proc = run_py(
        ["scripts/config_query.py", "--root", str(fresh), "policy.privacy_check"],
        cwd=fresh,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "false"


def test_a_re_sync_preserves_an_edited_config(fresh):
    (fresh / "docs" / "config.toml").write_text(EDITED, encoding="utf-8", newline="\n")
    before = config_of(fresh)
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", fresh], cwd=fresh)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert config_of(fresh) == before


def test_even_force_preserves_an_edited_config(fresh):
    # --force overwrites every ordinary scaffolded file; the adopter-owned
    # config must be the exception, which is why it is not a MAPPING row.
    (fresh / "docs" / "config.toml").write_text(EDITED, encoding="utf-8", newline="\n")
    before = config_of(fresh)
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", fresh, "--force"], cwd=fresh)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert config_of(fresh) == before


def test_a_retrofit_onto_an_existing_repo_converts_its_policies(tmp_path):
    # ADOPTING.md's case: the kit dropped into a repo that already declared its
    # behaviour the old way.
    legacy(tmp_path, "docs/push-policy", "agent\n")
    legacy(tmp_path, "docs/privacy-check", "true\n")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    document = tomllib.loads(
        (tmp_path / "docs" / "config.toml").read_text(encoding="utf-8")
    )
    assert document["policy"]["push"] == "agent"
    assert document["policy"]["privacy_check"] is True


def test_the_config_scripts_are_shipped_to_a_scaffold(fresh):
    for name in ("config.py", "config_query.py", "config_migrate.py"):
        assert (fresh / "scripts" / name).is_file(), name


def test_the_config_document_is_not_a_mapping_row():
    # Asserted, not assumed: a future edit adding it to MAPPING would silently
    # hand --force the power to clobber an adopter's whole setup.
    assert "docs/config.toml" not in {dst for _, dst in BOOTSTRAP.MAPPING}
