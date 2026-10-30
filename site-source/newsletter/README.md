# AP News Daily 운영

승인: 2026-10-09. 발신 AP News <alfred.park@apholdings.kr>. 무료 한국어, 매일 08:00 KST 목표.

## 발행 절차
1. 공식 원문을 확인하고 issues/YYYY-MM-DD.json 한 파일 작성. date, number, title, intro, edition_note, takeaway 및 stories 5~7개. 기사마다 title, source, url(HTTPS 원문), published(발표일), fact, insight, action을 기록.
2. 불확실한 내용이면 status=draft, verified=false로 보존하고 발행하지 않는다. 완료된 원문 검증 후 status=published, verified=true. 사람의 검수를 받지 않았다면 AI 작성·원문 확인이라고 표시.
3. Python 런타임에 requirements-newsletter.txt 설치 후 `python scripts/newsletter.py` 실행. 기존 뉴스와 함께 일일 웹·메일·PDF·최신호 링크를 생성.
4. `python scripts/test_newsletter.py`, `node --test supabase/functions/ap-news/core.test.mjs`, 기존 `python scripts/check_site.py` 실행. PDF를 페이지별 렌더해 실제 확인.
5. 로컬 제작은 아래 완성본 전달 절차를 따른다. 준비 커밋을 main에 push하지 않는다. 서버가08시 이후 공개·파일 일치 확인·DB 큐 등록을 담당한다.
6. DB에는 issue_date, number, title, status, verified, web_url, pdf_url, email_html(생성본), source_data(JSON), publish_at(날짜 08:00+09:00)을 등록. pg_cron의 5분 큐가 활성 구독자에게 해당 날짜의 호만 보낸다.

## 회사 메일 연결
Resend에서 apholdings.kr 도메인 인증. Supabase Edge Function Secrets에 RESEND_API_KEY 등록, AP_NEWS_MAIL_ENABLED=true 설정. 키를 채팅·파일·Git에 넣지 않는다. FROM은 회사 주소로 고정되어 있으며 개인 Gmail로 임의 대체하지 않는다.

기본값은 발송 비활성이다. 발신 도메인·인증이 완료됐다는 사실과 본인 주소로 확인 메일·일일판 수신·해지 시험이 성공해야 실제 운영 완료로 보고할 수 있다. 연결 전 구독 폼은 신청 접수/확인 대기라고 표시한다. pending 신청은 30일 안에 확인하지 않으면 삭제된다.

## 데이터·실패 처리
- 서버 전용 테이블과 RPC. 브라우저의 publishable key로 구독자 조회 불가. 관리자 endpoint는 기존 AP 관리자 UUID를 auth 서버에서 검증.
- 이메일 확인 토큰 48시간. 링크의 fragment에 담아 로그·referrer 노출 방지. 링크 열기만으로 상태가 바뀌지 않으며 실제 확인 버튼 POST가 필요.
- 구독 해지는 서명 링크 POST. 이후 큐는 해당 구독자 제외. 중복 발송은 호/구독자 유일 키와 Resend Idempotency-Key로 방지.
- 결과가 불확실한 발송은 23시간 이후 자동 재시도하지 않는다. 관리자에서 확인해야 한다. 전송 서비스 접수와 실제 받은편지함 도착은 구분한다.
- 해지 및 미확인 데이터 30일 내 삭제, 요청 제한 기록 7일 내 삭제. 매일 03:15 KST 삭제 예약.
- 발행 자동화는 이 채팅에 연결. 홈페이지 main과 발행번호가 바뀌었으면 최신 상태를 기준으로 중복 없이 작업. 발송 서비스를 설정하지 않아도 웹·PDF 발행은 계속한다.

## 서버 설치·검증 기록
구독 스키마는 supabase/ap_news_schema.sql, 검토 보완 RPC는 supabase/ap_news_queue_fixes.sql 순서로 적용한다. 초기 migration 도구는 요청 상태 만료 오류를 반환하여, 사용자 재승인 후 트랜잭션 SQL로 적용했다. 서버는 회사 메일 연결 전에도 신청 접수를 지원한다.

리뷰 보완: 준비 기간에 시도하지 않은 만료 확인 메일은 발송 연결 후 새 토큰을 발급한다. 이미 발송·실패한 메일을 자동 반복하지 않는다. 해지와 큐 취소를 한 트랜잭션으로 처리하고, 제공사 요청을 최초 시점에 저장해 재시도 때 같은 본문을 사용한다. 발송 직전 현재 구독·큐 상태를 다시 검사하고, 이미 제출된 요청은 처리 중으로 간주하며 취소 상태를 완료·재시도로 되돌리지 않는다.

