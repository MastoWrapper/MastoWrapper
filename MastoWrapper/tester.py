#TESTER.py
import time
import main

new = main.Client("FedAi","ccIFo24VX7O2IkoknpcPzUmdxXszJQ922HqW3at1LnY","https://techhub.social")
# @new.command
# def marker(message):
# 	print(f"New message: {message}")
# 	return

data = new.notifications()
for notification in data:
	if notification["type"] == "poll":
		print(f"Beware there was a vote by: {notification['account']['username']}")

while True:
	time.sleep(200)
	print("200 Passed")
#new.run()