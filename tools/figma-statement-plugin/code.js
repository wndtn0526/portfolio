/*
 * 웹의 두 번째 섹션(선언 + 오른쪽 소개)을 Figma 캔버스에 실제 레이어로 그린다.
 *
 * 값은 Figma(포트폴리오_MCP 1:24 · 2056 기준)에서 조절된 것을 웹(home.blade.php)과 함께 맞춘 것이다.
 *   배경 #504fed · 왼쪽 선언 46.08px / 행간 108% / 자간 -2.5% (1·2줄 Bold, 3줄 첫 '/' 만 Bold) · 넉 줄
 *   오른쪽 소개 — 인사 32 Bold · 요지 24 SemiBold(흰색 100%) · 소제목 24 · 본문 20(85%) · 맺음 흐림 없음
 *   좌우 여백 96, 두 단은 반반(2056 에서 932 | 932), 세로 가운데 정렬. 영문 라벨 없음.
 *
 * ⚠️ Figma MCP 서버는 읽기만 되고 쓰기 도구가 없어서 플러그인으로 넣는다.
 *    실행: Figma → 메뉴 Plugins → Development → Import plugin from manifest… → 이 폴더의 manifest.json
 *          → 같은 메뉴에서 「포트폴리오 · 선언 섹션 넣기」 실행.
 * ⚠️ Pretendard 가 이 맥에 설치돼 있어야 그 글꼴로 그려진다. 없으면 Inter 로 대신하고 알림을 띄운다.
 */

const BLUE = { r: 0x50 / 255, g: 0x4f / 255, b: 0xed / 255 };
const WHITE = { r: 1, g: 1, b: 1 };

// 크기 · 행간% · 자간% — Figma(포트폴리오_MCP 1:24, 2056 기준)에서 조절된 값. 웹은 폭 따라 흐르고 2056 에서 이 값이 된다.
const T = {
    statement: { size: 46.08, lh: 108, ls: -2.5 },
    greet:     { size: 32, lh: 131.8, ls: -4.55 },
    thesis:    { size: 24, lh: 162.5, ls: -3.75 },
    title:     { size: 24, lh: 150, ls: -5 },
    body:      { size: 20, lh: 162.5, ls: -3.75 },
};

const STATEMENT = [
    ['맡은 일의 본질적인 가치를', 'bold'],
    ['발견하는 일을 합니다.', 'bold'],
    ['/그 가치가 사용자에게 가장', 'slash'],   // 첫 글자 '/' 만 Bold
    ['매력적으로 닿도록 경험을 설계합니다.', 'regular'],
];

const ASIDE = {
    greet: '안녕하세요. 서비스기획자 신중수 입니다.',
    thesis: '저의 가장 큰 무기이자 차별점은 서로 다른 두 영역에서의 깊은 통찰을 결합했다는 점입니다.',
    pillars: [   // 영문 라벨은 Figma 에서 뺐다
        ['구조와 논리의 깊이',
         '그룹웨어 시장에서의 깊은 도메인 경험을 통해 어떤 기술도 도메인보다 앞설 수 없다는 신념을 가지고, 실제 현업의 복잡한 업무 흐름 (HR/재무) 을 깊이 이해하고 구조화할 수 있게 성장했습니다. 명확한 목표와 올바른 방향 설정이 정답에 가까운 결과를 만든다는 믿음으로, 엔터프라이즈의 비효율을 해소하는 논리적인 UX 설계에 집중합니다.'],
        ['브랜드와 소통의 폭',
         '이전 광고대행사 경험에서 얻은 브랜드 스토리텔링 및 비주얼 커뮤니케이션 능력은 제품의 매력도를 극대화하는 중요한 도구입니다. 딱딱하게 느껴지기 쉬운 B2B 솔루션에 사용자에게 공감을 주는 UX Writing 과 일관된 브랜드 경험을 입혀, 사용자가 사랑하고 습관적으로 이용하는 제품으로 전환시킵니다.'],
    ],
    closing: '이러한 사고와 통찰은 단순히 일을 하는 사람이 아니라, 사용자 효율성과 브랜드 매력을 동시에 높여 제품의 가치를 확장시키는 사람으로 성장하게 하는 원동력입니다. 저는 주어진 일의 가치를 넘어서는 새로운 가치를 만들어내는 엑스트라 마일을 실현하며, 함께 일하며 더 높은 곳을 바라보는 좋은 동료, 신뢰받는 협업자가 되고 싶습니다.',
    closingMuted: ' 멋진 관계를 기대합니다. 감사합니다.',
};

// 두 단은 반반(좌우 여백 96 씩). 반이 선언의 가장 긴 줄(662)보다 좁아지면 그 줄 폭은 지키고 나머지가 오른쪽.
const STATEMENT_MAX_W = 662;
const SCREENS = [
    { name: '02 선언 — 1440×900',  w: 1440, h: 900 },
    { name: '02 선언 — 2056×1100 (풀 화면)', w: 2056, h: 1100 },
].map((s) => { const half = (s.w - 192) / 2; const left = Math.max(half, STATEMENT_MAX_W); return { ...s, left, aside: s.w - 192 - left }; });

let FAMILY = 'Pretendard';
let REGULAR = 'Regular';
let BOLD = 'Bold';
let SEMIBOLD = 'SemiBold';   // 요지용. 없으면 Bold 로 대신한다

