# Perspective-review dispositions

The [first Opus review](2026-09-06-sn036-decomposition-structured-opus.md)
requested three corrections before landing. They are applied:

- **F1:** SR-186's acceptance remains at its original independent-child and
  stopping-rule obligation. Perspective outcomes belong once, in SR-161;
  TC-211 now cites both parents and inspects the one actual review record.
- **F2:** TC-178 retains its direct SR-161 link as supplementary evidence for
  that parent's existing Hat-Refs mechanism in LLR-183. Its Expected cell now
  names only those mechanics and explicitly points to TC-211 for SR-161's
  perspective-review acceptance. This is a counterpart correction required by
  the method change, beyond the ruling's enumerated rows, not a spine backfill.
  TC-178 remains Approved with a visible Expected amendment awaiting the same
  amendment adjudication as SR-161/LLR-183; no test snapshot is refreshed here.
- **F3:** the original TC-211 incomplete result is labelled historical and
  speaks in the past tense. It still reports precisely the missing input the
  earlier inspector encountered and is not converted into a passing result.
- **F4/F5:** stale pre-ruling record comments and the rubric's missing direct
  SN-036 anchor are queued as [WI-607](../work/queued/WI-607-refresh-sn-036-record-comments.md), separate follow-up scope. The current review explicitly
  applies SN-036 intent as well as the existing numbered rubric; neither an
  extra coverage sensor nor new metadata is warranted.
- **F6 (reopened before retry):** the original disposition retained the
  ruling citation by attributing “Rationale names this ruling” to the owner.
  The owner challenged that attribution; no direct owner message has been
  verified. The phrase is from an agent-authored ruling record and does not
  establish an owner override. The citation finding returns to ordinary
  review under the standing prose convention and authorized amendment scope.

The first review's incomplete and inconsistent abbreviation of the rubric hash
is not an authoritative content identity. The source manifest in its supplied
prompt and the launcher-bound prompt digest identify what it received. The
closure reviewer must quote the actual rubric SHA256 exactly, with no invented
suffix, and make its own judgment of the revised source.

The [closure review](2026-09-06-sn036-closure-structured-opus.md) approves the
corrected decomposition. Its A1 historical-text advisory is resolved in the
execution record alongside the new actual Inspection result. A2 (an additional
negative brief-question sample) is a non-blocking future procedure improvement;
the current procedure already checks every question. A3 records the still-open
artifact authority correctly except that the SN-036 needs-only snapshot was
already performed by the coordinator under the owner's earlier ruling.

Both reviewer bodies abbreviate the rubric digest incorrectly. The authoritative
rubric SHA256 supplied in both prompt manifests is `81a0de90c98ad2dac0b9774fd94c611181fc49bfde083cc22c52d1fb1ac31f8a`.
Their launcher-bound prompt digests and raw invocation logs preserve the source
binding; this coordinator correction changes neither original verdict nor body.
The record does not claim either reviewer output satisfies an additional
provenance inspection that was not executed.

The [independent TC-211 Inspection](2026-09-06-sn036-inspection-structured-opus.md)
reports **TC-211 PASS** but requests record corrections before final acceptance.
Its F1 is resolved by the authoritative manifest correction above, preserving the
original reviewer body. F4/F6 are resolved by rewriting the preflight as one
current observation with explicit provider calls and one ready count. F5 is
resolved by the amendment spec's full SR/LLR/TC absorption ledger, preserving
all newly present Drafted rows and requiring an actual judgment for every older
cell before a copy; RETURN with a scoped successor is explicit when that
judgment is unavailable. F7 is clarified in WI-607: only explanatory comments
may follow the already-recorded ruling; roster values remain owner-governed.
F2's additional negative brief sample is included in that documentation
follow-up, with its future execution kept separate. F3's historical roster
count is corrected here rather than rewriting an earlier ruling: the current
roster has ten `always` hats, not nine; no acceptance threshold relies on that
old illustrative figure.
<!-- fig: cmd=".venv/bin/python -c 'import tomllib,pathlib; print(sum(h["applies_when"] == "always" for h in tomllib.loads(pathlib.Path("docs/requirements/hats.toml").read_text())["hat"].values()))'" rev=a6b54584+oi86-sn036-final -->

The [final bounded record review](2026-09-06-sn036-records-final-structured-opus.md)
returns **APPROVE**, confirming F1, F4/F6 and F5 closed against the supplied
source and full parsed snapshot deltas. Its remaining tense/heading nits are
corrected in the Inspection procedure; no result or method changes. Its
observation about SR-183 is retained: that older Drafted row is not part of this
first-approval batch and remains unapproved. The roster comment/value boundary
is explicit in WI-607; no roster value change is authorized by that follow-up.
