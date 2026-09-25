# 포트폴리오 · Figma 작업

Figma 데스크톱에서 도는 개발용 플러그인이다. 코드는 고정이고, 할 일은 로컬 서버가 내주는 작업(JSON)이 정한다.

- **내보내기** 기존 노드를 PNG 2배로 받는다. Dev Mode MCP 의 `get_screenshot` 은 긴 변 1024px 까지라 덱 슬라이드를 웹에 쓸 만큼 선명하게 못 받는다.
- **그리기** 상자 · 막대 · 글 · 선 · 말풍선 · 벡터(SVG)로 도식을 그려 페이지에 놓고, 바로 PNG 2배로 내보낸다. 03 주 52시간 플로우차트와 결과 그래프가 이렇게 나왔다.

## 쓰는 법

1. 서버를 켠다.

   ```bash
   python3 tools/figma-export-plugin/server.py <PNG 저장 폴더> <작업 JSON 경로>
   ```

   `GET /task` 로 작업을 내주고, `POST /save?name=<이름>` 으로 받은 PNG 를 `<이름>.png` 로 저장한다. 127.0.0.1 과 ::1 의 8899 만 듣는다.
2. 작업 JSON 을 쓴다. 형식은 `code.js` 머리 주석에 있다. 예: `python3 tools/figma-export-plugin/tasks/overtime-52h.py <작업 JSON 경로>`
3. 작업의 `file` 과 같은 파일을 Figma 에서 연다. 다른 파일이면 플러그인이 알림만 띄우고 멈춘다.
4. 플러그인 › 개발 › **포트폴리오 · Figma 작업** 을 누른다. 끝나면 작업 JSON 을 `{}` 로 비워 둔다.

3~4 는 `run.sh <작업 JSON> <PNG 폴더>` 가 한 번에 한다. 작업의 파일 탭을 열어 창 제목으로 확인하고, 메뉴를 누르고, PNG 가 다 오면 작업을 비운 뒤 GPRO_PORTFOLIO 탭으로 돌아간다.
탭 전환(`open figma://file/<키>`)은 가끔 안 먹어서 창 제목을 보고 다시 시도한다. osascript 에 손쉬운 사용 권한이 필요하다.
개발용 플러그인은 실행할 때마다 `code.js` 를 새로 읽는다. 「핫 리로드 플러그인」 은 켜고 끄는 토글이라 누를 필요가 없다.

## 등록

`~/Library/Application Support/Figma/settings.json` 의 `localFileExtensions` 에 id 7(manifest) · 8(code) 로 등록돼 있다.
`networkAccess` 는 `devAllowedDomains: ["http://localhost:8899"]` 여야 한다. `127.0.0.1` 로 적으면 매니페스트 오류(⚠)가 난다.

## 작업 목록

| 작업 | 파일 | 결과 |
| --- | --- | --- |
| `tasks/overtime-52h.py` | 포트폴리오_MCP · 03 주 52시간 페이지 | `gpro-overtime-flow` · `gpro-holiday-flow` · `gpro-overtime-metrics` |

플로우차트는 덱 슬라이드 08 의 플로우차트 부품(시작끝 · 텍스트 박스 · 선택지 · 기본 연결선 · 박스 코멘트), 결과 그래프는 덱 16 의 「정량적 변화 그래프」 와 같은 색 · 치수 · 벡터를 쓴다. 값은 작업 파일 주석에 있다.
Figma 에서 손본 뒤에는 `export` 에 그 프레임 id 를 넣어 다시 내보내면 된다.

## 함께 쓰는 것

- `tools/figma-mcp.sh` Dev Mode MCP(127.0.0.1:3845)를 부르는 셸. 지금 활성 탭의 파일을 읽는다.
