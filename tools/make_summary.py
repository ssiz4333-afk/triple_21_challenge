#!/usr/bin/env python3
"""트리플21 PWA 결과물 한 장 요약 이미지 생성."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W = 1640
H = 968
SS = 2  # supersample

BG_TOP = (244, 250, 247)
BG_BOT = (226, 240, 233)
INK = (18, 36, 30)
INK2 = (73, 97, 88)
INK3 = (138, 160, 150)
MINT = (12, 143, 110)
MINT_DARK = (11, 95, 71)
CARD = (255, 255, 255)

FONT = '_work/fonts/NotoSansKR.ttf'


def font(size, weight='Regular'):
    f = ImageFont.truetype(FONT, int(size * SS))
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def text(d, xy, s, f, fill, anchor='la'):
    d.text((xy[0] * SS, xy[1] * SS), s, font=f, fill=fill, anchor=anchor)


def wrap(d, s, f, max_w):
    words = s.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if d.textlength(trial, font=f) / SS <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_mask(w, h, r):
    m = Image.new('L', (w * SS, h * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], radius=r * SS, fill=255)
    return m


def paste_rounded(base, img, box, radius, shadow=True, shadow_blur=18, shadow_alpha=70, ring=None):
    """box = (x, y, w, h) in final-pixel coordinates."""
    x, y, w, h = box
    im = img.convert('RGB').resize((w * SS, h * SS), Image.LANCZOS).convert('RGBA')
    mask = rounded_mask(w, h, radius)
    im.putalpha(mask)

    if shadow:
        sh = Image.new('RGBA', (w * SS + 120, h * SS + 120), (0, 0, 0, 0))
        sm = Image.new('L', (w * SS + 120, h * SS + 120), 0)
        ImageDraw.Draw(sm).rounded_rectangle([60, 60 + 10 * SS, 60 + w * SS, 60 + h * SS + 10 * SS],
                                            radius=radius * SS, fill=shadow_alpha)
        sm = sm.filter(ImageFilter.GaussianBlur(shadow_blur * SS))
        sh.putalpha(sm)
        base.alpha_composite(sh, ((x - 60 // SS) * SS, (y - 60 // SS) * SS))

    if ring:
        ring_im = Image.new('RGBA', (w * SS + 8 * SS, h * SS + 8 * SS), (0, 0, 0, 0))
        ImageDraw.Draw(ring_im).rounded_rectangle([0, 0, w * SS + 8 * SS - 1, h * SS + 8 * SS - 1],
                                                  radius=(radius + 4) * SS, outline=ring, width=int(1.5 * SS))
        base.alpha_composite(ring_im, ((x - 4) * SS, (y - 4) * SS))

    base.alpha_composite(im, (x * SS, y * SS))


def gradient_bg(w, h):
    small = Image.new('RGB', (32, 32))
    px = small.load()
    for yy in range(32):
        for xx in range(32):
            t = (xx / 31 * 0.35 + yy / 31 * 0.65)
            px[xx, yy] = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
    return small.resize((w * SS, h * SS), Image.BICUBIC)


def main():
    base = gradient_bg(W, H).convert('RGBA')
    d = ImageDraw.Draw(base)

    # ---- 헤더 ----
    pill_txt = 'PWA 적용 완료 · v2.1'
    f_pill = font(15, 'Bold')
    tw = d.textlength(pill_txt, font=f_pill) / SS
    d.rounded_rectangle([64 * SS, 46 * SS, (64 + tw + 34) * SS, 80 * SS], radius=17 * SS, fill=(223, 245, 234))
    text(d, (64 + 17, 55), pill_txt, f_pill, MINT_DARK)

    text(d, (64, 96), '바탕화면 앱 아이콘 · 시작 화면 · 홈 화면 추가 안내', font(34, 'Bold'), INK)
    text(d, (64, 146), 'ssiz4333-afk.github.io/triple_21_challenge  ·  홈 화면에 추가하면 주소창 없는 앱처럼 열립니다',
         font(16, 'Medium'), INK2)

    # ---- 폰 3대 ----
    pw, ph = 300, 527
    gap = 38
    x0 = 64
    y0 = 210

    phones = [
        ('browser/splash-final4-2026-11-24-082329.png', '① 시작 화면 (0.9초)', '앱을 열면 아이콘과 이름이 먼저 보였다가 부드럽게 사라집니다.'),
        ('browser/home-clean-2026-11-24-082116.png', '② 홈 화면 앱 실행 모습', '주소창 없이 전체 화면. 기록·인증샷·실시간 공유는 그대로 동작합니다.'),
        ('browser/install-sheet3-2026-11-24-082151.png', '③ 홈 화면 추가 안내 시트', '설정 → 📲 바탕화면 앱으로 추가하기. 아이폰·안드로이드 단계별 안내.'),
    ]

    f_cap = font(17, 'Bold')
    f_desc = font(13, 'Medium')

    for i, (path, cap, desc) in enumerate(phones):
        im = Image.open(path)
        x = x0 + i * (pw + gap)
        paste_rounded(base, im, (x, y0, pw, ph), 34, ring=(255, 255, 255, 235))
        text(d, (x + 2, y0 + ph + 20), cap, f_cap, INK)
        for k, line in enumerate(wrap(d, desc, f_desc, pw - 4)):
            text(d, (x + 2, y0 + ph + 46 + k * 18), line, f_desc, INK2)

    # ---- 아이콘 패널 ----
    px0 = x0 + 3 * pw + 2 * gap + 44
    panel_w = W - px0 - 64
    py0 = y0
    panel_h = ph + 90
    d.rounded_rectangle([px0 * SS, py0 * SS, (px0 + panel_w) * SS, (py0 + panel_h) * SS],
                        radius=30 * SS, fill=CARD + (255,))
    d.rounded_rectangle([px0 * SS, py0 * SS, (px0 + panel_w) * SS, (py0 + panel_h) * SS],
                        radius=30 * SS, outline=(226, 237, 231, 255), width=int(1.2 * SS))

    text(d, (px0 + 28, py0 + 26), '앱 아이콘', font(19, 'Bold'), INK)
    text(d, (px0 + 28, py0 + 56), '민트 그라데이션 + 흰 잎사귀 · 굵은 21', font(12.5, 'Medium'), INK3)

    icons = [
        ('_work/triple21-repo/icon-512.png', 168, 'icon-512.png', '512 × 512 · 안드로이드/크롬'),
        ('_work/triple21-repo/icon-192.png', 84, 'icon-192.png', '192 × 192 · 홈 화면'),
        ('_work/triple21-repo/apple-touch-icon.png', 84, 'apple-touch-icon.png', '180 × 180 · 아이폰'),
    ]
    ix = px0 + 28
    iy = py0 + 96
    # 큰 아이콘
    big = Image.open(icons[0][0])
    paste_rounded(base, big, (ix, iy, 168, 168), 38, shadow=True, shadow_blur=14, shadow_alpha=60)
    text(d, (ix, iy + 180), icons[0][2], font(13, 'Bold'), INK)
    text(d, (ix, iy + 199), icons[0][3], font(11.5, 'Medium'), INK3)

    # 작은 아이콘 2개 (가로 배치)
    sx = ix + 168 + 32
    sy = iy + 78
    for j, (path, size, name, desc) in enumerate(icons[1:]):
        im = Image.open(path)
        yy = sy + j * 108
        paste_rounded(base, im, (sx, yy, size, size), 20, shadow=True, shadow_blur=8, shadow_alpha=45)
        text(d, (sx + size + 16, yy + 14), name, font(12.5, 'Bold'), INK)
        text(d, (sx + size + 16, yy + 34), desc, font(11, 'Medium'), INK3)

    # 체크리스트
    cy = py0 + 340
    items = [
        ('manifest.json', 'display: standalone · 테마 #0d9488'),
        ('sw.js', '서비스 워커 등록 · 오프라인에서도 열림'),
        ('홈 화면 추가 버튼', '설정 시트 + 오늘 탭 안내 배너'),
    ]
    for j, (head, sub) in enumerate(items):
        yy = cy + j * 58
        d.ellipse([(ix) * SS, (yy + 5) * SS, (ix + 15) * SS, (yy + 20) * SS], fill=(18, 181, 139))
        d.line([(ix + 4) * SS, (yy + 12) * SS, (ix + 7) * SS, (yy + 16) * SS], fill=(255, 255, 255), width=int(1.8 * SS))
        d.line([(ix + 7) * SS, (yy + 16) * SS, (ix + 12) * SS, (yy + 8) * SS], fill=(255, 255, 255), width=int(1.8 * SS))
        text(d, (ix + 24, yy), head, font(13, 'Bold'), INK)
        text(d, (ix + 24, yy + 19), sub, font(11, 'Medium'), INK3)

    # ---- 하단 ----
    by = py0 + ph + 110
    d.rounded_rectangle([64 * SS, by * SS, (W - 64) * SS, (by + 56) * SS], radius=18 * SS, fill=(236, 248, 242))
    text(d, (86, by + 12), '실제 배포 주소에서 확인한 화면입니다 — manifest.json · icon-192/512 · apple-touch-icon · sw.js 모두 HTTP 200, 콘솔 오류 0건',
         font(13, 'SemiBold'), (30, 92, 72))
    text(d, (86, by + 32), '제작자 @erang_coach  ·  21일 트리플챌린지 (이오메가 리퀴드 · 레몬 · 포스티엠)',
         font(11.5, 'Medium'), INK3)

    out = base.resize((W, H), Image.LANCZOS).convert('RGB')
    os.makedirs('downloads', exist_ok=True)
    path = 'downloads/트리플21_앱아이콘_스플래시.png'
    out.save(path, 'PNG', optimize=True)
    print('saved', path, out.size)


if __name__ == '__main__':
    main()
