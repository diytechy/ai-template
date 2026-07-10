# Full-repo adversarial review — kit product code

> **RESOLVED 2026-07-10 (review triage, WI-1.53).** All 9 findings fixed:
> C3/C5/C7/C8 in triage commit 2/5 (text-boundary); C1/C2/C4/C6 in commit
> 4/5 (harness + drift); C9 in commit 5/5 (docstring posture notes). New
> regression tests for C1/C2/C4. See IMPROVEMENT_PLAN.md WI-1.53.

**Reviewer:** Reviewer C (whole-repo, cross-script) · **Date:** 2026-07-10 ·
**HEAD:** `33b40e302ae75495c850703aab7f9037dc9f4a70` · **Branch:** `MultiRepoSupport`

Scope: every script under `project-trajectory/scripts/`, the shipped hooks
(`project-trajectory/hooks/`, `.githooks/`), and `tests/` as a quality subject.
The value here is what a per-change review structurally cannot see: cross-script
inconsistencies, shared latent bugs, drifted conventions. This is a mature,
heavily-tested tree (445 tests); findings are correspondingly narrow — none rise
to HIGH, and I did not pad. Every item is verified against the tree (read + run
read-only). Ranked most-severe first.

## Severity index

| ID | Sev | One-liner |
|---|---|---|
| **C1** | MEDIUM | `okf` is a built-in check step but missing from `BUILTIN_STEP_NAMES`, so a downstream `[step:okf]` silently duplicates instead of being rejected — and the shadow-guard test can't catch it. |
| **C2** | MEDIUM | `check.py._expand` splits stack.ini commands with backslash-eating `shlex.split`, mangling Windows paths — while `agent_loop.split_cmd` was hardened for exactly this. Two command parsers, one drifted. |
| **C3** | MEDIUM | git subprocesses use `text=True` without `encoding="utf-8"`; only `check_privacy` guards it. The committed `PROJECT_STATE.html` already ships mojibake (`Â·`) from a Windows regen. |
| **C4** | MEDIUM | `pre-push` and `commit-msg` hooks don't honor `KIT_SCRIPTS_DIR` (only `pre-commit` was taught it in WI-1.42), so the "harness elsewhere" layout silently skips the message scan and fails the push closed. |
| **C5** | MEDIUM | 6 of 19 scripts lack the `_utf8_console` guard the other 13 carry, so registry-derived non-ASCII crashes them with `UnicodeEncodeError` on a legacy cp1252 Windows console. |
| **C6** | LOW | The SN-table parser is copy-pasted into `gen_okf.sn_rows` and `gen_trajectory._sn_rows` and has already drifted (one skips `-000`, one doesn't; one sorts, one doesn't). |
| **C7** | LOW | `gen_okf` forces LF on write; `gen_trajectory`/`gen_arch_map` use `write_text` → CRLF on Windows. Inconsistent; masked only by `.gitattributes eol=lf`. |
| **C8** | nit | `check.py.resolve_gate` reads `docs/gate` without `errors="replace"`, unlike every peer declared-policy reader — invalid UTF-8 crashes instead of degrading. |
| **C9** | nit | The generated-artifact `--check` family disagrees on the missing-target contract (`gen_arch_map` hard-`SystemExit` vs `gen_okf`/`gen_trajectory` treat-as-stale/vacuous). |

---

## C1 — MEDIUM · `okf` step name missing from the shadow-guard set

**What.** `check.py` protects its built-in step names: a project-declared
`[step:<name>]` in `docs/stack.ini` that reuses a kit step name is rejected
loudly, because otherwise it would *append* a second step under that name rather
than replace it (see `extra_steps`, line 255-260). The allow/deny set is
`BUILTIN_STEP_NAMES` (check.py:153-168). The `okf` step (Thread 48) was added to
`steps()` (check.py:506-512) but **never added to `BUILTIN_STEP_NAMES`.**

**Evidence.** `project-trajectory/scripts/check.py:153` (the frozenset) vs
`check.py:506` (the `okf` step). Verified by running:

```
$ python -c "import check; ... [s[0] for s in check.steps(80,'all','all')]"
in steps() but NOT in BUILTIN_STEP_NAMES: ['okf']
```

