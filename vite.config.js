import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite';

/*
 * Tailwind preflight 는 폰트를 이렇게 깐다:
 *
 *   font-family: var(--default-font-family, -apple-system, …, "Noto Sans", Arial, sans-serif, …);
 *
 * --default-font-family 는 var(--font-sans) 로 정의돼 있어서 이 폴백은 실제로 적용되지 않는다.
 * 그래도 빌드된 CSS 에는 죽은 폰트 이름이 문자열로 남는다. 잘라낸다.
 *
 * preflight 를 직접 들고 오는 대신(업스트림과 갈라진다) 산출물에서 폴백만 자른다.
 * Tailwind 가 패턴을 바꾸면 정규식이 안 맞아 아무 일도 일어나지 않는다 — 깨지지 않는다.
 */
function stripDeadFontFallbacks() {
    return {
        name: 'strip-dead-font-fallbacks',
        enforce: 'post',
        generateBundle(_options, bundle) {
            for (const file of Object.values(bundle)) {
                if (file.type !== 'asset' || !file.fileName.endsWith('.css')) continue;

                file.source = String(file.source).replace(
                    /var\((--default(?:-mono)?-font-family),[^)]*\)/g,
                    'var($1)',
                );
            }
        },
    };
}

/*
 * 폰트는 app.css 에서 CDN 으로 로드한다. laravel-vite-plugin 의 bunny() 는 Google Fonts
 * 미러라 한글 서체(Pretendard)가 없어서 쓰지 않는다.
 */
export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
        tailwindcss(),
        stripDeadFontFallbacks(),
    ],
    server: {
        watch: {
            ignored: ['**/storage/framework/views/**'],
        },
    },
});
