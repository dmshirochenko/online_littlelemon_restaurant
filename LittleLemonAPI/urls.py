from django.urls import path
from . import views

urlpatterns = [
    path("menu-items", views.MenuItemListView.as_view(), name="menu_item_list"),
    path("categories", views.CategoriesView.as_view(), name="category_list"),
    path("menu-items/<int:pk>", views.MenuItemDetailView.as_view(), name="menu_item_detail"),
    path("item-of-the-day/update/<int:pk>", views.UpdateItemOfTheDayView.as_view(), name="update_item_of_day"),
    path("cart/menu-items", views.CartOperationsView.as_view(), name="cart_operations"),
    path("orders", views.OrderOperationsView.as_view(), name="order_operations"),
    path("orders/<int:pk>", views.SingleOrderView.as_view(), name="single_order_view"),
    path("orders/assign", views.AssignOrderToDeliveryCrewView.as_view(), name="assign_order"),
    path("orders/mark-delivered/<int:pk>", views.MarkOrderDeliveredView.as_view(), name="mark_order_delivered"),
    path(
        "groups/manager/users",
        views.GroupViewSet.as_view({"get": "list", "post": "create", "delete": "destroy"}),
        name="manage_managers",
    ),
    path(
        "groups/delivery-crew/users",
        views.DeliveryCrewViewSet.as_view({"get": "list", "post": "create", "delete": "destroy"}),
        name="manage_delivery_crew",
    ),
]
