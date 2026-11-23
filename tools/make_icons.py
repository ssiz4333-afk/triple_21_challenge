#!/usr/bin/env python3
"""21일 트리플챌린지 PWA 앱 아이콘 생성 (Pillow 벡터 흉내 렌더링, 4x 슈퍼샘플)."""
from PIL import Image, ImageDraw
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..')

# 브랜드 색
MINT_DARK = (7, 102, 78)     # #07664E
MINT = (12, 143, 110)        # #0C8F6E
MINT_2 = (23, 192, 143)      # #17C08F
LEMON = (255, 225, 90)       # #FFE15A

SS = 4  # supersample


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient_bg(size):
    """대각선 민트 그라데이션 + 좌상단 은은한 하이라이트."""
    small = 96
    img = Image.new('RGB', (small, small))
    px = img.load()
    for y in range(small):
        for x in range(small):
            t = (x / (small - 1) * 0.55 + y / (small - 1) * 0.45)
            t = max(0.0, min(1.0, t))
            if t < 0.5:
                c = lerp(MINT_DARK, MINT, t / 0.5)
            else:
                c = lerp(MINT, MINT_2, (t - 0.5) / 0.5)
            # 좌상단 글로우
            d = math.hypot(x - small * 0.28, y - small * 0.18) / (small * 0.9)
            g = max(0.0, 1.0 - d) ** 2 * 0.20
            c = tuple(int(round(c[i] + (255 - c[i]) * g)) for i in range(3))
            px[x, y] = c
    return img.resize((size, size), Image.LANCZOS)


def cubic(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt ** 3 * p0[0] + 3 * mt ** 2 * t * p1[0] + 3 * mt * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = mt ** 3 * p0[1] + 3 * mt ** 2 * t * p1[1] + 3 * mt * t ** 2 * p2[1] + t ** 3 * p3[1]
        pts.append((x, y))
    return pts


def leaf_path(box):
    """브랜드 로고 SVG 잎사귀 경로를 box(24 기준 좌표)에 맞춰 스케일."""
    x0, y0, s = box  # 좌상단 + 24단위 스케일
    def P(x, y):
        return (x0 + x * s, y0 + y * s)
    pts = [P(20, 4.5)]
    pts += cubic(P(20, 4.5), P(20, 13), P(15, 18), P(6.5, 18))[1:]
    pts += [P(4.5, 18)]
    pts += cubic(P(4.5, 18), P(4.5, 9.5), P(9.5, 4.5), P(20, 4.5))[1:]
    return pts


def vein_path(box):
    x0, y0, s = box
    def P(x, y):
        return (x0 + x * s, y0 + y * s)
    return cubic(P(4.5, 18), P(7.5, 13.8), P(10.8, 10.8), P(15, 8.7), n=48)


def draw_icon(size):
    S = size * SS
    img = gradient_bg(S).convert('RGBA')
    d = ImageDraw.Draw(img, 'RGBA')

    # 중앙 방사형 소프트 글로우 (아이콘 깊이감)
    glow = Image.new('L', (S, S), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy = S * 0.5, S * 0.40
    r = S * 0.52
    steps = 60
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(26 * (1 - i / steps) ** 1.6)
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=a)
    img = Image.composite(Image.new('RGBA', (S, S), (255, 255, 255, 255)), img, glow.point(lambda v: v))
    d = ImageDraw.Draw(img, 'RGBA')

    # 잎사귀 (흰색)
    leaf_s = S * 0.0126           # 24단위 → 픽셀
    leaf_w = 24 * leaf_s          # 잎 크기
    leaf_x = (S - leaf_w * 0.86) / 2
    leaf_y = S * 0.225
    box = (leaf_x - 4.5 * leaf_s * 0, leaf_y, leaf_s)
    pts = leaf_path((leaf_x, leaf_y, leaf_s))
    d.polygon(pts, fill=(255, 255, 255, 255))
    # 잎맥 (배경색으로 파낸 선)
    vp = vein_path((leaf_x, leaf_y, leaf_s))
    d.line(vp, fill=(8, 116, 88, 255), width=max(2, int(leaf_s * 0.62)), joint='curve')

    # "21" 텍스트
    from PIL import ImageFont
    font_path = None
    for cand in (
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
    ):
        if os.path.exists(cand):
            font_path = cand
            break
    fsize = int(S * 0.330)
    font = ImageFont.truetype(font_path, fsize)
    text = '21'
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (S - tw) / 2 - bbox[0]
    ty = S * 0.515 - bbox[1]
    # 살짝 그림자
    shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((tx, ty + S * 0.012), text, font=font, fill=(3, 48, 36, 60))
    shadow = shadow.filter(__import__('PIL.ImageFilter', fromlist=['GaussianBlur']).GaussianBlur(S * 0.012))
    img = Image.alpha_composite(img, shadow)
    d = ImageDraw.Draw(img, 'RGBA')
    d.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

    # 하단 얇은 레몬 라인 (브랜드 포인트)
    bar_w = S * 0.115
    bar_h = S * 0.016
    bx = (S - bar_w) / 2
    by = S * 0.815
    d.rounded_rectangle([bx, by, bx + bar_w, by + bar_h], radius=bar_h / 2, fill=LEMON + (235,))

    return img.resize((size, size), Image.LANCZOS).convert('RGB')


def main():
    targets = {
        'icon-192.png': 192,
        'icon-512.png': 512,
        'apple-touch-icon.png': 180,
        'favicon-32.png': 32,
    }
    for name, size in targets.items():
        im = draw_icon(size)
        p = os.path.join(OUT, name)
        im.save(p, 'PNG', optimize=True)
        print('wrote', p, im.size)


if __name__ == '__main__':
    main()
