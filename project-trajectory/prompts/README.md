# `prompts/` — the briefs the loop sends, as reviewable text

Every prompt the unattended loop sends a session lives here as a file, loaded by
[`scripts/prompts.py`](../scripts/prompts.py). None of them is a Python string
constant any more, and that is the point: **prompt prose is what steers the
sessions this loop launches, so it belongs where a diff shows it.**

| File | Sent to | Overridable via `--prompt-map` |
|---|---|---|
| `worker.template.md` | the BUILD session of a claimed work item | **no** — see below |
| `reviewer.template.md` | REVIEW-A / REVIEW-B | yes (per phase key) |
| `critique.template.md` | CRITIQUE | yes (`CRITIQUE`) |
| `dual-plan-planner.template.md` | the two planner hats | yes (`DUALPLAN-PLANNER`) |
| `dual-plan-critic.template.md` | the critic hat | yes (`DUALPLAN-CRITIC`) |
| `dual-plan-arbiter.template.md` | the arbiter hat | yes (`DUALPLAN-ARBITER`) |
| `adjudicate-amendment.template.md` | meaning-vs-clarity on an amended spine row | yes |
| `adjudicate-disposition.template.md` | a `partial/` or `cancelled/` lane close | yes |
| `adjudicate-conflict.template.md` | a row about to enter the ready queue | yes |
| `adjudicate-red-tc.template.md` | unverified test cases found by the idle census | yes |

The worker assignment is deliberately **not** overridable: the assignment is the
whole scope of that session, and an env var that can replace it is a way to
widen a claim without a reviewed diff. Editing the template *is* the supported
way to change the worker brief.

---

## Authoring rules

These are enforced, not hoped. Each rule below has a test; a template that
breaks one reds the suite rather than quietly changing how a session behaves.

### 1. Every slot is named and bounded

A slot is `{lower_snake_case}` and is filled by
[`prompts.fill`](../scripts/prompts.py), which is **strict in both directions**:
a value with no matching slot raises, and a slot with no value raises. A brief
never ships with a hole where a redacted input belongs, and a template edit that
drops a slot fails loudly instead of silently sending less context.

Where a slot carries a *clipped* projection of something larger — a spec body, a
census, a diff — the dispatcher-notes block at the top of the file **declares
the clip**: which lines, how many, and from where. A brief whose caller silently
truncates is a brief whose author cannot know what the session actually read.

### 2. Verdict lines are machine-typed, never prose

Every judging template ends with exactly one machine line drawn from a closed
enum:

```
VERDICT: APPROVE|CHANGES-REQUESTED findings=N
VERDICT: MEANING|CLARITY rows=N
OUTCOME: COMPLETE|PARTIAL|CANCELLED successors=N
OUTCOME: QUEUE|QUEUE-WITH-EDGE|RETURN-TO-DRAFT needs=<id or ->
```

**Prose that carries control flow must be a typed field.** The rule is written
in blood: `NEEDS-HUMAN`, a magic substring inside a free-text handback reason,
was the *only* input selecting a disposition row's review tier — so a typo
(`NEEDS_HUMAN`, `needs human`) silently downgraded the judgement, with no
constant, no validation and no refusal on a miss. A closed enum on its own line
is parseable, testable, and impossible to typo silently.

### 3. A judge's brief never contains the judged party's self-assessment

Not the implementer's session notes, not `docs/status.md`, not `docs/log.md`,
not a prior verdict on the same artifact, and not a free-text reason the judged
party wrote about its own outcome.

Two measurements stand behind this. A leaked self-assessment collapses review
finding rates several-fold — which is why the reviewer brief is redacted **by
construction** (it can only read the diff and the requirement surface) rather
than by asking nicely. And when derived prose *did* leak into a judge's brief,
it anchored the judgement: a disposition row's `## Context` opened with the
returning lane's own clipped verdict, and the judge agreed with it.

Where a claim genuinely *is* the subject — the disposition brief must show the
lane's claimed outcome, because judging that claim is the whole job — it is
labelled as **a claim under judgement, never as the premise**, and the brief
says so in those words.

### 4. Say what is absent, and why

Each template's dispatcher-notes block lists what the session deliberately does
**not** get. A redaction nobody can see reads as an oversight to the next
author, who then "fixes" it.

### 5. State facts; let the session draw the inference

An imperative in a brief is obeyed whether or not the machinery behind it is
advisory. If a joined fact is worth showing (*"WI-391 was cancelled; reason:
…"*), show the fact. Reserve imperatives for genuine protocol — where to write
the verdict, what not to edit.

### 6. Do not re-wrap an existing template

Several phrases in `reviewer.template.md` and `critique.template.md` are pinned
as contiguous substrings by the suite, and the fake-CLI test harness tells a
reviewer session from a worker one by matching `Write your verdict to (\S+)`. A
newline inserted mid-phrase fails those tests in confusing ways. Change the
words deliberately; never re-flow the file.

### 7. `{` and `}` are hostile in `worker.template.md`

That one is filled with `str.format`, so a literal brace raises at
session-composition time — after preflight, inside a live run. Double it
(`{{`/`}}`) if you need one. The reviewer and critique briefs use
`str.replace` and are safe.

---

## Downstream

`bootstrap.py` copies this whole directory into a scaffolded repo's `prompts/`,
where `scripts/prompts.py` resolves it script-relatively. The files are
**kit-owned**: a re-sync overwrites them, so a repo that wants a different
reviewer brief wires its own file through `--prompt-map` / `AGENT_PROMPT_MAP`
rather than editing the shipped one. The one exception is the worker assignment,
which has no override — a repo that must change it forks the template and
records the fork, so the divergence is visible at the next re-sync.

`python scripts/prompts.py list` prints the catalogue (key, file, digest, slots)
and `python scripts/prompts.py check` exits nonzero if any shipped template
cannot be loaded — the same rung `agent_loop`'s preflight runs before iteration
one.
