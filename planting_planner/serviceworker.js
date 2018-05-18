//This is the "Offline copy of pages" wervice worker
// Source:  https://www.pwabuilder.com/serviceworker
var cacheName = 'lauzeplan-offline';
//Install stage sets up the offline page in the cahche and opens a new cache
self.addEventListener('install', function(event) {
  var offlinePage = new Request('offline');
  event.waitUntil(
  fetch(offlinePage).then(function(response) {
    return caches.open(cacheName).then(function(cache) {
      console.log('[PWA Builder] Cached offline page during Install'+ response.url);
      return cache.put(offlinePage, response);
    });
  }));
});

//If any fetch fails, it will show the offline page.
//Maybe this should be limited to HTML documents?
self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request).catch(function(error) {
        console.error( '[PWA Builder] Network request Failed. Serving offline page ' + error );
        return caches.open(cacheName).then(function(cache) {
          return cache.match('offline');
      });
    }));
});

//This is a event that can be fired from your page to tell the SW to update the offline page
self.addEventListener('refreshOffline', function(response) {
  return caches.open(cacheName).then(function(cache) {
    console.log('[PWA Builder] Offline page updated from refreshOffline event: '+ response.url);
    return cache.put(offlinePage, response);
  });
});