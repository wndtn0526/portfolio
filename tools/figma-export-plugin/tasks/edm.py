#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이디엠에듀케이션 세 프로젝트 플로우차트 → 플러그인 작업(JSON). 부품 · 치수는 flowkit.py(덱 08 실측).
내용은 projects.php 의 이디엠 글(사용자 경력기술서, 2026-09-26)에 적힌 것만 옮긴다.
  production 커리큘럼 개발 → 교안 제작 → 강의 녹화 → 편집 · 인강 제작 → AWS 서버 업로드 → LMS 강의 관리(사용자 설명, 2026-09-26)
  (정보구조도는 그림 대신 projects.php 의 표로 옮겼다 — 2026-09-26 사용자 요청)
  ielts   개선 전(흐린 줄) 게시글 목록 → 신청 방법을 찾았나(N 이탈) → 신청 글 → 관리자 수동 취합 / 개선 후 일정 선택 → 정보 입력 → 확인 · 접수 완료 → 명단 자동 생성
  global  해외 유학 준비생 → 해외 결제 → 무료 교재 해외배송(EMS) → AWS 로 강의 접속 → 수강
  business edm에듀케이션 유학원 → 아이엘츠 어학원 인수 → 아이엘츠 인강, 인강 수강생이 다시 유학 상담으로(개요 사업 확장 이유)
  funnel  개편 전 모의고사 접수 퍼널(도식) — 단계와 이탈이 몰린 첫 화면만. 수치는 경력기술서에 없어 넣지 않는다
  ⚠️ 회사 이름은 edm 이 아니라 edm에듀케이션(사용자, 2026-09-27)
