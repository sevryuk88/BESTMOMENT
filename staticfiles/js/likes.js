document.addEventListener('DOMContentLoaded', function () {
    console.log("Likes script loaded!");

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function formatNumber(n) {
        if (n >= 1000000) return (n / 1000000).toFixed(1).replace('.0', '') + 'M';
        if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'K';
        return n.toString();
    }

    function updateStats(container, data) {
        if (!container || !data) return;

        const setText = (selector, value) => {
            const el = container.querySelector(selector);
            if (el) el.textContent = formatNumber(value);
        };

        setText('.like-count', data.likes);
        setText('.dislike-count', data.dislikes);
        setText('.rating-count', data.rating);
        setText('.view-count', data.views);
        setText('.message-count', data.comments);
    }

    const csrftoken = getCookie('csrftoken');

    // Обработка лайков
    document.querySelectorAll('.fa-thumbs-up').forEach(button => {
        button.addEventListener('click', () => {
            const videoId = button.getAttribute('data-video-id');
            console.log("Лайк нажали для видео ID:", videoId);

            fetch('/like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'video_id=' + encodeURIComponent(videoId)
            })
            .then(response => response.json())
            .then(data => {
                const statsContainer = button.closest('.video-stats');
                updateStats(statsContainer, data);

                // Обновляем классы
                button.classList.add('liked');
                button.classList.remove('disliked');
                
                const downBtn = statsContainer.querySelector('.fa-thumbs-down');
                if (downBtn) downBtn.classList.remove('disliked');
            })
            .catch(error => console.error('Ошибка при обновлении лайка:', error));
        });
    });

    // Обработка дизлайков
    document.querySelectorAll('.fa-thumbs-down').forEach(button => {
        button.addEventListener('click', () => {
            const videoId = button.getAttribute('data-video-id');
            console.log("Дизлайк нажали для видео ID:", videoId);

            fetch('/dislike/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'video_id=' + encodeURIComponent(videoId)
            })
            .then(response => response.json())
            .then(data => {
                const statsContainer = button.closest('.video-stats');
                updateStats(statsContainer, data);

                button.classList.add('disliked');
                button.classList.remove('liked');

                const upBtn = statsContainer.querySelector('.fa-thumbs-up');
                if (upBtn) upBtn.classList.remove('liked');
            })
            .catch(error => console.error('Ошибка при обновлении дизлайка:', error));
        });
    });

    // Форматирование чисел при загрузке
    document.querySelectorAll('.like-count, .dislike-count, .rating-count, .view-count, .message-count')
        .forEach(el => {
            const num = parseInt(el.textContent.replace(/\D/g, ''), 10);
            if (!isNaN(num)) {
                el.textContent = formatNumber(num);
            }
        });
});
