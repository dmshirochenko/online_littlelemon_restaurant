from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservation, name="reservations"),
    path("basket/", views.basket, name="basket"),
    path("confirmation/", views.confirmation, name="order_confirmation_page"),
    path("privacy-policy/", views.privacy_policy_page, name="private_policy_page"),
    # Add the remaining URL path configurations here
    path("menu/", views.menu, name="menu"),
    path("menu_item/<int:pk>/", views.display_menu_items, name="menu_item"),
    path("menu_item/", views.display_menu_items, name="menu_item_no_pk"),
    # Bookings
    path("bookings/", views.bookings, name="bookings"),
    # Registration form
    path('register/', views.register, name='register'),
    # Login form
    path('login/', views.user_login, name='user_login'),
]
