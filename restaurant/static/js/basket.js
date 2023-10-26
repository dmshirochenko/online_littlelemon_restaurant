// After rendering all items, bind the event listeners
function bindEventListeners() {
    document.querySelectorAll('.minus-button').forEach(button => {
        button.addEventListener('click', function() {
            const item = {
                menuitem: this.dataset.menuitem,
                unit_price: this.dataset.unitPrice,
            };
            updateQuantity('decrement', item);
        });
    });

    document.querySelectorAll('.plus-button').forEach(button => {
        button.addEventListener('click', function() {
            const item = {
                menuitem: this.dataset.menuitem,
                unit_price: this.dataset.unitPrice,
            };
            updateQuantity('increment', item);
        });
    });

    // Add event listener for delete-button
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
        const menuitemId = this.dataset.menuitem;
        deleteMenuItem(menuitemId);
        });
    });
}

//function to calculate Overall Value
function calculateOverallValue() {
    let overallValue = 0;

    // Use a more specific selector to match the ID pattern
    let items = document.querySelectorAll('[id^="totalPrice_"]'); 

    items.forEach(item => {
        let priceText = item.textContent.replace('Total Price per unit: $', '');
        let price = parseFloat(priceText);
        
        // Check if price is a valid number before adding to overallValue
        if (!isNaN(price)) {
            overallValue += price;
        }
    });

    if (!isNaN(overallValue) && overallValue > 0) {
        document.getElementById('overallValue').textContent = 'Overall Value: $' + overallValue.toFixed(2);
    } else {
        document.getElementById('overallValue').textContent = ''; // Reset to empty if overallValue is NaN or 0
    }
}


// Function to render basket items on the page
function renderBasketItems(basketItems) {
    const basketContainer = document.getElementById('basket-container');
    basketItems.forEach(item => {
        const basketItem = document.createElement('div');

        basketItem.className = "basket-item";
        basketItem.id = `basket_item_${item.menuitem}`;
        basketItem.innerHTML = formatBasketData(item);
        
        // Update href for the menu item link
        const menuItemLink = basketItem.querySelector(`#menuitem_${item.menuitem}`);
        const baseUrl = menuItemLink.getAttribute('data-base-url');
        menuItemLink.href = baseUrl.slice(0, -2) + item.menuitem_details.id + '/';
        
        basketContainer.appendChild(basketItem);
    });
}

function transformLocalData(data) {
    return data.map(item => {
        return {
            menuitem: item.menuitem,
            menuitem_details: {
                title: item.title,
                id: item.menuitem  // assuming menuitem contains the id
            },
            unit_price: item.unit_price,
            quantity: item.quantity,
            price: item.price
        };
    });
}

function fetchBasket() {
    if (sessionStorage.getItem('token')) {
        const authToken = sessionStorage.getItem('token');
        fetch('/api/cart/menu-items', {
            method: 'GET',
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            renderBasketItems(data.results);
        })
        .catch(error => {
            console.error('Error fetching cart:', error);
        });
    } else {
        const localBasket = localStorage.getItem('clientBasket') ? JSON.parse(localStorage.getItem('clientBasket')) : [];
        const transformedLocalBasket = transformLocalData(localBasket);
        renderBasketItems(transformedLocalBasket);
    }
}

async function updateQuantity(action, item) {
    const quantityDisplay = document.getElementById('quantity_' + item.menuitem);
    let quantity = parseInt(quantityDisplay.textContent);

    // Assuming you have the unit_price available in the item object
    let unitPrice = parseFloat(item.unit_price); 

    try {
        if (action === 'decrement' && quantity > 1) {
            quantity--;
            let response = await updateBasket(action, item);
            if (!response) {
                return;
            }
        } else if (action === 'increment') {
            quantity++;
            let response = await updateBasket(action, item);
            if (!response) {
                return;
            }
        }

        // Calculate the updated total price for the item
        let updatedTotalPrice = quantity * unitPrice;

        // Update the DOM elements
        quantityDisplay.textContent = quantity;
        const totalPriceDisplay = document.getElementById('totalPrice_' + item.menuitem);
        totalPriceDisplay.textContent = 'Total Price per unit: $' + updatedTotalPrice.toFixed(2);

        // Update the item object
        item.quantity = quantity;
        item.price = updatedTotalPrice;

        // Recalculate the overall value
        calculateOverallValue();
    } catch (error) {
        console.error("Error in updateQuantity:", error);
    }
}


