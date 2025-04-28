const dropArea = document.getElementById('drop-new-payload');
const fileName = document.getElementById('file-name');

dropArea.addEventListener('drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    dropArea.classList.remove('bg-gray-100', 'dark:bg-gray-600');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        dropArea.files = files
        fileName.textContent = `File uploaded: ${files[0].name}`;
    }
});

dropArea.addEventListener('change', function (e) {
    let files = e.target.files;
    if (files.length > 0) {
        fileName.textContent = `File uploaded: ${files[0].name}`;
    }
});

function resetForm() {
    document.getElementById('create-link-form').reset();
}