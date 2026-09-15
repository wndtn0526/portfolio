{{--
    인트로 — Figma  PORTFOLIO 슬라이드 02 (node 1083:280397) 를 웹으로 옮긴 히어로 +
    레퍼런스(montone.studio)의 선언 섹션.

    좌우 여백은 레퍼런스 실측을 따른다. clamp 가 아니라 **1024px 에서 한 번 꺾이는 단계식**이다:

        폭 ≤768   여백 24 · 내비 높이 65 · 선언 글 72 (=24+48)
        폭 ≥1024  여백 48 · 내비 높이 73 · 선언 글 96 (=48+48)

    로고와 히어로 제목이 같은 세로선(여백)에 서고, 선언 섹션 글만 안쪽으로 48 더 들어간다.

    ⚠️ 시안 원문의 오탈자 두 곳을 고쳐서 옮겼다 — `Brand Experrience` → Experience,
       `브래느 스토리텔링` → 브랜드. Figma 원본도 같이 고쳐야 갈라지지 않는다.
--}}
<x-layouts.app title="신중수 · Product Manager / Product Designer">

    {{-- 내비 — 레퍼런스 실측: fixed · 높이 65/73 · 흰색 60% + blur(20px) · 내려가면 숨는다.
         ⚠️ [transform:translateZ(0)] 는 장식이 아니다. backdrop-blur 가 걸린 요소라
            합성 레이어가 붙었다 떨어졌다 하면 블러를 매번 다시 래스터화해서, 메뉴를 여닫을 때마다
            끊기는 느낌이 난다. 항등 변환으로 레이어를 고정해 둔다(레퍼런스도 같은 처리를 한다 —
            그쪽 nav 의 computed transform 이 matrix(1,0,0,1,0,0) 이다).
            ⚠️ Tailwind 4 의 -translate-y-full 은 transform 이 아니라 translate 속성을 쓰므로
               이 항등 변환과 부딪히지 않는다.
         좌측은 2줄 로고타입(레퍼런스의 `montone/ studio` 자리), 우측은 더보기 버튼이다.
         숨기는 동작은 resources/js/app.js 에 있다(개발·정적 양쪽에서 같이 돌게 하려고 Alpine 을 안 썼다). --}}
    <header data-nav
            class="fixed inset-x-0 top-0 z-50 h-[65px] [transform:translateZ(0)] bg-canvas/60 backdrop-blur-[20px] transition-transform duration-300 ease-out motion-reduce:transition-none lg:h-[73px]">
        <div class="flex h-full items-center justify-between px-6 lg:px-12">
            {{-- 로고타입 — 레퍼런스 로고는 24px 높이의 2줄 SVG 마크다. 글자로 같은 덩어리를 만든다. --}}
            <a href="#top" class="block text-[13px] leading-[13px] tracking-[-0.02em]">
                <span class="block font-bold text-ink">신중수</span>
                <span class="block text-muted">Product Designer</span>
            </a>

            {{-- 더보기 — 레퍼런스 실측: 박스 32x24, 선 24x2 가 위에서 4·11·18 위치. --}}
            <button type="button" data-menu-open aria-expanded="false" aria-controls="site-menu"
                    class="relative h-6 w-8 cursor-pointer outline-offset-4 focus-visible:outline-2 focus-visible:outline-ink" aria-label="메뉴 열기">
                <span aria-hidden="true" class="absolute left-1 top-1 h-0.5 w-6 bg-ink"></span>
                <span aria-hidden="true" class="absolute left-1 top-[11px] h-0.5 w-6 bg-ink"></span>
                <span aria-hidden="true" class="absolute left-1 top-[18px] h-0.5 w-6 bg-ink"></span>
            </button>
        </div>
    </header>

    {{-- 메뉴 오버레이 — 레퍼런스 실측: 배경 #504fed · z 1100 · 더보기 버튼 자리에서 펼쳐진다.
         항목 96px/300/자간 -0.03em · 행 간격 108 · 좌측 여백은 내비와 같은 24/48.
         ⚠️ 레퍼런스는 clip-path 로 여닫지만 우리는 transform(scale) 로 한다. 4K 화면에서 clip-path 는
            매 프레임 메인 스레드가 전체를 다시 칠해야 해서 접히다 말고 300ms 씩 멈췄다(화면 녹화로 확인).
            scale 은 합성 스레드에서만 돌아 멈추지 않고, 원점을 버튼에 두면 나오는 사각형은 수학적으로 같다.
         ⚠️ 항목의 목적지는 아직 정해지지 않았다. 기획을 다시 하는 중이라 자리만 잡아 둔 것이다. --}}
    <div data-menu id="site-menu" class="menu-overlay fixed inset-0 z-[1100]">
        {{-- 파란 면. 더보기 버튼을 원점으로 scale(0)→scale(1). transform 이라 합성 스레드에서만 돈다. --}}
        <div data-menu-bg class="menu-bg absolute inset-0 overflow-hidden bg-statement">
            {{-- 내용. 부모의 scale 을 1/s 로 되감아 원래 크기로 보이게 한다. 부모의 overflow:hidden 이 잘라 준다. --}}
            <div data-menu-inner class="menu-inner absolute inset-0">
                <button type="button" data-menu-close
                        class="absolute end-6 top-7 inline-flex cursor-pointer items-center gap-3 text-[13px] font-medium tracking-[0.1em] text-white uppercase lg:end-12">
                    <svg aria-hidden="true" viewBox="0 0 20 20" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.6">
                        <path d="M4 4l12 12M16 4L4 16" stroke-linecap="round" />
                    </svg>
                    Close
                </button>

                {{-- 목록은 레퍼런스 실측 위치(뷰포트 위에서 24%, 900 기준 219px)에 고정한다.
                     가운데 정렬로 두면 아래 요소가 빠지고 들어올 때마다 목록이 위아래로 흔들린다. --}}
                <div class="h-full px-6 pt-[24vh] lg:px-12">
                    <ul class="text-[clamp(3rem,6.67vw,96px)] leading-[1.13] font-light tracking-[-0.03em] text-white">
                        <li data-menu-item><a href="#top" class="inline-block transition-opacity hover:opacity-70">/소개</a></li>
                        <li data-menu-item><a href="#top" class="inline-block transition-opacity hover:opacity-70">/프로젝트</a></li>
                        <li data-menu-item><a href="#top" class="inline-block transition-opacity hover:opacity-70">/이력</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <main id="top">

        {{-- ── 히어로 ── 배경 메시는 시안의 freeform 2 를 color-burn 25% 로 미리 구워 넣은 것이다.
             구울 때 배경 #f9f9f9 를 깔았으므로 canvas 위에서만 이음매가 안 보인다. --}}
        <section class="relative flex min-h-dvh flex-col justify-center overflow-hidden">
            <img src="{{ asset('images/intro-mesh.webp') }}"
                 srcset="{{ asset('images/intro-mesh-1280.webp') }} 1280w, {{ asset('images/intro-mesh.webp') }} 1920w"
                 sizes="100vw" alt="" aria-hidden="true" fetchpriority="high" width="1920" height="1084"
                 class="pointer-events-none absolute inset-0 -z-10 h-full w-full object-cover object-top">

            <div class="px-6 lg:px-12">
                <h1 class="font-bold tracking-[-0.02em] text-ink text-[clamp(2.5rem,7.6vw,98px)] leading-[1.04]">
                    Beauty is in the<br>eye of the beholder.
                </h1>

                <p class="mt-[clamp(1.5rem,3vw,2.75rem)] text-ink text-[clamp(1.125rem,2.6vw,48px)] leading-[1.32]">
                    사랑하는 사람은 뭐든지 다 예뻐보인다는 말인데,<br>
                    <strong class="font-bold">저는 이 말이 좋습니다.</strong>
                </p>
            </div>

            {{-- 스크롤 안내 — 레퍼런스의 'Scroll' 자리 --}}
            <div class="absolute inset-x-0 bottom-10 px-6 lg:px-12">
                <span class="inline-flex items-center gap-3 text-xs tracking-[0.18em] text-muted uppercase">
                    Scroll
                    <span aria-hidden="true" class="h-px w-10 origin-left animate-scroll-cue bg-muted"></span>
                </span>
            </div>
        </section>

        {{-- ── 선언 ── montone.studio 의 선언 섹션을 그대로 옮겼다.
             실측(1440): 배경 #504fed · 섹션 높이 뷰포트 4배 · 안쪽 sticky · 패딩 120/48 ·
             글 x=96 폭 806 · 글자 46.08px 행간 1.08 자간 -0.025em ·
             앞 두 줄 700 / 뒤 세 줄 400 · 색 알파가 0.18 → 1 로 순차 상승.
             차오르는 동작은 resources/js/app.js 에 있다.

             ⚠️ 문구는 레퍼런스 원문이 아니라 Figma 슬라이드 02 의 우리 글을 다섯 줄로 나눈 것이다.
                레퍼런스 카피를 그대로 쓰면 남의 브랜드 문장을 베끼는 것이 된다. --}}
        <section data-statement class="relative h-[400vh] bg-statement">
            <div class="sticky top-0 flex h-dvh items-center px-6 py-[clamp(3rem,8vw,120px)] ps-[calc(1.5rem+3rem)] lg:px-12 lg:ps-24">
                {{-- ⚠️ 한 span 이 한 줄이어야 알파가 줄 단위로 찬다. 806px 안에서 안 접히게 짧게 끊었다.
                     46px 기준 한 줄에 한글 17자쯤 들어간다. 문구를 고칠 때 길이를 확인할 것. --}}
                <p class="max-w-statement text-[clamp(1.75rem,3.2vw,46.08px)] leading-[1.08] tracking-[-0.025em]">
                    <span data-statement-line class="statement-line block font-bold">맡은 일의 본질적인 가치를</span>
                    <span data-statement-line class="statement-line block font-bold">발견하는 일을 합니다.</span>
                    <span data-statement-line class="statement-line block"><span class="font-bold">/</span>그 가치가 사용자에게</span>
                    <span data-statement-line class="statement-line block">가장 매력적으로 닿도록</span>
                    <span data-statement-line class="statement-line block">경험을 설계합니다.</span>
                </p>
            </div>
        </section>
    </main>
</x-layouts.app>