And the failure mode reproduced directly — a profile with `[step:okf]` yields
**two** okf steps rather than an error:

```
$ # feed check.steps a ConfigParser with [step:okf]
okf count in plan: 2
DUPLICATE okf steps present: True
```

The regression-guard test that should catch this, `tests/test_stack_profile.py:220
test_extra_step_shadowing_a_builtin_fails_loudly`, uses `[step:lint]` — a name
that *is* in the set — so it passes and gives false confidence. It exercises one
hardcoded name instead of iterating the built-in set, so it can never detect an
incomplete set.

**Failure scenario.** A downstream repo that adds its own `[step:okf]` (e.g. a
different OKF exporter for its stack) gets the kit's `gen_okf.py --check` **and**
its own command both run at G3 under the same name — a confusing double-run, and
the kit step it meant to replace is still there. The whole point of the guard
(WI-that-introduced-it) is defeated for this one name.

**Fix direction.** Add `"okf"` to `BUILTIN_STEP_NAMES`, and change the test to
assert the guard for *every* name in `check.steps(...)`'s built-in output (loop,
don't hardcode), so the set can't drift again.

---

## C2 — MEDIUM · Two command-template parsers; only `agent_loop`'s survives Windows paths

**What.** The kit has two places that split a command *template* string into an
argv. `agent_loop.split_cmd` (agent_loop.py:380-388) was written specifically to
survive Windows paths:

```python
lex = shlex.shlex(template, posix=True)
lex.whitespace_split = True
lex.escape = ""           # "shlex's posix escape rules would eat C:\path separators"
```

`check.py._expand` (check.py:201-211) — the parser for the `docs/stack.ini`
product commands and every `[step:]` section, i.e. the documented "swap for your
stack" extension point — uses the naïve `shlex.split(template)`, which is
`posix=True` **with** escaping, so it eats backslashes.

**Evidence.** Verified:

```
$ python -c "import shlex; print(shlex.split(r'C:\tools\mytool --check {src}'))"
['C:toolsmytool', '--check', '{src}']
$ python -c "import shlex; print(shlex.split(r'.venv\Scripts\eslint {src}'))"
['.venvScriptseslint', '{src}']
```

`check.py` partially dodges this by splitting first and substituting `{py}`
*per token* (so the interpreter path survives — the WI-1.25 fix), but any path
an author writes *into* a stack.ini command value still goes through the
backslash-eating split.

**Failure scenario.** A downstream Windows author declares
`command = .venv\Scripts\eslint {src}` (or any native-path tool) in `docs/stack.ini`.
The token becomes `.venvScriptseslint`, `run_step`'s PATH probe fails to resolve
it, and the step is reported SKIP(missing)/FAIL — a silent corruption of the
primary extension mechanism, on one of the two first-class platforms. The kit
*already solved this* in `agent_loop`; `check.py` didn't inherit the fix.

**Fix direction.** Give `check.py._expand` the same `shlex.shlex(..., escape="")`
tokenizer `agent_loop` uses (factor it into one shared helper — it is the same
job), and add a stack.ini fixture with a backslash path to `test_stack_profile.py`.

---

## C3 — MEDIUM · `text=True` git subprocesses decode with the OS locale, not UTF-8 — mojibake already shipped

**What.** Of the scripts that capture git output, **only** `check_privacy.git`
sets `encoding="utf-8", errors="replace"` (check_privacy.py:204-205). `agent_loop.git`
(442), `check_docs` (401,413), `gen_trajectory` (871), and `bootstrap` (1120,1128,1136)
use `subprocess.run(..., text=True)` with no `encoding=`, so on Windows they
decode git's UTF-8 stdout with the locale codepage (cp1252).

**Evidence — this is not hypothetical; it is committed.** `gen_trajectory` builds
the as-of stamp with a git format string containing a literal `·` (U+00B7,
gen_trajectory.py:872 `--format=%h · %as`). git echoes the raw UTF-8 bytes
`C2 B7`; cp1252 decodes them to `Â·`. The committed dashboard shows it:

```
$ grep -o 'class="asof"[^<]*' PROJECT_STATE.html
class="asof">state as of commit 27ebc29 Â· 2026-07-10
```

