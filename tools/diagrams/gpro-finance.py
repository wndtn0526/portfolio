#!/usr/bin/env python3
"""
그룹웨어프로 · 법인카드 · 홈택스 프로젝트(02) 도식 여섯 장 → public/images/projects/gpro-fin-*.svg

PORTFOLIO 덱 슬라이드 05 · 07 · 08 · 10 · 12 · 13 의 내용을 사이트 문법(tokens.css 색 · Pretendard · 상자 · 화살표)으로 새로 그린 것.
캡처를 쓰지 않는다(2026-09-22 사용자 지시). 숫자는 덱 그대로.
화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다). 고치려면 이 파일을 고치고 다시 돌린다.
"""
from pathlib import Path
import math

INK, BODY, MUTED, CANVAS, ACCENT, WHITE, RULE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff', '#dee2e6'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
OUT = Path(__file__).resolve().parents[2] / 'public/images/projects'

class Svg:
    def __init__(self, w, h): self.w, self.h, self.o = w, h, []
    def add(self, s): self.o.append(s)
    def text(self, x, y, s, size=13, weight=500, color=BODY, anchor='start', opacity=1):
        self.add(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" font-weight="{weight}" fill="{color}" fill-opacity="{opacity}" text-anchor="{anchor}">{s}</text>')
    def box(self, x, y, w, h, title, sub=None, accent=False, size=15, r=12):
        fill, stroke, so = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 0.08)
        self.add(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}"/>')
        tc, sc = (WHITE, WHITE) if accent else (INK, BODY)
        lines = sub.split('|') if sub else []
        block = 20 + 18 * len(lines)
        ty = y + (h - block) / 2 + 15
        self.text(x + 16, ty, title, size, 600, tc)
        for i, l in enumerate(lines): self.text(x + 16, ty + 20 + 18 * i, l, 12, 500, sc, opacity=0.85 if accent else 1)
    def head(self, x, y, d):
        pts = {'r': f'{x-9},{y-5} {x},{y} {x-9},{y+5}', 'l': f'{x+9},{y-5} {x},{y} {x+9},{y+5}', 'd': f'{x-5},{y-9} {x},{y} {x+5},{y-9}', 'u': f'{x-5},{y+9} {x},{y} {x+5},{y+9}'}[d]
        self.add(f'<polygon points="{pts}" fill="{MUTED}"/>')
    def line(self, d, dashed=False, color=MUTED, w=1.5):
        dash = ' stroke-dasharray="4 4"' if dashed else ''
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{dash}/>')
    def arrow(self, x1, y1, x2, y2, dashed=False):   # 수평 또는 수직
        self.line(f'M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}', dashed)
        self.head(x2, y2, 'r' if x2 > x1 else 'l' if x2 < x1 else 'd' if y2 > y1 else 'u')
    def diamond(self, cx, cy, w, h, title):
        self.add(f'<polygon points="{cx-w/2:.0f},{cy:.0f} {cx:.0f},{cy-h/2:.0f} {cx+w/2:.0f},{cy:.0f} {cx:.0f},{cy+h/2:.0f}" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
        for i, l in enumerate(title.split('|')):
            self.text(cx, cy + 5 + (i - (title.count('|')) / 2) * 16, l, 12, 600, INK, 'middle')
    def save(self, name):
        p = OUT / name
        p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="{FONT}" aria-hidden="true">\n<rect width="{self.w}" height="{self.h}" fill="{WHITE}"/>\n' + '\n'.join(self.o) + '\n</svg>\n', encoding='utf-8')
        print(p.name, p.stat().st_size, 'bytes')

# ── 1. 문제 수치 (덱 05) ──
s = Svg(1200, 400)
# A. 불일치율 — 단절 지점마다 오른다
s.text(40, 56, '결재-재무 데이터 불일치율', 14, 600, INK)
s.text(40, 76, '단절 지점을 지날 때마다 쌓입니다', 12, 500, MUTED)
pts = [(80, 300), (240, 196), (400, 166)]
s.line(f'M80 320 H420', color=RULE, w=1)
s.line('M{} {} L{} {} L{} {}'.format(*[c for p in pts for c in p]), color=ACCENT, w=2)
for (x, y), lab, val in zip(pts, ['그룹웨어 결재', '재무 시스템 수기 입력', 'ERP 전표'], ['0%', '17%', '21%']):
    s.add(f'<circle cx="{x}" cy="{y}" r="6" fill="{WHITE}" stroke="{ACCENT}" stroke-width="2"/>')
    s.text(x, y - 16, val, 13, 700, INK, 'middle')
    s.text(x, 342, lab, 12, 500, MUTED, 'middle')
s.text(240, 140, '1차 단절', 11, 600, MUTED, 'middle'); s.text(400, 110, '2차 단절', 11, 600, MUTED, 'middle')
# B. 첨부 누락률 — 미연계 vs 연계
s.text(500, 56, '세금계산서 첨부 누락률', 14, 600, INK)
s.text(500, 76, '홈택스 메뉴에서 내려받아 첨부할 때', 12, 500, MUTED)
s.line('M500 320 H820', color=RULE, w=1)
for x, val, h, acc, lab in [(560, '43%', 180, False, '홈택스 미연계 고객사'), (700, '4%', 18, True, '홈택스 연계 고객사')]:
    s.add(f'<rect x="{x}" y="{320-h}" width="80" height="{h}" rx="6" fill="{ACCENT if acc else RULE}"/>')
    s.text(x + 40, 320 - h - 12, val, 15, 700, INK, 'middle'); s.text(x + 40, 342, lab, 12, 500, MUTED, 'middle')
# C. 카드 두 장
s.box(880, 100, 280, 96, '전표 반영 평균 리드타임', '2.8일 ~ 4.2일|전자결재 승인 로그 기준')
s.box(880, 216, 280, 96, '재무팀 재요청률', '25% ~ 33%|재무팀 VOC 분석')
s.text(880, 342, '정산 한 건에 6 ~ 8개 필드, 8 ~ 12분', 12, 500, MUTED)
s.save('gpro-fin-problem.svg')

# ── 2. 법인카드 정산 단계 (덱 07) ──
s = Svg(1200, 300)
phases = [(40, 250, '법인카드 지급', ['지급 신청', '카드 사용'], False), (318, 430, '구성원 정산', ['사용 내역 스크래핑', '정산서 작성 · 신청', '결재 승인'], True),
          (776, 230, '담당자 정산', ['사용 내역 확인 · 정산'], False), (1034, 126, '업무 완료', [], False)]
for x, w, title, steps, acc in phases:
    s.add(f'<rect x="{x}" y="70" width="{w}" height="150" rx="16" fill="{ACCENT if acc else CANVAS}" stroke="#000000" stroke-opacity="{0 if acc else 0.08}"/>')
    s.text(x + 20, 104, title, 16, 700, WHITE if acc else INK)
    for i, st in enumerate(steps):
        cx = x + 20 + i * 135
        s.add(f'<circle cx="{cx + 6}" cy="{148}" r="5" fill="{WHITE if acc else ACCENT}"/>')
        s.text(cx, 178, st, 12, 500, WHITE if acc else BODY, opacity=0.9 if acc else 1)
for x1, x2 in [(290, 318), (748, 776), (1006, 1034)]: s.arrow(x1, 145, x2, 145)
s.text(304, 250, '카드사 API → 스크래핑 서버 → GPRO', 12, 500, MUTED, 'middle')
s.text(891, 250, 'GPRO → ERP 전표 전송', 12, 500, MUTED, 'middle')
s.text(40, 46, '구성원과 재무 담당자 모두 입력 대신 검증만 합니다', 13, 600, MUTED)
s.save('gpro-fin-card-phases.svg')

# ── 3. 법인카드 자동 정산 플로우차트 (덱 08) ──
s = Svg(1200, 330)
y, h, w = 60, 64, 176
xs = [40, 248, 456, 664]
titles = [('관리자 기능 활성화', '재무 → 법인카드 계정 등록'), ('카드 등록', '무기명 · 기명 · 개인형|담당자 지정'), ('카드 지급', '사용일자 · 유효기간 설정|지급 시 정산 위임'), ('내역 스크래핑', '카드사 API → 스크래핑 서버 → GPRO')]
for x, (t, n) in zip(xs, titles):
    s.box(x, y, w, h, t, size=14)
    for i, l in enumerate(n.split('|')): s.text(x, y + h + 22 + 16 * i, l, 11, 500, MUTED)
for x in xs[:-1]: s.arrow(x + w, y + h / 2, x + w + 32, y + h / 2)
s.arrow(840, 92, 872, 92)
s.diamond(946, 92, 148, 84, '스크래핑 가능한|데이터인가?')
s.arrow(1020, 92, 1052, 92); s.text(1030, 82, '예', 11, 600, MUTED)
s.box(1052, 60, 108, 64, '정산 신청', '및 결재', size=14)
s.arrow(946, 134, 946, 202); s.text(956, 176, '아니오', 11, 600, MUTED)
s.box(858, 202, 176, 64, '담당자 수기 생성', '하이패스 · 교통비 · 외화 보정', size=14)
s.line('M1034 234 H1106 V124'); s.head(1106, 124, 'u')
s.save('gpro-fin-card-flow.svg')

# ── 4. 홈택스 지출결의서 플로우차트 (덱 10) ──
s = Svg(1200, 330)
y, h = 60, 64
s.box(40, y, 168, h, '관리자 연동 설정', size=14); s.arrow(208, 92, 240, 92)
s.box(240, y, 168, h, '세금계산서 수신', '국세청 서버에서 자동', size=14); s.arrow(408, 92, 440, 92)
s.diamond(514, 92, 148, 84, '등록된|거래처인가?'); s.arrow(588, 92, 620, 92); s.text(598, 82, '예', 11, 600, MUTED)
s.diamond(694, 92, 148, 84, '담당자 매칭에|성공했는가?'); s.arrow(768, 92, 800, 92); s.text(778, 82, '예', 11, 600, MUTED)
s.box(800, y, 176, h, '지출결의서 생성', '담당자가 버튼 한 번', accent=True, size=14); s.arrow(976, 92, 1008, 92)
s.box(1008, y, 152, h, '결재 · ERP 전표', '승인되면 자동 반영', size=14)
s.arrow(514, 134, 514, 202); s.text(524, 176, '아니오', 11, 600, MUTED)
s.box(430, 202, 168, 64, '신규 거래처 등록', size=14)
s.arrow(598, 234, 610, 234); s.box(610, 202, 168, 64, '담당자 지정', size=14)
s.arrow(694, 134, 694, 202); s.text(704, 176, '아니오', 11, 600, MUTED)
s.line('M778 234 H888 V124'); s.head(888, 124, 'u')
s.save('gpro-fin-hometax-flow.svg')

# ── 5. 결과 차트 (덱 12) ──
s = Svg(1200, 360)
s.text(40, 56, '전자결재-재무 데이터 일치율', 14, 600, INK); s.text(40, 76, '수기 입력(1 ~ 3월)에서 자동 매핑(4 ~ 6월)으로', 12, 500, MUTED)
s.line('M40 290 H600', color=RULE, w=1)
vals = [(83, False), (83, False), (83, False), (98, True), (98, True), (98, True)]
for i, (v, acc) in enumerate(vals):
    x = 60 + i * 88; bh = v * 1.8
    s.add(f'<rect x="{x}" y="{290-bh:.0f}" width="56" height="{bh:.0f}" rx="6" fill="{ACCENT if acc else RULE}"/>')
    s.text(x + 28, 310, f'{i+1}월', 12, 500, MUTED, 'middle')
s.text(148, 118, '평균 83%', 13, 700, INK, 'middle'); s.text(412, 92, '평균 98%', 13, 700, INK, 'middle')
s.text(600, 92, '+15%p', 22, 700, ACCENT, 'end')
s.text(720, 56, '업무 자동화율', 14, 600, INK); s.text(720, 76, '전체 재무 프로세스 기준', 12, 500, MUTED)
def donut(cx, cy, pct, acc, label):
    r = 62; c = 2 * math.pi * r
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RULE}" stroke-width="18"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT if acc else MUTED}" stroke-width="18" stroke-dasharray="{c*pct/100:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})" stroke-linecap="round"/>')
    s.text(cx, cy + 8, f'{pct}%', 22, 700, INK, 'middle'); s.text(cx, cy + 96, label, 12, 500, MUTED, 'middle')
