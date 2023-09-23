from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class CategoriesViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Category.objects.create(title="Category1", slug="category1")
        Category.objects.create(title="Category2", slug="category2")

    def test_list_categories(self):
        url = reverse("category_list")
        response = self.client.get(url)
        categories = Category.objects.all().order_by("id")
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MenuItemListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        category = Category.objects.create(title="Category1", slug="category1")
        MenuItem.objects.create(title="Item1", price="10.00", featured=False, category=category)
        MenuItem.objects.create(title="Item2", price="20.00", featured=False, category=category)

    def test_list_menu_items(self):
        url = reverse("menu_item_list")
        response = self.client.get(url)
        menu_items = MenuItem.objects.all().order_by("id")
        serializer = MenuItemSerializer(menu_items, many=True)
        self.assertEqual(response.data["results"], serializer.data)  # Considering pagination
        self.assertEqual(response.status_code, status.HTTP_200_OK)
