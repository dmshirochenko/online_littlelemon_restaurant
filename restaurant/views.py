import json
from datetime import datetime

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .forms import BookingForm
from .models import Booking
from LittleLemonAPI.models import MenuItem


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def basket(request):
    return render(request, "basket.html")


def confirmation(request):
    return render(request, "confirmation.html")


def register(request):
    return render(request, 'registration.html')


def user_login(request):
    return render(request, 'login.html')


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
    menu_data = MenuItem.objects.all()
    main_data = {"menu": menu_data}
    return render(request, "menu.html", main_data)


def display_menu_items(request, pk=None):
    if pk:
        menu_item = MenuItem.objects.get(pk=pk)
    else:
        menu_item = ""
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
