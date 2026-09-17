#!/usr/bin/env python3
"""
그룹웨어프로 · 전자결재 흐름 도식 → public/images/projects/gpro-approval-flow.svg

3. 제품 설계 둘째 단락(전자결재를 인사 데이터 위에 하나로 올렸다)을 그림으로 옮긴 것.
  왼쪽  인사코어 위의 데이터(인사 · 근태 · 재무) + 외부 증빙(법인카드 · 홈택스)
  가운데 전자결재 — 결재 양식 자동 채움 / 품의 한 번 → 승인(강조) / 지출결의서 초안
  오른쪽 예산 · 마감 · 자금 지급 반영, 피드

색은 tokens.css(canvas · ink · body · muted · statement). 글꼴은 페이지에서 상속(인라인으로 넣는다).
화살촉은 marker 대신 도형으로 그린다 — Figma SVG 가져오기가 marker 를 떨어뜨린다.
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-approval-flow.py
"""
from pathlib import Path

W, H = 1200, 612
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def box(x, y, w, h, title, subs=(), accent=False, title_size=17):
    fill, stroke, sw = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 1)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{0 if accent else 0.08}" stroke-width="{sw}"/>')
    tc, sc = (WHITE, WHITE) if accent else (INK, BODY)
    n = 1 + len(subs)
    # 세로 가운데: 제목 17 + 부제 14 줄들, 줄 간격 22
    block = 20 + 22 * len(subs)
    ty = y + (h - block) / 2 + 16
    add(f'<text x="{x + 20}" y="{ty:.0f}" font-size="{title_size}" font-weight="600" fill="{tc}">{title}</text>')
    for i, s in enumerate(subs):
        add(f'<text x="{x + 20}" y="{ty + 22 * (i + 1):.0f}" font-size="14" fill="{sc}" fill-opacity="{0.85 if accent else 1}">{s}</text>')

def label(x, y, s):
    add(f'<text x="{x}" y="{y}" font-size="13" font-weight="600" fill="{MUTED}">{s}</text>')

def path(d, dashed=False):
    dash = ' stroke-dasharray="4 4"' if dashed else ''
    add(f'<path d="{d}" fill="none" stroke="{MUTED}" stroke-width="1.5"{dash}/>')

def head(x, y, dir):   # 화살촉 — 끝점 (x, y), dir: r/d/u
    if dir == 'r': pts = f'{x-9},{y-5} {x},{y} {x-9},{y+5}'
    if dir == 'd': pts = f'{x-5},{y-9} {x},{y} {x+5},{y-9}'
    if dir == 'u': pts = f'{x-5},{y+9} {x},{y} {x+5},{y+9}'
    add(f'<polygon points="{pts}" fill="{MUTED}"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ── 왼쪽: 데이터 ──
label(40, 56, '인사코어 위의 데이터')
box(40, 68, 260, 76, '인사 데이터', ['구성원 · 조직 · 발령'])
box(40, 160, 260, 76, '근태 데이터', ['근무제 · 휴일 · 연차'])
box(40, 252, 260, 76, '재무 데이터', ['예산 · 마감 · 자금 지급'])
label(40, 396, '외부 증빙')
box(40, 408, 260, 64, '법인카드 승인 내역')
box(40, 488, 260, 64, '홈택스 세금계산서')

# ── 가운데: 전자결재 ──
add(f'<rect x="400" y="40" width="320" height="532" rx="16" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
add(f'<text x="424" y="74" font-size="16" font-weight="700" fill="{ACCENT}">전자결재</text>')
box(424, 96, 272, 100, '결재 양식 자동 채움', ['인사 · 근태 · 재무 정보를', '정합성 검증 후 채움'])
box(424, 262, 272, 88, '품의 한 번 → 승인', ['세 번 올리던 지출 건이 한 번으로'], accent=True)
box(424, 440, 272, 100, '지출결의서 초안', ['승인 내역 · 세금계산서가 초안이 되고', '구성원은 입력 대신 확인만'])

# ── 오른쪽: 결과 ──
box(820, 262, 340, 88, '예산 · 마감 · 자금 지급 반영', ['재무팀만 쓰던 기능을 전 직원이'])
box(820, 440, 340, 100, '피드', ['나에게 온 결재와 변경 사항이', '한곳에 모임'])

# ── 화살표 ──
# 데이터 셋 → 자동 채움 (x 360 에서 모여 y 146 으로)
path('M300 106 H360 V290 H300'); path('M300 198 H360'); path('M360 146 H424'); head(424, 146, 'r')
# 증빙 둘 → 초안 (스크래핑)
path('M300 440 H360 V520 H300'); path('M360 490 H424'); head(424, 490, 'r')
add(f'<text x="392" y="480" font-size="12" fill="{MUTED}" text-anchor="middle">스크래핑</text>')
# 자동 채움 ↓ 품의, 초안 ↑ 품의
path('M560 196 V262'); head(560, 262, 'd')
path('M560 440 V350'); head(560, 350, 'u')
# 승인 → 반영
path('M696 306 H820'); head(820, 306, 'r')
# 전자결재 → 피드 (알림)
path('M720 490 H820', dashed=True); head(820, 490, 'r')
add(f'<text x="770" y="480" font-size="12" fill="{MUTED}" text-anchor="middle">알림</text>')

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-approval-flow.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
