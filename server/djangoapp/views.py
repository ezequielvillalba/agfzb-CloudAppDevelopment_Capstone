import logging
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf
from .restapis import post_request
from .restapis import get_request
from .restapis import get_dealer_by_id_from_cf
from .restapis import get_dealer_by_state_from_cf
from .restapis import get_dealer_reviews_from_cf
from .restapis import analyze_review_sentiments
from .models import CarModel
from .models import CarMake
from .models import CarDealer
from .models import DealerReview

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration.html', context)
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
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ed85b03-2491-4385-a14a-5c8fb7f7c154/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)
    

# Create a `get_dealer_details` view to render the reviews of a dealer
    
# def get_dealer_details(request, id):
#    if request.method == "GET":
#        context = {}
#        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ed85b03-2491-4385-a14a-5c8fb7f7c154/dealership-package/get-dealership"
#        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
#        context["dealer"] = dealer

#        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ed85b03-2491-4385-a14a-5c8fb7f7c154/dealership-package/get-review"
#        reviews = get_dealer_reviews_from_cf(review_url, id=id)
#        print(reviews)
#        context["reviews"] = reviews

#        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    # dealer_id = "1"
    context={}
    if request.method == "GET":
        url ="https://us-south.functions.appdomain.cloud/api/v1/web/5ed85b03-2491-4385-a14a-5c8fb7f7c154/dealership-package/get-review"
        #url = "https://6c1cc8db.us-south.apigw.appdomain.cloud/dealer/get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        if dealer_reviews:
            context['dealer_reviews']= dealer_reviews
            return render(request, 'djangoapp/dealer_details.html', {'dealer_reviews':context['dealer_reviews']})
        else:
            context['dealer_id'] = dealer_id
            return render(request, 'djangoapp/dealer_details.html', {'dealer_id':context['dealer_id']})  

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# # ...
def add_review(request, dealerId):
    context = {
        "dealerId": dealerId
    }
    get_url = url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ed85b03-2491-4385-a14a-5c8fb7f7c154/dealership-package/get-dealership"
    car_dealer = get_dealers_from_cf(get_url, dealerId=dealerId)
    if request.method == 'POST':
        post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ed85b03-2491-4385-a14a-5c8fb7f7c154/dealership-package/post-review"
        form_data = request.POST
        car = CarModel.objects.get(id=form_data.get('car'))
        payload = {
            "review": {
                'id': 2022,
                'review': form_data.get('review_text'),
                'car_make': car.car_make.name,
                'car_year': int(car.year.strftime("%Y")),
                'car_model': car.name,
                'purchase': True if form_data.get('purchase') == 'on' else False,
                'purchase_date': form_data.get('purchase_date'),
                'name': form_data.get('name'),
                'dealership': dealerId,
                'sentiment': analyze_review_sentiments( "nautral" if form_data.get('review_text') == "" else "positive" if form_data.get('purchase') == 'on' else "negative" )
            }
        }
        response = post_request(post_url, payload)
        print("With url {}, \nresponse => {}".format(post_url, response))
        return redirect('djangoapp:dealer_details', dealerId=dealerId, dealerFullName=car_dealer[0].full_name)
    elif request.method == 'GET':
        context['cars'] = CarModel.objects.all()
        context['dealership'] = car_dealer[0]
        return render(request, 'djangoapp/add_review.html', context)
