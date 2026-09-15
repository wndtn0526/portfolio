/*
 * 스무스 스크롤 — 레퍼런스(montone.studio)가 쓰는 Lenis 를 그대로 쓴다.
 * 실측(휠 100 한 번): 160px 이동 · 남은 거리가 매 프레임 일정 비율로 줄어드는 lerp 방식 ·
 * 90% 도달 481ms · 99% 도달 911ms → 60fps 기준 lerp ≈ 0.08. 값은 아래에서 맞춘다.
 * ⚠️ html 의 scroll-smooth 는 뺐다 — 둘이 겹치면 두 번 감속한다.
 * ⚠️ 움직임 줄이기(prefers-reduced-motion)면 켜지 않는다. 그때는 브라우저 기본 스크롤.
 */
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';

const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
// 대조 결과: 이 페이지에서 휠 100 은 배율 1 일 때 200px 이라 0.8 이 레퍼런스의 160px 이 된다. lerp 0.085 가 90%/99% 도달 시간을 맞춘다.
const lenis = reducedMotion ? null : new Lenis({ lerp: 0.085, wheelMultiplier: 0.8, smoothWheel: true });
if (lenis) {
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
}
window.__lenis = lenis;   // 진단용

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

    const MIN_DELTA = 2;     // 이보다 작은 움직임은 방향으로 치지 않는다
    const update = () => {
        const y = window.scrollY;
        const delta = y - last;
        /*
         * ⚠️ 움직임이 거의 없으면 상태를 그대로 둔다.
         *    Lenis 가 목표에 다가가며 멈출 때 정수 scrollY 가 한 프레임 같았다가 1px 움직이는데,
         *    «내려갔나» 만 보고 매 프레임 토글하면 그 순간 내비가 한 번 보였다 사라진다.
         *    내려가는 중에만 숨기고 올라오는 중에만 보이며, 멈춤은 무시한다.
         */
        if (Math.abs(delta) >= MIN_DELTA) {
            if (delta > 0 && y > HIDE_AFTER) nav.classList.add('-translate-y-full');
            else if (delta < 0) nav.classList.remove('-translate-y-full');
            last = y;
        }
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
    const aside = statement.querySelector('[data-statement-aside]');
    const DIM = 0.18;          // 아직 안 드러난 줄
    const STEP = 0.6875 / lines.length;   // 레퍼런스: 다섯 줄이 0.6875 에 다 찬다. 줄 수가 바뀌어도 같은 시간에 끝나게 나눈다
    const ASIDE_FROM = 0.60;   // 오른쪽 소개가 떠오르기 시작하는 진행도(마지막 줄이 차오르는 중)
    const ASIDE_TO = 0.80;     // 다 떠오르는 진행도 — 나머지는 유지 구간
    const pinnedLayout = matchMedia('(min-width: 80rem) and (min-height: 52rem)');   // app.css 의 pin: 과 같은 조건
    let ticking = false;

    const paint = () => {
        const rect = statement.getBoundingClientRect();
        const pinned = pinnedLayout.matches ? statement.offsetHeight - innerHeight : 0;
        // 섹션이 화면 위로 올라간 만큼이 진행도. 고정을 푼 폭에서는 전부 밝힌다.
        const p = pinned > 0 ? Math.min(1, Math.max(0, -rect.top / pinned)) : 1;

        lines.forEach((line, i) => {
            const t = Math.min(1, Math.max(0, (p - i * STEP) / STEP));
            const eased = 1 - (1 - t) * (1 - t);           // ease-out
            line.style.setProperty('--line-alpha', (DIM + (1 - DIM) * eased).toFixed(3));
        });
        if (aside) {
            const t = Math.min(1, Math.max(0, (p - ASIDE_FROM) / (ASIDE_TO - ASIDE_FROM)));
            aside.style.setProperty('--intro-alpha', (t * (2 - t)).toFixed(3));   // ease-out
        }
        ticking = false;
    };

    const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(paint);
    };

    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll, { passive: true });
    pinnedLayout.addEventListener('change', onScroll);
    paint();
}

