from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from .permissions import IsManager, IsDeliveryCrew, IsCustomer
from .models import MenuItem, Category, Order, OrderItem, Cart
from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    UserSerializer,
    OrderSerializer,
    CartSerializer,
    OrderItemSerializer,
)


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "category__title"]
    filterset_fields = ["price", "category"]
    search_fields = ["title"]


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class ManagersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        managers_group = Group.objects.get(name="Managers")
        return User.objects.filter(groups=managers_group)


class ManagersRemoveView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        managers_group = Group.objects.get(name="Managers")
        instance.groups.remove(managers_group)


class DeliveryCrewListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        delivery_group = Group.objects.get(name="Delivery_Crew")
        return User.objects.filter(groups=delivery_group)


class DeliveryCrewRemoveView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        delivery_group = Group.objects.get(name="Delivery_Crew")
        instance.groups.remove(delivery_group)


class UpdateItemOfTheDayView(generics.UpdateAPIView):
    permission_classes = [IsManager]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_item_of_the_day = True
        instance.save()
        return Response({"message": "Item of the day updated"}, status=status.HTTP_200_OK)


class AssignUserToDeliveryCrewView(generics.UpdateAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        delivery_group = Group.objects.get(name="Delivery Crew")
        user.groups.add(delivery_group)
        user.save()
        return Response({"message": "User assigned to Delivery Crew"}, status=status.HTTP_200_OK)


class AssignOrderToDeliveryCrewView(generics.UpdateAPIView):
    permission_classes = [IsManager]
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        order_id = request.data.get("order_id")

        if not user_id or not order_id:
            return Response({"error": "Both user_id and order_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        order = get_object_or_404(Order, id=order_id)

        order.assigned_to = user
        order.save()

        return Response(
            {"message": f"Order {order.id} assigned to Delivery Crew member {user.username}"}, status=status.HTTP_200_OK
        )


class OrdersAssignedToDeliveryCrewView(generics.ListAPIView):
    permission_classes = [IsDeliveryCrew]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(assigned_to=self.request.user)


class MarkOrderDeliveredView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsDeliveryCrew]

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if order.assigned_to == request.user:
            order.is_delivered = True
            order.save()
            return Response({"message": "Order marked as delivered"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "You are not authorized to mark this order as delivered"}, status=status.HTTP_403_FORBIDDEN
            )


# Feature 18 & 19: Cart Operations
class CartOperationsView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        menu_item_id = request.data.get("menuitem")
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        data = {
            "user": request.user.id,
            "menuitem": menu_item.id,
            "quantity": request.data.get("quantity"),
            "unit_price": menu_item.price,
            "price": menu_item.price * int(request.data.get("quantity")),
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Feature 20 & 21: Order Operations
class OrderOperationsView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum([item.price for item in cart_items])
        order_data = {
            "user": request.user.id,
            "status": False,
            "total": total_price,
            "date": request.data.get("date", None),
        }

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()

            # Convert cart items to order items
            order_items = []
            for cart_item in cart_items:
                order_items.append(OrderItem(order=order, menuitem=cart_item.menuitem, quantity=cart_item.quantity))

            OrderItem.objects.bulk_create(order_items)

            # Clear the cart
            cart_items.delete()

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleOrderView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, id=self.kwargs["pk"])
