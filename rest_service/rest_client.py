import requests

url="http://localhost:8000/"
# GET Consulta a la lista estudiantes
ruta_get = url + "lista_estudiantes"
get_response = requests.request(method="GET", url=ruta_get)
#print (get_response.text)

ruta_buscar = url + "buscar_nombre"
buscar_response = requests.request(method="GET", url=ruta_buscar)
#print (buscar_response.text)

ruta_contar = url + "contar_carreras"
contar_response = requests.request(method="GET", url=ruta_contar)
print (contar_response.text)

ruta_total = url + "total_estudiantes"
total_response = requests.request(method="GET", url=ruta_total)
print (total_response.text)

# POST Agrega un nuevo estudiante por la ruta /agrega_estudiante
ruta_post= url+ "agrega_estudiante"
nuevo_estudiante = {
    "nombre":"Juanito",
    "apellido":"Perez",
    "carrera":"Ingieneria Agronomica"
}
post_response= requests.request(
    method="POST",
    url=ruta_post,
    json=nuevo_estudiante
)
#print(post_response.text)