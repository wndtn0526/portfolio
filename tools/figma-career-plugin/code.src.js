/*
 * 웹의 이력 섹션(#career)을 Figma 캔버스에 편집 가능한 레이어로 그린다.
 *
 * 값은 home.blade.php · tokens.css 를 1440/2056 폭에서 실측한 것이다(career-geo).
 *   섹션 패딩 90 / 48 · 사진 260×325 모서리 28 그림자(0 24 60 -20 · 17,17,17 25%) · 사진→글 56 · 글 단 위 24
 *   제목 display-2 40/130%/-2.5% ('/' 만 Bold) · 이름 heading-2 20/150%/-5% SemiBold · 소개 body-2 15/153.3%/-4% 폭 560
 *   링크 20 SemiBold 밑줄 + ↗ · 블록 사이 80/64 · 섹션 라벨 caption-2 11/154.5%/+12% SemiBold 대문자 흐림(#868e96)
 *   행: 위아래 패딩 14 · 위 보더 1px 검정 8%(마지막은 아래도) · 라벨 92 | 내용 | 오른쪽 기간 14 흐림 · 칸 사이 16
 *   행 제목 headline-1 19/152.6%/-3.16% Medium · 부제 label-1-reading 14/157.1%/-1.43% #495057 · 불릿 들여쓰기 16
 *   기술 막대 280×10 트랙 #dee2e6 · 채움 #34c75d→#25c7a6
 *
 * ⚠️ Figma MCP 서버는 읽기만 되고 쓰기 도구가 없어서 플러그인으로 넣는다(실행법은 README).
 * ⚠️ Pretendard(Regular/Medium/SemiBold/Bold)가 이 맥에 있어야 한다. 없으면 Inter 로 대신한다.
 * ⚠️ 이 파일은 code.src.js 다. 사진을 박은 code.js 는 build.sh 가 만든다.
 */

const PHOTO_B64 = '__PHOTO_B64__';

const hex = (h) => ({ r: parseInt(h.slice(1, 3), 16) / 255, g: parseInt(h.slice(3, 5), 16) / 255, b: parseInt(h.slice(5, 7), 16) / 255 });
const C = { canvas: hex('#f9f9f9'), ink: hex('#212529'), body: hex('#495057'), muted: hex('#868e96'), rule: hex('#dee2e6'), black: hex('#000000'),
            skillA: hex('#34c75d'), skillB: hex('#25c7a6') };

// 크기 · 행간% · 자간% — tokens.css 의 404 타이포 스케일
const T = {
    display2: { size: 40, lh: 130, ls: -2.5 },
    heading2: { size: 20, lh: 150, ls: -5 },
    body2:    { size: 15, lh: 153.3, ls: -4 },
    headline1:{ size: 19, lh: 152.6, ls: -3.16 },
    label1:   { size: 14, lh: 142.9, ls: -1.43 },
    label1r:  { size: 14, lh: 157.1, ls: -1.43 },
    caption2: { size: 11, lh: 154.5, ls: 12 },   // 대문자 라벨 자간은 DS(0)가 아니라 레퍼런스 값
};

