/**
 * GPI SDK Web Interface - Main JS
 */

// Global utilities and helper functions

/**
 * Show a notification to the user
 * @param {string} message - The message to display
 * @param {string} type - The notification type (success, danger, warning, info)
 */
function showNotification(message, type = 'info') {
    // Check if notification container exists, if not create it
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '1050';
        container.style.maxWidth = '350px';
        document.body.appendChild(container);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to container
    container.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * Format a date string
 * @param {string|Date} dateString - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

/**
 * Truncate a string to a maximum length and add ellipsis
 * @param {string} str - The string to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated string
 */
function truncateString(str, maxLength = 100) {
    if (!str) return '';
    return str.length > maxLength ? str.substring(0, maxLength) + '...' : str;
}

/**
 * Encode HTML to prevent XSS attacks
 * @param {string} html - The HTML string to encode
 * @returns {string} Encoded HTML
 */
function encodeHTML(html) {
    return html
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/**
 * Format JSON for display
 * @param {object} json - The JSON object to format
 * @returns {string} Formatted JSON string
 */
function formatJSON(json) {
    return JSON.stringify(json, null, 2);
}

/**
 * Copy text to clipboard
 * @param {string} text - The text to copy
 */
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        showNotification('Failed to copy text.', 'danger');
    }
    
    document.body.removeChild(textarea);
}

// Initialize common elements when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add click handler for elements with data-copy attribute
    document.addEventListener('click', (e) => {
        if (e.target.hasAttribute('data-copy')) {
            const text = e.target.getAttribute('data-copy');
            copyToClipboard(text);
        }
    });
}); 