#!/usr/bin/env bash
#
# 화면을 정적 HTML 로 뽑아 docs/ 에 넣는다. GitHub Pages 가 docs/ 를 서빙한다.
#
# 포트폴리오는 서버 로직이 없다 — 화면만 있으면 되므로 정적으로 내보낸다.
# 404 저장소의 scripts/export-styleguide.sh 와 같은 방식이다.
#
# 사용: ./scripts/export-static.sh [포트]
#
set -euo pipefail

PORT="${1:-8002}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/docs"
SRC="http://127.0.0.1:${PORT}"

# 뽑을 페이지 — "라우트:출력파일". 출력은 docs/ 바로 아래 평평하게 둔다.
# 하위 디렉터리로 내리면 ./build/ 상대경로가 깨진다.
# 여기 적은 출력파일 이름은 아래 «지워도 되는 것» 목록에도 자동으로 들어간다.
PAGES=(
    ":index.html"
    "mesh-off:mesh-off.html"
)

cd "$ROOT"

# 컴파일된 Blade 캐시를 먼저 비운다. app.css 가 storage/framework/views 를 @source 로
# 스캔하기 때문에, 삭제된 컴포넌트의 낡은 캐시가 남아 있으면 죽은 유틸리티 클래스가
# 그대로 CSS 에 실려 나간다.
echo "▸ 뷰 캐시 정리"
php artisan view:clear

# ⚠️ 프런트 빌드는 호스트에서 돈다. lightningcss(Tailwind 4)가 플랫폼별 네이티브
#    바이너리를 깔기 때문에 컨테이너와 섞어 쓰면 한쪽이 죽는다. README 참고.
echo "▸ 에셋 빌드"
npm run build --silent

echo "▸ 임시 서버 기동 (:${PORT})"
php artisan serve --host=127.0.0.1 --port="$PORT" >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT

for _ in $(seq 1 40); do
    if curl -sf -o /dev/null "${SRC}/"; then break; fi
    sleep 0.5
done

if ! curl -sf -o /dev/null "${SRC}/"; then
    echo "✗ 서버가 뜨지 않았다. .env 의 SESSION_DRIVER/CACHE_STORE 가 file 인지 확인할 것" >&2
    exit 1
fi

# ⚠️ docs/ 는 **이 스크립트가 만든 것만** 들어가는 곳이다. 손으로 쓴 문서는 notes/ 에 둔다.
#    전에 여기서 `rm -rf "$OUT"` 을 하는 바람에 docs/ 에 뒀던 정리 문서가 통째로 날아갔다
#    (스테이징돼 있어서 dangling blob 으로 겨우 건졌다). 그래서 지금은 만든 것만 지우고,
#    모르는 파일이 있으면 지우지 않고 멈춘다.
GENERATED=(".nojekyll" "build" "images")
for page in "${PAGES[@]}"; do GENERATED+=("${page##*:}"); done

if [ -d "$OUT" ]; then
    while IFS= read -r entry; do
        [ -z "$entry" ] && continue
        known=0
        for g in "${GENERATED[@]}"; do [ "$entry" = "$g" ] && known=1 && break; done
        if [ "$known" -eq 0 ]; then
            echo "✗ docs/${entry} 는 이 스크립트가 만든 것이 아니다 — 지우지 않고 멈춘다." >&2
            echo "  손으로 쓴 문서라면 notes/ 로 옮기고 다시 실행할 것." >&2
            exit 1
        fi
    done < <(ls -A "$OUT")

    for g in "${GENERATED[@]}"; do rm -rf "${OUT:?}/${g}"; done
fi
mkdir -p "$OUT"

echo "▸ 에셋 복사"
cp -R "$ROOT/public/build" "$OUT/build"
# 뷰가 asset() 으로 부르는 정적 파일(이미지 등)도 함께 옮긴다.
# 안 옮기면 Pages 에서 404 가 나는데 화면은 조용히 배경만 빠진 채 뜬다.
[ -d "$ROOT/public/images" ] && cp -R "$ROOT/public/images" "$OUT/images"

# 라우트 → 파일 매핑을 파이썬에 그대로 넘긴다(내부 링크 치환에 필요).
MAPPING="$(printf '%s\n' "${PAGES[@]}")"

for page in "${PAGES[@]}"; do
    route="${page%%:*}"
    file="${page##*:}"

    echo "▸ /${route} → docs/${file}"

    if ! curl -sf -o "$OUT/$file" "${SRC}/${route}"; then
        echo "✗ /${route} 를 가져오지 못했다" >&2
        exit 1
    fi

    python3 - "$OUT/$file" "$SRC" "$MAPPING" <<'PY'
import re, sys

path, src, mapping = sys.argv[1], sys.argv[2], sys.argv[3]
html = open(path, encoding='utf-8').read()

# 에셋 절대 URL → 상대 경로 (Pages 는 /<repo>/ 하위에 서빙된다)
html = html.replace(f'{src}/build/', './build/')
html = html.replace(f'{src}/images/', './images/')

# 페이지끼리의 내부 링크도 정적 파일명으로 바꾼다. 안 바꾸면 아래 검사에서 걸린다.
# 긴 라우트부터 치환해야 접두어가 겹칠 때 짧은 쪽이 먼저 먹지 않는다.
pairs = [line.split(':', 1) for line in mapping.splitlines() if line.strip()]
for route, out_file in sorted(pairs, key=lambda p: -len(p[0])):
    if not route:
        continue
    html = html.replace(f'{src}/{route}', f'./{out_file}')

# 루트 링크(로고 등)는 첫 화면으로 보낸다. Pages 루트가 곧 index.html 이다.
html = html.replace(f'"{src}/"', '"./index.html"').replace(f'"{src}"', '"./index.html"')

# Livewire 런타임은 정적 페이지에 없다. Alpine 만 CDN 으로 대체한다.
html = re.sub(r'<script[^>]*livewire[^>]*></script>', '', html, flags=re.I)
html = html.replace(
    '</head>',
    '    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js"></script>\n'
    '</head>',
)

# 남은 절대 URL 이 있으면 빌드를 실패시킨다 (조용히 깨진 링크가 나가는 것보다 낫다)
leftover = re.findall(re.escape(src) + r'[^"\']*', html)
if leftover:
    sys.exit(f'✗ 상대 경로로 못 바꾼 URL 이 남았다: {sorted(set(leftover))[:5]}')

open(path, 'w', encoding='utf-8').write(html)
print(f'  {len(html):,}자')
PY
done

# Jekyll 이 _ 로 시작하는 파일을 무시하지 않도록
touch "$OUT/.nojekyll"

echo "✓ docs/ 생성 완료 — GitHub Pages 소스를 main 브랜치 /docs 로 설정하면 서빙된다"
