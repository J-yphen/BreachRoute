document.addEventListener('DOMContentLoaded', () => {
    setupDropAreas();
    setupTableButtonHandler();
    setupSelectAllCheckbox();
    setupDeleteConfirmation();
    setupLinkFilterLogging();
    setupBulkActions();
    setupSearchForm();
    setupClearAllFilters();
    setupAutoDismissAlerts();
    setupS3BucketToggle();
    deleteCurrentlyEditingRouteHandler();
});

// --- Windows.onload ---

window.onload = function() {
    hideLoadingScreen();
};

// --- File Drop Areas ---

function setupDropAreas() {
    const dropConfigs = [
        {
            areaId: 'upload-new-payload',
            fileNameId: 'drop-new-payload',
            fileNameLabel: 'file-name'
        },
        {
            areaId: 'upload-updated-payload',
            fileNameId: 'drop-updated-payload',
            fileNameLabel: 'new-file-name'
        }
    ];

    dropConfigs.forEach(({ areaId, fileNameId, fileNameLabel }) => {
        const dropArea = document.getElementById(areaId);
        const fileName = document.getElementById(fileNameId);
        const fileLabel = document.getElementById(fileNameLabel);

        if (!dropArea || !fileName) return;

        // Drag over styling
        dropArea.addEventListener('dragover', e => {
            e.preventDefault();
            e.stopPropagation();
            if (e.dataTransfer.types.includes("Files")) {
                dropArea.classList.add('bg-gray-100', 'dark:bg-gray-600');
            }
        });

        dropArea.addEventListener('dragleave', e => {
            e.preventDefault();
            e.stopPropagation();
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
                fileName.files = files;
                fileLabel.textContent = `File uploaded: ${files[0].name}`;

            }
        });

        // File input change (if dropArea is an <input type="file">)
        dropArea.addEventListener('change', e => {
            e.preventDefault();
            e.stopPropagation();
            const files = e.target.files;
            if (files.length > 0) {
                fileLabel.textContent = `File uploaded: ${files[0].name}`;
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
        showLoadingScreen();
        fetch('delete_route/' + url_path)
            .then(response => response.json())
            .then(data => {
                hideLoadingScreen();
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 50);
            })
            .catch(error => {
                console.log(error);
            });
    });
}

// --- Link Filter Logging ---

function setupLinkFilterLogging() {
    const activeCheckbox = document.getElementById('active_links');
    const inactiveCheckbox = document.getElementById('inactive_links');
    const tableRows = document.querySelectorAll('tr[data-status]');

    if (!activeCheckbox || !inactiveCheckbox) {
        console.log('Filter checkboxes not found in DOM.');
        return;
    }

    function filterRows() {
        const showActive = activeCheckbox.checked;
        const showInactive = inactiveCheckbox.checked;

        // If no filters selected, show all rows (default behavior)
        if (!showActive && !showInactive) {
            tableRows.forEach(row => {
                row.style.display = '';
            });
            return;
        }

        // Otherwise, filter rows
        tableRows.forEach(row => {
            const status = row.getAttribute('data-status');
            if (
                (status === 'active' && showActive) ||
                (status === 'inactive' && showInactive)
            ) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Add event listeners
    activeCheckbox.addEventListener('change', filterRows);
    inactiveCheckbox.addEventListener('change', filterRows);
}

// --- Bulk Actions ---

function setupBulkActions() {
    const bulkToggleVisibilityBtn = document.getElementById('bulk-toggle-btn');
    const bulkDeleteBtn = document.getElementById('bulk-delete-btn');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');

    if (bulkToggleVisibilityBtn) {
        bulkToggleVisibilityBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const selectedRows = getSelectedRows(rowCheckboxes);
            if (selectedRows.length === 0) {
                alert('Please select at least one row to deactivate.');
                return;
            }
            bulkToggleVisibility(selectedRows);
        });
    }

    if (bulkDeleteBtn) {
        bulkDeleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const selectedRows = getSelectedRows(rowCheckboxes);
            if (selectedRows.length === 0) {
                alert('Please select at least one row to delete.');
                return;
            }
            if (!confirm('Are you sure you want to delete the selected rows?')) return;
            bulkDelete(selectedRows);
        });
    }
}

// Helper: Get selected table rows based on checked checkboxes
function getSelectedRows(rowCheckboxes) {
    const selected = [];
    rowCheckboxes.forEach(cb => {
        if (cb.checked) {
            const tr = cb.closest('tr');
            if (tr) selected.push(tr);
        }
    });
    return selected;
}

// Bulk deactivate/activate (calls your existing handleToggleVisibility on each row)
function bulkToggleVisibility(rows) {
    rows.forEach(tr => {
        handleToggleVisibility(tr);
    });
}

// Bulk delete (calls your existing handleDelete on each row)
function bulkDelete(rows) {
    showLoadingScreen();
    rows.forEach(tr => {
        fetch('delete_route/' + tr.id)
            .then(response => response.json())
            .then(data => {
                hideLoadingScreen();
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 50);
            })
            .catch(error => {
                console.log(error);
            });
    });
}

// --- Search Form Handler ---

function setupSearchForm() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('simple-search');

    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (!query) window.location.href = window.location.origin + "/admin";
            window.location.href = `/find_route?query=${encodeURIComponent(query)}`;
        });
    }
}

// --- "Clear all" Filter Handler ---

