// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelector('.flash-messages');

    // If the flash message container exists, add the timeout functionality
    if (flashMessages) {
        setTimeout(function () {
            // Fade out the flash message after 3 seconds
            flashMessages.style.opacity = '0';
            flashMessages.style.visibility = 'hidden';
        }, 3000); // Wait for 3 seconds before hiding
    }
});
