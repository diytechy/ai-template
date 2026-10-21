+++
id = "WI-966"
title = "The policy file's one-key-per-line shape rule retires: the hooks read it through one parse, so nothing reads it as text"
workstream = "process"
sr_refs = ["SR-137", "SR-031"]
specref = "docs/plans/2026-10-11-review-churn/README.md#10-one-configuration-file-in-toml"
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand in headless leg 07 (2026-10-21) at WI-962's landing, as that
row's scope answer S1 recommended: "the shape-rule retirement (SR-137's line
shape, `process_shape_findings`, `GREPPABLE_KEYS`, check_privacy's textual
mirror, IF-037's `data` cell) lands independently and only after this row
... `planmode = "none"` (deletion). It lands before item 10 step 5, whose
triple-quoted route strings need the shape rule gone." The ruling is the
review-churn plan's owner ruling 10: since WI-880 all three hooks refuse
without Python 3.11+, so the shell grep and the one-key-per-line shape rule
(SR-137) can go. Since WI-962 the hooks read the policy through one parse
(`check_privacy.py --hook-policy`), so the rule guards a reader that no
longer exists.

**What the rule is today (sites, found by grep at filing):**

- `agent_policy.process_shape_findings` (and its refusal text, "The git
  hooks read this file line-by-line in pure sh (M-42)"), `GREPPABLE_KEYS`
  (re-exported by `agent_common`), and `agent_policy.config_conflicts`'
  "while the git hooks keep acting on the text" string.
- `check_privacy`'s textual mirror (`_text_declares`, `_strip_comment`, and
  the gates' fallback to them "so this reader cannot conclude 'absent'
  about a key [the hooks] would act on").
- IF-037's `data` cell ("one key = value per line").
- The shipped template's header (`process.toml.template` lines 6 to 19)
  and its `KEYED-GREPPABLE` notes (about lines 188 and 197), the same
  text in this repo's `docs/process.toml` (lines 6, 57, 205, 219), and the
  kit README's `process.toml.template` cell ("because the three git hooks
  match the privacy dials with a keyed pure-sh grep").

**Review findings routed here** (wi-962 D-004 (c), D-007): SR-137's
acceptance says dotted keys and inline tables read ON "in both readers",
while TC-031 now requires the parser's reading; SR-137's rationale ("the
three git hooks in pure sh") and SN-028's acceptance ("because two grammars
read the file (a TOML parser and the hooks' plain-sh parse)") state the
premise WI-962 removed; and SR-031's rationale still says the file's two
readings are pinned equal. SN-028 and SR-137 are approved rows, so their
amendment or retirement is judged at this row's sitting.

Its scope critique (S1 to S6, `planmode` decided at S4) runs before its
claim.

## Done-when

- [ ] No kit reader refuses or reads a policy file by its line shape:
  `process_shape_findings`, `GREPPABLE_KEYS` and `check_privacy`'s textual
  mirror are deleted, with every caller and test that names them, and the
  remaining readers read the parse alone.
- [ ] A dotted key, an inline table or a multi-line string in the policy
  file is read as the TOML parser reads it, by every reader; no hook or
  checker refuses it for its shape.
- [ ] Every shipped and repo text listed under Context that states the
  shape rule or the hooks' text read is rewritten or removed.
- [ ] SR-137 is retired or amended, IF-037's `data` cell amended, and
  SN-028's and SR-031's premise wording corrected, each judged at the
  lane's sitting (SN-028 at the owner's rung if it is held).
- [ ] One RESYNC entry: what an adopter's policy file may now contain, and
  that a shape-rule refusal no longer fires.
- [ ] The commit bar is green, and both strict lints are clean.
