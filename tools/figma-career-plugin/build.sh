#!/usr/bin/env bash
# code.src.js + 프로필 사진(JPEG base64) → code.js. 플러그인은 파일 하나만 읽고 네트워크가 없어서 사진을 코드에 박는다.
set -euo pipefail
cd "$(dirname "$0")"
tmp="$(mktemp -d)"
sips -s format jpeg -s formatOptions 85 ../../public/images/profile.webp --out "$tmp/profile.jpg" >/dev/null
b64="$(base64 -i "$tmp/profile.jpg" | tr -d '\n')"
{ echo "// 생성물 — build.sh 가 code.src.js 에 사진을 박아 만든다. 고칠 땐 code.src.js 를 고친다."; sed "s|__PHOTO_B64__|$b64|" code.src.js; } > code.js
rm -rf "$tmp"
echo "code.js $(wc -c < code.js) bytes"
