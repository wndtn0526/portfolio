#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03 주 52시간 · 연장 근무 / 휴일 근무 플로우차트와 결과 지표 그래프 → 플러그인 작업(JSON)

덱 슬라이드 08 의 플로우차트(GPRO_PORTFOLIO 1958:5268)와 같은 부품 · 치수로 그린다(2026-09-26, get_design_context 실측):
  시작끝     #688DF1 면 · 4px 테두리 · 반경 6 · 폭 200 · 위아래 30 · Apple SD Gothic Neo Bold 15/23 흰 글자 · 자간 -0.6
  텍스트 박스 #ECF1FD 면 · #688DF1 4px 테두리 · 같은 치수 · Pretendard Bold 15/23 #4270ED
  선택지     212×110 마름모(덱 벡터 그대로) · Apple SD Gothic Neo Bold 15/23 #4270ED
  기본(연결선) #688DF1 4px 선 · 시작점 고리(r10 · 안쪽 r6 #ECF1FD) · 끝 화살촉(덱 벡터 그대로) · 모서리 반경 10
  박스 코멘트 Pretendard Bold 15/23 #ADB5BD · 상자 아래 16
상자 간격은 덱과 같이 322(상자 200 + 간격 122) — 웹에서 02 의 플로우차트와 같은 배율로 보이게.

