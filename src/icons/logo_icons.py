"""Ícones do app a partir do logo circular do Cotrim Studio."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1]
CX, CY, R = 450, 470, 353          # círculo do logo na foto original
BG = (11, 8, 6)

src = Image.open(SRC).convert("RGB")
logo = src.crop((CX - R, CY - R, CX + R, CY + R))
D = logo.size[0]
mask = Image.new("L", (D * 4, D * 4), 0)
ImageDraw.Draw(mask).ellipse((0, 0, D * 4 - 1, D * 4 - 1), fill=255)
mask = mask.resize((D, D), Image.LANCZOS)
logo_rgba = logo.copy(); logo_rgba.putalpha(mask)
logo_rgba.save("logo-circle.png", optimize=True)

def badge(im, text):
    S = im.size[0]; d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(S * 0.072))
    tw = d.textlength(text, font=f); h = S * 0.11; w = tw + S * 0.08
    x1 = S * 0.975; y1 = S * 0.975; x0 = x1 - w; y0 = y1 - h
    d.rounded_rectangle((x0, y0, x1, y1), radius=h / 2, fill=(232, 180, 67), outline=(255, 236, 180), width=max(1, S // 128))
    d.text((x0 + (w - tw) / 2, y0 + h * 0.14), text, font=f, fill=(20, 13, 9))
    return im

def icon(S, scale, adm=False):
    im = Image.new("RGB", (S, S), BG)
    size = int(S * scale); l = logo_rgba.resize((size, size), Image.LANCZOS)
    im.paste(l, ((S - size) // 2, (S - size) // 2), l)
    return badge(im, "ADM") if adm else im

for kind, adm in (("app", False), ("adm", True)):
    icon(512, 0.98, adm).save(f"{kind}-512.png", optimize=True)
    icon(192, 0.98, adm).save(f"{kind}-192.png", optimize=True)
    icon(180, 0.98, adm).save(f"{kind}-apple-180.png", optimize=True)
    icon(512, 0.84, adm).save(f"{kind}-maskable-512.png", optimize=True)
    icon(48, 1.0, False).save(f"{kind}-48.png", optimize=True)

a = Image.open("app-512.png"); b = Image.open("adm-512.png"); m = Image.open("app-maskable-512.png")
prev = Image.new("RGB", (512 * 3 + 40, 512), "white")
prev.paste(a, (0, 0)); prev.paste(b, (532, 0))
# simula o recorte redondo que o Android faz no ícone adaptável
mm = Image.new("L", (512, 512), 0); ImageDraw.Draw(mm).ellipse((26, 26, 486, 486), fill=255)
prev.paste(m, (1064, 0), mm)
prev.save("preview.jpg", quality=90)
