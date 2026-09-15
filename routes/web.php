<?php

use Illuminate\Support\Facades\Route;

// 첫 화면. Figma 포트폴리오 디자인이 들어오면 화면별로 라우트를 나눈다.
Route::view('/', 'home')->name('home');

/*
 * 진단용 — 히어로 메시를 이미지 대신 CSS 그라디언트로 그린 판.
 * 메뉴를 접을 때 300ms 멈추는 원인이 큰 WebP 의 재래스터화인지 가리려는 것이다.
 * 원인이 확정되면 이 라우트와 뷰 안의 @if 분기를 지운다.
 */
Route::view('/mesh-off', 'home', ['mesh' => false])->name('mesh-off');
