document.addEventListener('DOMContentLoaded', function() {
    console.log('Comments script loaded');

    const commentToggles = document.querySelectorAll('.comment-toggle');
    commentToggles.forEach(function(icon) {
        icon.addEventListener('click', function() {
            const videoId = icon.getAttribute('data-video-id');
            const commentsArea = document.getElementById('comments-area-' + videoId);
            const isOpening = !commentsArea.classList.contains('open');

            commentsArea.classList.toggle('open');
            
            // ✅ Добавляем/удаляем эффект на иконку
            icon.classList.toggle('active');

            const videoCard = icon.closest('.video-card');

            if (isOpening) {
                // ⛔ Блокируем скролл у карточки
                videoCard.classList.add('no-scroll');
                videoCard.classList.add('animating');

                setTimeout(() => {
                    videoCard.classList.remove('animating');
                    videoCard.classList.remove('no-scroll');
                }, 400); // Заменить на точную длительность твоей анимации
            }
        });
    });

    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const videoId = form.getAttribute('data-video-id');
            const formData = new FormData(form);

            const url = `/comment/${videoId}/`;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error('Ошибка:', data.error);
                } else {
                    const commentsList = document.getElementById('comments-list-' + videoId);
                    const li = document.createElement('li');
                    li.classList.add('comment-fade-in');

                    li.innerHTML = `
                        <div class="comment-item">
                            <div class="comment-avatar">
                                <img src="${data.photo_url || '/media/users/user.png'}" alt="${data.author}">
                            </div>
                            <div class="comment-body">
                                <div class="comment-header">
                                    <strong class="comment-author">${data.author}</strong>
                                    <span class="comment-date">${data.created_at}</span>
                                </div>
                                <p class="comment-text">${data.content}</p>
                            </div>
                        </div>
                    `;
                    commentsList.appendChild(li);

                    commentsList.scrollTo({
                        top: commentsList.scrollHeight,
                        behavior: 'smooth'
                    });

                    const textarea = form.querySelector('.comment-textarea');
                    const submitBtn = form.querySelector('.comment-submit-btn');
                    textarea.value = '';
                    textarea.style.height = 'auto';
                    submitBtn.disabled = true;
                    submitBtn.style.opacity = '0';
                    submitBtn.style.pointerEvents = 'none';
                }
            })
            .catch(error => console.error('Ошибка отправки комментария:', error));
        });
    });

    document.querySelectorAll('.comment-textarea').forEach(textarea => {
        const maxHeight = 64;

        textarea.addEventListener('input', () => {
            textarea.style.height = 'auto';
            const newHeight = Math.min(textarea.scrollHeight, maxHeight);
            textarea.style.height = newHeight + 'px';
            textarea.scrollTop = textarea.scrollHeight;
        });
    });
});
