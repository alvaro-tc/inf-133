import requests

url="http://localhost:8000/"

# Consulta por QUery params
ruta_filtrar_nombres = url + "estudiantes?carrera=Ingienieria de Sistemas"
filtrar_nombres_response = requests.request(method="GET", url=ruta_filtrar_nombres)
print (filtrar_nombres_response.text)

# GET Consulta a la lista estudiantes
ruta_filtrar_carreras = url + "carreras"
filtrar_carreras_response = requests.request(method="GET", url=ruta_filtrar_carreras)
print (filtrar_carreras_response.text)


ruta_filtrar_estudiantes_carrera = url + "estudiantes/Arquitectura"
filtrar_estudiantes_carrera_response = requests.request(method="GET", url=ruta_filtrar_estudiantes_carrera)
#print (filtrar_estudiantes_carrera_response.text)

#POST Agregar estudiantes de Economia

ruta_post =url +"estudiantes"
nuevo_estudiante= {
    "nombre":"Marcos",
    "apellido":"Ticona",
    "carrera":"Economia"
}
post_response= requests.request(
    method="POST",
    url=ruta_post,
    json=nuevo_estudiante
)
nuevo_estudiante2= {
    "nombre":"Carlos",
    "apellido":"Mamani",
    "carrera":"Economia"
}
#print(post_response.text)
post_response= requests.request(
    method="POST",
    url=ruta_post,
    json=nuevo_estudiante
)
#print(post_response.text)
