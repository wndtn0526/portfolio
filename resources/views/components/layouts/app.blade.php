<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{ $title ?? config('app.name') }}</title>

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