The stamp is excluded from `--check` (ASOF_RE strips the whole paragraph from
both sides), so the freshness gate cannot catch it — a Windows regen and a Linux
regen produce different committed bytes on that line and *both* pass `--check`.
That is why the mojibake persists in the tree.

**Failure scenario.** Cosmetic today (a defaced stamp in the flagship generated
deliverable). The sharper edge is latent: with `text=True` the decode is
*strict*, so any git output byte undecodable in cp1252 (`0x81/0x8D/0x8F/0x90/0x9D`
— reachable via a unicode branch name or commit subject) raises
`UnicodeDecodeError` and crashes the script rather than mojibaking. `agent_loop.git`
reads `branch --show-current`, so a unicode branch name would crash the unattended
loop on Windows.

**Fix direction.** Add `encoding="utf-8", errors="replace"` to every git
`subprocess.run(..., text=True)` (they should share one `git()` helper), and
regenerate `PROJECT_STATE.html` on a UTF-8 host to clear the shipped `Â·`.

---

## C4 — MEDIUM · `KIT_SCRIPTS_DIR` was taught to `pre-commit` only; `pre-push`/`commit-msg` still hard-look for `scripts/`

**What.** WI-1.42 taught `hooks/pre-commit` to locate the harness via
`KIT_SCRIPTS_DIR` (env var / delegating wrapper), so a repo whose harness lives
elsewhere — explicitly including "the kit's own meta-repo, where the harness is
under project-trajectory/scripts/" (hooks/pre-commit:58-82) — can still run the
floor. `hooks/pre-push` (line 69-72, 103-108) and `hooks/commit-msg` (line 38-47)
were **not** updated: they only search `scripts/`/`Scripts/` under the repo root
and ignore `KIT_SCRIPTS_DIR` entirely.

**Evidence.** `hooks/pre-commit` reads `${KIT_SCRIPTS_DIR:-}`; `grep KIT_SCRIPTS_DIR
hooks/pre-push hooks/commit-msg` → no matches. `.githooks/` in this meta-repo
holds only a `pre-commit` wrapper (no pre-push/commit-msg wrappers), so the gap
is invisible here.

**Failure scenario.** A downstream repo using the harness-elsewhere layout
(the documented KIT_SCRIPTS_DIR pattern) that also enables `docs/privacy-check`:
- `commit-msg` → "cannot find scripts/ dir … skipping message scan" (exit 0):
  the commit **message** privacy/secrets scan silently never runs — a security
  gap that is *supposed* to be closed at commit time.
- `pre-push` (privacy on) → cannot find `scripts/`, prints "FAILING CLOSED",
  exit 1: the repo cannot push at all.

**Fix direction.** Hoist the `KIT_SCRIPTS_DIR`-then-`scripts/`/`Scripts/`
discovery block (and the venv/PY probe) into one shared snippet all three hooks
source, or copy the pre-commit discovery into pre-push and commit-msg verbatim.

---

## C5 — MEDIUM · The `_utf8_console` guard is missing from 6 scripts that can print non-ASCII

**What.** 13 scripts define/call `_utf8_console()` (the guard the kit added so a
`§`, an em-dash, or an accented name in output can't `UnicodeEncodeError` a
legacy cp1252 Windows console — see the rationale in trace.py:181-190). Six do
not: `check_doc_refs.py`, `check_dupes.py`, `check_stubs.py`, `gen_cases.py`,
`gen_okf.py`, `gen_release_checklist.py`.

**Evidence.** Per-file grep for `_utf8_console`/`reconfigure(encoding` across
`project-trajectory/scripts/*.py` (6 "NO guard"). Of these, `gen_release_checklist`,
`gen_cases`, and `gen_okf` print registry/spec-derived strings (titles,
Permutations cells, exported paths) that legitimately carry non-ASCII.

**Failure scenario.** A downstream repo with an accented author name, a `—`, or a
`§` in a requirement Title runs `gen_release_checklist.py` (or `gen_cases.py`) in
a cmd.exe console at codepage 1252 → `UnicodeEncodeError`, wedging the run rather
than printing. The kit hardened the other 13 for exactly this; these six drifted.

