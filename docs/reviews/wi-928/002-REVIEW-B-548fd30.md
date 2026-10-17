Reviewed: 548fd30537db9ec5ed8a0469ed70a169b84d0122

## 2026-10-17 — WI-928 full-lane review (REVIEW-B, Claude Opus), range 61ee4e165..548fd3053

Rubric: docs/rubrics/kit-change-review.md (anchors K1–K4, B1). Spec of record: docs/work/active/wi-928/WI-928-blackout-drops-rare-forms.md, which I read in full. Normal stance; this is not a convergence round.

**Failure classes hunted first.** I hunted the worst classes first, in severity order:
1. Fail-open on a KEPT form. Each removal could have narrowed a form that sitting 017 or WI-834's Done-when keeps.
2. Fail-closed regressions. The narrowed `_operator_end` and `_right_hand` might now deny a harmless PowerShell line.
3. Silent loss of unreadable-line denial, other than inside bodies the row declares to be data.
4. Spine text that states something false.

**Verified.**
- I drove the real `coordinator_guard.command_words` at the base and at the head, over 71 lines (probe.py in this directory, base tree from `git archive 61ee4e165`).
- Every kept form gives the same verdict at base and head, all denied: the plain command, `FOO="two words"`, the `timeout` and `env -u/-i/--` prefixes, `time`, `!`, `if`, `while`, `{`, the chain operators, `$(...)`, backticks, double-quoted substitutions, the line after a quoted or unquoted here-document, sitting 017's assignment table (plain, typed, scoped, comma list, `+=`, `??=`, `$r=claude`), `$r = & claude`, `$r = $(claude)`, `$r = (claude)` and `&` with a quoted path.
- Every kept allowed case is also unchanged: the quoted mentions, `$r = 'claude -p x'`, `$r = $other`, `echo a = claude`, `$x -match 'a=claude'`, `function f { claude; }` and `@'` bodies.
- Only the eight removed forms flip from deny to allow: here bodies, `@"` bodies, chained assignment, `$o.'Answer'=`, dot invocation, `time -p`, `coproc` and `env -S '...'`.
- `$h['k=v'] = claude` and `$result.Answer = claude` still deny. They reach the spaced `=` word, which is the "incidental match" the bound allows.
- I found no fail-closed regression. By construction, the head's operator test finds an operator in no word where the base's per-character test found none.
- An unclosed `@'` or `@"` here-string is still unreadable. An unclosed `$(` inside a here body is now data, which is consistent with "bodies as data".
- Every Done-when name check is absent from `project-trajectory/` (grep). `_RESERVED_WORDS` (coordinator_guard.py:931) is flat, includes `time` and excludes `coproc`.
- The deleted-pin lists match the spec item by item, and every kept pin is present. All 12 of TC-339's evidence functions still exist.
- `launch_reason`'s docstring carries the set, the default and the residue. No other file restates the residue (grep over project-trajectory, .claude and docs reference pages).
- A word-diff of LLR-300 and TC-339 shows exactly the spec's replacement text and the `_invoked` drop from `code_symbol`. No other cell changed and no Status flipped (K3).
- The RESYNC entry names both kit-owned files, the armed-window visibility and "nothing needs migrating".

**Counterpart decisions for the changed LLR-300.**
- SR-229 is retained. It governs claim admission and the lease and names no shell form.
- SR-237 is retained. Its "starting no model work" and "a new ordinary call ... is refused" rest on admission at the kit launch points, which this diff does not touch; the hook is supervision.
- TC-339 is carried. Its method and expected text were amended to the narrowed set; its evidence functions are kept, with shorter case lists.
- IF-271 is retained, because `claim_refusal` is untouched.
- IF-274 is retained, because the payload is unchanged.
- IF-275 is retained. The response shape is unchanged, and "including unreadable command lines" still holds.
- No decomposition is involved.

I did not run `test_bootstrap.py`, the smoke tier or the smoke-budget check (the brief told me not to). That Done-when bar item is left to the landing.

