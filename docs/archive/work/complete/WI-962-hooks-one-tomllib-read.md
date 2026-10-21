+++
id = "WI-962"
title = "The commit and push hooks read the policy file through one tomllib read in their shared interpreter probe, and no hook reads configuration as text"
workstream = "process"
sr_refs = ["SR-031", "SR-019", "SR-020"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

Closed at its landing on 2026-10-21, after its gate, in a headless leg:

- The three shipped hooks (`pre-commit`, `commit-msg`, `pre-push`) read
  no configuration as text: each calls the probe's `kit_policy` right
  after `kit_python`, which resolves the kit scripts directory once for
  all three (an override naming no directory refuses with no fallback)
  and asks `check_privacy.py --hook-policy` for one closed answer
  (`privacy=off`, `privacy=on review=require`, `privacy=on
  review=warn-unwired`, `refuse=mixed`, `refuse=unreadable`); any other
  answer or a failed read refuses, naming the cause.
- `check_privacy.py` parses `docs/process.toml` once per run
  (`_load_process_toml`), every gate reads that parse, an unreadable file
  is its own outcome, and `read_privacy_review` and `hook_policy_answer`
  carry the posture rule and the answer (IF-298's contract body).
- `docs/runtime-flows.md` Flow 3, the two prose claims, and one RESYNC
  entry (forced: a malformed policy file refuses every commit and push; a
  `KIT_SCRIPTS_DIR` naming no directory refuses at every hook; a legacy
  privacy-check reading `TRUE` reads ON at pre-push).
- Spine: SR-031, LLR-021 (gaining SR-031), LLR-031, TC-021 and TC-031
  amended and re-attested (sitting 003, MEANING+BLESS; the act in the
  lane); IF-037's consumers amended and IF-298 added (Drafted).

## Context

Review-churn item 10, step 2's build (queue row P7). The ruling (plan,
"Owner rulings" row 10 and "Resolved (revision 5)"): since WI-880 all three
hooks refuse without Python 3.11+, so the shell grep and the one-key-per-line
shape rule can go, and "the remaining shell reads (the missing-scripts-
directory refusal, the mixed-config refusal, and the legacy
`docs/privacy-check` read …) become one `tomllib` read in `kit-python.sh`,
after the interpreter check". "The shared `tomllib` read lives once, in
`kit-python.sh` beside the interpreter probe, not in three hook copies."

**The premise holds (verified).** Each shipped hook sources the probe and
exits on its refusal: `hooks/pre-commit:98-99`, `hooks/commit-msg:88-89`,
`hooks/pre-push:123-124` (`kit_python … || exit 1`, `hooks/kit-python.sh`
`kit_python`, lines 26-42).

**What reads configuration in shell today** (the plan lists each read by
line):

- `_ptoml_body` and `process_declares`, three byte-identical copies:
  `hooks/pre-commit:56-80`, `hooks/commit-msg:37-61`, `hooks/pre-push:84-108`.
- The mixed-config refusal, three copies: `hooks/pre-commit:82-93`,
  `hooks/commit-msg:63-74`, `hooks/pre-push:113-118`. All three run **before**
  the interpreter probe today.
- The privacy gate, `hooks/pre-push` `privacy_declared_true` (139-148): a
  textual read of `[policies] privacy_check`, then the legacy
  `docs/privacy-check` first word (146). Its answer decides whether a push
  needs the LLM privacy review (162).
- The unwired-reviewer posture, `hooks/pre-push:208-220`: a textual read of
  `privacy_review`, then the legacy `docs/privacy-review` first word (219).
  **No Python reader of this key exists** (grep over `scripts/` finds only
  `agent_policy.PROCESS_KEYS` and bootstrap's migrator), so it is a shell-only
  gate today. The plan's list of three reads omits it; it is the same class
  and this row takes it.
- The scripts-directory resolution and refusal, three copies that disagree:
  with `KIT_SCRIPTS_DIR` naming a missing directory, `pre-commit` (109-131)
  refuses, while `commit-msg` (96-109) and `pre-push` (`find_scripts_dir`,
  64-74) fall back to `scripts/`.

**Python already mirrors the shell grammar.** `check_privacy._process_gate`
reads `[policies]` with `tomllib` and falls back to `_text_declares` /
`_strip_comment` "so this reader cannot conclude 'absent' about a key [the
hooks] would act on" (check_privacy.py 218-300). `tests/test_process_config.py`
`sh_privacy_declared_true` runs the hook's own sh functions against `tomllib`
over an adversarial table, including the 2026-08-08 trailing-comment decoy
(`privacy_check = true # privacy_check = false`), which made the gate fail
open.

**Anchor.** SN-028 (approved): one home, a dial declared twice is refused.
SR-031 (approved), "Declared-policy readers agree … one parse, one answer,
across the hooks, the loop and the checkers alike", is the requirement this
row delivers. SR-019 and SR-020 (approved) carry the hooks' refusals, which
this row keeps.

