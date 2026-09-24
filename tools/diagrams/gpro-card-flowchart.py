#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
그룹웨어프로 · 법인카드 정산 플로우차트(덱 08 「법인카드 스크래핑 기반 자동 정산 프로세스」) → public/images/projects/gpro-card-flowchart.svg

덱 원본(1823 폭)을 896 폭에 두 줄로 다시 그렸다(2026-09-24 사용자 지시: 스크롤 안 생기게).
1줄: Admin 기능 활성화 → 카드 등록 → 카드 지급 → 내역 스크래핑. 2줄: 스크래핑 가능한 데이터인가? Y → 정산 신청 및 결재 / N → 담당자 내역 수기 생성 → 합류.
글은 덱 문구를 그대로 옮기고 폭에 맞춰 줄만 바꿨다. 배경 투명(plain).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-card-flowchart.py
"""
from pathlib import Path

W, H = 896, 632
INK, BODY, MUTED, ACCENT, WHITE, LINE = '#212529', '#495057', '#868e96', '#504fed', '#ffffff', '#ced4da'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
BW, BH, GAP = 176, 72, 40
COL = [0, 216, 432, 648]
out = []
def add(s): out.append(s)
def text(x, y, s, size=12, weight=400, fill=BODY, anchor='start'):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>')
def box(x, y, title, accent=False):
    add(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="8" fill="{ACCENT if accent else WHITE}" stroke="{ACCENT if accent else LINE}" stroke-width="1"/>')
    text(x + BW / 2, y + BH / 2 + 5, title, size=14, weight=600, fill=WHITE if accent else INK, anchor='middle')
def notes(x, y, lines):
    for i, s in enumerate(lines):
        text(x, y + i * 18, s)
def head(x, y, d):  # 화살촉 — d: 'r' 오른쪽, 'd' 아래, 'l' 왼쫙
    p = {'r': f'{x-9},{y-5} {x},{y} {x-9},{y+5}', 'd': f'{x-5},{y-9} {x},{y} {x+5},{y-9}', 'l': f'{x+9},{y-5} {x},{y} {x+9},{y+5}'}[d]
    add(f'<polygon points="{p}" fill="{ACCENT}"/>')
def line(d):
    add(f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
# ── 1줄 ──
R1 = 0; cy1 = R1 + BH / 2
titles = ['Admin 에서 기능 활성화', '카드 등록', '카드 지급', '내역 스크래핑']
for i, (x, t) in enumerate(zip(COL, titles)):
    box(x, R1, t, accent=(i == 0))
    if i < 3:
        line(f'M{x + BW} {cy1} H{x + BW + GAP - 2}'); head(x + BW + GAP, cy1, 'r')
notes(COL[0], 100, ['Admin 에서 콘솔로 기능 ON/OFF', '재무 → 법인카드 계정등록 메뉴에서', '카드사 계정 등록 및 연동 진행'])
notes(COL[1], 100, ['법인카드 등록 유형', '· 무기명 (개별지급) 법인카드', '· 무기명 (부서지급) 법인카드', '· 기명 법인카드', '· 개인형 법인카드', '법인카드 담당자 지정'])
notes(COL[2], 100, ['· 지급 시 사용일자 지정', '  (유효 시작 · 종료일시)', '· 지급 내역 로우 생성,', '  사용일자 중복 불가', '· 지급 시 정산 위임 설정'])
notes(COL[3] + 28, 100, ['카드사 API →', 'VAN 스크래핑 서버 →', 'GPRO 전송'])
# 내역 스크래핑 → 분기 (칸 왼쪽 가장자리를 타고 내려간다 — 메모와 겹치지 않게)
DX, DY, DW, DH = COL[3] + BW / 2, 310, 88, 45   # 마름모 중심 · 반폭 · 반높이
line(f'M{COL[3] + 12} {R1 + BH} V240 H{DX} V{DY - DH - 2}'); head(DX, DY - DH, 'd')
# ── 2줄: 분기 ──
add(f'<polygon points="{DX - DW},{DY} {DX},{DY - DH} {DX + DW},{DY} {DX},{DY + DH}" fill="{WHITE}" stroke="{LINE}" stroke-width="1"/>')
text(DX, DY - 3, '스크래핑 가능한', size=13, weight=600, fill=INK, anchor='middle'); text(DX, DY + 14, '데이터인가?', size=13, weight=600, fill=INK, anchor='middle')
# Y → 정산 신청 및 결재 (0번 칸)
SX, SY = COL[0], DY - BH / 2
box(SX, SY, '정산 신청 및 결재', accent=True)
line(f'M{DX - DW} {DY} H{SX + BW + 2}'); head(SX + BW, DY, 'l')
text(DX - DW - 6, DY - 8, 'Y', size=12, weight=600, fill=MUTED, anchor='end')
notes(SX, SY + BH + 28, ['개인업무 메뉴의 법인카드 정산에서 프로젝트, 비용내역을 입력해 정산 신청서 상신', '결재가 끝난 정산서는 재무 메뉴의 법인카드 정산 목록에 노출'])
# N → 담당자 내역 수기 생성 (3번 칸, 3줄) → Y 선에 합류
R3 = 430
box(COL[3], R3, '담당자 내역 수기 생성')
line(f'M{DX} {DY + DH} V{R3 - 2}'); head(DX, R3, 'd')
text(DX + 8, DY + DH + 22, 'N', size=12, weight=600, fill=MUTED)
JX = COL[3] - 20
add(f'<path d="M{COL[3]} {R3 + BH / 2} H{JX} V{DY}" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>')
add(f'<circle cx="{JX}" cy="{DY}" r="3.5" fill="{ACCENT}"/>')
notes(COL[3], R3 + BH + 28, ['카드사 API 로 수집되지 않는', '하이패스, 교통비 내역은 담당자', '메뉴에서 수기로 처리', '외화 내역 환율 보정도 함께 처리'])
# 코멘트 — 0~2번 칸, 3줄
add(f'<rect x="0" y="{R3}" width="{COL[2] + BW}" height="96" rx="12" fill="{WHITE}" stroke="{LINE}" stroke-width="1"/>')
text(24, R3 + 34, '이 과정을 통해 구성원은 명확한 사용 기간 안에서 안전하게 카드를 쓰고 정산할 수 있고,', size=13, fill=INK, weight=500)
text(24, R3 + 56, '관리자는 불필요한 확인 · 수정 업무 없이 정확하고 투명한 데이터 흐름을 확보할 수 있습니다.', size=13, fill=INK, weight=500)
add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-card-flowchart.svg'
dst.write_text('\n'.join(s for s in out if s) + '\n', encoding='utf-8'); print(dst, f'{dst.stat().st_size} bytes')
