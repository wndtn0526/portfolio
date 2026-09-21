#!/usr/bin/env python3
"""
그룹웨어프로 · 「데이터가 따로 논다 vs 인사 데이터가 바뀌면 함께 바뀐다」 도식 → public/images/projects/gpro-one-flow.svg

3. 제품 설계 셋째 단락의 핵심 하나만 보인다(보조 설명 없음, 2026-09-21 사용자 지시):
  왼쪽  따로 쓸 때 — 구성원 정보가 바뀌면 인사 · 근태 · 결재 · 재무 · 커뮤니티 서비스에 각각 다시 입력. 데이터가 서비스마다 따로.
  오른쪽 그룹웨어프로 — 인사 데이터에 한 번 입력하면 근태 · 조직도 · 결재선 · 정산이 자동으로 함께 바뀐다.

색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-one-flow.py
"""
from pathlib import Path

W, H = 1200, 460
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def box(x, y, w, h, title, sub=None, accent=False):
    fill, stroke, so = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 0.08)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}" stroke-width="1"/>')
    tc, sc = (WHITE, WHITE) if accent else (INK, BODY)
    if sub:
        add(f'<text x="{x + 18}" y="{y + h / 2 - 3:.0f}" font-size="16" font-weight="600" fill="{tc}">{title}</text>')
        add(f'<text x="{x + 18}" y="{y + h / 2 + 18:.0f}" font-size="13" fill="{sc}" fill-opacity="{0.85 if accent else 1}">{sub}</text>')
    else:
        add(f'<text x="{x + 18}" y="{y + h / 2 + 6:.0f}" font-size="16" font-weight="600" fill="{tc}">{title}</text>')

def label(x, y, s, color=MUTED, anchor='start', size=13, weight=600):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')

def arrow_down(x, y1, y2, color=MUTED):
    add(f'<path d="M{x} {y1} V{y2}" fill="none" stroke="{color}" stroke-width="1.5"/>')
    add(f'<polygon points="{x-5},{y2-9} {x},{y2} {x+5},{y2-9}" fill="{color}"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ── 왼쪽: 따로 쓸 때 — 데이터가 서비스마다 따로 ──
label(40, 66, '따로 쓸 때')
box(40, 84, 400, 64, '구성원 정보가 바뀌면', '발령 · 입사 · 퇴사')
arrow_down(240, 148, 192)
label(252, 176, '서비스마다 다시 입력', size=12, weight=500)
services = ['인사 서비스', '근태 서비스', '결재 서비스', '재무 서비스', '커뮤니티 서비스']
pos = [(40, 196), (246, 196), (40, 276), (246, 276), (143, 356)]
for name, (x, y) in zip(services, pos):
    box(x, y, 194, 68, name, '자체 구성원 데이터')

# ── 오른쪽: 그룹웨어프로 — 인사 데이터가 바뀌면 함께 바뀐다 ──
add(f'<rect x="520" y="40" width="640" height="380" rx="16" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
label(544, 74, '그룹웨어프로', color=ACCENT, size=16, weight=700)
box(544, 92, 592, 64, '구성원 정보가 바뀌면', '발령 · 입사 · 퇴사')
arrow_down(840, 156, 188)
box(544, 188, 592, 68, '인사 데이터', '구성원 · 조직 · 발령을 한 번 입력', accent=True)
arrow_down(840, 256, 296)
label(852, 282, '자동으로 함께 바뀜', size=12, weight=500)
for i, name in enumerate(['근태', '조직도', '결재선', '정산']):
    box(544 + i * 152, 296, 136, 68, name, '자동 반영')

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-one-flow.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
