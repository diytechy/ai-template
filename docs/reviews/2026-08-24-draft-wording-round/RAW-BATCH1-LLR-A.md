# Raw return - batch 1 (LLR-187, LLR-199, LLR-202, LLR-193, LLR-198)

Unedited final message from `OPENAI-TERRA` (`gpt-5.6-terra`, `codex exec`),
captured with `--output-last-message`. Adjudicated in `RESUME.md`.

```
=== LLR-187 Title
SUGGEST: Frame-reference resolver and interface-cell checker
CUT-REDUNDANT: The repeated SR-to-crossing rule and severity split; SR-162 already states both.
CUT-KEPT: The title names both implemented mechanisms so neither the frame resolver nor interface cells disappear from scope.
RISK: The title no longer signals the severity split; Detail retains it.

=== LLR-187 Detail
SUGGEST: In the trace pipe, frame_findings resolves a crossing's Entity and a relationship's From and To against declared entity ids. It returns finding strings, not the older spine rules' (at_fault_id, finding) pairs, because no caller uses the id. These are FAILURE findings. An empty entity set is vacuous only when nothing references it; otherwise a reference to a missing entity would falsely report full resolution. sr_boundary_findings joins the SR side and returns (findings, advisories): an SR Boundary-Refs value naming an undeclared crossing is HARD and joins --strict, while the uncovered-requirement count, crossings named by no requirement, and the realization gap--a declared crossing with no InterfaceFromExternal/InterfaceToExternal interface row--are one advisory each and never gate. Both rules are vacuous with no declared frame, and _frame_report_section renders their state or findings. At the IF entries in this module's required-field and closed-vocabulary tables, endpoint pairs and the closed discrete/variable signal vocabulary are declared as this row's observables; the generic checker executes them but remains owned by the schema row. Not discharged: incompatible signal types on joined seams cannot be reported naming both rows because no join reads signal vocabulary; the carriage cell is the tier's only seam-to-seam edge and carries none. The cross-side requirement/interface amendment rule is also unimplemented.
CUT-REDUNDANT: The analogy between a dangling entity reference and a deleted requirement; SR-162 already requires an unresolvable crossing to fail.
CUT-KEPT: The empty-entity and no-frame vacuities, HARD/advisory split, never-gated advisories, interface-cell ownership boundary, missing seam join, and cross-side residual all prevent false compliance claims.
RISK: The shorter return-shape explanation may make the string-only frame_findings interface less visible.

=== LLR-199 Title
SUGGEST: Component-view generator and coverage placement
CUT-REDUNDANT: none.
CUT-KEPT: Coverage behavior and the no-approval rule remain in Detail because they are behavior, not a title.
RISK: The title does not enumerate the three coverage edges; Detail does.

=== LLR-199 Detail
SUGGEST: gen_components.py derives the component view from four registries: components.toml declares components, low-level-requirements.toml provides Component membership, system-requirements.toml is reached through that membership, and interfaces.toml provides seams. It writes docs/requirements/components.derived.toml; docs/stack.ini [generated] declares kind components, check.py freshness-gates component-view, trunk_step --regen regenerates it on trunk, and the file carries the generated-but-live staleness header. For each component it emits member design rows, their decomposed requirements, perspectives from trace.effective_hats over members, modules, and seams split into internal and boundary by the components layer rule. A requirement with no component appears once in the counted unplaced table; registries cannot distinguish missing decomposition from an all-component constraint. A requirement in several components appears in each and in each component's sr_shared_refs. A seam is placed from its Component tag unioned with components resolved from endpoints through trace_text.norm_module; an unresolved seam stays in the unplaced table. No approval cell appears: the hand file declares the component and its maturity, while this file describes it. With no real CMP row and no view on disk, the generator exits 0 and writes nothing. Not discharged: the view has no INTERNALS, so mechanism remains in named design rows; freshness compares the artifact with regeneration, not source correctness, which remains the amend-without-flip guard's residue.
CUT-REDUNDANT: The general offline, deterministic, and drift-checkable view contract; SR-070 states it.
CUT-KEPT: Registry-only derivation, all coverage edges, no-approval behavior, optional-layer vacuity, and the two residual limits remain because they define observable behavior and scope.
RISK: The compressed coverage rationale may make the lack of repository-specific placement judgment less apparent.

=== LLR-202 Title
SUGGEST: Staged Hat-Refs amendment guard
CUT-REDUNDANT: none.
CUT-KEPT: Hat-Refs and staged status remain named because they distinguish this guard from general perspective resolution.
RISK: The title no longer states the one-time warning limitation; Detail does.

=== LLR-202 Detail
SUGGEST: LLR-183 resolves the perspective record and derives its effective set; staged_hat_refs_findings(root) checks whether that record stayed current. As a Hat-Refs arm of the amend-without-flip guard, it reuses the amendment set from staged_spine_amendments and reports a row whose approved half is non-empty while Hat-Refs is absent from its traced half. The comparison is by cell class: line-based comparison cannot distinguish an approved-cell amendment from an informative-cell edit that re-dates the row, so this arm uses the split_changed_cells' A5.1 split and stays silent for traced-only perspective backfill. Scope is structural: traced_cells, extracted from spine_cell_class, detects whether a registry declares the column. The test-case tier is silent because it has no such cell; a third registry gaining one is guarded without an edit here. Its baseline is HEAD versus the index, with the same approved-text Status on both sides. A row created in the same commit and a row below approval are therefore vacuous. The warning appears only under --staged and never sets an exit code. Not discharged: it fires once when the amendment is staged; a last_approved snapshot would keep the finding until answered. That snapshot is not used because this arm warns at amendment time; promotion to a drift-tier finding remains a later option if warnings prove ignored.
CUT-REDUNDANT: The general requirement that applicable perspectives be recorded; SR-161 states it.
CUT-KEPT: The approved-half condition, traced-only silence, structural tier scope, both vacuities, warn-only severity, and last_approved limitation remain because each changes when a finding appears.
RISK: The shorter timing rationale may obscure why last_approved is intentionally not the baseline.

=== LLR-193 Title
SUGGEST: Loop-resume launcher interpreter selector
CUT-REDUNDANT: The general root-launcher outcome; SR-160 states the contributor-facing obligation.
CUT-KEPT: Loop-resume remains explicit so the title does not imply that environment preparation is delivered.
RISK: The title omits the undispatched environment-preparation half; Detail retains the gap.

=== LLR-193 Detail
SUGGEST: pick_py distinguishes found from usable: it first runs each candidate, then checks that sys.version_info meets the 3.11 floor required by every kit script's tomllib import. This rejects a Windows python3 PATH Microsoft-Store alias that exists but does not run. It tries both .venv layouts, bin/ for POSIX and Scripts/ for a Windows-created venv, before python3 and python on PATH, so the pinned toolchain wins. On refusal it names every rejected candidate and its PYWHY reason rather than reporting only "not found." agent-resume.cmd's :pickpy label performs the same two probes in cmd.exe, trying .venv\Scripts\python.exe, .venv\bin\python, python, then py. agent-resume.command has no separate probe; it executes exec ./agent-resume.sh and inherits its policy. Together the root loop-resume launchers provide SN-034's loop-resume action on Windows, macOS, and Linux. Not discharged: SN-034 has two universal actions, but only loop resume has root launchers. onboard.sh and dev-setup.sh remain under scripts/, not the root required for environment preparation; bootstrap.py's MAPPING and README.md's Still owed ledger expose the gap as a finding, not a claimed launcher.
CUT-REDUNDANT: The general requirement to report a missing interpreter clearly; SR-160 states it.
CUT-KEPT: The run-then-version probe, candidate order, PYWHY output, delegated macOS policy, all platform paths, and the missing preparation launchers remain because they are implementation behavior or a delivery gap.
RISK: Condensing the platform explanation may make the reason for the two .venv layouts less prominent.

=== LLR-198 Title
SUGGEST: Pending-owner-action read model and compatibility shim
CUT-REDUNDANT: none.
CUT-KEPT: Both the shared read model and shim remain named because the row delivers both.
RISK: The title does not list the three consumers; Detail does.

=== LLR-198 Detail
SUGGEST: This pending-owner-action model renders no page and makes no lane decisions. Its three committed-tree-pure, clock-free sources are blocked_pending, which names queued work carrying a blockref and its attestation page; spine_pending, which names each Drafted SR needing first approval and each SR whose text differs from docs/archive/last_approved needing re-attestation, with one pointer line to its on-demand brief; and pause_pending, which reads docs/work/pause and fails closed when unreadable. pending_items joins them into typed PendingItem values with kind and rendered bullet. pending_block is the rendered model and byte-compared pending region of the generated owner surface; owner_cards is the model without the pause, used by the drained-queue banner. The dashboard status snapshot, generated owner surface, and dispatcher exit banner read this model. Because only the dashboard is in the render family, placing it there forced the other consumers through gen_trajectory or into private names. traj_status.py re-exports blocked_pending, spine_pending, pause_pending, and pending_items under their former names, leaving callers unmoved and generated surfaces byte-identical. The Module cell names this split sibling because the shim is part of the delivered layer.
CUT-REDUNDANT: The state view's requirement to expose progress, work, and holds; SR-168 states it.
CUT-KEPT: All three source rules, unreadable-pause failure, typed joining, pending_block and owner_cards semantics, consumer siting, compatibility exports, and byte identity remain because they define the model's consumers and outputs.
RISK: The shortened siting explanation may make the former gen_trajectory dependency less obvious.
```
