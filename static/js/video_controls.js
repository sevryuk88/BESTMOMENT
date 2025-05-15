document.querySelectorAll(".custom-video").forEach((video) => {
    let controlsTimeout;
    let isUserInteracting = false; // Флаг взаимодействия с видео
    let isSpeedMenuOpen = false;  // Проверка, открыто ли меню выбора скорости

    // Показываем элементы управления при клике на видео
    video.addEventListener("click", (event) => {
        event.stopPropagation();
        video.controls = true;

        // Если меню скорости не открыто, запускаем таймер на скрытие
        if (!isSpeedMenuOpen && !isUserInteracting) {
            clearTimeout(controlsTimeout);
            controlsTimeout = setTimeout(() => {
                video.controls = false;
            }, 3000); // 3 секунды задержка перед скрытием
        }
    });

    // Следим за изменением скорости воспроизведения
    video.addEventListener("ratechange", () => {
        isSpeedMenuOpen = false;  // Меню скорости закрыто
        video.play(); // Видео начинает воспроизведение после изменения скорости
        // Скрытие элементов управления после задержки
        controlsTimeout = setTimeout(() => {
            video.controls = false;
        }, 3000); // Таймер на 3 секунды
    });

    // Если пользователь открывает меню выбора скорости
    video.addEventListener("pause", () => {
        isSpeedMenuOpen = true; // Меню выбора скорости открыто
        clearTimeout(controlsTimeout); // Останавливаем таймер скрытия
    });

    // При уходе мыши с видео
    video.addEventListener("mouseleave", () => {
        if (!isSpeedMenuOpen && !isUserInteracting) {
            video.controls = false;  // Скрытие управления, если нет взаимодействия
        }
    });

    // Останавливаем другие видео при воспроизведении
    video.addEventListener("play", () => {
        document.querySelectorAll(".custom-video").forEach((otherVideo) => {
            if (otherVideo !== video) {
                otherVideo.pause();
                otherVideo.controls = false; // Скрываем управление у других видео
            }
        });
    });

    // Отключаем стандартное управление по умолчанию
    video.controls = false;
});
