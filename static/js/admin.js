// Admin Panel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle for mobile
    initSidebarToggle();
    
    // Initialize datatables if available
    initDataTables();
    
    // Initialize WYSIWYG editors if available
    initSummernote();
    
    // Initialize confirmation dialogs
    initConfirmDialogs();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize image preview for file uploads
    initImagePreview();
});

/**
 * Initialize sidebar toggle functionality for mobile
 */
function initSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarToggleShow = document.getElementById('sidebarToggleShow');
    const adminSidebar = document.querySelector('.admin-sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            adminSidebar.classList.remove('show');
        });
    }
    
    if (sidebarToggleShow) {
        sidebarToggleShow.addEventListener('click', function() {
            adminSidebar.classList.add('show');
        });
    }
    
    // Close sidebar when clicking outside of it
    document.addEventListener('click', function(event) {
        const isClickInside = adminSidebar.contains(event.target) || 
                             (sidebarToggleShow && sidebarToggleShow.contains(event.target));
        
        if (!isClickInside && adminSidebar.classList.contains('show')) {
            adminSidebar.classList.remove('show');
        }
    });
}

/**
 * Initialize DataTables for better table functionality
 */
function initDataTables() {
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.datatable').DataTable({
            responsive: true,
            "language": {
                "search": "Filter:",
                "lengthMenu": "Show _MENU_ entries",
                "info": "Showing _START_ to _END_ of _TOTAL_ entries",
                "paginate": {
                    "first": "First",
                    "last": "Last",
                    "next": "Next",
                    "previous": "Previous"
                }
            }
        });
    }
}

/**
 * Initialize Summernote WYSIWYG editor for content editing
 */
function initSummernote() {
    if (typeof $.fn.summernote !== 'undefined') {
        $('.summernote').summernote({
            height: 300,
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture']],
                ['view', ['fullscreen', 'codeview', 'help']]
            ],
            callbacks: {
                onImageUpload: function(files) {
                    for (let i = 0; i < files.length; i++) {
                        uploadSummernoteImage(files[i], this);
                    }
                }
            }
        });
    }
}

/**
 * Upload images from Summernote editor
 */
function uploadSummernoteImage(file, editor) {
    // Create form data to send the file
    const formData = new FormData();
    formData.append('file', file);
    
    // AJAX request to upload the image
    fetch('/admin/blogs/upload-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Insert the uploaded image into the editor
        $(editor).summernote('insertImage', data.url);
    })
    .catch(error => {
        console.error('Error uploading image:', error);
        alert('Failed to upload image. Please try again.');
    });
}

/**
 * Initialize confirmation dialogs for delete actions
 */
function initConfirmDialogs() {
    document.querySelectorAll('form[data-confirm]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to proceed with this action?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

/**
 * Initialize basic form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Initialize image preview for file uploads
 */
function initImagePreview() {
    const fileInputs = document.querySelectorAll('input[type="file"][data-preview]');
    
    fileInputs.forEach(input => {
        const previewElementId = input.getAttribute('data-preview');
        const previewElement = document.getElementById(previewElementId);
        
        if (previewElement) {
            input.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        if (previewElement.tagName === 'IMG') {
                            previewElement.src = e.target.result;
                            previewElement.style.display = 'block';
                        } else {
                            // If not an image element, create an image inside the container
                            previewElement.innerHTML = '';
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            img.classList.add('img-fluid', 'rounded', 'mt-2');
                            previewElement.appendChild(img);
                        }
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    });
}

/**
 * Show an alert message
 * @param {string} message - The message to display
 * @param {string} type - Alert type (success, danger, warning, info)
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    
    // Add message
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the top of the content area
    const contentArea = document.querySelector('.admin-content');
    if (contentArea) {
        contentArea.insertBefore(alertDiv, contentArea.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 5000);
    }
}

/**
 * Format date for display
 * @param {string} dateString - ISO date string
 * @param {boolean} includeTime - Whether to include time in the output
 * @returns {string} Formatted date string
 */
function formatDate(dateString, includeTime = false) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };
    
    if (includeTime) {
        options.hour = '2-digit';
        options.minute = '2-digit';
    }
    
    return date.toLocaleDateString('en-US', options);
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} length - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 50) {
    if (!text) return '';
    if (text.length <= length) return text;
    
    return text.substring(0, length) + '...';
}

/**
 * Handle AJAX form submission
 * @param {HTMLFormElement} form - The form element
 * @param {Function} successCallback - Function to call on success
 */
function submitFormAjax(form, successCallback) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Disable submit button and show loading state
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
    }
    
    // Send AJAX request
    fetch(form.action, {
        method: form.method,
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message || 'Operation completed successfully', 'success');
            if (typeof successCallback === 'function') {
                successCallback(data);
            }
        } else {
            showAlert(data.message || 'An error occurred', 'danger');
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        showAlert('An unexpected error occurred. Please try again.', 'danger');
    })
    .finally(() => {
        // Re-enable submit button
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = submitButton.getAttribute('data-original-text') || 'Submit';
        }
    });
    
    // Prevent default form submission
    return false;
}