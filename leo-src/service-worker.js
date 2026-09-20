/* App-shell only. Never cache API traffic, credentials, recordings or user documents. */
const CACHE='leo-studio-__BUILD__';
const base=new URL('./',self.location.href);
const shell=['index.html','manifest.webmanifest','leo-icon.svg'].map(p=>new URL(p,base).href);
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(shell))));
self.addEventListener('message',e=>{if(e.data?.type==='LEO_ACTIVATE')self.skipWaiting();});
self.addEventListener('activate',e=>e.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('leo-studio-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();})()));
self.addEventListener('fetch',e=>{
 const request=e.request,url=new URL(request.url);
 if(request.method!=='GET'||url.origin!==base.origin)return;
 const isEntry=url.href===base.href||url.pathname===new URL('index.html',base).pathname;
 if(request.mode==='navigate'&&isEntry){e.respondWith(fetch(request).catch(()=>caches.open(CACHE).then(c=>c.match(shell[0]))));return;}
 if(!shell.includes(url.href))return;
 e.respondWith(caches.open(CACHE).then(async cache=>(await cache.match(request))||fetch(request)));
});
