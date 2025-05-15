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

function initCustomPlayers() {
  const players = document.querySelectorAll(".custom-video-player:not(.initialized)");
  console.log("▶ Инициализация custom video контролов, найдено:", players.length);

  players.forEach(player => {
    player.classList.add("initialized");

    const video = player.querySelector(".video-element");
    const overlay = player.querySelector(".video-overlay");
    const playBtn = overlay.querySelector(".play-btn");
    const controls = player.querySelector(".controls-container");
    const progressBar = player.querySelector(".progress-bar");
    const playToggle = player.querySelector(".play-toggle");
    const fullscreenBtn = player.querySelector(".fullscreen-toggle");
    const currentTimeEl = player.querySelector(".current-time");
    const durationEl = player.querySelector(".duration");
    const spinner = player.querySelector(".video-loading-spinner");

    const settingsToggle = player.querySelector(".settings-toggle");
    const speedMenu = player.querySelector(".speed-menu");
    const speedOptions = player.querySelectorAll(".speed-option");

    if (settingsToggle && speedMenu) {
      settingsToggle.addEventListener("click", () => {
        speedMenu.classList.toggle("hidden");
      });

      speedOptions.forEach(option => {
        option.addEventListener("click", () => {
          const speed = parseFloat(option.dataset.speed);
          video.playbackRate = speed;

          speedOptions.forEach(o => o.classList.remove("active"));
          option.classList.add("active");

          speedMenu.classList.add("hidden");
        });

        if (option.dataset.default) {
          option.classList.add("active");
        }
      });

      document.addEventListener("click", (e) => {
        if (!player.contains(e.target)) {
          speedMenu.classList.add("hidden");
        }
      });
    }

    let hideControlsTimeout;
    let lastTap = 0;
    video.dataset.viewed = "false";

    const formatTime = seconds => {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
    };

    video.addEventListener("loadedmetadata", () => {
      durationEl.textContent = formatTime(video.duration);
    });

    video.addEventListener("waiting", () => spinner.style.display = "block");
    video.addEventListener("playing", () => spinner.style.display = "none");

    video.addEventListener("timeupdate", () => {
      const percent = (video.currentTime / video.duration) * 100;
      progressBar.value = percent || 0;
      progressBar.style.setProperty('--value', `${percent}%`);
      currentTimeEl.textContent = formatTime(video.currentTime);
    });

    const pauseAllOthers = () => {
      document.querySelectorAll(".custom-video-player").forEach(p => {
        const v = p.querySelector(".video-element");
        if (v !== video) {
          v.pause();
          p.querySelector(".video-overlay").classList.remove("hidden");
          p.querySelector(".play-toggle i").textContent = "play_arrow";
        }
      });
    };

    const togglePlay = () => {
      if (video.paused) {
        pauseAllOthers();
        video.play();
        overlay.classList.add("hidden");
        playToggle.querySelector("i").textContent = "pause";
      } else {
        video.pause();
        overlay.classList.remove("hidden");
        playToggle.querySelector("i").textContent = "play_arrow";
      }
    };

    playBtn.addEventListener("click", togglePlay);
    playToggle.addEventListener("click", togglePlay);

    video.addEventListener("click", e => {
      const now = new Date().getTime();
      const delta = now - lastTap;
      lastTap = now;

      const rect = video.getBoundingClientRect();
      const tapX = e.clientX - rect.left;

      if (delta < 300) {
        const half = rect.width / 2;
        if (tapX < half) {
          video.currentTime = Math.max(0, video.currentTime - 10);
        } else {
          video.currentTime = Math.min(video.duration, video.currentTime + 10);
        }
      } else {
        togglePlay();
      }
    });

    progressBar.addEventListener("input", () => {
      const time = (progressBar.value / 100) * video.duration;
      video.currentTime = time;
      progressBar.style.setProperty('--value', `${progressBar.value}%`);
    });

    fullscreenBtn.addEventListener("click", () => {
      try {
        if (!document.fullscreenElement) {
          if (player.requestFullscreen) {
            player.requestFullscreen();
          } else if (player.webkitRequestFullscreen) {
            player.webkitRequestFullscreen();
          } else if (player.msRequestFullscreen) {
            player.msRequestFullscreen();
          }
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          }
        }
      } catch (err) {
        console.warn("⚠ Fullscreen API error:", err.message);
      }
    });

    const showControls = () => {
      controls.classList.remove("hidden");
      clearTimeout(hideControlsTimeout);
      hideControlsTimeout = setTimeout(() => {
        controls.classList.add("hidden");
      }, 3000);
    };

    video.addEventListener("play", () => {
      showControls();

      if (video.dataset.viewed === "false") {
        video.dataset.viewed = "true";
        const videoId = video.id.replace("video-", "");
        if (!videoId) {
          console.warn("ID видео не найден:", video);
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

    player.addEventListener("mousemove", showControls);
    player.addEventListener("touchstart", showControls);

    video.addEventListener("ended", () => {
      overlay.classList.remove("hidden");
      controls.classList.remove("hidden");
      playToggle.querySelector("i").textContent = "play_arrow";
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initCustomPlayers();

  // Повторная инициализация при переключении вкладок
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      setTimeout(() => {
        initCustomPlayers();
      }, 200);
    });
  });
});
