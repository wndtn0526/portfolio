# 선언 섹션을 Figma 로 넣는 플러그인

웹의 두 번째 섹션(파란 선언 + 오른쪽 소개)을 Figma 캔버스에 **편집 가능한 레이어**로 그린다.
Figma MCP 서버는 읽기만 되고 쓰기가 없어서 이 방법을 쓴다.

## 실행

1. Figma 데스크톱에서 넣을 파일을 연다.
2. 메뉴 **Plugins → Development → Import plugin from manifest…** → 이 폴더의 `manifest.json` 선택.
3. 같은 메뉴에 생긴 **「포트폴리오 · 선언 섹션 넣기」** 를 실행한다.
4. 1440×900 과 2056×1100 프레임 두 개가 생긴다. 끝나면 오른쪽 아래에 쓴 글꼴이 표시된다.

## 값의 출처

`resources/views/home.blade.php` · `resources/css/tokens.css` 를 그대로 옮겼다.
웹을 고치면 여기(`code.js` 의 `T`·`STATEMENT`·`ASIDE`)도 같이 고친다 — 두 곳이다.

⚠️ Pretendard 가 맥에 설치돼 있어야 한다. 없으면 Inter 로 그리고 알림에 표시한다.
