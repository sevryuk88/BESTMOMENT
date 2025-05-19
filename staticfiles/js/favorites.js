document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".favorite-btn").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault(); // Останавливаем переход по ссылке

            let videoId = this.dataset.videoId;
            let button = this;

            fetch("/toggle-favorite/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: `video_id=${videoId}`
            })
            .then(response => response.json())
            .then(data => {
                // ✅ Обновляем класс строго по is_favorited
                if (data.is_favorited === true) {
                    button.classList.add("favorited");
                } else {
                    button.classList.remove("favorited");
                }
            })
            .catch(error => console.error("Ошибка:", error));
        });
    });

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
