# TC-279 sample — sampled new-reader inspection of DA-011, drawn at f2bc66c1

The sample record the [sampled new-reader inspection](../../test/inspection-procedures.md#sampled-new-reader-inspection)
asks for: each reader's statement beside the part's linked requirement and
design rows, with the adjudicator's agreement ruling. The verdict on the
sample is [001-ADJUDICATE-f2bc66c.md](001-ADJUDICATE-f2bc66c.md). Rubric:
[sampled-new-reader](../../rubrics/sampled-new-reader.md), at revision
`1f1dc64e` (anchors R1, R2, B1, B2).

## The draw

Taken by the unattended coordinator, not by any part's author. Seed: trunk
HEAD `f2bc66c12fc8b8702af6d93568ddba01dbb00278` as an integer. Frame: every
function or class, at any depth, under the declared readability roots
`project-trajectory/scripts` and `tests` (`docs/stack.ini` `[paths]`) whose
docstring contains the text `Implements:`; 423 parts, sorted, then
`random.Random(seed).sample(parts, 5)`. The adjudicator re-ran the draw at
`f2bc66c1` and got the same five parts. The script, as run:

```python
roots = ["project-trajectory/scripts", "tests"]
head = git rev-parse HEAD
parts = [(path, node.name, node.lineno)
         for every FunctionDef/AsyncFunctionDef/ClassDef found by ast.walk
         whose ast.get_docstring contains "Implements:"]
parts.sort(); rng = random.Random(int(head, 16)); rng.sample(parts, 5)
```

**The frame is not the procedure's.** The procedure defines a part as "one
function, class or module-level block with its own back-link". Compared with the
kit's own back-link harvest (`gen_arch_map.declaration_sites`, which encloses each
literal `Implements:` line to its symbol), about 516 parts carry a back-link.
The frame left out about 101 of them, roughly a fifth, and none of these could
be drawn:

- 8 module headers;
- 82 module-level blocks (constants whose back-link is a `# Implements:` comment);
- 11 functions whose back-link is a comment above the `def` (mostly `main`).

The frame also held 8 functions whose docstrings only mention the word
`Implements:` and carry no back-link, so they could have been drawn. One example
is `trace._implementing_modules`. None of the five drawn parts is in either
group: each of them is a real back-linked part.

Reader kind, for all five: a fresh Claude Sonnet 5.5 session, told that it did
not author the part. Each read only the part's code and the rows its
`Implements:` names, and did not ask the author.

## The parts, the statements and the rows

### 1. `project-trajectory/scripts/session_keep.py:268` `write_tombstone`

- **Linked rows:** SR-227, LLR-270 (CMP-008).
  - SR-227: a retained adjudicator session is "retire[d] at once when a call
    on it fails".
  - LLR-270, the tombstone clause: a lockless `<record>.retire` file is written
    whole, naming the session, the reason and the lease holder. It is applied at
    once if the lock is free within a second, and otherwise by every locked read
    (`load_honoured`). The lockless keep-warm read skips a marked record.
- **Statement (reader 1).**
  - What it does: builds `{session_id, reason, holder}` from the kept session
    and writes it as JSON to a `.retire` file beside the route's record. It writes
    through the whole-file temp-and-replace helper and deliberately takes no lock.
    The function retires nothing itself; it leaves a durable marker that locked
    reads (`load_honoured`) apply.
  - Why it exists: a launch that fails after resuming a retained session must
    retire that session even when the store lock can't be had at that moment.
    The tombstone is the lock-free way to record that decision, written first,
    applied at once if the lock comes within a second, and otherwise applied by
    the next locked read. This serves SR-227's retire-at-once rule.
  - Inferred: the shape of `keep` from attribute use.
- **Ruling: AGREES.** The behaviour matches the code. The purpose is LLR-270's
  tombstone clause and SR-227's retire-at-once clause, stated without
  contradiction. The inference about `keep` is correct.

### 2. `project-trajectory/scripts/session_keep.py:282` `load_honoured`

- **Linked rows:** SR-227, LLR-270, as for part 1.
- **Statement (reader 2).**
  - What it does: `store_load`s the record and reads the tombstone. With no
    tombstone, or one it cannot read, it returns the record unchanged.
  - When both are dicts: it `_retire`s a matching session with the tombstone's
    reason (default "session unusable"), drops the lease if the holder matches,
    and then `store_save`s.
  - In every case it then deletes the tombstone, ignoring OS errors, and returns
    the record. Callers hold `store_lock`.
  - Why it exists: every locked read applies a pending retirement and lease
    release before anything else sees the record. This is how SR-227's "retired
    at once when a call on it fails" holds under LLR-270's tombstone.
  - Could not explain: why a tombstone is deleted unapplied when the record is
    not a dict.
