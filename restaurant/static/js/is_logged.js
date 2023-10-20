document.addEventListener("DOMContentLoaded", () => {
    const userInfoLi = document.getElementById("user-info");
    const registerUrl = document.getElementById("register-url").textContent;
    const loginUrl = document.getElementById("login-url").textContent;
    const logoutUrl = document.getElementById("logout-url").textContent;

    const token = sessionStorage.getItem('token');

    if (token) {
      userInfoLi.innerHTML = `<span>Logged In</span> | <a href="${logoutUrl}" id="logout-link">Log Out</a>`;
      document.getElementById("logout-link").addEventListener("click", function(event){
        event.preventDefault();
        logout();
      });
    } else {
      userInfoLi.innerHTML = `<a href="${registerUrl}">Register</a> / <a href="${loginUrl}">Login</a>`;
    }
});

function logout() {
    const logoutEndpoint = document.getElementById("logout-url").textContent;

    fetch(logoutEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + sessionStorage.getItem('token')
        }
    })
    .then(response => {
        if (response.status === 204) {
            sessionStorage.removeItem('token');
            window.location.href = '/login/'; 
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.detail) {
            console.error('Error:', data.detail);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
