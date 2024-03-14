from http.server import HTTPServer, BaseHTTPRequestHandler
import json
estudiantes = [
    {
        "id": 1,
        "nombre": "Pedrito",
        "apellido": "García",
        "carrera": "Ingeniería de Sistemas",
    },
]


class EstudiantesService:
    #Un metodo estatico no interviene en los datos del objeto
    @staticmethod
    def find_student(id):
        return next(
            (estudiante for estudiante in estudiantes if estudiante["id"] == id),
            None,
        )
    @staticmethod
    def filter_students_by_name(nombre):
        return [
            estudiante for estudiante in estudiantes if estudiante["nombre"] == nombre
        ]
    @staticmethod
    def add_student(data):
        data["id"] = len(estudiantes) + 1
        estudiantes.append(data)
        return estudiantes
    @staticmethod
    def update_student(id, data):
        estudiante = EstudiantesService.find_student(id)
        if estudiante:
            estudiante.update(data)
            return estudiantes
        else:
            return None

    @staticmethod
    def delete_students():
        estudiantes.clear()
        return estudiantes

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))



class RESTRequestHandler(BaseHTTPRequestHandler):    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_GET(self):
        if self.path == "/estudiantes":
            HTTPResponseHandler.handle_response(self, 200, estudiantes)
        elif self.path.startswith("/estudiantes/"):
            id = int(self.path.split("/")[-1])
            estudiante = EstudiantesService.find_student(id)
            if estudiante:
                HTTPResponseHandler.handle_response(self, 200, [estudiante])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])

        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


    def do_POST(self):
        if self.path == "/estudiantes":
            #Esta parte debe estar ya hecha con otra clase manejadora de estudiantes
            data = self.read_data()
            EstudiantesService.add_student(data)
            HTTPResponseHandler.handle_response(self,201,estudiantes)
        else:
            HTTPResponseHandler.handle_response(self,404,{"Error": "Ruta no existente"})


    def do_PUT(self):
        if self.path.startswith("/estudiantes/"):
            id = int(self.path.split("/")[-1])
            estudiante = EstudiantesService.find_student(id)
            data = self.read_data()
            if estudiante:
                estudiante.update(data)
                HTTPResponseHandler.handle_response(self, 200, [estudiantes])
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Estudiante no encontrado"})
                
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


    def do_DELETE(self):
        if self.path == "/estudiantes":
            estudiantes = EstudiantesService.delete_students()
            HTTPResponseHandler.handle_response(self, 200, estudiantes)
        elif self.path.startswith("/estudiantes/"):
            id = int(self.path.split("/")[-1])
            estudiante = EstudiantesService.find_student(id)
            if estudiante:
                EstudiantesService.delete_students()
                ##estudiantes.remove(estudiante)
                HTTPResponseHandler.handle_response(self, 200, estudiantes)
 
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Estudiante no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()