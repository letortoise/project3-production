from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers
from .models import MenuItem, Pizza, Order, OrderItem, Extra
import json
from json import JSONDecodeError


# Create your views here.
def index(request):
    print(request.user)
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    return HttpResponseRedirect(reverse("menu"))

def menu(request):

    # Prepare menu data for templating
    menu = [
        ("Regular Pizza", Pizza.objects.filter(type="Regular Pizza").all()),
        ("Sicilian Pizza", Pizza.objects.filter(type="Sicilian Pizza").all()),
        ("Subs",MenuItem.objects.filter(type="Sub").all()),
        ("Pasta", MenuItem.objects.filter(type="Pasta").all()),
        ("Salad", MenuItem.objects.filter(type="Salad").all()),
        ("Dinner Platters", MenuItem.objects.filter(type="Dinner Platter").all())
    ]

    context = {
        "menu": menu
    }
    return render(request, "orders/menu.html", context)

def cart(request):
    return render(request, "orders/cart.html")

def submitOrder(request):

    try:
        # Get information from XHR
        cartText = request.POST["cart"]
        cart = json.loads(cartText)
        print(cart)

        # Create order in database
        order = Order(user=request.user)
        order.save()

        # Create order items for each cart item
        for cartItem in cart:
            item = MenuItem.objects.get(pk=cartItem["id"])
            order_item = OrderItem(order=order, item=item, cost=0)
            size = cartItem.get("size")
            if size:
                order_item.size = size
            order_item.save()

            # Add extras to order
            extras = cartItem.get("extras")
            if extras:
                for extra in extras:
                    order_item.extras.add(Extra.objects.filter(name=extra["name"]).first())




    except KeyError:
        print("no such key")
        return JsonResponse({"success": False})
    except MenuItem.DoesNotExist:
        print("no such menu item")
        return JsonResponse({"success": False})
    except JSONDecodeError:
        print("invalid JSON document")
        return JsonResponse({"success": False})



    return JsonResponse({"success": True})

def lookupExtras(request):
    try:
        item_id = int(request.POST["item_id"])
        extras = MenuItem.get(pk=item_id).extras.all()
        print(extras)
        return JsonResponse(extras);
    except KeyError:
        print("no such key")
        return JsonResponse({"success": False})
    except MenuItem.DoesNotExist:
        print("no such menu item")
        return JsonResponse({"success": False})
    except JSONDecodeError:
        print("invalid JSON document")
        return JsonResponse({"success": False})


def login_view(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("index"))

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, "order/login.html", {"message": "Something went wrong"})
    else:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "GET":
        print('register view')
        return render(request, "orders/register.html", {"message": None})
    else:
        try:
            username = request.POST["username"]
            password = request.POST["password"]

            # Make sure username is valid
            if not username:
                print("must include a username")
            if not password:
                print("must include a password")

            # Check if username already exists
            if User.objects.get(username=username):
                return render(
                    request,
                    "orders/register.html",
                    {"message": "Username already taken"}
                )

            return render(request, "orders/register.html", {"message": "Smth wehnt rong"})
        except KeyError:
            return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            # Create the user
            User.objects.create_user(username, password=password)
            return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
