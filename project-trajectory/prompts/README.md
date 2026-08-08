# Prompt templates — the authoring and source-separation rules

Every operational prompt this kit launches is a file in this directory, not a
string inside a script. The rules are stated **here, once**; a template links to
this file rather than restating them, and `scripts/prompt_render.py` enforces
the mechanical half.

Why the rules exist at all: prompt prose carries control flow. The reviewer
prompt's redaction clause is the reason independent review finds anything; the
critique prompt's rubric anchors are the reason a critic cannot substitute its
own standard; and a brief that opened with the judged party's own verdict is a
recorded incident, not a hypothetical. Prose that steers a session is an
artifact under review like any other.

---

## 1. The file shape

Each template has three parts, in this order:

1. **A `DISPATCHER NOTES` HTML comment.** Who sends this prompt, to what kind of
   session, and the **declared slot list** — one line per `{{SLOT}}` saying what
   fills it and from which source class. The renderer **deletes this block
   before sending**, so it is written for the human or script assembling the
   brief, never for the model.
2. **The prompt body**, with `{{SLOT}}` placeholders. Nothing else is a
   placeholder: `{single-brace}` is ordinary prose, and the renderer will not
   fill it.
3. **The output contract** — the exact machine line the session must emit, named
   in `docs/config.toml` as the job's `output_schema` so a parser and a template
   cannot drift apart silently.

Slots are `{{UPPER_SNAKE}}`. A slot's content must be **named and bounded** in
the notes: what it is, where it comes from, and the clip limit if the assembler
clips it. An unbounded slot is how a 30-line brief becomes a 3000-line one that
buries its own instruction.

## 2. What the renderer refuses

`prompt_render.render()` refuses **before launch**, and reports every problem in
one run rather than the first:

| Refusal | What it caught |
|---|---|
| unknown slot | a caller filling a brief that moved on without that slot |
| declared-required slot absent from the template | the config row and the prose drifted apart |
| a template slot nobody supplied | a hole where evidence belongs |
| a `{{...}}` that survived the fill | template syntax carried in by a value |
| a prohibited source class | see §3 |

The surviving-placeholder rung is why a template's own syntax cannot be quoted
inside a slot **value**: if a brief must show `{{LIKE_THIS}}` to a model, the
assembler breaks the braces first. A launched prompt holds no placeholder.

## 3. Source separation — the rule this directory exists for

Each job declares, in `docs/config.toml`, the source classes it **may** be fed
(`allowed_sources`) and the ones it may **never** be fed (`prohibited_sources`).
Every slot value carries its class as a label. The classes are declared in
`prompt_render.SOURCE_CLASSES`; the generated catalog
(`python scripts/prompt_render.py catalog`) prints who may read what.

**A judge is never handed the claim under judgement.** Concretely:

- a **reviewer** gets the diff, the requirement surface and real harness output
  — never the implementer's session notes or self-assessment;
- a **critic** gets the rubric, the SN/SR intent and the artifact recipe — never
  the producer's own account of the artifact;
- an **adjudicator of a disposition** gets the frozen scope, the outcome
  **enum**, the branch facts and the harness result — never the worker's
  `rationale`. That exclusion is the whole reason `adjudicate-disposition.md` is
  a separate document rather than a mode of one adjudicator template;
- a **plan critic** gets the computed coverage diff — never the rival plan's
  text;
- an **arbiter** gets anonymized plans — never model, route or session identity.

The check runs **twice**: once over the labels, and once over the prompt **as
launched**, because the leak that matters arrives inside an *allowed* slot. The
second pass compares marker **counts** against the template's own prose, so a
template may freely contain the word it forbids (the reviewer's redaction clause
does) while a value that adds one more occurrence is refused.

**A class with no content markers is enforced by its label alone.** That is a
real limit, stated rather than hidden: markers loose enough to catch every
paraphrase would refuse honest registry prose, and a check that cries wolf gets
switched off. Label discipline is the primary control; markers are the backstop
for the classes whose shape is unmistakable.

## 4. Typed facts, not steering prose

A value injected into a prompt is **untrusted evidence**, never an instruction.
So:

- an outcome is an **enum plus a separately delimited rationale**, and the
  rationale is a source class of its own — a magic substring in free prose must
  never select a tier, a reviewer count, or a queue position;
- a verdict line is machine-typed (`VERDICT: <enum>`), so a parser reads the
  decision and prose stays prose;
- a brief that cannot support a decision says so. Every judging template
  declares an **`insufficient-evidence`** verdict and names what it would need.
  A judge that guesses when the evidence is thin is worse than one that stops,
  because nothing downstream can tell the two apart.

## 5. Provenance

`prompt_render.provenance()` returns the template identity, the **template
hash** and the **rendered-prompt hash** for every launch. Session, outcome and
verdict records carry those hashes beside the route identity and model — the
hashes, not the prompts: a recorded verdict must be attributable, and a tracked
history full of rendered briefs is a privacy and a size problem.

## 6. Transport

Prompts travel on **stdin**, never argv:

```
python scripts/prompt_render.py render --job reviewer --slots brief.json | <agent cli>
```

Slots arrive in a file for the same reason: a brief-sized value blows the OS
command-line cap and is visible in every process listing on the box.

## 7. The templates

| File | Job | Notes |
|---|---|---|
| [`worker.md`](worker.md) | `implementer` | One claimed work item on one branch. A faithful move of `agent_loop.WORKER_PROMPT`. |
| [`reviewer.md`](reviewer.md) | `reviewer` | Independent adversarial review. A faithful move of `agent_loop.REVIEWER_PROMPT`. |
| [`critique.md`](critique.md) | `critic` | Rubric-anchored subjective-quality judgement. A faithful move of `agent_loop.CRITIQUE_PROMPT`. |
| [`adjudicate-amendment.md`](adjudicate-amendment.md) | `adjudicate-amendment` | Clarity vs meaning on a spine artifact. |
| [`adjudicate-disposition.md`](adjudicate-disposition.md) | `adjudicate-disposition` | Confirm or override a Partial/Cancelled outcome; draft the successor. |
| [`adjudicate-conflict.md`](adjudicate-conflict.md) | `adjudicate-conflict` | Queue admission given the overlap graph. |
| [`adjudicate-red-test.md`](adjudicate-red-test.md) | `adjudicate-red-test` | Effort, tier, plan mode and scope for a red declared bar. |
| `dual-plan-planner.template.md` | `planner` | The dual-plan hats, shipped earlier and unchanged; the strict-slot pattern the rest follow. |
| `dual-plan-critic.template.md` | `critic` (plan) | |
| `dual-plan-arbiter.template.md` | `arbiter` | |

The three moved templates are **faithful moves, not rewrites**: their prose is
the constant's prose, re-wrapped, with the Python format slots converted to
`{{SLOT}}`. `tests/test_prompt_render.py` pins that faithfulness against the
live constants, so a rewrite dressed as a move fails the suite. The constants
themselves stay in `agent_loop.py` until the cutover slice moves the call sites
— one runtime change at a time.
