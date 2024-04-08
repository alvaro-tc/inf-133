from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
personas = {}
class Persona():
    def __init__(self):
        self.nombre = None
        self.apellido = None
        self.edad = None
    
class PersonaBuilder():
    def __init__(self):
        self.persona = Persona()
    def setNombre(self,nombre):
        self.persona.nombre=nombre
    def setApellido(self,apellido):
        self.persona.apellido=apellido
    def setEdad(self,edad):
        self.persona.edad=edad
    def getPersona(self):
        return self.persona

class PersonaService():
    def __init__(self):
        self.builder = PersonaBuilder()
    def readPersonas(self):
        return {ci:persona.__dict__ for ci, persona in personas.items()}
    def searchPorNombre(self,query_params):
        if "nombre" in query_params:
            nombre = query_params["nombre"][0]
            return {id: persona.__dict__ for id, persona in personas.items() if persona.nombre==nombre}
        else:
            return None       
    def createPersona(self,post_data):
        ci = post_data.get("ci",None)
        nombre = post_data.get("nombre",None)
        apellido = post_data.get("apellido",None)
        edad = post_data.get("edad",None)
        self.builder.setNombre(nombre)
        self.builder.setApellido(apellido)
        self.builder.setEdad(edad)
        persona = self.builder.getPersona()
        personas[ci]=persona
        return persona.__dict__
    def updatePersona(self,persona_ci,post_data):
        ci = post_data.get("ci",None)
        nombre = post_data.get("nombre",None)
        apellido = post_data.get("apellido",None)
        edad = post_data.get("edad",None)
        
        if persona_ci in personas:
            persona = personas[persona_ci]
            if nombre:
                persona.nombre = nombre
            if apellido:
                persona.apellido = apellido
            if edad:
                persona.edad = edad
        if ci:
            personas[ci]=persona[persona_ci].pop()
        if persona:
            return persona.__dict__
        else:
            return None
        
    def deletePersona(self,persona_ci):
        if persona_ci in personas:
            persona = personas[persona_ci]
            del personas[persona_ci]
            return persona
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
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))
    
class PersonaDataHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller = PersonaService()
        super().__init__(*args,**kwargs)
    def do_GET(self):
        if self.path == "/personas":
            get_data = self.controller.readPersonas()
            HTTPDataHandler.handle_response(self,200,get_data)
        elif self.path.startswith("/personas/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            data = self.controller.searchPorNombre(query_params)
            if data:
                HTTPDataHandler.handle_response(self,200,data)
            else:
                HTTPDataHandler.handle_response(self,200,{"message":"Persona(s) no encontradas"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_POST(self):
        if self.path == "/personas":
            data = HTTPDataHandler.handle_reader(self)
            post_data = self.controller.createPersona(data)
            HTTPDataHandler.handle_response(self,201,post_data)
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    

def run(server_class=HTTPServer,handler_class = PersonaDataHandler, port=8000):
    server_address = ("",port)
    httpd = server_class(server_address,handler_class)
    print ("Inicio Server")
    httpd.serve_forever()

if __name__ =="__main__":
    run()

