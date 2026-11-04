from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def font(sz): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", sz)
def icon(S, label, sub=None, maskable=False):
    W = S * 4
    im = Image.new("RGBA", (W, W), (20, 13, 9, 255)); d = ImageDraw.Draw(im)
    for r in range(W // 2, 0, -4):
        t = r / (W / 2); k = (1 - t) ** 2.2
        d.ellipse((W/2 - r*1.25, W*0.42 - r*1.25, W/2 + r*1.25, W*0.42 + r*1.25), fill=(int(20 + 140*k), int(13 + 60*k), int(9 + 24*k), 255))
    sc = 0.62 if maskable else 0.78
    cw = W * sc * 0.62; cx = W / 2; top = W * (0.31 if maskable else 0.27); ch = cw * 0.56
    pts = [(cx - cw/2 + cw*0.04, top + ch), (cx - cw/2, top + ch*0.2), (cx - cw/2 + cw*0.24, top + ch*0.52), (cx, top),
           (cx + cw/2 - cw*0.24, top + ch*0.52), (cx + cw/2, top + ch*0.2), (cx + cw/2 - cw*0.04, top + ch)]
    lw = int(W * 0.028)
    glow = Image.new("RGBA", (W, W), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.line(pts + [pts[0]], fill=(247, 216, 134, 150), width=lw * 3, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(W * 0.02)); im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    d.polygon(pts, fill=(28, 18, 12, 255))
    # ouro com degradê: linha escura + linha clara deslocada
    d.line(pts + [pts[0]], fill=(176, 120, 30, 255), width=lw, joint="curve")
    d.line(pts + [pts[0]], fill=(247, 210, 110, 255), width=int(lw * 0.6), joint="curve")
    d.line((pts[0][0] + cw*0.03, top + ch*0.8, pts[-1][0] - cw*0.03, top + ch*0.8), fill=(247, 216, 134, 230), width=int(lw * 0.55))
    for i, fx in enumerate((0.3, 0.5, 0.7)):
        x = pts[0][0] + (pts[-1][0] - pts[0][0]) * fx; y = top + ch * 0.62; r = lw * (0.45 if i != 1 else 0.6)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 244, 200, 255))
    for (x, y) in [pts[1], pts[3], pts[5]]:
        g = cw * 0.075; y = y - g * 0.55
        poly = [(x - g, y - g*0.3), (x - g*0.52, y - g), (x + g*0.52, y - g), (x + g, y - g*0.3), (x, y + g*1.05)]
        gl = Image.new("RGBA", (W, W), (0, 0, 0, 0)); ImageDraw.Draw(gl).polygon(poly, fill=(200, 238, 255, 210))
        gl = gl.filter(ImageFilter.GaussianBlur(W * 0.014)); im.alpha_composite(gl)
        d = ImageDraw.Draw(im); d.polygon(poly, fill=(214, 241, 255, 255), outline=(255, 255, 255, 255))
        d.polygon([(x - g, y - g*0.3), (x - g*0.52, y - g), (x - g*0.26, y - g*0.3)], fill=(255, 255, 255, 255))
        w2 = max(1, int(W * 0.004))
        d.line((x - g, y - g*0.3, x + g, y - g*0.3), fill=(140, 200, 235, 255), width=w2)
        d.line((x - g*0.26, y - g*0.3, x, y + g*1.05, x + g*0.26, y - g*0.3), fill=(140, 200, 235, 255), width=w2)
    f = font(int(W * (0.12 if maskable else 0.15))); tw = d.textlength(label, font=f); ty = top + ch + W * 0.07
    d.text((cx - tw/2, ty), label, font=f, fill=(255, 245, 232, 255))
    if sub:
        f2 = font(int(W * (0.062 if maskable else 0.075))); tw2 = d.textlength(sub, font=f2)
        d.text((cx - tw2/2, ty + W * (0.14 if maskable else 0.17)), sub, font=f2, fill=(247, 216, 134, 255))
    return im.resize((S, S), Image.LANCZOS)
for name, lab, sub in [("app", "Cotrim", "TRANÇAS"), ("adm", "Cotrim", "PAINEL ADM")]:
    icon(512, lab, sub).convert("RGB").save(f"{name}-512.png", optimize=True)
    icon(192, lab, sub).convert("RGB").save(f"{name}-192.png", optimize=True)
    icon(512, lab, sub, maskable=True).convert("RGB").save(f"{name}-maskable-512.png", optimize=True)
    icon(180, lab, sub).convert("RGB").save(f"{name}-apple-180.png", optimize=True)
a = Image.open("app-512.png"); b = Image.open("adm-maskable-512.png")
c = Image.new("RGB", (1034, 512), "white"); c.paste(a, (0, 0)); c.paste(b, (522, 0)); c.save("preview.jpg")
