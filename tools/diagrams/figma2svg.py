#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figma 노드(덱 슬라이드)의 일부 영역을 SVG 로 그대로 옮긴다 — 캡처가 아니라 도형 · 글자 · 벡터를 다시 그린 것이라 어느 크기에서도 선명하다.

  Dev Mode MCP get_design_context 의 JSX 를 읽는다: absolute left/top/size 클래스로 기하를, bg/text/font/rounded/opacity 로 스타일을,
  localhost 에셋(선 · 화살촉 · 원 · 그라디언트 도형)은 받아서 <image> 로 박는다. 크기가 클래스에 없는 노드는 get_metadata 의 w · h 로 보탠다.
  flex(auto-layout) 안의 자식은 위치를 못 계산하므로 부모 상자를 그대로 쓴다(배지 · 라벨처럼 한 자식만 있는 경우에 맞다).

사용: python3 tools/diagrams/figma2svg.py [이름 일부 …]
      Figma 데스크톱에서 GPRO_PORTFOLIO 가 열려 있고 MCP 서버(127.0.0.1:3845)가 살아 있어야 한다. 세션은 스크래치패드 figma.sh 로.
⚠️ 글자 줄바꿈은 JSX 의 <p> 줄만 따른다(자동 줄바꿈은 안 한다) — 도식 영역의 짧은 라벨에는 충분하다.
"""
import json, re, subprocess, sys, base64, urllib.request, html, math, os
DEBUG = bool(os.environ.get('F2S_DEBUG'))
from pathlib import Path
from html.parser import HTMLParser

SP = Path('/private/tmp/claude-501/-Users-sinjungsu-Documents-GitHub-404/2c6cef4f-1221-4214-8044-4ed6ffeece53/scratchpad')
CACHE = SP / 'f2s'; CACHE.mkdir(exist_ok=True)
OUT = Path(__file__).resolve().parents[2] / 'public/images/projects'
FONT = "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, sans-serif"
WEIGHT = {'Thin': 100, 'ExtraLight': 200, 'Light': 300, 'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Bold': 700, 'ExtraBold': 800, 'Black': 900}

def mcp(name, args):
    out = subprocess.run([str(SP / 'figma.sh'), 'call', name, json.dumps(args)], capture_output=True, text=True, cwd=SP).stdout
    return json.loads(out)['result']['content']

def fetch(nid):
    key = nid.replace(':', '-'); meta_p, jsx_p = CACHE / f'{key}.xml', CACHE / f'{key}.jsx'
    if not meta_p.exists(): meta_p.write_text(''.join(c.get('text', '') for c in mcp('get_metadata', {'nodeId': nid}) if c.get('type') == 'text'))
    if not jsx_p.exists(): jsx_p.write_text(''.join(c.get('text', '') for c in mcp('get_design_context', {'nodeId': nid, 'clientLanguages': 'html', 'clientFrameworks': 'unknown', 'excludeScreenshot': True}) if c.get('type') == 'text' and 'data-node-id' in c.get('text', '')))
    return meta_p.read_text(), jsx_p.read_text()

def meta_sizes(xml):
    return {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r'<\w+ id="([^"]+)" name="[^"]*" x="-?\d+" y="-?\d+" width="(\d+)" height="(\d+)"', xml)}

# ── JSX → 트리 ──
class Tree(HTMLParser):
    def __init__(self, assets):
        super().__init__(convert_charrefs=True); self.assets = assets
        self.root = {'tag': 'root', 'cls': '', 'kids': [], 'lines': [], 'line_cls': [], 'nid': None, 'img': None, 'grad': None}
        self.stack = [self.root]; self.cur_line = None; self.ul_depth = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = a.get('class', '') or ''
        node = {'tag': tag, 'cls': cls, 'kids': [], 'lines': [], 'line_cls': [], 'nid': a.get('data-node-id'), 'img': None, 'grad': a.get('data-grad')}
        parent = self.stack[-1]
        if tag in ('ul', 'ol'):
            self.ul_depth += 1; self.stack.append(parent); return
        if tag == 'img':
            parent['img'] = self.assets.get(a.get('src', ''), a.get('src')); return
        if tag == 'br':
            if self.cur_line: self.cur_line['lines'].append(''); self.cur_line['line_cls'].append('')
            return
        if tag in ('p', 'li') and not node['nid']:  # 부모 텍스트의 한 줄 (li 는 글머리표를 단다)
            bullet = ('•  ' if self.ul_depth == 1 else '      ·  ') if tag == 'li' else ''
            parent['lines'].append(bullet); parent['line_cls'].append(cls); self.cur_line = parent; self.trail = False
            self.stack.append(node); return
        if tag == 'p':                               # 자기 자신이 텍스트 노드
            node['lines'].append(''); node['line_cls'].append(''); self.cur_line = node
        parent['kids'].append(node); self.stack.append(node)
    def handle_endtag(self, tag):
        if tag in ('img', 'br'): return
        if tag in ('ul', 'ol'):
            self.ul_depth = max(0, self.ul_depth - 1)
            if len(self.stack) > 1: self.stack.pop()
            return
        if tag in ('p', 'li'): self.cur_line = None
        if len(self.stack) > 1: self.stack.pop()
    def handle_data(self, data):
        lead = ' ' if (data[:1].isspace() or data.startswith('{" "}') or getattr(self, 'trail', False)) else ''
        self.trail = data[-1:].isspace() or data.endswith('{" "}')
        t = re.sub(r'^\{`|`\}$', '', data.strip()).replace('{" "}', ' ').strip()
        if not t: return
        if self.cur_line and self.cur_line['lines']:
            cur = self.cur_line['lines'][-1]
            self.cur_line['lines'][-1] = cur + (lead if cur and not cur.endswith(' ') else '') + t
        else:
            n = self.stack[-1]
            if n['tag'] == 'div': n['lines'].append(t); n['line_cls'].append('')

def inline_helpers(jsx):
    """function X(...) { return (<jsx/>); } 로 정의된 헬퍼(인스턴스 컴포넌트)를 호출 자리에 펼친다. className 은 호출 쪽 값으로."""
    helpers = {m.group(1): m.group(2) for m in re.finditer(r'\nfunction (\w+)\([^)]*\)[^{]*\{\n  return \(\n([\s\S]*?)\n  \);\n\}', jsx)}
    main = jsx[jsx.index('export default function'):]
    body = main[main.index('return ('):main.rindex(');')]
    def expand(text, depth=0):
        if depth > 4: return text
        def sub(m):
            name, attrs = m.group(1), m.group(2)
            props = dict(re.findall(r'(\w+)=(?:"([^"]*)"|\{"([^"]*)"\}|\{([^}]*)\})', attrs) and [(k, a or b or c) for k, a, b, c in re.findall(r'(\w+)=(?:"([^"]*)"|\{"([^"]*)"\}|\{([^}]*)\})', attrs)])
            h = helpers[name]
            h = re.sub(r'className=\{className \|\| "([^"]*)"\}', lambda mm: f'className="{props.get("className", mm.group(1))}"', h)
            h = re.sub(r'className=\{`([^`]*)`\}', lambda mm: 'className="' + re.sub(r'\$\{[^}]*\}', '', mm.group(1)) + '"', h)
            for k, v in props.items(): h = h.replace('{' + k + '}', v)
            h = re.sub(r'src=\{(\w+)\}', r'src="\1"', h)
            h = re.sub(r'\{[^{}<>]*\}', '', h)   # 남은 표현식은 지운다
            return h
        pat = '<(' + '|'.join(map(re.escape, helpers)) + r')((?:\s+\w+=(?:"[^"]*"|\{[^}]*\}))*)\s*/>' if helpers else None
        return expand(re.sub(pat, sub, text), depth + 1) if pat and re.search(pat, text) else text
    return expand(body)

def parse_jsx(jsx):
    assets = dict(re.findall(r'const (\w+) = "([^"]+)";', jsx))
    body = inline_helpers(jsx)
    body = re.sub(r'style=\{\{\s*backgroundImage:\s*"([^"]+)"\s*\}\}', lambda m: f'data-grad="{html.escape(m.group(1))}"', body)
    body = re.sub(r'style=\{\{[^}]*\}\}', '', body)
    body = re.sub(r'src=\{(\w+)\}', r'src="\1"', body).replace('className=', 'class=')
    t = Tree(assets); t.feed(body); return t.root

def px(cls, key):
    m = re.search(r'(?<![\w-])' + key + r'-\[(-?[\d.]+)px\]', cls); return float(m.group(1)) if m else None
def calc(cls, key, parent_len):
    m = re.search(r'(?<![\w-])' + key + r'-\[calc\(50%([+-])([\d.]+)px\)\]', cls)
    if m: return parent_len / 2 + (float(m.group(2)) if m.group(1) == '+' else -float(m.group(2)))
    return px(cls, key)
def color(cls, prefix):
    m = re.search(r'(?<![\w-])' + prefix + r'-\[(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))\]', cls)
    if m: return m.group(1)
    m = re.search(r'(?<![\w-])' + prefix + r'-\[var\([^,\]]*,\s*([^)\]]+)\)\]', cls)   # bg-[var(--mono\/w,white)]
    if m: return {'white': '#ffffff', 'black': '#000000'}.get(m.group(1).strip(), m.group(1).strip())
    if re.search(r'(?<![\w-])' + prefix + r'-white\b', cls): return '#ffffff'
    if re.search(r'(?<![\w-])' + prefix + r'-black\b', cls): return '#000000'
    return None

_assets = {}
def asset_size(url):
    f = CACHE / url.rsplit('/', 1)[-1]
    if not f.exists(): f.write_bytes(urllib.request.urlopen(url, timeout=30).read())
    if f.suffix != '.svg': return None
    m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', f.read_text(errors='ignore'))
    return (float(m.group(1)), float(m.group(2))) if m else None
def data_uri(url):
    if url not in _assets:
        f = CACHE / url.rsplit('/', 1)[-1]
        if not f.exists(): f.write_bytes(urllib.request.urlopen(url, timeout=30).read())
        _assets[url] = f'data:{"image/svg+xml" if f.suffix == ".svg" else "image/png"};base64,' + base64.b64encode(f.read_bytes()).decode()
    return _assets[url]

def grad(g, gid, defs):
    m = re.match(r'linear-gradient\(([\d.]+)deg,\s*(.+)\)', g)
    if not m: return None
    a = math.radians(float(m.group(1))); x2, y2 = 0.5 + 0.5 * math.sin(a), 0.5 - 0.5 * math.cos(a)
    stops = re.findall(r'(rgba?\([^)]*\)|#[0-9a-fA-F]+)\s+([\d.]+)%', m.group(2))
    defs.append(f'<linearGradient id="{gid}" x1="{1-x2:.3f}" y1="{1-y2:.3f}" x2="{x2:.3f}" y2="{y2:.3f}">' + ''.join(f'<stop offset="{o}%" stop-color="{c}"/>' for c, o in stops) + '</linearGradient>')
    return f'url(#{gid})'

def render(nid, region, out_name, root_size=(1920, 1080), skip_png=False, skip_ids=(), flip_v_at=()):
    xml, jsx = fetch(nid); sizes = meta_sizes(xml); tree = parse_jsx(jsx)
    rx, ry, rw, rh = region; body, defs = [], []; gi = [0]
    def walk(node, px_, py_, pw, ph, in_flex, box=None, inh=None):
        cls = node['cls']
        inh = dict(inh or {})
        c_ = color(cls, 'text'); f_ = px(cls, 'text'); fam_ = re.search(r"font-\['[^:'\]]+:(\w+)'\]", cls)
        if c_: inh['color'] = c_
        if f_: inh['fs'] = f_
        if fam_: inh['weight'] = WEIGHT.get(fam_.group(1), 400)
        if node['nid'] in skip_ids: return
        if node['tag'] == 'root':
            for k in node['kids']: walk(k, 0, 0, root_size[0], root_size[1], False, inh=inh)
            return
        if 'contents' in cls.split():             # 그룹: 자식은 부모 좌표계 그대로
            for k in node['kids']: walk(k, px_, py_, pw, ph, in_flex, inh=inh)
            return
        # 크기
        w = px(cls, 'w') or px(cls, 'size'); h = px(cls, 'h') or px(cls, 'size')
        pw_ = pw or 0; ph_ = ph or 0
        pc = lambda key, L: (lambda m: L * float(m.group(1)) / 100 if m else None)(re.search(r'(?<![\w-])' + key + r'-\[([\d.]+)%\]', cls))
        w = w or pc('w', pw_); h = h or pc('h', ph_)
        if 'size-full' in cls or 'inset-0' in cls: w, h = pw, ph
        ins = re.search(r'inset-\[([^\]]+)\]', cls); ins_box = None
        if ins:
            parts = ins.group(1).split('_'); parts = (parts * 4)[:4] if len(parts) in (1, 2) else parts
            def L(v, ref): return 0 if v == '0' else (ref * float(v[:-1]) / 100 if v.endswith('%') else float(v[:-2]))
            tt, rr, bb, ll = L(parts[0], ph_), L(parts[1], pw_), L(parts[2], ph_), L(parts[3], pw_)
            ins_box = (px_ + ll, py_ + tt, pw_ - ll - rr, ph_ - tt - bb); w, h = ins_box[2], ins_box[3]
        if node['nid'] in sizes: mw, mh = sizes[node['nid']]; w = w or mw; h = h or mh
        # 위치
        if 'absolute' in cls.split():
            l = calc(cls, 'left', pw); t = calc(cls, 'top', ph)
            if l is None: l = pc('left', pw_)
            if t is None: t = pc('top', ph_)
            if 'inset-0' in cls: l, t = 0, 0
            x = px_ + (l or 0); y = py_ + (t or 0)
            if ins_box: x, y = ins_box[0], ins_box[1]
            if '-translate-x-1/2' in cls and w: x -= w / 2
            if '-translate-y-1/2' in cls and h: y -= h / 2
        elif node['nid'] == nid or 'relative size-full' in cls:
            x, y, w, h = 0, 0, root_size[0], root_size[1]
        elif box:                                    # flex 부모가 배치한 상자
            x, y, w, h = box
        else:                                        # 그 외 — 부모 상자
            x, y = px_, py_; w = w or pw; h = h or ph
        if w is None or h is None: w = w or 0; h = h or 0
        inside = not (x + w < rx or x > rx + rw or y + h < ry or y > ry + rh)
        if DEBUG: print(f'  {node["nid"]} {node["tag"]} ({x:.0f},{y:.0f},{w:.0f},{h:.0f}) inside={inside} lines={len(node["lines"])} img={bool(node["img"])} cls={cls[:60]}')
        if inside and node['nid'] != nid:
            op = re.search(r'\bopacity-(\d+)\b', cls); opacity = int(op.group(1)) / 100 if op else 1
            fill = color(cls, 'bg'); stroke = color(cls, 'border')
            rad = px(cls, 'rounded'); r = rad if rad is not None else (min(w, h) / 2 if 'rounded-full' in cls else 0)
            if node['grad'] and not node['lines'] and 'bg-clip-text' not in cls and w and h:
                gi[0] += 1; gfill = grad(html.unescape(node['grad']), f'g{gi[0]}', defs)
                if gfill: body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{gfill}" fill-opacity="{opacity}"/>')
            elif fill and 'bg-clip-text' not in cls and w and h:
                body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" fill-opacity="{opacity}"' + (f' stroke="{stroke}"' if stroke else '') + '/>')
            elif stroke and w and h:
                body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="none" stroke="{stroke}" opacity="{opacity}"/>')
            if node['img'] and str(node['img']).startswith('http') and w and h and not (skip_png and str(node['img']).endswith('.png')):
                nat = asset_size(node['img'])
                if nat and nat[0] > 0 and nat[1] > 0 and ((nat[0] > nat[1]) != (w > h)) and max(w, h) / max(min(w, h), 1) > 2:
                    # 회전된 인스턴스(예: 세로 화살표): 에셋은 가로인데 상자는 세로 — 90도 돌려 그린다
                    cx, cy = x + w / 2, y + h / 2
                    flip = any(abs(x - fx) < 2 and abs(y - fy) < 2 for fx, fy in flip_v_at)
                    tf = (f'translate(0 {2 * y + h:.1f}) scale(1 -1) ' if flip else '') + f'rotate(90 {cx:.1f} {cy:.1f})'
                    body.append(f'<image x="{cx - h / 2:.1f}" y="{cy - w / 2:.1f}" width="{h:.1f}" height="{w:.1f}" href="{data_uri(node["img"])}" preserveAspectRatio="none" opacity="{opacity}" transform="{tf}"/>')
                elif any(abs(x - fx) < 2 and abs(y - fy) < 2 for fx, fy in flip_v_at):
                    body.append(f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="{data_uri(node["img"])}" preserveAspectRatio="none" opacity="{opacity}" transform="translate(0 {2 * y + h:.1f}) scale(1 -1)"/>')
                else:
                    body.append(f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="{data_uri(node["img"])}" preserveAspectRatio="none" opacity="{opacity}"/>')
            if node['lines']:
                fs = px(cls, 'text') or inh.get('fs') or 14
                fam = re.search(r"font-\['[^:'\]]+:(\w+)'\]", cls); weight = WEIGHT.get(fam.group(1), 400) if fam else inh.get('weight', 400)
                col = color(cls, 'text') or inh.get('color') or '#212529'
                if node['grad'] and 'bg-clip-text' in cls: gi[0] += 1; col = grad(html.unescape(node['grad']), f'g{gi[0]}', defs) or col
                lh = px(cls, 'leading'); lh = lh if lh else round(fs * 1.2)
                center = 'text-center' in cls or (in_flex and 'items-center' in cls) or ('-translate-x-1/2' in cls)
                tx = x + w / 2 if center else x
                trk = px(cls, 'tracking'); ls = f' letter-spacing="{trk}"' if trk else ''
                n_l = len(node['lines']); total = lh * n_l
                top = y + (h - total) / 2 if h and h > total else y
                for i, line in enumerate(node['lines']):
                    lc = node['line_cls'][i] if i < len(node['line_cls']) else ''
                    lf = re.search(r"font-\['[^:'\]]+:(\w+)'\]", lc); lw = WEIGHT.get(lf.group(1), weight) if lf else weight
                    lcol = color(lc, 'text') or col; llh = px(lc, 'leading') or lh
                    by = top + llh * i + llh / 2 + fs * 0.35
                    body.append(f'<text x="{tx:.1f}" y="{by:.1f}" font-size="{fs:g}" font-weight="{lw}" fill="{lcol}" text-anchor="{"middle" if center else "start"}"{ls}>{html.escape(line)}</text>')
        flex = 'flex' in cls.split()
        if flex and node['kids']:
            col = 'flex-col' in cls
            g = px(cls, 'gap') or 0
            pad = lambda k: px(cls, k) or 0
            pt, pb, pl, pr = pad('pt') or pad('py') or pad('p'), pad('pb') or pad('py') or pad('p'), pad('pl') or pad('px') or pad('p'), pad('pr') or pad('px') or pad('p')
            def est(k):
                kc = k['cls']; kw = px(kc, 'w') or px(kc, 'size'); kh = px(kc, 'h') or px(kc, 'size')
                if k['nid'] in sizes: kw = kw or sizes[k['nid']][0]; kh = kh or sizes[k['nid']][1]
                if k['lines'] and (kw is None or kh is None):
                    fs_ = px(kc, 'text') or 14; lh_ = px(kc, 'leading') or round(fs_ * 1.2)
                    est_w = max(sum((1.0 if ord(ch) > 0x2E80 else 0.55) * fs_ for ch in ln) for ln in k['lines'])
                    kw = kw or est_w; kh = kh or lh_ * len(k['lines'])
                return kw or 0, kh or 0
            dims = [est(k) for k in node['kids']]
            inner_w = (w or 0) - pl - pr; inner_h = (h or 0) - pt - pb
            total = sum(d[1] if col else d[0] for d in dims) + g * (len(dims) - 1)
            start = (inner_h if col else inner_w) - total
            start = start / 2 if 'justify-center' in cls else (start if 'justify-end' in cls else 0)
            cur = start
            for k, (kw, kh) in zip(node['kids'], dims):
                if col:
                    kx = x + pl + ((inner_w - kw) / 2 if 'items-center' in cls else 0); ky = y + pt + cur; cur += kh + g
                else:
                    kx = x + pl + cur; ky = y + pt + ((inner_h - kh) / 2 if 'items-center' in cls else 0); cur += kw + g
                walk(k, kx, ky, kw, kh, True, box=(kx, ky, kw, kh), inh=inh)
        else:
            for k in node['kids']: walk(k, x, y, w, h, flex, inh=inh)
    walk(tree, 0, 0, *root_size, False)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{rx} {ry} {rw} {rh}" width="1200" height="{round(1200 * rh / rw)}" font-family="{FONT}" aria-hidden="true">\n'
           + (f'<defs>{"".join(defs)}</defs>\n' if defs else '') + '\n'.join(body) + '\n</svg>\n')
    (OUT / out_name).write_text(svg, encoding='utf-8'); print(out_name, len(body), '요소', (OUT / out_name).stat().st_size, 'bytes')

JOBS = [   # (노드, 영역 x y w h — 슬라이드 1920x1080 좌표, 파일, PNG 에셋 건너뛰기)
    ('1083:280499', (766, 186, 1154, 640), 'deck-04-screen.svg', False),       # 02 배경 — 법인카드 정산 화면 시안(표 + 팝업). 오른쪽은 슬라이드 끝에서 잘린다(사용자 OK)
    ('1083:280814', (40, 400, 1840, 590), 'deck-05-problem.svg', False, ('1083:280895',)),   # 💡 가설 정의 상자(Group 2258)는 글로 있으니 뺀다
    ('1083:280980', (0, 330, 1920, 420), 'deck-07-phases.svg', False),
    ('1083:281080', (40, 400, 1860, 590), 'deck-08-card-flow.svg', False, (), ((1532, 448),)),   # S자 선은 Figma 에서 세로로 뒤집힌 인스턴스
    ('1083:281052', (40, 410, 1860, 580), 'deck-10-hometax-flow.svg', False),
    ('1083:281117', (860, 180, 1040, 330), 'deck-12-results.svg', False),   # PNG(Rectangle 1861)는 5월 막대의 그라디언트 채움
    ('1083:281207', (40, 400, 1860, 360), 'deck-13-kpi.svg', False),
]
if __name__ == '__main__':
    only = sys.argv[1:]
    for job in JOBS:
        nid, region, name, skip_png = job[:4]; skip_ids = job[4] if len(job) > 4 else (); flip = job[5] if len(job) > 5 else ()
        if only and not any(o in name for o in only): continue
        render(nid, region, name, skip_png=skip_png, skip_ids=skip_ids, flip_v_at=flip)
