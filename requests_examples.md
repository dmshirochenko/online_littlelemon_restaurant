Endpoints and Request Examples
1. CategoriesView
Endpoint: GET /categories
Example Request: curl -X GET http://localhost:8000/api/categories/

2. MenuItemListView
Endpoint: GET /menu-items
Example Request: curl -X GET http://localhost:8000/api/menu-items/

3. MenuItemDetailView
Endpoint: GET /menu-items/<int:pk>
Example Request: curl -X GET http://localhost:8000/api/menu-items/1/

4. ManagersListView
Endpoint: GET /groups/managers/users
Example Request: curl -X GET http://localhost:8000/api/groups/managers/users/

5. ManagersRemoveView
Endpoint: DELETE /groups/managers/users/<int:pk>
Example Request: curl -X DELETE http://localhost:8000/api/groups/managers/users/1/

6. DeliveryCrewListView
Endpoint: GET /groups/delivery-crew/users
Example Request: curl -X GET http://localhost:8000/api/groups/delivery-crew/users/

7. DeliveryCrewRemoveView
Endpoint: DELETE /groups/delivery-crew/users/<int:pk>
Example Request: curl -X DELETE http://localhost:8000/api/groups/delivery-crew/users/1/

8. UpdateItemOfTheDayView
Endpoint: PUT /item-of-the-day/update/<int:pk>
Example Request: curl -X PUT http://localhost:8000/api/item-of-the-day/update/1/

9. AssignUserToDeliveryCrewView
Endpoint: PUT /groups/delivery-crew/assign/<int:pk>
Example Request: curl -X PUT http://localhost:8000/api/groups/delivery-crew/assign/1/

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
curl -X PUT http://localhost:8000/api/orders/assign/ -d '{"user_id": 1, "order_id": 42}' -H "Content-Type: application/json"

11. OrdersAssignedToDeliveryCrewView
CURL
bash
Copy code
curl -X GET "http://localhost:8000/api/api/orders/delivery-crew/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Postman
Method: GET
URL: http://localhost:8000/api/api/orders/delivery-crew/
Headers:
Key: Authorization, Value: Bearer YOUR_ACCESS_TOKEN

12. MarkOrderDeliveredView
CURL
bash
Copy code
curl -X PUT "http://localhost:8000/api/api/orders/mark-delivered/1/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Postman
Method: PUT
URL: http://localhost:8000/api/api/orders/mark-delivered/1/ (replace 1 with the order ID you want to mark as delivered)
Headers:
Key: Authorization, Value: Bearer YOUR_ACCESS_TOKEN