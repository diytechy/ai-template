+++
id = "WI-069"
title = "Pair-row agent registry - Family/Env + version-less resolution"
workstream = "unattended"
sr_refs = ["SR-154", "SR-155"]
needs = ["WI-059"]
order = 67
+++

## Deliverable

C3 (2026-07-11): the pair-row registry ("pairs now, factor later"). agents.csv columns become Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes - one row = one (model x route) pair, the table itself the allow matrix. IDENTITY (Family/Model/Version) vs ACCESS (CmdTemplate + Env); Provider retired (legacy Provider read as Family, never-breaking). agent_route gains parse_env (KEY=value;... merged over the launch env), load_tag_rank/parse_tag_rank (the GA>preview>beta>exp maturity vocabulary, per-registry override via a `# tag-rank:` comment or AGENT_TAG_RANK), and resolve_token/resolve_enabled: a version-less enable-list token resolves to the newest pair in its Family-Model line (exact-id else dotted-numeric then maturity-rank then date; preview/exp skipped unless named/only; equal-key route pairs by registry row order). select()'s heterogeneity + score_reviews' corroboration re-keyed on Family (a router-fronted row shares its native sibling's Family, so it is NOT diverse). agent_loop merges a selected pair row's Env into run_session (empty Env = the ambient env = today's call); second account = a second pair row (distinct id => independent cooldown by construction). SR-045 Requirement+AcceptanceCriteria extended (rides the pending G3 re-attestation); LLR-044/045 text extended. PROCESS_OPTIONS routing subsection rewritten (pair rows, version-less resolution, account/router rows, revisit trigger, LiteLLM 1.82.7/1.82.8 pin + Gemini OAuth race notes). agents.template.csv new header + compliant example rows (Model=gemini-3-pro/Version=3; commented -ACCT2 + router examples). Tests: test_agent_route.py (Family fallback, parse_env, resolver ordering incl. numeric-beats-date + preview-skip + tag-rank + multi-route registry order + exact-id + unresolvable + acct2 cooldown + router-not-diverse), test_agent_loop_env.py (Env merge + empty=ambient). Absent/legacy columns = byte-identical behavior.
