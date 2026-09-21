#!/usr/bin/env python3
"""
그룹웨어프로 · 「따로 쓸 때 vs 하나로」 도식 → public/images/projects/gpro-one-flow.svg

3. 제품 설계 셋째 단락을 그림으로 옮긴 것:
  왼쪽  따로 쓸 때 — 인사 · 근태 · 결재 · 재무 · 커뮤니티 · 칸반 서비스마다 조직도 · 결재 · 알림이 따로 → 구성원은 같은 정보를 여러 번 입력
  오른쪽 그룹웨어프로 하나 — 조직도 · 결재 · 알림은 제품에 하나씩. 인사 데이터에서 근태 → 결재 → 재무(정산)로 한 번 입력한 정보가 이어지고,
         구성원 정보가 바뀌면 결재선과 정산도 함께 바뀐다. 커뮤니티 · 칸반은 같은 조직도 · 알림 위에.

색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-one-flow.py
"""
from pathlib import Path

W, H = 1200, 560
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def box(x, y, w, h, title, subs=(), accent=False, title_size=17):
    fill, stroke, so = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 0.08)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}" stroke-width="1"/>')
    tc, sc = (WHITE, WHITE) if accent else (INK, BODY)
    block = 20 + 22 * len(subs)
    ty = y + (h - block) / 2 + 16
    add(f'<text x="{x + 20}" y="{ty:.0f}" font-size="{title_size}" font-weight="600" fill="{tc}">{title}</text>')
    for i, s in enumerate(subs):
        add(f'<text x="{x + 20}" y="{ty + 22 * (i + 1):.0f}" font-size="14" fill="{sc}" fill-opacity="{0.85 if accent else 1}">{s}</text>')

def chip(x, y, w, s, dim=False):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{WHITE}" stroke="#000000" stroke-opacity="0.08"/>')
    add(f'<text x="{x + w / 2}" y="{y + 16}" font-size="12" font-weight="600" fill="{MUTED if dim else BODY}" text-anchor="middle">{s}</text>')

def label(x, y, s, color=MUTED, anchor='start', size=13, weight=600):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')

def path(d, dashed=False, color=MUTED):
    dash = ' stroke-dasharray="4 4"' if dashed else ''
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{dash}/>')

def head(x, y, dir, color=MUTED):
    if dir == 'r': pts = f'{x-9},{y-5} {x},{y} {x-9},{y+5}'
    if dir == 'd': pts = f'{x-5},{y-9} {x},{y} {x+5},{y-9}'
    if dir == 'u': pts = f'{x-5},{y+9} {x},{y} {x+5},{y+9}'
    add(f'<polygon points="{pts}" fill="{color}"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ── 왼쪽: 따로 쓸 때 ──
label(40, 64, '따로 쓸 때')
services = ['인사', '근태', '결재', '재무', '커뮤니티', '칸반']
for i, name in enumerate(services):
    cx = 40 + (i % 3) * 138
    cy = 84 + (i // 3) * 124
    add(f'<rect x="{cx}" y="{cy}" width="124" height="108" rx="12" fill="{CANVAS}" stroke="#000000" stroke-opacity="0.08"/>')
    add(f'<text x="{cx + 14}" y="{cy + 26}" font-size="15" font-weight="600" fill="{INK}">{name} 서비스</text>')
    for k, c in enumerate(['조직도', '결재', '알림']):
        chip(cx + 14, cy + 38 + k * 22, 96, c, dim=True) if False else add(
            f'<rect x="{cx + 14}" y="{cy + 38 + k * 22}" width="96" height="18" rx="9" fill="{WHITE}" stroke="#000000" stroke-opacity="0.08"/>'
            f'<text x="{cx + 62}" y="{cy + 51 + k * 22}" font-size="11" font-weight="600" fill="{MUTED}" text-anchor="middle">{c}</text>')
label(40, 352, '조직도 · 결재 · 알림이 서비스마다 하나씩, 여섯 벌', color=MUTED, weight=500)
box(40, 420, 400, 92, '구성원', ['같은 정보를 여러 번 입력하고', '알림은 여러 곳에서 확인'])
for cx in (102, 240, 378):
    path(f'M{cx} 420 V332'); head(cx, 332, 'u')
label(240, 396, '반복 입력', anchor='middle', size=12, weight=500)

# ── 오른쪽: 그룹웨어프로 하나 ──
add(f'<rect x="520" y="40" width="640" height="480" rx="16" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
label(544, 74, '그룹웨어프로 하나', color=ACCENT, size=16, weight=700)
for i, c in enumerate(['조직도 하나', '결재 하나', '알림 하나']):
    chip(544 + i * 150, 92, 136, c)

# 흐름: 인사 데이터 → 근태 → 결재 → 재무
box(544, 176, 180, 96, '인사 데이터', ['구성원 · 조직 · 발령'], accent=True)
box(752, 176, 112, 96, '근태', ['근무제 · 휴가'])
box(888, 176, 112, 96, '결재', ['결재선'])
box(1024, 176, 112, 96, '재무', ['정산'])
for x1, x2 in ((724, 752), (864, 888), (1000, 1024)):
    path(f'M{x1} 224 H{x2}'); head(x2, 224, 'r')
label(944, 160, '한 번 입력한 정보가 다음 단계로 이어짐', anchor='middle', size=12, weight=500)

# 커뮤니티 · 칸반 — 같은 조직도 · 알림 위에
box(544, 300, 180, 72, '커뮤니티 · 칸반', ['같은 조직도 · 알림 위에서'])
path('M634 272 V300', dashed=True); head(634, 300, 'd')

# 구성원 정보가 바뀌면 → 결재선 · 정산도 함께
box(544, 420, 180, 72, '구성원 정보가 바뀌면', ['발령 · 입사 · 퇴사'])
path('M724 456 H1080 V272'); head(1080, 272, 'u')
path('M944 456 V272'); head(944, 272, 'u')
label(1012, 446, '결재선과 정산도 함께 바뀜', anchor='middle', size=12, weight=500)

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-one-flow.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
