import requests
url = 'http://localhost:8000/graphql'
query = """
    {
        estudiantePorCarrera(carrera: "Arquitectura"){
            nombre
        }

    }
"""
query_crear = """
mutation {
        crearEstudiante(nombre: "Angel", apellido: "Gomez", carrera: "Arquitectura") {
            estudiante {
                id
                nombre
                apellido
                carrera
            }
        }
    }
"""
query_crear2 = """
mutation {
        crearEstudiante(nombre: "Michael", apellido: "Torrez", carrera: "Arquitectura") {
            estudiante {
                id
                nombre
                apellido
                carrera
            }
        }
    }
"""
query_eliminar= """
mutation {
        deleteEstudiante(id : 3) {
            estudiante {
                id
                nombre
                apellido
                carrera
            }
        }
    }
"""
query_poner= """
mutation {
        putEstudiante(id : 2, nombre: "Jose", apellido: "Lopez", carrera: "Antropologia") {
            estudiante {
                id
                nombre
                apellido
                carrera
            }
        }
    }
"""
query_get= """
    {
        estudiantes{
            id
            nombre
            carrera
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_crear})
#print(response_mutation.text)
response_mutation2 = requests.post(url, json={'query': query_crear2})
#print(response_mutation2.text)
response_mutation3 = requests.post(url, json={'query': query_poner})
#print(response_mutation3.text)
response = requests.post(url, json={'query': query_get})
print(response.text)

