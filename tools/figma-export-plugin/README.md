# 포트폴리오 · 원본 2배 내보내기

Dev Mode MCP 의 `get_screenshot` 은 긴 변 1024px 까지만 준다. 덱 슬라이드(1920×1080)나 서비스 화면을 웹에 넣을 만큼 선명하게 받으려고 만든 우회로다.

## 쓰는 법

1. 수신 서버를 켠다 — `python3 scratchpad/hires_server.py <저장 폴더>` (127.0.0.1:8899, IPv6 는 `hires_server6.py`). POST `/save?name=<이름>` 본문을 `<이름>.png` 로 저장한다.
2. Figma 데스크톱에서 GPRO_PORTFOLIO 를 연다(`open figma://file/sJC6AduTG0I4cTttQJFAes`).
3. 플러그인 › 개발 › **포트폴리오 · 원본 2배 내보내기** 를 누른다. `code.js` 의 `JOBS`(노드 id · 파일명) 를 PNG 2x 로 내보내 서버에 보낸다.

`~/Library/Application Support/Figma/settings.json` 의 `localFileExtensions` 에 id 7(manifest) · 8(code) 로 등록돼 있다.
`networkAccess` 는 `devAllowedDomains: ["http://localhost:8899"]` — `127.0.0.1` 로 적으면 매니페스트 오류(⚠) 가 난다.

## 지금 JOBS

슬라이드 04~17(`s04`~`s17`) · 홈 `1002:10984`(`gpro-home`) · 인사 관리 `1002:263292`(`gpro-hr-list`).
다른 노드가 필요하면 `JOBS` 에 추가하고 플러그인 › 개발 › 핫 리로드 플러그인 뒤 다시 실행한다.

내보낸 PNG 를 자르는 스크립트는 세션 스크래치패드 `hires_crops.py`(PIL). 슬라이드 좌표 × 2 가 PNG 좌표다.
