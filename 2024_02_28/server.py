from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs


estudiantes= [
    {
        "id" : 1,
        "nombre" : "Pedrito",   
        "apellido" : "Garcia",
        "carrera" : "Ingienieria de Sistemas",
    },
     {
        "id" : 2,
        "nombre" : "Alvaro",
        "apellido" : "Torrez",
        "carrera" : "Ingienieria de Sistemas",
    },
     {
        "id" : 3,
        "nombre" : "Maria",
        "apellido" : "Perez",
        "carrera" : "Arquitectura",
    },
    {
        "id" : 4,
        "nombre" : "Fabiola",
        "apellido" : "Quispe",
        "carrera" : "Arquitectura",
    },
]
class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path= urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        print(query_params)
        if parsed_path.path == "/estudiantes":
            if "nombre" in query_params and "apellido" in query_params and "carrera" in query_params:
                nombre= query_params["nombre"][0]
                apellido= query_params["apellido"][0]
                carrera= query_params["carrera"][0]
                estudiantes_filtrados=[
                    estudiante
                    for estudiante in estudiantes
                    if estudiante["nombre"]==nombre and estudiante["apellido"]==apellido and estudiante["carrera"]==carrera
                ]
                if estudiantes_filtrados != []:
                    self.response_handler(200, estudiantes_filtrados)
                else:
                    self.response_handler(204, [])
            elif "nombre" in query_params:
                nombre= query_params["nombre"][0]
                estudiantes_filtrados=[
                    estudiante
                    for estudiante in estudiantes
                    if estudiante["nombre"]==nombre
                ]
                if estudiantes_filtrados != []:
                    self.response_handler(200, estudiantes_filtrados)
                else:
                    self.response_handler(204, [])
            elif "apellido" in query_params:
                apellido= query_params["apellido"][0]
                estudiantes_filtrados=[
                    estudiante
                    for estudiante in estudiantes
                    if estudiante["apellido"]==apellido
                ]
                if estudiantes_filtrados != []:
                    self.response_handler(200, estudiantes_filtrados)
                else:
                    self.response_handler(204, [])
            elif "carrera" in query_params:
                carrera= query_params["carrera"][0]
                estudiantes_filtrados=[
                    estudiante
                    for estudiante in estudiantes
                    if estudiante["carrera"]==carrera
                ]
                if estudiantes_filtrados != []:
                    self.response_handler(200, estudiantes_filtrados)
                else:
                    self.response_handler(204, [])
            else:
                dato=self.path.split('/')[-1]
                if dato.isdigit():
                    id=dato
                    estudiante = next(
                    (estudiante for estudiante in estudiantes if estudiante["id"]==id ),
                    None,
                    )
                    if estudiante:
                        self.send_response(200)
                        self.send_header("Content-type","application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(estudiante).encode("utf-8"))
                else:
                    carrera=dato
                    estudiantes_carrera = [estudiante for estudiante in estudiantes if estudiante['carrera'] == carrera]
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(estudiantes_carrera).encode('utf-8'))
            
        
        elif self.path == '/carreras':
            carreras = list(set([estudiante['carrera'] for estudiante in estudiantes]))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(carreras).encode('utf-8'))
                    
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"Error":"Ruta no existente"}).encode('utf-8'))


    def response_handler(self,status_code,data):
        self.send_response(status_code)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


    def find_student(self,id,estudiantes):
        return next(
            (
            (estudiante for estudiante in estudiantes if estudiante["id"]==id ),
            None,
            )
        )
    def read_data(self):
        content_lenght = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_lenght)
        post_data = json.loads(post_data.decode('utf-8'))
        return post_data
    

    def do_DELETE(self):
        if self.path == '/estudiantes' :
            self.response_handler(200,estudiantes)
            estudiantes.clear()
        else:
            self.response_handler(404,{"Error":"Ruta no existente"})
 
    
    def do_POST(self):
        if self.path == '/estudiantes':
            post_data=self.read_data()
            
            post_data['id']= len(estudiantes) +1
            estudiantes.append(post_data)
            self.response_handler(201,[])

        else:
            self.response_handler(404,{"Error":"Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/estudiantes"):
            id = int(self.path.split("/")[-1])

            estudiante = self.find_student(id,estudiantes)
            data= self.read_data()
            if estudiante:
                estudiante.update(data)
                self.response_handler(200,estudiante)

        else:
            self.response_handler(404,{"Error":"Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f'Iniciando servidor web en http://localhost:{port}/')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('apagando servidor web')
        httpd.socket.close()

if __name__=="__main__":
    run_server()

