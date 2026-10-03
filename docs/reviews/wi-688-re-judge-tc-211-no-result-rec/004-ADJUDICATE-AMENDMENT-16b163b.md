# ADJUDICATE (amendment): WI-688, TC-211 `inputs` at 16b163b4

An independent spine adjudicator (Claude Opus) judged this amendment. It made neither the
amendment nor the TC-211 observation. The judgement used the kit brief composed for this
amendment, read in the lane as the owner directed on 2026-10-03 (S11). The anchor is
`docs/archive/last_approved/docs/test/test-cases.toml` (copied 2026-10-03, commit eda73ca3).
One cell moved, TC-211 `inputs`. The new value appends the decomposition record
`docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md` and its SR-161
perspective record `DECOMPOSITION-AMENDMENTS.perspectives.toml`, in the same directory.

- [MEANING] TC-211 inputs -> before: the case's result is keyed to two inputs, the procedure
  document and SR-186. A record's `judged` digest folds those two, a change to either one is what
  the harness may treat as moving the judged state, and a re-judge brief names only those two as
  what the judgement reads. -> after: the result is keyed to four inputs. An edit to the
  decomposition record or to its perspective record now moves the judged state, every future
  record's digest folds all four, and the re-judge brief names all four. -> not the same.
  SR-198 makes the input declaration approved content ("the declarations are approved content
  because they state how the row's claim is kept current") and says "declaring or changing any of
  them re-opens the test case's attestation". The set of changes that can make the result
  stale, and the digest identity of a result, both differ. A record correct under the old cell
  (its digest over two inputs) does not reproduce under the new one. That is a different
  acceptance condition, however small the diff.

Blessed. The new declaration is the correct one. The Method follows
`inspection-procedures.md#decomposition-proportionality-inspection`, and that procedure reads
"the existing scoped decomposition/review record AND its applicable SR-161
applicability/no-finding record". Before this amendment, the cell omitted two inputs the
judgement reads, which is exactly the omission SR-198 requires the harness to report. The
amendment closes it. Nothing else in the row moved (Method, Expected, Rubric, Trigger, Max-Age
and Min-Work-Items are byte-exact), and both paths are repository-relative. Act 27 therefore
re-attests TC-211 in its own commit, leaving Status at Approved.

The standing of the TC-211 pass record (`docs/test/observations/TC-211.2026-10-03T210347Z.toml`,
added in 5a1aa2fb):
- Its `judged` value `sha256:b2b81ce0...cceb` is exactly `inputs_digest` over the OLD two-input
  declaration. Recomputed on the tree at 16b163b4, it is byte-equal, so neither of those two
  inputs has moved. Over the new four-input declaration the digest is `sha256:02995ee8...fab3`.
- `git diff 5a1aa2fb 16b163b4` over `docs/ai-template-redesign-2026-09-05-codex/` is empty, so
  the two added records are byte-identical to the state the judge inspected. The judge's own
  verdict (`docs/reviews/wi-688/001-ADJUDICATE-9e260e1.md`) and decision D-001 both name the
  SR-161 perspective record and the complete chain as read.
- `rejudge.due_cases` at 16b163b4 returns `['TC-036']` at merge and
  `['TC-036', 'TC-209', 'TC-210', 'TC-279']` at release; `checkpoint_drafts` files no TC-211
  draft at either. With `trigger = "release"`, a triggered case is due only when its trigger
  fires after its work-item floor (10), or on expiry (2027-01-01T21:03:47Z). An input-digest
  mismatch never makes it due.

Ruling on the record: it STANDS as TC-211's current result, and no fresh record is owed now.
All four inputs it would be judged against are byte-identical to the state the judge read, and
it read all four. A fresh record now would judge the identical state, and the release-trigger
cadence the row declares already schedules the next one. One limit is stated so that nobody
mistakes it for more: this record's digest attests only the two old inputs. Evidence that the
two added records were in the judged state is the commit history above, not the digest. The
next record written under the new declaration will carry a four-input digest and close that
gap.

VERDICT: MEANING rows=1
