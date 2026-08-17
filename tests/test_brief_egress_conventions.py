"""The push-channel egress conventions, as a standing sweep (SR-175 / LLR-176).

SR-175 (C-DPR-3, ruled at sitting-3 SS0.4 item 8, 2026-08-17): the loop's brief
composers keep a real inclusion discipline -- no commit authorship is ever
formatted into a prompt -- that until this row was held in place by nothing but
the code itself. The WI-468 intake measurement swept the prompt path for
authorship tokens and found zero hits; this module turns that one-time
measurement into a bar, so a composer that starts formatting `%an`/`%ae` into
a brief fails here rather than shipping quietly. The functional half of TC-171
(a sentinel planted in status.md/log.md never reaches the planning surface)
lives in test_plan_briefs.py.

The sweep asserts the ABSENCE CLASS, not any particular formatting: every
prompt-composing module and every shipped prompt template is scanned, so a new
template joins the bar by default without editing this file.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "project-trajectory" / "scripts"
PROMPTS = REPO / "project-trajectory" / "prompts"

# The modules that compose content for dispatch to an external model runner
# (LLR-176's enumerated composing path).
COMPOSING_MODULES = (
    "agent_loop.py",  # worker_prompt / critique_brief
    "plan_briefs.py",  # the dual-plan round's allowlist surface
    "adjudicate_brief.py",  # compose: spec + report + oneline/name-status logs
    "intake.py",  # context_block
    "prompts.py",  # the template loader/renderer
)

# Authorship egress tokens: git pretty-format authorship fields, the --author
# selector, and the two subcommands whose default output embeds authorship.
AUTHORSHIP_TOKENS = re.compile(r"%an|%ae|%ad|--author\b|git blame|git show\b")


def test_no_authorship_token_in_the_prompt_composing_path():
    surfaces = [SCRIPTS / name for name in COMPOSING_MODULES]
    templates = sorted(PROMPTS.glob("*.md"))
    assert templates, "no shipped prompt templates found -- sweep would be vacuous"
    surfaces += templates
    hits = []
    for path in surfaces:
        assert path.exists(), "composing surface missing: {}".format(path)
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if AUTHORSHIP_TOKENS.search(line):
                hits.append(
                    "{}:{}: {}".format(path.relative_to(REPO), lineno, line.strip())
                )
    assert not hits, (
        "authorship egress token(s) in the prompt-composing path "
        "(SR-175: the brief-inclusion rule excludes commit authorship):\n"
        + "\n".join(hits)
    )
