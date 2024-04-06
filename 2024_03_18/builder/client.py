import requests

url = "http://localhost:8000/pizza"
headers = {'Content-type': 'application/json'}

pizza1 = {
    "tamaño": "mediano",
    "masa": "delgado",
    "toppings": ["cereza", "piña", "queso"]
}
pizza2 = {
    "tamaño": "grande",
    "masa": "delgado",
    "toppings": ["jamon", "queso"]
}
response = requests.post(url, json=pizza1, headers=headers)
print(response.json())
response2 = requests.post(url, json=pizza2, headers=headers)
print(response2.json())