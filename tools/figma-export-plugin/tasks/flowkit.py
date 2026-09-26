#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
덱 스타일 플로우차트 부품 — 작업 파일(tasks/*.py)이 함께 쓴다.

덱 슬라이드 08 의 플로우차트(GPRO_PORTFOLIO 1958:5268)와 같은 부품 · 치수(2026-09-26, get_design_context 실측):
  시작끝     #688DF1 면 · 4px 테두리 · 반경 6 · 폭 200 · 위아래 30 · Apple SD Gothic Neo Bold 15/23 흰 글자 · 자간 -0.6
  텍스트 박스 #ECF1FD 면 · #688DF1 4px 테두리 · 같은 치수 · Pretendard Bold 15/23 #4270ED
  선택지     212×110 마름모(덱 벡터 그대로) · Apple SD Gothic Neo Bold 15/23 #4270ED
  기본(연결선) #688DF1 4px 선 · 시작점 고리(r10 · 안쪽 r6 #ECF1FD) · 끝 화살촉(덱 벡터 그대로) · 모서리 반경 10
  박스 코멘트 Pretendard Bold 15/23 #ADB5BD · 상자 아래 16
  말풍선     #212529 · 반경 4 · 좌우 6 위아래 2 · Pretendard Bold 12/22 #F8F9FA · 꼬리 10.392×7(덱 16 그래프 말풍선)
상자 간격은 덱과 같이 322(상자 200 + 간격 122) — 웹에서 02 의 플로우차트와 같은 배율로 보이게.
"""
import math

BLUE, TEXT_BLUE, LIGHT, NOTE, WHITE = '#688DF1', '#4270ED', '#ECF1FD', '#ADB5BD', '#FFFFFF'
MUTED_LINE, MUTED_FACE, MUTED_INK = '#ADB5BD', '#F1F3F5', '#868E96'   # 개선 전 줄 — 덱 회색(차트 Before 막대 · 코멘트와 같은 계열)
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
TIP_GAP = 17.45
TAIL = '<svg width="10.3923" height="7" viewBox="0 0 10.3923 7" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.4641 6C4.2339 7.33333 6.1584 7.33333 6.9282 6L10.3923 0H0L3.4641 6Z" fill="#212529"/></svg>'                    # 선은 화살촉 끝보다 이만큼 앞에서 끝난다(덱: 82 → 99.45)

def text(x, lines, font, color, cy=None, y=None, w=None, align='LEFT'):
    t = {'type': 'text', 'x': x, 'lines': lines, 'font': font, 'size': SIZE, 'lineHeight': LH, 'tracking': TRACK, 'color': color, 'align': align}
    if w: t['w'] = w
    if cy is not None: t['cy'] = cy
    else: t['y'] = y
    return t

class Flow:
    def __init__(self): self.items, self.nodes = [], {}
    def box(self, key, x, cy, lines, terminal=False, note=None, muted=False):
        h = 2 * PAD + LH * len(lines); top = cy - h / 2
        line, face, ink = (MUTED_LINE, MUTED_FACE, MUTED_INK) if muted else (BLUE, LIGHT, TEXT_BLUE)
        self.items.append({'type': 'rect', 'name': ' '.join(lines), 'x': x, 'y': top, 'w': W, 'h': h, 'fill': line if terminal else face, 'stroke': line, 'strokeWeight': 4, 'radius': 6})
        self.items.append(text(x + 20, lines, SD if terminal else PRE, WHITE if terminal else ink, cy=cy, w=160, align='CENTER'))
        if note: self.items.append(text(x, note, PRE, NOTE, y=top + h + 16))
        self.nodes[key] = {'left': x, 'right': x + W, 'top': top, 'bottom': top + h, 'cx': x + W / 2, 'cy': cy}
    def decision(self, key, x, cy, lines, muted=False):
        top = cy - 55
        line, face, ink = (MUTED_LINE, MUTED_FACE, MUTED_INK) if muted else (BLUE, LIGHT, TEXT_BLUE)
        svg = f'<svg width="{DW}" height="{DH}" viewBox="0 0 {DW} {DH}" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="{DIAMOND}" fill="{face}" stroke="{line}" stroke-width="4"/></svg>'
        self.items.append({'type': 'svg', 'name': ' '.join(lines), 'x': x + 7.04, 'y': top + 0.825, 'svg': svg})
        self.items.append(text(x + 39, lines, SD, ink, cy=cy, w=134, align='CENTER'))
        ox, oy = x + 7.04, top + 0.825      # 벡터 꼭짓점(곡선 끝 포함) — 왼 2.0 · 오 195.94 · 위 2.0 · 아래 106.48
        self.nodes[key] = {'left': ox + 2.0, 'right': ox + 195.94, 'top': oy + 2.0, 'bottom': oy + 106.48, 'cx': x + 106, 'cy': cy}
    def label(self, x, y, s): self.items.append(text(x, [s], PRE, NOTE, y=y))
    def line(self, pts, muted=False):
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
        c, ring = (MUTED_LINE, MUTED_FACE) if muted else (BLUE, LIGHT)
        svg = (f'<svg width="{w:.2f}" height="{h:.2f}" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" fill="none" xmlns="http://www.w3.org/2000/svg">'
               f'<path d="{"".join(d)}" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<path d="{"".join(a)}Z" fill="{c}"/>'
               f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="10" fill="{c}"/><circle cx="{sx:.2f}" cy="{sy:.2f}" r="6" fill="{ring}"/></svg>')
        self.items.append({'type': 'svg', 'name': '연결선', 'x': x0, 'y': y0, 'svg': svg})
    def right(self, a, b, muted=False):   # 가로 연결 — 고리는 앞 상자 오른쪽 끝, 화살촉 끝은 다음 상자 왼쪽 끝
        A, B = self.nodes[a], self.nodes[b]
        self.line([(A['right'] - 1, A['cy']), (B['left'] - 0.5, A['cy'])], muted=muted)
    def left(self, a, b):    # 오른쪽 → 왼쪽 연결(두 번째 줄을 거꾸로 흐를 때)
        A, B = self.nodes[a], self.nodes[b]
        self.line([(A['left'] + 1, A['cy']), (B['right'] + 0.5, A['cy'])])
    def pill(self, key, s):  # 상자 위 검은 말풍선 — 꼬리 끝이 상자 위 4px 앞
        N = self.nodes[key]; x, top = N['left'], N['top']
        self.items.append({'type': 'tooltip', 'name': s, 'x': x, 'y': top - 4 - 7 - 26, 'text': s, 'font': PRE, 'size': 12, 'lineHeight': 22, 'tracking': -0.12,
                           'color': '#F8F9FA', 'bg': '#212529', 'padX': 6, 'padY': 2, 'radius': 4})
        self.items.append({'type': 'svg', 'name': '꼬리', 'x': x + 7, 'y': top - 4 - 7, 'svg': TAIL})



def write_task(path, draws, file='포트폴리오_MCP', rename=None):
    """작업 JSON 쓰기 — draws: [{page, frame, x, y, export, items}]"""
    import json
    task = {'file': file, 'draw': draws}
    if rename: task['renamePages'] = rename
    json.dump(task, open(path, 'w'), ensure_ascii=False)
    print(path, sum(len(d['items']) for d in draws), 'items ·', ', '.join(d['export'] for d in draws))
