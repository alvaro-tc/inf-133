
import requests

url = "http://localhost:8000/"


response2 = requests.request(
    method="POST", url=url + "delivery", json={"vehicle_type": "scout"}
)

print(response2.text)