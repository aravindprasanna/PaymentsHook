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

    res = makeResponse(req)
    res = json.dumps(res,indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    return r

def makeResponse(req):
    json_res = {
        "data": {
          "google": {
            "expectUserResponse": True,
            "isSsml": False,
            "noInputPrompts": [],
            "systemIntent": {
              "data": {
                "@type": "type.googleapis.com/google.actions.v2.TransactionRequirementsCheckSpec",
                "paymentOptions": {
                  "googleProvidedOptions": {
                    "prepaidCardDisallowed": False,
                    "supportedCardNetworks": [
                      "VISA",
                      "AMEX"
                    ],
                    "tokenizationParameters": {
                      "parameters": {},
                      "tokenizationType": "PAYMENT_GATEWAY"
                    }
                  }
                }
              },
              "intent": "actions.intent.TRANSACTION_REQUIREMENTS_CHECK"
            }
          }
        }
    }


if __name__ == '__main__':
    app.run()
