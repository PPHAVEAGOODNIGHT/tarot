# -*- coding: utf-8 -*-
"""PPTAROT 分享海报生成（水晶球 / 蝴蝶 / 月亮 / 星球 / 宇宙）"""
import io, os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

W, H = 750, 1334


def _pick_font(cands, linux_glob=""):
    """按候选顺序找第一个存在的字体文件，兼容 Windows / macOS / Linux。"""
    for p in cands:
        if p and os.path.isfile(p):
            return p
    if linux_glob:
        try:
            import glob
            hit = sorted(glob.glob(linux_glob))
            if hit:
                return hit[0]
        except Exception:
            pass
    return ""


_WIN_FONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
F_TITLE = _pick_font([
    os.path.join(_WIN_FONTS, "georgiab.ttf"),
    os.path.join(_WIN_FONTS, "georgia.ttf"),
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
], "/usr/share/fonts/**/DejaVuSerif-Bold.ttf")
F_CN = _pick_font([
    os.path.join(_WIN_FONTS, "msyhbd.ttc"),
    os.path.join(_WIN_FONTS, "msyh.ttc"),
    "/System/Library/Fonts/PingFang.ttc",
], "/usr/share/fonts/**/NotoSansCJK*Bold*.ttc")
F_CN_L = _pick_font([
    os.path.join(_WIN_FONTS, "msyh.ttc"),
    os.path.join(_WIN_FONTS, "simhei.ttf"),
    "/System/Library/Fonts/PingFang.ttc",
], "/usr/share/fonts/**/NotoSansCJK*.ttc")



def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        try:
            return ImageFont.truetype(F_CN, size)
        except Exception:
            return ImageFont.load_default()


def radial_mask(size, cx, cy, r, power=2.0, aspect=1.0):
    """生成径向渐变遮罩 (L 模式 float 0-1)"""
    w, h = size
    xs = np.arange(w) - cx
    ys = (np.arange(h) - cy) / aspect
    d = np.sqrt(xs[None, :] ** 2 + ys[:, None] ** 2) / max(r, 1e-6)
    a = np.clip(1 - d, 0, 1) ** power
    return a


def add_glow(img, cx, cy, r, color, strength=1.0, power=2.2, aspect=1.0):
    """叠加径向发光"""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    a = radial_mask(img.size, cx, cy, r, power, aspect)[..., None] * strength
    arr = arr + a * np.array(color, dtype=np.float32)[None, None, :]
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    if img.mode == "RGBA":
        out.putalpha(img.getchannel("A"))
    return out


def star_field(img, n=260, seed=7, tint=(190, 235, 255)):
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(0, W)
        y = rnd.uniform(0, H)
        # 上密下疏
        if rnd.random() < 0.35 and y > H * 0.62:
            continue
        r = rnd.choice([0.7, 0.9, 1.1, 1.3, 1.6, 2.1])
        a = rnd.randint(40, 200)
        d.ellipse([x - r, y - r, x + r, y + r], fill=tint + (a,))
    return img


