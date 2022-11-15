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

backend = "https://backend.verefa.com/"
connect_server = (f"{backend}gate_auth/")
send_server = (f"{backend}send/")
get_server = (f"{backend}get/")
stream_server = (f"{backend}iterate/")
purge_server = (f"{backend}purge/")

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class machine:   
    def __init__(self, debug=None):
        if debug == None:
            debug = False
        if debug == False:
            self.stdout_val = False
        elif debug == True:
            self.stdout_val = True
        else:
            self.stdout_val = False
        print("Welcome to your client Verefa Machine.")
        print("https://verefa.com/")
        self.session = 0
        self.tokenid = 0
        self.token = 0
        print("INIT COMPLETE")
        print("AWAITING CALL verefa.connect(APPID, TOKEN, APPNAME)")

    def stdout(self, content):
        if self.stdout_val == True:
            time = datetime.now()
            reshour = time.hour
            resminute = time.minute
            return print(f"[{reshour}:{resminute}] ->> {content}")
        else:
            return

    def new(self):
        print()

    def detail(self):
        msg = (f"Verefa Python Client Package\nAuthored:Verefa Admin\nOwned:Verefa\nLicensing:Usage!=other\nReturns:https://backend.verefa.com/\nSession:{self.session}\nToken:{self.token}\nTokenid:{self.tokenid}")
        self.stdout(msg)
        return msg

    def scripter(self):
        print("Complete")

    def connect(self, tokenid=None, token=None, appname=None):
        self.stdout("CALL FOUND...")
        self.stdout("CALLING CONNECT...")
        self.token = token
        self.tokenid = tokenid
        self.appname = appname
        try:
            self.devicename = str(socket.gethostname())
            self.deviceuser = str(os.getlogin())
            self.ip = str(requests.get('https://checkip.amazonaws.com').text.strip())
            compiled = (f"{self.devicename} |||| {self.deviceuser} |||| {self.ip}")
        except:
            compiled = "ERROR |||| ERROR |||| ERROR"
            self.stdout(f"{WARNING}UNABLE TO FETCH DEVICE DETAILS{ENDC}")
            

        if tokenid == None or token == None or appname == None:
            self.stdout("ARGS NOT SUPPLIED")
            return "ARGS NOT SUPPLIED"
        try:
            data = { 'ID': f'{self.tokenid}','TOKEN': f'{self.token}','APPNAME': f'{self.appname}','TRACKERS':f'{compiled}'}
            connection = requests.post(connect_server, data=json.dumps(data), headers={'Content-Type': 'application/json'}) 
            partition = connection.text.split("----")
            self.session = partition[0]
            self.stdout(self.session)
            if partition[1] == "REQUEST POSITIVE":
                self.stdout("INIT SUCCESS")
                return self.session
            else:
                self.stdout("CONNECT FAIL")
                return "CONNECT FAIL"
        except:
            self.stdout("CONNECT FAIL")
            return "CONNECT FAIL"



    def send(self, location=None, packets=None):
        try:
            if self.session:
                sessionid = self.session
            else:
                self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
                return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        except:
            self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
            return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        if location == None or packets == None:
            self.stdout("ARGS NOT SUPPLIED")
            return "ARGS NOT SUPPLIED"

        preppacket = json.dumps(packets)
    
        try:


            data = {'SESSION': f'{sessionid}', 'LOCATION': f'{location}','PACKETS': f'{preppacket}'}
            connection = requests.post(send_server, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            self.stdout(connection.text)
            if connection.text == "SERVER - SET COMPLETE FOR NEW DOCUMENT" or connection.text == "SERVER - SET COMPLETE MERGED DATA":
                self.stdout("POST SUCCESS")
                return "POST SUCCESS"
            else:
                self.stdout("POST FAIL")
                return "POST FAIL"
        except:
            self.stdout("POST FAIL")
            return "POST FAIL"

    def get(self, location=None, specs=None):
        try:
            if self.session:
                sessionid = self.session
            else:
                self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
                return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        except:
            self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
            return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        if location == None:
            self.stdout("ARGS NOT SUPPLIED")
            return "ARGS NOT SUPPLIED"
        try:
            data = {'SESSION': f'{sessionid}', 'LOCATION': f'{location}','SPECS': f'{specs}'}
            content = requests.post(get_server, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            if content.json() != None:
                self.stdout("GET SUCCESS")
                return content.json()
            else:
                self.stdout("GET FAIL")
                return "GET FAIL"
        except:
            self.stdout("GET FAIL")
            return "GET FAIL"

    def iterate(self, location=None, specs=None):
        try:
            if self.session:
                sessionid = self.session
            else:
                self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
                return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        except:
            self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
            return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        if location == None:
            self.stdout("ARGS NOT SUPPLIED")
            return "ARGS NOT SUPPLIED"
        try:
            data = {'SESSION': f'{sessionid}', 'LOCATION': f'{location}','SPECS': f'{specs}'}
            content = requests.post(stream_server, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            if content.json() != None:
                self.stdout("ITERATE SUCCESS")
                return content.json()
            else:
                self.stdout("ITERATE FAIL")
                return "ITERATE FAIL"
        except:
            self.stdout("ITERATE FAIL")
            return "ITERATE FAIL"


    def purge(self, location=None, type=None, addressing=None):
        try:
            if self.session:
                sessionid = self.session
            else:
                self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
                return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        except:
            self.stdout("SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?")
            return "SESSION ID DOESN'T EXIST - HAVE YOU CALLED CONNECT?"
        if location == None or type == None:
            self.stdout("ARGS NOT SUPPLIED")
            return "ARGS NOT SUPPLIED"
        if type == "FIELD" and addressing == None:
            self.stdout("ADDRESSING NOT SUPPLIED")
            return "ADDRESSING NOT SUPPLIED"

        try:
            data = {'SESSION': f'{sessionid}', 'LOCATION': f'{location}', 'TYPE': f'{type}', 'ADDR': f'{addressing}'}
            content = requests.post(purge_server, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            if content.text == "SUCCESS":
                self.stdout("PURGE SUCCESS")
                return content
            else:
                self.stdout("PURGE FAIL")
                return content
        except:
            self.stdout("PURGE FAIL")
            return "PURGE FAIL"
