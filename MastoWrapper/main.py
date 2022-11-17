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
import threading



class Client:
    def __init__(self,name=None,token=None,address=None,scopes=None):
        try:
            if scopes == None:
                self.scopes = "read"
            elif ("read" in scopes) == False:
                self.scopes = (f"{scopes} read")
            else:
                self.scopes = scopes

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
            self.commands = {}
            headings = {"Authorization":f"Bearer {token}"}
            final_response = requests.get(f"{address}/api/v1/accounts/verify_credentials", headers = headings)
            if final_response.status_code == 200:
                self.active = True
                return
            else:
                self.active = False
        except Exception as e:
            self.active = False
            print(e)
            return e


    def listener(self,watch=None):
        while self.active == True:
            time.sleep(1)
            if watch == "commands":
                print("Checking for toot events.")
            elif watch == "events":
                print("Checking for general events.")
            else:
                print("Checking for general events.")
            


    def run(self):
        ## Create listener threads to listen for all instances of @command/@event
        command_listener = threading.Thread(target=self.listener,args=("commands",)).start()
        event_listener = threading.Thread(target=self.listener,args=("events",)).start()



    def account_info(self):
        if self.active == True:
            headings = {"Authorization":f"Bearer {self.token}"}
            account_data = requests.get(f"{self.address}/api/v1/accounts/verify_credentials", headers = headings)
            for data in account_data.json():
                print(f"{data}:{account_data.json()[data]}")




    def toot(self,word):
        if self.active == True:
            headers = {"Authorization":f"Bearer {self.token}"}
            params = {"status": word}
            oauth_response = requests.post(f"{self.address}/api/v1/statuses", data=params,headers=headers)
            print(oauth_response)


    def command(self,p_func):
        self.commands[p_func.__name__] = p_func
        print(f"Created and stored command ({p_func.__name__}) to root.")
        def runner(*args,**kwargs):
            p_func(*args,**kwargs)
        return runner

    def list_commands(self):
        for obj in self.commands:
            print(self.commands[obj])

    