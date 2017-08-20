import requests
import json
import base64
import hmac
import hashlib
import time

class Connection:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def __call__(self, cmd):
        payload = {"request": "/v1/{0}".format(cmd), "nonce": str(time.time()*1000000)}
        j = json.dumps(payload)
        data = base64.standard_b64encode(j.encode('utf8'))
        h = hmac.new(self.secret.encode('utf8'), data, hashlib.sha384)
        signature = h.hexdigest()
        signed_payload = {"X-BFX-APIKEY": self.key, 
                          "X-BFX-SIGNATURE": signature, 
                          "X-BFX-PAYLOAD": data}
        base = "{0:s}://{1:s}/{2:s}".format('https', 'api.bitfinex.com', 'v1')
        r = requests.post("{0}/{1}".format(base, cmd), headers=signed_payload, verify=True)
        response = r.json()
        return response