donut(820, 200, 18, False, '개선 전'); donut(1010, 200, 94, True, '개선 후')
s.text(1160, 92, '+76%p', 22, 700, ACCENT, 'end')
s.save('gpro-fin-results.svg')

# ── 6. KPI (덱 13) ──
s = Svg(1200, 300)
s.text(40, 56, '핵심 매출 지표 · 전 분기 대비', 14, 600, INK)
rows = [('매출 상승률', 47, '도입 고객 기준'), ('결제 전환율', 38, '데모 시연 이후 계약 전환'), ('고객 유지율', 21, '도입 6개월 내 유지 고객')]
for i, (lab, v, note) in enumerate(rows):
    y = 92 + i * 60
    s.text(40, y + 16, lab, 13, 600, INK); s.text(40, y + 34, note, 11, 500, MUTED)
    s.add(f'<rect x="200" y="{y}" width="320" height="16" rx="8" fill="{RULE}"/>')
    s.add(f'<rect x="200" y="{y}" width="{320*v/50:.0f}" height="16" rx="8" fill="{ACCENT}"/>')
    s.text(200 + 320 * v / 50 + 12, y + 13, f'{v}% 상승', 13, 700, INK)
s.text(640, 56, '핵심 운영 지표', 14, 600, INK)
for i, (v, lab, note) in enumerate([('+29%', '고객사 평균 거래 건수', '시스템이 일상 업무에 정착'), ('+19%', '기능 재활용률', '같은 기능을 반복 사용'), ('+34%', '고객 피드백 긍정률', '업무 효율 향상 체감')]):
    x = 640 + i * 180
    s.add(f'<rect x="{x}" y="80" width="164" height="150" rx="12" fill="{CANVAS}" stroke="#000000" stroke-opacity="0.08"/>')
    s.text(x + 16, 128, v, 26, 700, ACCENT); s.text(x + 16, 160, lab, 13, 600, INK); s.text(x + 16, 182, note, 11, 500, MUTED)
s.save('gpro-fin-kpi.svg')
