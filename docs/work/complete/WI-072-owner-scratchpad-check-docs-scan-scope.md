+++
id = "WI-072"
title = "OWNER_SCRATCHPAD + check_docs scan-scope (archive/scratchpad)"
workstream = "scripts"
sr_refs = ["SR-158"]
needs = ["WI-013"]
order = 71
+++

## Deliverable

FB3+FB4 (owner-feedback-2026-07-11): shipped root OWNER_SCRATCHPAD.md (meta) + OWNER_SCRATCHPAD.template.md (byte-identical, 651 B) scaffolded via bootstrap MAPPING - a loud owner-only header (LLM agents must not read/index/summarize/cite/act; working surfaces are status.md/registries/log.md; secrets floor still scans it, not a secrets-safe zone) then an empty notes area. check_docs.py: SCRATCHPAD dropped from doc discovery entirely (the WI-066 okf-exclusion idiom - links, orphans, stale hints); ARCHIVE_DIR (docs/archive) KEEPS broken-link validation but is dropped from orphan warnings + stale-mtime hints (_in_archive; frozen-history scan-scope). Agent-side ignore: meta CLAUDE.md one-liner; AGENTS.template.md UNTOUCHED (9,978 B - no clean sub-22-byte fold worth diluting a durable working-agreement rule), reinforcement line went to PROCESS_OPTIONS 7 memory/scratch discussion + kit README Contents row. No SR-012 text change: the scratchpad + archive scope are scan-scope within SR-012's existing claim (the WI-066 precedent). Meta run: stale hints 27->0 (all were archive docs), orphan warns 1->1 (docs/test/report.md, unchanged). Tests: test_check_docs.py (scratchpad-exempt, archive-broken-link-fails, archive-not-orphan-but-live-is, find_stale-skips-archive unit, archive-stale-suppressed-end-to-end) + test_bootstrap.py (file list + scaffolds-owner-scratchpad byte-identity).
