import requests
url = "http://localhost:5000/"
headers = {'Content-type': 'application/json'}

#SUMA
response = requests.get(url=url+"sumar?num1=5&num2=3")
print(response.text)

#PALINDROMO
response = requests.get(url=url+"palindromo?cadena=reconocer")
print(response.text)

#CUENTA VOCAL
response = requests.get(url=url+"contar?cadena=exepciones&vocal=e")
print(response.text)
