#!/usr/bin/env python3
"""
그룹웨어프로 · 시점 관리 도식 → public/images/projects/gpro-point-in-time.svg

한눈에 읽히는 한 가지만 보인다(2026-09-21 사용자: 표 도식은 너무 어렵다):
  구성원 A 의 발령이 시간축 위에 구간으로 쌓이고, 날짜를 하나 찍으면 그날의 소속 · 직책 · 결재선이 나온다.

예시 값(구성원 A · 영업1팀 · 경영지원팀 …)은 설명용 가상 데이터다.
색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-point-in-time.py
"""
from pathlib import Path

W, H = 1200, 380
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def label(x, y, s, color=MUTED, anchor='start', size=13, weight=600):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')

# 시간축: 2022-01 ~ 2025-07 (42개월) → x 80 ~ 1120. 마지막 구간을 넉넉히 두어 기준일 선이 글자를 지나지 않게.
X0, X1, MONTHS = 80, 1120, 42
px = lambda m: X0 + (X1 - X0) * m / MONTHS

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')
label(40, 52, '구성원 A 의 발령 이력. 발령이 날 때마다 구간이 하나 더 쌓입니다')

# 구간 (시작 개월, 끝 개월, 소속 · 직책, 시작일)
segs = [(0, 14, '영업1팀 · 팀원', '2022-01-03'), (14, 30, '영업2팀 · 팀장', '2023-03-01'), (30, 42, '경영지원팀 · 팀장', '2024-07-01')]
Y, HB = 116, 56
for i, (a, b, name, start) in enumerate(segs):
    x, w = px(a), px(b) - px(a)
    add(f'<rect x="{x:.0f}" y="{Y}" width="{w - 6:.0f}" height="{HB}" rx="10" fill="{CANVAS}" stroke="#000000" stroke-opacity="0.08"/>')
    add(f'<text x="{x + 16:.0f}" y="{Y + 34}" font-size="15" font-weight="600" fill="{INK}">{name}</text>')
    label(x, Y + HB + 22, start, size=12, weight=500)
# 마지막 구간은 열려 있다
add(f'<text x="{X1 - 6}" y="{Y + 34}" font-size="13" fill="{MUTED}" text-anchor="end">지금</text>')

# 기준일 두 개 — 축 위에 찍고 아래 결과 상자로
marks = [(12, '2022-12-31', '영업1팀 · 팀원', '결재선: 영업1팀장 → 영업본부장', 'left'),
         (38, '2025-03-01', '경영지원팀 · 팀장', '결재선: 경영지원본부장', 'right')]
for m, date, who, line, side in marks:
    x = px(m)
    add(f'<path d="M{x:.0f} 92 V270" stroke="{ACCENT}" stroke-width="2"/>')
    add(f'<circle cx="{x:.0f}" cy="{Y + HB / 2}" r="6" fill="{ACCENT}"/>')
    add(f'<text x="{x:.0f}" y="{84}" font-size="14" font-weight="700" fill="{ACCENT}" text-anchor="middle">{date} 에 결재를 올리면</text>')
    bx = x - 150 if side == 'left' else x - 190
    bx = max(40, min(bx, W - 40 - 340))
    add(f'<rect x="{bx:.0f}" y="270" width="340" height="72" rx="12" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
    add(f'<text x="{bx + 18:.0f}" y="{270 + 30}" font-size="16" font-weight="600" fill="{INK}">그날의 소속 · 직책: {who}</text>')
    add(f'<text x="{bx + 18:.0f}" y="{270 + 54}" font-size="13" fill="{BODY}">{line}</text>')

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-point-in-time.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
