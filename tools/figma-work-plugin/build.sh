#!/usr/bin/env bash
# code.src.js + 프로젝트 데이터(resources/data/projects.php → JSON) + 홈 화면 그림(PNG base64) → code.js
# 플러그인은 파일 하나만 읽고 네트워크가 없어서 전부 코드에 박는다. 데이터는 웹과 같은 파일에서 나오므로 두 곳을 따로 고치지 않는다.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
tmp="$(mktemp -d)"
php -r 'echo json_encode(require $argv[1], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);' "$ROOT/resources/data/projects.php" > "$tmp/data.json"
dwebp -quiet "$ROOT/public/images/projects/gpro-home.webp" -o "$tmp/gpro-home.png"
b64="$(base64 -i "$tmp/gpro-home.png" | tr -d '\n')"
# 도식 SVG — public/images/projects/*.svg 를 {경로: 문자열} 로
python3 - "$ROOT/public/images/projects" > "$tmp/diagrams.json" <<'PY'
import json,sys,pathlib
d=pathlib.Path(sys.argv[1]); print(json.dumps({f"images/projects/{p.name}": p.read_text() for p in sorted(d.glob("*.svg"))}, ensure_ascii=False))
PY
{
  echo "// 생성물 — build.sh 가 code.src.js 에 데이터(projects.php)와 그림을 박아 만든다. 고칠 땐 code.src.js 를 고친다."
  python3 - "$tmp/data.json" "$b64" code.src.js "$tmp/diagrams.json" <<'PY'
import sys
data=open(sys.argv[1]).read().strip(); b64=sys.argv[2]; src=open(sys.argv[3]).read(); diagrams=open(sys.argv[4]).read().strip()
print(src.replace('__DATA_JSON__', data).replace('__PHOTO_B64__', b64).replace('__DIAGRAMS_JSON__', diagrams), end='')
PY
} > code.js
rm -rf "$tmp"
echo "code.js $(wc -c < code.js | tr -d ' ') bytes"
