# Knowledge packs (`docs/knowledge/`)

These reviewed, advisory notes preserve findings that should outlive the WI or
session that produced them. A pack records evidence and rationale that do not
belong in the requirement registries; when a finding becomes a rule, promote it
through change intake and keep the spine authoritative.

## Pack index

| Label | Topic | Components | Last reviewed |
|---|---|---|---|
| [agent-routing](agent-routing.md) | Heterogeneous agent routing and review evidence | `CMP-008` | 2026-07-15 |
| [effort-tiering](effort-tiering.md) | Evidence and cautions for per-task reasoning effort | `CMP-008` | 2026-07-15 |
| [prompt-image-token-efficiency](prompt-image-token-efficiency.md) | Native prompt text versus rasterized prompt images | `CMP-008` | 2026-07-15 |
| [iterative-optimization](iterative-optimization.md) | Choosing and stopping LLM, constructed, and hybrid optimization loops | — | 2026-07-15 |
| [parallel-scheduling](parallel-scheduling.md) | Traincar packing: DAG scheduling + clustering research (heuristics, no bound claimed) | — | 2026-07-15 |
| [co-planning](co-planning.md) | Reconciling independent WI decompositions: select-and-port over merge or consensus | `CMP-008` | 2026-07-16 |
| [instruction-file-adherence](instruction-file-adherence.md) | What degrades agent instruction-file adherence: rule count and conflicts, not bytes | `CMP-008` | 2026-08-18 |
| [traceability-enforcement](traceability-enforcement.md) | registry→code (assert-and-verify) versus code→registry (an unmaintained annotation convention), with this repo's own adherence measured | `CMP-006` | 2026-08-18 |
| [security-review](security-review.md) | **DRAFT** — the `hat.SECURITY` perspective here: secrets, irreversible process actions, and who may reach them (supervision, not a sandbox) | — | DRAFT 2026-08-30 |
| [unattended-operation](unattended-operation.md) | **DRAFT** — the `hat.UNATTENDED-OPS` perspective: the 3am failure that pages nobody (silent degrade, partial write, unbounded retry, green because nothing looked) | — | DRAFT 2026-08-30 |
| [cross-platform-scripting](cross-platform-scripting.md) | **DRAFT** — the `hat.CROSS-PLATFORM` perspective: Windows/macOS/Linux from one stdlib-preferred kit (line endings, encoding, quoting, locks) | — | DRAFT 2026-08-30 |
| [crash-atomicity-recovery](crash-atomicity-recovery.md) | **DRAFT** — the `hat.INTEGRITY-RECOVERABILITY` perspective: what the next reader finds after an interrupted write, and the reader that refuses a torn state | — | DRAFT 2026-08-30 |
| [rendered-surface-review](rendered-surface-review.md) | **DRAFT** — shared by `hat.UX-DESIGNER`/`hat.UX-ENGINEER`/`hat.ACCESSIBILITY` (and cited by `hat.CONSISTENCY`): layout priority, rendered robustness, accessibility of the generated owner surfaces | — | DRAFT 2026-08-30 |

The five `DRAFT 2026-08-30` packs above were drafted by an agent for WI-546 to
give the hats roster's new `knowledge` cells (`docs/requirements/hats.toml`) a
target; the owner reviews and cuts them at RETURN, per the roster header's own
rule. They distill this repo's own perspective for a hat rather than retrieved
external research.

The pack contract and optional research-track workflow live in
[PROCESS_OPTIONS.md](../../project-trajectory/PROCESS_OPTIONS.md#research-track--knowledge-packs).
