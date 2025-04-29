const dropArea = document.getElementById('drop-new-payload');
const updateDropArea = document.getElementById('drop-updated-payload');
const fileName = document.getElementById('file-name');
const newFileName = document.getElementById('new-file-name');

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

updateDropArea.addEventListener('drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    updateDropArea.classList.remove('bg-gray-100', 'dark:bg-gray-600');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        updateDropArea.files = files
        newFileName.textContent = `File uploaded: ${files[0].name}`;
    }
});

updateDropArea.addEventListener('change', function (e) {
    let files = e.target.files;
    if (files.length > 0) {
        newFileName.textContent = `File uploaded: ${files[0].name}`;
    }
});

function resetForm() {
    document.getElementById('create-link-form').reset();
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('table').addEventListener('click', (event) => {
        let button = event.target.closest('button');
        if (!button) return;
        let tr = button.closest('tr');
        if (button.textContent.trim() === 'Edit') {
            if (tr) {
                console.log('Edit button clicked for row id:', tr.id);
                let filenameInput = document.getElementById('edit_filename');
                let urlPathInput = document.getElementById('edit_url_path');
                let preserver_url_path = document.getElementById('update-path');
                if (filenameInput && urlPathInput) {
                    filenameInput.value = tr.getAttribute('data-route-filename');
                    urlPathInput.value = tr.id;
                }
                if (preserver_url_path){
                    preserver_url_path.value = tr.id;
                }
                let payloadInput = document.getElementById('update-payload');
                if (payloadInput){
                    fetch('fetch_payload/'+ tr.id)
                    .then((response) => {
                        return response.json();
                    })
                    .then((data) => {
                        payloadInput.value = data.payload;
                    })
                    .catch(function(error) {
                        console.log(error);
                    });
                }
            }
        } else if (button.textContent.trim() === 'Deactivate' || button.textContent.trim() === 'Activate') {
            if (tr) {
                fetch('update_route_visibility/'+ tr.id)
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    alert(data.message);
                    window.location.href = data.redirect;
                })
                .catch(function(error) {
                    console.log(error);
                });
            }
        }
    });
});
