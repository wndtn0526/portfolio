{{--
    임시 첫 화면. Figma 포트폴리오 디자인을 읽어 오면 통째로 갈아엎는다.
    지금은 빌드 파이프라인(Vite · Tailwind · 정적 export)이 도는지 확인하는 용도다.
--}}
<x-layouts.app title="Portfolio">
    <main class="mx-auto flex min-h-dvh max-w-2xl flex-col justify-center gap-3 px-6">
        <p class="text-sm font-medium text-neutral-400">준비 중</p>
        <h1 class="text-3xl font-bold tracking-tight text-neutral-900">포트폴리오</h1>
        <p class="text-base leading-relaxed text-neutral-600">
            Figma 디자인을 옮기기 전의 빈 껍데기다. 이 문장이 Pretendard 로 보이고
            여백이 잡혀 있으면 Tailwind 빌드가 제대로 물린 것이다.
        </p>
    </main>
</x-layouts.app>
