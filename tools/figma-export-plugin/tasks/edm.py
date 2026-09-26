#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이디엠에듀케이션 세 프로젝트 플로우차트 → 플러그인 작업(JSON). 부품 · 치수는 flowkit.py(덱 08 실측).
내용은 projects.php 의 이디엠 글(사용자 경력기술서, 2026-09-26)에 적힌 것만 옮긴다.
  online  강의 제작 → 콘텐츠 업로드 → 수강 신청 · 결제 → 수강 → 수강생 통합 관리 / 결제 → 교재 배송 연동 / 오프라인 학원 수강생 → 통합 관리
  ielts   개선 전(흐린 줄) 익명 게시판 신청 → 관리자 수동 취합 / 개선 후 단계별 신청 → 자동 취합
  global  해외 유학 준비생 → 해외 결제 → 무료 교재 해외배송(EMS) → AWS 로 강의 접속 → 수강
  business edm 유학원 → 아이엘츠 어학원 인수 → 아이엘츠 인강, 인강 수강생이 다시 유학 상담으로(개요 문제 정의)
사용: python3 tools/figma-export-plugin/tasks/edm.py <작업 JSON 경로>
"""
import sys
from flowkit import *

CY = 60
X = [0, 322, 644, 966, 1288, 1610]

def online():
    f = Flow()
    f.box('make', X[0], CY, ['강의 제작'], terminal=True, note=['인강 콘텐츠 제작 프로세스', '강사용 매뉴얼'])
    f.box('upload', X[1], CY, ['콘텐츠 업로드'], note=['강의 영상과 자료 등록'])
    f.box('pay', X[2], CY, ['수강 신청 · 결제'])
    f.box('learn', X[3], CY, ['수강'], note=['영상 스트리밍', '학습 관리'])
    f.box('manage', X[4], CY, ['수강생 통합 관리'], terminal=True)
    CY2 = CY + 230
    f.box('book', X[2], CY2, ['교재 배송 연동'], note=['결제와 함께 교재 배송'])
    f.box('offline', X[3], CY2, ['오프라인', '학원 수강생'], terminal=True, note=['온라인 강의와 함께 관리'])
    f.right('make', 'upload'); f.right('upload', 'pay'); f.right('pay', 'learn'); f.right('learn', 'manage')
    P, B, O, M = f.nodes['pay'], f.nodes['book'], f.nodes['offline'], f.nodes['manage']
    f.line([(P['cx'], P['bottom']), (P['cx'], B['top'] - 0.5)])
    f.line([(O['right'] - 1, O['cy']), (M['cx'], O['cy']), (M['cx'], M['bottom'] + 0.5)])
    return f

def ielts():
    f = Flow()
    CY2 = CY + 240
    f.box('b1', X[0], CY, ['신청 사이트 접속'], terminal=True, muted=True)
    f.box('b2', X[1], CY, ['익명 게시판에', '신청 글 작성'], muted=True, note=['첫 화면에서 신청 방법이', '보이지 않아 이탈'])
    f.box('b3', X[2], CY, ['관리자가', '수동으로 취합'], muted=True, note=['게시글을 하나씩 모아 정리'])
    f.box('b4', X[3], CY, ['접수 명단'], terminal=True, muted=True)
    f.box('a1', X[0], CY2, ['신청 화면 접속'], terminal=True, note=['모바일 · 웹'])
    f.box('a2', X[1], CY2, ['단계를 따라', '신청'], note=['신청에 필요한 정보를', '차례로 입력'])
    f.box('a3', X[2], CY2, ['접수 데이터', '자동 취합'], note=['관리자 취합 작업 없음'])
    f.box('a4', X[3], CY2, ['접수 완료'], terminal=True)
    for a, b in (('b1', 'b2'), ('b2', 'b3'), ('b3', 'b4')):
        f.right(a, b, muted=True)
    for a, b in (('a1', 'a2'), ('a2', 'a3'), ('a3', 'a4')):
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
        {'page': P, 'frame': '이디엠 · 온라인 인강 서비스 구조', 'x': 0, 'y': 0, 'export': 'edm-online-flow', 'items': online().items},
        {'page': P, 'frame': '이디엠 · 모의고사 접수 개편 전후', 'x': 0, 'y': 700, 'export': 'edm-ielts-flow', 'items': ielts().items},
        {'page': P, 'frame': '이디엠 · 해외 수강생이 수강까지', 'x': 0, 'y': 1400, 'export': 'edm-global-flow', 'items': global_().items},
    ]

if __name__ == '__main__':
    write_task(sys.argv[1], draws())
