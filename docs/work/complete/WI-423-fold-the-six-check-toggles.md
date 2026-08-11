+++
id = "WI-423"
title = "Fold the six remaining check-enablement toggles into docs/process.toml, or rule that they stay files. SN-028 consolidated ~10 one-word policy files into one TOML home and left SIX behind, naming them in the shipped template rather than omitting them quietly: docs/trajectory-check, docs/interfaces-check, docs/components-check (check_trajectory.py), docs/subagent-gate (subagent_gate.py), docs/live-status (agent_loop.py) and docs/okf-export (gen_okf.py). The stated reason each was left is real and is the whole question this row has to answer: every one is read by an INDEPENDENTLY COPYABLE checker that imports nothing of the config layer, so folding it in means each of those scripts grows its own local tomllib reader - a genuine cost paid five times over, against a benefit (one home) that is real but smaller for a toggle than for a policy. DECIDE IT, do not drift: either (a) fold them, accepting five small local readers and stating the F5 duplication in docs/dupes-allow like every other sanctioned copy, or (b) RULE that check-enablement is a different KIND of declaration from process policy - it answers 'is this check on', not 'how is work processed' - and record that line in process.toml's header as a decision rather than as a to-do. Whichever way it goes, the shipped template's paragraph 4 must stop describing an open question."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**RULED (b): check-enablement toggles stay files.** The six —
`docs/trajectory-check`, `docs/interfaces-check`, `docs/components-check`
(check_trajectory.py), `docs/subagent-gate` (subagent_gate.py),
`docs/live-status` (agent_loop.py), `docs/okf-export` (gen_okf.py) — are a
different KIND of declaration from a process dial and stay where they are. The
shipped template's header item 4 now states this as a decision; nothing in the
six checkers changed, and no toggle file was created or moved.

**AGENT-RULED UNDER THIS WI'S OWN LICENSE; OWNER RATIFICATION OWED AT THE P0
SITTING.** The row licensed a decision either way; this is that decision, not an
owner ruling. It is tabled for the lock ledger.

### The evidence, including where it corrects the spec

1. **The cost argument the row leaned on is weaker than stated — say so first.**
   The spec anticipated "five copies of the shape contract the sh-parse hooks
   depend on." That is not so: `hooks/pre-commit`, `commit-msg` and `pre-push`
   sh-parse exactly three keys (`privacy_check`, `secrets_scan`,
   `privacy_review`). None of the six is hook-read — the pre-commit hook honors
   `docs/trajectory-check` only because it shells out to check_trajectory.py.
   So folding would NOT replicate `check_privacy._process_gate`'s ~90 lines of
   `_text_declares` / `_strip_comment` / fail-closed apparatus. Option (a) is
   genuinely cheaper than the row assumed (three stdlib checkers growing a
   ~15-line tomllib read; subagent_gate.py and gen_okf.py do not import tomllib
   today, check_trajectory.py already does). The ruling therefore does not rest
   on cost, and should not be read as if it did.

2. **The decisive reason is the DEFAULT, and it forks (a) into two losses.**
   None of the six is scaffolded — no MAPPING row in bootstrap.py, and none
   exists in this repo's own `docs/`. Absence IS the declaration: absent reads
   ON for the five checks, OFF for the subagent gate (README's dial table
   already prints their default as "on (no file)" / "off (no file)", and
   already renders them as a row class distinct from the `process.toml <key>`
   rows). A TOML key cannot be absent and still declare. So (a) forks: ship the
   keys and every fresh scaffold gains six visible invitations to type `false`
   against a check that is deliberately on-by-default; or omit them and the
   "one home" is a section that does not exist until an adopter writes it —
   strictly more steps than creating the one-word file it replaced. The benefit
   is only realized on the prong that damages the posture.

3. **F5 closes it.** The standing owner ruling (2026-07-12, recorded in
   `docs/dupes-allow`) rejected a shared `_kitcommon.py` so each kit script
   stays independently copy-able and stdlib-only. check_trajectory.py,
   subagent_gate.py and gen_okf.py are exactly those scripts. A one-word file
   is the only toggle interface a checker copied ALONE — into a repo with no
   `process.toml` and no intent to adopt the kit — can still satisfy. Binding
   their toggles to a kit-owned config file inverts that ruling for a benefit
   reason 2 shows to be near zero.

Reason 1 is included deliberately: a ruling that survives on a premise its own
evidence does not support is the kind that gets re-opened. This one is recorded
with the weak argument removed and the load moved onto reasons 2 and 3.

### Edits

- `project-trajectory/process.toml.template` — header item 4 rewritten from
  "SIX CHECK-ENABLEMENT TOGGLES are NOT YET HERE" (an open question) to
  "CHECK-ENABLEMENT TOGGLES stay files — RULED (WI-423), not pending", carrying
  the three reasons above. Header stays comments-only; the file still parses and
  `agent_common.process_shape_findings` returns `[]` for it scaffolded as
  `docs/process.toml`.
- `docs/process.toml` (this repo's own instance) — it did not carry the
  open-question paragraph, but its enumeration "THREE DELIBERATE EXCEPTIONS"
  became an undercount once the ruling made the toggles a fourth ruled
  category. Now "FOUR", with a compact item 4 pointing at the template for the
  full reasoning and recording that this repo declares none of the six.
- The six toggle files, the five checkers, `docs/dupes-allow`: untouched, which
  is what ruling (b) means.

## Context

`project-trajectory/process.toml.template` currently says, in its own header,
that these six are "NOT YET HERE, and this file would be lying if it did not
say so". That honesty is right for a template mid-consolidation and wrong as a
permanent state: a header that describes an open question invites every future
reader to re-open it.

The line the template draws today — "those six answer 'is this CHECK on', not
'how is work processed'" — is already a defensible ruling. It may simply need
to be *stated as one*. The alternative is a real cost with a real benefit, and
the point of this row is that somebody weighs them once and writes down the
answer, rather than the question surviving another program.

Note the asymmetry that makes (a) more expensive than it looks: these checkers
are the ones an adopter copies individually. A local TOML reader in each is not
just five copies of a function, it is five copies of the *shape contract* the
hooks' sh parse depends on (`agent_common.process_shape_findings`), and that
contract is exactly the thing SN-028's review found five fail-OPEN bugs in.
