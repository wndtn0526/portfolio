{{--
    인트로 — Figma  PORTFOLIO 슬라이드 02 (node 1083:280397) 실측을 웹으로 옮긴 것.

    시안은 1920x1080 고정 슬라이드다. 값(98/48/18px · 좌여백 80 · 본문폭 940)은 그대로 두되
    화면 크기를 따라 흐르게 clamp 로 감쌌다. 레퍼런스(montone.studio)를 따라
    세로 스크롤 · 최소 내비 · 번호 붙인 절(01·02) 구성으로 폈다.

    ⚠️ 시안 원문의 오탈자 두 곳을 고쳐서 옮겼다 — `Brand Experrience` → Experience,
       `브래느 스토리텔링` → 브랜드. Figma 원본도 같이 고쳐야 갈라지지 않는다.
--}}
<x-layouts.app title="신중수 · Product Manager / Product Designer">

    {{-- ── 상단 내비 — 스크롤해도 남는다. 이름과 연락처만. ── --}}
    {{-- 내비 — 레퍼런스 실측: fixed · 높이 73 · 흰색 60% + blur(20px) · 내려가면 숨는다.
         숨기는 동작은 resources/js/app.js 에 있다(개발·정적 양쪽에서 같이 돌게 하려고 Alpine 을 안 썼다). --}}
    <header data-nav
            class="fixed inset-x-0 top-0 z-50 h-[73px] border-b border-line/60 bg-canvas/60 backdrop-blur-[20px] transition-transform duration-300 ease-out motion-reduce:transition-none">
        <div class="mx-auto flex h-full max-w-[1760px] items-center justify-between px-[clamp(1.5rem,5vw,5rem)]">
            <a href="#top" class="text-sm font-bold tracking-[-0.02em] text-ink">신중수</a>
            <a href="mailto:wndtn0526@gmail.com"
               class="group inline-flex items-center gap-2 text-sm font-medium text-body transition-colors hover:text-ink">
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
            {{-- 아래쪽을 캔버스로 녹여 다음 절과 이어붙인다 --}}
            <div aria-hidden="true"
                 class="pointer-events-none absolute inset-x-0 bottom-0 -z-10 h-40 bg-gradient-to-b from-transparent to-canvas"></div>

            <div class="mx-auto w-full max-w-[1760px] px-[clamp(1.5rem,5vw,5rem)]">
                <h1 class="font-bold tracking-[-0.02em] text-ink text-[clamp(2.5rem,7.6vw,98px)] leading-[1.04]">
                    Beauty is in the<br>eye of the beholder.
                </h1>

                <p class="mt-[clamp(1.5rem,3vw,2.75rem)] text-ink text-[clamp(1.125rem,2.6vw,48px)] leading-[1.32]">
                    사랑하는 사람은 뭐든지 다 예뻐보인다는 말인데,<br>
                    <strong class="font-bold">저는 이 말이 좋습니다.</strong>
                </p>
            </div>

            {{-- 스크롤 안내 — 레퍼런스의 'Scroll' 자리 --}}
            <div class="absolute inset-x-0 bottom-10 mx-auto w-full max-w-[1760px] px-[clamp(1.5rem,5vw,5rem)]">
                <span class="inline-flex items-center gap-3 text-xs font-medium tracking-[0.18em] text-muted uppercase">
                    Scroll
                    <span aria-hidden="true" class="h-px w-10 origin-left animate-scroll-cue bg-muted"></span>
                </span>
            </div>
        </section>

        {{-- ── 소개 ── 시안에서는 한 덩어리 문단이다. 웹에서는 안 읽히므로
             원문에 이미 있던 두 축(1·2)을 절로 세우고 번호를 붙였다. --}}
        <section class="mx-auto w-full max-w-[1760px] px-[clamp(1.5rem,5vw,5rem)] pb-[clamp(5rem,12vw,10rem)]">
            <div class="max-w-readable">

                <p class="text-[clamp(1.0625rem,1.5vw,1.375rem)] leading-[1.5] tracking-[-0.02em] text-ink">
                    맡은 일의 본질적인 가치<span class="text-muted">(Value)</span>를 발견하고,
                    그 가치가 사용자에게 가장 매력적으로 다가갈 수 있는 방법을 고민합니다.
                    이는 기능적 완벽함을 넘어, 사용자의 마음을 사로잡는
                    브랜드 경험<span class="text-muted">(Brand Experience)</span>의 영역이기도 합니다.
                </p>

                <p class="mt-6 text-[0.9375rem] leading-[1.4] text-body">
                    저의 가장 큰 무기이자 차별점은 서로 다른 두 영역에서의 깊은 통찰을 결합했다는 점입니다.
                </p>

                <dl class="mt-[clamp(3rem,6vw,5rem)] grid gap-[clamp(2.5rem,5vw,4rem)] border-t border-line pt-[clamp(2.5rem,5vw,4rem)] md:grid-cols-2">
                    <div>
                        <dt class="text-lg tracking-tight text-ink">
                            구조와 논리의 깊이
                            <span class="mt-1 block text-xs tracking-[0.08em] text-muted uppercase">B2B Domain Logic</span>
                        </dt>
                        <dd class="mt-4 text-[0.9375rem] leading-[1.4] text-body">
                            그룹웨어 시장에서의 깊은 도메인 경험을 통해 어떤 기술도 도메인보다 앞설 수 없다는
                            신념을 가지고, 실제 현업의 복잡한 업무 흐름<span class="text-muted">(HR·재무)</span>을
                            깊이 이해하고 구조화할 수 있게 성장했습니다. 명확한 목표와 올바른 방향 설정이
                            정답에 가까운 결과를 만든다는 믿음으로, 엔터프라이즈의 비효율을 해소하는
                            논리적인 UX 설계에 집중합니다.
                        </dd>
                    </div>

                    <div>
                        <dt class="text-lg tracking-tight text-ink">
                            브랜드와 소통의 폭
                            <span class="mt-1 block text-xs tracking-[0.08em] text-muted uppercase">B2C Visual Communication</span>
                        </dt>
                        <dd class="mt-4 text-[0.9375rem] leading-[1.4] text-body">
                            이전 광고대행사 경험에서 얻은 브랜드 스토리텔링 및 비주얼 커뮤니케이션 능력은
                            제품의 매력도를 극대화하는 중요한 도구입니다. 딱딱하게 느껴지기 쉬운 B2B 솔루션에
                            사용자에게 공감을 주는 UX Writing 과 일관된 브랜드 경험을 입혀,
                            사용자가 사랑하고 습관적으로 이용하는 제품으로 전환시킵니다.
                        </dd>
                    </div>
                </dl>

                <p class="mt-[clamp(3rem,6vw,5rem)] border-t border-line pt-[clamp(2.5rem,5vw,4rem)] text-[clamp(1rem,1.3vw,1.25rem)] leading-[1.5] tracking-[-0.02em] text-ink">
                    저는 주어진 일의 가치를 넘어서는 새로운 가치를 만들어내는 엑스트라 마일을 실현하며,
                    함께 일하며 더 높은 곳을 바라보는 좋은 동료, 신뢰받는 협업자가 되고 싶습니다.
                    <span class="text-muted">멋진 관계를 기대합니다.</span>
                </p>
            </div>
        </section>


        {{-- ── 피처 ── montone.studio 의 두 번째 피처 섹션(서비스 01~05)을 그대로 옮긴 구조다.
             1440 기준 실측: 번호 100.8px/700/행간 0.85/자간 -0.03em · 제목 46.08px/**400**/행간 1.0/자간 -0.025em
             (앞 `/` 만 700) · 본문 15px/400/행간 1.4 · 본문폭 733.
             ⚠️ 레퍼런스는 큰 제목을 굵게 쓰지 않는다. 700 은 번호와 슬래시에만 쓴다.
             ⚠️ 항목 내용은 임시다. 기획을 다시 하는 중이라 확정본이 아니다. --}}
        <section class="mx-auto w-full max-w-[1760px] px-[clamp(1.5rem,5vw,5rem)] pb-[clamp(5rem,12vw,10rem)]">
            <ol class="mx-auto flex w-full max-w-feature flex-col gap-[clamp(3rem,6vw,5.5rem)]">
                @foreach ([
                    ['no' => '01', 'title' => '제품 기획과 전략',
                     'body' => '무엇을 만들지 정하는 일부터 시작합니다. 레거시를 확장할지 새로 지을지 같은 판단을 트레이드오프 표로 정리해 경영진에게 건의하고, 정보구조와 기능정의서로 옮겨 팀이 같은 그림을 보게 만듭니다.'],
                    ['no' => '02', 'title' => 'UX · UI 설계',
                     'body' => '복잡한 엔터프라이즈 업무 흐름을 화면으로 옮깁니다. 흩어진 기능을 과업 단위로 묶어 페이지 이동을 걷어내고, 담당자가 한 화면에서 일을 끝낼 수 있게 설계합니다.'],
                    ['no' => '03', 'title' => 'AI 파이프라인 설계',
                     'body' => '기획부터 구현·문서화·보고까지 하나의 흐름으로 잇습니다. 반복 절차를 표준화한 뒤 도구를 붙이고, 주기 자동 실행까지 올립니다. 판단이 필요한 자리는 사람에게 남깁니다.'],
                    ['no' => '04', 'title' => '디자인 시스템',
                     'body' => '토큰과 컴포넌트, 살아 있는 스타일가이드로 화면이 제각각 자라지 않게 붙듭니다. 새 화면을 빨리 만드는 것보다 오래 유지되는 쪽을 먼저 봅니다.'],
                    ['no' => '05', 'title' => '도메인 전문성',
                     'body' => '그룹웨어(HR · 재무)와 장기요양 두 도메인에서 실제 업무와 법·제도를 읽고 규칙으로 옮겼습니다. 어떤 기술도 도메인보다 앞설 수 없다고 봅니다.'],
                ] as $item)
                    <li>
                        <div class="flex items-center gap-[clamp(0.75rem,1.6vw,1.6rem)]">
                            <span aria-hidden="true"
                                  class="numeral-gradient font-bold tabular-nums leading-[0.85] tracking-[-0.03em] text-[clamp(3.25rem,7vw,100.8px)]">{{ $item['no'] }}</span>
                            <h2 class="font-normal leading-none tracking-[-0.025em] text-ink text-[clamp(1.5rem,3.2vw,46.08px)]">
                                <span class="font-bold">/</span>{{ $item['title'] }}
                            </h2>
                        </div>
                        <p class="mt-[clamp(0.75rem,1.4vw,1.25rem)] text-[0.9375rem] leading-[1.4] text-body">
                            {{ $item['body'] }}
                        </p>
                    </li>
                @endforeach
            </ol>
        </section>

        {{-- ── 연락 ── --}}
        <footer class="border-t border-line">
            <div class="mx-auto flex w-full max-w-[1760px] flex-col gap-6 px-[clamp(1.5rem,5vw,5rem)] py-[clamp(2.5rem,5vw,4rem)] sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <p class="text-xs font-medium tracking-[0.18em] text-muted uppercase">Contact</p>
                    <a href="mailto:wndtn0526@gmail.com"
                       class="mt-2 inline-block text-[clamp(1.25rem,3vw,2rem)] font-bold tracking-[-0.025em] text-ink underline-offset-[6px] hover:underline">
                        wndtn0526@gmail.com
                    </a>
                </div>
                <p class="text-sm text-muted">신중수 · Product Manager / Product Designer</p>
            </div>
        </footer>
    </main>
</x-layouts.app>
