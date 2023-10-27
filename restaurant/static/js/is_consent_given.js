document.addEventListener("DOMContentLoaded", function() {
    // Check if consent is given or declined
    if (document.cookie.split(';').some((item) => {
        const [name, value] = item.trim().split("=");
        return name === "consent_given" && (value === "true" || value === "false");
    })) {
        // Hide the consent banner
        document.getElementById("cookie-consent-banner").style.display = 'none';
    }
  
    // Handle user consent for Accept
    const consentButton = document.getElementById("consent-button");
    if (consentButton) {
      consentButton.addEventListener("click", function() {
        document.cookie = "consent_given=true; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/; Secure; SameSite=Strict";
        document.getElementById("cookie-consent-banner").style.display = 'none';
      });
    }
  
    // Handle user consent for Decline
    const declineButton = document.getElementById("decline-button");
    if (declineButton) {
      declineButton.addEventListener("click", function() {
        document.cookie = "consent_given=false; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/; Secure; SameSite=Strict";
        document.getElementById("cookie-consent-banner").style.display = 'none';
      });
    }
  });
  