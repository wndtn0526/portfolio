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

    {{-- 내비 — 레퍼런스 실측: fixed · 높이 65/73 · 흰색 60% + blur(20px) · 아래 보더 1px rgba(0,0,0,.06) · 내려가면 숨는다.
         ⚠️ [transform:translateZ(0)] 는 장식이 아니다. backdrop-blur 가 걸린 요소라
            합성 레이어가 붙었다 떨어졌다 하면 블러를 매번 다시 래스터화해서, 메뉴를 여닫을 때마다
            끊기는 느낌이 난다. 항등 변환으로 레이어를 고정해 둔다(레퍼런스도 같은 처리를 한다 —
            그쪽 nav 의 computed transform 이 matrix(1,0,0,1,0,0) 이다).
            ⚠️ Tailwind 4 의 -translate-y-full 은 transform 이 아니라 translate 속성을 쓰므로
               이 항등 변환과 부딪히지 않는다.
         좌측은 2줄 로고타입(레퍼런스의 `montone/ studio` 자리), 우측은 더보기 버튼이다.
         숨기는 동작은 resources/js/app.js 에 있다(개발·정적 양쪽에서 같이 돌게 하려고 Alpine 을 안 썼다). --}}
    <header data-nav
            class="fixed inset-x-0 top-0 z-50 h-[65px] border-b border-black/6 [transform:translateZ(0)] bg-canvas/60 backdrop-blur-[20px] transition-transform duration-300 ease-out motion-reduce:transition-none lg:h-[73px]">
        <div class="flex h-full items-center justify-between px-6 lg:px-12">
            {{-- 로고타입 — 한 줄 대문자 「PORTFOLIO」. 레퍼런스 로고 마크(24px 높이)와 같은 덩어리가 되도록
                 404 스케일 title-3(24px) ExtraBold(800) 에 행간 1.0 — 블록 높이가 딱 24px. 두 줄이던 것을 한 줄로 줄이며 키웠다. --}}
            <a href="#top" class="block text-title-3 font-extrabold leading-none text-ink">PORTFOLIO</a>

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
                        <li data-menu-item><a href="#intro" class="inline-block transition-opacity hover:opacity-70">/소개</a></li>
                        <li data-menu-item><a href="#top" class="inline-block transition-opacity hover:opacity-70">/프로젝트</a></li>
                        <li data-menu-item><a href="#career" class="inline-block transition-opacity hover:opacity-70">/이력</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <main id="top">

        {{-- ── 히어로 ── 배경 메시는 시안의 freeform 2(1083:280398) 를 color-burn 50% 로 미리 구워 넣은 것이다(처음엔 25% 였다).
             구울 때 배경 #f9f9f9 를 깔았으므로 canvas 위에서만 이음매가 안 보인다. --}}
        {{-- 글은 레퍼런스처럼 아래쪽에 — 실측: 글 바닥이 뷰포트 바닥에서 81px, SCROLL 은 글 아래 20px(바닥에서 48px). --}}
        <section class="relative flex min-h-dvh flex-col justify-end overflow-hidden pb-12">
            <img src="{{ asset('images/intro-mesh.webp') }}"
                 srcset="{{ asset('images/intro-mesh-1280.webp') }} 1280w, {{ asset('images/intro-mesh.webp') }} 1920w"
                 sizes="100vw" alt="" aria-hidden="true" fetchpriority="high" width="1920" height="1084"
                 class="pointer-events-none absolute inset-0 -z-10 h-full w-full object-cover object-top">

            <div class="px-6 lg:px-12">
                {{-- Figma 슬라이드 02 실측: Pretendard Black(900) · 98px · 행간 98(=1.0) · 자간 없음.
                     한때 레퍼런스(montone h1 700)에 맞춰 700/−0.02em 으로 뒀는데, 볼드감은 Figma 대로 가기로 했다. --}}
                <h1 class="font-black tracking-normal text-ink text-[clamp(2.5rem,7.6vw,98px)] leading-none">
                    Beauty is in the<br>eye of the beholder.
                </h1>

                {{-- 48px · 행간 62(=1.292) · 1줄 Regular, 2줄 Bold --}}
                <p class="mt-[clamp(1.5rem,3vw,2.75rem)] text-ink text-[clamp(1.125rem,2.6vw,48px)] leading-[1.292]">
                    사랑하는 사람은 뭐든지 다 예뻐보인다는 말인데,<br>
                    <strong class="font-bold">저는 이 말이 좋습니다.</strong>
                </p>
            </div>

            {{-- 스크롤 안내 — 레퍼런스의 'Scroll' 자리. 글 아래 20px. --}}
            {{-- 감싸는 div 를 flex 로 — 블록이면 인라인 span 아래에 줄 상자 여백이 5px 생겨 바닥 48 이 53 이 된다. --}}
            <div class="mt-5 flex px-6 lg:px-12">
                {{-- 레퍼런스 실측: 11px · 자간 1.54px(0.14em) · 높이 13 --}}
                <span class="inline-flex h-[13px] items-center gap-3 text-[11px] leading-none tracking-[0.14em] text-muted uppercase">
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
        <section data-statement id="intro" class="relative bg-statement pin:h-[400vh]">
            {{-- pin:(폭 1280·높이 832 이상) — 뷰포트 4배 높이에 안쪽을 sticky 로 붙여 스크롤로 줄이 차오르고
                 오른쪽 소개가 뒤이어 떠오른다. 그 아래 폭·높이 — 고정을 풀고 선언 아래에 소개가 이어진다
                 (app.js 도 같은 조건에서 전부 밝힌다). 조건은 app.css 의 @custom-variant pin 참고. --}}
            <div class="px-6 py-[clamp(3rem,6vh,120px)] ps-[calc(1.5rem+3rem)] lg:px-12 lg:ps-24 pin:sticky pin:top-0 pin:flex pin:h-dvh pin:items-center pin:pe-24">
                {{-- Figma(포트폴리오_MCP · 1:24, 2056 기준) 실측: 좌우 여백 96, 두 단이 정확히 반반(932 | 932),
                     오른쪽 단은 화면 정중앙에서 시작한다. 세로는 둘 다 가운데.
                     왼쪽 칸은 minmax(max-content, 1fr) — 화면이 좁아 반이 선언의 가장 긴 줄보다 작아지면
                     그 줄 폭만큼은 지킨다(한 줄이 두 줄로 접히면 줄 단위 밝아짐이 깨진다). 나머지가 오른쪽 단. --}}
                <div class="flex flex-col gap-14 pin:grid pin:w-full pin:grid-cols-[minmax(max-content,1fr)_minmax(0,1fr)] pin:items-center pin:gap-0">
                    {{-- ⚠️ 한 span 이 한 줄이어야 알파가 줄 단위로 찬다. 줄 나눔은 Figma(1:24)대로 넉 줄.
                         가장 긴 줄(넷째, 46px 에서 662px)이 접히지 않게 왼쪽 칸이 max-content 를 보장한다. --}}
                    <p class="max-w-statement shrink-0 text-[clamp(1.75rem,3.2vw,46.08px)] leading-[1.08] tracking-[-0.025em]">
                        <span data-statement-line class="statement-line block font-bold">맡은 일의 본질적인 가치를</span>
                        <span data-statement-line class="statement-line block font-bold">발견하는 일을 합니다.</span>
                        <span data-statement-line class="statement-line block"><span class="font-bold">/</span>그 가치가 사용자에게 가장</span>
                        <span data-statement-line class="statement-line block">매력적으로 닿도록 경험을 설계합니다.</span>
                    </p>

                    {{-- 오른쪽 소개 — 선언 다섯 줄이 다 밝아진 뒤 떠오른다(app.js 가 --intro-alpha 를 넣는다).
                         글은 Figma 슬라이드 02 의 자기소개. 타이포는 404 스케일(자간 포함).
                         ⚠️ 원문 오탈자 `브래느` → `브랜드` 로 고쳐 옮겼다. --}}
                    {{-- 오른쪽 소개 — 선언 줄이 다 밝아진 뒤 떠오른다(app.js 가 --intro-alpha 를 넣는다).
                         글자 크기는 Figma(2056 기준) 값이 2056 에서 그대로 나오고 1440 에서는 한 단 아래로 흐른다:
                           인사 32←22(Bold, 한 줄) · 요지 24←16(SemiBold, 흰색 100%) · 소제목 24←20 · 본문 20←16(85%).
                         행간·자간(%)은 Figma 그대로. 맺음은 전부 85%, 마지막 인사말(멋진 관계를…)은 Figma 에서 뺐다.
                         2056 값을 1440 에 그대로 쓰면 단이 뷰포트를 넘친다(실측 ~880px). 영문 라벨은 Figma 에서 뺐다.
                         ⚠️ 원문 오탈자 `브래느` → `브랜드` 로 고쳐 옮겼다. --}}
                    <aside data-statement-aside class="statement-aside w-full min-w-0 text-white">
                        <p class="text-[clamp(22px,1.556vw,32px)] leading-[1.318] font-bold tracking-[-0.0455em] break-keep">안녕하세요. 서비스기획자 신중수 입니다.</p>
                        <p class="mt-3 text-[clamp(16px,1.167vw,24px)] leading-[1.625] font-semibold tracking-[-0.0375em] break-keep">
                            저의 가장 큰 무기이자 차별점은 서로 다른 두 영역에서의 깊은 통찰을 결합했다는 점입니다.
                        </p>

                        <h3 class="mt-8 text-[clamp(20px,1.167vw,24px)] leading-[1.5] font-bold tracking-[-0.05em] break-keep">구조와 논리의 깊이</h3>
                        <p class="mt-2 text-[clamp(16px,0.973vw,20px)] leading-[1.625] tracking-[-0.0375em] text-white/85">
                            그룹웨어 시장에서의 깊은 도메인 경험을 통해 어떤 기술도 도메인보다 앞설 수 없다는 신념을 가지고,
                            실제 현업의 복잡한 업무 흐름 (HR/재무) 을 깊이 이해하고 구조화할 수 있게 성장했습니다.
                            명확한 목표와 올바른 방향 설정이 정답에 가까운 결과를 만든다는 믿음으로,
                            엔터프라이즈의 비효율을 해소하는 논리적인 UX 설계에 집중합니다.
                        </p>

                        <h3 class="mt-8 text-[clamp(20px,1.167vw,24px)] leading-[1.5] font-bold tracking-[-0.05em] break-keep">브랜드와 소통의 폭</h3>
                        <p class="mt-2 text-[clamp(16px,0.973vw,20px)] leading-[1.625] tracking-[-0.0375em] text-white/85">
                            이전 광고대행사 경험에서 얻은 브랜드 스토리텔링 및 비주얼 커뮤니케이션 능력은
                            제품의 매력도를 극대화하는 중요한 도구입니다. 딱딱하게 느껴지기 쉬운 B2B 솔루션에
                            사용자에게 공감을 주는 UX Writing 과 일관된 브랜드 경험을 입혀,
                            사용자가 사랑하고 습관적으로 이용하는 제품으로 전환시킵니다.
                        </p>

                        <p class="mt-8 text-[clamp(16px,0.973vw,20px)] leading-[1.625] tracking-[-0.0375em] text-white/85">
                            이러한 사고와 통찰은 단순히 일을 하는 사람이 아니라, 사용자 효율성과 브랜드 매력을 동시에 높여
                            제품의 가치를 확장시키는 사람으로 성장하게 하는 원동력입니다.
                            저는 주어진 일의 가치를 넘어서는 새로운 가치를 만들어내는 엑스트라 마일을 실현하며,
                            함께 일하며 더 높은 곳을 바라보는 좋은 동료, 신뢰받는 협업자가 되고 싶습니다.
                        </p>
                    </aside>
                </div>
            </div>
        </section>


        {{-- ── 이력 ── Figma 포트폴리오_MCP 3:131 「03 이력 — 2056 (풀 화면)」 을 웹으로 옮긴 것(사용자가 2056 기준으로 조절).
             Figma(2056) 값: 사진 260x325 모서리 28 그림자 · 제목 40('/' Bold) · 이름/직함 24 SemiBold+Regular · 소개 20/1.533 #495057
                            섹션 라벨·행 라벨 24 SemiBold #868e96 -2% · 라벨 칸 240 · 행 제목 24 Medium · 부제 20 · 불릿 16 · 기간 20 #868e96
                            행 py14 · 위 보더 1px 검정 8%(마지막 아래도) · 블록 간격 80/64/64 · 기술 막대는 Figma 에서 뺐다.
             웹은 폭 따라 흐르고 2056 에서 그 값이 된다 — clamp(최소, vw, Figma 값). vw = 값/2056. 1440 에서는 대략 한 단계 작다.
             ⚠️ 라벨 24 는 1440 에서 16.8 로 흐른다. 라벨 칸 240 도 같이 흘러(11.67vw) 1440 에서 168 이다.
             개인정보는 시안 그대로 싣기로 한 결정(notes/content-plan.md)을 따른다. --}}
        @php
            $label = 'text-[clamp(14px,1.167vw,24px)] leading-[1.545] font-semibold tracking-[-0.02em] text-muted';
            $row = 'grid grid-cols-[clamp(92px,11.67vw,240px)_1fr] items-baseline gap-x-4 border-t border-black/8 py-3.5 md:grid-cols-[clamp(92px,11.67vw,240px)_1fr_auto]';
            $title = 'text-[clamp(19px,1.167vw,24px)] leading-[1.526] font-medium tracking-[-0.0316em] break-keep text-ink';
            $sub = 'mt-1 text-[clamp(15px,0.973vw,20px)] leading-[1.571] tracking-[-0.0143em] break-keep text-body';
            $bullets = 'mt-1 space-y-1 ps-4 text-[clamp(14px,0.778vw,16px)] leading-[1.571] tracking-[-0.0143em] break-keep text-body';
            $right = 'col-start-2 text-[clamp(14px,0.973vw,20px)] leading-[1.429] tracking-[-0.0143em] text-muted md:col-start-3 md:text-end';
        @endphp
        <section id="career" class="px-6 py-[clamp(4rem,10vh,120px)] lg:px-12">
            {{-- 사진 + 소개 --}}
            <div class="grid gap-10 md:grid-cols-[260px_1fr] md:gap-14">
                <img src="{{ asset('images/profile.webp') }}" alt="신중수 프로필 사진" width="720" height="720"
                     class="aspect-[260/325] w-[220px] rounded-[24px] object-cover shadow-[0_24px_60px_-20px_rgba(17,17,17,0.25)] md:w-[260px] md:rounded-[28px]">
                <div class="md:pt-6">
                    <h2 class="text-display-2 break-keep text-ink"><span class="font-bold">/</span>이력</h2>
                    <p class="mt-5 text-[clamp(20px,1.167vw,24px)] leading-[1.5] font-semibold tracking-[-0.05em] break-keep text-ink">신중수 <span class="font-normal">· 서비스 기획자</span></p>
                    {{-- 줄바꿈은 Figma 대로. 좁은 폭에서는 br 을 죽이고 자연 줄바꿈. --}}
                    <p class="mt-3 text-[clamp(16px,0.973vw,20px)] leading-[1.533] tracking-[-0.04em] break-keep text-body">
                        B2B SaaS 그룹웨어 시장에 대한 깊이 있는 도메인 지식 (HR/재무/그룹웨어)을 보유하고 있습니다.<br class="hidden lg:inline">
                        사용자 중심의 데이터 분석 및 시스템 아키텍처 기획을 기반으로 복잡한 엔터프라이즈 프로세스를<br class="hidden lg:inline">
                        사용자 친화적 UX로 혁신하는 데 특화되어 있습니다.
                    </p>
                    <a href="mailto:wndtn0526@gmail.com" class="group mt-6 inline-flex items-center gap-3 text-heading-2 font-semibold text-ink">
                        <span class="underline decoration-1 underline-offset-[6px]">이메일 보내기</span>
                        <span aria-hidden="true" class="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5">↗</span>
                    </a>
                </div>
            </div>

            {{-- 경력. 행 = [라벨 | 내용 | 기간]. --}}
            <div class="mt-[clamp(3rem,6vw,5rem)]">
                <p class="{{ $label }} mb-3">경력</p>
                <div class="{{ $row }}">
                    <span class="{{ $label }}">2026</span>
                    <div>
                        <p class="{{ $title }}">청담원 주식회사</p>
                        <p class="{{ $sub }}">케어닷 신사업팀 / 서비스 기획</p>
                        <ul class="{{ $bullets }} list-disc">
                            <li>재가 돌봄 신규 서비스 플랫폼 A-Z 기획 및 구현</li>
                            <li>사업 전략 검토 · IA · 기능정의 · 데이터 설계 · 화면 구현 전 과정 리드 (지정심사, 상담, 채용, 수급자 관리, 직원 관리, 청구, 재무회계, 평가)</li>
                            <li>레거시 확장 vs 신규 구축 시나리오를 비용 · 확장성 · 운영 리스크로 비교 분석, 「신규 구축 + 핵심 기능 우선」 전략 제안 및 채택</li>
                            <li>기획-디자인-구현-검증을 잇는 AI 업무 파이프라인 설계, 주간보고 자동화로 비개발 이해관계자 소통 비용 절감</li>
                            <li>사업설명서 · 센터장 간담회 PT 등 내외부 이해관계자 커뮤니케이션 주도</li>
                        </ul>
                    </div>
                    <span class="{{ $right }}">2026년 5월 ~ 2026년 9월</span>
                </div>
                <div class="{{ $row }}">
                    <span class="{{ $label }}">2021 – 2025</span>
                    <div>
                        <p class="{{ $title }}">워크앤조이</p>
                        <p class="{{ $sub }}">그룹웨어프로팀 / 서비스 기획</p>
                        <ul class="{{ $bullets }} list-disc">
                            <li>그룹웨어프로 인사･재무･결재 모듈 A-Z기획</li>
                            <li>사용자 패턴 분석, 도메인 지식 바탕으로 UX Writing 전략 수립 및 적용</li>
                            <li>VOC 데이터 및 유저 패턴 기반 경험 중심의 화면 설계 및 UX 개선 기획</li>
                            <li>온 오프라인 홍보물, 캠페인 콘텐츠 등 Visual Design 제작 · 사내 서식류 디자인 관리</li>
                            <li>고객사 대상 데모 시연 및 기능 컨설팅, 인사·재무 담당자 기능 교육 운영</li>
                            <li>IR 자료 제작 핵심 기획자로 참여, 서비스 포지셔닝 및 투자 제안서 구성</li>
                        </ul>
                    </div>
                    <span class="{{ $right }}">2021년 10월 ~ 2025년 8월</span>
                </div>
                <div class="{{ $row }}">
                    <span class="{{ $label }}">2021</span>
                    <div>
                        <p class="{{ $title }}">풀다랩</p>
                        <p class="{{ $sub }}">아트팀 / 브랜드 비딩 기획 및 디자인 업무</p>
                    </div>
                    <span class="{{ $right }}">2021년 04월 ~ 2021년 09월</span>
                </div>
                <div class="{{ $row }}">
                    <span class="{{ $label }}">2019 – 2020</span>
                    <div>
                        <p class="{{ $title }}">미디어로그</p>
                        <p class="{{ $sub }}">LG U+ IP TV 사업본부 / IP TV 플랫폼 포스터 디자인</p>
                    </div>
                    <span class="{{ $right }}">2019년 12월 ~ 2020년 10월</span>
                </div>
                <div class="{{ $row }} border-b">
                    <span class="{{ $label }}">2017 – 2019</span>
                    <div>
                        <p class="{{ $title }}">이디엠에듀케이션</p>
                        <p class="{{ $sub }}">IELTS 인강 신사업부 서비스기획팀 / 시스템 기획 및 사업 기획 · 서비스 운영</p>
                        <ul class="{{ $bullets }} list-disc">
                            <li>연 매출 10억 규모 인강 사이트 운영 담당</li>
                            <li>edm IELTS 인강 플랫폼 기획</li>
                            <li>IELTS 토스 및 한국어 인강 론칭</li>
                        </ul>
                    </div>
                    <span class="{{ $right }}">2017년 10월 ~ 2019년 04월</span>
                </div>
            </div>

            <div class="mt-16">
                <p class="{{ $label }} mb-3">학력</p>
                <div class="{{ $row }} border-b">
                    <span class="{{ $label }}">2012 – 2016</span>
                    <div>
                        <p class="{{ $title }}">백석예술대학교</p>
                        <p class="{{ $sub }}">시각디자인과 졸업</p>
                    </div>
                    <span class="{{ $right }}">2012년 02월 ~ 2016년 3월</span>
                </div>
            </div>

            <div class="mt-16">
                <p class="{{ $label }} mb-3">프로필</p>
                @foreach ([['생년월일','1993-05-26'],['전화번호','+82 10-2262-5913'],['이메일','wndtn0526@gmail.com'],['주소','경기도 수원시 권선구 호매실로 165번길 70 경남아너스빌 1516동 202호']] as [$k, $val])
                    <div class="{{ $row }} {{ $loop->last ? 'border-b' : '' }}">
                        <span class="{{ $label }}">{{ $k }}</span>
                        <p class="{{ $title }}">{{ $val }}</p>
                    </div>
                @endforeach
            </div>
        </section>
    </main>
</x-layouts.app>
