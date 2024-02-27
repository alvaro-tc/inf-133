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

