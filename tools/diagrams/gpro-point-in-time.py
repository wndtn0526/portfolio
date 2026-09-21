#!/usr/bin/env python3
"""
그룹웨어프로 · 시점 관리 도식 → public/images/projects/gpro-point-in-time.svg

앞 도식(따로 쓸 때 vs 그룹웨어프로)과 같은 좌우 비교 문법:
  왼쪽  현재 상태만 저장하면 — 발령이 나면 예전 소속이 덮어써져 예전 조직도를 못 꺼내고 발령을 되돌릴 수 없다
  오른쪽 시점 기준으로 저장하면 — 발령마다 행이 하나 더 쌓여, 어느 날짜든 그날의 조직도 · 소속 · 결재선을 꺼내고 발령 정정도 그 행만 고친다

예시 값(구성원 A · 영업1팀 · 경영지원팀 …)은 설명용 가상 데이터다.
색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-point-in-time.py
"""
from pathlib import Path

W, H = 1200, 400
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def box(x, y, w, h, title, sub=None, accent=False, size=16, title_color=None):
    fill, stroke, so = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 0.08)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}" stroke-width="1"/>')
    tc, sc = (WHITE, WHITE) if accent else (title_color or INK, BODY)
    if sub:
        add(f'<text x="{x + 18}" y="{y + h / 2 - 3:.0f}" font-size="{size}" font-weight="600" fill="{tc}">{title}</text>')
        add(f'<text x="{x + 18}" y="{y + h / 2 + 18:.0f}" font-size="13" fill="{sc}" fill-opacity="{0.85 if accent else 1}">{sub}</text>')
    else:
        add(f'<text x="{x + 18}" y="{y + h / 2 + 6:.0f}" font-size="{size}" font-weight="600" fill="{tc}">{title}</text>')

def label(x, y, s, color=MUTED, anchor='start', size=13, weight=600):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')

def arrow(x1, y1, x2, y2):   # 수직 또는 수평
    add(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
    if x1 == x2: pts = f'{x2-5},{y2-9} {x2},{y2} {x2+5},{y2-9}'
    else: pts = f'{x2-9},{y2-5} {x2},{y2} {x2-9},{y2+5}'
    add(f'<polygon points="{pts}" fill="{MUTED}"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ── 왼쪽: 현재 상태만 저장하면 ──
label(40, 66, '현재 상태만 저장하면')
box(40, 84, 400, 60, '구성원 A', '소속: 영업1팀 · 팀원')
arrow(240, 144, 240, 184); label(252, 170, '발령', size=12, weight=500)
box(40, 188, 400, 60, '구성원 A', '소속: 경영지원팀 · 팀장 (영업1팀이었던 기록은 사라짐)')
box(40, 276, 194, 60, '예전 조직도를', '꺼낼 수 없음', size=15)
box(246, 276, 194, 60, '잘못 넣은 발령을', '되돌릴 수 없음', size=15)

# ── 오른쪽: 시점 기준으로 저장하면 ──
add(f'<rect x="520" y="40" width="640" height="320" rx="16" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
label(544, 74, '시점 기준으로 저장하면', color=ACCENT, size=16, weight=700)
rows = [('2022-01-03', '영업1팀 · 팀원'), ('2023-03-01', '영업2팀 · 팀장'), ('2024-07-01', '경영지원팀 · 팀장')]
for i, (d, who) in enumerate(rows):
    y = 92 + i * 60
    add(f'<rect x="544" y="{y}" width="300" height="48" rx="10" fill="{CANVAS}" stroke="#000000" stroke-opacity="0.08"/>')
    add(f'<text x="562" y="{y + 30}" font-size="13" fill="{MUTED}">{d}</text>')
    add(f'<text x="660" y="{y + 30}" font-size="15" font-weight="600" fill="{INK}">{who}</text>')
label(544, 296, '발령마다 행이 하나 더 쌓이고, 예전 행은 그대로 남습니다', size=12, weight=500)
arrow(844, 182, 900, 182)
box(912, 92, 224, 84, '어느 날짜든', '그날의 조직도 · 소속 · 결재선', size=15)
box(912, 200, 224, 84, '발령 정정은', '그 행만 고치고 이력은 남음', size=15)

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-point-in-time.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
