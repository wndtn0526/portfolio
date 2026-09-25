// 포트폴리오 · Figma 작업
// 로컬 서버(tools/figma-export-plugin/server.py)에서 작업(JSON)을 받아 그대로 한다 — 코드는 고정, 할 일은 작업 파일이 정한다.
//   task.file   이 파일에서만 실행한다(figma.root.name 과 대조). 엉뚱한 파일에 그리거나 내보내지 않게.
//   task.draw   [{ page, frame, x, y, export, items: [...] }] — 페이지에 프레임을 그리고(같은 이름 프레임은 지우고 다시), PNG 2x 로 내보낸다.
//               item: rect(상자) · text(글) · svg(선 · 화살표 · 마름모 같은 벡터). 좌표는 프레임 기준.
//   task.export [[노드 id, 이름], …] — 기존 노드를 PNG 2x 로 내보낸다.
// Dev Mode MCP get_screenshot 이 긴 변 1024px 로 막혀 있어서 만든 우회로에 그리기를 더한 것이다.
const SERVER = 'http://localhost:8899';
const FALLBACK = { family: 'Pretendard', style: 'Bold' };

function rgb(hex) {
  const h = hex.replace('#', '');
  return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 };
}
const solid = (hex) => [{ type: 'SOLID', color: rgb(hex) }];

async function post(name, bytes) {
  const r = await fetch(SERVER + '/save?name=' + encodeURIComponent(name), { method: 'POST', body: bytes });
  if (r.status !== 200) throw new Error('http ' + r.status);
}

// 폰트 — 없으면 Pretendard Bold 로 그리고 알린다.
const loaded = new Map();
async function font(f) {
  const key = f.family + '/' + f.style;
  if (!loaded.has(key)) {
    try { await figma.loadFontAsync(f); loaded.set(key, f); }
    catch (e) { await figma.loadFontAsync(FALLBACK); loaded.set(key, FALLBACK); MISSING.add(key); }
  }
  return loaded.get(key);
}
const MISSING = new Set();

async function make(it) {
  if (it.type === 'rect') {
    const n = figma.createRectangle();
    n.resize(it.w, it.h);
    n.fills = it.fill ? solid(it.fill) : [];
    if (it.stroke) { n.strokes = solid(it.stroke); n.strokeWeight = it.strokeWeight || 1; n.strokeAlign = 'INSIDE'; }
    n.cornerRadius = it.radius || 0;
    n.x = it.x; n.y = it.y;
    return n;
  }
  if (it.type === 'text') {
    const n = figma.createText();
    n.fontName = await font(it.font);
    n.fontSize = it.size;
    n.lineHeight = { value: it.lineHeight, unit: 'PIXELS' };
    n.letterSpacing = { value: it.tracking || 0, unit: 'PIXELS' };
    n.fills = solid(it.color);
    n.characters = it.lines.join('\n');
    n.textAlignHorizontal = it.align || 'LEFT';
    if (it.w) { n.textAutoResize = 'HEIGHT'; n.resize(it.w, n.height); n.textAutoResize = 'HEIGHT'; }
    else n.textAutoResize = 'WIDTH_AND_HEIGHT';
    n.x = it.x;
    n.y = it.cy !== undefined ? Math.round(it.cy - n.height / 2) : it.y;   // cy 가 오면 세로 가운데
    return n;
  }
  if (it.type === 'svg') {
    const n = figma.createNodeFromSvg(it.svg);
    n.fills = []; n.clipsContent = false;
    n.x = it.x; n.y = it.y;
    return n;
  }
  throw new Error('모르는 item: ' + it.type);
}

async function pageNamed(name) {
  let p = figma.root.children.find((c) => c.name === name);
  if (!p) { p = figma.createPage(); p.name = name; }
  await p.loadAsync();
  return p;
}

// 프레임을 내용에 딱 맞게 — 자식의 최소 좌표를 0 으로 옮기고 크기를 맞춘다(덱의 그룹을 내보낸 것과 같은 여백 없는 그림).
function fit(f) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const c of f.children) { x0 = Math.min(x0, c.x); y0 = Math.min(y0, c.y); x1 = Math.max(x1, c.x + c.width); y1 = Math.max(y1, c.y + c.height); }
  for (const c of f.children) { c.x -= x0; c.y -= y0; }
  f.resize(Math.ceil(x1 - x0), Math.ceil(y1 - y0));
}

async function main() {
  let task;
  try { task = await (await fetch(SERVER + '/task')).json(); }
  catch (e) { figma.notify('로컬 서버(8899)에서 작업을 못 받았다 — server.py 를 먼저 켠다', { error: true }); return figma.closePlugin(); }
  if (task.file && figma.root.name !== task.file) {
    figma.notify('이 작업은 ' + task.file + ' 파일에서 실행한다 (지금: ' + figma.root.name + ')', { error: true, timeout: 8000 });
    return figma.closePlugin();
  }
  const fails = []; let ok = 0;

  for (const d of task.draw || []) {
    const created = [];
    try {
      const page = await pageNamed(d.page);
      await figma.setCurrentPageAsync(page);
      for (const old of page.children.filter((c) => c.name === d.frame)) old.remove();
      const f = figma.createFrame(); created.push(f);
      f.name = d.frame; f.fills = []; f.clipsContent = false;
      page.appendChild(f);
      for (const it of d.items) { const n = await make(it); f.appendChild(n); if (it.name) n.name = it.name; }
      fit(f); f.x = d.x; f.y = d.y;
      if (d.export) { await post(d.export, await f.exportAsync({ format: 'PNG', constraint: { type: 'SCALE', value: 2 } })); ok++; }
    } catch (e) {
      for (const n of created) if (!n.removed) n.remove();      // 반쯤 그린 잔해를 남기지 않는다
      fails.push(d.frame + ' ' + (e && e.message ? e.message : e));
    }
  }

  for (const [id, name] of task.export || []) {
    try {
      const node = await figma.getNodeByIdAsync(id);
      if (!node) { fails.push(name + ' 없음'); continue; }
      await post(name, await node.exportAsync({ format: 'PNG', constraint: { type: 'SCALE', value: 2 } })); ok++;
    } catch (e) { fails.push(name + ' ' + (e && e.message ? e.message : e)); }
  }

  const miss = MISSING.size ? ' · 폰트 없음(Pretendard Bold 로 대체): ' + [...MISSING].join(', ') : '';
  figma.notify(ok + '장 내보냄' + (fails.length ? ' · 실패: ' + fails.join(', ') : '') + miss, { timeout: 8000 });
  figma.closePlugin();
}
main();
