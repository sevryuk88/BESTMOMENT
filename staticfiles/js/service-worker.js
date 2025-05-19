self.addEventListener("push", function(event) {
  const data = event.data.json();
  const title = data.title || "Новое уведомление";
  const options = {
    body: data.body,
    icon: "/static/img/icons/bell.png",
    data: data.url
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener("notificationclick", function(event) {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data)
  );
});
