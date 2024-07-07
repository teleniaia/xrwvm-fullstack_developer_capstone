# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    data = {"userName":""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "http://localhost:3000/dealerships/get"

        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        context["dealers"] = dealerships

        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, id):
    if request.method == "GET":
        url = "http://localhost:5000/api/get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, id)
        context = {
            "reviews": dealer_reviews
        }

        return render(request, 'djangoapp/dealer_details.html', context)



# submit a review
def add_review(request):

    if request.method == "GET":
        url = "http://localhost:3000/dealerships/get"
        cars = get_dealers_from_cf(url)
        context = {
            "cars": cars
        }
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        csrf_token = get_token(request)

        url = "http://localhost:5000/api/post_review"
        review = {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }

        headers = {
            "X-CSRFToken": csrf_token
        }

        status = post_request(url, json_payload=review, headers=headers)
        if status:
            return HttpResponse("Review added successfully")
        else:
            return HttpResponse("Failed to add review")
    else:
        return HttpResponse("Failed to add review")