/*
 * 메뉴 오버레이 — 더보기 버튼으로 열고 CLOSE·Esc 로 닫는다.
 *
 * 레퍼런스(montone.studio)와 같은 동작: 오버레이가 **더보기 버튼 자리에서** 자라나 화면을 채우고,
 * 닫을 때 그 자리로 되돌아간다. 열리면 본문 스크롤을 잠근다.
 *
 * ⚠️ 여닫는 움직임은 CSS transition 이 아니라 Web Animations 로 돌린다.
 *    파란 면(.menu-bg)은 scale(s), 안의 내용(.menu-inner)은 scale(1/s) 로 되감아야 하는데
 *    1/s 는 CSS 전환으로 표현할 수 없다. 그래서 같은 이징을 40칸으로 미리 계산해 두 요소에
 *    키프레임으로 넣는다. 둘 다 transform 이라 합성 스레드에서만 돈다.
 *    (전에 clip-path 로 했더니 4K 화면에서 접히다 말고 300ms 씩 멈췄다 — app.css 참고)
 * ⚠️ 오버레이는 닫혀 있어도 DOM 에 그대로 있다. inert 로 포커스·클릭에서 빼 준다.
 */
const menu = document.querySelector('[data-menu]');
const menuBg = document.querySelector('[data-menu-bg]');
const menuInner = document.querySelector('[data-menu-inner]');
const menuOpen = document.querySelector('[data-menu-open]');
const menuClose = document.querySelector('[data-menu-close]');

