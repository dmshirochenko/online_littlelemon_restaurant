from django.db.models import F

from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from .permissions import IsManager, IsDeliveryCrew
from .models import MenuItem, Category, Order, OrderItem, Cart
from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    UserSerilializer,
    OrderSerializer,
    CartSerializer,
    OrderItemSerializer,
)


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "category__title"]
    filterset_fields = ["price", "category"]
    search_fields = ["title"]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
            )

        category_id = request.data.get("category", None)

        if not Category.objects.filter(id=category_id).exists():
            return Response({"detail": "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class UpdateItemOfTheDayView(generics.UpdateAPIView):
    permission_classes = [IsManager]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_item_of_the_day = True
        instance.save()
        return Response({"message": "Item of the day updated"}, status=status.HTTP_200_OK)


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


class CartOperationsView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related("menuitem")

    def post(self, request, *args, **kwargs):
        menu_item_id = request.data.get("menuitem")
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)

        unit_price = float(menu_item.price)
        quantity = int(request.data.get("quantity"))

        # Find existing basket item
        existing_item = Cart.objects.filter(user=request.user.id, menuitem=menu_item.id).first()

        if existing_item:
            # Update existing item
            existing_item.quantity = F("quantity") + quantity  # Using F() for atomic update
            existing_item.save(update_fields=["quantity"])
            existing_item.refresh_from_db()

            # Now update price based on updated quantity
            existing_item.price = existing_item.unit_price * existing_item.quantity
            existing_item.save(update_fields=["price"])

            # Reload to get updated values
            existing_item.refresh_from_db()

            serializer = self.serializer_class(existing_item)
        else:
            # Create new basket item
            total_price = unit_price * quantity
            data = {
                "user": request.user.id,
                "menuitem": menu_item.id,
                "quantity": quantity,
                "unit_price": unit_price,
                "price": total_price,
            }

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem')

        if not menuitem_id:
            return Response({"error": "menuitem_id not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter based on user and menuitem
        cart_item = Cart.objects.filter(user=self.request.user, menuitem_id=menuitem_id)

        if not cart_item.exists():
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Item has been deleted"}, status=status.HTTP_200_OK)


class OrderOperationsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count() == 0:  # normal customer - no group
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name="Delivery_Crew").exists():  # delivery crew
            return Order.objects.all().filter(delivery_crew=self.request.user)  # only show oreders assigned to him
        else:  # delivery crew or manager
            return Order.objects.all()

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, id=self.kwargs["pk"])


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        users = User.objects.all().filter(groups__name="Managers")
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data["username"])
        managers = Group.objects.get(name="Managers")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data["username"])
        managers = Group.objects.get(name="Managers")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)


class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = User.objects.all().filter(groups__name="Delivery_Crew")
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        # only for super admin and managers
        if self.request.user.is_superuser is False:
            if not self.request.user.groups.filter(name="Managers").exists():
                return Response({"message": "forbidden"}, status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, username=request.data["username"])
        dc = Group.objects.get(name="Delivery_Crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        # only for super admin and managers
        if self.request.user.is_superuser is False:
            if not self.request.user.groups.filter(name="Managers").exists():
                return Response({"message": "forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data["username"])
        dc = Group.objects.get(name="Delivery_Crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)