const INTRO = {
    name: '신중수', role: ' · Product Manager · Product Designer',
    text: 'B2B SaaS 그룹웨어 시장에 대한 깊이 있는 도메인 지식 (HR/재무/그룹웨어)을 보유하고 있습니다. 사용자 중심의 데이터 분석 및 시스템 아키텍처 기획을 기반으로 복잡한 엔터프라이즈 프로세스를 사용자 친화적 UX로 혁신하는 데 특화되어 있습니다.',
    link: '이메일 보내기',
};
const CAREER = [
    { years: '2021 – 2025', title: '워크앤조이', sub: '서비스 기획 및 UX Design · Visual Design · IR & 영업 기획 (Groupware pro)', period: '2021년 10월 ~ 2025년 8월',
      bullets: ['사용자 패턴 분석, 도메인 지식 바탕으로 UX Writing 전략 수립 및 적용', 'VOC 데이터 및 유저 패턴 기반 경험 중심의 화면 설계 및 UX 개선 기획',
                '온 오프라인 홍보물, 캠페인 콘텐츠 등 Visual Design 제작 · 사내 서식류 디자인 관리', '고객사 대상 데모 시연 및 기능 컨설팅, 인사·재무 담당자 기능 교육 운영',
                'IR 자료 제작 핵심 기획자로 참여, 서비스 포지셔닝 및 투자 제안서 구성'] },
    { years: '2021', title: '풀다랩', sub: '아트팀 — 브랜드 비딩 기획 및 디자인 업무', period: '2021년 04월 ~ 2021년 09월' },
    { years: '2019 – 2020', title: '미디어로그', sub: 'LG U+ IP TV 사업본부 — IP TV 플랫폼 포스터 디자인', period: '2019년 12월 ~ 2020년 10월' },
    { years: '2017 – 2019', title: '이디엠에듀케이션', sub: 'IELTS 인강 신사업부 서비스기획팀 — 시스템 기획 및 사업 기획 · 서비스 운영', period: '2017년 10월 ~ 2019년 04월',
      bullets: ['edm IELTS 인강 플랫폼 기획 · IELTS 토스 및 한국어 인강 론칭', '연 매출 3억 규모 인강 사이트 운영 담당'] },
];
const EDU = [{ years: '2012 – 2016', title: '백석예술대학교', sub: '시각디자인과 졸업', period: '2012년 02월 ~ 2016년 3월' }];
const PROFILE = [['생년월일', '1993-05-26'], ['전화번호', '+82 010-2262-5913'], ['이메일', 'wndtn0526@gmail.com'], ['주소', '경기도 수원시 장안구 화산로 263 신일APT 106-302']];
const SKILLS = [['피그마', 100], ['SQL', 82], ['지라', 89], ['컨플루언스', 100], ['어도비 포토샵', 100], ['어도비 일러스트', 100]];

const SCREENS = [
    { name: '03 이력 — 1440', w: 1440 },
    { name: '03 이력 — 2056 (풀 화면)', w: 2056 },
];

let FAMILY = 'Pretendard';
let F = { regular: 'Regular', medium: 'Medium', semibold: 'SemiBold', bold: 'Bold' };

async function pickFonts() {
    const fonts = await figma.listAvailableFontsAsync();
    const byFamily = new Map();
    for (const f of fonts) {
        if (!byFamily.has(f.fontName.family)) byFamily.set(f.fontName.family, new Set());
        byFamily.get(f.fontName.family).add(f.fontName.style);
    }
    const first = (styles, cands) => cands.find((s) => styles.has(s));
    for (const fam of ['Pretendard', 'Pretendard Variable', 'Pretendard JP', 'Inter']) {
        const styles = byFamily.get(fam);
        if (!styles) continue;
        const regular = first(styles, ['Regular', 'Normal', 'Book']);
        const bold = first(styles, ['Bold', 'ExtraBold', 'SemiBold', 'Medium']);
        if (!regular || !bold) continue;
        FAMILY = fam;
        F = { regular, bold, medium: first(styles, ['Medium', 'SemiBold', 'Semi Bold']) || bold, semibold: first(styles, ['SemiBold', 'Semi Bold', 'Medium']) || bold };
        return;
    }
    throw new Error('쓸 수 있는 글꼴을 못 찾았다 (Pretendard 도 Inter 도 없음)');
}

function text(chars, style, spec, color, { stretch = false, width = null, align = 'LEFT', upper = false } = {}) {
    const t = figma.createText();
    t.fontName = { family: FAMILY, style };
    t.characters = chars;
    t.fontSize = spec.size;
    t.lineHeight = { unit: 'PERCENT', value: spec.lh };
    t.letterSpacing = { unit: 'PERCENT', value: spec.ls };
    t.fills = [{ type: 'SOLID', color }];
    t.textAlignHorizontal = align;
    if (upper) t.textCase = 'UPPER';
    if (width) { t.textAutoResize = 'HEIGHT'; t.resize(width, 10); }
    else if (stretch) { t.textAutoResize = 'HEIGHT'; t.layoutAlign = 'STRETCH'; }
    else t.textAutoResize = 'WIDTH_AND_HEIGHT';
    return t;
}

