#!/usr/bin/env python3
"""21일 트리플챌린지 카톡 공유 썸네일(OG 이미지) 생성.

- 1200x630 (카톡/페이스북 링크 미리보기 표준 비율)
- 공식 로고 JPG의 흰 배경을 알파로 키잉해 파스텔 민트 그라데이션 위에 중앙 배치
- 하단에 작은 제품 라인 텍스트 (이오메가 리퀴드 · 레몬 · 포스티엠)
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
SRC = "../../attachments/2026-11-24/IMG_1827-bad7596b9a1146f9a36f8a0f8fc319dc.jpg"
OUT_REPO = "og-image.png"
OUT_DL = "../../downloads/트리플21_카톡_공유썸네일.png"
FONT = "/usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf"

# ---------- 1) 배경: 중앙 화이트 → 외곽 민트 파스텔 (부드러운 방사형) ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = W / 2, H * 0.47
nx = (xx - cx) / 800.0
ny = (yy - cy) / 470.0
d = np.clip(np.sqrt(nx ** 2 + ny ** 2), 0, 1) ** 1.15
white = np.array([255, 255, 255], np.float32)
mint = np.array([219, 240, 229], np.float32)   # #DBF0E5
arr = white[None, None, :] * (1 - d[..., None]) + mint[None, None, :] * d[..., None]
bg = Image.fromarray(arr.round().astype(np.uint8), "RGB")

# ---------- 2) 로고: 흰 배경 알파 키잉 ----------
logo = Image.open(SRC).convert("RGB")
lx, ly = logo.size
la = np.asarray(logo).astype(np.int16)
minc = la.min(axis=2)
amask = np.clip((250 - minc) * 255.0 / 210.0, 0, 255).astype(np.uint8)
alpha = Image.fromarray(amask, "L").filter(ImageFilter.MedianFilter(3))
bbox = alpha.getbbox()
logo = logo.crop(bbox)
alpha = alpha.crop(bbox)
logo.putalpha(alpha)
print("cropped logo:", logo.size)

target_h = 486
scale = target_h / logo.size[1]
if logo.size[0] * scale > W * 0.82:
    scale = (W * 0.82) / logo.size[0]
nw, nh = int(round(logo.size[0] * scale)), int(round(logo.size[1] * scale))
logo = logo.resize((nw, nh), Image.LANCZOS)
print("placed logo:", logo.size)

pos = ((W - nw) // 2, 270 - nh // 2)
bg.paste(logo, pos, logo)

# ---------- 3) 하단 제품 라인 텍스트 ----------
d_ = ImageDraw.Draw(bg)
text = "이오메가 리퀴드 · 레몬 · 포스티엠"
f = ImageFont.truetype(FONT, 30)
tracking = 2
widths = [d_.textlength(ch, font=f) for ch in text]
tw = int(sum(widths) + tracking * (len(text) - 1))
x = (W - tw) // 2
y = 543
for ch, w in zip(text, widths):
    d_.text((x, y), ch, font=f, fill=(62, 107, 87), stroke_width=1, stroke_fill=(62, 107, 87))
    x += w + tracking

bg.save(OUT_REPO, "PNG", optimize=True)
bg.save(OUT_DL, "PNG", optimize=True)
print("saved", OUT_REPO, bg.size)
