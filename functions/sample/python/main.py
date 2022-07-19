#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from asyncio.windows_events import NULL
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

dict = {
    'st': "CA",
    'sty': NULL,
    'dealerId': 2,
}

def main(dict):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name="c1814c9d-49ff-488e-8be9-21eaa9214c7c-bluemix",
            api_key="IukMHXbwqVIr_OEbs5xGIiXBiTYwdg2lVOodqpjzVLHn",
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}


main(dict)
