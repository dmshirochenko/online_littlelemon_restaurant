document.addEventListener("DOMContentLoaded", function() {
    if (document.cookie.split(';').some((item) => item.trim() === 'consent_given=true')) {
      const gtmBodyNoScript = document.createElement("noscript");
      gtmBodyNoScript.innerHTML = `<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K7R9NVBX" height="0" width="0" style="display:none;visibility:hidden"></iframe>`;
      document.body.insertBefore(gtmBodyNoScript, document.body.firstChild);
    }
  });
  