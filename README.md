# 21일 트리플챌린지

이오메가 리퀴드 · 레몬 · 포스티엠 21일 트리플챌린지 체크 & 인증 앱 (v3.6 · 21일+3일 보충·마무리 여유 기간 · 21일 완주 팡파레 · 관리자 새 기수 전체 리셋/공식 시작일 · 인증샷 타임스탬프 · 함께 인증샷 실시간 댓글 · 카카오 로그인 · 실시간 채팅 · 관리자 페이지 · 홈 화면 앱)

- 웹 앱(회원용): https://ssiz4333-afk.github.io/triple_21_challenge/
- 관리자(대표님 전용): https://ssiz4333-afk.github.io/triple_21_challenge/admin.html
- 제작자: [@erang_coach](https://www.instagram.com/erang_coach/)
- `index.html` + `admin.html` + `manifest.json` + `sw.js` + 아이콘 PNG로 동작합니다. GitHub Pages 배포용 설정은 `.nojekyll`.
- 아이콘은 `tools/make_icons.py`로 다시 만들 수 있습니다(`icon-192.png`, `icon-512.png`, `apple-touch-icon.png`, `favicon-32.png`).

## 회원 앱 탭 구성 (`index.html`)

`오늘 체크` · `21일 달력` · `함께 인증샷` · `채팅` · `오일·제품` 5개 탭이고, 설정(닉네임·시작일·앱 설치 안내·백업·공지)은 상단 톱니바퀴 시트에 있습니다.

- `채팅`: 회원끼리 실시간 응원·소통. 닉네임 미설정 시 입력을 막고 설정을 안내하며, 빈 메시지·공백은 전송되지 않습니다.
- `오일·제품`: CPTG® 아로마오일 소개(레몬 하이라이트) + 이오 메가 리퀴드·포스티엠 공식 특징, 21일 트리플 시너지 루틴, 관리자 설정(`app_settings`)의 상담 버튼과 `@erang_coach` 링크.

## 관리자 페이지 (`admin.html`)

대표님 전용입니다. 회원에게 이 주소를 공유하지 마세요.

- 비밀번호 잠금(로그인 상태는 `sessionStorage`에만 유지, 로그아웃 버튼 있음).
- 전체 요약: 총 참여 회원 / 오늘 3종 완료 인원 / 누적 인증샷 / 21일 완주자 / 평균 달성률.
- 회원별 진행 현황(참여 일수·달성률 바·오늘 3종·마지막 활동), 검색·정렬, 회원별 21일 기록 상세.
- 회원 현황 CSV 내보내기(UTF-8 BOM → 엑셀에서 바로 열림).
- 인증샷 피드 관리: 개별 삭제, 회원(user_key)별 기록 일괄 삭제.
- 채팅 관리: 회원 앱 채팅방 메시지 최근 300개 조회·검색·삭제(실시간 반영).
- 공지 배너 문구·상담 버튼 문구/링크를 저장하면 회원 앱 상단에 실시간 반영(`app_settings`).

## 홈 화면 앱(PWA)

- `manifest.json`: 이름 `21일 트리플챌린지` / 짧은 이름 `트리플21` / `display: standalone` / 테마 `#0d9488` / 배경 `#f4faf7`
- `index.html`이 `sw.js`를 등록하고, 실행 직후 0.9초 스플래시 시작 화면을 보여 줍니다.
- 앱 안 `설정 → 📲 바탕화면 앱으로 추가하기`(또는 오늘 탭 안내 배너)에서 안드로이드 크롬은 바로 설치, 아이폰은 사파리 공유 → 홈 화면에 추가 안내를 봅니다.
- 서비스 워커는 네트워크 우선이라 항상 최신 화면을 먼저 받고, 오프라인일 때만 캐시로 엽니다. (관리자 페이지는 캐시 제외)

## 카카오 로그인 (v3.0)

Supabase Auth 의 **커스텀 OIDC 제공자**(`custom:kakao-oidc`)로 카카오 로그인을 붙였습니다.

- 카카오 디벨로퍼스 앱: `21일 트리플챌린지` (앱 ID 1664351, 회사명 아로마교육원, 카테고리 건강/피트니스)
- 카카오 로그인 ON · OpenID Connect ON · 리다이렉트 URI `https://lfphrvtbpomajgzglbya.supabase.co/auth/v1/callback`
- 동의항목: 닉네임(선택), 프로필 사진(선택). `account_email` 은 비즈 앱 전환 전에는 쓸 수 없습니다.
- Supabase: `custom:kakao-oidc` (Issuer `https://kauth.kakao.com`, scopes `openid,profile_nickname,profile_image`, Allow users without an email ON)
  - Supabase 기본 Kakao 제공자는 `account_email` 스코프를 강제로 붙여 KOE205 오류가 나므로 커스텀 OIDC 제공자를 씁니다.
- 로그인하면 `userKey()` 가 Supabase auth 사용자 id 가 되고, 그 계정의 `checkins` 기록을 내려받아 기기 기록과 합칩니다(기기·서버 중 완료된 쪽 우선). 로그인 직후 `kapi.kakao.com/v1/oidc/userinfo` 로 닉네임·프로필 사진을 받아 초기값으로 채우고 `localStorage` 에 캐시합니다.
- 로그아웃하면 다시 기기 임시 키로 돌아갑니다(기기에 남은 기록은 그대로).

## 링크 미리보기(OG 이미지)

- 카카오톡·SNS에 주소를 붙였을 때 뜨는 썸네일: `og-image.png`(1200×630, `tools/make_og.py`로 재생성).
- `index.html` `<head>`의 `og:title`·`og:description`·`og:image`·`og:image:width/height`와 `twitter:card`로 지정합니다.

## 저장 방식

- **내 체크 기록**은 기기 브라우저(localStorage)에 먼저 저장되어 오프라인에서도 열립니다.
- **인증 기록·소감·인증샷·응원**은 Supabase 서버에 저장되어, 링크를 받은 모든 회원이 `함께 인증샷` 탭에서 실시간으로 함께 봅니다.
- **채팅**은 `chat_messages` 테이블에 저장되고 Supabase Realtime으로 새 메시지가 즉시 표시됩니다(최근 100개).
- 서버 연결이 되지 않으면 자동으로 기기 저장 모드로 동작합니다.

## 서버 (Supabase)

- 프로젝트: `triple-21-challenge` (ref `lfphrvtbpomajgzglbya`, 리전 ap-northeast-2 서울)
- 테이블: `checkins`(user_key·day_no 당 1행, unique 인덱스), `reactions`(checkin_id·reactor_key·kind unique 인덱스), `app_settings`(id='default' 한 행 — 공지·상담 설정), `chat_messages`(id uuid·user_key·nickname·message·created_at, created_at 인덱스)
- 스토리지: 공개 버킷 `shots` — 사진은 `public/<사용자키>/<날짜>-<시각>.jpg` 로 저장
- 실시간: `checkins`, `reactions`, `app_settings`, `chat_messages` 네 표가 `supabase_realtime` 발행에 등록됨 (Realtime + 60초 주기 새로고침)
- 접속 정보는 `index.html`·`admin.html` 안의 상수(URL·publishable 키)에 있습니다.

원본: `documents/triple_21_challenge.html`, `documents/triple_21_challenge_admin.html`