메일 큐 ap-news-mail-queue는 5분마다, 보관 정책 ap-news-retention은 03:15 KST에 실행한다.

## 유료 AI API 없는 제작·예약 발행 (2026-10-27 전환)
사용자 승인: 이 채팅에서 assistant가 뉴스 조사·편집, 이미지, 웹·PDF·메일 제작과 검증을 수행한다. 서버는 완성본을 받아 오전08시 발행·메일 큐 등록만 담당한다. OpenAI API를 호출하거나 API 키를 작업에 전달하지 않는다. 이전 API 제작 구조는 폐기했다.

### 로컬 제작·검증·전달
1. 로컬 자동화 `ap-ai`는 KST06:00/06:30/07:00/07:30에 준비를 확인한다. 이 제작 단계에는 컴퓨터와 앱이 켜져 있어야 하며 구독의 사용 한도가 적용된다. 이미 서버에 전달한 완성본의 예약 발행·메일은 PC가 꺼져도 진행한다. PC가 꺼져 있으면 새 호 제작을 보장하지 않는다.
2. 최신 origin/main, 당일 공개 호와 준비용 draft release를 먼저 확인한다. 이미 전달한 완성본은 반복 제작하지 않는다. sources/와 다른 채팅의 체크아웃은 수정하지 않는다.
3. 원고·출력물은 최신 main에서 만든 로컬 준비 브랜치(예: prep/ap-news-YYYY-MM-DD)에서 다루고 로컬 커밋으로 보존한다. 준비 커밋을 main에 push하지 않는다. 다른 홈페이지 변경을 취소하지 않는다.
4. 기존 imagegen·PDF 스킬과 scripts/newsletter.py로 완성본을 만든다. 공식 원문·실제 발표일·모든 PDF 페이지·모바일·이미지·원문 링크를 확인한다. 유료 API로 대체하지 않고 사람 검수를 임의로 주장하지 않는다.
5. 검증 완료 후 `python scripts/newsletter_handoff.py package --date YYYY-MM-DD --file /absolute/output/AP-News-YYYY-MM-DD-ready.zip --reviewed`, 이어 `python scripts/newsletter_handoff.py upload --date YYYY-MM-DD --file /absolute/output/AP-News-YYYY-MM-DD-ready.zip`을 실행한다. --reviewed는 실제 확인이 끝났을 때만 사용한다.
6. 전달함은 사용자 회사 저장소 cksals00-ai/apholdings-dashboard의 인증된 GitHub draft release `ap-news-ready-YYYY-MM-DD`다. 공개 릴리스로 전환하지 않는다. 완성 ZIP은 해당 날짜 JSON·웹·PDF·이메일·기사 이미지·SHA256 및 AI 검증 기록만 포함한다. 키나 구독자 정보는 넣지 않는다. 업로드 후 draft 상태와 첨부파일 존재를 확인하고 로컬 진행 기록을 보존한다. 승인 검토가 차단하면 초안을 보존하고 사유를 알린다.

### 서버 발행·메일
- AP News server daily는 GitHub 서버에서 KST08:00 및 이후09:45까지 복구 점검을 실행한다. GitHub 예약 자체는 지연될 수 있으므로08:00은 목표이며 초 단위 정시를 보장하지 않는다.
- 당일 완성본의 날짜·번호·SHA256·허용 경로·원문 날짜 범위·이미지 디코딩·웹/메일/JSON 일치·PDF 내용/원문 링크를 확인한다. 변조·번호 충돌이면 보류한다. 완성본이 없으면 awaiting_ready로 종료하며 이전 호를 다시 보내지 않는다.
- 기존 발행 호는 바꾸지 않는다. 새 호는 받은 파일을 그대로 복사하고 기존 newsletter.py의 인덱스 전용 모드로 아카이브·최신호·뉴스 안내 링크만 갱신한다. 서버에서 PDF·이미지·원고를 생성하지 않는다.
- 최신 main 안전 통합 → 기존 회사 Pages 배포 → 공개 웹·PDF·이메일·이미지 바이트 확인 → Supabase 일회 등록 순서다. 제작용 API 키는 사용하지 않는다. 기존 SUPABASE_SERVICE_KEY는 큐 등록 단계만 사용한다.
- 기존 확인 완료 active 구독자 큐와 발신 alfred.park@apholdings.kr를 유지한다. publish_at=해당 날짜08:00+09:00, 큐는5분 간격이다. 이미 등록·제공사 접수된 건은 재발송하지 않는다. 제공사 접수와 받은편지함 도착은 구분한다.
- 수동 전달 검증: Actions → AP News server daily → Run workflow → verify_ready=true. 이 모드는 읽기 전용이며 공개·DB 등록·발송하지 않는다. 일반 Run workflow는 당일 발행/복구 절차다.
- 제작·전송·검증 오류는 초안과 완성 ZIP을 보존하고 알린다. 유료 AI API를 자동 복구 수단으로 사용하지 않는다.

