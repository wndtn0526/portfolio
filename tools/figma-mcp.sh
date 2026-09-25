#!/usr/bin/env bash
# Figma Dev Mode MCP 서버(데스크톱 앱이 띄우는 127.0.0.1:3845)를 HTTP 로 직접 부른다 — 읽기 전용 도구 6개.
#   tools/figma-mcp.sh init | tools | call <도구 이름> <JSON 인자>
# ⚠️ 데스크톱 앱에서 지금 열려 있는(활성 탭) 파일을 읽는다. 다른 파일 노드를 읽으려면 그 파일 탭을 먼저 연다.
# ⚠️ get_screenshot 은 긴 변 1024px 까지만 준다 — 선명한 그림은 tools/figma-export-plugin 으로 받는다.
set -euo pipefail
URL=http://127.0.0.1:3845/mcp
SID_FILE="${FIGMA_SID_FILE:-${TMPDIR:-/tmp}/figma-mcp.sid}"
post() { curl -s -X POST "$URL" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' ${2:+-H "$2"} --max-time 90 -d "$1"; }
unsse() { grep '^data: ' | sed 's/^data: //'; }
case "${1:-}" in
  init)
    hdr=$(mktemp)
    curl -s -D "$hdr" -o /dev/null -X POST "$URL" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
      -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"claude-code","version":"1.0"}}}'
    sid=$(grep -i '^mcp-session-id:' "$hdr" | tr -d '\r' | awk '{print $2}'); rm -f "$hdr"
    [ -n "$sid" ] || { echo "✗ 세션 id 를 못 받았다 — Figma 데스크톱 · Dev Mode MCP 서버가 켜져 있는지 확인" >&2; exit 1; }
    echo "$sid" > "$SID_FILE"
    post '{"jsonrpc":"2.0","method":"notifications/initialized"}' "mcp-session-id: $sid" >/dev/null
    echo "세션: $sid" ;;
  tools) post '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' "mcp-session-id: $(cat "$SID_FILE")" | unsse ;;
  call)
    [ -s "$SID_FILE" ] || "$0" init >/dev/null
    name="$2"; args="${3:-{\}}"
    out=$(post "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":$args}}" "mcp-session-id: $(cat "$SID_FILE")" | unsse || true)
    if [ -z "$out" ]; then "$0" init >/dev/null; out=$(post "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":$args}}" "mcp-session-id: $(cat "$SID_FILE")" | unsse); fi
    echo "$out" ;;
  *) echo "사용: tools/figma-mcp.sh init|tools|call <이름> <JSON>" >&2; exit 1;;
esac
