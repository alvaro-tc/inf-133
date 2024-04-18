import requests
url = "http://localhost:5000/"
headers = {'Content-type': 'application/json'}


response = requests.get(url=url)
print(response.text)