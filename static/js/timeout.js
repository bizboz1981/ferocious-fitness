// Initiate a timeout function to hide the messages after 5 seconds

setTimeout(function() {
    const messages = document.querySelector('.messages');
    if (messages) {
        messages.style.display = 'none';
    }
}, 5000);