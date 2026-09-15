# portfolio

포트폴리오 사이트. Figma 에 만들어 둔 디자인을 웹으로 옮긴다.

## 스택

| 레이어 | 선택 |
| --- | --- |
| 백엔드 | Laravel 13 / PHP 8.5 |
| 프론트 | Livewire 4 + Alpine.js + Tailwind CSS 4 (Vite) |
| 배포 | 정적 HTML export → GitHub Pages (`docs/`) |

DB 는 쓰지 않는다. 세션·캐시는 파일, 큐는 sync 다 — 화면만 있으면 되는 사이트라
`php artisan serve` 하나로 돌아가고 Docker 가 필요 없다.

## 실행

```bash
composer install
cp .env.example .env && php artisan key:generate
npm install
npm run dev          # 개발 서버 (Vite)
php artisan serve    # http://localhost:8000
```

⚠️ **프런트 빌드는 호스트에서 돌린다.** lightningcss(Tailwind 4 가 쓴다)가 플랫폼별
네이티브 바이너리를 깔기 때문에, 호스트와 컨테이너에서 번갈아 `npm install` 하면
한쪽이 `Cannot find module '../lightningcss.*.node'` 로 죽는다. 한쪽에서만 돌린다.

## 정적 배포

```bash
./scripts/export-static.sh
```

화면을 정적 HTML 로 뽑아 `docs/` 에 넣는다. GitHub Pages 소스를 `main` 브랜치 `/docs`
로 설정하면 서빙된다. 새 화면을 추가하면 스크립트 안 `PAGES` 배열에도 넣어야 한다.

## 아직 안 된 것

- **디자인 토큰이 없다.** Figma 포트폴리오 디자인을 읽어 오면 `resources/css/tokens.css`
  를 만들어 `app.css` 에서 `@import` 한다 (404 저장소와 같은 2계층 구조).
- 첫 화면(`resources/views/home.blade.php`)은 빌드 확인용 껍데기다. 통째로 갈아엎는다.
- 담을 내용(케이스 스터디)은 아직 정리 중이다.
