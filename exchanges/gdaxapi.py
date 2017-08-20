import hmac
import hashlib
import time
import requests
import base64
import json

class Connection:
    def __init__(self, key, secret, passphrase, api_url="https://api.gdax.com"):
        self.url = api_url.rstrip('/')
        self.auth = Authenticate(key, secret, passphrase)

    def __call__(self, command, arg=""):
        r = requests.get(self.url + '/'+ command+ '/' + arg, auth=self.auth, timeout=30)
        return r.json()        

class Authenticate:
    def __init__(self, key, secret, passphrase):
        self.key = key
        self.secret = secret
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        message = message.encode('ascii')
        hmac_key = base64.b64decode(self.secret)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        request.headers.update({
            'Content-Type': 'Application/JSON',
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.key,
            'CB-ACCESS-PASSPHRASE': self.passphrase})
        return request