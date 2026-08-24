# Raw return - batch 3 (TC-196, TC-195, TC-197, TC-182, TC-188)

Unedited final message from `OPENAI-TERRA` (`gpt-5.6-terra`, `codex exec`),
captured with `--output-last-message`. Adjudicated in `RESUME.md`.

```
=== TC-196 Method
SUGGEST: Drive a frame with two parties, one with two crossings and one with none; two crossings, one realized by a tie-back interface row and one unrealized; and one external-to-external relationship. Assert reads return SR, LLR, and TC in id order; join tie-backs from the interface registry with their tied side; retain an unrealized crossing with empty realization; resolve the display entity from the frame rather than the crossing row; and return an interface whose endpoint is outside the tree and ties back to nothing with its recorded reason. Render and assert the census equals registry counts, every declared row reaches the diagram, inbound direction points to the system and outbound direction to the party, the unrealized crossing appears in markup and table, and the block precedes the module map. With no frame, assert bytes match the pre-view artifact and a round trip; a -000-only frame is vacuous; a frame without symbols still yields the architecture tab. Read the meta repository frame as data and assert locked counts, one unrealized crossing, and three no-tie-back rows with their reasons.
CUT-REDUNDANT: none
CUT-KEPT: Empty realization, display-name resolution, the external endpoint case, both vacuity guards, and the meta-frame assertions remain because they prevent silent loss of declared boundary data.
RISK: Combining the checks into one fixture can obscure a missing assertion unless each stated outcome remains independently asserted.

=== TC-196 Expected
SUGGEST: LLR-200 / SR-168 outcome: the view returns id-ordered SR, LLR, and TC data; its census equals registry counts; every frame row, including the zero-crossing party and external-to-external relationship, is diagrammed with system-perspective direction; the unrealized crossing and no-tie-back reason remain visible; the block precedes the module map; no-frame and -000-only frames are vacuous; a frame without symbols shows the architecture tab; and the meta frame matches its locked counts, one unrealized crossing, and three no-tie-back reasons.
CUT-REDUNDANT: The generic conclusion that it satisfies the parent acceptance.
CUT-KEPT: LLR-200 and SR-168 remain for traceability.
RISK: none

=== TC-195 Method
SUGGEST: Drive a two-component spine. Assert membership derives from the design-tier Component tag, reaches the requirement tier, and lists its modules; a design row with no hat cell inherits its SR perspectives, and changing those perspectives changes the view without editing that design row. Assert a requirement without a design child appears once in counted unplaced and in no component; a two-component requirement appears shared in both, while a one-component requirement is not shared; same-component seams are internal, cross-component seams are boundaries of both, untagged interfaces are placed from endpoints, and unresolved interfaces are unplaced. With one Approved and one Drafted component, assert emitted cells contain no maturity key or either term. Open the generated view with network disabled and assert no external fetch. --check passes when fresh, fails after a registry move, passes after regeneration, and fails when an expected view is missing; bytes contain no CRLF and repeated renders agree. A repository lacking a source registry omits that view without an empty artifact and remains byte-stable. A CMP-only -000 repository emits no view and exits zero on generation and --check.
CUT-REDUNDANT: none
CUT-KEPT: Derived perspectives, unplaced and shared coverage, endpoint placement, the no-maturity assertion, freshness failures, missing-source omission, and -000 vacuity remain because each distinguishes an omitted view from a silently empty or stale one.
RISK: The compact seam cases must still assert internal, boundary, endpoint-derived, and unresolved placement separately.

=== TC-195 Expected
SUGGEST: LLR-199 / SR-070 outcome: the view is derived from registry joins, usable with network disabled, byte-stable, and free of CRLF; unplaced, shared, internal, boundary, endpoint-derived, and unresolved entries appear in their declared locations; maturity labels do not appear; --check rejects drift and an expected missing view; a missing source registry omits its view without an empty artifact; and a CMP-only -000 repository emits nothing and exits zero.
CUT-REDUNDANT: The generic conclusion that it satisfies the parent acceptance.
CUT-KEPT: LLR-199 and SR-070 remain for traceability.
RISK: none

=== TC-197 Method
SUGGEST: Drive each declared checker rule directly. Assert the orphan pass emits SR, LLR, TC, then SN and returns exactly the at-fault IDs in its findings; a Drafted SR disables child-completeness while retaining SN linkage; PB Refs accepts IDs and LLR Module paths, while an empty cell is a finding; an unknown Component tag is a finding, while an empty component registry disables membership only; knowledge refs resolve only below docs/knowledge and traversal cannot escape the pack root; the foundation phase appears under every filter and blank Phase; and an out-of-phase status is deferred, not failed. Drive Critique and an unknown verification value; Critique is accepted and the unknown value fails. Assert strict findings name their at-fault row and cell and exit nonzero at the declared gate, while interface and component advisories leave the exit code unchanged. Inspect the module boundary: it imports no sibling of the scripts directory; moved engine names resolve and every definition remains here; the loaded registry record is frozen, total, and constructed once; findings-list defaults are per instance and post-pass fields are declared; flags accepts its record or a CLI namespace; no caller imports argparse to construct engine configuration; and the composer spans 50 lines with no nested def.
CUT-REDUNDANT: none
CUT-KEPT: The Drafted-SR, empty-registry, path-traversal, blank-Phase, deferred-status, strict/advisory split, and construction-boundary checks remain because they enforce guards that ordinary invalid-input tests cannot prove.
RISK: The condensed rule list can hide a missing rule family unless every declared checker rule remains data-driven.

=== TC-197 Expected
SUGGEST: LLR-201 / SR-157 outcome: every driven violation names its at-fault row and cell; strict findings fail only at their declared gate, interface and component advisories never change the exit code, Critique is accepted, and an unknown verification value fails. Drafted SR completeness, empty optional registries, declared opt-outs, path containment, phase scope, deferral, registry immutability, independent findings defaults, configuration ownership, and the 50-line non-nested composer retain their stated behavior.
CUT-REDUNDANT: The generic conclusion that it satisfies the parent acceptance.
CUT-KEPT: LLR-201 and SR-157 remain for traceability.
RISK: none

=== TC-182 Method
SUGGEST: Drive scaffolded frames with invalid references and advisory gaps. Assert a crossing or relationship naming an undeclared entity, or an interface tie-back naming an undeclared crossing, names its row and joins --strict; a clean frame is silent. A frame with crossings or relationships but no entity emits its own finding. An empty frame and an absent frame registry emit nothing, and the SR-side check is vacuous. Assert an undeclared Boundary-Refs value is hard and a declared value is clean; one uncovered requirement and one crossing named by no requirement each produce exactly one zero-exit --strict advisory line; and a declared crossing without a realizing interface is reported and never gated. Drive an interface with no endpoint pair, no signal type, a signal outside discrete/variable, and two joined seams with incompatible signal types; each advisory names its at-fault row or rows, the invalid-signal message names the vocabulary, and each exits zero under --strict.
CUT-REDUNDANT: none
CUT-KEPT: The no-entity finding, true-vacuity cases, exact one-line advisory counts, reported-and-never-gated realization gap, and severity split remain because they prevent false green results and accidental gating of advisory data.
RISK: The combined interface case must preserve separate assertions for missing endpoints, missing signals, invalid signals, and incompatible seams.

=== TC-182 Expected
SUGGEST: LLR-187 / SR-162 outcome: unresolved entity and crossing references name their rows and fail --strict; a clean frame is silent; a nonempty entity-less frame is a finding; empty and absent frames are vacuous; undeclared Boundary-Refs fails while declared references pass; uncovered requirements, unreferenced crossings, realization gaps, missing endpoint pairs, missing or invalid signals, and incompatible seams are named advisories that exit zero under --strict, with realization reported and never gated.
CUT-REDUNDANT: The generic conclusion that it satisfies the parent acceptance.
CUT-KEPT: LLR-187 and SR-162 remain for traceability.
RISK: none

=== TC-188 Method
SUGGEST: Drive both root launcher sets in a fresh scaffold and this repository on Windows, macOS, and Linux. Assert environment preparation and loop resume start in one step, except that Linux documents the execute-bit as its single required step, and the adopter-facing guide names the capability and invites reuse. Run 11 live cases with a real interpreter and spoofed sys.version_info. On agent-resume.sh and agent-resume.cmd, a valid project .venv wins over a below-floor ambient Python. With no candidate at or above 3.11, assert nonzero exit, no engine start, and a message naming 3.11 plus every rejected candidate and its reason. A qualifying PATH Python starts the engine on both platforms. A stale below-floor .venv falls back to a qualifying PATH Python for sh and cmd; cmd also walks an alias stub to the py launcher. Assert .command inherits the agent-resume.sh .venv choice and delegates its whole body rather than copying selection policy.
CUT-REDUNDANT: none
CUT-KEPT: The real-interpreter execution, no-engine guard, rejected-candidate diagnostics, below-floor .venv fallback, alias-stub walk, and whole-body delegation remain because they prove launcher behavior rather than probe-text behavior.
RISK: Root presence and launch behavior must be tested independently for both actions and all three platforms.

=== TC-188 Expected
SUGGEST: LLR-193 / SR-160 outcome: both root launcher sets exist for Windows, macOS, and Linux; each starts its action in one step except for the documented Linux execute-bit step; the guide invites reuse; valid project .venv takes precedence; a qualifying PATH Python runs the engine; no qualifying interpreter exits nonzero without starting it and reports 3.11 plus each rejected candidate's reason; stale .venv falls back to PATH; cmd follows an alias stub to py; and .command delegates the shared selection policy.
CUT-REDUNDANT: The generic conclusion that it satisfies the parent acceptance.
CUT-KEPT: LLR-193 and SR-160 remain for traceability.
RISK: none
```
