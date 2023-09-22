from django.urls import path
from . import views

urlpatterns = [
    path("menu-items", views.MenuItemListView.as_view()),
    path("categories", views.CategoriesView.as_view()),
    path("menu-items/<int:pk>", views.MenuItemDetailView.as_view()),
    path("item-of-the-day/update/<int:pk>", views.UpdateItemOfTheDayView.as_view()),
    path("cart/menu-items", views.CartOperationsView.as_view()),
    path("orders", views.OrderOperationsView.as_view()),
    path("orders/<int:pk>", views.SingleOrderView.as_view()),
    path("orders/assign", views.AssignOrderToDeliveryCrewView.as_view()),
    path("orders/mark-delivered/<int:pk>", views.MarkOrderDeliveredView.as_view()),
    path("groups/manager/users", views.GroupViewSet.as_view({"get": "list", "post": "create", "delete": "destroy"})),
    path(
        "groups/delivery-crew/users",
        views.DeliveryCrewViewSet.as_view({"get": "list", "post": "create", "delete": "destroy"}),
    ),
]
