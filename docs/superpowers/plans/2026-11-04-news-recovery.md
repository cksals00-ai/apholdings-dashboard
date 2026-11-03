# AP News Recovery Implementation Plan

Goal: eliminate observed correction-loop defects and obtain real server qualification without paid APIs.
Architecture: bounded independent field review plus source-bound targeted repair; isolated current-day fresh-output rehearsal and immutable historical regression controls.
Tech Stack: Python unittest, public CPU llama.cpp models, GitHub Actions.

Global constraints: no paid AI API; no ordinary resend; no date/quality/source/dedup bypass; real server evidence required.

- [ ] Runtime: reproduce stop_type=limit via local HTTP response, recognize limit with raw receipt retained; run unittest.
- [ ] Review: add cases for field-bound supported/advice/unsupported/contradictory decisions, implement bounded field receipts; preserve input/source/model/revision hashes; run regression controls.
- [ ] Repair: reproduce failed-field replacement while retaining successful fields/assets; implement bounded14B correction then separate verification.
- [ ] Rehearsal: tests prove fresh current-day seed without published issue and old-date guard remains; add labelled immutable controls, genuine copy/image faults and automatic retry proof.
- [ ] Validate newsletter suite/workflow lint; review diff; deploy immutable pin; dispatch one exact full test.
- [ ] Monitor raw checkpoints/alerts; report failures immediately; inspect all outputs and qualification; restore existing automation schedule after actual activation.
