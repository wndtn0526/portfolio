<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{ $title ?? config('app.name') }}</title>
    {{-- 파비콘 — 로고타입 PORTFOLIO 의 P, 선언 섹션 색(#504fed). public/images 에 둬야 정적 export 가 함께 옮긴다. --}}
    <link rel="icon" type="image/svg+xml" href="{{ asset('images/favicon.svg') }}">

    {{-- 링크 미리보기(카카오톡 · 슬랙 · 지원서 링크) — 이미지와 주소는 절대 URL 이어야 대부분의 서비스가 읽는다.
         배포 주소(GitHub Pages)가 바뀌면 $site 를 함께 바꾼다. og.jpg 는 히어로 배경으로 만든 1200×630. --}}
    @php $site = 'https://wndtn0526.github.io/portfolio/'; $desc = '서비스 기획자 신중수의 포트폴리오입니다. 그룹웨어프로 SaaS 기획과 런칭, 이디엠에듀케이션 온라인 인강, 청담원 주식회사의 재가 돌봄 플랫폼 케어닷 프로젝트를 담았습니다.'; @endphp
    <meta name="description" content="{{ $desc }}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:title" content="{{ $title ?? config('app.name') }}">
    <meta property="og:description" content="{{ $desc }}">
    <meta property="og:url" content="{{ $site }}">
    <meta property="og:image" content="{{ $site }}images/og.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">

    {{--
        본문 서체 Pretendard (dynamic subset — 한글 용량 최적화).
        ⚠️ app.css 안에서 @import url(...) 로 걸면 안 된다. Tailwind 4 가 'tailwindcss' 를
           먼저 인라인해 버려서 이 @import 가 규칙들 뒤로 밀리고, lightningcss 가
           "@import 는 규칙보다 앞서야 한다"며 **조용히 잘라낸다** — 빌드는 성공하는데
           폰트만 안 걸린다. 그래서 여기 <link> 로 둔다.
        TODO(프로덕션): public/fonts 로 self-host 하거나 npm `pretendard` 사용.
    --}}
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-dvh bg-canvas font-sans text-body antialiased">
    {{ $slot }}
</body>
</html>
