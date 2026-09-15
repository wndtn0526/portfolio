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
