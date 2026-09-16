# 이력 섹션을 Figma 로 넣는 플러그인

웹의 이력 섹션(`#career` — 사진+소개, 경력·학력 행 목록, 프로필·기술)을 Figma 캔버스에
**편집 가능한 auto-layout 레이어**로 그린다. Figma MCP 서버는 읽기만 되고 쓰기가 없어서 이 방법을 쓴다.

## 실행

1. `./build.sh` — `code.src.js` 에 프로필 사진(JPEG base64)을 박아 `code.js` 를 만든다(저장소에 들어 있으니 사진·소스를 안 고쳤으면 건너뛴다).
2. Figma 데스크톱에서 넣을 파일을 연다.
3. 메뉴 **Plugins → Development → Import plugin from manifest…** → 이 폴더의 `manifest.json` 선택.
4. 같은 메뉴에 생긴 **「포트폴리오 · 이력 섹션 넣기」** 를 실행한다.
5. 1440 과 2056 폭 프레임 두 개가 생긴다(높이는 내용에 따라 자동).

## 값의 출처

`resources/views/home.blade.php` · `resources/css/tokens.css` 를 1440/2056 폭에서 실측해 옮겼다.
웹을 고치면 `code.src.js` 의 `T`·`INTRO`·`CAREER`·`EDU`·`PROFILE`·`SKILLS` 도 같이 고치고 `./build.sh` 를 다시 돈다 — 두 곳이다.

⚠️ Pretendard(Regular/Medium/SemiBold/Bold)가 맥에 설치돼 있어야 한다. 없으면 Inter 로 그리고 알림에 표시한다.
⚠️ `code.js` 는 생성물이다. 직접 고치지 않는다.
