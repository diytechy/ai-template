# BEFORE — subtree of SR-199 (verbatim from the registries at HEAD)

## SN excerpt (SN-043, SN-008, SN-024)
### SN-043 — 
need: **Scope: template (adopters + this repo).** A reviewer can see, for each stakeholder outcome, what its delivery relies on beyond the system's own checked behavior, and whether any of those premises has been shown false.
acceptance: Each premise that a requirement relies on beyond the system's own behavior is recorded once, with where its outcome lands, the conditions it holds under, what would break it and the observation that would show it false, and each requirement either names the premises it relies on or states why its own behavior alone delivers its needs. Each premise shows its approval status and whether it has been shown false; a premise shown false is reported with every requirement that relied on it.

### SN-008 — 
need: A reader can believe a **pass verdict**: gates are **honest**, and a pass verdict never hides a skipped check, a stub, or an unmet declared criterion.
acceptance: The harness **fails** (not skips) on a missing required tool — the explicitly-requested `--lenient` local mode is the one sanctioned degrade to SKIP (SR-006), never a CI/gate default; the no-stub detector and the privacy/secrets floor run at their declared gate.

### SN-024 — 
need: A reviewer can trust subjective/perceptual acceptance — a realistic-looking render, an artifact comparison with no crisp measurable interface — because it is adjudicated by an **independent critical eye against a written rubric**, never by the session that authored the artifact.
acceptance: A `Verification=Critique` requirement is judged by a fresh critique session against a written rubric derived from the SN/SR intent (not the possibly-lax TC); family heterogeneity is required on the unattended path, while the human chooses the reviewer for attended acceptance. The verdict cites numbered rubric anchor ids, bounded iteration drives rework, and the loop escalates to the human on budget exhaustion.

## SR-199 — Observation results are recorded apart from their test case
sn_refs = ['SN-043', 'SN-008', 'SN-024']
boundary_refs = ['B-05']
hat_refs = ['TEST-ENGINEER']
requirement = 'The delivered process shall record each observation result apart from its test case, with its outcome, when it was observed, who or what observed it, when it expires and a digest of the inputs it judged.'
rationale = "Keeping a result on the approved test case would mix what the test is with what it last found, and would force the row's re-attestation after every sample. A result carries what it judged — the digest of the rows and artifacts its test case declares it reads — so a later change to those inputs makes it stale without a clock, and it carries an expiry so it cannot stand forever. One record serves assumption observations and the verdicts of inspection, critique and attestation tests alike, so all of them share one freshness rule. Automated tests need no such record: their results join the harness's tree-bound evidence record."
acceptance_criteria = "An observation record names its observation test case and carries an outcome of pass or fail, an observation time, the person or process that observed, an expiry no later than the test case's declared lifetime after the observation, and the digest of the test case's declared inputs as judged, which is empty where the test case declares no inputs; a record missing any of these, naming a test case that is not an observation test case, or expiring later than the lifetime allows, is refused when written and fails the check when found; writing a record never edits the test case; a partly written record is never read as a result."
priority = 'M'
verification = 'Test'
status = 'Approved'
phase = 6
coincident = 'The needs ask for each premise showing whether it has been shown false; the observation result recorded apart, with its outcome, observer, expiry and judged digest, is the record a failing observation is read from.'

## LLRs (3)
### LLR-234 — The observation record: format, strict reader and atomic write  [sr_refs=['SR-199'], module=project-trajectory/scripts/kitlib/observation.py, code_symbol=OBSERVATIONS_DIR/FIELDS/OUTCOMES/parse/read_records/latest/write_atomic/parse_utc, component=CMP-006, test_refs=None]
detail (1047 chars): A kitlib module that imports no sibling script, in the pattern of kitlib/evidence.py. One TOML file per record under docs/test/observations/, named <TC id>.<observed-at in UTC, colon-free>.toml, so records written on different lanes never collide. FIELDS = (tc, outcome, observed_at, provenance, expires, judged); OUTCOMES = (pass, fail); `judged` is the inputs digest and is the empty string for a test case declaring no inputs. parse_utc accepts only the canonical form YYYY-MM-DDTHH:MM:SSZ. parse(text) returns None unless every field is present, observed_at and expires parse through parse_utc, expires is not earlier than observed_at, provenance is non-empty after trimming, and outcome is in OUTCOMES, so a truncated or hand-mangled file is never a result. read_records(root) skips any name with a leading dot, which is the temporary name write_atomic writes before os.replace; write_atomic retries a Windows PermissionError on the replace a bounded number of times, then raises. latest(records, tc) returns the newest record by observed_at.
rationale (248 chars): The record's atomicity and the Windows replace behaviour are this row's own: a crash mid-write must leave no readable half-record, and a replace can be refused while another process holds the target on Windows, which the requirement states nowhere.

