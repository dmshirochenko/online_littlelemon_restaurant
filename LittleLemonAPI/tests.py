import os
from dotenv import load_dotenv

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer
from .views import GroupViewSet, DeliveryCrewViewSet

load_dotenv()


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


class GroupViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username=os.environ.get("TEST_USERNAME", "admin"),
            email="",
            password=os.environ.get("TEST_SUPERUSER_PASSWORD", "admin"),
        )
        self.client.force_authenticate(user=self.admin_user)

        self.managers_group = Group.objects.create(name="Managers")
        self.manager_1 = User.objects.create_user(username="manager_1", password="some_password")
        self.managers_group.user_set.add(self.manager_1)

    def test_list(self):
        url = reverse("manage_managers")
        response = self.client.get(url, format="json")
        users = User.objects.filter(groups__name="Managers")
        serializer = UserSerializer(users, many=True)
        # Extract usernames from serializer.data
        expected_usernames = [d["username"] for d in serializer.data]
        # Extract usernames from response.data
        response_usernames = [d["username"] for d in response.data]
        self.assertEqual(expected_usernames, response_usernames)

    def test_create(self):
        url = reverse("manage_managers")
        data = {"username": "manager_1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "user added to the manager group")

    def test_destroy(self):
        url = reverse("manage_managers")
        data = {"username": "manager_1"}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "user removed from the manager group")


class DeliveryCrewViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create manager and login
        self.managers_group = Group.objects.create(name="Managers")
        self.manager_2 = User.objects.create_user(username="manager_2", password="some_password")
        self.managers_group.user_set.add(self.manager_2)
        self.client.force_authenticate(user=self.manager_2)

        # create deliveryman
        self.delivery_group = Group.objects.create(name="Delivery_Crew")
        self.deliveryman = User.objects.create_user(username="deliveryman_1", password="some_password")
        self.delivery_group.user_set.add(self.deliveryman)

    def test_list(self):
        url = reverse("manage_delivery_crew")
        response = self.client.get(url)
        users = User.objects.filter(groups__name="Delivery_Crew")
        serializer = UserSerializer(users, many=True)
        # Extract usernames from serializer.data
        expected_usernames = [d["username"] for d in serializer.data]
        # Extract usernames from response.data
        response_usernames = [d["username"] for d in response.data]
        self.assertEqual(expected_usernames, response_usernames)

    def test_create(self):
        url = reverse("manage_delivery_crew")
        data = {"username": "deliveryman_1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "user added to the delivery crew group")

    def test_destroy(self):
        url = reverse("manage_delivery_crew")
        data = {"username": "deliveryman_1"}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "user removed from the delivery crew group")
