from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from .permissions import IsManager, IsDeliveryCrew
from .models import MenuItem, Category, Order
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, OrderSerializer


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
