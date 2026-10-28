---
layout: null
sitemap: false
---
/* Offline support for avinashgosavi.com (registered from _layouts/default.html).
   - Pages: network first, always. A copy of each page you open is kept on this
     device (newest 40) and shown only when the network fails; otherwise /offline/.
   - Stylesheet + fonts: served from cache when present (style.css is
     content-hashed, fonts never change), fetched and cached otherwise. Fonts
     live in their own cache that survives deploys. A saved page names the
     style.css?v= of the day it was saved; once a deploy has replaced that
     file, offline it gets the current stylesheet instead of none.
   - A saved page served offline is marked <html data-saved-copy="<date>"> so
     the page can say it's a saved copy (script in _layouts/default.html).
   - Post images (/assets/images/): the copy on this device is shown at once and
     refreshed in the background (newest 60 kept), so saved posts keep their
     photos and diagrams offline.
   - Nothing else is touched: feeds, JSON, analytics go straight to the network.
   Kill switch: replace this file's body with
     self.addEventListener('install', () => self.skipWaiting());
     self.addEventListener('activate', () => self.registration.unregister());
*/
const BUILD = '{{ site.time | date: "%s" }}';
const STATIC = 'static-' + BUILD;
const FONTS = 'fonts-v1';
const PAGES = 'pages-v1';
const MAX_PAGES = 40;
const IMAGES = 'images-v1';
const MAX_IMAGES = 60;
const OFFLINE = '{{ "/offline/" | relative_url }}';
const PRECACHE = [
  OFFLINE,
  '{{ "/assets/css/style.css" | asset_version | relative_url }}',
  '{{ "/assets/fonts/dm-sans-latin-wght-normal.woff2" | relative_url }}'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC)
      .then((c) => c.addAll(PRECACHE.map((u) => new Request(u, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k.startsWith('static-') && k !== STATIC).map((k) => caches.delete(k)));
    if (self.registration.navigationPreload) {
      try { await self.registration.navigationPreload.enable(); } catch (e) {}
    }
    await self.clients.claim();
  })());
});

function pageKey(url) {
  return new Request(url.origin + url.pathname);
}

async function trim(name, max) {
  const c = await caches.open(name);
  const keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}

async function trimPages() {
  await trim(PAGES, MAX_PAGES);
}

async function handlePage(event, url) {
  try {
    const res = (await event.preloadResponse) || (await fetch(event.request));
    const type = res.headers.get('content-type') || '';
    if (res.ok && res.type === 'basic' && type.includes('text/html') && url.pathname !== OFFLINE) {
      const copy = res.clone();
      event.waitUntil((async () => {
        const c = await caches.open(PAGES);
        const key = pageKey(url);
        await c.delete(key); // re-insert so the newest visit sits at the end
        await c.put(key, copy);
        await trimPages();
      })());
    }
    return res;
  } catch (err) {
    const saved = await caches.match(pageKey(url), { cacheName: PAGES });
    if (saved) return markSaved(saved);
    const fallback = await caches.match(OFFLINE);
    if (fallback) return fallback;
    throw err;
  }
}

// Tag a saved page so its own script can show "you're reading the saved copy".
async function markSaved(res) {
  try {
    const when = (res.headers.get('date') || '').replace(/[^\w ,:+-]/g, '');
    const html = (await res.clone().text()).replace('<html lang="en"', '<html lang="en" data-saved-copy="' + when + '"');
    const headers = new Headers(res.headers);
    headers.delete('content-length');
    return new Response(html, { status: res.status, statusText: res.statusText, headers });
  } catch (e) {
    return res;
  }
}

async function handleStatic(request, cacheName) {
  const hit = await caches.match(request);
  if (hit) return hit;
  try {
    const res = await fetch(request);
    if (res.ok && res.type === 'basic') {
      const copy = res.clone();
      caches.open(cacheName).then((c) => c.put(request, copy));
    }
    return res;
  } catch (err) {
    // Offline, and this exact ?v= is gone (an older saved page): use the current stylesheet.
    const any = await caches.match(request, { ignoreSearch: true });
    if (any) return any;
    throw err;
  }
}

async function handleImage(event, request) {
  const key = new Request(request.url.split('#')[0]);
  const hit = await caches.match(key, { cacheName: IMAGES });
  const refresh = fetch(request).then((res) => {
    if (res.ok && res.type === 'basic' && res.status === 200) {
      const copy = res.clone();
      event.waitUntil((async () => {
        const c = await caches.open(IMAGES);
        await c.delete(key); // re-insert so recently used images sit at the end
        await c.put(key, copy);
        await trim(IMAGES, MAX_IMAGES);
      })().catch(() => {}));
    }
    return res;
  });
  if (hit) {
    event.waitUntil(refresh.catch(() => {}));
    return hit;
  }
  return refresh;
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (req.mode === 'navigate') {
    event.respondWith(handlePage(event, url));
  } else if (url.pathname.startsWith('/assets/fonts/')) {
    event.respondWith(handleStatic(req, FONTS));
  } else if (url.pathname.startsWith('/assets/css/')) {
    event.respondWith(handleStatic(req, STATIC));
  } else if (url.pathname.startsWith('/assets/images/') && !req.headers.has('range')) {
    event.respondWith(handleImage(event, req));
  }
});
