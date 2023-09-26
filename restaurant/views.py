import json
from datetime import datetime

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import BookingForm
from .models import Menu, Booking


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # Check for AJAX
                return JsonResponse({"success": True})
    context = {"form": form}
    return render(request, "book.html", context)


def reservation(request):
    return render(request, "reservation.html")


def menu(request):
    menu_data = Menu.objects.all()  # Fetch all menu items from the database
    main_data = {"menu": menu_data}  # Create dictionary with key-value pair

    return render(request, "menu.html", main_data)  # Render menu.html template with main_data


def display_menu_items(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)  # Retrieve menu item by primary key
    else:
        menu_item = ""  # Empty string if no primary key is provided

    return render(request, "menu_item.html", {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exist = (
            Booking.objects.filter(reservation_date=data["reservation_date"])
            .filter(reservation_slot=data["reservation_slot"])
            .exists()
        )
        if exist is False:
            booking = Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type="application/json")

    date = request.GET.get("date", datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize("json", bookings)

    return HttpResponse(booking_json, content_type="application/json")
