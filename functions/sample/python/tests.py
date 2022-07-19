
# ***
# prepare-entry-for-save
# ***
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
# 
# This function is part of a sequence that stores docs in cloudant database.
# Next function of the sequence should be the public create-document action from the Cloudant package

import sys

def main(dict):
    if not dict['id']:
        return {
            'statusCode': 10001,
            'message': 'Not \'id\' defined'
        }
    elif not dict['name']:
        return {
            'statusCode': 10002,
            'message': 'Not \'name\' defined'
        }
    elif not dict['dealership']:
        return {
            'statusCode': 10003,
            'message': 'Not \'dealership\' defined'
        }
    elif not dict['review']:
        return {
            'statusCode': 10004,
            'message': 'Not \'review\' defined'
        }
    elif not dict['purchase']:
        return {
            'statusCode': 10005,
            'message': 'Not \'purchase\' defined'
        }
    # elif not dict['another']:
    #     return {
    #         'statusCode': 10006,
    #         'message': 'Not \'another\' defined'
    #     }
    elif not dict['purchase_date']:
        return {
            'statusCode': 10007,
            'message': 'Not \'purchase_date\' defined'
        }
    elif not dict['car_make']:
        return {
            'statusCode': 10008,
            'message': 'Not \'car_make\' defined'
        }
    elif not dict['car_model']:
        return {
            'statusCode': 10009,
            'message': 'Not \'car_model\' defined'
        }
    elif not dict['car_year']:
        return {
            'statusCode': 10010,
            'message': 'Not \'car_year\' defined'
        }
    else:
        return{
            "doc": {
                "id": dict['id'],
                "name": dict['name'],
                "dealership": dict['dealership'],
                "review": dict['review'],
                "purchase": dict['purchase'],
                "another": dict['another'],
                "purchase_date": dict['purchase_date'],
                "car_make": dict['car_make'],
                "car_model": dict['car_model'],
                "car_year": dict['car_year']               
            }
        }
   

dict = {
  "id": 999,
  "name": "Federico Lumma",
  "dealership": 1,
  "review": "Excellent dealership",
  "another": "",
  "purchase": True,
  "purchase_date": "19/20/2020",
  "car_make": "Ford",
  "car_model": "Fiesta",
  "car_year": 2018            
}
main(dict)
