# AP News delivery operations (2026-11-10)

The content assistant runs once at04:00 KST to prepare and review the completed bundle, aiming for07:15 handoff. It does not poll delivery. Content preparation still requires the computer and app; no paid AI API or new CPU production path is enabled.

The verified reservation releases at07:40. Public file verification and duplicate-safe registration finish ahead of the08:00 target. New editions have a07:58 mail eligibility time, with additional existing-queue ticks at07:58 and07:59; the ordinary five-minute queue schedule is retained. Provider acceptance is not inbox delivery. External outages can still miss the target.

Pages identifies the deployment with the exact commit archived into its artifact, not the event commit from hours earlier. Artifact names are specific to each run and attempt. A Pages success is followed by actual public byte verification before registration.

The independent server watch checks07:40–09:59 without AI. A live same-day main publication blocks duplicate dispatches. When no publication is running and the completed bundle is verified, a durable database lease permits at most three fresh regular publication requests per date. It never reruns the stale event, generates content, changes subscribers or dispatches mail directly.

Progress, automatic retry, recovery-success and normal completion notifications are silent. Exhaustion or a missing verified bundle at08:00 produces one `YYYY-MM-DD:terminal-failure` operational message. Persistent unknown state after08:15 uses the same key. The existing database claim and provider idempotency key prevent repeat mail. Unknown/partial health never means zero or success. The admin page retains status.

The unqualified CPU production workflow and its startup crons remain disabled. The old workflow-run retry handler excludes the regular daily workflow; the independent watch owns that recovery budget. Manual repair must first check for running requests and existing complete delivery.
