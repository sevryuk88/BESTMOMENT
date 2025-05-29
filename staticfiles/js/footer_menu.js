const addBtn = document.querySelector(".add-menu");
if (addBtn) {
    addBtn.addEventListener("click", e => {
        addBtn.classList.toggle("closed");
    });
}
