#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
청담원 두 세부 프로젝트 플로우차트 → 플러그인 작업(JSON). 부품 · 치수는 flowkit.py(덱 08 실측).
  careplan  초기상담 기록지 → 매핑 규칙 적용 → 케어플랜 초안 → 방문 욕구사정 반영 → 담당자 검토 → 저장 · 확정
            (규칙 엔진 · 담당자 판단 말풍선. 근거: 저장소 CarePlanDraftService · CarePlanMatch 머리 주석, content-plan 2-6 ②)
  pipeline  기획(컨플루언스) → 이슈(지라) → 디자인(피그마 MCP) → 구현(Claude Code) → 검증(Playwright) → 문서화
            └ 둘째 줄(오른쪽 → 왼쪽): 주간보고 초안 → 보고 메일 → 비개발 이해관계자 (예약 에이전트 말풍선)
  service   무료 상담 신청 → 상담관리 → 계약 · 수급자 등록 → 구인 공고 · 채용 ↓ 직원 등록 · 공단 신고 → 방문 일정 → 방문 · 기록 → 보호자 마이페이지(01 개요)
⚠️ 회사 자료 원문 · 화면 · 사람 이름은 넣지 않는다. 수치는 projects.php 청담원 글과 같다.
사용: python3 tools/figma-export-plugin/tasks/cdw.py <작업 JSON 경로>
"""
import sys
from flowkit import *

CY = 60
X = [0, 322, 644, 966, 1288, 1610]

def careplan():
    f = Flow()
    f.box('intake', X[0], CY, ['초기상담 기록지'], terminal=True)
    f.box('rule', X[1], CY, ['매핑 규칙', '적용'], note=['척도 단계를 문구로', '법정 금지 항목은 꺼 둠'])
    f.box('draft', X[2], CY, ['케어플랜 초안'], note=['중점과 주차별 돌봄 계획'])
    f.box('need', X[3], CY, ['방문 욕구사정', '반영'], note=['덧붙이거나 중요도만 올림', '지우지 않음'])
    f.box('review', X[4], CY, ['담당자 검토'], note=['항목을 켜고 끄고', '문장을 다듬음'])
    f.box('save', X[5], CY, ['저장 · 확정'], terminal=True, note=['저장해야 기록이 됨', '규칙 버전을 함께 남김'])
    for a, b in (('intake', 'rule'), ('rule', 'draft'), ('draft', 'need'), ('need', 'review'), ('review', 'save')):
        f.right(a, b)
    f.pill('rule', '규칙 엔진'); f.pill('need', '규칙 엔진'); f.pill('review', '담당자 판단')
    return f

def pipeline():
    f = Flow()
    CY2 = CY + 260
    f.box('plan', X[0], CY, ['기획', '컨플루언스'], terminal=True, note=['기획서 · 기능정의서', '데이터베이스 설계서 97건'])
    f.box('issue', X[1], CY, ['이슈', '지라'], note=['이슈 키가 커밋 메시지까지', '이어짐'])
    f.box('design', X[2], CY, ['디자인', '피그마 MCP'], note=['시안 노드를 읽어', '화면으로 옮김'])
    f.box('build', X[3], CY, ['구현', 'Claude Code'], note=['운영 규칙 문서대로', '커밋 261건 · 테스트 969개'])
    f.box('check', X[4], CY, ['검증', 'Playwright'], note=['구현한 화면을', '브라우저로 직접 확인'])
    f.box('docs', X[5], CY, ['문서화', '매뉴얼 · 도움말'], terminal=True, note=['화면 캡처 자동화', '매뉴얼 18장 · 도움말 48단계'])
    for a, b in (('plan', 'issue'), ('issue', 'design'), ('design', 'build'), ('build', 'check'), ('check', 'docs')):
        f.right(a, b)
    f.box('draft', X[5], CY2, ['주간보고 초안'], note=['매주 금요일', '개발 용어 없이 쉬운 말로'])
    f.box('mail', X[4], CY2, ['보고 메일 발송'], note=['금요일 오후 자동 발송'])
    f.box('reader', X[3], CY2, ['비개발 이해관계자'], terminal=True, note=['진행 상황을', '쉬운 말로 받아 봄'])
    D, R = f.nodes['docs'], f.nodes['draft']
    ex = D['right'] + 40
    f.line([(D['right'] - 1, D['cy']), (ex, D['cy']), (ex, R['cy']), (R['right'] + 0.5, R['cy'])])
    f.left('draft', 'mail'); f.left('mail', 'reader')
    f.pill('draft', '예약 에이전트'); f.pill('mail', '예약 에이전트')
    return f

def service():
    """케어닷이 잇는 센터 업무 — 상담에서 방문 기록 · 보호자 마이페이지까지(01 개요).
    근거: 저장소 백오피스 LNB(상담관리 바로 아래 채용관리 · 상담 상세의 구인 공고 만들기 · 수급자 서류는 상세 탭 · 방문일정 · RFID),
    마이페이지(케어플랜 · 돌봄 일지 · 청구 내역), content-plan 2-6 ③(공단 · 희망이음 API · 미신고 표시). 둘째 줄은 오른쪽 → 왼쪽."""
    f = Flow()
    CY2 = CY + 250
    f.box('c1', X[0], CY, ['무료 상담 신청'], terminal=True, note=['메인사이트 · 전화'])
    f.box('c2', X[1], CY, ['상담관리'], note=['현황과 목록을', '한 화면에서'])
    f.box('c3', X[2], CY, ['계약 · 수급자 등록'], note=['수급자 서류는', '상세 탭에서'])
    f.box('c4', X[3], CY, ['구인 공고 · 채용'], note=['상담 상세에서', '바로 공고 작성'])
    f.box('d1', X[3], CY2, ['직원 등록 · 공단 신고'], note=['등록과 신고를 나눠 확인', '미신고면 목록에 표시'])
    f.box('d2', X[2], CY2, ['방문 일정 배정'], note=['수급자 · 종사자 일정'])
    f.box('d3', X[1], CY2, ['방문 · 기록'], note=['RFID로 방문 확인'])
    f.box('d4', X[0], CY2, ['보호자 마이페이지'], terminal=True, note=['케어플랜 · 돌봄 일지 · 청구 내역'])
    f.right('c1', 'c2'); f.right('c2', 'c3'); f.right('c3', 'c4')
    A, B = f.nodes['c4'], f.nodes['d1']; xr = A['right'] + 50
    f.line([(A['right'] - 1, CY), (xr, CY), (xr, CY2), (B['right'] + 0.5, CY2)])
    f.left('d1', 'd2'); f.left('d2', 'd3'); f.left('d3', 'd4')
    f.pill('d1', '공단 · 희망이음 API')
    return f

def draws():
    P = '청담원'
    return [
        {'page': P, 'frame': '청담원 · 케어닷 업무 흐름', 'x': 0, 'y': 1400, 'export': 'cdw-service-flow', 'items': service().items},
        {'page': P, 'frame': '청담원 · 케어플랜 초안 흐름', 'x': 0, 'y': 0, 'export': 'cdw-careplan-flow', 'items': careplan().items},
        {'page': P, 'frame': '청담원 · AI 업무 파이프라인', 'x': 0, 'y': 700, 'export': 'cdw-pipeline-flow', 'items': pipeline().items},
    ]

if __name__ == '__main__':
    write_task(sys.argv[1], draws())
