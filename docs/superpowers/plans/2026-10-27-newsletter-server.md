# AP News server publishing plan

Goal: Generate, verify and publish the daily AP News on hosted GitHub Actions; retain the existing Supabase confirmed-subscriber mail queue. Local computers are not required.

Design: Hosted runs start before 08:00 KST and recover at 30-minute intervals, with extra checks after 08:00. One concurrency group prevents overlapping writers. Daily artifacts checkpoint research and images between retries. Existing newsletter.py remains the only web/PDF/email builder. Public byte/content validation gates idempotent Supabase registration. GitHub Pages is deployed explicitly because GITHUB_TOKEN pushes do not trigger another Pages build. No other site generator runs.

Prerequisite: OPENAI_API_KEY in repository Actions secrets. Existing SUPABASE_SERVICE_KEY is reused only in the registration stage. No secrets enter source files, artifacts or logs. Model calls are billed to the API project.

Tasks:
1. Tests first: retry classification; official-source/date validation; reject unsupported verification; published-issue skip; public mismatch blocks DB; no update/resend of existing issue; checkpoint reuse.
2. Add Python server runner and pinned dependencies: research with live official web search, source fetch and publication-date verification, separate claim check, original AI illustrations, existing builder, PDF/mobile rendering with visual review, checkpoint/state recovery.
3. Add hosted workflow with restricted permissions, restore/upload daily checkpoint artifacts, safe rebase/push retries, Pages artifact deployment, verified public registration, and mail-result check. Preserve all unrelated site changes.
4. Add operating README and run offline tests, existing newsletter tests, browser/PDF checks, workflow validation. Upload and run today's existing edition through the no-generation/no-resend path.
5. Enable hosted schedule only after verifying credentials and the hosted run. Pause local heartbeat only after the hosted path succeeds; if missing credentials, clearly preserve and report incomplete migration.

Success: Hosted workflow succeeds while using no local runtime, public web/PDF matches the source, DB registration is idempotent, sent recipients are not re-enqueued. A missing API key must fail clearly before claiming production readiness.