## 이미지와 편집 품질 (2026-10-11 개편)
- 최신 호는 기사별 summary 한 줄과 AP 서비스에 연결되는 insight를 작성한다. 사실과 해석은 분리하고 제공 국가·실험 단계·신청 자격을 생략하지 않는다.
- 기사별 image는 path(`/img/newsletter/파일명.png` 등), alt, caption을 가진다. 파일은 저장소에 보관하며 원문 이미지 권리가 명확하지 않으면 독창적인 편집 일러스트를 사용한다.
- AI 생성 이미지는 `AI 제작 · 편집 일러스트 · 실제 제품 화면 아님`으로 표시한다. 실제 발표 사진이나 제품 화면처럼 소개하지 않는다. AP 로고를 새로 생성하지 않는다.
- 웹·PDF·HTML 이메일은 같은 JSON의 summary, fact, insight, action, image를 사용한다. PDF는 표지와 기사별 지면으로 구성한다. 이미지 없는 이전 호도 빌드할 수 있다.
- 이미지 제작 기록은 docs/newsletter-image-prompts-2026-10-11.md에 보관한다. 이후 매일 해당 기사 주제에 맞는 새 이미지를 준비하고 재사용 시 기사와 관련 있는지 확인한다.
- 이미 발행한 호를 수정해도 새 번호·새 발송을 만들지 않는다. DB 갱신 전 공개 웹과 PDF를 검증하고, 기존 발송의 고정 본문과 재시도 기록을 변경하지 않는다.

## 관리자에서 전달·발행·메일 상태 확인
- 기존 /admin/ → AP뉴스 구독·발송 상단에서 한국시간 오늘의 서버 전달, 홈페이지 공개 검증, 메일 전송 서비스 접수 건수를 확인한다. 내일 전달한 호는 상세의 다른 날짜 기록으로 분리한다.
- 전달 완료는 로컬 파일 존재가 아니라 GitHub 서버가 draft release ZIP을 다운로드하고 검증한 뒤 기록한 상태다. upload 명령이 이 기록용 서버 작업을 자동 요청한다. 보통 서버 실행이 끝난 뒤 표시된다.
- 이미 전달했는데 상태 기록만 누락되면 `python scripts/newsletter_handoff.py report --date YYYY-MM-DD`로 기록만 복구한다. ZIP을 다시 만들거나 메일을 재발송하지 않는다.
- 공개 확인은 실제 공개 파일과 JSON/웹/PDF/이메일/이미지 일치 및 ap_news_issues 등록을 확인한 결과다. URL이나 DB 행만으로 공개 완료를 주장하지 않는다.
- 메일 요약은 최근100행 목록이 아닌 서버의 전체 호별 집계를 사용한다. 접수·대기·실패·결과 불명은 구분하고 받은편지함 도착으로 표현하지 않는다. 본문·수신자 상세는 기존 관리자 인증을 그대로 사용한다.
- 발행 기록과 집계는 service_role만 접근하며 기존 owner 인증 Edge admin endpoint를 통해서만 관리자 브라우저에 전달한다. 브라우저에 서비스 키를 넣지 않는다. 유료 AI API는 사용하지 않는다.

## 2026-10-28: editorial motion edition

New editions use `layout: "editorial-v2"` and `hero` with `path: "/img/newsletter/ap-signal-v1.gif"`, `poster: "/img/newsletter/ap-signal-v1.png"`, Korean `alt`, and caption `AP 브랜드 모션 그래픽 · 실제 제품 화면 아님`. The original abstract signal graphic is reproducible with `python scripts/newsletter_motion.py` (Pillow only; no API). Keep the existing AP logo unchanged.