**Fix direction.** Add the four-line `_utf8_console()` (verbatim from trace.py)
and call it first in each of the six `main()`s. (The guard being copy-pasted 13×
is itself a smell — a shared `kitconsole` import would end the drift — but that
is a larger refactor; the immediate fix is to close the six gaps.)

---

## C6 — LOW · Duplicated SN-table parser has already drifted

**What.** `check_dupes` flags the largest block in the tree (~124 tokens):
`gen_okf.py:76` == `gen_trajectory.py:94`. Both parse the stakeholder-needs
markdown table into `{id, need, why, acceptance}` rows. They have **already
diverged**:

- `gen_okf.sn_rows` (gen_okf.py:83): `if not m or m.group(1).endswith("-000"): continue`
  — **skips** the `SN-000` placeholder, and returns `sorted(rows, key=id)`.
- `gen_trajectory._sn_rows` (gen_trajectory.py:101): `if not m: continue`
  — **keeps** `SN-000`, and returns `rows` in file order (unsorted).

**Evidence.** Read both regions (cited lines).

**Failure scenario.** A downstream repo mid-G1 with an `SN-000` placeholder still
in `stakeholder-needs.md` that adopts the trajectory layer: `gen_trajectory`
renders a phantom `SN-000` root in the dashboard icicle while `gen_okf` correctly
omits it — the two "views of one truth" disagree, defeating the single-source
premise the kit preaches. Latent in the kit itself (it is at G3, no `-000`), but
it is a live drift.

**Fix direction.** Extract one `sn_rows(root)` (placeholder-skipping, sorted) into
a shared module both import — `gen_trajectory` already imports `check_trajectory`,
so a shared spine-parse home exists.

---

## C7 — LOW · Newline-on-write inconsistency across the generator family

**What.** `gen_okf` deliberately writes with `open("w", newline="\n")` and even
documents why (write_text(newline=) is 3.10+, floor is 3.8 — gen_okf.py:422-424),
producing LF on every OS. `gen_trajectory` (write_text, 1086) and `gen_arch_map`
(write_text, 667) do not, so on Windows they emit CRLF.

**Evidence.** `python -c "Path.write_text('a\nb\n')"` yields `b'a\r\nb\r\n'` on
this Windows host; `PROJECT_STATE.html` and `docs/architecture.md` are CRLF in the
working tree (282/282 and 418/418 CRLF lines). It is masked only because
`.gitattributes` has `* text=auto eol=lf` (the stored blobs are LF —
`git ls-files --eol` shows `i/lf w/crlf`), and `bootstrap` scaffolds the same
`gitattributes.template` downstream.

**Failure scenario.** Any repo that overrides or drops that catch-all (or lists
`*.html`/`architecture.md` under a different rule) gets whole-file CRLF↔LF churn
between Windows and Linux regens for these two artifacts, while `docs/okf/`
stays clean. It is a latent, gitattributes-dependent inconsistency in files the
kit calls generated-not-hand-maintained.

**Fix direction.** Have `gen_trajectory`/`gen_arch_map` write with
`open("w", encoding="utf-8", newline="\n")` like `gen_okf`, so byte-stability
doesn't depend on a `.gitattributes` rule surviving downstream.

---

## C8 — nit · `resolve_gate` reads `docs/gate` without `errors="replace"`

**What.** Every declared-policy reader in the kit — `agent_loop.read_declared`
(159), `check_privacy._first_declared_line` (163), `check_trajectory._first_declared_line`
(69), `gen_okf.read_enabled` (101) — reads with `errors="replace"` (or tolerates
failure). `check.py.resolve_gate` (check.py:532) uses a bare
`read_text(encoding="utf-8")`. A `docs/gate` with a stray invalid byte crashes
`check.py` with `UnicodeDecodeError` instead of degrading. Trivial, but it is the
one reader out of step. Add `errors="replace"`.

---

## C9 — nit · The `--check` family disagrees on the missing-target contract

