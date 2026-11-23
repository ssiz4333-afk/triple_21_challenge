# 21일 트리플챌린지

이오메가 리퀴드 · 레몬 · 포스티엠 21일 트리플챌린지 체크 & 인증 앱 (v2.1 · 실시간 공유 · 홈 화면 앱)

- 웹 앱: https://ssiz4333-afk.github.io/triple_21_challenge/
- 제작자: [@erang_coach](https://www.instagram.com/erang_coach/)
- `index.html` + `manifest.json` + `sw.js` + 아이콘 PNG로 동작합니다. GitHub Pages 배포용 설정은 `.nojekyll`.
- 아이콘은 `tools/make_icons.py`로 다시 만들 수 있습니다(`icon-192.png`, `icon-512.png`, `apple-touch-icon.png`, `favicon-32.png`).

## 홈 화면 앱(PWA)

- `manifest.json`: 이름 `21일 트리플챌린지` / 짧은 이름 `트리플21` / `display: standalone` / 테마 `#0d9488` / 배경 `#f4faf7`
- `index.html`이 `sw.js`를 등록하고, 실행 직후 0.9초 스플래시 시작 화면을 보여 줍니다.
- 앱 안 `설정 → 📲 바탕화면 앱으로 추가하기`(또는 오늘 탭 안내 배너)에서 안드로이드 크롬은 바로 설치, 아이폰은 사파리 공유 → 홈 화면에 추가 안내를 봅니다.
- 서비스 워커는 네트워크 우선이라 항상 최신 화면을 먼저 받고, 오프라인일 때만 캐시로 엽니다.

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
