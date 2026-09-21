#!/usr/bin/env python3
"""
그룹웨어프로 · 시점 관리 구조 도식 → public/images/projects/gpro-point-in-time.svg

4. 진행의 「인사 모듈은 구성원 · 조직 · 발령이 시점 기준으로 남아야 한다」 단락을 그림으로:
  왼쪽  인사 데이터는 현재 상태가 아니라 이력으로 쌓인다 — 발령 이력 · 조직 이력 표(시작일 · 종료일)
  가운데 기준일을 넣으면 그날 유효한 행만 골라
  오른쪽 그날의 조직도와 결재선이 나온다 (두 날짜 예시)
  아래   이 데이터를 기준일로 읽는 곳 — 조직도 · 결재선 · 근태 기준 · 정산 · 발령 정정

예시 값(구성원 A · 영업1팀 · 경영지원팀 …)은 설명용 가상 데이터다.
색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-point-in-time.py
"""
from pathlib import Path

W, H = 1200, 580
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def label(x, y, s, color=MUTED, anchor='start', size=13, weight=600):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')

def box(x, y, w, h, title, sub=None, accent=False, size=16):
    fill, stroke, so = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 0.08)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}" stroke-width="1"/>')
    tc, sc = (WHITE, WHITE) if accent else (INK, BODY)
    if sub:
        add(f'<text x="{x + 18}" y="{y + h / 2 - 3:.0f}" font-size="{size}" font-weight="600" fill="{tc}">{title}</text>')
        add(f'<text x="{x + 18}" y="{y + h / 2 + 18:.0f}" font-size="13" fill="{sc}" fill-opacity="{0.85 if accent else 1}">{sub}</text>')
    else:
        add(f'<text x="{x + 18}" y="{y + h / 2 + 6:.0f}" font-size="{size}" font-weight="600" fill="{tc}">{title}</text>')

def table(x, y, title, widths, headers, rows):
    """제목 + 표. 종료일이 비면 '(지금)' 으로 보인다. 반환: 표 아래 y."""
    add(f'<text x="{x}" y="{y + 16}" font-size="14" font-weight="600" fill="{INK}">{title}</text>')
    top = y + 28
    w = sum(widths) + 32
    h = 28 + 30 * len(rows)
    add(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="10" fill="{WHITE}" stroke="#000000" stroke-opacity="0.08"/>')
    add(f'<rect x="{x + 1}" y="{top + 1}" width="{w - 2}" height="27" rx="9" fill="{CANVAS}"/>')
    cx = x + 16
    for hd, cw in zip(headers, widths):
        add(f'<text x="{cx}" y="{top + 19}" font-size="12" font-weight="600" fill="{MUTED}">{hd}</text>')
        cx += cw
    for r, row in enumerate(rows):
        ry = top + 28 + 30 * r
        if r: add(f'<path d="M{x + 1} {ry} H{x + w - 1}" stroke="#000000" stroke-opacity="0.08"/>')
        cx = x + 16
        for cell, cw in zip(row, widths):
            dim = cell == ''
            add(f'<text x="{cx}" y="{ry + 20}" font-size="13" fill="{MUTED if dim else BODY}">{cell or "(지금)"}</text>')
            cx += cw
    return top + h

def arrow_right(x1, x2, y, dashed=False):
    dash = ' stroke-dasharray="4 4"' if dashed else ''
    add(f'<path d="M{x1} {y} H{x2}" fill="none" stroke="{MUTED}" stroke-width="1.5"{dash}/>')
    add(f'<polygon points="{x2-9},{y-5} {x2},{y} {x2-9},{y+5}" fill="{MUTED}"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ── 왼쪽: 이력으로 쌓이는 인사 데이터 ──
label(40, 56, '인사 데이터는 현재 상태가 아니라 이력으로 쌓입니다')
b1 = table(40, 76, '발령 이력 · 구성원 A', [100, 100, 116, 80], ['시작일', '종료일', '소속', '직책'], [
    ['2022-01-03', '2023-02-28', '영업1팀', '팀원'],
    ['2023-03-01', '2024-06-30', '영업2팀', '팀장'],
    ['2024-07-01', '', '경영지원팀', '팀장'],
])
b2 = table(40, b1 + 24, '조직 이력', [100, 100, 116, 80], ['시작일', '종료일', '조직', '상위 조직'], [
    ['2022-01-01', '2023-12-31', '영업1팀', '영업본부'],
    ['2024-01-01', '', '영업1팀', '세일즈본부'],
    ['2022-01-01', '', '경영지원팀', '경영지원본부'],
])
label(40, b2 + 26, '고치지 않고 행을 더합니다. 예전 행은 그대로 남습니다.', weight=500, size=12)

# ── 가운데: 기준일 → 오른쪽: 그날의 조직도 · 결재선 ──
examples = [
    (120, '기준일 2022-12-31', '영업본부 > 영업1팀 > A (팀원)', '결재선: 영업1팀장 → 영업본부장'),
    (300, '기준일 2024-09-01', '경영지원본부 > 경영지원팀 > A (팀장)', '결재선: 경영지원본부장'),
]
for y, when, org, line in examples:
    arrow_right(468, 560, y + 28, dashed=True)
    box(560, y, 176, 56, when, accent=True, size=15)
    arrow_right(736, 800, y + 28)
    box(800, y - 16, 360, 88, org, line, size=15)
label(668, 104, '그날 유효한 행만 고르면', anchor='middle', size=12, weight=500)

# ── 아래: 기준일로 읽는 곳 ──
label(40, 480, '이 데이터를 기준일로 읽는 곳')
uses = [('조직도', '어느 날짜든 그날의 조직도'), ('결재선', '상신일의 소속 · 직책'), ('근태 기준', '그날의 근무제 · 휴일'),
        ('정산', '그달 소속으로 집계'), ('발령 정정', '과거 행만 고치고 이력은 보존')]
for i, (t, sub) in enumerate(uses):
    box(40 + i * 222, 494, 208, 60, t, sub, size=15)

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-point-in-time.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
