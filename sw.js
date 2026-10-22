/* Service worker : coquille en cache, éditions en « réseau d'abord » avec repli hors ligne */
const V='veille-pv-v2';
const SHELL=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const req=e.request;if(req.method!=='GET')return;
  const url=new URL(req.url);
  const fonts=/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if(url.origin!==location.origin&&!fonts)return;
  if(fonts){ // cache d'abord
    e.respondWith(caches.match(req).then(r=>r||fetch(req).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put(req,cp));return res;})));
    return;
  }
  // réseau d'abord (éditions toujours à jour), cache en secours
  e.respondWith(fetch(req).then(res=>{if(res.ok){const cp=res.clone();caches.open(V).then(c=>c.put(req,cp));}return res;})
    .catch(()=>caches.match(req,{ignoreSearch:true}).then(r=>r||(req.mode==='navigate'?caches.match('index.html'):undefined))));
});
