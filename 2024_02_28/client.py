import requests

url="http://localhost:8000/"
# DELETE Consulta a la lista estudiantes


ruta_filtrar_carreras = url + "estudiantes/Arquitectura"
filtrar_carreras_response = requests.request(method="GET", url=ruta_filtrar_carreras)
print (filtrar_carreras_response.text)