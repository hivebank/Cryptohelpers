import time
import hmac
import hashlib
import urllib
import requests

class Connection:
    def __init__(self, api_key='', api_secret=''):
        self.api_key = api_key
        self.api_secret = api_secret

    def __call__(self, command, args={}):
        nonce = str(int(time.time()*1000))
        method_set = 'account'
        request_url = ('https://bittrex.com/api/v1.1/%s/' % method_set) + command + '?'
        request_url += 'apikey=' + self.api_key + "&nonce=" + nonce + '&'
        request_url += urllib.parse.urlencode(args)
        apisign = hmac.new(self.api_secret.encode(), request_url.encode(), hashlib.sha512).hexdigest()
        return requests.get(request_url, headers={"apisign": apisign}).json()