function setupClearAllFilters() {
    const clearAllLink = document.getElementById('clearAllFilters');
    const activeCheckbox = document.getElementById('active_links');
    const inactiveCheckbox = document.getElementById('inactive_links');
    const tableRows = document.querySelectorAll('tr[data-status]');

    if (!clearAllLink) return;

    clearAllLink.addEventListener('click', function(e) {
        e.preventDefault();
        if (activeCheckbox) activeCheckbox.checked = false;
        if (inactiveCheckbox) inactiveCheckbox.checked = false;
        // Show all rows
        tableRows.forEach(row => row.style.display = '');
    });
}

// --- Alert Auto-Dismiss and Close Handler ---

function setupAutoDismissAlerts() {
    document.querySelectorAll('.auto-dismiss-alert .close-alert-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const alert = btn.closest('.auto-dismiss-alert');
            if (alert) {
                alert.classList.add('opacity-0');
                setTimeout(() => alert.remove(), 700); // match duration-700
            }
        });
    });

    // Auto-dismiss after 3 seconds
    document.querySelectorAll('.auto-dismiss-alert').forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('opacity-0');
            setTimeout(() => alert.remove(), 700); // match duration-700
        }, 3000); // 3 seconds
    });
}

// --- S3 Bucket Toggle Handler ---

function setupS3BucketToggle() {
    const toggleCheckbox = document.getElementById('toggle-s3-details-div');
    const s3Details = document.getElementById('s3-details');
    const providerSelect = document.getElementById('provider-type');

    if (!toggleCheckbox || !s3Details) return;

    s3Details.classList.toggle('hidden', !toggleCheckbox.checked);

    // Handle toggle changes
    toggleCheckbox.addEventListener('change', () => {
        s3Details.classList.toggle('hidden', !toggleCheckbox.checked);
        
        // Toggle required attributes for S3 fields
        // const s3Fields = s3Details.querySelectorAll('input');
        // s3Fields.forEach(field => {
        //     field.required = toggleCheckbox.checked;
        // });
    });

    providerSelect.addEventListener('change', function() {
        let providerName = getSelectedProviderName();
        let access_key_div = document.getElementById("access-key-div");
        let secret_key_div = document.getElementById("secret-key-div");
        let bucket_name_div = document.getElementById("bucket-name-div");
        let region_name_div = document.getElementById("region-name-div");
        let endpoint_url_div = document.getElementById("endpoint-url-div");
        switch (providerName) {
            case "aws":
                access_key_div.classList.remove('hidden');
                secret_key_div.classList.remove('hidden');
                bucket_name_div.classList.remove('hidden');
                region_name_div.classList.remove('hidden');
                endpoint_url_div.classList.remove('hidden');
                break;
            case "gcp":
                access_key_div.classList.remove('hidden');
                secret_key_div.classList.remove('hidden');
                bucket_name_div.classList.remove('hidden');
                region_name_div.classList.add('hidden');
                endpoint_url_div.classList.add('hidden');
                break;
            case "azure":
                access_key_div.classList.remove('hidden');
                secret_key_div.classList.remove('hidden');
                bucket_name_div.classList.remove('hidden');
                region_name_div.classList.add('hidden');
                endpoint_url_div.classList.add('hidden');
                break;
            case "digitalocean":
                access_key_div.classList.remove('hidden');
                secret_key_div.classList.remove('hidden');
                bucket_name_div.classList.remove('hidden');
                region_name_div.classList.remove('hidden');
                endpoint_url_div.classList.add('hidden');
                break;
            case "backblaze":
                access_key_div.classList.remove('hidden');
                secret_key_div.classList.remove('hidden');
                bucket_name_div.classList.remove('hidden');
                region_name_div.classList.add('hidden');
                endpoint_url_div.classList.add('hidden');
                break;        
            default:
                access_key_div.classList.add('hidden');
                secret_key_div.classList.add('hidden');
                bucket_name_div.classList.add('hidden');
                region_name_div.classList.add('hidden');
                endpoint_url_div.classList.add('hidden');
                break;
        }
    });

    function getSelectedProviderName() {
        let selectedOption = providerSelect.options[providerSelect.selectedIndex];
        if (providerSelect.value !== "" && providerSelect.selectedIndex !== 0) {
            return selectedOption.value;
        } else {
            return null;
        }
    }
}

// --- Delete Current Edit Route Handler ---

function deleteCurrentlyEditingRouteHandler() {
    let delete_btn = document.getElementById('delete-currently-editing-route');
    let urlPathInput = document.getElementById('edit_url_path');
    if (delete_btn){    
        delete_btn.addEventListener("click", function() {
            showLoadingScreen();
            if(urlPathInput){
                fetch('delete_route/' + urlPathInput.value)
                .then(response => response.json())
                .then(data => {
                    hideLoadingScreen();
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 50);
                })
                .catch(error => {
                    console.log(error);
                });
            } 
        });
    }
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
        showLoadingScreen();
        fetch('fetch_payload/' + tr.id)
            .then(response => response.json())
            .then(data => {
                if(data.msg === undefined){
                    payloadInput.value = data.payload;
                }
                else {
                    payloadInput.value = "==========" + data.msg + "==========";
                }
                hideLoadingScreen();
            })
            .catch(error => {
                console.log(error);
            });
    }
}

function handleToggleVisibility(tr) {
    if (!tr) return;
    showLoadingScreen();
    fetch('update_route_visibility/' + tr.id)
        .then(response => response.json())
        .then(data => {
            hideLoadingScreen();
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 50);
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
