import requests

url = "http://localhost:8000/tacos"
headers = {'Content-type': 'application/json'}

#Mostrando a todos los tacos (GET)
response = requests.get(url)
print(response.json())

#Creando a un nuevo taco (POST)
taco = {
    "base": "carne",
    "guiso": "picante",
    "salsa": "golf",
    "toppings": ["Queso", "Jamon"]
}
response = requests.post(url, json=taco, headers=headers)
print(response.json())



#Editando al primer taco (PUT)
edit_taco = {
    "base": "carne",
    "guiso": "picante",
    "salsa": "golf",
    "toppings": ["Jamon"]
}
response = requests.put(url + "/1", json=edit_taco, headers=headers)
print(response.json())




#Eliminando al primer taco(DELETE)

response = requests.delete(url + "/1")
print(response.json())


#Mostrando a todos los tacos (GET)
response = requests.get(url)
print(response.json())