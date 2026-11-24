# Finance evidence connection
Approved scope extends 2026-10-26 app-finance design: official account-level settlement/payment evidence, no bank permissions.
1. Add failing tests: unknown metrics remain null; real zero preserved; partial day coverage labeled; financial snapshot distinguishes expected payout from bank receipt and app revenue.
2. Reuse owner-read-only sync runtime table with asc_finance JSON evidence. Store directly observed September official amounts and source timestamps, never public files containing private financial records. Clearly label manual official verification, not automated bank/API connection.
3. Extend app-finance.mjs snapshot rendering and reusable metric summary. Fix legacy app metric cards/charts/tooltip empty periods; no zero-fill of missing evidence.
4. Run tests/syntax/security review; publish only modified tracked files to latest main. Verify authenticated live admin.
5. One-off followup after 2026-10-29 15:00 KST checks Apple payout vs actual bank evidence independently; notify and delete automation.
