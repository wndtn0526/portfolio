/*
 * 상단 내비 — 아래로 스크롤하면 숨고, 위로 올리면 다시 나온다.
 * 레퍼런스(montone.studio)가 그렇게 동작한다: fixed · 높이 73 · 흰색 60% + blur(20px) ·
 * 내려갈 때 translateY(-80px).
 *
 * ⚠️ Alpine 이 아니라 여기(app.js)에 둔다. Alpine 은 정적 export 에서만 CDN 으로 주입돼
 *    개발 서버에서는 없다 — 두 환경에서 다르게 도는 코드를 만들지 않으려는 것이다.
 */
const nav = document.querySelector('[data-nav]');

if (nav) {
    const HIDE_AFTER = 80;   // 이만큼 내려가기 전에는 숨기지 않는다
    let last = window.scrollY;
    let ticking = false;

    const update = () => {
        const y = window.scrollY;
        const down = y > last && y > HIDE_AFTER;
        nav.classList.toggle('-translate-y-full', down);
        last = y;
        ticking = false;
    };

    addEventListener('scroll', () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(update);
    }, { passive: true });
}

/*
 * 선언 섹션 — 스크롤에 따라 줄이 하나씩 밝아진다.
 *
 * 레퍼런스(montone.studio) 실측: 섹션 높이 3600 = 뷰포트(900) 4배, 안쪽은 sticky.
 * 핀 구간(3600-900=2700)을 진행도 0~1 로 보고, 각 줄의 **글자색 알파**가 0.18 → 1 로 찬다.
 * 실측 곡선: 줄마다 0.1375 씩 밀려 순차로 차고, 0.6875 에서 전부 완료된다(뒤 0.31 은 유지 구간).
 *
 * ⚠️ 투명도(opacity)가 아니라 color 의 알파다. opacity 를 쓰면 줄 전체가 흐려져 결이 다르다.
 */
const statement = document.querySelector('[data-statement]');

if (statement) {
    const lines = [...statement.querySelectorAll('[data-statement-line]')];
    const DIM = 0.18;          // 아직 안 드러난 줄
    const STEP = 0.1375;       // 줄 사이 간격 = 각 줄이 차는 데 걸리는 진행도
    let ticking = false;

    const paint = () => {
        const rect = statement.getBoundingClientRect();
        const pinned = statement.offsetHeight - innerHeight;
        // 섹션이 화면 위로 올라간 만큼이 진행도
        const p = pinned > 0 ? Math.min(1, Math.max(0, -rect.top / pinned)) : 1;

        lines.forEach((line, i) => {
            const t = Math.min(1, Math.max(0, (p - i * STEP) / STEP));
            const eased = 1 - (1 - t) * (1 - t);           // ease-out
            line.style.setProperty('--line-alpha', (DIM + (1 - DIM) * eased).toFixed(3));
        });
        ticking = false;
    };

    const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(paint);
    };

    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll, { passive: true });
    paint();
}

/*
 * 메뉴 오버레이 — 더보기 버튼으로 열고 CLOSE·Esc 로 닫는다.
 * 레퍼런스(montone.studio)와 같은 동작: 열리면 본문 스크롤을 잠그고, 닫는 버튼은 오버레이 안에 있다.
 *
 * ⚠️ 오버레이는 clip-path 로만 여닫으므로 닫혀 있어도 DOM 에 그대로 있다.
 *    그래서 inert 로 포커스·클릭에서 빼 준다 — 안 하면 Tab 으로 안 보이는 링크에 들어간다.
 */
const menu = document.querySelector('[data-menu]');
const menuOpen = document.querySelector('[data-menu-open]');
const menuClose = document.querySelector('[data-menu-close]');

if (menu && menuOpen && menuClose) {
    const setOpen = (open) => {
        menu.classList.toggle('is-open', open);
        menu.inert = !open;
        menuOpen.setAttribute('aria-expanded', String(open));
        document.body.style.overflow = open ? 'hidden' : '';
        (open ? menuClose : menuOpen).focus();
    };

    menuOpen.addEventListener('click', () => setOpen(true));
    menuClose.addEventListener('click', () => setOpen(false));
    addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu.classList.contains('is-open')) setOpen(false);
    });

    menu.inert = true;   // 첫 상태
}