function frame(name, dir, { gap = 0, pad = [0, 0, 0, 0], width = null, stretch = false, fill = null, align = 'MIN' } = {}) {
    const f = figma.createFrame();
    f.name = name;
    f.layoutMode = dir;
    f.itemSpacing = gap;
    [f.paddingTop, f.paddingRight, f.paddingBottom, f.paddingLeft] = pad;
    f.fills = fill ? [{ type: 'SOLID', color: fill }] : [];
    f.primaryAxisSizingMode = 'AUTO';
    f.counterAxisSizingMode = 'AUTO';
    f.counterAxisAlignItems = align;
    if (width) { if (dir === 'HORIZONTAL') { f.primaryAxisSizingMode = 'FIXED'; } else { f.counterAxisSizingMode = 'FIXED'; } f.resize(width, 10); }
    // STRETCH/GROW 는 그 축의 크기를 부모가 정한다 — hug(AUTO) 로 두면 Figma 가 순환으로 본다
    if (stretch) { f.layoutAlign = 'STRETCH'; if (dir === 'HORIZONTAL') f.primaryAxisSizingMode = 'FIXED'; else f.counterAxisSizingMode = 'FIXED'; }
    return f;
}
const fillWidth = (n) => { n.layoutGrow = 1; if (n.layoutMode === 'VERTICAL') n.counterAxisSizingMode = 'FIXED'; else n.primaryAxisSizingMode = 'FIXED'; return n; };   // 가로 auto-layout 안에서 남는 폭을 다 차지

function sectionLabel(s) { return text(s, F.semibold, T.caption2, C.muted, { upper: true }); }

// 한 행 — [라벨 92 | 내용(남는 폭) | 오른쪽]. 위 보더 1px 검정 8%, 마지막 행은 아래도.
function row(label, content, right, last) {
    const r = frame('행 · ' + label, 'HORIZONTAL', { gap: 16, pad: [14, 0, 14, 0], stretch: true, align: 'BASELINE' });
    r.strokes = [{ type: 'SOLID', color: C.black, opacity: 0.08 }];
    r.strokeTopWeight = 1; r.strokeBottomWeight = last ? 1 : 0; r.strokeLeftWeight = 0; r.strokeRightWeight = 0;
    const lab = frame('라벨', 'VERTICAL', { width: 92 }); lab.appendChild(sectionLabel(label)); r.appendChild(lab);
    r.appendChild(fillWidth(content));
    if (right) r.appendChild(text(right, F.regular, T.label1, C.muted, { align: 'RIGHT' }));
    return r;
}

function entry(e) {
    const c = frame('내용', 'VERTICAL', { gap: 4 });
    c.appendChild(text(e.title, F.medium, T.headline1, C.ink, { stretch: true }));
    c.appendChild(text(e.sub, F.regular, T.label1r, C.body, { stretch: true }));
    if (e.bullets) {
        const ul = frame('불릿', 'VERTICAL', { pad: [4, 0, 0, 16], stretch: true });
        for (const b of e.bullets) ul.appendChild(text('•  ' + b, F.regular, T.label1r, C.body, { stretch: true }));
        c.appendChild(ul);
    }
    return c;
}

function block(name, entries, topPad = 0) {
    const b = frame(name, 'VERTICAL', { gap: 12, pad: [topPad, 0, 0, 0], stretch: true });
    b.appendChild(sectionLabel(name));
    const list = frame('목록', 'VERTICAL', { stretch: true });
    entries.forEach((e, i) => list.appendChild(row(e.years, entry(e), e.period, i === entries.length - 1)));
    b.appendChild(list);
    return b;
}

function skillBar(pct) {
    const track = frame('막대', 'HORIZONTAL', { width: 280, fill: C.rule });
    track.resize(280, 10); track.primaryAxisSizingMode = 'FIXED'; track.counterAxisSizingMode = 'FIXED'; track.cornerRadius = 999;
    const fill = figma.createRectangle(); fill.name = '채움'; fill.resize(280 * pct / 100, 10); fill.cornerRadius = 999;
    fill.fills = [{ type: 'GRADIENT_LINEAR', gradientTransform: [[1, 0, 0], [0, 1, 0]],
                    gradientStops: [{ position: 0, color: { ...C.skillA, a: 1 } }, { position: 1, color: { ...C.skillB, a: 1 } }] }];
    track.appendChild(fill);
    return track;
}

