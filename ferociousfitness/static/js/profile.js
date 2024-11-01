// Toggle the display of the profile form when the button is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('show-form-btn').addEventListener('click', function() {
        var formContainer = document.getElementById('profile-form-container');
        if (formContainer.style.display === 'none' || formContainer.style.display === '') {
            formContainer.style.display = 'block';
        } else {
            formContainer.style.display = 'none';
        }
    });
});