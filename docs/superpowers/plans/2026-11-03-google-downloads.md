# Implementation
1. Add failing tests for same-window platform counts, missing values, real zero, mismatched windows, duplicate package rows and malformed snapshots.
2. Add focused app-downloads module consuming existing Apple metrics and owner-only Google runtime snapshot. Include verified Google release state, source dates and official links. Render in existing finance section and cache-bust module.
3. Store directly observed Google snapshot in runtime; missing numbers remain null. Do not touch Apple daily metrics or existing finance rows.
4. Run existing finance and new regression tests, syntax/diff checks; push only requested files to current main and verify authenticated live admin.
