# AP News Daily 운영

승인: 2026-10-09. 발신 AP News <alfred.park@apholdings.kr>. 무료 한국어, 매일 08:00 KST 목표.

## 발행 절차
1. 공식 원문을 확인하고 issues/YYYY-MM-DD.json 한 파일 작성. date, number, title, intro, edition_note, takeaway 및 stories 5~7개. 기사마다 title, source, url(HTTPS 원문), published(발표일), fact, insight, action을 기록.
2. 불확실한 내용이면 status=draft, verified=false로 보존하고 발행하지 않는다. 완료된 원문 검증 후 status=published, verified=true. 사람의 검수를 받지 않았다면 AI 작성·원문 확인이라고 표시.
3. Python 런타임에 requirements-newsletter.txt 설치 후 `python scripts/newsletter.py` 실행. 기존 뉴스와 함께 일일 웹·메일·PDF·최신호 링크를 생성.
4. `python scripts/test_newsletter.py`, `node --test supabase/functions/ap-news/core.test.mjs`, 기존 `python scripts/check_site.py` 실행. PDF를 페이지별 렌더해 실제 확인.
5. 다른 홈페이지 작업과 충돌하지 않도록 최신 main을 확인하고 변경 파일만 적용. 기존 public GitHub Pages가 배포한다. 공개 웹·PDF가 해당 원본으로 제공되는지 확인한 뒤 ap_news_issues에 등록한다. 검증되지 않은 URL은 DB 발행으로 등록하지 않는다.
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

## 컴퓨터가 꺼져 있어도 실행하는 서버 발행 (2026-10-27)
- GitHub Actions `AP News server daily`가 Ubuntu 서버에서 KST 06:00~09:45, 15분 간격으로 실행한다. 08:00 이전에는 검증한 초안·이미지·미리보기를 Actions artifact로 저장하고 공개 커밋과 메일 등록은 하지 않는다. 08:00 이후 최초 성공 실행이 발행·배포·등록한다. GitHub 예약은 지연될 수 있으므로 08:00은 목표이며 초 단위 정시 보장은 아니다.
- `OPENAI_API_KEY`는 저장소 Actions secret, `SUPABASE_SERVICE_KEY`는 기존 서버 secret을 사용한다. 로컬 PC와 Codex 실행이 필요 없다. API 사용료는 해당 OpenAI API 프로젝트에 청구된다. 키 값·구독자 주소·발송 본문은 작업 로그나 artifact에 저장하지 않는다.
- `scripts/newsletter_server.py`: 공식 도메인 실시간 검색 → 원문 직접 확인 → 발표일·수치·제공 국가·실험 단계 독립 AI 검증 → 기사 5개 선택 → 원본 편집 이미지 생성 → 기존 `scripts/newsletter.py` 빌드 → PDF 내용·링크·모바일·모든 지면 AI 시각 검증. 사람 검수를 주장하지 않는다.
- HTTP 408/429/5xx와 연결 오류는 제한된 지수 간격으로 재시도한다. 완료한 원문 검증과 이미지는 같은 날짜의 checkpoint artifact에서 복구한다. 검증이 실패하면 초안을 보존하고 공개/발송을 보류한다. checkpoint는 7일 보관한다.
- 하나의 concurrency 그룹이 발행 중복을 막는다. 오늘 발행 JSON이 있으면 다시 생성하지 않는다. 최신 main에 안전하게 rebase하고 뉴스 관련 파일만 커밋하며 충돌 시 멈춘다. 다른 홈페이지 생성기는 실행하지 않는다.
- `Publish existing AP Holdings site`는 기존 main의 정적 파일을 기존 도메인에 배포한다. 홈페이지의 다른 main 변경도 이 workflow로 배포한다. GITHUB_TOKEN으로 만든 뉴스 커밋은 별도 push workflow를 유발하지 않으므로 발행 workflow가 Pages 배포를 명시적으로 호출한다.
- 공개 웹·PDF·이메일 HTML·모든 기사 이미지가 저장소의 검증된 바이트와 같아야 Supabase에 등록한다. 이미 등록한 호는 수정하거나 재발송하지 않는다. 기존 확인 완료 active 구독자 큐만 사용하며 발신은 `alfred.park@apholdings.kr`다. `publish_at`은 해당 날짜 08:00+09:00이며 큐는 이후 처리한다.
- 수동 복구: Actions → `AP News server daily` → Run workflow. `connection_test=true`는 텍스트·이미지 API를 시험하며 구독자에게 별도 시험 메일을 보내지 않는다. 발행/등록도 같은 안전 절차로 확인한다.
- 운영 확인: Actions 실행 결과와 artifact, 관리자 뉴스 메뉴의 호·발송 상태를 확인한다. `sent` 및 provider ID는 전송 서비스 접수를 의미하며 받은편지함 도착을 보장하지 않는다. 인증·결제 오류는 자동 재시도로 해결되지 않으므로 해당 계정 설정이 필요하다.
- 로컬 heartbeat `ap-ai`는 서버 실운영 검증에 성공한 후 중복 실행을 피하도록 중지한다. 서버 연결 검증 전에는 대체 수단으로 유지한다.

## 이미지와 편집 품질 (2026-10-11 개편)
- 최신 호는 기사별 summary 한 줄과 AP 서비스에 연결되는 insight를 작성한다. 사실과 해석은 분리하고 제공 국가·실험 단계·신청 자격을 생략하지 않는다.
- 기사별 image는 path(`/img/newsletter/파일명.png` 등), alt, caption을 가진다. 파일은 저장소에 보관하며 원문 이미지 권리가 명확하지 않으면 독창적인 편집 일러스트를 사용한다.
- AI 생성 이미지는 `AI 제작 · 편집 일러스트 · 실제 제품 화면 아님`으로 표시한다. 실제 발표 사진이나 제품 화면처럼 소개하지 않는다. AP 로고를 새로 생성하지 않는다.
- 웹·PDF·HTML 이메일은 같은 JSON의 summary, fact, insight, action, image를 사용한다. PDF는 표지와 기사별 지면으로 구성한다. 이미지 없는 이전 호도 빌드할 수 있다.
- 이미지 제작 기록은 docs/newsletter-image-prompts-2026-10-11.md에 보관한다. 이후 매일 해당 기사 주제에 맞는 새 이미지를 준비하고 재사용 시 기사와 관련 있는지 확인한다.
- 이미 발행한 호를 수정해도 새 번호·새 발송을 만들지 않는다. DB 갱신 전 공개 웹과 PDF를 검증하고, 기존 발송의 고정 본문과 재시도 기록을 변경하지 않는다.
