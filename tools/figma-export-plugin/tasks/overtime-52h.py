#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03 주 52시간 · 연장 근무 / 휴일 근무 플로우차트 → 플러그인 작업(JSON)

부품 · 치수는 flowkit.py(덱 슬라이드 08 플로우차트 실측)를 쓴다.

내용은 projects.php 03 의 프로세스 설계 문단에 적힌 것만 옮긴다(새 단계를 지어내지 않는다).
사용: python3 tools/figma-export-plugin/tasks/overtime-52h.py <작업 JSON 경로>
"""
import json, sys
from flowkit import *   # 덱 플로우차트 부품(같은 폴더)

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

PAGE = '03 주 52시간'
task = {
    'file': '포트폴리오_MCP',
    'renamePages': [['플로우차트', PAGE]],
    'draw': [
        {'page': PAGE, 'frame': '03 · 연장 근무 신청 플로우', 'x': 0, 'y': 0, 'export': 'gpro-overtime-flow', 'items': overtime().items},
        {'page': PAGE, 'frame': '03 · 휴일 근무 신청 플로우', 'x': 0, 'y': 700, 'export': 'gpro-holiday-flow', 'items': holiday().items},
    ],
}
json.dump(task, open(sys.argv[1], 'w'), ensure_ascii=False)
print(sys.argv[1], sum(len(d['items']) for d in task['draw']), 'items')
