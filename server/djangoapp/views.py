from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def render_some_template(request):
    """
    A function to render a static template.
    """
    # Context to serve
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/some-template.html', context)




# Create an `about` view to render a static about page
def about(request):
    """
    A function to render the about page template
    """
    # Context to serve
    context = {}

    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    """
    A function to render the contact us page template
    """
    # Context to serve
    context = {}

    if request.method == 'GET':
        return render(request, 'djangoapp/contact-us.html', context)




# Create a `login_request` view to handle sign in request
def login_request(request):
    """
    Function to handle login
    """
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
            return render(request, 'onlinecourse/user_login.html', context)
    else:
        return render(request, 'onlinecourse/user_login.html', context)



# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """
    Function to handle logout.
    """
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')



# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        # return render(request, 'djangoapp/user_registration.html', context)
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)




# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    """
    Function to return delearship information
    """
    context = {}
    if request.method == "GET":
        url = 'https://141b0828.eu-gb.apigw.appdomain.cloud/api/dealership'

        try:

            # Get dealers from the URL
            dealerships = get_dealers_from_cf(url)
            # print('dealerships from get_dealership view:', dealerships)

            # Concat all dealers' short name
            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

            # Return a list of dealer short name
            context["dealers"] = dealerships 

            print('Should return dealers')
            # return HttpResponse(dealer_names, context)
            return render(request, 'djangoapp/index.html', context)
        
        except Exception as error:
            print("Error:", error)
            return render(request, 'djangoapp/index.html', context)




# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    """
    Function to return dealer details.
    """
    context = {}
    review_list = []
    if request.method == "GET":
        url = "https://141b0828.eu-gb.apigw.appdomain.cloud/api/review"

        try:
            print('get_dealer_details has kicked off.')
            reviews = get_dealer_reviews_from_cf(url, dealer_id)
            print('dealer reviews:', reviews)

            # # Concat all dealer's reviews
            # dealer_reviews = ' '.join([review.review for review in reviews])

            # dealer_sentiment = ' '.join([review.sentiment for review in reviews])

            # context['reviews'] = dealer_reviews

            # context['sentiment'] = dealer_sentiment

            review_list = []

            for review in reviews:
                print('this review:', review.review)
                print('this sentiment:', review.sentiment)
                review_obj = {}
                review_obj['review'] = review.review
                review_obj['sentiment'] = review.sentiment
                review_obj['car_make'] = review.car_make
                review_obj['car_model'] = review.car_model
                review_obj['car_year'] = review.car_year

                print('review obj:', review_obj)
                review_list.append(review_obj)
                
            context['reviews'] = review_list

            context['dealer_id'] = dealer_id
            print('context:', context)

            # return HttpResponse(context)
            return render(request, 'djangoapp/dealer_details.html', context)


        except Exception as error:
            print("get_dealer_details error:", error)
            # return HttpResponse(context)
            return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    """
    Function to add a review
    """

    context= {}

    try:

        url = "https://141b0828.eu-gb.apigw.appdomain.cloud/api/add-review"

        # check if authenticated
        if request.user.is_authenticated:
            if request.method=="GET":
                # Handle the rendering of the page
                context['dealer_id'] = dealer_id

                dealers_url = "https://141b0828.eu-gb.apigw.appdomain.cloud/api/dealership?id=" + str(dealer_id)
                dealer = get_dealers_from_cf(dealers_url)[0]

                print("add review dealer:", dealer.full_name)

                print(dealer)
                context['dealer'] = dealer

                cars = CarMake.objects.all()

                context['cars'] = cars

                print('cars:', cars)

                return render(request, 'djangoapp/add_review.html', context)

            if request.method=="POST":
                print('form submitted process kicked off')

                print('request body', request.POST)

                submitted_form = request.POST

                print('this review', submitted_form['content'])

                review = {}
                # review["time"] = datetime.utcnow().isoformat()
                review["dealership"] = dealer_id
                review["review"] = submitted_form['content']
                review["car_make"] = submitted_form['car-make']

                json_payload = {}
                json_payload["review"] = review

                json_payload = json.dumps(json_payload)

                # print('submitted review', review)

                url = "https://141b0828.eu-gb.apigw.appdomain.cloud/api/add-review"

                posted_request = post_request(url, json_payload, dealer_id=dealer_id)

                print('posted_request')

            
                # return HttpResponse({"request:":"Has been made"})

                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        else:
            # return render(request, 'djangoapp/dealer_details.html', context)
            return render(request, 'djangoapp/add_review.html', context)
    
    except Exception as error:
        print('add_review error:', error)

        return render(request, 'djangoapp/add_review.html', context)

