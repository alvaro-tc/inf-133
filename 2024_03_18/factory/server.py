from http.server import HTTPServer, BaseHTTPRequestHandler
import json



class DeliveryService:
    @staticmethod
    def createVehicle(vehicle_type):
        delivery_factory = DeliveryFactory()
        delivery_vehicle = delivery_factory.create_delivery_vehicle(vehicle_type)
        return(delivery_vehicle)
    @staticmethod
    def deliverVehicle(delivery_vehicle):
        return delivery_vehicle.deliver()



class DeliveryVehicle:
    def __init__(self, capacity):
        self.capacity = capacity
        self.packages_delivered = 0

    def deliver(self):
        if self.packages_delivered < self.capacity:
            self.packages_delivered += 1
            return "Entrega realizada con exito"
        else:
            return "El vehículo ha alcanzado su capacidad máxima de entregas"


        




class Motorcycle(DeliveryVehicle):
    def __init__(self):
        super().__init__(capacity=10)
                         
class Drone(DeliveryVehicle):
    def __init__(self):
        super().__init__(capacity=20)

class Scout(DeliveryVehicle):
    def __init__(self):
        super().__init__(capacity=5)


class DeliveryFactory:
    def create_delivery_vehicle(self, vehicle_type):
        if vehicle_type == "motorcycle":
            return Motorcycle()
        elif vehicle_type == "drone":
            return Drone()
        elif vehicle_type == "scout":
            return Scout()
        else:
            raise ValueError("Tipo de vehículo de entrega no válido")

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

class DeliveryRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/delivery":
            request_data = HTTPResponseHandler.read_data(self)
            vehicle_type = request_data.get("vehicle_type")
            delivery_vehicle = DeliveryService.createVehicle(vehicle_type)
            response_data = {"message": delivery_vehicle.deliver()}
            HTTPResponseHandler.handle_response(self,200,response_data)

        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})




def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, DeliveryRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()