
# ***
# save_review_entry
# ***
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
# 

import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from asyncio.windows_events import NULL

def main(dict):
    authenticator = IAMAuthenticator("IukMHXbwqVIr_OEbs5xGIiXBiTYwdg2lVOodqpjzVLHn")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://c1814c9d-49ff-488e-8be9-21eaa9214c7c-bluemix.cloudantnosqldb.appdomain.cloud")
    try:
        response = service.post_document(db='reviews', document=dict['review']).get_result()
        result={
            'headers':{'Content-Type':'application/json'},
            'status': 200,
            'message': 'Success',
            'body': {'data':response},
        }
        return result
    except Exception as e:
        return {
            'status': 404,
            'message': 'Something went wrong on the server '+ str(e)
        }

dict = {
    "review":{
      "id": 999,
      "name": "Alberto Ramos",
      "dealership": 2,
      "another": "",
      "review": "Good attention",
      "purchase": True,
      "purchase_date": "19/20/2021",
      "car_make": "Nissan",
      "car_model": "Versa",
      "car_year": 2018
    }
}
main(dict)

