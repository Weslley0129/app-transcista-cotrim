/* Cotrim Tranças: cache para abrir rápido e funcionar com internet fraca */
const V="cotrim-20261104182357-adm";
const CORE=["/", "/img/icon-adm-192.png", "/img/icon-adm-512.png", "/img/icon-adm-apple-180.png", "/img/icon-adm-maskable-512.png", "/img/quasartcode.png"];
self.addEventListener("install",e=>{ self.skipWaiting(); e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).catch(()=>{})); });
self.addEventListener("activate",e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim())); });
self.addEventListener("fetch",e=>{
  const r=e.request; if(r.method!=="GET") return;
  const u=new URL(r.url);
  if(u.origin!==location.origin){
    if(/cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net|fonts\.googleapis\.com|fonts\.gstatic\.com/.test(u.host))
      e.respondWith(caches.open(V).then(c=>c.match(r).then(m=>m||fetch(r).then(res=>{ if(res.ok||res.type==="opaque") c.put(r,res.clone()); return res; }))));
    return;
  }
  if(r.mode==="navigate"){
    e.respondWith(fetch(r).then(res=>{ const cp=res.clone(); caches.open(V).then(c=>c.put("/",cp)); return res; }).catch(()=>caches.match("/")));
    return;
  }
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{ if(res.ok){ const cp=res.clone(); caches.open(V).then(c=>c.put(r,cp)); } return res; })));
});
