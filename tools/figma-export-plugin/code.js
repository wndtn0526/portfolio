// 포트폴리오 · 원본 2배 내보내기
// GPRO_PORTFOLIO 를 열어 둔 상태에서 실행한다. JOBS 의 노드를 PNG(2x) 로 내보내 로컬 서버(127.0.0.1:8899)로 보낸다.
// 서버: scratchpad/hires_server.py — 받은 파일을 hires/<name>.png 로 저장한다.
// Dev Mode MCP get_screenshot 이 긴 변 1024px 로 막혀 있어서 만든 우회로다.
const SERVER = 'http://localhost:8899';
const JOBS = [
  ['1958:5268', 'card-flowchart-08b'],
];
async function main() {
  const fails = []; let ok = 0;
  for (const [id, name] of JOBS) {
    try {
      const node = await figma.getNodeByIdAsync(id);
      if (!node) { fails.push(name + ' 없음'); continue; }
      const bytes = await node.exportAsync({ format: 'PNG', constraint: { type: 'SCALE', value: 2 } });
      const r = await fetch(SERVER + '/save?name=' + encodeURIComponent(name), { method: 'POST', body: bytes });
      if (r.status !== 200) fails.push(name + ' http ' + r.status); else ok++;
    } catch (e) { fails.push(name + ' ' + (e && e.message ? e.message : e)); }
  }
  figma.notify(ok + '장 내보냄' + (fails.length ? ' · 실패: ' + fails.join(', ') : ''), { timeout: 8000 });
  figma.closePlugin();
}
main();
