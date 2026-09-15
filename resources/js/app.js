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
 *
 * 레퍼런스(montone.studio)와 같은 동작:
 *  · 오버레이가 **더보기 버튼 자리에서** 자라나 화면을 채우고, 닫을 때 그 자리로 되돌아간다.
 *    버튼의 화면 좌표를 --menu-* 로 넣어 주면 CSS 의 clip-path 가 거기서 출발한다.
 *  · 열리면 본문 스크롤을 잠근다.
 *
 * ⚠️ 스크롤을 잠글 때 스크롤바가 사라지면서 본문이 그 폭만큼 옆으로 밀린다(= 딱 끊기는 느낌).
 *    사라지는 스크롤바 폭만큼 padding-right 로 메워 밀림을 없앤다.
 * ⚠️ 오버레이는 clip-path 로만 여닫으므로 닫혀 있어도 DOM 에 그대로 있다.
 *    그래서 inert 로 포커스·클릭에서 빼 준다 — 안 하면 Tab 으로 안 보이는 링크에 들어간다.
 */
const menu = document.querySelector('[data-menu]');
const menuOpen = document.querySelector('[data-menu-open]');
const menuClose = document.querySelector('[data-menu-close]');

if (menu && menuOpen && menuClose) {
    /* 더보기 버튼의 한가운데를 오버레이가 자라나는 출발점으로 넘긴다. */
    const setOrigin = () => {
        const r = menuOpen.getBoundingClientRect();
        menu.style.setProperty('--menu-cx', `${r.left + r.width / 2}px`);
        menu.style.setProperty('--menu-cy', `${r.top + r.height / 2}px`);
    };

    const setOpen = (open) => {
        if (open) {
            // ⚠️ 내비가 스크롤로 숨어 있으면 버튼이 화면 밖이라 엉뚱한 자리에서 자라난다.
            //    먼저 내비를 되돌려 놓고 좌표를 잰다.
            nav?.classList.remove('-translate-y-full');
            // 잠그기 전에 스크롤바 폭을 재서 메운다 — 안 하면 본문이 옆으로 튄다.
            const gap = innerWidth - document.documentElement.clientWidth;
            document.body.style.paddingRight = gap > 0 ? `${gap}px` : '';
            document.body.style.overflow = 'hidden';
            setOrigin();
            // 출발 좌표가 반영된 뒤에 펼쳐야 한다. 같은 프레임에 바꾸면 전환이 생략된다.
            requestAnimationFrame(() => menu.classList.add('is-open'));
        } else {
            setOrigin();                       // 그 사이 창 크기가 바뀌었을 수 있다
            menu.classList.remove('is-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
        }

        menu.inert = !open;
        menuOpen.setAttribute('aria-expanded', String(open));
        // preventScroll — 포커스를 옮기다 화면이 튀는 것을 막는다
        (open ? menuClose : menuOpen).focus({ preventScroll: true });
    };

    menuOpen.addEventListener('click', () => setOpen(true));
    menuClose.addEventListener('click', () => setOpen(false));
    addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu.classList.contains('is-open')) setOpen(false);
    });
    addEventListener('resize', () => { if (!menu.classList.contains('is-open')) setOrigin(); }, { passive: true });

    menu.inert = true;   // 첫 상태
    setOrigin();
}
