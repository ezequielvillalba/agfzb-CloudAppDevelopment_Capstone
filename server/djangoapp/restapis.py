import requests
import json
import os
import sys
import time
from .models import CarDealer, DealerReview, CarModel, CarMake, CarDealer
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    try:
        request = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Network exception occurred")

    status_code = request.status_code
    print(request.request.body)
    print("With status {} ".format(status_code))
    json_data = json.loads(request.text)

    return request


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    # print('json_result from line 31', json_result)    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            print("dealer_doc", dealer_doc)
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
            results.append(dealer_obj)
    return results



# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result

        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],

                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
    return dealer_obj

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    # print(json_result)
    if json_result:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]

            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerReview, language="en"):
    try:
        url = "https://322d2895-8806-458a-992a-18f2fb8cd10a-bluemix.cloudantnosqldb.appdomain.cloud"
        api_key = "Tis_kkoet1gdM43W9j8hFT6IUe22ymwtFCx3LJFVy4Cw"
        authenticator = IAMAuthenticator(api_key)
        natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
        natural_language_understanding.set_service_url(url)
        response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
        label=json.dumps(response, indent=2)
        label = response['sentiment']['document']['label']
        return(label)
    except(requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
