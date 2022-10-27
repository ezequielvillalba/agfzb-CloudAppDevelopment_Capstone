import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
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
# e.g., response = requests.post(url, params=kwargs, json=payload)


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
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


def get_dealers_from_cf(url):
    results = [] 
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results



# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id(url, dealer_id):
    
    dealerId={} 
    dealerId['dealerId']=dealer_id
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
    results=[]
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# def get_dealer_by_state_from_cf(url, state):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_by_state(url, st):
    st1=st['st']
    if not st1:
        result=get_dealers_from_cf(url)
        return result
    results = [] 
    # Call get_request with a URL parameter
    json_result = get_request(url,st=st)
    if json_result:
        # Get the row list in JSON as dealers
        # For each dealer object
        dealers=json_result
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results=[]
    dealerId = {"dealer_id":dealer_id}
    json_result = get_request(url, dealer_id=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"]["docs"]
        print(f'dealers in cf are {dealers}')
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            try:
                if not dealer_doc["purchase"]:
                    dealer_obj=DealerReview(dealership="n", name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                    review=dealer_doc["review"], purchase_date="0", car_make="n",
                                    car_model="n",car_year="n",
                                    id=dealer_doc["id"])
                else:
                    # print(f'dealer_doc["dealership"] IS {dealer_doc["dealership"]}')
                    # print(f'dealer_doc["name"] IS {dealer_doc["name"]}')
                    # print(f'dealer_doc["purchase"] IS {dealer_doc["purchase"]}')
                    # print(f'dealer_doc["review"] IS {dealer_doc["review"]}')
                    # print(f'dealer_doc["purchase_date"] IS {dealer_doc["purchase_date"]}')
                    dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                    review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                    car_model=dealer_doc["car_model"],car_year=dealer_doc["car_year"],
                                    id=dealer_doc["id"])
                
                dealer_obj.sentiment = analyze_review_sentiments(dealer_obj.review +"hello hello hello")
                
                              
                results.append(dealer_obj)
                
            except:
                print('except')
                
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



def analyze_review_sentiments(dealerReview):
    try:
        url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2feb4018-a252-49bc-a8d0-f6f31a2254b1"
        api_key = "DQnQP7ZAiHPKQz-q2jMx8gsEDyH4sGY8G9Ppe4KSbtyJ"
        authenticator = IAMAuthenticator(api_key)
        natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
        natural_language_understanding.set_service_url(url)
        response = natural_language_understanding.analyze( text=dealerReview,features=Features(sentiment=SentimentOptions(targets=[dealerReview]))).get_result()
        label=json.dumps(response, indent=2)
        label = response['sentiment']['document']['label']
        return(label)
    except(requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
