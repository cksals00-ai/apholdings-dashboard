# AP News Admin Implementation Plan
Goal: 기존 관리자 메뉴에서 신청자와 발송 상태를 간결하게 확인.
Architecture: owner 보호 /admin 응답을 확장하고 newsletter.js에서 네이티브 details와 검색 필터로 표시.
Tech Stack: JavaScript, Deno Edge Function, HTML details.
- [ ] owner 응답의 허용 필드와 신청자별 발송 연결 변경을 테스트.
- [ ] admin/newsletter.js에 최근 5명, 접힌 전체 목록과 검색/필터, 신청자별 발송 기록 구현.
- [ ] index.ts에 email/name/created_at, subscriber_id와 subscribers 응답 추가. 인증·토큰 제외 유지.
- [ ] JS 테스트와 모바일 브라우저 검증, 익명 API 401 검증.
- [ ] Edge Function 및 Pages 배포, 실제 공개 코드 확인.
