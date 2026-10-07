# LIA interactive showcase · 2026-10-07

The LIA product page is the AP Entertainment destination linked by the existing portfolio. Its first screen uses a six-cell image atlas rather than a rigged 3D model. Cursor direction selects a pose; link hover and keyboard focus select greeting; tapping the portrait toggles greeting. Reduced-motion preference disables automatic reactions and perspective. A visible control pauses reactions. Existing locale sections, social destinations, and contact email remain.

Asset: `/media/lia/lia-interactive-atlas-v1.png`. Built-in image generation, based on existing `/media/lia/lia_hero_sq.jpg`. Prompt: preserve adult LIA identity and brown hair; premium stylized character in a white blouse behind a plain silver laptop; equal 3×2 cells for neutral, left/right, up/down and greeting; consistent camera, scale and lighting; no labels or trademarks. Generated atlas renders a studio background and the two side poses both look right, so the left reaction mirrors the side pose in CSS. No genuine continuous 3D head tracking is claimed.

Canonical renderer: `scripts/lia_showcase.py`; loaded only on LIA product pages in all six current locales. CSS/JS are separate and versioned. Content and links remain usable without JS. Existing content videos load only on demand, with controls and no autoplay.

Run `python3 scripts/build_site.py`, then keep the LIA generated pages only if unrelated generated output would regress current manually refined pages. The existing full site checker expects retired `RGRG` copy on the KO/EN home pages; current home pages say QuizRanker. Preserve their current content rather than reverting them to satisfy this legacy check.

## Identity correction

V2 replaces the consumed atlas after owner feedback that the stylized face differed. The prompt uses the original LIA photo as the authoritative identity and the previous atlas only for layout, requiring natural photographic facial proportions and subtle pose changes. Asset: `/media/lia/lia-interactive-atlas-v2.png`. Exact likeness remains subject to owner review; no deployment has been approved.

## Canonical Higgsfield identity · V3

Higgsfield reference element `71ea8d4d-b684-453f-9b99-9a074bef90c7`, named `Lia-soul`, points to media `cab1e84b-9980-4a20-b2b7-eff63dcfe667` (Yangyang surfboard photo). Found in existing portrait job `e63c3be1-5c29-4157-999f-fdbe32029237`. The same beach face crop is reused by hiking job `ca9d68d7-2a52-4d61-bbfa-c212fa9ae469`. V3 uses these references, not the rejected website hero photo or V1/V2 faces. Built-in image generation preserves natural photographic facial proportions, white blouse and laptop, six subtle poses. Left/right cells are now distinct, so mirroring is removed. Exact face likeness still requires owner judgement. Source identity reference is preserved at `/media/lia/lia-soul-reference.png`; consumed atlas is V3. Not deployed.
