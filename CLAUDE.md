# CLAUDE.md

포트폴리오 사이트. Figma 에 만들어 둔 포트폴리오 디자인을 웹으로 옮긴다.
스택·실행·배포는 README.md 에 있다.

## 이 저장소가 담을 것

지금까지 한 작업을 케이스 스터디로 싣는다. 무엇을 어디까지 실을지는 아직 정리 중이다.

| 대상 | 저장소 | 상태 |
| --- | --- | --- |
| GPRO 전자결재 | `wndtn0526/404` (로컬 `../404`) | 화면 33개 · DS 컴포넌트 47개 완성 · Pages 배포 중 |
| 청담원 재가 돌봄 플랫폼 | 로컬 `~/cheongdamwon-platform` | **대표 화면 재현까지** 싣기로 함 |

⚠️ **청담원은 회사 private 저장소다.**
- 해당 저장소 CLAUDE.md 에 "커밋·푸시는 직접 하지 말 것" 이 적혀 있다. **읽기만 한다.**
- 회사 코드·디자인을 그대로 옮기지 않는다. 재현물은 다시 그린 것만 싣는다.

⚠️ **읽을 클론은 `~/cheongdamwon-platform` 이다. `~/Documents/GitHub/cheongdamwon-platform`
   이 아니다.** GitHub 폴더 밑에도 같은 이름의 클론이 있는데 그건 2026-07-23 에서 멈춘
   낡은 것이라, 그걸 읽으면 8~9월 작업이 통째로 빠진다. 홈 디렉터리 쪽이 정본이다.

| | `~/cheongdamwon-platform` (정본) | `~/Documents/GitHub/…` (낡음) |
| --- | --- | --- |
| 마지막 커밋 | 2026-09-10 | 2026-07-23 |
| 전체 커밋 | 1158 | 292 |
| 본인 커밋 | 261 | 79 |

⚠️ **원격은 더 이상 못 읽는다.** `gh` 토큰으로 `gguleHub/cheongdamwon-platform` 이 404 다
   (SSO 거부가 아니라 접근 자체가 없음 — `X-GitHub-SSO` 헤더가 안 온다).
   `gguleHub` 는 조직이 아니라 개인 계정이다. 그러니 `git fetch` 로 최신화할 수 없고,
   위 로컬 클론이 가진 것이 전부다.

⚠️ **청담원 기획 문서는 Confluence 에 있다.** 저장소만 보면 「구현만 한 프로젝트」로 잘못 읽는다.
   실제로는 전략 판단 · IA · 기능정의 · DB 설계 · 도메인 매핑까지 본인이 했다.

| | |
| --- | --- |
| 사이트 | `cheongdamwon-platform.atlassian.net` |
| cloudId | `632b05fe-e945-49b2-b469-f1a3c63b341e` |
| 스페이스 | 「청담원 프로젝트」 — key `MFS`, alias `CDW` (CQL 은 `space = CDW`) |
| 본인 작성 문서 | 97개 (Confluence 계정명 **Jake** = wndtn0526@gmail.com) |

Atlassian MCP 로 읽는다. ⚠️ 검색 결과가 커서 토큰 한도를 넘기니 `limit` 을 낮추거나
저장된 결과 파일을 python 으로 파싱해 제목만 추린다.

⚠️ **Figma 는 데스크톱 앱의 Dev Mode MCP 서버(`127.0.0.1:3845/mcp`)로 읽는다.**
   그런데 그 서버는 `~/cheongdamwon-platform` 프로젝트에만 등록돼 있어서 이 저장소에서는
   MCP 도구로 안 잡힌다. `~/.claude.json` 의 이 프로젝트 `mcpServers` 에
   `{"figma-dev": {"type": "http", "url": "http://127.0.0.1:3845/mcp"}}` 를 넣고 세션을 다시 열면
   정식으로 붙는다. 급하면 curl 로 JSON-RPC 를 직접 쳐도 된다(세션 헤더 `mcp-session-id` 필요).
   포트폴리오 시안: 같은 파일의 `PORTFOLIO` 페이지 `1083:279330` · 17슬라이드 · 1920x1080.

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
- ⚠️ **`docs/` 는 export 스크립트가 만든 것만 들어가는 곳이다.** 손으로 쓴 문서는 `notes/` 에 둔다.
  전에 `docs/` 에 정리 문서를 뒀다가 스크립트의 `rm -rf` 에 통째로 날아갔다.
  지금은 스크립트가 모르는 파일을 보면 지우지 않고 멈추지만, 애초에 넣지 않는 게 맞다.
- 커밋 전 `vendor/bin/pint` 로 포맷을 맞춘다.
