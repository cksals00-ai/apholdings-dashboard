# AP News Editorial Implementation Plan

> **For agentic workers:** Use executing-plans to implement this plan task-by-task.

**Goal:** Publish the approved image-led AP News design for the current edition and future editions.
**Architecture:** Keep JSON as the canonical content. Add optional local image metadata and summaries to the existing builder; old editions remain compatible. Render consistent web, PDF and email content.
**Tech Stack:** Python, ReportLab, HTML/CSS, original generated editorial images.

## Global Constraints
- Keep AP logo, Korean OFL font, verified facts, announcement dates and source links.
- Preserve concurrent homepage changes and subscription queue semantics.
- Label generated illustrations; never present them as source photographs.

### Task 1: Canonical editorial metadata
Files: scripts/test_newsletter.py, scripts/newsletter.py, site-source/newsletter/issues/2026-10-11.json, img/newsletter/.
- [x] Add tests requiring image paths to stay within img/newsletter and summaries/images/actions to appear in web and email.
- [x] Run unittest and verify new tests fail.
- [x] Validate optional image path/alt/caption and optional summary; retain compatibility with old issues.
- [x] Create five original editorial illustrations and enrich current issue with summaries and AP service implications without changing source facts.

### Task 2: Magazine rendering
Files: scripts/newsletter.py, assets/v2/newsletter.css.
- [x] Use canonical images in hero and story figures, captions, summary digest, archive and email.
- [x] Give illustrated PDF a cover and one story per page with original links and complete text.
- [x] Run unit tests, build_all and local responsive checks; render every PDF page and inspect.

### Task 3: Publication
Files: newsletter README and operation record.
- [x] Reviewer checks feature and content before main publication.
- [ ] Fetch latest main and preserve other changes, push authorized existing site, verify Pages success.
- [ ] Verify public images/web/PDF bytes; then update existing issue database without sending duplicate mail.
