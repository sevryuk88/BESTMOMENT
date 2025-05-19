document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("photo-upload");
    const profilePreview = document.getElementById("profile-preview");

    fileInput.addEventListener("change", function (event) {
        if (event.target.files.length > 0) {
            let reader = new FileReader();
            reader.onload = function () {
                profilePreview.src = reader.result;
            };
            reader.readAsDataURL(event.target.files[0]);
        }
    });
});
