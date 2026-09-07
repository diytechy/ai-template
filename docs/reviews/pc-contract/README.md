# Independent PC contract proposal reviews

These are real provider responses to frozen proposal inputs. They are not
primary-turn records, accepted registry judgments, implementation verification,
or permission to publish snapshots. The coordinator stayed paused throughout.
The current author proposal is the
[PC contract packet](../../ai-template-redesign-2026-09-05-codex/PC-BATCH-CONTRACT.md).

## Round 001 — RETURN

[Verbatim result](round-001/review-result.md),
[provider metadata and input hashes](round-001/review-meta.json).
The sibling files preserve the exact reviewed patch, inventories and complete
chain input. `PC-BATCH-CONTRACT.txt` is the exact Markdown input with only its
filename extension changed so historical relative links are not interpreted
from the archive directory. Hashes refer to original input bytes and paths.

The logged invocation used the configured ANTHROPIC-FABLE strong route,
`claude-fable-5-1`, medium effort, with tools disabled and prompt on stdin.
The actual provider session ID and result usage are in the metadata. Raw
stream and prompt are retained locally under `out/run-logs/pc/`; no machine
approval artifact was synthesized from the response. The author's correction
of the review's mistaken row count and absent-test assumption is recorded in
the revised packet, without changing the reviewer output.

## Round 002 — RETURN

[Verbatim result](round-002/review-result.md),
[provider metadata and hashes](round-002/review-meta.json).
`round-002/review-prompt.txt` preserves the complete frozen input verbatim,
including the then-current packet, chain and supplementary source. The response
accepted the design direction but required cumulative ownership and explicit
partial-close refusal, plus smaller wording corrections. The current proposal
addresses those findings; this round accepts no live registry cells.

## Round 003 — RETURN

[Verbatim result](round-003/review-result.md),
[provider metadata and hashes](round-003/review-meta.json).
`round-003/review-prompt.txt` preserves the full frozen input. This round
accepted the preceding corrections and returned the resume requirement/test
alignment and conditional TC-061 ownership. The revised packet explains why
resume belongs to the dispatcher orchestration pair under SR-156 and why the
optional abandoned-claim wording was not adopted. No live approval resulted.

## Round 004 — conditional APPROVE for authoring/intake readiness

[Verbatim result](round-004/review-result.md),
[provider metadata and hashes](round-004/review-meta.json).
`round-004/review-prompt.txt` preserves the full frozen input. This opinion
requires F-12, F-13 and F-18 corrections and explicitly says those corrections
alone need no fifth opinion. The author applied them and recorded the
[exact correction verification](authoring-corrections.json). Only SR-144's
Requirement and LLR-150's Detail changed between the reviewed and corrected
candidate registry trees; F-18 is the complete proposed-row ownership table.
F-14's hard predecessor edge is a condition of future intake, not a claim that
a queued WI already carries it. Optional clarity suggestions remain for the
bound turn. The result still withholds live acceptance, publication and deletion.
