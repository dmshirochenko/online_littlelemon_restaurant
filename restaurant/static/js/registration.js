document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('registration-form');
    const messageBox = document.getElementById('message');

    form.addEventListener('submit', function (e) {
        e.preventDefault();  // Prevent default form submission behavior

        // Reset the message box to its initial state
        messageBox.style.display = 'none';
        messageBox.classList.remove('error', 'success');

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('/auth/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Django CSRF Token
            },
            body: JSON.stringify({
                email: email,
                username: email,  // Duplicate email as username
                password: password
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                // Parse the error JSON if the status is not OK
                return response.json().then(err => { throw err; });
            }
        })
        .then(data => {
            messageBox.textContent = 'Successfully registered.';
            messageBox.style.display = 'block';  // make it visible
            messageBox.classList.add('success');
            
            const homeUrl = document.getElementById('homeUrl').value;
            
            setTimeout(() => {
                window.location.href = homeUrl; // adjust the path as required
            }, 2000); // waits 2 seconds before redirecting
        })
        .catch(error => {
            if (error.username && error.username.length > 0) {
                messageBox.textContent = 'Registration failed. Error: ' + error.username[0];
            } else {
                messageBox.textContent = 'Registration failed. Error: ' + error;
            }
            messageBox.style.display = 'block';  // make it visible
            messageBox.classList.add('error');
        });
    });

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
});
