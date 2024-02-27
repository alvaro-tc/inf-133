from http.server import HTTPServer, BaseHTTPRequestHandler
import json

estudiantes= [
    {
        "id" : 1,
        "nombre" : "Pedrito",
        "apellido" : "Garcia",
        "carrera" : "Ingienieria de Sistemas",
    },
]

class RESTRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/lista_estudiantes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(estudiantes).encode('utf-8'))

        elif self.path == '/buscar_nombre':
            estudiantes_con_P = [estudiante for estudiante in estudiantes if estudiante['nombre'].startswith('P')]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(estudiantes_con_P).encode('utf-8'))

        elif self.path == '/contar_carreras':
            cantidad_por_carrera = {}
            for estudiante in estudiantes:
                carrera = estudiante['carrera']
                if carrera in cantidad_por_carrera:
                    cantidad_por_carrera[carrera] += 1
                else:
                    cantidad_por_carrera[carrera] = 1
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(cantidad_por_carrera).encode('utf-8'))
        elif self.path == '/total_estudiantes':
            total_estudiantes = len(estudiantes)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"total_estudiantes": total_estudiantes}).encode('utf-8'))


        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"Error":"Ruta no existente"}).encode('utf-8'))
    def do_POST(self):
        if self.path == '/agrega_estudiante':
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


