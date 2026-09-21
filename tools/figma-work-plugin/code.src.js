/*
 * 웹의 프로젝트 섹션(#work — 회사 탭 · 왼쪽 목록 · 오른쪽 아티클)을 Figma 캔버스에 편집 가능한 auto-layout 레이어로 그린다.
 *
 * 값은 home.blade.php · app.css(.project-tab) · tokens.css 에서 1440/2056 폭으로 계산한 것이다.
 *   섹션 패딩 90(1440) / 110(2056) · 좌우 48 · 머리(탭 40 · 아래 줄 16/20 · 아래 보더 1px 검정 8% · pb 32) · 그리드 mt 40, 3fr | 7fr, 사이 64
 *   목록 행: py 16 · 위 보더(마지막 아래도) · 번호 40 | 제목 19 Medium(활성 잉크 + '/', 비활성 본문색) · 태그 13 흐림
 *   아티클(최대 940): 라벨 16.8/24 · 제목 32 Bold · 요약 20 · 태그 14 · 그림(모서리 12 · 보더) · 섹션(mt 40 · 위 보더 · pt 24 · 제목 20 SemiBold · 본문 16/1.625)
 *   그려지는 상태: 그룹웨어프로 탭 활성 · 첫 프로젝트 아티클. 다른 회사 · 프로젝트는 SCREEN 의 company/project 를 바꿔 다시 돌린다.
 *
 * ⚠️ Figma MCP 서버는 읽기만 되고 쓰기 도구가 없어서 플러그인으로 넣는다(실행법은 README).
 * ⚠️ Pretendard(Regular/Medium/SemiBold/Bold)가 이 맥에 있어야 한다. 없으면 Inter 로 대신한다.
 * ⚠️ 이 파일은 code.src.js 다. 데이터와 그림을 박은 code.js 는 build.sh 가 만든다.
 */

const DATA = __DATA_JSON__;          // resources/data/projects.php 그대로 (build.sh)
const PHOTO_B64 = '__PHOTO_B64__';   // public/images/projects/gpro-home.webp → PNG
const IMAGES = __IMAGES_JSON__;      // public/images/projects/*.webp → PNG base64 (캐러셀 화면 캡처)
const DIAGRAMS = __DIAGRAMS_JSON__;  // public/images/projects/*.svg (도식) — createNodeFromSvg 로 편집 가능한 레이어가 된다

const hex = (h) => ({ r: parseInt(h.slice(1, 3), 16) / 255, g: parseInt(h.slice(3, 5), 16) / 255, b: parseInt(h.slice(5, 7), 16) / 255 });
const C = { canvas: hex('#f9f9f9'), ink: hex('#212529'), body: hex('#495057'), muted: hex('#868e96'), white: hex('#ffffff'), black: hex('#000000') };
const BORDER = { color: C.black, opacity: 0.08 };

// 크기 · 행간% · 자간% — tokens.css. clamp 로 흐르는 값은 화면별로 SCREEN 에서 준다.
const T = {
    title1:   { size: 32, lh: 150, ls: -3.13 },
    heading2: { size: 20, lh: 150, ls: -5 },
    headline1:{ size: 19, lh: 152.6, ls: -3.16 },
    body1r:   { size: 16, lh: 162.5, ls: -3.75 },
    label1:   { size: 14, lh: 142.9, ls: -1.43 },
    label2:   { size: 13, lh: 153.8, ls: -1.54 },
    caption2: { size: 11, lh: 154.5, ls: 12 },
    tabs:     { size: 40, lh: 130, ls: -2.5 },
    // 목록 행 — Figma 6:553(2056 조절본) 값
    listNum:  { size: 20, lh: 152.6, ls: -2 },
    listTitle:{ size: 20, lh: 152.6, ls: -3.16 },
    listMeta: { size: 16, lh: 153.8, ls: -1.54 },
};

