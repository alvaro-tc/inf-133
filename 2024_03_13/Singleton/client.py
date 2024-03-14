
import requests

url = "http://localhost:8000/"

response = requests.request(method="GET", url=url + "player")
print(response.text)
