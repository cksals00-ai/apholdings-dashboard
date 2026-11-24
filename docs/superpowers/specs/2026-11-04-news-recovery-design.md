# AP News recovery design

Approved by user in chat on 2026-11-04: source-bound sentence review, verdict consistency, failed-field correction, publication-independent isolated rehearsal; activate only after real whole-server proof.

## Evidence
Restored private run 41618734726 attempt1 checkpoint. Only1 accepted story after17 recorded failures. Current review also rejects proposals because absent from source, and emits findings whose rationale says the assertion is supported. Archived75 model outputs spent340.9 input-processing minutes and95.5 decoding minutes (across preserved history). One review ended stop_type=limit at1500tokens; runtime checks only stopped_limit and mislabels this as JSON parse error.

## Boundaries
No paid AI APIs, credential reads, fabricated receipts, date override, ordinary resend, source/date/duplicate/QA relaxation. Old fixture date is provenance only, never today's publication date. Production remains blocked until matching immutable runtime/worker/rehearsal and actual automatic recovery whole-server success.

## Design
1. Recognize token-limit responses before JSON parsing; retain raw response and reason.
2. Bind a bounded review to each individual copy field. Independent source-backed factual classification distinguishes advice from factual premises. All findings need exact draft span and an explicit source mismatch; ambiguous/contradictory verdict fails review, never becomes acceptance. Preserve full source context and raw receipts; version new receipt hashes.
3. Repair only rejected fields with original source and exact findings; rerun independent verification. Keep accepted stories/images and novelty receipts when identities match. Avoid cycling8B drafts through repeated14B rejection; use14B for targeted correction with a fresh independent verification request.
4. New isolated test run uses immutable historical controls as labelled regression fixtures and fresh current-day eligible sources for output. It neither requires a published issue today nor changes a prior trial date. Inject actual copy and image failures and require bot retry, byte checks, and owner-only mail receipts.
5. Update qualification to the exact new test and immutable runtime after reviewed changes; never allow pending/failed/cancelled proof.

## Acceptance
Normal MoEngage/AgentCore proposals pass; obtained AP outcome and both false efficacy premises are specifically rejected. Five independently accepted stories; actual CLIP failure and repaired hero with five preserved PNG hashes; all PDF/web/email/GIF QA; isolated public10files byte-equal; owner-only mail failure/retry accepted and both alarms; rollout qualified=true.
