+++
id = "WI-1021"
title = "Each code file declares its one component in a Component header, and component membership is read from the headers"
workstream = "process"
sr_refs = ["SR-159", "SR-165", "SR-049"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Variant F's first row (F-1), filed on trunk on 2026-11-21 after the operator
chose to build F before WI-1015 (queue-drill HANDOFF §3.1 Q1 (a), §3.3).
F point 1, ruled in revision 35: component membership has one home, the
realization. A code file declares its component in its header; the LLR's
`component` cell stops being the membership source (it leaves the schema in
WI-1023).

Today no file declares a component. Membership is derived by
`kitlib.spine.module_components` (LLR-373, "the join's one home", WI-1005):
a file belongs to every component its LLRs' `component` cells name. 34 files
carry LLRs tagged to more than one component, so the cross-component rule
(LLR-067) treats their edges as multi-membership advisories. That is
WI-1015's loophole 2, which this row dissolves (WI-1015 is restructured into
F's rows; HANDOFF §3.3 N1).

**One component per file (operator, 2026-11-21, §3.3 N3).** A file is
ascribed to one component. Reuse keeps one owner: the eight files on
`docs/kernel-modules-allow` are owned by CMP-006 and imported across
components without a seam (OI-48). Configuration keeps one owner: other
components read it through a `file` interface. Most of the 34 have a clear
majority (`trace.py` 25 to 1, `integrate.py` 17 to 1); a minority LLR is
placed later through the interface it constrains (WI-1024), not by the
file. The real calls are the near-even splits: `check.py` (9/4/1),
`acceptance_record.py` (8/5/1) and the files at 1 to 1 (`check_doc_refs.py`,
`census.py`, `held_status.py`, `kitlib/authority.py`, `id_carrier.py`). A
file doing two components' work is evidence about the partition (OI-14); it
is flagged and filed as its own row, never split here.

**Where the header goes (F point 1, revision 16).** In the same header that
holds the file's `Contracts:` marker, by the file's comment syntax (Done-when
1). Not built here: the inventory-entry form for a file type with no comment
syntax; no file in this row's scope lacks one, so it is filed when an
adopter needs it.

**The component registry's prose.** CMP-006's `notes` describe membership by
LLR tags and the multi-membership advisories this row retires; this row
rewrites those sentences. Removing the file names component rows still carry
is WI-1028's (no code in row text).

**Downstream.** Adopters gain the header grammar. This row writes its own
RESYNC entry, the first of variant F's (each F row writes its own entry,
apply in landing order; the operator: re-sync need not be one entry). Items
4 and 10 of the review-churn plan are not bundled with F.

## Scope answers

- **S1.** One deliverable: the header grammar, its reader and check, the
  headers written, and membership switched to them. They land together:
  headers without the switch are a second home, and the switch without
  headers empties every component.
- **S2.** The headers become the membership input to strict checks and the
  DevStg-Arch derivation, so a `## Trust` section follows.
- **S3.** The grammar, its carriers and the scope are closed (Done-when 1
  and 2); anything else is a finding or outside the rule, as stated there.
- **S4.** `single`: several script families (`kitlib/spine.py`,
  `arch_components.py`, `arch_seams.py`, `gen_components.py`,
  `derive_stage.py`, `gen_arch_map.py`) and a grammar over file headers.
- **S5.** No state, domain value or boundary is added; membership changes
  its input. Re-cut LLRs (text only, drifting): LLR-373 (the join), LLR-067
  and LLR-374 (the cross-component rule and its import resolution), LLR-199
  and LLR-049 (the component views), LLR-172 (the derivation record); the
  lane's plan completes the list from the code. The ruled table may move
  edges across a boundary; each is covered (Done-when 5).
- **S6.** `needs` is empty: nothing this row reads is unbuilt. No new
  package, tool or service.
- **B4.** The one-component table is the operator's ruling (Done-when 4).

