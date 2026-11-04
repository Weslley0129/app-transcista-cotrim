import json
SKEL='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>\n'
HEAD='''<title>Cotrim Tranças</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yeseva+One&family=Yellowtail&family=Outfit:wght@400;500;600;700&family=Lexend:wght@600;700&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js"></script>
'''
BODY='''<div class="app" id="app"></div>
<div class="tabbar"><nav id="tabs" aria-label="Navegação principal"></nav></div>
<div id="toast" class="toast" hidden></div>
<script>(function(){function show(m){if(window.__appOk)return;var a=document.getElementById("app");if(!a||document.getElementById("fail"))return;var d=document.createElement("div");d.id="fail";d.setAttribute("style","margin:16px 0;padding:16px;border-radius:16px;background:#1A120D;border:2px solid #E8B443;font:15px/1.5 system-ui,sans-serif;color:#FBF2E4");d.innerHTML='<b>Não foi possível abrir o app neste navegador.</b><br>Abra o link no Chrome ou no Safari, ou atualize o navegador do celular.<br><small>Detalhe: '+String(m).replace(/[<>&]/g,"")+'</small>';a.insertBefore(d,a.firstChild)}window.addEventListener("error",function(e){show(e.message||"erro de script")});setTimeout(function(){show("o app não iniciou")},6000)})();</script>
'''
css=open('style.css').read()
js=open('app.js').read()
img=open('img.json').read()
page=json.dumps({"skel":SKEL,"head":HEAD,"body":BODY},ensure_ascii=True).replace('</','<\\/')
js=js.replace('__IMG__',img).replace('__PAGE__',page)
cfg={"marca":"Cotrim Tranças","trancista":"Aline","wa":"5511954547431","cidade":"","pixTipo":"email","pixChave":"Cotrim2294@outlook.com","sinalPct":30,"precos":{"box":0,"nago":0,"masc":0,"infantil":0},"diasAtende":[0,6],"fechados":["2026-12-12"],"aberturas":[{"mes":"2026-12","abre":"2026-11-20"}],"tolerancia":10,"avisoDias":2}
out=HEAD+'<style id="main-css">'+css+'</style>\n'+BODY+'\n<script id="cfg-data" type="application/json">'+json.dumps(cfg,ensure_ascii=False)+'</script>\n<script id="dep-data" type="application/json">[]</script>\n<script id="main-js">'+js+'</script>\n'
open('index.html','w').write(out)
print(len(out))
