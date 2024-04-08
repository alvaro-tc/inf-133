import requests

url = "http://localhost:8000/personas"
headers = {"Content-Type": "application/json"}




data={
    "nombre":"Alvaro",
    "apellido":"Torrez"
}
response = requests.post(url=url, json=data, headers=headers)
print("Mostrar POST: ",response.text)

data={
    "nombre":"Pepito",
    "apellido":"Fernandez"
}
response = requests.post(url=url, json=data, headers=headers)


response = requests.get(url)
print("Mostrar GET: ",response.text)




response = requests.get(url+"/?apellido=Fernandez")
print("Mostrar GET por apelldio: ",response.text)