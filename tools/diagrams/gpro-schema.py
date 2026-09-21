#!/usr/bin/env python3
"""
그룹웨어프로 · 스키마 구조 도식 → public/images/projects/gpro-schema.svg

4. 진행 첫 단락(스키마 구조를 먼저 정리했다)의 그림. 표 상세가 아니라 구조만:
  가운데 인사 코어(구성원 · 조직 · 발령 이력, 시작일 · 종료일을 가진 행) — 모든 모듈이 여기를 읽는다
  둘레  근태 · 결재 · 재무 · 커뮤니티 — 구성원 · 조직을 따로 갖지 않고 코어를 읽는다
  재무 아래 ERP 커넥터 — 예산과목 · 계정 코드 테이블로 맞춘다

색은 tokens.css. 화살촉은 marker 대신 도형(Figma SVG 가져오기가 marker 를 떨어뜨린다).
고치려면 이 파일을 고치고 다시 돌린다: python3 tools/diagrams/gpro-schema.py
"""
from pathlib import Path

W, H = 1200, 500
INK, BODY, MUTED, CANVAS, ACCENT, WHITE = '#212529', '#495057', '#868e96', '#f9f9f9', '#504fed', '#ffffff'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
out = []
def add(s): out.append(s)

def entity(x, y, w, title, fields, accent=False):
    h = 40 + 22 * len(fields)
    fill, stroke, so = (WHITE, ACCENT, 1) if accent else (CANVAS, '#000000', 0.08)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-opacity="{so}" stroke-width="{1.5 if accent else 1}"/>')
    add(f'<text x="{x + 16}" y="{y + 26}" font-size="15" font-weight="600" fill="{ACCENT if accent else INK}">{title}</text>')
    for i, f in enumerate(fields):
        add(f'<text x="{x + 16}" y="{y + 50 + 22 * i}" font-size="13" fill="{BODY}">{f}</text>')
    return h

def label(x, y, s, color=MUTED, anchor='start', size=13, weight=600):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')

def link(d, x, y, dir):   # 꺾인 선 + 화살촉 (r/l/d)
    add(f'<path d="{d}" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
    pts = {'r': f'{x-9},{y-5} {x},{y} {x-9},{y+5}', 'l': f'{x+9},{y-5} {x},{y} {x+9},{y+5}', 'd': f'{x-5},{y-9} {x},{y} {x+5},{y-9}'}[dir]
    add(f'<polygon points="{pts}" fill="{MUTED}"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}" aria-hidden="true">')
add(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ── 가운데: 인사 코어 ──
add(f'<rect x="400" y="60" width="400" height="380" rx="16" fill="{WHITE}" stroke="{ACCENT}" stroke-width="1.5"/>')
label(420, 92, '인사 코어', color=ACCENT, size=16, weight=700)
label(500, 92, '모든 모듈이 여기를 읽습니다', size=12, weight=500)
entity(420, 112, 172, '구성원', ['사번 · 이름', '고용 구분', '재직 상태'])
entity(608, 112, 172, '조직', ['조직 코드 · 이름', '상위 조직', '시작일 · 종료일'])
entity(420, 232, 360, '발령 이력', ['구성원 → 조직 · 직책', '발령 유형 (입사 · 발령 · 퇴사)', '시작일 · 종료일'])
label(420, 386, '시작일 · 종료일을 가진 행은 날짜로 조회합니다.', size=12, weight=500)
label(420, 406, '다른 모듈은 구성원 · 조직 정보를 따로 갖지 않습니다.', size=12, weight=500)

# ── 둘레 모듈 ──
entity(40, 60, 300, '근태', ['근무제 · 휴일 · 연차 기준 (법인별)', '출퇴근 · 휴가 기록', '읽음: 구성원 · 조직'])
entity(40, 320, 300, '커뮤니티', ['게시판 · 글', '열람 범위 = 조직'])
entity(860, 60, 300, '결재', ['결재 문서 · 양식', '결재선 = 그날의 소속 · 직책', '읽음: 발령 이력'])
h = entity(860, 232, 300, '재무', ['지출결의서 = 결재 문서', '예산과목 · 계정 코드', '마감 · 자금 지급', '법인카드 내역 · 홈택스 세금계산서'])
entity(860, 232 + h + 12, 300, 'ERP 커넥터', ['예산과목 · 계정 코드로 회사별 ERP 에 맞춤'], accent=True)

# ── 연결선: 모듈 → 코어 ──
link('M340 126 H370 V180 H400', 400, 180, 'r')
link('M340 360 H370 V330 H400', 400, 330, 'r')
link('M860 126 H830 V180 H800', 800, 180, 'l')
link('M860 300 H830 V330 H800', 800, 330, 'l')
link('M1010 166 V232', 1010, 232, 'd'); label(1022, 204, '승인되면 재무로', size=12, weight=500)

add('</svg>')
dst = Path(__file__).resolve().parents[2] / 'public/images/projects/gpro-schema.svg'
dst.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(dst, f'{dst.stat().st_size} bytes')
