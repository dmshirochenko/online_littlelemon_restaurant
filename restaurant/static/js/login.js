document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");

    function getCSRFToken() {
        return document.getElementsByName("csrfmiddlewaretoken")[0].value;
    }

    function getUserCredentials() {
        return {
            username: document.getElementById("email").value,
            password: document.getElementById("password").value
        };
    }

    function handleAPIError(response) {
        if (response && response.non_field_errors) {
            if (response.non_field_errors.includes("Unable to log in with provided credentials.")) {
                return "The username or password you entered is incorrect. Please try again.";
            }
        }
        return "An unexpected error occurred. Please try again later.";
    }

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const { username, password } = getUserCredentials();
            const csrfToken = getCSRFToken();

            const data = {
                username,
                password,
                csrfmiddlewaretoken: csrfToken
            };

            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify(data)
            };

            const response = await fetch("/auth/token/login/", requestOptions);

            if (!response.ok) {
                const errorResponse = await response.json();
                const message = handleAPIError(errorResponse);
                throw new Error(message);
            }

            const result = await response.json();
            const homeUrl = document.getElementById('homeUrl').value;

            if (result.auth_token) {
                sessionStorage.setItem('token', result.auth_token);
                
                const clientBasket = localStorage.getItem('clientBasket') || null;
                console.log("Basket = ",  clientBasket)
                if(clientBasket){
                try {
                    const basketData = await saveBasket(result.auth_token, clientBasket);
                    console.log('Basket saved successfully', basketData);
                } catch (error) {
                    console.error('Failed to save basket:', error);
                }
                };
                showMessage("Successfully logged in", "success");
                

                setTimeout(() => {
                    window.location.href = homeUrl;
                }, 2000);
            } else {
                showMessage("Invalid credentials", "error");
            }
        } catch (error) {
            showMessage(error.message, "error");
        }
    });

    async function saveBasket(authToken, clientBasket) {
        const csrfToken = getCSRFToken();  // Added const here
    
        try {
            const response = await fetch('/api/sync-cart', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${authToken}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    clientBasket: JSON.parse(localStorage.getItem('clientBasket') || '[]'),
                }),
            });
    
            if (!response.ok) {
                throw new Error('Basket saving failed');
            }
    
            localStorage.removeItem('clientBasket');
            return await response.json();
    
        } catch (error) {
            console.error('An error occurred:', error);
            throw error;
        }
    }
    

    function showMessage(message, type) {
        const messageBox = document.getElementById("message");
        // Clear previous classes
        messageBox.classList.remove("error", "success");
        // Add the new class
        messageBox.classList.add(type);

        messageBox.style.display = "block";
        messageBox.innerHTML = message;
    }
});
