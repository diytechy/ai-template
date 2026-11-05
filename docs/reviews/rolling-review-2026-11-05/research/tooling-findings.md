# External research brief — FINAL (2026-11-05) — reviewer: external-research
Structured version returned to the lead via StructuredOutput; this file is the durable copy.

## Headline findings (severity, anchor)
HIGH F1 Shipped CI clones at depth 1 while the floor fails closed on shallow history — project-trajectory/ci/check.yml:46 (no fetch-depth) vs .github/workflows/test.yml:70,108,141 (fetch-depth: 0). Repro: depth-50 clone -> approval-fresh, registry-integrity, open-items FAIL ("NOT byte-identical ... at 37bcca3b, the commit that last wrote it"); 9 other findings in the same run correctly say "unverifiable - its landing lies past this shallow clone's history". Three shallow readers: baseline_snapshot.py:2060, retire.py:574, check_test_first.py:211.
HIGH F2 The commit hook is a whole-repo presubmit — hooks/pre-commit:287-288 (25 steps, no file scoping; only ruff at :326 is staged-scoped). Measured 28.0 s wall / 63.4 s CPU on 4 cores; trajectory 27.9 s, trajectory-map 19.8 s, open-items 12.7 s, registry-integrity 10.1 s, approval-fresh 5.9 s.
HIGH F3 Permanent advisories printed per row on the floor — check.py:140-142, 765-768, 911-912; 350 of 497 lines WARN; 128+30+20 from three per-row classes. ESLint: warn is transitional to error; a never-failing class is a report.
MED F4 Three ratchet representations with opposite improvement policies — check_complexity.py:448-463 (improvement FAILS: "RE-STAMP DOWNWARD ... in this same commit"), flag_axis.py:136-139 (improvement silent, WARN on rise), tests/test_module_size_ratchet.py:122 (BASELINE = {...} dict literal). Betterer auto-updates on improvement; ESLint keys by file+rule count (service.js:24 typedef; zero "line" mentions).
MED F5 Downstream update is 644 KB of prose — RESYNC_PACK.md 643,982 B; bootstrap.py:565 copy_if_new, :682-699 --sync force-overwrites and deletes. Copier/Cruft: stamped answers file + declared skip class + regenerate-and-diff with conflict markers + independent templates composed via separate answers files.
MED F6 Provenance frames in code/skills vs AGENTS.template.md:182-184; detector trace_text.py:692 covers spine cells only. 1,842 WI citations; 90/122 modules >1; 42 files "owner ruling"; check.py 741/2878 comment lines.
MED F7 Owner rulings have no immutable numbered record — decisions.template.toml:1-14 is per-run D-NNN; ADR practice: one record per decision, in-repo, superseded never deleted.
LOW F8 104 handoff-*.md in docs/ root; docs/iteration 46M, reviews 16M, archive 12M; no owner/freshness marker (SWE-book ch.10; git-sizer).
LOW F9 PROCESS.md (14,092 words) / PROCESS_OPTIONS (199,478 B) mix reference and explanation (Diataxis: reference "should be austere").
LOW F10 No single severity table; strict promotions hand-wired (check.py:501, 577-622, 1905). rustc builtin lints by default level (my regex): Allow 38 / Warn 80 / Deny 37 / Forbid 0.

## Ranked changes
1 one shallow-history policy (WARN unverifiable; FAIL only when a truncated answer is confidently wrong) + fetch-depth: 0 in shipped ci/check.yml
2 split the hook: staged-scoped fast steps at commit, whole-repo generators + history checks at pre-push/CI; per-class WARN summary with counts
3 one kitlib.ratchet: count-per-file(+rule) TSV, auto-tighten on improvement, fail on regression, --prune/--restamp; retire dict-literal test baselines
4 declarative ownership manifest + 3-way bootstrap --update; layers as independently stamped templates; RESYNC_PACK -> judgement entries only
5 provenance sweep + detector over .py/SKILL.md; ADR-shaped immutable rulings; explanation split out of PROCESS.md

## Not reached (DNS blocked in this session; substitutes used)
eslint.org, doc.rust-lang.org, docs.astral.sh, flake8.pycqa.org, pre-commit.com, abseil.io, copier.readthedocs.io, cruft.github.io, engineering.atspotify.com, kernel.org, google.github.io, diataxis.fr, cognitect.com, thinkrelevance.com, martinfowler.com, faq.arc42.org, setuptools-scm.readthedocs.io, gitversion.net, docs.sonarsource.com, community.sonarsource.com, web.stanford.edu, dev.to, notion.com, medium.com, docs.github.com, android.googlesource.com, sites.google.com, lore mirror, blog.codercops.com, *.github.io. GitHub-hosted sources were read from github.com / raw.githubusercontent.com (gh api is not enabled for unattached repos). Primary texts not obtained: Ousterhout APoSD ch.13, Clean Code ch.4, Nygard 2011 article, Spotify golden-paths post, Notion ratchet post, SonarQube docs, hook-latency blogs (snippets only).

## Reproduction commands
cd <scratch>/clone && time python3 project-trajectory/scripts/check.py --run-steps okf,trajectory-map,status-map,open-items,component-view,cli-reference,interface-reference,trajectory,registry-integrity,derived-stage,skills-sync,skills-index,prompt-catalog,verdict-rollup,approval-fresh,approval-immutable,staged-divergence,held-status,reserved-ids,ruling-sync,text-then-act,parent-first,done-when-blessed,plan-gate,adoption-record > hook-run.log  # real 0m27.998s user 1m3.371s
grep -c WARN hook-run.log  # 350 ; wc -l -> 497
git clone --depth 50 file:///home/user/ai-template shallow && cd shallow && python3 project-trajectory/scripts/check.py --run-steps approval-fresh,registry-integrity,open-items  # exit 1, 3 FAIL
curl -sS -L https://raw.githubusercontent.com/rust-lang/rust/master/compiler/rustc_lint_defs/src/builtin.rs | grep -cE "^\s+(Allow|Warn|Deny|Forbid),\s*$"  # 38/80/37/0
