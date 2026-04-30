/* SmartExpense — Shared utilities */

/**
 * Show a toast notification.
 * @param {string} message
 * @param {'success'|'error'|'info'} type
 */
function showToast(message, type = 'success') {
    const colorMap = {
        success: 'bg-green-500',
        error:   'bg-red-500',
        info:    'bg-blue-500'
    };
    const iconMap = {
        success: 'fa-check-circle',
        error:   'fa-exclamation-circle',
        info:    'fa-info-circle'
    };
    const toast = $(`
        <div class="toast ${colorMap[type]} text-white px-5 py-3 rounded-lg shadow-lg text-sm flex items-center gap-2 mb-2">
            <i class="fas ${iconMap[type]}"></i>
            <span>${message}</span>
        </div>
    `);
    $('#toast-container').append(toast);
    setTimeout(() => toast.fadeOut(300, () => toast.remove()), 3500);
}

/**
 * Toggle mobile sidebar.
 */
function toggleMobileMenu() {
    $('aside').toggleClass('hidden').toggleClass('flex');
}

/**
 * Generic AJAX DELETE with confirmation.
 * @param {string} url
 * @param {string} confirmMsg
 * @param {Function} onSuccess
 */
function confirmDelete(url, confirmMsg, onSuccess) {
    if (!confirm(confirmMsg || 'Are you sure you want to delete this?')) return;
    $.ajax({
        url: url,
        method: 'DELETE',
        success: function (res) {
            showToast(res.message || 'Deleted successfully');
            if (typeof onSuccess === 'function') onSuccess();
        },
        error: function (xhr) {
            const msg = xhr.responseJSON?.detail || 'Delete failed';
            showToast(msg, 'error');
        }
    });
}

// Highlight active sidebar link on load
$(function () {
    const path = window.location.pathname;
    $('.sidebar-link').each(function () {
        const href = $(this).attr('href');
        if (href && path.startsWith(href) && href !== '/') {
            $(this).addClass('active');
        }
    });
});
