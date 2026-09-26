#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이디엠에듀케이션 세 프로젝트 플로우차트 → 플러그인 작업(JSON). 부품 · 치수는 flowkit.py(덱 08 실측).
내용은 projects.php 의 이디엠 글(사용자 경력기술서, 2026-09-26)에 적힌 것만 옮긴다.
  production 커리큘럼 개발 → 교안 제작 → 강의 녹화 → 편집 · 인강 제작 → AWS 서버 업로드 → LMS 강의 관리(사용자 설명, 2026-09-26)
  (정보구조도는 그림 대신 projects.php 의 표로 옮겼다 — 2026-09-26 사용자 요청)
  ielts   개선 전(흐린 줄) 게시글 목록 → 신청 방법을 찾았나(N 이탈) → 신청 글 → 관리자 수동 취합 / 개선 후 일정 선택 → 정보 입력 → 확인 · 접수 완료 → 명단 자동 생성
  global  해외 유학 준비생 → 해외 결제 → 무료 교재 해외배송(EMS) → AWS 로 강의 접속 → 수강
  business edm 유학원 → 아이엘츠 어학원 인수 → 아이엘츠 인강, 인강 수강생이 다시 유학 상담으로(개요 문제 정의)
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
    """유학원 → 어학원 인수 → 인강 — 사업이 넓어진 순서와, 인강 수강생이 다시 유학 상담으로 이어지는 흐름(개요 문제 정의)."""
    f = Flow()
    f.box('agency', X[0], CY, ['edm 유학원'], terminal=True, note=['유학 상담 · 수속', '수속이 끝나면 거래도 끝남', '입학 시기 · 비자 · 환율에 출렁임'])
    f.box('academy', X[1], CY, ['아이엘츠', '어학원 인수'], note=['시험 준비 단계의 고객을', '먼저 만남', '강의실 · 강사 시간 · 거리 안에서만'])
    f.box('online', X[2], CY, ['아이엘츠 인강'], terminal=True, note=['강의를 한 번 만들어 계속 판매', '전국 · 해외 어디서나 수강'])
    f.right('agency', 'academy'); f.right('academy', 'online')
    A, O = f.nodes['agency'], f.nodes['online']
    yb = CY + 190; xl = A['left'] - 40; xr = O['right'] + 40
    f.line([(O['right'] - 1, O['cy']), (xr, O['cy']), (xr, yb), (xl, yb), (xl, A['cy']), (A['left'] - 0.5, A['cy'])])
    f.label(f.nodes['academy']['left'] - 6, yb - 32, '시험을 마친 수강생이 유학 상담으로')
    f.pill('online', '신규 사업')
    return f

def draws():
    P = '이디엠에듀케이션'
    return [
        {'page': P, 'frame': '이디엠 · 유학원에서 인강까지', 'x': 0, 'y': 2100, 'export': 'edm-business-flow', 'items': business().items},
        {'page': P, 'frame': '이디엠 · 강의 제작부터 관리까지', 'x': 0, 'y': 0, 'export': 'edm-production-flow', 'items': production().items},
        {'page': P, 'frame': '이디엠 · 모의고사 접수 개편 전후', 'x': 0, 'y': 700, 'export': 'edm-ielts-flow', 'items': ielts().items},
        {'page': P, 'frame': '이디엠 · 해외 수강생이 수강까지', 'x': 0, 'y': 1400, 'export': 'edm-global-flow', 'items': global_().items},
    ]

if __name__ == '__main__':
    write_task(sys.argv[1], draws())