**Not this row.** The shape rule itself (SR-137's line-shape contract,
`agent_policy.process_shape_findings`, `GREPPABLE_KEYS`, check_privacy's
textual mirror and IF-037's "one key = value per line") is a separate,
deletion-only deliverable that can land only after this one (S1). The
`[ -f docs/stack.ini ]` presence test at `hooks/pre-commit:362` is item 10
step 4's (it moves when `stack.ini` does). `setup.sh:59-60` and
`setup.ps1:72-73` read only the legacy `docs/privacy-check` for an advisory
and never `process.toml`; they are not hooks and gate nothing, so they go to
WI-817's legacy retirement.

## Deliverables

1. **One read, in the shared probe.** `kit-python.sh` gains, after the
   interpreter probe, the hooks' one resolution of the scripts directory and
   one interpreter invocation that reads the policy with `tomllib` and answers
   the three questions the hooks ask: is the configuration mixed, is the
   privacy gate on, and is the unwired-reviewer posture `warn-unwired` or
   `require`. Its answer is a closed set of tokens; the shell acts only on an
   exact token and refuses on anything else. Whether the read is inline in
   the probe or calls the kit's existing privacy reader is the plan's choice
   (recommended: the existing reader, so one parser serves SR-031); either way, the hooks and the checker answer alike over
   the adversarial table.
2. **The hooks lose their text reads.** `pre-commit`, `commit-msg` and
   `pre-push` delete `_ptoml_body`, `process_declares`, the mixed-config
   function, `privacy_declared_true`'s grep and the `privacy_review` grep, and
   their own scripts-directory blocks, and call the probe's functions. The
   mixed-config refusal moves after the interpreter probe (on a machine with
   no Python it is the interpreter refusal that names the fix; both refuse).
3. **Records.** SR-031's acceptance and coincident text drop "the two
   delivered reader grammars" for one parse (capability voice, below);
   TC-031's method and LLR-021's detail follow; IF-037's consumer list is
   checked against the new reader. One RESYNC entry (the hooks are kit-owned
   and ship to adopters as `.githooks/`, `kitlib/bootstrap_manifest.py:768`).

## Trust

Written under [PROCESS.md §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

The read gives a file authority over three gates: the mixed-config refusal
(refuses a commit or push), the privacy gate (decides whether a push must pass
the LLM privacy review), and the unwired-reviewer posture (decides whether an
unwired reviewer refuses the push or only warns).

- **Producer.** `docs/process.toml`, hand-edited by the owner or an agent, or
  written by `bootstrap.set_process_key` (one line at a time); during
  WI-817's window, the legacy one-word files `docs/privacy-check` and
  `docs/privacy-review`. `KIT_SCRIPTS_DIR` is set by a delegating wrapper
  (this repo's `.githooks/pre-commit:11` and `.githooks/commit-msg:13`). A
  failed write is a partial or unparseable file, a stray byte-order mark, a
  key under the wrong section, or a wrong-typed value.
- **Consumers** (grep): `project-trajectory/hooks/pre-commit`,
  `project-trajectory/hooks/commit-msg`, `project-trajectory/hooks/pre-push`,
  via `project-trajectory/hooks/kit-python.sh`; shipped as `.githooks/*` in
  every scaffold. The checker that must agree with them is
  `project-trajectory/scripts/check_privacy.py` (`read_privacy_enabled`,
  `_process_gate`), run by the same hooks.
- **Ruling** (fail closed; no read failure ever opens a gate):
  - *Absent `docs/process.toml` and absent legacy files:* nothing is
    declared, so the privacy gate is off and the review posture is moot. This
    is the opt-in default SR-018 states and every other reader already
    returns, not a read failure.
  - *Present but unreadable or unparseable* (OS error, decode error, TOML
    error): the hook **refuses** the commit or push, naming the file and the
    parser's message (decided at filing, `docs/decisions/coordinator-2026-10-20.toml#D-006`;
    today the checker reads it as ON instead).
  - *Missing key in a parsed file:* the legacy file answers during WI-817's
    window (exactly `true` turns privacy on; exactly `warn-unwired` opts
    down), else off for `privacy_check` and `require` for `privacy_review`.
  - *Wrong type or unknown value:* `privacy_check` other than the boolean
    `false` reads ON; `privacy_review` other than exactly `"warn-unwired"`
    reads `require`.
  - *Mixed:* `[policies] privacy_check` present and `docs/privacy-check`
    present refuses at all three hooks, naming both files and the migrator,
    as today.
  - *The read itself fails* (the interpreter exits nonzero, prints nothing,
    or prints anything outside the enumerated tokens): refuse, naming the
    read.
  - *Scripts directory:* one resolution for all three hooks. A
    `KIT_SCRIPTS_DIR` that names no directory refuses (pre-commit's rule
    today); with none set, `scripts/` then `Scripts/`; none found refuses.
- **The bound** (PROCESS.md §6, "Review threat model"): the promise covers
  files the kit's routes and a person's hand edit produce, and the legacy
  files during the window. A shimmed interpreter, a tampered hook and
  `--no-verify` are outside it (SR-019's pair with the hosted re-run).
- **Named failure class for every review brief** (plan item 10,
  "Trade-off"): the 2026-08-08 decoy, a gate that reads off from text a
  parser reads as on.

## Done-when

Each named test fails on the code before the change.
- No shipped hook and not `kit-python.sh` reads `docs/process.toml`,
  `docs/privacy-check` or `docs/privacy-review` with a text tool; a
  structural test pins it.
- Each hook runs the one read once, after the interpreter probe.
- Over the adversarial table in the process-config suite (trailing-comment
  decoy, dotted key, inline table, multi-line string, key under another
  section, byte-order mark, wrong type), the shipped hook's read and
  `check_privacy.read_privacy_enabled` return the same answer for every
  case, driven through the real hook, not an extracted function.
- All three hooks refuse a mixed config naming both files; refuse an
  unparseable or unreadable `process.toml` naming it; refuse when the read exits nonzero or answers
  outside its tokens.
- `pre-push`, when the privacy gate is on: `privacy_review =
  "warn-unwired"` warns and proceeds with no reviewer; any other value, a
  wrong type, or absence refuses; the legacy `docs/privacy-review` behaves
  the same during the window. When the privacy gate is off, no push is
  refused for an absent or unwired privacy reviewer, whatever
  `privacy_review` holds.
- All three hooks refuse a `KIT_SCRIPTS_DIR` naming a missing directory.
- `kit-python.sh` parses under bash 3.2 (`tests/test_shell_portability.py`).
- One scaffold bootstrap: a fresh scaffold ships the new probe and hooks,
  and commits through them.
- SR-031, TC-031 and LLR-021 amended as below and judged at the lane's
  sitting. Draft for SR-031's acceptance, capability voice: "Every enforcer
  reads the same value for the same dial through one parse; the hooks' and
  the checkers' answers agree over the adversarial file-shape table, the
  trailing-comment decoy included, and an unreadable declaration refuses at
  the hooks rather than reading a default."
- The RESYNC entry: the hooks overwrite; the forced changes are the
  malformed-file refusal and `pre-push`/`commit-msg` refusing
  a mis-set `KIT_SCRIPTS_DIR`.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` clean.

## Calls decided at filing

A headless leg filed this row, so its filing calls are the coordinator's
delegated decisions, for the owner to confirm or overrule:

- **The malformed policy file** (Trust): a present but unreadable or
  unparseable `docs/process.toml` refuses at all three hooks, naming the
  file and the parser's message, where today it reads as privacy ON and
  the commit proceeds (`docs/decisions/coordinator-2026-10-20.toml#D-006`,
  high risk: a forced change for adopters, in the RESYNC entry). The
  fixing commit passes, since the hook reads the working tree.
- **The scripts directory** (lane-settled): one resolution for all three
  hooks, pre-commit's rule today.

## Scope answers

- **S1.** One deliverable: the hooks' policy read, with its records. The
  shape-rule retirement (SR-137's line shape, `process_shape_findings`,
  `GREPPABLE_KEYS`, check_privacy's textual mirror, IF-037's `data` cell)
  lands independently and only after this row; recommended as its own row,
  filed on trunk once this row lands, `planmode = "none"` (deletion). It
  lands before item 10 step 5, whose triple-quoted route strings need the
  shape rule gone.
- **S2.** Yes: three gates; the Trust section above.
- **S3.** Closed: the read's answer is an enumerated token set; anything
  else refuses. Each input class has a stated outcome.
- **S4.** `single`: a Trust section, three hook files plus the probe and the
  checker, and a promise over the file-shape space.
- **S5.** No new state. The privacy and review gates get a new reader
  (`kit-python.sh`, or the checker it calls); the mixed-config refusal moves
  after the probe. IF-037's consumers are re-checked. No new component.
- **S6.** No hard `needs`. WI-880 and WI-926 (the probe and the
  scripts-directory refusal) are landed. Overlap: WI-817 (queued, needs
  WI-798) edits `check_privacy.py` and `agent_policy.py` and retires the
  legacy files this row still reads; whichever lands second rebases, and
  WI-817 then deletes the legacy branch from one place. No queued or active
  row edits the hooks or the probe. No new dependency.
- **B3.** The hooks trust one read made at the hook run; nothing re-derives
  a past decision.
- **B4.** No owner act. The malformed-file ruling is a delegated decision
  the owner confirms or overrules (`docs/decisions/coordinator-2026-10-20.toml#D-006`,
  high risk); an overrule rewrites that Trust line before the claim.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-20; CHANGES-REQUESTED,
findings=2):

- **MAJOR, S3 (the unwired-reviewer Done-when refuses a privacy-off push):
  adopted.** The `pre-push` bullet now opens "when the privacy gate is on"
  and adds "When the privacy gate is off, no push is refused for an absent
  or unwired privacy reviewer, whatever `privacy_review` holds", matching
  Trust's "the review posture is moot".
- **MINOR, S2 (no link to PROCESS.md §3's guard rule): adopted.** Trust now
  opens with a link to PROCESS.md §3, "When a guard is owed".

Confirming round (Codex Sol, medium, convergence stance, 2026-10-20): APPROVE, findings=0; the dispositions above are confirmed.
