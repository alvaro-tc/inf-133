import requests
import json

url = "http://localhost:8000/chocolates"
headers = {"Content-Type": "application/json"}

# CREATE chocolates
new_chocolate_data = {
    "chocolate_type":"trufa",
    "peso": 12,
    "sabor": "frutilla",
    "relleno": "chocolate blanco"
}
response = requests.post(url=url, json=new_chocolate_data, headers=headers)
print(response.json())

new_chocolate_data = {
    "chocolate_type":"bombon",
    "peso": 5,
    "sabor": "limon",
    "relleno": "chocolate blanco"

}
response = requests.post(url=url, json=new_chocolate_data, headers=headers)
print(response.json())


# READ chocolates
response = requests.get(url=url)
print(response.json())

# UPDATE chocolate 2
chocolate_id_to_update = 2
updated_chocolate_data = {
    "relleno": "dulce de limon"
}
response = requests.put(f"{url}/{chocolate_id_to_update}", json=updated_chocolate_data)
print("Respuesta PUT:", response.json())

# READ Chocolates
response = requests.get(url=url)
print(response.json())

# DELETE chocolate 1
chocolate_id_to_delete = 1
response = requests.delete(f"{url}/{chocolate_id_to_delete}")
print("Respuesta DELETE:", response.json())

# READ chocolates
response = requests.get(url=url)
print(response.json())

