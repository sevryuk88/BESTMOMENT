document.addEventListener("DOMContentLoaded", function () {
  const subscribeForm = document.getElementById("webpush-subscribe-form");
  const subscribeBtn = document.getElementById("webpush-subscribe-btn");

  // Функция преобразования VAPID ключа из base64 в Uint8Array
  function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, "+")
      .replace(/_/g, "/");

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  if (subscribeForm) {
    subscribeForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      if (!("serviceWorker" in navigator)) {
        alert("Service workers не поддерживаются в этом браузере");
        return;
      }

      try {
        const registration = await navigator.serviceWorker.register("/static/js/service-worker.js");

        const applicationServerKey = urlBase64ToUint8Array(window.vapidPublicKey);

        const subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: applicationServerKey
        });

        const subscriptionData = subscription.toJSON();  // ← важно!

        const response = await fetch("/webpush/subscribe/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrfToken
          },
          body: JSON.stringify({
            subscription: subscriptionData,
            group: "new_videos_" + subscribeBtn.dataset.username
          })
        });

        if (response.ok) {
          subscribeBtn.innerText = "✅ Подписка активна";
          subscribeBtn.disabled = true;
        } else {
          alert("Ошибка при подписке на уведомления.");
        }
      } catch (error) {
        console.error("Ошибка подписки:", error);
        alert("Не удалось подписаться на уведомления.");
      }
    });
  }
});
