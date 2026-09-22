# AP Holdings Website v2.0 / IR v2.0

This is the corporate, portfolio and public IR site. Existing GitHub Pages hosting, `CNAME`, app-policy URLs, product-media paths and App Store/social/connector destinations are preserved. Product, commerce and private administration remain separate surfaces.

## Build and validate

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check assets/v2/site.js
bash -n deploy_dashboard.sh
```

No application framework, npm installation, runtime API or build service is required. Commit the generated static files along with their source. The existing Pages deployment serves them from the repository root.

## Content and localization

- `content.json`: version, origin, contact and locale publication status.
- `locales/ko.json`: Korean source copy.
- `locales/en.json`: English brand reference aligned with the September 22 brief.
- The builder generates KO/EN home, IR, about, lab and 11 product pages per language.
- VI, JA, ZH-CN and FR currently show a localized preparation notice with KO/EN links. They are **not completed translations** and are excluded from the sitemap/hreflang with `noindex`.
- Complete translations, including professional boundaries, require human/professional QA before changing publication status. Future ZH-TW, ZH-HK and TH are configuration targets, not active routes.
- Source/version/reviewer/approval metadata must be updated when translations are approved. No AI review is recorded as human approval.
- Product names stay unchanged across locales; Korean pronunciation is supplemental to RGRG.

Canonical inputs: latest user Website v2.0 / IR v2.0 brief; Notion Website Canonical Guide; Living Master Plan; IR Standard; Global-by-Design Technical Standard; Market Pack Framework; Localization Standard. The latest user brief takes precedence where older document wording differs.

## Public boundaries

- AP Revenue is an independently developed Decision Intelligence Working Proof / Productization Candidate. It is not the company origin.
- Public IR is a webpage. Investor deck/memo/verified metrics are request-only; NDA/data-room materials are not included.
- No employer/customer dataset, real dashboard, numerical demo, internal algorithm, schema, invention detail or credential is added.
- The IR visual is a conceptual Priority → Human Action → Outcome workflow, not a data dashboard.
- Existing public business-plan PDFs and the operational board state are retired from current serving. Prior Git history remains unchanged; removal from the current tree is not historical erasure.
- Policy documents retain their contents and existing URLs. The RGRG policy display name is updated, with an additional `/rgrg/privacy.html` address.
- Existing public project images remain unchanged. RGRG character assets are shown; old screenshots with the previous branding remain historical files and are not embedded.

## Asset and feature preservation

- App Store destinations retained for Safelist, Hangeul Cubs, IRON GRADE, Dawn Grace, The Other Hours, K-Concert Trip and the first-investment learning app.
- Existing Safelist/Lightlist connector URLs and copy controls retained.
- AP mark, Hangeul Cubs product screens, RGRG character art, LAST WAVE art/characters/worlds, LIA image/videos and commerce product visuals retained.
- Old corporate/product URLs are compatibility redirects to the new portfolio. No functioning checkout or contact backend existed; contact and investor CTAs open the established email address.
- The old LAST WAVE page referenced several missing files, including an opening video. Those broken embeds are not carried forward. Existing valid art is reused.

## Deployment source protection

The Mac sync script now pulls first, stops on divergence and refuses a public source folder that lacks the v2 marker or has an older content version. It keeps the existing public/private repository separation.

**Required local follow-up:** update the actual Mac `site/` source folder and the script invoked by the scheduler to the new version. Editing the script in GitHub does not automatically replace an already installed scheduler copy. Until reconciled, pause the old scheduled corporate-site sync to prevent a pre-v2 script from restoring stale files.

## Remaining release gates

- VI / JA / ZH-CN / FR full localization and human/professional QA.
- Historical repository-content review if retired operational or planning material requires removal beyond current serving.
- Verify the seven linked App Store products' current availability across intended markets before applying a live/available-in-market claim. Current site identifies historical build evidence without declaring global availability.
- Sanitized downloadable one-pager after separate content approval; full deck remains request-only.
- External pilots, active users, transactions, revenue, repeat and outcome metrics require evidence before publication.
- Custom product/commerce/admin subdomains are architecture targets; this change does not create or move those applications.

## September 22 visual refinement

- KO uses the Noto Sans KR webfont (400/500/600/700) and concise noun/keyword copy; original English content source remains unchanged.
- Generated brand visual and six-second silent film: Higgsfield; source/model/job IDs and durable optimized-media URLs are in `brand-media.json`. These are abstract brand concepts, not real AP product evidence or data dashboards.
- Optimized poster: 16,716 bytes WebP. Film: 229,041 bytes H.264 MP4, 720p, no audio, fast-start.
- Poster is available without JavaScript. Desktop film starts only near the viewport; mobile, data-saver and reduced-motion users see the poster with optional playback. Pause control, offscreen pause and background-tab pause are included.
- Scroll reveal is progressive enhancement and disabled for reduced motion. Corporate pages retain static content, SEO and navigation.
- `/site-source/responsive-review.html` is an unlinked, non-indexed QA view with real CSS-width frames. It contains only already public pages.

## Show-first homepage refinement

Home order: Hero → Featured Projects (AP SELECT, LIA, AP Revenue) → three portfolio grids → compact Why AP → compact Global-by-Design → About / IR / Founder’s Lab / Contact. Homepage copy is separately managed in `home-copy.json`; full explanations, professional boundaries and technical market-pack content remain in product pages and public IR.

Original Safe food-scan, Light food-choice, Travel demand/event and craft visuals are reused in the homepage grids. Their existing videos are restored on the corresponding product pages using explicit controls, preload=none and existing poster files. Travel remains a global cross-market decision product.

AP SELECT uses a new Higgsfield concept image and eight-second silent film, identified as a design-stage AI concept. Media provenance is in `select-media.json`. LIA and Revenue use short, one-time CSS path animations; Revenue’s visual contains no actual metrics or operating data.
