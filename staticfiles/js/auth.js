// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Check if user is logged in
function checkAuth() {
    // In Django, we'll check this differently
    // For now, return true if on authenticated pages
    return true;
}

// Add user dropdown
function addUserDropdown() {
    // Get user data from Django template
    const userDataElement = document.getElementById('userData');
    if (!userDataElement) return;
    
    const currentUser = JSON.parse(userDataElement.textContent);
    
    // Update welcome text
    const userRoleElement = document.querySelector('.text-xs.text-gray-500');
    if (userRoleElement) {
        userRoleElement.textContent = currentUser.name;
    }
    
    // Rest of your dropdown code remains same...
}

// Logout function
function logout(event) {
    event.preventDefault();
    window.location.href = '/logout/';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    addUserDropdown();
});