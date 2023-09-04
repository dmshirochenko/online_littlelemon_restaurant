# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu


# Create your views here.
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
    context = {"form": form}
    return render(request, "book.html", context)


# Add your code here to create new views


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