function buildTop() {
    const top = frame('사진 + 소개', 'HORIZONTAL', { gap: 56, stretch: true });
    const photo = figma.createRectangle(); photo.name = '프로필 사진'; photo.resize(260, 325); photo.cornerRadius = 28;
    const img = figma.createImage(figma.base64Decode(PHOTO_B64));
    photo.fills = [{ type: 'IMAGE', scaleMode: 'FILL', imageHash: img.hash }];
    photo.effects = [{ type: 'DROP_SHADOW', color: { r: 17 / 255, g: 17 / 255, b: 17 / 255, a: 0.25 }, offset: { x: 0, y: 24 }, radius: 60, spread: -20, visible: true, blendMode: 'NORMAL' }];
    top.appendChild(photo);

    const col = frame('소개', 'VERTICAL', { pad: [24, 0, 0, 0] });
    const h2 = text('/이력', F.regular, T.display2, C.ink); h2.setRangeFontName(0, 1, { family: FAMILY, style: F.bold }); h2.name = '제목'; col.appendChild(h2);
    const name = text(INTRO.name + INTRO.role, F.semibold, T.heading2, C.ink); name.name = '이름 · 직함';
    name.setRangeFontName(INTRO.name.length, name.characters.length, { family: FAMILY, style: F.regular });
    name.setRangeFills(INTRO.name.length, name.characters.length, [{ type: 'SOLID', color: C.muted }]);
    col.appendChild(wrap(name, 20));
    col.appendChild(wrap(Object.assign(text(INTRO.text, F.regular, T.body2, C.body, { width: 560 }), { name: '소개 문단' }), 12));
    const link = frame('링크', 'HORIZONTAL', { gap: 12, align: 'CENTER' });
    const l = text(INTRO.link, F.semibold, T.heading2, C.ink); l.textDecoration = 'UNDERLINE'; link.appendChild(l);
    link.appendChild(text('↗', F.semibold, T.heading2, C.ink));
    col.appendChild(wrap(link, 24));
    top.appendChild(col);
    return top;
}
// 위 여백만 다른 항목을 auto-layout 에 넣기 위한 껍데기(mt-5 · mt-3 · mt-6)
function wrap(node, top) { const w = frame(node.name, 'VERTICAL', { pad: [top, 0, 0, 0] }); w.appendChild(node); return w; }

function buildBottom() {
    const grid = frame('프로필 + 기술', 'HORIZONTAL', { gap: 64, pad: [64, 0, 0, 0], stretch: true });
    const left = frame('프로필', 'VERTICAL', { gap: 12 });
    left.appendChild(sectionLabel('프로필'));
    const pl = frame('목록', 'VERTICAL', { stretch: true });
    PROFILE.forEach(([k, v], i) => { const c = frame('내용', 'VERTICAL'); c.appendChild(text(v, F.medium, T.headline1, C.ink, { stretch: true })); pl.appendChild(row(k, c, null, i === PROFILE.length - 1)); });
    left.appendChild(pl); grid.appendChild(fillWidth(left));
    const right = frame('기술', 'VERTICAL', { gap: 12 });
    right.appendChild(sectionLabel('기술'));
    const sl = frame('목록', 'VERTICAL', { stretch: true });
    SKILLS.forEach(([k, pct], i) => { const c = frame('내용', 'VERTICAL'); c.appendChild(skillBar(pct)); const r = row(k, c, null, i === SKILLS.length - 1); r.counterAxisAlignItems = 'CENTER'; sl.appendChild(r); });
    right.appendChild(sl); grid.appendChild(fillWidth(right));
    return grid;
}

function buildScreen(screen, x) {
    const root = frame(screen.name, 'VERTICAL', { gap: 0, pad: [90, 48, 90, 48], width: screen.w, fill: C.canvas });
    root.x = x; root.y = 0; root.clipsContent = true;
    root.appendChild(buildTop());
    root.appendChild(block('경력', CAREER, 80));
    root.appendChild(block('학력', EDU, 64));
    root.appendChild(buildBottom());
    return root;
}

(async () => {
    try {
        await pickFonts();
        for (const s of Object.values(F)) await figma.loadFontAsync({ family: FAMILY, style: s });
        const made = [];
        let x = 0;
        for (const s of SCREENS) { made.push(buildScreen(s, x)); x += s.w + 200; }
        figma.viewport.scrollAndZoomIntoView(made);
        figma.closePlugin(`완료 — 글꼴 ${FAMILY}, 프레임 ${made.length}개`);
    } catch (e) {
        figma.closePlugin('실패: ' + (e && e.message ? e.message : e));
    }
})();