**What.** For a *missing* target, `gen_arch_map` does
`raise SystemExit("target file not found")` (gen_arch_map.py:644-645);
`gen_okf --check` treats a missing bundle dir as vacuously-clean-or-stale
(gen_okf.py:397-404); `gen_trajectory --check` treats a missing output as STALE
(gen_trajectory.py:1069-1078). Each is individually defensible (arch-map's target
is a hand-authored doc that must exist; the others own a fully-generated output),
but the family reads as three different contracts. Worth a one-line note in each
docstring stating the intended posture so the next generator author copies the
right one, rather than a code change.

---

## Verified clean

Audited and found sound:

- **No `shell=True` anywhere.** All `subprocess.run` calls pass a list argv
  (grep across scripts). The LLM invocation (`agent_loop.py:759-767`) correctly
  sets `stdin=subprocess.DEVNULL` and a `timeout`; git helpers pass DEVNULL where
  it matters.
- **Python 3.8 floor holds.** No `is_relative_to` / `removeprefix` / `removesuffix`
  / `functools.cache` / `graphlib` / `ast.unparse` / dict-`|`-merge / `write_text(newline=)`
  anywhere (targeted grep). `gen_okf` *explicitly* avoids `write_text(newline=)`
  for the floor. Tests run under cpython-3.8 (`.pyc` tags confirm).
- **F4 (unbounded recursion) is genuinely resolved.** `check_trajectory._cycles`
  (146-181) is an explicit-stack iterative DFS with correct WHITE/GREY/BLACK
  colouring; a back-edge to a GREY node reconstructs the cycle via
  `path.index(p)`. No recursion-depth exposure.
- **Declared-policy parse is consistent.** `agent_loop`, `check_privacy`,
  `check_trajectory`, `gen_okf`, and `check.py.resolve_gate` all
  strip-then-`startswith("#")`, agreeing on leading-whitespace and blank-line
  edge cases (only the `errors=` handling differs — C8).
- **`trace.py` integrity floor is robust.** `structure_findings` (RFC-4180
  column-count over every `*.csv` by location) + `integrity_findings`
  (dup/malformed ids) + `triangle_findings` (SR/LLR citation coherence) are
  sound; the `REPO`/`MOD` coexistence read is correct.
- **The shadow guard, tier-marker opt-out, and coverage-env stripping in
  `check.py`** are correct in design (the only defect is the incomplete
  `BUILTIN_STEP_NAMES` set — C1).
- **`sitecustomize`/coverage isolation** (`_step_env` strips inherited
  `COVERAGE_*`/`COV_CORE_*`) is the right call for a meta-suite that measures a
  harness that itself spawns `pytest --cov`.

## Aging assumptions (true today, will bite later)

- **The hook behavior suite skips wholesale without `sh`+`git` on PATH**
  (`test_pre_commit_hook`, `test_pre_push_hook`, `commit-msg` tests). On a bare
  Windows box without Git-Bash `sh` exported, a contributor can break a shipped
  hook and still see green locally. CI covers it *today* (GitHub Windows runners
  ship Git-for-Windows `sh`); the day that stops being true, hook regressions go
  unnoticed. Consider a non-skipping smoke that at least lints the hook with a
  bundled minimal shell, or an explicit CI assertion that the hook tests ran.
- **`EXEMPT_EMAILS = ["*noreply*"]`** is a substring glob. It is fine now, but a
  real contactable address that merely contains "noreply" (e.g.
  `noreply.jane@gmail.com`) is silently exempted from the privacy layer. The
  stricter enumerated list is already in a comment (check_privacy.py:124-129).
- **`text=True` locale decoding "works"** only because the git output actually
  read in the hot paths is ASCII (short shas, ISO dates, epochs). The moment a
  path reads a commit subject, author name, or unicode ref, C3 turns from
  cosmetic into a crash on Windows.
- **CRLF-safety of `PROJECT_STATE.html`/`architecture.md` rests entirely on the
  `.gitattributes eol=lf` catch-all** (C7). The generators don't self-enforce it,
  so a future `.gitattributes` edit downstream silently reintroduces churn.
- **`_utf8_console` is duplicated verbatim into 13 scripts** (and missing from 6,
  C5). Every copy is a place the next person can forget; the drift already
  happened once. A single shared console helper would retire the whole class.
