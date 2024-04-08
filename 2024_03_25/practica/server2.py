from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

personas ={}

class Persona():
    def __init__(self):
        self.nombre = None
        self.apellido = None
    
    def setPersona(self, nombre,apellido):
        self.nombre = nombre
        self.apellido = apellido
        
class PersonaService():
    def readPersonas(self):
        return {id:persona.__dict__ for id, persona in personas.items()}
    def createPersona(self,post_data):
        nombre = post_data.get("nombre",None)
        apellido = post_data.get("apellido",None)
        persona = Persona()
        persona.setPersona(nombre,apellido)
        if personas:
            new_id = max(personas.keys())+1
        else:
            new_id =1
        personas[new_id]=persona
        return persona.__dict__
    def updatePersona(self,persona_id,post_data):
        nombre = post_data.get("nombre",None)
        apellido = post_data.get("apellido",None)
        if persona_id in personas:
            persona = personas[persona_id]
            if nombre:
                persona.nombre = nombre
            if apellido:
                persona.apellido = apellido        
        
        if persona:
            return persona.__dict__
        else:
            return None
    def deletePersona(self,persona_id):
        if persona_id in personas:
            persona =personas[persona_id]
            del personas[persona_id]
            return persona
        return None
    def buscarPorApellido(self,query_params):
        if "apellido" in query_params:
            apellido = query_params["apellido"][0]
            return {id: persona.__dict__ for id, persona in personas.items() if persona.apellido==apellido}
        else:
            return None


class HTTPDataHandler():
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod 
    def handle_reader(handler):
        content_lenght = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_lenght)
        return json.loads(post_data.decode("utf-8"))

class PersonaDataHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller = PersonaService()
        super().__init__(*args,**kwargs)
        
    def do_GET(self):
        if self.path == "/personas":
            data = self.controller.readPersonas()
            HTTPDataHandler.handle_response(self,200,data)
        
        elif self.path.startswith("/personas/"):
            parsed_url= urlparse(self.path)
            query_params= parse_qs(parsed_url.query)

            response_data= self.controller.buscarPorApellido(query_params)
            if response_data:
                HTTPDataHandler.handle_response(self,200,response_data)
            else:
                HTTPDataHandler.handle_response(self,404,{"message":"Persona(s) no encontrada"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_POST(self):
        if self.path == "/personas":
            post_data = HTTPDataHandler.handle_reader(self)
            response_data= self.controller.createPersona(post_data)

            HTTPDataHandler.handle_response(self,201,response_data)
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/personas/"):
            id = int(self.path.split("/")[-1])
            post_data = HTTPDataHandler.handle_reader(self)
            response_data= self.controller.updatePersona(id,post_data)
            if response_data:
                HTTPDataHandler.handle_response(self,200,response_data)
            else:
                HTTPDataHandler.handle_response(self,404,{"message":"Persona no encontrada"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_DELETE(self):
        if self.path.startswith("/personas/"):
            id = int(self.path.split("/")[-1])
            response_data= self.controller.deletePersona(id)
            if response_data:
                HTTPDataHandler.handle_response(self,200,{"message":"Persona eliminada"})
            else:
                HTTPDataHandler.handle_response(self,404,{"message":"Persona no encontrada"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
            

def run(server_class=HTTPServer,handler_class = PersonaDataHandler, port=8000):
    server_address=("",port)
    httpd = server_class(server_address,handler_class)
    print("Iniciando server web")
    httpd.serve_forever()


if __name__=="__main__":
    run()
        
        
        
        
    