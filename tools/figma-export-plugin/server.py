#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
포트폴리오 Figma 플러그인(tools/figma-export-plugin)의 로컬 짝 — 작업을 내주고, 내보낸 PNG 를 받는다.

  GET  /task              → TASK 파일(JSON) 내용. 플러그인이 실행될 때 가장 먼저 읽는다.
  POST /save?name=<이름>   → 본문(PNG)을 OUT/<이름>.png 로 저장.

사용: python3 tools/figma-export-plugin/server.py <OUT 폴더> <TASK 파일>
  127.0.0.1 과 ::1 두 곳에서 8899 를 듣는다 — Figma 는 localhost 를 ::1 로 먼저 푼다. 루프백만 열고 바깥에는 열지 않는다.
"""
import http.server, socket, sys, threading, urllib.parse, pathlib

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
TASK = pathlib.Path(sys.argv[2])
PORT = 8899

class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        if urllib.parse.urlparse(self.path).path != '/task':
            self.send_response(404); self._cors(); self.end_headers(); return
        body = TASK.read_bytes() if TASK.exists() else b'{}'
        self.send_response(200); self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8'); self.end_headers(); self.wfile.write(body)
        sys.stderr.write(f'task {len(body)} bytes\n'); sys.stderr.flush()
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = ''.join(ch for ch in q.get('name', ['x'])[0] if ch.isalnum() or ch in '-_') or 'x'
        n = int(self.headers.get('Content-Length', 0)); data = self.rfile.read(n)
        (OUT / (name + '.png')).write_bytes(data)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b'ok')
        sys.stderr.write(f'saved {name} {n}\n'); sys.stderr.flush()
    def log_message(self, *a): pass

class S6(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6

servers = [http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H), S6(('::1', PORT), H)]
for s in servers[1:]: threading.Thread(target=s.serve_forever, daemon=True).start()
sys.stderr.write(f'듣는 중 :{PORT} → {OUT} · 작업 {TASK}\n'); sys.stderr.flush()
servers[0].serve_forever()
