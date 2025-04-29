document.addEventListener('DOMContentLoaded', () => {
    setupDropAreas();
    setupTableButtonHandler();
    setupSelectAllCheckbox();
    setupDeleteConfirmation();
});

// --- File Drop Areas ---

function setupDropAreas() {
    const dropConfigs = [
        {
            areaId: 'drop-new-payload',
            fileNameId: 'file-name'
        },
        {
            areaId: 'drop-updated-payload',
            fileNameId: 'new-file-name'
        }
    ];

    dropConfigs.forEach(({ areaId, fileNameId }) => {
        const dropArea = document.getElementById(areaId);
        const fileName = document.getElementById(fileNameId);

        if (!dropArea || !fileName) return;

        // Drag over styling
        dropArea.addEventListener('dragover', e => {
            e.preventDefault();
            dropArea.classList.add('bg-gray-100', 'dark:bg-gray-600');
        });

        dropArea.addEventListener('dragleave', e => {
            e.preventDefault();
            dropArea.classList.remove('bg-gray-100', 'dark:bg-gray-600');
        });

        // Drop event
        dropArea.addEventListener('drop', e => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.remove('bg-gray-100', 'dark:bg-gray-600');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                // Optionally, you might want to store files somewhere
                // dropArea.files = files; // Not standard, but if you use a custom property
                fileName.textContent = `File uploaded: ${files[0].name}`;
            }
        });

        // File input change (if dropArea is an <input type="file">)
        dropArea.addEventListener('change', e => {
            const files = e.target.files;
            if (files.length > 0) {
                fileName.textContent = `File uploaded: ${files[0].name}`;
            }
        });
    });
}

// --- Table Button Actions ---

function setupTableButtonHandler() {
    const table = document.querySelector('table');
    if (!table) return;

    table.addEventListener('click', event => {
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

        // Copy to clipboard
        const copyBtn = event.target.closest('[data-copy-to-clipboard]');
        if (copyBtn && tr) {
            handleCopyToClipboard(copyBtn, tr);
        }
    });
}

// --- Select All Checkbox ---

function setupSelectAllCheckbox() {
    const selectAllCheckbox = document.getElementById('checkbox-all');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    if (!selectAllCheckbox || rowCheckboxes.length === 0) return;

    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
    });

    rowCheckboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            selectAllCheckbox.checked = Array.from(rowCheckboxes).every(c => c.checked);
        });
    });
}

// --- Delete Confirmation ---

function setupDeleteConfirmation() {
    const yesButton = document.getElementById('confirm-delete-btn');
    if (!yesButton) return;

    yesButton.addEventListener('click', function() {
        let url_path = document.getElementById('delete-row-id').value;
        fetch('delete_route/' + url_path)
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = data.redirect;
            })
            .catch(error => {
                console.log(error);
            });
    });
}

// --- Row Action Handlers ---

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
        if (defaultIcon && successIcon) {
            defaultIcon.classList.add('hidden');
            successIcon.classList.remove('hidden');
            setTimeout(() => {
                defaultIcon.classList.remove('hidden');
                successIcon.classList.add('hidden');
            }, 1000);
        }
    });
}

// --- Utility ---

function resetForm() {
    const form = document.getElementById('create-link-form');
    if (form) form.reset();
}
