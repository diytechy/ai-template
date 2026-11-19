"""HANDOFF 4.3 / 10.4, human: hand edits after r43a_human.py.

1. The push value's meaning widened (trap 14): `operator` lets a session the
   operator delegated the push to publish, where `human` excluded even an
   attended one. "An agent never pushes, even if asked" is reworded wherever
   it describes the default.
2. Role uses a keep pattern held back: the open-items page is the operator's
   ruling surface, not a page "a human reads".
3. The policy file's note on who the operator may be on a held rung.
4. The migrator's new step (push = "human" -> "operator") in its spine rows.
"""

SKILL = (
    "project-trajectory/skills/gate-advance/SKILL.md",
    ".claude/skills/gate-advance/SKILL.md",
    ".agents/skills/gate-advance/SKILL.md",
)
POLICY = ("project-trajectory/process.toml.template", "docs/process.toml")

EDITS = [
    # 1. push: the default's meaning widened
    (POLICY,
     '#   "operator"           the default: an agent never pushes, even if asked\n',
     '#   "operator"        the default: the operator pushes, or a session they\n'
     "#                     delegated the push to; never the loop, and never an agent\n"
     "#                     merely asked mid-session\n"),
    ("project-trajectory/push-policy.template",
     "#   operator           — the default: an agent never pushes, even if asked\n"
     "#                     mid-session; it prepares the branch and requests a push.\n",
     "#   operator        — the default: the operator pushes, or a session they\n"
     "#                     delegated the push to; any other agent prepares the branch\n"
     "#                     and requests a push, even if asked mid-session.\n"),
    ("project-trajectory/PROCESS_OPTIONS.md",
     "- **`operator`** *(default)* — the agent **never pushes, even if asked\n"
     "  mid-session**; it prepares the branch and requests the push. Publication is\n"
     "  a deliberate operator act, immune to hook/tool circumvention by construction;\n"
     "  the operator is a cheap bottleneck, because pushing is rare and takes seconds.\n",
     "- **`operator`** *(default)* — the operator pushes: a person, or a session\n"
     "  that person delegated the push to, with the delegation recorded. Any other\n"
     "  agent **never pushes, even if asked mid-session**; it prepares the branch and\n"
     "  requests the push. Publication is a deliberate operator act, immune to\n"
     "  hook/tool circumvention by construction; the operator is a cheap bottleneck,\n"
     "  because pushing is rare and takes seconds.\n"),
    ("project-trajectory/PROCESS.md",
     "assumed: the `[policies] push` dial (default **`operator`** — an agent never\n"
     "pushes, even if asked mid-session; it prepares the branch and requests). A\n",
     "assumed: the `[policies] push` dial (default **`operator`** — the operator, or\n"
     "a session they delegated it to; no other agent pushes, even if asked\n"
     "mid-session: it prepares the branch and requests). A\n"),
    ("project-trajectory/scripts/bootstrap.py",
     "declares who may publish (`git push`): `operator` (the scaffolded default — an\n"
     "agent never pushes, even if asked mid-session; it prepares the branch and\n"
     "requests), `agent-iteration` (only the scrubbed llm/<branch> iteration\n",
     "declares who may publish (`git push`): `operator` (the scaffolded default —\n"
     "the operator, or a session they delegated it to; no other agent pushes, even\n"
     "if asked mid-session), `agent-iteration` (only the scrubbed llm/<branch> iteration\n"),
    ("project-trajectory/scripts/bootstrap.py",
     '        "default: an agent never pushes; it prepares the branch and requests).",\n',
     '        "default: only the operator, or a session they delegated it to, pushes).",\n'),
    (SKILL,
     "point — but *pushing* follows the `push` dial (default `operator`: an agent never\n"
     "pushes; the operator publishes at leisure).\n",
     "point — but *pushing* follows the `push` dial (default `operator`: the operator,\n"
     "or a session they delegated it to, publishes at leisure).\n"),
    ("docs/knowledge/security-review.md",
     '  answers. Publishing is operator: `docs/process.toml` sets `push = "operator"` (an\n'
     "  agent never pushes, even if asked).",
     "  answers. Publishing is the operator's: `docs/process.toml` sets\n"
     '  `push = "operator"` (no other agent pushes, even if asked).'),
    ("tests/test_push_policy.py",
     "into every repo: `operator` (default — an agent never pushes, even if asked\n"
     "mid-session; it prepares the branch and requests), `agent-iteration` (only the\n",
     "into every repo: `operator` (default — only the operator or their delegate\n"
     "pushes, even if asked mid-session), `agent-iteration` (only the\n"),
    ("tests/test_push_policy.py",
     "    # The scaffolded authority is `operator` — an agent never pushes — so every\n",
     "    # The scaffolded authority is `operator` — no undelegated agent pushes — so every\n"),
    (".github/workflows/lock-check.yml",
     '# "operator"` states the repo-wide rule this would otherwise cut against ("an agent\n'
     '# never pushes, even if asked"), and the 2026-08-18 staged-divergence step\n',
     '# "operator"` states the repo-wide rule this would otherwise cut against (only the\n'
     "# operator or their delegate pushes), and the 2026-08-18 staged-divergence step\n"),
    # 2. the open-items page is the operator's ruling surface
    ("project-trajectory/scripts/gen_open_items.py",
     "the ONLY surface a human reads", "the ONLY surface the operator reads"),
    ("project-trajectory/scripts/gen_open_items.py",
     "document a human reads", "document the operator reads", 2),
    ("tests/test_gen_open_items_render.py",
     "the one document a human reads", "the one document the operator reads"),
    ("tests/test_gen_open_items_render.py",
     "the one document an\n    operator reads", "the one document the\n    operator reads"),
    ("tests/test_module_size_ratchet.py",
     "the surface a human reads", "the surface the operator reads"),
    ("project-trajectory/scripts/dispatch.py",
     "that a human reads it rather", "that the operator reads it rather"),
    ("tests/test_verdict_record.py",
     "read by humans deciding", "read by the operator deciding"),
    # 3. who the operator may be on a held rung
    (POLICY,
     '# WHO "THE OPERATOR" ABOVE MAY BE on a held rung (the owner, and which sessions\n'
     "# may take the owner's act) is stated once, with its enforcer, in process.md\n",
     "# WHO THE OPERATOR MAY BE on a held rung (a person, and which sessions may\n"
     "# take the act for them) is stated once, with its enforcer, in process.md\n"),
    # 4. the migrator's spine rows
    ("docs/requirements/low-level-requirements.toml",
     "POLICY_TABLES/POLICY_KEYS/_policy_table",
     "POLICY_TABLES/POLICY_KEYS/POLICY_VALUES/_policy_value/_policy_rest/_policy_table"),
    ("docs/requirements/low-level-requirements.toml",
     "and POLICY_KEYS maps, within a table, an earlier key to the current one.",
     "and POLICY_KEYS maps, within a table, an earlier key to the current one. "
     "POLICY_VALUES maps, within a table and a key, an earlier string value to the "
     'current one, as push = "human" to "operator" in [policies]; _policy_value '
     "applies it to a parsed value and _policy_rest to the one-line quoted value of "
     "a key line."),
    ("docs/test/test-cases.toml",
     "one writing the dial as an inline table or a dotted key, and one already current;",
     "one writing the dial as an inline table or a dotted key, and one already "
     "current; a policy file whose push authority reads the earlier default, with "
     "the same key under another table and with each current value, and one writing "
     "it as an inline table or a multi-line string;"),
    ("docs/requirements/system-requirements.toml",
     "and a table and a key of the policy file.",
     "and a table, a key and a value of the policy file."),
]
