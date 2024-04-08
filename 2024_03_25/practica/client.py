import requests
url = "http://localhost:8000/productos"
headers = {'Content-type': 'application/json'}

# READ chocolates
response = requests.get(url=url)
print(response.json())