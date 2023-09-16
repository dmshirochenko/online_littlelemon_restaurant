from rest_framework import generics
from rest_framework import permissions
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer
from django.contrib.auth.models import User, Group


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
        managers_group = Group.objects.get(name='Managers')
        return User.objects.filter(groups=managers_group)

class ManagersRemoveView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        managers_group = Group.objects.get(name='Managers')
        instance.groups.remove(managers_group)
        
class DeliveryCrewListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        delivery_group = Group.objects.get(name='Delivery_Crew')
        return User.objects.filter(groups=delivery_group)

class DeliveryCrewRemoveView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        delivery_group = Group.objects.get(name='Delivery_Crew')
        instance.groups.remove(delivery_group)  