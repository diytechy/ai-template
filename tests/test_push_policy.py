"""Push authority as declared policy (Thread 40, process-options.md "Agent
iteration branch & sync").

Who may publish (`git push`) is `policy.push` in `docs/config.toml`: `human`
(default — an agent never pushes, even if asked mid-session; it prepares the
branch and requests), `agent-iteration` (only the scrubbed llm/<branch>
iteration branch), or `agent`.

**Until P14 it was the one-word `docs/push-policy`, scaffolded into every repo
by a `--push-policy` flag.** File, template and flag are deleted, so the three
tests that drove them are gone with the feature rather than kept green against
nothing; what stands in their place is the assertion that the scaffold no
longer lays a SECOND source down beside the canonical one. The CI trigger and
the log template keep their one-line pieces of the ritual. The scrub/collate
steps themselves are LLM judgment verified by recorded §5 verdicts, not pytest
(the honesty stance the thread spec states).
"""

from conftest import KIT, SCRIPTS, run_py


def test_no_scaffold_lays_down_the_retired_push_policy_file(scaffold):
    # The successor default lives in config.py's SCHEMA (`policy.push =
    # "human"`), so publication is still a deliberate human act by default —
    # it is simply declared in one place now. A scaffolded `docs/push-policy`
    # beside a scaffolded `docs/config.toml` would be exactly the mixed-source
    # state `config.mixed_source_findings` refuses.
    assert not (scaffold / "docs" / "push-policy").exists()
    assert not (KIT / "push-policy.template").exists()


def test_the_retired_scaffold_flag_is_gone(tmp_path):
    # Driven rather than grepped: argparse must REFUSE the flag. A flag that
    # silently parsed and did nothing would be the worse failure — an adopter
    # would believe they had declared a policy.
    proc = run_py(
        [
            SCRIPTS / "bootstrap.py",
            "--dest",
            tmp_path / "repo",
            "--push-policy",
            "agent",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    assert "--push-policy" in (proc.stderr + proc.stdout)


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
