document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab-btn");
    const sections = document.querySelectorAll(".video-section");

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            // Убираем активный класс у всех вкладок
            tabs.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            // Показываем нужную секцию
            let target = this.getAttribute("data-tab");
            sections.forEach(section => {
                section.classList.toggle("hidden", section.id !== target);
            });
        });
    });
});
 