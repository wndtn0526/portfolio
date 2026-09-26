#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06 VOC 운영 프로세스 · VOC 처리와 보고 플로우차트 → 플러그인 작업(JSON)

부품 · 치수는 flowkit.py(덱 슬라이드 08 플로우차트 실측)를 쓴다.
첫 줄: VOC 한 건이 접수부터 배포까지 가는 길. 지라 오토메이션이 하는 단계(담당자 배정 · PR 상태 · 완료 상태)는 검은 말풍선으로 표시.
둘째 줄(오른쪽 → 왼쪽): 쌓인 티켓을 레이블로 모아 보고서 → 사용성 개선 지표.
내용은 사용자가 알려준 사실만(2026-09-26): 모듈별 자동 배정 · 알림 → 작업 시작 · 깃에 올리면 PR · 배포하면 완료 ·
문의별 레이블 · 주간 / 월간 / 분기 보고서 · 모듈 · 기능별 문의 집중도를 사용성 개선 지표로. 모듈 이름은 확인 전이라 쓰지 않는다.
사용: python3 tools/figma-export-plugin/tasks/voc.py <작업 JSON 경로>
"""
import json, sys
from flowkit import *   # 덱 플로우차트 부품(같은 폴더)

CY, CY2 = 60, 320
def voc():
    f = Flow()
    x = [0, 322, 644, 966, 1288, 1610]
    f.box('in', x[0], CY, ['문의 접수'], terminal=True, note=['교육 · 데모 질문, 고객 문의,', '사용 중 불편'])
    f.box('ticket', x[1], CY, ['지라 티켓 등록'], note=['문의별로 레이블 달기', '정해 둔 레이블 목록 안에서'])
    f.box('assign', x[2], CY, ['모듈별 담당자', '자동 배정'], note=['모듈마다 정해 둔', '담당 개발자에게 배정', '배정되면 바로 알림'])
    f.box('work', x[3], CY, ['개발자 작업 시작'], note=['알림을 받은 개발자가', '작업을 시작'])
    f.box('pr', x[4], CY, ['깃에 올려', 'PR 생성'], note=['티켓 상태가', 'PR 로 자동 변경'])
    f.box('deploy', x[5], CY, ['배포'], terminal=True, note=['티켓 상태가', '완료로 자동 변경'])
    for k in ('assign', 'pr', 'deploy'):
        f.pill(k, '지라 오토메이션')
    f.right('in', 'ticket'); f.right('ticket', 'assign'); f.right('assign', 'work'); f.right('work', 'pr'); f.right('pr', 'deploy')
    # 둘째 줄 — 오른쪽에서 왼쪽으로
    f.box('label', x[5], CY2, ['레이블별 집계'], note=['쌓인 티켓을 레이블로 모아', '모듈별, 기능별 문의 수 확인'])
    f.box('report', x[4], CY2, ['주간 · 월간 · 분기', '보고서'], note=['기간마다 보고서 자료로 정리'])
    f.box('metric', x[3], CY2, ['사용성 개선 지표'], terminal=True, note=['문의가 몰린 기능을', '다음 개선 과제의 근거로'])
    D, L = f.nodes['deploy'], f.nodes['label']
    ex = D['right'] + 40                                   # 배포 오른쪽으로 나가 아래로 꺾어 둘째 줄로
    f.line([(D['right'] - 1, CY), (ex, CY), (ex, CY2), (L['right'] + 0.5, CY2)])
    f.left('label', 'report'); f.left('report', 'metric')
    return f

task = {
    'file': '포트폴리오_MCP',
    'draw': [
        {'page': '06 VOC', 'frame': '06 · VOC 처리와 보고 플로우', 'x': 0, 'y': 0, 'export': 'gpro-voc-flow', 'items': voc().items},
    ],
}
json.dump(task, open(sys.argv[1], 'w'), ensure_ascii=False)
print(sys.argv[1], len(task['draw'][0]['items']), 'items')
