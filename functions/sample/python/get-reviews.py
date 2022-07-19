
#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from asyncio.windows_events import NULL

dict = {
    # 'st': "CA",
    # 'sty': NULL,
    'dealerId': 2,
}


def main(dict):
    authenticator = IAMAuthenticator("IukMHXbwqVIr_OEbs5xGIiXBiTYwdg2lVOodqpjzVLHn")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://c1814c9d-49ff-488e-8be9-21eaa9214c7c-bluemix.cloudantnosqldb.appdomain.cloud")

    try:
        response = service.post_find(
            db = 'reviews',
            selector={'dealership': {'$eq': int(dict['dealerId'])}},
            ).get_result()
    except Exception as e:
        if str(e) == "\'dealerId\'":
            response = service.post_find(
                db = 'reviews',
                selector={},
                ).get_result()
        else:
            return {
                'statusCode': 500,
                'message': 'Something went wrong on the server '+ str(e)
            }

    try:
        docs = response['docs']
        if (len(docs) == 0):
            result={
                'statusCode': 404,
                'message': 'dealerId does not exist',
                'body': {'data':docs},
            }
        else:
            result={
                'headers':{'Content-Type':'application/json'},
                'statusCode': 200,
                'message': 'Success',
                'body': {'data':docs},
            }
        return result
    except Exception as e:
        return {
            'statusCode': 500,
            'message': 'Something went wrong on the server '+ str(e)
        }
        
main(dict)
