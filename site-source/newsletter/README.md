# AP News Daily 운영

승인: 2026-10-09. 발신 AP News <alfred.park@apholdings.kr>. 무료 한국어, 매일 08:00 KST 목표.

## 발행 절차
1. 공식 원문을 확인하고 issues/YYYY-MM-DD.json 한 파일 작성. date, number, title, intro, edition_note, takeaway 및 stories 5~7개. 기사마다 title, source, url(HTTPS 원문), published(발표일), fact, insight, action을 기록.
2. 불확실한 내용이면 status=draft, verified=false로 보존하고 발행하지 않는다. 완료된 원문 검증 후 status=published, verified=true. 사람의 검수를 받지 않았다면 AI 작성·원문 확인이라고 표시.
3. Python 런타임에 requirements-newsletter.txt 설치 후 `python scripts/build_news.py` 실행. 기존 뉴스와 함께 일일 웹·메일·PDF·최신호 링크를 생성.
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

일일 예약: Codex heartbeat ap-ai, 이 채팅에서 매일 07:00 Asia/Seoul 실행(08:00 발행 목표). 메일 큐 ap-news-mail-queue는 5분마다, 보관 정책 ap-news-retention은 03:15 KST에 실행한다.
