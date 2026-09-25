# 포트폴리오 · Figma 작업

Figma 데스크톱에서 도는 개발용 플러그인이다. 코드는 고정이고, 할 일은 로컬 서버가 내주는 작업(JSON)이 정한다.

- **내보내기** 기존 노드를 PNG 2배로 받는다. Dev Mode MCP 의 `get_screenshot` 은 긴 변 1024px 까지라 덱 슬라이드를 웹에 쓸 만큼 선명하게 못 받는다.
- **그리기** 상자 · 글 · 벡터(SVG)로 도식을 그려 페이지에 놓고, 바로 PNG 2배로 내보낸다. 03 주 52시간 플로우차트가 이렇게 나왔다.

## 쓰는 법

1. 서버를 켠다.

   ```bash
   python3 tools/figma-export-plugin/server.py <PNG 저장 폴더> <작업 JSON 경로>
   ```

   `GET /task` 로 작업을 내주고, `POST /save?name=<이름>` 으로 받은 PNG 를 `<이름>.png` 로 저장한다. 127.0.0.1 과 ::1 의 8899 만 듣는다.
2. 작업 JSON 을 쓴다. 형식은 `code.js` 머리 주석에 있다. 예: `python3 tools/figma-export-plugin/tasks/overtime-52h.py <작업 JSON 경로>`
3. 작업의 `file` 과 같은 파일을 Figma 에서 연다. 다른 파일이면 플러그인이 알림만 띄우고 멈춘다.
4. 플러그인 › 개발 › **포트폴리오 · Figma 작업** 을 누른다. 끝나면 작업 JSON 을 `{}` 로 비워 둔다.

자동화할 때는 `open figma://file/<파일 키>` 로 탭을 열고 osascript 로 메뉴를 누른다(손쉬운 사용 권한 필요).
개발용 플러그인은 실행할 때마다 `code.js` 를 새로 읽는다. 「핫 리로드 플러그인」 은 켜고 끄는 토글이라 누를 필요가 없다.

## 등록

`~/Library/Application Support/Figma/settings.json` 의 `localFileExtensions` 에 id 7(manifest) · 8(code) 로 등록돼 있다.
`networkAccess` 는 `devAllowedDomains: ["http://localhost:8899"]` 여야 한다. `127.0.0.1` 로 적으면 매니페스트 오류(⚠)가 난다.

## 작업 목록

| 작업 | 파일 | 결과 |
| --- | --- | --- |
| `tasks/overtime-52h.py` | 포트폴리오_MCP · 플로우차트 페이지 | `gpro-overtime-flow` · `gpro-holiday-flow` |

그린 플로우차트는 덱 슬라이드 08 의 플로우차트 부품(시작끝 · 텍스트 박스 · 선택지 · 기본 연결선 · 박스 코멘트)과 같은 색 · 치수 · 벡터를 쓴다. 값은 작업 파일 머리 주석에 있다.
Figma 에서 손본 뒤에는 `export` 에 그 프레임 id 를 넣어 다시 내보내면 된다.

## 함께 쓰는 것

- `tools/figma-mcp.sh` Dev Mode MCP(127.0.0.1:3845)를 부르는 셸. 지금 활성 탭의 파일을 읽는다.
