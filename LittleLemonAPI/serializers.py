from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

    def create(self, validated_data):
        category_id = validated_data.get("category", None)
        if category_id:
            try:
                Category.objects.get(id=category_id.id)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": "Category does not exist"})
        return MenuItem.objects.create(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    menuitem_details = MenuItemSerializer(source="menuitem", read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "quantity", "unit_price", "price", "user", "menuitem", "menuitem_details"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "groups"]


class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
