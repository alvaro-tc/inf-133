import requests
url = "http://localhost:8000/personas"
headers = {"Content-Type":"application/json"}

data = {
    "ci":123,
    "nombre":"Alvaro",
    "apellido":"Torrez",
    "edad" :22
}

request = requests.post(url=url,json=data,headers=headers)
print (request.text)

data = {
    "ci":321,
    "nombre":"Alvaro",
    "apellido":"Perez",
    "edad" :21
}
request = requests.post(url=url,json=data,headers=headers)


request = requests.get(url+"/?nombre=Alvaro")
print (request.text)