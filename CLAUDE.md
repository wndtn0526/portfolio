# CLAUDE.md

포트폴리오 사이트. Figma 에 만들어 둔 포트폴리오 디자인을 웹으로 옮긴다.
스택·실행·배포는 README.md 에 있다.

## 이 저장소가 담을 것

지금까지 한 작업을 케이스 스터디로 싣는다. 무엇을 어디까지 실을지는 아직 정리 중이다.

| 대상 | 저장소 | 상태 |
| --- | --- | --- |
| GPRO 전자결재 | `wndtn0526/404` (로컬 `../404`) | 화면 33개 · DS 컴포넌트 47개 완성 · Pages 배포 중 |
| 청담원 재가 돌봄 플랫폼 | `gguleHub/cheongdamwon-platform` | **대표 화면 재현까지** 싣기로 함 |

⚠️ **청담원은 회사 private 저장소다.**
- 해당 저장소 CLAUDE.md 에 "커밋·푸시는 직접 하지 말 것" 이 적혀 있다. **읽기만 한다.**
- 로컬 클론(`../cheongdamwon-platform`)은 **2026-07-23 에서 멈춰 있다.**
  실제 작업은 2026-09-10 까지 이어졌고 그 최신본은 별도 Windows 머신에 있다.
  `gh` 토큰으로는 원격 접근이 안 된다(404). 최신 상태를 보려면 그 머신에서 가져와야 한다.
- 회사 코드·디자인을 그대로 옮기지 않는다. 재현물은 다시 그린 것만 싣는다.

## 규칙

- **뷰에 raw hex 를 쓰지 않는다.** 디자인 토큰이 생기면 토큰 유틸리티로만 쓴다.
- ⚠️ Tailwind 는 파일 내용을 문자열로 훑는다. `bg-{$token}` 처럼 런타임에 클래스명을
  조립하면 CSS 가 생성되지 않는다. 배열엔 완성된 클래스명(`'bg-primary'`)을 담는다.
- ⚠️ **폰트를 `app.css` 안에서 `@import url(...)` 로 걸지 않는다.** Tailwind 4 가
  `'tailwindcss'` 를 먼저 인라인해서 그 `@import` 가 규칙들 뒤로 밀리고, lightningcss 가
  "@import 는 규칙보다 앞서야 한다"며 **조용히 잘라낸다** — 빌드는 성공하는데 폰트만 안 걸린다.
  (404 저장소가 지금 이 상태다.) 레이아웃 `<head>` 의 `<link>` 로 건다.
- ⚠️ **`display` 유틸이 이미 붙은 요소에 `hidden` 을 토글하면 안 먹는다.** `hidden` 도
  `display` 유틸이라 `inline-flex`·`flex` 와 자리를 다투고 정적 클래스가 이긴다.
  `x-bind:class="열림 ? 'inline-flex' : 'hidden'"` 처럼 display 자체를 바꾼다.
- ⚠️ **템플릿 어디에든 `<x-…>` 를 글자로 적지 않는다.** 주석이든 속성값 안 문자열이든
  Blade 컴파일러가 훑어서 짝 없는 여는 태그가 된다. 태그 이름만 적는다(`x-table`).
- 익명 Blade 컴포넌트는 `resources/views/components/` 밑에 둔다.
  레이아웃도 컴포넌트다 — `components/layouts/app.blade.php` → `<x-layouts.app>`.
- 새 화면을 만들면 `scripts/export-static.sh` 의 `PAGES` 배열에도 넣는다.
  안 넣으면 Pages 에 올라가지 않는다.
- 커밋 전 `vendor/bin/pint` 로 포맷을 맞춘다.
