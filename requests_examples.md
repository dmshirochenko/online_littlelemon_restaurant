Endpoints and Request Examples
1. CategoriesView
Endpoint: GET /categories
Example Request: curl -X GET http://localhost:8000/api/api/categories/

2. MenuItemListView
Endpoint: GET /menu-items
Example Request: curl -X GET http://localhost:8000/api/api/menu-items/

3. MenuItemDetailView
Endpoint: GET /menu-items/<int:pk>
Example Request: curl -X GET http://localhost:8000/api/api/menu-items/1/

4. ManagersListView
Endpoint: GET /groups/managers/users
Example Request: curl -X GET http://localhost:8000/api/api/groups/managers/users/

5. ManagersRemoveView
Endpoint: DELETE /groups/managers/users/<int:pk>
Example Request: curl -X DELETE http://localhost:8000/api/api/groups/managers/users/1/

6. DeliveryCrewListView
Endpoint: GET /groups/delivery-crew/users
Example Request: curl -X GET http://localhost:8000/api/api/groups/delivery-crew/users/

7. DeliveryCrewRemoveView
Endpoint: DELETE /groups/delivery-crew/users/<int:pk>
Example Request: curl -X DELETE http://localhost:8000/api/api/groups/delivery-crew/users/1/

8. UpdateItemOfTheDayView
Endpoint: PUT /item-of-the-day/update/<int:pk>
Example Request: curl -X PUT http://localhost:8000/api/api/item-of-the-day/update/1/

9. AssignUserToDeliveryCrewView
Endpoint: PUT /groups/delivery-crew/assign/<int:pk>
Example Request: curl -X PUT http://localhost:8000/api/api/groups/delivery-crew/assign/1/

10. AssignOrderToDeliveryCrewView
Endpoint: PUT /orders/assign/
JSON Payload:

json
Copy code
{
  "user_id": 1,
  "order_id": 42
}
Example Request:

bash
Copy code
curl -X PUT http://localhost:8000/api/api/orders/assign/ -d '{"user_id": 1, "order_id": 42}' -H "Content-Type: application/json"

11. OrdersAssignedToDeliveryCrewView
CURL
bash
Copy code
curl -X GET "http://localhost:8000/api/api/api/orders/delivery-crew/" -H "Authorization: Token YOUR_ACCESS_TOKEN"
Postman
Method: GET
URL: http://localhost:8000/api/api/api/orders/delivery-crew/
Headers:
Key: Authorization, Value: Token YOUR_ACCESS_TOKEN

12. MarkOrderDeliveredView
CURL
bash
Copy code
curl -X PUT "http://localhost:8000/api/api/api/orders/mark-delivered/1/" -H "Authorization: Token YOUR_ACCESS_TOKEN"
Postman
Method: PUT
URL: http://localhost:8000/api/api/api/orders/mark-delivered/1/ (replace 1 with the order ID you want to mark as delivered)
Headers:
Key: Authorization, Value: Token YOUR_ACCESS_TOKEN


13. Add Menu Item to Cart (Feature 18)
Endpoint: /cart/menu-items/
Method: POST

cURL:

bash
Copy code
curl -X POST "http://localhost:8000/api/cart/menu-items/" \
     -H "Authorization: Token YOUR_ACCESS_TOKEN" \
     -d "menuitem=1" \
     -d "quantity=2"

14. Access Previously Added Items in Cart (Feature 19)
Endpoint: /cart/menu-items/
Method: GET

cURL:

bash
Copy code
curl -X GET "http://localhost:8000/api/cart/menu-items/" \
     -H "Authorization: Token YOUR_ACCESS_TOKEN"

15. Place an Order (Feature 20)
Endpoint: /orders/
Method: POST

cURL:

bash
Copy code
curl -X POST "http://localhost:8000/api/orders/" \
     -H "Authorization: Token YOUR_ACCESS_TOKEN" \
     -d "date=2023-09-14"

16. Browse Their Own Orders (Feature 21)
Endpoint: /orders/
Method: GET

cURL:

bash
Copy code
curl -X GET "http://localhost:8000/api/orders/" \
     -H "Authorization: Token YOUR_ACCESS_TOKEN"
Make sure to replace YOUR_ACCESS_TOKEN with the actual access token for authenticated users. The cURL commands assume you're running your development server on localhost at port 8000. Modify the URLs accordingly if your setup is different.