### LLR-235 — The observation writer  [sr_refs=['SR-199'], module=project-trajectory/scripts/record_observation.py, code_symbol=build_observation/record_refusal/inputs_digest/main, component=CMP-006, test_refs=None]
detail (876 chars): record_observation.py --tc TC-### --outcome pass|fail --by <provenance> [--expires <UTC>] resolves the test case from the registry, refuses an undeclared test case or one that is not an observation test case, an outcome outside OUTCOMES, a missing provenance, and an expiry later than observed_at plus the case's max_age; with no --expires it writes observed_at plus max_age. inputs_digest(root, inputs) folds each declared input in declared order as name, NUL, SHA-256 of its LF-normalized bytes, the fold kitlib/stage uses; a registry row id is digested as that row's cells as the carrier reads them. The writer calls write_atomic and never opens the test-case registry for writing. bootstrap.MAPPING ships the script and the kitlib module; the directory is not a declared stage input, so recording a sample never makes the stage's fingerprint or the release evidence stale.

### LLR-236 — Records found on disk are checked  [sr_refs=['SR-199'], module=project-trajectory/scripts/assumption_rules.py;project-trajectory/scripts/trace.py, code_symbol=observation_record_findings, component=CMP-006, test_refs=None]
detail (506 chars): trace.main reads the records once after analyze, which stays free of file reads, and observation_record_findings(records, raw_files, tcs) fails --strict naming the file for a file that does not parse by kitlib.observation.parse, including a non-canonical observed_at or expires, an expiry before the observation and an empty provenance; for a record naming an undeclared or automated test case; and for an expiry later than observed_at plus the case's max_age. A file with a leading-dot name is never read.

## TCs (3)
### TC-229  [verifies=['SR-199', 'LLR-234', 'IF-214'], level=Unit, tier=Smoke, automated=Yes, status=Approved]
method: The record module exercised in a temporary directory. A record with every field round-trips; a record missing any one field, or cut off mid-file, parses to nothing; an outcome outside pass and fail, an observed_at or expires not in the canonical UTC form, an expiry earlier than the observation, and an empty or whitespace provenance each parse to nothing; a leading-dot file is never read; latest returns the newest by observation time; an empty judged digest is valid. write_atomic is driven with the replace step failing twice with a permission error and then succeeding, and with it failing every time, which raises after the bounded retries and leaves no partial record readable.
expected: Satisfies SR-199's acceptance clauses on the record's fields, the empty digest for a case declaring no inputs, and a partly written record never read as a result.
evidence: tests/test_observation_record.py

### TC-230  [verifies=['SR-199', 'LLR-235', 'IF-215'], level=Integration, tier=Full, automated=Yes, status=Approved]
method: The writer run as a command on a scaffold, in a module registered as slow. It refuses an undeclared case, an automated case, an outcome outside the pair, a missing provenance, and an expiry later than the observation time plus the case's max_age, writing nothing each time. With no expiry given it writes the observation time plus max_age. The test-case registry's bytes are unchanged after every run. The inputs digest is equal for a declared input stored with LF and with CRLF line endings, and changes when its content changes; a registry row id among the inputs is digested from that row's cells. Recording a sample leaves the stage fingerprint and the release evidence binding unchanged. A fresh scaffold receives the writer and the record module.
expected: Satisfies SR-199's acceptance: a malformed or out-of-policy record refused when written; writing never edits the test case.
evidence: tests/test_observation_writer.py

### TC-231  [verifies=['SR-199', 'LLR-236'], level=Integration, tier=Full, automated=Yes, status=Approved]
method: Driven through the traceability check on a scaffold with records on disk, in a module registered as slow. An unparseable record file, one whose observed_at is not canonical UTC, one whose expiry precedes its observation, one with an empty provenance, a record naming an undeclared case, one naming an automated case, and one expiring later than its case allows, each fail the strict run naming the file. A leading-dot file is ignored. A well-formed record produces nothing.
expected: Satisfies SR-199's acceptance clause that a malformed or out-of-policy record found on disk fails the check.
evidence: tests/test_observation_writer.py

## METRICS (before)
rows=7 (1 SR + 3 LLR + 3 TC)
chars=5794 (SR requirement+AC, LLR title+detail, TC method+expected+evidence)
identifiers (broad IDENT)=48; first-pass regex matches=43; spine-id tokens=3