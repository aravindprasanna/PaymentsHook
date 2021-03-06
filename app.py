import json
import os
import requests


from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/webhook',methods=['POST'])
def webhook():
    req = request.get_json(silent=True,force=True)
    print(json.dumps(req,indent=4))

    query_result = req.get("queryResult")
    action = query_result.get("action")

    resp = ""
    if action == "BillerAdd":
        res = add_biller(query_result)

        if res:
            resp = makeResponse("Biller Added Successfully")
        else:
            resp = makeResponse("Unsuccessful")

    if action == "MakePayment":

        res = make_payment(query_result)

        if res:
            resp = makeResponse("Transaction successful")
        else:
            resp = makeResponse("Failed")

    resp = json.dumps(resp,indent=4)
    r = make_response(resp)
    r.headers['Content-Type'] = 'application/json'

    return r

def make_payment(query_result):

    input_json = {
        "user": "hari",
        "biller_ref": "SP12345",
        "biller_name": "SP Services"
    }

    url = "http://c9c856ac.ngrok.io/payments/"
    r = requests.post(url, input_json)
    json_object = r.json()
    if r.status_code == 200:
        return True
    else:
        return False


def add_biller(query_result):
    parameters = query_result.get("parameters")
    biller_ref = parameters.get("biller_ref")
    biller_name = parameters.get("biller_name")

    input_json = {
        "user":"hari",
        "biller_ref": biller_ref,
        "biller_name": biller_name
    }

    url = "http://c9c856ac.ngrok.io/billerprofile/"
    r = requests.post(url,input_json)
    json_object = r.json()
    if r.status_code == 201:
        return True
    else:
        return False


def makeResponse(speech):
    json_res = {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        speech
                    ]
                }
            }
        ],
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": speech
                            }
                        }
                    ]
                }
            }
        }
    }

    return json_res


if __name__ == '__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app on port {}".format(port))
    app.run(debug=False,port=port,host='0.0.0.0')