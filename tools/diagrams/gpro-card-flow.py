#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
그룹웨어프로 · 법인카드 정산 흐름(덱 07 「결재 한 번으로 끝나는 법인카드 정산 자동화 플로우」) → public/images/projects/gpro-card-flow.svg

덱 원본은 1920 폭 띠라 본문 폭(896)에 맞추면 글자가 읽히지 않아 896 폭으로 다시 그렸다(2026-09-24 사용자 지시: 스크롤 안 생기게).
지급 → 구성원 정산(강조) → 담당자 정산 → 업무 완료. 색은 tokens.css. 배경은 투명(plain 으로 캔버스 위에 놓는다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-card-flow.py
"""
from pathlib import Path

W, H = 896, 250
INK, BODY, MUTED, ACCENT, WHITE, PANEL, DOT_STROKE = '#212529', '#495057', '#868e96', '#504fed', '#ffffff', '#e9ecef', '#adb5bd'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)
def text(x, y, s, size=13, weight=400, fill=BODY, anchor='start', opacity=1):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" fill-opacity="{opacity}" text-anchor="{anchor}">{s}</text>')

LINE_Y = 118
# (x, w, 제목, [(단계 1줄, 2줄)], 강조)
cols = [
    (0,   224, '법인카드 지급', [('법인카드', '지급 신청'), ('법인카드', '사용')], False),
    (236, 332, '구성원 정산',   [('법인카드 사용내역', '스크래핑'), ('법인카드 정산서', '작성 및 신청'), ('법인카드 정산서', '결재 승인')], True),
    (580, 212, '담당자 정산',   [('법인카드 사용내역', '확인 및 정산')], False),
]
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
dots = []
for x, w, title, steps, accent in cols:
    add(f'<rect x="{x}" y="0" width="{w}" height="{H}" rx="20" fill="{ACCENT if accent else PANEL}"/>')
    text(x + 24, 46, title, size=18, weight=700, fill=WHITE if accent else INK)
    xs = [x + 24 + i * 100 for i in range(len(steps))]
    # 칸 안 실선
    add(f'<path d="M{xs[0]} {LINE_Y} H{xs[-1]}" stroke="{WHITE if accent else DOT_STROKE}" stroke-opacity="{0.7 if accent else 1}" stroke-width="1.5"/>' if len(xs) > 1 else '')
    for sx, (l1, l2) in zip(xs, steps):
        add(f'<circle cx="{sx}" cy="{LINE_Y}" r="7" fill="{WHITE}" stroke="{ACCENT if accent else DOT_STROKE}" stroke-width="1.5"/>')
        text(sx - 7, 152, l1, fill=WHITE if accent else BODY, weight=500)
        text(sx - 7, 171, l2, fill=WHITE if accent else BODY, weight=500)
    dots.append((xs[0], xs[-1]))
# 칸 사이 점선
for (a, b) in [(dots[0][1], dots[1][0]), (dots[1][1], dots[2][0])]:
    add(f'<path d="M{a + 7} {LINE_Y} H{b - 7}" stroke="{DOT_STROKE}" stroke-width="1.5" stroke-dasharray="4 4"/>')
# 업무 완료
add(f'<rect x="804" y="0" width="92" height="{H}" rx="20" fill="{PANEL}"/>')
add(f'<circle cx="850" cy="{LINE_Y}" r="30" fill="none" stroke="{DOT_STROKE}" stroke-width="1.5"/>')
text(850, LINE_Y - 3, '업무', size=13, weight=600, fill=INK, anchor='middle'); text(850, LINE_Y + 13, '완료', size=13, weight=600, fill=INK, anchor='middle')

def pill(cx, y, s, w):
    add(f'<rect x="{cx - w / 2:.0f}" y="{y}" width="{w}" height="22" rx="5" fill="{INK}"/>')
    text(cx, y + 15, s, size="11", weight=600, fill=WHITE, anchor='middle')
pill((dots[0][1] + dots[1][0]) / 2, 82, '카드사 API → VAN 스크래핑 서버', 168)   # 지급 → 구성원 정산 사이
pill(dots[2][0] + 76, 196, 'GPRO → ERP 전표 전송', 138)                          # 담당자 정산 아래
add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-card-flow.svg'
dst.write_text('\n'.join(s for s in out if s) + '\n', encoding='utf-8'); print(dst, f'{dst.stat().st_size} bytes')
