#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04 IR · 전환 지표 패널 → 플러그인 작업(JSON). 덱 슬라이드 12(1083:281117) 도넛 · 큰 숫자 실측으로 그린다(2026-09-26):
  도넛 210 · 두께 40(바깥 r105 · 안 r65) · 바탕 #F1F3F5 · 호 #34C759 → #24C7AA · 12시에서 시계 방향 · 가운데 값 Bold 32/32 그라디언트
  제목 Bold 18 #212529 · 회색 배지 #ADB5BD SemiBold 12/14 흰 글 · 항목 이름 SemiBold 14 #495057 · 큰 숫자 ExtraBold 62/62 자간 -3.1 그라디언트
수치는 2023년 4월 실측 전환 지표만(메모리 gpro-ir-figures-are-projections) — 호의 길이는 값 그대로.
사용: python3 tools/figma-export-plugin/tasks/ir_kpi.py <작업 JSON 경로>
"""
import math, sys
from flowkit import write_task

GREEN = ('#34C759', '#24C7AA')
INK, BODY, MUTED, TRACK = '#212529', '#495057', '#868E96', '#F1F3F5'
F = lambda style: {'family': 'Pretendard', 'style': style}

def text(x, y, s, style, size, lh, tracking, color=None, gradient=None, cx=None, cy=None):
    t = {'type': 'text', 'lines': [s], 'font': F(style), 'size': size, 'lineHeight': lh, 'tracking': tracking, 'color': color or INK, 'align': 'LEFT', 'x': x, 'y': y}
    if gradient: t['gradient'] = gradient
    if cx is not None: t['cx'] = cx
    if cy is not None: t['cy'] = cy; t.pop('y')
    return t

def donut(pct):
    R, r, c = 105, 65, 105
    def pt(rad, ang):   # ang: 12시 기준 시계 방향(도)
        a = math.radians(ang - 90)
        return c + rad * math.cos(a), c + rad * math.sin(a)
    track = (f'M{c} {c-R}A{R} {R} 0 1 1 {c-0.01} {c-R}Z M{c} {c-r}A{r} {r} 0 1 0 {c+0.01} {c-r}Z')
    ang = 360 * pct / 100
    large = 1 if ang > 180 else 0
    (x1, y1), (x2, y2), (x3, y3) = pt(R, 0), pt(R, ang), pt(r, ang)
    arc = (f'M{x1:.3f} {y1:.3f}A{R} {R} 0 {large} 1 {x2:.3f} {y2:.3f}L{x3:.3f} {y3:.3f}A{r} {r} 0 {large} 0 {c} {c-r}Z')
    return ('<svg width="210" height="210" viewBox="0 0 210 210" fill="none" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{track}" fill="{TRACK}" fill-rule="evenodd"/>'
            f'<path d="{arc}" fill="url(#g)"/>'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="222.682" y2="14.4411" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{GREEN[0]}"/><stop offset="1" stop-color="{GREEN[1]}"/></linearGradient></defs></svg>')

def panel():
    items = [text(0, 0, '전환 지표', 'Bold', 18, 22, -0.36),
             {'type': 'tooltip', 'name': '기준', 'x': 88, 'y': 0, 'text': '2023년 4월 기준', 'font': F('SemiBold'), 'size': 12, 'lineHeight': 14, 'tracking': -0.12,
              'color': '#F8F9FA', 'bg': '#ADB5BD', 'padX': 8, 'padY': 4, 'radius': 4}]
    donuts = [('온라인 데모 후 서비스 시작', 36.7, '36.7%', '도입 예정까지 포함하면 51.8%'),
              ('방문 PT 후 유료 전환', 63.3, '63.3%', '방문 PT를 본 고객 기준'),
              ('서비스 추천 의향', 73, '73%', '프로세스를 경험한 고객 기준')]
    for i, (label, pct, val, note) in enumerate(donuts):
        x0 = i * 245
        items.append(text(x0, 50, label, 'SemiBold', 14, 18, -0.14, BODY))
        items.append({'type': 'svg', 'name': f'도넛 {val}', 'x': x0, 'y': 82, 'svg': donut(pct)})
        items.append(text(0, 0, val, 'Bold', 32, 32, -0.64, gradient=GREEN, cx=x0 + 105, cy=82 + 105))
        items.append(text(x0, 82 + 210 + 16, note, 'Regular', 14, 20, -0.14, MUTED))
    items.append({'type': 'rect', 'name': '구분선', 'x': 725, 'y': 50, 'w': 1, 'h': 278, 'fill': '#DEE2E6'})
    stats = [('0%', '프로세스를 경험한 유료 고객 이탈률'), ('64.1일', '데모 후 서비스 시작까지 평균')]
    for j, (big, label) in enumerate(stats):
        y0 = 44 + j * 150
        items.append(text(765, y0, big, 'ExtraBold', 62, 62, -3.1, gradient=GREEN))
        items.append(text(765, y0 + 74, label, 'SemiBold', 14, 18, -0.14, BODY))
    return items

def draws():
    return [{'page': '04 IR', 'frame': '04 · 전환 지표', 'x': 0, 'y': 0, 'export': 'gpro-ir-kpi', 'items': panel()}]

if __name__ == '__main__':
    write_task(sys.argv[1], draws())
