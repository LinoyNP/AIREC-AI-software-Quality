// service_worker.js
const ASSETS = [
  '/',            // ודא שהשרת מחזיר את index.html לשורש
  '/index.html',
  'static/manifest.json'
];
self.addEventListener('install', event => {
  console.log('Service Worker installed');
});

self.addEventListener('activate', event => {
  console.log('Service Worker activated');
});
