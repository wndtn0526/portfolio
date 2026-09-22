#!/usr/bin/env python3
"""
그룹웨어프로 · 법인카드 정산 흐름 / 홈택스 지출결의서 흐름 → public/images/projects/gpro-card-flow.svg · gpro-hometax-flow.svg

PORTFOLIO 덱 슬라이드 07 · 09(서비스 프로세스 오버뷰)를 사이트 문법으로 옮긴 것. 단계는 덱 그대로, 구성원이 하는 구간만 파랑.
색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-card-flow.py
"""
from pathlib import Path

INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"

def flow(steps, lanes, notes, dst, W=1200, H=330):
    """steps: [(제목, 부제, accent)], lanes: [(시작 idx, 끝 idx, 라벨)] 위에 얹는 구간 표시, notes: [(idx 사이, 글)] 화살표 위 메모"""
    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
    add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')
    n = len(steps); gap = 28
    bw = (W - 80 - gap * (n - 1)) / n
    y, bh = 120, 96
    xs = [40 + i * (bw + gap) for i in range(n)]
    # 구간 라벨(위)
    for a, b, label in lanes:
        x1, x2 = xs[a], xs[b] + bw
        add(f'<rect x="{x1:.0f}" y="64" width="{x2 - x1:.0f}" height="26" rx="13" fill="{ACCENT}" fill-opacity="0.1"/>')
        add(f'<text x="{(x1 + x2) / 2:.0f}" y="82" font-size="12" font-weight="600" fill="{ACCENT}" text-anchor="middle">{label}</text>')
    for i, (title, sub, accent) in enumerate(steps):
        x = xs[i]
        fill, stroke, so = (ACCENT, ACCENT, 0) if accent else (CANVAS, '#000000', 0.08)
        add(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="{bh}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}"/>')
        tc, sc = (WHITE, WHITE) if accent else (INK, BODY)
        add(f'<text x="{x + 16:.0f}" y="{y + 40}" font-size="15" font-weight="600" fill="{tc}">{title}</text>')
        for k, line in enumerate(sub.split('|')):
            add(f'<text x="{x + 16:.0f}" y="{y + 62 + 18 * k}" font-size="12" fill="{sc}" fill-opacity="{0.85 if accent else 1}">{line}</text>')
        if i < n - 1:
            ax1, ax2, ay = x + bw, x + bw + gap, y + bh / 2
            add(f'<path d="M{ax1:.0f} {ay:.0f} H{ax2 - 2:.0f}" stroke="{MUTED}" stroke-width="1.5"/>')
            add(f'<polygon points="{ax2-9:.0f},{ay-5:.0f} {ax2:.0f},{ay:.0f} {ax2-9:.0f},{ay+5:.0f}" fill="{MUTED}"/>')
    for idx, note in notes:   # idx 번째 화살표 아래 메모
        cx = xs[idx] + bw + gap / 2
        add(f'<text x="{cx:.0f}" y="{y + bh + 34}" font-size="12" font-weight="500" fill="{MUTED}" text-anchor="middle">{note}</text>')
    add('</svg>')
    dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(dst, f'{dst.stat().st_size} bytes')

root = Path(__file__).resolve().parents[2] / 'public/images/projects'

# 법인카드 — 덱 07: 법인카드 지급 → 사용 → 사용내역 스크래핑 → 정산서 작성 · 신청 → 결재 승인 → 담당자 확인 · 정산 → ERP
flow([
    ('법인카드 지급', '지급 신청 · 사용 기간 설정', False),
    ('카드 사용', '구성원이 결제', False),
    ('사용 내역 수신', '카드사 → 스크래핑 서버 → GPRO', False),
    ('정산서 작성', '내역을 고르고 항목만 확인', True),
    ('결재 승인', '지급 신청 때 정한 결재선', True),
    ('담당자 정산', '내역 확인 · 마감', False),
    ('ERP 전표', '승인되면 자동 전송', False),
], lanes=[(3, 4, '구성원이 하는 일은 여기까지')], notes=[(2, '입력 대신 확인'), (5, 'GPRO → ERP')], dst=root / 'gpro-card-flow.svg')

# 홈택스 — 덱 09: 거래처 발행 → 수신 → 담당자 매핑 · 알림 → 지출결의서 생성(원클릭) → 결재 · 검증 → ERP
flow([
    ('거래처 발행', '홈택스에서 세금계산서 발행', False),
    ('GPRO 수신', '국세청 서버에서 자동 수신', False),
    ('담당자 매핑', '거래처 마스터로 담당자 찾고 알림', False),
    ('지출결의서 생성', '버튼 한 번, 거래처 · 금액 · 부가세 자동', True),
    ('결재 · 검증', '결재선 자동 지정 · 항목 검증', True),
    ('ERP 전표', '승인되면 자동 반영', False),
], lanes=[(3, 4, '담당자가 하는 일은 여기까지')], notes=[(1, '홈택스 API'), (2, '미등록 거래처면 등록부터')], dst=root / 'gpro-hometax-flow.svg')
