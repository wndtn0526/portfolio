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

    {{-- 내비 — 레퍼런스 실측: fixed · 높이 73 · 흰색 60% + blur(20px) · 내려가면 숨는다.
         숨기는 동작은 resources/js/app.js 에 있다(개발·정적 양쪽에서 같이 돌게 하려고 Alpine 을 안 썼다). --}}
    <header data-nav
            class="fixed inset-x-0 top-0 z-50 h-[65px] bg-canvas/60 backdrop-blur-[20px] transition-transform duration-300 ease-out motion-reduce:transition-none lg:h-[73px]">
        <div class="flex h-full items-center justify-between px-6 lg:px-12">
            <a href="#top" class="text-sm font-bold tracking-[-0.02em] text-ink">신중수</a>
            <a href="mailto:wndtn0526@gmail.com"
               class="group inline-flex items-center gap-2 text-sm text-body transition-colors hover:text-ink">
                연락하기
                <span aria-hidden="true" class="transition-transform group-hover:translate-x-0.5">→</span>
            </a>
        </div>
    </header>

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
                <p class="max-w-statement text-[clamp(1.75rem,3.2vw,46.08px)] leading-[1.08] tracking-[-0.025em]">
                    {{-- ⚠️ 한 span 이 한 줄이어야 알파가 줄 단위로 찬다. 806px 안에서 안 접히게 짧게 끊었다.
                         46px 기준 한 줄에 한글 17자쯤 들어간다. 문구를 고칠 때 길이를 확인할 것. --}}
                    <span data-statement-line class="statement-line block font-bold">맡은 일의 본질적인 가치를</span>
                    <span data-statement-line class="statement-line block font-bold">발견하는 일을 합니다</span>
                    <span data-statement-line class="statement-line block"><span class="font-bold">/</span>그 가치가 사용자에게</span>
                    <span data-statement-line class="statement-line block">가장 매력적으로 닿도록</span>
                    <span data-statement-line class="statement-line block">경험을 설계합니다.</span>
                </p>
            </div>
        </section>
    </main>
</x-layouts.app>
