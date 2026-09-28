"""Verifies SR-223 / LLR-280 / IF-253 (TC-290): a guardrails payload is selected
per model-name substring.

A repository may vendor `docs/guardrails/core.<substring>.md` beside its default
`core.md`. A guarded session whose model name contains that substring gets the
payload instead of the core, the longest matching substring winning, by the
same matcher the guardrails policy uses; a model matching none gets the core.
Whether a session is guarded at all stays the policy's decision. The kit
itself ships no payload, so it names no model to the selector. In-process:
the vendored set is planted under tmp_path and the selector and the prompt
composer are called directly; the shipped set is read from the kit's own
delivery inventory, with no scaffold run.
"""

import re
import tomllib

from conftest import KIT, ROOT, load_script

KIT_CORE = "<!-- BEGIN KIT CORE -->\n{}\n<!-- END KIT CORE -->\n"


def _vendor(root):
    gdir = root / "docs" / "guardrails"
    gdir.mkdir(parents=True)
    (gdir / "core.md").write_text("DEFAULT-CORE\n", encoding="utf-8")
    (gdir / "core.sonnet.md").write_text("BROAD-PAYLOAD\n", encoding="utf-8")
    (gdir / "core.claude-sonnet.md").write_text(
        "upstream noise\n" + KIT_CORE.format("NARROW-PAYLOAD"), encoding="utf-8"
    )


def test_the_longest_matching_substring_selects_the_payload(tmp_path):
    al = load_script("agent_loop")
    _vendor(tmp_path)
    narrow = al.guardrails_core(tmp_path, "claude-sonnet-5")
    assert "NARROW-PAYLOAD" in narrow and "noise" not in narrow
    assert al.guardrails_core(tmp_path, "vendor-sonnet-6") == "BROAD-PAYLOAD"
    assert al.guardrails_core(tmp_path, "claude-opus-4-8") == "DEFAULT-CORE"
    assert al.guardrails_core(tmp_path) == "DEFAULT-CORE"


def test_a_guarded_session_carries_its_payload_and_the_policy_still_decides(
    tmp_path,
):
    al = load_script("agent_loop")
    _vendor(tmp_path)
    prompt, guarded = al.compose_session_prompt(
        "claude-sonnet-5", "BODY", "", "all", tmp_path, []
    )
    assert guarded and prompt.startswith("<!-- BEGIN KIT CORE -->")
    assert "NARROW-PAYLOAD" in prompt and "DEFAULT-CORE" not in prompt
    # A matching payload never guards a session the policy leaves unguarded.
    prompt, guarded = al.compose_session_prompt(
        "claude-sonnet-5", "BODY", "", "all except sonnet", tmp_path, []
    )
    assert not guarded and "PAYLOAD" not in prompt


def test_the_kit_ships_no_payload_so_every_model_gets_the_default_core(tmp_path):
    # The selector reads model-name substrings only from payload file names, so
    # a kit that ships no `core.<substring>.md` names no model to it. Pinned
    # over the delivered-package universe (every physical kit source, every
    # MAPPING, conditional and generated destination) and this repository's
    # own guardrails directory, then over the selector itself: with only the
    # default core present, every model the kit's roster template names gets
    # that core, so no model is special-cased in code either.
    boot = load_script("bootstrap")
    al = load_script("agent_loop")
    payload = re.compile(r"(^|/)core\.[^/]+\.md$")
    sources, _exclusions, conditional, generated = boot.delivery_inventory()
    shipped = sorted(p for p in sources if payload.search(p))
    assert shipped == [], shipped
    destinations = [dst for _src, dst, _ref in boot.mapping_entries()]
    destinations += [dst for _src, dst in conditional + generated]
    assert [d for d in destinations if payload.search(d)] == []
    assert sorted((ROOT / "docs" / "guardrails").glob("core.?*.md")) == []
    gdir = tmp_path / "docs" / "guardrails"
    gdir.mkdir(parents=True)
    (gdir / "core.md").write_text("DEFAULT-CORE\n", encoding="utf-8")
    roster = tomllib.loads((KIT / "agents.template.toml").read_text(encoding="utf-8"))[
        "agent"
    ]
    models = [r["model"] for r in roster.values()]
    models += ["{}-{}".format(r["model"], r["version"]) for r in roster.values()]
    assert models
    for model in models:
        assert al.guardrails_core(tmp_path, model) == "DEFAULT-CORE", model