내용은 projects.php 03 의 프로세스 설계 문단에 적힌 것만 옮긴다(새 단계를 지어내지 않는다).
사용: python3 tools/figma-export-plugin/tasks/overtime-52h.py <작업 JSON 경로>
"""
import json, math, sys

BLUE, TEXT_BLUE, LIGHT, NOTE, WHITE = '#688DF1', '#4270ED', '#ECF1FD', '#ADB5BD', '#FFFFFF'
SD = {'family': 'Apple SD Gothic Neo', 'style': 'Bold'}
PRE = {'family': 'Pretendard', 'style': 'Bold'}
W, PAD, LH, SIZE, TRACK = 200, 30, 23, 15, -0.6
DIAMOND = ('M97.0682 2.48185C98.2553 1.83999 99.6858 1.84 100.873 2.48185L193.844 52.7494C196.695 54.2913 196.624 58.4071 193.721 59.85'
           'L100.751 106.061C99.6294 106.618 98.3116 106.618 97.1902 106.061L4.21955 59.85C1.31669 58.4071 1.24587 54.2913 4.09748 52.7494L97.0682 2.48185Z')
DW, DH = 197.941, 108.479          # 마름모 벡터 크기 · 212×110 칸 안 여백 7.04 / 0.825
# 화살촉(덱 벡터) — 끝점을 (0,0), 오른쪽을 향하게 옮긴 것
ARROW = [('M', (-21.2436, 8.2699)), ('C', (-21.9235, 9.2364), (-20.7922, 10.4326), (-19.7552, 9.8437)), ('L', (-0.3777, 0.4498)),
         ('C', (-0.002, 0.2676), (-0.0019, -0.2677), (-0.3776, -0.45)), ('L', (-19.7069, -9.82729)),
         ('C', (-20.7251, -10.445094), (-21.8932, -9.28122), (-21.2436, -8.2961)), ('C', (-17.7322, -2.97047), (-17.5679, 3.0453), (-21.2436, 8.2699))]
TIP_GAP = 17.45                    # 선은 화살촉 끝보다 이만큼 앞에서 끝난다(덱: 82 → 99.45)

def text(x, lines, font, color, cy=None, y=None, w=None, align='LEFT'):
    t = {'type': 'text', 'x': x, 'lines': lines, 'font': font, 'size': SIZE, 'lineHeight': LH, 'tracking': TRACK, 'color': color, 'align': align}
    if w: t['w'] = w
    if cy is not None: t['cy'] = cy
    else: t['y'] = y
    return t

class Flow:
    def __init__(self): self.items, self.nodes = [], {}
    def box(self, key, x, cy, lines, terminal=False, note=None):
        h = 2 * PAD + LH * len(lines); top = cy - h / 2
        self.items.append({'type': 'rect', 'name': ' '.join(lines), 'x': x, 'y': top, 'w': W, 'h': h, 'fill': BLUE if terminal else LIGHT, 'stroke': BLUE, 'strokeWeight': 4, 'radius': 6})
        self.items.append(text(x + 20, lines, SD if terminal else PRE, WHITE if terminal else TEXT_BLUE, cy=cy, w=160, align='CENTER'))
        if note: self.items.append(text(x, note, PRE, NOTE, y=top + h + 16))
        self.nodes[key] = {'left': x, 'right': x + W, 'top': top, 'bottom': top + h, 'cx': x + W / 2, 'cy': cy}
    def decision(self, key, x, cy, lines):
        top = cy - 55
        svg = f'<svg width="{DW}" height="{DH}" viewBox="0 0 {DW} {DH}" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="{DIAMOND}" fill="{LIGHT}" stroke="{BLUE}" stroke-width="4"/></svg>'
        self.items.append({'type': 'svg', 'name': ' '.join(lines), 'x': x + 7.04, 'y': top + 0.825, 'svg': svg})
        self.items.append(text(x + 39, lines, SD, TEXT_BLUE, cy=cy, w=134, align='CENTER'))
        ox, oy = x + 7.04, top + 0.825      # 벡터 꼭짓점(곡선 끝 포함) — 왼 2.0 · 오 195.94 · 위 2.0 · 아래 106.48
        self.nodes[key] = {'left': ox + 2.0, 'right': ox + 195.94, 'top': oy + 2.0, 'bottom': oy + 106.48, 'cx': x + 106, 'cy': cy}
    def label(self, x, y, s): self.items.append(text(x, [s], PRE, NOTE, y=y))
    def line(self, pts):
        """꺾인 연결선 — 시작점 고리, 모서리 반경 10, 마지막 방향으로 화살촉."""
        (ex, ey), (px, py) = pts[-1], pts[-2]
        L = math.hypot(ex - px, ey - py); ux, uy = (ex - px) / L, (ey - py) / L
        body = pts[:-1] + [(ex - ux * TIP_GAP, ey - uy * TIP_GAP)]
        d = [f'M{body[0][0]:.2f} {body[0][1]:.2f}']
        for i in range(1, len(body) - 1):
            (ax, ay), (bx, by), (cx, cy) = body[i - 1], body[i], body[i + 1]
            ia = math.hypot(bx - ax, by - ay); ib = math.hypot(cx - bx, cy - by)
            di, do = ((bx - ax) / ia, (by - ay) / ia), ((cx - bx) / ib, (cy - by) / ib)
            r = min(10, ia / 2, ib / 2); k = 0.5523 * r          # 사분원 베지어 — 덱 S자 선과 같은 반경 10
            s, e = (bx - di[0] * r, by - di[1] * r), (bx + do[0] * r, by + do[1] * r)
            d.append(f'L{s[0]:.2f} {s[1]:.2f}C{s[0] + di[0] * k:.2f} {s[1] + di[1] * k:.2f} {e[0] - do[0] * k:.2f} {e[1] - do[1] * k:.2f} {e[0]:.2f} {e[1]:.2f}')
        d.append(f'L{body[-1][0]:.2f} {body[-1][1]:.2f}')
        def rot(p):  # 오른쪽 기준 화살촉을 마지막 방향으로 돌려 끝점에 놓는다
            return (ex + p[0] * ux - p[1] * uy, ey + p[0] * uy + p[1] * ux)
        a = []
        for cmd, *ps in ARROW:
            a.append(cmd + ' '.join(f'{q[0]:.3f} {q[1]:.3f}' for q in map(rot, ps)))
        sx, sy = pts[0]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, y0 = min(xs) - 12, min(ys) - 12; x1, y1 = max(xs) + 12, max(ys) + 12
        w, h = x1 - x0, y1 - y0
        svg = (f'<svg width="{w:.2f}" height="{h:.2f}" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" fill="none" xmlns="http://www.w3.org/2000/svg">'
               f'<path d="{"".join(d)}" stroke="{BLUE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<path d="{"".join(a)}Z" fill="{BLUE}"/>'
               f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="10" fill="{BLUE}"/><circle cx="{sx:.2f}" cy="{sy:.2f}" r="6" fill="{LIGHT}"/></svg>')
        self.items.append({'type': 'svg', 'name': '연결선', 'x': x0, 'y': y0, 'svg': svg})
    def right(self, a, b):   # 가로 연결 — 고리는 앞 상자 오른쪽 끝, 화살촉 끝은 다음 상자 왼쪽 끝
        A, B = self.nodes[a], self.nodes[b]
        self.line([(A['right'] - 1, A['cy']), (B['left'] - 0.5, A['cy'])])

CY = 60
def overtime():
    f = Flow()
    f.box('admin', 0, CY, ['어드민 인정 기준 설정'], terminal=True, note=['연장 근무로 인정할 범위를', '회사마다 설정'])
    f.box('apply', 322, CY, ['연장 근무 신청'], note=['이번 주 누적 근로 시간을', '신청 화면에 실시간으로 표시', '주 52시간까지 남은 시간 확인'])
    f.box('split', 644, CY, ['연장 근무 시간', '자동 구분'], note=['출근부터 퇴근까지 머문 시간에서', '정규 근무를 뺀 나머지를', '연장 근무로 계산'])
    f.decision('check', 966, CY, ['정규 근무를', '채웠는가?'])
    d = f.nodes['check']
    f.box('approve', round(d['right'] + 131), CY, ['결재 상신 및 승인'])
    f.box('done', f.nodes['approve']['left'] + 322, CY, ['근태 기록 및', '수당 정산 반영'], terminal=True, note=['승인되면 근태 기록과', '수당 정산 데이터에 바로 반영'])
    f.box('block', d['cx'] - W / 2, d['bottom'] + 160 + 41.5, ['연장 근무 신청 차단'], terminal=True, note=['정규 근무 미달 시 신청 불가', '부적절한 수당 청구 차단'])
    f.right('admin', 'apply'); f.right('apply', 'split')
    f.line([(f.nodes['split']['right'] - 1, CY), (d['left'], CY)])
    f.line([(d['right'], CY), (f.nodes['approve']['left'] - 0.5, CY)])
    f.right('approve', 'done')
    f.line([(d['cx'], d['bottom']), (d['cx'], f.nodes['block']['top'] - 0.5)])
    f.label(d['right'] + 11, CY + 4, 'Y'); f.label(d['cx'] + 10, d['bottom'] + 9, 'N')
    return f

def holiday():
    f = Flow()
    f.box('apply', 0, CY, ['휴일 근무 신청'], terminal=True, note=['신청할 때 대체 휴가 발생 여부를', '시스템이 판단'])
    f.box('approve', 322, CY, ['결재 상신 및 승인'])
    f.decision('check', 644, CY, ['대체 휴가', '발생 대상인가?'])
    d = f.nodes['check']
    f.box('grant', round(d['right'] + 131), CY, ['대체 휴가 자동 부여'], note=['승인되면 바로 부여', '구성원과 관리자가 따로', '계산할 필요 없음'])
    f.box('done', f.nodes['grant']['left'] + 322, CY, ['근태 기록 및', '수당 정산 반영'], terminal=True)
    e = f.nodes['done']
    f.right('apply', 'approve')
    f.line([(f.nodes['approve']['right'] - 1, CY), (d['left'], CY)])
    f.line([(d['right'], CY), (f.nodes['grant']['left'] - 0.5, CY)])
    f.right('grant', 'done')
    f.line([(d['cx'], d['bottom']), (d['cx'], CY + 190), (e['cx'], CY + 190), (e['cx'], e['bottom'] + 0.5)])
    f.label(d['right'] + 11, CY + 4, 'Y'); f.label(d['cx'] + 10, d['bottom'] + 9, 'N')
    return f

# ── 결과 지표 그래프 — 덱 슬라이드 16 「정량적 변화 그래프 (Before vs After)」(1083:281916) 실측 ──
#   차트 간격 188 · Before 막대 x 0 / After 막대 x 64 · 폭 24 · 위 모서리 6 · 축 y 305 · 점선 격자 65 / 125 / 185 / 245(6 6, #DEE2E6)
#   Before #DEE2E6 · After 위 → 아래 #34C759 → #24C7AA · 값 글자 12/18 #868E96(막대 위 26) · Before / After 14/22 SemiBold #495057(축 아래 8)
#   말풍선 #212529 · 반경 4 · 좌우 6 위아래 2 · Bold 12/22 #F8F9FA · 꼬리 10.392×7(말풍선 왼쪽 7) · 값 글자 위 17
# 수치는 03 결과 표에 있는 것만: 검토 시간 하루 이상 → 5분 이내, 만족도 4.0 → 4.9. (부적절한 신청 0건은 이전 값이 없어 막대로 그리지 않는다.)
GRAY, GREEN = '#DEE2E6', ('#34C759', '#24C7AA')
TITLE_C, VALUE_C, TIP_BG, TIP_C = '#495057', '#868E96', '#212529', '#F8F9FA'
PRE_SB = {'family': 'Pretendard', 'style': 'SemiBold'}
PRE_R = {'family': 'Pretendard', 'style': 'Regular'}
TAIL = '<svg width="10.3923" height="7" viewBox="0 0 10.3923 7" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.4641 6C4.2339 7.33333 6.1584 7.33333 6.9282 6L10.3923 0H0L3.4641 6Z" fill="#212529"/></svg>'

def metrics():
    items, P, AXIS = [], 188, 305
    def t(lines, font, size, lh, tracking, color, **pos):
        d = {'type': 'text', 'lines': lines, 'font': font, 'size': size, 'lineHeight': lh, 'tracking': tracking, 'color': color, 'align': 'LEFT'}
        d.update(pos); return d
    for y in (65, 125, 185, 245):
        items.append({'type': 'line', 'x': 0, 'y': y, 'w': P + 88, 'color': GRAY, 'dash': [6, 6]})
    items.append({'type': 'line', 'x': 0, 'y': AXIS, 'w': P + 88, 'color': GRAY})
    charts = [
        # 제목, (Before 값 글자, 높이), (After 값 글자, 높이), 말풍선 — 검토 시간은 5분/24시간이 0.3% 라 After 막대를 보이는 최소 높이 10 으로 둔다
        ('연장 근무 검토 시간', ('하루 이상', 233), ('5분 이내', 10), '-98% 단축'),
        ('인사 담당자 만족도', ('4.0점', round(4.0 / 5 * 200)), ('4.9점', round(4.9 / 5 * 200)), '0.9점 상승'),   # 5점 = 200 으로 비례
    ]
    for i, (title, before, after, tip) in enumerate(charts):
        ox = i * P
        items.append(t([title], PRE_SB, 14, 22, -0.28, TITLE_C, x=ox, y=0))
        for j, (label, h) in enumerate((before, after)):
            bx = ox + 64 * j; top = AXIS - h
            bar = {'type': 'rect', 'name': ('Before ' if j == 0 else 'After ') + label, 'x': bx, 'y': top, 'w': 24, 'h': h, 'radii': [6, 6, 0, 0]}
            bar.update({'fill': GRAY} if j == 0 else {'gradient': GREEN})
            items.append(bar)
            items.append(t([label], PRE_R if j == 0 else PRE_SB, 12, 18, -0.24, VALUE_C, cx=bx + 12, y=top - 26))
            items.append(t(['Before' if j == 0 else 'After'], PRE_SB, 14, 22, -0.28, TITLE_C, cx=bx + 12, y=AXIS + 8))
            if j == 1:
                bottom = top - 26 - 17
                items.append({'type': 'tooltip', 'x': bx, 'y': bottom - 26, 'text': tip, 'font': PRE, 'size': 12, 'lineHeight': 22, 'tracking': -0.12,
                              'color': TIP_C, 'bg': TIP_BG, 'padX': 6, 'padY': 2, 'radius': 4})
                items.append({'type': 'svg', 'name': '꼬리', 'x': bx + 7, 'y': bottom, 'svg': TAIL})
    return items

PAGE = '03 주 52시간'
task = {
    'file': '포트폴리오_MCP',
    'renamePages': [['플로우차트', PAGE]],
    'draw': [
        {'page': PAGE, 'frame': '03 · 연장 근무 신청 플로우', 'x': 0, 'y': 0, 'export': 'gpro-overtime-flow', 'items': overtime().items},
        {'page': PAGE, 'frame': '03 · 휴일 근무 신청 플로우', 'x': 0, 'y': 700, 'export': 'gpro-holiday-flow', 'items': holiday().items},
        {'page': PAGE, 'frame': '03 · 결과 지표 그래프', 'x': 0, 'y': 1200, 'export': 'gpro-overtime-metrics', 'items': metrics()},
    ],
}
json.dump(task, open(sys.argv[1], 'w'), ensure_ascii=False)
print(sys.argv[1], sum(len(d['items']) for d in task['draw']), 'items')