def sparkle(img, x, y, size, color=(210, 245, 255), alpha=170):
    lay = Image.new("RGBA", (int(size * 6), int(size * 6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx = cy = size * 3
    d.line([(cx, cy - size * 3), (cx, cy + size * 3)], fill=color + (alpha,), width=max(1, int(size * 0.12)))
    d.line([(cx - size * 3, cy), (cx + size * 3, cy)], fill=color + (alpha,), width=max(1, int(size * 0.12)))
    lay = lay.filter(ImageFilter.GaussianBlur(size * 0.18))
    img.alpha_composite(lay, (int(x - size * 3), int(y - size * 3)))
    return img


def draw_moon(img, cx, cy, r, color=(243, 231, 196), glow=(255, 226, 160)):
    img = add_glow(img, cx, cy, r * 2.6, tuple(c * 0.30 for c in glow), power=2.6)
    lay = Image.new("RGBA", (int(r * 3), int(r * 3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = r * 1.5
    d.ellipse([c - r, c - r, c + r, c + r], fill=color + (255,))
    off = r * 0.52
    d.ellipse([c - r + off, c - r - off * 0.34, c + r + off, c + r - off * 0.34], fill=(0, 0, 0, 0))
    # 用透明挖洞
    mask = Image.new("L", lay.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([c - r, c - r, c + r, c + r], fill=255)
    md.ellipse([c - r + off, c - r - off * 0.34, c + r + off, c + r - off * 0.34], fill=0)
    solid = Image.new("RGBA", lay.size, color + (255,))
    lay = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    lay.paste(solid, (0, 0), mask)
    lay = lay.filter(ImageFilter.GaussianBlur(0.7))
    img.alpha_composite(lay, (int(cx - c), int(cy - c)))
    return img


def draw_planet(img, cx, cy, r, tilt=-22, body=(126, 214, 208), ring=(240, 215, 156)):
    img = add_glow(img, cx, cy, r * 2.4, tuple(c * 0.22 for c in body), power=2.4)
    # 环（后半）
    rw, rh = r * 2.5, r * 0.62
    ring_lay = Image.new("RGBA", (int(rw * 2), int(rh * 2.4)), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring_lay)
    cxr, cyr = rw, rh * 1.2
    rd.ellipse([cxr - rw * 0.94, cyr - rh * 0.94, cxr + rw * 0.94, cyr + rh * 0.94],
               outline=ring + (150,), width=max(2, int(r * 0.10)))
    rd.ellipse([cxr - rw * 0.74, cyr - rh * 0.74, cxr + rw * 0.74, cyr + rh * 0.74],
               outline=ring + (70,), width=max(1, int(r * 0.05)))
    ring_lay = ring_lay.rotate(tilt, resample=Image.BICUBIC, expand=False)
    back = ring_lay.crop((0, 0, ring_lay.width, int(cyr * 0.62)))
    img.alpha_composite(back, (int(cx - cxr), int(cy - cyr)))
    # 球体
    lay = Image.new("RGBA", (int(r * 2.4), int(r * 2.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = r * 1.2
    d.ellipse([c - r, c - r, c + r, c + r], fill=body + (235,))
    lay = lay.filter(ImageFilter.GaussianBlur(0.5))
    # 明暗
    shade = radial_mask(lay.size, c - r * 0.35, c - r * 0.38, r * 1.5, 1.6)
    arr = np.asarray(lay).astype(np.float32)
    arr[..., :3] *= (0.55 + 0.75 * shade[..., None])
    lay = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    img.alpha_composite(lay, (int(cx - c), int(cy - c)))
    # 环（前半）
    front = ring_lay.crop((0, int(cyr * 0.62), ring_lay.width, ring_lay.height))
    img.alpha_composite(front, (int(cx - cxr), int(cy + ring_lay.height - front.height - cyr)))
    return img


_FULL_CACHE = {}


def full_butterfly(path):
    """素材仅含单侧翅膀：沿翅根镜像拼接成左右对称的完整蝴蝶（结果缓存）"""
    key = os.path.abspath(path)
    if key in _FULL_CACHE:
        return _FULL_CACHE[key]
    im = Image.open(key).convert("RGBA")
    a = np.asarray(im)[..., 3].astype(np.float32)
    ys, xs = np.nonzero(a > 8)
    if len(xs) == 0:
        _FULL_CACHE[key] = im
        return im
    wing = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    w, h = wing.size
    col = a.sum(0)[xs.min():xs.max() + 1]
    half = w // 2
    root_left = col[:half].sum() > col[half:].sum()  # 像素强度大的一侧为翅根
    canvas = Image.new("RGBA", (w * 2, h), (0, 0, 0, 0))
    flip = wing.transpose(Image.FLIP_LEFT_RIGHT)
    if root_left:
        canvas.paste(flip, (0, 0))
        canvas.paste(wing, (w, 0))
    else:
        canvas.paste(wing, (0, 0))
        canvas.paste(flip, (w, 0))
    _FULL_CACHE[key] = canvas
    return canvas


def draw_butterfly(img, path, cx, cy, w, flip=False, alpha=185, tint=(150, 235, 235), margin=12):
    try:
        full = full_butterfly(path)
    except Exception:
        return img
    iw, ih = img.size
    h = int(w * full.height / full.width)
    bf = full.resize((int(w), h), Image.LANCZOS)
    if flip:
        bf = bf.transpose(Image.FLIP_LEFT_RIGHT)
    arr = np.asarray(bf).astype(np.float32)
    # 素材自带雾状低透明底，做阈值压掉，避免贴出海绵状方框
    raw = arr[..., 3]
    mask = np.clip((raw - 72.0) / 128.0, 0.0, 1.0)
    arr[..., 3] = mask * alpha
    # 轻微着色
    t = np.array(tint, dtype=np.float32) / 255.0
    for i in range(3):
        arr[..., i] = np.clip(arr[..., i] * (0.45 + 0.55 * t[i]) + 90 * t[i] * 0.5, 0, 255)
    bf = Image.fromarray(arr.astype(np.uint8))
    # 贴图坐标强制收敛到安全边距内，避免被画布边缘裁切
    px = int(round(cx - w / 2))
    py = int(round(cy - h / 2))
    px = max(margin, min(px, iw - int(w) - margin))
    py = max(margin, min(py, ih - h - margin))
    # 发光
    glow = bf.filter(ImageFilter.GaussianBlur(w * 0.10))
    img.alpha_composite(glow, (px, py))
    img.alpha_composite(bf, (px, py))
    return img


def draw_crystal_ball(img, cx, cy, r):
    # 外发光
    img = add_glow(img, cx, cy, r * 2.5, (30, 120, 120), power=2.6)
    # 球体
    lay = Image.new("RGBA", (int(r * 3), int(r * 3)), (0, 0, 0, 0))
    c = r * 1.5
    d = ImageDraw.Draw(lay)
    d.ellipse([c - r, c - r, c + r, c + r], fill=(120, 235, 220, 60))
    lay = Image.fromarray(np.asarray(lay))
    img.alpha_composite(lay, (int(cx - c), int(cy - c)))

    # 内部径向渐变（青绿 -> 深蓝）
    size = (int(r * 2), int(r * 2))
    inner = np.zeros((size[1], size[0], 4), dtype=np.float32)
    yy, xx = np.mgrid[0:size[1], 0:size[0]]
    dist = np.sqrt((xx - size[0] / 2) ** 2 + (yy - size[1] / 2) ** 2) / r
    inside = np.clip(1 - dist, 0, 1)
    top = np.array([150, 245, 225], dtype=np.float32)
    bot = np.array([22, 46, 96], dtype=np.float32)
    t = np.clip((yy / size[1]), 0, 1)[..., None]
    grad = top[None, None, :] * (1 - t) + bot[None, None, :] * t
    inner[..., :3] = grad
    inner[..., 3] = (inside ** 0.55) * 245
    ball = Image.fromarray(np.clip(inner, 0, 255).astype(np.uint8))
    ball = ball.filter(ImageFilter.GaussianBlur(r * 0.02))
    img.alpha_composite(ball, (int(cx - size[0] / 2), int(cy - size[1] / 2)))

    # 球内星尘
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(23)
    for _ in range(46):
        ang = rnd.uniform(0, math.tau)
        rr = r * (rnd.random() ** 0.5) * 0.88
        x, y = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr
        s = rnd.choice([0.8, 1.0, 1.4, 1.9])
        a = int(90 + 120 * (1 - rr / r))
        d.ellipse([x - s, y - s, x + s, y + s], fill=(225, 255, 250, a))
    # 球面高光
    hl = Image.new("RGBA", (int(r * 2), int(r * 2)), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.ellipse([r * 0.28, r * 0.20, r * 1.05, r * 0.82], fill=(255, 255, 255, 40))
    hl = hl.filter(ImageFilter.GaussianBlur(r * 0.12))
    img.alpha_composite(hl, (int(cx - r), int(cy - r)))
    # 弧光（上沿）
    arc = Image.new("RGBA", (int(r * 2.6), int(r * 2.6)), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arc)
    c2 = r * 1.3
    ad.arc([c2 - r * 0.93, c2 - r * 0.93, c2 + r * 0.93, c2 + r * 0.93], 190, 340,
           fill=(235, 255, 250, 150), width=max(2, int(r * 0.045)))
    arc = arc.filter(ImageFilter.GaussianBlur(r * 0.03))
    img.alpha_composite(arc, (int(cx - c2), int(cy - c2)))
    # 轮廓
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(210, 252, 245, 120), width=max(2, int(r * 0.018)))
    return img


def draw_qr(img, url, cx, cy, box, pad=26, card=True):
    import qrcode
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    qimg = qr.make_image(fill_color=(10, 16, 34), back_color=(255, 255, 255)).convert("RGB")
    qimg = qimg.resize((box, box), Image.NEAREST)
    card_w = box + pad * 2
    card_h = box + pad * 2
    lay = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=int(box * 0.11), fill=(255, 255, 255, 255))
    lay.paste(qimg, (pad, pad))
    img.alpha_composite(lay, (int(cx - card_w / 2), int(cy - card_h / 2)))
    return img


def grain(img, amount=7.0, seed=5):
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    rng = np.random.default_rng(seed)
    n = rng.normal(0, amount, arr.shape[:2])[..., None]
    arr = np.clip(arr + n, 0, 255).astype(np.uint8)
    return Image.fromarray(arr).convert("RGBA")




def draw_orbit_ring(img, cx, cy, rx, ry, rot=-8, color=(198, 228, 234), alpha=130,
                    width=2, dotted=True, star_n=54, glow=0.30):
    """细线星轨环：倾斜椭圆、断续弧段 + 环上星点，非实心圆盘"""
    if glow:
        img = add_glow(img, cx, cy, max(rx, ry) * 1.25, (26, 74, 84), strength=glow, power=2.2,
                       aspect=ry / max(rx, 1e-6))
    size = int(max(rx, ry) * 2.9)
    c = size / 2.0
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    box = [c - rx, c - ry, c + rx, c + ry]
    if dotted:
        seg = 88
        for k in range(seg):
            if k % 4 == 3:
                continue
            a0 = 360.0 * k / seg
            a1 = a0 + 360.0 / seg * 0.58
            d.arc(box, a0, a1, fill=color + (alpha,), width=width)
        d.arc([c - rx + 1, c - ry + 1, c + rx - 1, c + ry - 1], 0, 360,
              fill=color + (max(26, alpha // 4),), width=1)
    else:
        d.arc(box, 0, 360, fill=color + (alpha,), width=width)
    rnd = random.Random(19)
    for _ in range(star_n):
        t = rnd.uniform(0, math.tau)
        x = c + math.cos(t) * rx
        y = c + math.sin(t) * ry
        r = rnd.choice([0.8, 1.1, 1.5, 2.0])
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (rnd.randint(90, 200),))
    lay = lay.rotate(rot, resample=Image.BICUBIC)
    img.alpha_composite(lay, (int(cx - c), int(cy - c)))
    return img


def draw_tarot_card(img, cx, cy, w=148, h=222):
    """塔罗牌背：深蓝卡面 + 双描金细边 + 八芒星与月牙纹样，微弱发光"""
    img = add_glow(img, cx, cy, w * 2.5, (30, 88, 96), strength=0.50, power=2.2)
    pad = 22
    LW, LH = int(w + pad * 2), int(h + pad * 2)
    lay = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0 = pad, pad
    x1, y1 = pad + w, pad + h
    r = int(w * 0.12)
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=(13, 26, 52, 252),
                        outline=(232, 212, 154, 225), width=3)
    d.rounded_rectangle([x0 + 7, y0 + 7, x1 - 7, y1 - 7], radius=int(r * 0.8),
                        outline=(152, 208, 212, 130), width=1)
    d.rounded_rectangle([x0 + 12, y0 + 12, x1 - 12, y1 - 12], radius=int(r * 0.7),
                        outline=(232, 212, 154, 90), width=1)
    ccx, ccy = (x0 + x1) / 2.0, (y0 + y1) / 2.0

    # 中央八芒星
    R1, R2 = w * 0.30, w * 0.115
    pts = []
    for k in range(16):
        ang = -math.pi / 2 + k * math.pi / 8
        rr = R1 if k % 2 == 0 else R2
        pts.append((ccx + math.cos(ang) * rr, ccy + math.sin(ang) * rr * 1.02))
    d.polygon(pts, fill=(236, 220, 162, 235))
    d.polygon([(ccx + (px - ccx) * 0.42, ccy + (py - ccy) * 0.42) for px, py in pts], fill=(20, 34, 60, 255))

    # 上方月牙
    mr = w * 0.20
    my = ccy - h * 0.30
    d.ellipse([ccx - mr, my - mr * 1.7, ccx + mr, my + mr * 0.30], outline=(240, 224, 168, 215), width=2)
    d.ellipse([ccx - mr * 0.30, my - mr * 1.62, ccx + mr * 1.70, my + mr * 0.24], fill=(13, 26, 52, 255))

    # 下方月牙（倒置对称）
    my2 = ccy + h * 0.30
    d.ellipse([ccx - mr, my2 - mr * 0.30, ccx + mr, my2 + mr * 1.70], outline=(240, 224, 168, 200), width=2)
    d.ellipse([ccx - mr * 0.30, my2 - mr * 0.24, ccx + mr * 1.70, my2 + mr * 1.62], fill=(13, 26, 52, 255))

    # 四角星点与分隔线
    d.line([(x0 + w * 0.18, y0 + h * 0.12), (x1 - w * 0.18, y0 + h * 0.12)], fill=(232, 212, 154, 110), width=1)
    d.line([(x0 + w * 0.18, y1 - h * 0.12), (x1 - w * 0.18, y1 - h * 0.12)], fill=(232, 212, 154, 110), width=1)
    rnd = random.Random(37)
    for _ in range(22):
        sx = rnd.uniform(x0 + w * 0.15, x1 - w * 0.15)
        sy = rnd.uniform(y0 + h * 0.14, y1 - h * 0.14)
        if abs(sx - ccx) < R1 * 0.75 and abs(sy - ccy) < R1 * 0.9:
            continue
        rr2 = rnd.choice([1.0, 1.4, 2.0])
        d.ellipse([sx - rr2, sy - rr2, sx + rr2, sy + rr2], fill=(238, 240, 214, rnd.randint(90, 200)))

    lay = lay.filter(ImageFilter.GaussianBlur(0.35))
    img.alpha_composite(lay, (int(cx - LW / 2), int(cy - LH / 2)))
    return img


def spiral_path(cx, cy, r0, r1, turns=1.3, n=7, yscale=1.0, start=-math.pi / 2):
    """自下而上的星尘螺旋：返回 n 个等间隔路径点 (x, y, 切向角)"""
    pts = []
    for i in range(n):
        t = i / float(max(n - 1, 1))
        ang = start + t * turns * math.tau
        r = r0 + (r1 - r0) * t
        x = cx + math.cos(ang) * r
        y = cy + math.sin(ang) * r * yscale
        pts.append((x, y, ang))
    return pts


def draw_stardust_spiral(img, cx, cy, r0, r1, turns=1.3, yscale=1.0, color=(176, 236, 232), seed=13):
    """星尘螺旋流：淡淡光带 + 沿线碎钻星尘"""
    pts = spiral_path(cx, cy, r0, r1, turns, n=190, yscale=yscale)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(len(pts) - 1):
        t = i / float(len(pts) - 1)
        a = int(18 + 80 * (1 - abs(t - 0.45) * 1.2))
        d.line([(pts[i][0], pts[i][1]), (pts[i + 1][0], pts[i + 1][1])],
               fill=color + (max(12, a),), width=3)
    ribbon = lay.filter(ImageFilter.GaussianBlur(7))
    img.alpha_composite(ribbon)
    img.alpha_composite(lay)
    rnd = random.Random(seed)
    for i in range(len(pts)):
        if rnd.random() < 0.42:
            continue
        t = i / float(len(pts) - 1)
        jitter = rnd.uniform(-5, 5)
        x = pts[i][0] + jitter
        y = pts[i][1] + jitter
        r = rnd.choice([0.9, 1.3, 1.8, 2.4])
        a = int(70 + 150 * (1 - t))
        ImageDraw.Draw(img, "RGBA").ellipse([x - r, y - r, x + r, y + r],
                                            fill=color + (min(235, a),))
    return img


def draw_stardust_curve(img, pts, color=(176, 236, 232), seed=13, width=5):
    """沿任意点列绘制星尘光带（淡淡拖尾 + 沿线碎钻星尘）"""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    n = len(pts)
    for i in range(n - 1):
        t = i / float(n - 1)
        a = int(30 + 120 * (1 - abs(t - 0.42) * 1.15))
        d.line([pts[i], pts[i + 1]], fill=color + (max(18, a),), width=width)
    halo = lay.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(halo)
    img.alpha_composite(halo)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))
    img.alpha_composite(lay)
    rnd = random.Random(seed)
    dd = ImageDraw.Draw(img, "RGBA")
    for i, (x, y) in enumerate(pts):
        if rnd.random() < 0.40:
            continue
        t = i / float(n - 1)
        a = int(70 + 155 * (1 - t * 0.55))
        r = rnd.choice([0.9, 1.3, 1.8, 2.5])
        jx, jy = rnd.uniform(-5, 5), rnd.uniform(-5, 5)
        dd.ellipse([x + jx - r, y + jy - r, x + jx + r, y + jy + r], fill=color + (min(238, a),))
    return img


def _rect_hit(a, b, gap=0.0):
    """矩形相交判断（gap 为额外安全间距）"""
    return not (a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])


def layout_flies(seed, obstacles, n=7, margin=16, gap=12):
    """随机摆放完整蝴蝶：避让星球/月亮/文字/二维码，蝶间留间距，并分格取样保证覆盖全画面（含中部）"""
    rnd = random.Random(seed)
    pool = [(170, 238), (154, 226), (140, 208), (124, 188), (110, 170), (98, 150), (88, 138)]
    cols, rows = 3, 4
    cells = [(c, r) for r in range(rows) for c in range(cols)]
    rnd.shuffle(cells)
    grid = {}
    out = []          # (bname, cx, cy, w, alpha, flip, rect)

    def try_place(box=None, attempts=2500):
        for _ in range(attempts):
            w, alpha = pool[rnd.randrange(len(pool))]
            bname = "fly_l.png" if rnd.random() < 0.5 else "fly_r.png"
            flip = rnd.random() < 0.5
            src = full_butterfly(os.path.join(ASSETS, bname))
            h = int(w * src.height / src.width)
            x0, x1 = margin + w / 2.0, W - margin - w / 2.0
            y0, y1 = margin + h / 2.0, H - margin - h / 2.0
            if box is not None:
                x0 = max(x0, box[0])
                x1 = min(x1, box[2])
                y0 = max(y0, box[1])
                y1 = min(y1, box[3])
                if x0 >= x1 or y0 >= y1:
                    return False
            cx = rnd.uniform(x0, x1)
            cy = rnd.uniform(y0, y1)
            rect = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            gx = min(cols - 1, int(cx / (W / cols)))
            gy = min(rows - 1, int(cy / (H / rows)))
            if grid.get((gx, gy), 0) >= 1:
                continue
            if any(_rect_hit(rect, ob, gap) for ob in obstacles):
                continue
            if any(_rect_hit(rect, o[6], gap) for o in out):
                continue
            grid[(gx, gy)] = grid.get((gx, gy), 0) + 1
            out.append((bname, cx, cy, w, alpha, flip, rect))
            return True
        return False

    for gi, (gx, gy) in enumerate(cells):
        if len(out) >= n:
            break
        box = (gx * W / cols, gy * H / rows, (gx + 1) * W / cols, (gy + 1) * H / rows)
        try_place(box)
    guard = 0
    while len(out) < n and guard < 40:
        guard += 1
        if not try_place(None):
            break
    return out


FLY_RATIO = 317.0 / 402.0
LAST = {}


def _fly_height(w):
    return w * FLY_RATIO


def place_fly(bname, cx, cy, w, alpha, flip, obstacles, placed, margin=14, gap=12):
    """按中心点安置一只完整蝴蝶；越界自动收敛，命中障碍返回 None"""
    h = _fly_height(w)
    cx = min(max(cx, margin + w / 2.0), W - margin - w / 2.0)
    cy = min(max(cy, margin + h / 2.0), H - margin - h / 2.0)
    rect = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
    if any(_rect_hit(rect, ob, gap) for ob in obstacles):
        return None
    if any(_rect_hit(rect, o[6], gap) for o in placed):
        return None
    return (bname, cx, cy, w, alpha, flip, rect)


def place_fly_fit(bname, cx, cy, w, alpha, flip, obstacles, placed, margin=14, gap=12):
    """尺寸自适应：命中障碍时按 8% 递减重试，最多 4 次，仍失败返回 None"""
    cur = w
    for _ in range(5):
        f = place_fly(bname, cx, cy, cur, alpha, flip, obstacles, placed, margin, gap)
        if f:
            return f
        cur *= 0.92
    return None


def stream_hit(rect, pts, gap=8):
    """蝴蝶矩形与星尘流采样点的最小间距检查"""
    for px, py in pts:
        if (rect[0] - gap) <= px <= (rect[2] + gap) and (rect[1] - gap) <= py <= (rect[3] + gap):
            return True
    return False


def build(variant="A", url="http://192.168.8.187:8765/"):
    variant = (variant or "A").upper()
    if variant not in ("A", "B", "C"):
        variant = "A"

    # 背景渐变
    yy = np.linspace(0, 1, H)[:, None]
    top = np.array([14, 22, 52], np.float32)
    mid = np.array([9, 26, 44], np.float32)
    bot = np.array([4, 6, 14], np.float32)
    grad = np.where(yy < 0.5, top * (1 - yy * 2) + mid * (yy * 2), mid * (1 - (yy - 0.5) * 2) + bot * ((yy - 0.5) * 2))
    arr = np.repeat(grad[:, None, :], W, axis=1)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr).convert("RGBA")

    # 大范围宇宙光雾
    img = add_glow(img, W * 0.5, H * 0.40, W * 0.72, (10, 46, 52), power=2.0, aspect=1.0)
    img = add_glow(img, W * 0.18, H * 0.22, W * 0.42, (14, 30, 66), power=2.0)
    img = add_glow(img, W * 0.85, H * 0.72, W * 0.40, (24, 16, 58), power=2.0)
    img = star_field(img, 300, 11)

    # 星球 / 月亮：三案一律保持原位不动
    if variant == "A":
        moon = (W * 0.862, H * 0.128, 44)
        planet = (W * 0.128, H * 0.110, 30)
    else:
        moon = (W * 0.846, H * 0.120, 50)
        planet = (W * 0.148, H * 0.104, 34)

    img = draw_planet(img, planet[0], planet[1], planet[2])
    img = draw_moon(img, moon[0], moon[1], moon[2])
    img = sparkle(img, W * 0.32, H * 0.115, 6)
    img = sparkle(img, W * 0.66, H * 0.300, 5)
    img = sparkle(img, W * 0.12, H * 0.585, 6)
    img = sparkle(img, W * 0.90, H * 0.470, 5)

    d = ImageDraw.Draw(img, "RGBA")
    title_f = font(F_TITLE, 64)
    sub_f = font(F_CN_L, 24)
    theme_f = font(F_CN, 46)
    small_f = font(F_CN_L, 22)

    y_title = int(H * 0.068)
    y_sub = y_title + 76
    y_theme = int(H * 0.230)
    y_small = y_theme + 68

    def metrics(txt, f, y, spacing=0):
        if spacing:
            total = sum(d.textlength(c, font=f) for c in txt) + spacing * (len(txt) - 1)
        else:
            total = d.textlength(txt, font=f)
        asc, desc = f.getmetrics()
        return ((W - total) / 2.0, y, (W + total) / 2.0, y + asc + desc)

    text_rects = [
        metrics("PPTAROT", title_f, y_title, 10),
        metrics("T A R O T   ·   A S T R O L O G Y", sub_f, y_sub, 2),
        metrics("每日运势 · 占星", theme_f, y_theme, 1),
        metrics("塔罗  ·  星盘  ·  每日运程指引", small_f, y_small),
    ]

    qr_box = 236
    qr_cy = int(H * 0.815)
    card = qr_box / 2.0 + 26 + 10

    base_obs = [
        (moon[0] - moon[2] * 1.7, moon[1] - moon[2] * 1.7, moon[0] + moon[2] * 1.7, moon[1] + moon[2] * 1.7),
        (planet[0] - planet[2] * 3.0, planet[1] - planet[2] * 1.8, planet[0] + planet[2] * 3.0, planet[1] + planet[2] * 1.8),
        (W / 2.0 - card, qr_cy - card, W / 2.0 + card, qr_cy + card),
    ] + [(a - 16, b - 16, c + 16, e + 16) for a, b, c, e in text_rects]

    hero = None
    center_obs = None
    flies = []
    stream_pts = []
    specs = []

    if variant == "A":
        # A 案：中央一只超大全蝶作主角，外圈一圈细线星轨环（非实心圆盘）
        ccx, ccy = W * 0.5, 604.0
        img = draw_orbit_ring(img, ccx, ccy, 272, 152, rot=-8, alpha=124, width=2, star_n=60)
        center_obs = (ccx - 272 - 10, ccy - 152 - 10, ccx + 272 + 10, ccy + 152 + 10)
        hero = ("fly_l.png", ccx, ccy, 292, 246, False)
        specs = [
            ("fly_r.png", 104, 880, 178, 238, True),
            ("fly_l.png", 630, 880, 176, 234, False),
            ("fly_r.png", 116, 1140, 104, 196, True),
            ("fly_l.png", 634, 1156, 100, 190, False),
            ("fly_l.png", 244, 252, 60, 208, True),
            ("fly_r.png", 506, 252, 60, 202, False),
        ]
    elif variant == "B":
        # B 案：中央细线黄道星轨环，环内嵌塔罗牌背；整体下移避免压住上方文案
        ccx, ccy = W * 0.5, 684.0
        img = draw_orbit_ring(img, ccx, ccy, 154, 224, rot=-12, alpha=142, width=2, star_n=76)
        img = draw_tarot_card(img, ccx, ccy, 148, 222)
        center_obs = (ccx - 154 - 8, ccy - 224 - 8, ccx + 154 + 8, ccy + 224 + 8)
        # 四周蝴蝶统一缩小并随机散落（58~118px），左右两列 × 四段分区保证分布均衡
        rnd = random.Random(2411)
        obs_all = base_obs + [center_obs]
        cols = [(36, 186), (W - 186, W - 36)]
        rows = [(430, 660), (660, 880), (880, 1070), (1070, 1215)]
        cells = []
        for c in cols:
            rr = rows[:]
            rnd.shuffle(rr)
            for r in rr:
                cells.append((c, r))
        for (x0, x1), (y0, y1) in cells:
            for _t in range(400):
                ww = rnd.choice([58, 66, 74, 82, 90, 98, 106, 114])
                cx = rnd.uniform(x0, x1)
                cy = rnd.uniform(y0, y1)
                f = place_fly("fly_r.png" if rnd.random() < 0.5 else "fly_l.png", cx, cy, ww,
                              rnd.choice([188, 198, 208, 216, 224]), rnd.random() < 0.5,
                              obs_all, flies, 18, 12)
                if f:
                    flies.append(f)
                    break
    else:
        # C 案：中央自下而上盘旋的星尘螺旋流，蝴蝶紧贴星流两侧排布
        y_bot, y_top = 1006.0, 424.0
        mid = []
        for i in range(151):
            t = i / 150.0
            y = y_bot + (y_top - y_bot) * t
            x = W * 0.5 + 122.0 * math.sin(2.55 * math.pi * t) * (0.52 + 0.48 * t)
            mid.append((x, y))
        ribbon = mid + [(x + 9, y) for x, y in reversed(mid)] + mid[:1]
        img = add_glow(img, W * 0.5, 700, 250, (14, 64, 70), strength=0.62, power=2.0, aspect=1.45)
        img = draw_stardust_curve(img, mid, width=6)
        img = draw_stardust_curve(img, [(x + 11, y) for x, y in mid], color=(150, 214, 216),
                                  seed=29, width=2)
        img = add_glow(img, W * 0.5, 950, 205, (16, 74, 80), strength=0.58, power=2.1, aspect=1.5)
        for frac in (0.04, 0.14, 0.26, 0.40, 0.54, 0.68, 0.82, 0.94):
            bx, by = mid[int(frac * (len(mid) - 1))]
            img = add_glow(img, bx, by, 52, (38, 140, 134), strength=0.60, power=2.4)
            img = sparkle(img, bx, by, 7)
        for k in range(9):
            sx = W * 0.5 + 150.0 * math.sin(k * 1.7) * (0.35 + 0.1 * (k % 3))
            sy = 880 + 62.0 * math.cos(k * 2.1) + 22.0 * (k % 2)
            img = sparkle(img, sx, sy, 5)
        stream_pts = mid
        center_obs = None

        sizes = [(224, 244), (196, 236), (168, 218), (140, 200), (118, 184), (100, 170), (90, 156)]
        targets = [0.46, 0.24, 0.64, 0.12, 0.80, 0.36, 0.92]
        for idx, (w, al) in enumerate(sizes):
            bname = "fly_l.png" if idx % 2 == 0 else "fly_r.png"
            found = None
            cur = w
            t0 = targets[idx] if idx < len(targets) else 0.5
            c0 = int(round(t0 * (len(mid) - 1)))
            seq = []
            for d in range(0, len(mid), 5):
                for i in (c0 - d, c0 + d):
                    if 2 <= i < len(mid) - 2 and i not in seq:
                        seq.append(i)
            for _try in range(3):
                for i in seq:
                    px, py = mid[i]
                    for side in (1, -1):
                        for extra in (16, 28, 44, 62, 84):
                            f = place_fly(bname, px + side * (cur / 2.0 + extra), py, cur, al,
                                          side < 0, base_obs, flies, 16, 12)
                            if not f or stream_hit(f[6], mid, 12):
                                continue
                            found = f
                            break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
                cur *= 0.90
            if found:
                flies.append(found)
            else:
                print("[warn] C 未安置 %s w=%s" % (bname, w))

        # 底部中心（星流末端与二维码之间）补两只小蝶，消除中下部空旷
        extras = [(W * 0.5 - 96, 962, 108, 176), (W * 0.5 + 94, 982, 98, 168)]
        for k, (ex, ey, ew, eal) in enumerate(extras):
            placed = None
            for dx in (0, -18, 18, -36, 36, -54, 54):
                for dy in (0, -16, 16, -30, 30):
                    f = place_fly("fly_r.png" if k % 2 else "fly_l.png", ex + dx, ey + dy, ew,
                                  eal, k % 2 == 1, base_obs, flies, 16, 12)
                    if f and not stream_hit(f[6], mid, 12):
                        placed = f
                        break
                if placed:
                    break
            if placed:
                flies.append(placed)

    # 主角大蝶（A 案）
    if hero:
        hb, hx, hy, hw, ha, hflip = hero
        hh = _fly_height(hw)
        hero_rect = (hx - hw / 2.0, hy - hh / 2.0, hx + hw / 2.0, hy + hh / 2.0)
        hero = (hb, hx, hy, hw, ha, hflip, hero_rect)

    lay_obs = base_obs + ([center_obs] if center_obs else [])
    for bname, fx, fy, fw, fa, fflip in specs:
        f = place_fly_fit(bname, fx, fy, fw, fa, fflip, lay_obs, flies)
        if f and stream_pts and stream_hit(f[6], stream_pts, 10):
            f = None
        if f:
            flies.append(f)
        else:
            print("[warn] %s 未安置 %s w=%s" % (variant, bname, fw))

    # 光晕：最大两只 + 主角
    glow_list = list(flies)
    if hero:
        glow_list.append(hero)
    for fl in sorted(glow_list, key=lambda t: -t[3])[:3]:
        img = add_glow(img, int(fl[1]), int(fl[2]), int(fl[3] * 1.35), (44, 148, 138), strength=0.44, power=2.2)

    for bname, fx, fy, fw, fa, fflip, _r in flies:
        img = draw_butterfly(img, os.path.join(ASSETS, bname), int(fx), int(fy), int(fw),
                             flip=fflip, alpha=fa)
    if hero:
        img = draw_butterfly(img, os.path.join(ASSETS, hero[0]), int(hero[1]), int(hero[2]),
                             int(hero[3]), flip=hero[5], alpha=hero[4])

    img = grain(img, 6.5)
    d = ImageDraw.Draw(img, "RGBA")

    def ctext(y, txt, f, fill, spacing=0):
        if spacing:
            widths = [d.textlength(ch, font=f) for ch in txt]
            total = sum(widths) + spacing * (len(txt) - 1)
            x = (W - total) / 2
            for ch, w in zip(txt, widths):
                d.text((x, y), ch, font=f, fill=fill)
                x += w + spacing
        else:
            w = d.textlength(txt, font=f)
            d.text(((W - w) / 2, y), txt, font=f, fill=fill)

    ctext(y_title, "PPTAROT", title_f, (243, 233, 205, 252), spacing=10)
    ctext(y_sub, "T A R O T   ·   A S T R O L O G Y", sub_f, (168, 214, 219, 210), spacing=2)
    ctext(y_theme, "每日运势 · 占星", theme_f, (238, 245, 250, 245), spacing=1)
    ctext(y_small, "塔罗  ·  星盘  ·  每日运程指引", small_f, (150, 200, 208, 205))

    img = draw_qr(img, url, W // 2, qr_cy, qr_box, pad=26)
    img = add_glow(img, W // 2, qr_cy, qr_box * 1.5, (40, 90, 86), strength=0.55, power=2.4)

    LAST.clear()
    LAST.update({
        "variant": variant,
        "flies": [t[:6] + (t[6],) for t in flies] + ([hero] if hero else []),
        "hero": hero,
        "center_box": center_obs,
        "text_rects": text_rects,
        "qr": (W / 2.0 - card, qr_cy - card, W / 2.0 + card, qr_cy + card),
        "moon": (moon[0] - moon[2] * 1.7, moon[1] - moon[2] * 1.7, moon[0] + moon[2] * 1.7, moon[1] + moon[2] * 1.7),
        "planet": (planet[0] - planet[2] * 3.0, planet[1] - planet[2] * 1.8, planet[0] + planet[2] * 3.0, planet[1] + planet[2] * 1.8),
        "stream": stream_pts,
    })
    return img.convert("RGB")


def default_url(port=8765):
    """探测本机局域网 IP，拼出扫码落地地址（可用环境变量 PPTAROT_PUBLIC_URL 覆盖为正式域名）"""
    import os, socket
    env = (os.environ.get("PPTAROT_PUBLIC_URL") or "").strip()
    if env:
        return env if env.endswith("/") else env + "/"
    ip = ""
    for target in (("8.8.8.8", 80), ("114.114.114.114", 53)):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.4)
            s.connect(target)
            cand = s.getsockname()[0]
            s.close()
            if cand and not cand.startswith(("127.", "169.254.")):
                ip = cand
                break
        except Exception:
            continue
    if not ip:
        ip = "192.168.8.187"
    return "http://%s:%d/" % (ip, port)


def poster_bytes(url=None, variant="B", fmt="JPEG"):
    """返回海报图片二进制，供 HTTP 接口直接输出"""
    if not url:
        url = default_url()
    im = build(variant, url)
    buf = io.BytesIO()
    im.save(buf, format=fmt, quality=92)
    return buf.getvalue()


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(BASE), "output")
    os.makedirs(out, exist_ok=True)
    ims = []
    for v in ("A", "B", "C"):
        im = build(v)
        p = os.path.join(out, "poster_%s.png" % v)
        im.save(p, quality=95)
        ims.append(im)
        print("saved", p, im.size)
        lay = LAST
        print("  %s flies=%d sizes=%s" % (v, len(lay["flies"]), sorted([round(t[3]) for t in lay["flies"]], reverse=True)))
    gap = 24
    cw = W * 3 + gap * 4
    ch = H + gap * 2
    canvas = Image.new("RGB", (cw, ch), (8, 10, 16))
    for i, im in enumerate(ims):
        canvas.paste(im, (gap * (i + 1) + W * i, gap))
    cp = os.path.join(out, "poster_compare_ABC.jpg")
    canvas.save(cp, quality=92)
    print("saved", cp, canvas.size)
