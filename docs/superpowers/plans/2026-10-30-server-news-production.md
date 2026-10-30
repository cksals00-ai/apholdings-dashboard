# AP News server-only production

Goal: produce and publish daily AP News without the local computer/app and without paid AI APIs.

Architecture: GitHub-hosted CPU production starts before the publication window.
Pinned public Qwen GGUF weights perform Korean editorial work through a localhost
llama.cpp process; pinned public diffusion weights produce original editorial
images on CPU. No hosted inference endpoints, AI keys, billing setup or paid
fallbacks. Existing isolated publisher, confirmed-subscriber queue and independent
Supabase alert remain responsible for publication, delivery and notification.

The user's request authorizes this migration; do not insert another approval into
routine production. Model quality/time must be measured before enabling schedule.

- [ ] Probe pinned CPU text/image models on the actual server; inspect output and resource/time limits.
- [ ] Implement allowlisted official feed/article collection, source evidence/date validation and prior-URL deduplication.
- [ ] Implement grounded Korean generation with quoted evidence, independent claim review and restrictive factual validation; preserve draft on failure.
- [ ] Produce varied topic-specific artwork, date-specific GIF/poster, retain original AP logo and truthful AI illustration labels.
- [ ] Render web/email/PDF from same JSON; render all PDF pages and check Korean/text bounds/links; browser390/1440/image/motion QA; compare image similarity with prior3 editions.
- [ ] Checkpoint every accepted story/image, preserve server artifacts, package only after all gates pass, reuse existing valid bundles.
- [ ] Add server producer schedule, bounded failed-job recovery and immediate pre-recovery alerts; retire local producer as an active dependency after verified handover.
- [ ] Run isolated full production rehearsal without regular subscriber resend; review and enable only validated server path.

Limits: source verification is automated and never represented as human review.
Invalid/insufficient source material or failed quality checks stop publication and
trigger notification; no old issue or fabricated news is substituted. Infrastructure
execution still uses the existing runner quotas; no new paid infrastructure is purchased.

## Qualification evidence so far

- Standard public CPU runner measured 4 CPUs / 15.6 GiB. Public SSD-1B/LCM
  art probe completed in196 seconds; no hosted AI inference or billing used.
- 68 newsletter unit tests, regular mail queue core tests, four watchdog health
  tests and workflow/type validation pass. These do not qualify content quality.
- Private draft checkpoint actually saved/restored; no raw drafts retained in
  public Actions artifacts.
- Operational Edge function v5 and minimal RPC migration deployed; unauthenticated
  watch denied401; independent server minute-watch returns200. Today's original
  regular queue remains accepted3 / blockers0; no resend.
- Full 8B source-to-art/PDF rehearsal40995176898 in progress. Main recovery
  rehearsal40995484330 queued with private resume and intentional first failure.
- Daily server production schedule remains OFF; local producer is not retired
  until successful end-to-end qualification and actual output review.
