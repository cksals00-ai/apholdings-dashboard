# News environment incident recovery

Incident: 2026-11-03 KST 03:05 independent kickoff succeeded, but three attempts failed before generation: Playwright1.51 does not support ubuntu26.04. Floating ubuntu-latest drifted; successful full rehearsal41031927070 actually used ubuntu24.04.

Approved objective: repair environment, resume only today's edition, verify actual public bytes and all eligible mail provider acceptance, no paid AI, report failures before recovery.

Implementation: pin only worker runs-on to ubuntu-24.04. Keep immutable producer E31 and all source/art/document/mail gates. Retain successful recovered full rehearsal. Before migration qualification, require new successful main compatibility run with identical pinned worker and exact reviewed probe definition (SHA256): same CPU wheel pins, exact production dependencies, actual Chromium launch, existing news tests. Reject any worker difference beyond that one OS pin; reject altered probe, failed/unknown runs, wrong branch/path/event. Original full qualification unchanged.

Verification: local qualification tests; independent code review; actual environment run41543046848; then immutable scoped verifier and actual production. Preserve source/image checkpoints across retry. Never infer publication/mail from production status. Read actual publication public_verified_at and health eligible_missing/all blockers zero.
