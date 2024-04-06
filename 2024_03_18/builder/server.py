from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class PizzaService:
    def __init__(self):
        self.builder = PizzaBuilder()
        self.pizzeria = Pizzeria(self.builder)
    @staticmethod
    def createPizza(self,data):
        tamaño = data.get('tamaño', None)
        masa = data.get('masa', None)
        toppings = data.get('toppings', [])
        builder = PizzaBuilder()
        pizzeria = Pizzeria(builder)
        pizza = pizzeria.create_pizza(tamaño, masa, toppings)
        return pizza
    @staticmethod
    def getPizza(pizza):
        response = {
                'tamaño': pizza.tamaño,
                'masa': pizza.masa,
                'toppings': pizza.toppings
        }
        return response
    
    


class Pizza:
    def __init__(self):
        self.tamaño = None
        self.masa = None
        self.toppings = []

    def __str__(self):
        return f"Tamaño: {self.tamaño}, Masa: {self.masa}, Toppings: {', '.join(self.toppings)}"



class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_tamaño(self, tamaño):
        self.pizza.tamaño = tamaño

    def set_masa(self, masa):
        self.pizza.masa = masa

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)

    def get_pizza(self):
        return self.pizza

class Pizzeria:
    def __init__(self, builder):
        self.builder = builder

    def create_pizza(self, tamaño, masa, toppings):
        self.builder.set_tamaño(tamaño)
        self.builder.set_masa(masa)
        for topping in toppings:
            self.builder.add_topping(topping)
        return self.builder.get_pizza()
    
class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data.decode("utf-8"))
        return request_data
    

class PizzaHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/pizza':
            data = HTTPResponseHandler.read_data(self)
            pizza =PizzaService.createPizza(self,data)
            response = PizzaService.getPizza(pizza)
            HTTPResponseHandler.handle_response(self,200,response)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})





def run(server_class=HTTPServer, handler_class=PizzaHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()