if (menu && menuBg && menuInner && menuOpen && menuClose) {
    const OPEN_MS = 634;    // 레퍼런스 실측(3회 평균)
    const CLOSE_MS = 806;
    const MIN_INNER = 0.1;  // s 가 이보다 작을 땐 되감기를 멈춘다 — 그 구간은 어차피 잘려서 안 보인다
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

    /*
     * 이징. 열기는 레퍼런스가 선언한 cubic-bezier(0.76, 0, 0.24, 1) 그대로다.
     * 닫기는 p1x 만 0.86 으로 올렸다 — 순수 베지어로 닫으면 중간(400ms)에 26% 만 남아 뚝 줄어드는 느낌인데,
     * 레퍼런스가 실제로 그려 내는 닫힘은 그 지점에 62% 가 남고(두 단계로 이어지는 구현 특성),
     * 전에 clip-path 로 만들어 «속도 괜찮다» 확인받은 판도 42% 였다. 0.86 이 그 42% 를 다시 만든다.
     */
    const bezier = (x, p1x = 0.76) => {
        const cx = 3 * p1x, bx = 3 * (0.24 - p1x) - cx, ax = 1 - cx - bx;
        const cy = 3 * 0, by = 3 * (1 - 0) - cy, ay = 1 - cy - by;
        let t = x;
        for (let i = 0; i < 8; i++) {                       // 뉴턴법으로 x(t)=x 인 t 를 찾는다
            const xt = ((ax * t + bx) * t + cx) * t - x;
            const dx = (3 * ax * t + 2 * bx) * t + cx;
            if (Math.abs(xt) < 1e-5 || dx === 0) break;
            t -= xt / dx;
        }
        return ((ay * t + by) * t + cy) * t;
    };

    /* 지금 파란 면이 어느 크기인지 — 도중에 다시 눌러도 그 자리에서 이어 가려고 읽는다. */
    const currentScale = () => {
        const m = getComputedStyle(menuBg).transform;
        const a = m.startsWith('matrix(') ? parseFloat(m.slice(7)) : (m === 'none' ? 1 : 0);
        return Number.isFinite(a) ? a : 0;
    };

    let running = [];
    const animateTo = (target, onDone) => {
        running.forEach((a) => a.cancel());
        const from = currentScale();
        const dist = Math.abs(target - from);
        if (dist < 0.001 || reduced) {
            menuBg.style.transform = `scale(${target})`;
            menuInner.style.transform = `scale(${1 / Math.max(target, MIN_INNER)})`;
            onDone?.();
            return;
        }
        const opening = target > from;
        const duration = (opening ? OPEN_MS : CLOSE_MS) * dist;   // 도중에 이어 갈 땐 남은 거리만큼만
        const p1x = opening ? 0.76 : 0.86;
        const bg = [], inner = [];
        for (let i = 0; i <= 40; i++) {
            const t = i / 40;
            const s = from + (target - from) * bezier(t, p1x);
            bg.push({ transform: `scale(${Math.max(s, 0.001)})`, offset: t });
            inner.push({ transform: `scale(${1 / Math.max(s, MIN_INNER)})`, offset: t });
        }
        const opts = { duration, easing: 'linear', fill: 'forwards' };
        // 움직이는 동안만 레이어를 잡아 둔다 — 늘 잡아 두면 4K 에서 전체화면 레이어 둘이 메모리를 먹는다
        menuBg.style.willChange = menuInner.style.willChange = 'transform';
        running = [menuBg.animate(bg, opts), menuInner.animate(inner, opts)];
        running[0].onfinish = () => {
            // 끝난 값을 스타일에 박고 애니메이션은 지운다 — fill:forwards 를 쌓아 두지 않는다
            menuBg.style.transform = `scale(${target})`;
            menuInner.style.transform = `scale(${1 / Math.max(target, MIN_INNER)})`;
            running.forEach((a) => a.cancel());
            running = [];
            menuBg.style.willChange = menuInner.style.willChange = '';
            onDone?.();
        };
    };

    /* 더보기 버튼의 한가운데를 오버레이가 자라나는 원점으로 넘긴다. */
    const setOrigin = () => {
        const r = menuOpen.getBoundingClientRect();
        menu.style.setProperty('--menu-cx', `${r.left + r.width / 2}px`);
        menu.style.setProperty('--menu-cy', `${r.top + r.height / 2}px`);
    };

    const setOpen = (open) => {
        menuOpen.setAttribute('aria-expanded', String(open));

        if (open) {
            // ⚠️ 내비가 스크롤로 숨어 있으면 버튼이 화면 밖이라 엉뚱한 자리에서 자라난다.
            nav?.classList.remove('-translate-y-full');
            setOrigin();
            document.body.style.overflow = 'hidden';   // scrollbar-gutter:stable 이라 본문이 밀리지 않는다
            lenis?.stop();                              // 휠이 뒤 페이지를 움직이지 않게
            menu.inert = false;
            menu.classList.add('is-open');
            animateTo(1);
            menuClose.focus({ preventScroll: true });
        } else {
            setOrigin();
            menu.classList.remove('is-open');
            menuOpen.focus({ preventScroll: true });
            animateTo(0, () => {
                // 무거운 일(스크롤 복구·inert)은 다 접힌 뒤에 한다 — 움직이는 동안 리레이아웃을 일으키지 않는다
                if (menu.classList.contains('is-open')) return;   // 그 사이 다시 열렸으면 두지 않는다
                document.body.style.overflow = '';
                lenis?.start();
                menu.inert = true;
                goPending();                                        // 메뉴에서 고른 곳으로
            });
        }
    };

    menuOpen.addEventListener('click', () => setOpen(true));
    menuClose.addEventListener('click', () => setOpen(false));

    /* 메뉴 안의 앵커 — 열린 채로 뒤에서 스크롤되면 오버레이만 보인다. 먼저 닫고, 다 닫힌 뒤에 내려간다. */
    let pendingTarget = null;
    menu.querySelectorAll('a[href^="#"]').forEach((a) => {
        a.addEventListener('click', (e) => {
            e.preventDefault();
            pendingTarget = a.getAttribute('href');
            setOpen(false);
        });
    });
    const goPending = () => {
        if (!pendingTarget) return;
        const target = pendingTarget === '#top' ? 0 : document.querySelector(pendingTarget);
        pendingTarget = null;
        if (target === null) return;
        if (lenis) lenis.scrollTo(target, { offset: 0 });
        else (target === 0 ? window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }) : target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' }));
    };
    addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu.classList.contains('is-open')) setOpen(false);
    });
    addEventListener('resize', () => { if (!menu.classList.contains('is-open')) setOrigin(); }, { passive: true });

    menu.inert = true;   // 첫 상태
    setOrigin();
    menuInner.style.transform = `scale(${1 / MIN_INNER})`;
}
