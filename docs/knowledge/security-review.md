# Security review: secrets, irreversible actions, and who may reach them — DRAFT

> **DRAFT (agent-authored, WI-546, 2026-08-30).** Drafted by the unattended lane so the `hat.SECURITY` roster entry has a `knowledge` value to point at; the owner reviews and cuts at RETURN, per the `hats.toml` header's own rule. This distills THIS repo's accumulated perspective from its own decisions and surfaces — it is not retrieved external research, and its claims are the drafter's reading, not a settled finding.

The SECURITY hat asks, of every decomposition: *what secret, credential, or
irreversible action does this touch — and which requirement names who may reach
it?* It fires `always` (`hats.toml` `[hat.SECURITY]`). In this repo the answer
is unusual, and the whole hat turns on getting it right: the kit builds no
product, so its irreversible actions are process actions — a `git push`, a
subagent fan-out, content leaving the machine for a model provider — and its
governing honesty is that **almost none of its controls are security in the
sandbox sense.** They are supervision that a model which can edit files can
remove (`subagent_gate.py` module doc; SR-043 rationale). A reviewer who
credits a hook with a refusal it cannot enforce has mis-priced the risk.

## What this hat looks for here

- **An irreversible action with no requirement naming its authority.** This is
  the charter's `listens_for` verbatim, and the repo already has the canonical
  answers. Publishing is human: `docs/process.toml` sets `push = "human"` (an
  agent never pushes, even if asked). Fan-out is dialled: `subagent_gate.py`
  refuses/defers spawns of `Task`/`Agent` per `[checks] subagent_gate`
  (`off|ask|deny`, absent = off), and the only bypass is `SUBAGENT_GATE=allow`
  set in the **launcher environment the model cannot write** (SR-043; realizes
  SN-006's "override a human provides — never one the model can set"). If a new
  decomposition adds an undoable action, look for the row that names its
  authority the way SR-043 names the gate's.

- **The human-held override, and whether anything lets the model reach it.**
  SN-006 makes this the load-bearing invariant: declared limits bound spawned
  workers and irreversible actions, and *only* a human-provided override may
  relax them. The one thing the gate's deliberate fail-open must never relax is
  that override itself (SR-043 rationale). Scrutinize any change that reads a
  policy dial, an env var, or a launch flag for whether the model could set the
  value that loosens its own leash.

- **A secret that could be spent, or committed, or echoed back.** Three seams
  cover this, each honest about being a floor not a guarantee. The commit-time
  lint `check_privacy.py` runs an always-on secrets floor (PEM headers, GitHub /
  Slack / AWS / `sk-` shapes) plus a toggle-gated PII/privacy layer, across
  staged / message / range / repo modes; it fails **closed** on an unparseable
  `docs/process.toml`, matching the sh hooks. The credential *class* vocabulary
  has one home, `kitlib/secret_classes.py` — a single table both the floor and
  the transcript redactor read, so a class cannot be enforced on commit yet
  slip un-redacted into a committed log (the WI-520 PEM fix). And SR-176 rules
  that a durable finding is recorded by **class and location, never the matched
  value** — the control must not publish what it protects.

- **Content composed for an external model runner.** SR-146 makes launched
  prompts reviewable shipped files with a per-session digest (an unreviewed
  prompt assembled in source is an egress path no write-side gate covers,
  C-SEC-5). SR-175 makes the inclusion rule for each dispatched brief a
  *declared* set — with the standing discipline that the project log is excluded
  **by name** in the composers and no authorship fields are formatted into any
  prompt. Watch for a new dispatch path that composes repo content without
  landing in that declared set.

## Application

- When reviewing a decomposition, enumerate its secrets and undoable actions
  first, then demand the row that names the authority for each — that is C-SEC-2
  applied, and SR-043 is the worked example of a single such action getting its
  own row.
- Treat "the hook will stop it" as false by default. Every control here is
  supervision; ask what a human still holds (push, the `SUBAGENT_GATE` override)
  and confirm the model cannot reach it.
- For any new provider dispatch, check it against SR-175's declared inclusion
  set, not against convention — and remember the **pull channel** cannot be
  technically bounded: an enabled runner launched with permission-bypass flags
  reads the whole tree itself, so the declared rule bounds what the loop
  *assembles* and states the scope of consent, nothing more.
- For a new credential shape or scanned artifact, add the class to
  `secret_classes.py` (both sides decide together) rather than to one call site,
  and keep durable records value-free (SR-176).

## Open questions / bounded here

- **Supervision, not a sandbox — stated, not solved.** Nothing here contains a
  model that has already gone adversarial with file-write access. The kit's
  posture is to make the honest boundary *legible*, not to pretend it is a wall.
- **Stated-but-not-mechanized gaps, so their absence is not read as coverage:**
  SR-175's declared-set surface and its planted-credential dispatch block are
  not built; SR-176's redaction covers the credential classes but **not** the
  privacy-layer PII classes, so under an adopter's privacy gate a PII match can
  still reach a committed transcript. These are named build debt, not settled
  controls.
- **Deep secrets scanning is out of scope by design.** `check_privacy.py` is a
  pattern lint; gitleaks/trufflehog are a named external product category the
  kit never rebuilds. Do not review the floor as if it were DLP.
- **This pack is the drafter's reading.** Cite it to orient the hat; re-derive
  any specific claim against the cited file or row before resting a decision on
  it, and let the owner's RETURN edit settle what the roster keeps.
