# 하자증권 B2B 지원 페이지 Implementation Plan

> **For agentic workers:** Use executing-plans to implement this plan task-by-task in this session.

**Goal:** apholdings.kr/hajeung/ 에 설치 안내, 회사 이메일 신청, 비공개 수정 요청과 기존 관리자 처리를 제공한다.
**Architecture:** 기존 정적 사이트 + Supabase email magic link 인증 + 소유자·작성자 RLS + 비공개 Storage. 앱 계정 발급은 운영 관리자가 명시적으로 실행하며 demo=true, 등록·수정 역할만 부여한다.
**Tech Stack:** HTML/CSS/ES modules, 기존 고정 Supabase JS 버전, Postgres, Node test/PGlite.

## Global Constraints
- Apple ID 발급 없음. Apple 유료화 동등성은 실제 대조 전 완료로 표시하지 않음.
- 원본 운영 앱 데이터와 웹 신청 데이터 분리, 코드는 공개·게시글·로그에 저장하지 않음.
- 다른 사용자의 신청·게시물·첨부 접근 차단, 관리자 권한은 서버에서 확인.
- 실제 심사 제출·출시는 별도 작업. 기존15개 업로드를 정식 출시로 표현하지 않음.
- 실환경 보안 권한 적용·메일 인증 설정은 구체적 검증 결과와 함께 사용자 확인 후 실행.

### Task 1: 데이터 계약과 권한 검증
Files: hajeung/model.mjs, tests/hajeung-model.test.mjs, supabase/hajeung_support.sql, tests/hajeung-rls.test.mjs.
- [ ] Node 테스트로 이메일·필수 항목·사진 MIME/크기·상태 전환 경계를 먼저 실패 확인한다.
- [ ] validateApplication, validateRequest, validateAttachment, labels 함수를 구현한다.
- [ ] b2b_applications, b2b_requests, b2b_replies와 비공개 첨부 정책을 SQL로 작성한다.
- [ ] PGlite에 auth.uid/auth.jwt와 storage mock을 구성하고 authenticated 두 사용자·익명·관리자 권한을 실제 SQL로 검사한다.
- [ ] 승인/발급 분리, 기존 운영 이메일 충돌 차단, demo 담당자 코드 hash만 저장, 코드 한 번 반환 계약을 검증한다.

### Task 2: 모바일 공개·비공개 화면과 관리자
Files: hajeung/index.html, style.css, app.mjs, config.mjs, admin/b2b-support.mjs; modify admin/index.html, admin/admin.js.
- [ ] 공개 화면에 실제 TestFlight 링크와 Android 준비 중 상태, 순서별 가이드, 유료화 확인 중 안내를 작성한다.
- [ ] 이메일 링크로 확인 후 신청·수정 요청·첨부 업로드·본인 기록 조회를 구현한다.
- [ ] 메시지는 textContent로 출력, 중복 전송 방지, 실패 시 재입력 유지, 세션 종료 시 비공개 화면·사진 URL 제거를 구현한다.
- [ ] 관리자 신청 승인·보류·거절, 발급 버튼, 요청 상태·답변·첨부 열람을 연결한다.
- [ ] 일반 사용자 클라이언트에서 임의 owner/status/email 재지정으로 권한 확대가 불가능한지 검증한다.

### Task 3: 검증과 운영 준비
Files: docs/hajeung-support-operations.md, tests/hajeung-site.test.mjs, outputs/hajeung-support-20261027/.
- [ ] Node/PGlite 테스트 및 JS 구문 검사, 기존 관리자 금융 테스트를 실행한다.
- [ ] 로컬 페이지를 CUA로 모바일360/390px 및 데스크톱에서 확인해 이미지와 검증 범위를 남긴다.
- [ ] 로그인·업로드 실검증은 서버 적용 전 미검증으로 기록한다.
- [ ] 코드 검토 후 소스 커밋. 실제 서버 권한·인증 설정·배포에 필요한 마지막 승인을 요청한다.
