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
    def __init__(self,token=None,address=None,scopes=None):

        self.directions = {
            "create_app":"https://mastodon.example/api/v1/apps"
        }


        self.auth = {'Authorization': 'Bearer 4-Y3nDFgrz8hV7WmbRqDAV52TiAnsQ8jeSvfbYN0g30'}

        url = self.directions["create_app"]
        #auth = {'Authorization': 'Bearer 4-Y3nDFgrz8hV7WmbRqDAV52TiAnsQ8jeSvfbYN0g30'}
        params = {"client_name": "Bob","redirect_uris":"urn:ietf:wg:oauth:2.0:oob"}
        response = requests.post(url, data=params, headers=None)
        if response.code == 200:
            print(response)