// app/static/js/app.js - Enhanced with better animations
/* SmartExpense — Enhanced Shared utilities */

/**
 * Show a toast notification with animation.
 * @param {string} message
 * @param {'success'|'error'|'info'} type
 */
function showToast(message, type = 'success') {
    const colorMap = {
        success: 'bg-gradient-to-r from-green-500 to-emerald-600',
        error:   'bg-gradient-to-r from-red-500 to-rose-600',
        info:    'bg-gradient-to-r from-blue-500 to-indigo-600'
    };
    const iconMap = {
        success: 'fa-check-circle',
        error:   'fa-exclamation-circle',
        info:    'fa-info-circle'
    };
    const toast = $(`
        <div class="toast ${colorMap[type]} text-white px-5 py-3 rounded-xl shadow-2xl text-sm flex items-center gap-2 mb-2 transform transition-all duration-300">
            <i class="fas ${iconMap[type]} text-lg"></i>
            <span class="font-medium">${escapeHtml(message)}</span>
            <button onclick="$(this).parent().fadeOut(300, function() { $(this).remove(); })" class="ml-3 text-white/80 hover:text-white">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `);
    $('#toast-container').append(toast);
    toast.hide().fadeIn(300);
    setTimeout(() => {
        toast.fadeOut(300, () => toast.remove());
    }, 4000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Toggle mobile sidebar with animation.
 */
function toggleMobileMenu() {
    $('aside').toggleClass('hidden').toggleClass('flex');
    if ($('aside').hasClass('flex')) {
        $('aside').css('animation', 'slideInLeft 0.3s ease');
    }
}

/**
 * Generic AJAX DELETE with confirmation.
 * @param {string} url
 * @param {string} confirmMsg
 * @param {Function} onSuccess
 */
function confirmDelete(url, confirmMsg, onSuccess) {
    if (!confirm(confirmMsg || 'Are you sure you want to delete this?')) return;
    const btn = $('button[onclick*="' + url + '"]');
    btn.html('<i class="fas fa-spinner fa-spin"></i>').prop('disabled', true);
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
            btn.html('<i class="fas fa-trash"></i>').prop('disabled', false);
        }
    });
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Show loading overlay
 */
function showLoading() {
    if ($('#loading-overlay').length === 0) {
        $('body').append(`
            <div id="loading-overlay" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
                <div class="bg-white rounded-2xl p-6 shadow-2xl flex flex-col items-center">
                    <div class="spinner"></div>
                    <p class="mt-3 text-gray-600 text-sm">Loading...</p>
                </div>
            </div>
        `);
    }
    $('#loading-overlay').fadeIn(200);
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    $('#loading-overlay').fadeOut(200);
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
    
    // Add fade-up animation to all content sections
    $('.animate-fade-up').each(function(index) {
        $(this).css('animation-delay', `${index * 0.05}s`);
    });
    
    // Add ripple effect to buttons
    $('.btn-ripple').on('click', function(e) {
        const ripple = $(this);
        ripple.css('transform', 'scale(0.98)');
        setTimeout(() => ripple.css('transform', ''), 150);
    });
});