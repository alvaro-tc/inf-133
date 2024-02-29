from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def saludar(nombre):
    return "Hola, {}!".format(nombre)

def palindromo(texto):
    if(texto == texto[::-1]):
        return "True"
    else:
        return "False"

dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000",
    action="http://localhost:8000",
    namespace="http://localhost:8000",
    trace=True,
    ns=True,
)
dispatcher.register_function(
    "Saludar",
    saludar,
    returns={"saludo": str},
    args={"nombre": str},
)
dispatcher.register_function(
    "Palindromo",
    palindromo,
    returns={"es_palindromo": str},
    args={"texto": str},
)

server = HTTPServer(("",8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()