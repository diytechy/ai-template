"""Local change selection accounts for the whole proposal and broadens safely."""

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "check_changed", ROOT / "scripts/check_changed.py"
)
selection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selection)
CORE = "project-trajectory/scripts/check_need_form.py"
DATA = "docs/requirements/stakeholder-needs.toml"
RENDER = "project-trajectory/scripts/rendering/traj_render.py"


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def write(root, path, text):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


@pytest.fixture
def repository(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "Selection test")
    write(tmp_path, CORE, "value = 1\n")
    write(tmp_path, RENDER, "STYLE = 'old'\n")
    write(tmp_path, DATA, '[need.SN-1]\nneed="Readable"\nstatus="Approved"\n')
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "base")
    return tmp_path, git(tmp_path, "rev-parse", "HEAD")


def test_complete_proposal_includes_earlier_commit_index_worktree_and_untracked(
    repository,
):
    root, base = repository
    write(root, RENDER, "STYLE = 'new'\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "rendering change before the latest commit")
    write(root, CORE, "value = 2\n")
    git(root, "add", CORE)
    write(root, DATA, '[need.SN-1]\nneed="Current data"\nstatus="Approved"\n')
    write(root, "assets/new icon.svg", "<svg/>")
    result = selection.select(root, base)
    assert result["suite"] == "full"
    assert set(result["paths"]) == {RENDER, CORE, DATA, "assets/new icon.svg"}


def test_independent_validator_and_its_tests_can_narrow(repository):
    root, base = repository
    write(root, CORE, "value = 2\n")
    write(root, "tests/test_check_need_form.py", "def test_new_case(): pass\n")
    assert selection.select(root, base)["suite"] == "core+boundary"


def test_existing_registry_value_change_runs_trace_and_real_output_freshness(
    repository,
):
    root, base = repository
    write(
        root,
        DATA,
        '[need.SN-1]\nneed="Readable <script> & content"\nstatus="Approved"\n',
    )
    result = selection.select(root, base)
    assert result["suite"] == "core+boundary"
    commands = selection.commands(root, result)
    assert any("--strict-schema" in command for command in commands)
    checks = [command for command in commands if "--check" in command]
    assert sum("--status" in command for command in checks) == 1
    assert any(selection.BOUNDARY_CASE in command for command in commands)


@pytest.mark.parametrize(
    ("path", "begin", "end"),
    [
        ("docs/status.md", selection.STATUS_BEGIN, selection.STATUS_END),
        (
            "docs/cli-reference.md",
            selection.CLI_BEGIN,
            selection.CLI_END,
        ),
        (
            "docs/interface-reference.md",
            selection.INTERFACE_BEGIN,
            selection.INTERFACE_END,
        ),
    ],
)
def test_regenerated_regions_allow_data_changes_but_not_authored_prose(
    repository, path, begin, end
):
    root, _ = repository
    marked = "# Owner intent\n" + begin + "\nold\n" + end
    write(root, path, marked)
    git(root, "add", ".")
    git(root, "commit", "-qm", "existing generated region")
    base = git(root, "rev-parse", "HEAD")
    write(root, DATA, '[need.SN-1]\nneed="Updated intent"\nstatus="Approved"\n')
    write(root, "PROJECT_STATE.html", "regenerated current data")
    write(root, "docs/stage", "current fingerprint")
    write(root, path, marked.replace("old", "current data"))
    assert selection.select(root, base)["suite"] == "core+boundary"
    write(root, path, marked.replace("Owner intent", "Different instructions"))
    assert selection.select(root, base)["suite"] == "full"


@pytest.mark.parametrize("path", sorted(selection.GENERATED))
def test_generated_output_alone_cannot_authorize_narrowing(repository, path):
    root, base = repository
    write(root, path, "changed output")
    assert selection.select(root, base)["suite"] == "full"


@pytest.mark.parametrize(
    "path",
    [
        "docs/open-items.html",
        "docs/requirements/components.derived.toml",
        "docs/ratify/CURRENT.md",
    ],
)
def test_whole_generated_companions_can_follow_a_classified_data_edit(repository, path):
    root, base = repository
    write(root, DATA, '[need.SN-1]\nneed="Updated intent"\nstatus="Approved"\n')
    write(root, path, "regenerated\n")
    assert selection.select(root, base)["suite"] == "core+boundary"


def test_deleting_a_generated_companion_broadens(repository):
    root, _ = repository
    path = "docs/ratify/CURRENT.md"
    write(root, path, "generated\n")
    git(root, "add", path)
    git(root, "commit", "-qm", "record generated brief")
    base = git(root, "rev-parse", "HEAD")
    write(root, DATA, '[need.SN-1]\nneed="Updated intent"\nstatus="Approved"\n')
    (root / path).unlink()
    assert selection.select(root, base)["suite"] == "full"


def test_other_generated_or_immutable_records_still_broaden(repository):
    root, base = repository
    write(root, DATA, '[need.SN-1]\nneed="Updated intent"\nstatus="Approved"\n')
    for path in ("docs/okf/index.md", "docs/ratify/2026-09-06-approved.md"):
        write(root, path, "generated elsewhere\n")
        assert selection.select(root, base)["suite"] == "full"
        (root / path).unlink()


def test_existing_work_item_values_use_the_shared_frontmatter_reader(repository):
    root, _ = repository
    path = "docs/work/queued/WI-1-real-scope.md"
    original = '+++\nid="WI-1"\nneeds=[]\n+++\n# Intent\nOriginal\n'
    write(root, path, original)
    git(root, "add", path)
    git(root, "commit", "-qm", "existing work item")
    base = git(root, "rev-parse", "HEAD")
    write(root, path, original.replace("Original", "Clarified intent"))
    assert selection.select(root, base)["suite"] == "core+boundary"
    write(root, path, original.replace("needs=[]", "needs=[]\nnew_schema_field=true"))
    assert selection.select(root, base)["suite"] == "full"


def test_authored_component_carrier_is_real_registry_data(repository):
    root, _ = repository
    path = "docs/requirements/components.toml"
    write(root, path, '[component.CMP-1]\nname="Original"\nstatus="Drafted"\n')
    git(root, "add", path)
    git(root, "commit", "-qm", "declare component")
    base = git(root, "rev-parse", "HEAD")
    write(root, path, '[component.CMP-1]\nname="Renamed"\nstatus="Drafted"\n')
    assert selection.select(root, base)["suite"] == "core+boundary"


@pytest.mark.parametrize(
    "text",
    [
        '[need.SN-1]\nneed="Readable"\nstatus="Approved"\nnew_field="shape changed"\n',
        '[need.SN-1]\nneed=123\nstatus="Approved"\n',
        '[need.SN-2]\nneed="Readable"\nstatus="Approved"\n',
        '[need.SN-1]\nneed="broken\n',
    ],
)
def test_new_fields_rows_types_and_malformed_carriers_broaden(repository, text):
    root, base = repository
    write(root, DATA, text)
    assert selection.select(root, base)["suite"] == "full"


@pytest.mark.parametrize(
    "path",
    [
        "project-trajectory/scripts/traj_display.py",
        "project-trajectory/scripts/traj_parse.py",
        "project-trajectory/scripts/kitlib/ladder.py",
        "project-trajectory/scripts/bootstrap.py",
        "project-trajectory/scripts/rendering/theme.css",
        "project-trajectory/scripts/rendering/behavior.js",
        "project-trajectory/templates/page.html",
        "scripts/dashboard-shots/shoot.mjs",
        "requirements-dev.txt",
        "pytest.ini",
        "tests/conftest.py",
        "scripts/check_changed.py",
        "unknown-source.py",
    ],
)
def test_shared_renderer_assets_tooling_and_unknown_impact_broaden(repository, path):
    root, base = repository
    write(root, path, "changed\n")
    assert selection.select(root, base)["suite"] == "full"


@pytest.mark.parametrize("rename", [False, True])
def test_renderer_delete_or_rename_outside_its_directory_still_broadens(
    repository, rename
):
    root, base = repository
    if rename:
        git(root, "mv", RENDER, "moved.py")
    else:
        (root / RENDER).unlink()
    result = selection.select(root, base)
    assert result["suite"] == "full"
    assert RENDER in result["paths"]


def test_unknown_nonancestor_and_absent_bases_are_full(repository):
    root, base = repository
    for candidate in (None, "unavailable"):
        assert selection.select(root, candidate)["suite"] == "full"
    git(root, "checkout", "-qb", "other")
    write(root, CORE, "value = 2\n")
    git(root, "commit", "-am", "other work", "-q")
    other = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "--detach", base)
    assert selection.select(root, other)["suite"] == "full"