사용: python3 tools/figma-export-plugin/tasks/edm.py <작업 JSON 경로>
"""
import sys
from flowkit import *

CY = 60
X = [0, 322, 644, 966, 1288, 1610]

def production():
    """강의가 만들어져 수강생에게 가기까지(2026-09-26 사용자 설명): 커리큘럼 개발 → 교안 제작 → 강의 녹화 → 편집 · 인강 제작 → AWS 서버 업로드 → LMS 강의 관리."""
    f = Flow()
    f.box('curri', X[0], CY, ['커리큘럼 개발'], terminal=True, note=['제작 과정을 정의하고', '강사용 매뉴얼로 정리'])
    f.box('text', X[1], CY, ['교안 제작'])
    f.box('rec', X[2], CY, ['강의 녹화'])
    f.box('edit', X[3], CY, ['편집 · 인강 제작'])
    f.box('up', X[4], CY, ['AWS 서버 업로드'], note=['국내 · 해외 어디서나', '끊기지 않고 수강'])
    f.box('lms', X[5], CY, ['LMS 강의 관리'], terminal=True, note=['강의와 수강을 관리'])
    for a_, b_ in (('curri', 'text'), ('text', 'rec'), ('rec', 'edit'), ('edit', 'up'), ('up', 'lms')):
        f.right(a_, b_)
    f.pill('up', '해외 수강까지')
    return f

def ielts():
    """모의고사 신청 개편 전후(경력기술서 + projects.php 02 글). 개선 전은 흐린 줄 — 첫 화면(게시글 목록)에서 신청 방법을 못 찾으면 이탈."""
    f = Flow()
    f.box('b1', X[0], CY, ['신청 사이트 접속'], terminal=True, muted=True)
    f.box('b2', X[1], CY, ['익명 게시판', '글 목록'], muted=True, note=['첫 화면에', '다른 사람의 신청 글만 보임'])
    f.decision('q', X[2], CY, ['신청 방법을', '찾았는가?'], muted=True)
    d = f.nodes['q']
    f.box('b3', round(d['right'] + 131), CY, ['신청 글 작성'], muted=True, note=['적는 방식이 사람마다 제각각'])
    f.box('b4', f.nodes['b3']['left'] + 322, CY, ['관리자가', '수동으로 취합'], muted=True, note=['글을 하나씩 열어', '명단으로 옮겨 적음'])
    f.box('out', d['cx'] - W / 2, d['bottom'] + 160 + 41.5, ['이탈'], terminal=True, muted=True, note=['이탈이 매우 높았던 구간'])
    f.right('b1', 'b2', muted=True)
    f.line([(f.nodes['b2']['right'] - 1, CY), (d['left'], CY)], muted=True)
    f.line([(d['right'], CY), (f.nodes['b3']['left'] - 0.5, CY)], muted=True)
    f.right('b3', 'b4', muted=True)
    f.line([(d['cx'], d['bottom']), (d['cx'], f.nodes['out']['top'] - 0.5)], muted=True)
    f.label(d['right'] + 11, CY + 4, 'Y'); f.label(d['cx'] + 10, d['bottom'] + 9, 'N')
    CY2 = CY + 500
    f.box('a1', X[0], CY2, ['신청 화면 접속'], terminal=True, note=['모바일 · 웹'])
    f.box('a2', X[1], CY2, ['모의고사', '일정 선택'], note=['첫 화면에서 바로 시작'])
    f.box('a3', X[2], CY2, ['응시자 정보 입력'], note=['꼭 필요한 항목만', '화면마다 한 가지씩'])
    f.box('a4', X[3], CY2, ['신청 확인 후', '접수 완료'], note=['신청한 일정과 정보를', '다시 보여 줌'])
    f.box('a5', X[4], CY2, ['접수 명단', '자동 생성'], terminal=True, note=['관리자 취합 작업 없음'])
    for a, b in (('a1', 'a2'), ('a2', 'a3'), ('a3', 'a4'), ('a4', 'a5')):
        f.right(a, b)
    f.pill('b1', '개선 전'); f.pill('a1', '개선 후')
    return f

def global_():
    f = Flow()
    f.box('who', X[0], CY, ['해외 유학 준비생'], terminal=True, note=['교재 구매와 접속 품질 때문에', '수강을 망설임'])
    f.box('pay', X[1], CY, ['해외 결제'])
    f.box('book', X[2], CY, ['무료 교재', '해외배송'], note=['우체국 EMS 별도 계약으로', '배송비 절감'])
    f.box('aws', X[3], CY, ['AWS로', '강의 접속'], note=['국내 인강 최초', 'AWS 클라우드 도입'])
    f.box('learn', X[4], CY, ['수강'], terminal=True)
    f.right('who', 'pay'); f.right('pay', 'book'); f.right('book', 'aws'); f.right('aws', 'learn')
    f.pill('book', '프로모션'); f.pill('aws', '인프라')
    return f

def business():
    """유학원 → 어학원 인수 → 인강(처음 그린 판). ⚠️ 사용자가 Figma 에서 고친 뒤로는 draws() 에 넣지 않는다 — 원본은 포트폴리오_MCP 105:1056."""
    f = Flow()
    f.box('agency', X[0], CY, ['edm에듀케이션', '유학원'], terminal=True, note=['유학 상담 · 수속', '수속이 끝나면 거래도 끝남', '입학 시기 · 비자 · 환율에 출렁임'])
    f.box('academy', X[1], CY, ['아이엘츠', '어학원 인수'], note=['시험 준비 단계의 고객을', '먼저 만남', '강의실 · 강사 시간 · 거리 안에서만'])
    f.box('online', X[2], CY, ['아이엘츠 인강'], terminal=True, note=['강의를 한 번 만들어 계속 판매', '전국 · 해외 어디서나 수강'])
    f.right('agency', 'academy'); f.right('academy', 'online')
    A, O = f.nodes['agency'], f.nodes['online']
    yb = CY + 190; xl = A['left'] - 40; xr = O['right'] + 40
    f.line([(O['right'] - 1, O['cy']), (xr, O['cy']), (xr, yb), (xl, yb), (xl, A['cy']), (A['left'] - 0.5, A['cy'])])
    f.label(f.nodes['academy']['left'] - 6, yb - 32, '시험을 마친 수강생이 유학 상담으로')
    f.pill('online', '신규 사업')
    return f

def _rpoly(pts, r=6):
    """모서리를 반경 r 로 굴린 다각형 path."""
    import math
    def toward(p, q, d):
        L = math.hypot(q[0] - p[0], q[1] - p[1]); return (p[0] + (q[0] - p[0]) * d / L, p[1] + (q[1] - p[1]) * d / L)
    out = []
    for i in range(len(pts)):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
        a, b = toward(p1, p0, r), toward(p1, p2, r)
        out.append(('M' if i == 0 else 'L') + f'{a[0]:.2f} {a[1]:.2f}Q{p1[0]:.2f} {p1[1]:.2f} {b[0]:.2f} {b[1]:.2f}')
    return ''.join(out) + 'Z'

def _layer(f, cx, y, h, tw, bw, lines, solid, muted=False):
    """깔때기 한 층 — 윗변 tw · 아랫변 bw 사다리꼴, 가운데 글. 선 2(1:1 로 보이는 그림)."""
    line = MUTED_LINE if muted else BLUE
    face = line if solid else (MUTED_FACE if muted else LIGHT)
    ink = WHITE if solid else (MUTED_INK if muted else TEXT_BLUE)
    pts = [(cx - tw / 2, y), (cx + tw / 2, y), (cx + bw / 2, y + h), (cx - bw / 2, y + h)]
    x0, y0, w, hh = cx - tw / 2 - 2, y - 2, tw + 4, h + 4
    svg = (f'<svg width="{w}" height="{hh}" viewBox="{x0} {y0} {w} {hh}" fill="none" xmlns="http://www.w3.org/2000/svg">'
           f'<path d="{_rpoly(pts)}" fill="{face}" stroke="{line}" stroke-width="2"/></svg>')
    f.items.append({'type': 'svg', 'name': lines[0], 'x': x0, 'y': y0, 'svg': svg})
    f.items.append(text(cx - 110, lines, SD if solid else PRE, ink, cy=y + h / 2, w=220, align='CENTER'))

def _heading(f, x, s, color):
    """도식 머리 — 기간(2018년 2분기 · 3분기, 사용자). 본문 글자보다 크게."""
    t = text(x, [s], SD, color, cy=14); t['size'] = 18; t['lineHeight'] = 26
    f.items.append(t)

def _pill(f, x, y_top, s, bg='#212529'):
    """글 위 말풍선 — y_top 은 말풍선이 가리키는 글의 윗변."""
    f.items.append({'type': 'tooltip', 'name': s, 'x': x, 'y': y_top - 4 - 7 - 26, 'text': s, 'font': PRE, 'size': 12, 'lineHeight': 22, 'tracking': -0.12,
                    'color': '#F8F9FA', 'bg': bg, 'padX': 6, 'padY': 2, 'radius': 4})
    f.items.append({'type': 'svg', 'name': '꼬리', 'x': x + 7, 'y': y_top - 4 - 7, 'svg': TAIL.replace('#212529', bg)})

# 퍼널 예시 수치 — 경력기술서에 단계별 수치가 없어 사용자가 정하게 했다(「알아서 넣어줘」 → 「분기 기준으로」, 2026-09-27).
#   실측은 「개편 전 분기 대비 신청자 150% 증가」 하나 — 신청 완료를 320 → 800 명으로 맞췄다. 도식에 예시라고 적는다.
BEFORE = [('첫 화면 · 게시글 목록', 3200), ('게시글 열람', 960), ('신청 글 작성', 450), ('신청 완료', 320)]
AFTER = [('첫 화면 · 모의고사 일정', 3300), ('일정 선택', 1820), ('응시자 정보 입력', 1060), ('신청 완료', 800)]

def funnel():
    """개편 전 모의고사 접수 퍼널 — 1:1 로 보이는 도식(글자 15 · 선 2). 층마다 인원, 오른쪽에 빠져나간 인원과 이유."""
    f = Flow()
    CX, AX = 220, 512                     # 깔때기 가운데 · 오른쪽 설명 칸
    geo = [(40, 96, 440, 220), (146, 64, 220, 188), (220, 64, 188, 156), (294, 64, 156, 124)]
    why = [['신청 방법이 보이지 않아', '게시글 목록에서 바로 나감'], ['다른 사람의 글을 열어 적는 방식을 확인'],
           ['정해진 양식 없이 자유롭게 작성'], ['관리자가 글을 옮겨 적어 명단에 반영']]
    _heading(f, 0, '2018년 2분기 (개편 전)', '#212529')
    for i, ((y, h, tw, bw), (name, c)) in enumerate(zip(geo, BEFORE)):
        _layer(f, CX, y, h, tw, bw, [name, f'{c:,}명'], i == 0)
        cy = y + h / 2; edge = CX + (tw + bw) / 4
        if i == 0:                        # 첫 화면 — 이탈이 몰린 곳
            f.line([(edge + 1, cy), (AX - 12, cy)], k=0.5)
            f.items.append(text(AX, [f'첫 화면에서 {c - BEFORE[1][1]:,}명 이탈'], SD, '#212529', cy=cy))
            f.items.append(text(AX, why[0], PRE, NOTE, y=cy + 11.5 + 6))
            _pill(f, AX, cy - 11.5, '이탈 집중')
        elif i < 3:                       # 다음 단계로 못 간 인원 + 이유
            f.items.append({'type': 'line', 'name': '점선', 'x': edge + 8, 'y': cy - 11.5, 'w': AX - 12 - edge - 8, 'color': NOTE, 'weight': 1.5, 'dash': [4, 4]})
            f.items.append(text(AX, [f'{c - BEFORE[i + 1][1]:,}명 이탈'], SD, MUTED_INK, cy=cy - 11.5))
            f.items.append(text(AX, why[i], PRE, NOTE, cy=cy + 11.5))
        else:                             # 신청 완료
            f.items.append({'type': 'line', 'name': '점선', 'x': edge + 8, 'y': cy, 'w': AX - 12 - edge - 8, 'color': NOTE, 'weight': 1.5, 'dash': [4, 4]})
            f.items.append(text(AX, why[i], PRE, NOTE, cy=cy))
    f.items.append(text(0, ['단계별 수치는 예시'], PRE, NOTE, y=294 + 64 + 24))
    return f

def funnel_compare():
    """개편 전후 분기 모의고사 접수 퍼널을 나란히 — 예시 수치(분기 기준). 층 폭은 유입 대비 비율에 맞춰 좁아진다."""
    f = Flow()
    ys = [(40, 72), (120, 60), (188, 60), (256, 60)]
    for cx, muted, tag, st in ((150, True, '2018년 2분기 (개편 전)', BEFORE), (600, False, '2018년 3분기 (개편 후)', AFTER)):
        wid = lambda c, top=st[0][1]: 120 + 180 * c / top
        for i, ((name, c), (y, h)) in enumerate(zip(st, ys)):
            tw = wid(c); bw = wid(st[i + 1][1]) if i + 1 < len(st) else tw - 24
            _layer(f, cx, y, h, tw, bw, [name, f'{c:,}명'], i == 0, muted)
            if i + 1 < len(st):
                cy = y + h / 2; edge = cx + (tw + bw) / 4; lx = cx + 174
                f.line([(edge + 1, cy), (lx - 8, cy)], muted=muted, k=0.5)
                ink = '#212529' if (muted and i == 0) else (MUTED_INK if muted else TEXT_BLUE)
                f.items.append(text(lx, [f'{c - st[i + 1][1]:,}명 이탈'], SD, ink, cy=cy))
        _heading(f, cx - 150, tag, '#212529' if muted else TEXT_BLUE)
    f.items.append(text(220, [f'신청 완료 {BEFORE[-1][1]:,}명 → {AFTER[-1][1]:,}명 · 150% 증가'], SD, '#212529', cy=356, w=440, align='CENTER'))
    f.items.append(text(170, ['신청자 150% 증가만 실측, 단계별 수치는 예시'], PRE, NOTE, cy=386, w=540, align='CENTER'))
    return f

def draws():
    P = '이디엠에듀케이션'
    return [
        # 사업 확장 도식은 사용자가 Figma 에서 고쳤다(105:1056, 2026-09-27) — 다시 그리면 같은 이름 프레임이 지워진다. 내보내기만: task.export [['105:1056', 'edm-business-flow']]
        {'page': P, 'frame': '이디엠 · 강의 제작부터 관리까지', 'x': 0, 'y': 0, 'export': 'edm-production-flow', 'items': production().items},
        {'page': P, 'frame': '이디엠 · 모의고사 접수 개편 전후', 'x': 0, 'y': 700, 'export': 'edm-ielts-flow', 'items': ielts().items},
        {'page': P, 'frame': '이디엠 · 모의고사 접수 퍼널', 'x': 2200, 'y': 700, 'export': 'edm-ielts-funnel', 'items': funnel().items},
        {'page': P, 'frame': '이디엠 · 모의고사 접수 퍼널 개편 전후', 'x': 3200, 'y': 700, 'export': 'edm-ielts-funnel-compare', 'items': funnel_compare().items},
        {'page': P, 'frame': '이디엠 · 해외 수강생이 수강까지', 'x': 0, 'y': 1400, 'export': 'edm-global-flow', 'items': global_().items},
    ]

if __name__ == '__main__':
    write_task(sys.argv[1], draws())