## Trust

The header becomes the authority on a file's component, which strict checks
and the stage derivation read (PROCESS.md §3, "When a guard is owed").

- **Producer.** A person or model editing the file in a lane (the supported
  route), and this row's migration. No script writes a header.
- **Failed write.** A header left absent, doubled, malformed or naming no
  live CMP row. Each is a finding (Done-when 1); no kit route half-writes a
  header.
- **Consumers.** The one header reader (beside
  `gen_arch_map.module_contracts`), read by the membership home in
  `kitlib/spine.py`, `arch_components.py`, `arch_seams.py`,
  `gen_components.py` and `derive_stage.py`.
- **Ruling, shared by every consumer.** A file whose declaration is absent
  or invalid belongs to no component: it is reported, and every import edge
  touching it is reported as unclassified, never treated as internal or
  exempt.

## Done-when

- [ ] **Grammar.** A declaration is one line reading exactly
      `Component: CMP-NNN` (digits as the id space spells them), placed by
      file type: a Python module docstring; a `#` line in the top-of-file
      comment block for `.sh`, `.command`, `.ps1`, `.toml`, `.ini`, `.csv`
      and files with no suffix (the hooks, `docs/agents-enabled`); a `REM`
      line in the top-of-file comment block for `.cmd`; a line inside the
      opening `<!-- ... -->` comment of a `.md` file (`docs/runtime-flows.md`,
      `docs/status.md`). One reader, beside the existing `Contracts:` header
      reader, returns each in-scope file's component. A file with no
      declaration, two declarations, a malformed one or an id no live CMP
      row has is a finding; warn-first, failing `--strict` from DevStg-Arch
      upward, like the cross-component rule it feeds.
- [ ] **Scope, closed.** Every file under `[paths] src` of a type the
      grammar lists (`README.md` excluded as documentation), and every file
      the contract scan reads as a file owner today
      (`arch_interfaces._owner_files`: 13 non-directory paths, the hooks,
      configuration files and registries among them). A file of another
      type under `[paths] src` is outside the rule unless it states a
      `Contract IF-NNN:` body, which is then a finding naming its type. A
      file outside the scope may carry a declaration, judged by the same
      grammar.
- [ ] **Membership reads the headers.** `kitlib.spine.module_components`'s
      callers (`arch_components`, `arch_seams`, `gen_components`) and the
      DevStg-Arch derivation read file membership from the one header
      reader, under the Trust ruling. No check compares an LLR's
      `component` cell with a header. The LLRs in S5 are amended to the
      header source (Accepted: text only, drifting for adjudication).
- [ ] **The table, ruled by the operator.** The lane's plan lists each of
      the 34 files with LLRs tagged to several components: its candidate
      components with LLR counts, the pick and its reason, and a flag where
      the file does two components' work. The lane commits the table and
      stops; the coordinator puts it to the operator. The reader and the
      headers for every other file may be built meanwhile. The lane goes
      to review only once the ruling is recorded in this spec's Context.
      Each flagged file keeps the ruled header and gets a queued row filed
      on trunk.
- [ ] **No new silence.** Every import edge the ruled headers turn into a
      crossing is covered by an existing interface row naming both files,
      shown inside one component, or covered by a new `Drafted` `call` row
      from the lane's id range. The multi-membership advisory retires, and
      CMP-006's `notes` stop describing it (drifting for adjudication).
      `trace.py --strict` and `check_trajectory --strict` are clean.
- [ ] Every in-scope file carries its declaration; the kernel allowlist is
      unchanged.
- [ ] A RESYNC entry tells adopters the grammar, that headers are owed from
      DevStg-Arch upward, and that it is the first of variant F's entries.
      PROCESS.md §8 states where the header goes, once.
- [ ] Tests: red-before for each finding class, each carrier syntax, the
      Trust ruling (an unclassified edge) and membership from headers;
      every test module importing a changed module runs green.
