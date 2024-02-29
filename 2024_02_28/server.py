from http.server import HTTPServer, BaseHTTPRequestHandler
import json

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

    def do_DELETE(self):
        if self.path == '/estudiantes' :
            self.send_response(200)
            self.send_header('content-type','application/json')
            self.end_headers()
            estudiantes.clear()
            self.wfile.write(json.dumps(estudiantes).encode('utf-8'))
    
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"Error":"Ruta no existente"}).encode('utf-8'))
    def do_GET(self):
        if self.path.startswith("/estudiantes"):
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

    
    def do_POST(self):
        if self.path == '/estudiantes':
            content_lenght = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_lenght)
            post_data = json.loads(post_data.decode('utf-8'))
            post_data['id']= len(estudiantes) +1
            estudiantes.append(post_data)
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(estudiantes).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"Error":"Ruta no existente"}).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith("/estudiantes"):
            content_lenght = int(self.headers['Content-Length'])
            data = self.rfile.read(content_lenght)
            data = json.loads(post_data.decode('utf-8'))
            id = data["id"]
            estudiante = next((estudiante for estudiante in estudiantes if estudiante["id"]==id),
            None,)
            if estudiante:
                estudiante.update(data)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(estudiante).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"Error":"Ruta no existente"}).encode('utf-8'))

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

