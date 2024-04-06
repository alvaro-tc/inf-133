from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# CHOCOLATES diccionario
chocolates = {}


class Chocolate:
    def __init__(self, chocolate_type, peso, sabor ,relleno=None):
        self.chocolate_type = chocolate_type
        self.peso = peso
        self.sabor = sabor
        self.relleno = relleno

class Tableta(Chocolate):
    def __init__(self, peso, sabor):
        super().__init__("tableta", peso, sabor)


class Bombon(Chocolate):
    def __init__(self, peso, sabor):
        super().__init__("bombon", peso, sabor)

class Trufa(Chocolate):
    def __init__(self, peso, sabor, relleno):
        super().__init__("trufa", peso, sabor, relleno)


class ChocolateFactory:
    @staticmethod
    def create_chocolate(chocolate_type, peso, sabor,relleno):
        if chocolate_type == "tableta":
            return Tableta(peso, sabor)
        elif chocolate_type == "bombon":
            return Bombon(peso, sabor)
        elif chocolate_type == "trufa":
            return Trufa(peso, sabor, relleno)
        else:
            raise ValueError("Tipo de chocolate no válido")


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class ChocolateService:
    def __init__(self):
        self.factory = ChocolateFactory()

    def add_chocolate(self, data):
        chocolate_type = data.get("chocolate_type", None)
        peso = data.get("peso", None)
        sabor = data.get("sabor", None)
        relleno = data.get("relleno", None)

        if not(chocolate_type=="trufa") and relleno:
            return "noTrufa"
        else:
            chocolate = self.factory.create_chocolate(
            chocolate_type, peso, sabor, relleno
            )
            if not chocolates:
                chocolates[1] = chocolate
            else:
                chocolates[max(chocolates.keys()) + 1] = chocolate
            
            return chocolate


    def list_chocolates(self):
        return {index: chocolate.__dict__ for index, chocolate in chocolates.items()}

    def update_chocolate(self, chocolate_id, data):
        if chocolate_id in chocolates:
            chocolate = chocolates[chocolate_id]
            peso = data.get("peso", None)
            sabor = data.get("sabor", None)
            relleno = data.get("relleno", None)
            
            if peso:
                chocolate.peso = peso
            if sabor:
                chocolate.sabor = sabor
            
            #return chocolate
            if not(chocolate.chocolate_type=="trufa") and relleno:
                return "noTrufa"
            else:
                if relleno:
                    chocolate.relleno = relleno
                return chocolate
            
            
        else:
            return None

    def delete_chocolate(self, chocolate_id):
        if chocolate_id in chocolates:
            del chocolates[chocolate_id]
            return {"message": "Chocolate eliminado"}
        else:
            return None


class ChocolateRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.chocolate_service = ChocolateService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/chocolates":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.chocolate_service.add_chocolate(data)
            if response_data == "noTrufa":
                HTTPDataHandler.handle_response(
                self, 404, {"message": "El chocolate no es Trufa"}
            )
            else:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        if self.path == "/chocolates":
            response_data = self.chocolate_service.list_chocolates()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/chocolates/"):
            chocolate_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.chocolate_service.update_chocolate(chocolate_id, data)
            if response_data:
                if response_data == "noTrufa":
                    HTTPDataHandler.handle_response(
                    self, 404, {"message": "El chocolate no es trufa"}
                )
                else:
                    HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Chocolate no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/chocolates/"):
            chocolate_id = int(self.path.split("/")[-1])
            response_data = self.chocolate_service.delete_chocolate(chocolate_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Chocolate no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ChocolateRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()