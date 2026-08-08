"""Push authority as declared policy (Thread 40, process-options.md "Agent
iteration branch & sync").

Who may publish (`git push`) is a one-word `docs/push-policy` value scaffolded
into every repo: `human` (default — an agent never pushes, even if asked
mid-session; it prepares the branch and requests), `agent-iteration` (only the
scrubbed llm/<branch> iteration branch), or `agent`. These tests mechanize the
mechanical half of the layer — the policy file scaffolds, parses, and is set
at creation the same consent-first way as gate-policy; the CI trigger and the
log template carry their one-line pieces of the ritual. The scrub/collate
steps themselves are LLM judgment verified by recorded §5 verdicts, not
pytest (the honesty stance the thread spec states).
"""

from conftest import KIT, SCRIPTS, process_key, run_py


def _push(root):
    """The declared push authority — SN-028 moved it out of the one-word
    docs/push-policy file into `docs/process.toml [policies] push`."""
    return process_key(root, "policies", "push")


def test_scaffold_push_policy_defaults_human(scaffold):
    # The scaffolded authority is `human` — an agent never pushes — so every
    # default scaffold starts with publication as a deliberate human act.
    policy = scaffold / "docs" / "process.toml"
    assert _push(scaffold) == "human"
    assert policy.read_text(encoding="utf-8").startswith("#"), "header kept"
    assert not (scaffold / "docs" / "push-policy").exists(), "one policy home"


def _bootstrap(tmp_path, *extra):
    dest = tmp_path / "repo"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest, *extra], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return dest


def test_push_policy_flag_sets_value(tmp_path):
    dest = _bootstrap(tmp_path, "--push-policy", "agent-iteration")
    policy = dest / "docs" / "process.toml"
    assert _push(dest) == "agent-iteration"
    assert policy.read_text(encoding="utf-8").startswith("#"), "header kept"


def test_push_policy_explicit_human_matches_default(tmp_path):
    dest = _bootstrap(tmp_path, "--push-policy", "human")
    assert _push(dest) == "human"


def test_ci_floor_runs_on_iteration_branch():
    # The shipped CI triggers include the llm/** iteration-branch pattern so
    # the process floor runs remotely on agent legs too.
    ci = (KIT / "ci" / "check.yml").read_text(encoding="utf-8")
    assert '"llm/**"' in ci


def test_log_template_states_sha_citation_rule():
    # Scrub/collation rewrite iteration-branch SHAs, so the durable record
    # cites stable ids — the log template is the rule's single home.
    log = (KIT / "LOG.template.md").read_text(encoding="utf-8")
    assert "stable ids" in log
    assert "SHA" in log
