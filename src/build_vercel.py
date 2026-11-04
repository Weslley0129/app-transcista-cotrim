import json, os, re, shutil, sys
from PIL import Image
BASE = sys.argv[1] if len(sys.argv)>1 else "https://cotrim-trancas.vercel.app"
OUT = "dist"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT+"/img"); os.makedirs(OUT+"/painel")
# fotos como arquivos
for n,k in [('p2','nago'),('p3','infantil'),('p4','box'),('p5','masc')]:
    im=Image.open('/mnt/user-data/uploads/'+n+'.jpeg').convert('RGB'); w,h=im.size
    g=im.convert('L'); rows=[sum(g.crop((0,y,w,y+1)).getdata())/w for y in range(h)]
    top=next(y for y in range(h) if rows[y]>18); bot=h-next(y for y in range(h) if rows[h-1-y]>18)
    im=im.crop((0,top,w,bot)); im.thumbnail((900,900)); im.save(f'{OUT}/img/{k}.jpg','JPEG',quality=78,optimize=True,progressive=True)
# imagem de prévia para o WhatsApp (1200x630)
src=Image.open(f'{OUT}/img/box.jpg'); og=Image.new('RGB',(1200,630),(181,83,42))
s2=src.copy(); s2.thumbnail((630,630)); og.paste(s2,(1200-s2.width,0))
from PIL import ImageDraw, ImageFont
d=ImageDraw.Draw(og)
def font(sz):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f,sz)
    return ImageFont.load_default()
d.rectangle((0,0,560,630),fill=(20,13,9))
for x in range(0,560,55):
    d.rectangle((x,600,x+16,612),fill=(232,180,67)); d.rectangle((x+20,600,x+32,612),fill=(201,206,214)); d.rectangle((x+36,600,x+42,612),fill=(247,216,134))
d.text((50,170),"Cotrim",font=font(84),fill=(255,245,232)); d.text((50,265),"Tranças",font=font(84),fill=(247,216,134))
d.text((52,390),"Box braids · Nagô · Masculino · Infantil",font=font(24),fill=(246,214,186))
d.text((52,430),"Agende o seu horário",font=font(30),fill=(232,180,67))
og.save(f'{OUT}/og.jpg','JPEG',quality=82)

css=open('style.css').read(); js=open('app.js').read()
cfg=json.loads(re.search(r'cfg=(\{.*?\})\nout=',open('build.py').read(),re.S).group(1))
IMG={k:f"/img/{k}.jpg" for k in ["nago","infantil","box","masc"]}; IMG["quasar"]="/img/quasartcode.png"; shutil.copy("quasartcode-logo.png",OUT+"/img/quasartcode.png")
js=js.replace('__IMG__',json.dumps(IMG)).replace('__PAGE__','{}')
RESET=':root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}'
SB={"url":"https://oqjmjavnyfjdpezjelht.supabase.co","key":"sb_publishable_kNPbFEl2_f70YY6tYOyJ0g_X49hPwfe"}
FAIL='''<script>(function(){function show(m){if(window.__appOk)return;var a=document.getElementById("app");if(!a||document.getElementById("fail"))return;var d=document.createElement("div");d.id="fail";d.setAttribute("style","margin:16px 0;padding:16px;border-radius:16px;background:#140D09;border:2px solid #E8B443;font:15px/1.5 system-ui,sans-serif;color:#FFF5E8");d.innerHTML='<b>Não foi possível abrir o app neste navegador.</b><br>Abra o link no Chrome ou no Safari, ou atualize o navegador do celular. Para agendar, chame no WhatsApp: <b>(11) 95454-7431</b>.';a.insertBefore(d,a.firstChild)}window.addEventListener("error",function(e){show(e.message||"erro")});setTimeout(function(){show("timeout")},8000)})();</script>'''
def page(mode,title,desc,robots,url):
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#B5532A">
<meta name="author" content="QuasarTcode"><link rel="author" href="https://www.quasartcode.com.br">
{'<meta name="robots" content="noindex,nofollow">' if robots else ''}
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 46 30'%3E%3Cpath d='M4 25 2 7l11 8 10-13 10 13 11-8-2 18z' fill='%23E8B443'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yeseva+One&family=Yellowtail&family=Outfit:wght@400;500;600;700&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>
<style>{RESET}</style>
<style id="main-css">{css}</style>
</head><body>
<div class="app" id="app"></div>
<div class="tabbar"><nav id="tabs" aria-label="Navegação principal"></nav></div>
<div id="toast" class="toast" hidden></div>
{FAIL}
<script>window.APP_MODE="{mode}";window.SB_CFG={json.dumps(SB)};window.APP_LINKS={{app:"/",painel:location.origin+"/painel"}};</script>
<script id="cfg-data" type="application/json">{json.dumps(cfg,ensure_ascii=False)}</script>
<script id="dep-data" type="application/json">[]</script>
<script id="main-js">{js}</script>
</body></html>
'''
open(f'{OUT}/index.html','w').write(page("cliente","Cotrim Tranças","Tranças com a Aline: box braids, nagô, masculino e infantil. Veja os modelos e agende o seu horário.",False,BASE+"/"))
open(f'{OUT}/painel/index.html','w').write(page("painel","Painel · Cotrim Tranças","Painel da trancista.",True,BASE+"/painel"))
json.dump({"cleanUrls":True,"trailingSlash":False,"headers":[{"source":"/painel","headers":[{"key":"X-Robots-Tag","value":"noindex"}]}]},open(f'{OUT}/vercel.json','w'))
for r,_,fs in os.walk(OUT):
    for f in fs: print(os.path.join(r,f), os.path.getsize(os.path.join(r,f)))
