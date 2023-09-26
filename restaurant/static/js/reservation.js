// Get elements
const datePicker = document.getElementById('datePicker');
const fetchButton = document.getElementById('fetchButton');
const jsonOutput = document.getElementById('jsonOutput');

// Set today's date as default
const today = new Date();
const day = String(today.getDate()).padStart(2, '0');
const month = String(today.getMonth() + 1).padStart(2, '0');
const year = today.getFullYear();

datePicker.value = `${year}-${month}-${day}`;

// Event listener for fetchButton
fetchButton.addEventListener('click', function() {
  const selectedDate = datePicker.value;
  const bookingUrl = document.getElementById('bookingUrl').value;

  if (!selectedDate) {
    alert('Please select a date.');
    return;
  }

  fetch(`${bookingUrl}?date=${selectedDate}`)
    .then(response => response.json())
    .then(data => {
      const rawJSON = JSON.stringify(data, null, 2);
      const preTag = `<pre>${rawJSON}</pre>`;
      jsonOutput.innerHTML = preTag;
    })
    .catch(error => {
      console.error('Error fetching bookings:', error);
    });
});