async function updateBasket(action, item) {
    const authToken = sessionStorage.getItem('token');
    item.menuitem = parseInt(item.menuitem, 10);
    let quantity_diff = 0;

    if (action === 'decrement') {
        quantity_diff = -1;
    } else if (action === 'increment') {
        quantity_diff = 1;
    }

    if (authToken) {
        // Authenticated User: Add to server-side basket
        try {
            const response = await fetch(cartUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${authToken}`,
                    'Content-Type': 'application/json',
                    // 'X-CSRFToken': csrfToken   // if you need CSRF token
                },
                body: JSON.stringify({ menuitem: item.menuitem, quantity: quantity_diff })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.message);
            }

            const data = await response.json();
            // Handle authenticated user response
            return true; // Return true if everything went well
        } catch (error) {
            showMessage(item.menuitem, "Item has not been updated", "error");
            return false; // Return false if any error occurred
        }
    } else {
        let clientBasket = JSON.parse(localStorage.getItem('clientBasket')) || [];
        const existingItem = clientBasket.find(existing => existing.menuitem === item.menuitem);

        if (existingItem) {
            existingItem.quantity += quantity_diff; // Add the new selected quantity to the existing item
            existingItem.price = existingItem.unit_price * existingItem.quantity; // Update total price
        } else {
            clientBasket.push(item);
        }

        localStorage.setItem('clientBasket', JSON.stringify(clientBasket));
        return true; // Assuming success for the client-side basket update
    }
}


function waitForElement(selector, callback) {
    if (document.querySelector(selector)) {
        callback();
    } else {
        setTimeout(function() {
            waitForElement(selector, callback);
        }, 100);
    }
}

function deleteMenuItem(menuitemId) {
    const authToken = sessionStorage.getItem('token');
    if (authToken) {
        // For authenticated users: Make a DELETE request
        fetch(cartUrl, {
            method: 'DELETE',
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ menuitem: menuitemId })
        })
        .then(response => {
            if (response.status === 200) {
                const basketItem = document.getElementById(`basket_item_${menuitemId}`);
                    if (basketItem) {
                        basketItem.remove();
                    }
                    calculateOverallValue();
                    hideOrderButtonIfNoItems();
            } else {
                // Handle error
                console.error("Error deleting the item.");
                showMessage(menuitemId, "Error deleting the item.", "error");
                
            }
        });
    } else {
        // For non-auth users: Remove from localStorage
        let cart = JSON.parse(localStorage.getItem('clientBasket') || '[]');
        cart = cart.filter(item => item.menuitem !== parseInt(menuitemId));
        localStorage.setItem('clientBasket', JSON.stringify(cart));

        const basketItem = document.getElementById(`basket_item_${menuitemId}`);
                    if (basketItem) {
                        basketItem.remove();
                    }
                    
        calculateOverallValue();
    }
}

function showMessage(menuitemId, message, type) {
    const messageBox = document.getElementById("message_" + menuitemId);
    
    // Clear previous 'error' and 'success' classes
    messageBox.classList.remove("error", "success");
    
    // Add the new type class
    messageBox.classList.add(type);
    
    // Display the message
    messageBox.style.display = "block";
    messageBox.innerHTML = message;

    // Hide the message after 3 seconds
    setTimeout(() => {
        messageBox.style.display = "none";
    }, 3000);
}

async function placeOrder() {
    const today = new Date();
    const formattedDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    const payload = {
        date: formattedDate
    };

    const authToken = sessionStorage.getItem('token');

    try {
        const response = await fetch(orderUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            const data = await response.json();
            // On success, redirect to the confirmation page
            window.location.href = confirmationUrl;
        } else {
            const errorData = await response.json();
            // Handle and show error
            console.error('Order failed:', errorData.message);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

function hideOrderButtonIfNoItems() {
    const authToken = sessionStorage.getItem('token');
    const emptyMessage = document.querySelector('.empty-cart-message');
    const orderButton = document.querySelector('#orderButton');
    if(authToken){
    // Initialize MutationObserver
    const observer = new MutationObserver(() => {
      const items = document.querySelectorAll('.basket-item');
      if (items.length === 0 && orderButton) {
        orderButton.style.display = 'none';
        emptyMessage.style.display = 'block';
      } else {
        orderButton.style.display = 'block';
        emptyMessage.style.display = 'none';
      }
    });
  
    // Configuration of the observer
    const config = { childList: true, subtree: true };
  
    // Target node to observe
    const targetNode = document.body;
  
    // Observe target
    observer.observe(targetNode, config);
  
    // Disconnect after 5 seconds
    setTimeout(() => {
      observer.disconnect();
    }, 5000);
    }
  }
  

document.addEventListener('DOMContentLoaded', () => {
    fetchBasket();
    waitForElement('.component-container', function() {
        bindEventListeners();
        calculateOverallValue();
        
    });
    //Check if order button is needed
    hideOrderButtonIfNoItems();
    // Adding event listener to the "Order" button
    const orderButton = document.querySelector('.order-button');
    if (orderButton) {
        orderButton.addEventListener('click', placeOrder);
    }
    
});