Web uses a looping GIF with pause control and reduced-motion static poster; email uses a 600px presentation table and GIF with meaningful first frame (some email readers show only that frame). PDF uses the corresponding PNG poster. Every bundle includes both assets, and public verification checks their bytes. Story summary, fact, insight and source remain shared; action is retained in JSON for compatibility but is omitted in v2 outputs. `takeaway` provides the final **AP의 시선**, a synthesis of business implications rather than repeated instructions. Existing editions retain legacy rendering. Run `scripts/test_newsletter_editorial.py` alongside existing checks; inspect all PDF pages, GIF frames and mobile/desktop before upload. No paid AI API is used.


## 2026-10-28:08:00 server reservation and cron fallback

Observed incident: the AP workflow had correct UTC23:00 schedule on active default-main configuration, but no schedule event was created. Other repository scheduled jobs existed. GitHub's internal reason is not observable; cron timing alone cannot guarantee08:00. Today's local bundle was also only delivered after08:00.

`newsletter_handoff.py upload` now requests both receipt verification and a separate `reserve_publication=true` server run. The reservation validates the completed ZIP and records server receipt, runs safety checks, then holds the server runner until08:00 KST before normal publication. It accepts today's date and at most five hours of early waiting; job timeout is six hours. No public files or queue are changed before08:00. The unchanged verified publication and confirmed-active queue handle existing editions without duplicate sends. The existing cron remains a recovery fallback and its failure handler records errors in admin. This uses the existing GitHub Actions runner and credentials; no paid AI API or copied personal token.

When a bundle is already uploaded but no reservation run exists, use `python scripts/newsletter_handoff.py reserve --date YYYY-MM-DD`; do not regenerate/reupload it. `report` continues to record receipt only. A successful upload/dispatch is not proof of final publication: check the reservation run, admin public verification, and delivery summary. Preparation must finish before08:00 (target07:45); delayed local preparation or infrastructure can still delay delivery.

### 2026-10-29 cover replacement
New issues use `/img/newsletter/ap-editorial-v2.gif` and matching `.png`, with alt `아이보리 지면과 네이비·세이지 패널이 천천히 펼쳐지는 AP 편집 그래픽`. Caption remains `AP 브랜드 모션 그래픽 · 실제 제품 화면 아님`. This original code-native editorial paper composition replaces the orbit graphic for future issues. Generate with `scripts/newsletter_cover.py`; no external assets or API. Retain earlier issue assets unchanged. From2026-10-29, explicit light text colors in the email masthead fix nested-table color inheritance in mail readers.

## Independent server watchdog and automatic recovery
`ap-news-independent-watch` runs every minute on Supabase, independently of the local app. It alerts the fixed owner recipient if completed handoff is missing after07:45, publication is missing after08:05, mail is incomplete after08:10 or an explicit publication error exists. Events are private in `ap_news_ops_events`; operational alerts are separate from subscriber deliveries. Existing confirmed-active owner check, fixed sender and provider idempotency apply. A recovered public issue with complete mail produces one recovery notice.

`AP News automatic recovery` watches failed `AP News server daily` and isolated rehearsal runs. It sends an operational alert and reruns only failed jobs, at most three total attempts; it does not generate new content or overwrite sent deliveries. The watchdog remains independent if GitHub fails to start a job. If new content itself is absent, the server cannot generate it without the authorized local production step; it alerts instead of silently substituting an old issue.

`AP News automation rehearsal` publishes only a noindex preview under `/ko/news/daily/preview/automation-RUN/` and `/newsletters/previews/`. It deliberately fails the first scheduled publication attempt, relies on the same recovery workflow, verifies public bytes, and tests transient mail failure/retry. Only `cksals00@naver.com` receives clearly labelled test/incident/recovery messages. No ordinary issue, archive, number or subscriber queue is modified. Provider acceptance is not inbox delivery. Credentials are neither copied into files nor emitted in logs.

## 2026-10-29 unattended boundary and completion gate
Daily production must not edit or deploy operational code. Before writing articles or generating images, pass candidate official URLs and dates to `scripts/newsletter_preflight.py --date YYYY-MM-DD --candidates /absolute/candidates.json`. Unsupported, duplicate and stale candidates are rejected independently; choose other verified, supported original sources within the disclosed date window. Five supported originals are required. This does not verify article facts and never relaxes source policy. Insufficient verified news triggers an alert, not fabricated content or an old-issue resend.

