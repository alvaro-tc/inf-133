
import requests

url = "http://localhost:8000/"

response = requests.request(
    method="POST", url=url + "player/damage", json={"damage": 10}
)
print(response.text)