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
        self.active = False
        self.address = address
        self.directions = {
            "create_app":f"{address}/api/v1/apps",
            "verify_credentials":f"{address}/api/v1/apps/verify_credentials",
            "auth":f"{address}/oauth/authorize?",
            "token":f"{address}/oauth/token",
            "account":f"{address}/api/v1/accounts"
        }
        url1 = self.directions["create_app"]
        params = {"client_name": f"{name}","redirect_uris":"urn:ietf:wg:oauth:2.0:oob","scopes":"write:accounts read"}
        app_response = requests.post(url1, data=params)
        if app_response.status_code == 200:
            print("Returned 200")
            print(app_response)
            self.app_instance = app_response.json()
            ## Created app instance
            ## Preparing to generate oauth tokens from app instance
            client_id = str(self.app_instance['client_id'])
            client_secret = str(self.app_instance['client_secret'])
            # Now we have the client id, the client secret, and finally the access token from the init all prepared.
            url2 = self.directions["token"]
            params = {"grant_type": "client_credentials","client_id": client_id,"client_secret":client_secret,"redirect_uri":"urn:ietf:wg:oauth:2.0:oob","scope":"write:accounts read"}
            oauth_response = requests.post(url2, data=params)
            print(oauth_response)
            print("Here 1")
            if oauth_response.status_code == 200:
                print(oauth_response.json()["access_token"])
                temp_access = str(oauth_response.json()["access_token"])
                self.key = temp_access
                #url3 = self.directions["account"]
                #headings = {"Authorization":f"Bearer {temp_access}"}
                #final_response = requests.post(url3, data=params, headers = headings)
                #print(final_response.json())
                #print("Here 2")
                #print(oauth_response.history[0].url)

                headings = {"Authorization":f"Bearer {token}"}
                final_response = requests.get(f"{address}/api/v1/accounts/verify_credentials", headers = headings)
                print(final_response.json())


                print("COMPLETED AUTHENTICATION!")
                self.active = True
            else:
                print("Failed to generate oauth token from app data")
            #auth = {"Authorization": f"Bearer {token}"}
            #response = requests.post(url, data=params, headers=auth)
            self.active = True
        else:
            self.active = False


    def account_info(self):
        if self.active == True:
            for data in self.app_instance:
                print(data)


    def toot(self,word):
        if self.active == True:
            headers = {"Authorization":f"Bearer {self.key}"}
            params = {"status": word}
            oauth_response = requests.post(f"{self.address}/api/v1/statuses", data=params,headers=headers)
            print(oauth_response)



