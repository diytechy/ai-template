# External skill sources — a curated reference index

Third-party **agent-skill** collections a downstream adopter might mine for
domain expertise or workflow accelerators the kit itself does not ship. This is a
**reading list, not a dependency list**: the kit vendors none of these, endorses
none, and pins none. Evaluate each yourself before use.

Read it alongside the skills subsystem's own plug-in contract
([`skills/README.md`](skills/README.md), *"Future external skill sources"*) — the
same trust rules apply.

**One exception exists, ruled rather than mined.** `skills/antidote/` IS
vendored — verbatim, license-cleared, source-commit-pinned — per an explicit
owner ruling (OI-58, WI-507); its row lives in
[`docs/dependencies.md`](../docs/dependencies.md), the ledger every entered
dependency owes. It is not listed as a source below because it did not come
through this page's mine-don't-install triage: it is the one case the "vendors
none of these" rule above does not cover.

## How to use this list

Three rules govern every entry, without exception:

1. **Mine, don't install.** A skill is *instructions an agent will follow* — a
   prompt-injection surface. Every source below also ships an installer, an
   `npx`/CLI runner, or a live in-editor tool; the kit's stdlib-only,
   install-nothing posture means you **read and adapt** the useful prose into
   your own `skills/` source, never wire a third-party runner into your gate or
   dispatcher. A fetched skill is materialized only on explicit selection and
   stays reviewable, diffable text in the PR that adds it (`skills/README.md`,
   *Trust*).
2. **License decides copy-vs-link.** An MIT / Apache-2.0 source can be *mined*
   into your repo **with attribution and a pinned commit**; a CC-BY source
   carries an attribution obligation that propagates; a source with **no
   license**, or one that is *source-available but not open-source*, can only be
   **linked**, never copied. The License column is the gate — check it before you
   paste anything.
3. **Discount the star counts.** The 2026 "skills" popularity wave inflates star
   and fork numbers; treat them as reach, not as evidence of review rigor or
   correctness. Judge the actual content.

## Referenced sources

| Source | Role / domain | Format | License | Reference for / what to mine (caveat) |
|---|---|---|---|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | UI/UX, front-end legibility | portable `SKILL.md` | MIT | A mandatory, *mechanical* visual pre-flight — contrast, dark-mode theme-lock, viewport-fit, readable-string audit — worth distilling (stack-neutral) into a UI/legibility review rubric. Strip its Tailwind class names and aesthetic dogma; keep the checkable floors. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX generation | code + data package (heavy) | MIT | A pre-delivery contrast/typography checklist worth mining as prose. The Python search engine + CSV databases are far too heavy to vendor — take the checklist, leave the machinery. |
| [obra/superpowers](https://github.com/obra/superpowers) | Dev workflow / review discipline | portable `SKILL.md` (multi-harness) | MIT | Closest to this kit's own turf. Mine `verification-before-completion`, the `requesting-code-review` severity/blocking model, and the subagent two-stage review as *cross-checks* against your gate discipline — do not wholesale-adopt (it overlaps the kit's gates and carries a prescriptive TDD/worktree stance). |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) — Legal suite | Regulated-domain reviewer "hat" | Claude/Cowork plugin (`SKILL.md` + `.mcp.json`) | Apache-2.0 | An exemplar of a **domain reviewer hat**: playbook-driven review with GREEN/YELLOW/RED flags and escalation gates *before anything is relied on* — the same "gates-before-reliance" shape as this kit's review/attestation loop. Borrow the pattern, not the packaging; it reviews contracts, not code. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Marketing / growth / copy | portable `SKILL.md` (agent-neutral) | MIT | A broad, well-maintained marketing-domain pack (CRO, copywriting, SEO, analytics) for a team that ships a product *and* markets it. Orthogonal to the process core — reference, don't fold in. |
| [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills) | Social / creator content | portable `SKILL.md` | MIT | A narrower creator/personal-brand pack (post-writing, scoring drafts against real engagement). *Caveat:* several skills require paid third-party APIs (scraping, image/video keys) — a real cost and credential surface; mine the prose, not the wiring. |
| [WH-2099/mermaid-skill](https://github.com/WH-2099/mermaid-skill) | Mermaid diagram authoring | portable `SKILL.md` + per-type references | MIT | The one source here whose payload is *upstream documentation, not opinion*: a thin router `SKILL.md` over ~40 reference files that a scheduled GitHub Action re-syncs verbatim from `mermaid-js/mermaid` `docs/syntax` + `docs/config`. Relevant because the kit's own authored diagrams are mermaid under a structural contract (`check_flows.py`, IF-029) and the failure mode is silent — a fence with bad syntax renders as nothing, not as an error. **Install it per-developer, never into `skills/`:** at ~620 KB it dwarfs the whole kit skill set, and `.claude/skills/` is a byte-identical fan-out of `skills/` policed by `gen_skills_index.py --check-agents`, so a copy there is drift by construction. Prefer `~/.claude/skills/mermaid/` (a `skills-dir` plugin). Nothing in the kit's gate may depend on it. |
| [upstash/context7](https://github.com/upstash/context7) | Current library docs at build time | MCP server + CLI (external service) | MIT (client only; backend closed) | The one *build-quality* lever here: current, version-specific API docs → fewer hallucinated or deprecated calls. **Caveat, the sharpest on this list:** a **hosted external service** with a closed, unauditable backend; lookup queries **leave the machine**. Opt-in per developer only; **never** a hard dependency of a kit script or gate (that breaks the offline/stdlib bar). |
| [anthropics/skills](https://github.com/anthropics/skills) | The `SKILL.md` format itself | official reference implementation | Apache-2.0 (split) | Cite as the **authoritative Agent-Skills / `SKILL.md` format provenance** (the same shape this kit's `skills/` use) and for its `skill-creator`. Its capability skills are orthogonal task tools, not process/quality skills. *Caveat:* the four document skills (`docx`/`pdf`/`pptx`/`xlsx`) are **source-available, not open-source** — do not redistribute them. |

## Evaluated and not listed

Kept honest — an audited exclusion, not a silent omission:

- **[Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev)** —
  **no license** in the repo (all-rights-reserved → link-only, uncopyable) and
  paywalled; CSS motion snippets are off-target for a process/quality kit.
- **[rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all)** —
  a single skill-authoring meta-skill (CC-BY, attribution propagates); tangential
  to gated delivery, and the kit already owns skill authoring
  ([`skills/README.md`](skills/README.md) + `gen_skills_index.py`).
- **knowledge-work-plugins — Finance** — a real accounting-ops toolkit, but its
  only thread to software delivery (`/sox-testing` compliance workpapers) is thin;
  a fintech adopter can still reach it in the repo linked above.
- **knowledge-work-plugins — Small Business** — payroll / CRM / month-end
  business operations; no tie to engineering a software product.

---

*This index is a snapshot; sources move, re-license, and go stale. Re-verify a
source's license and maintenance before mining it. Nothing here is endorsed or
supported by the kit.*
