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
import verefa




class Client:
    def __init__(self,name=None,token=None,address=None,scopes=None):
        try:
            if scopes == None:
                self.scopes = "read read:statuses"
            elif ("read" in scopes) == False:
                self.scopes = (f"{scopes} read")
            else:
                self.scopes = scopes

            self.active = False
            self.recent_status_id = 0
            self.address = address
            self.token = token
            self.directions = {
                "create_app":f"{address}/api/v1/app ",
                "verify_credentials":f"{address}/api/v1/apps/verify_credentials",
                "auth":f"{address}/oauth/authorize?",
                "token":f"{address}/oauth/token",
                "account":f"{address}/api/v1/accounts"
            }
            self.commands = {}
            self.events = {}
            self.auth_headings = {"Authorization":f"Bearer {token}"}
            final_response = requests.get(f"{address}/api/v1/accounts/verify_credentials", headers = self.auth_headings)
            if final_response.status_code == 200:
                self.account_id = final_response.json()["id"]
                self.active = True
                return
            else:
                self.active = False
        except Exception as e:
            self.active = False
            print(e)
            return e

    def timeline(self,limit=20,since_id=None,max_id=None,min_id=None,local=None,remote=None,only_media=False):
        #"It appears that the 'remote' parameter is not functional on some mastodon instances so it is currently set as False, to collect data you must therefore set remote=None in your requests."

        try:
            limit = int(limit)
            if since_id != None:
                since_id = str(since_id)
            if max_id != None:
                max_id = str(max_id)
            if min_id != None:
                min_id = str(min_id)

            params = {"local": local, "remote":remote, "only_media":only_media, "max_id":max_id,"since_id":since_id,"min_id":min_id,"limit":limit}
            response = requests.get(f"{self.address}/api/v1/timelines/public", data=params, headers = self.auth_headings)
            if response.status_code == 200:
                returned_data = response.content
                returned_data = json.loads(returned_data.decode('utf-8'))
                return(returned_data)
            else:
                print("ERROR")
                return (response)
        except Exception as error:
            print(error)
            return (error)


    def status(self, status_id=1):
        ## Collects a single status by its ID#
        try:
            params = {":id": status_id}
            response = requests.get(f"{self.address}/api/v1/statuses", data=params, headers = self.auth_headings)
            if response.status_code == 200:
                returned_data = response.content
                returned_data = json.loads(returned_data.decode('utf-8'))
                return(returned_data)
            else:
                return (response)
        except Exception as error:
            return (error)

    def listener(self,watch=None):
        result = self.timeline(limit=1)
        self.recent_status_id = int(result[0]["id"])
        while self.active == True:
            time.sleep(1)
            if watch == "commands":
                try:
                    toot = self.status(self.recent_status_id)
                    print(toot[0]["mentions"])
                    #print(result[0]["content"])
                    #targetted = result["mentions"]["id"]
                    #print(targetted)
                    #if int(targetted) == self.account_id:
                    #    print("Found a message which mentions this account.")     

                except Exception as error:
                    self.recent_status_id+=1
                    print(self.recent_status_id)
                    pass

            elif watch == "events":
                print("Checking for events.")
            else:
                print("Checking for events.")
            


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

    def notifications(self,event=["All"],limit=20,max_id=None,min_id=None,ignore=[],account_id=None):
        if self.active == True:
            params = {"max_id":max_id,"min_id":min_id,"limit":limit,"types":event,"exclude_types":ignore,"account_id":account_id}
            headings = {"Authorization":f"Bearer {self.token}"}
            returned_notif = requests.get(f"{self.address}/api/v1/notifications", params=params, headers = headings)
            if returned_notif.status_code == 200:
                return(returned_notif.json())
            else:
                return(returned_notif.json())


    def command(self,p_func):
        self.commands[p_func.__name__] = p_func
        print(f"Created and stored command ({p_func.__name__}) to root.")
        def runner(*args,**kwargs):
            p_func(*args,**kwargs)
        return runner

    def event(self,p_func):
        self.events[p_func.__name__] = p_func
        print(f"Created and stored event ( {p_func.__name__}) to root.")
        def runner(*args,**kwargs):
            p_func(*args,**kwargs)
        return runner

    def handles(self):
        for obj in self.commands:
            print(self.commands[obj])
        for obj in self.events:
            print(self.events[obj])