Prepare from04:00 KST; aim for completed handoff by07:15, retaining later checks for recovery. This still requires the computer and app for new content. The uploaded bundle and server reservation require no further local approval. Operational changes are separate from daily production.

The server registration job now waits for whole-issue mail acceptance with `wait-mail`. The read-only service-role RPC `ap_news_delivery_health` returns confirmed-active count and aggregated delivery states, without recipient data. Pending/processing/retry/failed/uncertain/unconfirmed never count as completion. A bounded timeout fails the job, so the existing independent alert/recovery chain can detect incomplete mail. It never dispatches or resends itself. Provider acceptance is not inbox arrival.

Fault rehearsal additionally inserts an unsupported source candidate and proves it is excluded without changing the allowlist. The existing deliberate first-publication failure and first-operational-test-mail failure still exercise real bot rerun, public byte verification, fixed-owner test mail and incident/recovery notices. This is isolated from the regular subscriber queue; it does not prove every provider failure mode or exact08:00 wall-clock delivery. GitHub Pages deployment and provider latency remain external dependencies.

### Independent publication runtime (2026-10-30)

The daily publisher and recovery notifier use reviewed runtime revision
`f38cded5abffd43f49c4c3dc95191563b0bc0d6f`, not mutable homepage scripts on main.
`AP_NEWS_SITE_ROOT` points that runtime at the current content/preparation checkout.
Run safety tests in the runtime checkout with this variable unset; run source
preflight, rendering, packaging and handoff against the preparation checkout with
it set. The producer must use the same pinned renderer as the server. Changing
this pin is a reviewed newsletter release, not an incidental homepage deployment.

`ap-news-daily.yml` validates only newsletter safety gates and complete bundle
checksums/documents; unrelated `check_site.py` does not gate newsletter publication.
`ap-news-pages.yml` archives current main without executing homepage generators,
analytics installers or checks. It shares the Pages deployment mutex, preserving
latest homepage files while preventing simultaneous domain deployments.
The rehearsal injects broken homepage tools in disposable checkouts, forces a first
publication failure, and verifies recovery, actual public preview bytes and one
owner-only test mail. Regular recipients are not included in that rehearsal.

New content still requires the local producer and app to run at04:00 KST.
A verified server reservation does not require the local computer to remain on.
08:00 starts the reserved publication; Pages rollout and mail provider acceptance
are separate measured milestones. Do not claim exact public/inbox timing before
these milestones have actually been observed.

Daily handoff updates only newsletter-owned paths. The six homepage promo links
use `/ko/news/daily/latest/` and `/newsletters/AP-News-latest.pdf`; homepage files
and the root sitemap are not edited or staged by daily publication.

The ordinary homepage Pages workflow defers deployments during07:40–08:25 KST
and catches up at08:25. Its deployment mutex is acquired only after this guard,
which reduces homepage competition in the target window. GitHub Pages is still a
shared deployment service: its queue is not a strict priority/SLA mechanism. The
newsletter dedicated delivery workflow bypasses this homepage guard.

## Server-only production migration (qualification in progress, 2026-10-30)

The new `AP News server production` workflow has a fail-closed qualification
job before its producer. Scheduled checks at KST03:05/03:35 and04:05–07:05 can
start generation only after main rehearsal41031927070 succeeds after automatic
bot recovery, with the exact same worker workflow and runtimee31f34dd. The
rehearsal covers actual collection, grounded Korean copy, new public-model art,
all-page PDF and browser QA, isolated public-byte checks and owner test-mail
failure/recovery. A running model probe is not a completed migration. Arming the
qualification check does not mark an unfinished rehearsal as qualified.

Generation uses pinned public model weights on the standard CPU runner, with no
hosted inference API, AI key or paid fallback. See `server-models.md`. Prompts and
raw source evidence are kept in authenticated private draft-release checkpoints,
not public Actions artifacts. Accepted copy/art and validated ZIPs survive retries.
The pinned renderer/publisher and regular subscriber queue remain separate from
homepage builders and homepage checks.

The independent server watchdog now reports 07:15 readiness delay, 08:00 progress,
explicit failures before recovery, and one final verified-publication/whole-active-
audience provider-acceptance result. Unknown mail health is an alert, never zero.
Retire the local producer when this gated server cadence is armed, to avoid
competing creators. Once the full rehearsal succeeds, activation is entirely
server-side; it does not wait for the local computer or app to reconnect.
Server email alerts work without the local app; this chat observer still requires
an active app. Provider acceptance is not an inbox-delivery guarantee.
