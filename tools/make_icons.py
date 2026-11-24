#!/usr/bin/env python3
"""공식 트리플챌린지 로고(tools/logo-master.png)로 PWA 앱 아이콘·스플래시용 이미지를 만든다.

사용: python3 tools/make_icons.py
- icon-192 / icon-512 / apple-touch-icon : 흰 바탕 정사각, 로고를 82% 크기로 중앙 배치
  (maskable 안전 영역 80% 안에 로고의 원형 테두리가 모두 들어오도록 82%)
- favicon-32 : 작은 크기에서도 형태가 남도록 94%
- logo.webp  : 시작 화면용 560px
"""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, 'tools', 'logo-master.png')
WHITE = (255, 255, 255)

TARGETS = [
    ('icon-192.png', 192, 0.82),
    ('icon-512.png', 512, 0.82),
    ('apple-touch-icon.png', 180, 0.82),
    ('favicon-32.png', 32, 0.94),
]


def place(master, size, ratio):
    canvas = Image.new('RGB', (size, size), WHITE)
    box = max(1, int(round(size * ratio)))
    logo = master.resize((box, box), Image.LANCZOS)
    off = (size - box) // 2
    canvas.paste(logo, (off, off))
    return canvas


def main():
    master = Image.open(MASTER).convert('RGB')
    for name, size, ratio in TARGETS:
        im = place(master, size, ratio)
        p = os.path.join(ROOT, name)
        im.save(p, 'PNG', optimize=True)
        print('wrote', p, im.size)
    splash = place(master, 560, 0.98)
    p = os.path.join(ROOT, 'logo.webp')
    splash.save(p, 'WEBP', quality=90, method=6)
    print('wrote', p, splash.size)


if __name__ == '__main__':
    main()