- **Ruling: AGREES.** The described behaviour, including the flagged edge, is
  exactly the code's. The flagged edge is a rationale for a corner case, not the
  part's behaviour or purpose. `store_load` returns None only for a record that
  is absent, unreadable or not this route's, and its docstring says such a store
  "reads as 'no session', and the next launch mints". So no retained session is
  left for the tombstone to retire, and removing it is the right clean-up. The
  rows' tombstone rule speaks to a live record and is not contradicted. This is
  out of scope, not B1.

### 3. `project-trajectory/scripts/kitlib/spine.py:447` `sn_all_ids`

- **Linked rows:** SR-189, LLR-215 (CMP-006).
  - SR-189: needs resolve to the declared stakeholders.
  - LLR-215: the needs file gains a stakeholder list, and "sn_all_ids scrapes
    need ids from the need tables only, so a need id quoted in a stakeholder's
    prose never joins the need universe".
- **Statement (reader 3).**
  - What it does: returns every SN id in a needs registry's text, as a token
    scrape that drops `-000` ids.
  - For a TOML registry it narrows the text to the `[need.*]` tables first, so
    ids in stakeholder prose or comments stay out.
  - `carrier` is the file suffix. With no carrier, the text counts as TOML only
    when it parses to at least one table.
  - "Markdown, unparseable text, and TOML with no `need` table get a whole-text
    scrape."
  - Why it exists: it is the single definition of the need universe, used by both
    the stage derivation and the orphan listing. It reads only the need tables, so
    an id quoted in a stakeholder's prose never becomes an approved-but-uncited
    need that caps the stage.
- **Ruling: AGREES on purpose and the main behaviour. One branch is misstated.**
  - A TOML document that parses but has no `need` table yields the EMPTY set,
    not a whole-text scrape. The adjudicator confirmed this by calling the
    function at `f2bc66c1`:
    - `sn_all_ids('[stakeholder.STK-01]\ndescription = "owns SN-005"\n', '.toml')`
      returns `set()`.
    - The same text with no carrier also returns `set()`.
    - Markdown, and `.toml` text that does not parse, do take the whole-text
      scrape.
  - On that degenerate input the reader's account would let stakeholder prose
    into the universe, which is what LLR-215 rules out. The code itself keeps to
    the row.
  - A nit: "at least one table" should read "a non-empty document".
  - This is not ruled B1. The reader states the row's rule and the part's
    purpose correctly. The slip is about which fallback an input with no need
    tables takes, and no live needs registry is that input. It is the sample's
    closest call (see the verdict).

### 4. `project-trajectory/scripts/trace.py:1610` `triangle_findings`

- **Linked rows:** SR-157, LLR-002 (CMP-006).
  - SR-157: every declared spine-rule violation is reported, naming the row.
  - LLR-002: id, structure and SR/LLR citation coherence (`triangle_findings`)
    form the always-valid `--strict-integrity` floor, because they are wrong the
    moment they are written.
- **Statement (reader 4).**
  - What it does: maps each LLR to its SR-Refs. For each TC that cites at least
    one SR, every cited LLR whose parent set does not meet the TC's cited SRs
    yields a message naming the TC, the LLR, the cited SRs and the LLR's parents.
    A TC citing no SR is skipped.
  - Why it exists: a TC may discharge an SR and an LLR together. The LLR's
    SR-Refs is the authoritative parent link, and a mismatched pair is wrong at
    any stage, so it is an always-on integrity finding (LLR-002), serving
    SR-157's named-row reporting.
  - Inferred: `refs` and `ID_PATTERNS` from their names.
- **Ruling: AGREES.** It matches the code line for line, and the call site
  (`integrity += triangle_findings(...)`) confirms the integrity-floor placement.
  Both inferences are correct: `kitlib.spine.refs` splits a multi-ref cell into
  ids.

### 5. `project-trajectory/scripts/rendering/traj_render.py:451` `_cedge_marker`

- **Linked rows:** SR-054, LLR-105 (CMP-009).
  - SR-054: dashboard usability.
  - LLR-105: every control on a node fill clears 3:1 in both themes, computed
    per fill. The descend arrow's marker head takes a per-ink marker because
    marker content renders from the defs tree. The rationale: the fixed arrow
    measured 1.06:1 light and 1.99:1 dark.
- **Statement (reader 5).**
  - What it does: for a hex fill, returns `cedgearrow-<hex>` and the white or
    near-black ink that contrasts more (`_ring_ink`). For a missing fill or a
    theme token, it returns `cedgearrow` and `None`, so the CSS
    `var(--accent)` fallback applies.
  - Why it exists: the old fixed-accent arrow had 1.06:1 and 1.99:1 contrast. A
    marker cannot inherit the host's `--ring`, so there is one marker per ink.
    This serves LLR-105's 3:1 floor under SR-054.
  - Inferred: `_ring_ink` from its name.
- **Ruling: AGREES.** It matches the code and LLR-105 exactly. The inference is
  correct: `_ring_ink` returns one of `RING_INKS = ("#ffffff", "#0f172a")`.

## Bound

Even on a valid frame, a passing sample bounds discovery to these five parts.
It says nothing about the parts the sample did not reach (rubric intent, B2).