async function pickFonts() {
    const fonts = await figma.listAvailableFontsAsync();
    const byFamily = new Map();
    for (const f of fonts) {
        if (!byFamily.has(f.fontName.family)) byFamily.set(f.fontName.family, new Set());
        byFamily.get(f.fontName.family).add(f.fontName.style);
    }
    const pick = (fam) => {
        const styles = byFamily.get(fam);
        if (!styles) return null;
        const reg = ['Regular', 'Normal', 'Book'].find((s) => styles.has(s));
        const bold = ['Bold', 'SemiBold', 'Semi Bold', 'ExtraBold', 'Medium'].find((s) => styles.has(s));
        const semi = ['SemiBold', 'Semi Bold', 'Medium'].find((s) => styles.has(s)) || bold;
        return reg && bold ? { reg, bold, semi } : null;
    };
    for (const fam of ['Pretendard', 'Pretendard Variable', 'Pretendard JP', 'Inter']) {
        const got = pick(fam);
        if (got) { FAMILY = fam; REGULAR = got.reg; BOLD = got.bold; SEMIBOLD = got.semi; return; }
    }
    throw new Error('쓸 수 있는 글꼴을 못 찾았다 (Pretendard 도 Inter 도 없음)');
}

function text(chars, style, spec, { opacity = 1, stretch = false } = {}) {
    const t = figma.createText();
    t.fontName = { family: FAMILY, style };
    t.characters = chars;
    t.fontSize = spec.size;
    t.lineHeight = { unit: 'PERCENT', value: spec.lh };
    t.letterSpacing = { unit: 'PERCENT', value: spec.ls };
    t.fills = [{ type: 'SOLID', color: WHITE, opacity }];
    t.textAutoResize = stretch ? 'HEIGHT' : 'WIDTH_AND_HEIGHT';
    if (stretch) t.layoutAlign = 'STRETCH';
    return t;
}

function column(name, gap, width = null) {
    const f = figma.createFrame();
    f.name = name;
    f.layoutMode = 'VERTICAL';
    f.itemSpacing = gap;
    f.fills = [];
    f.primaryAxisSizingMode = 'AUTO';
    if (width) { f.counterAxisSizingMode = 'FIXED'; f.resize(width, 10); }
    else f.counterAxisSizingMode = 'AUTO';
    return f;
}

function buildStatement() {
    const col = column('선언 (왼쪽)', 0);
    for (const [line, kind] of STATEMENT) {
        const t = text(line, kind === 'bold' ? BOLD : REGULAR, T.statement);
        if (kind === 'slash') t.setRangeFontName(0, 1, { family: FAMILY, style: BOLD });
        t.name = line;
        col.appendChild(t);
    }
    return col;
}

function buildAside(width) {
    const col = column('소개 (오른쪽)', 32, width);

    const head = column('인사', 12, width); head.layoutAlign = 'STRETCH';
    head.appendChild(Object.assign(text(ASIDE.greet, BOLD, T.greet, { stretch: true }), { name: '인사' }));
    head.appendChild(Object.assign(text(ASIDE.thesis, SEMIBOLD, T.thesis, { stretch: true }), { name: '요지' }));   // Figma: SemiBold · 흰색 100%
    col.appendChild(head);

    for (const [title, body] of ASIDE.pillars) {
        const p = column(title, 8, width); p.layoutAlign = 'STRETCH';
        p.appendChild(Object.assign(text(title, BOLD, T.title, { stretch: true }), { name: '소제목' }));
        p.appendChild(Object.assign(text(body, REGULAR, T.body, { opacity: 0.85, stretch: true }), { name: '본문' }));
        col.appendChild(p);
    }

    const closing = text(ASIDE.closing + ASIDE.closingMuted, REGULAR, T.body, { opacity: 0.85, stretch: true });
    closing.name = '맺음';   // Figma: 흐린 구간 없이 전부 85%
    col.appendChild(closing);
    return col;
}

function buildScreen(screen, x) {
    const frame = figma.createFrame();
    frame.name = screen.name;
    frame.x = x; frame.y = 0;
    frame.resize(screen.w, screen.h);
    frame.fills = [{ type: 'SOLID', color: BLUE }];
    frame.layoutMode = 'HORIZONTAL';
    frame.primaryAxisSizingMode = 'FIXED';
    frame.counterAxisSizingMode = 'FIXED';
    frame.paddingLeft = 96;   // Figma 실측 — 좌우 96
    frame.paddingRight = 96;
    frame.paddingTop = 0; frame.paddingBottom = 0;
    frame.itemSpacing = 0;    // 두 칸이 맞닿는다 — 오른쪽 단은 왼쪽 칸(반) 끝에서 시작
    frame.primaryAxisAlignItems = 'MIN';
    frame.counterAxisAlignItems = 'CENTER';   // 세로 가운데 — 두 단 모두 뷰포트 중심에 선다
    frame.clipsContent = true;
    const left = buildStatement();            // 왼쪽 칸: 반(또는 가장 긴 줄) 폭으로 고정
    left.counterAxisSizingMode = 'FIXED'; left.resize(screen.left, left.height);
    frame.appendChild(left);
    frame.appendChild(buildAside(screen.aside));
    return frame;
}

(async () => {
    try {
        await pickFonts();
        await figma.loadFontAsync({ family: FAMILY, style: REGULAR });
        await figma.loadFontAsync({ family: FAMILY, style: BOLD });
        await figma.loadFontAsync({ family: FAMILY, style: SEMIBOLD });

        const made = [];
        let x = 0;
        for (const s of SCREENS) { made.push(buildScreen(s, x)); x += s.w + 200; }
        figma.currentPage.appendChild(made[0]); // 이미 페이지에 있지만 순서 보장
        figma.viewport.scrollAndZoomIntoView(made);
        figma.closePlugin(`완료 — 글꼴 ${FAMILY} (${REGULAR}/${BOLD}), 프레임 ${made.length}개`);
    } catch (e) {
        figma.closePlugin('실패: ' + (e && e.message ? e.message : e));
    }
})();
