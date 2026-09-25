#!/usr/bin/env bash
# 작업 한 번 돌리기 — Figma 탭을 열고, 플러그인을 누르고, PNG 가 다 올 때까지 기다린 뒤, 작업을 비우고 원래 탭(GPRO_PORTFOLIO)으로 돌아간다.
#   run.sh <작업 JSON> <PNG 폴더>
# 작업의 file(파일 이름) 로 탭을 고른다. 서버(server.py)는 먼저 켜 둔다. macOS 손쉬운 사용 권한이 필요하다.
set -euo pipefail
TASK="$1"; OUT="$2"
key() { case "$1" in 포트폴리오_MCP) echo fAhUR1W7RM9YVXmiSUb6b1;; GPRO_PORTFOLIO) echo sJC6AduTG0I4cTttQJFAes;; *) echo "";; esac; }   # macOS bash 3.2 — 연관 배열 없음
FILE=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('file',''))" "$TASK")
NAMES=$(python3 -c "import json,sys; t=json.load(open(sys.argv[1])); print(' '.join([d['export'] for d in t.get('draw',[]) if d.get('export')] + [n for _,n in t.get('export',[])]))" "$TASK")
[ -n "$(key "$FILE")" ] || { echo "✗ 모르는 파일: $FILE" >&2; exit 1; }

switch() {  # 탭 전환 — 창 제목으로 확인하고, 안 바뀌면 한 번 더
  for i in 1 2 3; do
    open "figma://file/$(key "$1")"; sleep 5
    t=$(osascript -e 'tell application "System Events" to tell process "Figma" to return name of window 1')
    [[ "$t" == *"$1"* ]] && return 0
  done
  echo "✗ $1 탭으로 못 옮겼다(지금: $t)" >&2; return 1
}

for n in $NAMES; do rm -f "$OUT/$n.png"; done
switch "$FILE"
osascript <<'AS'
tell application "System Events"
  tell process "Figma"
    set frontmost to true
    delay 1
    set m to menu 1 of menu item "개발" of menu 1 of menu bar item "플러그인" of menu bar 1
    set names to name of every menu item of m
    repeat with i from 1 to count of names
      set n to item i of names
      if n is not missing value then
        if (n as string) contains "Figma 작업" then
          click menu item i of m
          return
        end if
      end if
    end repeat
    error "플러그인 메뉴를 못 찾았다"
  end tell
end tell
AS
left="$NAMES"
for i in $(seq 1 40); do
  sleep 3; left=""
  for n in $NAMES; do [ -f "$OUT/$n.png" ] || left="$left $n"; done
  [ -z "$left" ] && break
done
echo '{}' > "$TASK"
switch GPRO_PORTFOLIO || true
[ -z "$left" ] && echo "✓ 받음: $NAMES" || { echo "✗ 못 받음:$left" >&2; exit 1; }
