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
    setupTableButtonHandler();
    setupSelectAllCheckbox();
});

function setupTableButtonHandler() {
    const table = document.querySelector('table');
    if (!table) return;

    table.addEventListener('click', (event) => {
        let button = event.target.closest('button');
        if (!button) return;
        let tr = button.closest('tr');

        switch (button.textContent.trim()) {
            case 'Edit':
                handleEdit(tr);
                break;
            case 'Deactivate':
            case 'Activate':
                handleToggleVisibility(tr);
                break;
            case 'Delete':
                handleDelete(tr);
                break;
            case 'Preview':
                handlePreview(tr);
                break;
        }

        const copyBtn = event.target.closest('[data-copy-to-clipboard]');
        if (copyBtn && tr) {
            handleCopyToClipboard(copyBtn, tr);
        }
    });
}

function setupSelectAllCheckbox() {
    const selectAllCheckbox = document.getElementById('checkbox-all');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    if (!selectAllCheckbox || rowCheckboxes.length === 0) return;

    // When header checkbox is toggled, set all row checkboxes
    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
    });

    // When any row checkbox is toggled, update header checkbox
    rowCheckboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            selectAllCheckbox.checked = Array.from(rowCheckboxes).every(c => c.checked);
        });
    });
}

function handleEdit(tr) {
    if (!tr) return;
    console.log('Edit button clicked for row id:', tr.id);

    let filenameInput = document.getElementById('edit_filename');
    let urlPathInput = document.getElementById('edit_url_path');
    let preserver_url_path = document.getElementById('update-path');
    if (filenameInput && urlPathInput) {
        filenameInput.value = tr.getAttribute('data-route-filename');
        urlPathInput.value = tr.id;
    }
    if (preserver_url_path) {
        preserver_url_path.value = tr.id;
    }
    let payloadInput = document.getElementById('update-payload');
    if (payloadInput) {
        fetch('fetch_payload/' + tr.id)
            .then(response => response.json())
            .then(data => {
                payloadInput.value = data.payload;
            })
            .catch(error => {
                console.log(error);
            });
    }
}

function handleToggleVisibility(tr) {
    if (!tr) return;
    fetch('update_route_visibility/' + tr.id)
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.href = data.redirect;
        })
        .catch(error => {
            console.log(error);
        });
}

function handleDelete(tr) {
    if (!tr) return;
    let deleteInput = document.getElementById('delete-row-id');
    if (deleteInput) {
        deleteInput.value = tr.id;
    }
}

function handlePreview(tr) {
    if (!tr) return;
    window.open("/" + tr.id, '_blank');
}

function handleCopyToClipboard(copyBtn, tr) {
    const container = copyBtn.closest('.flex');
    const contentSpan = container.querySelector('[data-copy-content]');
    contentSpan.textContent = window.location.origin + "/" + tr.id;
    const textToCopy = contentSpan.textContent.trim();

    navigator.clipboard.writeText(textToCopy).then(() => {
        const defaultIcon = copyBtn.querySelector('.default-icon');
        const successIcon = copyBtn.querySelector('.success-icon');
        defaultIcon.classList.add('hidden');
        successIcon.classList.remove('hidden');
        setTimeout(() => {
            defaultIcon.classList.remove('hidden');
            successIcon.classList.add('hidden');
        }, 1000);
    });
}

const yesButton = document.getElementById('confirm-delete-btn');
yesButton.addEventListener('click', function() {
    let url_path = document.getElementById('delete-row-id').value;
    fetch('delete_route/'+ url_path)
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
});