const SCREENS = [
    { name: '04 프로젝트 — 1440', w: 1440, pad: 90,  meta: { size: 16, lh: 153.3, ls: -4 }, label: { size: 16.8, lh: 154.5, ls: -2 }, company: 'gpro', project: 'gpro-launch' },
    { name: '04 프로젝트 — 2056 (풀 화면)', w: 2056, pad: 110, meta: { size: 20, lh: 153.3, ls: -4 }, label: { size: 24, lh: 154.5, ls: -2 }, company: 'gpro', project: 'gpro-launch' },
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

// ── 텍스트 ──
// parts: [{ t, style, color }] 를 한 텍스트 노드로 — 라벨(SemiBold 잉크) + ' : ' + 본문 같은 혼합 문단용
const CREATED = [];   // 이번 실행에서 만든 노드 — 실패 시 정리용
function rich(parts, spec, { width = null, stretch = false, align = 'LEFT' } = {}) {
    const node = figma.createText(); CREATED.push(node);
    node.fontName = { family: FAMILY, style: F.regular };
    node.characters = parts.map((p) => p.t).join('');
    node.fontSize = spec.size;
    node.lineHeight = { unit: 'PERCENT', value: spec.lh };
    node.letterSpacing = { unit: 'PERCENT', value: spec.ls };
    node.textAlignHorizontal = align;
    let i = 0;
    for (const p of parts) {
        const len = p.t.length;
        if (len) {
            node.setRangeFontName(i, i + len, { family: FAMILY, style: p.style || F.regular });
            node.setRangeFills(i, i + len, [{ type: 'SOLID', color: p.color || C.body }]);
            if (p.underline) node.setRangeTextDecoration(i, i + len, 'UNDERLINE');
        }
        i += len;
    }
    if (width) { node.textAutoResize = 'HEIGHT'; node.resize(width, 10); }
    else if (stretch) { node.textAutoResize = 'HEIGHT'; node.layoutAlign = 'STRETCH'; }
    else node.textAutoResize = 'WIDTH_AND_HEIGHT';
    return node;
}
const text = (t, style, spec, color, opts) => rich([{ t, style, color }], spec, opts);

// '<strong>…</strong>' 만 쓰는 본문을 parts 로 — 굵은 구간은 SemiBold 잉크
function strongParts(html) {
    html = String(html).replace(/<(?!\/?strong\b)[^>]+>/g, '');   // <a> 등 다른 태그는 글자만 남긴다
    const parts = [];
    const re = /<strong>(.*?)<\/strong>/g;
    let last = 0, m;
    while ((m = re.exec(html))) {
        if (m.index > last) parts.push({ t: html.slice(last, m.index), style: F.regular, color: C.body });
        parts.push({ t: m[1], style: F.semibold, color: C.ink });
        last = m.index + m[0].length;
    }
    if (last < html.length) parts.push({ t: html.slice(last), style: F.regular, color: C.body });
    return parts;
}

// ── 프레임 ──
function frame(name, dir, { gap = 0, pad = [0, 0, 0, 0], width = null, stretch = false, fill = null, align = 'MIN' } = {}) {
    const f = figma.createFrame(); CREATED.push(f);
    f.name = name;
    f.layoutMode = dir;
    f.itemSpacing = gap;
    [f.paddingTop, f.paddingRight, f.paddingBottom, f.paddingLeft] = pad;
    f.fills = fill ? [{ type: 'SOLID', color: fill }] : [];
    f.primaryAxisSizingMode = 'AUTO';
    f.counterAxisSizingMode = 'AUTO';
    f.counterAxisAlignItems = align;
    if (width) {
        // ⚠️ auto-layout 프레임에 resize() 를 부르면 두 축 sizing 이 모두 FIXED 로 바뀐다 — 그래서 목록 · 아티클이 높이 10 에 갇혀 있었다.
        //    resize 뒤에 폭은 FIXED, 진행 방향은 AUTO(hug) 로 다시 정한다.
        f.resize(width, 10);
        if (dir === 'HORIZONTAL') { f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'AUTO'; }
        else { f.counterAxisSizingMode = 'FIXED'; f.primaryAxisSizingMode = 'AUTO'; }
    }
    if (stretch) { f.layoutAlign = 'STRETCH'; if (dir === 'HORIZONTAL') f.primaryAxisSizingMode = 'FIXED'; else f.counterAxisSizingMode = 'FIXED'; }
    return f;
}
// ⚠️ 텍스트 노드에는 sizing 속성이 없다 — 첫 실행에서 여기서 죽어 반쯤 만든 노드가 페이지에 남았다. 프레임일 때만 만진다.
const grow = (n) => { n.layoutGrow = 1; if (n.type === 'FRAME') { if (n.layoutMode === 'VERTICAL') n.counterAxisSizingMode = 'FIXED'; else n.primaryAxisSizingMode = 'FIXED'; } return n; };
function border(node, { top = false, bottom = false } = {}) {
    node.strokes = [{ type: 'SOLID', color: BORDER.color, opacity: BORDER.opacity }];
    node.strokeTopWeight = top ? 1 : 0; node.strokeBottomWeight = bottom ? 1 : 0; node.strokeLeftWeight = 0; node.strokeRightWeight = 0;
    return node;
}

// ── 머리: 회사 탭 + 기간 줄 ──
function buildHeader(screen, company) {
    const head = border(frame('머리', 'VERTICAL', { gap: 12, pad: [0, 0, 32, 0], stretch: true }), { bottom: true });
    const tabs = frame('회사 탭', 'HORIZONTAL', { gap: 32, align: 'BASELINE' });
    for (const c of DATA) tabs.appendChild(text(c.name, F.regular, T.tabs, c.slug === company.slug ? C.ink : C.muted));
    head.appendChild(tabs);
    head.appendChild(text(company.meta, F.regular, screen.meta, C.body, { stretch: true }));
    return head;
}

// ── 왼쪽 목록 ──
function buildList(company, activeSlug, width) {
    const col = frame('목록', 'VERTICAL', { width });
    company.projects.forEach((p, i) => {
        const active = p.slug === activeSlug;
        const row = border(frame('행 · ' + p.title, 'HORIZONTAL', { gap: 16, pad: [16, 0, 16, 0], stretch: true, align: 'BASELINE' }),
                           { top: i > 0, bottom: i === company.projects.length - 1 });   // Figma 6:553: 첫 행은 위 보더 없음
        const num = frame('번호', 'VERTICAL', { width: 40 });
        num.appendChild(text(String(i + 1).padStart(2, '0'), F.semibold, T.listNum, C.muted));
        row.appendChild(num);
        const body = frame('내용', 'VERTICAL', { gap: 4 });
        // '/' 는 비활성일 때도 자리를 차지한다(웹: opacity 0). 여기서는 배경색 글자로 숨긴다.
        body.appendChild(rich([{ t: '/', style: F.bold, color: active ? C.ink : C.canvas }, { t: p.title, style: F.medium, color: active ? C.ink : C.body }], T.listTitle, { stretch: true }));
        body.appendChild(text(p.year || p.tags.join(' · '), F.regular, T.listMeta, C.muted, { stretch: true }));   // Figma 6:553: 태그 대신 연도
        row.appendChild(grow(body));
        col.appendChild(row);
    });
    return col;
}

// ── 오른쪽 아티클 ──
function buildArticle(screen, company, project, width) {
    const art = frame('아티클 · ' + project.title, 'VERTICAL', { width });
    const idx = company.projects.indexOf(project);
    art.appendChild(text('Project ' + String(idx + 1).padStart(2, '0'), F.semibold, screen.label, C.muted));
    art.appendChild(wrap(text(project.title, F.bold, T.title1, C.ink, { stretch: true }), 12));
    art.appendChild(wrap(text(project.lead, F.regular, T.heading2, C.body, { stretch: true }), 16));
    const tags = frame('태그', 'HORIZONTAL', { gap: 12 });
    for (const t of project.tags) tags.appendChild(text(t, F.regular, T.label1, C.muted));
    art.appendChild(wrap(tags, 16));

    if (project.figure) {
        const fig = frame('그림', 'VERTICAL', { gap: 12, stretch: true });
        const img = figma.createRectangle(); CREATED.push(img);
        img.name = project.figure.caption || '그림';
        img.resize(width, Math.round(width * project.figure.height / project.figure.width));
        img.cornerRadius = 12;
        img.strokes = [{ type: 'SOLID', color: BORDER.color, opacity: BORDER.opacity }]; img.strokeWeight = 1;
        const image = figma.createImage(figma.base64Decode(PHOTO_B64));
        img.fills = [{ type: 'IMAGE', scaleMode: 'FILL', imageHash: image.hash }];
        fig.appendChild(img);
        if (project.figure.caption) fig.appendChild(text(project.figure.caption, F.regular, T.label2, C.muted, { stretch: true }));
        art.appendChild(wrap(fig, 32));
    }

    project.sections.forEach((s, n) => {
        const sec = border(frame(`${n + 1}. ${s.title}`, 'VERTICAL', { gap: 16, pad: [24, 0, 0, 0], stretch: true }), { top: true });
        sec.appendChild(text(`${n + 1}. ${s.title}`, F.semibold, T.heading2, C.ink));
        const items = frame('항목', 'VERTICAL', { gap: 16, stretch: true });
        for (const it of s.items) {
            if (it.image) continue;   // 본문 그림은 이 화면에 없다(머리 그림만)
            if (it.diagram) {         // 도식 — SVG 를 네이티브 레이어로. 아티클 폭에 맞춰 축소.
                const svg = DIAGRAMS[it.diagram.file];
                if (svg) {
                    const fig = frame('도식', 'VERTICAL', { gap: 12, stretch: true });
                    const n = figma.createNodeFromSvg(svg); CREATED.push(n);
                    n.name = it.diagram.caption || '도식';
                    n.rescale(width / n.width);
                    fig.appendChild(n);
                    if (it.diagram.caption) fig.appendChild(text(it.diagram.caption, F.regular, T.label2, C.muted, { stretch: true }));
                    items.appendChild(fig);
                }
                continue;
            }
            if (it.carousel) {        // 캐러셀 — Figma 에서는 세로로 쌓는다(한 장씩 + 설명)
                const col = frame('캐러셀', 'VERTICAL', { gap: 16, stretch: true });
                for (const sl of it.carousel.slides) {
                    const b64 = IMAGES[sl.src];
                    if (!b64) continue;
                    const one = frame(sl.label, 'VERTICAL', { gap: 8, stretch: true });
                    const img = figma.createRectangle(); CREATED.push(img);
                    img.name = sl.label; img.resize(width, Math.round(width * sl.height / sl.width)); img.cornerRadius = 12;
                    img.strokes = [{ type: 'SOLID', color: BORDER.color, opacity: BORDER.opacity }]; img.strokeWeight = 1;
                    img.fills = [{ type: 'IMAGE', scaleMode: 'FILL', imageHash: figma.createImage(figma.base64Decode(b64)).hash }];
                    one.appendChild(img);
                    one.appendChild(rich([{ t: sl.label, style: F.semibold, color: C.ink }, { t: ' · ' + sl.note, style: F.regular, color: C.muted }], T.label2, { stretch: true }));
                    col.appendChild(one);
                }
                if (it.carousel.caption) col.appendChild(text(it.carousel.caption, F.regular, T.label2, C.muted, { stretch: true }));
                items.appendChild(col);
                continue;
            }
            if (it.links) {           // 딥다이브 링크 목록 — 밑줄 제목 + 연도 + →
                const ul = frame('링크', 'VERTICAL', { gap: 12, stretch: true });
                for (const slug of it.links) {
                    const lp = company.projects.find((q) => q.slug === slug);
                    if (lp) ul.appendChild(rich([{ t: lp.title, style: F.semibold, color: C.ink, underline: true }, { t: '  ' + (lp.year || ''), style: F.regular, color: C.muted }, { t: '  →', style: F.semibold, color: C.ink }], T.heading2));
                }
                items.appendChild(ul);
                continue;
            }
            const item = frame(it.label || '단락', 'VERTICAL', { gap: 8, stretch: true });
            const parts = [];
            if (it.label) parts.push({ t: it.label, style: F.semibold, color: C.ink });
            if (it.label && it.text) parts.push({ t: ' : ', style: F.regular, color: C.muted });
            if (it.text) parts.push(...strongParts(it.text));
            if (parts.length) item.appendChild(rich(parts, T.body1r, { stretch: true }));
            if (it.sub && it.sub.length) {
                const list = frame('하위', 'VERTICAL', { gap: 6, stretch: true });
                it.sub.forEach((sub, k) => {
                    const li = frame('항', 'HORIZONTAL', { gap: 0, stretch: true, align: 'MIN' });
                    const marker = frame('표', 'VERTICAL', { width: 24 });
                    marker.appendChild(text(String.fromCharCode(97 + k) + '.', F.regular, T.body1r, C.muted));
                    li.appendChild(marker);
                    const sp = typeof sub === 'string'
                        ? strongParts(sub)
                        : [{ t: sub.label, style: F.semibold, color: C.ink }, { t: ' : ', style: F.regular, color: C.muted }, ...strongParts(sub.text)];
                    li.appendChild(grow(rich(sp, T.body1r, { stretch: true })));
                    list.appendChild(li);
                });
                item.appendChild(list);
            }
            items.appendChild(item);
        }
        sec.appendChild(items);
        art.appendChild(wrap(sec, 40));
    });

    if (project.draft) {   // appendChild 는 값을 돌려주지 않는다 — 이어 붙이지 말고 먼저 만든다
        const dr = border(frame('정리 중', 'VERTICAL', { pad: [24, 0, 0, 0], stretch: true }), { top: true });
        dr.appendChild(text('상세 내용은 정리 중입니다.', F.regular, T.label1, C.muted));
        art.appendChild(wrap(dr, 40));
    }

    if (company.projects.length > 1) {
        const next = company.projects[(idx + 1) % company.projects.length];
        const nx = border(frame('다음 프로젝트', 'VERTICAL', { gap: 8, pad: [24, 0, 0, 0], stretch: true }), { top: true });
        nx.appendChild(text('다음 프로젝트', F.regular, T.label1, C.muted));
        nx.appendChild(rich([{ t: next.title, style: F.semibold, color: C.ink, underline: true }, { t: '  →', style: F.semibold, color: C.ink }], T.heading2));
        art.appendChild(wrap(nx, 48));
    }
    return art;
}
// 위 여백만 다른 항목을 auto-layout 에 넣기 위한 껍데기(mt-*)
function wrap(node, top) { const w = frame(node.name, 'VERTICAL', { pad: [top, 0, 0, 0], stretch: true }); w.appendChild(node); return w; }

function buildScreen(screen, x) {
    const company = DATA.find((c) => c.slug === screen.company) || DATA[0];
    const project = company.projects.find((p) => p.slug === screen.project) || company.projects[0];
    const root = frame(screen.name, 'VERTICAL', { pad: [screen.pad, 48, screen.pad, 48], width: screen.w, fill: C.canvas });
    root.x = x; root.y = 0; root.clipsContent = true;
    root.appendChild(buildHeader(screen, company));

    const inner = screen.w - 96;
    const listW = Math.round((inner - 64) * 0.3);
    const artW = Math.min(940, inner - 64 - listW);   // max-w-readable 940
    const grid = frame('목록 + 아티클', 'HORIZONTAL', { gap: 64, pad: [40, 0, 0, 0], stretch: true, align: 'MIN' });
    grid.appendChild(buildList(company, project.slug, listW));
    grid.appendChild(buildArticle(screen, company, project, artW));
    root.appendChild(grid);
    return root;
}

// 이전 실행이 중간에 죽어 페이지 맨 위에 남은 잔해를 치운다.
// 우리 이름표를 단 최상위 노드(중간 프레임 · 우리 글 텍스트)와, 덜 만들어진 '04 프로젝트' 프레임(높이 600 미만)만 지운다 — 완성돼 사용자가 손댄 프레임은 남긴다.
function sweepLeftovers() {
    const ours = new Set(['목록 + 아티클', '머리', '회사 탭', '목록', '번호', '내용', '태그', '그림', '도식', '링크', '캐러셀', '항목', '하위', '항', '표', '정리 중', '다음 프로젝트', '단락']);
    const strip = (t) => String(t || '').replace(/<[^>]+>/g, '');
    for (const c of DATA) {
        ours.add(c.name); ours.add(c.meta);
        for (const p of c.projects) {
            ours.add(p.title); ours.add(p.lead); ours.add('아티클 · ' + p.title); ours.add('행 · ' + p.title);
            p.tags.forEach((t) => ours.add(t));
            if (p.figure && p.figure.caption) ours.add(p.figure.caption);
            p.sections.forEach((s) => s.items.forEach((it) => { if (it.diagram && it.diagram.caption) ours.add(it.diagram.caption); }));
            p.sections.forEach((s, n) => {
                ours.add(`${n + 1}. ${s.title}`);
                for (const it of s.items) {
                    if (it.label) { ours.add(it.label); ours.add(it.label + ' : ' + strip(it.text)); }
                    if (it.text) ours.add(strip(it.text));
                    (it.sub || []).forEach((sub) => { if (typeof sub === 'string') ours.add(strip(sub)); else { ours.add(sub.label); ours.add(sub.label + ' : ' + strip(sub.text)); } });
                }
            });
        }
    }
    let n = 0;
    for (const node of [...figma.currentPage.children]) {
        const half = node.name.startsWith('04 프로젝트') && node.height < 600;
        if (half || ours.has(node.name) || (node.type === 'TEXT' && ours.has(node.characters))) { node.remove(); n++; }
    }
    return n;
}

(async () => {
    let swept = 0;
    try {
        swept = sweepLeftovers();
        await pickFonts();
        for (const s of Object.values(F)) await figma.loadFontAsync({ family: FAMILY, style: s });
        const made = [];
        let x = 0;
        for (const s of SCREENS) { made.push(buildScreen(s, x)); x += s.w + 200; }
        figma.viewport.scrollAndZoomIntoView(made);
        figma.closePlugin(`완료 — 글꼴 ${FAMILY}, 프레임 ${made.length}개` + (swept ? ` (이전 잔해 ${swept}개 정리)` : ''));
    } catch (e) {
        // 이번에 만든 노드 중 페이지에 직접 붙은 것을 지운다(자식은 함께 사라진다) — 반쯤 만든 것이 남지 않게
        for (const n of CREATED) { try { if (!n.removed && n.parent && n.parent.type === 'PAGE') n.remove(); } catch (_) {} }
        figma.closePlugin('실패: ' + (e && e.message ? e.message : e));
    }
})();
