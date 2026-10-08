## 2026-10-08 — Owner ruling: the review threat model, and who ends a review

Given in the coordinator session of 2026-10-08, after WI-846's lane drew six
Codex Sol rounds, the last three chasing reproductions that needed a fake
runner binary (one that reads the token file and prints the token as its
version) or a runner whose version depends on the working directory.

The owner's words: "Those sorts of claims should be ignored, and not reacted
to with yet additional code. Sol will find real issues, but it will also
contrive issues that will never occur … If a system is compromised to the
point a false claude.exe can print tokens there are much bigger issues going
on. … Without that, the review period will never end, and it is exactly why I
want the claude adjudicator to step in and stop ad-nauseam reviewer
directives." And: "It is specifically the adjudicator's job to make the call
on these sorts of things unless they are high risk."

The ruling, as recorded:

1. **The review threat model is bugs and fail-open behaviour in a normal
   working environment, not a compromised host.** A finding whose
   reproduction needs the host itself to be compromised or contrived is out
   of scope and is dismissed, never answered with more code. Examples: a fake
   or hostile runner binary; a shim whose output depends on cwd; the
   environment or `PATH` changed by another process between two steps of one
   call; a tampered OS or installed tool. Still in scope: content agents
   write into the repository (specs, registries, verdicts, frontmatter),
   which the gates exist to check; supported configurations; and
   regressions of supported behaviour.
2. **The adjudicator makes the call on a contested or repeated finding,**
   not the coordinator by sending every finding back to the builder. Its
   call is final (OI-103 Q3). A high-risk finding goes to the owner.
3. **Until the kit carries both** (WI-860 states the threat model in
   PROCESS.md; WI-811, which absorbed WI-861 the same day, gives the adjudicator its dispute class), the
   coordinator states the out-of-scope class in every reviewer prompt,
   applies rule 1 itself, and records each dismissal in the lane's
   `docs/decisions/<branch>.toml` for the owner to confirm or overrule.

The owner also confirmed the coordinator's direction for WI-846 ("your
direction is fine"), read together with rule 1.