**Done-when map.**
- (1) Names absent: grep, as above.
- (2) Flat set with `time`, without `coproc`: checked by inspection. Behaviour is not pinned; see finding 2.
- (3) Kept cases pass and deleted cases are gone: `test_a_quoted_launch_form_is_denied`, `test_a_quoted_operator_is_not_a_command_boundary` and `test_the_one_reading_keeps_quoted_text_in_its_word`, all passing, with the file inspected.
- (4) Docstring bound: coordinator_guard.py:938-967.
- (5) LLR-300 and TC-339 amended, and the gates clean: the commands below. The checkpoint sitting is pending.
- (6) RESYNC entry: present, but see finding 1.
- (7) The bar: partial, covering only the four files below.

There is no fixed-defect regression test to red-check, because the row only removes. The spec says the kept pins pass before the change, and my base probe confirms it.

**Commands.**
- `git rev-parse HEAD` -> `548fd30537db9ec5ed8a0469ed70a169b84d0122`
- `python lowprio.py python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1-opus/wi-928 tests/test_blackout_window.py tests/test_blackout_isolation.py tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py` -> `174 passed, 1 skipped in 10.49s`. The skip is the environment-gated posix-shell gate.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (934 work item(s), 812 done (87%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ...` exit 0. The worktree stayed clean afterwards.
- `python -B r1-opus/probe.py <scripts>`, run at the head and at the 61ee4e165 base tree, with a side-by-side diff of the two outputs (head.json and base.json in this directory).

- [MINOR] project-trajectory/RESYNC_PACK.md:8554 -> K4. The new entry is anchored `[since 785b29e11]`. That commit is four trunk commits before the lane's base, 61ee4e165, and it is older than the entry directly above it, WI-930's `[since 1a182d154]`. An adopter stamped at 1a182d154, 87ceeafea, 1d4e7ca7b or 61ee4e165 has a re-sync range that does not contain 785b29e11, so that adopter never selects this entry. Kit-file overwrite still delivers the code. -> Re-anchor at the landing's parent, as .claude/skills/coordinator-cycle/references/recipes.md:457 directs (no earlier than 61ee4e165), and keep the parenthetical. -> @coordinator
- [MINOR] tests/test_blackout_window.py:461 -> Deliverable 2 keeps `time` in the flat reserved set so that "plain `time claude` is still denied", and the bound promises "after the reserved words". Before this lane, the four deleted `time -p` and `time --` cases were the only pins on `time`. No line in the four guard test files now puts `time` before a model CLI (grep). Dropping `"time"` from `_RESERVED_WORDS` would therefore leave the bar green while breaking a kept promise. -> Add a kept-form pin, `("time claude -p x", "Bash")`, to QUOTED_DENIED or DENIED. This pins a retained behaviour, not a removed form, so it adds no new promise. -> @builder
- [MINOR] project-trajectory/scripts/kitlib/shell_line.py:179 -> `_heredoc_body` still collects every body line (line 191) and returns `"\n".join(lines)`. Its only caller, `_heredoc_bodies` at line 176, now throws the value away, because the reader that used it was deleted in deliverable 3. That leaves dead work and a docstring ("One here-document body ...") that describes a product nobody consumes. -> Drop `lines` and the return so the method only advances past the body to its delimiter line, and say so in the docstring. -> @builder
- [MINOR] project-trajectory/scripts/kitlib/shell_line.py:8 -> The rewrap of the WHY paragraph leaves one 120-column docstring line, and coordinator_guard.py:1043 breaks `_assigned`'s docstring mid-sentence ("quoted piece of its word; any other" / "statement's words ..."). Both are readability debt in the module an adopter's reviewer reads first. -> Rewrap both paragraphs to the file's width. -> @builder
- [MINOR] docs/requirements/low-level-requirements.toml:3177 -> K1, for clarity. The kept clause "window_check exits nonzero inside it." now follows "... it may incidentally match this reading, and carries no guarantee either way." The nearest antecedent of "it" is therefore the reading, not the armed window. -> At the checkpoint sitting that judges this cell, write "window_check exits nonzero inside an armed window." -> @adjudicator

VERDICT: APPROVE findings=5
