<?php

use Illuminate\Support\Facades\Route;

// 첫 화면. Figma 포트폴리오 디자인이 들어오면 화면별로 라우트를 나눈다.
Route::view('/', 'home')->name('home');