def test_full_cadence_override_and_omitted_modules_are_explicit(repository):
    root, base = repository
    write(root, CORE, "value = 2\n")
    result = selection.select(root, base, full=True)
    assert result["suite"] == "full"
    assert selection.commands(root, result) == [
        [selection.sys.executable, "-m", "pytest", "-q", "-n", "auto"]
    ]
    narrowed = selection.commands(ROOT, {"suite": "core+boundary"})[0]
    for module in selection.HTML_TESTS:
        assert module not in narrowed
    for module in (
        "tests/test_traj_status.py",
        "tests/test_traj_parse.py",
        "tests/test_gen_trajectory_pending.py",
        "tests/test_trajectory_arch.py",
    ):
        assert module in narrowed


def test_narrow_commands_keep_every_affected_generated_surface_fresh(repository):
    root, base = repository
    write(root, DATA, '[need.SN-1]\nneed="Updated intent"\nstatus="Approved"\n')
    commands = selection.commands(root, selection.select(root, base))
    rendered = [" ".join(command) for command in commands]
    for fragment in (
        "derive_stage.py --root . --check",
        "gen_trajectory.py --root . --check",
        "gen_trajectory.py --root . --status --check",
        "gen_open_items.py --root . --check",
        "gen_components.py --root . --check",
        "gen_arch_map.py --root . --src project-trajectory/scripts "
        "--cli-doc docs/cli-reference.md --check",
        "gen_arch_map.py --root . --src project-trajectory/scripts "
        "--contracts-doc docs/interface-reference.md --check",
        "trace.py --root . --approve modified --check",
    ):
        assert any(fragment in command for command in rendered), fragment


def test_narrow_run_stops_on_first_failed_command(monkeypatch):
    monkeypatch.setattr(
        selection, "select", lambda *args, **kwargs: {"suite": "core+boundary"}
    )
    monkeypatch.setattr(selection, "commands", lambda *args: [["core"], ["freshness"]])
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(selection.subprocess, "run", run)
    assert selection.main(["--base", "recorded", "--run"]) == 7
    assert calls == [["core"]]


def test_declared_independent_validators_are_not_display_dependencies():
    from test_import_layers import import_graph

    graph = import_graph()
    pending = ["gen_trajectory", "traj_display", "traj_status"]
    reached = set()
    while pending:
        module = pending.pop()
        if module not in reached:
            reached.add(module)
            pending.extend(graph.get(module, {}))
    independent = {
        Path(path).stem
        for path in selection.CORE_ONLY
        if path.startswith("project-trajectory/")
    }
    assert independent.isdisjoint(reached), independent & reached
