from django.shortcuts import render
from .models import CarModel
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from .restapis import *
import logging
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://3d18d20f.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)
 
def get_dealer_by_id(url, dealer_id):
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url, dealerId=dealer_id)
    return dealerships

def get_dealer_by_state(url, state):
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url, state=state)
    return dealerships

def get_dealer_details(request, dealer_id, dealer_name):
    context = {}
    # TODO: Hide this keys
    reviews_url = "https://3d18d20f.us-south.apigw.appdomain.cloud/api/review"
    nlu_api_key = "0Bd2RNmcgTVR8UuWD2d9hXh1IVd943ZGC5CFOw0WAyRb"
    nlu_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/d932f8aa-31e7-44ff-b7d1-03d17bf23579"

    dealer_reviews = get_dealer_reviews_from_cf(reviews_url, dealerId=dealer_id, nlu_url=nlu_url, nlu_api_key=nlu_api_key)

    # Concat all reviews
    # reviews = ""
    # for review in dealer_reviews:
    #     reviews += "\'" + review.review + " (" + review.sentiment + ")\' \n"
    context["dealer_id"] = dealer_id
    context["dealer"] = dealer_name
    context["review_list"] = dealer_reviews
    
    # Return a list of dealer short name
    return render(request, 'djangoapp/dealer_details.html', context)

# submit a review
def add_review(request, dealer_id, dealer_name):
    context = {}

    url_dealership = "https://3d18d20f.us-south.apigw.appdomain.cloud/api/dealership"
    url_review = "https://3d18d20f.us-south.apigw.appdomain.cloud/api/review"

    if request.method == 'GET':
        try:
            context["cars"] = CarModel.objects.filter(dealerId = dealer_id)
        except:
            return redirect('djangoapp:index')
        context["dealer_id"] = dealer_id
        context["dealer"] = dealer_name
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        time = datetime.utcnow().isoformat(),
        id = int(dealer_id)
        name = request.user.first_name + ' ' + request.user.last_name
        another = ""
        review = request.POST['content']
        purchase_check = request.POST.get('purchasecheck', 'off')
        purchase = True if purchase_check=='on' else False
        purchase_date = request.POST['purchasedate']
        car = CarModel.objects.get(pk = request.POST['car'])
        car_make = car.make.name
        car_model = car.name
        car_year = car.year
        review = {
            "time": time,
            "id": int(dealer_id),
            "name": name,
            "dealership": int(dealer_id),
            "another": another,
            "review": review,
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car_make": car_make,
            "car_model": car_model,
            "car_year": car_year
        }
        json_payload = {
            "review": review
        }
        response = post_request(url_review, json_payload)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id, dealer_name=dealer_name)
    else:
        return render(request, 'djangoapp/index.html', context)


