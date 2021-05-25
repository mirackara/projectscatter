import requests

SITE = "http://127.0.0.1:5000/"

#response = requests.get(SITE+ "test/Seinfeld")
response2 = requests.get(SITE+ "test/Schitt%27s%20Creek")
#print(response.json())
print(response2.json())