# 21일 트리플챌린지

이오메가 리퀴드 · 레몬 · 포스티엠 21일 트리플챌린지 체크 & 인증 앱 (v2.0 · 실시간 공유)

- 웹 앱: https://ssiz4333-afk.github.io/triple_21_challenge/
- 제작자: [@erang_coach](https://www.instagram.com/erang_coach/)
- `index.html` 한 파일로 동작합니다(아이콘은 base64 내장). GitHub Pages 배포용 설정은 `.nojekyll`.

## 저장 방식

- **내 체크 기록**은 기기 브라우저(localStorage)에 먼저 저장되어 오프라인에서도 열립니다.
- **인증 기록·소감·인증샷·응원**은 Supabase 서버에 저장되어, 링크를 받은 모든 회원이 `함께 인증샷` 탭에서 실시간으로 함께 봅니다.
- 서버 연결이 되지 않으면 자동으로 기기 저장 모드로 동작합니다.

## 서버 (Supabase)

- 프로젝트: `triple-21-challenge` (ref `lfphrvtbpomajgzglbya`, 리전 ap-northeast-2 서울)
- 테이블: `checkins`(user_key·day_no 당 1행, unique 인덱스), `reactions`(checkin_id·reactor_key·kind unique 인덱스)
- 스토리지: 공개 버킷 `shots` — 사진은 `public/<사용자키>/<날짜>-<시각>.jpg` 로 저장
- 실시간: `checkins`, `reactions` 두 표가 `supabase_realtime` 발행에 등록됨 (Realtime + 60초 주기 새로고침)
- 접속 정보는 `index.html` 안의 `CLOUD` 객체(URL·publishable 키)에 있습니다.

원본: `documents/triple_21_challenge.html`
