document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-upload");
    const fileListContainer = document.getElementById("file-list");

    fileInput.addEventListener("change", () => {
        fileListContainer.innerHTML = "";

        const files = fileInput.files;
        if (files.length > 0) {
            const fileList = document.createElement("ul");
            for (let i = 0; i < files.length; i++) {
                const fileItem = document.createElement("li");
                fileItem.textContent = files[i].name;
                fileList.appendChild(fileItem);
            }
            fileListContainer.appendChild(fileList);
        } else {
            fileListContainer.textContent = "No files selected.";
        }
    });
});