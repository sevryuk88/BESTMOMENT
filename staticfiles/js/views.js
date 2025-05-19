document.addEventListener("DOMContentLoaded", () => {
  const videos = document.querySelectorAll(".video-element");

  videos.forEach(video => {
    // Флаг, чтобы засчитать просмотр один раз
    let viewed = false;

    video.addEventListener("play", () => {
      if (!viewed) {
        viewed = true;

        const videoId = video.dataset.id;

        if (!videoId) {
          console.warn("Видео не содержит data-id:", video);
          return;
        }

        fetch("/record-view/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: new URLSearchParams({ video_id: videoId }),
        })
          .then(res => res.json())
          .then(data => {
            console.log("Просмотр засчитан:", data);

            const viewCountEl = document.querySelector(`#view-count-${videoId}`);
            if (viewCountEl && data.view_count) {
              viewCountEl.textContent = data.view_count;
            }
          })
          .catch(err => {
            console.error("Ошибка засчета просмотра:", err);
          });
      }
    });
  });
});

// Получение CSRF токена
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
