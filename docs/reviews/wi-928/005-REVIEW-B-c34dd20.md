Reviewed: c34dd2067dd47adf6d47cb271d1e6b9ab2d884d7

Verified. Full-lane review, convergence stance, of 8c72559ed..c34dd2067 against WI-928's spec, its Done-when, LLR-300, TC-339, SR-229, SR-237 and the kit-change rubric (K1-K4, B1). I read no earlier verdict, decision record or lane commit message. Pre-fix code came from the range diff and from `git log -p --format=%h`.

Failure classes hunted, worst first:
1. Fail-open on a kept form: an ordinary capture or a reserved-word, prefix or substitution launch that stops being denied.
2. A false denial of a harmless quoted mention, which is the property the quote-aware reading exists to keep.
3. Requirement text that no longer matches the code (K1).

I drove the real `coordinator_guard.command_words` on this checkout with 38 probe lines (script at C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/wi-928/gate-opus/probe/probe.py).

- Every kept form is still denied: `$r = claude -p x`, `$r=claude -p x`, `$r=claude -p 'x y'`, `[string]$r='a'; claude`, `$a, $b = claude`, `$r ??= codex`, `$r +=claude`, `$r = "$(claude -p x)"`, `$r = $(claude -p x)`, `$r = & claude`, `time claude`, `env -i claude`, `env -u A FOO=1 claude`, `timeout -s KILL 5 claude`, a backtick substitution inside double quotes, and the line after an unquoted or `<<-` here-document body. An unclosed `@"` here-string is still unreadable and denied.
- These are still allowed: `$x -match 'a=claude'`, `$r=''`, `$r= ''` and `echo 'pause; claude notes'`.
- The removed forms are no longer recognised: `time -p`, `coproc`, `env -S`, `. claude`, `$a = $b = claude`, and here bodies.

By reading the code, the new denial set can only shrink, never grow:
- `_operator_end` now accepts only the leftmost operator, and only when it ends at or before the word's first quoted piece. That match is also the old reading's first unquoted match, so no line that was allowed before is denied now.
- `_right_hand`, the heredoc and here-string branches, and `_past_prefix` each only lose branches.
- `_tail` rebases `quote_start` so it is never negative.

Done-when coverage:
1. Removed names: `git grep` for `_invoked|_GRAMMAR_WORDS|_past_grammar|_NO_SHAPE|_expansions|.spans|.quoted(|_split_string` under project-trajectory/ prints nothing. Inspection.
2. Flat reserved-word set: project-trajectory/scripts/coordinator_guard.py:931 is one frozenset that contains `time` and not `coproc`, and `_segment_command` (line 1092) skips it. Pinned by `time claude -p x` in QUOTED_DENIED.
3. Test lists: I checked every case the spec lists as deleted (absent) and as kept (present) by fixed-string search, and DENIED, ALLOWED and UNREADABLE are unchanged. The lane also adds eleven QUOTED_DENIED pins, one per reserved word plus two backtick substitutions. They pin the enumerated set, not a fixed defect, so no red-before is owed. Covered by test_a_quoted_launch_form_is_denied, test_a_quoted_operator_is_not_a_command_boundary and test_the_one_reading_keeps_quoted_text_in_its_word.
4. The bound: `launch_reason`'s docstring states the enumerated set, the default and the residue. A grep of project-trajectory/, AGENTS.md, the registries, skills and tests for coproc, dot invocation, split string and `env -S` hits only that docstring and the WI-834 history entry. Inspection.
5. Spine: the spec's LLR-300 sentence block appears verbatim in `detail`, and `code_symbol` drops `_invoked`. TC-339's `method` and `expected` match the spec and no status flipped (K3). The live LLR-300 and TC-339 equal their docs/archive/last_approved snapshots under act 124 (re-attested LLR-300 and TC-339). The amended text matches the code (K1), and no SN or SR cell is touched (K2). `check_trajectory --strict` and `trace --strict-integrity` are clean.
6. RESYNC entry: present, and it names both kit-owned files, the blackout arming and "nothing needs migrating". Its anchor is stale; see the finding.
7. The bar: the four named test modules pass. The round facts said not to run the smoke tier, the smoke-budget check or test_bootstrap.py, so for this round those parts are UNVERIFIED, not failed.

Counterpart decisions:
- SR-229 is retained. It covers claim admission and the lease and names no shell form.
- SR-237 is retained. "Starting no model work" rests on each kit launch point's own refusal, and the hook is supervision.
- IF-274 and IF-275 are retained. The payload and denial shape are unchanged: `launch_reason` still reads `tool_input.command` and still returns the same reason strings.
- There is no decomposition. No child row was added or split.

Commands:
- `git rev-parse HEAD`: c34dd2067dd47adf6d47cb271d1e6b9ab2d884d7
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/wi-928/gate-opus/wi-928 tests/test_blackout_window.py tests/test_blackout_isolation.py tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py` (through lowprio.py): `174 passed, 1 skipped in 14.78s`. The skip is the environment-gated posix-shell test.
- `python project-trajectory/scripts/check_trajectory.py --strict`: `check_trajectory: clean (934 work item(s), 813 done (87%), 30 cancelled, graph acyclic).` rc=0
- `python project-trajectory/scripts/trace.py --strict-integrity`: `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ...` rc=0
- `python probe/probe.py <lane>`: the 38 shell-line probes, results as summarised above.
- `git status --short`: clean afterwards. No file in the worktree was changed.

- [MINOR] project-trajectory/RESYNC_PACK.md:8554 -> The new entry is anchored `[since 785b29e11]` and its line 8556 says "Anchored at the preceding commit". The lane's base is 8c72559ed, five trunk commits later, so 785b29e11 does not precede the change. The entry also sits after the WI-930 entry `[since 1a182d154]` while carrying an older sha, which breaks the pack's oldest-first order. An adopter stamped at any of the five commits in between would have the entry fall outside their range and skip it. The harm is bounded: the entry asks only to overwrite two kit-owned files, which a resync does anyway, and nothing needs migrating. (K4) -> re-anchor the heading at the landing's parent, as the coordinator-cycle landing recipe already states -> @owner

VERDICT: APPROVE findings=1
