// service_worker.js
const CACHE_NAME = 'quality-code-model';
//The elements that will be in cache
const ASSETS = [
  '/',           
  '/templates/index.html',
  '/static/manifest.json',
  '/static/script.js',
  '/static/style.css',
  '/static/Airec.png',
  '/static/icons/Airec-192x192.png'

];
// self.addEventListener('install', event => {
//     console.log('Service Worker installed');
//     event.waitUntil(
//     caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)) //open caching and store
//     );
// });
self.addEventListener('install', event => {
  console.log('Service Worker installed');
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of ASSETS) {
        try {
          const response = await fetch(asset);
          if (response.ok) {
            await cache.put(asset, response);
          } else {
            console.warn(`Skipping ${asset}: Response not OK`);
          }
        } catch (err) {
          console.error(`Failed to fetch ${asset}:`, err);
        }
      }
    })
  );
  self.skipWaiting(); //The new service worker does not wait for the old version, but goes into action immediately.
});


self.addEventListener('activate', event => {
  console.log('Service Worker activated');
});

//Fetch events - any network request that comes from the page.
//When receive the request (event.request), if the response exists in the cache it will be returned from there, otherwise a response from the fetch will be returned to the network.
self.addEventListener('fetch', event => {
    console.log(event);
    event.respondWith(
    caches.match(event.request).then((cached) => {
        return cached || fetch(event.request);
    })
  );
});
