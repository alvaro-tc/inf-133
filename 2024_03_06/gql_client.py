import requests

query = """
    {
        estudiantes{
            nombre
        }
        estudiantes{
            nombre
            apellido
        }
    }
"""
query2= """
    {
        estudiantes{
            nombre
            apellido
        }
    }
"""

url='http://localhost:8000/graphql'

response=requests.post(url,json={'query': query})
response2=requests.post(url,json={'query': query2})
print(response.text)
#print(response2.text)