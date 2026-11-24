# Website Copy Implementation Plan
> **For agentic workers:** Use executing-plans to implement the approved copy in this isolated checkout.
**Goal:** Explain AP services clearly and distinguish live and planned offerings.
**Architecture:** Update Korean source JSON and apply a repeatable Korean-only editorial pass after the existing page generators. Preserve DOM structure, URLs, other locales and news articles.
**Tech Stack:** Python, JSON, static HTML, existing Pages workflow.
## Global Constraints
- sources/ is read-only.
- No unsupported operating, medical, privacy or first-in-market claims.
- No unrelated layout or application changes.
### Task 1: Copy revision
- [x] Update site-source/divisions.json Korean hub copy and service statuses.
- [x] Store approved replacements and apply them to Korean company/service HTML and source text.
- [x] Replace animated slogan with a static service description; preserve existing visual.
### Task 2: Validation and publication
- [x] Run python3 scripts/check_site.py and inspect changed source/HTML.
- [x] Check desktop/mobile layout and link destinations.
- [ ] Commit, synchronize latest main without overwriting others, push and verify Pages workflow for the published SHA.
