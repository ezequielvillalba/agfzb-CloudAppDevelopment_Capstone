import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create a `get_request` to make HTTP GET requests
# Help on this topic:
# https://requests.readthedocs.io/en/latest/api/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMCD0321ENSkillsNetwork23970854-2022-01-01#main-interface
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    try:
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
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))

    try:
        # Call post method of requests library with URL, json payload and parameters
        response = requests.post(url, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# get_dealers_from_cf
# get dealers from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result and json_result["status"]==200:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

# def get_dealer_reviews_from_cf(url, **kwargs)
# get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    nlu_api_key = kwargs["nlu_api_key"]
    nlu_url = kwargs["nlu_url"]
    sentiment_temp = "neutral"

    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result and json_result["status"]==200:
        # Get the row list in JSON as dealers
        reviews = json_result["body"]
        # For each dealer object
        for review in reviews["data"]:
            # Create a DealerReview object with values in `doc` object
            # TODO: remove id
            if not "id" in review:
                review["id"] = 999   
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                   review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                   car_model=review["car_model"], car_year=review["car_year"], sentiment=sentiment_temp,
                                   id=review["id"])

            review_obj.sentiment = analyze_review_sentiments(review_obj.review, nlu_api_key, nlu_url)

            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
# Help on this topic:
# https://github.com/watson-developer-cloud/python-sdk
# https://cloud.ibm.com/apidocs/natural-language-understanding?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMCD0321ENSkillsNetwork23970854-2022-01-01#analyzeget
def analyze_review_sentiments(text, nlu_api_key, nlu_url):
    sentiment_temp = "neutral"
    
    authenticator = IAMAuthenticator(nlu_api_key)
    service = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    service.set_service_url(nlu_url)
    
    try:
        response = service.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
        print(json.dumps(response, indent=2))
        return response['sentiment']['document']['label']
    except Exception as e:
        print(str(e))
        return sentiment_temp

    # sentiment_temp = "neutral"

    # # Authentication via IAM
    # authenticator = IAMAuthenticator(nlu_api_key)
    # service = NaturalLanguageUnderstandingV1(
    #     version='2018-03-16',
    #     authenticator=authenticator)
    # service.set_service_url(nlu_url)

    # try:
    #     response = service.analyze(text=text, 
    #                     features=Features(sentiment=SentimentOptions()),
    #                     language="en").get_result()
    #     print(json.dumps(response, indent=2))
    #     return response['sentiment']['document']['label']
    # except Exception as e:
    #     print(str(e))
    #     return sentiment_temp
