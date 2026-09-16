# 프로젝트 섹션을 Figma 로 넣는 플러그인

웹의 프로젝트 섹션(`#work` — 회사 탭 · 왼쪽 목록 · 오른쪽 아티클)을 Figma 캔버스에
**편집 가능한 auto-layout 레이어**로 그린다. Figma MCP 서버는 읽기만 되고 쓰기가 없어서 이 방법을 쓴다.

## 실행

1. `./build.sh` — `resources/data/projects.php` 를 JSON 으로, 홈 화면 그림을 PNG base64 로 박아 `code.js` 를 만든다
   (저장소에 들어 있으니 데이터 · 그림 · 소스를 안 고쳤으면 건너뛴다). `php` · `dwebp` 가 필요하다.
2. Figma 데스크톱에서 넣을 파일을 연다.
3. 메뉴 **Plugins → Development → Import plugin from manifest…** → 이 폴더의 `manifest.json` 선택.
4. 같은 메뉴에 생긴 **「포트폴리오 · 프로젝트 섹션 넣기」** 를 실행한다.
5. 1440 과 2056 폭 프레임 두 개가 생긴다(높이는 내용 따라 자동). 그룹웨어프로 탭 · 첫 프로젝트가 열린 상태다.

다른 회사 · 프로젝트를 그리려면 `code.src.js` 의 `SCREENS[*].company / project` 를 slug 로 바꾸고 `./build.sh` 를 다시 돈다.

## 값의 출처

내용은 웹과 같은 `resources/data/projects.php` 에서 빌드 때 읽는다 — 두 곳을 따로 고치지 않는다.
치수 · 글자는 `home.blade.php` · `app.css`(.project-tab) · `tokens.css` 를 1440/2056 폭으로 계산한 것이다(`code.src.js` 머리 주석).

⚠️ Pretendard(Regular/Medium/SemiBold/Bold)가 맥에 설치돼 있어야 한다. 없으면 Inter 로 그리고 알림에 표시한다.
⚠️ `code.js` 는 생성물이다. 직접 고치지 않는다.
⚠️ 그림은 지금 MCP 캡처(1024)라 흐리다. 원본을 `public/images/projects/gpro-home.webp` 에 넣고 다시 빌드하면 같이 바뀐다.
