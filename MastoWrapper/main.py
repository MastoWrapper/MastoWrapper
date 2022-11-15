## CLIENT SIDE PACKAGE ##
##python setup.py sdist
##pip install -e ./
##python -m twine upload dist/*


import os
import time
from datetime import datetime
import sys
import json
import requests
import socket



class Client:
    def __init__(self,name=None,token=None,address=None,scopes=None):
        try:
            self.active = False
            self.address = address
            self.token = token
            self.directions = {
                "create_app":f"{address}/api/v1/apps",
                "verify_credentials":f"{address}/api/v1/apps/verify_credentials",
                "auth":f"{address}/oauth/authorize?",
                "token":f"{address}/oauth/token",
                "account":f"{address}/api/v1/accounts"
            }
            headings = {"Authorization":f"Bearer {token}"}
            final_response = requests.get(f"{address}/api/v1/accounts/verify_credentials", headers = headings)
            if final_response.status_code == 200:
                self.active = True
                return 200
            else:
                self.active = False
        except Exception as e:
            self.active = False
            print(e)
            return e


    def account_info(self):
        if self.active == True:
            for data in self.app_instance:
                print(data)


    def toot(self,word):
        if self.active == True:
            headers = {"Authorization":f"Bearer {self.token}"}
            params = {"status": word}
            oauth_response = requests.post(f"{self.address}/api/v1/statuses", data=params,headers=headers)
            print(oauth_response)



