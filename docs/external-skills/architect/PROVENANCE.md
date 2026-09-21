# Review candidate — Architect

Status: unapproved external review copy; not a shipped or materialized kit skill.

- Marketplace listing: https://mcpmarket.com/tools/skills/architect
- Marketplace author: violetio
- Resolved source: https://github.com/violetio/gstack
- Source path: plan-eng-review/SKILL.md
- Pinned source commit: bb46ca6b217e5732f8c0b9458ebecb4c90c382ad
- License: MIT, copied as LICENSE in this directory.
- Upstream provenance: Violet's repository is a fork of garrytan/gstack.

## Why this is review-only

The marketplace calls this skill "Architect," while the source names it
"plan-eng-review." Its useful subject is pre-implementation architecture and
feasibility review, but it is not portable as-is:

- it requires the Claude-specific AskUserQuestion tool and a gstack update
  checker;
- it assumes a gstack/Bun installation and other gstack skill files;
- it hard-codes JavaScript/Rails test expectations, TODOS.md, and ASCII-diagram
  preferences;
- its T-shirt sizing and per-issue interactive prompts are preferences, not the
  kit's authority or traceability model.

If it is later adapted, start from the existing architecture, planning, and
adjudication homes rather than adding a competing gate. Keep only behavior that
has a clear trigger, landing surface, and verification story.
